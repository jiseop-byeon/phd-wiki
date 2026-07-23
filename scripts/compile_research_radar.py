#!/usr/bin/env python3
"""Compile the Research Radar JSON from cached DBLP proceedings pages."""

from __future__ import annotations

import html
import json
import os
import re
import statistics
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(os.environ.get("RADAR_CACHE", "/private/tmp/research-radar-dblp"))
OUT = ROOT / "quartz/static/research-radar/data.json"
YEARS = [2021, 2022, 2023, 2024, 2025]
VENUES = {"nips": "NeurIPS", "icml": "ICML", "iclr": "ICLR",
          "cvpr": "CVPR", "icra": "ICRA", "corl": "CoRL"}
JOURNALS = {
    "automation-in-construction": {
        "name": "Automation in Construction",
        "issn": "0926-5805",
    },
    "construction-robotics": {
        "name": "Construction Robotics",
        "issn": "2509-8780",
    },
}

TOPICS = json.loads((ROOT / "scripts/research_radar_taxonomy.json").read_text(encoding="utf-8"))

CONSTRUCTION_DOMAIN = [
    r"construction (site|industry|project|task|process|robot|automat)", r"\bjobsite\b",
    r"\bexcavat", r"\bearthmov", r"\bexcavator", r"wheel loader", r"\bbulldozer",
    r"tower crane", r"\bmasonry\b", r"\bbricklay", r"\brebar\b", r"\bconcrete\b",
    r"\bdrywall\b", r"building information model", r"\bBIM\b", r"scan.to.bim",
    r"\bas.built\b", r"construction worker", r"built environment",
]
INFRASTRUCTURE_DOMAIN = [r"\bbridge\b", r"\btunnel\b", r"\bpavement\b", r"\bbuilding\b", r"civil infrastructure"]
FIELD_TASK = [r"inspect", r"damage", r"defect", r"maintenance", r"repair", r"progress monitor", r"\bconstruction\b", r"as.built"]
PHYSICAL_TECH = [
    r"\brobot", r"\bautonom", r"\bautomation\b", r"\bmanipulat", r"\bplanning\b",
    r"\bcontrol\b", r"reinforcement learning", r"imitation learning", r"computer vision",
    r"semantic segmentation", r"instance segmentation", r"image segmentation", r"crack segmentation",
    r"(crack|damage|defect|object|equipment|worker|hazard).{0,20}detect", r"\bSLAM\b",
    r"locali[sz]", r"3d mapping", r"point cloud mapping", r"digital twin", r"\bUAV\b",
    r"\bdrone\b", r"\bnavigation\b", r"point cloud", r"3d reconstruction",
    r"teleoperat", r"human.robot", r"\bexoskeleton",
]
EMBODIED_TECH = [
    r"\brobot", r"\bautonom", r"\bmanipulat", r"\bnavigation\b",
    r"\bUAV\b", r"\bdrone\b", r"teleoperat", r"\bexoskeleton",
]
PERCEPTION_TECH = [
    r"computer vision", r"semantic segmentation", r"instance segmentation",
    r"image segmentation", r"crack segmentation",
    r"(crack|damage|defect|object|equipment|worker|hazard).{0,20}detect",
    r"\bSLAM\b", r"locali[sz]", r"3d mapping", r"point cloud mapping", r"\bscan",
    r"point cloud", r"3d reconstruction", r"photogrammetr", r"\bvisual\b", r"vision.based",
]
NON_PHYSICAL = [
    r"risk (prediction|management|assessment)", r"cost (prediction|estimation)",
    r"schedule (prediction|optimization)", r"contract management", r"real estate",
    r"energy consumption", r"occupant behavior", r"supply chain",
    r"cause of delay", r"\bscientometric", r"\bbibliometric", r"special issue",
]
GENERIC_CONSTRUCTION_PHRASES = [
    r"model construction", r"construction and analysis", r"dataset construction",
    r"communication infrastructure building",
]
EARTHMOVING = [r"\bexcavat", r"\bearthmov", r"\bexcavator", r"wheel loader", r"\bbulldozer", r"material loading", r"soil loading"]
ASSEMBLY = [r"\bassembly\b", r"\bfabricat", r"\bmasonry\b", r"\bbrick", r"\brebar\b", r"\btimber\b", r"\bdrywall\b", r"concrete print", r"additive manufactur"]
PERCEPTION = [r"\bperception\b", r"computer vision", r"\bsegment", r"\bdetect", r"\binspect", r"progress monitor", r"point cloud", r"\bscan", r"\bSLAM\b", r"locali[sz]", r"3d reconstruction"]
TWIN = [r"digital twin", r"\bBIM\b", r"building information model", r"scan.to.bim", r"\bas.built\b"]
HRC_SAFETY = [r"human.robot", r"construction worker", r"shared autonomy", r"\bsafety\b", r"\bergonomic", r"\bexoskeleton"]


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip().rstrip(".")


