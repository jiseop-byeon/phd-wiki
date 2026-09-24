---
title: "12.6 Writing Tools: LaTeX, Figures and References"
tags: [foundations, tools, writing]
study-depth: Working
wiki-support: Working
depth-goal: "On RS1's paper, say what each LaTeX run and the BibTeX step read and write and why a first run prints ?? and [?]; predict where a figure or table floats; plan a figure for its column - print scale, printed text size, the pixels a raster needs, vector against raster file size; write a BibTeX entry with its DOI from the publisher's page; and print a table's numbers to the digits their uncertainty supports."
mastery-when: "Raise when the thesis itself is being typeset, or when a venue's template, figure checks or reference style start to cost days."
---

> [!note] Prerequisites · 선수 지식
> [[06-research-practice/index|6. Research Practice — RS1]] (the frozen study: its question, trial and twenty pilot forces, restated below) · [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]] (what RS1's paper says: its Table 1 from the worked case and its Figure 1 from §4 — this page typesets them and changes nothing they claim) · [[02-foundations/ml-practice|9. ML Practice §4]] (standard deviation, standard error and confidence interval: which of the three an error bar shows). Nothing has to be installed to follow the page: its LaTeX was checked against the documentation cited, not compiled (§1), and its one runnable listing uses the Python standard library.
> [[06-research-practice/index|6. 연구 실무 — RS1]](고정된 연구: 질문, 시행, 예비 실험의 힘 스무 개. 아래에 다시 적는다) · [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사]](RS1 논문이 말하는 것: 끝까지 계산의 표 1과 §4의 그림 1. 이 페이지는 그것을 조판할 뿐 주장은 하나도 바꾸지 않는다) · [[02-foundations/ml-practice|9. ML 실무 §4]](표준편차, 표준오차, 신뢰구간 — 오차 막대가 셋 중 무엇을 보이는가). 따라가는 데 설치할 것은 없다. 이 페이지의 LaTeX는 컴파일하지 않고 인용한 문서와 대조했으며(§1), 실행하는 코드 하나는 Python 표준 라이브러리만 쓴다.

## English

*Stands on RS1, the study every page of [[06-research-practice/index|6. Research Practice]] shares, and on [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]], which decided what RS1's paper claims and built its Table 1 and Figure 1. This page is the workshop behind that paper: the program that turns its source into a PDF, the rules that move its figure, the file the figure is saved as, the size its text prints at, the database its references come from, and the digits its table prints.*

> [!note] Why this matters · 왜 배우는가
> This page is part of the floor beneath the physical-AI stack of [[07-research-program/index|research program §5]] — the tools, beside research practice (its place is marked on the [[physical-ai-map|Physical AI Map]]). In that section's worked instance, "Install that panel on the frame", it performs none of the eight steps; it carries the evidence about them — RS1's peak forces when the arm meets the panel, and in the end whether the panel seated, counted over trials — to a reader, as a figure, a table and a list of references. Get the tools wrong and a correct experiment is misreported: RS1's Figure 1 drawn at matplotlib's default prints its labels at 5.47 pt, a table that prints 10.6600 N claims a precision ten trials cannot support, and a citation key typed in the wrong case prints [?] after every build. [[06-research-practice/scientific-writing-peer-review|Research practice 4 §4]] decides what the figure and the table must show and [[06-research-practice/experimental-design-reproducibility|research practice 2 §7]] what the repository must record; this page sits outside the seven blocks of the dissertation path ([[07-research-program/index|research program §8]]), so take it with research practice 4 — its worked case in block 5, the rest in block 8 — and at the latest before the first draft of a paper. After it you can carry a result from data to a submitted PDF: a figure planned for its column, a table printed to the digits its uncertainty supports, references built from their DOIs, and a build whose log is clean.

> [!note] First pass · 처음이라면
> Two sessions of about 90 minutes. **Session 1 — the build and the figure.** Look at the picture, read §1 and §2, then cover the run table in §1 and rebuild it from memory: what each of the four steps reads and writes, and what the PDF shows after each. Then read §6 and §7 and work Steps 1–4 of the Worked case with a calculator before reading them. End with Self-check 1, 3 and 5. **Session 2 — the paper around the figure.** Read §5, §8 and §9, work Steps 5–6, and answer Self-check 2 and 6. After that, open §3 when a figure floats somewhere unexpected, §4 before you start from a new template and §10 before a co-author first edits the paper, and do the problem set last. Every *Deeper* callout can wait.

### Running object · 이 페이지의 대상

**RS1**, the running study of [[06-research-practice/index|6. Research Practice]], restated so that this page can be read alone. *Question:* does impedance control (**B**) make the contact of the planar arm **P2** of [[02-foundations/lab-plants|0.6 Lab Plants]] with a 400 N/m panel safer than position control with a force-threshold stop (**A**)? *Trial:* one approach that ends in contact; a success when the peak contact force is at most 10 N. *Pilot*, illustrative and frozen, ten unpaired trials per arm — A: 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 N, so 6/10, mean 10.66 N, sample sd 2.414 N; B: 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 N, so 9/10, mean 7.50 N, sd 1.356 N. *Main study:* planned at 32 trials per arm.

The object of this page is **RS1's paper** — three of its parts, each already decided by [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]]:

- **Figure 1**, the print version in page 4's §4: every trial's peak force as a dot, A's ten on one row and B's below, the 10 N line fixed before the pilot, and each arm's mean with its 95% t-interval, A 10.66 N [8.93, 12.39] and B 7.50 N [6.53, 8.47]. Counted in page 4's drawing, it is **61 drawn elements** — 20 dots, 19 lines, 19 pieces of text, 2 diamonds and a shaded band.
- **Table 1**, from page 4's worked case: A − B = 3.16 N with its Welch 95% interval [1.28, 5.04] N, and the success rates 6/10 and 9/10 with their Wilson 95% intervals [0.31, 0.83] and [0.60, 0.98].
- **One reference**, followed from the publisher's page to the printed "[1]": Weissgerber et al. (2015), which page 4 cites for showing every trial as a point rather than a bar.

On top of RS1 the page freezes a course template and the costs of a figure file. **These are this page's own course numbers, chosen for clean arithmetic — not measurements, and not any real venue's specification**; a real venue's template gives the real values (§4).

| Symbol | Value | What it is |
|---|---:|---|
| $W$, $g$ | 7.25 in, 0.25 in | text width of the two-column page, and the gap between its columns |
| $w$ | 3.5 in | column width, $(W-g)/2$ — derived (§1) |
| $H$ | 9.0 in | text height: the height of each column |
| $f_{\min}$ | 8 pt | smallest size a figure's text may print at — the size of the template's captions |
| $h_{\text{fig}}$, $h_{\text{cap}}$ | 1.5 in, 0.5 in | height planned for Figure 1, and for its caption with the space around it |
| $r$ | 600 dpi | resolution the course venue asks of a raster plot (300 dpi for a photograph) |
| $F_0$ | 20,000 bytes | fixed part of a vector PDF figure: file structure and an embedded font subset |
| $b_{\text{obj}}$, $b_{\text{vtx}}$ | 100, 15 bytes | cost to a vector file of one more drawn object, and of one more vertex of a long path |
| trace | 1 kHz for 2 s | the main study's force record per trial, 2,000 samples (§6) |

Two numbers are facts about the tools, not course numbers: LaTeX's standard classes set text at 10 pt, and matplotlib starts every figure at 6.4 × 4.8 in and 100 dpi with 10-pt text — the defaults the first draft of Figure 1 was made with.

*Scope: this page teaches the tools that carry RS1's claim into a submitted paper — LaTeX as a compiler, with its runs, cross-references and floats; packages and a venue's template; BibTeX, a reference manager and DOIs; figures that survive their column; tables whose digits match their uncertainty; and the paper kept in a Git repository. What the paper should say is [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]], the statistics behind its numbers [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]], and where to send it [[06-research-practice/venue-strategy|5. Venue Strategy]]; §11 lists what else is left out.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 274" style="max-width:100%;height:auto" role="img" aria-label="RS1's Figure 1 planned for a 3.5-inch column. (a) The column to scale: the draft, drawn at matplotlib's default 6.4 by 4.8 inches, is scaled by 0.547 to 2.63 inches tall, 3.13 inches with its caption, and its 640 pixels spread to 183 dots per inch; the final version, drawn at 3.5 by 1.5 inches, prints at scale 1.00 and takes 2.00 inches with its caption. (b) The draft's 10-point text prints at 5.47 points, under the course minimum of 8; the final prints at 8. (c) File size on a log scale: the drawing as a vector PDF, 26.1 kilobytes, against raw rasters of 1.42 megabytes at 300 and 5.67 megabytes at 600 dots per inch.">
<text x="16" y="18" font-size="12" fill="currentColor">(a) RS1's Figure 1 in the 3.5-in column, to scale</text>
<rect x="20" y="34" width="112" height="84" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
<line x1="34" y1="111" x2="126" y2="111" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="34" y1="111" x2="34" y2="114" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="80" y1="111" x2="80" y2="114" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="126" y1="111" x2="126" y2="114" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="80" y1="37" x2="80" y2="111" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 2" stroke-opacity="0.8"/>
<circle cx="58.8" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="62.5" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="71.7" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="74.5" cy="59.1" r="1.7" fill="currentColor"/>
<circle cx="78.2" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="79.1" cy="59.1" r="1.7" fill="currentColor"/>
<circle cx="92" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="103.9" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="115.9" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="124.2" cy="57.1" r="1.7" fill="currentColor"/>
<line x1="70.2" y1="67.9" x2="102" y2="67.9" stroke="currentColor" stroke-width="1"/>
<path d="M86.1 65.7l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="23" y="60.6" font-size="10" fill="currentColor">A</text>
<circle cx="42.3" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="45" cy="83.7" r="1.7" fill="currentColor"/>
<circle cx="48.7" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="50.6" cy="83.7" r="1.7" fill="currentColor"/>
<circle cx="53.3" cy="79.7" r="1.7" fill="currentColor"/>
<circle cx="57" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="60.7" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="61.6" cy="83.7" r="1.7" fill="currentColor"/>
<circle cx="65.3" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="85.5" cy="81.7" r="1.7" fill="currentColor"/>
<line x1="48.1" y1="92.5" x2="65.9" y2="92.5" stroke="currentColor" stroke-width="1"/>
<path d="M57 90.3l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="23" y="85.2" font-size="10" fill="currentColor">B</text>
<rect x="20" y="121" width="112" height="10" fill="currentColor" fill-opacity="0.16"/>
<rect x="20" y="137" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="144" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="151" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="158" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="165" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="172" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<path d="M20 185H132 M20 187v-4 M132 187v-4" stroke="currentColor" stroke-width="0.8" fill="none" stroke-opacity="0.7"/>
<text x="76" y="197" font-size="10" text-anchor="middle" fill="currentColor">3.5 in</text>
<path d="M135 34h3V134h-3" stroke="currentColor" stroke-width="0.8" fill="none"/>
<text x="20" y="211" font-size="10" fill="currentColor" font-weight="bold">draft</text>
<text x="20" y="224" font-size="10" fill="currentColor">drawn 6.4 × 4.8 in</text>
<text x="20" y="237" font-size="10" fill="currentColor">×0.547 → 2.63 in tall</text>
<text x="20" y="250" font-size="10" fill="currentColor">+ caption: 3.13 in = 0.35 H</text>
<text x="20" y="263" font-size="10" fill="currentColor">640 px → 183 dpi</text>
<rect x="162" y="34" width="112" height="48" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
<line x1="176" y1="75" x2="268" y2="75" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="176" y1="75" x2="176" y2="78" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="222" y1="75" x2="222" y2="78" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="268" y1="75" x2="268" y2="78" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="222" y1="37" x2="222" y2="75" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 2" stroke-opacity="0.8"/>
<circle cx="200.8" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="204.5" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="213.7" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="216.5" cy="48.3" r="1.7" fill="currentColor"/>
<circle cx="220.2" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="221.1" cy="48.3" r="1.7" fill="currentColor"/>
<circle cx="234" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="245.9" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="257.9" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="266.2" cy="46.3" r="1.7" fill="currentColor"/>
<line x1="212.2" y1="52" x2="244" y2="52" stroke="currentColor" stroke-width="1"/>
<path d="M228.1 49.8l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="165" y="49.8" font-size="10" fill="currentColor">A</text>
<circle cx="184.3" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="187" cy="61.4" r="1.7" fill="currentColor"/>
<circle cx="190.7" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="192.6" cy="61.4" r="1.7" fill="currentColor"/>
<circle cx="195.3" cy="57.4" r="1.7" fill="currentColor"/>
<circle cx="199" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="202.7" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="203.6" cy="61.4" r="1.7" fill="currentColor"/>
<circle cx="207.3" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="227.5" cy="59.4" r="1.7" fill="currentColor"/>
<line x1="190.1" y1="65.2" x2="207.9" y2="65.2" stroke="currentColor" stroke-width="1"/>
<path d="M199 63l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="165" y="62.9" font-size="10" fill="currentColor">B</text>
<rect x="162" y="85" width="112" height="10" fill="currentColor" fill-opacity="0.16"/>
<rect x="162" y="101" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="108" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="115" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="122" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="129" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="136" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="143" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="150" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="157" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="164" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="171" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<path d="M162 185H274 M162 187v-4 M274 187v-4" stroke="currentColor" stroke-width="0.8" fill="none" stroke-opacity="0.7"/>
<text x="218" y="197" font-size="10" text-anchor="middle" fill="currentColor">3.5 in</text>
<path d="M277 34h3V98h-3" stroke="currentColor" stroke-width="0.8" fill="none"/>
<text x="162" y="211" font-size="10" fill="currentColor" font-weight="bold">final</text>
<text x="162" y="224" font-size="10" fill="currentColor">drawn 3.5 × 1.5 in</text>
<text x="162" y="237" font-size="10" fill="currentColor">×1.00 → 1.50 in tall</text>
<text x="162" y="250" font-size="10" fill="currentColor">+ caption: 2.00 in = 0.22 H</text>
<text x="162" y="263" font-size="10" fill="currentColor">vector: no pixels</text>
<text x="300" y="18" font-size="12" fill="currentColor">(b) printed text size (pt)</text>
<text x="306" y="38" font-size="10.5" fill="currentColor">draft, as drawn</text>
<rect x="306" y="41" width="180" height="9" fill="currentColor" fill-opacity="0.18"/>
<text x="494" y="49" font-size="10.5" fill="currentColor">10</text>
<text x="306" y="62" font-size="10.5" fill="currentColor">draft, printed (×0.547)</text>
<rect x="306" y="65" width="98.4" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="412.4" y="73" font-size="10.5" fill="currentColor">5.47</text>
<text x="306" y="86" font-size="10.5" fill="currentColor">final, printed (×1.00)</text>
<rect x="306" y="89" width="144" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="458" y="97" font-size="10.5" fill="currentColor">8.00</text>
<line x1="450" y1="36" x2="450" y2="104" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="450" y="116" font-size="10" text-anchor="middle" fill="currentColor">min 8 pt</text>
<line x1="306" y1="104" x2="486" y2="104" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="306" y1="104" x2="306" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="306" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">0</text>
<line x1="342" y1="104" x2="342" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="342" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">2</text>
<line x1="378" y1="104" x2="378" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="378" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">4</text>
<line x1="414" y1="104" x2="414" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="414" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">6</text>
<text x="300" y="140" font-size="12" fill="currentColor">(c) file size, log scale</text>
<text x="306" y="158" font-size="10.5" fill="currentColor">vector PDF (course numbers): 26.1 kB</text>
<rect x="306" y="161" width="30" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="306" y="184" font-size="10.5" fill="currentColor">raster 300 dpi, 1050 × 450 px: 1.42 MB</text>
<rect x="306" y="187" width="154.9" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="306" y="210" font-size="10.5" fill="currentColor">raster 600 dpi, 2100 × 900 px: 5.67 MB</text>
<rect x="306" y="213" width="198.3" height="9" fill="currentColor" fill-opacity="0.7"/>
<line x1="306" y1="232" x2="522" y2="232" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="306" y1="232" x2="306" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="306" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">10 kB</text>
<line x1="378" y1="232" x2="378" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="378" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">100 kB</text>
<line x1="450" y1="232" x2="450" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="450" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">1 MB</text>
<line x1="522" y1="232" x2="522" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="522" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">10 MB</text>
</svg>

RS1's Figure 1 on its way into the course template's 3.5-in column. Left, to scale: drawn at matplotlib's default 6.4 × 4.8 in, the draft shrinks by 0.547, takes 3.13 in of the column with its caption and spreads its 640 pixels to 183 dpi, while the final version, drawn at 3.5 × 1.5 in, prints at scale 1.00 in 2.00 in. Right: the draft's 10-pt text prints at 5.47 pt, under the course minimum of 8 pt, and the same drawing costs 26.1 kB as a vector PDF against 1.42 MB and 5.67 MB as raw 300- and 600-dpi rasters (course numbers, §6).

### 1. A LaTeX build: from source to a settled PDF

*In one sentence:* LaTeX compiles plain-text source into a PDF, and because each run can use only what the previous run wrote down, a paper with references and citations needs several runs before its numbers settle.

**The problem.** A co-author opens the first PDF of RS1's paper and finds "Fig. ??" and "[?]" where the figure number and the citation should be. The text is fine; the PDF is the first of several passes.

**The idea.** A LaTeX paper is **source** that a program compiles, the way code is compiled — not a document arranged on the page. RS1's paper is a few plain-text files: `main.tex` with the text and layout commands, `refs.bib` with the reference entries, and one file per figure. Invoked as `pdflatex`, the engine writes the PDF (LaTeX2e reference manual §2.3) and, beside it, a **`.log`** transcript of the run and an **`.aux`** file of auxiliary information for cross-references (manual §2.2). The catch is timing: a run reads the `.aux` file that the *previous* run wrote. When the first run meets `\ref{fig:peak}` it does not yet know Figure 1's number, so it prints **??** and writes the number down for next time. Citations need one more program, BibTeX, to turn cited keys into a formatted list, and one more run to print their labels. The working loop is therefore edit, compile, and read both the PDF and the log.

The **document class** sets the page. RS1's draft uses `article` with the `twocolumn` option — 10-pt text on US-letter paper by default (manual §3.1), each column half of the text width left after the gap (manual §5.2):

```latex
% main.tex - RS1's paper, reduced to what this page follows. Not compiled here (see below).
\documentclass[twocolumn]{article}   % 10 pt text and US letter are the class defaults
\usepackage{amsmath}                 % align, equation* (section 2)
\usepackage{graphicx}                % \includegraphics (sections 4 and 7)
\usepackage{booktabs}                % \toprule, \midrule, \bottomrule (section 9)
\usepackage{siunitx}                 % \qty, \unit (section 4)

\begin{document}
\section{Experiments}\label{sec:exp}
Fig.~\ref{fig:peak} shows every pilot trial as a point rather than a bar,
as recommended in~\cite{weissgerber2015}. The main study logs each trial's
force trace at \qty{1}{\kilo\hertz}.

\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{rs1_fig1}
  \caption{RS1 pilot (illustrative data): peak contact force of every trial.}
  \label{fig:peak}
\end{figure}

\bibliographystyle{IEEEtran}
\bibliography{refs}                  % refs.bib, named without its extension
\end{document}
```

**The rule, on RS1's draft.** Four steps, and what each leaves in the PDF (the sequence Overleaf's *Bibliography management with bibtex* walks through):

| step | reads | writes | the PDF shows |
|---|---|---|---|
| `pdflatex main` | `main.tex` | `main.aux`: the labels and the cited keys | "Fig. ??", "[?]", no reference list |
| `bibtex main` | `main.aux`, `refs.bib`, the style IEEEtran | `main.bbl`: the formatted list | — |
| `pdflatex main` | `main.tex`, `main.aux`, `main.bbl` | `main.aux`, now with the list's labels | "Fig. 1", the reference list, still "[?]" |
| `pdflatex main` | the same | `main.aux`, unchanged | "Fig. 1", "[1]" |

