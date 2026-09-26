---
title: 2. Computer Vision
tags: [deep-learning, computer-vision, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Translate pixels into classification, detection, segmentation, depth, and 3D outputs while tracking geometry, tensor shapes, supervision, and metrics."
mastery-when: "Raise when visual representation, geometry, or perception evaluation carries the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/foundations/index|1. Learning Systems]], [[02-foundations/signal-processing|6. Signal Processing]], and [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]]. Object **D2** from [[03-deep-learning/lab-objects|0. Lab Objects]], at the pixel values frozen below; the Tier A lab in §5 needs NumPy and nothing else. If NumPy is new, read [[02-foundations/tools/python-research-code|12.3 Python for Research Code §3–§4]] (arrays, shapes and vectorised loops) first.
> [[03-deep-learning/foundations/index|1. 학습 시스템]], [[02-foundations/signal-processing|6. 신호처리]], [[04-robotics/geometric-perception-calibration|3.5 기하 인식]]. 대상은 [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D2**이고 픽셀 값은 아래에서 고정한다. §5의 Tier A 실습에는 NumPy만 있으면 된다. NumPy가 처음이면 [[02-foundations/tools/python-research-code|12.3 연구 코드를 위한 Python §3–§4]](배열, shape, 벡터화한 반복)를 먼저 읽는다.

## English

> [!note] Why this matters · 왜 배우는가
> This page's chip sits in the learning-and-adaptation band of the [[physical-ai-map|Physical AI Map]], but what it powers is the first layer of the physical-AI stack in [[07-research-program/index|7. Research Program §5]], perception: in *"install that panel on the frame"* it serves step 2, *identify panel and frame*, where pixels become labels, boxes, masks and depths. A perception number cannot be read until its threshold and its averaging unit are known. On D2, the page's frozen $8\times8$ test image ([[03-deep-learning/lab-objects|0. Lab Objects]]), one box at IoU $0.6$ is a hit at $0.5$ and a miss at $0.75$, so the same three predictions score $\mathrm{AP}@0.5=0.833$ or $\mathrm{mAP}@[.5{:}.95]=0.600$; a segmenter that never finds a thin cable still reports mIoU $0.76$ on a 20-class benchmark; and a box that passes IoU $0.5$ may still sit $111$ mm off, where S1, the construction track's facade-panel task ([[05-construction-robotics/site-engineering|2.5]]), needs its two holes within $\pm5$ mm (§3). [[03-deep-learning/vlm/index|3. VLM §1]] puts a text encoder beside an image encoder like this one, [[03-deep-learning/vla/index|4. VLA]] hands the image features to its policy as the observation, and [[05-construction-robotics/imitating-contact|10. Imitating Contact §1]] assumes a camera that reads the hole's offset with a $0.5$ mm standard deviation; on the dissertation path ([[07-research-program/index|7. Research Program §8]]) this is the second of block 4's deep-learning pages, deep-learning sessions 11–13. After it you can compute a convolution's output size and parameter count, an IoU, an AP and an mIoU by hand, and say which robot claim a vision metric supports and which it does not.

> [!note] First pass · 처음이라면
> About three sessions of 60–90 minutes, rows 11–13 of the [[03-deep-learning/index|deep-learning schedule]]; the first two are the first pass. **Session 1:** the Running object, the picture and the Worked case, by hand with the solution covered: $y_{0,2}=40$, $n_{\text{out}}=6$, $\mathrm{IoU}=0.6$. **Session 2:** §1–§4, then self-check 1–5 and problems 1–3. **Session 3:** run §5's listing, read its three sweeps and the figure, and do problem 4. Finish by explaining in your own words why the same three boxes score $0.833$ and $0.600$, and why IoU $0.5$ cannot certify S1's $\pm5$ mm.

### Running object: D2

**D2**, one of the deep-learning track's frozen tensor objects D1–D6 of [[03-deep-learning/lab-objects|0. Lab Objects]], is one grayscale $8\times8$ image. Divide it into non-overlapping $4\times4$ patches: a $2\times2$ grid, hence four patch tokens. Flattening gives 16 values per token; a learned projection $E\in\mathbb R^{16\times d}$ maps each to dimension $d$.

The catalog fixes D2's size and patch grid but leaves its pixels open, so this page — D2's home — freezes them here and never changes them again:

$$I[i,j]=\begin{cases}0,&j\le3\\10,&j\ge4\end{cases}\qquad i,j\in\{0,\dots,7\}$$

a vertical step edge of height 10 falling exactly between columns 3 and 4, which is also the patch boundary. Two consequences to keep in mind, because the rest of the page uses both. Patches 1 and 3 (the left column of the grid) are all zeros and patches 2 and 4 are all tens, so **two of the four tokens are bit-identical to two others** — without position information, attention cannot tell the top-left patch from the bottom-left one. And the edge is a single discontinuity with a known location, so every convolution response below can be predicted before it is computed.

Two more page-local objects are frozen here for §2's metrics, both in D2's pixel coordinates. **Boxes**, written $(x_1,y_1,x_2,y_2)$ with the second corner exclusive: ground truth $G_1=(0,0,4,4)$ and $G_2=(4,4,8,8)$, each of area 16; predictions $P_1=(0,0,4,4)$ at confidence $0.90$, $P_2=(3,3,7,7)$ at $0.80$, $P_3=(4,3,8,7)$ at $0.60$. **Masks**, a two-class segmentation of the same image: the "cable" class occupies column 4 only — 8 pixels of 64 — and everything else is background.

*Scope: this page teaches how a visual input becomes a tensor (convolution arithmetic and patch tokens), how the choice of output turns a backbone into a task, and how to read the metrics that score those outputs — IoU, mAP, and per-class mIoU — on objects small enough to recompute by hand. It does not teach the camera geometry underneath the pixels, which is [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §1]]; nor depth recovery and 3D reconstruction, which are [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §2]] and the 3D entries of the [[01-canonical-papers/canonical-list|canonical list]]; nor the training machinery — loss, optimizer, step size — which is [[03-deep-learning/foundations/index|1. Learning Systems §1–§2]] and its §6 lab; nor attention itself, which is the [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer note]] and, worked on this page's D2, [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]]. The depth and 3D rows of §2's table are named so the table is complete, the depth metrics are defined in §3, and neither row is taught here.*

### The picture

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="D2's 8 by 8 step-edge image with its 2 by 2 patch grid and the 3 by 3 window that gives 40, its cell on the 6 by 6 output map, the token shapes, the five boxes with corner coordinates and the 4 by 3 intersection of P3 and G2, and the cable mask counted as 8 and 56">
  <defs><marker id="aD2e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) pixels, patch grid, one 3×3 window · stride 1, pad 0</text>
  <rect x="102" y="50" width="72" height="144" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <line x1="30" y1="50" x2="174" y2="50" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="68" x2="174" y2="68" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="86" x2="174" y2="86" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="104" x2="174" y2="104" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="122" x2="174" y2="122" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="140" x2="174" y2="140" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="158" x2="174" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="176" x2="174" y2="176" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="194" x2="174" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="50" x2="30" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="48" y1="50" x2="48" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="66" y1="50" x2="66" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="84" y1="50" x2="84" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="102" y1="50" x2="102" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="120" y1="50" x2="120" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="138" y1="50" x2="138" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="156" y1="50" x2="156" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="174" y1="50" x2="174" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <rect x="30" y="50" width="144" height="144" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <line x1="102" y1="50" x2="102" y2="194" stroke="currentColor" stroke-width="2.4"/>
  <line x1="30" y1="122" x2="174" y2="122" stroke="currentColor" stroke-width="2.4"/>
  <text x="24" y="63" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">0</text>
  <text x="39" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">0</text>
  <text x="24" y="81" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">1</text>
  <text x="57" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <text x="24" y="99" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">2</text>
  <text x="75" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">2</text>
  <text x="24" y="117" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">3</text>
  <text x="93" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">3</text>
  <text x="24" y="135" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">4</text>
  <text x="111" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">4</text>
  <text x="24" y="153" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">5</text>
  <text x="129" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">5</text>
  <text x="24" y="171" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">6</text>
  <text x="147" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">6</text>
  <text x="24" y="189" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">7</text>
  <text x="165" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">7</text>
  <text x="66" y="117" font-size="11" fill="currentColor" text-anchor="middle">patch 1</text>
  <text x="138" y="117" font-size="11" fill="currentColor" text-anchor="middle">patch 2</text>
  <text x="66" y="189" font-size="11" fill="currentColor" text-anchor="middle">patch 3</text>
  <text x="138" y="189" font-size="11" fill="currentColor" text-anchor="middle">patch 4</text>
  <text x="12" y="225" font-size="11" fill="currentColor" fill-opacity="0.8">shaded = 10, blank = 0; the step lies on the patch line</text>
  <rect x="66" y="50" width="54" height="54" stroke="currentColor" stroke-width="2.6" fill="currentColor" fill-opacity="0.12"/>
  <line x1="232" y1="50" x2="340" y2="50" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="68" x2="340" y2="68" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="86" x2="340" y2="86" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="104" x2="340" y2="104" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="122" x2="340" y2="122" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="140" x2="340" y2="140" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="158" x2="340" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="50" x2="232" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="250" y1="50" x2="250" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="268" y1="50" x2="268" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="286" y1="50" x2="286" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="304" y1="50" x2="304" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="322" y1="50" x2="322" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="340" y1="50" x2="340" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <rect x="232" y="50" width="108" height="108" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <rect x="268" y="50" width="18" height="18" stroke="currentColor" stroke-width="2.6" fill="currentColor" fill-opacity="0.12"/>
  <text x="241" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1.0" font-weight="bold">40</text>
  <text x="295" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="63" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">0</text>
  <text x="241" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">0</text>
  <text x="241" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="81" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">1</text>
  <text x="259" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <text x="241" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="99" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">2</text>
  <text x="277" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">2</text>
  <text x="241" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="117" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">3</text>
  <text x="295" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">3</text>
  <text x="241" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="135" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">4</text>
  <text x="313" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">4</text>
  <text x="241" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="153" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">5</text>
  <text x="331" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">5</text>
  <text x="286" y="189" font-size="11" fill="currentColor" text-anchor="middle">output map 6 × 6 · y<tspan dy="3" font-size="10">0,2</tspan><tspan dy="-3" dx="3.5">= 40</tspan></text>
  <text x="286" y="205" font-size="11" fill="currentColor" text-anchor="middle">n<tspan dy="3" font-size="10">out</tspan><tspan dy="-3" dx="3.5">= ⌊(8 + 0 − 3)/1⌋ + 1 = 6</tspan></text>
  <path d="M 114 49 C 124 19, 277.0 15, 277.0 48" stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aD2e)"/>
  <text x="362" y="42" font-size="11" fill="currentColor">flatten: 4 × 16</text>
  <line x1="385" y1="52" x2="385" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="52" x2="392" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="52" x2="399" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="52" x2="406" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="52" x2="413" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="52" x2="420" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="52" x2="427" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="52" x2="434" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="52" x2="441" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="52" x2="448" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="52" x2="455" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="52" x2="462" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="52" x2="469" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="52" x2="476" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="52" x2="483" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="52" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="61" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">1</text>
  <rect x="378" y="66" width="112" height="9" stroke="none" fill="currentColor" fill-opacity="0.3"/>
  <line x1="385" y1="66" x2="385" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="66" x2="392" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="66" x2="399" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="66" x2="406" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="66" x2="413" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="66" x2="420" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="66" x2="427" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="66" x2="434" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="66" x2="441" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="66" x2="448" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="66" x2="455" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="66" x2="462" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="66" x2="469" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="66" x2="476" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="66" x2="483" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="66" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="75" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">2</text>
  <line x1="385" y1="80" x2="385" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="80" x2="392" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="80" x2="399" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="80" x2="406" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="80" x2="413" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="80" x2="420" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="80" x2="427" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="80" x2="434" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="80" x2="441" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="80" x2="448" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="80" x2="455" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="80" x2="462" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="80" x2="469" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="80" x2="476" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="80" x2="483" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="80" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="89" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">3</text>
  <rect x="378" y="94" width="112" height="9" stroke="none" fill="currentColor" fill-opacity="0.3"/>
  <line x1="385" y1="94" x2="385" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="94" x2="392" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="94" x2="399" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="94" x2="406" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="94" x2="413" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="94" x2="420" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="94" x2="427" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="94" x2="434" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="94" x2="441" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="94" x2="448" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="94" x2="455" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="94" x2="462" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="94" x2="469" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="94" x2="476" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="94" x2="483" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="94" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="103" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">4</text>
  <text x="498" y="61" font-size="11" fill="currentColor" fill-opacity="0.85">1 = 3</text>
  <text x="498" y="75" font-size="11" fill="currentColor" fill-opacity="0.85">2 = 4</text>
  <line x1="402" y1="110" x2="402" y2="128" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD2e)"/>
  <text x="411" y="123" font-size="11" fill="currentColor">× E (16 × d)</text>
  <text x="402" y="146" font-size="11" fill="currentColor" text-anchor="middle">4 × d</text>
  <line x1="402" y1="152" x2="402" y2="180" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD2e)"/>
  <text x="411" y="162" font-size="11" fill="currentColor">+ position p<tspan dy="3" font-size="10">i</tspan></text>
  <text x="411" y="180" font-size="11" fill="currentColor">+ class token</text>
  <text x="402" y="198" font-size="11" fill="currentColor" text-anchor="middle">5 × d</text>
  <text x="12" y="246" font-size="12" fill="currentColor">(b) boxes, corners in pixel coordinates</text>
  <line x1="30" y1="270" x2="182" y2="270" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="289" x2="182" y2="289" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="308" x2="182" y2="308" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="327" x2="182" y2="327" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="346" x2="182" y2="346" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="365" x2="182" y2="365" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="384" x2="182" y2="384" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="403" x2="182" y2="403" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="422" x2="182" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="270" x2="30" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="49" y1="270" x2="49" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="68" y1="270" x2="68" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="87" y1="270" x2="87" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="106" y1="270" x2="106" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="125" y1="270" x2="125" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="144" y1="270" x2="144" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="163" y1="270" x2="163" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="182" y1="270" x2="182" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <rect x="30" y="270" width="152" height="152" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.6"/>
  <text x="30" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">0</text>
  <text x="24" y="274" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">0</text>
  <text x="49" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <text x="24" y="293" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">1</text>
  <text x="68" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">2</text>
  <text x="24" y="312" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">2</text>
  <text x="87" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">3</text>
  <text x="24" y="331" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">3</text>
  <text x="106" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">4</text>
  <text x="24" y="350" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">4</text>
  <text x="125" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">5</text>
  <text x="24" y="369" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">5</text>
  <text x="144" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">6</text>
  <text x="24" y="388" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">6</text>
  <text x="163" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">7</text>
  <text x="24" y="407" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">7</text>
  <text x="182" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">8</text>
  <text x="24" y="426" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">8</text>
  <rect x="106" y="346" width="76" height="57" stroke="none" fill="currentColor" fill-opacity="0.28"/>
  <rect x="30" y="270" width="76" height="76" stroke="currentColor" stroke-width="2.2" fill="none"/>
  <rect x="106" y="346" width="76" height="76" stroke="currentColor" stroke-width="2.2" fill="none"/>
  <rect x="32.5" y="272.5" width="71" height="71" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="5 3"/>
  <rect x="87" y="327" width="76" height="76" stroke="currentColor" stroke-width="1.4" fill="none" stroke-opacity="0.7" stroke-dasharray="5 3"/>
  <rect x="106" y="327" width="76" height="76" stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="9 3 2 3"/>
  <circle cx="106" cy="346" r="2.8" stroke="none" fill="currentColor"/>
  <circle cx="182" cy="403" r="2.8" stroke="none" fill="currentColor"/>
  <text x="144" y="379.5" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">12</text>
  <text x="34.8" y="288.1" font-size="11" fill="currentColor">G<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, P</tspan><tspan dy="3" font-size="10">1</tspan></text>
  <text x="179.2" y="418.2" font-size="11" fill="currentColor" text-anchor="end">G<tspan dy="3" font-size="10">2</tspan></text>
  <text x="89.8" y="399.2" font-size="11" fill="currentColor" fill-opacity="0.85">P<tspan dy="3" font-size="10">2</tspan></text>
  <text x="180.5" y="340.7" font-size="11" fill="currentColor" text-anchor="end">P<tspan dy="3" font-size="10">3</tspan></text>
  <line x1="200" y1="270" x2="222" y2="270" stroke="currentColor" stroke-width="2.2"/>
  <text x="228" y="274" font-size="11" fill="currentColor">G<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= (0, 0, 4, 4)</tspan></text>
  <line x1="200" y1="289" x2="222" y2="289" stroke="currentColor" stroke-width="2.2"/>
  <text x="228" y="293" font-size="11" fill="currentColor">G<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= (4, 4, 8, 8)</tspan></text>
  <line x1="200" y1="308" x2="222" y2="308" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 3"/>
  <text x="228" y="312" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= (0, 0, 4, 4) · 0.90</tspan></text>
  <line x1="200" y1="327" x2="222" y2="327" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.7" stroke-dasharray="5 3"/>
  <text x="228" y="331" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= (3, 3, 7, 7) · 0.80</tspan></text>
  <line x1="200" y1="346" x2="222" y2="346" stroke="currentColor" stroke-width="1.8" stroke-dasharray="9 3 2 3"/>
  <text x="228" y="350" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">= (4, 3, 8, 7) · 0.60</tspan></text>
  <rect x="200" y="364" width="22" height="10" stroke="none" fill="currentColor" fill-opacity="0.28"/>
  <text x="228" y="373" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">∩ G</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">: x 4–8, y 4–7</tspan></text>
  <text x="228" y="390" font-size="11" fill="currentColor">4 × 3 = 12</text>
  <text x="200" y="411" font-size="11.5" fill="currentColor" font-weight="bold">IoU = 12 / (16 + 16 − 12) = 0.6</text>
  <text x="426" y="246" font-size="12" fill="currentColor">(c) mask, as counts</text>
  <rect x="488" y="270" width="13" height="104" stroke="none" fill="currentColor" fill-opacity="0.45"/>
  <line x1="436" y1="270" x2="540" y2="270" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="283" x2="540" y2="283" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="296" x2="540" y2="296" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="309" x2="540" y2="309" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="322" x2="540" y2="322" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="335" x2="540" y2="335" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="348" x2="540" y2="348" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="361" x2="540" y2="361" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="374" x2="540" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="270" x2="436" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="449" y1="270" x2="449" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="462" y1="270" x2="462" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="475" y1="270" x2="475" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="488" y1="270" x2="488" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="501" y1="270" x2="501" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="514" y1="270" x2="514" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="527" y1="270" x2="527" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="540" y1="270" x2="540" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <rect x="436" y="270" width="104" height="104" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <rect x="488" y="270" width="13" height="104" stroke="currentColor" stroke-width="1.8" fill="none"/>
  <text x="462" y="327" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">56</text>
  <text x="494.5" y="390" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">8</text>
  <text x="426" y="418" font-size="11" fill="currentColor">cable (column 4): 8</text>
  <text x="426" y="434" font-size="11" fill="currentColor">background: 56</text>
