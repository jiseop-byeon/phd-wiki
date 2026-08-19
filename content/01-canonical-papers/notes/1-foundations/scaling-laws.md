---
title: "Scaling Laws for Neural Language Models (+ Chinchilla)"
authors: Jared Kaplan, Sam McCandlish, et al. (2020) · Jordan Hoffmann, et al. (2022)
affiliation: OpenAI (2020) · DeepMind (2022)
venue: arXiv (2020) · NeurIPS (2022)
year: 2020
arxiv: https://arxiv.org/abs/2001.08361
pdf: https://arxiv.org/pdf/2001.08361
project: https://arxiv.org/abs/2203.15556
tags: [paper, foundations, scaling]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Kaplan et al., 2020 · Hoffmann et al., NeurIPS 2022** — [arXiv](https://arxiv.org/abs/2001.08361) · [PDF](https://arxiv.org/pdf/2001.08361) · [Official](https://arxiv.org/abs/2203.15556)

> [!note] 수학 준비물 · Math on-ramp
> A power law $L \propto N^{-\alpha}$ is a straight line on log-log axes ([[02-foundations/engineering-math|0.5 §6]]) — that single fact is what makes the paper's plots readable, and the slope is $-\alpha$.
> 거듭제곱 법칙 $L \propto N^{-\alpha}$은 log-log 축에서 직선이다([[02-foundations/engineering-math|0.5 §6]]의 로그 규칙) — 논문의 모든 그림이 그 직선 위의 데이터다. 기울기 $\alpha$가 "규모의 수익률".

## English

**One-line summary**: LM loss follows precise power laws in parameters, data, and compute — turning "how big should we train?" from folklore into arithmetic; Chinchilla later corrected the recipe (params and tokens should scale equally).

### Context

Before 2020, model sizing was intuition-driven. Kaplan et al. measured how cross-entropy loss changes across 7+ orders of magnitude of model size, dataset size, and compute — and found the returns are not just positive but *predictable*.

### Method & findings (Kaplan 2020)

> [!tip] Key intuition
> Loss falls as a smooth power law in each of N (params), D (tokens), C (compute), as long as the other two aren't bottlenecks. If performance is predictable, then optimal allocation of a compute budget is a solvable equation — you can plan a giant training run from small pilot runs.

- $L(N) \propto N^{-0.076}$, $L(D) \propto D^{-0.095}$, $L(C) \propto C^{-0.050}$ (approximately), remarkably stable across scales.
- Architecture details (depth vs. width) matter far less than raw scale.
- Larger models are more **sample-efficient**; Kaplan's allocation advice: grow N fast, D slowly — and stop training well before convergence.

### The Chinchilla correction (Hoffmann 2022)

- With a better experimental design (varying learning-rate schedules per token budget), the compute-optimal frontier changes: **N and D should scale in equal proportion** — roughly **20 tokens per parameter**.
- Most large models of 2020–22 (GPT-3 175B, Gopher 280B) were substantially **undertrained** for their size.
- Proof: Chinchilla 70B, trained on 1.4T tokens with Gopher's compute, beats Gopher 280B across the board.

### Limitations & critique

- Power laws describe pretraining loss, not downstream abilities; emergent capabilities ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]) are not directly predicted.
- Laws are fitted to one architecture family and data distribution; data quality, repetition, and inference-cost considerations (over-training small models, à la LLaMA) shift the practical optimum.
- "Scale is all you need" readings ignore that data may run out — the very concern Chinchilla sharpened.

### Impact & follow-ups