```bash
# not run here: no LaTeX distribution is installed on this machine; the sequence is Overleaf's (bibtex page)
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

> **A LaTeX build, defined.** A **LaTeX build** is *a sequence of program runs over a fixed set of source files that ends when a further run would change nothing* — a process, not one command, and not the PDF it leaves. Four conditions: (1) each engine run reads the source **and the auxiliary files the previous run wrote**, and writes new ones; (2) when the paper cites anything, a **bibliography step** — BibTeX, or Biber for biblatex (§5) — runs between engine runs; (3) the **source is held fixed** throughout, and an edit starts the sequence again; (4) the build is **settled** once a run writes the same auxiliary data it read.
>
> $$\text{PDF}_n=E\big(\text{source},\ \text{aux}_{n-1},\ \text{bbl}\big),\qquad \text{settled at the first } n \text{ with } \text{aux}_n=\text{aux}_{n-1}$$
>
> where $E$ is the engine, $\text{aux}_{n-1}$ what run $n-1$ wrote (nothing before the first run) and bbl the bibliography step's output — so a paper whose labels all exist settles in two engine runs, and one that also cites in the four steps of the table.
>
> - **Example**: RS1's draft settles after the four steps; a fifth would print the identical PDF.
> - **Non-example**: a PDF still showing "[?]" after all four steps. The build *has* settled; the key is missing from `refs.bib` (§5), no further run can fix it, and the log's "undefined citation" warning names the key.
> - **Why it matters**: a submitted PDF must come from a settled build whose log has no undefined references or citations. Overleaf runs the sequence for you — its documentation says cross-references work immediately there — while a local build is your job.

**The traps.** A PDF from a single run, mailed round with "??" in it, is unfinished, not broken: build to the end before anyone reads it. And a warning, unlike an error, lets the run finish with a PDF that looks fine — so a build is checked in its log, not in its PDF.

**No LaTeX was compiled for this page:** the machine's one TeX engine (Tectonic) has no local copy of the packages and would have to download them, which this wiki's rules forbid; every LaTeX listing was checked against the documentation in the Sources instead.

### 2. Cross-references and equations

*In one sentence:* LaTeX numbers sections, equations, figures and tables itself, and a `\label` placed right after the thing it names lets `\ref` print that number anywhere, one run later.

**The problem.** RS1's text says "Fig. 1" in four places. A reviewer asks for a photograph of the rig before it, and the dot plot becomes Figure 2: typed numbers would now be wrong in four places, silently.

**The idea.** Never type a number LaTeX assigns. Name the thing with `\label{fig:peak}` and write `\ref{fig:peak}` wherever its number is needed; when the numbering changes, every reference follows as soon as the build settles again.

> **A cross-reference, defined.** A **cross-reference** is *a name for a number LaTeX assigns — to a section, equation, figure or table — resolved one run late through the `.aux` file*: a pointer, not the number. Four conditions: (1) `\label{key}` stands **right after the command that sets the number**, in the same environment — after `\caption` in a float, after `\section` (TeX FAQ, *LaTeX gets cross-references wrong*); (2) the **key is unique**; (3) `\ref{key}` prints the number **the previous run recorded**; (4) with no record it prints **??** and the log warns (manual §2.2).
>
> $$\text{ref}_n(k)=\begin{cases}\text{num}_{n-1}(k) & \text{if run } n-1 \text{ recorded } k\\ \text{??} & \text{otherwise}\end{cases}$$
>
> where $k$ is the key and $\text{num}_{n-1}$ the number run $n-1$ wrote into the `.aux` file — so a reference can go wrong only by being undefined, which the log reports, or by breaking condition (1), which it does not.
>
> - **Example**: `\label{fig:peak}` right after Figure 1's `\caption`. Add the rig photograph before it: the first run after the edit still prints "Fig. 1" — it reads the old `.aux` — while recording 2, and the next run prints "Fig. 2" in all four places.
> - **Non-example**: `\label{fig:peak}` *before* the `\caption`. It records the number of the section the figure sits in (TeX FAQ), so with the figure in Section 4 the text says "Fig. 4" — with no warning, because the reference is defined, only to the wrong thing.
> - **Why it matters**: a typed "Figure 1" goes stale without a sound; a reference cannot go stale, only undefined, and then the log says so.

**Equations, on RS1.** **Inline** math sits in a line of text between `\(` and `\)`, or between single dollar signs (Overleaf). **Display** math stands on its own line: `\[ … \]` is unnumbered and `equation` numbered; for lines that must align, amsmath's `align` numbers each line and `align*` none, with `&` marking where the lines align and `\\` ending each line (Overleaf, *Aligning equations with amsmath*). RS1's Method states the interval its Table 1 reports:

```latex
The difference of means is reported with Welch's 95\% interval,
\begin{align}
  \mathrm{SE} &= \sqrt{s_A^2/n_A + s_B^2/n_B}, \label{eq:se}\\
  \bar{y}_A - \bar{y}_B &\pm t_{0.975,\nu}\,\mathrm{SE}, \label{eq:ci}
\end{align}
whose values for the pilot are in Table~\ref{tab:pilot}.
```

For the pilot the lines evaluate to $\mathrm{SE}=0.876$ N and $3.16\pm1.88=[1.28,\ 5.04]$ N, page 4's numbers. Each line has its own label, so "Eq.~\ref{eq:ci}" stays right wherever the equations move.

**The trap:** a label before its caption compiles cleanly, raises no warning and prints a plausible wrong number. When a figure reference looks too large, check the order of `\caption` and `\label` first.

> [!note]- Deeper · 더 깊이
> - Write `Fig.~\ref{fig:peak}`: `~` is LaTeX's non-breakable space (TeX FAQ, *Defining characters as macros*), so "Fig." and its number never land on different lines.
> - Name keys by kind — `fig:`, `tab:`, `eq:`, `sec:` — so a reference to the wrong kind of thing reads wrong in the source before it prints wrong.
> - If a caption sits inside an environment of its own, its label must be inside that environment too (TeX FAQ).

### 3. Floats: why figures and tables move

*In one sentence:* a figure or table cannot be split across pages, so LaTeX takes it out of the text and puts it at the first place its rules allow — often the top of a later column.

**The problem.** Figure 1 is written in the middle of the Results paragraph, and in the PDF it sits at the top of the next column. Nobody asked for that, and the sentence "the figure below" is now false.

**The idea.** A figure cut in half by a page break would be useless, so LaTeX sets figures and tables outside the running text, as **floats**, and moves each to the first place it fits whole — the top of a later page, for instance (manual §5.7). The optional argument of `figure` or `table` lists where it may go: `t`, the top of a text page; `b`, the bottom; `h`, here, where the environment appears; `p`, a separate page of floats. The default in `article` is `tbp`, and `h` alone is not allowed: LaTeX adds `t` (manual §5.7), with the warning Overleaf's documentation lists, "'h' float specifier changed to 'ht'". Floats of one kind also **keep their order** (manual §5.7), so one figure that cannot be placed holds back every figure after it.

> **A float, defined.** A **float** is *a box — a figure or table with its caption — that LaTeX keeps out of the running text and places at the first position its rules allow*: a placement problem the engine solves, not a position the author picks. Four conditions: (1) it **cannot be broken** across pages or columns; (2) it goes only where its **placement specifier** allows, `tbp` by default; (3) it **keeps its order** among floats of its kind; (4) on a text page it obeys the **fraction limits** below, unless `!` lifts them for that one float (manual §5.7):
>
> $$\sum_{\text{top}} h_i\le 0.7\,H,\qquad \sum_{\text{bottom}} h_i\le 0.3\,H,\qquad h_{\text{text}}\ge 0.2\,H,\qquad \sum_{\text{float page}} h_i\ge 0.5\,H$$
>
> where $h_i$ is a float's height with its caption, $H$ the text height and $h_{\text{text}}$ the text left on a page that carries floats — so on the course template, with $H=9.0$ in, floats at a page's top may add up to 6.3 in, and a page of floats must hold at least 4.5 in of them.
>
> - **Example**: Figure 1 with `[t]`: $1.5+0.5=2.0$ in, $0.22H$, well inside the top area, so it lands at the top of the column where its environment falls — even above the sentence that introduces it — or of the next column.
> - **Non-example**: `\begin{figure}[h]` under "the figure below". `h` alone becomes `ht`, the figure floats to a top, and "below" becomes false.
> - **Why it matters**: a figure is seldom where it was written, so the text points at it with `\ref`, never by position, and its height decides where it can go at all.

**On RS1.** A figure as wide as the page, `figure*`, spans both columns; LaTeX puts it only at the top of a page or on a page of floats, never at the bottom (manual §5.7; TeX FAQ). Problem 1 plans Figure 1 that way.

**The traps.** Writing "below" about a float; forcing a place with the `float` package's `H`, which pins the figure where it is written (Overleaf) so that it stops being a float and the page breaks around it however badly; and one oversized figure early on, holding back every later one.

> [!note]- Deeper · 더 깊이
> The limits are parameters with documented defaults (manual §5.7; TeX FAQ, *Moving tables and figures in LaTeX*): `\topfraction` 0.7, `\bottomfraction` 0.3, `\textfraction` 0.2, `\floatpagefraction` 0.5; at most 2 floats at a page's top, 1 at its bottom and 3 on one text page (`topnumber`, `bottomnumber`, `totalnumber`); `\dbltopfraction` 0.7 for full-width floats. The `flafter` package stops a float appearing above the text that defines it (TeX FAQ). `\clearpage` starts a new page and puts out every waiting float (manual §5.7); a long backlog ends in the error "Too many unprocessed floats" (TeX FAQ).

### 4. Packages and templates

*In one sentence:* a package adds commands to LaTeX and a template fixes a venue's page, so a paper loads the few packages it uses and starts from the venue's own template.

**The problem.** Plain LaTeX has no command for a table rule or a unit, and every venue wants its own page. Both come as files other people wrote; the skill is choosing few and changing none.

**The idea.** A **package** is loaded with `\usepackage{name}` before `\begin{document}`. RS1's paper loads five, each checked on its CTAN page:

| package | what RS1's paper uses it for |
|---|---|
| amsmath | `align`, `align*`, `equation*` (§2); the principal AMS-LaTeX package, in LaTeX's required set |
| graphicx | `\includegraphics` with `width`, `height`, `scale`, `angle`; given only a width, the height keeps the aspect ratio (Overleaf) |
| booktabs | `\toprule`, `\midrule`, `\bottomrule`, a table's three rules (§9) |
| siunitx | a number and its unit as one quantity, `\qty{1}{\kilo\hertz}`, and alignment of numbers in table columns; version 3's `\qty` and `\unit` replace `\SI` and `\si`, which still work (Overleaf's TeX Live 2021 announcement) |
| biblatex (with Biber) | the bibliography, if the template uses it rather than BibTeX (§5) |

A **template** is the file a venue gives its authors: a document class, usually with a bibliography style, and a sample paper. For IEEE's journals and conferences it is **IEEEtran**, a class with its own BibTeX style (CTAN, version 1.8b), shipped with sample papers such as `bare_conf.tex` and `bare_jrnl.tex`.

**The rule.** Start from the venue's own template file and change none of its layout — the venue's format rules are written for it — and read the page's real dimensions from it: `\the\columnwidth` typesets the current column width in points (TeX FAQ, *How to print contents of variables*).

**On RS1.** For the course template's 3.5-in column that would print about 252.9 pt, since a TeX point is $1/72.27$ in, about 0.3515 mm (Overleaf, *Lengths in LaTeX*). Dividing the printed width by 72.27 gives the inches the plotting script of §7 needs.

**The trap.** Squeezing a paper into its page limit by shrinking the template's margins or font: the page fits, and the paper no longer meets the format it will be checked against.

**Where the build runs.** Overleaf is a hosted editor: its documentation describes a LaTeX editor and collaboration platform that compiles on Overleaf's servers, with nothing to install. pdfLaTeX is its default compiler, beside LaTeX, XeLaTeX and LuaLaTeX, and each project picks its TeX Live version. Full project history, track changes, the Git integration and the Zotero link are premium features; on the free plan the history shows only the last 24 hours and any labelled versions (§10).

> [!note]- Deeper · 더 깊이
> matplotlib's point is $1/72$ in (matplotlib, *Transformations tutorial*) and TeX's $1/72.27$ in, a difference of $72.27/72-1=0.375\%$: harmless for legibility, but it is why 3.5 in is 252.9 TeX points and 252 matplotlib points. Packages load in order and can clash; when two define the same command the log names it — one more reason to load only what the paper uses.

### 5. References: BibTeX, a reference manager and DOIs

*In one sentence:* the reference list is computed, not typed — every `\cite{key}` is looked up in a `.bib` database, a style formats what it finds, and a key that is not there prints as [?].

**The problem.** A reference list typed by hand drifts — a year copied wrong, an entry nobody cites any more, numbers that stop matching the text when a paragraph moves — and with forty references and three co-authors it will.

**The idea.** Keep references as data and let the build write the list. A `.bib` file is a small database; each **entry** has a type — `@article`, `@inproceedings`, `@book` — a **citation key**, the name `\cite` uses, and fields such as `author`, `title`, `journal`, `year`, with several authors joined by `and`, each written `Lastname, Firstname` (Overleaf, *Bibliography management with bibtex*). The text cites by key, `\cite{weissgerber2015}`; `\bibliographystyle{IEEEtran}` names the style and `\bibliography{refs}` the database, without its `.bib` extension; BibTeX, run between the LaTeX runs of §1, keeps the cited entries and formats them in the style's order and look.

> **A bibliography entry and its key, defined.** A **bibliography entry** is *a record in a `.bib` database — a type, a key and fields — that a paper cites by its key*; the key is a lookup name, not a label that prints. Four conditions: (1) the **key is unique** and matches the cited key **exactly, case included**; (2) the **type** tells the style which fields to expect; (3) the **printed list is computed** — exactly the entries whose keys the text cites; (4) a cited key **absent** from the database prints as [?], with an "undefined citation" warning in the log.
>
> $$L=\{\,e\in\text{bib}:\ \text{key}(e)\in C\,\},\qquad U=C\setminus\text{keys}(\text{bib})$$
>
> where $C$ is the set of keys the text cites, $L$ the printed list and $U$ the keys that print as [?] — so an entry nobody cites never prints, and a key in $U$ stays [?] however many times the build runs.
>
> - **Example**: RS1's text cites `weissgerber2015`, which `refs.bib` holds, so $U$ is empty and IEEEtran's numeric style prints [1]. The Worked case builds the entry from the publisher's page.
> - **Non-example**: `\cite{Weissgerber2015}` against the key `weissgerber2015`. Keys are case-sensitive (Overleaf), so the cited key is in $U$: [?] after any number of runs.
> - **Why it matters**: the list cannot print an uncited entry or miss a cited one that exists — but it cannot tell a typo from a missing paper, and only the log lists the keys it could not find.

**The traps.** *Case in keys*: this page's convention is the first author's surname in lower case plus the year, `weissgerber2015`, with a letter added for a second paper by the same author that year. *Styles recase titles*: BibTeX's standard styles impose their own capitalisation, so a word that must keep its capitals goes in braces, a whole word at a time — `{RS1}`, `{ROS}` — never the entire title (TeX FAQ, *Capitalisation in BibTeX*); a sentence-case style prints "Force limits for the RS1 arm" as "Force limits for the rs1 arm" unless the source says `{RS1}`. *A style prints only the fields it knows*: `plain` ignores a `url` that IEEEtran prints (Overleaf), so check the compiled list before assuming a DOI is in it.

**A reference manager** keeps the library the `.bib` file comes from: Zotero exports BibTeX and BibLaTeX (Zotero, *Bibliographic Data Formats*) — right-click a collection, *Export Collection…* (Zotero, *How do I export my Zotero library?*). Keys can change between exports (Overleaf warns of it after Zotero updates), so the exported `.bib` is committed with the paper (§10) and the log is read for undefined citations after every re-export.

**A DOI** is a persistent identifier — a prefix and a suffix separated by a slash — resolved through `https://doi.org/` to the object's current location (DOI Foundation, *What is a DOI?*). Weissgerber et al.'s is `10.1371/journal.pbio.1002128`: prefix `10.1371`, suffix `journal.pbio.1002128`. Crossref's display guidelines, in force since March 2017, print it as a full link, `https://doi.org/10.1371/journal.pbio.1002128`, never after "doi:" and never with "dx" in the domain. A DOI outlives a publisher's web address, so an entry's metadata is taken from the page its DOI resolves to — not from a search result or another paper's reference list, where errors are copied from paper to paper.

> [!note]- Deeper · 더 깊이
> **BibTeX or biblatex.** BibTeX is the older route and the one IEEEtran's style uses; its standard styles include `plain`, `unsrt`, `alpha`, `abbrv` and `ieeetr`, and `\nocite{*}` prints the whole database (Overleaf). It handles text as bytes and knows no Unicode sorting (CTAN). biblatex is the newer route — `\usepackage[backend=biber]{biblatex}`, `\addbibresource{refs.bib}` *with* the extension, and `\printbibliography` where the list goes; its formatting lives in LaTeX macros, and its backend Biber reads UTF-8 and sorts by Unicode rules (CTAN). Overleaf's documentation recommends biblatex, but the venue's template decides. In Zotero, an export format such as BibLaTeX set as the Quick Copy default makes Ctrl/Cmd-Shift-C copy the selected entries (Zotero, *Export*). Overleaf's Zotero link, a premium feature, brings the library in as a read-only `.bib` refreshed by hand, one way.

### 6. Vector and raster: what a figure file stores

*In one sentence:* a raster stores a fixed grid of pixels, so its sharpness and size are settled when it is saved, while a vector stores drawing instructions, sharp at any size and priced by what it draws.

**The problem.** Figure 1 must be sharp in a 3.5-in column, sharp when a reviewer zooms in on a tick label, and small enough to upload — which depends on the kind of file, often decided unnoticed by one line of the plotting script.

**The idea.** A **raster** (bitmap) stores a grid of coloured pixels; a **vector** file stores instructions — a circle here, a line there, this text in this font — that the viewer carries out afresh at whatever size the page is shown. PNG and JPG are raster formats; PDF and EPS can hold vector drawings (Overleaf, *Advanced LaTeX image topics*).

> **Vector and raster graphics, defined.** A **raster** holds *a grid of pixels*: (1) its pixel counts are fixed when it is saved, and (2) its size in bytes, before compression, grows with the pixel count. A **vector** file holds *drawing instructions* in the page's own units: (3) its size grows with the number of objects and path vertices it draws, and (4) not with the size it prints at or the resolution a venue asks for.
>
> $$B_{\text{raster}}=3\,(w\,r)(h\,r),\qquad B_{\text{vector}}\approx F_0+K\,b_{\text{obj}}$$
>
> where $w\times h$ is the printed size in inches, $r$ the resolution in dots per inch, 3 the bytes of a 24-bit RGB pixel before compression, $K$ the number of drawn objects and $F_0$, $b_{\text{obj}}$ the running object's course numbers — so doubling the resolution quadruples a raster and leaves a vector unchanged.
>
> - **Example**: Figure 1 at 3.5 × 1.5 in. At 600 dpi it is $2100\times900=1{,}890{,}000$ pixels, 5,670,000 bytes before compression; as a vector, $20{,}000+61\times100=26{,}100$ bytes — 217 times smaller, and still 26,100 bytes at whatever size the figure prints.
> - **Non-example**: a PNG placed inside a PDF: the file ends in `.pdf`, the figure is still pixels, and Overleaf notes that bitmaps stored in PDF or EPS take a lot of disk space. matplotlib makes the slip silently: `fig.savefig("rs1_fig1")` with no extension falls back to `savefig.format`, whose default is `png` (matplotlib, `savefig`).
> - **Why it matters**: only a vector stays sharp at every zoom and costs the same at any resolution; a raster's quality is settled the moment it is saved.

**Resolution, for the rasters you cannot avoid.** A photograph of the rig is a raster by nature: Overleaf advises JPG for photographs, which it calls much more space-efficient for them, and PNG or PDF for plots and line drawings (Overleaf, *Optimising very large image files*). A raster's sharpness in print is its **effective resolution**, pixels across over printed width,

$$r_{\text{eff}}=\frac{N_{\text{px}}}{w_{\text{print}}}$$

because LaTeX stretches the same pixels over whatever width it is given. The draft of Figure 1 has 640 pixels across; printed 3.5 in wide that is $640/3.5=182.9$ dpi — pixels 0.139 mm apart, against 0.042 mm at 600 dpi — and its 5.47-pt labels (§7) get $5.47/72\times182.9=13.9$ pixels for their whole font size.

**The traps.** Enlarging a 640-pixel screenshot to 2100 pixels in an image editor: the file now claims 600 dpi, but the new pixels are interpolated from the old, and the blur is only spread thinner — unlike re-running the plotting script at a higher `dpi`, which draws the figure again (§7). And saving a plot as JPG, the format Overleaf keeps for photographs.

> [!note]- Deeper · 더 깊이
> **When a vector loses.** A vector's size grows with what it draws. The main study logs each trial's force at 1 kHz for 2 s, so a figure of all 64 traces has $64\times2000=128{,}000$ path vertices: $20{,}000+128{,}000\times15=1{,}940{,}000$ bytes at the course cost, all redrawn whenever the page is shown. One hour of a 200 Hz log — P6's controller rate — is 720,000 vertices and 10,820,000 bytes, more than even the uncompressed 600-dpi raster of a 3.5 × 1.5 in panel, 5,670,000; the two are equal at $(5{,}670{,}000-20{,}000)/15\approx376{,}667$ vertices. The cure is to rasterize **only the dense layer**: an artist created with `rasterized=True` becomes pixels inside an otherwise vector PDF or SVG, the axes and text stay vectors, and the pixels are sized by the `dpi` passed to `savefig` — which, matplotlib's documentation says, can speed up rendering and shrink files for large data sets at the cost of a fixed resolution (matplotlib, *Rasterization for vector graphics*).

### 7. Text at print size, and the plotting script

*In one sentence:* LaTeX shrinks or enlarges a figure to the width it is given, and everything in it — text, lines, markers — scales by the same factor, so a figure drawn at the wrong size prints its text at the wrong size.

**The problem.** On screen the draft's 10-pt labels looked fine; in the column they print at 5.47 pt, smaller than anything else in the paper.

**The idea.** `\includegraphics[width=\columnwidth]` does not re-lay-out a figure; it scales the whole picture, like a photocopier's zoom. A 6.4-in file in a 3.5-in column shrinks letters, lines and dots by the same factor. matplotlib starts every figure at 6.4 × 4.8 in with a 10-pt font and sizes tick and axis labels relative to it (default `matplotlibrc`, version 3.11.2) — defaults that know nothing of the column.

> **Print scale, defined.** The **print scale** of an included figure is *the factor by which LaTeX multiplies every length in the figure's file to fit the width the source asks for* — a property of file and page together. Four conditions: (1) it is **uniform** — given only a width, graphicx keeps the aspect ratio (Overleaf); (2) it applies to **everything in the file**, text and line widths included; (3) it is set by the file's **saved** width, which `bbox_inches="tight"` changes, since then only the tight bounding box is saved (matplotlib, `savefig`); (4) it is **independent of the resolution** — `dpi` sets how many pixels an inch holds, not how many inches the figure has.
>
> $$s=\frac{w_{\text{print}}}{w_{\text{file}}},\qquad f_{\text{print}}=s\,f_{\text{drawn}}$$
>
> where $w$ are widths in inches and $f$ font sizes in points — so text drawn at 10 pt in a 6.4-in figure prints at 5.47 pt in a 3.5-in column, and printing 8 pt at that scale would need 14.63-pt text.
>
> - **Example**: the draft, $s=3.5/6.4=0.547$: 10-pt labels print at 5.47 pt, 1.5-pt lines at 0.82 pt, 6-pt markers at 3.28 pt, and the figure is 2.63 in tall instead of 1.5.
> - **Non-example**: the same draft saved with `dpi=600`: $3840\times2880$ pixels, still 6.4 in wide, still scaled by 0.547, labels still 5.47 pt. Resolution and print scale are separate knobs.
> - **Why it matters**: the reader sees only the printed size; a figure drawn larger than its column prints every label smaller than it looked on screen, and nothing inside LaTeX recovers them.

**The rule: draw at the printed size.** Set `figsize` to the column width read from the template and the planned height, and the font to its printed size; then $s=1$, and what the script draws is what the page prints. The script for Figure 1 — shown, not run, as matplotlib is not installed on this machine; every call was checked against the matplotlib 3.11.2 documentation:

