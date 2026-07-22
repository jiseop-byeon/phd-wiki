---
title: Reinforcement Learning Basics
tags: [foundations]
---

## English

You cannot read [[canonical-papers/notes/instructgpt|RLHF]], the Dreamer line of world
models, or half of modern robot learning without the MDP vocabulary. This page is the
minimum viable RL — enough to read those papers, not to do RL research.

### 1. The MDP

- **Markov Decision Process**: states $s$, actions $a$, transition $p(s'|s,a)$, reward
  $r(s,a)$, discount $\gamma \in [0,1)$. Markov = the state summarizes the past
  ([[50-foundations/probability|probability]]).
- **Policy** $\pi(a|s)$: the agent. **Return**: $G_t = \sum_k \gamma^k r_{t+k}$.
  Objective: maximize $E_\pi[G]$.
- Robotics reality check: the "state" is unobserved (POMDP) — you see images and
  proprioception; VLAs sidestep this by conditioning on observation histories.

### 2. Value functions

- $V^\pi(s) = E_\pi[G_t | s_t = s]$: how good is standing here under $\pi$.
- $Q^\pi(s,a) = E_\pi[G_t | s_t = s, a_t = a]$: how good is doing $a$ here.
- **Bellman equation** — value today = reward + discounted value tomorrow:
  $Q^\pi(s,a) = E\big[r + \gamma\, Q^\pi(s',a')\big]$
  Every TD method is "make both sides agree"; the *advantage* $A = Q - V$ measures how much
  better an action is than average.

### 3. The two families

- **Value-based**: learn $Q$, act greedily (Q-learning, DQN). Off-policy, sample-efficient,
  finicky with continuous actions.
- **Policy-gradient**: differentiate the objective directly —
  $\nabla_\theta J = E_\pi\big[\nabla_\theta \log \pi_\theta(a|s)\, A(s,a)\big]$
  ("make good-outcome actions more probable"). REINFORCE → actor-critic (a learned $V$
  reduces variance) → **PPO**: clip the update so the new policy stays near the old one —
  the algorithm inside [[canonical-papers/notes/instructgpt|InstructGPT]].
- The exploration-exploitation tradeoff runs under everything: entropy bonuses
  ([[50-foundations/information-theory|information theory]]) keep policies stochastic.

### 4. Model-based RL — the world-model connection

- Model-free RL asks the *real world* for every gradient — catastrophic for robots (wear,
  time, safety). Model-based RL learns dynamics $\hat{p}(s'|s,a)$ and trains the policy on
  *imagined* rollouts.
- This is precisely the [[canonical-papers/canonical-list|world models]] section: World
  Models (2018) → PlaNet → Dreamer v1–v3 learn latent dynamics with
  [[canonical-papers/notes/vae|VAE]]-style machinery and backprop through imagination.
- The tradeoff: sample efficiency vs model bias (errors compound over imagined horizons —
  the same compounding-error logic as [[canonical-papers/notes/act|ACT]]'s motivation).

### 5. RL vs imitation in robot learning (orientation map)

- **Imitation** ([[canonical-papers/notes/rt-1|RT-1]], [[canonical-papers/notes/diffusion-policy|Diffusion Policy]]):
  supervised on demos; stable, but capped by data coverage.
- **RL**: can exceed the demonstrator and discover recoveries, but needs a reward and many
  trials — practical mostly in simulation (sim-to-real) or as *fine-tuning* on top of
  imitation-pretrained VLAs (the current frontier, mirroring the
  [[canonical-papers/notes/instructgpt|pretrain → RLHF]] recipe).
- Reading key: when a robotics paper says "BC baseline," "advantage-weighted," or
  "KL-regularized policy," this page is the decoder ring.

## 한국어

MDP 어휘 없이는 [[canonical-papers/notes/instructgpt|RLHF]]도, Dreamer 계열 월드모델도,
현대 로봇 학습의 절반도 읽을 수 없다. 이 페이지는 그 논문들을 읽기 위한 최소한의 RL이다 —
RL 연구를 하기 위한 것이 아니라.

### 1. MDP

- **마르코프 결정 과정**: 상태 $s$, 행동 $a$, 전이 $p(s'|s,a)$, 보상 $r(s,a)$,
  할인율 $\gamma \in [0,1)$. 마르코프 = 상태가 과거를 요약한다
  ([[50-foundations/probability|확률]]).
- **정책** $\pi(a|s)$: 에이전트. **리턴**: $G_t = \sum_k \gamma^k r_{t+k}$.
  목표: $E_\pi[G]$ 최대화.
- 로보틱스 현실 점검: "상태"는 관측되지 않는다(POMDP) — 보이는 건 이미지와 고유수용감각뿐;
  VLA는 관측 이력을 조건으로 삼아 이를 우회한다.

### 2. 가치 함수

- $V^\pi(s) = E_\pi[G_t | s_t = s]$: $\pi$ 아래에서 여기 서 있는 것이 얼마나 좋은가.
- $Q^\pi(s,a) = E_\pi[G_t | s_t = s, a_t = a]$: 여기서 $a$를 하는 것이 얼마나 좋은가.
- **벨만 방정식** — 오늘의 가치 = 보상 + 할인된 내일의 가치:
  $Q^\pi(s,a) = E\big[r + \gamma\, Q^\pi(s',a')\big]$
  모든 TD 기법은 "양변을 일치시키기"다; *어드밴티지* $A = Q - V$는 행동이 평균보다 얼마나
  나은지를 잰다.

### 3. 두 가지 계열

- **가치 기반**: $Q$를 배우고 탐욕적으로 행동 (Q-learning, DQN). Off-policy라 샘플 효율이
  좋지만 연속 행동에서 까다롭다.
- **정책 그래디언트**: 목적함수를 직접 미분 —
  $\nabla_\theta J = E_\pi\big[\nabla_\theta \log \pi_\theta(a|s)\, A(s,a)\big]$
  ("좋은 결과를 낸 행동의 확률을 높여라"). REINFORCE → actor-critic(학습된 $V$가 분산을
  줄임) → **PPO**: 새 정책이 옛 정책 근처에 머물도록 업데이트를 클리핑 —
  [[canonical-papers/notes/instructgpt|InstructGPT]] 안에서 도는 알고리즘이 이것이다.
- 탐험-활용 트레이드오프가 모든 것 밑에 흐른다: 엔트로피 보너스
  ([[50-foundations/information-theory|정보이론]])가 정책을 확률적으로 유지한다.

### 4. 모델 기반 RL — 월드모델과의 연결

- 모델 프리 RL은 그래디언트 하나하나를 *실제 세계*에 묻는다 — 로봇에게는 재앙이다
  (마모, 시간, 안전). 모델 기반 RL은 동역학 $\hat{p}(s'|s,a)$를 배우고 *상상된* 롤아웃으로
  정책을 학습한다.
- 이것이 정확히 [[canonical-papers/canonical-list|월드모델]] 섹션이다: World Models(2018) →
  PlaNet → Dreamer v1–v3는 [[canonical-papers/notes/vae|VAE]]식 기계장치로 잠재 동역학을
  배우고 상상을 통해 역전파한다.
- 트레이드오프: 샘플 효율 vs 모델 편향 (상상 지평에서 오차가 누적된다 —
  [[canonical-papers/notes/act|ACT]]의 동기였던 복합 오차와 같은 논리).

### 5. 로봇 학습에서 RL vs 모방 (지도)

- **모방** ([[canonical-papers/notes/rt-1|RT-1]], [[canonical-papers/notes/diffusion-policy|Diffusion Policy]]):
  시연에 대한 지도학습; 안정적이지만 데이터 커버리지가 상한.
- **RL**: 시연자를 넘어설 수 있고 회복 동작을 발견하지만, 보상과 많은 시도가 필요 —
  주로 시뮬레이션(sim-to-real)에서 실용적이거나, 모방으로 사전학습된 VLA 위의
  *파인튜닝*으로 쓰인다 ([[canonical-papers/notes/instructgpt|사전학습 → RLHF]] 레시피를
  그대로 비추는 현재의 최전선).
- 읽기 열쇠: 로보틱스 논문의 "BC baseline", "advantage-weighted", "KL-regularized policy"가
  나오면 이 페이지가 해독기다.

## 더 깊이 (외부 자료)

- Lilian Weng, [A (Long) Peek into Reinforcement Learning](https://lilianweng.github.io/posts/2018-02-19-rl-overview/) — 이 페이지의 확장판 격인 명문 서베이
- Sutton & Barto, *Reinforcement Learning: An Introduction* — 표준 교과서 (무료 공개)
