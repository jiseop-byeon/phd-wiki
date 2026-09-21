---
title: 3. Vision–Language Models
tags: [deep-learning, vlm, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Distinguish contrastive alignment, fusion, and generation; compute a contrastive batch; and bound what language-grounded evidence proves."
mastery-when: "Raise when multimodal grounding, representation, or language-conditioned perception is modified in the thesis."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/computer-vision/index|2. Computer Vision]], [[02-foundations/information-theory|5. Information Theory]], and [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|the Transformer note]]. Object **D3** from [[03-deep-learning/lab-objects|0. Lab Objects]]; the Tier A lab in §5 needs NumPy and nothing else.
> [[03-deep-learning/computer-vision/index|2. 컴퓨터비전]], [[02-foundations/information-theory|5. 정보이론]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]. 대상은 [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D3**이고, §5의 Tier A 실습에는 NumPy만 있으면 된다.

## English

> [!note] First pass
> Read D3, §2, and questions 1–2. Work the Worked case by hand — nine dot products, three row losses, one average — before you open §5. Return to §3 when a caption or VQA number is treated as grounding.

### Running object: D3

**D3** from [[03-deep-learning/lab-objects|0. Lab Objects]] is three matched image–caption pairs with frozen unit embeddings and $\tau=1/2$:

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix}.$$

Similarity logits are $\ell_{ij}=v_i^\top t_j/\tau$. Rows ask “which text matches this image?”; columns ask the reverse.

Everything on this page follows from those six vectors and one knob. All are unit length, so each dot product is the cosine of the angle between two of them, and the three images sit at $0^\circ$, $60^\circ$ and $90^\circ$. Matched pairs are *exactly* aligned — this is a batch the encoder has already solved — so the only thing that can go wrong on D3 is the objective itself, which is what makes it the right object for reading a contrastive loss. Two page-local variants are frozen here for §5 and the problem set, changing one vector each. **The one-wrong batch** moves image 2 to $v_2'=(0,1)$, i.e. to $90^\circ$, so the encoder now places it on top of caption 3. **The duplicate-caption batch** sets $t_3=t_2$, so captions 2 and 3 are the same sentence and the "negative" in row 2 is a correct match.

*Scope: this page teaches the contrastive objective of a dual encoder — the similarity matrix, the two directions, the temperature, the negatives, and what the resulting number does and does not certify — and the vocabulary that separates conditioning from grounding. It does not teach the image encoder, which is [[03-deep-learning/computer-vision/index|2. Computer Vision §1]]; nor the cross-attention that fusion models use, which is [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer §1]] and the [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer note]]; nor the loss and optimizer machinery around the objective, which is [[03-deep-learning/foundations/index|1. Learning Systems §6]]; nor generative decoding, captioning metrics, or action, which are the generative entries of the [[01-canonical-papers/canonical-list|canonical list]] and the [[03-deep-learning/vla/index|VLA course]]. The retrieval metrics named in §3 are defined in [[02-foundations/ml-practice|9. ML Practice §3]].*

### Homework diagram

One figure in two parts, and the problem set asks for exactly this one. The figure is the worked case at $\tau=1/2$, with the three row losses and their mean.

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

And the matrix itself, which is the part the problem set asks you to draw by hand. At $\tau=1/2$:

| $\ell_{ij}$ | $t_1$ | $t_2$ | $t_3$ |
|---|---:|---:|---:|
| $v_1$ | $\mathbf{2}$ | $1$ | $0$ |
| $v_2$ | $1$ | $\mathbf{2}$ | $1.732051$ |
| $v_3$ | $0$ | $1.732051$ | $\mathbf{2}$ |

