---
title: 3. Vision–Language Models
tags: [deep-learning, vlm, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Distinguish contrastive alignment, fusion, and generation; compute a contrastive batch; and bound what language-grounded evidence proves."
mastery-when: "Raise when multimodal grounding, representation, or language-conditioned perception is modified in the thesis."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/foundations/index|1. Learning Systems §1–§2]] (softmax, cross-entropy and $p-y$), [[03-deep-learning/computer-vision/index|2. Computer Vision]], [[02-foundations/information-theory|5. Information Theory]], and [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|the Transformer note]]. Object **D3**, three frozen image–caption pairs, from [[03-deep-learning/lab-objects|0. Lab Objects]]; the Tier A lab in §5 needs NumPy and nothing else.
> [[03-deep-learning/foundations/index|1. 학습 시스템 §1–§2]](softmax, cross-entropy, $p-y$), [[03-deep-learning/computer-vision/index|2. 컴퓨터비전]], [[02-foundations/information-theory|5. 정보이론]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]. 대상은 [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D3**(고정된 이미지–캡션 3쌍)이고, §5의 Tier A 실습에는 NumPy만 있으면 된다.

## English

> [!note] Why this matters · 왜 배우는가
> In the physical-AI stack of [[07-research-program/index|7. Research Program §5]] this page belongs to the learning-and-adaptation layer, as the "VLM or VLA reasoning" box that opens the stack's language-driven form, and in *"install that panel on the frame"* it serves step 1, *resolve the instruction*: "that panel" has to be tied to something in the image before step 2 can identify it (its chip sits in the learning-and-adaptation band of the [[physical-ai-map|Physical AI Map]]). Without it a vision–language number is easy to over-read: D3, the track's three frozen image–caption pairs ([[03-deep-learning/lab-objects|0. Lab Objects]]), is a batch its encoder has already solved perfectly, yet its loss runs from $0.933538$ down to $0.000001$ on the temperature alone (§5); a success detector that fires above one half calls a perfect match a failure at $\tau=1/2$, where $p=0.468861$, and a success at $\tau=1/4$, where $p=0.581234$, with nothing in the scene changed (§4); and a correct "red valve" says nothing about whether the valve's pixels were used (§3). Later pages stand on it: [[03-deep-learning/vla/index|4. VLA]] puts an action head on this backbone and, in its §6, prices the backbone's rate; a VLM success check is the kind of binary reward [[02-foundations/rl-robot-learning|7.5 RL for Robot Learning §8]] trains on; and on the dissertation path ([[07-research-program/index|7. Research Program §8]]) the page is the third of block 4's four deep-learning pages, deep-learning sessions 35–38. After it you can compute a contrastive batch by hand, say what its number certifies — at most $\log N$ nats — and tell conditioning from grounding in a paper's claim.

> [!note] First pass · 처음이라면
> About four sessions of 60–90 minutes, rows 35–38 of the [[03-deep-learning/index|deep-learning schedule]]; the first two are the first pass. **Session 1:** D3 and the picture, then the Worked case by hand with the solution covered — nine dot products, three row losses, and $\mathcal L=0.602352$ nats against $\log3=1.098612$. **Session 2:** §1–§4, self-checks 1–5 and problems 1–3. **Session 3:** the §5 lab and problem 4. **Session 4:** §6 and self-check 6; its collapsed note on the omni models is second-pass reading. Finish by saying in two sentences what a contrastive loss certifies — at most $\log N$ nats of mutual information — and what it does not: that an answer is grounded in the pixels.

### Running object: D3

**D3** from [[03-deep-learning/lab-objects|0. Lab Objects]] is three matched image–caption pairs with frozen unit embeddings and $\tau=1/2$:

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix}.$$

Similarity logits are $\ell_{ij}=v_i^\top t_j/\tau$: row $i$ is image $i$'s logit vector, the $s$ of [[03-deep-learning/foundations/index|1. Learning Systems]], with the batch's $N$ captions as its classes ($N=3$ on D3). Rows ask “which text matches this image?”; columns ask the reverse.

Everything on this page follows from those six vectors and one knob. All are unit length, so each dot product is the cosine of the angle between two of them, and the three images sit at $0^\circ$, $60^\circ$ and $90^\circ$. Matched pairs are *exactly* aligned — this is a batch the encoder has already solved — so the only thing that can go wrong on D3 is the objective itself, which is what makes it the right object for reading a contrastive loss. Two page-local variants are frozen here for §5 and the problem set, changing one vector each. **The one-wrong batch** moves image 2 to $v_2'=(0,1)$, i.e. to $90^\circ$, so the encoder now places it on top of caption 3. **The duplicate-caption batch** sets $t_3=t_2$, so captions 2 and 3 are the same sentence and the "negative" in row 2 is a correct match.

*Scope: this page teaches the contrastive objective of a dual encoder — the similarity matrix, the two directions, the temperature, the negatives, and what the resulting number does and does not certify — and the vocabulary that separates conditioning from grounding. It does not teach the image encoder, which is [[03-deep-learning/computer-vision/index|2. Computer Vision §1]]; nor the cross-attention that fusion models use — each text token weighting the image patches and reading their weighted sum — which is [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer §1]], off the dissertation path, and the [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer note]]; nor the loss and optimizer machinery around the objective, which is [[03-deep-learning/foundations/index|1. Learning Systems §1–§2]] and its §6 lab; nor generative decoding, captioning metrics, or action, which are the generative entries of the [[01-canonical-papers/canonical-list|canonical list]] and the [[03-deep-learning/vla/index|VLA course]] — §6 only places those larger models by where their modalities meet. The retrieval metrics named in §3 are defined in [[02-foundations/ml-practice|9. ML Practice §3]].*

### The picture

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="D3's two encoders feed a 3 by 3 cosine matrix, dividing every cell by tau = 1/2 gives the one logit matrix with its diagonal marked as positives inside a batch box, and that matrix is read along rows and along columns, each giving losses 0.407606, 0.757448, 0.642002 and the objective 0.602352 nats">
  <defs><marker id="aD3e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="38" font-size="11" fill="currentColor">3 images</text>
  <line x1="78" y1="34" x2="90" y2="34" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3e)"/>
  <rect x="92" y="23" width="90" height="22" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="137" y="38" font-size="11" fill="currentColor" text-anchor="middle">image encoder</text>
  <line x1="137" y1="45" x2="137" y2="51" stroke="currentColor" stroke-width="1.2"/>
  <text x="137" y="63" font-size="11" fill="currentColor" text-anchor="middle">v<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, v</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">, v</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· unit</tspan></text>
  <text x="12" y="88" font-size="11" fill="currentColor">3 captions</text>
  <line x1="78" y1="84" x2="90" y2="84" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3e)"/>
  <rect x="92" y="73" width="90" height="22" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="137" y="88" font-size="11" fill="currentColor" text-anchor="middle">text encoder</text>
  <line x1="137" y1="95" x2="137" y2="101" stroke="currentColor" stroke-width="1.2"/>
  <text x="137" y="113" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, t</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">, t</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· unit</tspan></text>
  <text x="137" y="132" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">at 0°, 60°, 90°</text>
  <text x="430" y="71" font-size="11" fill="currentColor" fill-opacity="0.85">V T<tspan dy="-4" font-size="10">T</tspan><tspan dy="4">: cosines</tspan></text>
  <text x="267" y="35" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">t<tspan dy="3" font-size="10">1</tspan></text>
  <text x="329" y="35" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">t<tspan dy="3" font-size="10">2</tspan></text>
  <text x="391" y="35" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">t<tspan dy="3" font-size="10">3</tspan></text>
  <text x="230" y="53" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">v<tspan dy="3" font-size="10">1</tspan></text>
  <text x="267" y="53" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <text x="329" y="53" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <text x="391" y="53" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <text x="230" y="71" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">v<tspan dy="3" font-size="10">2</tspan></text>
  <text x="267" y="71" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <text x="329" y="71" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <text x="391" y="71" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.866025</text>
  <text x="230" y="89" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">v<tspan dy="3" font-size="10">3</tspan></text>
  <text x="267" y="89" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <text x="329" y="89" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.866025</text>
  <text x="391" y="89" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <rect x="236" y="40" width="186" height="54" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.6"/>
  <line x1="198" y1="67" x2="212" y2="58" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3e)"/>
  <line x1="198" y1="117" x2="212" y2="78" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3e)"/>
  <line x1="329" y1="97" x2="329" y2="146" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD3e)"/>
  <text x="337" y="124" font-size="11" fill="currentColor">÷ τ, τ = 1/2, on all nine cells</text>
  <rect x="236" y="170" width="62" height="26" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <rect x="298" y="196" width="62" height="26" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <rect x="360" y="222" width="62" height="26" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <line x1="298" y1="170" x2="298" y2="248" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <line x1="236" y1="196" x2="422" y2="196" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <line x1="360" y1="170" x2="360" y2="248" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <line x1="236" y1="222" x2="422" y2="222" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <text x="267" y="157" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">1</tspan></text>
  <text x="329" y="157" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">2</tspan></text>
  <text x="391" y="157" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">3</tspan></text>
  <text x="227" y="187" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">1</tspan></text>
  <text x="267" y="188" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <text x="329" y="188" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <text x="391" y="188" font-size="12" fill="currentColor" text-anchor="middle">0</text>
  <text x="227" y="213" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">2</tspan></text>
  <text x="267" y="214" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <text x="329" y="214" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <text x="391" y="214" font-size="12" fill="currentColor" text-anchor="middle">1.732051</text>
  <text x="227" y="239" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">3</tspan></text>
  <text x="267" y="240" font-size="12" fill="currentColor" text-anchor="middle">0</text>
  <text x="329" y="240" font-size="12" fill="currentColor" text-anchor="middle">1.732051</text>
  <text x="391" y="240" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <text x="12" y="182" font-size="11" fill="currentColor">ℓ<tspan dy="3" font-size="10">ij</tspan><tspan dy="-3" dx="3.5">= v</tspan><tspan dy="3" font-size="10">i</tspan><tspan dy="-7" font-size="10">T</tspan><tspan dy="4">t</tspan><tspan dy="3" font-size="10">j</tspan><tspan dy="-3" dx="3.5">/ τ</tspan></text>
  <text x="12" y="208" font-size="11" fill="currentColor" fill-opacity="0.85">shaded diagonal = positives,</text>
  <text x="12" y="224" font-size="11" fill="currentColor" fill-opacity="0.85">nothing else marked</text>
  <rect x="232" y="166" width="194" height="86" rx="3" stroke="currentColor" stroke-width="2" fill="none"/>
  <text x="232" y="267" font-size="11" fill="currentColor">batch, N = 3</text>
  <line x1="426" y1="209" x2="444" y2="209" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD3e)"/>
  <text x="550" y="141" font-size="11" fill="currentColor" text-anchor="end">row softmax</text>
  <text x="550" y="157" font-size="11" fill="currentColor" text-anchor="end">image → text</text>
  <text x="450" y="187" font-size="11" fill="currentColor">L<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= 0.407606</tspan></text>
  <text x="450" y="213" font-size="11" fill="currentColor">L<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= 0.757448</tspan></text>
  <text x="450" y="239" font-size="11" fill="currentColor">L<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">= 0.642002</tspan></text>
  <line x1="450" y1="251" x2="534" y2="251" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="450" y="265" font-size="11" fill="currentColor" font-weight="bold">mean 0.602352</text>
  <line x1="329" y1="252" x2="329" y2="280" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD3e)"/>
  <text x="267" y="296" font-size="11" fill="currentColor" text-anchor="middle">0.407606</text>
  <text x="329" y="296" font-size="11" fill="currentColor" text-anchor="middle">0.757448</text>
  <text x="391" y="296" font-size="11" fill="currentColor" text-anchor="middle">0.642002</text>
  <text x="227" y="296" font-size="11" fill="currentColor" text-anchor="end">column softmax · text → image</text>
  <line x1="240" y1="302" x2="418" y2="302" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="329" y="317" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">mean 0.602352</text>
  <text x="227" y="317" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">same three: the matrix is symmetric</text>
  <text x="12" y="342" font-size="12" fill="currentColor" font-weight="bold">𝓛 = ½(0.602352 + 0.602352) = 0.602352 nats</text>
  <text x="12" y="360" font-size="11" fill="currentColor" fill-opacity="0.85">no information: log 3 = 1.098612</text>
</svg>

| $\ell_{ij}$ | $t_1$ | $t_2$ | $t_3$ |
|---|---:|---:|---:|
| $v_1$ | $\mathbf{2}$ | $1$ | $0$ |
| $v_2$ | $1$ | $\mathbf{2}$ | $1.732051$ |
| $v_3$ | $0$ | $1.732051$ | $\mathbf{2}$ |

D3's worked case at $\tau=1/2$: the two encoders give a $3\times3$ cosine matrix, and dividing all nine cells by $\tau$ gives the one logit matrix — repeated in the table — with the diagonal shaded as the positives and a box around the batch of $N=3$. The same matrix is read twice, by the row softmax (image → text) and by the column softmax (text → image), and because D3's matrix is symmetric both give the losses $0.407606$, $0.757448$ and $0.642002$, mean $0.602352$. The objective is $\mathcal L=0.602352$ nats, against $\log3=1.098612$ for a model with no information.

### Worked case

This is the homework object. Do the three things the problem set asks — the matrix, one row loss, the batch average — here first, on the catalog numbers.

**The nine dot products.** Because every vector is unit length, $v_i^\top t_j=\cos\theta_{ij}$, and the three angles are $0^\circ$, $60^\circ$, $90^\circ$:

$$V T^\top=\begin{pmatrix}1&1/2&0\\1/2&1&\sqrt3/2\\0&\sqrt3/2&1\end{pmatrix}=\begin{pmatrix}1&0.5&0\\0.5&1&0.866025\\0&0.866025&1\end{pmatrix}.$$

The matrix is symmetric, since $v_i=t_i$ for every $i$, which is a property of D3 and not of contrastive learning in general. Dividing by $\tau=1/2$ doubles every entry, giving the table above.

**Row 1, in full.** Image 1's logits are $(2,1,0)$, so

$$p_{11}=\frac{e^2}{e^2+e^1+e^0}=\frac{7.389056}{11.107338}=0.665241,\qquad L_{1}=-\log p_{11}=0.407606 \text{ nats}.$$

**All three rows, and the other direction.** Row 2's logits are $(1,2,1.732051)$ and row 3's are $(0,1.732051,2)$, giving

$$L_{1}=0.407606,\qquad L_{2}=0.757448,\qquad L_{3}=0.642002.$$

The column losses are the *same three numbers*, because the matrix is symmetric, so on D3 the two directions cannot disagree. The full objective is therefore

$$\mathcal L=\tfrac12\left(\tfrac13\textstyle\sum_i L_i^{\,i\to t}+\tfrac13\sum_i L_i^{\,t\to i}\right)=\tfrac13(0.407606+0.757448+0.642002)=0.602352 \text{ nats}.$$

**What that number is measured against.** A batch of $N=3$ that has learned nothing puts $1/3$ on every cell, so its loss is $\log 3=1.098612$ nats. D3 sits at $0.602352$, a little under half the way down — and the *floor* is $0$, reached only as $\tau\to0$. So the number alone says almost nothing: the same encoder scores anywhere between $0.933538$ and $0.000001$ on this very batch depending only on $\tau$, which §5 measures.

