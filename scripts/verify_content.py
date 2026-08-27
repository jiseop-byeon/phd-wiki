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
  9. Substantive curriculum pages declare a valid study-depth profile.
 10. No **bold** run is left unrendered by CommonMark's right-flanking rule
     (a closing ** preceded by punctuation and followed by a letter never closes —
     it bites Korean text like `**용어(term)**이`, which then shows literal asterisks).
Exit code 1 on any failure, with a per-file report.
"""

import os
import re
import unicodedata
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

# 9. Global topic-depth contract. Indexes, templates, logs, and the Radar itself
# are navigation/operations pages rather than study objects.
depth_exclusions = {
    "index.md",
    "glossary.md",
    "study-log.md",
    "08-research-radar/index.md",
}
depth_exclusion_prefixes = ("templates/",)
valid_depths = {"Literacy", "Working", "Mastery"}
for p in md_files:
    rel = os.path.relpath(p, CONTENT)
    if rel in depth_exclusions or rel.endswith("/index.md") or rel.startswith(depth_exclusion_prefixes):
        continue
    text = open(p, encoding="utf-8").read()
    match = re.search(r"^study-depth:\s*(.+?)\s*$", text, re.M)
    if not match:
        err(p, "missing global study-depth profile")
        continue
    if match.group(1).strip() not in valid_depths:
        err(p, f"invalid study-depth: {match.group(1).strip()}")
    if not re.search(r"^depth-goal:\s*.+$", text, re.M):
        err(p, "frontmatter missing depth-goal:")
    if not re.search(r"^mastery-when:\s*.+$", text, re.M):
        err(p, "frontmatter missing mastery-when:")

# 10. Bold runs that CommonMark will not close.
# A closing "**" is right-flanking only if it is NOT preceded by punctuation, or is
# followed by whitespace/punctuation. `**연속 극한(continuum limit)**의` fails both and
# renders as literal asterisks. Fix by moving the parenthetical outside: `**연속 극한**(...)`.
# CommonMark counts Unicode *symbols* as punctuation here too, so `**HIL-SERL ★**을`
# fails for the same reason — hence the category test rather than a literal character set.
bold_re = re.compile(r"\*\*(?=\S)([^*\n]{1,120}?)\*\*(.?)", re.S)
def _is_punct(ch):
    return unicodedata.category(ch)[0] in ("P", "S")
class _PunctSet:
    def __contains__(self, ch):
        return bool(ch) and _is_punct(ch)
punct = _PunctSet()
def _bold_scan(path, text, lineno):
    text = re.sub(r"`[^`]*`", "", text)  # inline code is not parsed as emphasis
    for m in bold_re.finditer(text):
        inner, nxt = m.group(1), m.group(2)
        if not inner or inner[-1] not in punct:
            continue
        if nxt and not nxt.isspace() and nxt not in punct:
            flat = " ".join(inner.split())
            err(path, f"line {lineno}: bold never closes (** preceded by '{inner[-1]}', "
                      f"followed by '{nxt}') — move the parenthetical outside the ** in: "
                      f"**{flat}**{nxt}")

for p in md_files:
    lines = open(p, encoding="utf-8").read().split("\n")
    # (a) per line
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith(("<", "|")):
            continue
        _bold_scan(p, line, i)
    # (b) per paragraph — a bold run split across a line break escapes the per-line scan,
    #     because the regex cannot cross a newline. Join wrapped prose and scan again.
    start, buf = 0, []
    def _flush():
        if buf:
            _bold_scan(p, " ".join(buf), start)
        buf.clear()
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith(("<", "|", "#", "```")):
            _flush()
            continue
        if not buf:
            start = i
        buf.append(re.sub(r"^>\s?", "", line).strip())
    _flush()

# 11. Section references that point OUT OF RANGE on the target page.
# Convention: [[target|<page-no>. §<n>]] — the label's § numbers must exist as
# "### <n>." headings in the target.
# KNOWN LIMIT, do not overtrust: this catches only refs to sections that do not
# exist. It cannot catch a ref to the WRONG existing section, which is the more
# common failure — six refs went stale in one session by pointing at §4 when the
# material had moved to §7, and every one of them would pass this check. It does
# catch the "§<page>.<sec>" fused form (§21.4), which parses as out of range.
_sec_cache = {}
def _sections_of(rel):
    if rel not in _sec_cache:
        try:
            body = open(os.path.join("content", rel + ".md"), encoding="utf-8").read()
        except OSError:
            _sec_cache[rel] = set()
        else:
            _sec_cache[rel] = set(re.findall(r"^#{3,4}\s*(\d+(?:\.\d+)?)[.\s]", body, re.M))
    return _sec_cache[rel]

_link_re = re.compile(r"\[\[([^\]|#]+)\|([^\]]*?)\]\]")
for p in md_files:
    rel_src = os.path.relpath(p, "content")[:-3]
    text = open(p, encoding="utf-8").read()
    for m in _link_re.finditer(text):
        tgt_raw, label = m.group(1), m.group(2)
        secs = re.findall(r"§\s*(\d+(?:\.\d+)?)", label)
        if not secs:
            continue
        tgt_raw = tgt_raw.split("#")[0].strip().rstrip("\\")
        src_dir = os.path.dirname(rel_src)
        tgt = None
        for cand in (tgt_raw, os.path.normpath(os.path.join(src_dir, tgt_raw))):
            if cand in targets:
                tgt = cand
                break
        if tgt is None:
            continue                      # broken link: already reported by check 4
        have = _sections_of(tgt)
        if not have:
            continue                      # target has no numbered sections
        for s in secs:
            if s not in have:
                err(p, f"section reference {tgt} §{s} does not exist "
                       f"(that page has §{', §'.join(sorted(have, key=float))})")

# --- 12. self-counts: numbers the wiki states about its own contents ---------
# These drift silently: a page is added, a mark is changed, and a sentence
# somewhere else still reports the old total.  Every count below is derived
# from the files, so the derivation is the authority.  A claim whose pattern
# no longer matches is also an error — a reworded claim must be re-checked
# deliberately, not lose its check by accident.
_notes = [f for f in md_files
          if "01-canonical-papers/notes/" in f.replace(os.sep, "/")
          and os.path.basename(f) != "index.md"]
_n_notes = len(_notes)
_n_secs = len({os.path.basename(os.path.dirname(f)) for f in _notes})

def _track(d):
    return len([f for f in md_files
                if os.path.relpath(f, "content").replace(os.sep, "/").rsplit("/", 1)[0] == d
                and os.path.basename(f) != "index.md"])

_cl = ""
try:
    _cl = open("content/01-canonical-papers/canonical-list.md", encoding="utf-8").read()
except OSError:
    err("content/01-canonical-papers/canonical-list.md", "missing: cannot derive ★/◐/○ counts")
_marks = {m: len(re.findall(r"^- (?:\[.\] )?" + m + " ", _cl, re.M)) for m in "★◐○"}
# one ★ is the Modern Robotics textbook, which overview.md counts separately
_star_papers = _marks["★"] - 1
_total_pages = (_track("02-foundations") + _track("04-robotics")
                + _track("04-robotics/modern-robotics") + _track("05-construction-robotics")
                + _track("06-research-practice") + _track("07-research-program") + _n_notes)

_claims = [
    ("01-canonical-papers/index.md", r"\((\d+) notes across (\d+) sections\)",
     (_n_notes, _n_secs), "note and section count (EN)"),
    ("01-canonical-papers/index.md", r"\((\d+)편, (\d+)개 섹션\)",
     (_n_notes, _n_secs), "note and section count (KR)"),
    ("02-foundations/overview.md", r"\| Paper notes \((\d+)\) \| (\d+) \|",
     (_n_notes, _n_notes), "reading-load table, notes row (EN)"),
    ("02-foundations/overview.md", r"\| 논문 노트 \((\d+)편\) \| (\d+) \|",
     (_n_notes, _n_notes), "reading-load table, notes row (KR)"),
    ("02-foundations/overview.md", r"\*\*Total\*\* \| \*\*(\d+)\*\*",
     (_total_pages,), "reading-load table total (EN)"),
    ("02-foundations/overview.md", r"\*\*합계\*\* \| \*\*(\d+)\*\*",
     (_total_pages,), "reading-load table total (KR)"),
    ("02-foundations/overview.md", r"extra: \*\*(\d+)\*\* of them read in the original",
     (_star_papers,), "★ paper count (EN)"),
    ("02-foundations/overview.md", r"★ 논문은 별도다: \*\*(\d+)편\*\*",
     (_star_papers,), "★ paper count (KR)"),
    ("02-foundations/overview.md", r"the (\d+) ◐ and (\d+) ○",
     (_marks["◐"], _marks["○"]), "◐/○ counts (EN)"),
    ("02-foundations/overview.md", r"◐ (\d+)편과 ○ (\d+)편",
     (_marks["◐"], _marks["○"]), "◐/○ counts (KR)"),
]
for rel, pat, expect, what in _claims:
    fp = os.path.join("content", rel)
    try:
        body = open(fp, encoding="utf-8").read()
    except OSError:
        err(fp, f"missing: cannot verify {what}")
        continue
    m = re.search(pat, body)
    if not m:
        err(fp, f"self-count claim not found — {what}: the wording changed, so "
                f"its check no longer applies. Update the pattern in check 12.")
        continue
    got = tuple(int(g) for g in m.groups())
    if got != tuple(expect):
        err(fp, f"self-count mismatch — {what}: page says {got}, "
                f"the files give {tuple(expect)}")

# --- 13. bilingual parity of section references ------------------------------
# A correction that reaches only one language half leaves the other half
# asserting the superseded claim.  Section references are the decidable part
# of that: the two halves of a page must cite the same sections.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import audit_parity
except ImportError:
    err("scripts/audit_parity.py", "missing: bilingual parity cannot be checked")
else:
    for p in md_files:
        h = audit_parity.halves(open(p, encoding="utf-8").read())
        if not h:
            continue
        en, kr = audit_parity.section_refs(h[0]), audit_parity.section_refs(h[1])
        for side, only in (("English", en - kr), ("Korean", kr - en)):
            for tgt, sec in sorted(only):
                err(p, f"section reference {tgt} §{sec} appears in the {side} half "
                       f"only — the other half was not updated with it")

errors = list(dict.fromkeys(errors))
if errors:
    print(f"CONTENT CHECK FAILED — {len(errors)} problem(s):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"Content check passed: {len(md_files)} files, {len(errors)} problems.")
