#!/usr/bin/env python3
"""Report study pages that do not meet the course contract in content/templates/course-page.md.

Checks, per page, on both halves:
  1. the rule-5 skeleton headings: Running object / Homework diagram / Worked case
  2. a problem set with an explicit tier line
  3. Draw / Derive / (Do | Interpret) items and a Solutions callout
  4. a self-check
  5. heading parity between the two halves (a drifting Korean half is invisible to
     audit_parity.py, which only compares section *references*)

Exit status is always 0: this is a worklist, not a gate. Promote it into
verify_content.py once the tracks conform.

Scope: 02-foundations and 04-robotics study pages. Excluded by design — index/map
pages, the two lab catalogs, and the algorithms track, which the study-depth guide
keeps as an interview track rather than a course.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EXCLUDE_SUBSTR = ("/algorithms/", "lab-plants", "lab-kernel", "modern-robotics-book",
                  # 0. Overview is the Foundations map (tags: moc) — prerequisite table,
                  # study order, connection map and the cumulative gate check, with no
                  # subject of its own to derive; an index page that is not named index.md.
                  "02-foundations/overview")
PATTERNS = ("content/02-foundations/*.md", "content/04-robotics/*.md",
            "content/04-robotics/modern-robotics/*.md",
            "content/04-robotics/haptics-teleoperation/*.md",
            "content/04-robotics/ros2/*.md")

# The wiki carries two accepted styles: a `###` heading, or a bold run-in inside a
# section ("**Worked: plant P2 …**"). Both satisfy the contract; only absence does not.
RUNNING = re.compile(r"^#{3,4} .*(Running object|Running plant)|^#{3,4} .*(계속 쓰는 대상|이 페이지의 장치|이 페이지의 대상)"
                     r"|\*\*(Running plant|Running object|계속 쓰는 대상)", re.M)
PLANT_ID = re.compile(r"\*\*(P[1-6]|D[1-6])\*\*")
DIAGRAM = re.compile(r"^#{3,4} .*(Homework diagram|과제가 그릴 그림)|\*\*(Homework diagram|과제가 그릴 그림)", re.M)
WORKED = re.compile(r"^#{3,4} .*(Worked case|Worked on|장치로 한 번 끝까지|대상으로 한 번 끝까지)"
                    r"|\*\*(Worked|계산:|장치로 한 번 끝까지|대상으로 한 번 끝까지)", re.M)
PROBLEM = re.compile(r"^#{3,4} .*(Problem set|과제)", re.M)
TIER = re.compile(r"\bTier [ABC]\b")
SELFCHECK = re.compile(r"^#{3,4} .*(Self-check|스스로 점검)", re.M)
HEADING = re.compile(r"^#{3,4} ", re.M)


def halves(text):
    if "## 한국어" not in text:
        return None, None
    en, ko = text.split("## 한국어", 1)
    return en.split("## English", 1)[-1], ko


def audit(path):
    text = open(path, encoding="utf-8").read()
    en, ko = halves(text)
    if en is None:
        return ["single-language page"]
    problems = []
    for half, t in (("EN", en), ("KO", ko)):
        if not RUNNING.search(t) and not PLANT_ID.search(t):
            problems.append(f"names no running object ({half})")
    for name, rx in (("homework diagram", DIAGRAM),
                     ("worked case", WORKED), ("problem set", PROBLEM),
                     ("self-check", SELFCHECK)):
        missing = [half for half, t in (("EN", en), ("KO", ko)) if not rx.search(t)]
        if missing:
            problems.append(f"no {name} ({'+'.join(missing)})")
    ps = PROBLEM.split(en)
    if len(ps) > 1 and not TIER.search(ps[-1]):
        problems.append("problem set has no tier line")
    tail = ps[-1] if len(ps) > 1 else ""
    if tail:
        for item in ("Draw", "Derive"):
            if f"**{item}" not in tail:
                problems.append(f"problem set has no {item} item")
        if "**Do" not in tail and "**Interpret" not in tail and "**Run" not in tail:
            problems.append("problem set has no Do/Interpret item")
        if "Solutions" not in tail:
            problems.append("problem set has no solutions")
    nh_en, nh_ko = len(HEADING.findall(en)), len(HEADING.findall(ko))
    if nh_en != nh_ko:
        problems.append(f"heading counts differ: EN {nh_en} vs KO {nh_ko}")
    return problems


def main():
    rows = []
    for pattern in PATTERNS:
        for path in sorted(glob.glob(pattern)):
            rel = os.path.relpath(path, "content").replace(os.sep, "/")
            if os.path.basename(path) == "index.md" or any(s in "/" + rel for s in EXCLUDE_SUBSTR):
                continue
            problems = audit(path)
            if problems:
                rows.append((rel, problems))
    for rel, problems in rows:
        print(f"{rel}\n    " + "\n    ".join(problems))
    total = len(glob.glob("content/02-foundations/*.md")) + len(glob.glob("content/04-robotics/**/*.md", recursive=True))
    print(f"\n{len(rows)} page(s) below the course contract "
          f"(of {total} pages scanned, index/catalog/algorithms pages excluded).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