```python
# not-run: matplotlib is not installed on this machine; every call was checked against the Matplotlib 3.11.2 documentation
import numpy as np
import matplotlib.pyplot as plt

A = np.array([8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3])    # RS1 pilot, peak force (N)
B = np.array([6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6])
mean = np.array([10.66, 7.50])                                         # page 4's means and 95% t-intervals
lo, hi = np.array([8.93, 6.53]), np.array([12.39, 8.47])

plt.rcParams["font.size"] = 8              # the size the text prints at, because the figure is drawn at print size
plt.style.use("petroff10")                 # a colour cycle built with colour-vision-deficiency modelling (3.10 and later)
fig, ax = plt.subplots(figsize=(3.5, 1.5)) # inches: the column width, and the height planned for Figure 1
ax.plot(A, np.full(10, 1.0), "o")          # row A: circles
ax.plot(B, np.full(10, 0.0), "s")          # row B: squares, so the rows differ by more than colour (section 8)
ax.errorbar(mean, [0.75, -0.25], xerr=np.vstack((mean - lo, hi - mean)), fmt="D", color="black")
ax.axvline(10, linestyle="--", color="black")      # the 10 N line, fixed before the pilot
ax.set_yticks([0.0, 1.0], labels=["B", "A"])
ax.set_xlabel("Peak contact force (N)")            # the quantity and its unit
fig.savefig("rs1_fig1.pdf")                        # the extension picks the format: PDF, a vector file
```

It is included with `\includegraphics[width=\columnwidth]{rs1_fig1}`, the width kept as a guard: if the real column is 3.4 in, the scale is $3.4/3.5=0.971$ and 8 pt prints as 7.8 pt — invisible — where the 6.4-in draft lost almost half its size.

**The trap in the error bars.** `errorbar`'s `xerr` takes **distances** from each mean, not the ends of the interval: in its two-row form the first row holds the lower distances and the second the upper, all non-negative (matplotlib, `Axes.errorbar`). The script passes `mean - lo` and `hi - mean`, for A 1.73 N each way. Passing the ends, `xerr=np.vstack((lo, hi))`, would draw A's bar from $10.66-8.93=1.73$ N to $10.66+12.39=23.05$ N — across the whole plot, with no error message, since every value is non-negative.

> [!note]- Deeper · 더 깊이
> matplotlib's other defaults (default `matplotlibrc`, 3.11.2): 100 dpi; tick and axis labels `medium` and titles `large`, relative to `font.size`; lines 1.5 pt, markers 6 pt; `savefig` writes PNG unless the file name or `format` says otherwise; and PDF output embeds Type 3 fonts, which `pdf.fonttype = 42` switches to TrueType — the setting to change if a venue's PDF check asks for TrueType. `bbox_inches="tight"` saves the tight bounding box of what was drawn rather than the canvas, so the saved width, and the print scale with it, can differ from `figsize`.

### 8. Colour, one message, and error bars that say what they are

*In one sentence:* a figure makes one comparison, keeps it readable without colour, and says in its caption exactly what each mark and bar is.

**The problem.** A reviewer prints the paper in grayscale; another reader has red–green colour-vision deficiency; a third compares RS1's bars with another paper's, not knowing that one shows standard deviations and the other confidence intervals. Each reads a different figure from the one the authors meant.

**The idea.** *One message:* Figure 1 answers one question — where does each trial's peak fall against the 10 N line, arm by arm? Even the difference of means is left to Table 1 (page 4's §4 drops that panel from the print version), and how force rises and falls within a contact, which the main study's traces will show, is a second figure. *Colour as a helper, not a carrier:* matplotlib's colormap guide notes that the most common colour-vision deficiency is difficulty telling red from green, so avoiding the two together avoids many problems (matplotlib, *Choosing Colormaps*); colour cycles designed to stay distinguishable, such as matplotlib's `petroff10`, help further (Deeper, below), and a second channel does the rest. *Named bars:* the caption says what each bar is and how many trials it rests on.

> **Redundant encoding, defined.** A figure uses **redundant encoding** when *every pair of categories it shows differs in at least two visual channels, at least one of which is not hue* — a property of the design, not the palette. The channels are position (row or panel), marker shape, line style, lightness, a direct label, and hue. Three conditions: (1) each pair differs in **at least two channels**; (2) at least one **survives the loss of hue**, for a reader with red–green deficiency or on a grayscale printout; (3) the mapping is **stated**, by a direct label or in the caption.
>
> $$c(i,j)\ge2\quad\text{and}\quad c_{\neg\text{hue}}(i,j)\ge1\qquad\text{for every pair of categories } i\ne j$$
>
> where $c(i,j)$ counts the channels in which categories $i$ and $j$ differ and $c_{\neg\text{hue}}$ those other than hue — so a figure passes when a reader could still tell A from B with the colour turned off.
>
> - **Example**: Figure 1 from §7's script: A and B differ by row, marker (circles against squares) and colour, $c=3$, $c_{\neg\text{hue}}=2$. Page 4's single-colour drawing still separates them by row and by the letters A and B, $c=2$.
> - **Non-example**: A as red dots and B as green dots on one shared row, with a legend: $c=1$, $c_{\neg\text{hue}}=0$. The most common deficiency and a grayscale printer both erase the comparison the figure exists to make.
> - **Why it matters**: reviewers print, projectors wash colours out, and some readers cannot see the difference; a figure that needs its colours to be read is one some readers cannot read.

**Error bars, on RS1.** The same ten trials give three different bars, and nothing in a bar's look says which it is. For arm A the standard deviation is 2.41 N, the standard error of the mean $2.414/\sqrt{10}=0.76$ N, and the half-width of the 95% t-interval $2.262\times0.764=1.73$ N; for B, 1.36, 0.43 and 0.97 N. The standard deviation describes single trials, the standard error the mean, and the interval multiplies the standard error by $t_{0.975,9}=2.262$ ([[02-foundations/ml-practice|9. ML Practice §4]]; [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §4]] sizes experiments with them). On the same data, $\pm0.76$ and $\pm1.73$ differ by a factor of 2.3, and $\pm2.41$ and $\pm0.76$ by $\sqrt{10}=3.2$.

**The traps.** A legend that makes the reader match colours where a direct label would do. A caption that says "error bars" without saying which — RS1's names the diamond and bar under each row as the mean and its 95% t-interval and gives the ten unpaired trials per arm, and page 4's §4 lists what else a results figure owes its reader. And a lopsided interval, such as a Wilson interval, drawn with one ± number: it needs the two-row `xerr` or `yerr` of §7.

> [!note]- Deeper · 더 깊이
> matplotlib ships colour cycles built for categories: `petroff10`, added in 3.10 with colour-vision-deficiency modelling, and the Okabe–Ito sequence, added in 3.11, whose colours stay distinguishable for common deficiencies and in print (release notes 3.10.0 and 3.11.0). For a continuous quantity, its guide recommends a colormap whose lightness rises steadily, which still reads when printed in grayscale (*Choosing Colormaps*).

### 9. Tables: three rules, units, and the digits the data support

*In one sentence:* a table's rules, units and digits are part of what it claims, so it uses three horizontal rules, states each unit once, and prints no digit its uncertainty cannot support.

**The problem.** The analysis script prints A's mean peak force as 10.6600 N. Four decimals look careful; they claim the mean is known to a ten-thousandth of a newton, from ten trials whose 95% interval is 3.5 N wide.

**The idea.** A number in a table claims a precision as well as a size. Keep the structure quiet — booktabs gives three horizontal rules, `\toprule` above the header, `\midrule` under it, `\bottomrule` at the end — and let each number carry only the digits its uncertainty supports. This page's layout advice: no vertical rules; each unit once, in the header or row label, "(N)"; numbers right-aligned so their decimal points line up; the caption where the venue's template puts it (Overleaf: above or below both work). For the digits, the page's convention follows how NIST's guideline on reporting uncertainty writes its examples — a standard uncertainty of 0.35 mg beside a mass of 100.021 47 g: two significant digits of uncertainty, and the value ending at the same decimal place (NIST TN 1297, §7).

> **Digits matched to the uncertainty, defined.** A number is **printed to its uncertainty** when *its last digit sits at the decimal place of the second significant digit of the uncertainty printed with it* — a reporting convention, not a property of the data. Four conditions: (1) the uncertainty $U$ is **named** — an interval's half-width (for a lopsided interval, its longer side) or a standard error; (2) $U$ keeps **two significant digits** and the value is rounded to the same place; (3) rounding happens **once**, from unrounded values; (4) the numbers of **one column share one decimal place**, the coarsest any row needs.
>
> $$d=\lfloor\log_{10}U\rfloor-1,\qquad x_{\text{printed}}=\text{round}\big(x,\ 10^{d}\big)$$
>
> where $d$ is the decimal exponent of $U$'s second significant digit, so the value and its interval stop at $10^{d}$ — a half-width between 1 and 10 N gives $d=-1$, tenths of a newton.
>
> - **Example**: A's mean, 10.66 N with $U=1.727$ N: $d=\lfloor0.237\rfloor-1=-1$, so 10.7 N [8.9, 12.4]. B alone, $U=0.970$, would give $d=-2$ and 7.50 [6.53, 8.47]; in a column shared with A it prints 7.5 [6.5, 8.5]. The success rates, whose Wilson intervals reach 0.29 and 0.30 below them, $U$ of 0.29 and 0.30, keep two decimals: 0.60 [0.31, 0.83] and 0.90 [0.60, 0.98].
> - **Non-example**: rounding twice — 0.849 straight to one decimal is 0.8, but first to 0.85 and then, half up, to one decimal it becomes 0.9.
> - **Why it matters**: a reviewer reads 10.66 N as a claim that the second decimal is known; the table should say only what the interval beside it allows, as [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review §4]] asks of every number in a results table.

**On RS1.** Page 4's Table 1 prints forces to two decimals, which keeps every cell traceable to its hand calculation there; the submitted table rounds by the convention. The rows are page 4's — only the digits and the typesetting are this page's:

```latex
\begin{table}[t]
  \centering
  \caption{RS1 pilot, ten unpaired trials per arm (illustrative data): mean peak
    force with its 95\% t-interval, and success rate (peak at most 10~N) with its
    Wilson 95\% interval. Differences are A $-$ B for force, B $-$ A for success.}
  \label{tab:pilot}
  \begin{tabular}{lrrr}
    \toprule
    Outcome                    & A              & B              & Difference \\
    \midrule
    Peak force, mean (N)       & 10.7           & 7.5            & 3.2 \\
    \quad 95\% interval (N)    & [8.9, 12.4]    & [6.5, 8.5]     & [1.3, 5.0] \\
    Success rate               & 0.60 (6/10)    & 0.90 (9/10)    & 0.30 \\
    \quad 95\% interval        & [0.31, 0.83]   & [0.60, 0.98]   & [$-$0.08, 0.60] \\
    \bottomrule
  \end{tabular}
\end{table}
```

The difference column follows the same rule: the force's half-width of 1.88 N gives 3.2 [1.3, 5.0], and the rates' interval, which reaches 0.38 below the difference, keeps two decimals, 0.30 [−0.08, 0.60]. What a narrower interval would cost in trials is [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §4]].

**The trap.** Pasting `"%.4f" % m` output into the table: Python prints the digits it was asked for, not the digits the experiment measured (how a float becomes decimal text, and why `repr` and `%.4f` disagree, is [[02-foundations/tools/config-data-formats|12.4 Config and Data Formats §2]]). Put the formatting in the table-making code, driven by $U$, and round once.

### 10. The paper in a Git repository

*In one sentence:* a paper is source code, so it lives in a Git repository with the scripts and data that make its figures, while everything the build regenerates stays out.

**The problem.** Six months after submission a reviewer asks which data made Figure 1, and the PDF on your laptop came from a draft nobody can find. [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review §9]] asks that paper, code, data and figures refer to compatible versions, and [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §7]] lists what a reproducible result must record. For the paper itself, that is a repository.

**The idea.** Track what people write and what regenerates the figures; leave out what the build writes anew each time. RS1's repository holds `main.tex`, one sentence per line so a change shows as a change to one sentence; `refs.bib`, exported and committed, because a re-export can change keys (§5); `figures/fig1.py`, which reads `data/pilot.csv` and writes `figures/rs1_fig1.pdf`, so Figure 1 and Table 1 come from the same data; and that figure PDF, committed, so a co-author — or Overleaf — can build the paper without running Python.

**The rule, on RS1's repository.** `.gitignore` names what to leave out: a pattern without a slash matches at any level, one that begins with a slash only at the `.gitignore` file's own level, and `*` matches anything but a slash (Git documentation, *gitignore*).

```text
# what a LaTeX build writes beside main.tex; the next build makes them again
*.aux
*.log
*.bbl
# the paper's own PDF, at the top level only: the figure PDFs stay tracked
/main.pdf
```

Checked in a scratch copy of the repository — files empty, output as printed (Git 2.46.0 on macOS 26.6.2, arm64):

```bash
$ git status --short --untracked-files=all
?? .gitignore
?? data/pilot.csv
?? figures/fig1.py
?? figures/rs1_fig1.pdf
?? main.tex
?? refs.bib
$ git check-ignore -v -n main.aux main.bbl main.pdf figures/rs1_fig1.pdf
.gitignore:2:*.aux	main.aux
.gitignore:4:*.bbl	main.bbl
.gitignore:6:/main.pdf	main.pdf
::	figures/rs1_fig1.pdf
```

The build files have left the status list; `check-ignore` names the rule that hides each, and `::` marks the one no rule matches — the figure, which stays tracked.

**The traps.** A plain `*.pdf` would have hidden the figure PDFs too; that is why the paper's PDF is anchored with a slash. A `.gitignore` affects only files Git does not already track, so a build file committed by mistake must first leave the index with `git rm --cached` (Git documentation). And on Overleaf the Git integration — premium — lets you clone, pull and push but supports neither branches nor tags, while the free plan's history keeps only the last 24 hours and labelled versions. So label the submitted version in Overleaf's history, and keep its tag — the commit the submitted PDF was built from — in your own clone, beside the scripts and data Overleaf cannot run.

### Worked case · 대상으로 한 번 끝까지

It comes after §10 because it uses §1, §3 and §5–§9: Figure 1 carried from its first draft into the course template's column, its file priced both ways, its one reference carried from the publisher's page into the printed list, and Table 1's digits. The symbols are the running object's.

**Step 1 — the column.** Two columns and the gap between them fill the text width (§1), so

$$w=\frac{W-g}{2}=\frac{7.25-0.25}{2}=3.5\ \text{in},$$

which is $3.5\times72.27=252.9$ TeX points, or 88.9 mm. On a real template this is the number `\the\columnwidth` prints (§4).

**Step 2 — the draft in the column.** The draft was drawn at matplotlib's default 6.4 × 4.8 in with 10-pt text and saved as a 640 × 480 PNG at 100 dpi. `\includegraphics[width=\columnwidth]` multiplies every length in it by the same factor (§7), so

$$s=\frac{w}{w_{\text{file}}}=\frac{3.5}{6.4}=0.547,\qquad f_{\text{print}}=0.547\times10=5.47\ \text{pt}<f_{\min}=8\ \text{pt},$$

since text scales with everything else. The figure prints $4.8\times0.547=2.63$ in tall — 3.13 in with its caption, $0.35H$, inside the top-area limit of §3 but 1.13 in more than planned — and its 640 pixels over 3.5 in give $r_{\text{eff}}=640/3.5=182.9$ dpi, under a third of the 600 asked for (§6). The two failures are independent: saving at `dpi=600` would cure the second and leave the first, because the file would still be 6.4 in wide (§7).

**Step 3 — drawn at print size.** With `figsize=(3.5, 1.5)` and `font.size = 8`, the scale is $3.5/3.5=1.00$: the text prints at 8 pt and the figure is 1.5 in tall, 2.0 in with its caption, $0.22H$, so `[t]` puts it at the top of its column (§3). Saved as `rs1_fig1.pdf`, it has no pixels to count.

**Step 4 — the file, both ways.** As a vector, $B=F_0+K\,b_{\text{obj}}=20{,}000+61\times100=26{,}100$ bytes. As a raster at 600 dpi, $(3.5\times600)(1.5\times600)=2100\times900=1{,}890{,}000$ pixels and $3\times1{,}890{,}000=5{,}670{,}000$ bytes before compression — 217 times the vector. At 300 dpi it is $1050\times450$ pixels and 1,417,500 bytes, 54 times: halving the resolution quartered the raster and left the vector where it was (§6).

**Step 5 — the reference.** The DOI `10.1371/journal.pbio.1002128` resolves to the article's page at PLOS Biology, which gives the title with its capitals, four authors, volume 13, issue 4, article e1002128, published 22 April 2015. From that page, not from a citation elsewhere (§5):

```bibtex
@article{weissgerber2015,
  author  = {Weissgerber, Tracey L. and Milic, Natasa M. and Winham, Stacey J. and Garovic, Vesna D.},
  title   = {Beyond Bar and Line Graphs: Time for a New Data Presentation Paradigm},
  journal = {PLOS Biology},
  volume  = {13},
  number  = {4},
  pages   = {e1002128},
  year    = {2015},
  doi     = {10.1371/journal.pbio.1002128}
}
```

The key follows this page's convention. PLOS numbers its articles instead of paging them, and its own suggested citation puts the article number where a page range would go, so the entry does too. No title word needs braces: a sentence-case style would print "bar and line graphs", which is correct English, and there is no acronym or name to protect. The `doi` field holds the bare DOI; where the style prints it, it should read `https://doi.org/10.1371/journal.pbio.1002128`. Through the build of §1: the first run writes the key into `main.aux` and prints [?]; BibTeX finds it in `refs.bib` and writes `main.bbl`; the second run prints the list; the third prints [1]. $U$ of §5 is empty, and the log has no undefined citation.

**Step 6 — Table 1's digits.** By §9's convention: A's mean 10.66 N with half-width 1.73 N gives $d=-1$, 10.7 [8.9, 12.4]; B's half-width of 0.97 N alone would give $d=-2$, but the column takes A's $d=-1$, 7.5 [6.5, 8.5]; the difference, half-width 1.88 N, prints 3.2 [1.3, 5.0]; and the standard deviations, to two significant digits, 2.4 and 1.4 N.

**The same numbers, computed.** The listing redoes Steps 1–4 and 6 from the course numbers and the twenty pilot forces; its output follows.

```python
# 12.6 worked case: RS1's Figure 1 planned for the course template, and Table 1's digits. Standard library only.
import math

W, GAP, H = 7.25, 0.25, 9.0                  # course template: text width, column gap, text height (in)
F_MIN, H_FIG, H_CAP = 8.0, 1.5, 0.5          # smallest printed text (pt); Figure 1 and its caption (in)
F0, B_OBJ, B_VTX, K = 20000, 100, 15, 61     # vector PDF: fixed bytes, bytes per object, per vertex; objects
w = (W - GAP) / 2                            # two columns and one gap fill the text width
print("column w = %.3f in = %.1f TeX pt = %.1f mm" % (w, w * 72.27, w * 25.4))

print("%-20s %-12s %7s %13s %7s %7s %6s" % ("figure", "drawn (in)", "s", "text (pt)", "tall", "float", "dpi"))
for name, wd, hd, f, dpi in (("matplotlib default", 6.4, 4.8, 10.0, 100), ("drawn at print size", w, H_FIG, 8.0, None)):
    s = w / wd                               # print scale: every length in the file is multiplied by s
    eff = "vector" if dpi is None else "%.1f" % (wd * dpi / w)       # pixels across / printed inches
    print("%-20s %-12s %7.4f %5.2f -> %5.2f %6.3f %6.3fH %6s"
          % (name, "%.2f x %.2f" % (wd, hd), s, f, s * f, s * hd, (s * hd + H_CAP) / H, eff))
print("to print %.0f pt at the default size, draw text at %.2f pt" % (F_MIN, F_MIN * 6.4 / w))

vec = F0 + K * B_OBJ
print("vector: %d + %d x %d = %d bytes" % (F0, K, B_OBJ, vec))
for dpi in (300, 600):
    nx, ny = round(w * dpi), round(H_FIG * dpi)
    raw = 3 * nx * ny                        # 24-bit RGB, before compression
    print("raster %d dpi: %d x %d px = %d px, %d bytes, %.1f x the vector" % (dpi, nx, ny, nx * ny, raw, raw / vec))
cross = (3 * round(w * 600) * round(H_FIG * 600) - F0) / B_VTX
print("dense path: raw 600-dpi raster = vector at %.0f vertices; 64 x 2000 samples -> %d bytes; 1 h at 200 Hz -> %d bytes"
      % (cross, F0 + 64 * 2000 * B_VTX, F0 + 3600 * 200 * B_VTX))

A = [8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3]         # RS1 pilot, peak force (N)
B = [6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6]
T9, TW = 2.2622, 2.1425                      # Student-t 97.5% points: 9 df, and Welch's 14.16 df

def mean_sd(x):
    m = sum(x) / len(x)
    return m, math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))

def place(u):                                # decimal exponent of u's second significant digit
    return math.floor(math.log10(u)) - 1

(mA, sA), (mB, sB) = mean_sd(A), mean_sd(B)
rows = [("A", mA, T9 * sA / math.sqrt(10)), ("B", mB, T9 * sB / math.sqrt(10)),
        ("A - B", mA - mB, TW * math.sqrt(sA ** 2 / 10 + sB ** 2 / 10))]
d_col = max(place(u) for _, _, u in rows[:2])        # one decimal place per column: the coarsest row's
for label, m, u in rows:
    n = -(d_col if label != "A - B" else place(u))
    print("%-6s %7.4f +- %.4f  d = %2d  printed %.*f [%.*f, %.*f]" % (label, m, u, place(u), n, m, n, m - u, n, m + u))
print("sd: A %.4f -> %.1f, B %.4f -> %.1f" % (sA, sA, sB, sB))
```

```text
column w = 3.500 in = 252.9 TeX pt = 88.9 mm
figure               drawn (in)         s     text (pt)    tall   float    dpi
matplotlib default   6.40 x 4.80   0.5469 10.00 ->  5.47  2.625  0.347H  182.9
drawn at print size  3.50 x 1.50   1.0000  8.00 ->  8.00  1.500  0.222H vector
to print 8 pt at the default size, draw text at 14.63 pt
vector: 20000 + 61 x 100 = 26100 bytes
raster 300 dpi: 1050 x 450 px = 472500 px, 1417500 bytes, 54.3 x the vector
raster 600 dpi: 2100 x 900 px = 1890000 px, 5670000 bytes, 217.2 x the vector
dense path: raw 600-dpi raster = vector at 376667 vertices; 64 x 2000 samples -> 1940000 bytes; 1 h at 200 Hz -> 10820000 bytes
A      10.6600 +- 1.7272  d = -1  printed 10.7 [8.9, 12.4]
B       7.5000 +- 0.9698  d = -2  printed 7.5 [6.5, 8.5]
A - B   3.1600 +- 1.8760  d = -1  printed 3.2 [1.3, 5.0]
sd: A 2.4144 -> 2.4, B 1.3556 -> 1.4
```

