"""Download Kaggle's ARC-AGI-2 leaderboard when credentials are available."""

from __future__ import annotations

import argparse
import csv
import io
import os
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from common import RAW, PROCESSED, ensure_dirs, fetch_bytes, number, timestamp, write_json


COMPETITION = "arc-prize-2026-arc-agi-2"
API_URL = f"https://www.kaggle.com/api/v1/competitions/{COMPETITION}/leaderboard/download"


def parse_csv_bytes(body: bytes, source: str) -> list[dict[str, Any]]:
    if body[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            csv_names = [name for name in archive.namelist() if name.lower().endswith((".csv", ".tsv"))]
            if not csv_names:
                return []
            body = archive.read(csv_names[0])
    text = body.decode("utf-8-sig", errors="replace")
    dialect = csv.excel_tab if "\t" in text.splitlines()[0] else csv.excel
    rows = list(csv.DictReader(io.StringIO(text), dialect=dialect))
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append({
            "source": "kaggle",
            "verification_status": "kaggle_leaderboard",
            "competition": COMPETITION,
            "rank": number(row.get("rank") or row.get("Rank")),
            "team": row.get("team") or row.get("Team") or row.get("teamName") or row.get("TeamName"),
            "submission": row.get("submission") or row.get("Submission") or row.get("description") or row.get("Description"),
            "score": number(row.get("score") or row.get("Score") or row.get("publicScore") or row.get("PrivateScore")),
            "raw": row,
            "retrieved_at": timestamp(),
        })
    return normalized


def download_with_cli(output_dir: Path) -> bytes:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["kaggle", "competitions", "leaderboard", COMPETITION, "--download", "--path", str(output_dir), "--quiet"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "kaggle CLI failed")
    candidates = sorted(output_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise RuntimeError("kaggle CLI returned no leaderboard file")
    return candidates[0].read_bytes()


def download_with_api() -> bytes:
    username = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")
    if not username or not key:
        raise RuntimeError("Set KAGGLE_USERNAME and KAGGLE_KEY, or install/configure kaggle CLI")
    import base64
    token = base64.b64encode(f"{username}:{key}".encode()).decode()
    return fetch_bytes(API_URL, headers={"Authorization": f"Basic {token}"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, help="use an already downloaded CSV/TSV/ZIP")
    parser.add_argument("--method", choices=["auto", "cli", "api"], default="auto")
    args = parser.parse_args()
    ensure_dirs()
    raw_dir = RAW / "kaggle"
    raw_dir.mkdir(parents=True, exist_ok=True)

    if args.csv:
        body = args.csv.read_bytes()
        source = str(args.csv)
    else:
        attempts = []
        body = None
        source = ""
        if args.method in {"auto", "cli"}:
            try:
                body = download_with_cli(raw_dir)
                source = "kaggle-cli"
            except Exception as exc:
                attempts.append(f"cli: {exc}")
                if args.method == "cli":
                    raise
        if body is None:
            try:
                body = download_with_api()
                source = API_URL
            except Exception as exc:
                attempts.append(f"api: {exc}")
                raise RuntimeError("Kaggle download failed:\n" + "\n".join(attempts))

    raw_path = raw_dir / "leaderboard.bin"
    raw_path.write_bytes(body)
    records = parse_csv_bytes(body, source)
    write_json(PROCESSED / "kaggle_records.json", {
        "source_url": "https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard",
        "retrieved_at": timestamp(),
        "records": records,
        "note": "Kaggle rows are submissions/teams; model matching is only heuristic when description contains a target model name.",
    })
    print(f"Kaggle records: {len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

