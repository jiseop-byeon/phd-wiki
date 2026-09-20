---
title: 0. Deep-Learning Lab Objects
tags: [deep-learning, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Reuse six small, fully specified objects to trace tensor shapes, objectives, inference, and failure across the deep-learning curriculum."
mastery-when: "Raise only the object family that becomes part of the thesis contribution."
---

## English

These objects are deliberately tiny. Their purpose is not benchmark performance; it is to make every symbol and tensor in the six course pages concrete. All numbers below are fixed so that a calculation in one page can be checked in another.

| ID | Object | Fixed specification | Used in |
|---|---|---|---|
| **D1** | small classifier | $x=(1,2)$, $W_1\in\mathbb R^{3\times2}$, $W_2\in\mathbb R^{2\times3}$, biases $0$; forward $s=(2,1)$ | learning foundations |
| **D2** | patch image | grayscale $8\times8$ image, $4\times4$ patches, 4 patch tokens | computer vision |
| **D3** | aligned batch | three unit 2-D pairs, $\tau=1/2$; image-1 logits $(2,1,0)$ | VLM |
| **D4** | action chunk | observation token plus three 2-D delta actions of $0.02\,\mathrm{m}$; 20 Hz control, 100 ms inference | VLA |
| **D5** | scalar latent plant | $z_{t+1}=0.8z_t+0.5a_t$, reward $r_t=-z_t^2-0.1a_t^2$, $z_0=1$ | world models |
| **D6** | scalar diffusion datum | clean $x_0=2$, noise $\epsilon=-1$, $\bar\alpha_t=0.64$ on a 20-level schedule | diffusion and flow |

### The common reading contract

For every object, keep four lines separate:

1. **Representation:** what numbers stand for the world.
2. **Prediction:** what the model computes from its inputs.
3. **Objective:** which discrepancy changes learned parameters.
4. **Evaluation:** which measurement supports the paper's claim.

If a paper changes only line 1, it proposes a representation. If it changes line 3, it proposes a training method. If it reports only line 4 without defining the deployment distribution, its claim is incomplete. This four-line ledger is the bridge from the equations here to the canonical-paper notes.

### Frozen numbers

**D1.** Biases zero, $\sigma=\mathrm{ReLU}$. Distinct from **P1** ($2\to3\to1$ MSE) on [[02-foundations/lab-plants|0.6]].

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}$$

Forward: $W_1x=(1,2,1)$, $h=(1,2,1)$, $s=W_2h=(2,1)$. Home of [[03-deep-learning/foundations/index|1. Learning Systems]].

**D3.** Matched pairs are aligned. All vectors are unit length.

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix},\quad\tau=\tfrac12$$

Dots $v_1^\top t_j=(1,1/2,0)$, so image-1 logits are $\ell_{1j}=v_1^\top t_j/\tau=(2,1,0)$. Lowering $\tau$ to $1/4$ on the same row gives $(4,2,0)$. Home of [[03-deep-learning/vlm/index|3. VLM]].

**D4.** A 2-D task plane in metres, with the clocks that make a chunk a latency decision. The instruction is "move left, then down," and the policy plans one axis at a time.

$$o=(p_x,p_y,g_x,g_y),\quad p_0=(0,0),\quad g=(-0.04,-0.02),\quad a_{1:3}=\big\{(-0.02,0),\,(-0.02,0),\,(0,-0.02)\big\}$$

Interface limit $a_{\max}=0.02\,\mathrm{m}$ per control step, axis-switch band $\delta=0.005\,\mathrm{m}$, control period $\Delta t=0.05\,\mathrm{s}$, inference $t_{\mathrm{inf}}=0.10\,\mathrm{s}$, per-axis perception jitter $\sigma=0.002\,\mathrm{m}$. The chunk's path length is $0.06\,\mathrm{m}$ for a net displacement of $0.0447\,\mathrm{m}$. Home of [[03-deep-learning/vla/index|4. VLA]]. Nearest plant on [[02-foundations/lab-plants|0.6]] is **P6**, the cart and a clock; both carry two rates and a delay, but P6 delays a single *measurement* through a pipeline while D4 delays a *buffer of decisions*, so D4's staleness grows with the chunk length and not only with transport.

**D5.** Discrete-time scalar latent, with the two learned gains the page compares and the grid a planner may search.

$$z_{t+1}=\lambda z_t+\beta a_t,\quad \lambda=0.8,\ \beta=0.5,\ z_0=1,\quad r_t=-z_t^2-0.1a_t^2,\quad a_t\in\{-1,-\tfrac12,0,\tfrac12,1\}$$

