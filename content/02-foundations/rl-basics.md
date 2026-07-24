---
title: 7. Reinforcement Learning Basics
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [[02-foundations/overview|0. Overview]] — 이 페이지에 필요한 사전 수학과 다른 지식과의 연결 지도 · prerequisites & connection map

## English

You cannot read [[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]], the
[[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]] line, or half of modern robot learning without
the MDP vocabulary. Course-depth treatment: the Bellman machinery, both algorithm families
with their update rules, the policy gradient theorem, and PPO's actual objective.

### 1. The MDP

- **Markov Decision Process** $(\mathcal{S}, \mathcal{A}, p, r, \gamma)$: states, actions,
  transition kernel $p(s'|s,a)$, reward $r(s,a)$, discount $\gamma \in [0,1)$.
  Markov = the state summarizes the past ([[02-foundations/probability|probability]]).
- **Policy** $\pi(a|s)$; **return** $G_t = \sum_{k\ge 0} \gamma^k r_{t+k}$; objective
  $J(\pi) = E_\pi[G_0]$. Discounting makes infinite sums finite and encodes impatience;
  $1/(1-\gamma)$ is the effective horizon (γ=0.99 ⇒ ~100 steps).
- Robotics reality: the state is *unobserved* (POMDP) — you see images and proprioception.
  Practical dodge: condition on observation histories / recurrent state (what
  [[01-canonical-papers/notes/5-world-models/dreamer|RSSM]]s formalize).

### 2. Value functions and the Bellman equations

- $V^\pi(s) = E_\pi[G_t | s_t{=}s]$, $Q^\pi(s,a) = E_\pi[G_t | s_t{=}s, a_t{=}a]$,
  **advantage** $A^\pi = Q^\pi - V^\pi$ (how much better than my average move).
- **Bellman expectation** (consistency of $V^\pi$):
  $$V^\pi(s) = E_{a\sim\pi,\, s'\sim p}\big[r(s,a) + \gamma V^\pi(s')\big]$$