The `d` column is each row's own decimal place; B prints with the column's. The case in one line: the draft failed twice, for independent reasons — scale and pixels — and one decision, drawing at the printed size and saving a vector, cures both, while the reference list and the table print only what the build and the uncertainty allow.

### 11. What this page does not cover

What RS1's paper argues, how its results table and figure are chosen, its limitations and its review are [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]]; the statistics behind its numbers are page 4 and [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]]; which venue it goes to, and the rules each one sets, are [[06-research-practice/venue-strategy|5. Venue Strategy]] and the venue's own author instructions. Git itself — commits, branches, merges — is assumed here, not taught: it is [[02-foundations/tools/git-research-code|12.2 Git for Research Code]], as the Python of the plotting and table scripts is [[02-foundations/tools/python-research-code|12.3]] and the CSV and JSON they read are [[02-foundations/tools/config-data-formats|12.4]]. The page also leaves out drawing inside LaTeX (TikZ, pgfplots), slides and posters, writing macros and packages, fonts beyond §7's Type 3–TrueType switch, accessibility beyond colour (alternative text for figures, for instance), word processors and shared online documents, and proofs and production after acceptance.

### After reading

- [ ] Say what a LaTeX run reads and writes, why a first run prints "??" and "[?]", and how many steps RS1's paper needs to settle.
- [ ] Place a `\label` so that it names the right number, and say what a label written before its `\caption` prints.
- [ ] Say where a float of a given height may go, what `h` alone becomes, and why a paper starts from the venue's template.
- [ ] Write a BibTeX entry from the page a DOI resolves to, with its key, any braces it needs and its DOI; say why a key prints [?].
- [ ] Compute a figure's print scale, printed text size and effective resolution, and its vector and raster sizes.
- [ ] Check a figure for redundant encoding and its caption for what the bars are; print a table's numbers to the digits their uncertainty supports.
- [ ] Say what a paper's repository tracks and what its `.gitignore` leaves out.

### Self-check

1. A co-author's PDF shows "Fig. ??" and "[?]" everywhere. What happened, and what does not need fixing?
2. After a full build, one citation still prints [?]. Where do you look, and what are the two likeliest causes?
3. Why must `\label` come after `\caption`, and what does the text print if it comes before?
4. A figure written with `[h]` appears at the top of the next column. Is anything wrong?
5. You re-save the draft of Figure 1 with `dpi=600`. Which of its two problems does that fix, and which does it not?
6. Table 1 prints B's mean as 7.50 in one draft and 7.5 in another. Which follows §9, and why does the answer depend on the column?

> [!tip]- Answers
> 1. It came from a single engine run, which cannot yet know the labels or the bibliography: unfinished, not broken. Nothing in the source needs fixing; build to the end, or let Overleaf do it (§1).
> 2. In the log, whose "undefined citation" warning names the key. Either the key is not in the database as cited — a typo, or a difference of case, since keys are case-sensitive — or the entry sits in a file the document does not load: `\bibliography{...}` names another file, or the file name's case differs, which matters on some systems, Overleaf included (§5).
> 3. Inside a float the number is set by `\caption`, and a label records the number set before it. Written before the caption, the label records the number of the section the figure sits in, so with the figure in Section 4 the text says "Fig. 4" — with no warning, because the reference is defined (§2).
> 4. No. `h` alone is not allowed, LaTeX made it `ht`, and the float went to the first place its rules allowed. Refer to it with `\ref`, not "below"; to bring it nearer its text, move the environment earlier in the source (§3).
> 5. The pixels: $6.4\times600=3840$ across 3.5 in is 1,097 dpi. Not the text: the file is still 6.4 in wide and scaled by 0.547, so its labels still print at 5.47 pt. Drawing at the printed size fixes both (§6, §7).
> 6. 7.5. Alone, B's half-width of 0.97 N would give $d=-2$ and 7.50; in a column shared with A, whose half-width of 1.73 N gives $d=-1$, every row prints tenths, so the decimal points line up and the column reads at one precision (§9).

### Problem set · 과제

Tier B. Worked by hand with this page, its prerequisites and RS1. Every item changes a knob of the worked case — the figure's width, its resolution, the number of trials, the reference — so none of the page's numbers can be copied.

1. **Draw.** RS1's Figure 1 as a full-width `figure*` on the course template, drawn at matplotlib's default 6.4 × 4.8 in and saved with `dpi=300`. Draw the text block, 7.25 × 9.0 in, to scale with the figure in place, and mark the print scale; the figure's printed height with its 0.5-in caption, as a fraction of $H$; the printed size of its 10-pt text against $f_{\min}$; and its effective resolution against 600 dpi. Say which of the draft's two failures the wider figure removes, which it does not, and where on a page LaTeX may put it.
2. **Derive.** (a) Re-planned at 7.25 × 2.5 in and drawn at that size, the figure as a 600-dpi raster: its pixels, raw bytes and ratio to the 26,100-byte vector; and, if it were drawn 6.4 in wide instead, the text size that prints at 8 pt. Its height with the caption as a fraction of $H$. (b) The main study runs 32 trials per arm. If the pilot's standard deviations hold, each arm's 95% half-width with $t_{0.975,31}=2.0395$, and the decimal place §9 then prints; and, with $t\approx1.96$, roughly how many trials per arm A's mean would need to earn a third decimal. (c) The BibTeX entry for the paper page 4 cites for its Wilson intervals — Lawrence D. Brown, T. Tony Cai and Anirban DasGupta, "Interval Estimation for a Binomial Proportion", *Statistical Science* 16(2): 101–133, May 2001, DOI 10.1214/ss/1009213286, as its publisher's page gives them — with a key by this page's convention, braces where needed, and the DOI as Crossref prints it.
3. **Interpret.** A lab-mate sends the first full draft of RS1's paper as a PDF made by one `pdflatex` run, with the excerpt below and these notes: Figure 1 was saved by a script that sets neither `figsize` nor `dpi`, with `fig.savefig("rs1_fig1")`; its x-axis reads "Peak force"; A is red dots and B green dots on one shared row; Table 1's numbers were pasted from `print("%.4f" % m)` — "10.6600 ± 2.4144" and a success rate of "0.9000"; `refs.bib`, exported from Zotero, holds the key `weissgerber2015`; Results is Section 4. Name each defect, the symptom a reader of the PDF sees, and the fix, with the section of this page it comes from.

```latex
\section{Results}
As Fig.~\ref{fig:peak} shows, every trial is plotted, following
Weissgerber et al.~\cite{Weissgerber2015}.

\begin{figure}[h]
  \label{fig:peak}
  \includegraphics[width=\columnwidth]{rs1_fig1}
  \caption{Peak force of every trial, A in red and B in green.}
\end{figure}
```

> [!note]- How to draw it · 그리는 법
> - Draw the text block to scale first — 7.25 × 9.0 in, with the two 3.5-in columns and the 0.25-in gap — and put the `figure*` across both columns at the top, the only place a full-width float takes on a text page.
> - Scale the figure before drawing it: its printed height is $s$ times its drawn height, and the caption comes on top; write the total as a fraction of $H$ beside `\dbltopfraction`'s 0.7.
> - Write the printed text size as $s\,f_{\text{drawn}}$ beside the 8-pt minimum; a scale above 1 enlarges the text, a scale below 1 shrinks it.
> - Write the effective resolution as pixels across over printed inches. The pixels across are the drawn width times the `dpi` the file was saved at, and nothing done in LaTeX changes them.
> - Keep the two checks apart: text size and resolution pass or fail independently, and this variant makes them come out differently.

> [!tip]- Solutions
> 1. $s=7.25/6.4=1.133$. The figure prints $4.8\times1.133=5.44$ in tall, 5.94 in with its caption, $0.66H$ — under `\dbltopfraction`'s 0.7, so it fits at the top of a page (the only place a `figure*` may take on a text page) or on a page of floats, never at the bottom. Its text prints at $10\times1.133=11.33$ pt, above 8: that failure is gone. Its $6.4\times300=1920$ pixels across 7.25 in are 264.8 dpi, under 600: that failure stays, since scaling up only spreads the pixels. And a two-row strip 5.44 in tall takes two-thirds of a page: the knob that matters is the drawn size.
> 2. (a) $7.25\times600=4350$ by $2.5\times600=1500$: 6,525,000 pixels, 19,575,000 bytes raw, 750 times the vector (the same 61 objects, 26,100 bytes). Drawn 6.4 in wide, $s=7.25/6.4=1.133$, so the text is drawn at $8/1.133=7.06$ pt. With its caption, $2.5+0.5=3.0$ in, $0.33H$, under 0.7. (b) A: $2.0395\times2.4144/\sqrt{32}=0.870$ N; B: $2.0395\times1.3556/\sqrt{32}=0.489$ N; both give $d=-2$, so the main study's table earns its second decimal. A third needs $U<0.1$ N, so $n>(1.96\times2.4144/0.1)^2=2239.4$: about 2,240 trials per arm (2,242 with the exact $t$ quantile), seventy times the planned 32.
>    (c)
>
>    ```bibtex
>    @article{brown2001,
>      author  = {Brown, Lawrence D. and Cai, T. Tony and DasGupta, Anirban},
>      title   = {Interval Estimation for a Binomial Proportion},
>      journal = {Statistical Science},
>      volume  = {16},
>      number  = {2},
>      pages   = {101--133},
>      year    = {2001},
>      doi     = {10.1214/ss/1009213286}
>    }
>    ```
>
>    No title word needs braces: "binomial proportion" is ordinary English in sentence case, and there is no acronym or name to protect. By Crossref's guidelines the DOI prints as `https://doi.org/10.1214/ss/1009213286`.
> 3. Eight defects. (i) One engine run: "Fig. ??" and "[?]" throughout — build to the end (§1). (ii) `\label` before `\caption`: once built, the text says "Fig. 4", Section 4's number, with no warning — label after caption (§2). (iii) `[h]` alone becomes `ht` with a warning and the figure floats anyway — use `[t]` or the default and refer only by `\ref` (§3). (iv) `\cite{Weissgerber2015}` against the key `weissgerber2015`: [?] even after a full build — cite the key exactly (§5). (v) `savefig` without an extension wrote a 640 × 480 PNG, scaled by 0.547: 5.47-pt text at 183 dpi — draw at 3.5 × 1.5 in with 8-pt text and save `rs1_fig1.pdf` (§6, §7). (vi) An axis without its unit — "Peak contact force (N)" (§8, §9). (vii) Red against green on one row, $c=1$, $c_{\neg\text{hue}}=0$, with a caption naming only colours — rows, markers, a colour-vision-safe cycle, and a caption stating the mapping, the bars and the trials per arm (§8). (viii) "10.6600 ± 2.4144" and "0.9000": 10.7 (the mean's half-width is 1.73 N), sd 2.4, and 0.90 [0.60, 0.98] (§9).

### Sources

