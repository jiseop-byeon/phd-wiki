---
title: "Score-Based Generative Modeling through SDEs"
authors: Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, Ben Poole
affiliation: Stanford University, Google Brain
venue: ICLR
year: 2021
arxiv: https://arxiv.org/abs/2011.13456
pdf: https://arxiv.org/pdf/2011.13456
code: https://github.com/yang-song/score_sde
tags: [paper, generative, diffusion]
status: to-read
---

**Song et al., ICLR 2021** — [arXiv](https://arxiv.org/abs/2011.13456) · [PDF](https://arxiv.org/pdf/2011.13456) · [Code](https://github.com/yang-song/score_sde)

> [!note] 수학 준비물 · SDE 한 입 크기
> 이 논문에 필요한 SDE 지식의 전부: $dx = f\,dt + g\,dW$는 이산화하면 $x_{t+\Delta} = x_t + f\Delta + g\sqrt{\Delta}\,\epsilon$ — 결정론적 흐름(drift) + 랜덤 워크 증분이다. $\sqrt{\Delta}$가 붙는 이유는 랜덤 워크의 분산이 시간에 비례하기 때문([[02-foundations/probability|확률 §5]]의 백색 잡음). 나머지는 전부 이 한 줄의 변주다.

## English

**One-line summary**: Noising is a continuous-time SDE, generation is the reverse SDE driven by the score $\nabla_x \log p_t(x)$ — one framework that unifies DDPM and score matching, and yields ODE sampling, exact likelihoods, and controllable generation.

### Context

By late 2020 two families produced near-identical results with different stories:
score matching with Langevin dynamics (Song & Ermon 2019) and [[ddpm|DDPM]]'s variational
chain. Were these the same thing? And could the discrete 1000-step chain be understood — and
improved — as a continuous process?

### Method

> [!tip] Key intuition
> Take the noising chain to its continuum limit: a stochastic differential equation
> $dx = f(x,t)dt + g(t)dw$. A classical result says this SDE has a *reverse-time* SDE that
> depends on only one unknown — the score $\nabla_x \log p_t(x)$. Learn the score with a
> network, and generation = numerically integrating the reverse SDE.

- **Forward SDE** generalizes both prior families: VE-SDE (variance exploding ← score
  matching) and VP-SDE (variance preserving ← DDPM).
- Train $s_\theta(x,t) \approx \nabla_x \log p_t(x)$ by denoising score matching across all $t$
  — equivalent to DDPM's noise prediction up to scaling.
- **Probability-flow ODE**: a deterministic ODE with the *same marginals* — enables exact
  log-likelihood computation and fast deterministic sampling (DDIM is its discretization).
- **Controllable generation**: add a classifier's gradient to the score at sampling time to
  steer generation (class-conditional, inpainting, colorization) — no retraining.
- Predictor-corrector samplers combine SDE integration with Langevin correction steps.

### Results

- CIFAR-10: FID **2.20** and the first likelihood-competitive score models — state of the art
  in both sample quality and density estimation among comparable models.
- First high-fidelity 1024×1024 score-based generation.
- Demonstrated inpainting/colorization as posterior sampling with an unconditional model.

### Limitations & critique

- Continuous-time machinery raises the mathematical entry cost; solver choices introduce
  their own hyperparameters.
- Sampling still needs many network evaluations (the ODE view later enabled fast solvers —
  DPM-Solver — and consistency/distillation methods).
- Guidance via classifiers was soon simplified by classifier-free guidance.

### Impact & follow-ups

The theoretical backbone of modern diffusion: the score/ODE view underlies DDIM, DPM-Solver,
classifier(-free) guidance, and **flow matching** — which learns the probability-flow field
directly and is exactly the action-generation mechanism of π0. When robotics papers write
"denoise a trajectory," this paper supplies the mathematics being invoked.

### Connections

- Previous: [[ddpm|DDPM]] (the discrete special case it unifies)
- Next: DDIM, Flow Matching → π0 · Foundations: [[02-foundations/probability|probability]] (SDE ← random processes)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 노이즈 주입은 연속 시간 SDE이고, 생성은 score $\nabla_x \log p_t(x)$가 이끄는 역방향 SDE다 — DDPM과 score matching을 하나로 통합하고, ODE 샘플링·정확한 우도·제어 가능한 생성을 덤으로 주는 프레임워크.

### 배경

2020년 말, 서로 다른 이야기로 거의 같은 결과를 내는 두 계열이 있었다: Langevin 동역학을
쓰는 score matching(Song & Ermon 2019)과 [[ddpm|DDPM]]의 변분 체인. 이 둘은 같은 것인가?
그리고 이산적인 1000 스텝 체인을 연속 과정으로 이해하고 — 개선할 수 있는가?

### 방법

> [!tip] 핵심 직관
> 노이즈 체인을 연속 극한으로 보내면 확률미분방정식 $dx = f(x,t)dt + g(t)dw$가 된다.
> 고전적 결과에 따르면 이 SDE에는 *역시간* SDE가 존재하고, 거기서 미지수는 단 하나 —
> score $\nabla_x \log p_t(x)$다. score를 네트워크로 배우면, 생성 = 역방향 SDE의 수치 적분이다.

- **순방향 SDE**가 두 기존 계열을 일반화: VE-SDE(분산 폭발 ← score matching)와
  VP-SDE(분산 보존 ← DDPM).
- 모든 $t$에 대한 denoising score matching으로 $s_\theta(x,t) \approx \nabla_x \log p_t(x)$ 학습
  — 스케일 차이를 빼면 DDPM의 노이즈 예측과 동치.
- **확률 흐름 ODE**: *같은 주변 분포*를 갖는 결정론적 ODE — 정확한 로그 우도 계산과 빠른
  결정론적 샘플링을 가능하게 한다 (DDIM이 그 이산화다).
- **제어 가능한 생성**: 샘플링 시 분류기의 그래디언트를 score에 더해 생성을 조향
  (클래스 조건부, 인페인팅, 채색) — 재학습 없이.
- Predictor-corrector 샘플러: SDE 적분 + Langevin 보정 스텝의 결합.

### 결과

- CIFAR-10: FID **2.20**, 그리고 우도에서도 경쟁력 있는 최초의 score 모델 — 샘플 품질과
  밀도 추정 양쪽에서 동급 최고.
- 최초의 고품질 1024×1024 score 기반 생성.
- 무조건부 모델 하나로 인페인팅/채색을 사후 샘플링으로 시연.

### 한계와 비판

- 연속 시간 기계장치는 수학적 진입 비용을 높인다; 솔버 선택이 자체 하이퍼파라미터를 만든다.
- 샘플링은 여전히 많은 네트워크 평가가 필요 (ODE 관점이 이후 빠른 솔버 DPM-Solver와
  증류·일관성 기법을 가능하게 했다).
- 분류기 기반 조향은 곧 classifier-free guidance로 단순화됐다.

### 영향과 후속 연구

현대 디퓨전의 이론적 등뼈: score/ODE 관점이 DDIM, DPM-Solver, classifier(-free) guidance,
그리고 **flow matching** — 확률 흐름장을 직접 배우는 기법이자 π0의 행동 생성 메커니즘 —
의 밑바탕이다. 로보틱스 논문이 "궤적의 노이즈를 제거한다"고 쓸 때, 인용되고 있는 수학이
바로 이 논문이다.

### 연결

- 이전: [[ddpm|DDPM]] (이 프레임워크가 통합하는 이산 특수 사례)
- 다음: DDIM, Flow Matching → π0 · 기초: [[02-foundations/probability|확률]] (SDE ← 랜덤 프로세스)
- 계보: [[03-deep-learning/lineage|논문 계보도]]