- **Bellman optimality**: $Q^*(s,a) = E\big[r + \gamma \max_{a'} Q^*(s',a')\big]$;
  the greedy policy on $Q^*$ is optimal.
- These are fixed-point equations; the Bellman operator is a $\gamma$-contraction, so
  iterating it converges — the license behind everything below.

### 3. Dynamic programming and TD learning

- **Value iteration**: apply the optimality operator repeatedly (needs the model $p$).
  **Policy iteration**: evaluate $\pi$, then act greedily; repeat.
- Without a model, sample: **TD(0)** update
  $V(s) \leftarrow V(s) + \alpha\,[\underbrace{r + \gamma V(s')}_{\text{target}} - V(s)]$
  — bootstrap from your own estimate. The bracket is the **TD error** $\delta$, RL's
  all-purpose learning signal.
- **Q-learning** (off-policy):
  $Q(s,a) \leftarrow Q(s,a) + \alpha\,[r + \gamma \max_{a'}Q(s',a') - Q(s,a)]$.
  DQN = this + neural $Q$ + replay buffer + target network (a
  [[02-foundations/calculus-backprop|stop-gradient]] copy for stable targets).
- Value-based methods are sample-efficient but awkward for continuous actions
  (the $\max_{a'}$ needs an inner optimization) — hence robotics leans policy-side.
- **Worked example — value iteration you can do on paper.** Two states, fixed policy,
  $\gamma = 0.9$: state $A$ gives reward 1 and moves to $B$; state $B$ gives 0 and moves
  back to $A$. Bellman: $V(A) = 1 + 0.9V(B)$, $V(B) = 0.9V(A)$. Iterate from $V_0 = (0,0)$:
  $V_1 = (1, 0)$, $V_2 = (1, 0.9)$, $V_3 = (1.81, 0.9)$, … converging to the fixed point
  $V(A) = 1/(1 - 0.81) \approx 5.26$, $V(B) \approx 4.74$. Watch what happened: each
  sweep pushes reward information one step further back — that is all "bootstrapping" means.

### 4. Policy gradients — differentiate the objective itself

- **The log-derivative trick** (the whole derivation in three steps):
  $$\nabla_\theta J = \nabla_\theta \int p_\theta(\tau) G(\tau)\,d\tau = \int p_\theta(\tau)\,\nabla_\theta \log p_\theta(\tau)\, G(\tau)\,d\tau = E_\tau\Big[\sum_t \nabla_\theta \log \pi_\theta(a_t|s_t)\, G_t\Big]$$
  (dynamics terms vanish from $\nabla\log p_\theta(\tau)$ because they don't depend on
  $\theta$). Interpretation: *raise the log-probability of actions in proportion to the
  return that followed*.
- **REINFORCE** is exactly this — unbiased, catastrophically high variance. Variance
  reductions, in order of importance: subtract a **baseline** $b(s)$ (unbiased for any
  state-only baseline; best choice ≈ $V(s)$, making the weight the advantage $A$);
  use reward-to-go; **actor-critic**: learn $V_\phi$ with TD and use
  $\delta = r + \gamma V(s') - V(s)$ as a one-sample advantage estimate. **GAE** (generalized advantage estimation) interpolates
  between TD (biased, low-variance) and Monte Carlo (unbiased, high-variance) with a knob λ.
- **PPO** — the workhorse ([[01-canonical-papers/notes/1-foundations/instructgpt|the one inside RLHF]]):
  with ratio $\rho_t = \pi_\theta(a_t|s_t)/\pi_{old}(a_t|s_t)$,
  $$\mathcal{L} = E_t\big[\min\big(\rho_t A_t,\ \text{clip}(\rho_t, 1{-}\epsilon, 1{+}\epsilon)\, A_t\big)\big]$$
  (**maximized**, despite the $\mathcal{L}$ — PPO's objective is a reward-like surrogate, not a loss)
  — take policy-gradient steps but *clip away the incentive* to move far from the data-
  collecting policy. A trust region by clamp, plus (in RLHF) an explicit KL penalty
  ([[02-foundations/information-theory|information theory]]).

### 5. Model-based RL — the world-model connection

- Model-free RL asks the *real world* for every gradient — untenable for robots (time,
  wear, safety). Model-based RL learns $\hat p(s'|s,a)$ and trains the policy on
  *imagined* rollouts: [[01-canonical-papers/notes/5-world-models/world-models|World Models]] →
  [[01-canonical-papers/notes/5-world-models/planet|PlaNet]] (plan through the model) →
  [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]] (backprop through the model).
- The tradeoff: sample efficiency vs **model bias** — errors compound over imagined
  horizons (the same compounding-error logic as [[01-canonical-papers/notes/4-vla/act|ACT]]'s
  motivation), managed by short horizons and value bootstrapping.

### 6. RL vs imitation in robot learning (orientation map)

- **Imitation** ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]],
  [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]): supervised on demos —
  stable, no reward design, but plain offline BC is capped by data coverage and cannot
  learn recoveries *outside the support of its demos* (demos with recoveries, or DAgger-style
  data collection, change this).
- **RL** *can* exceed the demonstrator — when an informative reward and enough exploration
  are available — practical mostly in
  simulation (sim-to-real) or as *fine-tuning* atop imitation-pretrained VLAs, mirroring
  the [[01-canonical-papers/notes/1-foundations/instructgpt|pretrain → RLHF]] recipe.

**The imitation-learning toolbox** (the vocabulary of every VLA paper). Read it in three
groups — *the core objective and its one failure mode*, *what the data looks like*, and
*what makes a policy expressive* — not as six loose facts.

*Group 1 — the objective and its Achilles' heel.* **BC** just maximizes
$\log \pi_\theta(a|o)$ over demo pairs — supervised learning wearing a policy costume
([[01-canonical-papers/how-to-read|how-to-read §3]] walks this exact equation). Its one
structural weakness is **covariate shift**: the policy is trained on *expert* states but
runs on *its own*, so small errors drift the state off-distribution where errors compound.
That single failure mode is why **DAgger** exists — execute the learner, let the expert
label the states it actually visited, retrain.

*Group 2 — reading a dataset section.* Demos come from teleoperation
([[01-canonical-papers/notes/4-vla/act|ALOHA]]-style rigs, VR, kinesthetic teaching), scripted
policies, or cross-embodiment pooling ([[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]]).
Two things to check: **time-synchronization** (a mislabeled 100 ms offset silently corrupts
every observation-action pair) and **curation over count** — success filtering and
*trajectory diversity* (scenes, objects, initial conditions) usually matter more than "N
thousand demos," which is the number to audit skeptically.

*Group 3 — why the fancy output heads exist.* Demonstrations are **multimodal**: two
experts pass an obstacle on opposite sides, so a mean-regressing policy drives straight
through the middle. The fixes you'll meet are **action chunking** (predict $k$ future
actions at once — [[01-canonical-papers/notes/4-vla/act|ACT]] — trading reactivity to fight
compounding error) and **expressive heads** that can represent multiple modes
([[01-canonical-papers/notes/4-vla/diffusion-policy|diffusion]],
[[01-canonical-papers/notes/4-vla/pi0|flow matching]]). (Action *representation* also varies:
absolute vs delta, joint vs end-effector space.) Aside: **offline RL** learns from a fixed
dataset too, but uses rewards to *stitch* behavior better than any single demonstrator — at
the price of value-extrapolation instability BC never has.

Entry chain into the papers: this section →
[[01-canonical-papers/notes/4-vla/act|ACT]] →
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] →
[[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]] →
[[01-canonical-papers/notes/4-vla/rt-1|RT-1]]/[[01-canonical-papers/notes/4-vla/rt-2|RT-2]] →
[[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]/[[01-canonical-papers/notes/4-vla/pi0|π0]].

- Decoder ring for papers: "BC baseline" = behavior cloning; "advantage-weighted" =
  policy improvement re-weighted by $e^{A/\beta}$; "KL-regularized policy" = stay near a
  reference policy while improving.

### Self-check

1. Derive the Bellman expectation equation from the definition of $V^\pi$ (one line of
   linearity + Markov).
2. Why does subtracting a state-only baseline leave the policy gradient unbiased?
   (Show $E_{a\sim\pi}[\nabla\log\pi(a|s)] = 0$.)
3. In PPO's objective, what does the $\min$ do when $A_t > 0$ vs $A_t < 0$? Why clip at all?
4. Give two reasons Dreamer-style imagination training keeps horizons short (~15 steps).
5. Why does action chunking reduce compounding error, and what does it trade away?

### Robotics bridge

MDPs, policies, and uncertainty connect to graph/trajectory methods and belief-space reasoning in [[04-robotics/planning-decision-making|Planning & Decision-Making]].

## 한국어

MDP 어휘 없이는 [[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]]도,
[[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]] 계열도, 현대 로봇 학습의 절반도 읽을 수 없다.
교재 수준의 서술: 벨만 기계장치, 갱신 규칙까지 포함한 두 알고리즘 계열, 정책 그래디언트
정리, 그리고 PPO의 실제 목적함수.

### 1. MDP

- **마르코프 결정 과정** $(\mathcal{S}, \mathcal{A}, p, r, \gamma)$: 상태, 행동, 전이 커널
  $p(s'|s,a)$, 보상 $r(s,a)$, 할인율 $\gamma \in [0,1)$.
  마르코프 = 상태가 과거를 요약한다 ([[02-foundations/probability|확률]]).
- **정책** $\pi(a|s)$; **리턴** $G_t = \sum_{k\ge 0} \gamma^k r_{t+k}$; 목표
  $J(\pi) = E_\pi[G_0]$. 할인은 무한 합을 유한하게 만들고 조급함을 인코딩한다;
  $1/(1-\gamma)$이 유효 지평이다 (γ=0.99 ⇒ 약 100 스텝).
- 로보틱스의 현실: 상태는 *관측되지 않는다*(POMDP) — 보이는 건 이미지와 고유수용감각.
  실전적 우회: 관측 이력/순환 상태를 조건으로 ([[01-canonical-papers/notes/5-world-models/dreamer|RSSM]]이
  이를 정식화한 것).

### 2. 가치 함수와 벨만 방정식

- $V^\pi(s) = E_\pi[G_t | s_t{=}s]$, $Q^\pi(s,a) = E_\pi[G_t | s_t{=}s, a_t{=}a]$,
  **어드밴티지** $A^\pi = Q^\pi - V^\pi$ (내 평균 수보다 얼마나 나은가).
- **벨만 기대 방정식** ($V^\pi$의 일관성):
  $$V^\pi(s) = E_{a\sim\pi,\, s'\sim p}\big[r(s,a) + \gamma V^\pi(s')\big]$$
- **벨만 최적성**: $Q^*(s,a) = E\big[r + \gamma \max_{a'} Q^*(s',a')\big]$;
  $Q^*$에 대한 탐욕 정책이 최적이다.
- 이들은 고정점 방정식이고, 벨만 연산자는 $\gamma$-수축이라 반복하면 수렴한다 —
  아래 모든 것의 면허장.

### 3. 동적 계획법과 TD 학습

- **가치 반복**: 최적성 연산자를 반복 적용 (모델 $p$ 필요).
  **정책 반복**: $\pi$를 평가하고 탐욕적으로 개선; 반복.
- 모델이 없으면 샘플링: **TD(0)** 갱신
  $V(s) \leftarrow V(s) + \alpha\,[\underbrace{r + \gamma V(s')}_{\text{타깃}} - V(s)]$
  — 자기 자신의 추정으로 부트스트랩. 괄호 안이 **TD 오차** $\delta$, RL의 만능 학습 신호다.
- **Q-learning** (off-policy):
  $Q(s,a) \leftarrow Q(s,a) + \alpha\,[r + \gamma \max_{a'}Q(s',a') - Q(s,a)]$
  DQN = 이것 + 신경망 $Q$ + 리플레이 버퍼 + 타깃 네트워크(안정된 타깃을 위한
  [[02-foundations/calculus-backprop|stop-gradient]] 복사본).
- 가치 기반은 샘플 효율이 좋지만 연속 행동에 어색하다($\max_{a'}$가 내부 최적화를
  요구) — 로보틱스가 정책 쪽으로 기우는 이유.
- **계산 예제 — 종이로 하는 가치 반복.** 상태 둘, 고정 정책, $\gamma = 0.9$:
  상태 $A$는 보상 1을 주고 $B$로, $B$는 0을 주고 $A$로 간다. 벨만:
  $V(A) = 1 + 0.9V(B)$, $V(B) = 0.9V(A)$. $V_0 = (0,0)$에서 반복하면
  $V_1 = (1, 0)$, $V_2 = (1, 0.9)$, $V_3 = (1.81, 0.9)$, … 고정점
  $V(A) = 1/(1-0.81) \approx 5.26$, $V(B) \approx 4.74$로 수렴한다. 무슨 일이 일어났는지
  보라: 스윕마다 보상 정보가 한 스텝씩 뒤로 전파된다 — "부트스트래핑"의 의미가 이것의 전부다.

### 4. 정책 그래디언트 — 목적함수 자체를 미분하기

- **로그 미분 트릭** (유도 전체가 세 단계):
  $$\nabla_\theta J = \nabla_\theta \int p_\theta(\tau) G(\tau)\,d\tau = \int p_\theta(\tau)\,\nabla_\theta \log p_\theta(\tau)\, G(\tau)\,d\tau = E_\tau\Big[\sum_t \nabla_\theta \log \pi_\theta(a_t|s_t)\, G_t\Big]$$
  (동역학 항은 $\theta$에 의존하지 않아 $\nabla\log p_\theta(\tau)$에서 사라진다.)
  해석: *뒤따른 리턴에 비례해 행동의 로그 확률을 올려라*.
- **REINFORCE**가 정확히 이것 — 불편이지만 분산이 파국적으로 크다. 분산 감소책, 중요한
  순서로: **베이스라인** $b(s)$ 빼기(상태만의 베이스라인이면 무편향; 최선은 ≈ $V(s)$,
  그러면 가중치가 어드밴티지 $A$가 된다); reward-to-go 사용; **actor-critic**: $V_\phi$를
  TD로 배우고 $\delta = r + \gamma V(s') - V(s)$를 1-샘플 어드밴티지로. **GAE**(generalized advantage estimation)는
  λ 손잡이로 TD(편향, 저분산)와 몬테카를로(무편향, 고분산)를 보간한다.
- **PPO** — 주력 알고리즘 ([[01-canonical-papers/notes/1-foundations/instructgpt|RLHF 속의 그것]]):
  비율 $\rho_t = \pi_\theta(a_t|s_t)/\pi_{old}(a_t|s_t)$에 대해
  $$\mathcal{L} = E_t\big[\min\big(\rho_t A_t,\ \text{clip}(\rho_t, 1{-}\epsilon, 1{+}\epsilon)\, A_t\big)\big]$$
  ($\mathcal{L}$ 표기지만 **최대화**한다 — PPO의 목적함수는 손실이 아니라 보상형 대리 함수다)
  — 정책 그래디언트 스텝을 밟되, 데이터를 모은 정책에서 멀어질 *유인을 클리핑으로
  제거*한다. 클램프로 만든 신뢰 영역, 그리고 (RLHF에서는) 명시적 KL 페널티
  ([[02-foundations/information-theory|정보이론]])까지.

### 5. 모델 기반 RL — 월드모델과의 연결

- 모델 프리 RL은 그래디언트 하나하나를 *실제 세계*에 묻는다 — 로봇에게는 지속 불가능
  (시간, 마모, 안전). 모델 기반 RL은 $\hat p(s'|s,a)$를 배우고 *상상된* 롤아웃으로 정책을
  학습한다: [[01-canonical-papers/notes/5-world-models/world-models|World Models]] →
  [[01-canonical-papers/notes/5-world-models/planet|PlaNet]](모델을 통해 계획) →
  [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]](모델을 통해 역전파).
- 트레이드오프: 샘플 효율 vs **모델 편향** — 상상 지평에서 오차가 누적된다
  ([[01-canonical-papers/notes/4-vla/act|ACT]]의 동기였던 복합 오차와 같은 논리); 짧은 지평과 가치
  부트스트래핑으로 관리한다.

### 6. 로봇 학습에서 RL vs 모방 (지도)

- **모방** ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]],
  [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]): 시연에 대한 지도학습 —
  안정적이고 보상 설계가 없지만, 순수 오프라인 BC는 데이터 커버리지가 상한이고 *시연
  분포 밖의* 회복 동작은 학습할 수 없다(회복이 담긴 시연이나 DAgger식 데이터 수집은
  이를 바꾼다).
- **RL**은 유익한 보상과 충분한 탐색이 있으면 시연자를 넘어설 *수 있다* — 주로
  시뮬레이션(sim-to-real)
  에서, 또는 모방으로 사전학습된 VLA 위의 *파인튜닝*으로 —
  [[01-canonical-papers/notes/1-foundations/instructgpt|사전학습 → RLHF]] 레시피의 미러링이다.

**모방 학습 도구 상자** (모든 VLA 논문의 어휘). 여섯 개의 사실이 아니라 *세 묶음*으로
읽어라 — *핵심 목적함수와 그 하나의 약점*, *데이터의 모습*, *정책을 표현력 있게 만드는 것*.

*묶음 1 — 목적함수와 아킬레스건.* **BC**는 시연 쌍에 대해 $\log \pi_\theta(a|o)$를 최대화할
뿐 — 정책의 옷을 입은 지도학습이다([[01-canonical-papers/how-to-read|how-to-read §3]]이 이
식을 해부한다). 유일한 구조적 약점은 **covariate shift**다: 정책은 *전문가의* 상태에서
학습되지만 *자신의* 상태에서 실행되므로, 작은 오차가 상태를 분포 밖으로 밀고 거기서 오차가
누적된다. 이 하나의 실패 모드가 **DAgger**가 존재하는 이유다 — 학습자를 실행시키고, 실제로
방문한 상태를 전문가가 라벨하고, 재학습.

*묶음 2 — 데이터셋 절 읽기.* 시연은 원격조작([[01-canonical-papers/notes/4-vla/act|ALOHA]]식
장비, VR, 직접 교시), 스크립트 정책, 교차-embodiment 풀링
([[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]])에서 온다. 확인할 것 둘:
**시간 동기화**(100 ms 어긋난 라벨이 모든 관측-행동 쌍을 조용히 오염시킨다)와 **개수보다
큐레이션** — 성공 필터링과 *궤적 다양성*(장면·물체·초기 조건)이 "시연 N천 개"보다 대개 더
중요하며, 그 개수야말로 회의적으로 검사할 대상이다.

*묶음 3 — 화려한 출력 헤드가 존재하는 이유.* 시연은 **다봉**이다: 두 전문가가 장애물을
반대쪽으로 지나가면 평균 회귀 정책은 한가운데로 돌진한다. 만나게 될 처방은 **행동
청킹**(미래 행동 $k$개를 한 번에 예측 — [[01-canonical-papers/notes/4-vla/act|ACT]] — 반응성을
지불해 오차 누적과 싸움)과 여러 모드를 표현할 수 있는 **표현력 있는 헤드**
([[01-canonical-papers/notes/4-vla/diffusion-policy|디퓨전]],
[[01-canonical-papers/notes/4-vla/pi0|flow matching]])다. (행동 *표현*도 갈린다: 절대 vs 델타,
관절 vs 말단 공간.) 곁가지: **오프라인 RL**도 고정 데이터셋에서 배우지만 보상으로 어느 단일
시연자보다 나은 행동을 *꿰맨다* — BC엔 없는 가치 외삽 불안정을 대가로.

논문으로 들어가는 진입 사슬: 이 절 →
[[01-canonical-papers/notes/4-vla/act|ACT]] →
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] →
[[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]] →
[[01-canonical-papers/notes/4-vla/rt-1|RT-1]]/[[01-canonical-papers/notes/4-vla/rt-2|RT-2]] →
[[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]/[[01-canonical-papers/notes/4-vla/pi0|π0]].

- 논문 해독기: "BC baseline" = 행동 복제; "advantage-weighted" = $e^{A/\beta}$로 재가중된
  정책 개선; "KL-regularized policy" = 기준 정책 근처에 머물며 개선하기.

### 스스로 점검

1. $V^\pi$의 정의에서 벨만 기대 방정식을 유도하라 (선형성 + 마르코프 한 줄).
2. 상태만의 베이스라인을 빼도 정책 그래디언트가 무편향인 이유는?
   ($E_{a\sim\pi}[\nabla\log\pi(a|s)] = 0$을 보여라.)
3. PPO 목적함수의 $\min$은 $A_t > 0$일 때와 $A_t < 0$일 때 각각 무슨 일을 하는가?
   애초에 왜 클리핑하는가?
4. Dreamer식 상상 학습이 지평을 짧게(~15 스텝) 유지하는 이유 두 가지를 들어라.
5. 행동 청킹이 오차 누적을 줄이는 이유는? 그 대가로 잃는 것은?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $V^\pi(s) = E[r_t + \gamma G_{t+1} \mid s]$에서 안쪽 기댓값을 마르코프 성질로 $V^\pi(s')$로 접으면 $E[r + \gamma V^\pi(s')]$.
> 2. $E_{a\sim\pi}[\nabla\log\pi(a|s)]\,b(s) = b(s)\,\nabla E_{a\sim\pi}[1] = b(s)\,\nabla 1 = 0$ — 스코어 함수의 기댓값이 0이라 베이스라인 항이 사라진다.
> 3. $A_t > 0$: 비율이 $1+\epsilon$을 넘으면 이득이 잘려 과도한 확률 *증가* 유인이 사라진다. $A_t < 0$: 비율이 $1-\epsilon$ 아래로 내려가는 과도한 확률 *감소*가 클리핑으로 제한되고, min이 잘리지 않은(더 나쁜) 항을 고르므로 정책이 나쁜 방향으로 움직이는 동안에는 페널티가 계속 작용한다. 클리핑의 목적 = 데이터를 모은 정책 근처에 머무는 신뢰 영역.
> 4. ① 모델 오차가 상상 지평을 따라 지수적으로 누적된다(복합 오차) ② 가치 부트스트랩이 짧은 지평 너머를 대신 평가하므로 길 필요가 없다.
> 5. 정책이 자기 오차 위에서 다시 예측하는 횟수가 $k$분의 1로 줄어 분포 이탈이 느려진다; 대가는 반응성 — 청크 실행 중에 들어온 새 관측을 (부분적으로만) 반영한다.

### 로보틱스 다리

MDP·정책·불확실성은 [[04-robotics/planning-decision-making|4. Planning & Decision-Making]]의 그래프/궤적 방법과 belief-space 추론으로 연결된다.