- LaTeX2e unofficial reference manual, CTAN [latex2e-help-texinfo](https://ctan.org/pkg/latex2e-help-texinfo) — build outputs (§2.2–2.3), class options (§3.1), columns (§5.2), floats (§5.7).
- CTAN package pages — [amsmath](https://ctan.org/pkg/amsmath), [graphicx](https://ctan.org/pkg/graphicx), [booktabs](https://ctan.org/pkg/booktabs), [siunitx](https://ctan.org/pkg/siunitx), [biblatex](https://ctan.org/pkg/biblatex), [biber](https://ctan.org/pkg/biber), [bibtex](https://ctan.org/pkg/bibtex), [IEEEtran](https://ctan.org/pkg/ieeetran): purpose and version of each.
- [The TeX FAQ](https://texfaq.org/) — float placement and order, `\label` after `\caption`, BibTeX capitalisation, `\the`, `~`.
- [Overleaf documentation](https://docs.overleaf.com/) and [Learn LaTeX](https://www.overleaf.com/learn) — the four build steps, [?], keys, math, figures, image formats, plans, Git and Zotero limits, siunitx 3.
- [Zotero documentation](https://www.zotero.org/support/) — BibTeX and BibLaTeX export, Quick Copy.
- [Matplotlib 3.11.2 documentation](https://matplotlib.org/stable/) — defaults, `savefig`, rasterization, `errorbar`, colour cycles and colormaps.
- [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/) and [Crossref display guidelines](https://www.crossref.org/display-guidelines/) — what a DOI is, and how to print it.
- [NIST TN 1297 §7](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty) — the reporting examples behind §9's convention.
- [Git documentation: gitignore](https://git-scm.com/docs/gitignore) — pattern rules.
- Weissgerber et al., *PLOS Biology* 13(4): e1002128 (2015), [doi.org/10.1371/journal.pbio.1002128](https://doi.org/10.1371/journal.pbio.1002128) — the worked case's entry.
- Brown, Cai & DasGupta, *Statistical Science* 16(2): 101–133 (2001), [doi.org/10.1214/ss/1009213286](https://doi.org/10.1214/ss/1009213286) — problem 2(c)'s entry.

## 한국어

*[[06-research-practice/index|6. 연구 실무]]의 모든 페이지가 함께 쓰는 연구 RS1, 그리고 RS1 논문이 무엇을 주장할지 정하고 표 1과 그림 1을 만든 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사]] 위에 선다. 이 페이지는 그 논문 뒤편의 작업장이다. 소스를 PDF로 바꾸는 프로그램, 그림을 움직이는 규칙, 그림을 담는 파일, 글자가 인쇄되는 크기, 참고문헌을 꺼내 오는 데이터베이스, 그리고 표가 찍는 자릿수를 다룬다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]가 그리는 피지컬 AI 스택 아래의 바닥, 곧 연구 실무 곁의 도구에 속한다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 그 절의 사례 "저 패널을 프레임에 설치해"의 여덟 단계 가운데 어느 것도 직접 해내지는 않지만, 그 단계들에 대한 증거 — 팔이 패널에 닿을 때의 RS1 최대 힘, 그리고 끝내는 시행 수로 센 패널의 안착 — 를 그림, 표, 참고문헌 목록으로 독자에게 옮기는 길이 이 페이지다. 도구를 잘못 다루면 옳은 실험도 틀리게 보고된다. matplotlib 기본값으로 그린 RS1의 그림 1은 눈금 글자를 5.47 pt로 인쇄하고, 10.6600 N을 찍은 표는 시행 열 번이 받쳐 줄 수 없는 정밀도를 주장하며, 대소문자를 틀리게 친 인용 키는 몇 번을 빌드해도 [?]로 찍힌다. 그림과 표가 무엇을 보여야 하는지는 [[06-research-practice/scientific-writing-peer-review|연구 실무 4 §4]]가, 저장소가 무엇을 기록해야 하는지는 [[06-research-practice/experimental-design-reproducibility|연구 실무 2 §7]]이 정한다. 이 페이지는 학위논문 경로([[07-research-program/index|연구 프로그램 §8]])의 일곱 블록 밖에 있으니 연구 실무 4와 함께 — 그 끝까지 계산은 블록 5에서, 나머지는 블록 8에서 — 읽고, 늦어도 첫 논문 초안을 쓰기 전에는 읽는다. 읽고 나면 결과를 데이터에서 제출할 PDF까지 옮길 수 있다. 단 폭에 맞춰 계획한 그림, 불확실성이 받쳐 주는 자릿수만 찍은 표, DOI에서 만든 참고문헌, 그리고 로그가 깨끗한 빌드.

> [!note] 처음이라면 · First pass
> 약 90분씩 두 번. **1회차 — 빌드와 그림.** 그림을 보고 §1과 §2를 읽은 다음, §1의 실행 표를 가리고 기억으로 다시 채운다. 네 단계가 각각 무엇을 읽고 쓰는지, 단계마다 PDF에 무엇이 보이는지. 이어서 §6과 §7을 읽고, 끝까지 계산의 1–4단계를 읽기 전에 계산기로 먼저 풀어 본다. 스스로 점검 1, 3, 5번으로 마친다. **2회차 — 그림을 둘러싼 논문.** §5, §8, §9를 읽고 5–6단계를 푼 뒤 스스로 점검 2번과 6번에 답한다. 그다음 §3은 그림이 엉뚱한 곳으로 떠 갔을 때, §4는 새 템플릿으로 시작하기 전에, §10은 공동 저자가 처음 논문을 고치기 전에 열고, 과제는 맨 나중에 한다. *더 깊이* 상자는 모두 미뤄도 된다.

### 이 페이지의 대상 · Running object

**RS1**은 [[06-research-practice/index|6. 연구 실무]]의 관통 연구이고, 이 페이지만 읽어도 되도록 여기 다시 적는다. *질문:* 임피던스 제어(**B**)가 힘 문턱에서 멈추는 위치 제어(**A**)보다, [[02-foundations/lab-plants|0.6 Lab Plants]]의 평면 팔 **P2**가 400 N/m 패널과 접촉하는 일을 더 안전하게 만드는가? *시행:* 접촉으로 끝나는 접근 한 번. 최대 접촉력이 10 N 이하면 성공이다. *예비 실험*(설명용으로 만든 고정 데이터), 팔마다 짝짓지 않은 시행 열 번 — A: 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 N이라 6/10, 평균 10.66 N, 표본 표준편차 2.414 N. B: 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 N이라 9/10, 평균 7.50 N, 표준편차 1.356 N. *본 실험:* 팔마다 32회로 계획되어 있다.

이 페이지의 대상은 **RS1의 논문**이고, 그중 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사]]가 이미 정해 둔 세 부분이다.

- **그림 1** — 4쪽 §4의 인쇄판. 시행마다 최대 힘을 점 하나로 찍어 A의 열 개를 한 줄에, B의 열 개를 그 아래 줄에 놓고, 예비 실험 전에 정한 10 N 선과, 팔마다 평균과 그 95% t-구간(A 10.66 N [8.93, 12.39], B 7.50 N [6.53, 8.47])을 그린다. 4쪽의 그림을 세어 보면 **그리는 요소가 61개**다 — 점 20, 선 19, 글자 19, 마름모 2, 음영 띠 1.
- **표 1** — 4쪽 끝까지 계산의 표. A − B = 3.16 N과 그 Welch 95% 구간 [1.28, 5.04] N, 성공률 6/10과 9/10과 그 Wilson 95% 구간 [0.31, 0.83], [0.60, 0.98].
- **참고문헌 하나** — 출판사 페이지에서 시작해 인쇄된 "[1]"까지 따라간다. 4쪽이 시행을 막대가 아니라 점으로 보여 주는 근거로 인용하는 Weissgerber 외(2015)다.

RS1 위에 이 페이지는 교과용 템플릿 하나와 그림 파일의 비용을 고정한다. **이것은 이 페이지만의 교과용 숫자로, 계산이 깔끔하도록 고른 값이다. 측정값도 아니고 실제 어느 venue의 규격도 아니다.** 실제 값은 실제 venue의 템플릿이 준다(§4).

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $W$, $g$ | 7.25 in, 0.25 in | 두 단짜리 쪽의 본문 폭, 그리고 두 단 사이 간격 |
| $w$ | 3.5 in | 단 폭 $(W-g)/2$ — 위 둘에서 나온다(§1) |
| $H$ | 9.0 in | 본문 높이, 곧 각 단의 높이 |
| $f_{\min}$ | 8 pt | 그림 속 글자가 인쇄될 수 있는 가장 작은 크기 — 템플릿 캡션의 크기 |
| $h_{\text{fig}}$, $h_{\text{cap}}$ | 1.5 in, 0.5 in | 그림 1에 계획한 높이, 그리고 여백을 포함한 캡션의 높이 |
| $r$ | 600 dpi | 교과용 venue가 래스터 그래프에 요구하는 해상도(사진은 300 dpi) |
| $F_0$ | 20,000 바이트 | 벡터 PDF 그림의 고정 부분: 파일 구조와 내장된 글꼴 일부 |
| $b_{\text{obj}}$, $b_{\text{vtx}}$ | 100, 15 바이트 | 그리는 요소 하나, 그리고 긴 경로의 꼭짓점 하나가 벡터 파일에 더하는 크기 |
| 궤적 | 1 kHz로 2 s | 본 실험이 시행마다 남기는 힘 기록, 샘플 2,000개(§6) |

숫자 둘은 교과용 값이 아니라 도구의 사실이다. LaTeX의 표준 클래스는 본문을 10 pt로 짜고, matplotlib는 모든 그림을 6.4 × 4.8 in, 100 dpi, 10 pt 글자로 시작한다. 그림 1의 첫 초안은 바로 이 기본값으로 만들어졌다.

*범위: 이 페이지는 RS1의 주장을 제출할 논문으로 옮기는 도구를 가르친다. 실행, 상호 참조, 플로트가 있는 컴파일러로서의 LaTeX, 패키지와 venue 템플릿, BibTeX와 참고문헌 관리자와 DOI, 단 안에서 살아남는 그림, 불확실성에 맞는 자릿수의 표, 그리고 Git 저장소에 둔 논문이다. 논문이 무엇을 말해야 하는지는 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사]], 숫자 뒤의 통계는 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성]], 어디로 보낼지는 [[06-research-practice/venue-strategy|5. Venue 전략]]이다. 나머지로 빠진 것은 §11에 적는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 274" style="max-width:100%;height:auto" role="img" aria-label="3.5인치 단에 맞춰 계획한 RS1의 그림 1. (a) 같은 척도로 그린 단: matplotlib 기본값 6.4×4.8인치로 그린 초안은 0.547배로 줄어 높이 2.63인치, 캡션까지 3.13인치가 되고 640픽셀이 인치당 183점으로 퍼진다. 3.5×1.5인치로 그린 최종본은 배율 1.00으로 인쇄되고 캡션까지 2.00인치를 차지한다. (b) 초안의 10포인트 글자는 5.47포인트로 인쇄되어 교과용 최소치 8포인트에 못 미치고, 최종본은 8포인트로 인쇄된다. (c) 로그 척도의 파일 크기: 벡터 PDF 26.1킬로바이트, 압축하지 않은 래스터는 300 dpi에서 1.42메가바이트, 600 dpi에서 5.67메가바이트.">
<text x="16" y="18" font-size="12" fill="currentColor">(a) 3.5 in 단 속의 RS1 그림 1, 같은 척도</text>
<rect x="20" y="34" width="112" height="84" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
<line x1="34" y1="111" x2="126" y2="111" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="34" y1="111" x2="34" y2="114" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="80" y1="111" x2="80" y2="114" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="126" y1="111" x2="126" y2="114" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="80" y1="37" x2="80" y2="111" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 2" stroke-opacity="0.8"/>
<circle cx="58.8" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="62.5" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="71.7" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="74.5" cy="59.1" r="1.7" fill="currentColor"/>
<circle cx="78.2" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="79.1" cy="59.1" r="1.7" fill="currentColor"/>
<circle cx="92" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="103.9" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="115.9" cy="57.1" r="1.7" fill="currentColor"/>
<circle cx="124.2" cy="57.1" r="1.7" fill="currentColor"/>
<line x1="70.2" y1="67.9" x2="102" y2="67.9" stroke="currentColor" stroke-width="1"/>
<path d="M86.1 65.7l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="23" y="60.6" font-size="10" fill="currentColor">A</text>
<circle cx="42.3" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="45" cy="83.7" r="1.7" fill="currentColor"/>
<circle cx="48.7" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="50.6" cy="83.7" r="1.7" fill="currentColor"/>
<circle cx="53.3" cy="79.7" r="1.7" fill="currentColor"/>
<circle cx="57" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="60.7" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="61.6" cy="83.7" r="1.7" fill="currentColor"/>
<circle cx="65.3" cy="81.7" r="1.7" fill="currentColor"/>
<circle cx="85.5" cy="81.7" r="1.7" fill="currentColor"/>
<line x1="48.1" y1="92.5" x2="65.9" y2="92.5" stroke="currentColor" stroke-width="1"/>
<path d="M57 90.3l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="23" y="85.2" font-size="10" fill="currentColor">B</text>
<rect x="20" y="121" width="112" height="10" fill="currentColor" fill-opacity="0.16"/>
<rect x="20" y="137" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="144" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="151" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="158" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="165" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="20" y="172" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<path d="M20 185H132 M20 187v-4 M132 187v-4" stroke="currentColor" stroke-width="0.8" fill="none" stroke-opacity="0.7"/>
<text x="76" y="197" font-size="10" text-anchor="middle" fill="currentColor">3.5 in</text>
<path d="M135 34h3V134h-3" stroke="currentColor" stroke-width="0.8" fill="none"/>
<text x="20" y="211" font-size="10" fill="currentColor" font-weight="bold">초안</text>
<text x="20" y="224" font-size="10" fill="currentColor">6.4 × 4.8 in로 그림</text>
<text x="20" y="237" font-size="10" fill="currentColor">×0.547 → 높이 2.63 in</text>
<text x="20" y="250" font-size="10" fill="currentColor">+ 캡션: 3.13 in = 0.35 H</text>
<text x="20" y="263" font-size="10" fill="currentColor">640 px → 183 dpi</text>
<rect x="162" y="34" width="112" height="48" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
<line x1="176" y1="75" x2="268" y2="75" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="176" y1="75" x2="176" y2="78" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="222" y1="75" x2="222" y2="78" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="268" y1="75" x2="268" y2="78" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="222" y1="37" x2="222" y2="75" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 2" stroke-opacity="0.8"/>
<circle cx="200.8" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="204.5" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="213.7" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="216.5" cy="48.3" r="1.7" fill="currentColor"/>
<circle cx="220.2" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="221.1" cy="48.3" r="1.7" fill="currentColor"/>
<circle cx="234" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="245.9" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="257.9" cy="46.3" r="1.7" fill="currentColor"/>
<circle cx="266.2" cy="46.3" r="1.7" fill="currentColor"/>
<line x1="212.2" y1="52" x2="244" y2="52" stroke="currentColor" stroke-width="1"/>
<path d="M228.1 49.8l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="165" y="49.8" font-size="10" fill="currentColor">A</text>
<circle cx="184.3" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="187" cy="61.4" r="1.7" fill="currentColor"/>
<circle cx="190.7" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="192.6" cy="61.4" r="1.7" fill="currentColor"/>
<circle cx="195.3" cy="57.4" r="1.7" fill="currentColor"/>
<circle cx="199" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="202.7" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="203.6" cy="61.4" r="1.7" fill="currentColor"/>
<circle cx="207.3" cy="59.4" r="1.7" fill="currentColor"/>
<circle cx="227.5" cy="59.4" r="1.7" fill="currentColor"/>
<line x1="190.1" y1="65.2" x2="207.9" y2="65.2" stroke="currentColor" stroke-width="1"/>
<path d="M199 63l2.2 2.2l-2.2 2.2l-2.2 -2.2z" fill="currentColor"/>
<text x="165" y="62.9" font-size="10" fill="currentColor">B</text>
<rect x="162" y="85" width="112" height="10" fill="currentColor" fill-opacity="0.16"/>
<rect x="162" y="101" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="108" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="115" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="122" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="129" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="136" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="143" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="150" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="157" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="164" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<rect x="162" y="171" width="112" height="3" fill="currentColor" fill-opacity="0.12"/>
<path d="M162 185H274 M162 187v-4 M274 187v-4" stroke="currentColor" stroke-width="0.8" fill="none" stroke-opacity="0.7"/>
<text x="218" y="197" font-size="10" text-anchor="middle" fill="currentColor">3.5 in</text>
<path d="M277 34h3V98h-3" stroke="currentColor" stroke-width="0.8" fill="none"/>
<text x="162" y="211" font-size="10" fill="currentColor" font-weight="bold">최종본</text>
<text x="162" y="224" font-size="10" fill="currentColor">3.5 × 1.5 in로 그림</text>
<text x="162" y="237" font-size="10" fill="currentColor">×1.00 → 높이 1.50 in</text>
<text x="162" y="250" font-size="10" fill="currentColor">+ 캡션: 2.00 in = 0.22 H</text>
<text x="162" y="263" font-size="10" fill="currentColor">벡터: 픽셀 없음</text>
<text x="300" y="18" font-size="12" fill="currentColor">(b) 인쇄되는 글자 크기 (pt)</text>
<text x="306" y="38" font-size="10.5" fill="currentColor">초안, 그린 크기</text>
<rect x="306" y="41" width="180" height="9" fill="currentColor" fill-opacity="0.18"/>
<text x="494" y="49" font-size="10.5" fill="currentColor">10</text>
<text x="306" y="62" font-size="10.5" fill="currentColor">초안, 인쇄 (×0.547)</text>
<rect x="306" y="65" width="98.4" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="412.4" y="73" font-size="10.5" fill="currentColor">5.47</text>
<text x="306" y="86" font-size="10.5" fill="currentColor">최종본, 인쇄 (×1.00)</text>
<rect x="306" y="89" width="144" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="458" y="97" font-size="10.5" fill="currentColor">8.00</text>
<line x1="450" y1="36" x2="450" y2="104" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="450" y="116" font-size="10" text-anchor="middle" fill="currentColor">최소 8 pt</text>
<line x1="306" y1="104" x2="486" y2="104" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="306" y1="104" x2="306" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="306" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">0</text>
<line x1="342" y1="104" x2="342" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="342" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">2</text>
<line x1="378" y1="104" x2="378" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="378" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">4</text>
<line x1="414" y1="104" x2="414" y2="107" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="414" y="116" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">6</text>
<text x="300" y="140" font-size="12" fill="currentColor">(c) 파일 크기, 로그 척도</text>
<text x="306" y="158" font-size="10.5" fill="currentColor">벡터 PDF (교과용 숫자): 26.1 kB</text>
<rect x="306" y="161" width="30" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="306" y="184" font-size="10.5" fill="currentColor">래스터 300 dpi, 1050 × 450 px: 1.42 MB</text>
<rect x="306" y="187" width="154.9" height="9" fill="currentColor" fill-opacity="0.7"/>
<text x="306" y="210" font-size="10.5" fill="currentColor">래스터 600 dpi, 2100 × 900 px: 5.67 MB</text>
<rect x="306" y="213" width="198.3" height="9" fill="currentColor" fill-opacity="0.7"/>
<line x1="306" y1="232" x2="522" y2="232" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<line x1="306" y1="232" x2="306" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="306" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">10 kB</text>
<line x1="378" y1="232" x2="378" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="378" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">100 kB</text>
<line x1="450" y1="232" x2="450" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="450" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">1 MB</text>
<line x1="522" y1="232" x2="522" y2="235" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.6"/>
<text x="522" y="246" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">10 MB</text>
</svg>

교과용 템플릿의 3.5 in 단으로 들어가는 RS1의 그림 1이다. 왼쪽은 같은 척도로 그린 단이다. matplotlib 기본값 6.4 × 4.8 in로 그린 초안은 0.547배로 줄어 캡션까지 단의 3.13 in를 차지하고 640픽셀이 183 dpi로 퍼지는데, 3.5 × 1.5 in로 그린 최종본은 배율 1.00으로 인쇄되어 2.00 in를 차지한다. 오른쪽을 보면 초안의 10 pt 글자는 교과용 최소치 8 pt에 못 미치는 5.47 pt로 인쇄되고, 같은 그림이 벡터 PDF로는 26.1 kB, 압축하지 않은 래스터로는 300 dpi에서 1.42 MB, 600 dpi에서 5.67 MB다(교과용 숫자, §6).

### 1. LaTeX 빌드: 소스에서 안정된 PDF까지

*한 문장으로:* LaTeX는 평문 소스를 PDF로 컴파일하는데, 한 번의 실행은 앞선 실행이 적어 둔 것만 쓸 수 있으므로, 참조와 인용이 있는 논문은 숫자가 자리를 잡을 때까지 여러 번 실행해야 한다.

**문제.** 공동 저자가 RS1 논문의 첫 PDF를 열었더니 그림 번호와 인용이 있어야 할 자리에 "Fig. ??"와 "[?]"가 찍혀 있다. 글에는 아무 문제가 없다. 그 PDF는 여러 번 거쳐야 할 과정의 첫 번째 결과일 뿐이다.

**생각.** LaTeX 논문은 쪽 위에 배치하는 문서가 아니라, 코드를 컴파일하듯 프로그램이 컴파일하는 **소스**다. RS1 논문은 평문 파일 몇 개로 이루어진다. 본문과 조판 명령이 든 `main.tex`, 참고문헌 항목이 든 `refs.bib`, 그림마다 파일 하나. `pdflatex`로 부르면 엔진은 PDF를 쓰고(LaTeX2e 참고 매뉴얼 §2.3), 그 옆에 실행 기록인 **`.log`** 파일과 상호 참조에 필요한 보조 정보를 담은 **`.aux`** 파일을 쓴다(§2.2). 요점은 시점이다. 한 번의 실행은 *앞선* 실행이 쓴 `.aux` 파일을 읽는다. 그래서 첫 실행은 `\ref{fig:peak}`를 만났을 때 그림 1이 몇 번이 될지 아직 모른다. 그 자리에 ??를 찍고, 다음번을 위해 번호를 적어 둔다. 인용은 프로그램이 하나 더 필요하다. 인용된 키를 형식 갖춘 목록으로 바꾸는 BibTeX, 그리고 그 번호를 찍을 실행 한 번이 더 든다. 그래서 작업의 고리는 고치고, 컴파일하고, PDF와 로그를 *둘 다* 읽는 것이다.

쪽을 정하는 것은 **문서 클래스**다. RS1 초안은 `article` 클래스에 `twocolumn` 옵션을 쓴다. 기본값은 US letter 용지에 10 pt 본문이고(매뉴얼 §3.1), 두 단 모드에서 각 단의 폭은 본문 폭에서 단 간격을 뺀 나머지의 절반이다(§5.2). 이 페이지가 따라갈 부분만 남긴 소스가 영어 절의 `main.tex` 목록이다. 클래스와 패키지 다섯 줄, `\ref`와 `\cite`가 한 번씩 나오는 본문 한 단락, `[t]`로 둔 그림 1, 그리고 `\bibliographystyle{IEEEtran}`과 확장자 없이 적은 `\bibliography{refs}`가 전부다.

**규칙, RS1 초안 위에서.** 네 단계와, 단계마다 PDF에 남는 것이다(Overleaf의 *Bibliography management with bibtex*가 같은 순서를 단계별로 설명한다). 명령 넷은 영어 절에 적었고, 여기서는 실행하지 않았다.

| 단계 | 읽는 것 | 쓰는 것 | PDF에 보이는 것 |
|---|---|---|---|
| `pdflatex main` | `main.tex` | `main.aux`: 레이블과 인용된 키 | "Fig. ??", "[?]", 참고문헌 목록 없음 |
| `bibtex main` | `main.aux`, `refs.bib`, IEEEtran 스타일 | `main.bbl`: 형식을 갖춘 목록 | — |
| `pdflatex main` | `main.tex`, `main.aux`, `main.bbl` | `main.aux`, 이제 목록의 번호까지 | "Fig. 1", 참고문헌 목록, 아직 "[?]" |
| `pdflatex main` | 위와 같음 | `main.aux`, 바뀌지 않음 | "Fig. 1", "[1]" |

> **LaTeX 빌드의 정의.** **LaTeX 빌드**(LaTeX build)는 *고정된 소스 파일 묶음에 대해 프로그램을 여러 번 실행하되, 한 번 더 돌려도 아무것도 바뀌지 않을 때 끝나는 실행의 연쇄*다. 명령 하나가 아니라 과정이고, 그것이 남긴 PDF도 아니다. 조건 넷. (1) 엔진의 각 실행은 소스와 **앞선 실행이 쓴 보조 파일**을 읽고 새 보조 파일을 쓴다. (2) 논문이 무엇이든 인용하면 엔진 실행 사이에 **참고문헌 단계** — BibTeX, biblatex라면 Biber(§5) — 가 들어간다. (3) 연쇄 동안 **소스는 고정**되고, 고치면 처음부터 다시 시작한다. (4) 어떤 실행이 읽은 것과 같은 보조 데이터를 쓰면 빌드는 **안정된다**.
>
> $$\text{PDF}_n=E\big(\text{source},\ \text{aux}_{n-1},\ \text{bbl}\big),\qquad \text{settled at the first } n \text{ with } \text{aux}_n=\text{aux}_{n-1}$$
>
> $E$는 엔진, $\text{aux}_{n-1}$은 실행 $n-1$이 쓴 것(첫 실행 전에는 없음), bbl은 참고문헌 단계의 출력이다. 그러므로 레이블이 모두 있는 논문은 엔진 실행 두 번에, 인용까지 있는 논문은 표의 네 단계에 안정된다.
>
> - **예**: RS1 초안은 네 단계 뒤에 안정되고, 다섯 번째 단계는 똑같은 PDF를 찍는다.
> - **비예**: 네 단계를 모두 거쳤는데도 "[?]"가 남은 PDF. 빌드는 *이미* 안정되었다. 그 키가 `refs.bib`에 없을 뿐이고(§5), 몇 번을 더 돌려도 고쳐지지 않으며, 로그의 "undefined citation" 경고가 그 키를 알려 준다.
> - **왜 중요한가**: 제출하는 PDF는 로그에 정의되지 않은 참조나 인용이 하나도 없는, 안정된 빌드에서 나와야 한다. Overleaf는 이 연쇄를 대신 돌려 준다 — 문서에 따르면 거기서는 상호 참조가 곧바로 동작한다. 자기 컴퓨터에서 하는 빌드는 자기 몫이다.

**함정.** 한 번만 돌린 PDF를 "??"가 박힌 채 돌리는 것은 망가진 게 아니라 덜 끝난 것이다. 누가 읽기 전에 끝까지 빌드한다. 그리고 경고는 오류와 달라서 실행을 끝까지 마치고 멀쩡해 보이는 PDF를 남긴다. 그래서 빌드는 PDF가 아니라 로그에서 확인한다.

**이 페이지에서는 LaTeX를 컴파일하지 않았다.** 이 컴퓨터의 유일한 TeX 엔진(Tectonic)에는 패키지의 로컬 사본이 없어서 내려받아야 하는데, 이 위키를 쓰는 규칙이 그것을 금한다. 그래서 모든 LaTeX 목록을 출처의 문서와 한 줄씩 대조했다.

### 2. 상호 참조와 수식

*한 문장으로:* 절, 수식, 그림, 표의 번호는 LaTeX가 스스로 매기며, 이름 붙일 대상 바로 뒤에 둔 `\label`이 있으면 `\ref`가 그 번호를 어디서든, 한 실행 늦게 찍어 준다.

**문제.** RS1 본문에는 "Fig. 1"이 네 군데 있다. 리뷰어가 그 앞에 장치 사진을 넣어 달라고 하면 점 그림은 그림 2가 된다. 손으로 친 번호라면 네 군데가 소리 없이 틀린다.

**생각.** LaTeX가 매기는 번호는 절대 손으로 치지 않는다. 대상에 `\label{fig:peak}`로 이름을 붙이고, 번호가 필요한 곳마다 `\ref{fig:peak}`를 쓴다. 번호 매김이 바뀌면 빌드가 다시 안정되는 즉시 모든 참조가 따라온다.

> **상호 참조의 정의.** **상호 참조**(cross-reference)는 *LaTeX가 절, 수식, 그림, 표에 매기는 번호에 붙인 이름으로, `.aux` 파일을 거쳐 한 실행 늦게 풀리는 것*이다. 번호 자체가 아니라 번호를 가리키는 포인터다. 조건 넷. (1) `\label{key}`는 **번호를 매기는 명령 바로 뒤**, 같은 환경 안에 둔다. 플로트에서는 `\caption` 뒤, 절에서는 `\section` 뒤다(TeX FAQ, *LaTeX gets cross-references wrong*). (2) **키는 하나뿐**이어야 한다. (3) `\ref{key}`는 **앞선 실행이 기록한** 번호를 찍는다. (4) 기록이 없으면 ??를 찍고 로그가 경고한다(매뉴얼 §2.2).
>
> $$\text{ref}_n(k)=\begin{cases}\text{num}_{n-1}(k) & \text{if run } n-1 \text{ recorded } k\\ \text{??} & \text{otherwise}\end{cases}$$
>
> $k$는 키, $\text{num}_{n-1}$은 실행 $n-1$이 `.aux` 파일에 적은 번호다. 그러므로 참조가 틀리는 길은 둘뿐이다. 정의되지 않는 것(로그가 알려 준다), 그리고 조건 (1)을 어기는 것(알려 주지 않는다).
>
> - **예**: 그림 1의 `\caption` 바로 뒤에 둔 `\label{fig:peak}`. 그 앞에 장치 사진을 넣으면, 고친 뒤 첫 실행은 옛 `.aux`를 읽으므로 아직 "Fig. 1"을 찍으면서 2를 기록하고, 그다음 실행이 네 군데 모두 "Fig. 2"를 찍는다.
> - **비예**: `\caption` *앞에* 둔 `\label{fig:peak}`. 그러면 레이블은 그림이 들어 있는 절의 번호를 기록한다(TeX FAQ). 그림이 4절에 있으면 본문은 "Fig. 4"라고 쓰고, 경고는 나오지 않는다. 참조가 정의되기는 했으니까 — 엉뚱한 것으로.
> - **왜 중요한가**: 손으로 친 "Figure 1"은 소리 없이 낡는다. 참조는 낡을 수 없고 정의되지 않을 수만 있으며, 그때는 로그가 말해 준다.

**수식, RS1 위에서.** **인라인** 수식은 글줄 안에서 `\(`와 `\)` 사이, 또는 달러 기호 하나씩 사이에 둔다(Overleaf). **디스플레이** 수식은 따로 한 줄을 차지한다. `\[ … \]`는 번호가 없고 `equation`은 번호가 있다. 여러 줄을 맞춰 세워야 하면 amsmath의 `align`이 줄마다 번호를 붙이고 `align*`는 붙이지 않는다. `&`는 줄들이 맞춰질 지점을, `\\`는 줄의 끝을 표시한다(Overleaf, *Aligning equations with amsmath*). 영어 절의 두 번째 목록은 RS1의 방법 절이 표 1이 보고하는 구간을 적는 모습이다. `align` 두 줄에 표준오차와 Welch 구간을 쓰고 줄마다 레이블을 단다. 예비 실험에서 두 줄의 값은 $\mathrm{SE}=0.876$ N과 $3.16\pm1.88=[1.28,\ 5.04]$ N으로 4쪽의 숫자이고, 줄마다 레이블이 있으니 수식이 어디로 옮겨 가도 "Eq.~\ref{eq:ci}"는 맞는 번호를 찍는다.

**함정:** 캡션 앞에 둔 레이블은 깨끗하게 컴파일되고, 경고도 없이, 그럴듯한 틀린 번호를 찍는다. 그림 번호가 너무 커 보이면 `\caption`과 `\label`의 순서부터 본다.

> [!note]- 더 깊이 · Deeper
> - `Fig.~\ref{fig:peak}`로 쓴다. `~`는 LaTeX의 줄바꿈 없는 공백이라(TeX FAQ, *Defining characters as macros*) "Fig."와 번호가 다른 줄로 갈라지지 않는다.
> - 키에 종류를 붙인다 — `fig:`, `tab:`, `eq:`, `sec:`. 그러면 엉뚱한 종류를 가리키는 참조가 PDF에서 틀리기 전에 소스에서 먼저 어색하게 읽힌다.
> - 캡션이 따로 환경 안에 들어 있으면 레이블도 그 환경 안에 있어야 한다(TeX FAQ).

### 3. 플로트: 그림과 표가 움직이는 이유

*한 문장으로:* 그림과 표는 쪽을 넘어 쪼갤 수 없으므로 LaTeX가 본문에서 떼어 내 규칙이 허락하는 첫 자리에 놓으며, 그 자리는 흔히 다음 단의 맨 위다.

**문제.** 그림 1을 결과 단락 한가운데에 적었는데, PDF에서는 다음 단의 맨 위에 가 있다. 아무도 그렇게 해 달라고 하지 않았고, "아래 그림"이라는 문장은 이제 틀렸다.

**생각.** 쪽이 넘어가면서 반으로 잘린 그림은 쓸모가 없다. 그래서 LaTeX는 그림과 표를 본문 흐름 밖에서 **플로트**로 짜고, 통째로 들어가는 첫 자리 — 예를 들면 뒤쪽 어느 쪽의 맨 위 — 로 옮긴다(매뉴얼 §5.7). `figure`나 `table`의 선택 인자는 갈 수 있는 곳을 나열한다. `t`는 본문 쪽의 맨 위, `b`는 맨 아래, `h`는 환경이 적힌 바로 그 자리, `p`는 플로트만 모은 별도의 쪽이다. `article`의 기본값은 `tbp`이고, `h` 하나만은 허용되지 않아 LaTeX가 `t`를 덧붙인다(§5.7). 이때 나오는 경고가 Overleaf 문서가 적어 둔 "'h' float specifier changed to 'ht'"다. 또 같은 종류의 플로트는 **순서를 지킨다**(§5.7). 그래서 자리를 못 찾은 그림 하나가 그 뒤의 그림을 모두 붙잡아 둔다.

> **플로트의 정의.** **플로트**(float)는 *본문 흐름 밖에 두었다가 규칙이 허락하는 첫 자리에 놓는 상자, 곧 캡션을 포함한 그림이나 표*다. 저자가 고르는 위치가 아니라 엔진이 푸는 배치 문제다. 조건 넷. (1) 쪽이나 단을 넘어 **쪼갤 수 없다**. (2) **배치 지정자**가 허락하는 곳으로만 가며, 기본값은 `tbp`다. (3) 같은 종류의 플로트 사이에서 **순서를 지킨다**. (4) 본문 쪽에서는 아래의 **비율 한도**를 따른다. 단 지정자에 `!`를 붙이면 그 플로트 하나에 한해 한도가 풀린다(§5.7).
>
> $$\sum_{\text{top}} h_i\le 0.7\,H,\qquad \sum_{\text{bottom}} h_i\le 0.3\,H,\qquad h_{\text{text}}\ge 0.2\,H,\qquad \sum_{\text{float page}} h_i\ge 0.5\,H$$
>
> $h_i$는 캡션을 포함한 플로트의 높이, $H$는 본문 높이, $h_{\text{text}}$는 플로트가 있는 쪽에 남는 본문이다. 그러므로 $H=9.0$ in인 교과용 템플릿에서 쪽 맨 위의 플로트는 합쳐서 6.3 in까지 가능하고, 플로트만 모은 쪽은 적어도 4.5 in를 플로트로 채워야 한다.
>
> - **예**: `[t]`로 둔 그림 1. $1.5+0.5=2.0$ in, 곧 $0.22H$로 위쪽 영역에 넉넉히 들어가므로, 환경이 놓인 단의 맨 위 — 그림을 소개하는 문장보다 위일 수도 있다 — 나 다음 단의 맨 위에 자리 잡는다.
> - **비예**: "아래 그림" 밑에 쓴 `\begin{figure}[h]`. `h` 하나는 `ht`가 되고 그림은 어느 쪽의 맨 위로 떠 가며 "아래"는 틀린 말이 된다.
> - **왜 중요한가**: 그림은 적힌 자리에 있는 일이 드물다. 그러니 본문은 위치가 아니라 `\ref`로 그림을 가리키고, 그림의 높이가 애초에 어디에 갈 수 있는지를 정한다.

**RS1 위에서.** 쪽 폭 전체를 쓰는 `figure*`는 두 단에 걸치고, LaTeX는 이것을 쪽의 맨 위나 플로트 쪽에만 두며 맨 아래에는 두지 않는다(§5.7; TeX FAQ). 과제 1이 그림 1을 이렇게 계획한다.

**함정.** 플로트를 두고 "아래"라고 쓰는 것. `float` 패키지의 `H`로 자리를 강제하는 것 — 그림을 적힌 자리에 못박으니(Overleaf) 더는 플로트가 아니게 되고, 쪽은 아무리 보기 싫어도 그 둘레에서 끊긴다. 그리고 앞쪽의 너무 큰 그림 하나가 그 뒤 그림을 모두 붙잡는 것.

> [!note]- 더 깊이 · Deeper
> 한도는 기본값이 문서화된 매개변수다(매뉴얼 §5.7; TeX FAQ, *Moving tables and figures in LaTeX*). `\topfraction` 0.7, `\bottomfraction` 0.3, `\textfraction` 0.2, `\floatpagefraction` 0.5. 쪽 맨 위에 최대 2개, 맨 아래에 1개, 본문 쪽 하나에 3개(`topnumber`, `bottomnumber`, `totalnumber`). 전폭 플로트는 `\dbltopfraction` 0.7. `flafter` 패키지는 플로트가 자기를 정의한 글보다 위에 나오지 못하게 한다(TeX FAQ). `\clearpage`는 새 쪽을 시작하면서 기다리던 플로트를 모두 내보내고(§5.7), 밀린 플로트가 길게 쌓이면 "Too many unprocessed floats" 오류로 끝난다(TeX FAQ).

### 4. 패키지와 템플릿

*한 문장으로:* 패키지는 LaTeX에 명령을 더하고 템플릿은 venue의 쪽을 고정하므로, 논문은 쓰는 패키지만 조금 불러오고 venue가 준 템플릿에서 시작한다.

**문제.** 맨 LaTeX에는 표의 괘선이나 단위를 위한 명령이 없고, venue마다 자기 쪽 모양을 원한다. 둘 다 남이 쓴 파일로 해결된다. 요령은 적게 고르고 아무것도 고치지 않는 것이다.

**생각.** **패키지**는 `\begin{document}` 앞에서 `\usepackage{이름}`으로 불러온다. RS1 논문은 다섯 개를 쓰며, 하나하나 CTAN 페이지에서 확인했다.

| 패키지 | RS1 논문이 쓰는 곳 |
|---|---|
| amsmath | `align`, `align*`, `equation*`(§2). AMS-LaTeX의 중심 패키지로 LaTeX 필수 묶음에 들어 있다 |
| graphicx | `width`, `height`, `scale`, `angle`을 받는 `\includegraphics`. 폭만 주면 높이는 가로세로 비를 지킨다(Overleaf) |
| booktabs | 표의 괘선 셋, `\toprule`, `\midrule`, `\bottomrule`(§9) |
| siunitx | 숫자와 단위를 한 양으로 묶는 `\qty{1}{\kilo\hertz}`, 그리고 표 열 안의 숫자 정렬. 버전 3의 `\qty`와 `\unit`이 `\SI`와 `\si`를 대신하되, 옛 이름도 여전히 동작한다(Overleaf의 TeX Live 2021 공지) |
| biblatex(Biber와 함께) | 템플릿이 BibTeX 대신 이것을 쓸 때의 참고문헌(§5) |

**템플릿**은 venue가 저자에게 주는 파일이다. 대개 참고문헌 스타일이 딸린 문서 클래스와, 그 안에 써 넣을 견본 논문이다. IEEE의 저널과 학회라면 **IEEEtran**, 곧 자기 BibTeX 스타일을 가진 클래스이고(CTAN, 버전 1.8b), `bare_conf.tex`와 `bare_jrnl.tex` 같은 견본 논문이 함께 온다.

**규칙.** venue가 준 템플릿 파일에서 시작하고 조판은 하나도 고치지 않는다. venue의 형식 규칙은 그 템플릿을 두고 쓰였기 때문이다. 그리고 쪽의 실제 치수는 이 페이지가 아니라 그 템플릿에서 읽는다. `\the\columnwidth`는 지금의 단 폭을 포인트 단위로 찍어 준다(TeX FAQ, *How to print contents of variables*).

**RS1 위에서.** 교과용 템플릿의 3.5 in 단이라면 약 252.9 pt가 찍힌다. TeX의 포인트는 $1/72.27$ in, 약 0.3515 mm이기 때문이다(Overleaf, *Lengths in LaTeX*). 찍힌 폭을 72.27로 나누면 §7의 그림 스크립트에 넣을 인치가 나온다.

**함정.** 쪽수 제한에 맞추려고 템플릿의 여백이나 글자를 줄이는 것. 쪽은 맞아도 논문은 검사받을 형식을 더는 지키지 못한다.

**빌드가 도는 곳.** Overleaf는 호스팅 편집기다. 문서에 따르면 LaTeX 편집기이자 협업 플랫폼으로, Overleaf의 서버에서 컴파일하므로 아무것도 설치할 필요가 없다. 기본 컴파일러는 pdfLaTeX이고 LaTeX, XeLaTeX, LuaLaTeX도 고를 수 있으며, 프로젝트마다 TeX Live 버전을 고른다. 전체 기록, 변경 추적, Git 연동, Zotero 연결은 유료 기능이고, 무료 요금제의 기록은 최근 24시간과 레이블을 붙인 버전만 보여 준다(§10).

> [!note]- 더 깊이 · Deeper
> matplotlib의 포인트는 $1/72$ in(matplotlib, *Transformations tutorial*)이고 TeX의 포인트는 $1/72.27$ in이라 $72.27/72-1=0.375\%$ 차이가 난다. 가독성에는 아무 영향이 없지만, 3.5 in가 TeX로는 252.9 pt이고 matplotlib로는 252 pt인 이유가 이것이다. 패키지는 순서대로 불러오며 서로 부딪칠 수 있다. 둘이 같은 명령을 정의하면 로그가 그 이름을 알려 준다 — 쓰는 것만 불러올 이유가 하나 더 있는 셈이다.

### 5. 인용과 서지 목록: BibTeX, 서지 관리자, DOI

*한 문장으로:* 참고문헌 목록은 손으로 치는 것이 아니라 계산되는 것이다. `\cite{key}`마다 `.bib` 데이터베이스에서 찾고, 스타일이 찾은 것을 꾸미며, 거기 없는 키는 [?]로 찍힌다.

**문제.** 손으로 친 참고문헌 목록은 어긋나기 마련이다. 연도를 잘못 옮기고, 아무도 인용하지 않는 항목이 남고, 단락 하나가 옮겨 가면 번호가 본문과 맞지 않게 된다. 참고문헌 마흔 개에 공동 저자가 셋이면 반드시 어긋난다.

**생각.** 참고문헌은 데이터로 두고 목록은 빌드가 쓰게 한다. `.bib` 파일은 작은 데이터베이스다. 각 **항목**에는 유형 — `@article`, `@inproceedings`, `@book` — 과, `\cite`가 부르는 이름인 **인용 키**, 그리고 `author`, `title`, `journal`, `year` 같은 필드가 있다. 저자가 여럿이면 `and`로 잇고 저자마다 `성, 이름` 꼴로 쓸 수 있다(Overleaf, *Bibliography management with bibtex*). 본문은 키로 인용하고(`\cite{weissgerber2015}`), `\bibliographystyle{IEEEtran}`이 스타일을, `\bibliography{refs}`가 확장자 `.bib`를 뺀 데이터베이스 이름을 댄다. §1의 LaTeX 실행 사이에 돌아가는 BibTeX가 인용된 항목만 골라 스타일의 순서와 모양대로 꾸민다.

> **참고문헌 항목과 키의 정의.** **참고문헌 항목**(bibliography entry)은 *`.bib` 데이터베이스 안의 기록 — 유형, 키, 필드 — 으로, 논문이 그 키로 인용하는 것*이다. 키는 찾아보는 이름이지 찍히는 번호가 아니다. 조건 넷. (1) **키는 하나뿐**이며 인용한 키와 **대소문자까지 정확히** 같아야 한다. (2) **유형**이 스타일에게 어떤 필드를 기대할지 알려 준다. (3) **찍히는 목록은 계산된다** — 본문이 키를 인용한 항목만 정확히. (4) 데이터베이스에 **없는** 키를 인용하면 [?]가 찍히고 로그에 "undefined citation" 경고가 남는다.
>
> $$L=\{\,e\in\text{bib}:\ \text{key}(e)\in C\,\},\qquad U=C\setminus\text{keys}(\text{bib})$$
>
> $C$는 본문이 인용한 키의 집합, $L$은 찍히는 목록, $U$는 [?]로 찍히는 키다. 그러므로 아무도 인용하지 않은 항목은 결코 찍히지 않고, $U$에 든 키는 빌드를 몇 번 돌려도 [?]로 남는다.
>
> - **예**: RS1 본문이 `weissgerber2015`를 인용하고 `refs.bib`에 그 항목이 있으니 $U$는 비고, IEEEtran의 번호 스타일은 [1]을 찍는다. 끝까지 계산이 이 항목을 출판사 페이지에서 직접 만든다.
> - **비예**: 키가 `weissgerber2015`인데 `\cite{Weissgerber2015}`로 인용한 경우. 키는 대소문자를 가리므로(Overleaf) 인용한 키가 $U$에 들어가고, 몇 번을 돌려도 [?]다.
> - **왜 중요한가**: 목록은 인용하지 않은 항목을 찍거나 있는 항목을 빠뜨릴 수 없다. 하지만 오타와 없는 논문을 구별하지도 못하고, 찾지 못한 키를 알려 주는 것은 로그뿐이다.

**함정.** 데이터베이스가 옳아도 목록이 옳게 찍히려면 세 가지를 지켜야 한다. *키의 대소문자:* 이 페이지의 규칙은 제1저자 성을 소문자로 쓰고 연도를 붙이는 것(`weissgerber2015`)이며, 같은 저자의 같은 해 두 번째 논문이면 글자 하나를 더한다. *스타일은 제목의 대소문자를 바꾼다:* BibTeX의 표준 스타일은 제목에 자기 대문자 규칙을 적용하므로, 대문자를 지켜야 하는 단어는 중괄호로 감싸되 한 단어 전체를 감싸고 — `{RS1}`, `{ROS}` — 제목 전체를 감싸지는 않는다(TeX FAQ, *Capitalisation in BibTeX*). 첫 글자만 대문자로 남기는 스타일은 "Force limits for the RS1 arm"이라는 제목을 소스에 `{RS1}`이라고 적지 않은 한 "Force limits for the rs1 arm"으로 찍는다. *스타일은 아는 필드만 찍는다:* `plain`은 IEEEtran이 찍는 `url`을 무시하므로(Overleaf), DOI가 목록에 들어갔다고 여기기 전에 컴파일된 목록을 본다.

**참고문헌 관리자**는 `.bib` 파일의 출처인 서지 목록을 관리한다. Zotero는 BibTeX와 BibLaTeX로 내보낸다(Zotero, *Bibliographic Data Formats*). 컬렉션을 오른쪽 클릭해 *Export Collection…*을 고르면 된다(Zotero, *How do I export my Zotero library?*). 내보낼 때마다 키가 바뀔 수 있으므로(Overleaf는 Zotero가 업데이트되면 그럴 수 있다고 경고한다), 내보낸 `.bib`은 논문과 함께 커밋하고(§10), 다시 내보낼 때마다 로그에서 정의되지 않은 인용을 찾아본다.

**DOI**는 영구 식별자다. 접두사와 접미사를 빗금으로 잇고, `https://doi.org/`를 거쳐 대상의 현재 위치로 풀린다(DOI Foundation, *What is a DOI?*). Weissgerber 외의 DOI는 `10.1371/journal.pbio.1002128`로, 접두사가 `10.1371`, 접미사가 `journal.pbio.1002128`이다. 2017년 3월부터 적용된 Crossref의 표시 지침은 이것을 온전한 링크 `https://doi.org/10.1371/journal.pbio.1002128`로 찍고, 앞에 "doi:"를 붙이지 않으며 도메인에 "dx"를 넣지 않는다. 출판사 웹 주소는 바뀌어도 DOI는 남는다. 그러니 항목의 서지 정보는 DOI가 가리키는 페이지에서 가져온다. 검색 결과나 다른 논문의 참고문헌 목록에서 가져오면 거기 있던 오류가 논문에서 논문으로 그대로 옮겨 온다.

> [!note]- 더 깊이 · Deeper
> **BibTeX냐 biblatex냐.** BibTeX는 오래된 길이고 IEEEtran의 스타일이 쓰는 길이다. 표준 스타일로 `plain`, `unsrt`, `alpha`, `abbrv`, `ieeetr`가 있고, `\nocite{*}`는 데이터베이스 전체를 찍는다(Overleaf). 글을 바이트로만 다루고 유니코드 정렬은 모른다(CTAN). biblatex는 새 길이다. `\usepackage[backend=biber]{biblatex}`, 확장자를 *붙인* `\addbibresource{refs.bib}`, 그리고 목록이 들어갈 자리에 `\printbibliography`를 쓴다. 꾸미는 일이 LaTeX 매크로 안에서 이루어지고, 백엔드 Biber는 UTF-8을 읽고 유니코드 규칙으로 정렬한다(CTAN). Overleaf 문서는 biblatex를 권하지만 결정은 venue의 템플릿이 한다. Zotero에서는 BibLaTeX 같은 내보내기 형식을 Quick Copy 기본값으로 두면 Ctrl/Cmd-Shift-C가 고른 항목을 복사한다(Zotero, *Export*). Overleaf의 Zotero 연결은 유료 기능으로, 서지 목록을 읽기 전용 `.bib`으로 들여오고 손으로 새로 고치며, 방향은 한쪽뿐이다.

### 6. 벡터와 래스터: 그림 파일이 담는 것

*한 문장으로:* 래스터는 고정된 픽셀 격자를 담아서 선명도와 크기가 저장하는 순간 정해지고, 벡터는 그리는 지시를 담아서 어떤 크기에서도 선명하고 그리는 양만큼 값이 든다.

**문제.** 그림 1은 3.5 in 단에서 선명해야 하고, 리뷰어가 눈금 글자를 읽으려고 확대해도 선명해야 하며, 올릴 수 있을 만큼 작아야 한다. 이 셋이 지켜지는지는 파일의 종류에 달려 있는데, 그 종류는 흔히 그림 스크립트의 한 줄이 아무도 모르게 정한다.

**생각.** **래스터**(비트맵)는 색칠된 픽셀의 격자를 저장한다. **벡터** 파일은 지시를 저장한다 — 여기 원, 저기 선, 이 글꼴로 이 글자 — 그리고 보는 프로그램이 쪽이 어떤 크기로 보이든 그때마다 새로 그린다. PNG와 JPG는 래스터 형식이고, PDF와 EPS는 벡터 그림을 담을 수 있다(Overleaf, *Advanced LaTeX image topics*).

> **벡터와 래스터 그래픽의 정의.** **래스터**(raster)는 *픽셀의 격자*를 담는다. (1) 픽셀 수는 저장할 때 정해지고, (2) 압축 전 바이트 수는 픽셀 수에 비례해 는다. **벡터**(vector) 파일은 쪽의 단위로 적은 *그리는 지시*를 담는다. (3) 크기는 그리는 요소와 경로 꼭짓점의 수에 따라 늘고, (4) 인쇄되는 크기나 venue가 요구하는 해상도에 따라서는 늘지 않는다.
>
> $$B_{\text{raster}}=3\,(w\,r)(h\,r),\qquad B_{\text{vector}}\approx F_0+K\,b_{\text{obj}}$$
>
> $w\times h$는 인쇄 크기(인치), $r$은 해상도(dpi), 3은 압축 전 24비트 RGB 픽셀 하나의 바이트, $K$는 그리는 요소의 수, $F_0$와 $b_{\text{obj}}$는 이 페이지 대상의 교과용 숫자다. 그러므로 해상도를 두 배로 하면 래스터는 네 배가 되고 벡터는 그대로다.
>
> - **예**: 3.5 × 1.5 in의 그림 1. 600 dpi 래스터로는 $2100\times900=1{,}890{,}000$픽셀, 압축 전 5,670,000바이트다. 벡터로는 $20{,}000+61\times100=26{,}100$바이트로 217배 작고, 그림을 어떤 크기로 인쇄하든 26,100바이트 그대로다.
> - **비예**: PDF 안에 넣은 PNG. 파일 이름은 `.pdf`로 끝나도 그림은 여전히 픽셀이고, Overleaf는 PDF나 EPS에 비트맵을 담으면 디스크를 많이 차지한다고 적는다. matplotlib도 같은 실수를 소리 없이 한다. 확장자 없이 `fig.savefig("rs1_fig1")`를 부르면 `savefig.format`으로 넘어가는데 그 기본값이 `png`다(matplotlib, `savefig`).
> - **왜 중요한가**: 어떤 확대에서도 선명하고 어떤 해상도에서도 크기가 같은 것은 벡터뿐이다. 래스터의 품질은 저장하는 순간 정해진다.

**피할 수 없는 래스터라면, 해상도.** 장치 사진은 본래 래스터다. Overleaf는 사진에는 훨씬 공간 효율적인 JPG를, 그래프와 선 그림에는 PNG나 PDF를 권한다(Overleaf, *Optimising very large image files*). 인쇄된 래스터의 선명도는 **유효 해상도**, 곧 가로 픽셀 수를 인쇄 폭으로 나눈 값이 정한다.

$$r_{\text{eff}}=\frac{N_{\text{px}}}{w_{\text{print}}}$$

LaTeX는 주어진 폭이 얼마든 같은 픽셀을 늘려 채우기 때문이다. 그림 1 초안은 가로 640픽셀이다. 3.5 in 폭으로 인쇄하면 $640/3.5=182.9$ dpi, 픽셀 간격이 0.139 mm로 600 dpi의 0.042 mm보다 세 배 넘게 성기고, 5.47 pt로 인쇄되는 눈금 글자(§7)는 글자 크기 전체에 $5.47/72\times182.9=13.9$픽셀밖에 받지 못한다.

**함정.** 640픽셀 스크린숏을 이미지 편집기에서 2100픽셀로 늘리는 것. 파일은 이제 600 dpi라고 주장하지만 새 픽셀은 옛 픽셀에서 보간한 것이고, 흐림은 더 얇게 퍼질 뿐이다. 그림 스크립트를 더 높은 `dpi`로 다시 돌리는 것과는 다르다. matplotlib는 그림을 지시에서부터 다시 그리기 때문이다(§7). 그리고 그래프를 JPG로 저장하는 것. Overleaf는 그 형식을 사진 몫으로 둔다.

> [!note]- 더 깊이 · Deeper
> **벡터가 지는 때.** 벡터의 크기는 그리는 양만큼 는다. 본 실험은 시행마다 힘을 1 kHz로 2 s 기록하므로, 궤적 64개를 모두 그린 그림은 경로 꼭짓점이 $64\times2000=128{,}000$개다. 교과용 비용으로 $20{,}000+128{,}000\times15=1{,}940{,}000$바이트이고, 쪽이 보일 때마다 전부 다시 그려진다. P6 제어기의 주기인 200 Hz로 한 시간 기록하면 꼭짓점 720,000개, 10,820,000바이트로, 3.5 × 1.5 in 패널을 600 dpi로 압축 없이 저장한 래스터(5,670,000바이트)보다도 크다. 둘이 같아지는 곳은 $(5{,}670{,}000-20{,}000)/15\approx376{,}667$개다. 처방은 **빽빽한 층만** 래스터로 바꾸는 것이다. `rasterized=True`로 만든 요소는 나머지가 벡터인 PDF나 SVG 안에서 픽셀이 되고, 축과 글자는 벡터로 남으며, 픽셀의 크기는 `savefig`에 넘긴 `dpi`가 정한다. matplotlib 문서에 따르면 이렇게 하면 큰 데이터에서 그리기가 빨라지고 파일이 작아질 수 있지만 해상도가 고정된다(matplotlib, *Rasterization for vector graphics*).

### 7. 인쇄 크기의 글자, 그리고 그림 스크립트

*한 문장으로:* LaTeX는 그림을 주어진 폭에 맞게 줄이거나 늘리고 그 안의 모든 것 — 글자, 선, 표지 — 이 같은 비율로 변하므로, 잘못된 크기로 그린 그림은 글자도 잘못된 크기로 인쇄된다.

**문제.** 화면에서 초안의 10 pt 글자는 괜찮아 보였다. 단 안에서는 5.47 pt로 인쇄되어 논문의 어떤 글자보다 작다.

**생각.** `\includegraphics[width=\columnwidth]`는 그림을 다시 배치하지 않는다. 복사기의 확대·축소처럼 그림 전체의 배율을 바꿀 뿐이다. 6.4 in 파일을 3.5 in 단에 넣으면 글자, 선, 점이 모두 같은 비율로 줄어든다. matplotlib는 모든 그림을 6.4 × 4.8 in에 10 pt 글꼴로 시작하고, 눈금과 축 이름은 그 글꼴 크기에 상대적으로 정한다(기본 `matplotlibrc`, 버전 3.11.2). 이 기본값들은 그림이 인쇄될 단에 대해 아무것도 모른다.

> **인쇄 배율의 정의.** 포함된 그림의 **인쇄 배율**(print scale)은 *소스가 요구하는 폭에 맞추려고 LaTeX가 그림 파일 안의 모든 길이에 곱하는 수*다. 파일만의 성질도 쪽만의 성질도 아니고 둘을 함께 본 성질이다. 조건 넷. (1) **균일하다** — 폭만 주면 graphicx가 가로세로 비를 지킨다(Overleaf). (2) 파일 안의 **모든 것**, 글자 크기와 선 두께에 똑같이 걸린다. (3) 파일의 **저장된** 폭이 정하는데, `bbox_inches="tight"`를 쓰면 그림의 빠듯한 경계 상자만 저장되므로 그 폭이 달라진다(matplotlib, `savefig`). (4) **해상도와 무관하다** — `dpi`는 1인치에 픽셀이 몇 개 드는지를 바꿀 뿐, 그림이 몇 인치인지는 바꾸지 않는다.
>
> $$s=\frac{w_{\text{print}}}{w_{\text{file}}},\qquad f_{\text{print}}=s\,f_{\text{drawn}}$$
>
> $w$는 폭(인치), $f$는 글자 크기(포인트)다. 그러므로 6.4 in 그림에 10 pt로 그린 글자는 3.5 in 단에서 5.47 pt로 인쇄되고, 그 배율에서 8 pt를 찍으려면 14.63 pt로 그려야 한다.
>
> - **예**: 초안, $s=3.5/6.4=0.547$. 10 pt 글자는 5.47 pt로, 1.5 pt 선은 0.82 pt로, 6 pt 표지는 3.28 pt로 인쇄되고, 그림 높이는 계획한 1.5 in가 아니라 2.63 in가 된다.
> - **비예**: 같은 초안을 `dpi=600`으로 저장하는 것. $3840\times2880$픽셀이 되지만 여전히 폭 6.4 in, 배율 0.547이고 글자는 여전히 5.47 pt다. 해상도와 인쇄 배율은 서로 다른 손잡이다.
> - **왜 중요한가**: 독자가 보는 것은 인쇄된 크기뿐이다. 단보다 크게 그린 그림은 모든 글자를 화면에서보다 작게 인쇄하고, LaTeX 안의 어떤 설정도 그것을 되돌리지 못한다.

**규칙: 인쇄될 크기로 그린다.** `figsize`를 템플릿에서 읽은 단 폭과 계획한 높이로, 글꼴을 인쇄될 크기로 둔다. 그러면 $s=1$이고, 스크립트가 그리는 것이 곧 쪽에 인쇄되는 것이다. 영어 절의 matplotlib 스크립트가 그림 1을 이렇게 그린다. 이 컴퓨터에는 matplotlib가 없어 실행하지 않았고, 모든 호출을 matplotlib 3.11.2 문서와 대조했다. 요점은 네 줄이다. 글꼴을 8 pt로, 그림을 `figsize=(3.5, 1.5)`로 두고, A는 동그라미 B는 네모로 다른 줄에 찍으며, `rs1_fig1.pdf`로 저장해 확장자가 형식을 벡터 PDF로 고르게 한다. 논문에서는 `\includegraphics[width=\columnwidth]{rs1_fig1}`로 넣고 폭 지정은 안전장치로 남긴다. 실제 템플릿의 단이 3.4 in라면 배율은 $3.4/3.5=0.971$이고 8 pt는 7.8 pt로 인쇄되어 아무도 모르는 차이인 반면, 6.4 in 초안은 크기의 거의 절반을 잃었다.

**오차 막대의 함정.** `errorbar`의 `xerr`는 구간의 양 끝이 아니라 각 평균으로부터의 **거리**를 받는다. 두 줄 꼴에서 첫 줄은 아래쪽 거리, 둘째 줄은 위쪽 거리이고, 모두 음수가 아니어야 한다(matplotlib, `Axes.errorbar`). 스크립트는 `mean - lo`와 `hi - mean`, A라면 양쪽 모두 1.73 N을 넘긴다. 끝값을 그대로 넘기면(`xerr=np.vstack((lo, hi))`) A의 막대가 $10.66-8.93=1.73$ N에서 $10.66+12.39=23.05$ N까지 그래프 전체를 가로지르는데, 값이 모두 음수가 아니니 오류 메시지도 없다.

> [!note]- 더 깊이 · Deeper
> matplotlib의 다른 기본값(기본 `matplotlibrc`, 3.11.2): 100 dpi. 눈금과 축 이름은 `medium`, 제목은 `large`로 `font.size`에 상대적이다. 선 1.5 pt, 표지 6 pt. `savefig`는 파일 이름이나 `format`이 달리 말하지 않으면 PNG를 쓴다. PDF 출력은 Type 3 글꼴을 내장하는데 `pdf.fonttype = 42`로 TrueType으로 바꿀 수 있다 — venue의 PDF 검사가 TrueType 글꼴을 요구하면 바꿀 설정이다. `bbox_inches="tight"`는 캔버스가 아니라 그린 것의 빠듯한 경계 상자를 저장하므로, 저장된 폭과 그에 따른 인쇄 배율이 `figsize`와 달라질 수 있다.

### 8. 색, 한 가지 메시지, 무엇인지 말하는 오차 막대

*한 문장으로:* 그림은 비교 하나를 하고, 그 비교를 색 없이도 읽히게 하며, 표지와 막대가 정확히 무엇인지 캡션에서 말한다.

**문제.** 한 리뷰어는 논문을 흑백으로 인쇄한다. 다른 독자는 적록 색각 이상이 있다. 또 다른 독자는 RS1의 막대를 다른 논문의 막대와 견주는데, 하나는 표준편차이고 하나는 신뢰구간이라는 것을 모른다. 저마다 저자가 뜻한 것과 다른 그림을 읽는다.

**생각.** *메시지 하나:* 그림 1은 질문 하나에 답한다 — 팔마다 각 시행의 최대 힘이 10 N 선에 대해 어디에 떨어지는가? 평균의 차이조차 표 1에 맡긴다(4쪽 §4는 인쇄판에서 그 패널을 뺀다). 접촉 동안 힘이 어떻게 오르내리는지는 본 실험의 궤적이 보여 줄 두 번째 그림이지, 이 그림의 세 번째 패널이 아니다. *색은 돕는 것이지 싣는 것이 아니다:* matplotlib의 컬러맵 안내는 가장 흔한 색각 이상이 빨강과 초록을 가르기 어려운 것이라, 둘을 함께 쓰지 않으면 많은 문제를 피한다고 적는다(matplotlib, *Choosing Colormaps*). matplotlib의 `petroff10`처럼 구별이 유지되도록 설계한 색 순환이 더 돕고(아래 *더 깊이*), 나머지는 두 번째 통로가 맡는다. *이름 붙은 막대:* 캡션이 막대가 무엇이고 몇 번의 시행에 기대는지 말한다.

> **중복 부호화의 정의.** 그림이 보여 주는 범주의 모든 쌍이 *적어도 두 가지 시각 통로에서 다르고, 그중 적어도 하나가 색상이 아닐 때* 그 그림은 **중복 부호화**(redundant encoding)를 쓴다. 팔레트가 아니라 설계의 성질이다. 통로는 위치(어느 줄이나 패널), 표지 모양, 선 모양, 밝기, 표지 옆의 직접 이름표, 그리고 색상이다. 조건 셋. (1) 모든 쌍이 **적어도 두 통로**에서 다르다. (2) 그중 하나는 **색상을 잃어도 살아남는다** — 적록 색각 이상이 있는 독자에게도, 흑백 인쇄물에서도. (3) 대응 관계를 직접 이름표나 캡션으로 **밝힌다**.
>
> $$c(i,j)\ge2\quad\text{and}\quad c_{\neg\text{hue}}(i,j)\ge1\qquad\text{for every pair of categories } i\ne j$$
>
> $c(i,j)$는 범주 $i$와 $j$가 다른 통로의 수, $c_{\neg\text{hue}}$는 그중 색상이 아닌 것의 수다. 그러므로 색을 끄고도 A와 B를 가를 수 있으면 그 그림은 통과한다.
>
> - **예**: §7 스크립트의 그림 1. A와 B는 줄, 표지(동그라미 대 네모), 색에서 달라 $c=3$, $c_{\neg\text{hue}}=2$다. 한 색으로만 그린 4쪽의 그림도 줄과 글자 A, B로 갈라 $c=2$다.
> - **비예**: A는 빨간 점, B는 초록 점으로 한 줄에 섞고 범례를 단 그림. $c=1$, $c_{\neg\text{hue}}=0$이라 가장 흔한 색각 이상과 흑백 프린터가 모두 이 그림이 존재하는 이유인 비교를 지워 버린다.
> - **왜 중요한가**: 리뷰어는 인쇄하고, 프로젝터는 색을 바래게 하며, 어떤 독자는 그 차이를 보지 못한다. 색이 있어야 읽히는 그림은 어떤 독자는 읽을 수 없는 그림이다.

**오차 막대, RS1 위에서.** 같은 시행 열 번에서 막대 세 가지가 나오고, 막대 모양만 보고는 어느 것인지 알 수 없다. 팔 A의 표준편차는 2.41 N, 평균의 표준오차는 $2.414/\sqrt{10}=0.76$ N, 95% t-구간의 반폭은 $2.262\times0.764=1.73$ N이다. B는 각각 1.36, 0.43, 0.97 N이다. 표준편차는 시행 하나하나의 흩어짐을, 표준오차는 평균의 불확실성을 말하고, 구간은 표준오차에 $t_{0.975,9}=2.262$를 곱한 것이다([[02-foundations/ml-practice|9. ML 실무 §4]]. [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §4]]는 이것으로 실험 규모를 정한다). 같은 데이터 위에서 $\pm0.76$과 $\pm1.73$은 2.3배, $\pm2.41$과 $\pm0.76$은 $\sqrt{10}=3.2$배 차이가 난다.