def parse(path: Path, venue: str, year: int) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    records = []
    for block in re.findall(r"<(?:inproceedings|article)\b.*?</(?:inproceedings|article)>", raw, re.S):
        title_match = re.search(r"<title[^>]*>(.*?)</title>", block, re.S)
        if not title_match:
            continue
        title = clean(title_match.group(1))
        if not title:
            continue
        ee = re.search(r"<ee[^>]*>(.*?)</ee>", block, re.S)
        # DBLP appends four-digit homonym identifiers to some display names.
        authors = [
            re.sub(r"\s+\d{4}$", "", clean(x))
            for x in re.findall(r"<author[^>]*>(.*?)</author>", block, re.S)
        ]
        url = clean(ee.group(1)) if ee else ""
        if url.startswith("http://"):
            url = "https://" + url.removeprefix("http://")
        records.append({"title": title, "venue": venue, "year": year,
                        "url": url, "authors": authors[:8]})
    return list({r["title"].lower(): r for r in records}.values())


def parse_crossref(path: Path, venue: str) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = []
    excluded = re.compile(r"^(editorial board|front matter|contents|erratum|corrigendum|retraction|publisher correction)", re.I)
    for item in payload.get("items", []):
        titles = item.get("title") or []
        title = clean(titles[0]) if titles else ""
        parts = ((item.get("published") or {}).get("date-parts") or [[]])[0]
        year = int(parts[0]) if parts and str(parts[0]).isdigit() else 0
        if not title or year not in YEARS or excluded.search(title):
            continue
        authors = []
        for author in item.get("author") or []:
            name = " ".join(x for x in (author.get("given", ""), author.get("family", "")) if x).strip()
            if name:
                authors.append(name)
        doi = item.get("DOI", "")
        records.append(
            {
                "title": title,
                "venue": venue,
                "year": year,
                "url": f"https://doi.org/{doi}" if doi else "",
                "authors": authors[:8],
            }
        )
    return list({r["title"].lower(): r for r in records}.values())


def any_match(patterns: list[str], title: str) -> bool:
    return any(re.search(pattern, title, re.I) for pattern in patterns)


def construction_flags(title: str, venue: str) -> dict[str, bool]:
    primary_domain = any_match(CONSTRUCTION_DOMAIN, title)
    infrastructure_domain = any_match(INFRASTRUCTURE_DOMAIN, title)
    field_task = any_match(FIELD_TASK, title)
    physical_tech = any_match(PHYSICAL_TECH, title)
    embodied = any_match(EMBODIED_TECH, title)
    perception = any_match(PERCEPTION_TECH, title)
    non_physical = any_match(NON_PHYSICAL, title)
    generic_phrase = any_match(GENERIC_CONSTRUCTION_PHRASES, title)
    if venue == "Construction Robotics":
        parent = not non_physical and (
            embodied
            or perception
            or any_match(TWIN + EARTHMOVING + ASSEMBLY + HRC_SAFETY, title)
            or any_match([r"3d print", r"digital manufactur", r"robotic"], title)
        )
    elif venue == "Automation in Construction":
        # The venue supplies the construction-domain prior, but management-only work
        # still needs to be excluded. Embodied systems, field perception, and closed-loop
        # digital workflows remain in scope.
        parent = not non_physical and (
            embodied
            or perception
            or (any_match(TWIN, title) and any_match([r"\bscan", r"\brobot", r"\bautomation", r"closed.loop"], title))
            or (any_match(ASSEMBLY, title) and any_match([r"\brobot", r"\bautomation", r"3d print", r"additive manufactur"], title))
        )
    else:
        parent = not generic_phrase and (
            (primary_domain and physical_tech)
            or (infrastructure_domain and field_task and physical_tech)
        )
    return {
        "construction": parent,
        "construction_earthmoving": parent and any_match(EARTHMOVING, title),
        "construction_assembly": parent and any_match(ASSEMBLY, title),
        "construction_perception": parent and any_match(PERCEPTION, title),
        "construction_twin": parent and any_match(TWIN, title),
        "construction_hrc": parent and any_match(HRC_SAFETY, title),
    }


def matches_topic(key: str, paper: dict, patterns: list[re.Pattern]) -> bool:
    if key.startswith("construction"):
        return construction_flags(paper["title"], paper["venue"]).get(key, False)
    return any(pattern.search(paper["title"]) for pattern in patterns)