**The negative that is not obviously wrong.** Row 2's softmax at $\tau=1/2$ is $(0.172485,\ 0.468861,\ 0.358654)$. The gradient of a softmax cross-entropy is $p-y$ (worked in [[03-deep-learning/foundations/index|1. Learning Systems §2]]), so this row pushes image 2 *away from caption 3* with weight $0.358654$. All the push-down in the row together is $1-0.468861=0.531139$, the mass the softmax put on wrong captions, and caption 3 takes $0.358654/0.531139=67.5\%$ of it — two-thirds, against a third for caption 1 — because at $30^\circ$ it is the nearer negative. Caption 3 is a negative because it sits in a different slot of the batch, and for no other reason. Keep that number in mind for §2's paragraph about false negatives, and for problem 4, where caption 3 is a copy of caption 2. The figure puts the angles and the row side by side.

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="D3's three images and three captions coincide on the unit circle at 0, 60 and 90 degrees, so image 2 is 60 degrees from caption 1 and 30 degrees from caption 3; image 2's row softmax at tau = 1/2 is 0.172485, 0.468861, 0.358654, and caption 3 takes 67.5 percent of the push-down mass 0.531139; a dashed arc marks the one-wrong batch, which moves image 2 to 90 degrees">
  <defs><marker id="aVce" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="22" font-size="12" fill="currentColor">(a) D3 on the unit circle</text>
  <line x1="62" y1="282" x2="276" y2="282" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <line x1="62" y1="282" x2="62" y2="68" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <path d="M 258.0 282.0 A 196 196 0 0 0 62.0 86.0" stroke="currentColor" stroke-width="0.8" fill="none" stroke-opacity="0.35" stroke-dasharray="2 3"/>
  <line x1="62" y1="282" x2="258.0" y2="282.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#aVce)"/>
  <circle cx="258.0" cy="282.0" r="2.6" fill="currentColor"/>
  <text x="258.0" y="300.0" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= t</tspan><tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">· 0°</tspan></text>
  <line x1="62" y1="282" x2="160.0" y2="112.3" stroke="currentColor" stroke-width="1.6" marker-end="url(#aVce)"/>
  <circle cx="160.0" cy="112.3" r="2.6" fill="currentColor"/>
  <text x="168.0" y="110.3" font-size="11" fill="currentColor" text-anchor="start">v<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= t</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">· 60°</tspan></text>
  <line x1="62" y1="282" x2="62.0" y2="86.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#aVce)"/>
  <circle cx="62.0" cy="86.0" r="2.6" fill="currentColor"/>
  <text x="70.0" y="108.0" font-size="11" fill="currentColor" text-anchor="start">v<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">= t</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· 90°</tspan></text>
  <path d="M 116.0 282.0 A 54 54 0 0 0 89.0 235.2" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="120.9" y="252.0" font-size="11" fill="currentColor" text-anchor="middle">60°</text>
  <path d="M 110.0 198.9 A 96 96 0 0 0 62.0 186.0" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="91.0" y="177.8" font-size="11" fill="currentColor" text-anchor="middle">30°</text>
  <path d="M 167.0 100.1 A 210 210 0 0 0 69.3 72.1" stroke="currentColor" stroke-width="1.3" fill="none" stroke-dasharray="5 3" marker-end="url(#aVce)"/>
  <text x="70" y="48" font-size="11" fill="currentColor">v<tspan dy="3" font-size="10">2</tspan><tspan dy="-3">′, the one-wrong batch of §5:</tspan></text>
  <text x="70" y="62" font-size="11" fill="currentColor">moved to 90°, onto t<tspan dy="3" font-size="10">3</tspan></text>
  <text x="290" y="72" font-size="12" fill="currentColor">(b) image 2's row at τ = 1/2</text>
  <text x="384" y="109" font-size="11" fill="currentColor" text-anchor="end">caption 1, 60° away</text>
  <rect x="392" y="96" width="37.9" height="18" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="0.8"/>
  <text x="435.9" y="109" font-size="11" fill="currentColor">0.172485</text>
  <text x="384" y="143" font-size="11" fill="currentColor" text-anchor="end">caption 2, its match</text>
  <rect x="392" y="130" width="103.1" height="18" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="0.8"/>
  <text x="501.1" y="143" font-size="11" fill="currentColor">0.468861</text>
  <text x="501.1" y="157" font-size="10" fill="currentColor" fill-opacity="0.8">positive</text>
  <text x="384" y="177" font-size="11" fill="currentColor" text-anchor="end">caption 3, 30° away</text>
  <rect x="392" y="164" width="78.9" height="18" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="0.8"/>
  <text x="476.9" y="177" font-size="11" fill="currentColor">0.358654</text>
  <text x="476.9" y="191" font-size="10" fill="currentColor" fill-opacity="0.8">hard negative</text>
  <line x1="392" y1="90" x2="392" y2="194" stroke="currentColor" stroke-width="0.9"/>
  <text x="290" y="222" font-size="11" fill="currentColor">cosines: 0.5 to caption 1, 0.866025 to caption 3</text>
  <text x="290" y="240" font-size="11" fill="currentColor">push-down mass 1 − 0.468861 = 0.531139</text>
  <text x="290" y="258" font-size="11" fill="currentColor" font-weight="bold">caption 3 takes 0.358654/0.531139 = 67.5%</text>
  <text x="290" y="276" font-size="11" fill="currentColor" fill-opacity="0.85">the nearer negative is pushed harder</text>
</svg>

D3's images and captions coincide on the unit circle at $0^\circ$, $60^\circ$ and $90^\circ$, so image 2 sits $60^\circ$ from caption 1 (cosine $0.5$) and only $30^\circ$ from caption 3 (cosine $0.866025$). Its row softmax at $\tau=1/2$ is $(0.172485,\ 0.468861,\ 0.358654)$, and of the push-down mass $0.531139$ the nearer caption 3 takes $67.5\%$. The dashed arc is the one-wrong batch of §5 and problems 1–2, which moves image 2 to $90^\circ$, on top of caption 3.

### 1. Three VLM families

Three quite different machines are all called VLMs, and a paper's task usually decided which one it could use: the practical difference between them is cost, and the cost follows from where the two modalities meet.

- **dual encoder:** image and text encoded separately; fast retrieval and zero-shot classification through similarity.
- **fusion model:** tokens interact through cross-attention; stronger pair reasoning, more expensive all-pairs use.
- **generative model:** predicts language tokens conditioned on visual representations; fluent output is not proof of grounded perception.

A dual encoder computes $N$ image vectors and $M$ text vectors once and then scores any pair with a dot product, so ranking a query against a million images is a million multiply-adds. A fusion model has to run the joint network once per pair, so the same ranking is a million forward passes. That is why retrieval systems are built on dual encoders and why fusion models appear where the pair set is small — and it explains, without any appeal to quality, which architecture a paper's task forced on it.

**Zero-shot classification, on D3.** A dual encoder classifies by retrieval: write one caption per class, embed each once, and pick the caption closest to the image. Read D3's three captions as three class prompts and image 2's cosines to them are $(0.5,\ 1,\ 0.866025)$, so it is classified correctly, as class 2 — by a margin of only $1-0.866025=0.133975$ over class 3, the $30^\circ$ between their vectors. At $\tau=1/2$ that margin becomes a probability of $0.468861$, less than one half, and the decision is still right, because dividing by $\tau$ never moves the arg max. What this family outputs is a ranking, and its probabilities depend on a knob the ranking ignores (§2's temperature box). [[01-canonical-papers/notes/3-vlm/clip|CLIP]] is this procedure at scale: trained on $400$ million image–text pairs from the web, it matched the original supervised ResNet-50 on ImageNet zero-shot, without using any of ImageNet's training labels.

**What the other two families buy.** A fusion model reads the image and the text together, text tokens attending to image patches through cross-attention ([[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer §1]]), so it can score what a single angle cannot, such as which object a word in the caption refers to. A generative model writes the caption instead of scoring it, one sequential decoder pass per token, so a $20$-token answer costs $20$ passes after the image is read. Its fluency shows that it is conditioned on the image; whether it is grounded is §3's separate question, and §6 re-sorts all three families by where their modalities meet.

### 2. Contrastive learning, by hand

A dual encoder has pairs but no labels, so it learns by making each image pick its own caption out of the batch, and every other caption in the batch counts as wrong. The Worked case did this by hand for D3's three rows. Written for any batch, the full CLIP-style objective averages the image-to-text and text-to-image cross-entropies over the batch, and the other batch members are not generic "wrong language" but sampled negatives, so false negatives and batch composition affect what is learned.

That is the whole objective, so it is worth writing out with every symbol rather than describing.

> **The contrastive (InfoNCE) objective, defined.** A **contrastive objective** is a *classification loss over a batch* — each item's job is to pick its partner out of a lineup — and not a distance, not a regression onto a target embedding, and not a similarity that is maximised on its own. Four defining conditions, and dropping any one of them changes what the number means. The **positives are the diagonal by assumption**: pairing comes from how the batch was assembled, not from a judgement that the off-diagonal pairs are mismatched. The **negatives are the rest of the batch**, so the loss depends on $N$ and on which items were drawn together. The **logits are scaled by a temperature $\tau$** before the softmax, so the same embeddings can produce any loss between $0$ and $\log N$. And it is **symmetrised over the two directions**, image-to-text and text-to-image, which are two different classification problems over the same matrix.
>
> $$\mathcal L=\frac{1}{2N}\sum_{i=1}^{N}\left[-\log\frac{\exp(v_i^\top t_i/\tau)}{\sum_{j=1}^{N}\exp(v_i^\top t_j/\tau)}\;-\;\log\frac{\exp(v_i^\top t_i/\tau)}{\sum_{j=1}^{N}\exp(v_j^\top t_i/\tau)}\right]$$
>
> where $N$ is the batch size; $v_i\in\mathbb R^{d}$ is the L2-normalised embedding of image $i$ and $t_j$ that of caption $j$, so each $v_i^\top t_j$ is a cosine in $[-1,1]$; $\tau>0$ is the temperature; the first fraction normalises along **row** $i$ of the similarity matrix and the second along **column** $i$; and the $1/(2N)$ averages the two directions over the batch **so that** the objective is one scalar rather than two.
>
> - **Example**: D3 at $\tau=1/2$ gives row losses $(0.407606,\,0.757448,\,0.642002)$, identical column losses, and $\mathcal L=0.602352$ nats against a no-information value of $\log 3=1.098612$.
> - **Non-example**: maximising $\sum_i v_i^\top t_i$, the matched similarity alone. That is unbounded and trivially solved by collapsing every embedding to the same vector; the denominator is the only thing preventing collapse, which is why "the model learns to align images and text" is an incomplete description of the method.
> - **Non-example**: a per-pair binary loss on "match / no match". That scores pairs independently, so it neither depends on $N$ nor punishes ranking errors, and the two are not interchangeable even when they agree on D3.
> - **Non-example**: a symmetric *distance*. $\mathcal L$ is not symmetric in images and texts by construction — it is made symmetric by adding the two directions — and on a batch whose similarity matrix is not symmetric the two terms differ. D3's do not, because $v_i=t_i$.
> - **Why it matters**: $\log N$ is a ceiling on what one batch can certify. The standard InfoNCE bound (van den Oord et al. 2018; Poole et al. 2019) reads $I(V;T)\ge\log N-\mathbb E[\mathcal L]$ in expectation over batches, so a batch of 3 can certify at most $1.098612$ nats — about $1.584963$ bits — of mutual information no matter how good the encoder is. That, and not optimizer folklore, is the reason contrastive papers report batch sizes in the tens of thousands. Mutual information itself is [[02-foundations/information-theory|5. Information Theory §4]].

> **Temperature, defined.** The **temperature** $\tau$ is a *positive scalar dividing every logit before a softmax* — a property of the objective, not of a pair, not of the encoder, and not a learning rate. Three defining conditions. It is **shared across the whole matrix**, so it cannot express that one pair is more certain than another. It acts **only through the logit differences**, since the softmax is shift invariant ([[03-deep-learning/foundations/index|1. Learning Systems §1]]), so halving $\tau$ doubles every gap at once. And it **changes the loss without changing the model**: the embeddings, the ranking, and every retrieval decision are untouched by $\tau$, because dividing by a positive constant preserves order.
>
> $$p_{ij}=\frac{\exp(v_i^\top t_j/\tau)}{\sum_{k}\exp(v_i^\top t_k/\tau)},\qquad \tau\to\infty\Rightarrow p_{ij}\to\frac1N,\qquad \tau\to0\Rightarrow p_{ij}\to\mathbf 1\big[j=\arg\max_k v_i^\top t_k\big]$$
>
> where the two limits are the two ends of the sweep in §5 — a uniform distribution whose loss is $\log N$, and a hard arg max whose loss is $0$ if the arg max is the positive and unbounded if it is not.
>
> - **Example**: D3's row 1 at $\tau=1/2$ has $p_{11}=0.665241$; at $\tau=1/4$ the same dot products give logits $(4,2,0)$ and $p_{11}=0.866813$. The embeddings did not move.
> - **Non-example**: a confidence calibration. A small $\tau$ makes the training distribution sharp; it says nothing about how often the top-1 retrieval is correct, which is measured by recall@$k$ ([[02-foundations/ml-practice|9. ML Practice §3]]).
> - **Non-example**: a learning rate. Both are positive scalars that "control how aggressive training is", and there the resemblance ends: $\eta$ scales the *step*, $\tau$ reshapes the *loss surface*, and in real CLIP-style systems $\tau$ is itself a learned parameter while $\eta$ never is.
> - **Why it matters**: $\tau$ decides how the gradient is distributed over the negatives. A large $\tau$ spreads the push-down mass almost uniformly; a small $\tau$ concentrates it on the single hardest negative. That is why §5's sweep is not monotone once one pair in the batch is wrong — the hardest negative is then the thing the model is most confidently wrong about.

### 3. Conditioning is not grounding

A model can answer "red valve" correctly without having used the valve's pixels, and a robot that must then reach for the valve needs to know whether it did. A model is *conditioned on* an image when the image changes its output distribution. Grounding additionally asks whether a claim or token is supported by localized visual evidence. Caption likelihood, retrieval accuracy, VQA accuracy (visual question answering: the share of questions about an image answered correctly), hallucination rate (the share of outputs that mention an object or attribute the image does not contain), and spatial grounding measure different abilities.

Those two words carry the whole section, so both get definitions rather than a contrast.

> **Conditioning and grounding, defined.** **Conditioning** is a *property of a model's output distribution*: the model is conditioned on an input when changing that input changes the distribution. **Grounding** is a *property of a particular output together with particular evidence*: a token or claim is grounded when it is supported by identifiable visual evidence in this image. The first is a statement about a function, the second about an instance, which is why one can be established by an ablation and the other cannot.
>
> $$\text{conditioned on }x:\ \exists\,x,x'\ \text{s.t.}\ p(y\mid x)\ne p(y\mid x')\qquad\text{versus}\qquad\text{grounded: the evidence for }y\text{ lies in a region of }x$$
>
> where $x$ is the image and $y$ the output — and the left condition is an *existence* claim over inputs while the right is a claim about one output, **so** no amount of the left implies the right.
>
> - **Example of conditioning without grounding**: a captioner that reliably says "a person riding a horse" more often for outdoor photographs than indoor ones. The image is changing the distribution, so it is conditioned; whether any horse is in the picture is a separate question.
> - **Example of the test that separates them**: intervene on the image. Occlude, move, or recolour the region the claim is about and see whether the claim follows. A model whose answer is unchanged when the valve is painted blue was not reading the valve's colour.
> - **Non-example**: high accuracy on a benchmark. If "red valve" is the most common answer to that question in the training distribution, a language prior answers correctly with no visual evidence at all, and accuracy cannot tell the two apart.
> - **Non-example**: an attention map over the right region. Attention shows where the computation *looked*, not what the answer *depended on*; the two come apart routinely, which is why an intervention beats a visualisation as evidence.
> - **Why it matters**: for a robot the difference is the difference between a label and a target. A conditioned label can be right on average and still not tell the arm where to reach; a grounded one comes with the pixels, and therefore with a frame, that the controller needs ([[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §1]]).

### 4. From VLM to robot use

VLM representations can supply semantic labels, language-conditioned goals, reward signals, or a backbone for a VLA. None of these alone supplies control frequency, action feasibility, or recovery.