**함정.** 직접 이름표로 될 일을 범례로 돌려 독자에게 색을 맞춰 보게 하는 것. "오차 막대"라고만 하고 어느 것인지 말하지 않는 캡션 — RS1의 캡션은 각 줄 아래 마름모와 막대가 평균과 그 95% t-구간이라고 밝히고 팔마다 짝짓지 않은 시행 열 번이라고 적으며, 결과 그림이 독자에게 빚진 나머지는 4쪽 §4가 나열한다. 그리고 Wilson 구간처럼 한쪽으로 치우친 구간을 ± 숫자 하나로 그리는 것 — §7의 두 줄 꼴 `xerr`나 `yerr`가 필요하다.

> [!note]- 더 깊이 · Deeper
> matplotlib는 범주용으로 설계한 색 순환을 싣고 있다. 3.10에서 색각 이상 모형을 써서 만든 `petroff10`이 들어왔고, 3.11에서 흔한 색각 이상에서도 인쇄에서도 구별이 유지되는 Okabe–Ito 순서가 들어왔다(릴리스 노트 3.10.0, 3.11.0). 연속적인 양에는 밝기가 꾸준히 올라가는 컬러맵을 권하는데, 그런 컬러맵은 흑백으로 인쇄해도 읽힌다(*Choosing Colormaps*).

