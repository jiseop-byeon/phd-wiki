---
title: Proximal Policy Optimization Algorithms
authors: John Schulman et al.
affiliation: OpenAI
venue: arXiv
year: 2017
arxiv: https://arxiv.org/abs/1707.06347
pdf: https://arxiv.org/pdf/1707.06347
tags: [paper, reinforcement-learning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Schulman et al., arXiv 2017** — [arXiv](https://arxiv.org/abs/1707.06347) · [PDF](https://arxiv.org/pdf/1707.06347)

> [!note] 수학 준비물 · Math on-ramp
> Read the derivation in [[02-foundations/rl-basics|7. RL Basics §4]] first — log-derivative trick → REINFORCE → baseline/advantage → clipped surrogate. This note does not repeat that chain; it covers only what the paper adds on top of it.
> [[02-foundations/rl-basics|RL 기초 §4]]에서 log-derivative trick → REINFORCE → baseline/advantage → clipped surrogate까지의 유도를 먼저 읽어라 — 이 노트는 그 유도를 반복하지 않고, 논문이 그 위에 무엇을 얹었는지만 다룬다.

## English

**One-line summary**: PPO reuses policy-gradient data for several minibatch epochs while clipping probability-ratio changes that would move the new policy too far from the data-collecting policy — TRPO's trust-region idea reduced to a first-order clamp.

### Context

Vanilla policy gradients allow exactly one gradient step per batch of environment interaction — take more and the data is off-policy, and performance can collapse. TRPO (2015) fixed this with a KL-constrained update, but needed second-order machinery (conjugate gradient, line search) that is awkward to implement and does not compose with common architectures. The question PPO answers: can we get TRPO-like stability with nothing but SGD on a modified objective?

### Method

> [!tip] Key intuition
> Instead of *constraining* the policy change, remove the *incentive* to change too much: once the probability ratio leaves $[1-\epsilon, 1+\epsilon]$, clip it so the objective stops rewarding further movement in that direction.

- The clipped surrogate (derived in [[02-foundations/rl-basics|RL 기초 §4]]) is $L^{CLIP}=\mathbb{E}_t[\min(r_t(\theta)A_t,\ \operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)A_t)]$ with ratio $r_t(\theta)=\pi_\theta(a_t|s_t)/\pi_{\theta_{old}}(a_t|s_t)$; typical $\epsilon=0.2$.
- The $\min$ makes clipping one-sided in the pessimistic direction: the objective is a lower bound on the unclipped surrogate, so unfavorable ratio changes are never hidden.
<svg viewBox="0 0 560 268" style="max-width:100%;height:auto" role="img" aria-label="the clipped objective plotted against the probability ratio, flat above one plus epsilon when the advantage is positive and flat below one minus epsilon when it is negative">
  <g font-size="11" fill="currentColor">
    <text x="60" y="18">advantage &gt; 0</text><text x="330" y="18">advantage &lt; 0</text>
  </g>
  <g fill="currentColor" fill-opacity="0.07">
    <rect x="110" y="30" width="100" height="120" rx="2"/>
    <rect x="380" y="30" width="100" height="120" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.55" fill="none">
    <polyline points="60,30 60,150 260,150"/>
    <polyline points="330,30 330,150 530,150"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <polyline points="60,136.2 210,53.8 260,53.8"/>
    <polyline points="330,53.8 380,53.8 530,136.2"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="3 3">
    <line x1="160" y1="30" x2="160" y2="150"/><line x1="430" y1="30" x2="430" y2="150"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.75" text-anchor="middle">
    <text x="110" y="164">1&#8722;&#949;</text><text x="160" y="164">1</text><text x="210" y="164">1+&#949;</text>
    <text x="380" y="164">1&#8722;&#949;</text><text x="430" y="164">1</text><text x="480" y="164">1+&#949;</text>
    <text x="160" y="178">trust band 1 &#177; &#949;</text><text x="430" y="178">trust band 1 &#177; &#949;</text>
    <text x="160" y="192">probability ratio r</text><text x="430" y="192">probability ratio r</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="214" y="48">flat above 1+&#949;</text>
    <text x="334" y="48">flat below 1&#8722;&#949;</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.7">
    <text x="24" y="26">L&#7580;&#7551;&#7615;&#7510;</text><text x="294" y="26">L&#7580;&#7551;&#7615;&#7510;</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="214">With a positive advantage the objective stops rising once r passes 1 + &#949;; with a negative one</text>
    <text x="24" y="230">it stops falling once r drops below 1 &#8722; &#949;. Each case is clipped on exactly one side &#8212; the side</text>
    <text x="24" y="246">that would carry the policy away from the data that produced it &#8212; while the min leaves the</text>
    <text x="24" y="262">unfavourable direction ungated. That is what &#8220;removes the incentive&#8221; means. Drawn with &#949; = 0.2.</text>
  </g>
</svg>

- **This buys data reuse**: collect a batch, then run *multiple epochs* of minibatch SGD on it — the practical speedup over one-step vanilla PG.
- The paper also proposes an adaptive-KL-penalty variant; clipping won empirically and is what "PPO" means in practice.
- The full training loss adds a value-function error term and an entropy bonus, optimized jointly when actor and critic share parameters.

**GAE — not PPO's own, but the estimator it runs on.** (Generalized advantage estimation is Schulman et al. 2015, [arXiv:1506.02438](https://arxiv.org/abs/1506.02438); PPO cites and truncates it.) The advantage $A_t$ is estimated with **generalized advantage estimation** (truncated at the rollout horizon $T$ in practice): with TD residual $\delta_t=r_t+\gamma V(s_{t+1})-V(s_t)$, GAE takes $A_t^{GAE}=\sum_{l\ge 0}(\gamma\lambda)^l\delta_{t+l}$ — a λ-interpolation between one-step TD ($\lambda=0$: biased, low variance) and Monte Carlo returns ($\lambda=1$: unbiased, high variance). Every serious PPO implementation pairs clipping with GAE (typically $\lambda\approx 0.95$); reading "PPO" without reading GAE misses half the algorithm.

### Results

**What it measured.** The abstract reports no quantitative result. [Abstract checked](https://arxiv.org/abs/1707.06347).

- On MuJoCo continuous control, clipped PPO beats or matches TRPO, A2C, and vanilla PG variants on most tasks with a far simpler implementation.
- Scales to harder settings in the paper — Roboschool humanoid running/steering and Atari — with the same recipe.
- The clipping limits the *incentive* for excessive change; it is not a hard bound on parameter distance and carries no monotonic-improvement guarantee.

### Limitations & critique

- No theoretical guarantee survives from TRPO: clipping is a heuristic trust region, and large updates can still slip through (ratios are only evaluated on sampled actions).
- Notoriously sensitive to code-level details — advantage normalization, value clipping, learning-rate annealing, reward scaling — which later replication studies found can matter as much as the clipping itself.
- On-policy at heart: sample efficiency is far below off-policy methods like [[01-canonical-papers/notes/1-foundations/sac|SAC]], which matters when samples are expensive.

### Impact & follow-ups

The default policy-gradient algorithm of the field: simulator locomotion, dexterous manipulation, game-playing, and — via RLHF — language-model alignment ([[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]] runs PPO in its third stage). In construction robotics, PPO-class methods train the simulator experts that pipelines like [[01-canonical-papers/notes/8-construction/ext|ExT]] later distill into deployable transformer policies.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> "PPO-trained" does not specify observation design, reward, simulator, curriculum, safety constraints, or real transfer. These choices often explain more than the optimizer name — read them before crediting or blaming PPO.

### Connections

- Math on-ramp: [[02-foundations/rl-basics|RL 기초 §4]] (clipped objective derived there)
- Downstream: [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]] (PPO inside RLHF) · [[01-canonical-papers/notes/8-construction/ext|ExT]] (RL experts trained with PPO-class methods)
- Counterpart: [[01-canonical-papers/notes/1-foundations/sac|SAC]] (off-policy alternative)
- Deployment context: [[05-construction-robotics/sim-to-real|sim-to-real guide]]

## 한국어

**한 줄 요약**: PPO는 행동 확률비가 데이터를 수집한 정책에서 너무 멀어지려는 변화를 clip하면서 정책경사 데이터를 여러 minibatch epoch에 재사용한다 — TRPO의 trust-region 아이디어를 1차 최적화의 clamp 하나로 줄인 것.

### 배경

순수 정책경사는 환경 상호작용 한 배치당 정확히 한 번의 그래디언트 스텝만 허용한다 — 더 밟으면 데이터가 off-policy가 되어 성능이 무너질 수 있다. TRPO(2015)는 KL 제약 업데이트로 이를 고쳤지만 2차 최적화 장치(conjugate gradient, line search)가 필요해 구현이 번거롭고 일반적인 아키텍처와 잘 결합되지 않았다. PPO가 답하는 질문: 수정된 목적함수에 SGD만 돌려서 TRPO급 안정성을 얻을 수 있는가?

### 방법

> [!tip] 핵심 직관
> 정책 변화를 *제약*하는 대신 과도하게 변할 *유인*을 제거하라: 확률비가 $[1-\epsilon, 1+\epsilon]$ 밖으로 나가면 clip해서, 그 방향으로 더 움직여도 목적함수가 보상하지 않게 만든다.

- clipped surrogate([[02-foundations/rl-basics|RL 기초 §4]]에서 유도)는 $L^{CLIP}=\mathbb{E}_t[\min(r_t(\theta)A_t,\ \operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)A_t)]$, 확률비는 $r_t(\theta)=\pi_\theta(a_t|s_t)/\pi_{\theta_{old}}(a_t|s_t)$; 통상 $\epsilon=0.2$.
- $\min$이 clip을 비관적 방향으로 한쪽만 작동하게 만든다: 목적함수는 clip 없는 surrogate의 하한이 되어, 불리한 확률비 변화는 절대 가려지지 않는다.
<svg viewBox="0 0 560 268" style="max-width:100%;height:auto" role="img" aria-label="확률비에 대한 clip된 목적함수 그래프. advantage가 양수면 1+엡실론 위에서 평평하고 음수면 1-엡실론 아래에서 평평하다">
  <g font-size="11" fill="currentColor">
    <text x="60" y="18">advantage &gt; 0</text><text x="330" y="18">advantage &lt; 0</text>
  </g>
  <g fill="currentColor" fill-opacity="0.07">
    <rect x="110" y="30" width="100" height="120" rx="2"/>
    <rect x="380" y="30" width="100" height="120" rx="2"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" opacity="0.55" fill="none">
    <polyline points="60,30 60,150 260,150"/>
    <polyline points="330,30 330,150 530,150"/>
  </g>
  <g stroke="currentColor" stroke-width="2.4" fill="none">
    <polyline points="60,136.2 210,53.8 260,53.8"/>
    <polyline points="330,53.8 380,53.8 530,136.2"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="3 3">
    <line x1="160" y1="30" x2="160" y2="150"/><line x1="430" y1="30" x2="430" y2="150"/>
  </g>
  <g font-size="9" fill="currentColor" opacity="0.75" text-anchor="middle">
    <text x="110" y="164">1&#8722;&#949;</text><text x="160" y="164">1</text><text x="210" y="164">1+&#949;</text>
    <text x="380" y="164">1&#8722;&#949;</text><text x="430" y="164">1</text><text x="480" y="164">1+&#949;</text>
    <text x="160" y="178">신뢰 구간 1 &#177; &#949;</text><text x="430" y="178">신뢰 구간 1 &#177; &#949;</text>
    <text x="160" y="192">확률비 r</text><text x="430" y="192">확률비 r</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="214" y="48">1+&#949; 위로는 평평</text>
    <text x="334" y="48">1&#8722;&#949; 아래는 평평</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.7">
    <text x="24" y="26">L&#7580;&#7551;&#7615;&#7510;</text><text x="294" y="26">L&#7580;&#7551;&#7615;&#7510;</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="214">advantage가 양수면 r이 1 + &#949;를 넘는 순간 목적함수가 더 오르지 않고, 음수면 r이 1 &#8722; &#949; 아래로</text>
    <text x="24" y="230">내려가는 순간 더 내려가지 않는다. 두 경우 모두 잘리는 쪽은 정확히 한쪽 &#8212; 정책을 그 데이터에서</text>
    <text x="24" y="246">멀어지게 하는 쪽 &#8212; 뿐이고, min이 불리한 방향은 가리지 않고 남겨 둔다.</text>
    <text x="24" y="262">clip이 변화를 제약하는 것이 아니라 과도하게 변할 *유인*을 없앤다는 말의 뜻이 이것이다. &#949; = 0.2.</text>
  </g>