Test sequence $(a_0,a_1)=(-1,0)$: $z_1=0.3$, $r_0=-1.1$, $z_2=0.24$, $r_1=-0.09$, two-step return $-1.19$. Learned gains $\hat\lambda=0.9$ (pessimistic) and $\hat\lambda'=0.7$ (optimistic), both with $\hat\beta=\beta$. Home of [[03-deep-learning/world-models/index|5. World Models]]. Nearest plant is **P4**, the leaky heater: P4's model is exact and its uncertainty is an additive disturbance a controller rejects, while D5's *parameter* is wrong and the map is iterated, so its error compounds through its own gain.

**D6.** One datum, one noise draw, and the schedule that turns them into a level.

$$\sqrt{\bar\alpha_i}=1-0.8\,\frac{i}{T},\quad T=20,\qquad x_0=2,\ \epsilon=-1,\qquad \bar\alpha_5=0.64,\ \bar\alpha_{20}=0.04$$

The catalog level is $i=5$, where $x_5=0.8(2)+0.6(-1)=1$; there $\alpha_5=\bar\alpha_5/\bar\alpha_4=(20/21)^2=0.907029$ and $\beta_5=41/441=0.092971$. The frozen network returns $\epsilon_\theta(x,i)=(x-\sqrt{\bar\alpha_i}x_0)/\sqrt{1-\bar\alpha_i}+b$ with $b=0.2$, so it outputs $-0.8$ at the catalog level, and one network call is assumed to cost $c=5\,\mathrm{ms}$. Home of [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]. Nearest plant is **P5**, the 1-D range: P5 fuses one noisy reading of a static scalar in a single step with a known variance, while D6 corrupts a known scalar across a *sequence* of noise levels and inverts it in a chosen number of steps, so its error depends on which level the last estimate was made at rather than on one gain.

## 한국어

이 장치들은 의도적으로 작다. 벤치마크 성능이 목적이 아니라 여섯 교과 페이지의 기호와 텐서를 모두 손으로 추적하는 것이 목적이다. 한 페이지의 계산을 다른 페이지에서 검산할 수 있도록 숫자를 고정한다.

| ID | 대상 | 고정 사양 | 사용처 |
|---|---|---|---|
| **D1** | 작은 분류기 | $x=(1,2)$, $W_1\in\mathbb R^{3\times2}$, $W_2\in\mathbb R^{2\times3}$, bias $0$; 순전파 $s=(2,1)$ | 학습 기초 |
| **D2** | 패치 이미지 | 회색조 $8\times8$, $4\times4$ 패치, 패치 토큰 4개 | 컴퓨터비전 |
| **D3** | 정렬 배치 | 단위 2차원 3쌍, $\tau=1/2$; 이미지 1 logit $(2,1,0)$ | VLM |
| **D4** | 행동 청크 | 관측 토큰 하나와 $0.02\,\mathrm{m}$짜리 2차원 델타 행동 3개; 제어 20 Hz, 추론 100 ms | VLA |
| **D5** | 스칼라 잠재 장치 | $z_{t+1}=0.8z_t+0.5a_t$, $r_t=-z_t^2-0.1a_t^2$, $z_0=1$ | 월드모델 |
| **D6** | 스칼라 확산 자료 | $x_0=2$, 잡음 $\epsilon=-1$, 20레벨 schedule 위의 $\bar\alpha_t=0.64$ | 디퓨전·flow |

### 공통 독해 계약

모든 대상에서 네 줄을 분리한다.

1. **표현:** 어떤 숫자가 세계의 무엇을 뜻하는가.
2. **예측:** 모델이 입력에서 무엇을 계산하는가.
3. **목적함수:** 어떤 오차가 학습 파라미터를 바꾸는가.
4. **평가:** 어떤 측정이 논문의 주장을 뒷받침하는가.

1번만 바꾸면 표현 연구, 3번을 바꾸면 학습법 연구다. 배포 분포를 정의하지 않은 채 4번만 보고하면 주장은 불완전하다. 이 네 줄 장부가 여기의 수식과 핵심 논문 노트를 잇는다.

### 고정 숫자

**D1.** bias 0, $\sigma=\mathrm{ReLU}$. [[02-foundations/lab-plants|0.6]]의 **P1**($2\to3\to1$ MSE)과 다른 장치다.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}$$

순전파: $W_1x=(1,2,1)$, $h=(1,2,1)$, $s=W_2h=(2,1)$. 사용처 [[03-deep-learning/foundations/index|1. Learning Systems]].

