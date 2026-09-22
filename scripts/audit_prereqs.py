#!/usr/bin/env python3
"""Compare what each course page declares as prerequisites with what it actually leans on.

For every Foundations and Robotics course page it reports:
  LATER    a page listed in the Prerequisites callout that comes AFTER this page in study
           order (the listed page cannot have been read yet), and
  UNLISTED an earlier page this page's lecture cites at least MIN_CITES times (wikilinks,
           counted in the English half, Sources excluded) that the Prerequisites callout
           does not list.
Study order comes from the number at the start of each page's title (0.5, 3.2, 10.5, 24.3,
25.5.1 ...), Foundations before Robotics; Modern Robotics chapters 2-9 sit at 2.CC and the later
chapters beside the page they serve (ch.10 with 4, ch.11 after 5, ch.12 with 15, ch.13 with 16). Pages in
the robotics specialisations (12 and up) are "later" than every common-track page (1-11).

Exit status is always 0: this is a worklist for judgment, not a gate.
Usage: python3 scripts/audit_prereqs.py [--min-cites N]
"""
import argparse
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
TITLE = re.compile(r'^title:\s*"?(.+?)"?\s*$', re.M)


def rank(rel, title):
    """(track, number tuple) or None for pages outside the ordered tracks."""
    if rel.startswith("02-foundations/algorithms/"):
        return None
    track = 0 if rel.startswith("02-foundations/") else 1 if rel.startswith("04-robotics/") else None
    if track is None:
        return None
    m = re.match(r"MR Ch\.?\s*0?(\d+)", title)
    if m:
        ch = int(m.group(1))
        # Chapters 2-9 are read as block 2; the later chapters are read alongside the page
        # they serve (04-robotics/index.md study-order note): ch.10 with 4, ch.11 after 5,
        # ch.12 with 15, ch.13 with 16. "With" is ranked just before that page, so the page
        # may list its chapter as a prerequisite; "after" is ranked just after.
        serve = {10: (3, 99), 11: (5, 1), 12: (14, 99), 13: (15, 99)}
        return (track, serve.get(ch, (2, ch)))
    m = re.match(r"(\d+(?:\.\d+)*)", title)
    if not m:
        return None
    return (track, tuple(int(x) for x in m.group(1).split(".")))


def halves(text):
    if "## 한국어" not in text:
        return text, ""
    en, ko = text.split("## 한국어", 1)
    return en, ko


def prereq_block(en):
    m = re.search(r"^> \[!note\] Prerequisites.*?\n((?:>.*\n)+)", en, re.M)
    if not m:
        m = re.search(r"^> \[!note\] Prerequisites.*?\n((?:>.*\n)+)", en + "\n", re.M)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-cites", type=int, default=3)
    args = ap.parse_args()
    pages = {}
    for p in glob.glob("content/0[24]-*/**/*.md", recursive=True):
        rel = os.path.relpath(p, "content")[:-3]
        if os.path.basename(p) == "index.md":
            continue
        t = open(p, encoding="utf-8").read()
        m = TITLE.search(t)
        r = rank(rel + ".md", m.group(1) if m else "")
        if r:
            pages[rel] = (r, t)
    out = []
    for rel, (r, t) in sorted(pages.items(), key=lambda kv: kv[1][0]):
        en, _ = halves(t)
        # the Prerequisites callout may sit above "## English"
        head = t.split("## English", 1)[0] + en
        listed = {x.strip() for x in LINK.findall(prereq_block(head))}
        body = re.split(r"^### (Sources|출처)", en, flags=re.M)[0]
        cites = {}
        for x in LINK.findall(body):
            x = x.strip()
            cites[x] = cites.get(x, 0) + 1
        later = [x for x in listed if x in pages and pages[x][0] > r
                 and not (r[0] == 1 and r[1][0] <= 11 and pages[x][0][1][0] <= 11 and pages[x][0] < r)]
        unlisted = [(x, n) for x, n in cites.items()
                    if n >= args.min_cites and x not in listed and x != rel and x in pages and pages[x][0] < r]
        if later or unlisted:
            out.append(f"{rel}")
            for x in sorted(later):
                out.append(f"    LATER    {x}")
            for x, n in sorted(unlisted, key=lambda z: -z[1]):
                out.append(f"    UNLISTED {x}  (cited {n}x)")
    print("\n".join(out))
    print(f"\n{sum(1 for l in out if not l.startswith(' '))} page(s) with prerequisite findings "
          f"(min cites {args.min_cites}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