Four things the drawing has to get right, each of which is a claim about the objective.
**The diagonal marked as the positives, and nothing else marked.** Every off-diagonal cell is a negative *by construction of the batch*, not by any evidence that the pair is wrong. That is the single assumption the whole loss rests on, and the duplicate-caption variant is what happens when it fails.
**Two arrows out of the same matrix, not two matrices.** The row softmax and the column softmax read the identical numbers in two directions. Drawing two matrices claims there are two models; there is one, scored twice.
**The $\tau$ division drawn before the softmax, on the whole matrix.** Temperature is not a property of a pair and not a property of the encoder — it scales every cell at once, which is why it can be pulled out of the picture and swept in §5.
**The batch boundary drawn as a box around all nine cells.** Nothing outside the box is a negative. A loss computed over three items is a different function from the same loss over 32,768 items, and the box is where the difference lives.

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

**The negative that is not obviously wrong.** Row 2's softmax at $\tau=1/2$ is $(0.172485,\ 0.468861,\ 0.358654)$. The gradient of a softmax cross-entropy is $p-y$ (worked in [[03-deep-learning/foundations/index|1. Learning Systems §2]]), so this row pushes image 2 *away from caption 3* with weight $0.358654$ — more than a third of all the push-down mass in the row. Caption 3 is a negative because it sits in a different slot of the batch, and for no other reason. Keep that number in mind for §2's paragraph about false negatives, and for the problem set, where caption 3 is a copy of caption 2.

### 1. Three VLM families

- **dual encoder:** image and text encoded separately; fast retrieval and zero-shot classification through similarity.
- **fusion model:** tokens interact through cross-attention; stronger pair reasoning, more expensive all-pairs use.
- **generative model:** predicts language tokens conditioned on visual representations; fluent output is not proof of grounded perception.

The cost structure is the practical difference, and it follows from where the two modalities meet. A dual encoder computes $N$ image vectors and $M$ text vectors once and then scores any pair with a dot product, so ranking a query against a million images is a million multiply-adds. A fusion model has to run the joint network once per pair, so the same ranking is a million forward passes. That is why retrieval systems are built on dual encoders and why fusion models appear where the pair set is small — and it explains, without any appeal to quality, which architecture a paper's task forced on it.

### 2. Contrastive learning, by hand

Image 1 dots are $v_1^\top t_j=(1,1/2,0)$. Dividing by $\tau=1/2$ gives logits $(2,1,0)$. Its correct-pair probability is

$$p_{11}=\frac{e^2}{e^2+e+1}=0.665,\qquad L_{i\to t}=-\log p_{11}=0.408.$$

The full CLIP-style objective averages image-to-text and text-to-image cross-entropies over the batch. The other batch members are not generic “wrong language”; they are sampled negatives. False negatives and batch composition therefore affect what is learned.

That sentence is the whole objective, so it is worth writing out with every symbol rather than describing.

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

A model is *conditioned on* an image when the image changes its output distribution. Grounding additionally asks whether a claim or token is supported by localized visual evidence. Caption likelihood, retrieval accuracy, VQA accuracy, hallucination rate, and spatial grounding measure different abilities.

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

VLM representations can supply semantic labels, language-conditioned goals, reward signals, or a backbone for a VLA. None of these alone supplies control frequency, action feasibility, or recovery. Read [[01-canonical-papers/notes/3-vlm/clip|CLIP]] first, then fusion/generative entries and the [[03-deep-learning/vla/index|VLA course]].

### 5. The lab: what the temperature does, and to whom

One knob, two batches. Part 1 reproduces the Worked case. Part 2 sweeps $\tau$ over the aligned D3 — the batch the encoder has already solved — and over the one-wrong batch that moves image 2 to $90^\circ$. The second column is the point: on a perfect batch the sweep is monotone and says nothing, and only a batch with a mistake in it has an opinion about $\tau$.

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
- **With one pair wrong, the loss is not monotone in $\tau$ and has an interior minimum.** The right-hand column falls to $0.527329$ at $\tau=1/4$, turns, and reaches $2.463960$ at $\tau=1/100$ — worse than the no-information $\log 3$. A grid search over $\tau\in[0.01,3]$ puts the minimum at $\tau=0.1639$, $\mathcal L=0.507409$. Sharpening amplifies whatever the model believes, and below the optimum it is amplifying a mistake. This is the sentence in the problem set's old solution — "sharper logits improve confidence here but also sharpen mistakes" — with the turning point measured.
- **A large enough $\tau$ hides the error completely.** At $\tau=2$ the wrong encoder scores $0.932611$ against the correct encoder's $0.933538$ — marginally *better*. The two curves cross at $\tau\approx1.6542$. Above that, the softmax is so flat that a $30^\circ$ encoding error is invisible in the loss, which is worth remembering whenever a training curve is used as evidence that an encoder is working.

