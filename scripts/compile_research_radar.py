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

TOPICS = [
    ("foundation_models", "Foundation Models", "Deep Learning", "Literacy",
     [r"foundation model", r"large language model", r"\bllm\b", r"scaling law"]),
    ("self_supervised", "Self-Supervised Learning", "Deep Learning", "Literacy",
     [r"self.supervised", r"masked autoencoder", r"contrastive learning"]),
    ("efficient_adaptation", "Efficient Adaptation", "Deep Learning", "Working",
     [r"parameter.efficient", r"low.rank adaptation", r"\blora\b", r"prompt tuning"]),
    ("diffusion", "Diffusion Models", "Generative Models", "Working",
     [r"diffusion", r"score.based", r"denoising"]),
    ("flow_matching", "Flow Matching", "Generative Models", "Working",
     [r"flow matching", r"rectified flow"]),
    ("world_models", "World Models", "Physical AI", "Working",
     [r"world model", r"latent dynamics", r"video prediction"]),
    ("vision_language", "Vision-Language Models", "Physical AI", "Literacy",
     [r"vision.language", r"visual.language", r"image.text", r"multimodal language"]),
    ("vla", "Vision-Language-Action", "Physical AI", "Working",
     [r"vision.language.action", r"\bvla\b", r"generalist robot"]),
    ("imitation", "Imitation & Behavior Cloning", "Robot Learning", "Working",
     [r"imitation learning", r"behavior cloning", r"behaviour cloning", r"learning from demonstration"]),
    ("offline_rl", "Offline Reinforcement Learning", "Robot Learning", "Working",
     [r"offline reinforcement", r"offline rl"]),
    ("sim_to_real", "Sim-to-Real", "Robot Learning", "Working",
     [r"sim.to.real", r"simulation.to.real", r"reality gap", r"domain randomization"]),
    ("action_chunking", "Action Chunking", "Robot Learning", "Working",
     [r"action chunk", r"temporal action"]),
    ("robot_manipulation", "Robot Manipulation", "Physical AI", "Working",
     [r"robotic manipulation", r"robot manipulation", r"grasp", r"dexterous", r"bimanual"]),
    ("tactile", "Tactile & Contact Learning", "Physical AI", "Working",
     [r"tactile", r"contact.rich", r"force control", r"visuotactile"]),
    ("3d_geometry", "3D Geometry & Reconstruction", "Computer Vision", "Working",
     [r"3d reconstruction", r"novel view", r"neural radiance", r"gaussian splat", r"structure.from.motion"]),
    ("depth", "Depth Estimation", "Computer Vision", "Literacy",
     [r"depth estimation", r"monocular depth", r"stereo depth"]),
    ("point_clouds", "Point Clouds & LiDAR", "Computer Vision", "Working",
     [r"point cloud", r"\blidar\b", r"3d point"]),
    ("slam", "SLAM & Localization", "Robotics", "Working",
     [r"\bslam\b", r"visual odometry", r"locali[sz]ation"]),
    ("motion_planning", "Motion & Task Planning", "Robotics", "Working",
     [r"motion planning", r"task and motion", r"trajectory optimization", r"path planning"]),
    ("human_robot", "Human-Robot Collaboration", "Robotics", "Working",
     [r"human.robot", r"shared autonomy", r"human aware", r"collaborative robot"]),
    ("legged", "Legged & Humanoid Robotics", "Physical AI", "Literacy",
     [r"legged", r"quadruped", r"humanoid", r"biped"]),
    ("construction", "Construction Robotics", "Construction Physical AI", "Working",
     [r"construction robot", r"autonomous excavat", r"robotic excavat", r"earthmov", r"construction site"]),
]


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

    totals = defaultdict(int)
    for paper in papers:
        totals[paper["year"]] += 1

    topics = []
    for key, label, group, depth, aliases in TOPICS:
        patterns = [re.compile(x, re.I) for x in aliases]
        matched = [p for p in papers if any(pattern.search(p["title"]) for pattern in patterns)]
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
        elif score >= 5 and support >= 6 and momentum > 0:
            status = "Emerging"
        elif recent >= 60:
            status = "Established"
        elif momentum < -0.5 and shares[-1] < max(shares) * 0.7 and support >= 15:
            status = "Cooling"
        else:
            status = "Stable"
        representatives = sorted(matched, key=lambda p: (p["year"], p["venue"]), reverse=True)[:6]
        topics.append({
            "id": key, "label": label, "group": group, "depth": depth,
            "counts": counts, "shares": [round(v, 3) for v in shares],
            "recentVolume": recent, "momentum": round(momentum, 3),
            "burst": round(burst, 2), "breadth": len(recent_venues),
            "venues": recent_venues, "support": support, "confidence": confidence,
            "status": status, "trendScore": round(score, 1),
            "aliases": aliases, "papers": representatives,
        })

    payload = {
        "schemaVersion": 1, "generated": date.today().isoformat(),
        "method": "Published proceedings indexed by DBLP; title-based multi-label taxonomy; arXiv excluded.",
        "years": YEARS, "venues": list(VENUES.values()), "paperCount": len(papers),
        "yearTotals": {str(y): totals[y] for y in YEARS},
        "topics": topics, "audit": audit,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}: {len(papers)} papers, {len(topics)} topics")


if __name__ == "__main__":
    main()