### 9. 표: 세 줄의 괘선, 단위, 데이터가 받쳐 주는 자릿수

*한 문장으로:* 표의 괘선, 단위, 자릿수는 표가 주장하는 것의 일부이므로, 표는 가로 괘선 셋을 쓰고, 단위는 한 번만 적으며, 불확실성이 받쳐 주지 못하는 자릿수는 찍지 않는다.

**문제.** 분석 스크립트가 A의 평균 최대 힘을 10.6600 N으로 찍는다. 소수 넷째 자리는 꼼꼼해 보이지만, 95% 구간 폭이 3.5 N인 시행 열 번으로부터 평균을 1만분의 1 뉴턴까지 안다고 주장하는 셈이다.

**생각.** 표 속의 숫자는 크기와 함께 정밀도도 주장한다. 구조는 조용하게 둔다. booktabs는 가로 괘선 셋을 준다. 머리 위의 `\toprule`, 머리 아래의 `\midrule`, 끝의 `\bottomrule`. 그리고 숫자마다 불확실성이 받쳐 주는 자릿수만 싣는다. 이 페이지의 조판 권고는 이렇다. 세로 괘선을 쓰지 않는다. 단위는 머리나 행 이름에 한 번, "(N)"으로 적는다. 숫자는 오른쪽 정렬해 소수점이 줄을 맞추게 한다. 캡션은 venue의 템플릿이 두는 자리에 둔다(Overleaf에 따르면 위든 아래든 된다). 자릿수는 NIST의 불확실성 보고 지침이 예를 적는 방식을 따른다. 질량 100.021 47 g 옆에 표준 불확실성 0.35 mg — 불확실성은 유효숫자 두 자리, 값은 같은 소수 자리에서 끝난다(NIST TN 1297, §7).

> **불확실성에 맞춘 자릿수의 정의.** 숫자가 *함께 적힌 불확실성의 둘째 유효숫자 자리에서 마지막 자릿수가 끝날 때* 그 숫자는 **불확실성에 맞춰 찍힌**(printed to its uncertainty) 것이다. 데이터의 성질이 아니라 보고의 약속이다. 조건 넷. (1) 불확실성 $U$ — 구간의 반폭(한쪽으로 치우친 구간이면 긴 쪽)이나 표준오차 — 가 표나 캡션에 **이름으로 밝혀진다**. (2) $U$는 **유효숫자 두 자리**로 두고, 값은 같은 소수 자리로 반올림한다. (3) 반올림은 반올림하지 않은 값에서 **한 번만** 한다. (4) **한 열의 숫자는 소수 자리를 하나로 맞추며**, 어느 행이든 필요한 것 중 가장 거친 자리를 쓴다.
>
> $$d=\lfloor\log_{10}U\rfloor-1,\qquad x_{\text{printed}}=\text{round}\big(x,\ 10^{d}\big)$$
>
> $d$는 $U$의 둘째 유효숫자의 소수 지수이므로, 값과 그 구간은 모두 $10^{d}$에서 멈춘다. 반폭이 1 N과 10 N 사이면 $d=-1$, 곧 0.1 N 자리까지 찍는다.
>
> - **예**: A의 평균 10.66 N, 반폭 $U=1.727$ N이면 $d=\lfloor0.237\rfloor-1=-1$이라 10.7 N [8.9, 12.4]. B만 보면 $U=0.970$이라 $d=-2$, 7.50 [6.53, 8.47]이지만, A와 같은 열에서는 7.5 [6.5, 8.5]로 찍는다. 성공률은 Wilson 구간이 아래로 0.29와 0.30까지 내려가 $U$가 0.29와 0.30이므로 소수 둘째 자리까지 둔다. 0.60 [0.31, 0.83], 0.90 [0.60, 0.98].
> - **비예**: 두 번 반올림하기. 0.849를 곧장 소수 첫째 자리로 반올림하면 0.8이지만, 먼저 0.85로 만든 다음 사사오입으로 첫째 자리까지 줄이면 0.9가 된다.
> - **왜 중요한가**: 리뷰어는 10.66 N을 소수 둘째 자리까지 안다는 주장으로 읽는다. 표는 옆에 적힌 구간이 허락하는 만큼만 말해야 하고, [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사 §4]]가 결과 표의 모든 숫자에 요구하는 것도 그것이다.

**RS1 위에서.** 4쪽의 표 1은 힘을 소수 둘째 자리까지 찍는데, 그래야 그 쪽에서 손으로 한 계산과 칸마다 대조할 수 있기 때문이다. 제출하는 표는 이 약속대로 반올림한다. 영어 절의 LaTeX 목록이 그 표 1이다. 행은 4쪽의 것이고 자릿수와 조판만 이 페이지의 것이다. booktabs 괘선 셋 사이에 결과, A, B, 차이의 네 열을 두고, 힘은 10.7 [8.9, 12.4], 7.5 [6.5, 8.5], 3.2 [1.3, 5.0], 성공률은 0.60 (6/10) [0.31, 0.83], 0.90 (9/10) [0.60, 0.98], 0.30 [−0.08, 0.60]으로 찍는다. 차이 열도 같은 규칙을 따른다. 힘의 반폭 1.88 N은 3.2 [1.3, 5.0]을, 성공률 차이의 구간은 차이보다 0.38 아래까지 내려가므로 소수 둘째 자리를 준다. 구간을 좁히는 데 시행이 얼마나 드는지는 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §4]]가 다룬다.

**함정.** `"%.4f" % m`의 출력을 표에 붙여 넣는 것. Python은 실험이 잰 자릿수가 아니라 요청받은 자릿수를 찍는다(부동소수점 수가 어떻게 십진 텍스트가 되는지, `repr`와 `%.4f`가 왜 다른지는 [[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식 §2]]). 형식 지정은 표를 만드는 코드 안에 $U$를 기준으로 두고, 반올림은 한 번만 한다.

### 10. Git 저장소 속의 논문

*한 문장으로:* 논문은 소스 코드이므로 그림을 만드는 스크립트와 데이터와 함께 Git 저장소에 두고, 빌드가 다시 만들어 내는 것은 모두 빼 둔다.

**문제.** 제출하고 여섯 달 뒤, 리뷰어가 그림 1을 어떤 데이터로 만들었는지 묻는다. 노트북에 있는 PDF는 아무도 찾을 수 없는 초고에서 나왔다. [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사 §9]]는 논문, 코드, 데이터, 그림이 서로 맞는 버전을 가리키기를 요구하고, [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §7]]은 재현 가능한 결과가 기록해야 할 것을 나열한다. 논문 자체에 대해서는 그것이 곧 저장소다.

**생각.** 사람이 쓰는 것과 그림을 다시 만드는 것은 추적하고, 빌드가 매번 새로 쓰는 것은 뺀다. RS1의 저장소에는 `main.tex`(한 문장을 한 줄에 써서 고친 곳이 문장 하나의 변경으로 보이게 한다), 내보낸 뒤 커밋한 `refs.bib`(다시 내보내면 키가 바뀔 수 있으니까, §5), `data/pilot.csv`를 읽어 `figures/rs1_fig1.pdf`를 쓰는 `figures/fig1.py`(그래서 그림 1과 표 1이 같은 데이터에서 나온다), 그리고 그 그림 PDF(공동 저자나 Overleaf가 Python을 돌리지 않고도 논문을 빌드하도록 커밋한다)가 들어 있다.

**규칙, RS1 저장소 위에서.** 뺄 것은 `.gitignore`가 정한다. 빗금이 없는 패턴은 어느 깊이에서나 맞고, 빗금으로 시작하는 패턴은 그 `.gitignore` 파일이 있는 깊이에서만 맞으며, `*`는 빗금을 뺀 무엇에나 맞는다(Git 문서, *gitignore*). 영어 절의 `.gitignore`는 주석 두 줄과 패턴 넷 — `*.aux`, `*.log`, `*.bbl`, 그리고 빗금을 붙인 `/main.pdf` — 으로 되어 있다. 그 아래 목록은 실제로 확인한 결과다(macOS 26.6.2, arm64의 Git 2.46.0, 빈 파일로 만든 저장소 사본, 출력은 찍힌 그대로). `git status`의 목록에서 빌드 파일이 빠졌고, `git check-ignore -v -n`이 파일마다 숨긴 규칙을 대며, 어느 규칙에도 맞지 않는 그림 파일에는 `::`를 붙인다. 그림은 계속 추적된다.

**함정.** 그냥 `*.pdf`라고 썼다면 그림 PDF까지 숨겼을 것이다. 논문 PDF에 빗금을 붙여 고정한 이유다. `.gitignore`는 Git이 아직 추적하지 않는 파일에만 작용하므로, 실수로 커밋한 빌드 파일은 먼저 `git rm --cached`로 인덱스에서 빼야 한다(Git 문서). 그리고 Overleaf의 Git 연동은 유료이며, 복제하고 끌어오고 밀어 넣을 수는 있지만 브랜치도 태그도 지원하지 않고, 무료 요금제의 기록은 최근 24시간과 레이블 붙인 버전만 남긴다. 그러니 제출한 버전에는 Overleaf 기록에서 레이블을 붙이고, 그 태그 — 제출한 PDF를 만든 커밋 — 는 Overleaf가 돌릴 수 없는 스크립트와 데이터 옆, 자기 복제본에 둔다.

### 대상으로 한 번 끝까지 · Worked case

§1, §3, §5–§9를 모두 쓰므로 §10 뒤에 둔다. 그림 1을 첫 초안에서 교과용 템플릿의 단까지 옮기고, 파일을 두 방식으로 값 매기고, 그림이 기대는 참고문헌 하나를 출판사 페이지에서 인쇄된 목록까지 옮기고, 표 1의 자릿수를 정한다. 기호는 이 페이지 대상의 것이다.

