#!/usr/bin/env python3
"""Bilingual parity — section references that appear in one language half of
a page but not the other.

Imported by verify_content.py as check 13, and runnable on its own for a
readable report.  This wiki interleaves
bilingual pairs (an English line immediately followed by its Korean twin)
with blocks that are written once for both languages, so an `## English` /
`## 한국어` split does not cleanly separate the two languages everywhere.
Two structural patterns are filtered out below because they are known,
recurring, and not defects:

  * pages whose two headings are only preamble labels over a shared body
    (canonical-list.md) — detected by the length ratio of the two halves;
  * callouts written once for both languages (`> [!note] Prerequisites ·
    선수 지식`), which sit physically inside the English half.

With those filtered the wiki reports zero, so a flag means a real one-sided
edit.  It found one on its first run: ch13's Korean self-check answer 3 had
never received the enrichment the English answer got, including its
cross-reference to State Estimation §8 — the same failure mode as the
deployment-ladder fix that reached only the English half.

    python3 scripts/audit_parity.py        # from the repo root
"""
import re, os, glob, sys

HAN = re.compile(r"[가-힣]")
LAT = re.compile(r"[A-Za-z]")


def halves(text):
    e = re.search(r"^##\s*English\s*$", text, re.M)
    k = re.search(r"^##\s*한국어\s*$", text, re.M)
    if not e or not k or e.start() > k.start():
        return None
    en, kr = text[e.end():k.start()], text[k.end():]
    if len(kr) > 3 * max(len(en), 1):
        return None                      # preamble labels over a shared body
    return _drop_shared_callouts(en), _drop_shared_callouts(kr)


def _prose(line):
    """The line with wikilink targets and URLs removed.

    Language is decided on prose only. A wikilink *path* is always Latin
    (`04-robotics/contact-force-tactile`), and so is LaTeX ($0.90 \\times 0.02$),
    so counting either makes Korean lines full of links or arithmetic look
    English and defeats the shared-block filter.
    """
    line = re.sub(r"\[\[[^\]|]*\\?\|", "", line)     # [[path| → keep the label
    line = re.sub(r"\[\[[^\]]*\]\]", "", line)         # [[path]] → no label at all
    line = re.sub(r"\$\$.*?\$\$", "", line)             # display math is language-neutral
    line = re.sub(r"\$[^$]*\$", "", line)                # so is inline math
    return re.sub(r"https?://\S+", "", line)


def _drop_shared_callouts(half):
    """Remove callout blocks written once for both languages."""
    lines, out, i = half.split("\n"), [], 0
    while i < len(lines):
        if re.match(r"\s*>\s*\[!\w+\]", lines[i]):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                j += 1
            blk = lines[i:j]
            # The callout's own title is bilingual by convention ("Reading the
            # claim · 핵심 주장 읽는 법"), so it says nothing about which
            # languages the block's body serves. Test the body only.
            body = blk[1:]
            has_kr = any(HAN.search(_prose(l)) for l in body)
            has_en = any(LAT.search(_prose(l)) and not HAN.search(_prose(l)) for l in body)
            if not (has_kr and has_en):   # both languages present ⇒ shared
                out += blk
            i = j
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def section_refs(text):
    text = re.sub(r"<svg.*?</svg>", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    found = set()
    for m in re.finditer(r"\[\[([^\]|#]+)(?:\\?\|([^\]]*?))?\]\]", text):
        target = os.path.basename(m.group(1).split("#")[0].strip().rstrip("\\"))
        for s in re.findall(r"§\s*(\d+(?:\.\d+)?)", m.group(2) or ""):
            found.add((target, s))
    return found


def main():
    if not os.path.isdir("content"):
        sys.exit("run this from the repo root (content/ not found)")
    flagged = 0
    for path in sorted(glob.glob("content/**/*.md", recursive=True)):
        h = halves(open(path, encoding="utf-8").read())
        if not h:
            continue
        en, kr = section_refs(h[0]), section_refs(h[1])
        if en == kr:
            continue
        flagged += 1
        print(f"[{os.path.relpath(path, 'content')}]")
        if en - kr:
            print("   English only:", sorted(en - kr))
        if kr - en:
            print("   Korean only: ", sorted(kr - en))
    print(f"\n{flagged} page(s) whose two halves cite different sections.")


if __name__ == "__main__":
    main()