</svg>

D2 on its frozen numbers, with the embedding width left as $d$. (a) The step edge lies on the line of the $2\times2$ patch grid, so the four flattened tokens ($4\times16$) are only two distinct vectors until position is added; $E$ projects them to $4\times d$ and the class token makes $5\times d$, and the $3\times3$ window at rows 0–2, columns 2–4 gives $y_{0,2}=40$ on the $6\times6$ output map. (b) The five boxes by their corner coordinates, with the $4\times3$ intersection of $P_3$ and $G_2$ that gives $\mathrm{IoU}=12/20=0.6$, and (c) the cable mask as counts, 8 cable pixels against 56 background.

### Worked case

This is the homework object. Do the three things the problem set asks — one window, one output size, one overlap — here first, on the frozen numbers.

**One convolution response, by hand.** Take the vertical-edge kernel

$$K=\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}$$

and slide it with stride 1 and no padding. Deep-learning "convolution" is cross-correlation: the output at $(i,j)$ is $\sum_{u,v}K[u,v]\,I[i+u,j+v]$, with no kernel flip. At $(0,2)$ the window covers rows 0–2 and columns 2–4, which is $(0,0,10)$ in every row, so

$$y_{0,2}=(-1)(0)+(0)(0)+(1)(10)\;+\;(-2)(0)+(0)(0)+(2)(10)\;+\;(-1)(0)+(0)(0)+(1)(10)=40.$$

Because $I$ is constant down every column, the whole map collapses to $y_{i,j}=4\big(I[\cdot,j+2]-I[\cdot,j]\big)$, which is $40$ for $j\in\{2,3\}$ and $0$ otherwise. So a single step edge is reported **two columns wide** by a three-wide kernel: an edge detector of width $k$ smears a discontinuity over $k-1$ output positions, which is why edge maps look thick and why a "1-pixel localisation" claim needs a kernel width beside it.

**The output size, with every symbol.** The sliding window can start at $0,s,2s,\dots$ and its last start must leave $k$ columns, so the count of valid starts is

$$n_{\text{out}}=\left\lfloor\frac{n+2p-k}{s}\right\rfloor+1,$$

where $n$ is the input side length, $k$ the kernel side, $s$ the stride, $p$ the zero-padding added to **each** side, and the $+1$ counts the start at position 0. For D2 with $k=3$, $s=1$, $p=0$: $\lfloor(8+0-3)/1\rfloor+1=6$, matching the $6\times6$ map above. The floor is not decoration — at $k=3,s=2,p=0$ it gives $\lfloor5/2\rfloor+1=3$ windows, spanning columns 0–2, 2–4 and 4–6, and column 7 is never covered at all. Trailing pixels that no window covers are discarded silently, which is a real source of "my feature map is one off".

**One overlap, by hand.** $P_3=(4,3,8,7)$ against $G_2=(4,4,8,8)$. The intersection is $[\max(4,4),\min(8,8)]\times[\max(3,4),\min(7,8)]$, which is $4$ wide and $3$ tall, so $|A\cap B|=12$. Each box has area 16, so $|A\cup B|=16+16-12=20$ and

$$\mathrm{IoU}(P_3,G_2)=\frac{12}{20}=0.6.$$

One prediction, one truth, and the answer to "is this a detection?" is already threshold-dependent: $0.6\ge0.5$ makes it a true positive under the convention of the PASCAL VOC benchmark, which counts a hit at IoU $0.5$, and $0.6<0.75$ makes it a false positive under a stricter one. Nothing about the box changed. §5 turns that single fact into the gap between $\mathrm{AP}@0.5=0.833$ and $\mathrm{mAP}@[.5{:}.95]=0.600$, the COCO benchmark's average over the ten thresholds $0.50,0.55,\dots,0.95$; §2 defines both.

### 1. Two ways to impose visual structure

An image has more pixels than a network can afford one weight each, and a detector that works in one corner should work in the others. Every vision architecture answers this with an **inductive bias** — an assumption built into the model before it sees any data — and the two families differ in how much they build in: a convolution assumes that nearby pixels belong together and that a pattern means the same thing wherever it appears, while a Vision Transformer assumes almost nothing and learns it from data ([[01-canonical-papers/notes/1-foundations/vit|ViT note]]).

A convolution builds its assumptions in by **weight sharing**: one small filter, reused at every location. On D2 a $3\times3$ kernel at stride 1 without padding gives the Worked case's $6\times6$ map, and one input and four output channels need $4(3\cdot3+1)=40$ parameters including bias. That count, $C_{\text{out}}(C_{\text{in}}k^2+1)$, does not contain $n$: the same 40 numbers serve an $8\times8$ image and a $4000\times4000$ one, because the layer is a single filter *reused*, not one weight per pixel. A fully connected layer that produced the same $4\times6\times6=144$ outputs from D2's 64 pixels would need $144(64+1)=9{,}360$ parameters, and it would have to learn the same edge detector separately at each of the 36 positions. The discrete convolution itself, and why shift-invariance is what makes the reuse legitimate, is [[02-foundations/signal-processing|6. Signal Processing §1]].

A Vision Transformer takes the other road. It flattens each $4\times4$ patch into a **token**, a vector of 16 numbers, projects it with $E$, adds a position vector, and prepends a **class token** — one extra learned vector that belongs to no patch; attention lets it gather from every patch, and the classifier reads only its final state, which is why the picture's four tokens become $5\times d$. Attention then mixes the tokens with weights computed from their contents. Nothing ties a token to its neighbours, so patch attention can learn long-range interaction directly but has to learn locality from data, and it typically relies more heavily on data and pretraining than a convolution does.

D2 shows the cost of that trade in one line. Its four flattened patches are $(0,\dots,0)$, $(10,\dots,10)$, $(0,\dots,0)$, $(10,\dots,10)$, so tokens 1 and 3 are identical vectors and so are 2 and 4. Self-attention is **permutation-equivariant** — reorder its input tokens and its outputs are reordered the same way and changed in no other way — so without the added position vectors it sees the four tokens as a set: two dark, two bright. Flipping D2 top to bottom is not the test, because every column is constant and the flipped image is D2 itself. What attention without position cannot tell apart are the layouts built from the same four tokens — all six ways of placing two dark and two bright patches on the $2\times2$ grid, among them D2, its mirror image with the dark half on the right, and a checkerboard with dark patches at top-left and bottom-right — and the class token, which reads a weighted sum over the set, ends in the same state for all six. The position information is not a refinement; it is the only thing carrying layout. A convolution never faced this problem, because its output grid *is* the layout. [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer §5]] defines permutation equivariance and proves it in one line, and its lab in [[03-deep-learning/foundations/attention-transformer|1.2 §8]] runs the mirror test on D2: the mirrored image's outputs differ from a reordering of the original's by $1.217719$ with the position table and by exactly $0$ without.

### 2. The output defines the problem

*In one sentence:* a vision task is fixed by what the model outputs and how that output is scored, so a headline number means little until you know the metric's threshold, its matching rule and what it averages over.

*If you need only one thing from this section:* the threshold belongs to the metric, not to the method, which is why the Worked case's box turns the same three predictions into $0.833$ or $0.600$ (the mAP box below; §5 draws both).

| Task | Output | Typical metric | Metric caveat |
|---|---|---|---|
| classification | one label/distribution per image | top-1 accuracy | hides class imbalance |
| detection | boxes, labels, confidence | mAP over IoU thresholds | depends on matching and thresholds |
| segmentation | label/mask per pixel or object | IoU / mIoU | small classes can disappear in averages |
| monocular depth | depth per pixel | AbsRel, RMSE, $\delta$ | metric scale may be unknown |
| 3D reconstruction | camera/geometry/appearance | pose error, depth, rendering | photorealism is not geometric accuracy |

The architecture name does not define the claim. A backbone can feed several heads; inspect the output representation, loss, and evaluation protocol.

Every metric in the table is defined here — the depth metrics in §3 — or linked, because a row whose metric is only named cannot be checked. The general dictionary is [[02-foundations/ml-practice|9. ML Practice §3]]; what follows adds what a vision paper gets wrong about these metrics, on D2's own boxes and masks. **Top-1 accuracy** is the fraction of images whose highest-scoring class is the true one — it is the $k=1$ case of top-$k$ and needs no more than that here.

#### Overlap between two regions: IoU

> **Intersection over union, defined.** **IoU** is a *similarity score between two regions of the same image* — a dimensionless ratio of areas (or of pixel counts), not a distance, not an error, and not a probability. Three defining conditions. It is **symmetric**: $\mathrm{IoU}(A,B)=\mathrm{IoU}(B,A)$, so it says nothing about which region is the prediction. It is **normalised by the union**, not by either region, which is what stops a huge box from scoring well by swallowing the truth. And it is **scale-free**: multiply both regions' coordinates by 10 and the number is unchanged.
>
> $$\mathrm{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}$$
>
> where $|\cdot|$ is area for boxes and pixel count for masks, and the second form is the one to implement **because** it needs only the intersection, computed from $\max$ of the lower corners and $\min$ of the upper ones.
>
> - **Example**: D2's $P_3=(4,3,8,7)$ and $G_2=(4,4,8,8)$ intersect in a $4\times3$ rectangle, so $\mathrm{IoU}=12/(16+16-12)=0.6$.
> - **Non-example**: the overlap fraction $|A\cap B|/|B|$. A prediction covering the whole $8\times8$ image scores $1.0$ on that and $16/64=0.25$ on IoU. The union in the denominator is exactly the term that punishes a lazy large box, and a paper reporting "coverage" is not reporting IoU.
> - **Non-example**: a similarity that degrades gracefully. Two boxes that do not touch have $\mathrm{IoU}=0$ whether they are 1 pixel apart or 100, so IoU carries no gradient information outside contact — which is why detectors are trained on coordinate regression or on GIoU-style variants and *evaluated* on IoU.
> - **Why it matters**: every detection and segmentation number on this page is a count of IoU comparisons against a threshold, so the threshold is part of the metric and never part of the method — the point of this section's opening line, which §5 turns into a headline gap.

#### Ranking detections: AP and mAP

> **Average precision and mAP, defined.** **AP** is the *area under one class's precision–recall curve, at one IoU threshold* — a summary of a ranking, not of a single decision, which is why it needs confidences and not just boxes. Four defining conditions, and papers lose comparability by dropping any of them. Detections are **ranked by confidence** and matched **greedily to unmatched ground truth**, so a second box on an object already claimed is a false positive however good it is. A match counts only if its **IoU reaches the threshold $t$**. Recall is normalised by the **number of ground-truth objects**, so missed objects enter as recall that is never reached. And **mAP averages AP over classes** — and, in the COCO convention, over ten thresholds as well.
>
> $$\mathrm{AP}(t)=\sum_{n}\big(R_n-R_{n-1}\big)\,P^{\mathrm{interp}}_n,\qquad P^{\mathrm{interp}}_n=\max_{m\ge n}P_m,\qquad \mathrm{mAP}=\frac1C\sum_{c=1}^{C}\mathrm{AP}_c$$
>
> where $P_n$ and $R_n$ are precision and recall after the $n$-th ranked detection, $R_0=0$, $C$ is the number of classes, and the interpolation takes the best precision at this recall or higher **so that** the curve is monotone and a late lucky detection cannot be undone by an earlier false positive.
>
> - **Example**: D2's three predictions at $t=0.5$ rank TP, FP, TP, giving $P=(1,0.5,0.667)$ and $R=(0.5,0.5,1)$, so $\mathrm{AP}=0.5(1)+0.5(0.667)=0.833$ — the same shape as the worked ranking in [[02-foundations/ml-practice|9. ML Practice §3]], now on boxes whose coordinates are on this page.
> - **Non-example**: a VOC number compared with a COCO number. VOC mAP is $\mathrm{AP}(0.5)$; COCO mAP is the mean over $t=0.50,0.55,\dots,0.95$. On D2 those are $0.833$ and $0.600$ — a 23-point gap produced entirely by the convention, with no change to the detector.
> - **Why it matters**: mAP is the only number most detection papers report, and it hides three separate choices — the threshold set, the matching rule, and the class weighting. A method that improves mAP by improving localisation and one that improves it by improving ranking are different contributions with the same headline.

#### Averaging over classes: mIoU

> **Mean IoU, and what a segmentation metric averages over.** **mIoU** is the *mean, over classes, of the per-class IoU computed on pooled pixel counts* — and the averaging unit is the whole claim. Three defining conditions. The per-class IoU is computed from **pixel counts, $\mathrm{IoU}_c=TP_c/(TP_c+FP_c+FN_c)$**, so a class with more pixels contributes more evidence to *its own* score. The outer average is **over classes, uniformly**: each class gets weight $1/C$ whatever its pixel count, which is the deliberate opposite of pixel accuracy. And the pooling is **over the whole evaluation set before the ratio is taken**, so mIoU is not the average of per-image mIoUs, and a per-image average is a different and usually larger number.
>
> $$\mathrm{mIoU}=\frac1C\sum_{c=1}^{C}\frac{TP_c}{TP_c+FP_c+FN_c}\qquad\text{versus}\qquad \mathrm{acc}_{\text{pixel}}=\frac{\sum_c TP_c}{\text{total pixels}}$$
>
> where $TP_c$, $FP_c$, $FN_c$ are pixel counts for class $c$ and $C$ is the number of classes — and the two differ **because** the left expression takes the ratio inside the sum and the right one takes it outside, so only the left can let a class with 8 pixels matter as much as a class with 56.
>
> - **Example**: D2's cable is 8 pixels of 64. A model predicting background everywhere scores pixel accuracy $56/64=0.875$ and $\mathrm{mIoU}=(0.875+0)/2=0.4375$. §5 gives a second prediction with the *same* pixel accuracy and $\mathrm{mIoU}=0.679$.
> - **Non-example**: pixel accuracy. On any image with a dominant background it is close to the background fraction and nearly independent of the model, which is why segmentation benchmarks abandoned it.
> - **Non-example**: "IoU" quoted for a whole dataset with no class index. That is either mIoU with $C$ unstated or the IoU of one binary foreground, and when a rare class fails the first drops by that class's share while the second barely moves.
> - **Why it matters**: the uniform class weight is protection, not a guarantee. On a 20-class benchmark, 19 classes at $0.80$ and the cable at $0.00$ gives $\mathrm{mIoU}=19\cdot0.80/20=0.76$ — four points below a clean run, comfortably inside normal variation, for a class the robot is about to drive into. mIoU protects a rare class against a *large* background; it does not protect it against 19 other classes.

### 3. Geometry survives learning

A learned output helps a robot only once it is in the robot's frame and units, and a score computed in pixels, or after an alignment, carries no claim about metres. Cropping, resizing, and augmentation change camera coordinates. A depth network may predict relative depth while a robot needs metres. A segmentation model can have excellent mIoU and still miss a thin cable that determines safety: on §2's 20-class arithmetic that is mIoU $0.76$ against $0.80$, a difference no reviewer would call a failure. For robotics, record frame, units, latency, confidence, and how the prediction enters a closed loop.

#### Depth: three errors that disagree by design

The depth row of §2's table is scored by three metrics. For predicted depths $\hat d_i$ against ground truth $d_i$ over $N$ valid pixels,

$$\mathrm{AbsRel}=\frac1N\sum_i\frac{|\hat d_i-d_i|}{d_i},\qquad \mathrm{RMSE}=\sqrt{\frac1N\sum_i(\hat d_i-d_i)^2},\qquad \delta_1=\frac1N\Big|\Big\{i:\max\big(\tfrac{\hat d_i}{d_i},\tfrac{d_i}{\hat d_i}\big)<1.25\Big\}\Big|,$$

so AbsRel is dimensionless and weights near pixels most, RMSE is in metres and is dominated by far ones, and $\delta_1$ is a *threshold accuracy* — the fraction of pixels within a factor of $1.25$ either way. Two pixels with $d=(2,4)$ m and $\hat d=(2.5,3.6)$ m give $\mathrm{AbsRel}=0.175$, $\mathrm{RMSE}=0.452769$ m, and $\delta_1=0.5$, the first pixel failing at a ratio of exactly $1.25$ because the inequality is strict. The three disagree by construction, which is why depth papers report all of them.