**1단계 — 단.** 두 단과 그 사이 간격이 본문 폭을 채우므로(§1)

$$w=\frac{W-g}{2}=\frac{7.25-0.25}{2}=3.5\ \text{in},$$

TeX 포인트로 $3.5\times72.27=252.9$ pt, 88.9 mm다. 실제 템플릿에서는 `\the\columnwidth`가 찍는 바로 그 숫자다(§4).

**2단계 — 단에 들어간 초안.** 초안은 matplotlib 기본값 6.4 × 4.8 in에 10 pt 글자로 그려 100 dpi, 640 × 480 PNG로 저장했다. `\includegraphics[width=\columnwidth]`는 그 안의 모든 길이에 같은 수를 곱하므로(§7)

$$s=\frac{w}{w_{\text{file}}}=\frac{3.5}{6.4}=0.547,\qquad f_{\text{print}}=0.547\times10=5.47\ \text{pt}<f_{\min}=8\ \text{pt}$$

이다. 글자도 다른 모든 것과 함께 줄기 때문이다. 그림은 $4.8\times0.547=2.63$ in 높이로 인쇄되어 캡션까지 3.13 in, 곧 $0.35H$를 차지한다 — §3의 위쪽 한도 안이지만 계획보다 1.13 in 더 쓴다. 640픽셀이 3.5 in에 퍼지니 $r_{\text{eff}}=640/3.5=182.9$ dpi로 요구한 600의 3분의 1에도 못 미친다(§6). 두 실패는 서로 독립이다. `dpi=600`으로 저장하면 둘째는 고쳐지고 첫째는 남는다. 파일이 여전히 6.4 in 폭이기 때문이다(§7).

**3단계 — 인쇄 크기로 그리기.** `figsize=(3.5, 1.5)`, `font.size = 8`이면 배율은 $3.5/3.5=1.00$이다. 글자는 8 pt로 인쇄되고, 그림은 1.5 in, 캡션까지 2.0 in, 곧 $0.22H$라 `[t]`가 단의 맨 위에 둔다(§3). `rs1_fig1.pdf`로 저장하면 셀 픽셀이 없다.

**4단계 — 파일, 두 방식으로.** 벡터로는 $B=F_0+K\,b_{\text{obj}}=20{,}000+61\times100=26{,}100$바이트다. 600 dpi 래스터로는 $(3.5\times600)(1.5\times600)=2100\times900=1{,}890{,}000$픽셀, 압축 전 $3\times1{,}890{,}000=5{,}670{,}000$바이트로 벡터의 217배다. 300 dpi면 $1050\times450$픽셀에 1,417,500바이트로 54배다. 해상도를 반으로 줄이면 래스터는 4분의 1이 되고 벡터는 그대로다(§6).

**5단계 — 참고문헌.** DOI `10.1371/journal.pbio.1002128`은 PLOS Biology의 논문 페이지로 풀리고, 그 페이지가 대문자까지 그대로인 제목, 저자 넷, 13권 4호, 논문 번호 e1002128, 2015년 4월 22일 게재를 준다. 다른 곳의 인용이 아니라 그 페이지에서(§5) 만든 항목이 영어 절의 `@article{weissgerber2015, …}`다. 키는 이 페이지의 규칙을 따른다. PLOS는 논문에 쪽이 아니라 번호를 매기고, 자기가 제안하는 인용 형식에서도 쪽 범위 자리에 논문 번호를 쓰므로 항목도 `pages`에 e1002128을 둔다. 제목에는 중괄호가 필요한 단어가 없다. 첫 글자만 대문자로 남기는 스타일이 "bar and line graphs"로 찍어도 올바른 영어이고, 지켜야 할 약어나 고유명사가 없다. `doi` 필드에는 DOI만 적고, 스타일이 찍는다면 `https://doi.org/10.1371/journal.pbio.1002128`로 읽혀야 한다. §1의 빌드를 거치면, 첫 실행이 키를 `main.aux`에 적고 [?]를 찍으며, BibTeX가 `refs.bib`에서 키를 찾아 `main.bbl`을 쓰고, 둘째 실행이 목록을 찍고, 셋째 실행이 [1]을 찍는다. §5의 $U$는 비어 있고 로그에 정의되지 않은 인용이 없다.

**6단계 — 표 1의 자릿수.** §9의 약속대로다. A의 평균 10.66 N과 반폭 1.73 N은 $d=-1$, 곧 10.7 [8.9, 12.4]. B의 반폭 0.97 N은 혼자라면 $d=-2$지만 열은 A의 $d=-1$을 따라 7.5 [6.5, 8.5]. 차이는 반폭 1.88 N이라 3.2 [1.3, 5.0]. 표준편차는 유효숫자 두 자리로 2.4와 1.4 N.

**같은 숫자, 계산으로.** 영어 절의 Python 목록이 교과용 숫자와 예비 실험의 힘 스무 개에서 1–4단계와 6단계를 다시 계산하고, 그 출력이 위의 숫자를 모두 확인해 준다. 출력의 `d` 열은 행마다 자기 소수 자리이고, B는 열의 자리로 찍힌다. 한 줄로 줄이면 이렇다. 초안은 배율과 픽셀이라는 서로 독립인 두 이유로 실패했고, 인쇄 크기로 그려 벡터로 저장한다는 결정 하나가 둘 다 고친다. 참고문헌 목록과 표는 빌드와 불확실성이 허락하는 만큼만 찍는다.

### 11. 이 페이지가 다루지 않는 것

RS1 논문이 무엇을 논증하는지, 결과 표와 그림을 어떻게 고르는지, 한계와 심사는 [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 동료 심사]]가 다룬다. 숫자 뒤의 통계는 4쪽과 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성]]이, 어느 venue로 보낼지와 venue마다의 규칙은 [[06-research-practice/venue-strategy|5. Venue 전략]]과 venue의 저자 안내가 다룬다. Git 자체 — 커밋, 브랜치, 병합 — 는 여기서 가르치지 않고 안다고 가정한다. 그것은 [[02-foundations/tools/git-research-code|12.2 연구 코드를 위한 Git]]이고, 그림과 표를 만드는 스크립트의 Python은 [[02-foundations/tools/python-research-code|12.3]], 그 스크립트가 읽는 CSV와 JSON은 [[02-foundations/tools/config-data-formats|12.4]]다. LaTeX 안에서 그리기(TikZ, pgfplots), 슬라이드와 포스터, 매크로와 패키지 작성, §7의 Type 3–TrueType 전환을 넘어서는 글꼴 문제, 색을 넘어서는 접근성(예를 들어 그림의 대체 텍스트), 워드프로세서와 온라인 공유 문서, 채택 뒤의 교정과 제작 단계도 다루지 않는다.

### 읽고 나면

- [ ] LaTeX 실행 한 번이 무엇을 읽고 쓰는지, 첫 실행이 왜 "??"와 "[?]"를 찍는지, RS1 논문이 안정되기까지 몇 단계가 드는지 말한다.
- [ ] `\label`을 맞는 번호를 가리키는 자리에 두고, `\caption` 앞에 둔 레이블이 무엇을 찍는지 말한다.
- [ ] 주어진 높이의 플로트가 어디로 갈 수 있는지, `h` 하나가 무엇이 되는지, 논문이 왜 venue의 템플릿에서 시작하는지 말한다.
- [ ] DOI가 가리키는 페이지에서 키, 필요한 중괄호, DOI를 갖춘 BibTeX 항목을 쓰고, 키가 왜 [?]로 찍히는지 말한다.
- [ ] 그림의 인쇄 배율, 인쇄되는 글자 크기, 유효 해상도, 벡터와 래스터의 크기를 계산한다.
- [ ] 그림이 중복 부호화를 쓰는지, 캡션이 막대가 무엇인지 말하는지 점검하고, 표의 숫자를 불확실성이 받쳐 주는 자릿수로 찍는다.
- [ ] 논문 저장소가 무엇을 추적하고 `.gitignore`가 무엇을 빼는지 말한다.

### 스스로 점검

1. 공동 저자의 PDF 곳곳에 "Fig. ??"와 "[?]"가 찍혀 있다. 무슨 일이 있었고, 무엇은 고칠 필요가 없는가?
2. 끝까지 빌드했는데도 인용 하나가 [?]로 남는다. 어디를 보며, 가장 그럴듯한 원인 둘은 무엇인가?
3. `\label`은 왜 `\caption` 뒤에 와야 하며, 앞에 오면 본문은 무엇을 찍는가?
4. `[h]`로 쓴 그림이 다음 단의 맨 위에 나타났다. 무언가 잘못되었는가?
5. 그림 1 초안을 `dpi=600`으로 다시 저장한다. 두 문제 중 무엇이 고쳐지고 무엇이 남는가?
6. 표 1이 B의 평균을 한 초안에서는 7.50, 다른 초안에서는 7.5로 찍는다. §9의 약속을 따르는 것은 어느 쪽이며, 왜 답이 열에 따라 달라지는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 엔진을 한 번만 돌린 결과라, 레이블도 참고문헌도 아직 알 수 없었다. 망가진 것이 아니라 덜 끝난 것이다. 소스에는 고칠 것이 없다. 끝까지 빌드하거나 Overleaf에 맡긴다(§1).
> 2. 로그를 본다. "undefined citation" 경고가 키를 알려 준다. 키가 인용한 모양대로 데이터베이스에 없거나 — 오타, 또는 대소문자 차이(키는 대소문자를 가린다) — 항목이 문서가 불러오지 않는 파일에 있다. `\bibliography{...}`가 다른 파일을 가리키거나 파일 이름의 대소문자가 다른 경우인데, Overleaf를 포함해 파일 이름의 대소문자를 가리는 시스템이 있다(§5).
> 3. 플로트 안에서 번호를 매기는 것은 `\caption`이고, 레이블은 그보다 먼저 매겨진 번호를 기록한다. 캡션 앞에 두면 레이블은 그림이 든 절의 번호를 기록하므로, 그림이 4절에 있으면 본문은 "Fig. 4"라고 쓴다 — 참조가 정의되기는 했으니 경고도 없다(§2).
> 4. 아니다. `h` 하나는 허용되지 않아 LaTeX가 `ht`로 바꾸었고, 플로트는 규칙이 허락하는 첫 자리로 갔다. "아래"가 아니라 `\ref`로 가리키고, 글 가까이 두고 싶으면 환경을 소스에서 더 앞에 옮긴다(§3).
> 5. 픽셀은 고쳐진다. $6.4\times600=3840$픽셀이 3.5 in에 퍼지면 1,097 dpi다. 글자는 남는다. 파일이 여전히 6.4 in 폭이라 배율 0.547로 줄어 5.47 pt로 인쇄된다. 인쇄 크기로 그리면 둘 다 고쳐진다(§6, §7).
> 6. 7.5다. B만 보면 반폭 0.97 N이 $d=-2$를 주어 7.50이지만, 반폭 1.73 N으로 $d=-1$인 A와 한 열에 있으면 모든 행이 0.1 자리까지 찍혀 소수점이 줄을 맞추고 열 전체가 한 정밀도로 읽힌다(§9).

### 과제 · Problem set

Tier B. 이 페이지와 그 선수 지식, RS1만 가지고 손으로 푼다. 모든 문항은 끝까지 계산의 손잡이 하나 — 그림의 폭, 해상도, 시행 수, 참고문헌 — 를 바꾸므로 이 페이지의 숫자를 베낄 수 없다.

1. **그리기(Draw).** 그림 1을 교과용 템플릿의 전폭 `figure*`로, matplotlib 기본값 6.4 × 4.8 in로 그려 `dpi=300`으로 저장했다. 7.25 × 9.0 in 본문 영역을 같은 척도로 그리고 그림을 제자리에 둔 다음, 인쇄 배율, 0.5 in 캡션을 포함한 인쇄 높이를 $H$에 대한 비율로, 10 pt 글자의 인쇄 크기를 $f_{\min}$과 견주어, 유효 해상도를 600 dpi와 견주어 표시한다. 넓은 그림이 초안의 두 실패 중 무엇을 없애고 무엇은 못 없애는지, LaTeX가 이 그림을 쪽의 어디에 둘 수 있는지 말한다.
2. **유도(Derive).** (a) 그림을 7.25 × 2.5 in로 다시 계획해 그 크기로 그렸다. 600 dpi 래스터라면 픽셀 수, 압축 전 바이트, 26,100바이트 벡터에 대한 비를 구하고, 대신 6.4 in 폭으로 그렸다면 8 pt로 인쇄되게 할 글자 크기를 구한다. 캡션을 포함한 높이를 $H$에 대한 비율로 구한다. (b) 본 실험은 팔마다 32회다. 예비 실험의 표준편차가 그대로라면 $t_{0.975,31}=2.0395$로 각 팔의 95% 반폭과 §9가 그때 찍는 소수 자리를 구하고, $t\approx1.96$으로 A의 평균이 소수 셋째 자리를 얻으려면 팔마다 대략 몇 회가 필요한지 구한다. (c) 4쪽이 Wilson 구간의 근거로 인용하는 논문 — Lawrence D. Brown, T. Tony Cai, Anirban DasGupta, "Interval Estimation for a Binomial Proportion", *Statistical Science* 16(2): 101–133, 2001년 5월, DOI 10.1214/ss/1009213286, 출판사 페이지가 주는 그대로 — 의 BibTeX 항목을, 이 페이지의 규칙에 따른 키, 필요한 곳의 중괄호, Crossref 지침대로의 DOI와 함께 쓴다.
3. **해석(Interpret).** 연구실 동료가 RS1 논문의 첫 완성 초안을 `pdflatex` 한 번으로 만든 PDF로 보내 왔다. 영어 절의 발췌와 함께 온 메모는 이렇다. 그림 1은 `figsize`도 `dpi`도 정하지 않은 스크립트에서 `fig.savefig("rs1_fig1")`로 저장했다. x축 이름은 "Peak force"다. A는 빨간 점, B는 초록 점으로 한 줄에 섞었다. 표 1의 숫자는 `print("%.4f" % m)`에서 붙여 넣어 "10.6600 ± 2.4144"와 성공률 "0.9000"이다. Zotero에서 내보낸 `refs.bib`의 키는 `weissgerber2015`이다. 결과는 논문의 4절이다. 발췌 쪽에서는 `\cite{Weissgerber2015}`로 인용하고, 그림 환경을 `[h]`로 열며, `\label{fig:peak}`를 `\caption`보다 먼저 쓰고, 캡션은 "A는 빨강, B는 초록"이라고만 한다. 결함마다 PDF 독자가 보는 증상과 고치는 법을, 그것이 나온 이 페이지의 절과 함께 댄다.

> [!note]- 그리는 법 · How to draw it
> - 본문 영역부터 같은 척도로 — 7.25 × 9.0 in, 3.5 in 두 단과 0.25 in 간격 — 그리고, `figure*`를 두 단에 걸쳐 맨 위에 둔다. 본문 쪽에서 전폭 플로트가 가는 곳은 거기뿐이다.
> - 그리기 전에 그림에 배율을 먼저 곱한다. 인쇄 높이는 그린 높이의 $s$배이고 그 위에 캡션이 더해진다. 합을 $H$에 대한 비율로 적어 `\dbltopfraction`의 0.7 옆에 둔다.
> - 인쇄되는 글자 크기는 $s\,f_{\text{drawn}}$으로 적어 8 pt 최소치 옆에 둔다. 배율이 1보다 크면 글자가 커지고, 작으면 작아진다.
> - 유효 해상도는 가로 픽셀 수를 인쇄 인치로 나눠 적는다. 가로 픽셀은 그린 폭 곱하기 저장한 `dpi`이고, LaTeX에서 무엇을 해도 바뀌지 않는다.
> - 두 점검은 떼어 둔다. 글자 크기와 해상도는 서로 무관하게 통과하거나 실패하고, 이 변형은 둘의 결과가 갈리도록 골랐다.

> [!tip]- 정답 · Solutions
> 1. $s=7.25/6.4=1.133$. 그림은 $4.8\times1.133=5.44$ in 높이, 캡션까지 5.94 in, 곧 $0.66H$로 인쇄된다. `\dbltopfraction`의 0.7보다 작으니 쪽의 맨 위(본문 쪽에서 `figure*`가 갈 수 있는 유일한 곳)나 플로트 쪽에 들어가고, 맨 아래에는 결코 가지 않는다. 글자는 $10\times1.133=11.33$ pt로 8보다 크다. 그 실패는 사라졌다. $6.4\times300=1920$픽셀이 7.25 in에 퍼져 264.8 dpi로 600에 못 미친다. 이 실패는 남는다. 늘리면 픽셀이 더 성기게 퍼질 뿐이다. 게다가 두 줄짜리 띠 그림이 5.44 in 높이로 쪽의 3분의 2를 차지한다. 중요한 손잡이는 그린 크기다.
> 2. (a) $7.25\times600=4350$ 곱하기 $2.5\times600=1500$: 6,525,000픽셀, 압축 전 19,575,000바이트로 벡터(같은 요소 61개, 26,100바이트)의 750배다. 6.4 in 폭으로 그렸다면 $s=7.25/6.4=1.133$이라 글자를 $8/1.133=7.06$ pt로 그린다. 캡션까지 $2.5+0.5=3.0$ in, $0.33H$로 0.7보다 작다. (b) A: $2.0395\times2.4144/\sqrt{32}=0.870$ N, B: $2.0395\times1.3556/\sqrt{32}=0.489$ N으로 둘 다 $d=-2$라, 본 실험의 표는 소수 둘째 자리를 얻는다. 셋째 자리는 $U<0.1$ N이 필요하므로 $n>(1.96\times2.4144/0.1)^2=2239.4$, 곧 팔마다 약 2,240회(정확한 $t$ 분위수로는 2,242회)로, 계획한 32회의 70배다.
>    (c) 영어 절의 `@article{brown2001, …}` 항목이다. 저자 셋을 `and`로 잇고 `성, 이름` 꼴로 적으며, 제목 "Interval Estimation for a Binomial Proportion", 학술지 Statistical Science, 16권 2호, 쪽 `101--133`, 2001년, `doi = {10.1214/ss/1009213286}`. 제목에는 중괄호가 필요한 단어가 없다. "binomial proportion"은 첫 글자만 대문자로 둔 문장에서도 올바른 영어이고, 지킬 약어나 고유명사가 없다. Crossref 지침대로라면 DOI는 `https://doi.org/10.1214/ss/1009213286`으로 찍힌다.
> 3. 결함 여덟. (i) 엔진 한 번: 곳곳의 "Fig. ??"와 "[?]" — 끝까지 빌드한다(§1). (ii) `\caption` 앞의 `\label`: 빌드가 끝나면 본문이 4절의 번호인 "Fig. 4"를 경고 없이 찍는다 — 레이블을 캡션 뒤로(§2). (iii) `[h]` 하나는 경고와 함께 `ht`가 되고 그림은 어차피 떠 간다 — `[t]`나 기본값을 쓰고 `\ref`로만 가리킨다(§3). (iv) 키 `weissgerber2015`에 대해 `\cite{Weissgerber2015}`: 끝까지 빌드해도 [?] — 키를 정확히 인용한다(§5). (v) 확장자 없는 `savefig`가 640 × 480 PNG를 썼고 0.547배로 줄어 183 dpi에 5.47 pt 글자 — 3.5 × 1.5 in에 8 pt로 그려 `rs1_fig1.pdf`로 저장한다(§6, §7). (vi) 단위 없는 축 — "Peak contact force (N)"(§8, §9). (vii) 한 줄에 빨강 대 초록, $c=1$, $c_{\neg\text{hue}}=0$, 색 이름만 댄 캡션 — 줄과 표지를 나누고 색각에 안전한 색 순환을 쓰며, 캡션에 대응 관계와 막대의 정체와 팔마다 시행 수를 적는다(§8). (viii) "10.6600 ± 2.4144"와 "0.9000": 10.7(평균의 반폭이 1.73 N), 표준편차 2.4, 성공률 0.90 [0.60, 0.98](§9).

### 출처

- LaTeX2e 비공식 참고 매뉴얼, CTAN [latex2e-help-texinfo](https://ctan.org/pkg/latex2e-help-texinfo) — 빌드의 출력 파일(§2.2–2.3), 클래스 옵션(§3.1), 단(§5.2), 플로트(§5.7).
- CTAN 패키지 페이지 — [amsmath](https://ctan.org/pkg/amsmath), [graphicx](https://ctan.org/pkg/graphicx), [booktabs](https://ctan.org/pkg/booktabs), [siunitx](https://ctan.org/pkg/siunitx), [biblatex](https://ctan.org/pkg/biblatex), [biber](https://ctan.org/pkg/biber), [bibtex](https://ctan.org/pkg/bibtex), [IEEEtran](https://ctan.org/pkg/ieeetran): 패키지마다의 용도와 버전.
- [The TeX FAQ](https://texfaq.org/) — 플로트의 배치와 순서, `\caption` 뒤의 `\label`, BibTeX의 대소문자, `\the`, `~`.
- [Overleaf 문서](https://docs.overleaf.com/)와 [Learn LaTeX](https://www.overleaf.com/learn) — 빌드 네 단계, [?], 키, 수식, 그림, 이미지 형식, 요금제, Git과 Zotero의 제약, siunitx 3.
- [Zotero 문서](https://www.zotero.org/support/) — BibTeX·BibLaTeX 내보내기, Quick Copy.
- [Matplotlib 3.11.2 문서](https://matplotlib.org/stable/) — 기본값, `savefig`, 래스터화, `errorbar`, 색 순환과 컬러맵.
- [DOI Foundation](https://www.doi.org/the-identifier/what-is-a-doi/)과 [Crossref 표시 지침](https://www.crossref.org/display-guidelines/) — DOI가 무엇이며 어떻게 찍는가.
- [NIST TN 1297 §7](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty) — §9의 약속이 따르는 보고 예.
- [Git 문서: gitignore](https://git-scm.com/docs/gitignore) — 패턴 규칙.
- Weissgerber 외, *PLOS Biology* 13(4): e1002128 (2015), [doi.org/10.1371/journal.pbio.1002128](https://doi.org/10.1371/journal.pbio.1002128) — 끝까지 계산의 항목.
- Brown, Cai & DasGupta, *Statistical Science* 16(2): 101–133 (2001), [doi.org/10.1214/ss/1009213286](https://doi.org/10.1214/ss/1009213286) — 과제 2(c)의 항목.
