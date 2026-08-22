---
title: "Attention Is All You Need (Transformer)"
authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
affiliation: Google Brain, Google Research, University of Toronto
venue: NeurIPS
year: 2017
arxiv: https://arxiv.org/abs/1706.03762
pdf: https://arxiv.org/pdf/1706.03762
code: https://github.com/tensorflow/tensor2tensor
project: https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
tags: [paper, foundations, transformer]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Vaswani et al., NeurIPS 2017** — [arXiv](https://arxiv.org/abs/1706.03762) · [PDF](https://arxiv.org/pdf/1706.03762) · [Code](https://github.com/tensorflow/tensor2tensor) · [Official](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)

> [!note] 수학 준비물 · Math on-ramp
> Do [[02-foundations/linear-algebra|1. Linear Algebra §1]]'s attention shape walk by hand once ($Q = XW_Q$ coming out $T\times 64$) — every equation in this paper is that one line repeated. Softmax's numerical stabilization is log-sum-exp in [[02-foundations/engineering-math|0.5 §6]].
> [[02-foundations/linear-algebra|선형대수 §1]]의 어텐션 차원 따라가기($Q = XW_Q$가 $T\times 64$가 되는 계산)를 먼저 한 번 손으로 해 보라 — 이 논문의 모든 수식이 그 한 줄의 반복이다. softmax의 수치 안정화는 [[02-foundations/engineering-math|0.5 §6]]의 log-sum-exp.

## English

**One-line summary**: Replaces recurrence and convolution entirely with attention, giving a fully parallelizable sequence model — the Transformer — that became the dominant backbone across modern deep learning (with notable exceptions — diffusion U-Nets, SSM/Mamba lines, GNNs).

### Context

Before 2017, sequence transduction (machine translation, etc.) was dominated by RNNs (LSTM/GRU) with encoder-decoder structure. Two chronic problems: (1) **sequential computation** — an RNN must process tokens one at a time, so training cannot be parallelized along the sequence; (2) **long-range dependencies** — information must survive many recurrent steps to connect distant tokens. Attention had already been introduced (Bahdanau et al., 2015) but only as an *add-on* to RNNs. This paper asks: what if attention is the *only* mechanism?

### Method

> [!tip] Key intuition
> An RNN passes information through time step by step; attention lets every token *look up* every other token directly, like a differentiable key-value database. Order is then re-injected separately (positional encoding).

The Transformer is an encoder-decoder built from stacked identical blocks (6 each in the original), with no recurrence:

- **Scaled dot-product attention** — the core operation:
  $\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$
  Every token directly attends to every other token in one step; the $\sqrt{d_k}$ scaling prevents softmax saturation for large key dimensions.
  **Reading the equation, axis by axis**: $QK^\top$ = a $T{\times}T$ table of "who should
  look at whom" scores; softmax turns each row into weights summing to 1; multiplying by
  $V$ mixes the value vectors with those weights; $\sqrt{d_k}$ keeps scores from growing
  with dimension. Output shape: (number of queries) × (value dimension).

<svg viewBox="0 0 620 226" style="max-width:100%;height:auto" role="img" aria-label="one attention head as a chain of shapes">
  <defs><marker id="atA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <rect x="24" y="76" width="58" height="44" rx="3"/>
    <rect x="128" y="30" width="52" height="30" rx="3"/><rect x="128" y="80" width="52" height="30" rx="3"/><rect x="128" y="130" width="52" height="30" rx="3"/>
    <rect x="238" y="46" width="70" height="52" rx="3"/>
    <rect x="348" y="46" width="70" height="52" rx="3"/>
    <rect x="470" y="76" width="58" height="44" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" marker-end="url(#atA)" opacity="0.8">
    <line x1="82" y1="90" x2="124" y2="48"/><line x1="82" y1="98" x2="124" y2="95"/><line x1="82" y1="106" x2="124" y2="142"/>
    <line x1="180" y1="45" x2="234" y2="62"/><line x1="180" y1="95" x2="234" y2="78"/>
    <line x1="308" y1="72" x2="344" y2="72"/>
    <line x1="418" y1="72" x2="466" y2="90"/><line x1="180" y1="145" x2="466" y2="108"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="53" y="94">X</text><text x="53" y="110" font-size="9.5" opacity="0.8">T&#215;512</text>
    <text x="154" y="44">Q</text><text x="154" y="56" font-size="9.5" opacity="0.8">T&#215;64</text>
    <text x="154" y="94">K</text><text x="154" y="106" font-size="9.5" opacity="0.8">T&#215;64</text>
    <text x="154" y="144">V</text><text x="154" y="156" font-size="9.5" opacity="0.8">T&#215;64</text>
    <text x="273" y="68">QK&#7488;</text><text x="273" y="84" font-size="9.5" opacity="0.8">T&#215;T</text>
    <text x="383" y="68">softmax</text><text x="383" y="84" font-size="9.5" opacity="0.8">T&#215;T</text>
    <text x="499" y="94">out</text><text x="499" y="110" font-size="9.5" opacity="0.8">T&#215;64</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.85">
    <text x="238" y="40">who looks at whom</text><text x="348" y="40">rows sum to 1</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="24" y="186" opacity="0.9">One head with d_model = 512 and d_k = 64, drawn as shapes. The only square thing in the</text>
    <text x="24" y="201" opacity="0.9">diagram is the T&#215;T table &#8212; that is the quadratic cost, and the reason a whole subfield</text>
    <text x="24" y="216" opacity="0.9">exists to avoid building it.</text>
  </g>
</svg>


- **Multi-head attention** — run $h=8$ attention operations in parallel on different learned projections, then concatenate. Different heads learn different relation types (syntax, coreference, …).
- **Three uses of attention**: encoder self-attention, decoder *masked* self-attention (causal mask preserves autoregression), and encoder-decoder cross-attention.
- **Position-wise feed-forward** networks, **residual connections + LayerNorm** around every sublayer.
- **Positional encoding** — since attention is permutation-invariant, inject order with fixed sinusoids: $PE_{(pos,2i)} = \sin(pos/10000^{2i/d_{model}})$.

The whole sequence is processed in parallel; path length between any two tokens is $O(1)$ instead of $O(n)$.

### Results

- WMT14 English→German: **28.4 BLEU**, beating all prior single models and ensembles by >2 BLEU.
- WMT14 English→French: **41.8 BLEU**, new single-model SOTA at a fraction of prior training cost (3.5 days on 8 GPUs).
- Generalizes beyond translation: strong results on English constituency parsing with little tuning.

### Limitations & critique

- Self-attention is $O(n^2)$ in sequence length — the central scaling bottleneck that spawned an entire subfield (sparse/linear/flash attention).
- Sinusoidal positional encoding was quickly replaced in practice (learned, relative, RoPE).
- Evaluated only on NLP tasks; the claim that "attention is all you need" was validated for vision, audio, and robotics only years later — by others.

### Impact & follow-ups

Arguably the most influential DL paper of the decade. Direct descendants: BERT (encoder-only), GPT line (decoder-only), ViT (images as token sequences), and every VLM/VLA/world model in this wiki. Reading it is a prerequisite for [[03-deep-learning/index|the entire deep learning track]].

### Connections

- Predecessor: seq2seq + attention (Bahdanau 2015)
- Successors to read next: BERT, GPT-3, ViT

## 한국어

**한 줄 요약**: 순환(RNN)과 합성곱을 완전히 걷어내고 어텐션만으로 시퀀스를 처리하는 Transformer를 제안 — 이후 현대 딥러닝의 지배적 골격이 된 논문(예외도 있다 — 디퓨전 U-Net, SSM/Mamba 계열, GNN).

### 배경

2017년 이전의 기계번역 등 시퀀스 변환은 LSTM/GRU 기반 인코더-디코더가 표준이었다. 고질적인 문제 두 가지: (1) **순차 계산** — RNN은 토큰을 하나씩 처리해야 해서 시퀀스 방향으로 학습을 병렬화할 수 없다. (2) **장거리 의존성** — 멀리 떨어진 토큰을 연결하려면 정보가 수많은 순환 스텝을 통과해야 한다. 어텐션 자체는 이미 있었지만(Bahdanau 2015) RNN에 붙이는 *보조 장치*였다. 이 논문의 질문: 어텐션*만* 쓰면 어떻게 될까?

### 방법

> [!tip] 핵심 직관
> RNN은 정보를 시간 순서대로 한 칸씩 전달하지만, 어텐션은 모든 토큰이 다른 모든 토큰을 직접 *조회*하게 만든다 — 미분 가능한 key-value 데이터베이스에 가깝다. 순서 정보는 위치 인코딩으로 따로 주입한다.

Transformer는 동일한 블록을 쌓은(원 논문 기준 각 6층) 인코더-디코더이며, 순환이 전혀 없다:

- **Scaled dot-product attention** — 핵심 연산:
  $\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$
  모든 토큰이 다른 모든 토큰을 한 번에 참조한다. $\sqrt{d_k}$로 나누는 것은 차원이 클 때 softmax가 포화되는 것을 막기 위함.
  **수식을 축 단위로 읽기**: $QK^\top$ = "누가 누구를 볼지"의 $T{\times}T$ 점수표;
  softmax가 각 행을 합 1의 가중치로 바꾸고; $V$를 곱해 그 가중치로 값 벡터들을 섞는다;
  $\sqrt{d_k}$는 점수가 차원과 함께 자라는 것을 막는다. 출력 모양: (쿼리 수) × (값 차원).

<svg viewBox="0 0 620 226" style="max-width:100%;height:auto" role="img" aria-label="어텐션 헤드 하나를 모양의 연쇄로 본 것">
  <defs><marker id="atA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="none" stroke="currentColor" stroke-width="1.3">
    <rect x="24" y="76" width="58" height="44" rx="3"/>
    <rect x="128" y="30" width="52" height="30" rx="3"/><rect x="128" y="80" width="52" height="30" rx="3"/><rect x="128" y="130" width="52" height="30" rx="3"/>
    <rect x="238" y="46" width="70" height="52" rx="3"/>
    <rect x="348" y="46" width="70" height="52" rx="3"/>
    <rect x="470" y="76" width="58" height="44" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" marker-end="url(#atA)" opacity="0.8">
    <line x1="82" y1="90" x2="124" y2="48"/><line x1="82" y1="98" x2="124" y2="95"/><line x1="82" y1="106" x2="124" y2="142"/>
    <line x1="180" y1="45" x2="234" y2="62"/><line x1="180" y1="95" x2="234" y2="78"/>
    <line x1="308" y1="72" x2="344" y2="72"/>
    <line x1="418" y1="72" x2="466" y2="90"/><line x1="180" y1="145" x2="466" y2="108"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="53" y="94">X</text><text x="53" y="110" font-size="9.5" opacity="0.8">T&#215;512</text>
    <text x="154" y="44">Q</text><text x="154" y="56" font-size="9.5" opacity="0.8">T&#215;64</text>
    <text x="154" y="94">K</text><text x="154" y="106" font-size="9.5" opacity="0.8">T&#215;64</text>
    <text x="154" y="144">V</text><text x="154" y="156" font-size="9.5" opacity="0.8">T&#215;64</text>
    <text x="273" y="68">QK&#7488;</text><text x="273" y="84" font-size="9.5" opacity="0.8">T&#215;T</text>
    <text x="383" y="68">softmax</text><text x="383" y="84" font-size="9.5" opacity="0.8">T&#215;T</text>
    <text x="499" y="94">out</text><text x="499" y="110" font-size="9.5" opacity="0.8">T&#215;64</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.85">
    <text x="238" y="40">누가 누구를 보는가</text><text x="348" y="40">각 행의 합이 1</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="24" y="186" opacity="0.9">d_model = 512, d_k = 64인 헤드 하나를 모양으로 그린 것. 그림에서 정사각형인 것은</text>
    <text x="24" y="201" opacity="0.9">T&#215;T 표 하나뿐이고 &#8212; 그것이 이차 비용이며, 그 표를 만들지 않으려는 하위 분야가</text>
    <text x="24" y="216" opacity="0.9">통째로 생겨난 이유다.</text>
  </g>
</svg>


- **Multi-head attention** — 서로 다른 학습된 투영 위에서 어텐션을 $h=8$개 병렬로 수행한 뒤 이어붙인다. 헤드마다 다른 종류의 관계(문법 구조, 지시 관계 등)를 학습한다.
- **어텐션의 세 가지 쓰임**: 인코더 self-attention, 디코더의 *마스킹된* self-attention(인과 마스크로 자기회귀 유지), 인코더-디코더 cross-attention.
- 위치별 feed-forward 네트워크, 모든 서브레이어에 **residual 연결 + LayerNorm**.
- **위치 인코딩** — 어텐션은 순서를 모르는 연산이므로, 고정된 사인파로 순서 정보를 주입: $PE_{(pos,2i)} = \sin(pos/10000^{2i/d_{model}})$

시퀀스 전체가 병렬로 처리되고, 임의의 두 토큰 사이 경로 길이가 $O(n)$에서 $O(1)$로 줄어든다.

### 결과

- WMT14 영→독: **BLEU 28.4** — 기존 단일 모델과 앙상블을 모두 2점 이상 앞섬.
- WMT14 영→불: **BLEU 41.8** — 기존 대비 훨씬 적은 학습 비용(8 GPU, 3.5일)으로 단일 모델 최고 기록.
- 번역 밖으로도 일반화: 영어 구문 분석에서도 거의 튜닝 없이 좋은 성능.

### 한계와 비판

- Self-attention은 시퀀스 길이에 대해 $O(n^2)$ — 이후 sparse/linear/flash attention이라는 하위 분야가 통째로 생겨난 근본 병목.
- 사인파 위치 인코딩은 실전에서 금방 대체됨(학습형, 상대 위치, RoPE).
- 검증은 NLP에만 국한 — "어텐션이면 충분하다"는 주장이 비전·오디오·로보틱스에서 입증된 것은 수년 뒤, 다른 연구자들에 의해서였다.

### 영향과 후속 연구

지난 10년 딥러닝에서 가장 영향력 있는 논문이라 해도 과언이 아니다. 직계 후손: BERT(인코더만), GPT 계열(디코더만), ViT(이미지를 토큰 시퀀스로), 그리고 이 위키에 실릴 모든 VLM·VLA·월드모델. [[03-deep-learning/index|딥러닝 트랙]] 전체의 선수 과목에 해당한다.

### 연결

- 이전: seq2seq + attention (Bahdanau 2015)
- 다음으로 읽을 것: BERT, GPT-3, ViT

> [!question] 핵심 주장 읽는 법 · Reading the claim
> The title "Attention Is All You Need" does not claim "attention suffices for every task"; it claims that *for sequence transduction*, attention alone — no recurrence, no convolution — reaches state of the art. The verified scope is translation (plus parsing); generalization to vision and robotics was proven years later by other papers. Read the ambition of the title separately from the reach of the experiments.
>
> 제목 "Attention Is All You Need"는 "모든 과제에 어텐션이면 충분"이 아니라 "시퀀스 변환에서 순환·합성곱 없이 어텐션만으로 SOTA가 가능"이라는 주장이다. 검증 범위는 번역(+구문 분석)뿐 — 비전·로봇으로의 일반화는 수년 뒤 다른 논문들이 증명했다. 제목의 야심과 실험의 범위를 분리해서 읽어라.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Say what Q, K and V each are in $\text{softmax}(QK^\top/\sqrt{d_k})V$, and why the division by $\sqrt{d_k}$ is there · $\text{softmax}(QK^\top/\sqrt{d_k})V$에서 Q·K·V가 각각 무엇이고, $\sqrt{d_k}$로 나누는 이유를 설명할 수 있다
- [ ] Distinguish what self-attention, masked self-attention and cross-attention each attend to · self-attention / masked self-attention / cross-attention이 각각 무엇을 참조하는지 구분할 수 있다
- [ ] Explain why it parallelizes where an RNN cannot (path length $O(1)$ between any two tokens) · RNN 대비 병렬화가 가능한 이유(임의 두 토큰 사이 경로 길이 $O(1)$)를 설명할 수 있다
- [ ] Say exactly which operation produces the $O(n^2)$ cost, and why that became the target of follow-up work · $O(n^2)$ 비용이 정확히 어느 연산에서 나오고, 왜 후속 연구의 표적이 됐는지 말할 수 있다
