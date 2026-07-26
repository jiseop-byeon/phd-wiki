---
title: "InstructGPT — Training Language Models to Follow Instructions (RLHF)"
authors: Long Ouyang, Jeff Wu, Xu Jiang, et al.
affiliation: OpenAI
venue: NeurIPS
year: 2022
arxiv: https://arxiv.org/abs/2203.02155
pdf: https://arxiv.org/pdf/2203.02155
tags: [paper, foundations, alignment]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Ouyang et al., NeurIPS 2022** — [arXiv](https://arxiv.org/abs/2203.02155) · [PDF](https://arxiv.org/pdf/2203.02155)

> [!note] 수학 준비물 · Math on-ramp
> [[02-foundations/rl-basics|RL 기초 §4]]의 정책 그래디언트→PPO 구간을 먼저 읽어라 — 이 논문의 3단계 중 마지막이 정확히 그 PPO이고, KL 페널티는 [[02-foundations/information-theory|정보이론 §3]]의 언어로 쓰여 있다.

## English

**One-line summary**: The three-stage RLHF recipe — supervised fine-tuning, reward model from human preferences, PPO — turns a raw language model into an assistant; a 1.3B aligned model was preferred over 175B GPT-3.

### Context

[[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] predicts plausible next tokens, which is not the same as doing what users want: outputs could be unhelpful, fabricated, or toxic, and prompting alone couldn't reliably fix it. The objective (LM likelihood) was **misaligned** with the goal (helpful, honest, harmless assistance). How do you optimize for "what humans actually prefer" when that can't be written as a loss function?

### Method

> [!tip] Key intuition
> Humans can't write the reward function, but they *can* compare two outputs. So learn the reward function from comparisons, then optimize the policy against it with RL — human judgment becomes the training signal.

1. **SFT**: fine-tune GPT-3 on ~13k labeler-written demonstrations of instruction-following.
2. **Reward model**: labelers rank multiple model outputs per prompt; train a 6B model to predict these preferences (pairwise ranking loss).
3. **PPO**: optimize the SFT policy to maximize the reward model's score, with a per-token KL penalty against the SFT policy to prevent reward over-optimization, plus mixed-in pretraining gradients ("PPO-ptx") to limit capability regression.

### Results

- **Labelers preferred 1.3B InstructGPT outputs over 175B GPT-3** — alignment beat two orders of magnitude of scale on human preference.
- Better truthfulness (TruthfulQA) and less toxicity at similar capability; "alignment tax" on standard NLP benchmarks largely removed by PPO-ptx.
- Generalized to instructions unseen in training (e.g., other languages, code questions).

### Limitations & critique

- Aligned to the preferences of a small labeler group under researcher-written guidelines — "whose values?" is unresolved.
- Reward hacking / over-optimization is held off by a KL penalty, not solved; the model still hallucinates and can follow harmful instructions.
- RLHF's complexity motivated simpler successors (DPO, RLAIF/Constitutional AI).

### Impact & follow-ups

The direct blueprint of ChatGPT and the template for aligning every modern assistant. Made "preference data" a core asset class. The same structure — demonstrations → preference/reward signal → policy optimization — now appears in robot learning as demo pretraining + preference- or outcome-based fine-tuning of VLAs.

### Connections

- Previous: [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] · Successors: DPO, Constitutional AI
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 지도 파인튜닝 → 인간 선호로 보상 모델 학습 → PPO의 3단계 RLHF 레시피로 날것의 언어모델을 어시스턴트로 바꾼 논문 — 정렬된 1.3B 모델이 175B GPT-3보다 선호됐다.

### 배경

[[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]는 그럴듯한 다음 토큰을 예측할 뿐, 그것이 사용자가 원하는 일을 하는 것과 같지 않다: 출력은 도움이 안 되거나, 지어냈거나, 유해할 수 있었고 프롬프팅만으로는 안정적으로 고칠 수 없었다. 목적함수(LM 우도)가 목표(도움되고 정직하고 무해한 어시스턴트)와 **어긋나 있었던** 것이다. "인간이 실제로 선호하는 것"을 손실함수로 쓸 수 없다면 어떻게 최적화할까?

### 방법

> [!tip] 핵심 직관
> 인간은 보상 함수를 써줄 수는 없지만 두 출력 중 어느 쪽이 나은지 *비교*는 할 수 있다. 그러니 비교 데이터로 보상 함수를 학습하고, 그 보상을 RL로 최적화하자 — 인간의 판단이 학습 신호가 된다.

1. **SFT**: 라벨러가 작성한 약 1.3만 개의 지시-수행 시연으로 GPT-3를 파인튜닝.
2. **보상 모델**: 프롬프트마다 여러 출력을 라벨러가 순위 매김; 이 선호를 예측하는 6B 모델을 학습(쌍별 랭킹 손실).
3. **PPO**: 보상 모델 점수를 최대화하도록 SFT 정책을 최적화. 보상 과최적화를 막는 토큰별 KL 페널티(SFT 정책 기준) + 능력 퇴행을 막는 사전학습 그래디언트 혼합("PPO-ptx").

### 결과

- **라벨러들이 1.3B InstructGPT 출력을 175B GPT-3보다 선호** — 인간 선호 기준으로 정렬이 두 자릿수 규모 차이를 이겼다.
- 비슷한 능력에서 더 나은 진실성(TruthfulQA)과 낮은 유해성; 표준 NLP 벤치마크에서의 "정렬 세금"은 PPO-ptx로 대부분 제거.
- 학습에 없던 지시(다른 언어, 코드 질문 등)로도 일반화.

### 한계와 비판

- 소수 라벨러 집단의 선호에, 연구자가 쓴 가이드라인 아래 정렬된 것이다 — "누구의 가치인가"는 미해결.
- 보상 해킹/과최적화는 KL 페널티로 억제될 뿐 해결된 게 아니다; 여전히 환각하고 유해 지시를 따를 수 있다.
- RLHF의 복잡성이 더 단순한 후속(DPO, RLAIF/Constitutional AI)을 낳았다.

### 영향과 후속 연구

ChatGPT의 직접적 설계도이자 모든 현대 어시스턴트 정렬의 템플릿. "선호 데이터"를 핵심 자산으로 만들었다. 시연 → 선호/보상 신호 → 정책 최적화라는 같은 구조가 로봇 학습에도 나타난다: VLA의 시연 사전학습 + 선호·결과 기반 파인튜닝.

### 연결

- 이전: [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] · 후속: DPO, Constitutional AI
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Name the input and output of each of the three stages (SFT → reward model → PPO) · 3단계(SFT→보상 모델→PPO) 각각의 입력과 출력을 말할 수 있다
- [ ] Explain why the reward is learned from comparisons rather than absolute scores · 보상을 절대 점수가 아니라 비교로 학습하는 이유를 설명할 수 있다
- [ ] Say what the KL penalty prevents (reward over-optimization) and give its information-theoretic reading · KL 페널티가 무엇을 막는지(보상 과최적화)와 그 정보이론적 독해를 말할 수 있다
- [ ] Say what the 1.3B-beats-175B result actually proves · 1.3B가 175B를 이긴 결과가 무엇을 증명하는지 말할 수 있다
