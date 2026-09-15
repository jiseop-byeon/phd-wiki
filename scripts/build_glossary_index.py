#!/usr/bin/env python3
"""Build quartz/static/glossary/terms.json from content/glossary.md.

The glossary page is the single source of truth. Each entry is one bullet:

    - **English term (ALIAS, ALIAS)** · 한국어 용어 — English definition. · 한국어 정의. → [[page|label]], [[page|label]]

The `· 한국어 용어` part and the `→` links are optional. The JSON feeds the hover
tooltips in plugins/glossary-tooltips. Run after editing the glossary:

    python3 scripts/build_glossary_index.py          # write
    python3 scripts/build_glossary_index.py --check  # exit 1 if the JSON is stale
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "content", "glossary.md")
OUT = os.path.join(ROOT, "quartz", "static", "glossary", "terms.json")

HANGUL = re.compile(r"[\uac00-\ud7a3]")
WIKILINK = re.compile(r"\[\[([^\[\]|#]+)(#[^\[\]|]*)?(?:\|([^\[\]]*))?\]\]")
ENTRY = re.compile(r"^- \*\*(?P<term>(?:[^*\\]|\\.)+?)\*\*(?: · (?P<ko>[^—]+?))? — (?P<body>.+)$")

# Names that are also everyday English or carry several technical senses: the entry
# stays in the glossary but the bare word is never auto-highlighted.
STOP = {
    "accuracy", "action", "agent", "alignment", "asset", "availability", "bias", "binding",
    "collapse", "contribution", "coupon", "critic", "data", "deadline", "demonstration",
    "discovery", "distribution", "drift", "emergent", "entity", "exclusions", "expectation",
    "exploration", "exposure", "frame", "frontier", "frozen", "gate", "goal", "group", "head",
    "hypothesis", "innovation", "intervention", "iteration", "joint", "layer", "link", "map",
    "message", "mode", "model", "momentum", "negatives", "node", "novelty", "observer", "p", "package",
    "parameter", "partition", "pilot", "plant", "pole", "policy", "port", "precision", "prior",
    "proxy", "rank", "recall", "reconstruction", "recovery", "recurrence", "reduction",
    "redundancy", "registration", "relaxation", "reliability", "reset", "return", "scope",
    "seed", "service", "spin", "stability", "stack", "state", "support", "surprise", "tap",
    "task", "temperature", "token", "tolerance", "topic", "trades", "transparency", "twist",
    "update", "weights", "workspace", "zero",
}

KO_STOP = {
    "전달", "배치", "보정", "정규화", "모델", "상태", "데이터", "목표", "행동", "지도",
    "프레임", "관절", "작업", "업데이트", "그룹", "모드", "검출", "충돌", "범위", "노출",
    "분할", "변환", "변형", "출처", "닫힘",
}

TEX = [
    (r"\\top", "ᵀ"), (r"\\gamma", "γ"), (r"\\lambda", "λ"), (r"\\theta", "θ"),
    (r"\\omega", "ω"), (r"\\alpha", "α"), (r"\\beta", "β"), (r"\\sigma", "σ"),
    (r"\\Sigma", "Σ"), (r"\\mu", "μ"), (r"\\pi", "π"), (r"\\tau", "τ"),
    (r"\\epsilon", "ε"), (r"\\varepsilon", "ε"), (r"\\Delta", "Δ"), (r"\\delta", "δ"),
    (r"\\nabla", "∇"), (r"\\partial", "∂"), (r"\\infty", "∞"), (r"\\approx", "≈"),
    (r"\\le(q)?", "≤"), (r"\\ge(q)?", "≥"), (r"\\neq", "≠"), (r"\\times", "×"),
    (r"\\cdot", "·"), (r"\\sum", "Σ"), (r"\\int", "∫"), (r"\\to", "→"),
    (r"\\in", "∈"), (r"\\Lambda", "Λ"), (r"\\phi", "φ"), (r"\\psi", "ψ"),
    (r"\\eta", "η"), (r"\\rho", "ρ"), (r"\\kappa", "κ"), (r"\\xi", "ξ"),
    (r"\\mid", "|"), (r"\\lvert|\\rvert|\\lVert|\\rVert", "‖"),
]


def plain(text):
    """Strip markdown and approximate inline TeX so a tooltip reads as plain text."""
    text = WIKILINK.sub(lambda m: m.group(3) or m.group(1).split("/")[-1], text)

    def tex(m):
        s = m.group(1)
        for pat, rep in TEX:
            s = re.sub(pat + r"(?![A-Za-z])", rep, s)
        s = re.sub(r"\\(?:text|mathrm|mathbf|mathcal|operatorname|hat|bar|tilde|dot|ddot)\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"\\(?:big|Big|left|right)", "", s)
        s = s.replace("\\,", " ").replace("\\;", " ").replace("\\!", "")
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
        s = re.sub(r"\^\{([^{}]*)\}", r"^\1", s)
        s = re.sub(r"_\{([^{}]*)\}", r"_\1", s)
        s = s.replace("{", "").replace("}", "").replace("\\", "")
        return s

    text = re.sub(r"\$([^$]+)\$", tex, text)
    text = re.sub(r"\*\*([^*]+)\*\*|\*([^*]+)\*", lambda m: m.group(1) or m.group(2), text)
    text = text.replace("\\*", "*").replace("`", "")
    return text.strip()


def split_defs(body):
    """Split 'EN def · KO def' at the ' · ' with the most Hangul after it and the least before."""
    best, score = None, 0
    for m in re.finditer(r" · ", body):
        after = len(HANGUL.findall(body[m.end():]))
        before = len(HANGUL.findall(body[:m.start()]))
        if after and after - 3 * before > score:
            best, score = m, after - 3 * before
    if best is None:
        return body, ""
    return body[:best.start()], body[best.end():]


def parse(line, section):
    m = ENTRY.match(line)
    if not m:
        return None
    term = m.group("term").replace("\\*", "*").strip()
    body = m.group("body")
    links = []
    if " → " in body:
        body, tail = body.rsplit(" → ", 1)
        for lm in WIKILINK.finditer(tail):
            links.append({"path": lm.group(1).strip(), "anchor": (lm.group(2) or "")[1:],
                          "label": (lm.group(3) or lm.group(1).split("/")[-1]).strip().replace("\\", "")})
    en_def, ko_def = split_defs(body)

    names_en = []
    base = term
    pm = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", term)
    if pm:
        base, inner = pm.group(1).strip(), pm.group(2)
        parts = [p.strip() for p in inner.split(",")]
        # an alias looks like a name (has a capital letter or digit); a qualifier
        # such as "(filter)" or "(of a distribution)" is lower-case prose
        aliases = [p for p in parts if p and "$" not in p and len(p) >= 2
                   and re.search(r"[A-Z0-9]", p) and len(p.split()) <= 4]
        names_en.extend(aliases)
    names_en.insert(0, base)
    for piece in re.split(r"\s+/\s+|\s+·\s+", base):
        # a slash piece stands alone only if it is still a specific name
        if piece != base and len(piece) >= 5 and piece.lower() not in STOP:
            names_en.append(piece)

    ko = (m.group("ko") or "").strip()
    names_ko = []
    en_words = len(base.split())
    if ko and base.lower() not in STOP:
        kbase = re.sub(r"\([^()]*\)", "", ko).strip()
        for piece in re.split(r"\s*[/,]\s*", kbase):
            hangul = len(HANGUL.findall(piece))
            if hangul < 2 or piece in KO_STOP:
                continue
            # a two-syllable Korean word standing for a multi-word English term is
            # usually a generic word ("박스" for bounding box), so it is not matched
            if hangul <= 2 and en_words > 1:
                continue
            names_ko.append(piece)

    auto = " vs " not in term and "Confusable" not in section
    names_en = [n for n in dict.fromkeys(names_en)
                if len(n) >= 2 and "·" not in n and "$" not in n and n.lower() not in STOP]
    return {
        "term": plain(term),
        "ko": plain(ko),
        "en": plain(en_def),
        "kodef": plain(ko_def),
        "links": links,
        "match_en": names_en if auto else [],
        "match_ko": names_ko if auto else [],
    }


def build():
    section = ""
    entries = []
    for line in open(SRC, encoding="utf-8").read().split("\n"):
        if line.startswith("## "):
            section = line[3:]
        elif line.startswith("- **"):
            e = parse(line, section)
            if e:
                entries.append(e)
    return entries


def main():
    entries = build()
    data = json.dumps({"version": 1, "entries": entries}, ensure_ascii=False, separators=(",", ":"))
    if "--check" in sys.argv:
        try:
            cur = open(OUT, encoding="utf-8").read()
        except OSError:
            cur = ""
        if cur != data:
            print("glossary terms.json is stale: run python3 scripts/build_glossary_index.py")
            sys.exit(1)
        print(f"glossary terms.json up to date ({len(entries)} entries)")
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(data)
    print(f"wrote {OUT} ({len(entries)} entries, {len(data) // 1024} KB)")


if __name__ == "__main__":
    main()
