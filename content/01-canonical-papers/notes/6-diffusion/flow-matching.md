---
title: "Flow Matching for Generative Modeling"
authors: Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, Matt Le
affiliation: Meta AI (FAIR), Weizmann Institute
venue: ICLR
year: 2023
arxiv: https://arxiv.org/abs/2210.02747
pdf: https://arxiv.org/pdf/2210.02747
tags: [paper, generative, diffusion]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Lipman et al., ICLR 2023** — [arXiv](https://arxiv.org/abs/2210.02747) · [PDF](https://arxiv.org/pdf/2210.02747)

> [!note] 수학 준비물 · ODE 적분 한 입 크기
> Sampling is Euler integration: repeat $x \leftarrow x + v_\theta(x,t)\,\Delta t$ from noise ($t{=}0$) to data ($t{=}1$) — that is all of it ([[02-foundations/engineering-math|0.5 §8]]'s differential-equation sense). The straighter the path, the larger a $\Delta t$ you *may* get away with — a geometric condition that makes few steps possible, not an automatic guarantee.
> 샘플링 = 오일러 적분: $x \leftarrow x + v_\theta(x, t)\,\Delta t$를 노이즈($t{=}0$)에서 데이터($t{=}1$)까지 반복하는 것이 전부다([[02-foundations/engineering-math|0.5 §8]]의 미분방정식 감각). 경로가 직선에 가까울수록 큰 $\Delta t$로 건너뛰어도 안전*할 수 있다* — "스텝 수가 적다"를 *가능하게 하는* 기하학적 조건이지 자동 보장은 아니다.

## English

**One-line summary**: Skip the SDE — directly regress the velocity field of a probability path from noise to data (per-sample conditional targets make it trivial), yielding (with OT-style path choices) straighter paths, simpler training, and the action-generation engine of π0.

### Context

[[score-sde|The ODE view]] showed generation is transporting noise to data along a flow —
but diffusion still *trains* through the noising-chain formalism, and its curved paths need
many integration steps. Continuous normalizing flows trained the transport directly but
required simulating the ODE during training (intractable). Wanted: simulation-free training
of the flow itself.

### Method

> [!tip] Key intuition
> You can't regress the marginal velocity field (unknown), but *conditioned on one data
> point* the path and its velocity are trivial — e.g., the straight line from noise to that
> sample. Training on conditional targets provably gives gradients of the marginal
> objective: learn u_t by averaging over easy per-sample problems.

- **Flow Matching**: learn $v_\theta(x, t)$ with
  $E_{t, x_1, x_t}\|v_\theta(x_t, t) - u_t(x_t|x_1)\|^2$ over designed conditional
  probability paths — no ODE simulation, no ELBO.
- **Optimal-transport (straight-line) paths**: $x_t = (1-t)x_0 + t x_1$ with constant

<svg viewBox="0 0 620 218" style="max-width:100%;height:auto" role="img" aria-label="a curved probability path needs many integration steps; a straight one needs few">
  <defs><marker id="fmA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor"><circle cx="60" cy="120" r="5"/><circle cx="290" cy="62" r="5"/><circle cx="330" cy="120" r="5"/><circle cx="560" cy="62" r="5"/></g>
  <path d="M60,120 C110,152 150,42 200,56 C230,64 260,60 288,62" fill="none" stroke="currentColor" stroke-width="1.8" opacity="0.75"/>
  <g fill="currentColor" opacity="0.9">
    <circle cx="88" cy="136" r="2.6"/><circle cx="118" cy="122" r="2.6"/><circle cx="146" cy="78" r="2.6"/><circle cx="176" cy="57" r="2.6"/><circle cx="206" cy="57" r="2.6"/><circle cx="236" cy="61" r="2.6"/><circle cx="264" cy="61" r="2.6"/>
  </g>
  <line x1="330" y1="120" x2="556" y2="64" stroke="currentColor" stroke-width="1.8" opacity="0.75" marker-end="url(#fmA)"/>
  <g fill="currentColor" opacity="0.9"><circle cx="405" cy="101" r="2.6"/><circle cx="481" cy="82" r="2.6"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="30" y="140">noise</text><text x="272" y="48">data</text>
    <text x="300" y="140">noise</text><text x="542" y="48">data</text>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="175" y="26">a curved path</text><text x="445" y="26">a straight (OT-style) path</text>
    <text x="175" y="172">many small Euler steps to stay on it</text><text x="445" y="172">a few large steps suffice</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="198" opacity="0.9">Sampling is Euler integration either way. The number of steps is not a property of the model but of the path's</text>
    <text x="30" y="212" opacity="0.9">curvature &#8212; which is why choosing a straighter path is a design decision that pays at runtime.</text>
  </g>
</svg>


  velocity $x_1 - x_0$ — straighter than diffusion's curved paths, which *permits* far fewer inference
  steps; diffusion paths are recovered as a special case.
- Sampling: integrate the learned ODE from noise to data.

### Results

- Better ImageNet likelihood/FID than score-based baselines with faster, more stable
  training; sample quality holds with few integration steps thanks to path straightness.

### Limitations & critique

- Deterministic-transport view drops some of diffusion's stochastic flexibility;
  path/coupling design (e.g., minibatch OT) becomes the new hyperparameter surface.
- Shares few-step precision limits with all ODE samplers before distillation.

### Impact & follow-ups

Now a *dominant training objective* among frontier generators (Stable Diffusion 3, Flux,
video models) — and for robotics: [[pi0|π0]]'s action expert and [[gr00t-n1|GR00T]]'s
System 1 generate 50–120 Hz action chunks with exactly this recipe, because few-step
straight-path inference is what real-time control demands. The MIT tutorial in the local
reference folder (Holderrieth & Erives) teaches this paper's framework.

### Connections

- Previous: [[ddpm|DDPM]], [[score-sde|Score SDE]], [[ddim|DDIM]] (the ODE lineage)
- Next: [[pi0|π0]], [[gr00t-n1|GR00T N1]] action heads, SD3/Flux
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: SDE를 건너뛰고 노이즈→데이터 확률 경로의 속도장을 직접 회귀 — 샘플별 조건부 타깃 덕분에 학습이 자명해지고, 더 곧은 경로·더 단순한 학습을 얻는다; π0의 행동 생성 엔진이 바로 이것이다.

### 배경

[[score-sde|ODE 관점]]은 생성이 흐름을 따라 노이즈를 데이터로 수송하는 일임을 보였다 —
하지만 디퓨전은 여전히 노이즈 체인 형식론을 *거쳐* 학습하고, 그 굽은 경로는 많은 적분
스텝을 요구한다. 연속 정규화 흐름(CNF)은 수송을 직접 학습했지만 학습 중 ODE 시뮬레이션이
필요했다(비현실적). 원하는 것: 흐름 자체의 시뮬레이션 없는 학습.

### 방법

> [!tip] 핵심 직관
> 주변 속도장은 회귀할 수 없다(모른다). 하지만 *데이터 포인트 하나를 조건으로 하면* 경로와
> 속도는 자명하다 — 예컨대 노이즈에서 그 샘플로 가는 직선. 조건부 타깃으로 학습해도 주변
> 목적함수의 그래디언트와 같음이 증명된다: 쉬운 샘플별 문제들의 평균으로 $u_t$를 배워라.

- **Flow Matching**: 설계된 조건부 확률 경로 위에서
  $E_{t, x_1, x_t}\|v_\theta(x_t, t) - u_t(x_t|x_1)\|^2$로 $v_\theta$ 학습 —
  ODE 시뮬레이션도 ELBO도 없다.
- **최적 수송(직선) 경로**: $x_t = (1-t)x_0 + t x_1$, 속도는 상수 $x_1 - x_0$ —

<svg viewBox="0 0 620 218" style="max-width:100%;height:auto" role="img" aria-label="휘어진 확률 경로는 적분 스텝이 많이 필요하고, 곧은 경로는 적게 필요하다">
  <defs><marker id="fmA" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g fill="currentColor"><circle cx="60" cy="120" r="5"/><circle cx="290" cy="62" r="5"/><circle cx="330" cy="120" r="5"/><circle cx="560" cy="62" r="5"/></g>
  <path d="M60,120 C110,152 150,42 200,56 C230,64 260,60 288,62" fill="none" stroke="currentColor" stroke-width="1.8" opacity="0.75"/>
  <g fill="currentColor" opacity="0.9">
    <circle cx="88" cy="136" r="2.6"/><circle cx="118" cy="122" r="2.6"/><circle cx="146" cy="78" r="2.6"/><circle cx="176" cy="57" r="2.6"/><circle cx="206" cy="57" r="2.6"/><circle cx="236" cy="61" r="2.6"/><circle cx="264" cy="61" r="2.6"/>
  </g>
  <line x1="330" y1="120" x2="556" y2="64" stroke="currentColor" stroke-width="1.8" opacity="0.75" marker-end="url(#fmA)"/>
  <g fill="currentColor" opacity="0.9"><circle cx="405" cy="101" r="2.6"/><circle cx="481" cy="82" r="2.6"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="30" y="140">노이즈</text><text x="272" y="48">데이터</text>
    <text x="300" y="140">노이즈</text><text x="542" y="48">데이터</text>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="175" y="26">휘어진 경로</text><text x="445" y="26">곧은 (OT식) 경로</text>
    <text x="175" y="172">경로를 벗어나지 않으려면 작은 스텝이 많이 필요</text><text x="445" y="172">큰 스텝 몇 번이면 충분</text>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="30" y="198" opacity="0.9">어느 쪽이든 샘플링은 오일러 적분이다. 스텝 수는 모델의 성질이 아니라 경로의 곡률이 정한다 &#8212;</text>
    <text x="30" y="212" opacity="0.9">더 곧은 경로를 고르는 것이 실행 시간의 이득으로 돌아오는 설계 결정인 이유다.</text>
  </g>
</svg>


  디퓨전의 굽은 경로보다 곧다 ⇒ 추론 스텝이 훨씬 적어도 된다; 디퓨전 경로는 특수 사례로
  복원된다.
- 샘플링: 학습된 ODE를 노이즈에서 데이터로 적분.

### 결과

- score 기반 베이스라인보다 나은 ImageNet 우도/FID를 더 빠르고 안정적인 학습으로;
  경로의 직선성 덕에 적분 스텝이 적어도 샘플 품질이 유지된다.

### 한계와 비판

- 결정론적 수송 관점은 디퓨전의 확률적 유연성 일부를 버린다; 경로/커플링 설계(예:
  미니배치 OT)가 새로운 하이퍼파라미터 표면이 된다.
- 증류 전에는 극소 스텝 정밀도 한계를 모든 ODE 샘플러와 공유한다.

### 영향과 후속 연구

이제 프런티어 생성기(Stable Diffusion 3, Flux, 비디오 모델) 사이의 *지배적 학습 목적함수 중 하나*다 —
그리고 로보틱스에서: [[pi0|π0]]의 행동 전문가와 [[gr00t-n1|GR00T]]의 System 1이 정확히 이
레시피로 50~120 Hz 행동 청크를 생성한다. 실시간 제어가 요구하는 것이 바로 소수 스텝의
직선 경로 추론이기 때문이다. 로컬 reference 폴더의 MIT 튜토리얼(Holderrieth & Erives)이
이 논문의 프레임워크를 가르친다.

### 연결

- 이전: [[ddpm|DDPM]], [[score-sde|Score SDE]], [[ddim|DDIM]] (ODE 계보)
- 다음: [[pi0|π0]], [[gr00t-n1|GR00T N1]] 행동 헤드, SD3/Flux
- 계보: [[03-deep-learning/lineage|논문 계보도]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> Read two claims separately: (1) the theoretical one — it is a general framework containing diffusion paths as a special case (proved); (2) the empirical one — straight OT paths work better in practice (benchmark-dependent). The first does not automatically guarantee the second, and the real reason for adoption is that the second happened to fit robot real-time control.
>
> 두 주장을 분리해서 읽어라: ① 이론적 주장 — 디퓨전 경로를 특수 사례로 포함하는 일반 프레임이다(증명됨), ② 경험적 주장 — OT 직선 경로가 실용적으로 낫다(벤치마크 의존). ①이 ②를 자동으로 보장하지 않는다 — 채택의 실제 이유는 ②가 로봇 실시간 제어와 맞아떨어졌기 때문이다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Say what the velocity field $v_\theta(x,t)$ does and why sampling is ODE integration · 속도장 $v_\theta(x, t)$가 무엇을 하는 함수이고, 샘플링이 왜 ODE 적분인지 말할 수 있다
- [ ] Explain conceptually why training on the conditional target (constant velocity along a per-sample straight path) is still correct · 조건부 타깃(샘플별 직선 경로의 상수 속도)으로 학습해도 옳은 이유를 개념 수준에서 설명할 수 있다
- [ ] Say why straighter paths mean fewer inference steps · 경로가 곧을수록 추론 스텝이 줄어드는 이유를 말할 수 있다
- [ ] Connect why π0 adopted this for action generation (few steps → real-time control) · π0가 행동 생성에 이 방식을 채택한 이유(소수 스텝 → 실시간 제어)를 연결할 수 있다