### Self-check

1. Why does D3's image-to-text loss equal its text-to-image loss, and is that a property of contrastive learning?
2. The batch has $N=3$. What is the largest mutual information this objective could certify, and why?
3. Lowering $\tau$ from $1/2$ to $1/4$ raises $p_{11}$ from $0.665$ to $0.867$. Which retrieval decisions changed?
4. Row 2 pushes $0.359$ of its mass away from caption 3. What has to be true about caption 3 for that to be correct supervision?
5. A model answers "red valve" correctly. Name the experiment that distinguishes conditioning from grounding, and say why higher accuracy cannot substitute for it.

> [!tip]- Answers
> 1. Because $v_i=t_i$ for every $i$, so the similarity matrix is symmetric and transposing it changes nothing. It is a property of this object, not of the method: any batch whose matched pairs are not exactly aligned gives two different direction losses, which is why the objective sums both.
> 2. $\log 3=1.098612$ nats, about $1.584963$ bits. The InfoNCE bound is $I\ge\log N-\mathbb E[\mathcal L]$ and $\mathcal L\ge0$, so the batch size caps the certificate regardless of the encoder.
> 3. None. Dividing by a positive constant preserves the order of the logits, so every arg max, every ranking and therefore every recall@$k$ is unchanged. Only the loss moved.
> 4. Caption 3 must not describe image 2. On D3 that is assumed rather than checked — it holds because the batch was built that way — and the problem set's duplicate-caption variant is the case where the assumption is false and the gradient is actively wrong.
> 5. Intervene on the image: occlude or recolour the valve and see whether the answer follows. Accuracy cannot substitute because a language prior that answers "red" for valves scores well with no visual evidence, so the benchmark number is consistent with both explanations.

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and [[03-deep-learning/lab-objects|0. Lab Objects]]. D3 and its two variants are frozen in the Running object; question 4 uses the duplicate-caption variant, which §5 never runs, so none of the lab's numbers can be copied.

1. **Draw.** Draw D3's $3\times3$ similarity matrix and mark positives on the diagonal. Add the two softmax directions as arrows off the same matrix, the $\tau$ division before them, and a box around the batch; label which cells would stop being negatives if the batch were larger.
2. **Derive.** On D3 image 1, recompute logits and row loss at $\tau=1/4$. Explain the effect of the lower temperature.
3. **Interpret.** A model answers “red valve” correctly but no localization or intervention is tested. What claim remains open?
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

> [!tip]- Solutions
> 1. Rows are images, columns captions; $(i,i)$ are matched pairs. The two arrows leave the same matrix — one softmax along rows, one along columns — with the $\tau$ division applied to all nine cells first. Nothing outside the box is a negative: enlarging the batch adds columns and rows, and every new off-diagonal cell becomes a negative the moment it is drawn, which is the whole mechanism by which $N$ enters the loss.
> 2. Dots unchanged, so logits $(4,2,0)$. $p=e^4/(e^4+e^2+1)=0.867$, loss $0.143$. Sharper logits improve confidence here but also sharpen mistakes — §5 measures where that turns, at $\tau=0.1639$ on the one-wrong batch.
> 3. Whether the answer is grounded in the valve pixels rather than language priors.
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

## 한국어

> [!note] 처음이라면
> D3, §2, 문제 1–2를 먼저 한다. §5를 열기 전에 계산 절 — 내적 아홉 개, 행 loss 셋, 평균 하나 — 을 손으로 끝낸다. caption이나 VQA 숫자를 grounding으로 읽을 때 §3으로 돌아온다.

### 계속 쓰는 대상: D3

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D3**는 이미지–캡션 3쌍이다. 고정 임베딩과 $\tau=1/2$는

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix}.$$