All three are computed *after* an alignment step whenever the method is scale-ambiguous — when its output fixes depth only up to an unknown scale, and often an unknown shift, as a network that predicts inverse depth $r=s/Z+t$ with an unknown scale $s$ and shift $t$ does (3.5 §6's letters; elsewhere on this page $s$ is the stride and $t$ the IoU threshold). Such a method is evaluated after fitting a per-image scale (and often the shift) to the ground truth, so its AbsRel measures *shape* agreement and carries no claim about metres at all. Ask which alignment was applied before comparing a depth number with a robot's requirement. On a robot the scale has to come from something real: [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §6]] works the three places it can enter on one rig — calibrated stereo, a known length, and alignment to anchor pixels of known depth — and [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §3–§4]] covers the sensors that measure metres directly, stereo and time-of-flight, with their error bars. The geometry that defines metres in the first place is [[04-robotics/geometric-perception-calibration|3.5 §1]].

#### From an IoU threshold to millimetres

A detection threshold is a tolerance, but a relative one. Two boxes of the same height and the same width $w$, one shifted sideways by $d$ against the other — a shift in the units of $w$, not the depth $d_i$ above — overlap in a strip $w-d$ wide and cover $w+d$ together, and the height cancels, so

$$\mathrm{IoU}=\frac{w-d}{w+d}\ge t\quad\Longleftrightarrow\quad d\le w\,\frac{1-t}{1+t}.$$

At PASCAL's $t=0.5$ that is $d\le w/3$: a box may slide a third of its own width and still count as a hit. Take 3.5's camera, $f=600$ px, looking at a panel $2$ m away, where one pixel spans $2000/600=3.33$ mm. A box $100$ px wide there may slide $33.3$ px, which is $111$ mm, and still be a true positive. S1, the construction track's facade-panel task ([[05-construction-robotics/site-engineering|2.5]]), aligns two holes to $\pm5$ mm, which at this range is $1.5$ px and would need $\mathrm{IoU}\ge(100-1.5)/(100+1.5)=0.970$, above every rung of the COCO ladder. IoU is scale-free by definition (§2's box), so no IoU threshold can certify a tolerance in millimetres; that takes 3.5's geometry and an error measured in the robot's frame.

### 4. Reading the canonical line

A backbone's name says little about why a result holds, so read the canonical line for what supervision and pretraining each paper used and what transferred, not merely for which backbone is newer. Read [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] and [[01-canonical-papers/notes/1-foundations/resnet|ResNet]] for learned hierarchies and optimization, [[01-canonical-papers/notes/1-foundations/vit|ViT]] for patch tokens, then the detection/segmentation/3D entries in the [[01-canonical-papers/canonical-list|canonical list]].

### 5. The lab: the formula, the threshold, and the average

Three sweeps on the same frozen D2, each one a knob the paper's method never touches. Part 1 checks the output-size formula against an actual sliding window at nine settings. Part 2 sweeps the IoU threshold through the COCO ladder. Part 3 scores two segmentations that a pixel-accuracy report cannot distinguish.

```python
# D2: convolution arithmetic, IoU/AP, and segmentation averaging. NumPy only.
import numpy as np

I = np.zeros((8, 8)); I[:, 4:] = 10.0                  # D2: vertical step edge at column 4
Kx = np.array(((-1., 0., 1.), (-2., 0., 2.), (-1., 0., 1.)))     # 3x3 vertical-edge kernel

def conv2d(img, ker, s=1, p=0):
    if p: img = np.pad(img, p)                          # zero padding
    k, n = ker.shape[0], img.shape[0]
    m = (n - k)//s + 1
    cell = lambda i, j: (img[i*s:i*s+k, j*s:j*s+k]*ker).sum()
    return np.array([ [cell(i, j) for j in range(m)] for i in range(m) ])

print("one window at output (0,2):\n", I[0:3, 2:5], "-> ", (I[0:3, 2:5]*Kx).sum())
Y = conv2d(I, Kx); print("valid output", Y.shape, "\n", Y)

Kx5 = np.zeros((5, 5)); Kx5[:, 0] = -1; Kx5[:, 1] = -2; Kx5[:, 3] = 2; Kx5[:, 4] = 1
print("\n k  s  p | formula | numpy | max    | min    | nonzero")
for k, s, p in ((3,1,0),(3,1,1),(3,2,0),(3,2,1),(3,3,0),(3,3,1),(3,4,0),(5,1,0),(5,1,2)):
    Y = conv2d(I, Kx if k == 3 else Kx5, s, p)
    print(" %d  %d  %d |    %d    |   %d   | %6.1f | %6.1f |   %d"
          % (k, s, p, (8 + 2*p - k)//s + 1, Y.shape[0], Y.max(), Y.min(), int((np.abs(Y) > 1e-9).sum())))

def iou(a, b):
    w = max(0, min(a[2], b[2]) - max(a[0], b[0])); h = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = w*h
    return inter / ((a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter)

G = ((0, 0, 4, 4), (4, 4, 8, 8))                        # ground truth
P = (((0, 0, 4, 4), 0.90), ((3, 3, 7, 7), 0.80), ((4, 3, 8, 7), 0.60))   # box, confidence

print("\nIoU matrix (rows = predictions, cols = ground truth)")
print(np.round(np.array([ [iou(b, g) for g in G] for b, _ in P ]), 6))

def AP(t):
    used, tp = set(), []
    for b, _ in sorted(P, key=lambda z: -z[1]):         # highest confidence first
        best, arg = -1.0, None
        for gi, g in enumerate(G):
            if gi not in used and iou(b, g) > best: best, arg = iou(b, g), gi
        if best >= t: used.add(arg); tp.append(1)
        else: tp.append(0)
    ctp = np.cumsum(tp); prec = ctp/np.arange(1, len(tp)+1); rec = ctp/len(G)
    a, prev = 0.0, 0.0
    for i in range(len(prec)):
        if rec[i] > prev: a += (rec[i]-prev)*max(prec[i:]); prev = rec[i]
    return a, tp, np.round(prec, 4), np.round(rec, 4)

for t in (0.5, 0.75):
    a, tp, pr, rc = AP(t); print("t=%.2f  TP flags %s  precision %s  recall %s  AP=%.6f" % (t, tp, pr, rc, a))
ts = [round(0.5 + 0.05*i, 2) for i in range(10)]
aps = [AP(t)[0] for t in ts]
print("COCO sweep", [round(a, 4) for a in aps], " mAP[.5:.95] =", round(float(np.mean(aps)), 6))

gt = np.zeros((8, 8), int); gt[:, 4] = 1                # the cable: one column, 8 of 64 pixels
predA = np.zeros((8, 8), int)                           # predicts background everywhere
predB = np.zeros((8, 8), int); predB[:, 4:6] = 1        # cable, two columns wide
def scores(pred):
    per = [((gt == c) & (pred == c)).sum() / ((gt == c) | (pred == c)).sum() for c in (0, 1)]
    return per, float(np.mean(per)), float((gt == pred).mean())
for name, pr in (("A (all background)", predA), ("B (cable 2 cols)", predB)):
    per, m, acc = scores(pr)
    print("%-19s IoU bg %.6f  IoU cable %.6f  mIoU %.6f  pixel acc %.6f" % (name, per[0], per[1], m, acc))
print("a 20-class benchmark with 19 classes at 0.80 and the cable at 0.00: mIoU =", 19*0.80/20)
```

**Sweep 1 — the formula against the window.** "Nonzero" counts output cells that saw the edge; the map is $n_{\text{out}}\times n_{\text{out}}$.

| $k$ | $s$ | $p$ | formula | NumPy | max | min | nonzero cells |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 0 | 6 | 6 | $40$ | $0$ | 12 |
| 3 | 1 | 1 | 8 | 8 | $40$ | $-40$ | 24 |
| 3 | 2 | 0 | 3 | 3 | $40$ | $0$ | 3 |
| 3 | 2 | 1 | 4 | 4 | $40$ | $0$ | 4 |
| 3 | 3 | 0 | 2 | 2 | $40$ | $0$ | 2 |
| 3 | 3 | 1 | 3 | 3 | $40$ | $0$ | 3 |
| 3 | 4 | 0 | 2 | 2 | $0$ | $0$ | 0 |
| 5 | 1 | 0 | 4 | 4 | $150$ | $50$ | 16 |
| 5 | 1 | 2 | 8 | 8 | $150$ | $-150$ | 48 |

**Sweep 2 — the IoU threshold.** $\mathrm{AP}(0.5)=0.833333$ with TP/FP flags $(1,0,1)$; $\mathrm{AP}(0.75)=0.500000$ with flags $(1,0,0)$. Across the COCO ladder $t=0.50,0.55,\dots,0.95$ the AP values are $0.8333$ three times and then $0.5$ seven times, so $\mathrm{mAP}@[.5{:}.95]=(3\cdot0.8333+7\cdot0.5)/10=0.600000$. COCO's own evaluator reads the interpolated curve at 101 evenly spaced recall levels instead of integrating it, which turns the two values into $0.834983$ and $0.504950$ and the mean into $0.603960$ — a second convention hiding inside the first, with the same 23-point gap.

<svg viewBox="0 0 560 360" style="max-width:100%;height:auto" role="img" aria-label="Precision-recall curves of D2's three ranked boxes. (a) At IoU threshold 0.5 the flags are TP, FP, TP; points (R, P) = (0.5, 1), (0.5, 0.5), (1, 0.667); the interpolated envelope encloses AP = 0.833. (b) At 0.75 the third box fails, recall stops at 0.5 and AP = 0.5. (c) AP along the COCO ladder t = 0.50 to 0.95: 0.833 three times, then 0.5 seven times, mean 0.600.">
  <text x="12" y="18" font-size="12" fill="currentColor">(a) threshold t = 0.5</text>
  <path d="M 52.0 194.0 L 52.0 44.0 L 152.0 44.0 L 152.0 94.0 L 252.0 94.0 L 252.0 194.0 L 252.0 194.0 Z" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <polyline points="52.0,44.0 152.0,44.0 152.0,94.0 252.0,94.0 252.0,194.0" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="52" y1="194" x2="258" y2="194" stroke="currentColor" stroke-width="1"/>
  <line x1="52" y1="194" x2="52" y2="38" stroke="currentColor" stroke-width="1"/>
  <line x1="52.0" y1="194" x2="52.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="52.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="48" y1="194.0" x2="52" y2="194.0" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="197.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="152.0" y1="194" x2="152.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="152.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <line x1="48" y1="119.0" x2="52" y2="119.0" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="122.5" font-size="10" fill="currentColor" text-anchor="end">0.5</text>
  <line x1="252.0" y1="194" x2="252.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="252.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="48" y1="44.0" x2="52" y2="44.0" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="47.5" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <text x="258" y="209" font-size="10.5" fill="currentColor" text-anchor="end">recall R</text>
  <text x="57" y="36" font-size="10.5" fill="currentColor">precision P</text>
  <circle cx="152.0" cy="44.0" r="3.2" fill="currentColor"/>
  <circle cx="152.0" cy="119.0" r="3.2" fill="currentColor"/>
  <circle cx="252.0" cy="94.0" r="3.2" fill="currentColor"/>
  <text x="159.0" y="55.0" font-size="10.5" fill="currentColor">1 · P<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3">TP</tspan></text>
  <text x="159.0" y="123.0" font-size="10.5" fill="currentColor">2 · P<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3">FP</tspan></text>
  <text x="246.0" y="87.0" font-size="10.5" fill="currentColor" text-anchor="end">3 · P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3">TP</tspan></text>
  <text x="152.0" y="173.0" font-size="10.5" fill="currentColor" text-anchor="middle">AP = 0.5·1 + 0.5·0.667 = 0.833</text>
  <text x="282" y="18" font-size="12" fill="currentColor">(b) threshold t = 0.75</text>
  <path d="M 322.0 194.0 L 322.0 44.0 L 422.0 44.0 L 422.0 194.0 L 422.0 194.0 Z" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <polyline points="322.0,44.0 422.0,44.0 422.0,194.0" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="322" y1="194" x2="528" y2="194" stroke="currentColor" stroke-width="1"/>
  <line x1="322" y1="194" x2="322" y2="38" stroke="currentColor" stroke-width="1"/>
  <line x1="322.0" y1="194" x2="322.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="322.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="318" y1="194.0" x2="322" y2="194.0" stroke="currentColor" stroke-width="1"/>
  <text x="315" y="197.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="422.0" y1="194" x2="422.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="422.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <line x1="318" y1="119.0" x2="322" y2="119.0" stroke="currentColor" stroke-width="1"/>
  <text x="315" y="122.5" font-size="10" fill="currentColor" text-anchor="end">0.5</text>
  <line x1="522.0" y1="194" x2="522.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="522.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="318" y1="44.0" x2="322" y2="44.0" stroke="currentColor" stroke-width="1"/>
  <text x="315" y="47.5" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <text x="528" y="209" font-size="10.5" fill="currentColor" text-anchor="end">recall R</text>
  <text x="327" y="36" font-size="10.5" fill="currentColor">precision P</text>
  <circle cx="422.0" cy="44.0" r="3.2" fill="currentColor"/>
  <circle cx="422.0" cy="119.0" r="3.2" fill="currentColor"/>
  <circle cx="422.0" cy="144.0" r="3.2" fill="currentColor"/>
  <text x="429.0" y="55.0" font-size="10.5" fill="currentColor">1 · P<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3">TP</tspan></text>
  <text x="429.0" y="123.0" font-size="10.5" fill="currentColor">2 · P<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3">FP</tspan></text>
  <text x="429.0" y="148.0" font-size="10.5" fill="currentColor">3 · P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3">FP</tspan></text>
  <text x="429.0" y="161.0" font-size="10.5" fill="currentColor">IoU 0.6 &lt; 0.75</text>
  <text x="372.0" y="173.0" font-size="10.5" fill="currentColor" text-anchor="middle">AP = 0.5·1 = 0.5</text>
  <text x="429.0" y="175.0" font-size="10.5" fill="currentColor">recall stops at 0.5</text>
  <text x="12" y="226" font-size="10.5" fill="currentColor" fill-opacity="0.85">dots: P and R after each ranked box · solid: the interpolated envelope · shaded: its area, the AP</text>
  <text x="12" y="252" font-size="12" fill="currentColor">(c) AP(t) along the COCO ladder, and their mean</text>
  <rect x="61.0" y="280.3" width="30" height="41.7" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="76.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.833</text>
  <text x="76.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.50</text>
  <rect x="109.0" y="280.3" width="30" height="41.7" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="124.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.833</text>
  <text x="124.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.55</text>
  <rect x="157.0" y="280.3" width="30" height="41.7" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="172.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.833</text>
  <text x="172.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.60</text>
  <rect x="205.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="220.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="220.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.65</text>
  <rect x="253.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="268.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="268.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.70</text>
  <rect x="301.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="316.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="316.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.75</text>
  <rect x="349.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="364.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="364.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.80</text>
  <rect x="397.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="412.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="412.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.85</text>
  <rect x="445.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="460.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="460.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.90</text>
  <rect x="493.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="508.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="508.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.95</text>
  <line x1="52" y1="322" x2="532" y2="322" stroke="currentColor" stroke-width="1"/>
  <line x1="52" y1="292.0" x2="532" y2="292.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3"/>
  <text x="532" y="288.0" font-size="10.5" fill="currentColor" text-anchor="end">mean 0.600</text>
  <line x1="196" y1="264" x2="196" y2="322" stroke="currentColor" stroke-width="1" stroke-dasharray="1 2"/>
  <text x="200" y="270" font-size="10.5" fill="currentColor">the step sits at P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3">'s IoU, 0.6</tspan></text>
  <text x="292" y="352" font-size="10.5" fill="currentColor" text-anchor="middle">IoU threshold t</text>
</svg>

D2's three predictions ranked by confidence, $P_1$ ($0.90$), $P_2$ ($0.80$), $P_3$ ($0.60$), as precision–recall points. (a) At $t=0.5$ the flags are TP, FP, TP and the interpolated envelope encloses $\mathrm{AP}=0.5\cdot1+0.5\cdot0.667=0.833$; (b) at $t=0.75$ the $0.6$ overlap of $P_3$ fails, recall stops at $0.5$, and $\mathrm{AP}=0.5$. (c) Along the COCO ladder AP is $0.833$ up to $t=0.60$ and $0.5$ from $0.65$ on — the step sits at $P_3$'s IoU of $0.6$ — so the mean is $0.600$.

**Sweep 3 — the averaging unit.**

| prediction | IoU background | IoU cable | mIoU | pixel accuracy |
|---|---:|---:|---:|---:|
| A: background everywhere | $0.875000$ | $0.000000$ | $0.437500$ | $0.875000$ |
| B: cable two columns wide | $0.857143$ | $0.500000$ | $0.678571$ | $0.875000$ |

**Reading the sweeps.** Five things the formula alone could not have told you.

