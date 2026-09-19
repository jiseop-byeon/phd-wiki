---
title: 6. Diffusion & Flow
tags: [deep-learning, diffusion, flow-matching, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Compute one forward noising and denoising target, distinguish score/noise/velocity parameterizations, and connect sampling steps to robot-policy latency."
mastery-when: "Raise when the generative objective, sampler, action distribution, or flow field is modified in the thesis."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/probability|3. Probability]], [[02-foundations/information-theory|5. Information Theory]], and [[03-deep-learning/foundations/index|1. Learning Systems]].

## English

> [!note] First pass
> Read D6, §§1–2, and questions 1–2. Return to §4 when a policy cuts denoising steps.

### Running object: D6

For **D6**, $x_0=2$, $\epsilon=-1$, and $\bar\alpha_t=0.64$. The standard closed-form forward sample is

$$x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon=0.8(2)+0.6(-1)=1.$$

Training can ask a network to recover the known noise $\epsilon=-1$ from $(x_t,t)$, optionally conditioned on context.

### 1. Training target and sampling process are different

The common noise-prediction loss is

$$L=\mathbb E_{x_0,\epsilon,t}\|\epsilon-\epsilon_\theta(x_t,t,c)\|^2.$$

During training, $x_t$ is produced directly from $x_0$ at a sampled time. During generation, there is no $x_0$: start from noise and integrate or step backward repeatedly. A paper's parameterization may predict noise, clean data, score, velocity, or a flow vector; translate it before comparing objectives.

### 2. One reconstruction calculation

If the model predicts $\hat\epsilon=-0.8$, estimate

$$\hat x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\hat\epsilon}{\sqrt{\bar\alpha_t}}=\frac{1-0.6(-0.8)}{0.8}=1.85.$$

The residual error comes from imperfect noise prediction. This equation is an estimator, not a claim that every sampler reconstructs $x_0$ in one step.

### 3. Diffusion and flow matching

Diffusion objectives learn quantities associated with a noisy probability path. Flow matching directly regresses the vector field of a chosen probability path. Diffusion paths can be represented within flow formulations; optimal-transport-inspired paths may be straighter, but “flow matching” does not universally mean straight or one-step generation.

### 4. Robot policy consequences

For images, extra sampling steps cost latency. For action policies they also determine control rate and how often observations can correct a plan. Report solver, step count, action horizon, receding execution, and wall-clock latency. Fewer numerical steps are useful only if closed-loop quality is maintained.

Read [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]], DDIM, score-SDE, flow-matching, and DiT notes before [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] and $\pi_0$.

### Problem set

1. **Draw.** Draw data $x_0$ to noisy $x_t$ for training and noise $x_T$ to sample for inference as two distinct paths.
2. **Derive.** For D6, compute $x_t$ when $\epsilon=+1$, then recover $x_0$ with a perfect predictor.
3. **Interpret.** A robot policy cuts denoising steps from 20 to 4 and reports the same offline action MSE. What deployment evidence is still required?

> [!tip]- Solutions
> 1. Training samples a time and corrupts known data; inference begins without clean data and solves backward/along a field.
> 2. $x_t=2.2$; $(2.2-0.6)/0.8=2$.
> 3. Wall-clock control rate and closed-loop success/recovery under the same observation and action protocol.

### Exit check

Given a generative paper, identify path, prediction target, conditioning, solver and steps, and which downstream metric—not sample aesthetics alone—supports the claim.

## 한국어

> [!note] 처음이라면
> D6, §1–2, 문제 1–2를 먼저 한다. 정책이 denoising step을 줄이면 §4로 돌아온다.

### 계속 쓰는 대상: D6

**D6**는 $x_0=2$, $\epsilon=-1$, $\bar\alpha_t=0.64$다. $x_t=0.8(2)+0.6(-1)=1$. 학습에서는 $(x_t,t)$에서 이미 알고 있는 noise $-1$을 복원하게 할 수 있다.

### 1. 학습 target과 sampling은 다르다

$L=\mathbb E\|\epsilon-\epsilon_\theta(x_t,t,c)\|^2$. 학습은 깨끗한 $x_0$에서 임의 시간의 $x_t$를 바로 만든다. 생성에는 $x_0$가 없으므로 noise에서 시작해 반복적으로 적분한다. noise·clean data·score·velocity·flow vector 중 무엇을 예측하는지 번역한 뒤 비교한다.

### 2. 한 번의 복원 계산

$\hat\epsilon=-0.8$이면 $\hat x_0=(1-0.6(-0.8))/0.8=1.85$다. 오차는 noise prediction이 완벽하지 않아서 생긴다. 이 식은 estimator이지 모든 sampler가 한 step에 복원한다는 뜻이 아니다.

### 3. Diffusion과 flow matching

diffusion은 noisy probability path와 관련된 양을 학습하고, flow matching은 선택한 path의 vector field를 회귀한다. diffusion path도 flow formulation에 들어갈 수 있다. OT 계열 경로가 더 곧을 수 있지만 모든 FM이 직선·one-step인 것은 아니다.

### 4. 로봇 정책에서의 결과

sampling step은 latency·control rate·재관측 주기를 바꾼다. solver·step 수·action horizon·receding execution·실제 시간을 보고해야 한다.

### 과제

1. 학습의 $x_0\to x_t$와 생성의 $x_T\to$ sample을 별개로 그린다.
2. $\epsilon=+1$일 때 D6의 $x_t$와 완벽 predictor의 복원을 구한다.
3. step 20→4, offline MSE 동일일 때 필요한 배포 증거를 말한다.

> [!tip]- 정답
> 1. 학습은 known data를 오염시키고, 추론은 clean data 없이 noise에서 시작한다.
> 2. $x_t=2.2$, 복원 $x_0=2$.
> 3. 같은 protocol의 wall-clock control rate와 폐루프 성공·회복.

### 통과 기준

path·prediction target·conditioning·solver/step과 sample 미관이 아닌 downstream metric을 식별할 수 있다.