logit은 $\ell_{ij}=v_i^\top t_j/\tau$다. 행은 이미지에 맞는 텍스트, 열은 텍스트에 맞는 이미지를 묻는다.

이 페이지의 전부가 그 벡터 여섯 개와 손잡이 하나에서 나온다. 모두 단위 길이라 각 내적은 두 벡터 사이 각의 코사인이고, 세 이미지는 $0^\circ$, $60^\circ$, $90^\circ$에 놓인다. 짝이 맞는 쌍은 *정확히* 정렬되어 있다. 즉 encoder가 이미 풀어 놓은 배치라서, D3에서 잘못될 수 있는 것은 목적함수 자체뿐이다. 대조 loss를 읽기에 알맞은 대상인 이유가 그것이다. §5와 과제를 위해 벡터 하나씩만 바꾼 페이지 고유 변형 둘도 여기서 고정한다. **한 쌍이 틀린 배치**는 이미지 2를 $v_2'=(0,1)$, 즉 $90^\circ$로 옮겨 encoder가 캡션 3 위에 겹쳐 놓게 한다. **중복 캡션 배치**는 $t_3=t_2$로 두어 캡션 2와 3이 같은 문장이 되고, 행 2의 "negative"가 실제로는 맞는 짝이 된다.

*범위: 이 페이지는 dual encoder의 대조 목적함수 — similarity matrix, 두 방향, temperature, negative, 그리고 그 결과 숫자가 보증하는 것과 보증하지 못하는 것 — 와 conditioning을 grounding에서 가르는 어휘를 가르친다. 이미지 encoder는 가르치지 않는다. 그것은 [[03-deep-learning/computer-vision/index|2. 컴퓨터비전 §1]]이다. fusion 모델이 쓰는 cross-attention도 아니다. 그것은 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer §1]]과 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer 노트]]다. 목적함수 주변의 loss·optimizer 기계도 아니다. 그것은 [[03-deep-learning/foundations/index|1. 학습 시스템 §6]]이다. 생성 디코딩, 캡션 metric, 행동도 아니다. 그것은 [[01-canonical-papers/canonical-list|canonical list]]의 생성 항목과 [[03-deep-learning/vla/index|VLA 교과]]다. §3에 이름만 나오는 retrieval metric은 [[02-foundations/ml-practice|9. ML 실무 §3]]에 정의되어 있다.*

### 과제가 그릴 그림

두 부분으로 된 그림 하나이고, 과제가 요구하는 것이 정확히 이 그림이다. 그림은 $\tau=1/2$의 계산 절이고, 행 loss 셋과 그 평균까지 적었다.

<svg viewBox="0 0 560 372" style="max-width:100%;height:auto" role="img" aria-label="D3의 두 encoder가 3×3 코사인 행렬을 만들고, 아홉 칸 전부를 τ = 1/2로 나눈 logit 행렬 하나에 대각선을 positive로 표시하고 배치 상자를 두른 뒤, 그 행렬을 행 방향과 열 방향으로 읽어 각각 loss 0.407606, 0.757448, 0.642002와 목적함수 0.602352 nat을 얻는 그림">
  <defs><marker id="aD3k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="38" font-size="11" fill="currentColor">이미지 3장</text>
  <line x1="78" y1="34" x2="90" y2="34" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3k)"/>
  <rect x="92" y="23" width="90" height="22" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="137" y="38" font-size="11" fill="currentColor" text-anchor="middle">image encoder</text>
  <line x1="137" y1="45" x2="137" y2="51" stroke="currentColor" stroke-width="1.2"/>
  <text x="137" y="63" font-size="11" fill="currentColor" text-anchor="middle">v<tspan dy="3" font-size="10">1</tspan><tspan dy="-3">, v</tspan><tspan dy="3" font-size="10">2</tspan><tspan dy="-3">, v</tspan><tspan dy="3" font-size="10">3</tspan><tspan dy="-3" dx="3.5">· 단위</tspan></text>
  <text x="12" y="88" font-size="11" fill="currentColor">캡션 3개</text>
  <line x1="78" y1="84" x2="90" y2="84" stroke="currentColor" stroke-width="1.2" marker-end="url(#aD3k)"/>
  <rect x="92" y="73" width="90" height="22" rx="4" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <text x="137" y="88" font-size="11" fill="currentColor" text-anchor="middle">text encoder</text>
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