Each use leans on a different part of the model, and D3's numbers show where each can mislead. As a **semantic label** — which object does "the valve" mean — the VLM answers with a ranking, which is what a dual encoder is good at. As a **goal or success detector** it has to turn a similarity into a yes or no, and that needs a threshold set on the robot's own scenes: image 2 matches caption 2 exactly, cosine $1$, yet at $\tau=1/2$ its probability against the three captions is $0.468861$, so a detector that fires above one half calls a perfect match a failure, while at $\tau=1/4$ the same embeddings give $0.581234$ and the verdict flips with nothing in the scene changed. As a **reward** the cosine is flattest where precision matters: turning an embedding from $60^\circ$ off its caption to $0^\circ$ gains $0.5$, and the last $10^\circ$ of that turn gain only $0.015192$, three percent of it. As a **backbone** it supplies features but not a rate: OpenVLA, a 7B VLM turned into a policy, is capped near $6\,\mathrm{Hz}$ by decoding its action tokens one at a time, and π0 spends $32\,\mathrm{ms}$ on one pass over its observation before its action expert starts ([[03-deep-learning/vla/index|4. VLA §6]]).

Read [[01-canonical-papers/notes/3-vlm/clip|CLIP]] first, then fusion/generative entries and the [[03-deep-learning/vla/index|VLA course]]. How such a backbone is adapted — full fine-tuning or LoRA, and what each costs in memory and compute — is [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale §8]].

### 5. The lab: what the temperature does, and to whom

Contrastive papers tune $\tau$, and the loss they report moves with $\tau$ whether or not the encoder got any better — so before a loss curve can count as evidence you need to know what the temperature alone does, and to which batch. One knob, two batches. Part 1 reproduces the Worked case. Part 2 sweeps $\tau$ over the aligned D3 — the batch the encoder has already solved — and over the one-wrong batch that moves image 2 to $90^\circ$. The one-wrong column is the point: on a perfect batch the sweep is monotone and says nothing, and only a batch with a mistake in it has an opinion about $\tau$.

```python
# D3: contrastive logits, the two directions, and the temperature sweep. NumPy only.
import numpy as np

V = np.array(((1., 0.), (0.5, np.sqrt(3)/2), (0., 1.)))     # image embeddings, unit length
T = V.copy()                                                # matched captions are aligned

def infonce(V, T, tau):
    S = (V @ T.T) / tau                                     # logits: rows images, cols texts
    def ce(M):                                              # cross-entropy on the diagonal
        E = np.exp(M - M.max(1, keepdims=True))
        P = E / E.sum(1, keepdims=True)
        return -np.log(np.diag(P)), P
    li, Pi = ce(S)                                          # image -> text
    lt, Pt = ce(S.T)                                        # text  -> image
    return S, li, Pi, lt, Pt, float((li.mean() + lt.mean())/2)

S, li, Pi, lt, Pt, L = infonce(V, T, 0.5)
print("dot products V @ T.T\n", np.round(V @ T.T, 6))
print("logits at tau = 1/2\n", np.round(S, 6))
print("image->text row losses", np.round(li, 6), " diagonal p", np.round(np.diag(Pi), 6))
print("text->image col losses", np.round(lt, 6))
print("row 2 softmax", np.round(Pi[1], 6), " -> mass pushed off caption 3:", round(float(Pi[1, 2]), 6))
print("InfoNCE L =", round(L, 6), "  ceiling log 3 =", round(float(np.log(3)), 6))

Vm = V.copy(); Vm[1] = np.array((0., 1.))                   # image 2 encoded at 90 deg, not 60
taus = (2.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.01)
print("\n tau    p11       p22       p33       mean diag  L(aligned)  L(one wrong)")
for tau in taus:
    _, _, Pi, _, _, L = infonce(V, T, tau)
    d = np.diag(Pi)
    Lm = infonce(Vm, T, tau)[5]
    print("%5.2f  %.6f  %.6f  %.6f  %.6f   %.6f    %.6f" % (tau, d[0], d[1], d[2], d.mean(), L, Lm))

grid = np.exp(np.linspace(np.log(0.01), np.log(3.0), 20001))
Lm = np.array([infonce(Vm, T, t)[5] for t in grid]); i = int(Lm.argmin())
print("one wrong pair: best tau = %.4f at L = %.6f" % (grid[i], Lm[i]))
La = np.array([infonce(V, T, t)[5] for t in grid])
print("aligned batch : best tau = %.4f at L = %.6f (monotone: %s)"
      % (grid[La.argmin()], La.min(), bool(np.all(np.diff(La) > 0))))
print("log 3 in bits =", round(float(np.log(3)/np.log(2)), 6), "  log 2 =", round(float(np.log(2)), 6))
```

**The sweep.** $p_{ii}$ is the probability the row softmax puts on the correct caption; $\mathcal L$ is the symmetrised objective in nats. The no-information value is $\log 3=1.098612$.

| $\tau$ | $p_{11}$ | $p_{22}$ | $p_{33}$ | mean diagonal $p$ | $\mathcal L$ aligned | $\mathcal L$ one wrong |
|---:|---:|---:|---:|---:|---:|---:|
| $2$ | $0.419229$ | $0.368459$ | $0.393432$ | $0.393706$ | $0.933538$ | $0.932611$ |
| $1$ | $0.506480$ | $0.403040$ | $0.445933$ | $0.451818$ | $0.798859$ | $0.805616$ |
| $1/2$ | $0.665241$ | $0.468861$ | $0.526238$ | $0.553447$ | $0.602352$ | $0.644393$ |
| $1/4$ | $0.866813$ | $0.581234$ | $0.623652$ | $0.690566$ | $0.385899$ | $0.527329$ |
| $1/10$ | $0.993262$ | $0.788239$ | $0.792420$ | $0.857974$ | $0.159126$ | $0.535171$ |
| $1/20$ | $0.999955$ | $0.935766$ | $0.935806$ | $0.957175$ | $0.044261$ | $0.699810$ |
| $1/100$ | $1.000000$ | $0.999998$ | $0.999998$ | $0.999999$ | $0.000001$ | $2.463960$ |

**Reading the sweep.** Four things the row-1 calculation could not have told you.

- **On a batch it has already solved, lowering $\tau$ only buys confidence.** The aligned column falls monotonically from $0.933538$ at $\tau=2$ to $0.000001$ at $\tau=1/100$, and the grid search confirms the minimum is at the low end of the range. Nothing was learned; the same six vectors produced a loss that spans six orders of magnitude. A contrastive loss quoted without its $\tau$ and its $N$ is not a comparable number, and neither is a plot of it across a paper that tunes $\tau$.
- **The spread is not uniform across rows, and that is the geometry.** At $\tau=1/2$, $p_{11}=0.665241$ but $p_{22}=0.468861$ — image 2 is at $60^\circ$ from caption 1 and only $30^\circ$ from caption 3, so it has a genuinely hard negative and image 1 does not. Row 2 is the hardest row at every temperature in the table. Hard negatives are a property of the embedding geometry, not of the sampling code.
- **With one pair wrong, the loss is not monotone in $\tau$ and has an interior minimum.** The right-hand column falls to $0.527329$ at $\tau=1/4$, turns, and reaches $2.463960$ at $\tau=1/100$ — worse than the no-information $\log 3$. A grid search over $\tau\in[0.01,3]$ puts the minimum at $\tau=0.1639$, $\mathcal L=0.507409$. Sharpening amplifies whatever the model believes, and below the optimum it is amplifying a mistake.
- **A large enough $\tau$ hides the error completely.** At $\tau=2$ the wrong encoder scores $0.932611$ against the correct encoder's $0.933538$ — marginally *better*. The two curves cross at $\tau\approx1.6542$. Above that, the softmax is so flat that a $30^\circ$ encoding error is invisible in the loss, which is worth remembering whenever a training curve is used as evidence that an encoder is working.

### 6. Where the modalities meet: from VLM to omni-modal

§1 sorted vision–language models by what they output. Every multimodal model can also be placed by *where its modalities meet*, and that one choice sets what it can generate, what it costs, and whether a robot's actions can join it. D3 is the latest possible meeting point: an image and a caption never see each other and meet only in one dot product, $\ell_{ij}=v_i^\top t_j/\tau$.

| where they meet | how | examples | what it buys | what it costs |
|---|---|---|---|---|
| at the end | two encoders and one similarity | [[01-canonical-papers/notes/3-vlm/clip\|CLIP]], D3 | ranking a million items for the price of dot products | no generation, and nothing about a pair beyond one angle |
| through a bridge | visual features enter a language model by cross-attention, a small query transformer, or a projection into its token space | [[01-canonical-papers/notes/3-vlm/flamingo\|Flamingo]], [[01-canonical-papers/notes/3-vlm/blip-2\|BLIP-2]], [[01-canonical-papers/notes/3-vlm/llava\|LLaVA]], [[01-canonical-papers/notes/3-vlm/paligemma\|PaliGemma]] | text generated about an image | the image is read, never generated; one joint pass per pair |
| in one sequence | every modality becomes positions in one transformer — as discrete codes (Chameleon) or as continuous patches trained with a diffusion loss (Transfusion) | Chameleon (2024); Transfusion (2024) | images and text read and generated in any interleaving | every image costs many positions; discrete codes lose detail, and Transfusion reports scaling better than a model over quantized image tokens |
| omni-modal | the one-sequence design widened to audio and video, in and out, trained end to end | GPT-4o (2024); Qwen2.5-Omni (2025) | one network that perceives and answers in speech | the longest sequences of all, since every second of audio and video adds positions |

On D3 the difference is countable. Three images and three captions cost six encoder passes, after which all nine pairs are scored by dot products; a model that meets the modalities in one sequence needs nine joint passes for the same nine scores, and in exchange can say *why* a pair matches or write the caption itself. That is §1's cost argument, carried to its end. The collapsed note below says how the table's two omni models work inside and where the one-sequence designs came from.

