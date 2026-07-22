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
status: to-read   # to-read | reading | done
---

**📄 원문**: [arXiv](https://arxiv.org/abs/1706.03762) · [PDF](https://arxiv.org/pdf/1706.03762) · [Code](https://github.com/tensorflow/tensor2tensor) · [Official](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)

## English

**One-line summary**: Replaces recurrence and convolution entirely with attention, giving a fully parallelizable sequence model — the Transformer — that became the backbone of essentially all modern deep learning.

### Context

Before 2017, sequence transduction (machine translation, etc.) was dominated by RNNs (LSTM/GRU) with encoder-decoder structure. Two chronic problems: (1) **sequential computation** — an RNN must process tokens one at a time, so training cannot be parallelized along the sequence; (2) **long-range dependencies** — information must survive many recurrent steps to connect distant tokens. Attention had already been introduced (Bahdanau et al., 2015) but only as an *add-on* to RNNs. This paper asks: what if attention is the *only* mechanism?

### Method

> [!tip] Key intuition
> An RNN passes information through time step by step; attention lets every token *look up* every other token directly, like a differentiable key-value database. Order is then re-injected separately (positional encoding).

The Transformer is an encoder-decoder built from stacked identical blocks (6 each in the original), with no recurrence:

- **Scaled dot-product attention** — the core operation:
  $\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$
  Every token directly attends to every other token in one step; the $\sqrt{d_k}$ scaling prevents softmax saturation for large key dimensions.
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

Arguably the most influential DL paper of the decade. Direct descendants: BERT (encoder-only), GPT line (decoder-only), ViT (images as token sequences), and every VLM/VLA/world model in this wiki. Reading it is a prerequisite for [[10-deep-learning/index|the entire deep learning track]].

### Connections

- Predecessor: seq2seq + attention (Bahdanau 2015)
- Successors to read next: BERT, GPT-3, ViT

## 한국어

**한 줄 요약**: 순환(RNN)과 합성곱을 완전히 걷어내고 어텐션만으로 시퀀스를 처리하는 Transformer를 제안 — 이후 현대 딥러닝 전체의 기본 골격이 된 논문.

### 배경

2017년 이전의 기계번역 등 시퀀스 변환은 LSTM/GRU 기반 인코더-디코더가 표준이었다. 고질적인 문제 두 가지: (1) **순차 계산** — RNN은 토큰을 하나씩 처리해야 해서 시퀀스 방향으로 학습을 병렬화할 수 없다. (2) **장거리 의존성** — 멀리 떨어진 토큰을 연결하려면 정보가 수많은 순환 스텝을 통과해야 한다. 어텐션 자체는 이미 있었지만(Bahdanau 2015) RNN에 붙이는 *보조 장치*였다. 이 논문의 질문: 어텐션*만* 쓰면 어떻게 될까?

### 방법

> [!tip] 핵심 직관
> RNN은 정보를 시간 순서대로 한 칸씩 전달하지만, 어텐션은 모든 토큰이 다른 모든 토큰을 직접 *조회*하게 만든다 — 미분 가능한 key-value 데이터베이스에 가깝다. 순서 정보는 위치 인코딩으로 따로 주입한다.

Transformer는 동일한 블록을 쌓은(원 논문 기준 각 6층) 인코더-디코더이며, 순환이 전혀 없다:

- **Scaled dot-product attention** — 핵심 연산:
  $\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$
  모든 토큰이 다른 모든 토큰을 한 번에 참조한다. $\sqrt{d_k}$로 나누는 것은 차원이 클 때 softmax가 포화되는 것을 막기 위함.
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

지난 10년 딥러닝에서 가장 영향력 있는 논문이라 해도 과언이 아니다. 직계 후손: BERT(인코더만), GPT 계열(디코더만), ViT(이미지를 토큰 시퀀스로), 그리고 이 위키에 실릴 모든 VLM·VLA·월드모델. [[10-deep-learning/index|딥러닝 트랙]] 전체의 선수 과목에 해당한다.

### 연결

- 이전: seq2seq + attention (Bahdanau 2015)
- 다음으로 읽을 것: BERT, GPT-3, ViT