둘째 부분은 $\tau=1/2$의 행렬 자체이고, 과제가 손으로 그리라는 것이 그것이다.

| $\ell_{ij}$ | $t_1$ | $t_2$ | $t_3$ |
|---|---:|---:|---:|
| $v_1$ | $\mathbf{2}$ | $1$ | $0$ |
| $v_2$ | $1$ | $\mathbf{2}$ | $1.732051$ |
| $v_3$ | $0$ | $1.732051$ | $\mathbf{2}$ |

그림이 맞혀야 할 것이 넷이고, 각각이 목적함수에 대한 주장이다.
**대각선만 positive로 표시하고 그 밖에는 아무것도 표시하지 않는다.** 대각선 밖의 모든 칸은 그 쌍이 틀렸다는 어떤 증거 때문이 아니라 *배치를 그렇게 구성했기 때문에* negative다. loss 전체가 이 가정 하나에 얹혀 있고, 중복 캡션 변형이 그 가정이 깨졌을 때의 모습이다.
**행렬 둘이 아니라 같은 행렬에서 나오는 화살표 둘.** 행 softmax와 열 softmax는 동일한 숫자를 두 방향으로 읽는다. 행렬을 둘 그리면 모델이 둘이라고 주장하는 셈이다. 모델은 하나이고 채점이 둘이다.
**$\tau$ 나눗셈은 softmax 앞에, 행렬 전체에 그린다.** temperature는 쌍의 성질도 encoder의 성질도 아니다. 아홉 칸을 한꺼번에 비례 조정하므로 그림에서 떼어 내 §5에서 훑을 수 있다.
**배치 경계는 아홉 칸을 감싸는 상자로 그린다.** 상자 밖에는 negative가 없다. 항목 3개에 대한 loss와 32,768개에 대한 같은 loss는 다른 함수이고, 그 차이가 사는 자리가 이 상자다.

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

**명백히 틀렸다고 할 수 없는 negative.** $\tau=1/2$에서 행 2의 softmax는 $(0.172485,\ 0.468861,\ 0.358654)$다. softmax cross-entropy의 gradient는 $p-y$이므로([[03-deep-learning/foundations/index|1. 학습 시스템 §2]]의 계산) 이 행은 이미지 2를 *캡션 3에서* 가중치 $0.358654$만큼 밀어낸다. 행 전체의 밀어내기 질량 중 3분의 1이 넘는다. 캡션 3이 negative인 이유는 배치의 다른 칸에 있다는 것뿐이고 다른 이유는 없다. 이 숫자를 §2의 false negative 문단과, 캡션 3이 캡션 2의 복사본이 되는 과제를 위해 기억해 둔다.

### 1. 세 VLM 계열

- dual encoder: 따로 encoding해 similarity로 retrieval·zero-shot 분류.
- fusion model: cross-attention으로 token을 섞어 pair reasoning.
- generative model: 시각 표현을 조건으로 language token 생성. 유창함은 grounding 증거가 아니다.

실무적 차이는 비용 구조이고, 그것은 두 양상이 어디서 만나는지에서 따라 나온다. dual encoder는 이미지 벡터 $N$개와 텍스트 벡터 $M$개를 한 번 계산해 두고 어떤 쌍이든 내적 하나로 점수를 매기므로, 질의 하나를 백만 장에 대해 순위 매기는 일이 곱셈덧셈 백만 번이다. fusion model은 쌍마다 결합 신경망을 한 번씩 돌려야 하므로 같은 순위 매기기가 순전파 백만 번이다. 검색 시스템이 dual encoder 위에 세워지는 이유이고, fusion model이 쌍 집합이 작은 곳에 나타나는 이유다. 품질을 들먹이지 않고도, 논문의 과제가 어떤 구조를 강요했는지 설명해 준다.