</svg>

- **이것이 데이터 재사용을 산다**: 배치를 모은 뒤 그 위에서 *여러 epoch*의 minibatch SGD를 돌린다 — 1스텝 순수 정책경사 대비 실질적인 효율 향상.
- 논문은 적응형 KL 페널티 변형도 제안하지만, 실험에서 clip이 이겼고 실무에서 "PPO"는 clip 버전을 뜻한다.
- 전체 학습 손실에는 가치함수 오차 항과 entropy 보너스가 추가되며, actor와 critic이 파라미터를 공유할 때 함께 최적화된다.

**GAE — 논문의 나머지 절반.** Advantage $A_t$는 **generalized advantage estimation**(실전에서는 롤아웃 지평 $T$에서 절단)으로 추정한다: TD 잔차 $\delta_t=r_t+\gamma V(s_{t+1})-V(s_t)$에 대해 $A_t^{GAE}=\sum_{l\ge 0}(\gamma\lambda)^l\delta_{t+l}$ — 1스텝 TD($\lambda=0$: 편향, 저분산)와 Monte Carlo 수익($\lambda=1$: 무편향, 고분산) 사이를 λ로 보간한다. 제대로 된 PPO 구현은 전부 clip과 GAE를 짝지어 쓴다(보통 $\lambda\approx 0.95$); GAE 없이 "PPO"만 읽으면 알고리즘의 절반을 놓친 것이다.