> [!note]- Deeper · 더 깊이
> **The omni models, briefly.** GPT-4o accepts any mix of text, audio, image and video and produces text, audio and images from one network trained across all of them; its system card reports answers to speech in as little as $232$ ms, $320$ ms on average — the latency of a human reply ([OpenAI, 2024](https://arxiv.org/abs/2410.21276)). Qwen2.5-Omni streams text and speech at once by splitting the work: a *Thinker*, the language model, writes text, and a *Talker* turns the Thinker's hidden states into audio tokens, while a time-aligned position embedding keeps interleaved video and audio in step ([Qwen, 2025](https://arxiv.org/abs/2503.20215)). The early-fusion ancestors are Chameleon, which tokenizes images with a codebook of the kind in [[03-deep-learning/diffusion/vae-gan|6.1 §10]] ([Chameleon Team, 2024](https://arxiv.org/abs/2405.09818)), and Transfusion, which trains one transformer with next-token prediction on text and diffusion on images ([Zhou et al., 2024](https://arxiv.org/abs/2408.11039)).

**Action is one more modality.** π0's architecture is, in its authors' words, inspired by Transfusion — one transformer, a cross-entropy loss on its discrete tokens and a flow-matching loss on its continuous ones — and adds a separate set of weights for the robot's state and action tokens, the Mixture of Transformers of [[03-deep-learning/vla/index|4. VLA §6]]. It starts from PaliGemma, a 3B VLM that writes its answers a token at a time, and supervises its own action tokens with flow matching, which trains the network to turn random noise into an action chunk in a few integration steps — the denoiser family of that same §6 ([[01-canonical-papers/notes/4-vla/pi0|π0]]). A VLA is therefore an early-fusion model — its modalities meet in one sequence, the table's third row — whose extra output modality is action, and Gemini Robotics built one directly on Gemini 2.0, a large multimodal model ([Gemini Robotics Team, 2025](https://arxiv.org/abs/2503.20020)). Inputs widen the same way: ManiWAV put a microphone in the gripper and learned contact-rich skills from audio and video together, because sound carried contact events and surface materials that vision alone left ambiguous ([Liu et al., 2024](https://arxiv.org/abs/2406.19464)). A construction site is where that matters — loud, cluttered, often poorly lit — and where a worker's spoken instruction is the natural interface. So read "omni-modal" in a robot paper as two questions: which modalities go in, and whether action is among those that come out.

### Self-check

1. Why does D3's image-to-text loss equal its text-to-image loss, and is that a property of contrastive learning?
2. The batch has $N=3$. What is the largest mutual information this objective could certify, and why?
3. Lowering $\tau$ from $1/2$ to $1/4$ raises $p_{11}$ from $0.665$ to $0.867$. Which retrieval decisions changed?
4. Row 2 pushes $0.359$ of its mass away from caption 3. What has to be true about caption 3 for that to be correct supervision?
5. A model answers "red valve" correctly. Name the experiment that distinguishes conditioning from grounding, and say why higher accuracy cannot substitute for it.
6. A robot paper calls its model "omni-modal" because it takes images, language and audio. Which two questions from §6 place it, and what would have to be true for it to be a VLA?

> [!tip]- Answers
> 1. Because $v_i=t_i$ for every $i$, so the similarity matrix is symmetric and transposing it changes nothing. It is a property of this object, not of the method: any batch whose matched pairs are not exactly aligned gives two different direction losses, which is why the objective sums both.
> 2. $\log 3=1.098612$ nats, about $1.584963$ bits. The InfoNCE bound is $I\ge\log N-\mathbb E[\mathcal L]$ and $\mathcal L\ge0$, so the batch size caps the certificate regardless of the encoder.
> 3. None. Dividing by a positive constant preserves the order of the logits, so every arg max, every ranking and therefore every recall@$k$ is unchanged. Only the loss moved.
> 4. Caption 3 must not describe image 2. On D3 that is assumed rather than checked — it holds because the batch was built that way — and the problem set's duplicate-caption variant is the case where the assumption is false and the gradient is actively wrong.
> 5. Intervene on the image: occlude or recolour the valve and see whether the answer follows. Accuracy cannot substitute because a language prior that answers "red" for valves scores well with no visual evidence, so the benchmark number is consistent with both explanations.
> 6. Where its modalities meet — at the end, through a bridge, or in one sequence — and which modalities it *outputs*. Taking images, language and audio in says only what it perceives. It is a VLA only if action is among its outputs, trained with a loss on actions and run at a control rate; otherwise it is a perception model feeding someone else's policy, and its "omni" describes the ears, not the hands.

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and [[03-deep-learning/lab-objects|0. Lab Objects]]. D3 and its two variants are frozen in the Running object. Questions 1–2 open the one-wrong batch at $\tau=1/2$, whose single loss §5 prints but whose rows and columns it never shows, and question 4 uses the duplicate-caption variant, which §5 never runs, so none of the lab's numbers can be copied.

1. **Draw.** The picture above, redrawn for the one-wrong batch — image 2 encoded at $90^\circ$ — at $\tau=1/2$: its $3\times3$ logit matrix with only the diagonal shaded as positives, the $\tau$ division in front of it, the row softmax and the column softmax as two arrows off the same matrix with their three losses each, and the batch box. Circle the cell each row ranks first, and mark where a fourth pair would add cells and which of the added cells would be negatives.
2. **Derive.** On the same batch: (a) the logit matrix, and why it is no longer symmetric; (b) the three row losses, the three column losses and $\mathcal L$, checked against §5's one-wrong column; (c) row 2's softmax, the caption it ranks first, and the share of its push-down mass that caption 3 takes, against D3's $67.5\%$.
3. **Interpret.** A VLM asked to point at "the left bolt hole" of S1's panel — S1 is the construction track's facade-panel task, whose panel has two mounting holes $400$ mm apart ([[05-construction-robotics/site-engineering|2.5]]) — lands on the left hole in all $20$ test images, every one taken from the same tripod. (a) Which claim is still open? (b) Design two interventions on the image that separate grounding from a learned position, and say what a grounded answer must do under each. (c) Why is "left" a harder word to ground than "red"?
4. **Do.** Fill the `?` blanks, then run the **duplicate-caption** variant: caption 3 is an exact copy of caption 2, so $t_3=t_2$ while the images are unchanged. Sweep $\tau\in\{2,1,1/2,1/4,1/10,1/20,1/100\}$ and report (a) $\mathcal L$ at each $\tau$; (b) the three image-to-text row losses and the three text-to-image column losses at $\tau=1/2$ and at $\tau=1/100$; (c) the $\tau$ that minimises $\mathcal L$, by grid search. Then answer in two sentences: which of the six losses is unbounded as $\tau\to0$ and which ones converge to $\log 2$, and what that difference says about how a duplicate caption damages the two directions differently.

```python
# D3 with a duplicate caption. Reuse infonce from section 5. Fill ?.
import numpy as np
V = np.array(((1., 0.), (0.5, np.sqrt(3)/2), (0., 1.)))
T = V.copy()
Td = T.copy(); Td[2] = ?                     # caption 3 becomes a copy of caption 2

print("dot products\n", np.round(V @ Td.T, 6))
for tau in (2.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.01):
    S, li, Pi, lt, Pt, L = infonce(V, Td, tau)
    print("tau=%.2f  L=%.6f  i->t %s  t->i %s" % (tau, L, np.round(li, 6), np.round(lt, 6)))

grid = np.exp(np.linspace(np.log(0.01), np.log(3.0), 20001))
Ld = np.array([? for t in grid])             # L at each tau on the grid
print("best tau = %.4f at L = %.6f" % (grid[Ld.argmin()], Ld.min()))
```

> [!note]- How to draw it · 그리는 법
> - Mark the diagonal as the positives, and nothing else. Every off-diagonal cell is a negative *by construction of the batch*, not by any evidence that the pair is wrong; that is the single assumption the whole loss rests on, and the duplicate-caption variant is what happens when it fails.
> - Draw two arrows out of the same matrix, not two matrices. The row softmax and the column softmax read the identical numbers in two directions; drawing two matrices claims there are two models, and there is one, scored twice.
> - Draw the $\tau$ division before the softmax, on the whole matrix. Temperature is not a property of a pair or of the encoder — it scales every cell at once, which is why §5 can pull it out and sweep it.
> - Draw the batch boundary as a box around all the cells. Nothing outside the box is a negative: a loss computed over three items is a different function from the same loss over 32,768 items, and the box is where the difference lives.
> - Write each direction's three losses at the end of its own arrow. On D3 they are the same three numbers; on the one-wrong batch they differ, and a drawing with one set of losses has hidden the error.

> [!tip]- Solutions
> 1. Rows are images, columns captions, and the shaded diagonal $(2,\ 1.732051,\ 2)$ holds the matched pairs. The matrix is $\begin{pmatrix}2&1&0\\0&1.732051&2\\0&1.732051&2\end{pmatrix}$ after the $\tau$ division on all nine cells. The row arrow ends in the losses $(0.407606,\ 0.909951,\ 0.642002)$, the column arrow in $(0.239545,\ 0.908630,\ 0.758624)$ — two different sets now. The circles fall on $(1,1)$, $(2,3)$ and $(3,3)$: row 2's is off the diagonal, because image 2 now ranks caption 3 first. A fourth pair adds a fourth row and column, seven new cells: the one on the diagonal is a positive and the six off it are negatives the moment they are drawn, which is the whole mechanism by which $N$ enters the loss.
> 2. (a) $v_2'=(0,1)$ gives $v_2'^\top t_j=(0,\ 0.866025,\ 1)$, so row 2 of the logits is $(0,\ 1.732051,\ 2)$, the same as row 3 because $v_2'=v_3$. The matrix is not symmetric — $\ell_{12}=1$ but $\ell_{21}=0$ — because image 2 moved and caption 2 did not, so $v_2'\ne t_2$. (b) Rows: $L_1=0.407606$ and $L_3=0.642002$ are unchanged, and $L_2=-\log\big(e^{1.732051}/(e^0+e^{1.732051}+e^2)\big)=0.909951$, mean $0.653187$. Columns: $0.239545$, $0.908630$ and $0.758624$, mean $0.635600$. So $\mathcal L=\tfrac12(0.653187+0.635600)=0.644393$, the $\tau=1/2$ entry of §5's one-wrong column. Column 1 *fell*, from $0.407606$ to $0.239545$: image 2 moved away from caption 1, cosine $0.5$ to $0$, so caption 1's lineup got easier — a wrong encoder lowered one direction's loss. In columns 2 and 3 images 2 and 3 now tie, because $v_2'=v_3$. (c) Row 2's softmax is $(0.071219,\ 0.402544,\ 0.526238)$, so caption 3 ranks first and image 2 now retrieves the wrong caption. The push-down mass is $1-0.402544=0.597456$ and caption 3 takes $0.526238$ of it, $88.1\%$ against D3's $67.5\%$: the hard negative has become the model's first choice, and the gradient $p-y$ pushes hardest exactly there.
> 3. (a) Whether the point comes from the hole's pixels or from where left holes sit in these pictures. With one tripod the left hole is always near the same pixel, so a model that returns that pixel without looking scores $20/20$ — the "red valve" ambiguity, with a position prior in place of a colour prior. (b) *Shift*: move the panel, or translate the image, sideways by a known number of pixels; a grounded answer moves by the same amount, and a position prior stays put. *Mirror*: flip the image left to right; the hole that was on the right is now the left one, so a grounded answer jumps to the other hole, $400$ mm away on the panel, while an answer that stays put was not reading "left" off the image. Covering the left hole is a third test: a grounded model loses it rather than pointing at the cover. (c) "Red" is a property of the object's own pixels, so recolouring tests it directly. "Left" is a relation between the two holes *and* a viewpoint — the camera's left is the worker's right when the worker faces the camera — so "left" has no answer until a frame is fixed: the camera frame of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception §1]], or the worker's.
> 4. Blanks: `Td[2] = T[1]` and `Ld = np.array([infonce(V, Td, t)[5] for t in grid])`. The dot products become $\begin{pmatrix}1&0.5&0.5\\0.5&1&1\\0&0.866025&0.866025\end{pmatrix}$, with columns 2 and 3 identical.
>
>    (a) and (c):
>
>    | $\tau$ | $2$ | $1$ | $1/2$ | $1/4$ | $1/10$ | $1/20$ | $1/100$ |
>    |---|---:|---:|---:|---:|---:|---:|---:|
>    | $\mathcal L$ | $0.978047$ | $0.878017$ | $0.730300$ | $0.578480$ | $0.537591$ | $0.699788$ | $2.463960$ |
>
>    The grid search gives $\tau=0.1362$ at $\mathcal L=0.521824$ — an interior minimum, like the one-wrong batch of §5 but for a different reason: nothing about the *encoder* is wrong here, only the labelling of the batch.
>
>    (b) At $\tau=1/2$: image-to-text $(0.551445,\,0.861995,\,0.777912)$, text-to-image $(0.407606,\,0.757448,\,1.025397)$. At $\tau=1/100$: image-to-text $(0,\,0.693147,\,0.693147)$, text-to-image $(0,\,0.000002,\,13.397461)$.
>
>    The unbounded one is the text-to-image loss of column 3; the two converging to $\log 2=0.693147$ are the image-to-text losses of rows 2 and 3. The asymmetry is the point. Along a row the model must choose between two *identical* captions, so the best it can do is split the mass, and $\log 2$ is the price of a tie it cannot win — bounded, and arguably not even an error. Along column 3 the model must choose between two *different* images for the duplicated caption, and image 2 wins it ($v_2^\top t_3=1$ against $v_3^\top t_3=0.866025$), so the correct image is ranked second and its loss grows without bound as $\tau\to0$. A duplicate caption costs a tie in one direction and an outright wrong answer in the other, and only the second is unbounded — which is why deduplicating captions matters more than it looks, and why low temperatures make a noisy batch actively dangerous.

### Sources

The paper notes linked from §1, §4 and §6 — CLIP, Flamingo, BLIP-2, LLaVA, PaliGemma, π0 — carry each paper's own citation. The rest of the page cites:

- van den Oord, A., Li, Y. & Vinyals, O. "Representation Learning with Contrastive Predictive Coding." arXiv:1807.03748, 2018 — the InfoNCE objective and its $\log N$ bound (§2).
- Poole, B., Ozair, S., van den Oord, A., Alemi, A. A. & Tucker, G. "On Variational Bounds of Mutual Information." *ICML*, 2019 — the same bound among the mutual-information estimators (§2).
- Black, K. et al. "π0: A Vision-Language-Action Flow Model for General Robot Control." arXiv:2410.24164, 2024 — the architecture "inspired by Transfusion", the separate weights for state and action tokens, flow matching on the action tokens (§6).
- Gemini Robotics Team. "Gemini Robotics: Bringing AI into the Physical World." arXiv:2503.20020, 2025 — a VLA built on Gemini 2.0 (§6).
- Liu, Z., Chi, C., Cousineau, E. et al. "ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data." *CoRL*, 2024 — contact skills learned from audio and video together (§6).
- OpenAI. "GPT-4o System Card." arXiv:2410.21276, 2024 — any mix of inputs and outputs, $232$ and $320$ ms replies to speech (§6, the collapsed note).
- Xu, J., Guo, Z., He, J. et al. "Qwen2.5-Omni Technical Report." arXiv:2503.20215, 2025 — the Thinker and the Talker (§6, the collapsed note).
- Chameleon Team. "Chameleon: Mixed-Modal Early-Fusion Foundation Models." arXiv:2405.09818, 2024; Zhou, C., Yu, L., Babu, A. et al. "Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model." arXiv:2408.11039, 2024 — the two one-sequence designs (§6).

## 한국어

> [!note] 왜 배우는가 · Why this matters
> [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 이 페이지는 학습과 적응 층에 속하고, 그 스택을 언어가 구동하는 형태가 시작되는 "VLM 또는 VLA 추론" 상자다. "*저 패널을 프레임에 설치해*"에서는 첫 단계인 *지시 해석*을 받친다. 둘째 단계가 패널을 식별하려면 먼저 "저 패널"이 이미지 속 무언가에 묶여야 하기 때문이다([[physical-ai-map|피지컬 AI 지도]]의 학습과 적응 띠에 이 페이지의 자리가 있다). 이것 없이는 시각–언어 숫자를 과하게 읽기 쉽다. 이 트랙이 고정해 둔 이미지–캡션 3쌍 D3([[03-deep-learning/lab-objects|0. Lab Objects]])는 인코더가 이미 완벽하게 풀어 놓은 배치인데도 loss가 temperature 하나만으로 $0.933538$에서 $0.000001$까지 오르내린다(§5). 절반을 넘으면 켜지는 성공 판정기는 $\tau=1/2$에서는 완벽한 일치를 실패라 부르고($p=0.468861$), $\tau=1/4$에서는 성공이라 부른다($p=0.581234$). 장면은 하나도 바뀌지 않았다(§4). 그리고 "red valve"라는 맞는 답은 밸브의 픽셀을 썼는지에 대해 아무것도 말하지 않는다(§3). 뒤 페이지들이 이 위에 선다. [[03-deep-learning/vla/index|4. VLA]]는 이 백본에 행동 헤드를 달고 그 §6에서 백본의 주기에 값을 매기며, VLM 성공 판정은 [[02-foundations/rl-robot-learning|7.5 로봇 학습을 위한 RL §8]]이 학습에 쓰는 바로 그런 이진 보상이다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 블록 4의 딥러닝 페이지 넷 가운데 셋째이고, 딥러닝 회차 35–38이다. 이 페이지를 마치면 대조 배치를 손으로 계산하고, 그 숫자가 무엇을 보증하는지 — 최대 $\log N$ nat — 말하고, 논문의 주장에서 conditioning과 grounding을 가를 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 회차 네 번쯤이고, [[03-deep-learning/index|딥러닝 학습 일정]]의 35–38행이다. 앞의 두 회차가 첫 읽기다. **첫 회차:** D3와 그림을 본 뒤, 풀이를 가리고 계산 절을 손으로 한다. 내적 아홉 개, 행 loss 셋, 그리고 $\log3=1.098612$에 대한 $\mathcal L=0.602352$ nat이다. **둘째 회차:** §1–§4, 스스로 점검 1–5, 과제 1–3. **셋째 회차:** §5 실습과 과제 4. **넷째 회차:** §6과 스스로 점검 6. 옴니 모델에 관한 접힌 메모는 두 번째 읽기로 미룬다. 마지막으로 대조 loss가 무엇을 보증하는지 — 최대 $\log N$ nat의 상호정보량 — 와 무엇을 보증하지 않는지 — 답이 픽셀에 grounded되어 있다는 것 — 를 두 문장으로 말해 본다.

### 계속 쓰는 대상: D3

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D3**는 이미지–캡션 3쌍이다. 고정 임베딩과 $\tau=1/2$는

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix}.$$

logit은 $\ell_{ij}=v_i^\top t_j/\tau$다. 행 $i$가 이미지 $i$의 logit 벡터, 곧 [[03-deep-learning/foundations/index|1. 학습 시스템]]의 $s$이고, 배치의 캡션 $N$개가 그 클래스다(D3에서는 $N=3$). 행은 이미지에 맞는 텍스트, 열은 텍스트에 맞는 이미지를 묻는다.

이 페이지의 전부가 그 벡터 여섯 개와 손잡이 하나에서 나온다. 모두 단위 길이라 각 내적은 두 벡터 사이 각의 코사인이고, 세 이미지는 $0^\circ$, $60^\circ$, $90^\circ$에 놓인다. 짝이 맞는 쌍은 *정확히* 정렬되어 있다. 즉 encoder가 이미 풀어 놓은 배치라서, D3에서 잘못될 수 있는 것은 목적함수 자체뿐이다. 대조 loss를 읽기에 알맞은 대상인 이유가 그것이다. §5와 과제를 위해 벡터 하나씩만 바꾼 페이지 고유 변형 둘도 여기서 고정한다. **한 쌍이 틀린 배치**는 이미지 2를 $v_2'=(0,1)$, 즉 $90^\circ$로 옮겨 encoder가 캡션 3 위에 겹쳐 놓게 한다. **중복 캡션 배치**는 $t_3=t_2$로 두어 캡션 2와 3이 같은 문장이 되고, 행 2의 "negative"가 실제로는 맞는 짝이 된다.

*범위: 이 페이지는 dual encoder의 대조 목적함수 — similarity matrix, 두 방향, temperature, negative, 그리고 그 결과 숫자가 보증하는 것과 보증하지 못하는 것 — 와 conditioning을 grounding에서 가르는 어휘를 가르친다. 이미지 encoder는 가르치지 않는다. 그것은 [[03-deep-learning/computer-vision/index|2. 컴퓨터비전 §1]]이다. fusion 모델이 쓰는 cross-attention — 텍스트 토큰 하나하나가 이미지 패치들에 가중치를 매기고 그 가중합을 읽는 것 — 도 아니다. 그것은 학위논문 경로 밖의 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer §1]]과 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]다. 목적함수 주변의 loss·optimizer 기계도 아니다. 그것은 [[03-deep-learning/foundations/index|1. 학습 시스템 §1–§2]]와 그 §6 실습이다. 생성 디코딩, 캡션 metric, 행동도 아니다. 그것은 [[01-canonical-papers/canonical-list|canonical list]]의 생성 항목과 [[03-deep-learning/vla/index|VLA 교과]]다. §6은 그 더 큰 모델들을 모달리티가 만나는 곳으로만 자리 매긴다. §3에 이름만 나오는 retrieval metric은 [[02-foundations/ml-practice|9. ML 실무 §3]]에 정의되어 있다.*

