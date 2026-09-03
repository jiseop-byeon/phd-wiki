#!/usr/bin/env python3
"""Re-measure the two worklists behind README-easier-and-fuller.md.

Run from the repo root:  python3 .plan/rescan.py
Rewrites terse-sections.json and note-worklist.json and prints the counts the
completion criteria in README §8 refer to. Pure measurement; changes nothing.
"""
import collections, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
WHY = re.compile(r"(?i)\b(because|why |the reason|comes from|so that|which is why|that is why|for example|e\.g\.|worked|with numbers)\b")
SKIP = re.compile(r"(Self-check|Sources|After reading|Connections|Robotics bridge|Where to go|Continue)")


def english(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"^##\s*한국어\s*$", s, re.M)
    en = s[:m.start()] if m else s
    en = re.sub(r"<svg.*?</svg>", "", en, flags=re.S)
    return re.sub(r"```.*?```", "", en, flags=re.S)


def terse():
    out = []
    targets = []
    for d in ["02-foundations", "04-robotics", "05-construction-robotics", "06-research-practice", "07-research-program"]:
        targets += glob.glob(f"content/{d}/**/*.md", recursive=True)
    targets.append("content/00-study-depth-guide.md")
    for f in sorted(targets):
        if os.path.basename(f) == "index.md":
            continue
        en = english(f)
        secs = [(m.start(), m.group(1)) for m in re.finditer(r"^### (.+)$", en, re.M)]
        for i, (pos, title) in enumerate(secs):
            if SKIP.match(title):
                continue
            body = en[pos:(secs[i + 1][0] if i + 1 < len(secs) else len(en))]
            w = len(re.findall(r"\S+", body))
            ex = len(re.findall(r"\[!example\]", body))
            why = len(WHY.findall(body))
            bl = [l for l in body.split("\n") if l.strip()]
            bfrac = sum(1 for l in bl if re.match(r"\s*[-*|]", l)) / max(1, len(bl))
            if w < 140 or (bfrac > 0.6 and ex == 0 and why <= 1):
                out.append(dict(file=f.replace("content/", ""), section=title.strip(), words=w,
                                bullet_frac=round(bfrac, 2), why=why))
    json.dump(out, open(".plan/terse-sections.json", "w"), ensure_ascii=False, indent=1)
    return out


def notes():
    tier = {}
    cl = open("content/01-canonical-papers/canonical-list.md", encoding="utf-8").read()
    for m in re.finditer(r"(★|◐|○)\s*\[\[notes/([^\]|]+)", cl):
        tier[os.path.basename(m.group(2))] = m.group(1)
    rows = []
    for f in sorted(glob.glob("content/01-canonical-papers/notes/**/*.md", recursive=True)):
        if os.path.basename(f) == "index.md":
            continue
        raw = open(f, encoding="utf-8").read()
        en = english(f)
        b = os.path.basename(f)[:-3]
        miss = []
        if not re.search(r"Key intuition|핵심 직관|In plain words", en): miss.append("intuition")
        if not re.search(r"^### Context|^\*\*Context|^\*\*Why read|^\*\*Lineage position", en, re.M): miss.append("context")
        if not re.search(r"\d+(?:\.\d+)?\s*(%|×|x\b|ms|Hz|mm|cm|m/s|N\b|success)", en): miss.append("numbers")
        if not re.search(r"Reading the claim", en): miss.append("claim")
        if not re.search(r"^### Limitations|\*\*Limitations|\*\*Evidence and limitations|^### Critique", en, re.M): miss.append("limits")
        rows.append(dict(note=f.replace("content/", ""), tier=tier.get(b, "?"),
                         words=len(re.findall(r"\S+", en[en.find("## English"):])),
                         missing=miss, arxiv=bool(re.search(r"arxiv\.org/abs/\d", raw)),
                         doi=bool(re.search(r"doi\.org/|DOI", raw))))
    json.dump(rows, open(".plan/note-worklist.json", "w"), ensure_ascii=False, indent=1)
    return rows


if __name__ == "__main__":
    t = terse()
    c = collections.Counter(x["file"].split("/")[0] for x in t)
    print("terse sections:", len(t), dict(c))
    print("  06 sections under 140 words:", sum(1 for x in t if x["file"].startswith("06-") and x["words"] < 140))
    n = notes()
    mc = collections.Counter(k for r in n for k in r["missing"])
    print("notes:", len(n), "missing:", dict(mc))
    core = [r for r in n if r["tier"] in "★◐" and ({"intuition", "claim"} & set(r["missing"]))]
    print("  ★/◐ notes still missing intuition or claim:", len(core))
    print("  worked examples in 05:", sum(open(f, encoding="utf-8").read().count("[!example]")
                                          for f in glob.glob("content/05-construction-robotics/*.md")))
