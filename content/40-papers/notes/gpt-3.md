---
title: "GPT-3 — Language Models are Few-Shot Learners"
authors: Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, et al.
affiliation: OpenAI
venue: NeurIPS
year: 2020
arxiv: https://arxiv.org/abs/2005.14165
pdf: https://arxiv.org/pdf/2005.14165
tags: [paper, foundations, nlp, scaling]
status: to-read
---

## English

**One-line summary**: A 175B-parameter decoder-only Transformer performs new tasks from a few examples in its prompt, without any gradient updates — scale itself produces a general-purpose learner.

### Context

The [[40-papers/notes/bert|BERT]] paradigm required task-specific fine-tuning: thousands of labeled examples and a separate model copy per task. GPT-2 (2019) had hinted that a big enough LM performs tasks zero-shot from a text prompt. Meanwhile [[40-papers/notes/scaling-laws|scaling laws]] predicted smooth returns to scale. GPT-3 was the bet that pushing scale ~100× would qualitatively change what prompting can do.

### Method

> [!tip] Key intuition
> Training on enough diverse text forces the model to implicitly learn *how to pick up tasks from context* — so at inference, a few examples in the prompt act like a temporary training set the model "learns" from in its forward pass.

- Architecture: essentially GPT-2 (decoder-only [[40-papers/notes/attention-is-all-you-need|Transformer]], alternating sparse attention), scaled to **175B parameters**, 96 layers, 2048-token context.
- Trained autoregressively on ~300B tokens (filtered Common Crawl, WebText2, books, Wikipedia).
- Evaluation protocol: **zero-shot / one-shot / few-shot** — task descriptions and examples given purely in the prompt; **no weight updates**.

### Results

- Few-shot performance rises smoothly with model size and often approaches fine-tuned SOTA (translation, QA, cloze); the *gap between zero- and few-shot grows with scale* — evidence of in-context learning as an emergent ability.
- Generates news articles humans struggle to distinguish from human-written ones.
- Arithmetic, novel word usage, unscrambling — capabilities absent in smaller models appear discontinuously.

### Limitations & critique

- Still fails at systematic reasoning, and few-shot lags fine-tuning on many benchmarks (e.g., natural language inference).
- Data contamination analysis was partly post-hoc; results on some benchmarks are inflated.
- Training cost and closed weights concentrated capability; bias and misuse sections read as an early warning of everything that followed.
- Raw LM output is not aligned with user intent — the gap [[40-papers/notes/instructgpt|InstructGPT]] was built to close.

### Impact & follow-ups

Made "scale + prompting" the dominant paradigm and prompting a first-class interface. Directly enabled [[40-papers/notes/instructgpt|InstructGPT]]/ChatGPT. In robotics, the same bet — capability from scale on diverse data — underlies robot foundation models (RT-2, π0, GR00T).

### Connections

- Previous: [[40-papers/notes/bert|BERT]] (contrast), [[40-papers/notes/scaling-laws|Scaling Laws]] · Next: [[40-papers/notes/instructgpt|InstructGPT]]
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 1750억 파라미터 디코더 Transformer가 프롬프트 속 몇 개의 예시만으로, 가중치 업데이트 없이 새 과제를 수행 — 규모 그 자체가 범용 학습자를 만든다는 증명.

### 배경

[[40-papers/notes/bert|BERT]] 패러다임은 과제별 파인튜닝을 요구했다: 라벨 수천 개와 과제마다 별도의 모델 복사본. GPT-2(2019)는 충분히 큰 LM이 텍스트 프롬프트만으로 과제를 zero-shot 수행할 수 있음을 암시했고, [[40-papers/notes/scaling-laws|스케일링 법칙]]은 규모에 대한 매끄러운 수익을 예측했다. GPT-3는 규모를 100배쯤 밀면 프롬프팅으로 할 수 있는 일이 질적으로 달라진다는 데 건 베팅이었다.

### 방법

> [!tip] 핵심 직관
> 충분히 다양한 텍스트로 학습하면 모델은 "문맥에서 과제를 파악하는 법" 자체를 암묵적으로 배우게 된다 — 추론 시 프롬프트의 예시 몇 개가 임시 학습 데이터처럼 작동하고, 모델은 forward pass 안에서 "학습"한다.

- 구조: 본질적으로 GPT-2(디코더 전용 [[40-papers/notes/attention-is-all-you-need|Transformer]], 교대 sparse attention)를 **1750억 파라미터**, 96층, 2048 토큰 문맥으로 확장.
- 약 3000억 토큰(필터링된 Common Crawl, WebText2, 도서, Wikipedia)으로 자기회귀 학습.
- 평가 프로토콜: **zero-shot / one-shot / few-shot** — 과제 설명과 예시를 프롬프트로만 제공; **가중치 업데이트 없음**.

### 결과

- Few-shot 성능이 모델 크기에 따라 매끄럽게 상승하며 번역·QA·빈칸 채우기에서 파인튜닝 SOTA에 근접; *zero-shot과 few-shot의 격차가 규모와 함께 벌어짐* — in-context learning이 창발적 능력이라는 증거.
- 사람이 사람 글과 구별하기 어려운 수준의 뉴스 기사 생성.
- 산술, 새 단어 활용, 철자 재배열 등 작은 모델에 없던 능력이 불연속적으로 등장.

### 한계와 비판

- 체계적 추론에는 여전히 취약하고, 여러 벤치마크(예: 자연어 추론)에서 few-shot이 파인튜닝에 뒤진다.
- 데이터 오염 분석이 사후적이어서 일부 벤치마크 수치는 부풀려져 있다.
- 학습 비용과 비공개 가중치가 능력을 소수에 집중시켰다; 편향·오용 섹션은 이후 벌어질 모든 일의 예고편처럼 읽힌다.
- 날것의 LM 출력은 사용자 의도와 정렬되어 있지 않다 — [[40-papers/notes/instructgpt|InstructGPT]]가 메우려 한 바로 그 간극.

### 영향과 후속 연구

"규모 + 프롬프팅"을 지배적 패러다임으로, 프롬프트를 일급 인터페이스로 만들었다. [[40-papers/notes/instructgpt|InstructGPT]]/ChatGPT를 직접 가능하게 했고, 로보틱스에서도 같은 베팅 — 다양한 데이터에 대한 규모에서 능력이 나온다 — 이 로봇 파운데이션 모델(RT-2, π0, GR00T)의 밑바탕이다.

### 연결

- 이전: [[40-papers/notes/bert|BERT]] (대비), [[40-papers/notes/scaling-laws|Scaling Laws]] · 다음: [[40-papers/notes/instructgpt|InstructGPT]]
- 계보: [[10-deep-learning/lineage|논문 계보도]]