### 그림으로 먼저 보기

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="D3의 두 encoder가 3×3 코사인 행렬을 만들고, 아홉 칸 전부를 τ = 1/2로 나눈 logit 행렬 하나에 대각선을 positive로 표시하고 배치 상자를 두른 뒤, 그 행렬을 행 방향과 열 방향으로 읽어 각각 loss 0.407606, 0.757448, 0.642002와 목적함수 0.602352 nat을 얻는 그림">
  <defs><marker id="aD3k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="38" font-size="11" fill="currentColor">이미지 3장</text>
  <line x1="78" y1="34" x2="90" y2="34" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3k)"/>
  <rect x="92" y="23" width="90" height="22" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="137" y="38" font-size="11" fill="currentColor" text-anchor="middle">이미지 encoder</text>
  <line x1="137" y1="45" x2="137" y2="51" stroke="currentColor" stroke-width="1.2"/>
  <text x="137" y="63" font-size="11" fill="currentColor" text-anchor="middle">v<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, v</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">, v</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· 단위</tspan></text>
  <text x="12" y="88" font-size="11" fill="currentColor">캡션 3개</text>
  <line x1="78" y1="84" x2="90" y2="84" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3k)"/>
  <rect x="92" y="73" width="90" height="22" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="137" y="88" font-size="11" fill="currentColor" text-anchor="middle">텍스트 encoder</text>
  <line x1="137" y1="95" x2="137" y2="101" stroke="currentColor" stroke-width="1.2"/>
  <text x="137" y="113" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, t</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">, t</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· 단위</tspan></text>
  <text x="137" y="132" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">각 0°, 60°, 90°</text>
  <text x="430" y="71" font-size="11" fill="currentColor" fill-opacity="0.85">V T<tspan dy="-4" font-size="10">T</tspan><tspan dy="4">: 코사인</tspan></text>
  <text x="267" y="35" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">t<tspan dy="3" font-size="10">1</tspan></text>
  <text x="329" y="35" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">t<tspan dy="3" font-size="10">2</tspan></text>
  <text x="391" y="35" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">t<tspan dy="3" font-size="10">3</tspan></text>
  <text x="230" y="53" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">v<tspan dy="3" font-size="10">1</tspan></text>
  <text x="267" y="53" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <text x="329" y="53" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <text x="391" y="53" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <text x="230" y="71" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">v<tspan dy="3" font-size="10">2</tspan></text>
  <text x="267" y="71" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.5</text>
  <text x="329" y="71" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <text x="391" y="71" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.866025</text>
  <text x="230" y="89" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">v<tspan dy="3" font-size="10">3</tspan></text>
  <text x="267" y="89" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0</text>
  <text x="329" y="89" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">0.866025</text>
  <text x="391" y="89" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">1</text>
  <rect x="236" y="40" width="186" height="54" stroke="currentColor" stroke-width="1" fill="none" stroke-opacity="0.6"/>
  <line x1="198" y1="67" x2="212" y2="58" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3k)"/>
  <line x1="198" y1="117" x2="212" y2="78" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3k)"/>
  <line x1="329" y1="97" x2="329" y2="146" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD3k)"/>
  <text x="337" y="124" font-size="11" fill="currentColor">÷ τ, τ = 1/2, 아홉 칸 전부에</text>
  <rect x="236" y="170" width="62" height="26" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <rect x="298" y="196" width="62" height="26" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <rect x="360" y="222" width="62" height="26" stroke="none" fill="currentColor" fill-opacity="0.22"/>
  <line x1="298" y1="170" x2="298" y2="248" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <line x1="236" y1="196" x2="422" y2="196" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <line x1="360" y1="170" x2="360" y2="248" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <line x1="236" y1="222" x2="422" y2="222" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.4"/>
  <text x="267" y="157" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">1</tspan></text>
  <text x="329" y="157" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">2</tspan></text>
  <text x="391" y="157" font-size="11" fill="currentColor" text-anchor="middle">t<tspan dy="3" font-size="10">3</tspan></text>
  <text x="227" y="187" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">1</tspan></text>
  <text x="267" y="188" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <text x="329" y="188" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <text x="391" y="188" font-size="12" fill="currentColor" text-anchor="middle">0</text>
  <text x="227" y="213" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">2</tspan></text>
  <text x="267" y="214" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <text x="329" y="214" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <text x="391" y="214" font-size="12" fill="currentColor" text-anchor="middle">1.732051</text>
  <text x="227" y="239" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">3</tspan></text>
  <text x="267" y="240" font-size="12" fill="currentColor" text-anchor="middle">0</text>
  <text x="329" y="240" font-size="12" fill="currentColor" text-anchor="middle">1.732051</text>
  <text x="391" y="240" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <text x="12" y="182" font-size="11" fill="currentColor">ℓ<tspan dy="3" font-size="10">ij</tspan><tspan dy="-3" dx="3.5">= v</tspan><tspan dy="3" font-size="10">i</tspan><tspan dy="-7" font-size="10">T</tspan><tspan dy="4">t</tspan><tspan dy="3" font-size="10">j</tspan><tspan dy="-3" dx="3.5">/ τ</tspan></text>
  <text x="12" y="208" font-size="11" fill="currentColor" fill-opacity="0.85">음영 대각선 = positive,</text>
  <text x="12" y="224" font-size="11" fill="currentColor" fill-opacity="0.85">그 밖에는 표시 없음</text>
  <rect x="232" y="166" width="194" height="86" rx="3" stroke="currentColor" stroke-width="2" fill="none"/>
  <text x="232" y="267" font-size="11" fill="currentColor">배치, N = 3</text>
  <line x1="426" y1="209" x2="444" y2="209" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD3k)"/>
  <text x="550" y="141" font-size="11" fill="currentColor" text-anchor="end">행 softmax</text>
  <text x="550" y="157" font-size="11" fill="currentColor" text-anchor="end">이미지 → 텍스트</text>
  <text x="450" y="187" font-size="11" fill="currentColor">L<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= 0.407606</tspan></text>
  <text x="450" y="213" font-size="11" fill="currentColor">L<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= 0.757448</tspan></text>
  <text x="450" y="239" font-size="11" fill="currentColor">L<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">= 0.642002</tspan></text>
  <line x1="450" y1="251" x2="534" y2="251" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="450" y="265" font-size="11" fill="currentColor" font-weight="bold">평균 0.602352</text>
  <line x1="329" y1="252" x2="329" y2="280" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD3k)"/>
  <text x="267" y="296" font-size="11" fill="currentColor" text-anchor="middle">0.407606</text>
  <text x="329" y="296" font-size="11" fill="currentColor" text-anchor="middle">0.757448</text>
  <text x="391" y="296" font-size="11" fill="currentColor" text-anchor="middle">0.642002</text>
  <text x="227" y="296" font-size="11" fill="currentColor" text-anchor="end">열 softmax · 텍스트 → 이미지</text>
  <line x1="240" y1="302" x2="418" y2="302" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="329" y="317" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">평균 0.602352</text>
  <text x="227" y="317" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">같은 세 숫자: 행렬이 대칭</text>
  <text x="12" y="342" font-size="12" fill="currentColor" font-weight="bold">𝓛 = ½(0.602352 + 0.602352) = 0.602352 nat</text>
  <text x="12" y="360" font-size="11" fill="currentColor" fill-opacity="0.85">정보 없음: log 3 = 1.098612</text>
</svg>

| $\ell_{ij}$ | $t_1$ | $t_2$ | $t_3$ |
|---|---:|---:|---:|
| $v_1$ | $\mathbf{2}$ | $1$ | $0$ |
| $v_2$ | $1$ | $\mathbf{2}$ | $1.732051$ |
| $v_3$ | $0$ | $1.732051$ | $\mathbf{2}$ |

$\tau=1/2$에서의 D3 계산 절로, 두 encoder가 $3\times3$ 코사인 행렬을 만들고 아홉 칸 전부를 $\tau$로 나누면 logit 행렬 하나 — 표에 다시 적었다 — 가 되며, 대각선은 positive로 음영을 넣고 $N=3$인 배치를 상자로 감쌌다. 같은 행렬을 행 softmax(이미지 → 텍스트)와 열 softmax(텍스트 → 이미지)로 두 번 읽는데, D3의 행렬이 대칭이라 두 방향 모두 loss $0.407606$, $0.757448$, $0.642002$, 평균 $0.602352$를 준다. 목적함수는 $\mathcal L=0.602352$ nat이고, 정보가 없는 모델의 값은 $\log3=1.098612$다.

### 대상으로 한 번 끝까지

이것이 과제의 대상이다. 과제가 요구하는 세 가지 — 행렬, 행 loss 하나, 배치 평균 — 를 카탈로그 숫자로 여기서 먼저 한다.

**내적 아홉 개.** 모든 벡터가 단위 길이이므로 $v_i^\top t_j=\cos\theta_{ij}$이고 세 각은 $0^\circ$, $60^\circ$, $90^\circ$다.

$$V T^\top=\begin{pmatrix}1&1/2&0\\1/2&1&\sqrt3/2\\0&\sqrt3/2&1\end{pmatrix}=\begin{pmatrix}1&0.5&0\\0.5&1&0.866025\\0&0.866025&1\end{pmatrix}.$$

모든 $i$에서 $v_i=t_i$이므로 행렬이 대칭인데, 이것은 D3의 성질이지 대조학습 일반의 성질이 아니다. $\tau=1/2$로 나누면 모든 항이 두 배가 되어 위의 표가 된다.

**행 1, 끝까지.** 이미지 1의 logit은 $(2,1,0)$이므로

$$p_{11}=\frac{e^2}{e^2+e^1+e^0}=\frac{7.389056}{11.107338}=0.665241,\qquad L_{1}=-\log p_{11}=0.407606\ \text{nat}.$$

**세 행 전부, 그리고 반대 방향.** 행 2의 logit은 $(1,2,1.732051)$, 행 3은 $(0,1.732051,2)$이므로

$$L_{1}=0.407606,\qquad L_{2}=0.757448,\qquad L_{3}=0.642002.$$

행렬이 대칭이라 열 loss도 *같은 세 숫자*이고, 따라서 D3에서는 두 방향이 어긋날 수 없다. 목적함수 전체는

$$\mathcal L=\tfrac12\left(\tfrac13\textstyle\sum_i L_i^{\,i\to t}+\tfrac13\sum_i L_i^{\,t\to i}\right)=\tfrac13(0.407606+0.757448+0.642002)=0.602352\ \text{nat}.$$

**그 숫자는 무엇에 대고 재는가.** 아무것도 배우지 못한 $N=3$ 배치는 아홉 칸에 $1/3$씩 두므로 loss가 $\log 3=1.098612$ nat이다. D3는 $0.602352$로 절반이 조금 못 되게 내려와 있고, *바닥*은 $0$인데 $\tau\to0$에서만 닿는다. 그래서 숫자만으로는 말할 수 있는 것이 거의 없다. 같은 encoder가 바로 이 배치에서 $\tau$만으로 $0.933538$과 $0.000001$ 사이 아무 값이나 낸다. 그것을 §5가 측정한다.

**명백히 틀렸다고 할 수 없는 negative.** $\tau=1/2$에서 행 2의 softmax는 $(0.172485,\ 0.468861,\ 0.358654)$다. softmax cross-entropy의 gradient는 $p-y$이므로([[03-deep-learning/foundations/index|1. 학습 시스템 §2]]의 계산) 이 행은 이미지 2를 *캡션 3에서* 가중치 $0.358654$만큼 밀어낸다. 행 전체의 밀어내기, 곧 softmax가 틀린 캡션들에 둔 질량은 $1-0.468861=0.531139$이고, 캡션 3이 그중 $0.358654/0.531139=67.5\%$를 가져간다. 3분의 2이고, 캡션 1의 몫은 3분의 1이다. $30^\circ$ 떨어진 캡션 3이 더 가까운 negative이기 때문이다. 캡션 3이 negative인 이유는 배치의 다른 칸에 있다는 것뿐이고 다른 이유는 없다. 이 숫자를 §2의 false negative 문단과, 캡션 3이 캡션 2의 복사본이 되는 과제 4를 위해 기억해 둔다. 그림이 각도와 이 행을 나란히 놓는다.

<svg viewBox="0 0 560 312" style="max-width:100%;height:auto" role="img" aria-label="D3의 세 이미지와 세 캡션이 단위원 위 0°, 60°, 90°에 겹쳐 있고, 이미지 2는 캡션 1에서 60°, 캡션 3에서 30° 떨어져 있다. τ = 1/2에서 이미지 2의 행 softmax는 0.172485, 0.468861, 0.358654이고, 밀어내기 질량 0.531139 가운데 캡션 3이 67.5%를 가져간다. 점선 호는 이미지 2를 90°로 옮긴 한 쌍이 틀린 배치다">
  <defs><marker id="aVck" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="22" font-size="12" fill="currentColor">(a) 단위원 위의 D3</text>
  <line x1="62" y1="282" x2="276" y2="282" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <line x1="62" y1="282" x2="62" y2="68" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <path d="M 258.0 282.0 A 196 196 0 0 0 62.0 86.0" stroke="currentColor" stroke-width="0.8" fill="none" stroke-opacity="0.35" stroke-dasharray="2 3"/>
  <line x1="62" y1="282" x2="258.0" y2="282.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#aVck)"/>
  <circle cx="258.0" cy="282.0" r="2.6" fill="currentColor"/>
  <text x="258.0" y="300.0" font-size="11" fill="currentColor" text-anchor="end">v<tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">= t</tspan><tspan dy="3" font-size="10">1</tspan><tspan dy="-3" dx="3.5">· 0°</tspan></text>
  <line x1="62" y1="282" x2="160.0" y2="112.3" stroke="currentColor" stroke-width="1.6" marker-end="url(#aVck)"/>
  <circle cx="160.0" cy="112.3" r="2.6" fill="currentColor"/>
  <text x="168.0" y="110.3" font-size="11" fill="currentColor" text-anchor="start">v<tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">= t</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3" dx="3.5">· 60°</tspan></text>
  <line x1="62" y1="282" x2="62.0" y2="86.0" stroke="currentColor" stroke-width="1.6" marker-end="url(#aVck)"/>
  <circle cx="62.0" cy="86.0" r="2.6" fill="currentColor"/>
  <text x="70.0" y="108.0" font-size="11" fill="currentColor" text-anchor="start">v<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">= t</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· 90°</tspan></text>
  <path d="M 116.0 282.0 A 54 54 0 0 0 89.0 235.2" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="120.9" y="252.0" font-size="11" fill="currentColor" text-anchor="middle">60°</text>
  <path d="M 110.0 198.9 A 96 96 0 0 0 62.0 186.0" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="91.0" y="177.8" font-size="11" fill="currentColor" text-anchor="middle">30°</text>
  <path d="M 167.0 100.1 A 210 210 0 0 0 69.3 72.1" stroke="currentColor" stroke-width="1.3" fill="none" stroke-dasharray="5 3" marker-end="url(#aVck)"/>
  <text x="70" y="48" font-size="11" fill="currentColor">v<tspan dy="3" font-size="10">2</tspan><tspan dy="-3">′: 한 쌍이 틀린 배치(§5),</tspan></text>
  <text x="70" y="62" font-size="11" fill="currentColor">90°로, t<tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">위에 놓인다</tspan></text>
  <text x="290" y="72" font-size="12" fill="currentColor">(b) τ = 1/2에서 이미지 2의 행</text>
  <text x="384" y="109" font-size="11" fill="currentColor" text-anchor="end">캡션 1, 60° 떨어짐</text>
  <rect x="392" y="96" width="37.9" height="18" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="0.8"/>
  <text x="435.9" y="109" font-size="11" fill="currentColor">0.172485</text>
  <text x="384" y="143" font-size="11" fill="currentColor" text-anchor="end">캡션 2, 제 짝</text>
  <rect x="392" y="130" width="103.1" height="18" fill="currentColor" fill-opacity="0.34" stroke="currentColor" stroke-width="0.8"/>
  <text x="501.1" y="143" font-size="11" fill="currentColor">0.468861</text>
  <text x="501.1" y="157" font-size="10" fill="currentColor" fill-opacity="0.8">positive</text>
  <text x="384" y="177" font-size="11" fill="currentColor" text-anchor="end">캡션 3, 30° 떨어짐</text>
  <rect x="392" y="164" width="78.9" height="18" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="0.8"/>
  <text x="476.9" y="177" font-size="11" fill="currentColor">0.358654</text>
  <text x="476.9" y="191" font-size="10" fill="currentColor" fill-opacity="0.8">어려운 negative</text>
  <line x1="392" y1="90" x2="392" y2="194" stroke="currentColor" stroke-width="0.9"/>
  <text x="290" y="222" font-size="11" fill="currentColor">코사인: 캡션 1과 0.5, 캡션 3과 0.866025</text>
  <text x="290" y="240" font-size="11" fill="currentColor">밀어내기 질량 1 − 0.468861 = 0.531139</text>
  <text x="290" y="258" font-size="11" fill="currentColor" font-weight="bold">캡션 3의 몫 0.358654/0.531139 = 67.5%</text>
  <text x="290" y="276" font-size="11" fill="currentColor" fill-opacity="0.85">더 가까운 negative가 더 세게 밀린다</text>
