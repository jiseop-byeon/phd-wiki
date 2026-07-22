---
title: "LSTM — Long Short-Term Memory"
authors: Sepp Hochreiter, Jürgen Schmidhuber
affiliation: TU München, IDSIA
venue: Neural Computation
year: 1997
pdf: https://deeplearning.cs.cmu.edu/F23/document/readings/LSTM.pdf
project: https://doi.org/10.1162/neco.1997.9.8.1735
tags: [paper, foundations, nlp]
status: to-read
---

## English

**One-line summary**: Gated memory cells with constant error flow solved the vanishing gradient problem, making RNNs actually able to learn long-range dependencies — the workhorse of sequence modeling until the Transformer.

### Context

Plain RNNs in the early 1990s could not learn dependencies more than ~10 steps apart: backpropagated gradients shrink (or blow up) exponentially with sequence length — the **vanishing/exploding gradient problem**, formally analyzed in Hochreiter's 1991 thesis. Sequence learning was stuck.

### Method

> [!tip] Key intuition
> Give the network a protected memory cell where the error signal can flow backward unchanged (the "constant error carousel"), and let learned gates decide when to write to it and when to read from it.

- **Memory cell** with a self-connection of weight 1.0 — gradients passing along it neither vanish nor explode.
- **Input gate** controls what enters the cell; **output gate** controls what the rest of the network reads. (The now-standard **forget gate** was added by Gers et al., 1999.)
- Gates are sigmoid units learned end-to-end; the architecture is otherwise a standard RNN.

### Results

- Solved synthetic benchmark tasks with dependencies spanning **1000+ steps**, which plain RNNs and other contemporaries could not learn at all.
- Learning was faster and more reliable across noise conditions.

### Limitations & critique

- Still sequential: computation cannot be parallelized across time — the flaw that eventually made room for the [[40-papers/notes/attention-is-all-you-need|Transformer]].
- The original paper lacks the forget gate and uses dated notation/tasks; in practice everyone uses the 1999+ variant.
- Memory capacity is finite: everything must squeeze through a fixed-size hidden state — the same bottleneck [[40-papers/notes/bahdanau-attention|attention]] later bypassed.

### Impact & follow-ups

Dominant sequence architecture for two decades: speech recognition, handwriting, translation ([[40-papers/notes/seq2seq|seq2seq]] is two LSTMs), and early robot learning. GRU (2014) is its popular simplification. Conceptually, gating and additive information flow survive in modern architectures (residual connections, state-space models like Mamba).

### Connections

- Next: [[40-papers/notes/seq2seq|seq2seq]] → [[40-papers/notes/bahdanau-attention|Bahdanau Attention]] → [[40-papers/notes/attention-is-all-you-need|Transformer]]
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 오차가 소실되지 않고 흐르는 게이트 달린 메모리 셀로 vanishing gradient 문제를 해결 — Transformer 등장 전까지 시퀀스 모델링을 이끈 주역.

### 배경

1990년대 초의 일반 RNN은 약 10스텝 이상 떨어진 의존성을 학습하지 못했다. 역전파되는 그래디언트가 시퀀스 길이에 대해 지수적으로 줄거나(소실) 폭발하기 때문 — Hochreiter의 1991년 학위논문에서 정식으로 분석된 **vanishing/exploding gradient 문제**다. 시퀀스 학습은 여기서 막혀 있었다.

### 방법

> [!tip] 핵심 직관
> 오차 신호가 변형 없이 거꾸로 흐를 수 있는 보호된 메모리 셀("constant error carousel")을 만들고, 언제 쓰고 언제 읽을지는 학습된 게이트가 결정하게 한다.

- 자기 연결 가중치가 1.0인 **메모리 셀** — 이 경로를 따라 흐르는 그래디언트는 소실도 폭발도 하지 않는다.
- **입력 게이트**가 셀에 들어갈 정보를, **출력 게이트**가 네트워크가 읽어갈 정보를 통제. (지금은 표준인 **forget 게이트**는 Gers et al. 1999에서 추가됨.)
- 게이트는 시그모이드 유닛으로 전체가 end-to-end 학습된다.

### 결과

- **1000스텝 이상** 떨어진 의존성이 있는 합성 과제들을 해결 — 일반 RNN과 당대 경쟁 기법들은 아예 학습하지 못했던 문제들.
- 노이즈 조건 전반에서 더 빠르고 안정적으로 학습.

### 한계와 비판

- 여전히 순차 계산: 시간 방향 병렬화가 불가능 — 결국 [[40-papers/notes/attention-is-all-you-need|Transformer]]에게 자리를 내주게 된 약점.
- 원 논문에는 forget 게이트가 없고 표기·과제도 오래됨; 실제로 쓰이는 건 1999년 이후 변형이다.
- 기억 용량이 유한하다: 모든 정보가 고정 크기 은닉 상태를 통과해야 함 — [[40-papers/notes/bahdanau-attention|어텐션]]이 나중에 우회한 바로 그 병목.

### 영향과 후속 연구

20년간 시퀀스 구조의 지배자: 음성 인식, 필기 인식, 번역([[40-papers/notes/seq2seq|seq2seq]]가 LSTM 두 개다), 초기 로봇 학습까지. GRU(2014)는 대중적인 단순화 버전. 게이트와 덧셈형 정보 흐름이라는 개념은 residual 연결, Mamba 같은 state-space 모델에 지금도 살아 있다.

### 연결

- 다음: [[40-papers/notes/seq2seq|seq2seq]] → [[40-papers/notes/bahdanau-attention|Bahdanau Attention]] → [[40-papers/notes/attention-is-all-you-need|Transformer]]
- 계보: [[10-deep-learning/lineage|논문 계보도]]
