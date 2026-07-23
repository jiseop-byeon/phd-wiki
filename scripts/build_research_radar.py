#!/usr/bin/env python3
"""Fetch DBLP proceedings and rebuild the static Research Radar dataset.

The pipeline deliberately uses only venue-whitelisted proceedings metadata.
It does not query arXiv and does not require a personal API key.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get("RADAR_CACHE", "/private/tmp/research-radar-dblp"))
YEARS = range(2021, 2026)
VENUES = ("nips", "icml", "iclr", "cvpr", "icra", "corl")
BASE_URL = "https://dblp.org/db/conf/{venue}/{venue}{year}.xml"


def fetch(url: str, destination: Path) -> str:
    if destination.exists() and destination.stat().st_size >= 1_000:
        return "cached"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Physical-AI-Notes-Research-Radar/1.0 "
                "(venue-level bibliographic research; contact via repository)"
            )
        },
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read()
            if len(payload) < 1_000:
                raise ValueError(f"unexpectedly small response ({len(payload)} bytes)")
            destination.write_bytes(payload)
            return "downloaded"
        except HTTPError as exc:
            if exc.code == 404:
                return "not published/indexed"
            if exc.code != 429 and 500 > exc.code:
                raise
            retry_after = float(exc.headers.get("Retry-After", 2 ** attempt))
        except (URLError, TimeoutError, ValueError):
            retry_after = 2 ** attempt
        if attempt == 4:
            return "failed after retries"
        time.sleep(min(retry_after, 30))
    return "failed"


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    for venue in VENUES:
        for year in YEARS:
            destination = CACHE / f"{venue}-{year}.xml"
            result = fetch(BASE_URL.format(venue=venue, year=year), destination)
            print(f"{venue.upper()} {year}: {result}")
            # DBLP asks automated clients to remain polite. Cached runs do not wait.
            if result == "downloaded":
                time.sleep(2)

    env = {**os.environ, "RADAR_CACHE": str(CACHE)}
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/compile_research_radar.py")],
        check=True,
        env=env,
    )


if __name__ == "__main__":
    main()