</svg>

D3의 이미지와 캡션은 단위원 위 $0^\circ$, $60^\circ$, $90^\circ$에 겹쳐 있으므로, 이미지 2는 캡션 1에서 $60^\circ$(코사인 $0.5$), 캡션 3에서는 $30^\circ$(코사인 $0.866025$)밖에 떨어져 있지 않다. $\tau=1/2$에서 그 행 softmax는 $(0.172485,\ 0.468861,\ 0.358654)$이고, 밀어내기 질량 $0.531139$ 가운데 더 가까운 캡션 3이 $67.5\%$를 가져간다. 점선 호는 이미지 2를 $90^\circ$, 곧 캡션 3 위로 옮긴, §5와 과제 1–2의 한 쌍이 틀린 배치다.

### 1. 세 VLM 계열

꽤 다른 기계 셋이 모두 VLM이라 불리고, 그중 어느 것을 쓸 수 있었는지는 대개 논문의 과제가 정했다. 셋의 실무적 차이는 비용이고, 비용은 두 모달리티가 어디서 만나는지에서 따라 나온다.

- dual encoder: 따로 encoding해 similarity로 retrieval·zero-shot 분류.
- fusion model: cross-attention으로 token을 섞어 pair reasoning.
- generative model: 시각 표현을 조건으로 language token 생성. 유창함은 grounding 증거가 아니다.

dual encoder는 이미지 벡터 $N$개와 텍스트 벡터 $M$개를 한 번 계산해 두고 어떤 쌍이든 내적 하나로 점수를 매기므로, 질의 하나를 백만 장에 대해 순위 매기는 일이 곱셈덧셈 백만 번이다. fusion model은 쌍마다 결합 신경망을 한 번씩 돌려야 하므로 같은 순위 매기기가 순전파 백만 번이다. 검색 시스템이 dual encoder 위에 세워지는 이유이고, fusion model이 쌍 집합이 작은 곳에 나타나는 이유다. 품질을 들먹이지 않고도, 논문의 과제가 어떤 구조를 강요했는지 설명해 준다.

**D3에서 본 zero-shot 분류.** dual encoder는 검색으로 분류한다. 클래스마다 캡션을 하나씩 쓰고, 각각 한 번 임베딩한 뒤, 이미지에 가장 가까운 캡션을 고른다. D3의 캡션 셋을 클래스 프롬프트 셋으로 읽으면 이미지 2의 코사인은 $(0.5,\ 1,\ 0.866025)$이므로 클래스 2로 맞게 분류된다. 그러나 클래스 3과의 차이는 $1-0.866025=0.133975$, 두 벡터 사이의 $30^\circ$뿐이다. $\tau=1/2$에서 그 차이는 확률 $0.468861$이 되어 절반에 못 미치는데도 결정은 여전히 맞다. $\tau$로 나누는 것은 arg max를 결코 옮기지 않기 때문이다. 이 계열이 내놓는 것은 순위이고, 그 확률은 순위가 무시하는 손잡이에 달려 있다(§2의 temperature 상자). [[01-canonical-papers/notes/3-vlm/clip|CLIP]]은 이 절차를 규모로 키운 것이다. 웹의 이미지–텍스트 쌍 $4$억 개로 학습해, ImageNet의 학습 label을 하나도 쓰지 않은 zero-shot으로 원래의 지도학습 ResNet-50과 맞먹었다.

**나머지 두 계열이 사는 것.** fusion model은 이미지와 텍스트를 함께 읽는다. 텍스트 토큰이 cross-attention으로 이미지 패치를 참조하므로([[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer §1]]), 캡션의 어느 단어가 어느 물체를 가리키는지처럼 각도 하나로는 매길 수 없는 것을 채점할 수 있다. generative model은 캡션을 채점하는 대신 쓴다. 토큰마다 순차 디코더 패스가 하나이므로, 이미지를 읽은 뒤 $20$토큰짜리 답에 패스 $20$번이 든다. 유창함은 이미지에 conditioned되어 있다는 증거이고, grounded인지는 §3의 별개 질문이다. §6은 세 계열을 모달리티가 만나는 곳에 따라 다시 정렬한다.

### 2. 대조학습 계산

dual encoder에게는 짝은 있어도 label이 없다. 그래서 각 이미지가 배치 안에서 자기 캡션을 골라내게 하고, 배치의 다른 캡션은 모두 오답으로 친다. 계산 절이 D3의 세 행에서 이것을 손으로 했다. 어떤 배치에나 쓰이게 적으면 CLIP식 목적함수 전체는 image→text와 text→image cross-entropy를 배치에 대해 평균한다. 배치의 다른 항목은 막연한 "틀린 언어"가 아니라 표본으로 뽑힌 negative이므로, false negative와 배치 구성이 무엇을 배우는지를 바꾼다.

이것이 목적함수 전체이므로, 서술하지 말고 기호를 모두 달아 적을 가치가 있다.

> **대조(InfoNCE) 목적함수의 정의.** **대조 목적함수**는 *배치 위의 분류 loss*다. 각 항목의 과제는 줄 세운 후보 중에서 자기 짝을 고르는 것이다. 거리도 아니고, 목표 임베딩으로의 회귀도 아니고, 혼자서 최대화되는 유사도도 아니다. 정의 조건 넷이고, 하나만 빠져도 숫자의 뜻이 달라진다. **positive는 가정에 의해 대각선**이다. 짝은 배치를 어떻게 모았는가에서 나오지, 대각선 밖이 어긋난 쌍이라는 판단에서 나오지 않는다. **negative는 배치의 나머지**이므로 loss가 $N$과 어떤 항목이 함께 뽑혔는가에 의존한다. **logit을 temperature $\tau$로 비례 조정**한 뒤 softmax를 걸므로 같은 임베딩이 $0$과 $\log N$ 사이 아무 loss나 낼 수 있다. 그리고 image→text와 text→image **두 방향에 대해 대칭화**되는데, 같은 행렬 위의 서로 다른 두 분류 문제다.
>
> $$\mathcal L=\frac{1}{2N}\sum_{i=1}^{N}\left[-\log\frac{\exp(v_i^\top t_i/\tau)}{\sum_{j=1}^{N}\exp(v_i^\top t_j/\tau)}\;-\;\log\frac{\exp(v_i^\top t_i/\tau)}{\sum_{j=1}^{N}\exp(v_j^\top t_i/\tau)}\right]$$
>
> $N$은 배치 크기, $v_i\in\mathbb R^{d}$는 이미지 $i$의 L2 정규화된 임베딩, $t_j$는 캡션 $j$의 것이라 각 $v_i^\top t_j$가 $[-1,1]$의 코사인이다. $\tau>0$은 temperature이고, 첫 분수는 similarity matrix의 **행** $i$를 따라, 둘째는 **열** $i$를 따라 정규화한다. $1/(2N)$이 두 방향을 배치에 대해 평균하므로 목적함수가 둘이 아니라 하나의 스칼라가 된다.
>
> - **예**: $\tau=1/2$의 D3는 행 loss $(0.407606,\,0.757448,\,0.642002)$, 같은 열 loss, $\mathcal L=0.602352$ nat이다. 정보가 없을 때의 값은 $\log 3=1.098612$다.
> - **비예**: 맞는 쌍의 유사도만 더한 $\sum_i v_i^\top t_i$의 최대화. 위로 유계가 아니고, 모든 임베딩을 한 벡터로 뭉개면 자명하게 풀린다. 붕괴를 막는 유일한 것이 분모이고, 그래서 "모델이 이미지와 텍스트를 정렬하도록 배운다"는 방법의 불완전한 서술이다.
> - **비예**: "맞다/아니다"의 쌍별 이진 loss. 쌍을 독립으로 채점하므로 $N$에 의존하지도 않고 순위 오류를 벌하지도 않는다. D3에서 답이 같더라도 둘은 바꿔 쓸 수 없다.
> - **비예**: 대칭 *거리*. $\mathcal L$은 이미지와 텍스트에 대해 구성상 대칭이 아니다. 두 방향을 더해서 대칭으로 만든 것이고, similarity matrix가 대칭이 아닌 배치에서는 두 항이 다르다. D3는 $v_i=t_i$라 같을 뿐이다.
> - **왜 중요한가**: $\log N$이 한 배치가 보증할 수 있는 양의 천장이다. 표준 InfoNCE 경계(van den Oord 외 2018; Poole 외 2019)는 배치에 대한 기댓값에서 $I(V;T)\ge\log N-\mathbb E[\mathcal L]$이므로, 배치 3은 encoder가 아무리 좋아도 상호정보량을 최대 $1.098612$ nat, 약 $1.584963$ bit까지만 보증한다. 대조학습 논문이 배치 크기를 수만 단위로 보고하는 이유가 optimizer 민담이 아니라 이것이다. 상호정보량 자체는 [[02-foundations/information-theory|5. 정보이론 §4]]에 있다.

> **Temperature의 정의.** **Temperature** $\tau$는 *softmax 앞에서 모든 logit을 나누는 양의 스칼라*다. 목적함수의 성질이지 쌍의 성질도, encoder의 성질도, learning rate도 아니다. 정의 조건 셋. **행렬 전체가 공유**하므로 어떤 쌍이 다른 쌍보다 확실하다는 것을 표현할 수 없다. softmax가 평행이동 불변이므로([[03-deep-learning/foundations/index|1. 학습 시스템 §1]]) **logit 차이를 통해서만** 작용하고, $\tau$를 반으로 줄이면 모든 간격이 한꺼번에 두 배가 된다. 그리고 **모델을 바꾸지 않고 loss만 바꾼다**. 양수로 나누는 것은 순서를 보존하므로 임베딩도, 순위도, 모든 retrieval 결정도 $\tau$에 손대지 않는다.
>
> $$p_{ij}=\frac{\exp(v_i^\top t_j/\tau)}{\sum_{k}\exp(v_i^\top t_k/\tau)},\qquad \tau\to\infty\Rightarrow p_{ij}\to\frac1N,\qquad \tau\to0\Rightarrow p_{ij}\to\mathbf 1\big[j=\arg\max_k v_i^\top t_k\big]$$
>
> 두 극한이 §5 sweep의 양끝이다. 하나는 loss가 $\log N$인 균등분포, 다른 하나는 arg max가 positive이면 loss가 $0$이고 아니면 위로 유계가 아닌 딱딱한 arg max다.
>
> - **예**: $\tau=1/2$에서 D3의 행 1은 $p_{11}=0.665241$이고, $\tau=1/4$이면 같은 내적이 logit $(4,2,0)$을 주어 $p_{11}=0.866813$이 된다. 임베딩은 움직이지 않았다.
> - **비예**: confidence calibration. 작은 $\tau$는 학습 분포를 날카롭게 할 뿐, top-1 retrieval이 얼마나 자주 맞는지는 말하지 않는다. 그것은 recall@$k$가 잰다([[02-foundations/ml-practice|9. ML 실무 §3]]).
> - **비예**: learning rate. 둘 다 "학습을 얼마나 과감하게 할지 조절하는" 양의 스칼라이고 닮은 점은 거기까지다. $\eta$는 *스텝*의 크기를, $\tau$는 *loss 지형*의 모양을 바꾼다. 실제 CLIP 계열에서는 $\tau$가 학습되는 파라미터이고 $\eta$는 결코 그렇지 않다.
> - **왜 중요한가**: $\tau$가 gradient를 negative들에게 어떻게 배분할지 정한다. 큰 $\tau$는 밀어내기 질량을 거의 균등하게 퍼뜨리고, 작은 $\tau$는 가장 어려운 negative 하나에 몰아준다. 배치에 틀린 쌍이 하나라도 있으면 §5의 sweep이 단조가 아닌 이유가 이것이다. 그때 가장 어려운 negative는 모델이 가장 확신을 가지고 틀린 대상이다.

### 3. Conditioning은 grounding이 아니다

모델은 밸브의 픽셀을 쓰지 않고도 "red valve"라고 맞힐 수 있고, 그다음 그 밸브로 손을 뻗어야 하는 로봇은 모델이 그 픽셀을 썼는지 알아야 한다. 이미지가 출력 분포를 바꾸면 conditioning이다. grounding은 주장이나 token이 국소 시각 증거에 지지되는지 추가로 묻는다. caption likelihood, retrieval 정확도, VQA 정확도(visual question answering: 이미지에 관한 질문 가운데 맞게 답한 비율), hallucination 비율(이미지에 없는 물체나 속성을 말한 출력의 비율), spatial grounding은 서로 다른 능력을 잰다.

이 절 전체를 그 두 단어가 떠받치므로, 대비가 아니라 정의를 둘 다 붙인다.

> **Conditioning과 grounding의 정의.** **Conditioning**은 *모델 출력 분포의 성질*이다. 입력을 바꾸면 분포가 바뀔 때 그 입력에 조건화되어 있다고 한다. **Grounding**은 *특정 출력과 특정 증거가 함께 가지는 성질*이다. token이나 주장이 이 이미지 안의 식별 가능한 시각 증거에 지지될 때 grounded라고 한다. 앞은 함수에 대한 진술이고 뒤는 사례에 대한 진술이다. 그래서 하나는 ablation으로 확립할 수 있고 다른 하나는 그럴 수 없다.
>
> $$x\text{에 조건화:}\ \exists\,x,x'\ \text{s.t.}\ p(y\mid x)\ne p(y\mid x')\qquad\text{대}\qquad\text{grounded: }y\text{의 근거가 }x\text{의 한 영역에 있다}$$
>
> $x$는 이미지, $y$는 출력이다. 왼쪽은 입력에 대한 *존재* 주장이고 오른쪽은 출력 하나에 대한 주장이므로, 왼쪽을 아무리 많이 모아도 오른쪽이 따라 나오지 않는다.
>
> - **Grounding 없는 conditioning의 예**: 실내 사진보다 실외 사진에서 "말을 탄 사람"이라고 더 자주 말하는 captioner. 이미지가 분포를 바꾸고 있으므로 조건화되어 있다. 사진에 말이 있는지는 별개의 질문이다.
> - **둘을 가르는 실험의 예**: 이미지에 개입한다. 주장이 가리키는 영역을 가리거나 옮기거나 색을 바꾸고 주장이 따라가는지 본다. valve를 파랗게 칠했는데 답이 그대로인 모델은 valve의 색을 읽고 있지 않았다.
> - **비예**: 벤치마크에서의 높은 정확도. 그 질문에 "red valve"가 학습 분포의 최빈 답이면 언어 prior만으로 시각 증거 없이 맞힐 수 있고, 정확도는 둘을 구별하지 못한다.
> - **비예**: 맞는 영역 위의 attention map. attention은 계산이 *어디를 보았는지*를 보이지 답이 *무엇에 의존했는지*를 보이지 않는다. 둘은 흔히 어긋나고, 그래서 증거로는 시각화보다 개입이 낫다.
> - **왜 중요한가**: 로봇에게 이 차이는 label과 target의 차이다. 조건화된 label은 평균적으로 맞으면서도 팔이 어디로 갈지 말해 주지 못한다. grounded label은 픽셀과 함께 오고 따라서 제어기가 필요로 하는 frame과 함께 온다([[04-robotics/geometric-perception-calibration|3.5 기하 인식 §1]]).

