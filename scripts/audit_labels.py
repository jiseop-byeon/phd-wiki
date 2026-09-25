#!/usr/bin/env python3
"""List the pages where a catalog label is used with no gloss at its first use.

The wiki reuses a few frozen worked examples under short labels:

  P1-P6  the lab plants of content/02-foundations/lab-plants.md (0.6)
  D1-D6  the tensor objects of content/03-deep-learning/lab-objects.md (0. Lab Objects)
  S1, S2 the construction site objects of content/05-construction-robotics/site-engineering.md (2.5)
  RS1    the frozen research study of content/06-research-practice/index.md

Rule 10 of content/templates/course-page.md says that these labels, and field
jargon such as "plant", are glossed in plain words with a link at their first use
on each page, even when an earlier page defined them: a reader who opens a page
from search or from a link has not read the catalog. This script finds the gaps.

For each page and each language half (split at "## 한국어"), it takes the first
use of every label and reports it when no link to the label's home page lies
within 400 characters on either side. Code blocks, inline SVG, math, frontmatter
and wikilinks to other pages are blanked first, so a label inside them is not a
use. Glossary, study log, templates and the four home pages are skipped.

It is a worklist, not a gate: it always exits 0, and every hit has to be read.
Known false positives, each checked by reading the page:

  * a different thing with the same name: Skild AI's policy S1 on the VLA pages,
    a paper's supplementary "Table S2", a code variable named P2 (3. State
    Estimation's tracking detections were renamed z1-z3 on 2026-09-25 so they
    no longer look like the D1-D6 catalog labels);
  * a page-local object that reuses a label: 14. Tactile & Visuotactile Sensing
    calls its fingertip patch S1 (glossed in words at its first use);
  * a label glossed in plain words at its first use without a link, or restated
    in full in the page's own Running object section.

It does not check "plant" or other jargon, and it does not check page-local
objects such as MLP-256 or H1, which are defined in their own Running object
sections; read for those.

    python3 scripts/audit_labels.py        # every page with a gap, then counts by folder
    python3 scripts/audit_labels.py 10     # only the first ten pages
"""
import glob
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

LAB = re.compile(r"(?<![A-Za-z0-9_\-/])(P[1-6]|D[1-6]|S[12]|RS1)(?![A-Za-z0-9_])")
HOME = {
    "P": "02-foundations/lab-plants",
    "D": "03-deep-learning/lab-objects",
    "S": "05-construction-robotics/site-engineering",
    "R": "06-research-practice/index",
}
WINDOW = 400


def strip(text):
    """Blank what is not prose, keeping offsets: code, SVG, math, and links to other pages."""
    text = re.sub(r"```.*?```", lambda m: " " * len(m.group()), text, flags=re.S)
    text = re.sub(r"<svg.*?</svg>", lambda m: " " * len(m.group()), text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", lambda m: " " * len(m.group()), text, flags=re.S)
    text = re.sub(r"\$[^$\n]*\$", lambda m: " " * len(m.group()), text)
    text = re.sub(r"\[\[[^\]]*\]\]",
                  lambda m: m.group() if any(h in m.group() for h in HOME.values())
                  else " " * len(m.group()), text)
    return text


def audit():
    rows = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(path, CONTENT)[:-3].replace(os.sep, "/")
        if (rel in HOME.values() or "glossary" in rel or "study-log" in rel
                or rel.startswith("templates")):
            continue
        raw = open(path, encoding="utf-8").read()
        raw = re.sub(r"^---\n.*?\n---\n", lambda m: " " * len(m.group()), raw, flags=re.S)
        k = raw.find("## 한국어")
        halves = [("EN", raw[:k] if k > 0 else raw), ("KO", raw[k:] if k > 0 else "")]
        bad = []
        for name, half in halves:
            s = strip(half)
            seen = set()
            for m in LAB.finditer(s):
                label = m.group(1)
                if label in seen:
                    continue
                seen.add(label)
                window = s[max(0, m.start() - WINDOW): m.end() + WINDOW]
                if HOME[label[0]] not in window:
                    bad.append(f"{name}:{label}")
        if bad:
            rows.append((rel, bad))
    return rows


def main():
    rows = audit()
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(rows)
    print(f"{len(rows)} pages with an unglossed first use")
    for rel, bad in rows[:limit]:
        print(" ", rel, " ".join(bad))
    print(dict(Counter(rel.split("/")[0] for rel, _ in rows)))


if __name__ == "__main__":
    main()
