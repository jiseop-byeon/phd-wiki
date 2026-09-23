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
import collections
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
                if "\\\\|" in m.group(0):
                    err(p, f"line {i}: table-cell wikilink pipe is double-escaped; use one backslash")
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

_depths = collections.Counter()
_ch01_literacy = 0
for _f in md_files:
    _m = re.search(r"^study-depth:\s*(\S+)", open(_f, encoding="utf-8").read(), re.M)
    if not _m:
        continue
    _depths[_m.group(1)] += 1
    if _m.group(1) == "Literacy" and "01-canonical-papers" in _f.replace(os.sep, "/"):
        _ch01_literacy += 1

_claims = [
    ("01-canonical-papers/index.md", r"\((\d+) notes across (\d+) sections\)",
     (_n_notes, _n_secs), "note and section count (EN)"),
    ("01-canonical-papers/index.md", r"\((\d+)편, (\d+)개 섹션\)",
     (_n_notes, _n_secs), "note and section count (KR)"),
    ("07-research-program/index.md",
     r"(\d+) pages sit at Working, (\d+) at\nLiteracy, (\d+) at Mastery",
     (_depths["Working"], _depths["Literacy"], _depths["Mastery"]),
     "study-depth distribution (EN)"),
    ("07-research-program/index.md",
     r"Working이 (\d+)쪽, Literacy가 (\d+)쪽,\nMastery가 (\d+)쪽이다",
     (_depths["Working"], _depths["Literacy"], _depths["Mastery"]),
     "study-depth distribution (KR)"),
    ("07-research-program/index.md", r"— (\d+) of the (\d+) sit in",
     (_ch01_literacy, _depths["Literacy"]),
     "Literacy pages inside chapter 01 (EN)"),
    ("07-research-program/index.md", r"(\d+)쪽 중 (\d+)쪽이 \[\[01-canonical-papers",
     (_depths["Literacy"], _ch01_literacy),
     "Literacy pages inside chapter 01 (KR)"),
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

# --- 14. depth assignments against the study guide's own defaults ----------
# The guide states a default depth per area, and a sharper one in the
# construction-manipulation profile.  A page may sit below its default; sitting
# above it without a documented reason is the drift the 2026-09-09 evaluation
# suspected.  audit_depth also fails if a table row's wording changes.
try:
    import audit_depth
except ImportError:
    err("scripts/audit_depth.py", "missing: depth conformance cannot be checked")
else:
    for _f, _msg in audit_depth.audit():
        err(_f, _msg)

# --- 15. glossary ordering ---------------------------------------------------
# The four alphabetical sections are sorted case-insensitively with punctuation
# and spaces ignored, so Anti-windup precedes Antipodal grasp and k-means
# precedes KL divergence. Nothing enforced it until 2026-09-10, and two entries
# had slipped. The "Confusable pairs" section is grouped by theme, not sorted.
_gloss = os.path.join("content", "glossary.md")
try:
    _g = open(_gloss, encoding="utf-8").read()
except OSError:
    err(_gloss, "missing: glossary ordering cannot be checked")
else:
    _key = lambda s: re.sub(r"[^a-z0-9]", "", s.casefold())
    _sections = re.split(r"^## ", _g, flags=re.M)[1:]
    if len(_sections) < 2:
        err(_gloss, "no '## ' sections found — glossary ordering check no longer applies")
    for _s in _sections:
        _name = _s.split("\n")[0]
        if "Confusable" in _name:
            continue
        _names = [m.group(1) for m in re.finditer(r"^- \*\*(.+?)\*\*", _s, re.M)]
        for _a, _b in zip(_names, _names[1:]):
            if _key(_a) > _key(_b):
                err(_gloss, f"glossary section {_name!r} out of order: "
                            f"{_a!r} is listed before {_b!r}")

# --- 16. glossary tooltip index in sync --------------------------------------
# quartz/static/glossary/terms.json is generated from content/glossary.md and
# committed; a glossary edit without a rebuild would ship stale tooltips.
import subprocess as _sp
_r = _sp.run([sys.executable, os.path.join("scripts", "build_glossary_index.py"), "--check"],
             capture_output=True, text=True)
if _r.returncode != 0:
    err("quartz/static/glossary/terms.json", _r.stdout.strip() or "glossary index check failed")

# --- 17. SVG ids unique on a page ---------------------------------------------
# Both language halves render into one HTML page, and the language toggle hides
# one half with display:none. A figure whose marker or gradient id repeats an id
# first defined in the hidden half can lose its arrowheads, so every id inside
# an inline SVG must be unique on its page (the Korean copy takes a suffix).
_svg_block = re.compile(r"<svg\b.*?</svg>", re.S)
_svg_id = re.compile(r'\sid="([^"]+)"')
for p in md_files:
    _ids = []
    for _svg in _svg_block.findall(open(p, encoding="utf-8").read()):
        _ids += _svg_id.findall(_svg)
    _dup = sorted({i for i in _ids if _ids.count(i) > 1})
    if _dup:
        err(p, f"SVG id defined more than once on the page: {', '.join(_dup)} — "
               f"give the Korean half's copy its own id")

# --- 18. Session tables assign every section of the pages they schedule ------
# A track index's session table is the course's syllabus. A section added to a
# scheduled page without a row is taught but never assigned: nine deep-learning
# sections and two of MR ch.3 went unassigned until 2026-09-22. A page counts as
# scheduled when a row introduces it (object, plant, diagram, worked case, or
# "all"); a page the table only cross-reads by section — 13 and 24.4 in the
# robotics track's session 81 — is exempt. Sections are the `### N.` and
# `### N.M` headings of the English half; the Korean table must match row for row.
_SCHED_TRACKS = ("03-deep-learning/index.md", "04-robotics/index.md",
                 "06-research-practice/index.md")
_sched_row = re.compile(r"^\| (?:\*\*)?\d+(?:\*\*)? \|")
_sched_link = re.compile(r"\[\[([^|\]\\]+)\\?\|([^\]]+)\]\]")
_sched_intro = re.compile(r"\b(object|plant|diagram|worked case|all)\b")


def _sched_halves(text):
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    m = re.search(r"^## 한국어", body, re.M)
    return (body[:m.start()], body[m.start():]) if m else (body, "")


def _sched_key(s):
    return tuple(int(x) for x in s.split("."))


for _track in _SCHED_TRACKS:
    _tp = os.path.join(CONTENT, _track)
    _en, _ko = _sched_halves(open(_tp, encoding="utf-8").read())
    _rows_en = [l for l in _en.splitlines() if _sched_row.match(l)]
    _rows_ko = [l for l in _ko.splitlines() if _sched_row.match(l)]
    if len(_rows_en) != len(_rows_ko):
        err(_tp, f"session table has {len(_rows_en)} rows in English and {len(_rows_ko)} in Korean")
    _bold = sum(1 for l in _rows_en if l.startswith("| **"))
    _tot_en = re.search(r"^\*\*Totals\.\*\* (\d+) sessions for the Working pass, (\d+) of them bold", _en, re.M)
    _tot_ko = re.search(r"^\*\*합계\.\*\* Working 통과는 (\d+)회이고 그중 굵은 회차가 (\d+)회", _ko, re.M)
    for _lang, _tot in (("English", _tot_en), ("Korean", _tot_ko)):
        if not _tot:
            err(_tp, f"session table's {_lang} Totals line not found in its expected wording")
        elif (int(_tot.group(1)), int(_tot.group(2))) != (len(_rows_en), _bold):
            err(_tp, f"{_lang} Totals say {_tot.group(1)} sessions, {_tot.group(2)} bold; "
                     f"the table has {len(_rows_en)} rows, {_bold} bold")
    _labels = {lab: path for l in _rows_en for path, lab in _sched_link.findall(l)}
    _intro, _cov = set(), collections.defaultdict(set)
    for l in _rows_en:
        _cell = _sched_link.sub(r"\2", l.split(" | ")[1])
        _cur = None
        for _seg in re.split(r",? and (?=\S)", _cell):
            _seg = _seg.strip()
            _m = re.match(r"(MR ch\.\d+|\d+(?:\.\d+)*)\b", _seg)
            if _m and _m.group(1) in _labels:
                _cur, _seg = _labels[_m.group(1)], _seg[_m.end():]
                if _sched_intro.search(_seg):
                    _intro.add(_cur)
            if _cur is None:
                continue
            if re.search(r"\ball\b", _seg):
                _cov[_cur].add(("0", "9999"))
            for _a, _b in re.findall(r"§(\d+(?:\.\d+)?)(?:[–-](\d+(?:\.\d+)?))?", _seg):
                _cov[_cur].add((_a, _b or _a))
    for _page in sorted(_intro):
        _pp = os.path.join(CONTENT, _page + ".md")
        _secs = re.findall(r"^### (\d+(?:\.\d+)?)\.? ", _sched_halves(open(_pp, encoding="utf-8").read())[0], re.M)
        _miss = [s for s in _secs
                 if not any(_sched_key(a) <= _sched_key(s) <= _sched_key(b) for a, b in _cov[_page])]
        if _miss:
            err(_tp, f"session table never assigns {_page}.md " + ", ".join("§" + s for s in _miss)
                     + " — add a row, and update the Totals line")

errors = list(dict.fromkeys(errors))
if errors:
    print(f"CONTENT CHECK FAILED — {len(errors)} problem(s):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"Content check passed: {len(md_files)} files, {len(errors)} problems.")