### 4. 로봇으로의 연결

VLM은 의미 label, 언어 목표, reward, VLA backbone을 줄 수 있지만 제어 주기·행동 가능성·recovery를 자동으로 주지 않는다.

쓰임마다 모델의 다른 부분에 기대고, D3의 숫자가 저마다 어디서 오도할 수 있는지 보여 준다. **의미 label** — "밸브"가 어느 물체인가 — 로 쓰면 VLM은 순위로 답하고, 그것이 dual encoder가 잘하는 일이다. **목표나 성공 판정기**로 쓰면 유사도를 예·아니오로 바꿔야 하고, 그러려면 로봇 자신의 장면에서 정한 임계값이 필요하다. 이미지 2는 캡션 2와 정확히 맞아 코사인이 $1$인데도 $\tau=1/2$에서 캡션 셋에 대한 확률은 $0.468861$이다. 절반을 넘을 때 켜지는 판정기는 완벽한 일치를 실패라 부르고, $\tau=1/4$에서는 같은 임베딩이 $0.581234$를 주어 장면이 하나도 바뀌지 않았는데 판정이 뒤집힌다. **reward**로 쓰면 코사인은 정밀함이 필요한 곳에서 가장 평평하다. 임베딩을 캡션에서 $60^\circ$ 떨어진 곳에서 $0^\circ$로 돌리면 $0.5$를 얻지만, 그 마지막 $10^\circ$가 주는 것은 $0.015192$, 그중 3퍼센트뿐이다. **backbone**으로 쓰면 특징은 주지만 주기는 주지 않는다. VLM을 정책으로 바꾼 7B의 OpenVLA는 행동 토큰을 하나씩 디코드하느라 $6\,\mathrm{Hz}$ 근처에서 막히고, π0는 action expert가 시작하기 전에 관측을 한 번 지나는 데 $32\,\mathrm{ms}$를 쓴다([[03-deep-learning/vla/index|4. VLA §6]]).

[[01-canonical-papers/notes/3-vlm/clip|CLIP]]을 먼저 읽고, fusion·generative 항목과 [[03-deep-learning/vla/index|VLA 교과]]로 간다. 그런 backbone을 적응시키는 법 — 전체 파인튜닝이나 LoRA, 그리고 각각이 메모리와 연산에서 치르는 비용 — 은 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §8]]에 있다.

### 5. 실습: temperature가 하는 일과, 그 대상

대조학습 논문들은 $\tau$를 튜닝하는데, 보고되는 loss는 encoder가 나아졌든 아니든 $\tau$를 따라 움직인다. 그래서 loss 곡선을 증거로 치기 전에 temperature 하나가 무엇을 하는지, 그리고 어느 배치에 하는지부터 알아야 한다. 손잡이 하나, 배치 둘. 영어 절 코드 1부는 계산 절을 재현한다. 2부는 encoder가 이미 풀어 놓은 정렬된 D3와, 이미지 2를 $90^\circ$로 옮긴 "한 쌍 틀린" 배치에 대해 $\tau$를 훑는다. 요점은 한 쌍 틀림 열이다. 완벽한 배치에서 sweep은 단조이고 아무것도 말하지 않는다. $\tau$에 대해 의견을 가지는 것은 실수가 섞인 배치뿐이다.

**Sweep.** $p_{ii}$는 행 softmax가 맞는 캡션에 둔 확률이고 $\mathcal L$은 nat 단위의 대칭화된 목적함수다. 정보가 없을 때의 값은 $\log 3=1.098612$다.

| $\tau$ | $p_{11}$ | $p_{22}$ | $p_{33}$ | 대각 평균 $p$ | $\mathcal L$ 정렬 | $\mathcal L$ 한 쌍 틀림 |
|---:|---:|---:|---:|---:|---:|---:|
| $2$ | $0.419229$ | $0.368459$ | $0.393432$ | $0.393706$ | $0.933538$ | $0.932611$ |
| $1$ | $0.506480$ | $0.403040$ | $0.445933$ | $0.451818$ | $0.798859$ | $0.805616$ |
| $1/2$ | $0.665241$ | $0.468861$ | $0.526238$ | $0.553447$ | $0.602352$ | $0.644393$ |
| $1/4$ | $0.866813$ | $0.581234$ | $0.623652$ | $0.690566$ | $0.385899$ | $0.527329$ |
| $1/10$ | $0.993262$ | $0.788239$ | $0.792420$ | $0.857974$ | $0.159126$ | $0.535171$ |
| $1/20$ | $0.999955$ | $0.935766$ | $0.935806$ | $0.957175$ | $0.044261$ | $0.699810$ |
| $1/100$ | $1.000000$ | $0.999998$ | $0.999998$ | $0.999999$ | $0.000001$ | $2.463960$ |

**Sweep 읽기.** 행 1의 계산이 알려줄 수 없었던 것 넷.

- **이미 풀어 놓은 배치에서 $\tau$를 낮추는 것은 확신을 사는 일일 뿐이다.** 정렬 열은 $\tau=2$의 $0.933538$에서 $\tau=1/100$의 $0.000001$까지 단조로 내려가고, 격자 탐색도 최소가 범위의 아래 끝에 있음을 확인한다. 배운 것은 없다. 같은 벡터 여섯 개가 여섯 자릿수를 넘나드는 loss를 냈다. $\tau$와 $N$ 없이 인용된 대조 loss는 비교 가능한 숫자가 아니고, $\tau$를 튜닝하는 논문의 loss 그래프도 마찬가지다.
- **퍼짐은 행마다 다르고, 그것이 기하다.** $\tau=1/2$에서 $p_{11}=0.665241$인데 $p_{22}=0.468861$이다. 이미지 2는 캡션 1에서 $60^\circ$, 캡션 3에서는 $30^\circ$밖에 떨어져 있지 않아 진짜 어려운 negative를 가지고 있고 이미지 1은 그렇지 않다. 표의 모든 temperature에서 행 2가 가장 어려운 행이다. hard negative는 임베딩 기하의 성질이지 샘플링 코드의 성질이 아니다.
- **한 쌍이 틀리면 loss는 $\tau$에 대해 단조가 아니고 내부 최소를 가진다.** 오른쪽 열은 $\tau=1/4$의 $0.527329$까지 내려갔다가 돌아서서 $\tau=1/100$에서 $2.463960$에 이른다. 정보가 없을 때의 $\log 3$보다 나쁘다. $\tau\in[0.01,3]$ 격자 탐색은 최소를 $\tau=0.1639$, $\mathcal L=0.507409$에 둔다. 날카롭게 하는 것은 모델이 믿는 것을 증폭하는 일이고, 최적점 아래에서는 실수를 증폭한다.
- **$\tau$가 충분히 크면 오류가 완전히 숨는다.** $\tau=2$에서 틀린 encoder는 $0.932611$로 맞는 encoder의 $0.933538$보다 근소하게 *낫다*. 두 곡선은 $\tau\approx1.6542$에서 교차한다. 그 위에서는 softmax가 너무 평평해 $30^\circ$의 인코딩 오류가 loss에 보이지 않는다. 학습 곡선을 encoder가 잘 작동한다는 증거로 쓸 때마다 기억할 일이다.

### 6. 모달리티가 만나는 곳: VLM에서 옴니모달까지

§1은 시각–언어 모델을 무엇을 내놓는지로 갈랐다. 모든 멀티모달 모델은 *모달리티가 어디서 만나는지*로도 자리를 정할 수 있고, 그 선택 하나가 무엇을 생성할 수 있는지, 비용이 얼마인지, 로봇의 행동이 거기 합류할 수 있는지를 정한다. D3는 가장 늦은 만남이다. 이미지와 캡션은 서로를 보지 않고, 내적 하나 $\ell_{ij}=v_i^\top t_j/\tau$에서만 만난다.

| 만나는 곳 | 방식 | 예 | 사는 것 | 치르는 것 |
|---|---|---|---|---|
| 끝에서 | 인코더 둘과 유사도 하나 | [[01-canonical-papers/notes/3-vlm/clip\|CLIP]], D3 | 내적 값만으로 백만 개를 순위 매김 | 생성이 없고, 한 쌍에 대해 각도 하나 이상은 모른다 |
| 다리를 거쳐 | 시각 특징이 cross-attention, 작은 질의 트랜스포머, 또는 토큰 공간으로의 투영을 거쳐 언어 모델로 들어간다 | [[01-canonical-papers/notes/3-vlm/flamingo\|Flamingo]], [[01-canonical-papers/notes/3-vlm/blip-2\|BLIP-2]], [[01-canonical-papers/notes/3-vlm/llava\|LLaVA]], [[01-canonical-papers/notes/3-vlm/paligemma\|PaliGemma]] | 이미지에 대해 생성한 텍스트 | 이미지는 읽기만 하고 생성하지 못한다. 쌍마다 결합 패스 한 번 |
| 한 시퀀스 안에서 | 모든 모달리티가 한 트랜스포머의 위치가 된다 — 이산 코드로(Chameleon), 또는 디퓨전 손실로 학습하는 연속 패치로(Transfusion) | Chameleon(2024); Transfusion(2024) | 어떤 순서로 섞여도 이미지와 텍스트를 읽고 생성 | 이미지 하나가 위치를 많이 차지한다. 이산 코드는 세부를 잃고, Transfusion은 양자화한 이미지 토큰 위의 모델보다 스케일이 낫다고 보고한다 |
| 옴니모달 | 한 시퀀스 설계를 오디오와 비디오로, 입력과 출력 모두로 넓혀 끝에서 끝까지 학습 | GPT-4o(2024); Qwen2.5-Omni(2025) | 인식하고 말로 답하는 신경망 하나 | 가장 긴 시퀀스. 오디오와 비디오는 초마다 위치를 더한다 |

D3에서는 그 차이를 셀 수 있다. 이미지 셋과 캡션 셋은 인코더 패스 여섯 번이면 되고, 그다음 아홉 쌍 전부를 내적으로 채점한다. 모달리티를 한 시퀀스에서 만나게 하는 모델은 같은 아홉 점수에 결합 패스 아홉 번이 들고, 그 대가로 한 쌍이 *왜* 맞는지 말하거나 캡션을 직접 쓸 수 있다. §1의 비용 논증을 끝까지 밀고 간 것이다. 아래의 접힌 메모는 표의 두 옴니 모델이 안에서 어떻게 돌아가는지, 한 시퀀스 설계가 어디서 왔는지 말한다.