- **The formula is exact, and the floor is where the pixels go missing.** All nine rows match NumPy. The interesting ones are $(k,s,p)=(3,2,0)$ and $(3,3,0)$, where $\lfloor5/2\rfloor+1=3$ and $\lfloor5/3\rfloor+1=2$: the last one and two image columns are never covered by any window. No error is raised; the feature map is simply smaller than an off-by-one mental model expects.
- **A stride wider than the kernel can miss the whole signal.** At $(3,4,0)$ the output is a legal $2\times2$ map of exact zeros. The two windows start at columns 0 and 4, and each sees a *constant* patch — column 0–2 all dark, column 4–6 all bright — so neither straddles the edge. The image has one feature and the layer reports nothing. Any stride $s>k$ leaves gaps, and D2's edge falls in one.
- **Zero padding manufactures an edge.** At $(3,1,1)$ the minimum is $-40$: the right-hand column of the padded map compares bright pixels against the zeros that were invented outside the image, producing an edge response as strong as the real one. In the top and bottom rows the three nonzero columns — the real edge's 3 and 4 and the invented one at 7 — read $30$ and $-30$ instead of $\pm40$, because the zero row padded above or below removes one of the three contributing rows. A border artifact is not a bug in the padding, it is what "same" padding costs.
- **The threshold, not the detector, moves the headline.** $P_3$ never changes: it always overlaps $G_2$ by $0.6$. Reporting $\mathrm{AP}@0.5=0.833$ and reporting $\mathrm{mAP}@[.5{:}.95]=0.600$ describe the same three boxes, and the 23-point gap is the localisation quality of one box seen through two conventions. $P_2$ is a false positive at every threshold in the ladder, because $0.391$ never reaches $0.5$ — a detection can be visually "nearly right" and score zero.
- **Pixel accuracy cannot see the cable; mIoU can.** Predictions A and B have *identical* pixel accuracy, $0.875$, and mIoU of $0.4375$ against $0.678571$. B is a real improvement — it finds the cable and over-segments it by one column — and only the class-averaged metric records it. The background IoU actually *falls* from $0.875$ to $0.857143$ when B is right about the cable, which is the honest cost of the trade and the reason the two numbers must be reported per class.

### Self-check

1. Give the output size and parameter count of a $3\times3$, stride-1, padding-1 convolution with 1 input and 4 output channels on D2. Which of the two numbers depends on the image size?
2. D2's four patch tokens contain only two distinct vectors. What breaks if the position embedding is omitted, and why does a convolution not have this problem?
3. A detector's box overlaps the truth with $\mathrm{IoU}=0.6$. Is it a true positive?
4. Two segmentations have the same pixel accuracy but mIoU $0.44$ and $0.68$. What must be true about the class the second one found?
5. A depth paper reports $\mathrm{AbsRel}=0.10$ and does not mention alignment. What has not been established?

> [!tip]- Answers
> 1. $\lfloor(8+2-3)/1\rfloor+1=8$, so $8\times8\times4$; parameters $4(1\cdot9+1)=40$. Only the output size depends on $n$ — the parameter count is $C_{\text{out}}(C_{\text{in}}k^2+1)$ and contains no $n$, which is the whole point of weight sharing.
> 2. Self-attention is permutation-equivariant, so identical tokens at different places are indistinguishable and the model cannot tell top-left from bottom-left, nor D2 from its mirror image. A convolution's output grid is itself the layout, so position never has to be added.
> 3. Unanswerable as asked: true positive at $t=0.5$, false positive at $t=0.75$, and the threshold belongs to the protocol, not the detector. It is also only a TP if that ground-truth object was not already claimed by a higher-confidence detection.
> 4. It is a class small enough that getting it wrong costs almost no pixels — D2's cable is 8 of 64. mIoU's uniform per-class weight is what makes the improvement visible; pixel accuracy weights by pixel count and cannot see it.
> 5. Whether the number refers to metric depth at all. A scale-ambiguous method is aligned to ground truth per image before AbsRel is computed, so the result measures relative shape; metres, and therefore any manipulation or navigation claim, are unsupported.

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and [[03-deep-learning/lab-objects|0. Lab Objects]]. D2's pixels, boxes, and masks are frozen in the Running object; questions 1 and 3 move the window, the box pair and the range, and question 4 changes the kernel, one box, and one mask, so none of the page's numbers can be copied.

1. **Draw.** The picture's three panels for a second window, box pair and mask: (a) D2 with the $3\times3$ window whose output cell is $(0,4)$, its value, and that cell on the $6\times6$ map; (b) $P_2$ and $G_2$ by their corners, with their intersection rectangle, its area and their IoU; (c) prediction B of §5, the cable two columns wide, as counts — the intersection and the union of each class.
2. **Derive.** Compute output size and parameter count for a $3\times3$, stride-2, padding-1 convolution with 1 input and 8 output channels on D2.
3. **Interpret.** 3.5's camera ($f=600$ px) looks at S1's two mounting holes, $400$ mm apart, from $1.2$ m, and a detector puts a box around the pair. (a) How wide is that box in pixels, and how far sideways can it slide and still be a hit at $t=0.5$, in pixels and in millimetres? (b) The same at COCO's strictest rung, $t=0.95$. (c) What IoU would S1's $\pm5$ mm require, and why does that number not depend on the range?
4. **Do.** Fill the `?` blanks, then run three variants and report each as a small table. (a1) Sweep the $5\times5$ vertical-edge kernel `K5` over $(k,s,p)=(5,1,0)$, $(5,1,2)$, $(5,2,0)$, $(5,2,2)$, $(5,3,0)$, checking the formula each time. (a2) Replace $K$ by its transpose, the *horizontal*-edge kernel `Ky`, run it at $3\times3$ with $p=0$ and with $p=1$, print the top and bottom rows of the padded map, and say in one sentence where its responses come from. (b) Move $P_3$ to $(4,4,8,8)$, an exact hit, and recompute $\mathrm{AP}(0.5)$, $\mathrm{AP}(0.75)$, and $\mathrm{mAP}@[.5{:}.95]$. (c) Score a third segmentation that puts the cable at column 3 instead of column 4, and say why its cable IoU is what it is.

```python
# D2 variants. Reuse conv2d, iou and AP from section 5. Fill ?.
import numpy as np
I = np.zeros((8, 8)); I[:, 4:] = 10.0
Kx = np.array(((-1., 0., 1.), (-2., 0., 2.), (-1., 0., 1.)))
Ky = ?                                   # the horizontal-edge kernel: transpose of Kx

K5 = np.zeros((5, 5)); K5[:, 0] = -1; K5[:, 1] = -2; K5[:, 3] = 2; K5[:, 4] = 1
for k, s, p in ((5,1,0), (5,1,2), (5,2,0), (5,2,2), (5,3,0)):
    n_out = ?                            # the formula, from n=8, k, s, p
    Y = conv2d(I, K5, s, p)
    print(k, s, p, n_out, Y.shape[0], Y.max(), Y.min())
print("horizontal kernel, p=0: max", conv2d(I, Ky).max(), " min", conv2d(I, Ky).min())
Yp = conv2d(I, Ky, 1, ?)                 # the same kernel with one ring of zero padding
print("p=1:", Yp.shape, "\n top row", Yp[0], "\n bottom row", Yp[-1])

G = ((0, 0, 4, 4), (4, 4, 8, 8))
P = (((0, 0, 4, 4), 0.90), ((3, 3, 7, 7), 0.80), (?, 0.60))     # P3 becomes an exact hit
print("AP(0.5) =", AP(0.5)[0], "  AP(0.75) =", AP(0.75)[0])
print("mAP =", np.mean([AP(round(0.5 + 0.05*i, 2))[0] for i in range(10)]))

gt = np.zeros((8, 8), int); gt[:, 4] = 1
predC = np.zeros((8, 8), int); predC[:, ?] = 1                  # cable predicted one column early
per = [((gt == c) & (predC == c)).sum() / ((gt == c) | (predC == c)).sum() for c in (0, 1)]
print("IoU bg %.6f  IoU cable %.6f  mIoU %.6f  pixel acc %.6f"
      % (per[0], per[1], np.mean(per), (gt == predC).mean()))
```

> [!note]- How to draw it · 그리는 법
> - Draw the patch grid on the pixels, not beside them, with the step edge on the vertical grid line: it is what puts the window at $(0,4)$ on a constant patch.
> - Draw the convolution window as one $3\times3$ square on the pixels and mark its output cell on a separate $n_{\text{out}}\times n_{\text{out}}$ grid: one square, one cell, one arrow. Write the window's pixel values beside it, so that its output can be checked.
> - Draw boxes as corners with coordinates, not as sketched rectangles. IoU is computed from $\max$ and $\min$ of coordinates, and a rectangle whose corners are not written down cannot be checked.
> - Mark the intersection rectangle explicitly, with its area — it is the only part of the picture the union needs.
> - Draw the mask panel as counts, not as shading: for each class, its intersection and its union. Every segmentation metric here is a ratio of two integers, and §5's metrics disagree for a reason visible only when those integers are on the page.

> [!tip]- Solutions
> 1. (a) The window covers rows 0–2 and columns 4–6, all bright, so every row reads $(10,10,10)$ and $y_{0,4}=(-1+0+1)\cdot10+(-2+0+2)\cdot10+(-1+0+1)\cdot10=0$: a kernel whose entries sum to zero returns $0$ on any constant patch, bright or dark. (b) $P_2=(3,3,7,7)$ and $G_2=(4,4,8,8)$ meet in $x\in[4,7]$, $y\in[4,7]$, a $3\times3$ square of area $9$, so $\mathrm{IoU}=9/(16+16-9)=9/23=0.391304$ — §5's false positive at every threshold. (c) Cable: intersection $8$, union $16$, IoU $0.5$; background: intersection $48$, union $56$, IoU $0.857143$; their mean is B's mIoU, $0.678571$.
> 2. $\lfloor(8+2-3)/2\rfloor+1=4$, so $4\times4\times8$ output; parameters $8(3\cdot3+1)=80$.
> 3. (a) One pixel spans $1200/600=2$ mm there, so the box is $400/2=200$ px wide and $d\le w/3=66.7$ px, which is $133$ mm. (b) $d\le w(1-t)/(1+t)=200\cdot0.05/1.95=5.13$ px, $10.3$ mm — still twice S1's tolerance at the ladder's strictest rung. (c) $5$ mm is $2.5$ px, so $\mathrm{IoU}\ge(200-2.5)/(200+2.5)=0.975$. Written in millimetres the pixels cancel, $\mathrm{IoU}\ge(W-\delta)/(W+\delta)$ with $W=400$ mm and $\delta=5$ mm, because IoU is scale-free; the range changes only how many pixels the $5$ mm is — $2.5$ px here, $1.5$ px at §3's $2$ m — which is what the detector would have to resolve. A benchmark IoU cannot certify S1's alignment; an error in millimetres, measured through 3.5's geometry, is what can.
> 4. Blanks: `Ky = Kx.T`, `n_out = (8 + 2*p - k)//s + 1`, `1` for the padding of `Yp`, `(4, 4, 8, 8)`, and `predC[:, 3] = 1`.
>
>    (a1) The formula matches NumPy at every setting, and a $5\times5$ kernel smears the single edge over four columns:
>
>    | $k$ | $s$ | $p$ | formula = NumPy | max | min |
>    |---:|---:|---:|---:|---:|---:|
>    | 5 | 1 | 0 | 4 | $150$ | $50$ |
>    | 5 | 1 | 2 | 8 | $150$ | $-150$ |
>    | 5 | 2 | 0 | 2 | $150$ | $50$ |
>    | 5 | 2 | 2 | 4 | $150$ | $-50$ |
>    | 5 | 3 | 0 | 2 | $50$ | $50$ |
>
>    The unpadded rows never reach zero — every valid 5-wide window straddles the edge, so the wider kernel has no "quiet" position on an $8$-wide image.
>
>    (a2) At $p=0$ `Ky` returns max $0$ and min $0$ everywhere: D2 is constant down every column, so a detector of change from one row to the next sees nothing, and a feature map of zeros is evidence about the image, not about the layer. At $p=1$ the map is $8\times8$ with top row $(0,0,0,10,30,40,40,30)$, bottom row its negative, and zeros between: the zero row padded above row 0 and below row 7 is a horizontal edge the image does not have, strongest under the bright columns. Padding manufactures an edge — §5's third reading, turned on its side.
>
>    (b) With $P_3=(4,4,8,8)$ its IoU with $G_2$ is $1.0$, so the flags are $(1,0,1)$ at every threshold in the ladder: $\mathrm{AP}(0.5)=\mathrm{AP}(0.75)=\mathrm{mAP}@[.5{:}.95]=0.833333$. The COCO gap of §5 vanishes entirely, which identifies it as a localisation gap and not a ranking one — the false positive $P_2$ is still there and still costs the same precision.
>
>    (c) Cable at column 3: $\mathrm{IoU}_{\text{cable}}=0/(8+8)=0$, $\mathrm{IoU}_{\text{bg}}=48/64=0.750000$, $\mathrm{mIoU}=0.375000$, pixel accuracy $0.750000$. A one-column shift on a one-column-wide object has *no* intersection, so IoU gives no partial credit at all — it drops from $0.5$ (prediction B, which at least overlapped) to $0$, and scores worse than predicting nothing. For thin structures IoU is nearly binary, which is why safety-critical thin-object evaluation uses distance-based or dilated criteria instead.

### Sources

- A. Krizhevsky, I. Sutskever & G. E. Hinton, "ImageNet classification with deep convolutional neural networks," *NeurIPS* 2012 ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet note]]).
- K. He, X. Zhang, S. Ren & J. Sun, "Deep residual learning for image recognition," *CVPR* 2016 ([[01-canonical-papers/notes/1-foundations/resnet|ResNet note]]).
- A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition at scale," *ICLR* 2021 — patch tokens, the class token and the inductive-bias argument of §1 ([[01-canonical-papers/notes/1-foundations/vit|ViT note]]).
- M. Everingham, L. Van Gool, C. K. I. Williams, J. Winn & A. Zisserman, "The PASCAL Visual Object Classes (VOC) challenge," *International Journal of Computer Vision* 88(2):303–338 (2010) — the $0.5$ overlap criterion and average precision.
- COCO Consortium, [`cocoeval.py`](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py), the official evaluation code — the IoU thresholds from $0.50$ to $0.95$ in steps of $0.05$, and the 101 recall levels of §5.
- H. Rezatofighi, N. Tsoi, J. Gwak, A. Sadeghian, I. Reid & S. Savarese, "Generalized intersection over union: A metric and a loss for bounding box regression," *CVPR* 2019 — the GIoU of §2's IoU box.
- D2's pixels, boxes and masks are teaching objects frozen on this page ([[03-deep-learning/lab-objects|0. Lab Objects]]); every number was computed here, by hand or by the listing in §5.

## 한국어

> [!note] 왜 배우는가 · Why this matters
> 이 페이지의 자리는 [[physical-ai-map|피지컬 AI 지도]]의 학습과 적응 띠에 있지만, 이 페이지가 받치는 것은 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 첫 층인 인식이고, "*저 패널을 프레임에 설치해*"에서는 2단계 *패널과 프레임을 식별하는* 일, 곧 픽셀이 label, 박스, 마스크, 깊이가 되는 자리다. 인식 숫자는 임계값과 평균의 단위를 알기 전에는 읽을 수 없다. 이 페이지가 고정한 $8\times8$ 연습 이미지 D2([[03-deep-learning/lab-objects|0. Lab Objects]])에서 IoU $0.6$인 박스 하나는 $0.5$에서는 맞고 $0.75$에서는 틀리므로, 같은 예측 셋이 $\mathrm{AP}@0.5=0.833$을 받기도 하고 $\mathrm{mAP}@[.5{:}.95]=0.600$을 받기도 하며, 얇은 케이블을 한 번도 찾지 못하는 분할기도 20클래스 벤치마크에서는 mIoU $0.76$을 보고한다. 그리고 IoU $0.5$를 통과한 박스가 $111$ mm 어긋나 있을 수 있는데, 건설 트랙의 외장 패널 과제 S1([[05-construction-robotics/site-engineering|2.5]])은 구멍 둘을 $\pm5$ mm 안에 맞춰야 한다(§3). [[03-deep-learning/vlm/index|3. VLM §1]]은 이런 이미지 인코더 옆에 텍스트 인코더를 두고, [[03-deep-learning/vla/index|4. VLA]]는 이미지 특징을 정책의 관측으로 넘기며, [[05-construction-robotics/imitating-contact|10. 접촉 모방 §1]]은 구멍의 어긋남을 표준편차 $0.5$ mm의 오차로 읽는 카메라를 가정하며, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지는 블록 4 딥러닝 쪽의 두 번째 페이지로 딥러닝 11–13회차에 해당한다. 이 페이지를 마치면 convolution의 출력 크기와 parameter 수, IoU, AP, mIoU를 손으로 계산할 수 있고, 비전 metric이 어떤 로봇 주장을 뒷받침하고 어떤 주장을 뒷받침하지 못하는지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 세 회차이고, [[03-deep-learning/index|딥러닝 학습 일정]]의 11–13행이다. 앞의 두 회차가 첫 읽기다. **1회차:** 계속 쓰는 대상, 그림, 계산 절을 풀이를 가리고 손으로 한다. $y_{0,2}=40$, $n_{\text{out}}=6$, $\mathrm{IoU}=0.6$이 나오면 된다. **2회차:** §1–§4를 읽고 스스로 점검 1–5와 과제 1–3을 한다. **3회차:** §5의 코드를 돌리고 세 sweep과 그림을 읽은 뒤 과제 4를 한다. 끝으로 같은 박스 셋이 왜 $0.833$과 $0.600$을 받는지, 그리고 IoU $0.5$가 왜 S1의 $\pm5$ mm를 보증하지 못하는지를 자기 말로 설명한다.

### 계속 쓰는 대상: D2

**D2**는 딥러닝 트랙의 고정 텐서 대상 D1–D6([[03-deep-learning/lab-objects|0. Lab Objects]]) 가운데 하나로, 회색조 $8\times8$ 이미지다. 겹치지 않는 $4\times4$ 패치로 나누면 $2\times2$, 즉 토큰 4개다. 각 패치는 값 16개이고 $E\in\mathbb R^{16\times d}$가 $d$차원으로 투영한다.