def slope(values: list[float]) -> float:
    xs = range(len(values))
    mx, my = statistics.mean(xs), statistics.mean(values)
    denom = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, values)) / denom if denom else 0


def main() -> None:
    papers, audit = [], []
    for slug, venue in VENUES.items():
        for year in YEARS:
            path = CACHE / f"{slug}-{year}.xml"
            if not path.exists() or path.stat().st_size < 1000:
                audit.append({"venue": venue, "year": year, "status": "missing"})
                continue
            rows = parse(path, venue, year)
            papers.extend(rows)
            audit.append({"venue": venue, "year": year, "status": "ok", "papers": len(rows),
                          "source": f"https://dblp.org/db/conf/{slug}/"})
    for slug, journal in JOURNALS.items():
        venue = journal["name"]
        path = CACHE / f"crossref-{slug}.json"
        if not path.exists() or path.stat().st_size < 1_000:
            for year in YEARS:
                audit.append({"venue": venue, "year": year, "status": "missing"})
            continue
        rows = parse_crossref(path, venue)
        papers.extend(rows)
        for year in YEARS:
            count = sum(row["year"] == year for row in rows)
            audit.append(
                {
                    "venue": venue,
                    "year": year,
                    "status": "ok",
                    "papers": count,
                    "source": f"https://api.crossref.org/journals/{journal['issn']}/works",
                }
            )

    totals = defaultdict(int)
    for paper in papers:
        totals[paper["year"]] += 1

    topics = []
    for topic in TOPICS:
        key = topic["id"]
        label = topic["label"]
        category = topic["category"]
        scopes = topic["scopes"]
        aliases = topic["aliases"]
        patterns = [re.compile(x, re.I) for x in aliases]
        matched = [p for p in papers if matches_topic(key, p, patterns)]
        counts = [sum(p["year"] == y for p in matched) for y in YEARS]
        shares = [1000 * c / totals[y] if totals[y] else 0 for y, c in zip(YEARS, counts)]
        momentum = slope(shares)
        baseline = statistics.mean(shares[:-1])
        spread = statistics.pstdev(shares[:-1]) if len(set(shares[:-1])) > 1 else 0
        burst = (shares[-1] - baseline) / max(spread, 0.2)
        recent = sum(counts[-2:])
        recent_venues = sorted({p["venue"] for p in matched if p["year"] >= 2024})
        support = sum(counts)
        shrink = support / (support + 12)
        score = (momentum * 18 + max(0, burst) * 2.5 + len(recent_venues) * 1.5) * shrink
        confidence = "High" if support >= 30 and len(recent_venues) >= 3 else "Medium" if support >= 10 else "Early"
        if score >= 18 and recent >= 12 and momentum > 0:
            status = "Fast Rising"
        elif recent >= 60:
            status = "Established"
        elif score >= 5 and support >= 6 and momentum > 0:
            status = "Emerging"
        elif momentum < -0.5 and shares[-1] < max(shares) * 0.7 and support >= 15:
            status = "Cooling"
        else:
            status = "Stable"
        representatives = sorted(matched, key=lambda p: (p["year"], p["venue"]), reverse=True)[:6]
        topics.append({
            "id": key, "label": label, "category": category, "scopes": scopes,
            "counts": counts, "shares": [round(v, 3) for v in shares],
            "recentVolume": recent, "momentum": round(momentum, 3),
            "burst": round(burst, 2), "breadth": len(recent_venues),
            "venues": recent_venues, "support": support, "confidence": confidence,
            "status": status, "trendScore": round(score, 1),
            "aliases": aliases, "papers": representatives,
        })

    payload = {
        "schemaVersion": 1, "generated": date.today().isoformat(),
        "method": "Published proceedings indexed by DBLP plus peer-reviewed construction journals from Crossref; title-based multi-label taxonomy; arXiv excluded.",
        "years": YEARS, "venues": [*VENUES.values(), *(j["name"] for j in JOURNALS.values())], "paperCount": len(papers),
        "yearTotals": {str(y): totals[y] for y in YEARS},
        "scopes": list(dict.fromkeys(scope for topic in TOPICS for scope in topic["scopes"])),
        "topics": topics, "audit": audit,
    }
    if not papers:
        raise SystemExit(
            f"Refusing to overwrite {OUT}: 0 papers parsed. "
            f"The DBLP/Crossref cache at {CACHE} is missing or empty — "
            f"run scripts/build_research_radar.py to fetch it first."
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}: {len(papers)} papers, {len(topics)} topics")


if __name__ == "__main__":
    main()