**D3.** 짝이 맞는 쌍은 정렬되어 있고 모든 벡터는 단위 길이다.

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix},\quad\tau=\tfrac12$$

내적 $v_1^\top t_j=(1,1/2,0)$이므로 이미지 1 logit은 $(2,1,0)$이다. 같은 행에서 $\tau=1/4$이면 $(4,2,0)$이다. 사용처 [[03-deep-learning/vlm/index|3. VLM]].

**D4.** 미터 단위 2차원 작업 평면과, chunk를 지연 결정으로 만드는 시계들. instruction은 "왼쪽으로 간 다음 아래로"이고 정책은 한 번에 한 축씩 계획한다.

$$o=(p_x,p_y,g_x,g_y),\quad p_0=(0,0),\quad g=(-0.04,-0.02),\quad a_{1:3}=\big\{(-0.02,0),\,(-0.02,0),\,(0,-0.02)\big\}$$

interface 한계는 제어 스텝당 $a_{\max}=0.02\,\mathrm{m}$, 축 전환 폭 $\delta=0.005\,\mathrm{m}$, 제어 주기 $\Delta t=0.05\,\mathrm{s}$, 추론 $t_{\mathrm{inf}}=0.10\,\mathrm{s}$, 축별 지각 흔들림 $\sigma=0.002\,\mathrm{m}$다. chunk의 경로 길이는 $0.06\,\mathrm{m}$, 알짜 변위는 $0.0447\,\mathrm{m}$다. 사용처 [[03-deep-learning/vla/index|4. VLA]]. [[02-foundations/lab-plants|0.6]]에서 가장 가까운 장치는 카트와 시계인 **P6**다. 둘 다 주기 둘과 지연을 갖지만, P6는 *측정* 하나를 파이프라인으로 늦추고 D4는 *결정의 버퍼*를 늦춘다. 그래서 D4의 묵은 정도는 전송만이 아니라 chunk 길이를 따라 자란다.

**D5.** 이산시간 스칼라 latent에, 페이지가 비교하는 학습 이득 둘과 planner가 뒤질 격자를 붙인 것.

$$z_{t+1}=\lambda z_t+\beta a_t,\quad \lambda=0.8,\ \beta=0.5,\ z_0=1,\quad r_t=-z_t^2-0.1a_t^2,\quad a_t\in\{-1,-\tfrac12,0,\tfrac12,1\}$$

시험 sequence $(a_0,a_1)=(-1,0)$: $z_1=0.3$, $r_0=-1.1$, $z_2=0.24$, $r_1=-0.09$, 2스텝 return $-1.19$. 학습 이득은 $\hat\lambda=0.9$(비관)와 $\hat\lambda'=0.7$(낙관)이고 둘 다 $\hat\beta=\beta$다. 사용처 [[03-deep-learning/world-models/index|5. World Models]]. 가장 가까운 장치는 새는 히터 **P4**다. P4는 모델이 정확하고 불확실성이 제어기가 배제하는 외란인 반면, D5는 *파라미터*가 틀렸고 사상이 반복되므로 오차가 자기 이득을 타고 누적된다.

**D6.** 자료 하나, noise 하나, 그리고 둘을 레벨로 바꾸는 schedule.

$$\sqrt{\bar\alpha_i}=1-0.8\,\frac{i}{T},\quad T=20,\qquad x_0=2,\ \epsilon=-1,\qquad \bar\alpha_5=0.64,\ \bar\alpha_{20}=0.04$$

카탈로그 레벨은 $i=5$이고 거기서 $x_5=0.8(2)+0.6(-1)=1$이다. 그 레벨의 $\alpha_5=\bar\alpha_5/\bar\alpha_4=(20/21)^2=0.907029$, $\beta_5=41/441=0.092971$이다. 고정된 신경망은 $\epsilon_\theta(x,i)=(x-\sqrt{\bar\alpha_i}x_0)/\sqrt{1-\bar\alpha_i}+b$, $b=0.2$이므로 카탈로그 레벨에서 $-0.8$을 내놓고, 신경망 1회 호출 비용은 $c=5\,\mathrm{ms}$로 가정한다. 사용처 [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]. 가장 가까운 장치는 1차원 거리 **P5**다. P5는 정적인 스칼라의 시끄러운 측정 하나를 알려진 분산으로 한 스텝에 융합하는 반면, D6는 알려진 스칼라를 noise 레벨의 *수열*을 따라 오염시키고 고른 스텝 수로 되돌린다. 그래서 오차는 이득 하나가 아니라 마지막 추정을 어느 레벨에서 했는지에 달린다.