카탈로그는 D2의 크기와 패치 격자를 고정하지만 픽셀 값은 열어 둔다. 그래서 D2의 집인 이 페이지가 여기서 픽셀을 고정하고 다시는 바꾸지 않는다.

$$I[i,j]=\begin{cases}0,&j\le3\\10,&j\ge4\end{cases}\qquad i,j\in\{0,\dots,7\}$$

높이 10의 수직 계단 모서리가 3열과 4열 사이, 즉 패치 경계에 정확히 놓인다. 페이지 나머지가 둘 다 쓰므로 결과 두 가지를 기억한다. 패치 1과 3(격자의 왼쪽 열)은 전부 0이고 패치 2와 4는 전부 10이므로 **네 토큰 중 둘이 다른 둘과 비트 단위로 같다**. 위치 정보가 없으면 attention은 왼쪽 위 패치와 왼쪽 아래 패치를 구별할 수 없다. 그리고 모서리가 위치를 아는 단일 불연속이므로, 아래의 모든 convolution 응답을 계산하기 전에 예측할 수 있다.

§2의 metric을 위한 페이지 고유 대상 둘도 여기서 고정한다. 둘 다 D2의 픽셀 좌표다. **박스**는 $(x_1,y_1,x_2,y_2)$로 쓰고 두 번째 모서리는 배타적이다. 정답 $G_1=(0,0,4,4)$, $G_2=(4,4,8,8)$으로 각각 넓이 16이고, 예측은 $P_1=(0,0,4,4)$ 신뢰도 $0.90$, $P_2=(3,3,7,7)$ 신뢰도 $0.80$, $P_3=(4,3,8,7)$ 신뢰도 $0.60$이다. **마스크**는 같은 이미지의 2클래스 분할이다. "케이블" 클래스는 4열만 차지해 64픽셀 중 8픽셀이고 나머지는 배경이다.

*범위: 이 페이지는 시각 입력이 텐서가 되는 방식(convolution 산술과 패치 토큰), 출력 선택이 backbone을 과제로 바꾸는 방식, 그리고 그 출력을 채점하는 metric — IoU, mAP, 클래스별 평균 mIoU — 을 손으로 다시 계산할 수 있을 만큼 작은 대상에서 읽는 법을 가르친다. 픽셀 아래의 카메라 기하는 가르치지 않는다. 그것은 [[04-robotics/geometric-perception-calibration|3.5 기하 인식 §1]]이다. depth 복원과 3D 복원도 아니다. 그것은 [[04-robotics/geometric-perception-calibration|3.5 기하 인식 §2]]와 [[01-canonical-papers/canonical-list|canonical list]]의 3D 항목이다. loss·optimizer·보폭 같은 학습 기계도 아니다. 그것은 [[03-deep-learning/foundations/index|1. 학습 시스템 §1–§2]]와 그 §6 실습이다. attention 자체도 아니다. 그것은 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]와, 이 페이지의 D2 위에서 계산한 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]]다. §2 표의 depth와 3D 행은 표를 완성하려고 이름만 싣고, depth metric의 정의는 §3에 두며, 둘 다 여기서 가르치지는 않는다.*

### 그림으로 먼저 보기

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="D2의 8×8 계단 이미지와 2×2 패치 격자, 40을 내는 3×3 창과 6×6 출력 맵의 칸, 토큰 shape, 모서리 좌표를 적은 박스 다섯과 P3·G2의 4×3 교집합, 그리고 8과 56으로 센 케이블 마스크">
  <defs><marker id="aD2k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) 픽셀, 패치 격자, 3×3 창 하나 · stride 1, pad 0</text>
  <rect x="102" y="50" width="72" height="144" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <line x1="30" y1="50" x2="174" y2="50" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="68" x2="174" y2="68" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="86" x2="174" y2="86" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="104" x2="174" y2="104" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="122" x2="174" y2="122" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="140" x2="174" y2="140" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="158" x2="174" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="176" x2="174" y2="176" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="194" x2="174" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="30" y1="50" x2="30" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="48" y1="50" x2="48" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="66" y1="50" x2="66" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="84" y1="50" x2="84" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="102" y1="50" x2="102" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="120" y1="50" x2="120" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="138" y1="50" x2="138" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="156" y1="50" x2="156" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="174" y1="50" x2="174" y2="194" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <rect x="30" y="50" width="144" height="144" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <line x1="102" y1="50" x2="102" y2="194" stroke="currentColor" stroke-width="2.4"/>
  <line x1="30" y1="122" x2="174" y2="122" stroke="currentColor" stroke-width="2.4"/>
  <text x="24" y="63" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">0</text>
  <text x="39" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">0</text>
  <text x="24" y="81" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">1</text>
  <text x="57" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <text x="24" y="99" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">2</text>
  <text x="75" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">2</text>
  <text x="24" y="117" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">3</text>
  <text x="93" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">3</text>
  <text x="24" y="135" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">4</text>
  <text x="111" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">4</text>
  <text x="24" y="153" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">5</text>
  <text x="129" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">5</text>
  <text x="24" y="171" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">6</text>
  <text x="147" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">6</text>
  <text x="24" y="189" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">7</text>
  <text x="165" y="207" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">7</text>
  <text x="66" y="117" font-size="11" fill="currentColor" text-anchor="middle">패치 1</text>
  <text x="138" y="117" font-size="11" fill="currentColor" text-anchor="middle">패치 2</text>
  <text x="66" y="189" font-size="11" fill="currentColor" text-anchor="middle">패치 3</text>
  <text x="138" y="189" font-size="11" fill="currentColor" text-anchor="middle">패치 4</text>
  <text x="12" y="225" font-size="11" fill="currentColor" fill-opacity="0.8">음영 = 10, 빈칸 = 0, 계단은 패치 경계선 위</text>
  <rect x="66" y="50" width="54" height="54" stroke="currentColor" stroke-width="2.6" fill="currentColor" fill-opacity="0.12"/>
  <line x1="232" y1="50" x2="340" y2="50" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="68" x2="340" y2="68" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="86" x2="340" y2="86" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="104" x2="340" y2="104" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="122" x2="340" y2="122" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="140" x2="340" y2="140" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="158" x2="340" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="232" y1="50" x2="232" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="250" y1="50" x2="250" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="268" y1="50" x2="268" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="286" y1="50" x2="286" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="304" y1="50" x2="304" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="322" y1="50" x2="322" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="340" y1="50" x2="340" y2="158" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <rect x="232" y="50" width="108" height="108" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <rect x="268" y="50" width="18" height="18" stroke="currentColor" stroke-width="2.6" fill="currentColor" fill-opacity="0.12"/>
  <text x="241" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1.0" font-weight="bold">40</text>
  <text x="295" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="63" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="63" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">0</text>
  <text x="241" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">0</text>
  <text x="241" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="81" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="81" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">1</text>
  <text x="259" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <text x="241" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="99" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="99" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">2</text>
  <text x="277" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">2</text>
  <text x="241" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="117" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="117" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">3</text>
  <text x="295" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">3</text>
  <text x="241" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="135" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="135" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">4</text>
  <text x="313" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">4</text>
  <text x="241" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="259" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="277" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="295" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">40</text>
  <text x="313" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="331" y="153" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.45">0</text>
  <text x="226" y="153" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">5</text>
  <text x="331" y="171" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">5</text>
  <text x="286" y="189" font-size="11" fill="currentColor" text-anchor="middle">출력 맵 6 × 6 · y<tspan dy="3" font-size="10">0,2</tspan><tspan dy="-3" dx="3.5">= 40</tspan></text>
  <text x="286" y="205" font-size="11" fill="currentColor" text-anchor="middle">n<tspan dy="3" font-size="10">out</tspan><tspan dy="-3" dx="3.5">= ⌊(8 + 0 − 3)/1⌋ + 1 = 6</tspan></text>
  <path d="M 114 49 C 124 19, 277.0 15, 277.0 48" stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#aD2k)"/>
  <text x="362" y="42" font-size="11" fill="currentColor">flatten: 4 × 16</text>
  <line x1="385" y1="52" x2="385" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="52" x2="392" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="52" x2="399" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="52" x2="406" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="52" x2="413" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="52" x2="420" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="52" x2="427" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="52" x2="434" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="52" x2="441" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="52" x2="448" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="52" x2="455" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="52" x2="462" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="52" x2="469" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="52" x2="476" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="52" x2="483" y2="61" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="52" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="61" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">1</text>
  <rect x="378" y="66" width="112" height="9" stroke="none" fill="currentColor" fill-opacity="0.3"/>
  <line x1="385" y1="66" x2="385" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="66" x2="392" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="66" x2="399" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="66" x2="406" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="66" x2="413" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="66" x2="420" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="66" x2="427" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="66" x2="434" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="66" x2="441" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="66" x2="448" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="66" x2="455" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="66" x2="462" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="66" x2="469" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="66" x2="476" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="66" x2="483" y2="75" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="66" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="75" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">2</text>
  <line x1="385" y1="80" x2="385" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="80" x2="392" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="80" x2="399" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="80" x2="406" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="80" x2="413" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="80" x2="420" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="80" x2="427" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="80" x2="434" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="80" x2="441" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="80" x2="448" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="80" x2="455" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="80" x2="462" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="80" x2="469" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="80" x2="476" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="80" x2="483" y2="89" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="80" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="89" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">3</text>
  <rect x="378" y="94" width="112" height="9" stroke="none" fill="currentColor" fill-opacity="0.3"/>
  <line x1="385" y1="94" x2="385" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="392" y1="94" x2="392" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="399" y1="94" x2="399" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="406" y1="94" x2="406" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="413" y1="94" x2="413" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="420" y1="94" x2="420" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="427" y1="94" x2="427" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="434" y1="94" x2="434" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="441" y1="94" x2="441" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="448" y1="94" x2="448" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="455" y1="94" x2="455" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="462" y1="94" x2="462" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="469" y1="94" x2="469" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="476" y1="94" x2="476" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <line x1="483" y1="94" x2="483" y2="103" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.35"/>
  <rect x="378" y="94" width="112" height="9" stroke="currentColor" stroke-width="0.9" fill="none"/>
  <text x="373" y="103" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">4</text>
  <text x="498" y="61" font-size="11" fill="currentColor" fill-opacity="0.85">1 = 3</text>
  <text x="498" y="75" font-size="11" fill="currentColor" fill-opacity="0.85">2 = 4</text>
  <line x1="402" y1="110" x2="402" y2="128" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD2k)"/>
  <text x="411" y="123" font-size="11" fill="currentColor">× E (16 × d)</text>
  <text x="402" y="146" font-size="11" fill="currentColor" text-anchor="middle">4 × d</text>
  <line x1="402" y1="152" x2="402" y2="180" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD2k)"/>
  <text x="411" y="162" font-size="11" fill="currentColor">+ 위치 p<tspan dy="3" font-size="10">i</tspan></text>
  <text x="411" y="180" font-size="11" fill="currentColor">+ class 토큰</text>
  <text x="402" y="198" font-size="11" fill="currentColor" text-anchor="middle">5 × d</text>
  <text x="12" y="246" font-size="12" fill="currentColor">(b) 박스, 픽셀 좌표로 적은 모서리</text>
  <line x1="30" y1="270" x2="182" y2="270" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="289" x2="182" y2="289" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="308" x2="182" y2="308" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="327" x2="182" y2="327" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="346" x2="182" y2="346" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="365" x2="182" y2="365" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="384" x2="182" y2="384" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="403" x2="182" y2="403" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="422" x2="182" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="30" y1="270" x2="30" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="49" y1="270" x2="49" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="68" y1="270" x2="68" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="87" y1="270" x2="87" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="106" y1="270" x2="106" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="125" y1="270" x2="125" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="144" y1="270" x2="144" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="163" y1="270" x2="163" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <line x1="182" y1="270" x2="182" y2="422" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.18"/>
  <rect x="30" y="270" width="152" height="152" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.6"/>
  <text x="30" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">0</text>
  <text x="24" y="274" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">0</text>
  <text x="49" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <text x="24" y="293" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">1</text>
  <text x="68" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">2</text>
  <text x="24" y="312" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">2</text>
  <text x="87" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">3</text>
  <text x="24" y="331" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">3</text>
  <text x="106" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">4</text>
  <text x="24" y="350" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">4</text>
  <text x="125" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">5</text>
  <text x="24" y="369" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">5</text>
  <text x="144" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">6</text>
  <text x="24" y="388" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">6</text>
  <text x="163" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">7</text>
  <text x="24" y="407" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">7</text>
  <text x="182" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">8</text>
  <text x="24" y="426" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.7">8</text>
  <rect x="106" y="346" width="76" height="57" stroke="none" fill="currentColor" fill-opacity="0.28"/>
  <rect x="30" y="270" width="76" height="76" stroke="currentColor" stroke-width="2.2" fill="none"/>
  <rect x="106" y="346" width="76" height="76" stroke="currentColor" stroke-width="2.2" fill="none"/>
  <rect x="32.5" y="272.5" width="71" height="71" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="5 3"/>
  <rect x="87" y="327" width="76" height="76" stroke="currentColor" stroke-width="1.4" fill="none" stroke-opacity="0.7" stroke-dasharray="5 3"/>
  <rect x="106" y="327" width="76" height="76" stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="9 3 2 3"/>
  <circle cx="106" cy="346" r="2.8" stroke="none" fill="currentColor"/>
  <circle cx="182" cy="403" r="2.8" stroke="none" fill="currentColor"/>
  <text x="144" y="379.5" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">12</text>
  <text x="34.8" y="288.1" font-size="11" fill="currentColor">G<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, P</tspan><tspan dy="3" font-size="10">1</tspan></text>
  <text x="179.2" y="418.2" font-size="11" fill="currentColor" text-anchor="end">G<tspan dy="3" font-size="10">2</tspan></text>
  <text x="89.8" y="399.2" font-size="11" fill="currentColor" fill-opacity="0.85">P<tspan dy="3" font-size="10">2</tspan></text>
  <text x="180.5" y="340.7" font-size="11" fill="currentColor" text-anchor="end">P<tspan dy="3" font-size="10">3</tspan></text>
  <line x1="200" y1="270" x2="222" y2="270" stroke="currentColor" stroke-width="2.2"/>
  <text x="228" y="274" font-size="11" fill="currentColor">G<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= (0, 0, 4, 4)</tspan></text>
  <line x1="200" y1="289" x2="222" y2="289" stroke="currentColor" stroke-width="2.2"/>
  <text x="228" y="293" font-size="11" fill="currentColor">G<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= (4, 4, 8, 8)</tspan></text>
  <line x1="200" y1="308" x2="222" y2="308" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 3"/>
  <text x="228" y="312" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= (0, 0, 4, 4) · 0.90</tspan></text>
  <line x1="200" y1="327" x2="222" y2="327" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.7" stroke-dasharray="5 3"/>
  <text x="228" y="331" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= (3, 3, 7, 7) · 0.80</tspan></text>
  <line x1="200" y1="346" x2="222" y2="346" stroke="currentColor" stroke-width="1.8" stroke-dasharray="9 3 2 3"/>
  <text x="228" y="350" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">= (4, 3, 8, 7) · 0.60</tspan></text>
  <rect x="200" y="364" width="22" height="10" stroke="none" fill="currentColor" fill-opacity="0.28"/>
  <text x="228" y="373" font-size="11" fill="currentColor">P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">∩ G</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">: x 4–8, y 4–7</tspan></text>
  <text x="228" y="390" font-size="11" fill="currentColor">4 × 3 = 12</text>
  <text x="200" y="411" font-size="11.5" fill="currentColor" font-weight="bold">IoU = 12 / (16 + 16 − 12) = 0.6</text>
  <text x="426" y="246" font-size="12" fill="currentColor">(c) 마스크, 개수로</text>
  <rect x="488" y="270" width="13" height="104" stroke="none" fill="currentColor" fill-opacity="0.45"/>
  <line x1="436" y1="270" x2="540" y2="270" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="283" x2="540" y2="283" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="296" x2="540" y2="296" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="309" x2="540" y2="309" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="322" x2="540" y2="322" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="335" x2="540" y2="335" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="348" x2="540" y2="348" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="361" x2="540" y2="361" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="374" x2="540" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="436" y1="270" x2="436" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="449" y1="270" x2="449" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="462" y1="270" x2="462" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="475" y1="270" x2="475" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="488" y1="270" x2="488" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="501" y1="270" x2="501" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="514" y1="270" x2="514" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="527" y1="270" x2="527" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <line x1="540" y1="270" x2="540" y2="374" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>
  <rect x="436" y="270" width="104" height="104" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <rect x="488" y="270" width="13" height="104" stroke="currentColor" stroke-width="1.8" fill="none"/>
  <text x="462" y="327" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">56</text>
  <text x="494.5" y="390" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">8</text>
  <text x="426" y="418" font-size="11" fill="currentColor">케이블(4열): 8</text>
  <text x="426" y="434" font-size="11" fill="currentColor">배경: 56</text>
</svg>

고정된 숫자로 그린 D2이고, 임베딩 폭은 $d$로 남겨 두었다. (a) 계단 모서리가 $2\times2$ 패치 격자의 선 위에 놓이므로 펼친 토큰 넷($4\times16$)은 위치를 더하기 전까지 서로 다른 벡터 둘뿐이고, $E$가 이를 $4\times d$로 투영한 뒤 class 토큰이 붙어 $5\times d$가 되며, 0–2행, 2–4열의 $3\times3$ 창은 $6\times6$ 출력 맵에 $y_{0,2}=40$을 낸다. (b) 모서리 좌표로 적은 박스 다섯과 $\mathrm{IoU}=12/20=0.6$을 내는 $P_3$·$G_2$의 $4\times3$ 교집합, 그리고 (c) 개수로 센 케이블 마스크, 케이블 8픽셀 대 배경 56픽셀이다.

