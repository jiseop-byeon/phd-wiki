#!/usr/bin/env python3
"""Content QA gate for the Physical AI Notes wiki.

Checks (run before every deploy):
  1. No wikilink spans a line break (breaks Quartz parsing silently).
  2. No wikilink inside a markdown heading (breaks parsing).
  3. Table-cell wikilinks with labels use escaped pipes (\\|).
  4. Every wikilink target resolves to an existing content file.
  5. Every checked [x] canonical-list paper entry carries a depth marker (star/half/circle).
  6. Every paper note has ## English, ## 한국어, and an after-reading checklist.
  7. Every paper note frontmatter has status: and last_verified:.
  8. New robotics-literacy and research-practice pages keep the bilingual learning scaffold.
Exit code 1 on any failure, with a per-file report.
"""

import os
import re
import sys

CONTENT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")
errors = []


def err(path, msg):
    errors.append(f"{os.path.relpath(path, CONTENT)}: {msg}")


md_files = []
for root, _dirs, files in os.walk(CONTENT):
    for f in files:
        if f.endswith(".md"):
            md_files.append(os.path.join(root, f))

# Map of resolvable link targets (path without extension, relative to content/)
targets = set()
for p in md_files:
    rel = os.path.relpath(p, CONTENT)[:-3]
    targets.add(rel)
    targets.add(os.path.basename(rel))  # Obsidian shortest-path links

WIKILINK = re.compile(r"\[\[([^\[\]]+?)\]\]")

for p in md_files:
    text = open(p, encoding="utf-8").read()
    lines = text.split("\n")

    # 1. line-spanning wikilinks: an unclosed [[ on a line
    for i, line in enumerate(lines, 1):
        stripped = WIKILINK.sub("", line)
        if "[[" in stripped:
            err(p, f"line {i}: wikilink opens but does not close on the same line")

    # 2. wikilinks inside headings
    for i, line in enumerate(lines, 1):
        if line.startswith("#") and "[[" in line:
            err(p, f"line {i}: wikilink inside a heading")

    # 3. unescaped pipe in table-cell wikilink labels
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("|"):
            for m in WIKILINK.finditer(line):
                if "|" in m.group(1) and "\\|" not in m.group(0):
                    err(p, f"line {i}: table-cell wikilink needs an escaped pipe (\\|)")

    # 4. link targets resolve (skip templates/ — placeholder links by design)
    if os.sep + "templates" + os.sep not in p:
        file_dir = os.path.relpath(os.path.dirname(p), CONTENT)
        for m in WIKILINK.finditer(text):
            target = m.group(1).split("|")[0].split("#")[0].strip().rstrip("\\")
            if not target:
                continue
            candidates = {target, os.path.normpath(os.path.join(file_dir, target))}
            if not candidates & targets:
                err(p, f"broken wikilink target: {target}")

# 5. canonical list depth markers on completed entries; star notes need a claim box
canonical = os.path.join(CONTENT, "01-canonical-papers", "canonical-list.md")
star_targets = []
if os.path.exists(canonical):
    for i, line in enumerate(open(canonical, encoding="utf-8"), 1):
        if line.startswith("- [x]") and not any(s in line for s in ("★", "◐", "○")):
            err(canonical, f"line {i}: completed entry missing depth marker")
        if line.startswith("- [x] ★"):
            m = WIKILINK.search(line)
            if m:
                star_targets.append(m.group(1).split("|")[0].strip().rstrip("\\"))
for target in star_targets:
    p = os.path.join(CONTENT, "01-canonical-papers", target + ".md")
    if os.path.exists(p):
        text = open(p, encoding="utf-8").read()
        if "핵심 주장 읽는 법" not in text and "Reading the claim" not in text:
            err(p, "★ note missing a Reading-the-claim box")

# 6-7. note structure and frontmatter
notes_dir = os.path.join(CONTENT, "01-canonical-papers", "notes")
for root, _dirs, files in os.walk(notes_dir):
    for f in files:
        if not f.endswith(".md") or f == "index.md":
            continue
        p = os.path.join(root, f)
        text = open(p, encoding="utf-8").read()
        if "## English" not in text:
            err(p, "missing ## English section")
        if "## 한국어" not in text:
            err(p, "missing ## 한국어 section")
        if "읽고 나면" not in text:
            err(p, "missing after-reading checklist")
        if not re.search(r"^status:", text, re.M):
            err(p, "frontmatter missing status:")
        if not re.search(r"^last_verified:", text, re.M):
            err(p, "frontmatter missing last_verified:")

# 8. Curriculum pages added beyond the paper-note collection
curriculum_pages = [
    "04-robotics/state-estimation-slam.md",
    "04-robotics/planning-decision-making.md",
    "04-robotics/contact-force-tactile.md",
    "04-robotics/robot-systems-deployment.md",
    "04-robotics/hri-safety.md",
    "06-research-practice/research-questions-claims.md",
    "06-research-practice/experimental-design-reproducibility.md",
    "06-research-practice/failure-analysis-system-evaluation.md",
    "06-research-practice/scientific-writing-peer-review.md",
]
for rel in curriculum_pages:
    p = os.path.join(CONTENT, rel)
    if not os.path.exists(p):
        err(p, "required curriculum page is missing")
        continue
    text = open(p, encoding="utf-8").read()
    if "## English" not in text:
        err(p, "missing ## English section")
    if "## 한국어" not in text:
        err(p, "missing ## 한국어 section")
    if "### After reading" not in text:
        err(p, "missing after-reading checklist")
    if "### Self-check" not in text:
        err(p, "missing self-check")

if errors:
    print(f"CONTENT CHECK FAILED — {len(errors)} problem(s):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"Content check passed: {len(md_files)} files, {len(errors)} problems.")
