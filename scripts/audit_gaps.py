#!/usr/bin/env python3
"""Find gaps in the two study tracks that the other checks cannot see.

verify_content.py catches breakage — broken links, unbalanced markup, stale
self-counts. audit_parity.py catches the two halves drifting apart. This
script catches the third kind: a page that is internally correct and still
leaves the reader stuck.

Four detectors, in decreasing order of how much each one has actually found:

  1. UNDEFINED   a concept the wiki uses but chapters 2 and 4 never teach.
                 The concept dictionary is the union of the index entries of
                 the canonical texts under reference/canonical-texts/ (run
                 with --build-index once to extract them). A term is exempt
                 if it has its own paper note, since the note is where it is
                 explained.
  2. ARITHMETIC  every evaluable expression of the form <numbers> = <number>
                 in chapters 2 and 4, recomputed. Unit and power-of-ten
                 rescalings are accepted, because "0.785/31.4 = 25" is
                 correct when the answer is in milliseconds.
  3. PREREQ      a page that uses several concepts homed on another study
                 page without declaring that page in its prerequisites.
                 Forward pointers to later pages are expected and are not
                 dependencies; check the wording rather than the count.
  4. SELFCHECK   self-check questions whose answer block does not cover them.
  5. UNEXPLAINED a display equation stated with no motivation, derivation or
                 consequence anywhere near it. Many hits are legitimate --
                 definitions have nothing to derive, and worked-example steps are
                 explained by the example around them -- so read each one and ask
                 whether a textbook would say where the formula comes from.

Exit status is 0 always: these are leads to judge, not failures. Most hits
in detector 1 are ordinary English words that a book happened to index.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTS = os.path.join(ROOT, "reference", "canonical-texts")
INDEX = os.path.join(TEXTS, "index_terms.json")
STUDY = ["content/02-foundations/**/*.md", "content/04-robotics/**/*.md"]
# Checked by hand and confirmed not to be gaps, so the detector stays readable.
# Two kinds: ordinary English words a book happened to index (philosophy, regular,
# terminology, evolution, steering, ...), and terms the wiki explains where it uses
# them rather than in a study page (euler integration is written out in the
# flow-matching note; random walk is derived in score-sde and linked to probability).
NOISE = {
    # ordinary English words that a book happened to index
    "evolution", "philosophy", "regular", "terminology", "british", "brain",
    "replication", "permutation", "normalized", "standardized", "ensemble",
    "portfolio", "bearing", "arrangement", "steering", "shrinkage", "regular",
    "dependent variable", "big data", "artificial intelligence", "acceptance rate",
    "annealing", "chatgpt", "mnist",
    # covered under a different name: rl-basics teaches reward design at length
    "reward function",
    # explained where they are used rather than in a study page: euler integration
    # is written out in the flow-matching note, random walk is derived in score-sde
    # and linked back to the probability page
    "euler integration", "random walk",
}


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def files(pats):
    out = []
    for p in pats:
        out += glob.glob(os.path.join(ROOT, p), recursive=True)
    return sorted(set(out))


def build_index():
    """Extract index entries from the plain-text extractions of each book."""
    entry = re.compile(r"^([A-Za-z][A-Za-z0-9 \-'/(),.:&]{2,58}?),\s*(?:see\s|\d)")
    out = collections.defaultdict(set)
    for f in sorted(glob.glob(os.path.join(TEXTS, "txt", "*.txt"))):
        t = read(f)
        hits = [m.start() for m in re.finditer(r"\n\s*Index\s*\n", t)]
        if not hits:
            continue
        idx = re.sub(r"<<<PAGE \d+>>>", "", t[hits[-1]:])
        for line in idx.split("\n"):
            m = entry.match(line.strip())
            if m:
                out[os.path.basename(f)[:-4]].add(m.group(1).strip().rstrip(","))
    with open(INDEX, "w") as fh:
        json.dump({k: sorted(v) for k, v in out.items()}, fh, ensure_ascii=False, indent=0)
    print(f"wrote {INDEX}: {sum(len(v) for v in out.values())} entries from {len(out)} books")


def ngrams(pats, maxn=4):
    S = set()
    for f in files(pats):
        toks = re.findall(r"[a-z][a-z0-9\-']*", read(f).lower())
        for n in range(1, maxn + 1):
            for i in range(len(toks) - n + 1):
                S.add(" ".join(toks[i:i + n]))
    return S


def undefined():
    if not os.path.exists(INDEX):
        print("  (no index_terms.json — run with --build-index; needs reference/canonical-texts/txt)")
        return
    idx = json.load(open(INDEX))
    concepts = collections.defaultdict(set)
    for book, terms in idx.items():
        for t in terms:
            t = " ".join(t.strip().lower().split())
            if 4 < len(t) < 40 and not t[0].isdigit():
                concepts[t].add(book)
    teach = ngrams(STUDY + ["content/glossary.md"])
    rest = ngrams(["content/01-canonical-papers/**/*.md", "content/03-*/**/*.md",
                   "content/05-*/**/*.md", "content/06-*/**/*.md", "content/*.md"])
    notes = {os.path.basename(f)[:-3].replace("-", " ")
             for f in files(["content/01-canonical-papers/notes/**/*.md"])}
    hits = [(len(b), t) for t, b in concepts.items()
            if t in (teach | rest) and t not in teach and t not in notes and t not in NOISE]
    hits.sort(key=lambda r: -r[0])
    strong = [h for h in hits if h[0] >= 2]
    print(f"  {len(hits)} concept(s) used but not taught; {len(strong)} indexed by 2+ books")
    for n, t in strong[:25]:
        print(f"     {n} books  {t}")


def arithmetic():
    def ok(v, c):
        for s in (1, 1e-3, 1e3, 1e-2, 1e2, 1e-6, 1e6, 60, 1 / 60):
            dp = len(str(c).split(".")[1]) if "." in str(c) else 0
            if abs(v * s - c) <= max(abs(c) * 0.02, 0.51 * 10 ** -dp):
                return True
        return False
    checked = 0
    bad = []
    for f in files(STUDY):
        s = re.sub(r"<svg.*?</svg>", "", read(f), flags=re.S)
        t = s.replace("\\times", " * ").replace("\\cdot", " * ").replace("×", " * ").replace("·", " * ")
        t = re.sub(r"10\^\{?(-?\d+)\}?", lambda m: f"(10**{m.group(1)})", t)
        # LaTeX thousands separators, then plain ones: 10{,}000 and 10,000 alike
        t = t.replace("{,}", "")
        t = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", t)
        for m in re.finditer(
                r"(?<![\w.+\-])((?:\(?10\*\*-?\d+\)?|[0-9][0-9.]*)"
                r"(?:\s*[*+\-/]\s*(?:\(?10\*\*-?\d+\)?|[0-9][0-9.]*)){1,6})"
                r"\s*=\s*\\?(?:mathbf|mathrm)?\{?(-?[0-9][0-9.]*)", t):
            expr, claim = m.group(1), m.group(2)
            tail = t[m.end():m.end() + 3]
            # an equation, not an evaluation: the right side keeps going
            if tail[:1] in ("(", "^") or tail.startswith("\\,"):
                continue
            # implicit multiplication the parser cannot see: 600(-0.3)/1.5
            if re.search(r"\d\s*\(", t[max(0, m.start() - 12):m.start() + len(expr)]):
                continue
            try:
                v = eval(expr, {"__builtins__": {}}, {})
                c = float(claim)
            except Exception:
                continue
            checked += 1
            after = t[m.end():m.end() + 6]
            pct = "%" in after
            # a claim written without decimals is a rounded claim
            rounded = "." not in claim and (round(v) == c or (pct and round(v * 100) == c))
            if ok(v, c) or (pct and ok(v * 100, c)) or rounded:
                continue
            bad.append((os.path.relpath(f, ROOT), expr.strip(), claim, v))
    print(f"  {checked} expression(s) recomputed, {len(bad)} unexplained")
    for fn, e, c, v in bad:
        print(f"     {fn}: {e} = {c}  (computes to {v:.6g})")


def prereq():
    home = {}
    for line in read(os.path.join(ROOT, "content/glossary.md")).split("\n"):
        m = re.match(r"- \*\*(.+?)\*\*.*?→\s*\[\[([^\]|]+)", line)
        if not m:
            continue
        term = re.sub(r"\(\$.*?\$\)", "", m.group(1)).strip()
        if "vs" in term or "·" in term or len(term) < 5:
            continue
        home[term.lower()] = m.group(2).strip()
    issues = []
    for p in files(["content/02-foundations/*.md", "content/04-robotics/*.md"]):
        if os.path.basename(p) in ("index.md", "overview.md"):
            continue
        s = read(p)
        slug = os.path.relpath(p, ROOT).replace("content/", "")[:-3]
        m = re.search(r"^##\s*한국어\s*$", s, re.M)
        en = s[:m.start()] if m else s
        pr = re.search(r">\s*\[!note\][^\n]*(?:Prerequisites|선수 지식)(.*?)(?=\n\n)", s, re.S)
        decl = {d.strip() for d in re.findall(r"\[\[([^\]|#]+)", pr.group(1))} if pr else set()
        body = re.sub(r">\s*\[!note\][^\n]*(?:Prerequisites|선수 지식).*?(?=\n\n)", "", en, flags=re.S).lower()
        used = collections.Counter()
        for t, h in home.items():
            if h == slug or h in decl:
                continue
            if not (h.startswith("02-foundations/") or h.startswith("04-robotics/")):
                continue
            if re.search(r"(?<![a-z])" + re.escape(t) + r"(?![a-z])", body):
                used[h] += 1
        # A page cannot depend on a later page in the study order; a reference from
        # 1. Linear Algebra to 4. Optimization is a forward pointer by construction.
        mine = re.search(r"^title:\s*\"?(\d+(?:\.\d+)?)\.", s, re.M)
        for h, n in used.items():
            theirs = None
            hp = os.path.join(ROOT, "content", h + ".md")
            if os.path.exists(hp):
                mt = re.search(r"^title:\s*\"?(\d+(?:\.\d+)?)\.", read(hp), re.M)
                theirs = float(mt.group(1)) if mt else None
            if mine and theirs is not None and theirs > float(mine.group(1)):
                continue          # forward pointer, not a missing prerequisite
            if n >= 3:
                issues.append((slug, h, n))
    print(f"  {len(issues)} page(s) leaning on an undeclared study page")
    for a, b, n in sorted(issues, key=lambda r: -r[2]):
        print(f"     {a} → {b} ({n} concepts)")


def selfcheck():
    bad = 0
    for f in files(["content/02-foundations/*.md", "content/04-robotics/*.md"]):
        s = read(f)
        m = re.search(r"^##\s*한국어\s*$", s, re.M)
        for lab, half in (("EN", s[:m.start()] if m else s), ("KR", s[m.start():] if m else "")):
            sc = re.search(r"^### (Self-check|스스로 점검)", half, re.M)
            if not sc:
                continue
            blk = half[sc.end():]
            nx = re.search(r"^### ", blk, re.M)
            blk = blk[:nx.start()] if nx else blk
            ans = re.search(r"^>\s*\[!\w+\]", blk, re.M)
            qs = len(re.findall(r"^\d+\.\s", blk[:ans.start()] if ans else blk, re.M))
            an = len(re.findall(r"(?:^>\s*|\s)(\d+)\.\s", blk[ans.start():], re.M)) if ans else 0
            if qs and an < qs:
                print(f"     {os.path.basename(f)[:-3]} {lab}: {qs} question(s), {an} answer(s)")
                bad += 1
    print(f"  {bad} self-check block(s) missing answers")


def unexplained():
    """Display equations with no explanatory scaffolding nearby.

    A textbook does not only state a formula; it says why it has that shape.
    This flags equations whose surrounding 500 characters contain none of the
    words explanation is normally made of. Expect false positives on
    definitions (a definition has no derivation) and on intermediate steps of
    a worked example (the example is the explanation) -- the check is a
    reading list, not a verdict.
    """
    why = re.compile(
        r"(?i)\b(because|why|the reason|comes from|derive|derivation|follows from|"
        r"which is just|is nothing but|rearrang|substitut|solve for|set .{0,12}= 0|"
        r"minimi[sz]ing|maximi[sz]ing|expand|taylor|equate|in other words|that is,|"
        r"read it as|the shape of|says that|means that|so that|falls out|forced)\b")
    total, bare = 0, []
    for f in files(["content/02-foundations/*.md", "content/04-robotics/*.md"]):
        s = read(f)
        m = re.search(r"^##\s*한국어\s*$", s, re.M)
        en = re.sub(r"<svg.*?</svg>", "", s[:m.start()] if m else s, flags=re.S)
        for mm in re.finditer(r"\$\$(.+?)\$\$", en, re.S):
            eq = mm.group(1).strip()
            if len(eq) < 12:
                continue
            total += 1
            ctx = en[max(0, mm.start() - 500):mm.start()] + en[mm.end():mm.end() + 500]
            if not why.search(ctx):
                bare.append((os.path.basename(f)[:-3], " ".join(eq.split())[:64]))
    print(f"  {len(bare)} of {total} display equation(s) stated without nearby explanation")
    for fn, eq in bare:
        print(f"     {fn}: {eq}")


if __name__ == "__main__":
    if "--build-index" in sys.argv:
        build_index()
        sys.exit(0)
    for name, fn in (("UNDEFINED", undefined), ("ARITHMETIC", arithmetic),
                     ("PREREQ", prereq), ("SELFCHECK", selfcheck),
                     ("UNEXPLAINED", unexplained)):
        print(f"\n{name}")
        fn()
    print()