### 대상으로 한 번 끝까지

이것이 과제의 대상이다. 과제가 요구하는 세 가지 — 창 하나, 출력 크기 하나, 겹침 하나 — 를 고정된 숫자로 여기서 먼저 한다.

**convolution 응답 하나, 손으로.** 수직 모서리 커널

$$K=\begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix}$$

을 stride 1, padding 0으로 민다. 딥러닝의 "convolution"은 상관(cross-correlation)이다. 출력 $(i,j)$는 $\sum_{u,v}K[u,v]\,I[i+u,j+v]$이고 커널을 뒤집지 않는다. $(0,2)$에서 창은 0–2행, 2–4열을 덮고 모든 행이 $(0,0,10)$이므로

$$y_{0,2}=(-1)(0)+(0)(0)+(1)(10)\;+\;(-2)(0)+(0)(0)+(2)(10)\;+\;(-1)(0)+(0)(0)+(1)(10)=40.$$

$I$가 모든 열에서 일정하므로 전체 맵은 $y_{i,j}=4\big(I[\cdot,j+2]-I[\cdot,j]\big)$로 줄고, $j\in\{2,3\}$에서 $40$, 나머지에서 $0$이다. 즉 계단 모서리 하나를 폭 3 커널이 **두 열 너비로** 보고한다. 폭 $k$의 모서리 검출기는 불연속을 출력 $k-1$칸에 번지게 한다. 모서리 맵이 두껍게 보이는 이유이고, "1픽셀 정밀도" 주장 옆에 커널 폭이 있어야 하는 이유다.

**출력 크기, 기호를 모두 달아서.** 미끄러지는 창은 $0,s,2s,\dots$에서 시작할 수 있고 마지막 시작점은 뒤에 $k$칸을 남겨야 하므로, 유효한 시작점의 개수는

$$n_{\text{out}}=\left\lfloor\frac{n+2p-k}{s}\right\rfloor+1,$$

$n$은 입력 한 변, $k$는 커널 한 변, $s$는 stride, $p$는 **한쪽마다** 붙이는 zero padding이고 $+1$은 위치 0의 시작을 센다. $k=3$, $s=1$, $p=0$인 D2에서는 $\lfloor(8+0-3)/1\rfloor+1=6$으로 위의 $6\times6$ 맵과 맞는다. floor는 장식이 아니다. $k=3,s=2,p=0$이면 창이 $\lfloor5/2\rfloor+1=3$개로 0–2열, 2–4열, 4–6열을 덮고, 7열은 어떤 창에도 들어가지 않는다. 어떤 창도 덮지 않은 끝자락 픽셀은 조용히 버려진다. "feature map이 하나 어긋난다"의 진짜 출처다.

**겹침 하나, 손으로.** $P_3=(4,3,8,7)$과 $G_2=(4,4,8,8)$. 교집합은 $[\max(4,4),\min(8,8)]\times[\max(3,4),\min(7,8)]$로 가로 $4$, 세로 $3$이므로 $|A\cap B|=12$다. 각 박스가 넓이 16이므로 $|A\cup B|=16+16-12=20$이고

$$\mathrm{IoU}(P_3,G_2)=\frac{12}{20}=0.6.$$

예측 하나, 정답 하나인데 "이것은 검출인가"의 답이 벌써 임계값에 달려 있다. $0.6\ge0.5$이면 IoU $0.5$에서 맞힘으로 세는 PASCAL VOC 벤치마크의 관례에서 참양성이고, $0.6<0.75$이면 더 엄한 관례에서 거짓양성이다. 박스는 아무것도 바뀌지 않았다. §5가 이 사실 하나를 $\mathrm{AP}@0.5=0.833$과, COCO 벤치마크가 임계값 $0.50,0.55,\dots,0.95$ 열 개에 대해 평균한 $\mathrm{mAP}@[.5{:}.95]=0.600$의 간극으로 바꾼다. 둘의 정의는 §2에 있다.

### 1. 시각 구조를 넣는 두 방식

이미지에는 픽셀마다 가중치 하나씩을 줄 수 없을 만큼 많은 픽셀이 있고, 한 구석에서 통하는 검출기는 다른 구석에서도 통해야 한다. 모든 비전 구조는 이 문제에 **귀납 편향**(inductive bias), 곧 모델이 데이터를 보기 전에 구조에 넣어 둔 가정으로 답하는데, 두 계열은 얼마나 넣어 두느냐가 다르다. convolution은 가까운 픽셀끼리 한 덩어리이고 한 무늬는 어디에 나타나든 같은 뜻이라고 가정하고, Vision Transformer는 거의 아무것도 가정하지 않은 채 그것을 데이터에서 배운다([[01-canonical-papers/notes/1-foundations/vit|ViT 노트]]).

convolution은 **가중치 공유**(weight sharing)로 가정을 넣는다. 작은 필터 하나를 모든 위치에서 다시 쓰는 것이다. D2에 $3\times3$ 커널을 stride 1, padding 0으로 걸면 계산 절의 $6\times6$ 맵이 나오고, 입력 1채널·출력 4채널이면 bias를 포함해 parameter가 $4(3\cdot3+1)=40$개다. 이 개수 $C_{\text{out}}(C_{\text{in}}k^2+1)$에는 $n$이 없다. 같은 40개의 숫자가 $8\times8$ 이미지에도 $4000\times4000$ 이미지에도 쓰인다. 층이 픽셀마다 가중치를 두는 것이 아니라 필터 하나를 *재사용*하기 때문이다. 같은 출력 $4\times6\times6=144$개를 D2의 64픽셀에서 내는 완전연결층은 $144(64+1)=9{,}360$개가 필요하고, 같은 모서리 검출기를 36개 위치에서 저마다 따로 배워야 한다. 이산 convolution 자체와, 왜 이동 불변성이 그 재사용을 정당화하는지는 [[02-foundations/signal-processing|6. 신호처리 §1]]에 있다.

Vision Transformer는 다른 길을 간다. $4\times4$ 패치마다 펼쳐 숫자 16개짜리 벡터, 곧 **토큰**(token)으로 만들고, $E$로 투영하고, 위치 벡터를 더한 뒤, 맨 앞에 **class 토큰**(class token)을 붙인다. class 토큰은 어느 패치에도 속하지 않는 학습된 벡터 하나로, attention을 통해 모든 패치에서 정보를 모으고, 분류기는 그 마지막 상태만 읽는다. 그림에서 토큰 넷이 $5\times d$가 되는 이유다. 그다음 attention이 토큰의 내용에서 계산한 가중치로 토큰들을 섞는다. 토큰을 이웃에 묶어 두는 것이 없으므로 패치 attention은 먼 거리의 상호작용을 곧바로 배울 수 있지만 지역성은 데이터에서 배워야 하고, 대개 convolution보다 데이터와 사전학습에 더 크게 기댄다.

D2가 그 거래의 대가를 한 줄로 보여 준다. 평탄화한 네 패치는 $(0,\dots,0)$, $(10,\dots,10)$, $(0,\dots,0)$, $(10,\dots,10)$이므로 토큰 1과 3이 같은 벡터이고 2와 4도 그렇다. self-attention은 **순열 등변**(permutation-equivariant)이다. 입력 토큰의 순서를 바꾸면 출력도 같은 순서로 바뀔 뿐 다른 것은 바뀌지 않는다. 그래서 위치 벡터를 더하지 않으면 네 토큰을 집합, 곧 어두운 것 둘과 밝은 것 둘로만 본다. D2를 위아래로 뒤집는 것은 시험이 되지 못한다. 모든 열이 일정해서 뒤집은 이미지가 D2 그 자체이기 때문이다. 위치 없는 attention이 구별하지 못하는 것은 같은 네 토큰으로 만든 배치들, 곧 $2\times2$ 격자에 어두운 패치 둘과 밝은 패치 둘을 놓는 여섯 가지 배치 전부다. D2와, 어두운 절반이 오른쪽에 있는 거울상과, 왼쪽 위와 오른쪽 아래가 어두운 바둑판도 그 안에 있고, 집합 위의 가중합을 읽는 class 토큰은 여섯 모두에서 같은 상태로 끝난다. 위치 정보는 개선이 아니라 배치를 나르는 유일한 것이다. convolution은 이 문제를 겪은 적이 없다. 출력 격자 자체가 배치이기 때문이다. [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer §5]]가 순열 등변성을 정의하고 한 줄로 증명하며, [[03-deep-learning/foundations/attention-transformer|1.2 §8]]의 실습이 D2에서 거울 시험을 한다. 거울상의 출력은 원래 출력을 재배열한 것과, 위치 표가 있으면 $1.217719$만큼, 없으면 정확히 $0$만큼 다르다.

### 2. 출력이 문제를 정의한다

*한 문장으로:* 시각 과제는 모델이 무엇을 출력하고 그 출력을 어떻게 채점하느냐로 정해진다. 그래서 headline 숫자는 metric의 임계값, 매칭 규칙, 무엇에 대해 평균하는지를 알기 전에는 거의 아무 말도 하지 않는다.

*이 절에서 하나만 가져간다면:* 임계값은 방법이 아니라 metric에 속한다. 그래서 계산 절의 박스 하나가 같은 세 예측을 $0.833$으로도, $0.600$으로도 만든다(아래 mAP 상자, 둘을 그리는 곳은 §5).

| 과제 | 출력 | 대표 metric | 주의 |
|---|---|---|---|
| 분류 | 이미지당 label/분포 | top-1 accuracy | 클래스 불균형을 숨김 |
| 검출 | box, label, confidence | IoU 임계값 위의 mAP | matching과 임계값에 의존 |
| 분할 | pixel 또는 object mask | IoU / mIoU | 작은 클래스가 평균에서 사라질 수 있음 |
| 단안 depth | pixel당 깊이 | AbsRel, RMSE, $\delta$ | metric scale이 없을 수 있음 |
| 3D 복원 | camera/geometry/appearance | pose 오차, depth, rendering | photorealism은 기하 정확도가 아님 |

backbone 이름보다 출력 표현·loss·평가 protocol을 먼저 본다.

표의 모든 metric은 여기서 — depth metric은 §3에서 — 정의하거나 연결한다. 이름만 적힌 metric의 행은 검산할 수 없기 때문이다. 일반 사전은 [[02-foundations/ml-practice|9. ML 실무 §3]]에 있고, 아래는 비전 논문이 이 metric들에서 틀리는 부분을 D2의 박스와 마스크 위에서 더한다. **Top-1 accuracy**는 최고 점수 클래스가 정답인 이미지의 비율, 즉 top-$k$의 $k=1$이고 여기서는 그 이상이 필요 없다.

#### 두 영역의 겹침: IoU

> **Intersection over union의 정의.** **IoU**는 *같은 이미지 안의 두 영역 사이의 유사도 점수*다. 넓이(또는 픽셀 수)의 무차원 비이지 거리도, 오차도, 확률도 아니다. 정의 조건 셋. **대칭**이라 $\mathrm{IoU}(A,B)=\mathrm{IoU}(B,A)$이므로 어느 쪽이 예측인지에 대해 아무 말도 하지 않는다. 어느 한쪽이 아니라 **합집합으로 정규화**되므로, 거대한 박스가 정답을 삼켜서 좋은 점수를 받는 일이 막힌다. 그리고 **척도 무관**이라 두 영역의 좌표에 10을 곱해도 값이 같다.
>
> $$\mathrm{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}$$
>
> $|\cdot|$은 박스에서는 넓이, 마스크에서는 픽셀 수다. 구현할 것은 두 번째 형태인데, 아래 모서리의 $\max$와 위 모서리의 $\min$으로 얻는 교집합만 있으면 되기 때문이다.
>
> - **예**: D2의 $P_3=(4,3,8,7)$과 $G_2=(4,4,8,8)$은 $4\times3$ 직사각형에서 만나므로 $\mathrm{IoU}=12/(16+16-12)=0.6$이다.
> - **비예**: 피복 비율 $|A\cap B|/|B|$. $8\times8$ 전체를 덮는 예측은 그 값이 $1.0$이고 IoU로는 $16/64=0.25$다. 분모의 합집합이 게으른 큰 박스를 벌주는 항이고, "coverage"를 보고하는 논문은 IoU를 보고한 것이 아니다.
> - **비예**: 완만하게 나빠지는 유사도. 닿지 않는 두 박스는 1픽셀 떨어졌든 100픽셀 떨어졌든 $\mathrm{IoU}=0$이라, 접촉 밖에서는 IoU가 아무 기울기 정보도 나르지 않는다. 검출기를 좌표 회귀나 GIoU 계열로 *학습*하고 IoU로 *평가*하는 이유다.
> - **왜 중요한가**: 이 페이지의 모든 검출·분할 수치가 임계값에 대한 IoU 비교의 개수다. 그러므로 임계값은 metric의 일부이지 방법의 일부가 아니다. 이 절의 첫 줄이 말한 요점이고, §5가 그것을 headline의 간극으로 바꾼다.

#### 검출의 순위: AP와 mAP

> **Average precision과 mAP의 정의.** **AP**는 *한 클래스의, 한 IoU 임계값에서의 precision–recall 곡선 아래 넓이*다. 단일 결정이 아니라 순위를 요약하므로 박스만이 아니라 신뢰도가 필요하다. 정의 조건 넷이고, 논문은 이 중 하나를 빠뜨려 비교 가능성을 잃는다. 검출은 **신뢰도 순으로 정렬**되고 **아직 매칭되지 않은 정답에 탐욕적으로 매칭**되므로, 이미 차지된 물체에 붙은 두 번째 박스는 아무리 좋아도 거짓양성이다. **IoU가 임계값 $t$에 도달할 때만** 매칭으로 센다. recall은 **정답 물체 수**로 정규화하므로 놓친 물체는 도달되지 않는 recall로 들어온다. 그리고 **mAP는 AP를 클래스에 대해 평균**하고, COCO 관례에서는 임계값 열 개에 대해서도 평균한다.
>
> $$\mathrm{AP}(t)=\sum_{n}\big(R_n-R_{n-1}\big)\,P^{\mathrm{interp}}_n,\qquad P^{\mathrm{interp}}_n=\max_{m\ge n}P_m,\qquad \mathrm{mAP}=\frac1C\sum_{c=1}^{C}\mathrm{AP}_c$$
>
> $P_n$과 $R_n$은 $n$번째 검출 뒤의 precision과 recall, $R_0=0$, $C$는 클래스 수다. 보간은 이 recall 이상에서의 최고 precision을 취하는데, 그래야 곡선이 단조가 되고 뒤늦은 좋은 검출이 앞선 거짓양성에 취소되지 않기 때문이다.
>
> - **예**: $t=0.5$에서 D2의 예측 셋은 TP, FP, TP 순이므로 $P=(1,0.5,0.667)$, $R=(0.5,0.5,1)$이고 $\mathrm{AP}=0.5(1)+0.5(0.667)=0.833$이다. [[02-foundations/ml-practice|9. ML 실무 §3]]의 예제와 같은 모양을, 이번에는 좌표가 이 페이지에 적힌 박스 위에서 한 것이다.
> - **비예**: VOC 수치와 COCO 수치의 비교. VOC의 mAP는 $\mathrm{AP}(0.5)$이고 COCO의 mAP는 $t=0.50,0.55,\dots,0.95$의 평균이다. D2에서 각각 $0.833$과 $0.600$이다. 검출기는 그대로인데 관례만으로 23포인트가 벌어진다.
> - **왜 중요한가**: 대부분의 검출 논문이 보고하는 유일한 숫자가 mAP인데, 이 숫자는 임계값 집합·매칭 규칙·클래스 가중이라는 세 선택을 숨긴다. 위치 정확도를 올려 mAP를 올린 방법과 순위를 올려 mAP를 올린 방법은 다른 기여인데 headline이 같다.

#### 클래스에 대한 평균: mIoU

> **Mean IoU, 그리고 분할 metric이 무엇에 대해 평균하는가.** **mIoU**는 *묶은 픽셀 수로 계산한 클래스별 IoU를 클래스에 대해 평균한 값*이고, 평균의 단위가 주장 전체다. 정의 조건 셋. 클래스별 IoU는 **픽셀 수로** $\mathrm{IoU}_c=TP_c/(TP_c+FP_c+FN_c)$처럼 계산되므로, 픽셀이 많은 클래스는 *자기 점수*에 더 많은 증거를 낸다. 바깥 평균은 **클래스에 대해 균등**하다. 픽셀 수와 무관하게 각 클래스가 $1/C$의 가중을 받는데, 이것이 pixel accuracy와 정확히 반대되는 의도적 선택이다. 그리고 비를 취하기 전에 **평가 집합 전체에서 묶는다**. 그래서 mIoU는 이미지별 mIoU의 평균이 아니고, 이미지별 평균은 보통 더 큰 다른 숫자다.
>
> $$\mathrm{mIoU}=\frac1C\sum_{c=1}^{C}\frac{TP_c}{TP_c+FP_c+FN_c}\qquad\text{대}\qquad \mathrm{acc}_{\text{pixel}}=\frac{\sum_c TP_c}{\text{전체 픽셀}}$$
>
> $TP_c$, $FP_c$, $FN_c$는 클래스 $c$의 픽셀 수이고 $C$는 클래스 수다. 둘이 다른 이유는 왼쪽이 합 안에서 비를 취하고 오른쪽이 합 밖에서 취하기 때문이다. 8픽셀짜리 클래스가 56픽셀짜리 클래스만큼 중요해질 수 있는 쪽은 왼쪽뿐이다.
>
> - **예**: D2의 케이블은 64픽셀 중 8픽셀이다. 전부 배경으로 예측하는 모델은 pixel accuracy $56/64=0.875$, $\mathrm{mIoU}=(0.875+0)/2=0.4375$다. §5는 pixel accuracy가 *같으면서* $\mathrm{mIoU}=0.679$인 두 번째 예측을 준다.
> - **비예**: pixel accuracy. 배경이 지배적인 이미지에서는 배경 비율에 가깝고 모델과 거의 무관하다. 분할 벤치마크가 이것을 버린 이유다.
> - **비예**: 클래스 지표 없이 데이터셋 전체에 붙은 "IoU". $C$를 적지 않은 mIoU이거나 이진 전경 하나의 IoU인데, 희귀 클래스가 실패하면 앞의 것은 그 클래스의 몫만큼 떨어지고 뒤의 것은 거의 움직이지 않는다.
> - **왜 중요한가**: 균등한 클래스 가중은 보호이지 보증이 아니다. 20클래스 벤치마크에서 19개가 $0.80$이고 케이블이 $0.00$이면 $\mathrm{mIoU}=19\cdot0.80/20=0.76$이다. 깨끗한 run보다 4포인트 낮고 정상 변동 안쪽인데, 로봇이 곧 들이받을 클래스가 그것이다. mIoU는 희귀 클래스를 *큰 배경*으로부터 지키지, 다른 19개 클래스로부터 지키지 않는다.

