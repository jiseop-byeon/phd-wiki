---
title: "Neural Machine Translation by Jointly Learning to Align and Translate (Bahdanau Attention)"
authors: Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio
affiliation: Jacobs University, Université de Montréal
venue: ICLR
year: 2015
arxiv: https://arxiv.org/abs/1409.0473
pdf: https://arxiv.org/pdf/1409.0473
tags: [paper, foundations, nlp]
status: to-read
---

**Bahdanau et al., ICLR 2015** — [arXiv](https://arxiv.org/abs/1409.0473) · [PDF](https://arxiv.org/pdf/1409.0473)

## English

**One-line summary**: Introduced attention — let the decoder look back at all encoder states and learn where to look — removing seq2seq's fixed-vector bottleneck.

### Context

seq2seq (Sutskever et al., 2014) translated by compressing the entire source sentence into one fixed-length vector, then decoding from it. This worked for short sentences and degraded sharply for long ones: a single vector is an information bottleneck. The question: can the decoder access the *whole* source sequence instead?

### Method

> [!tip] Key intuition
> Instead of memorizing the sentence into one vector, keep all encoder states and let the decoder *softly search* over them at each output step — alignment becomes a learned, differentiable part of translation itself.

- Bidirectional RNN encoder produces one annotation vector $h_j$ per source word.
- At each decoding step $i$, a small network scores every source position: $e_{ij} = a(s_{i-1}, h_j)$ (additive/MLP attention), normalized to weights $\alpha_{ij} = \text{softmax}(e_{ij})$.
- The context vector $c_i = \sum_j \alpha_{ij} h_j$ is fed to the decoder — a different, dynamically chosen summary for every output word.
- The attention weights $\alpha_{ij}$ double as a soft word alignment, visualizable as a heatmap.

### Results

- Matched or beat the state-of-the-art phrase-based SMT system on English→French (WMT14).
- Crucially, performance no longer collapsed with sentence length — the fixed-vector bottleneck was gone.
- Attention heatmaps showed linguistically sensible alignments, learned without supervision.

### Limitations & critique

- Still fundamentally an RNN: sequential computation, limited parallelism — the constraint the [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]] later removed.
- Additive attention scoring was later simplified to (scaled) dot products.

### Impact & follow-ups

The conceptual birth of attention in deep learning. Two years later, [[01-canonical-papers/notes/attention-is-all-you-need|Attention Is All You Need]] asked "what if we keep only this part?" — and the rest of the wiki follows from the answer.

### Connections

- Previous: seq2seq (Sutskever 2014), LSTM (1997)
- Next: [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 디코더가 인코더의 모든 상태를 되돌아보며 "어디를 볼지"를 학습하게 만든 어텐션의 원조 — seq2seq의 고정 벡터 병목을 제거했다.

### 배경

seq2seq(Sutskever et al., 2014)는 원문 문장 전체를 고정 길이 벡터 하나로 압축한 뒤 그것만 보고 번역을 생성했다. 짧은 문장에서는 통했지만 긴 문장에서 성능이 급락했다 — 벡터 하나가 정보 병목이기 때문. 그렇다면 디코더가 원문 *전체*에 접근하게 할 수는 없을까?

### 방법

> [!tip] 핵심 직관
> 문장을 벡터 하나에 암기시키는 대신, 인코더의 상태를 전부 남겨두고 디코더가 출력 단어를 만들 때마다 그 위를 *부드럽게 검색*하게 한다 — 정렬(alignment) 자체가 번역의 학습 가능한 일부가 된다.

- 양방향 RNN 인코더가 원문 단어마다 주석 벡터 $h_j$를 생성.
- 디코딩 스텝 $i$마다 작은 네트워크가 모든 원문 위치에 점수를 매긴다: $e_{ij} = a(s_{i-1}, h_j)$ (가산형/MLP 어텐션), softmax로 정규화해 가중치 $\alpha_{ij}$를 얻음.
- 문맥 벡터 $c_i = \sum_j \alpha_{ij} h_j$를 디코더에 공급 — 출력 단어마다 동적으로 달라지는 요약본.
- 가중치 $\alpha_{ij}$는 단어 정렬의 역할을 겸하며 히트맵으로 시각화 가능.

### 결과

- WMT14 영→불에서 당시 최고 성능이던 구문 기반 통계 번역(SMT)과 대등하거나 상회.
- 결정적으로, 문장이 길어져도 성능이 무너지지 않았다 — 고정 벡터 병목의 해소.
- 어텐션 히트맵이 언어학적으로 타당한 정렬을 보여줌 — 별도 감독 없이 학습된 결과.

### 한계와 비판

- 여전히 본질은 RNN: 순차 계산, 제한된 병렬성 — 이 제약을 걷어낸 것이 [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]].
- 가산형 점수 함수는 이후 (스케일된) 내적으로 단순화된다.

### 영향과 후속 연구

딥러닝에서 어텐션이라는 개념이 태어난 지점. 2년 뒤 [[01-canonical-papers/notes/attention-is-all-you-need|Attention Is All You Need]]가 "이 부분만 남기면 어떻게 될까"를 물었고, 이 위키의 나머지 전부가 그 답에서 나온다.

### 연결

- 이전: seq2seq (Sutskever 2014), LSTM (1997)
- 다음: [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]