Turned frontier training into an engineering discipline: every serious lab now fits scaling curves before committing compute. Chinchilla-optimality reshaped model sizing (LLaMA's small-but-long-trained recipe). The same methodology now guides vision and robot-policy scaling studies.

### Connections

- Motivated: [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] · Applied everywhere from LLMs to VLAs
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: LM의 손실은 파라미터·데이터·연산량에 대한 정밀한 거듭제곱 법칙을 따른다 — "얼마나 크게 학습해야 하나"를 감에서 산수로 바꾼 논문; 2년 뒤 Chinchilla가 레시피를 교정했다(파라미터와 토큰은 같은 비율로 키워라).

### 배경

2020년 이전의 모델 크기 결정은 직관의 영역이었다. Kaplan 등은 모델 크기·데이터셋 크기·연산량을 7자릿수 이상 바꿔가며 교차 엔트로피 손실의 변화를 측정했고, 규모의 수익이 단지 양수인 것이 아니라 *예측 가능*하다는 것을 발견했다.

### 방법과 발견 (Kaplan 2020)

> [!tip] 핵심 직관
> 나머지 둘이 병목이 아닌 한, 손실은 N(파라미터), D(토큰), C(연산량) 각각에 대해 매끄러운 거듭제곱 법칙으로 떨어진다. 성능이 예측 가능하다면 연산 예산의 최적 배분은 풀 수 있는 방정식이 된다 — 작은 파일럿 실험으로 거대 학습을 설계할 수 있다.

- 대략 $L(N) \propto N^{-0.076}$, $L(D) \propto D^{-0.095}$, $L(C) \propto C^{-0.050}$ — 규모 전반에서 놀랍도록 안정적.
- 구조 세부(깊이 vs 폭)는 순수 규모에 비해 훨씬 덜 중요하다.
- 큰 모델일수록 **샘플 효율**이 좋다; Kaplan의 배분 조언은 "N을 빨리, D를 천천히 키우고, 수렴 훨씬 전에 학습을 멈춰라"였다.

### Chinchilla의 교정 (Hoffmann 2022)

- 더 나은 실험 설계(토큰 예산별 학습률 스케줄)로 다시 재보니 최적 지점이 달라진다: **N과 D는 같은 비율로** — 대략 **파라미터당 20 토큰**.
- 2020~22년의 대형 모델들(GPT-3 175B, Gopher 280B)은 크기에 비해 상당히 **덜 학습된** 상태였다.
- 증명: Gopher와 같은 연산량으로 1.4조 토큰을 학습한 Chinchilla 70B가 Gopher 280B를 전면적으로 이겼다.

### 한계와 비판

- 거듭제곱 법칙은 사전학습 손실을 기술할 뿐, 다운스트림 능력은 아니다; [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]의 창발적 능력은 직접 예측되지 않는다.
- 하나의 구조 계열·데이터 분포에 맞춘 적합이다; 데이터 품질, 반복, 추론 비용 고려(LLaMA처럼 작은 모델을 오래 학습)가 실전 최적점을 이동시킨다.
- "규모면 다 된다"는 독해는 데이터가 고갈될 수 있다는 점을 놓친다 — Chinchilla가 날카롭게 만든 바로 그 문제.

### 영향과 후속 연구

프런티어 학습을 공학 분야로 만들었다: 이제 모든 주요 랩이 연산을 투입하기 전에 스케일링 곡선부터 적합한다. Chinchilla 최적성은 모델 크기 관행을 재편했고(LLaMA의 "작지만 오래 학습" 레시피), 같은 방법론이 비전과 로봇 정책의 스케일링 연구에도 적용되고 있다.

### 연결

- 동기가 된 것: [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] · LLM부터 VLA까지 어디에나 적용
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Name the variables of the three power laws (N, D, C) and the conditions under which each holds · 세 거듭제곱 법칙의 변수(N, D, C)와 각 법칙이 성립하는 조건을 말할 수 있다
- [ ] State the difference between Kaplan's and Chinchilla's allocation conclusions (~20 tokens per parameter) · Kaplan과 Chinchilla의 배분 결론 차이(파라미터당 ~20토큰)를 말할 수 있다
- [ ] Say what it means engineering-wise that a small pilot can now size a huge training run · 작은 파일럿에서 거대 학습을 설계할 수 있게 된 것의 공학적 의미를 말할 수 있다
- [ ] State the gap between predicting pretraining loss and predicting downstream capability · 사전학습 손실 예측과 다운스트림 능력 예측의 간극을 말할 수 있다