### 3. 학습 뒤에도 기하는 남는다

학습된 출력은 로봇의 좌표계와 단위로 옮겨진 뒤에야 로봇에 쓸모가 있고, 픽셀에서 잰 점수나 정렬을 거친 뒤의 점수는 미터에 대해 아무 주장도 하지 않는다. crop·resize·augmentation은 카메라 좌표를 바꾼다. depth 신경망은 상대 깊이를 예측할 수 있는데 로봇에는 미터가 필요하다. 높은 mIoU도 안전을 결정하는 얇은 케이블을 놓칠 수 있다. §2의 20클래스 산술로는 mIoU $0.76$ 대 $0.80$이고, 어떤 심사자도 실패라고 부르지 않을 차이다. 로봇에서는 frame·unit·latency·confidence와 폐루프 연결을 기록한다.

#### 깊이: 설계상 엇갈리는 세 오차

§2 표의 depth 행은 metric 셋으로 채점한다. 유효 픽셀 $N$개에서 예측 깊이 $\hat d_i$와 정답 $d_i$에 대해

$$\mathrm{AbsRel}=\frac1N\sum_i\frac{|\hat d_i-d_i|}{d_i},\qquad \mathrm{RMSE}=\sqrt{\frac1N\sum_i(\hat d_i-d_i)^2},\qquad \delta_1=\frac1N\Big|\Big\{i:\max\big(\tfrac{\hat d_i}{d_i},\tfrac{d_i}{\hat d_i}\big)<1.25\Big\}\Big|,$$

이므로 AbsRel은 무차원이고 가까운 픽셀을 가장 무겁게 치며, RMSE는 미터 단위이고 먼 픽셀이 지배하며, $\delta_1$은 *임계 정확도*로 양방향 $1.25$배 안에 든 픽셀의 비율이다. $d=(2,4)$ m와 $\hat d=(2.5,3.6)$ m인 픽셀 둘이면 $\mathrm{AbsRel}=0.175$, $\mathrm{RMSE}=0.452769$ m, $\delta_1=0.5$이고, 첫 픽셀이 비가 정확히 $1.25$라 엄격 부등호에서 탈락한다. 셋은 설계상 엇갈리므로 depth 논문은 셋 다 보고한다.

방법이 척도 모호하면 셋 다 정렬 단계 *뒤에* 계산된다. 척도 모호하다는 것은 출력이 깊이를 알 수 없는 척도, 흔히 알 수 없는 이동까지 남긴 채로만 정한다는 뜻이다. 척도 $s$와 이동 $t$를 모르는 채 역깊이 $r=s/Z+t$를 예측하는 신경망이 그렇다(3.5 §6의 기호다. 이 페이지의 다른 곳에서 $s$는 stride, $t$는 IoU 임계값이다). 그런 방법은 이미지마다 척도(흔히 그 이동까지)를 정답에 맞춰 놓고 평가하므로, 그 AbsRel은 *형태* 일치를 재고 미터에 대해서는 아무 주장도 하지 않는다. depth 수치를 로봇의 요구와 비교하기 전에 어떤 정렬이 적용됐는지 묻는다. 로봇에서는 척도가 실제의 무언가에서 와야 한다. [[04-robotics/geometric-perception-calibration|3.5 기하 인식 §6]]이 한 리그에서 척도가 들어오는 세 자리 — 보정된 스테레오, 알려진 길이, 깊이를 아는 앵커 픽셀에 대한 정렬 — 를 계산하고, [[04-robotics/perception-sensors-rigs|3.6 인식 센서 §3–§4]]가 미터를 직접 재는 센서, 곧 스테레오와 ToF를 오차 막대와 함께 다룬다. 애초에 미터를 정의하는 기하는 [[04-robotics/geometric-perception-calibration|3.5 §1]]이다.

#### IoU 임계값에서 밀리미터로

검출 임계값은 허용오차이지만 상대적인 허용오차다. 높이가 같고 폭도 $w$로 같은 두 박스를 옆으로 $d$만큼 어긋나게 두면 — $w$와 같은 단위의 어긋남이고, 위의 깊이 $d_i$가 아니다 — 겹치는 띠의 폭은 $w-d$이고 둘을 합친 폭은 $w+d$이며 높이는 약분되므로

$$\mathrm{IoU}=\frac{w-d}{w+d}\ge t\quad\Longleftrightarrow\quad d\le w\,\frac{1-t}{1+t}.$$

PASCAL의 $t=0.5$에서는 $d\le w/3$이다. 박스가 자기 폭의 3분의 1만큼 미끄러져도 여전히 맞힌 것으로 센다. 3.5의 카메라($f=600$ px)가 $2$ m 떨어진 패널을 보면 픽셀 하나가 $2000/600=3.33$ mm다. 거기서 폭 $100$ px인 박스는 $33.3$ px, 곧 $111$ mm를 미끄러져도 참양성이다. 건설 트랙의 외장 패널 과제 S1([[05-construction-robotics/site-engineering|2.5]])은 구멍 둘을 $\pm5$ mm 안에 맞추는데, 이 거리에서 그것은 $1.5$ px이고 $\mathrm{IoU}\ge(100-1.5)/(100+1.5)=0.970$이 필요하다. COCO 사다리의 어느 칸보다도 높다. IoU는 정의상 척도 무관이므로(§2의 상자) 어떤 IoU 임계값도 밀리미터 단위의 허용오차를 보증하지 못한다. 그것은 3.5의 기하와 로봇 좌표계에서 잰 오차가 할 일이다.

### 4. 계보 읽기

backbone의 이름은 결과가 왜 나오는지를 거의 말해 주지 않으므로, 계보는 어느 backbone이 더 새로운지가 아니라 논문마다 어떤 supervision과 pretraining을 썼고 무엇이 전이됐는지를 보려고 읽는다. [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]과 [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]에서 학습된 계층 표현과 최적화를, [[01-canonical-papers/notes/1-foundations/vit|ViT]]에서 patch token을 읽고, [[01-canonical-papers/canonical-list|canonical list]]의 검출·분할·3D 항목으로 간다.

### 5. 실습: 공식, 임계값, 그리고 평균

고정된 같은 D2에서 sweep 셋, 각각이 논문의 방법이 건드리지 않는 손잡이다. 코드 1부는 아홉 가지 설정에서 실제로 창을 밀어 출력 크기 공식을 검산한다. 2부는 COCO 사다리를 따라 IoU 임계값을 훑는다. 3부는 pixel accuracy 보고로는 구별할 수 없는 분할 둘을 채점한다.

**Sweep 1 — 공식 대 실제 창.** "비0 칸"은 모서리를 본 출력 칸의 수이고, 맵은 $n_{\text{out}}\times n_{\text{out}}$이다.

| $k$ | $s$ | $p$ | 공식 | NumPy | 최대 | 최소 | 비0 칸 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 0 | 6 | 6 | $40$ | $0$ | 12 |
| 3 | 1 | 1 | 8 | 8 | $40$ | $-40$ | 24 |
| 3 | 2 | 0 | 3 | 3 | $40$ | $0$ | 3 |
| 3 | 2 | 1 | 4 | 4 | $40$ | $0$ | 4 |
| 3 | 3 | 0 | 2 | 2 | $40$ | $0$ | 2 |
| 3 | 3 | 1 | 3 | 3 | $40$ | $0$ | 3 |
| 3 | 4 | 0 | 2 | 2 | $0$ | $0$ | 0 |
| 5 | 1 | 0 | 4 | 4 | $150$ | $50$ | 16 |
| 5 | 1 | 2 | 8 | 8 | $150$ | $-150$ | 48 |

**Sweep 2 — IoU 임계값.** TP/FP 표시 $(1,0,1)$로 $\mathrm{AP}(0.5)=0.833333$, 표시 $(1,0,0)$으로 $\mathrm{AP}(0.75)=0.500000$이다. COCO 사다리 $t=0.50,0.55,\dots,0.95$에서 AP는 $0.8333$이 세 번, 그다음 $0.5$가 일곱 번이므로 $\mathrm{mAP}@[.5{:}.95]=(3\cdot0.8333+7\cdot0.5)/10=0.600000$이다. COCO의 공식 평가기는 보간한 곡선을 적분하지 않고 고르게 나눈 재현율 101곳에서 읽으므로, 두 값은 $0.834983$과 $0.504950$, 평균은 $0.603960$이 된다. 첫 관례 안에 숨은 두 번째 관례이고, 23포인트 간극은 그대로다.

<svg viewBox="0 0 560 360" style="max-width:100%;height:auto" role="img" aria-label="D2의 순위 매긴 박스 셋의 정밀도–재현율 곡선. (a) IoU 임계값 0.5에서 표시는 TP, FP, TP이고 점 (R, P) = (0.5, 1), (0.5, 0.5), (1, 0.667), 보간 외곽선이 감싸는 넓이가 AP = 0.833. (b) 0.75에서는 세 번째 박스가 탈락해 재현율이 0.5에서 멈추고 AP = 0.5. (c) COCO 사다리 t = 0.50–0.95의 AP: 0.833이 세 번, 0.5가 일곱 번, 평균 0.600.">
  <text x="12" y="18" font-size="12" fill="currentColor">(a) 임계값 t = 0.5</text>
  <path d="M 52.0 194.0 L 52.0 44.0 L 152.0 44.0 L 152.0 94.0 L 252.0 94.0 L 252.0 194.0 L 252.0 194.0 Z" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <polyline points="52.0,44.0 152.0,44.0 152.0,94.0 252.0,94.0 252.0,194.0" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="52" y1="194" x2="258" y2="194" stroke="currentColor" stroke-width="1"/>
  <line x1="52" y1="194" x2="52" y2="38" stroke="currentColor" stroke-width="1"/>
  <line x1="52.0" y1="194" x2="52.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="52.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="48" y1="194.0" x2="52" y2="194.0" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="197.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="152.0" y1="194" x2="152.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="152.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <line x1="48" y1="119.0" x2="52" y2="119.0" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="122.5" font-size="10" fill="currentColor" text-anchor="end">0.5</text>
  <line x1="252.0" y1="194" x2="252.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="252.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="48" y1="44.0" x2="52" y2="44.0" stroke="currentColor" stroke-width="1"/>
  <text x="45" y="47.5" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <text x="258" y="209" font-size="10.5" fill="currentColor" text-anchor="end">재현율 R</text>
  <text x="57" y="36" font-size="10.5" fill="currentColor">정밀도 P</text>
  <circle cx="152.0" cy="44.0" r="3.2" fill="currentColor"/>
  <circle cx="152.0" cy="119.0" r="3.2" fill="currentColor"/>
  <circle cx="252.0" cy="94.0" r="3.2" fill="currentColor"/>
  <text x="159.0" y="55.0" font-size="10.5" fill="currentColor">1 · P<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3">참양성</tspan></text>
  <text x="159.0" y="123.0" font-size="10.5" fill="currentColor">2 · P<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3">거짓양성</tspan></text>
  <text x="246.0" y="87.0" font-size="10.5" fill="currentColor" text-anchor="end">3 · P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3">참양성</tspan></text>
  <text x="152.0" y="173.0" font-size="10.5" fill="currentColor" text-anchor="middle">AP = 0.5·1 + 0.5·0.667 = 0.833</text>
  <text x="282" y="18" font-size="12" fill="currentColor">(b) 임계값 t = 0.75</text>
  <path d="M 322.0 194.0 L 322.0 44.0 L 422.0 44.0 L 422.0 194.0 L 422.0 194.0 Z" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <polyline points="322.0,44.0 422.0,44.0 422.0,194.0" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="322" y1="194" x2="528" y2="194" stroke="currentColor" stroke-width="1"/>
  <line x1="322" y1="194" x2="322" y2="38" stroke="currentColor" stroke-width="1"/>
  <line x1="322.0" y1="194" x2="322.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="322.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="318" y1="194.0" x2="322" y2="194.0" stroke="currentColor" stroke-width="1"/>
  <text x="315" y="197.5" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="422.0" y1="194" x2="422.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="422.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <line x1="318" y1="119.0" x2="322" y2="119.0" stroke="currentColor" stroke-width="1"/>
  <text x="315" y="122.5" font-size="10" fill="currentColor" text-anchor="end">0.5</text>
  <line x1="522.0" y1="194" x2="522.0" y2="198" stroke="currentColor" stroke-width="1"/>
  <text x="522.0" y="209" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="318" y1="44.0" x2="322" y2="44.0" stroke="currentColor" stroke-width="1"/>
  <text x="315" y="47.5" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <text x="528" y="209" font-size="10.5" fill="currentColor" text-anchor="end">재현율 R</text>
  <text x="327" y="36" font-size="10.5" fill="currentColor">정밀도 P</text>
  <circle cx="422.0" cy="44.0" r="3.2" fill="currentColor"/>
  <circle cx="422.0" cy="119.0" r="3.2" fill="currentColor"/>
  <circle cx="422.0" cy="144.0" r="3.2" fill="currentColor"/>
  <text x="429.0" y="55.0" font-size="10.5" fill="currentColor">1 · P<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3">참양성</tspan></text>
  <text x="429.0" y="123.0" font-size="10.5" fill="currentColor">2 · P<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3">거짓양성</tspan></text>
  <text x="429.0" y="148.0" font-size="10.5" fill="currentColor">3 · P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3">거짓양성</tspan></text>
  <text x="429.0" y="161.0" font-size="10.5" fill="currentColor">IoU 0.6 &lt; 0.75</text>
  <text x="372.0" y="173.0" font-size="10.5" fill="currentColor" text-anchor="middle">AP = 0.5·1 = 0.5</text>
  <text x="429.0" y="175.0" font-size="10.5" fill="currentColor">재현율이 0.5에서 멈춤</text>
  <text x="12" y="226" font-size="10.5" fill="currentColor" fill-opacity="0.85">점: 순위대로 박스를 더할 때의 P와 R · 실선: 보간 외곽선 · 음영: 그 넓이, 곧 AP</text>
  <text x="12" y="252" font-size="12" fill="currentColor">(c) COCO 사다리를 따라 본 AP(t)와 그 평균</text>
  <rect x="61.0" y="280.3" width="30" height="41.7" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="76.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.833</text>
  <text x="76.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.50</text>
  <rect x="109.0" y="280.3" width="30" height="41.7" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="124.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.833</text>
  <text x="124.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.55</text>
  <rect x="157.0" y="280.3" width="30" height="41.7" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="172.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.833</text>
  <text x="172.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.60</text>
  <rect x="205.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="220.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="220.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.65</text>
  <rect x="253.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="268.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="268.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.70</text>
  <rect x="301.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="316.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="316.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.75</text>
  <rect x="349.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="364.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="364.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.80</text>
  <rect x="397.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="412.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="412.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.85</text>
  <rect x="445.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="460.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="460.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.90</text>
  <rect x="493.0" y="297.0" width="30" height="25.0" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="508.0" y="318.0" font-size="10" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="508.0" y="336" font-size="10" fill="currentColor" text-anchor="middle">0.95</text>
  <line x1="52" y1="322" x2="532" y2="322" stroke="currentColor" stroke-width="1"/>
  <line x1="52" y1="292.0" x2="532" y2="292.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3"/>
  <text x="532" y="288.0" font-size="10.5" fill="currentColor" text-anchor="end">평균 0.600</text>
  <line x1="196" y1="264" x2="196" y2="322" stroke="currentColor" stroke-width="1" stroke-dasharray="1 2"/>
  <text x="200" y="270" font-size="10.5" fill="currentColor">계단은 P<tspan dy="3" font-size="10">3</tspan><tspan dy="-3">의 IoU 0.6에 있다</tspan></text>
  <text x="292" y="352" font-size="10.5" fill="currentColor" text-anchor="middle">IoU 임계값 t</text>
</svg>

신뢰도 순으로 세운 D2의 예측 셋, $P_1$($0.90$), $P_2$($0.80$), $P_3$($0.60$)을 정밀도–재현율 점으로 그린 것이다. (a) $t=0.5$에서 표시는 참양성, 거짓양성, 참양성이고, 보간 외곽선이 감싸는 넓이가 $\mathrm{AP}=0.5\cdot1+0.5\cdot0.667=0.833$이다. (b) $t=0.75$에서는 $P_3$의 겹침 $0.6$이 탈락해 재현율이 $0.5$에서 멈추고 $\mathrm{AP}=0.5$다. (c) COCO 사다리를 따라 AP는 $t=0.60$까지 $0.833$, $0.65$부터 $0.5$이고 — 계단은 $P_3$의 IoU $0.6$에 있다 — 평균은 $0.600$이다.