### 2. 대조학습 계산

이미지 1의 내적은 $v_1^\top t_j=(1,1/2,0)$이고 $\tau=1/2$로 나누면 logit $(2,1,0)$이다. 정답 확률은 $0.665$, loss는 $0.408$이다. 전체 목적함수는 image→text와 text→image cross-entropy를 평균한다. batch의 다른 항목은 sampled negative라서 false negative와 batch 구성이 학습을 바꾼다.

그 문장이 목적함수 전체이므로, 서술하지 말고 기호를 모두 달아 적을 가치가 있다.

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

이미지가 출력 분포를 바꾸면 conditioning이다. grounding은 주장이나 token이 국소 시각 증거에 지지되는지 추가로 묻는다. caption likelihood·retrieval·VQA·hallucination·spatial grounding은 서로 다른 능력이다.

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

### 5. 실습: temperature가 하는 일과, 그 대상

손잡이 하나, 배치 둘. 영어 절 코드 1부는 계산 절을 재현한다. 2부는 encoder가 이미 풀어 놓은 정렬된 D3와, 이미지 2를 $90^\circ$로 옮긴 "한 쌍 틀린" 배치에 대해 $\tau$를 훑는다. 요점은 둘째 열이다. 완벽한 배치에서 sweep은 단조이고 아무것도 말하지 않는다. $\tau$에 대해 의견을 가지는 것은 실수가 섞인 배치뿐이다.

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
- **한 쌍이 틀리면 loss는 $\tau$에 대해 단조가 아니고 내부 최소를 가진다.** 오른쪽 열은 $\tau=1/4$의 $0.527329$까지 내려갔다가 돌아서서 $\tau=1/100$에서 $2.463960$에 이른다. 정보가 없을 때의 $\log 3$보다 나쁘다. $\tau\in[0.01,3]$ 격자 탐색은 최소를 $\tau=0.1639$, $\mathcal L=0.507409$에 둔다. 날카롭게 하는 것은 모델이 믿는 것을 증폭하는 일이고, 최적점 아래에서는 실수를 증폭한다. 과제의 옛 정답에 있던 문장 — "맞을 때 더 자신 있지만 오류도 날카로워진다" — 의 전환점을 측정한 것이 이것이다.
- **$\tau$가 충분히 크면 오류가 완전히 숨는다.** $\tau=2$에서 틀린 encoder는 $0.932611$로 맞는 encoder의 $0.933538$보다 근소하게 *낫다*. 두 곡선은 $\tau\approx1.6542$에서 교차한다. 그 위에서는 softmax가 너무 평평해 $30^\circ$의 인코딩 오류가 loss에 보이지 않는다. 학습 곡선을 encoder가 잘 작동한다는 증거로 쓸 때마다 기억할 일이다.

### 스스로 점검 · Self-check

1. D3에서 image→text loss와 text→image loss가 같은 이유는 무엇이고, 그것은 대조학습의 성질인가.
2. 배치가 $N=3$이다. 이 목적함수가 보증할 수 있는 상호정보량의 최대는 얼마이고 왜 그런가.
3. $\tau$를 $1/2$에서 $1/4$로 낮추면 $p_{11}$이 $0.665$에서 $0.867$이 된다. 어떤 retrieval 결정이 바뀌었는가.
4. 행 2는 질량의 $0.359$를 캡션 3에서 밀어낸다. 그것이 올바른 지도가 되려면 캡션 3에 대해 무엇이 참이어야 하는가.
5. 모델이 "red valve"를 맞혔다. conditioning과 grounding을 가르는 실험을 말하고, 더 높은 정확도가 그것을 대신할 수 없는 이유를 말하라.