> [!note]- 더 깊이 · Deeper
> **옴니 모델, 짧게.** GPT-4o는 텍스트·오디오·이미지·비디오를 어떻게 섞어도 받고, 그 모두로 학습한 신경망 하나에서 텍스트·오디오·이미지를 낸다. 시스템 카드는 말에 대한 응답이 빠르면 $232$ ms, 평균 $320$ ms라고 보고한다. 사람이 대꾸하는 지연이다([OpenAI, 2024](https://arxiv.org/abs/2410.21276)). Qwen2.5-Omni는 일을 나눠 텍스트와 음성을 동시에 흘려보낸다. 언어 모델인 *Thinker*가 텍스트를 쓰고, *Talker*가 Thinker의 은닉 상태를 오디오 토큰으로 바꾸며, 시간에 맞춘 위치 임베딩이 섞인 비디오와 오디오의 박자를 맞춘다([Qwen, 2025](https://arxiv.org/abs/2503.20215)). 조기 결합의 조상은, [[03-deep-learning/diffusion/vae-gan|6.1 §10]]과 같은 종류의 코드북으로 이미지를 토큰화하는 Chameleon([Chameleon Team, 2024](https://arxiv.org/abs/2405.09818))과, 트랜스포머 하나를 텍스트에는 다음 토큰 예측으로, 이미지에는 디퓨전으로 학습하는 Transfusion([Zhou 외, 2024](https://arxiv.org/abs/2408.11039))이다.

**행동은 모달리티가 하나 더 느는 것이다.** 저자들의 말로 π0의 구조는 Transfusion — 트랜스포머 하나에 이산 토큰은 cross-entropy 손실, 연속 토큰은 flow matching 손실 — 에서 영감을 받았고, 여기에 로봇의 상태·행동 토큰을 위한 가중치 한 벌을 따로 더했다. [[03-deep-learning/vla/index|4. VLA §6]]의 Mixture of Transformers다. 출발점은 답을 토큰 하나씩 쓰는 3B VLM인 PaliGemma이고, 자기 행동 토큰은 flow matching으로 지도한다. 신경망이 무작위 노이즈를 적분 몇 스텝 만에 행동 청크로 바꾸도록 배우는 방식으로, 같은 §6의 노이즈 제거기 계열이다([[01-canonical-papers/notes/4-vla/pi0|π0]]). 그러니 VLA는 조기 결합 모델 — 표의 셋째 줄처럼 모달리티가 한 시퀀스 안에서 만나는 모델 — 에 출력 모달리티로 행동이 더해진 것이고, Gemini Robotics는 대형 멀티모달 모델인 Gemini 2.0 위에 곧바로 그것을 지었다([Gemini Robotics Team, 2025](https://arxiv.org/abs/2503.20020)). 입력도 같은 방식으로 넓어진다. ManiWAV는 그리퍼에 마이크를 달아 오디오와 비디오를 함께 써서 접촉이 많은 기술을 배웠다. 시각만으로는 모호했던 접촉 사건과 표면 재질을 소리가 실어 날랐기 때문이다([Liu 외, 2024](https://arxiv.org/abs/2406.19464)). 건설 현장은 그것이 중요한 곳이다 — 시끄럽고, 어수선하고, 자주 어둡다 — 그리고 작업자의 말로 된 지시가 자연스러운 인터페이스인 곳이다. 그러니 로봇 논문의 "옴니모달"은 두 질문으로 읽어라. 어떤 모달리티가 들어가는가, 그리고 나오는 것 가운데 행동이 있는가.

### 스스로 점검 · Self-check

1. D3에서 image→text loss와 text→image loss가 같은 이유는 무엇이고, 그것은 대조학습의 성질인가.
2. 배치가 $N=3$이다. 이 목적함수가 보증할 수 있는 상호정보량의 최대는 얼마이고 왜 그런가.
3. $\tau$를 $1/2$에서 $1/4$로 낮추면 $p_{11}$이 $0.665$에서 $0.867$이 된다. 어떤 retrieval 결정이 바뀌었는가.
4. 행 2는 질량의 $0.359$를 캡션 3에서 밀어낸다. 그것이 올바른 지도가 되려면 캡션 3에 대해 무엇이 참이어야 하는가.
5. 모델이 "red valve"를 맞혔다. conditioning과 grounding을 가르는 실험을 말하고, 더 높은 정확도가 그것을 대신할 수 없는 이유를 말하라.
6. 어느 로봇 논문이 이미지·언어·오디오를 받는다는 이유로 자기 모델을 "옴니모달"이라 부른다. §6의 어떤 두 질문이 그것의 자리를 정하며, VLA가 되려면 무엇이 참이어야 하는가?

> [!tip]- 정답 · Answers
> 1. 모든 $i$에서 $v_i=t_i$라 similarity matrix가 대칭이고 전치해도 달라지지 않기 때문이다. 방법의 성질이 아니라 이 대상의 성질이다. 맞는 쌍이 정확히 정렬되지 않은 배치는 두 방향 loss가 다르고, 그래서 목적함수가 둘을 더한다.
> 2. $\log 3=1.098612$ nat, 약 $1.584963$ bit다. InfoNCE 경계가 $I\ge\log N-\mathbb E[\mathcal L]$이고 $\mathcal L\ge0$이므로, encoder와 무관하게 배치 크기가 보증서의 상한이다.
> 3. 아무것도 바뀌지 않았다. 양수로 나누는 것은 logit 순서를 보존하므로 모든 arg max, 모든 순위, 따라서 모든 recall@$k$가 그대로다. 움직인 것은 loss뿐이다.
> 4. 캡션 3이 이미지 2를 서술하지 않아야 한다. D3에서 그것은 확인된 것이 아니라 가정이다. 배치를 그렇게 만들었으므로 성립할 뿐이다. 과제의 중복 캡션 변형이 그 가정이 거짓이고 gradient가 실제로 틀린 경우다.
> 5. 이미지에 개입한다. valve를 가리거나 색을 바꾸고 답이 따라가는지 본다. 정확도로 대신할 수 없는 이유는, valve에 "red"라고 답하는 언어 prior가 시각 증거 없이도 좋은 점수를 받기 때문이다. 벤치마크 숫자는 두 설명 모두와 양립한다.
> 6. 모달리티가 어디서 만나는지 — 끝에서, 다리를 거쳐, 한 시퀀스 안에서 — 그리고 어떤 모달리티를 *내놓는지*다. 이미지·언어·오디오를 받는다는 것은 무엇을 지각하는지만 말한다. 행동이 출력에 있고, 행동에 대한 손실로 학습되며, 제어 주기로 돌 때에만 VLA다. 그렇지 않으면 다른 누군가의 정책을 먹이는 인식 모델이고, 그 "옴니"는 손이 아니라 귀를 말한다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[03-deep-learning/lab-objects|0. Lab Objects]]만 쓴다. D3와 두 변형은 대상 절에 고정되어 있다. 문제 1–2는 §5가 loss 하나만 찍고 행과 열은 한 번도 펼쳐 보이지 않는 $\tau=1/2$의 한 쌍 틀린 배치를 열고, 문제 4는 §5가 한 번도 돌리지 않는 중복 캡션 변형을 쓰므로 실습의 숫자를 그대로 옮길 수 없다.

1. **그리기.** 위의 그림을 한 쌍이 틀린 배치 — 이미지 2를 $90^\circ$에 인코딩한 것 — 에 대해 $\tau=1/2$로 다시 그린다. $3\times3$ logit 행렬에 대각선만 positive로 음영을 넣고, 그 앞에 $\tau$ 나눗셈을 두고, 같은 행렬에서 나가는 두 화살표로 행 softmax와 열 softmax를 그려 각 화살표 끝에 loss 셋씩을 적고, 배치 상자를 두른다. 각 행이 1위로 매기는 칸에 동그라미를 치고, 넷째 쌍이 칸을 어디에 더하는지, 더해진 칸 가운데 어느 것이 negative가 되는지 표시한다.
2. **유도.** 같은 배치에서 (a) logit 행렬과, 그것이 더는 대칭이 아닌 이유, (b) 행 loss 셋, 열 loss 셋, 그리고 §5의 한 쌍 틀림 열과 맞춰 본 $\mathcal L$, (c) 행 2의 softmax, 그 행이 1위로 매기는 캡션, 그리고 밀어내기 질량 가운데 캡션 3이 가져가는 몫을 D3의 $67.5\%$와 견준 것.
3. **해석.** VLM에게 S1 패널의 "왼쪽 볼트 구멍"을 가리키라고 했다. S1은 건설 트랙의 외장 패널 과제이고, 그 패널에는 $400$ mm 떨어진 체결 구멍이 둘 있다([[05-construction-robotics/site-engineering|2.5]]). 시험 이미지 $20$장 모두에서 왼쪽 구멍을 짚었는데, 이미지는 모두 같은 삼각대에서 찍었다. (a) 아직 열려 있는 주장은 무엇인가? (b) grounding을 학습된 위치와 가를 이미지 개입 둘을 설계하고, 각 개입에서 grounded된 답이 무엇을 해야 하는지 말하라. (c) "왼쪽"이 "빨간"보다 grounding하기 어려운 단어인 이유는?
4. **실행.** 영어 절 템플릿의 `?`를 채우고 **중복 캡션** 변형을 돌린다. 캡션 3이 캡션 2의 정확한 복사본이므로 $t_3=t_2$이고 이미지는 그대로다. $\tau\in\{2,1,1/2,1/4,1/10,1/20,1/100\}$을 훑어 (a) 각 $\tau$의 $\mathcal L$, (b) $\tau=1/2$과 $\tau=1/100$에서의 image→text 행 loss 셋과 text→image 열 loss 셋, (c) 격자 탐색으로 $\mathcal L$을 최소화하는 $\tau$를 보고한다. 그리고 두 문장으로 답한다. 여섯 loss 중 $\tau\to0$에서 위로 유계가 아닌 것은 무엇이고 $\log 2$로 수렴하는 것은 무엇이며, 그 차이는 중복 캡션이 두 방향을 서로 다르게 망가뜨리는 방식에 대해 무엇을 말하는가.

> [!note]- 그리는 법 · How to draw it
> - 대각선만 positive로 표시하고 그 밖에는 아무것도 표시하지 않는다. 대각선 밖의 모든 칸은 그 쌍이 틀렸다는 어떤 증거 때문이 아니라 *배치를 그렇게 구성했기 때문에* negative다. loss 전체가 이 가정 하나에 얹혀 있고, 중복 캡션 변형이 그 가정이 깨졌을 때의 모습이다.
> - 행렬 둘이 아니라 같은 행렬에서 나오는 화살표 둘을 그린다. 행 softmax와 열 softmax는 동일한 숫자를 두 방향으로 읽는다. 행렬을 둘 그리면 모델이 둘이라고 주장하는 셈인데, 모델은 하나이고 채점이 둘이다.
> - $\tau$ 나눗셈은 softmax 앞에, 행렬 전체에 그린다. temperature는 쌍의 성질도 encoder의 성질도 아니다. 모든 칸을 한꺼번에 비례 조정하므로 §5가 그것을 떼어 내 훑을 수 있다.
> - 배치 경계는 모든 칸을 감싸는 상자로 그린다. 상자 밖에는 negative가 없다. 항목 3개에 대한 loss와 32,768개에 대한 같은 loss는 다른 함수이고, 그 차이가 사는 자리가 이 상자다.
> - 각 방향의 loss 셋은 그 방향 화살표 끝에 따로 적는다. D3에서는 같은 세 숫자이지만 한 쌍이 틀린 배치에서는 다르고, loss를 한 벌만 적은 그림은 오류를 숨긴 것이다.

> [!tip]- 정답 · Solutions
> 1. 행=이미지, 열=캡션이고, 음영을 넣은 대각선 $(2,\ 1.732051,\ 2)$가 짝이 맞는 쌍이다. 아홉 칸 전부에 $\tau$ 나눗셈을 건 행렬은 $\begin{pmatrix}2&1&0\\0&1.732051&2\\0&1.732051&2\end{pmatrix}$다. 행 화살표 끝의 loss는 $(0.407606,\ 0.909951,\ 0.642002)$, 열 화살표 끝은 $(0.239545,\ 0.908630,\ 0.758624)$로, 이제 두 벌이 다르다. 동그라미는 $(1,1)$, $(2,3)$, $(3,3)$에 친다. 행 2의 동그라미가 대각선 밖에 있는데, 이미지 2가 이제 캡션 3을 1위로 매기기 때문이다. 넷째 쌍은 넷째 행과 열, 곧 새 칸 일곱을 더한다. 대각선 위의 하나는 positive이고 대각선 밖의 여섯은 그려지는 순간 negative다. $N$이 loss에 들어오는 기제 전체가 그것이다.
> 2. (a) $v_2'=(0,1)$이면 $v_2'^\top t_j=(0,\ 0.866025,\ 1)$이므로 logit의 행 2는 $(0,\ 1.732051,\ 2)$이고, $v_2'=v_3$이라 행 3과 같다. 행렬은 대칭이 아니다 — $\ell_{12}=1$인데 $\ell_{21}=0$ — 이미지 2는 움직였고 캡션 2는 움직이지 않아 $v_2'\ne t_2$이기 때문이다. (b) 행: $L_1=0.407606$과 $L_3=0.642002$는 그대로이고 $L_2=-\log\big(e^{1.732051}/(e^0+e^{1.732051}+e^2)\big)=0.909951$, 평균은 $0.653187$이다. 열: $0.239545$, $0.908630$, $0.758624$, 평균 $0.635600$이다. 그래서 $\mathcal L=\tfrac12(0.653187+0.635600)=0.644393$으로, §5 한 쌍 틀림 열의 $\tau=1/2$ 값이다. 열 1은 $0.407606$에서 $0.239545$로 *내려갔다*. 이미지 2가 캡션 1에서 멀어져 코사인이 $0.5$에서 $0$이 되었으므로 캡션 1의 후보 줄이 쉬워졌다. 틀린 encoder가 한 방향의 loss를 낮춘 것이다. 열 2와 열 3에서는 $v_2'=v_3$이라 이미지 2와 3이 동점이다. (c) 행 2의 softmax는 $(0.071219,\ 0.402544,\ 0.526238)$이므로 캡션 3이 1위이고, 이미지 2는 이제 틀린 캡션을 검색한다. 밀어내기 질량은 $1-0.402544=0.597456$이고 캡션 3이 그중 $0.526238$, 곧 $88.1\%$를 가져간다. D3의 $67.5\%$보다 크다. 어려운 negative가 모델의 1순위가 되었고, gradient $p-y$가 바로 거기를 가장 세게 민다.
> 3. (a) 그 점이 구멍의 픽셀에서 나왔는지, 이 사진들에서 왼쪽 구멍이 늘 놓이는 자리에서 나왔는지다. 삼각대가 하나면 왼쪽 구멍은 늘 거의 같은 픽셀에 있으므로, 보지 않고 그 픽셀을 내놓는 모델도 $20/20$을 받는다. "red valve"의 모호함에서 색 prior가 위치 prior로 바뀐 것이다. (b) *이동*: 패널을 옮기거나 이미지를 옆으로 알려진 픽셀 수만큼 평행이동한다. grounded된 답은 같은 양만큼 따라 움직이고, 위치 prior는 제자리에 머문다. *좌우 반전*: 이미지를 좌우로 뒤집는다. 오른쪽에 있던 구멍이 이제 왼쪽 구멍이므로 grounded된 답은 패널 위에서 $400$ mm 떨어진 다른 구멍으로 옮겨 가고, 제자리에 머무는 답은 이미지에서 "왼쪽"을 읽고 있지 않았던 것이다. 왼쪽 구멍을 가리는 것이 셋째 시험이다. grounded된 모델은 가리개를 짚는 대신 구멍을 놓친다. (c) "빨간"은 물체 자신의 픽셀이 가진 성질이라 색을 바꾸면 곧바로 시험된다. "왼쪽"은 두 구멍 *그리고* 시점 사이의 관계다. 작업자가 카메라를 마주 보면 카메라의 왼쪽은 작업자의 오른쪽이다. 그래서 "왼쪽"은 프레임을 정하기 전에는 답이 없다. [[04-robotics/geometric-perception-calibration|3.5 기하 인식 §1]]의 카메라 프레임인가, 작업자의 프레임인가.
> 4. 빈칸은 `Td[2] = T[1]`과 `Ld = np.array([infonce(V, Td, t)[5] for t in grid])`이다. 내적은 $\begin{pmatrix}1&0.5&0.5\\0.5&1&1\\0&0.866025&0.866025\end{pmatrix}$가 되고 2열과 3열이 같아진다.
>
>    (a)와 (c):
>
>    | $\tau$ | $2$ | $1$ | $1/2$ | $1/4$ | $1/10$ | $1/20$ | $1/100$ |
>    |---|---:|---:|---:|---:|---:|---:|---:|
>    | $\mathcal L$ | $0.978047$ | $0.878017$ | $0.730300$ | $0.578480$ | $0.537591$ | $0.699788$ | $2.463960$ |
>
>    격자 탐색은 $\tau=0.1362$에서 $\mathcal L=0.521824$를 준다. §5의 한 쌍 틀린 배치처럼 내부 최소인데 이유가 다르다. 여기서는 *encoder*에 틀린 것이 없고 배치의 라벨링만 틀렸다.
>
>    (b) $\tau=1/2$에서 image→text는 $(0.551445,\,0.861995,\,0.777912)$, text→image는 $(0.407606,\,0.757448,\,1.025397)$이다. $\tau=1/100$에서 image→text는 $(0,\,0.693147,\,0.693147)$, text→image는 $(0,\,0.000002,\,13.397461)$이다.
>
>    위로 유계가 아닌 것은 3열의 text→image loss이고, $\log 2=0.693147$로 수렴하는 것은 행 2와 행 3의 image→text loss다. 비대칭이 요점이다. 행을 따라가면 모델은 *똑같은* 캡션 둘 중에서 골라야 하므로 최선이 질량을 반으로 가르는 것이고, $\log 2$는 이길 수 없는 무승부의 값이다. 유계이고 오류라고 부르기도 어렵다. 3열을 따라가면 모델은 중복된 캡션에 대해 *서로 다른* 이미지 둘 중에서 골라야 하는데 이미지 2가 이긴다($v_2^\top t_3=1$ 대 $v_3^\top t_3=0.866025$). 맞는 이미지가 2위로 밀리고 그 loss는 $\tau\to0$에서 한없이 커진다. 중복 캡션은 한 방향에서 무승부를, 다른 방향에서 노골적인 오답을 치르게 하고 유계가 아닌 쪽은 후자뿐이다. 캡션 중복 제거가 보기보다 더 중요한 이유이고, 낮은 temperature가 잡음 섞인 배치를 실제로 위험하게 만드는 이유다.

### 출처 · Sources

§1, §4, §6이 잇는 논문 노트 — CLIP, Flamingo, BLIP-2, LLaVA, PaliGemma, π0 — 가 각 논문의 인용을 담는다. 페이지의 나머지 인용은 다음과 같다.

- van den Oord, A., Li, Y. & Vinyals, O. "Representation Learning with Contrastive Predictive Coding." arXiv:1807.03748, 2018 — InfoNCE 목적함수와 그 $\log N$ 경계(§2).
- Poole, B., Ozair, S., van den Oord, A., Alemi, A. A. & Tucker, G. "On Variational Bounds of Mutual Information." *ICML*, 2019 — 상호정보량 추정량들 가운데 놓인 같은 경계(§2).
- Black, K. 외. "π0: A Vision-Language-Action Flow Model for General Robot Control." arXiv:2410.24164, 2024 — "Transfusion에서 영감을 받은" 구조, 상태·행동 토큰의 별도 가중치, 행동 토큰의 flow matching(§6).
- Gemini Robotics Team. "Gemini Robotics: Bringing AI into the Physical World." arXiv:2503.20020, 2025 — Gemini 2.0 위에 지은 VLA(§6).
- Liu, Z., Chi, C., Cousineau, E. 외. "ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data." *CoRL*, 2024 — 오디오와 비디오를 함께 써서 배운 접촉 기술(§6).
- OpenAI. "GPT-4o System Card." arXiv:2410.21276, 2024 — 어떤 입력·출력 조합이든 받는 모델, 말에 대한 $232$ ms와 $320$ ms 응답(§6의 접힌 메모).
- Xu, J., Guo, Z., He, J. 외. "Qwen2.5-Omni Technical Report." arXiv:2503.20215, 2025 — Thinker와 Talker(§6의 접힌 메모).
- Chameleon Team. "Chameleon: Mixed-Modal Early-Fusion Foundation Models." arXiv:2405.09818, 2024; Zhou, C., Yu, L., Babu, A. 외. "Transfusion: Predict the Next Token and Diffuse Images with One Multi-Modal Model." arXiv:2408.11039, 2024 — 한 시퀀스 설계 둘(§6).