### 결과

**무엇을 쟀는가.** 초록에 정량 결과가 제시되지 않았다. [초록 확인](https://arxiv.org/abs/1707.06347).

- MuJoCo 연속 제어에서 clipped PPO는 대부분의 과제에서 TRPO, A2C, 순수 정책경사 변형을 이기거나 대등하다 — 훨씬 단순한 구현으로.
- 같은 레시피로 논문 내 더 어려운 설정 — Roboschool humanoid 달리기/조향, Atari — 까지 확장된다.
- clip은 과도한 변화의 *유인*을 제한할 뿐이다; 파라미터 거리에 대한 hard bound가 아니고 성능의 단조 향상도 보장하지 않는다.

### 한계와 비판

- TRPO의 이론적 보장은 남지 않는다: clip은 휴리스틱 trust region이고, 큰 업데이트가 여전히 새어 나갈 수 있다(확률비는 샘플된 행동에서만 평가되므로).
- 코드 수준 세부사항에 악명 높게 민감하다 — advantage 정규화, value clipping, 학습률 annealing, 보상 스케일링 — 이후 재현 연구들은 이것들이 clip 자체만큼 중요할 수 있음을 밝혔다.
- 본질적으로 on-policy: 샘플 효율은 [[01-canonical-papers/notes/1-foundations/sac|SAC]] 같은 off-policy 방법에 크게 못 미치고, 샘플이 비쌀수록 이 차이가 아프다.

### 영향과 후속 연구

이 분야 정책경사의 기본값: 시뮬레이터 locomotion, 정밀 조작, 게임, 그리고 RLHF를 통한 언어모델 정렬까지([[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]]의 3단계가 바로 PPO다). 건설 로보틱스에서는 [[01-canonical-papers/notes/8-construction/ext|ExT]] 같은 파이프라인이 나중에 배포용 transformer 정책으로 증류할 시뮬레이터 expert를 PPO 계열로 학습한다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "PPO로 학습했다"는 관측 설계, 보상, 시뮬레이터, 커리큘럼, 안전 제약, 실기계 전이를 아무것도 특정하지 않는다. 이 선택들이 옵티마이저 이름보다 더 많은 것을 설명하는 경우가 많다 — PPO를 칭찬하거나 탓하기 전에 이것들부터 읽어라.

### 연결

- 수학 준비물: [[02-foundations/rl-basics|RL 기초 §4]] (clipped objective가 거기서 유도된다)
- 하류: [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT/RLHF]] (RLHF 안의 PPO) · [[01-canonical-papers/notes/8-construction/ext|ExT]] (PPO 계열로 학습한 RL expert)
- 대응 관계: [[01-canonical-papers/notes/1-foundations/sac|SAC]] (off-policy 대안)
- 배포 맥락: [[05-construction-robotics/sim-to-real|sim-to-real guide]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain what $r_t$, the advantage, and the clip each do, and why the $\min$ is needed · $r_t$, advantage, clip이 각각 무엇을 하고, $\min$이 왜 필요한지 설명할 수 있다
- [ ] Say what PPO's clip does *not* guarantee (not a hard constraint, not monotonic improvement) · PPO clip이 보장하지 않는 것(hard constraint 아님, 단조 향상 아님)을 말할 수 있다
- [ ] Say what GAE's λ interpolates between, and why it is always paired with the clip · GAE의 λ가 무엇과 무엇 사이를 보간하는지, 왜 clip과 항상 짝지어 쓰이는지 말할 수 있다
- [ ] Identify how far PPO's role extends in an excavation pretraining/fine-tuning pipeline such as ExT · 굴착 pretraining/finetuning 파이프라인(예: ExT)에서 PPO의 역할이 어디까지인지 짚을 수 있다