> [!tip]- 정답 · Answers
> 1. 모든 $i$에서 $v_i=t_i$라 similarity matrix가 대칭이고 전치해도 달라지지 않기 때문이다. 방법의 성질이 아니라 이 대상의 성질이다. 맞는 쌍이 정확히 정렬되지 않은 배치는 두 방향 loss가 다르고, 그래서 목적함수가 둘을 더한다.
> 2. $\log 3=1.098612$ nat, 약 $1.584963$ bit다. InfoNCE 경계가 $I\ge\log N-\mathbb E[\mathcal L]$이고 $\mathcal L\ge0$이므로, encoder와 무관하게 배치 크기가 보증서의 상한이다.
> 3. 아무것도 바뀌지 않았다. 양수로 나누는 것은 logit 순서를 보존하므로 모든 arg max, 모든 순위, 따라서 모든 recall@$k$가 그대로다. 움직인 것은 loss뿐이다.
> 4. 캡션 3이 이미지 2를 서술하지 않아야 한다. D3에서 그것은 확인된 것이 아니라 가정이다. 배치를 그렇게 만들었으므로 성립할 뿐이다. 과제의 중복 캡션 변형이 그 가정이 거짓이고 gradient가 실제로 틀린 경우다.
> 5. 이미지에 개입한다. valve를 가리거나 색을 바꾸고 답이 따라가는지 본다. 정확도로 대신할 수 없는 이유는, valve에 "red"라고 답하는 언어 prior가 시각 증거 없이도 좋은 점수를 받기 때문이다. 벤치마크 숫자는 두 설명 모두와 양립한다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[03-deep-learning/lab-objects|0. Lab Objects]]만 쓴다. D3와 두 변형은 대상 절에 고정되어 있고, 문제 4는 §5가 한 번도 돌리지 않는 중복 캡션 변형을 쓰므로 실습의 숫자를 그대로 옮길 수 없다.

1. **그리기.** D3의 $3\times3$ similarity matrix와 diagonal positive를 그린다. 같은 행렬에서 나오는 두 softmax 방향을 화살표로, 그 앞의 $\tau$ 나눗셈을, 그리고 배치를 감싸는 상자를 더한다. 배치가 더 커지면 어떤 칸이 negative이기를 그만두는지 표시한다.
2. **유도.** D3 이미지 1에서 $\tau=1/4$일 때 logit과 row loss, 낮은 temperature의 효과를 계산한다.
3. **해석.** “red valve” 정답만으로 남는 grounding 질문을 말한다.
4. **실행.** 영어 절 템플릿의 `?`를 채우고 **중복 캡션** 변형을 돌린다. 캡션 3이 캡션 2의 정확한 복사본이므로 $t_3=t_2$이고 이미지는 그대로다. $\tau\in\{2,1,1/2,1/4,1/10,1/20,1/100\}$을 훑어 (a) 각 $\tau$의 $\mathcal L$, (b) $\tau=1/2$과 $\tau=1/100$에서의 image→text 행 loss 셋과 text→image 열 loss 셋, (c) 격자 탐색으로 $\mathcal L$을 최소화하는 $\tau$를 보고한다. 그리고 두 문장으로 답한다. 여섯 loss 중 $\tau\to0$에서 위로 유계가 아닌 것은 무엇이고 $\log 2$로 수렴하는 것은 무엇이며, 그 차이는 중복 캡션이 두 방향을 서로 다르게 망가뜨리는 방식에 대해 무엇을 말하는가.

> [!tip]- 정답 · Solutions
> 1. 행=image, 열=caption, $(i,i)$가 positive. 화살표 둘은 같은 행렬에서 나가고, 하나는 행 방향 softmax, 다른 하나는 열 방향 softmax이며, $\tau$ 나눗셈이 아홉 칸 전부에 먼저 걸린다. 상자 밖에는 negative가 없다. 배치를 키우면 행과 열이 늘고, 새로 그려지는 대각선 밖 칸은 그려지는 순간 negative가 된다. $N$이 loss에 들어오는 기제 전체가 그것이다.
> 2. 내적은 같고 logit은 $(4,2,0)$. 확률 $0.867$, loss $0.143$. 맞을 때 더 자신 있지만 오류도 날카로워진다. §5가 그 전환점을 한 쌍 틀린 배치에서 $\tau=0.1639$로 측정한다.
> 3. valve pixel을 실제 사용했는지 language prior를 사용했는지 미확인이다.
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