**Sweep 3 — 평균의 단위.**

| 예측 | 배경 IoU | 케이블 IoU | mIoU | pixel accuracy |
|---|---:|---:|---:|---:|
| A: 전부 배경 | $0.875000$ | $0.000000$ | $0.437500$ | $0.875000$ |
| B: 케이블 두 열 | $0.857143$ | $0.500000$ | $0.678571$ | $0.875000$ |

**Sweep 읽기.** 공식만으로는 알 수 없었던 것 다섯.

- **공식은 정확하고, floor는 픽셀이 사라지는 자리다.** 아홉 행이 모두 NumPy와 맞는다. 재미있는 것은 $(k,s,p)=(3,2,0)$과 $(3,3,0)$으로, $\lfloor5/2\rfloor+1=3$, $\lfloor5/3\rfloor+1=2$다. 마지막 한 열과 두 열은 어떤 창도 덮지 않는다. 오류는 나지 않고 feature map만 머릿속 계산보다 작아진다.
- **커널보다 넓은 stride는 신호 전체를 놓칠 수 있다.** $(3,4,0)$의 출력은 합법적인 $2\times2$짜리 0의 맵이다. 창 둘이 0열과 4열에서 시작해 각각 *일정한* 패치만 본다. 0–2열은 전부 어둡고 4–6열은 전부 밝아서 어느 쪽도 모서리를 걸치지 않는다. 이미지에는 특징이 하나뿐인데 층은 아무것도 보고하지 않는다. $s>k$이면 언제나 틈이 생기고, D2의 모서리가 그 틈에 빠진다.
- **Zero padding은 없던 모서리를 만든다.** $(3,1,1)$의 최소가 $-40$이다. padding된 맵의 오른쪽 열이 밝은 픽셀을 이미지 밖에 발명된 0과 비교해, 진짜 모서리만큼 강한 응답을 낸다. 맨 위와 맨 아래 행에서는 0이 아닌 세 열 — 진짜 모서리의 3열과 4열, 만들어진 7열 — 이 $\pm40$이 아니라 $30$과 $-30$인데, 위나 아래에 padding한 0의 행이 기여 행 셋 중 하나를 없애기 때문이다. 경계 인공물은 padding의 버그가 아니라 "same" padding의 비용이다.
- **Headline을 움직이는 것은 검출기가 아니라 임계값이다.** $P_3$는 전혀 바뀌지 않는다. $G_2$와 늘 $0.6$만큼 겹친다. $\mathrm{AP}@0.5=0.833$을 보고하든 $\mathrm{mAP}@[.5{:}.95]=0.600$을 보고하든 같은 박스 셋을 서술하는 것이고, 23포인트의 간극은 박스 하나의 위치 정확도를 두 관례로 본 것이다. $P_2$는 사다리의 모든 임계값에서 거짓양성인데, $0.391$이 $0.5$에 끝내 닿지 않기 때문이다. 보기에 "거의 맞는" 검출이 0점일 수 있다.
- **Pixel accuracy는 케이블을 보지 못하고 mIoU는 본다.** 예측 A와 B의 pixel accuracy는 *같은* $0.875$이고 mIoU는 $0.4375$ 대 $0.678571$이다. B는 진짜 개선이다. 케이블을 찾았고 한 열만큼 넘겨 칠했다. 그리고 클래스 평균 metric만 그것을 기록한다. B가 케이블을 맞히자 배경 IoU는 오히려 $0.875$에서 $0.857143$으로 *떨어진다*. 그것이 거래의 정직한 비용이고, 두 숫자를 클래스별로 보고해야 하는 이유다.

### 스스로 점검 · Self-check

1. D2에 $3\times3$, stride 1, padding 1, 입력 1채널, 출력 4채널 convolution의 출력 크기와 parameter 수는? 둘 중 이미지 크기에 의존하는 것은 어느 쪽인가.
2. D2의 패치 토큰 넷에는 서로 다른 벡터가 둘뿐이다. 위치 임베딩을 빼면 무엇이 깨지고, convolution은 왜 이 문제를 겪지 않는가.
3. 검출기의 박스가 정답과 $\mathrm{IoU}=0.6$으로 겹친다. 참양성인가.
4. pixel accuracy가 같은 두 분할의 mIoU가 $0.44$와 $0.68$이다. 두 번째가 찾아낸 클래스에 대해 무엇이 참이어야 하는가.
5. depth 논문이 $\mathrm{AbsRel}=0.10$을 보고하고 정렬을 언급하지 않았다. 확립되지 않은 것은 무엇인가.

> [!tip]- 정답 · Answers
> 1. $\lfloor(8+2-3)/1\rfloor+1=8$이므로 $8\times8\times4$, parameter는 $4(1\cdot9+1)=40$개다. $n$에 의존하는 것은 출력 크기뿐이다. parameter 수는 $C_{\text{out}}(C_{\text{in}}k^2+1)$로 $n$을 포함하지 않고, 그것이 weight sharing의 요점이다.
> 2. self-attention은 순열 등변이라 서로 다른 위치의 같은 토큰을 구별할 수 없고, 모델은 왼쪽 위와 왼쪽 아래를, 그리고 D2와 그 거울상을 가르지 못한다. convolution은 출력 격자 자체가 배치라서 위치를 따로 더할 일이 없다.
> 3. 질문만으로는 답할 수 없다. $t=0.5$에서는 참양성, $t=0.75$에서는 거짓양성이고, 임계값은 검출기가 아니라 protocol에 속한다. 그리고 그 정답 물체를 더 높은 신뢰도의 검출이 이미 차지하지 않았을 때만 참양성이다.
> 4. 틀려도 픽셀 비용이 거의 없을 만큼 작은 클래스여야 한다. D2의 케이블은 64픽셀 중 8픽셀이다. 개선을 보이게 하는 것은 mIoU의 균등한 클래스 가중이고, pixel accuracy는 픽셀 수로 가중하므로 보지 못한다.
> 5. 그 숫자가 metric depth를 가리키는지 자체가 확립되지 않았다. 척도 모호한 방법은 AbsRel을 재기 전에 이미지마다 정답에 정렬되므로 결과는 상대적 형태를 재고, 미터와 그에 따른 조작·주행 주장은 뒷받침되지 않는다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[03-deep-learning/lab-objects|0. Lab Objects]]만 쓴다. D2의 픽셀·박스·마스크는 대상 절에 고정되어 있다. 문제 1과 3은 창과 박스 쌍과 거리를 옮기고, 문제 4는 커널과 박스 하나와 마스크 하나를 바꾸므로 페이지의 숫자를 그대로 옮길 수 없다.

1. **그리기.** 그림의 세 칸을 다른 창, 다른 박스 쌍, 다른 마스크로 그린다. (a) 출력 칸 $(0,4)$를 만드는 $3\times3$ 창과 그 값, 그리고 $6\times6$ 맵 위의 그 칸, (b) 모서리 좌표로 그린 $P_2$와 $G_2$, 그 교집합 직사각형과 넓이와 IoU, (c) §5의 예측 B(케이블 두 열)를 개수로, 곧 클래스마다 교집합과 합집합.
2. **유도.** $3\times3$, stride 2, padding 1, 출력 channel 8개의 크기와 parameter 수를 구한다.
3. **해석.** 3.5의 카메라($f=600$ px)가 $400$ mm 떨어진 S1의 설치 구멍 둘을 $1.2$ m에서 보고, 검출기가 그 쌍을 박스 하나로 둘러싼다. (a) 그 박스는 몇 픽셀 폭이고, $t=0.5$에서 여전히 맞힌 것으로 세려면 옆으로 몇 픽셀, 몇 밀리미터까지 미끄러질 수 있는가. (b) COCO 사다리의 가장 엄한 칸 $t=0.95$에서는 어떤가. (c) S1의 $\pm5$ mm에는 어떤 IoU가 필요하고, 그 값은 왜 거리에 의존하지 않는가.
4. **실행.** 영어 절 템플릿의 `?`를 채우고 변형 셋을 돌려 각각 작은 표로 보고한다. (a1) $5\times5$ 수직 모서리 커널 `K5`로 $(k,s,p)$를 $(5,1,0)$, $(5,1,2)$, $(5,2,0)$, $(5,2,2)$, $(5,3,0)$으로 훑으며 매번 공식을 검산한다. (a2) $K$를 전치한 *수평* 모서리 커널 `Ky`로 바꿔 $3\times3$에서 $p=0$과 $p=1$로 돌리고, padding한 맵의 맨 위와 맨 아래 행을 찍은 뒤, 그 응답이 어디서 오는지 한 문장으로 쓴다. (b) $P_3$를 정확히 맞는 $(4,4,8,8)$로 옮기고 $\mathrm{AP}(0.5)$, $\mathrm{AP}(0.75)$, $\mathrm{mAP}@[.5{:}.95]$를 다시 구한다. (c) 케이블을 4열이 아니라 3열에 둔 세 번째 분할을 채점하고, 그 케이블 IoU가 왜 그 값인지 말한다.

> [!note]- 그리는 법 · How to draw it
> - 패치 격자는 픽셀 옆이 아니라 픽셀 위에 그리고, 계단 모서리를 세로 격자선 위에 둔다. $(0,4)$의 창이 일정한 패치 위에 놓이는 이유가 그것이다.
> - convolution 창은 픽셀 위의 $3\times3$ 정사각형 하나로 그리고, 출력 칸은 따로 그린 $n_{\text{out}}\times n_{\text{out}}$ 격자 위에 표시한다. 정사각형 하나, 칸 하나, 화살표 하나다. 창의 픽셀 값을 옆에 적어 그 출력을 검산할 수 있게 한다.
> - 박스는 대충 그린 사각형이 아니라 좌표가 적힌 모서리로 그린다. IoU는 좌표의 $\max$와 $\min$에서 나오고, 모서리가 적히지 않은 사각형은 검산할 수 없다.
> - 교집합 직사각형을 넓이와 함께 명시한다. 합집합이 필요로 하는 유일한 부분이 그것이다.
> - 마스크 패널은 음영이 아니라 개수로, 클래스마다 교집합과 합집합을 적는다. 여기의 모든 분할 metric은 정수 둘의 비이고, §5에서 metric들이 엇갈리는 이유는 그 정수가 종이 위에 있을 때만 보인다.

> [!tip]- 정답 · Solutions
> 1. (a) 창은 0–2행, 4–6열을 덮고 모두 밝으므로 행마다 $(10,10,10)$이고 $y_{0,4}=(-1+0+1)\cdot10+(-2+0+2)\cdot10+(-1+0+1)\cdot10=0$이다. 성분의 합이 0인 커널은 밝든 어둡든 일정한 패치에서 $0$을 낸다. (b) $P_2=(3,3,7,7)$과 $G_2=(4,4,8,8)$은 $x\in[4,7]$, $y\in[4,7]$에서 만나 넓이 $9$인 $3\times3$ 정사각형이 되므로 $\mathrm{IoU}=9/(16+16-9)=9/23=0.391304$다. §5에서 모든 임계값에서 거짓양성인 박스다. (c) 케이블은 교집합 $8$, 합집합 $16$, IoU $0.5$이고, 배경은 교집합 $48$, 합집합 $56$, IoU $0.857143$이며, 둘의 평균이 B의 mIoU $0.678571$이다.
> 2. $\lfloor(8+2-3)/2\rfloor+1=4$이므로 출력은 $4\times4\times8$이고, parameter는 $8(3\cdot3+1)=80$개다.
> 3. (a) 그 거리에서 픽셀 하나는 $1200/600=2$ mm이므로 박스 폭은 $400/2=200$ px이고, $d\le w/3=66.7$ px, 곧 $133$ mm다. (b) $d\le w(1-t)/(1+t)=200\cdot0.05/1.95=5.13$ px, $10.3$ mm로, 사다리의 가장 엄한 칸에서도 S1 허용오차의 두 배다. (c) $5$ mm는 $2.5$ px이므로 $\mathrm{IoU}\ge(200-2.5)/(200+2.5)=0.975$다. 밀리미터로 쓰면 픽셀이 약분되어 $\mathrm{IoU}\ge(W-\delta)/(W+\delta)$, $W=400$ mm, $\delta=5$ mm가 된다. IoU가 척도 무관이기 때문이다. 거리가 바꾸는 것은 $5$ mm가 몇 픽셀이냐 — 여기서 $2.5$ px, §3의 $2$ m에서 $1.5$ px — 뿐이고, 그것이 검출기가 가려내야 할 크기다. 벤치마크 IoU는 S1의 정렬을 보증하지 못하고, 3.5의 기하를 거쳐 밀리미터로 잰 오차가 보증할 수 있다.
> 4. 빈칸은 `Ky = Kx.T`, `n_out = (8 + 2*p - k)//s + 1`, `Yp`의 padding `1`, `(4, 4, 8, 8)`, `predC[:, 3] = 1`이다.
>
>    (a1) 모든 설정에서 공식과 NumPy가 맞고, $5\times5$ 커널은 모서리 하나를 네 열에 번지게 한다.
>
>    | $k$ | $s$ | $p$ | 공식 = NumPy | 최대 | 최소 |
>    |---:|---:|---:|---:|---:|---:|
>    | 5 | 1 | 0 | 4 | $150$ | $50$ |
>    | 5 | 1 | 2 | 8 | $150$ | $-150$ |
>    | 5 | 2 | 0 | 2 | $150$ | $50$ |
>    | 5 | 2 | 2 | 4 | $150$ | $-50$ |
>    | 5 | 3 | 0 | 2 | $50$ | $50$ |
>
>    padding 없는 행은 0에 닿지 않는다. 폭 5의 유효한 창이 모두 모서리를 걸치므로, 폭 $8$짜리 이미지에서 넓은 커널에는 "조용한" 위치가 없다.
>
>    (a2) $p=0$에서 `Ky`는 어디서나 최대 $0$, 최소 $0$을 낸다. D2는 모든 열에서 일정하므로 행에서 행으로의 변화를 보는 검출기에는 아무것도 없고, 0으로 채워진 feature map은 층에 대한 증거가 아니라 이미지에 대한 증거다. $p=1$에서는 맵이 $8\times8$이고 맨 위 행이 $(0,0,0,10,30,40,40,30)$, 맨 아래 행이 그 부호를 바꾼 값, 그 사이는 0이다. 0행 위와 7행 아래에 padding한 0의 행이 이미지에 없는 수평 모서리가 되고, 밝은 열 아래에서 가장 강하다. padding은 없던 모서리를 만든다 — §5의 세 번째 읽기를 옆으로 돌린 것이다.
>
>    (b) $P_3=(4,4,8,8)$이면 $G_2$와의 IoU가 $1.0$이라 사다리의 모든 임계값에서 표시가 $(1,0,1)$이다. 따라서 $\mathrm{AP}(0.5)=\mathrm{AP}(0.75)=\mathrm{mAP}@[.5{:}.95]=0.833333$이다. §5의 COCO 간극이 완전히 사라지므로 그것이 순위 간극이 아니라 위치 간극이었음이 확인된다. 거짓양성 $P_2$는 그대로 남아 같은 precision을 계속 깎는다.
>
>    (c) 케이블을 3열에 두면 $\mathrm{IoU}_{\text{cable}}=0/(8+8)=0$, $\mathrm{IoU}_{\text{bg}}=48/64=0.750000$, $\mathrm{mIoU}=0.375000$, pixel accuracy $0.750000$이다. 한 열 너비 물체를 한 열 옮기면 교집합이 *없으므로* IoU는 부분 점수를 전혀 주지 않는다. (적어도 겹쳤던) 예측 B의 $0.5$에서 $0$으로 떨어져, 아무것도 예측하지 않은 것보다 나쁜 점수가 된다. 얇은 구조에서 IoU는 거의 이진이고, 안전이 걸린 얇은 물체 평가가 거리 기반이나 팽창 기준을 쓰는 이유다.

### 출처 · Sources

- A. Krizhevsky, I. Sutskever & G. E. Hinton, "ImageNet classification with deep convolutional neural networks," *NeurIPS* 2012([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet 노트]]).
- K. He, X. Zhang, S. Ren & J. Sun, "Deep residual learning for image recognition," *CVPR* 2016([[01-canonical-papers/notes/1-foundations/resnet|ResNet 노트]]).
- A. Dosovitskiy et al., "An image is worth 16x16 words: Transformers for image recognition at scale," *ICLR* 2021 — §1의 패치 토큰, class 토큰, 귀납 편향 논증([[01-canonical-papers/notes/1-foundations/vit|ViT 노트]]).
- M. Everingham, L. Van Gool, C. K. I. Williams, J. Winn & A. Zisserman, "The PASCAL Visual Object Classes (VOC) challenge," *International Journal of Computer Vision* 88(2):303–338 (2010) — $0.5$ 겹침 기준과 average precision.
- COCO Consortium, [`cocoeval.py`](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py), 공식 평가 코드 — $0.50$부터 $0.95$까지 $0.05$ 간격의 IoU 임계값과 §5의 재현율 101곳.
- H. Rezatofighi, N. Tsoi, J. Gwak, A. Sadeghian, I. Reid & S. Savarese, "Generalized intersection over union: A metric and a loss for bounding box regression," *CVPR* 2019 — §2 IoU 상자의 GIoU.
- D2의 픽셀·박스·마스크는 이 페이지에 고정한 교육용 대상이다([[03-deep-learning/lab-objects|0. Lab Objects]]). 모든 숫자는 손으로 또는 §5의 코드로 여기서 계산했다.
