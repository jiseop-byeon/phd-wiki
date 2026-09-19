---
title: 5. World Models
tags: [deep-learning, world-models, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Separate representation, transition, observation, reward, and planner; roll out a latent model and diagnose model exploitation."
mastery-when: "Raise when learned dynamics, latent planning, uncertainty, or model-based data generation carries the contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/probability|3. Probability]], [[02-foundations/rl-basics|7. RL]], and [[04-robotics/state-estimation-slam|3. State Estimation]].

## English

### Running object: D5

**D5** uses scalar latent dynamics $z_{t+1}=0.8z_t+0.5a_t$ and reward $r_t=-z_t^2-0.1a_t^2$. Start at $z_0=1$ and test actions $a_0=-1$, $a_1=0$:

$$z_1=0.3,\quad r_0=-1.1;\qquad z_2=0.24,\quad r_1=-0.09.$$

The model can compare candidate action sequences without executing them in the real world.

### 1. A world model is several models

| Component | Question |
|---|---|
| encoder/inference | what latent state explains observations? |
| transition | how do state and action change it? |
| observation decoder | what would sensors see? |
| reward/termination | what task signal and ending follow? |
| policy/planner | which imagined action sequence should be chosen? |

Some papers omit a pixel decoder and predict representations; others generate video but never use it for control. “World model” does not itself imply planning or physical consistency.

### 2. Multi-step error matters

Suppose the learned coefficient is $0.9$ rather than $0.8$. With zero actions and $z_0=1$, true state after 5 steps is $0.8^5=0.328$ while the model predicts $0.9^5=0.590$. Small one-step bias compounds. Evaluate rollout horizon and downstream decisions, not only one-step loss.

### 3. Planning can exploit model errors

An optimizer searches specifically for trajectories the model rates highly. It can find unrealistic blind spots outside the training distribution. Ensembles, uncertainty penalties, short horizons, replanning, conservative objectives, and real-data correction limit—not eliminate—this problem.

### 4. Read claims by use

Representation learning asks whether latents preserve useful state. Prediction asks whether future observations/states are calibrated. Control asks whether imagined rollouts improve real return or success. Generation quality alone answers none of the other two.

Read [[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]], and JEPA/Genie entries with this component table.

### Problem set

1. **Draw.** Draw observation → encoder → $z_t$ → transition with $a_t$ → $z_{t+1}$, plus reward and planner.
2. **Derive.** From $z_0=1$, compare two-step returns for actions $(-1,0)$ and $(0,0)$ without discount.
3. **Interpret.** A video model has low perceptual loss but no action-conditioned evaluation. Which world-model claim remains unsupported?

> [!tip]- Solutions
> 1. Keep inference, transition, reward, and planning as separate boxes.
> 2. $(-1,0)$ gives $-1.1-0.09=-1.19$; $(0,0)$ gives $-1-0.64=-1.64$, so the first is preferred.
> 3. That it predicts controllable dynamics well enough for planning or policy improvement.

### Exit check

Decompose a world-model paper into five components, identify its rollout horizon and uncertainty treatment, and name the real-world decision metric supporting its claim.

## 한국어

### 계속 쓰는 대상: D5

**D5**는 $z_{t+1}=0.8z_t+0.5a_t$, $r_t=-z_t^2-0.1a_t^2$다. $z_0=1$, 행동 $(-1,0)$이면 $z_1=0.3$, $r_0=-1.1$, $z_2=0.24$, $r_1=-0.09$다. 실제 실행 없이 행동 sequence를 비교할 수 있다.

### 1. 월드모델은 여러 모델이다

encoder/inference는 관측에서 latent state, transition은 행동 뒤 변화, decoder는 센서 관측, reward/termination은 task signal, policy/planner는 상상 rollout에서 행동을 고른다. 일부는 pixel decoder가 없고 일부는 video만 생성한다. “world model”이라는 이름만으로 planning이나 물리 일관성이 보장되지 않는다.

### 2. 다단계 오차

실제 계수 0.8 대신 0.9를 학습했다면 5 step 뒤 실제 $0.328$, 예측 $0.590$이다. 작은 one-step bias가 누적되므로 one-step loss뿐 아니라 rollout horizon과 downstream decision을 평가한다.

### 3. Planner는 모델 오류를 악용한다

optimizer는 모델이 높게 평가하는 trajectory를 적극 찾으므로 학습 분포 밖 허점을 찾을 수 있다. ensemble·uncertainty penalty·짧은 horizon·replanning·보수적 목적함수·실자료 보정은 이를 줄이지만 없애지 않는다.

### 4. 사용에 따라 주장 읽기

representation은 latent가 state를 보존하는지, prediction은 미래가 calibrated됐는지, control은 상상 rollout이 실제 return을 높이는지 묻는다. 생성 화질만으로 나머지를 증명하지 못한다.

### 과제

1. observation→encoder→latent→action-conditioned transition과 reward·planner를 그린다.
2. 행동 $(-1,0)$과 $(0,0)$의 2-step 무할인 return을 비교한다.
3. action-conditioned 평가 없는 고화질 video model이 증명하지 못한 주장은 무엇인가.

> [!tip]- 정답
> 1. inference·transition·reward·planning을 분리한다.
> 2. 각각 $-1.19$, $-1.64$라 첫 sequence가 낫다.
> 3. 제어 가능한 동역학을 planning에 충분히 예측한다는 주장.

### 통과 기준

월드모델을 다섯 구성요소로 분해하고 rollout horizon·불확실성 처리·실세계 의사결정 metric을 말할 수 있다.

