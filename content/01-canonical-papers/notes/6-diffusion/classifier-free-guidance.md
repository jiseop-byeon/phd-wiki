---
title: "Classifier-Free Diffusion Guidance"
authors: Jonathan Ho, Tim Salimans
affiliation: Google Research (Brain)
venue: NeurIPS Workshop 2021 / arXiv 2022
year: 2022
arxiv: https://arxiv.org/abs/2207.12598
pdf: https://arxiv.org/pdf/2207.12598
tags: [paper, generative, diffusion]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Ho & Salimans, 2022** — [arXiv](https://arxiv.org/abs/2207.12598) · [PDF](https://arxiv.org/pdf/2207.12598)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]] first. The whole trick is one line of arithmetic on the predicted noise: $\hat\epsilon = \epsilon_u + w(\epsilon_c - \epsilon_u)$ — an extrapolation *away* from the unconditional prediction. Write that line out and note that $w = 1$ recovers ordinary conditional sampling.
> [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]을 먼저. 요령 전체가 예측된 노이즈에 대한 산수 한 줄이다: $\hat\epsilon = \epsilon_u + w(\epsilon_c - \epsilon_u)$ — 무조건 예측에서 *멀어지는* 외삽. 이 줄을 직접 써 보고, $w = 1$이면 평범한 조건부 샘플링으로 되돌아온다는 점을 확인하라.

## English

**One-line summary**: Drop the conditioning at random during training, then at sampling extrapolate *away* from the unconditional prediction — one knob that trades diversity for prompt fidelity, used by essentially every conditional diffusion system.

### Context

[[score-sde|Classifier guidance]] steered diffusion with a separate classifier's gradients —
but that requires training a noise-robust classifier, and "classifier gradients" don't
exist for free-form text conditions. Conditional models alone, meanwhile, often ignore
their conditioning. A guidance signal without any external model was needed.

### Method

> [!tip] Key intuition
> One network can be both conditional and unconditional — just drop the condition (~10% of
> training). The *difference* between its two predictions points from "any image" toward
> "images matching the condition"; step further along that direction than either predicts.

- Training: randomly replace condition $c$ with null token ∅.
- Sampling: $\tilde\epsilon = (1+w)\,\epsilon_\theta(x_t, c) - w\,\epsilon_\theta(x_t, \varnothing)$
  — guidance scale $w$ interpolates (and extrapolates) between unconditional and conditional scores.
- Two forward passes per step; no classifier, works with any conditioning modality.

### Results

- Sweeps the fidelity-diversity frontier with one scalar: higher $w$ → sharper,
  more condition-faithful, less diverse. Became the quality lever behind GLIDE, Imagen,
  [[latent-diffusion|Stable Diffusion]] (typical $w\sim$5–7.5).

### Limitations & critique

- High guidance causes over-saturation and mode-dropping artifacts; doubles inference cost;
  the "why does extrapolation work so well" theory arrived only later.
- Tuning $w$ is empirical per domain — including in robotics uses.

### Impact & follow-ups

The universal conditioning trick of generative AI — text-to-image, video ([[sora|Sora]]-class
systems), and robot policies (goal-conditioned [[diffusion-policy|Diffusion Policy]]
variants use CFG to sharpen goal-following). Follow-ups: distilled guidance, interval
guidance, autoguidance.

### Connections

- Previous: [[score-sde|classifier guidance]], [[ddpm|DDPM]] · Used by: [[latent-diffusion|Stable Diffusion]], [[sora|Sora]]-class models
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 학습 중 조건을 무작위로 떨어뜨리고, 샘플링 때 무조건부 예측에서 *멀어지는* 방향으로 외삽 — 다양성과 조건 충실도를 맞바꾸는 손잡이 하나로, 사실상 모든 조건부 디퓨전 시스템이 쓴다.

### 배경

[[score-sde|분류기 가이던스]]는 별도 분류기의 그래디언트로 디퓨전을 조향했다 — 하지만
노이즈에 강건한 분류기를 따로 학습해야 하고, 자유 형식 텍스트 조건에는 "분류기
그래디언트"라는 것이 애초에 없다. 한편 조건부 모델 단독으로는 조건을 자주 무시한다.
외부 모델 없는 가이던스 신호가 필요했다.

### 방법

> [!tip] 핵심 직관
> 한 네트워크가 조건부이자 무조건부일 수 있다 — 학습의 ~10%에서 조건을 빼면 된다. 두
> 예측의 *차이*가 "아무 이미지"에서 "조건에 맞는 이미지" 쪽을 가리킨다; 그 방향으로 둘 중
> 어느 예측보다도 더 멀리 내딛어라.

- 학습: 조건 $c$를 확률적으로 널 토큰 ∅로 교체.
- 샘플링: $\tilde\epsilon = (1+w)\,\epsilon_\theta(x_t, c) - w\,\epsilon_\theta(x_t, \varnothing)$
  — 가이던스 스케일 $w$가 무조건부와 조건부 score 사이를 보간(그리고 외삽)한다.
- 스텝당 forward pass 두 번; 분류기 없음, 어떤 조건 모달리티와도 작동.

### 결과

- 스칼라 하나로 충실도-다양성 프런티어를 쓸어 담는다: $w$가 클수록 선명하고 조건에
  충실하며 덜 다양하다. GLIDE, Imagen, [[latent-diffusion|Stable Diffusion]]의 품질
  레버가 됐다(보통 $w\sim$5~7.5).

### 한계와 비판

- 높은 가이던스는 과포화와 모드 탈락 아티팩트를 만든다; 추론 비용 2배; "왜 외삽이 이렇게
  잘 되는가"의 이론은 한참 뒤에야 나왔다.
- $w$ 튜닝은 도메인별로 경험적 — 로보틱스 사용처에서도 마찬가지.

### 영향과 후속 연구

생성 AI의 보편 조건화 트릭 — 텍스트-이미지, 비디오([[sora|Sora]]급 시스템), 로봇
정책(목표 조건 [[diffusion-policy|Diffusion Policy]] 변형이 목표 추종을 날카롭게 하는 데
CFG를 쓴다). 후속: 증류된 가이던스, 구간 가이던스, autoguidance.

### 연결

- 이전: [[score-sde|분류기 가이던스]], [[ddpm|DDPM]] · 쓰는 곳: [[latent-diffusion|Stable Diffusion]], [[sora|Sora]]급 모델
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Name the two predictors created by dropping the condition during training (conditional and unconditional) · 학습 중 조건 드롭이 만드는 두 예측기(조건부/무조건부)를 말할 수 있다
- [ ] Explain what direction the extrapolation formula points along · 외삽 공식의 방향이 가리키는 것을 설명할 수 있다
- [ ] State what $w$ trades off (fidelity vs diversity) and its typical range · $w$가 맞바꾸는 것(충실도 vs 다양성)과 전형적 값 범위를 말할 수 있다
- [ ] Say why inference costs twice as much · 추론 비용 2배의 이유를 말할 수 있다
