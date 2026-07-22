---
title: "seq2seq — Sequence to Sequence Learning with Neural Networks"
authors: Ilya Sutskever, Oriol Vinyals, Quoc V. Le
affiliation: Google
venue: NeurIPS
year: 2014
arxiv: https://arxiv.org/abs/1409.3215
pdf: https://arxiv.org/pdf/1409.3215
tags: [paper, foundations, nlp]
status: to-read
---

**📄 원문**: [arXiv](https://arxiv.org/abs/1409.3215) · [PDF](https://arxiv.org/pdf/1409.3215)

## English

**One-line summary**: Two LSTMs — one encoding the input into a vector, one decoding the output from it — established the encoder-decoder paradigm for mapping sequences to sequences.

### Context

By 2014, [[40-canonical-papers/notes/lstm|LSTMs]] handled sequence *labeling* well, but general sequence-to-sequence mapping (translation: variable-length input → different variable-length output) had no clean end-to-end neural solution. Machine translation was ruled by phrase-based statistical systems.

### Method

> [!tip] Key intuition
> Read the whole input sentence into one thought-vector, then generate the output word by word from that vector. Simple — and its very simplicity exposed the bottleneck that attention would fix.

- **Encoder LSTM** consumes the source sequence; its final hidden state becomes a fixed-length representation.
- **Decoder LSTM** is conditioned on that vector and generates the target autoregressively until an end-of-sequence token.
- 4-layer deep LSTMs, ~380M parameters; beam search decoding.
- Killer trick: **reversing the source sentence** — puts early source words near early target words, creating short-range dependencies that make optimization much easier (+4~5 BLEU).

### Results

- WMT14 English→French: **BLEU 34.8** (ensemble), beating a strong phrase-based SMT baseline (33.3) — the first time pure neural MT surpassed SMT on a major benchmark.
- Learned representations were sensitive to word order and reasonably robust to sentence length (with the reversal trick).

### Limitations & critique

- The **fixed-vector bottleneck**: the whole sentence must fit in one vector; quality degrades on long sentences. Directly motivated [[40-canonical-papers/notes/bahdanau-attention|Bahdanau attention]] (published within months).
- The reversal trick is a hack that only exists because of that bottleneck.
- Enormous (for the time) compute: 8 GPUs for 10 days.

### Impact & follow-ups

Established the encoder-decoder framing that still structures the field: the [[40-canonical-papers/notes/attention-is-all-you-need|Transformer]] is an encoder-decoder, and "sequence in, sequence out" now covers translation, captioning, speech, and even robot action generation in VLAs.

### Connections

- Previous: [[40-canonical-papers/notes/lstm|LSTM]] · Next: [[40-canonical-papers/notes/bahdanau-attention|Bahdanau Attention]]
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 입력을 벡터로 압축하는 LSTM과 그 벡터에서 출력을 생성하는 LSTM — 시퀀스를 시퀀스로 사상하는 인코더-디코더 패러다임을 확립한 논문.

### 배경

2014년 시점에 [[40-canonical-papers/notes/lstm|LSTM]]은 시퀀스 *라벨링*은 잘했지만, 일반적인 시퀀스→시퀀스 사상(번역: 가변 길이 입력 → 다른 가변 길이 출력)에는 깔끔한 end-to-end 신경망 해법이 없었다. 기계번역은 구문 기반 통계 시스템(SMT)의 영역이었다.

### 방법

> [!tip] 핵심 직관
> 입력 문장 전체를 하나의 "생각 벡터"로 읽어들인 뒤, 그 벡터에서 출력을 단어 단위로 생성한다. 단순하다 — 그리고 바로 그 단순함이 어텐션이 고치게 될 병목을 드러냈다.

- **인코더 LSTM**이 원문을 읽고, 마지막 은닉 상태가 고정 길이 표현이 된다.
- **디코더 LSTM**이 그 벡터를 조건으로 종료 토큰이 나올 때까지 자기회귀 생성.
- 4층 LSTM, 약 3.8억 파라미터; 빔 서치 디코딩.
- 결정적 트릭: **원문 문장 뒤집기** — 원문 앞 단어들이 번역문 앞 단어들과 가까워져 단거리 의존성이 생기고, 최적화가 크게 쉬워진다(BLEU +4~5).

### 결과

- WMT14 영→불: **BLEU 34.8**(앙상블) — 강력한 SMT 베이스라인(33.3)을 넘어섬. 순수 신경망 번역이 주요 벤치마크에서 SMT를 이긴 첫 사례.
- 학습된 표현이 어순에 민감했고, (뒤집기 트릭 덕에) 문장 길이에도 비교적 강건했다.

### 한계와 비판

- **고정 벡터 병목**: 문장 전체가 벡터 하나에 들어가야 해서 긴 문장에서 품질 저하. 몇 달 뒤 나온 [[40-canonical-papers/notes/bahdanau-attention|Bahdanau 어텐션]]의 직접적 동기가 됐다.
- 문장 뒤집기는 이 병목 때문에 존재하는 임시방편이다.
- 당시 기준으로 막대한 연산: GPU 8장 × 10일.

### 영향과 후속 연구

지금도 분야를 구조 짓는 인코더-디코더 틀을 확립했다. [[40-canonical-papers/notes/attention-is-all-you-need|Transformer]]도 인코더-디코더이며, "시퀀스 입력, 시퀀스 출력"이라는 틀은 번역·캡셔닝·음성은 물론 VLA의 로봇 행동 생성까지 포괄한다.

### 연결

- 이전: [[40-canonical-papers/notes/lstm|LSTM]] · 다음: [[40-canonical-papers/notes/bahdanau-attention|Bahdanau Attention]]
- 계보: [[10-deep-learning/lineage|논문 계보도]]
