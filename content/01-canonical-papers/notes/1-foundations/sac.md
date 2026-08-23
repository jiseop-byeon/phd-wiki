---
title: Soft Actor-Critic
authors: Tuomas Haarnoja et al.
affiliation: UC Berkeley
venue: ICML
year: 2018
arxiv: https://arxiv.org/abs/1801.01290
pdf: https://arxiv.org/pdf/1801.01290
tags: [paper, reinforcement-learning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Haarnoja et al., ICML 2018** — [arXiv](https://arxiv.org/abs/1801.01290) · [PDF](https://arxiv.org/pdf/1801.01290)

> [!note] Math on-ramp · 수학 준비물
> [[02-foundations/rl-basics|7. RL Basics §3]] (Q-learning and what off-policy buys you) and [[02-foundations/rl-basics|§4]] (actor-critic). The one extra ingredient is the entropy term, whose definition is [[02-foundations/information-theory|5. Information Theory §1]] — SAC maximizes return *plus* entropy, so read it as "stay as random as you can afford to be".
> [[02-foundations/rl-basics|7. RL 기초 §3]](Q-러닝과 오프폴리시가 사주는 것)과 [[02-foundations/rl-basics|§4]](액터-크리틱). 추가 재료는 엔트로피 항 하나이고 그 정의는 [[02-foundations/information-theory|5. 정보이론 §1]]이다 — SAC은 리턴 *더하기* 엔트로피를 최대화하므로 "감당할 수 있는 만큼 무작위로 남아 있어라"로 읽으면 된다.

## English

**One-line summary**: SAC is an off-policy actor–critic that maximizes expected return *plus* policy entropy, getting replay-buffer sample efficiency and robust exploration from one maximum-entropy objective.

### Context

On-policy methods like [[01-canonical-papers/notes/1-foundations/ppo|PPO]] throw data away after a few epochs — untenable when samples are expensive, as on real hardware. Off-policy methods (DDPG) reuse a replay buffer but were brittle: deterministic policies plus overestimating critics made training hypersensitive to hyperparameters. SAC's bet: make the *objective itself* stochastic — reward entropy explicitly — and off-policy learning becomes both stable and exploratory.

### Method

> [!tip] Key intuition
> Don't treat exploration as a bolt-on (noise injected at action time); pay the policy for staying uncertain. Maximizing reward plus entropy keeps many action modes alive until the critic gives a real reason to commit.

- The maximum-entropy objective is $J(\pi)=\mathbb{E}[\sum_t r(s_t,a_t)+\alpha\mathcal{H}(\pi(\cdot|s_t))]$, where temperature $\alpha$ trades off reward against stochasticity.
- **Soft policy iteration** instantiated with function approximators: a soft Q-critic trained on Bellman targets that include the entropy term, and an actor updated toward the softmax of the Q-values (minimizing KL to $\exp(Q/\alpha)$, up to normalization).
- **Twin critics**: two Q-networks, take the minimum for targets — suppresses the overestimation bias that destabilized DDPG-style methods.
- **Reparameterized actor**: actions are a squashed (tanh) Gaussian sampled via the reparameterization trick, giving low-variance pathwise gradients through the critic.
- Replay buffer + target networks complete the recipe; the follow-up (arXiv 1812.05905) adds **automatic temperature tuning**, replacing the most sensitive hyperparameter with a constraint on target entropy.

### Results

- State-of-the-art sample efficiency and final performance on MuJoCo continuous-control benchmarks, beating DDPG and on-policy PPO — most visibly on the high-dimensional Humanoid.
- Markedly more stable across random seeds than DDPG — the entropy term and twin critics both contribute.
- The follow-up work demonstrated real-robot learning (quadruped locomotion, dexterous manipulation) in hours, which made SAC the default off-policy baseline for hardware-adjacent research.

### Limitations & critique

- The original formulation is sensitive to reward scale (it silently sets the reward/entropy trade-off); automatic $\alpha$ tuning in the follow-up largely fixes this — cite the right version.
- Entropy encourages stochasticity, not safety: exploratory actions on a hydraulic machine can still be destructive. Constraints, shielding, or simulation remain necessary.
- Off-policy bootstrapping from replayed data inherits the classic instability triad (function approximation + bootstrapping + off-policy); twin critics mitigate rather than eliminate it.
- Version note: the ICML 2018 paper trains a **separate state-value network $V$** (with its own target network); the merged 1812.05905 recipe most implementations follow drops $V$ and adds automatic temperature — opening the ICML PDF, expect that extra component.

### Impact & follow-ups

The standard continuous-control off-policy baseline — most model-free comparisons in manipulation and locomotion papers include it, and its machinery (twin critics, squashed Gaussians, auto-temperature) became community defaults. For heavy machinery, replay efficiency is attractive because samples are expensive, but real deployments still route through simulation, constraints, or supervised data rather than raw on-hardware SAC.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "Off-policy and sample-efficient" is measured in simulators with resets and dense rewards. On a real machine, add reset cost, safety envelopes, and reward instrumentation before the efficiency claim transfers.

### Connections

- Counterpart: [[01-canonical-papers/notes/1-foundations/ppo|PPO]] (the on-policy counterpart — data reuse vs on-policy freshness is the axis)
- Foundations: [[02-foundations/rl-basics|RL 기초]] (value functions, actor–critic, off-policy TD)

## 한국어

**한 줄 요약**: SAC는 기대 수익에 정책 entropy를 *더해* 최대화하는 off-policy actor–critic — 하나의 maximum-entropy 목적함수에서 replay buffer의 샘플 효율과 견고한 탐색을 동시에 얻는다.

### 배경

[[01-canonical-papers/notes/1-foundations/ppo|PPO]] 같은 on-policy 방법은 몇 epoch 뒤 데이터를 버린다 — 실기계처럼 샘플이 비싼 곳에서는 감당이 안 된다. off-policy 방법(DDPG)은 replay buffer로 데이터를 재사용하지만 취약했다: 결정론적 정책과 과대평가하는 critic의 조합이 학습을 하이퍼파라미터에 극도로 민감하게 만들었다. SAC의 승부수: *목적함수 자체*를 확률적으로 만들자 — entropy에 명시적으로 보상을 주면 — off-policy 학습이 안정적이면서 탐색적이 된다.

### 방법

> [!tip] 핵심 직관
> 탐색을 나중에 덧붙이는 것(행동에 노이즈 주입)으로 취급하지 말고, 정책이 불확실성을 유지하는 것 자체에 보상을 지급하라. 보상+entropy를 최대화하면 critic이 확신할 근거를 줄 때까지 여러 행동 모드가 살아남는다.

- maximum-entropy 목적함수는 $J(\pi)=\mathbb{E}[\sum_t r(s_t,a_t)+\alpha\mathcal{H}(\pi(\cdot|s_t))]$ — 온도 $\alpha$가 보상과 확률성 사이를 조율한다.
- **Soft policy iteration**을 함수 근사로 구현: entropy 항이 포함된 Bellman 타깃으로 soft Q-critic을 학습하고, actor는 Q값의 softmax 방향으로 업데이트한다($\exp(Q/\alpha)$에 대한 KL 최소화, 정규화 상수 무시).
- **Twin critic**: Q 네트워크 두 개를 두고 타깃에 최솟값을 사용 — DDPG 계열을 불안정하게 만든 과대평가 편향을 억제.
- **재매개화된 actor**: 행동은 tanh로 눌러 짠(squashed) Gaussian에서 reparameterization trick으로 샘플 — critic을 관통하는 저분산 pathwise 그래디언트를 얻는다.
- replay buffer + target network가 레시피를 완성한다; 후속 논문(arXiv 1812.05905)이 **자동 온도 조정**을 추가해 가장 민감한 하이퍼파라미터를 목표 entropy 제약으로 대체했다.

### 결과

- MuJoCo 연속 제어 벤치마크에서 샘플 효율과 최종 성능 모두 최고 수준 — DDPG와 on-policy PPO를 이기며, 고차원 Humanoid에서 격차가 가장 뚜렷하다.
- 랜덤 시드에 걸친 안정성이 DDPG보다 현저히 좋다 — entropy 항과 twin critic이 각각 기여한다.
- 후속 연구는 실로봇 학습(사족 locomotion, 정밀 조작)을 수 시간 안에 시연했고, 이것이 SAC를 하드웨어 인접 연구의 기본 off-policy 기준선으로 만들었다.

### 한계와 비판

- 원 논문 버전은 보상 스케일에 민감하다(보상/entropy 트레이드오프를 암묵적으로 결정하므로); 후속의 자동 $\alpha$ 조정이 대부분 해결 — 어느 버전을 인용하는지 확인하라.
- entropy는 확률성을 장려할 뿐 안전을 장려하지 않는다: 유압 장비에서 탐색적 행동은 여전히 파괴적일 수 있다. 제약, shielding, 시뮬레이션이 여전히 필요하다.
- replay 데이터로부터의 off-policy bootstrapping은 고전적 불안정 삼요소(함수 근사 + bootstrapping + off-policy)를 물려받는다; twin critic은 이를 완화할 뿐 제거하지 못한다.
- 버전 주의: ICML 2018 판은 **별도의 상태 가치 네트워크 $V$**(와 그 타깃 네트워크)를 학습한다; 대부분의 구현이 따르는 병합판 1812.05905는 $V$를 없애고 자동 온도를 더했다 — ICML PDF를 열면 이 추가 구성요소를 만나게 된다.

### 영향과 후속 연구

연속 제어 off-policy의 표준 기준선 — 조작·locomotion 논문의 model-free 비교 대부분에 등장하고, 그 장치들(twin critic, squashed Gaussian, 자동 온도)은 커뮤니티 기본값이 됐다. 중장비에서는 샘플이 비싸기 때문에 replay 효율이 매력적이지만, 실제 배포는 여전히 실기계 위 SAC가 아니라 시뮬레이션, 제약, 지도 데이터를 경유한다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "off-policy라 샘플 효율적"이라는 주장은 리셋과 촘촘한 보상이 있는 시뮬레이터에서 측정된 것이다. 실기계에서는 리셋 비용, 안전 영역, 보상 계측을 더한 뒤에야 그 효율 주장이 전이된다.

### 연결

- 대응 관계: [[01-canonical-papers/notes/1-foundations/ppo|PPO]] (on-policy 대응물 — 데이터 재사용 vs on-policy 신선도가 비교 축이다)
- 기초: [[02-foundations/rl-basics|RL 기초]] (가치 함수, actor–critic, off-policy TD)

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain the reward–entropy trade-off and the role of the temperature $\alpha$ (including automatic tuning) · 보상과 entropy 항의 trade-off, 그리고 온도 $\alpha$의 역할(및 자동 조정)을 설명할 수 있다
- [ ] State how on-policy PPO and off-policy SAC differ in data use, and the price of each (freshness vs reuse) · on-policy PPO와 off-policy SAC의 데이터 사용 차이와 그 대가(신선도 vs 재사용)를 말할 수 있다
- [ ] Explain why replay efficiency alone is not enough on real hardware (safety, resets, reward instrumentation) · 실제 장비에서 replay 효율만으로 충분하지 않은 이유(안전, 리셋, 보상 계측)를 설명할 수 있다
