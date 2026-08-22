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
import json
import urllib.parse
import urllib.request
from pathlib import Path
from http.client import HTTPException
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get("RADAR_CACHE", "/private/tmp/research-radar-dblp"))
YEARS = range(2021, 2026)
VENUES = ("nips", "icml", "iclr", "cvpr", "icra", "corl", "iros", "rss")
BASE_URL = "https://dblp.org/db/conf/{venue}/{slug}{year}.xml"
# DBLP keeps NeurIPS under conf/nips/ but renamed the per-year files to "neurips".
DBLP_SLUG = {"nips": "neurips"}
JOURNALS = {
    "automation-in-construction": {
        "issn": "0926-5805",
        "name": "Automation in Construction",
    },
    "construction-robotics": {
        "issn": "2509-8780",
        "name": "Construction Robotics",
    },
    "ieee-ral": {
        "issn": "2377-3766",
        "name": "IEEE Robotics and Automation Letters",
    },
    "ieee-tro": {
        "issn": "1552-3098",
        "name": "IEEE Transactions on Robotics",
    },
}


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
        except (URLError, TimeoutError, ValueError, ConnectionError, HTTPException):
            retry_after = 2 ** attempt
        if attempt == 4:
            return "failed after retries"
        time.sleep(min(retry_after, 30))
    return "failed"


def fetch_crossref(slug: str, issn: str, name: str) -> str:
    destination = CACHE / f"crossref-{slug}.json"
    if destination.exists() and destination.stat().st_size >= 1_000:
        return "cached"

    items: list[dict] = []
    offset = 0
    total = None
    while True:
        params = urllib.parse.urlencode(
            {
                "filter": "from-pub-date:2021-01-01,until-pub-date:2025-12-31,type:journal-article",
                "rows": 1000,
                "offset": offset,
                "select": "DOI,title,author,published,container-title,type",
            }
        )
        url = f"https://api.crossref.org/journals/{issn}/works?{params}"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Physical-AI-Notes-Research-Radar/1.0"},
        )
        for attempt in range(5):
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    message = json.load(response)["message"]
                break
            except (HTTPError, URLError, TimeoutError, ValueError, KeyError,
                    ConnectionError, HTTPException):
                if attempt == 4:
                    return "failed after retries"
                time.sleep(min(2 ** attempt, 30))
        batch = message.get("items", [])
        items.extend(batch)
        total = int(message.get("total-results", len(items)))
        offset += len(batch)
        if not batch or offset >= total:
            break
        time.sleep(1)

    destination.write_text(
        json.dumps(
            {"source": "Crossref", "journal": name, "issn": issn, "items": items},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return f"downloaded {len(items)} records"


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    for venue in VENUES:
        for year in YEARS:
            destination = CACHE / f"{venue}-{year}.xml"
            slug = DBLP_SLUG.get(venue, venue)
            result = fetch(BASE_URL.format(venue=venue, slug=slug, year=year), destination)
            print(f"{venue.upper()} {year}: {result}")
            # DBLP asks automated clients to remain polite. Cached runs do not wait.
            if result == "downloaded":
                time.sleep(2)
    for slug, journal in JOURNALS.items():
        result = fetch_crossref(slug, journal["issn"], journal["name"])
        print(f"{journal['name']}: {result}")

    env = {**os.environ, "RADAR_CACHE": str(CACHE)}
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/compile_research_radar.py")],
        check=True,
        env=env,
    )


if __name__ == "__main__":
    main()
