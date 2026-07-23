---
title: "Diffusion Policy — Visuomotor Policy Learning via Action Diffusion"
authors: Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song
affiliation: Columbia University, Toyota Research Institute, MIT
venue: RSS
year: 2023
arxiv: https://arxiv.org/abs/2303.04137
pdf: https://arxiv.org/pdf/2303.04137
code: https://github.com/real-stanford/diffusion_policy
project: https://diffusion-policy.cs.columbia.edu
tags: [paper, vla, robot-learning, diffusion]
status: note-complete
last_verified: 2026-07-22
---

**Chi et al., RSS 2023** — [arXiv](https://arxiv.org/abs/2303.04137) · [PDF](https://arxiv.org/pdf/2303.04137) · [Code](https://github.com/real-stanford/diffusion_policy) · [Official](https://diffusion-policy.cs.columbia.edu)

## English

**One-line summary**: Represent the policy as a conditional [[ddpm|diffusion model]] that denoises a short *sequence* of future actions — cleanly capturing multimodal demonstrations and lifting imitation learning success rates by ~47% on average.

### Context

Human demonstrations are **multimodal**: to pass an obstacle, half the demos go left, half go
right. A policy regressing the mean does neither (it drives into the obstacle); discretized
tokens ([[rt-1|RT-1]]) quantize the space; explicit generative policies (energy-based
models) were unstable to train. Meanwhile [[ddpm|DDPM]] had just shown how to sample from
complex multimodal distributions with a stable regression loss. The transfer was waiting to happen.

### Method

> [!tip] Key intuition
> "What action?" is the wrong question when demonstrations disagree — ask "sample an action
> *trajectory* from the demo distribution, given what I see." Diffusion answers exactly
> that: start from noise, denoise a whole action chunk conditioned on the observation.

- **Action-sequence diffusion**: the model denoises a chunk of the next $T_a$ actions
  (e.g., 16 steps) conditioned on recent observations — not one action at a time.
- **Receding-horizon control**: execute the first few actions of the chunk, re-plan —
  MPC's structure with a learned generative "solver" inside.
- Visual encoder (CNN or Transformer) feeds the conditioning; the denoiser is a 1-D temporal
  U-Net (or Transformer) over the action sequence, trained with the standard
  noise-prediction MSE.
- Position control output; inference uses few (~10) denoising steps (DDIM-style) for real-time rates.

### Results

- **+46.9% average success** over prior state of the art across 15 tasks / 4 benchmarks
  (RoboMimic, Push-T, and more), simulation and real robots.
- Visibly handles multimodality (commits to one mode instead of averaging), long-horizon
  chunks reduce compounding error, and training is as stable as supervised learning.
- Robust on high-precision, contact-rich real tasks (e.g., 6-DoF mug flipping, sauce spreading).

### Limitations & critique

- No language/semantics: a single-task visuomotor policy — the VLA merger came later
  (π0 puts a flow/diffusion head *on* a VLM).
- Iterative denoising costs inference-time compute; naive step reduction degrades precision
  (flow matching and consistency-style distillation respond to this).
- Still pure imitation: multimodality is captured, but data coverage and quality remain the ceiling.

### Impact & follow-ups

Made diffusion the default action head of robot learning. Successors: 3D Diffusion Policy,
diffusion heads in Octo, and π0's flow-matching head ([[flow-matching|the related training formulation]]); together with [[act|ACT]] it established **action chunking** as standard practice.

### Connections

- Previous: [[ddpm|DDPM]] (the generative engine), [[rt-1|RT-1]] (the tokenized alternative)
- Next: [[act|ACT]] (parallel chunking approach), Octo, π0
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 정책을 조건부 [[ddpm|디퓨전 모델]]로 표현해 미래 행동의 짧은 *시퀀스*의 노이즈를 제거 — 다봉적 시연 분포를 깔끔하게 담아내며 모방학습 성공률을 평균 약 47% 끌어올렸다.

### 배경

인간의 시연은 **다봉적**이다: 장애물을 지날 때 시연의 절반은 왼쪽, 절반은 오른쪽으로 간다.
평균을 회귀하는 정책은 어느 쪽도 아니게 된다(장애물로 돌진한다); 이산 토큰([[rt-1|RT-1]])은
공간을 양자화하고; 명시적 생성 정책(에너지 기반 모델)은 학습이 불안정했다. 마침
[[ddpm|DDPM]]이 안정적인 회귀 손실로 복잡한 다봉 분포에서 샘플링하는 법을 막 보여준
참이었다. 이식은 시간 문제였다.

### 방법

> [!tip] 핵심 직관
> 시연들이 서로 다를 때 "어떤 행동?"은 잘못된 질문이다 — "지금 보이는 것을 조건으로,
> 시연 분포에서 행동 *궤적*을 샘플링하라"고 물어야 한다. 디퓨전이 정확히 그 답이다:
> 노이즈에서 시작해, 관측을 조건으로 행동 청크 전체의 노이즈를 제거한다.

- **행동 시퀀스 디퓨전**: 최근 관측을 조건으로 다음 $T_a$개 행동 청크(예: 16 스텝)의
  노이즈를 제거 — 행동을 하나씩이 아니라 덩어리로.
- **Receding-horizon 제어**: 청크의 앞부분 몇 개만 실행하고 재계획 — 학습된 생성형
  "솔버"를 안에 품은 MPC의 구조다.
- 시각 인코더(CNN 또는 Transformer)가 조건을 공급; 노이즈 제거기는 행동 시퀀스 위의
  1차원 시간 U-Net(또는 Transformer)이며 표준 노이즈 예측 MSE로 학습.
- 위치 제어 출력; 추론은 실시간을 위해 약 10 스텝(DDIM식)만 사용.

### 결과

- 15개 과제 / 4개 벤치마크(RoboMimic, Push-T 등), 시뮬레이션과 실제 로봇에서 기존 최고
  대비 **평균 +46.9% 성공률**.
- 다봉성을 눈에 띄게 처리(평균 내지 않고 한 모드에 전념), 긴 청크가 복합 오차를 줄이며,
  학습은 지도학습만큼 안정적.
- 고정밀·접촉 많은 실제 과제(6자유도 머그 뒤집기, 소스 바르기)에서 강건.

### 한계와 비판

- 언어/의미론이 없다: 단일 과제 시각-운동 정책 — VLA와의 결합은 나중에 온다
  (π0가 VLM *위에* flow/디퓨전 헤드를 얹는다).
- 반복적 노이즈 제거는 추론 연산 비용이 든다; 스텝을 무리하게 줄이면 정밀도가 떨어진다
  (flow matching과 증류 계열이 이에 대한 응답).
- 여전히 순수 모방: 다봉성은 담지만 데이터의 커버리지와 품질이 상한이다.

### 영향과 후속 연구

디퓨전을 로봇 학습의 기본 행동 헤드로 만들었다. 후속: 3D Diffusion Policy, Octo의 디퓨전
헤드, π0의 flow matching 헤드([[flow-matching|관련 학습 정식화]]); [[act|ACT]]와 함께
**행동 청킹**을 표준 관행으로 확립했다.

### 연결

- 이전: [[ddpm|DDPM]] (생성 엔진), [[rt-1|RT-1]] (토큰화 대안)
- 다음: [[act|ACT]] (병행하는 청킹 접근), Octo, π0
- 계보: [[03-deep-learning/lineage|논문 계보도]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "+46.9%"는 15개 과제의 평균이고 과제별 편차가 크다. 주장의 본질은 "다봉 행동 분포를 표현할 수 있다"이지 "조작 문제의 일반 해"가 아니다 — 언어도, 과제 간 일반화도 이 논문의 범위 밖이다(그건 VLA와의 결합에서 온다).

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 시연의 다봉성이 평균 회귀를 실패시키는 이유를 장애물 예시로 설명할 수 있다
- [ ] 노이즈 제거의 조건(관측)과 생성 대상(행동 청크)을 구분할 수 있다
- [ ] receding-horizon 실행이 [[04-robotics/mpc|MPC]]의 구조를 어떻게 빌렸는지 말할 수 있다
- [ ] 추론 스텝 수가 정밀도·지연과 맺는 트레이드오프를 말할 수 있다
