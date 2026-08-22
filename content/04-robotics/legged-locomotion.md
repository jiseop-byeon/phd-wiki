---
title: 18. Legged Locomotion
tags: [robotics, locomotion, unstructured]
study-depth: Working
wiki-support: Working
depth-goal: "Explain privileged teacher-student distillation, say what each landmark locomotion result actually claimed, and read a locomotion paper without inheriting its reputation."
mastery-when: "Raise to Mastery only if locomotion becomes the platform your contribution runs on — the research program keeps it supporting."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to read the canon accurately and to use these platforms, not to
> advance them.
> **Working** — 정본을 정확히 읽고 이 플랫폼들을 쓸 만큼. 그것을 진전시키기 위해서가 아니라.

> [!note] Before you start · 시작 전 점검
> You need RL and policy gradients ([[02-foundations/rl-basics|7. RL Basics §4]]), the manipulator equation and why actuator models matter ([[02-foundations/manipulator-kinematics-dynamics|10. §2, §7]]), and DAgger ([[01-canonical-papers/notes/4-vla/dagger|DAgger]]) — because distillation here is DAgger with a simulator as the expert.
> RL과 정책 경사([[02-foundations/rl-basics|7. RL 기초 §4]]), 매니퓰레이터 방정식과 액추에이터 모델이 중요한 이유([[02-foundations/manipulator-kinematics-dynamics|10. §2, §7]]), 그리고 DAgger([[01-canonical-papers/notes/4-vla/dagger|DAgger]])가 필요하다 — 여기서의 증류가 시뮬레이터를 전문가로 삼은 DAgger이기 때문이다.

## English

### 1. Why this page exists

This literature is **systematically over-cited beyond its actual claims**. The famous results
are famous for approximately the right reasons and are then quoted for something adjacent
that they did not show. That makes it a good page for practising the reading discipline the
rest of this wiki asks for, and it makes the corrections below the most useful content here.

It also matters directly: legged platforms are what most of
[[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] runs on, and
the field's single highest-leverage training idea was invented here.

### 2. The idea worth taking away: privileged teacher-student distillation

If you learn one thing from this page, learn this. It has no analogue in classical robotics,
and it — not any particular reward design — is what made rough-terrain locomotion work.

<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="a teacher trained on privileged simulator state is distilled into a student that sees only proprioceptive history">
  <g fill="currentColor">
    <rect x="24" y="52" width="150" height="76" rx="4" fill-opacity="0.14"/>
    <rect x="330" y="52" width="150" height="76" rx="4" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="52" width="150" height="76" rx="4"/><rect x="330" y="52" width="150" height="76" rx="4"/>
  </g>
  <g stroke="currentColor" stroke-width="3.4" fill="none" opacity="0.85" marker-end="url(#arL)">
    <line x1="180" y1="82" x2="324" y2="82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" marker-end="url(#arL)" stroke-dasharray="5 3">
    <path d="M 405 134 L 405 156 L 99 156 L 99 134"/>
  </g>
  <defs><marker id="arL" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="99" y="72">teacher</text>
    <text x="99" y="90" font-size="9.5" opacity="0.85">trained by RL, in simulation</text>
    <text x="99" y="106" font-size="9.5" opacity="0.85">sees privileged state</text>
    <text x="405" y="72">student</text>
    <text x="405" y="90" font-size="9.5" opacity="0.85">supervised by the teacher</text>
    <text x="405" y="106" font-size="9.5" opacity="0.85">sees proprioceptive history</text>
    <text x="252" y="76" font-size="10" opacity="0.85">distil</text>
    <text x="252" y="172" font-size="9.5" opacity="0.8">the student rolls out; the teacher labels the states it actually visited</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.9">
    <text x="24" y="196">privileged, and unavailable on the robot: terrain profile under each foot, contact states and forces,</text>
    <text x="24" y="210">friction coefficients, applied disturbances</text>
    <text x="24" y="232" font-size="11">The student never learns to see. It learns to INFER those quantities from how the body just moved.</text>
  </g>
</svg>

The teacher is trained by RL with access to **ground-truth simulator state** — the terrain
profile, contact states and forces, friction coefficients, applied disturbance forces. None
of that exists on the real robot. The teacher is then **distilled by supervised learning**
into a student that sees only a short history of proprioception, with DAgger-style data
collection: the student rolls out, the teacher labels the states the student actually
visited.

The student does not learn to perceive. It learns to **infer the privileged quantities from
how the body has just been moving** — which is why a blind robot can adapt to mud it cannot
see, after it has stepped in it.

**RMA** is the same family arrived at independently, with a sharper deployment story:
compress a 17-dimensional privileged environment vector into an **8-dimensional latent**,
estimate that latent from 0.5 s of proprioceptive history by supervised regression trained
purely in simulation, and run it **asynchronously — base policy at 100 Hz, adaptation module
at 10 Hz — on a cheap robot's onboard CPU.**

The pattern has since generalised well past locomotion: multi-expert distillation into a
generalist, model-based experts relabelling passive data, and — in a different guise — the
teacher-student structure inside sim-to-real recipes generally
([[05-construction-robotics/sim-to-real|Sim-to-Real §2]]).

### 3. The canon, and what each result actually claimed

| Work | What it is famous for | What it actually claimed |
|---|---|---|
| **Hwangbo et al. 2019** | "RL locomotion" | the **actuator net** — a hybrid simulator. Demonstrated skills are flat-ground command following and **fall recovery**. Rough terrain is not the claim |
| **Lee et al. 2020** | rough-terrain locomotion | **blind** robustness via privileged distillation; mud, snow, rubble, vegetation, running water. Speed gains modest and terrain-specific |
| **Rudin et al. 2021** | "walk in minutes" | **wall-clock training time on one GPU** — not sample efficiency. Matters as infrastructure |
| **Miki et al. 2022** | "beat a human hiker" | perceptive locomotion with a **learned gate** on how much to trust the height map |
| **ANYmal parkour 2024** | parkour | **hierarchical** skills plus a high-level policy aware of each skill's capability envelope |

Three of those deserve expanding, because the gap between reputation and claim is where the
reading practice lives.

**Hwangbo 2019's contribution is a simulator, not a gait.** They keep analytical rigid-body
physics and replace the part nobody models well — the series-elastic actuator and its control
software — with a small network regressing joint torque from a history of position errors
and velocities, trained on **under four minutes of robot data**. The payoff is roughly
1000× real-time simulation on one workstation. The durable idea is "learn the component you
cannot model, keep the physics you can" — and it is the ancestor of every sim-to-real
actuator-modelling result since.

**Rudin 2021 is infrastructure, and should be framed that way.** Thousands of robots in
parallel on a single workstation GPU, PPO retuned for that regime, and a game-inspired
terrain curriculum that promotes and demotes robots by difficulty. The released
`legged_gym` / `rsl_rl` code is what made the 2022–2026 explosion economically possible in
ordinary labs. Its scientific claim is narrow; its causal influence is enormous. Keeping
those two things separate is exactly the kind of correction this wiki exists to make.

**Miki 2022's mechanism is the interesting part, not the hike.** An attention-based recurrent
**belief-state** encoder fuses proprioception with an exteroceptive height map and learns an
**adaptive gating factor** for how much of the map to trust — so when the map lies (snow,
tall grass, water, reflective surfaces) the controller degrades gracefully back to
proprioceptive locomotion, with no hand-designed rule for when to stop believing it.

> [!warning] Three over-citations to avoid
> - **The Alps hike is one instrumented route against a guidebook time**, not a benchmarked
>   comparison against human hikers. 2.2 km, 120 m of gain, 78 minutes against a 76-minute
>   guidebook estimate.
> - **"Walk in minutes" is wall-clock on one GPU.** It consumes vastly *more* simulated
>   experience than prior work, and it is not real-robot learning time.
> - **The humanoid rough-terrain paper is a preprint.** Radosavovic et al.'s peer-reviewed
>   *Science Robotics* humanoid result is **blind flat-to-mildly-uneven outdoor walking**; the
>   challenging-terrain follow-up with the Berkeley trails and San Francisco hills is an
>   arXiv preprint that is frequently cited as though it were published.

### 4. The parkour contrast, and why it is instructive

Two papers months apart, opposite architectures, opposite hardware, and both called parkour.

| | **ANYmal parkour** (Science Robotics 2024) | **Extreme Parkour** (ICRA 2024) |
|---|---|---|
| Architecture | hierarchical: separate RL skills + a skill-selecting navigation policy | one monolithic network, depth to action |
| Perception | explicit obstacle reconstruction from occluded, noisy depth | a single front-facing depth camera, end to end |
| Hardware | ANYmal, ~50 kg research quadruped | low-cost robot, imprecise actuators |
| Notable mechanism | the high-level policy knows each skill's **capability envelope** | a learned inner yaw reward lets the policy **aim itself**, no separate planner |

Neither has been shown to generalise beyond hand-built or hand-selected obstacle courses.
The pair is worth reading together because it shows the field genuinely undecided between
composition and monolith at the same moment — and because **ANYmal parkour is where
locomotion crosses into navigation**: a high-level policy reasoning about which skill a
piece of terrain affords is skill-affordance-aware planning, and that is the actual interface
between this page and [[04-robotics/semantic-language-navigation|19]].

### 5. Where it went, 2025–2026

The centre of gravity moved from "can it walk on X" to **generalist and cross-embodiment
policies**, plus terrain-representation learning.

- **Attention-based map encoding** (Science Robotics, 2025) trains a terrain-map encoder
  conditioned on proprioception **end to end inside the RL controller**, learning to attend
  to steppable regions for future footholds — and demonstrates it on **both a 12-DoF ANYmal-D
  and a 23-DoF humanoid**, which is the notable part.
- **Parkour in the wild** (IJRR, 2026) distils terrain-specific experts into one generalist
  depth-input policy by DAgger, then RL fine-tunes on expanded terrain including real-world
  3D scans — collapsing ANYmal parkour's skill hierarchy into a single extensible policy.
- **High-speed control on discrete terrain** (Science Robotics, 2025) is a **planner-plus-learner
  hybrid**: sampling-based foothold optimisation with heuristic and neural filtering, plus an
  RL tracker. Stepping stones at 4 m/s, a 1.3 m gap jump. Worth citing as evidence the
  pendulum is swinging partly back toward hybrids for precision terrain.
- **LocoFormer** (CoRL 2025, Best Paper finalist) is the nearest thing to a locomotion
  foundation model: one policy for unseen legged *and wheeled* robots without precise
  kinematics, trained over procedurally generated morphologies, whose actual novelty is a
  context window extended to **span episode boundaries** — producing emergent cross-episode
  adaptation, so the policy learns from falls in earlier episodes.

There is no consensus locomotion foundation model, and no 2026 result of Miki-2022 or
Rudin-2021 stature. Saying so is more useful than naming a preprint.

### 6. The tooling, because it dates the papers

- **Isaac Gym Preview is formally deprecated** — NVIDIA's own page calls it legacy software
  that is no longer supported, and the `IsaacGymEnvs` / `OmniIsaacGymEnvs` repositories were
  archived read-only in April 2026. A 2026 paper saying "we use Isaac Gym" is on a dead
  preview release.
- **Isaac Lab** is the successor; as of August 2026 the stable line is 2.3.x with 3.0 in beta.
- **MuJoCo Playground / MJX** is the credible vendor-neutral alternative and the reason MJX
  became an academic default.
- **Newton** — co-developed by Disney Research, Google DeepMind and NVIDIA, contributed to the
  Linux Foundation in September 2025 — is becoming the shared physics layer under both,
  integrating MuJoCo Warp as a backend. The Isaac/MuJoCo split is converging at the solver
  layer.

See [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]]
for the full picture and the licensing traps.

### After reading

- [ ] Draw the teacher-student diagram and name what is privileged.
- [ ] State what Hwangbo 2019 actually demonstrated.
- [ ] Explain why "walk in minutes" is not a sample-efficiency claim.
- [ ] Describe Miki's gating mechanism and what it is protecting against.
- [ ] Give the two parkour architectures and say what neither has shown.

### Self-check

1. Why can a blind robot adapt to mud it cannot see?
2. A 2026 paper reports locomotion results trained in Isaac Gym. What do you note?
3. Someone cites Miki 2022 as evidence that robots now outperform human hikers. Correct them.
4. What does LocoFormer's extended context window actually buy?
5. Your project needs a legged platform to carry a manipulator over rough ground. Which
   result on this page is the closest precedent, and what does it not give you?

> [!tip]- Answers
> 1. Because the student was distilled from a teacher that *could* see the friction coefficient and terrain profile, and it learned to infer those quantities from a short history of proprioception — how the body actually moved over the last fraction of a second. It cannot anticipate the mud, but once a foot is in it the recent motion history is informative about what changed, and the policy was trained on exactly that inference. Blindness is why it must make contact first; distillation is why contact is enough.
> 2. That Isaac Gym Preview is deprecated — NVIDIA's own page calls it legacy and unsupported, and the associated env repositories were archived read-only in April 2026. It does not invalidate the result, but it dates the work and makes reproduction harder, and a current project should be on Isaac Lab or MuJoCo MJX instead.
> 3. The comparison was **one instrumented alpine route** — 2.2 km, 120 m of elevation gain — completed in 78 minutes against a **76-minute guidebook estimate** for that route. That is a single route against a published time, not a benchmark against human hikers, and the robot was slightly slower overall. The result is genuinely impressive; the claim it supports is narrower than the one usually attributed to it.
> 4. Adaptation *across* episodes rather than within one. With a context window spanning episode boundaries, the policy can condition on what happened in earlier attempts — including falls — so it improves within a deployment without any weight update. That is a different mechanism from RMA-style latent estimation, which adapts within an episode from proprioceptive history and resets when the episode does.
> 5. **ANYmal parkour**, because it is the only one whose high-level policy reasons about what a piece of terrain affords, which is what a mobile manipulator needs to reach a workspace. What it does not give you is the manipulator: it is a navigation-among-obstacles result on a curated course, with no arm, no payload, and no account of how carrying one changes the dynamics. The error-budget consequences of adding an arm are in [[04-robotics/navigation-mobile-manipulation|16. §4]].

### Sources

- J. Hwangbo, J. Lee, A. Dosovitskiy, et al., "Learning agile and dynamic motor skills for legged robots," *Science Robotics*, vol. 4, no. 26, eaau5872, 2019 ([arXiv:1901.08652](https://arxiv.org/abs/1901.08652)).
- J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, M. Hutter, "Learning Quadrupedal Locomotion over Challenging Terrain," *Science Robotics*, vol. 5, no. 47, eabc5986, 2020 ([arXiv:2010.11251](https://arxiv.org/abs/2010.11251)) — privileged teacher-student.
- N. Rudin, D. Hoeller, P. Reist, M. Hutter, "Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning," CoRL 2021 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — `legged_gym` / `rsl_rl`.
- A. Kumar, Z. Fu, D. Pathak, J. Malik, "RMA: Rapid Motor Adaptation for Legged Robots," RSS 2021, DOI 10.15607/RSS.2021.XVII.011 ([arXiv:2107.04034](https://arxiv.org/abs/2107.04034)).
- T. Miki, J. Lee, J. Hwangbo, et al., "Learning robust perceptive locomotion for quadrupedal robots in the wild," *Science Robotics*, vol. 7, no. 62, eabk2822, 2022 ([arXiv:2201.08117](https://arxiv.org/abs/2201.08117)).
- D. Hoeller, N. Rudin, D. Sako, M. Hutter, "ANYmal parkour: Learning agile navigation for quadrupedal robots," *Science Robotics*, vol. 9, no. 88, eadi7566, 2024 ([arXiv:2306.14874](https://arxiv.org/abs/2306.14874)).
- X. Cheng, K. Shi, A. Agarwal, D. Pathak, "Extreme Parkour with Legged Robots," ICRA 2024, pp. 11443–11450 ([arXiv:2309.14341](https://arxiv.org/abs/2309.14341)); Z. Zhuang et al., "Robot Parkour Learning," CoRL 2023 oral ([arXiv:2309.05665](https://arxiv.org/abs/2309.05665)).
- I. Radosavovic, T. Xiao, B. Zhang, et al., "Real-world humanoid locomotion with reinforcement learning," *Science Robotics*, vol. 9, no. 89, eadi9579, 2024 ([arXiv:2303.03381](https://arxiv.org/abs/2303.03381)). The challenging-terrain follow-up, [arXiv:2410.03654](https://arxiv.org/abs/2410.03654), is **a preprint**.
- 2025–26: He, Zhang, Jenelten, et al., "Attention-based map encoding for learning generalized legged locomotion," *Science Robotics*, vol. 10, no. 105, eadv3604, 2025 ([arXiv:2506.09588](https://arxiv.org/abs/2506.09588)); Rudin, He, Aurand, Hutter, "Parkour in the wild," *IJRR*, 2026, DOI 10.1177/02783649261455067 ([arXiv:2505.11164](https://arxiv.org/abs/2505.11164)); Kim, Oh, Park, et al., "High-speed control and navigation for quadrupedal robots on complex and discrete terrain," *Science Robotics*, vol. 10, no. 102, eads6192, 2025 ([arXiv:2506.02835](https://arxiv.org/abs/2506.02835)); Liu, Pathak, Agarwal, "LocoFormer," CoRL 2025 ([arXiv:2509.23745](https://arxiv.org/abs/2509.23745)).

**Within this wiki**

- **Paper notes** — [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] · [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al. 2022]] · [[01-canonical-papers/notes/9-navigation/rma|RMA]] · [[01-canonical-papers/notes/9-navigation/anymal-parkour|ANYmal Parkour]]
- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — where these robots are sent
- [[04-robotics/convex-mpc-legged|Convex MPC for legged robots]] — the model-based side of the same problem
- [[05-construction-robotics/sim-to-real|Sim-to-Real for Field Robots]] — teacher-student as one strategy among several
- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — the tooling status in §6

## 한국어

### 1. 이 페이지가 존재하는 이유

이 문헌은 **실제 주장 너머로 체계적으로 과잉 인용된다.** 유명한 결과들이 대체로 옳은 이유로
유명해진 뒤, 그것이 보이지 않은 인접한 무언가에 대해 인용된다. 그래서 이 위키의 나머지가 요구하는
독해 규율을 연습하기 좋은 페이지이고, 아래의 교정들이 여기서 가장 쓸모 있는 내용이다.

직접적으로도 중요하다: [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]]의
대부분이 레그드 플랫폼 위에서 돌아가고, 이 분야의 가장 파급력 큰 학습 아이디어가 여기서 나왔다.

### 2. 가져갈 발상: privileged teacher-student 증류

이 페이지에서 하나만 배운다면 이것이다. 고전 로보틱스에 대응물이 없고, 거친 지형 로코모션을
동작하게 만든 것이 어떤 보상 설계가 아니라 이것이다.

<svg viewBox="0 0 560 244" style="max-width:100%;height:auto" role="img" aria-label="시뮬레이터의 특권적 상태로 학습한 교사가 고유수용감각 이력만 보는 학생으로 증류된다">
  <g fill="currentColor">
    <rect x="24" y="52" width="150" height="76" rx="4" fill-opacity="0.14"/>
    <rect x="330" y="52" width="150" height="76" rx="4" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="52" width="150" height="76" rx="4"/><rect x="330" y="52" width="150" height="76" rx="4"/>
  </g>
  <g stroke="currentColor" stroke-width="3.4" fill="none" opacity="0.85" marker-end="url(#arLk)">
    <line x1="180" y1="82" x2="324" y2="82"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" marker-end="url(#arLk)" stroke-dasharray="5 3">
    <path d="M 405 134 L 405 156 L 99 156 L 99 134"/>
  </g>
  <defs><marker id="arLk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="99" y="72">교사</text>
    <text x="99" y="90" font-size="9.5" opacity="0.85">시뮬레이션에서 RL로 학습</text>
    <text x="99" y="106" font-size="9.5" opacity="0.85">특권적 상태를 본다</text>
    <text x="405" y="72">학생</text>
    <text x="405" y="90" font-size="9.5" opacity="0.85">교사가 지도한다</text>
    <text x="405" y="106" font-size="9.5" opacity="0.85">고유수용감각 이력만 본다</text>
    <text x="252" y="76" font-size="10" opacity="0.85">증류</text>
    <text x="252" y="172" font-size="9.5" opacity="0.8">학생이 실행하고, 학생이 실제로 방문한 상태를 교사가 라벨한다</text>
  </g>
  <g font-size="10" fill="currentColor" opacity="0.9">
    <text x="24" y="196">특권적이며 실제 로봇에는 없는 것: 각 발 밑의 지형 프로파일, 접촉 상태와 힘,</text>
    <text x="24" y="210">마찰계수, 가해진 외란</text>
    <text x="24" y="232" font-size="11">학생은 보는 법을 배우지 않는다. 몸이 방금 어떻게 움직였는지에서 그 양들을 추론하는 법을 배운다.</text>
  </g>
</svg>

교사는 **시뮬레이터의 실제 상태**에 접근한 채 RL로 학습된다 — 지형 프로파일, 접촉 상태와 힘,
마찰계수, 가해진 외란력. 그중 무엇도 실제 로봇에는 없다. 그다음 교사는 짧은 고유수용감각 이력만
보는 학생으로 **지도학습을 통해 증류**되며, 데이터 수집은 DAgger식이다: 학생이 실행하고, 학생이
실제로 방문한 상태를 교사가 라벨한다.

학생은 지각하는 법을 배우지 않는다. **몸이 방금 어떻게 움직였는가로부터 특권적 양들을 추론하는
법**을 배운다 — 눈이 먼 로봇이 보지 못하는 진흙에, 한 번 밟은 뒤에는 적응할 수 있는 이유다.

**RMA**는 같은 계열에 독립적으로 도달한 것이고 배치 이야기가 더 날카롭다: 17차원 특권적 환경
벡터를 **8차원 잠재**로 압축하고, 그 잠재를 0.5초의 고유수용감각 이력에서 지도 회귀로 추정하되
전적으로 시뮬레이션에서 학습하며, **비동기로 — 기본 정책 100 Hz, 적응 모듈 10 Hz — 저가 로봇의
온보드 CPU에서** 돌린다.

이 패턴은 이후 로코모션을 훨씬 넘어 일반화되었다: 다수 전문가를 일반가로 증류하기, 모델 기반
전문가가 수동 데이터를 다시 라벨하기, 그리고 다른 옷을 입고 sim-to-real 레시피 일반의 교사-학생
구조로([[05-construction-robotics/sim-to-real|Sim-to-Real §2]]).

### 3. 정본과, 각 결과가 실제로 주장한 것

| 연구 | 무엇으로 유명한가 | 실제로 무엇을 주장했나 |
|---|---|---|
| **Hwangbo 등 2019** | "RL 로코모션" | **액추에이터 넷** — 하이브리드 시뮬레이터. 실증된 기술은 평지 명령 추종과 **넘어짐 복구**. 거친 지형은 주장이 아니다 |
| **Lee 등 2020** | 거친 지형 로코모션 | privileged 증류를 통한 **눈먼** 견고성. 진흙·눈·잔해·초목·흐르는 물. 속도 이득은 완만하고 지형에 특정적 |
| **Rudin 등 2021** | "몇 분 만에 걷기" | **GPU 하나에서의 벽시계 학습 시간** — 샘플 효율이 아니다. 인프라로서 중요 |
| **Miki 등 2022** | "사람 등산객을 이겼다" | 높이 지도를 얼마나 믿을지에 대한 **학습된 게이트**를 가진 지각 로코모션 |
| **ANYmal parkour 2024** | 파쿠르 | **계층적** 스킬 + 각 스킬의 능력 범위를 아는 상위 정책 |

셋은 풀어 쓸 값이 있다. 명성과 주장 사이의 간극이 곧 독해 실습이 사는 곳이기 때문이다.

**Hwangbo 2019의 기여는 걸음걸이가 아니라 시뮬레이터다.** 해석적 강체 물리를 유지하고, 아무도
잘 모델링하지 못하는 부분 — 직렬 탄성 액추에이터와 그 제어 소프트웨어 — 을 위치 오차와 속도의
이력에서 관절 토크를 회귀하는 작은 네트워크로 대체한다. **4분 미만의 로봇 데이터**로 학습한다.
대가는 워크스테이션 한 대에서 실시간의 약 1000배 시뮬레이션이다. 남는 발상은 "모델링할 수 없는
구성 요소는 배우고, 할 수 있는 물리는 지켜라"이며, 이후 모든 sim-to-real 액추에이터 모델링 결과의
조상이다.

**Rudin 2021은 인프라이고, 그렇게 서술해야 한다.** 워크스테이션 GPU 하나에서 수천 로봇을 병렬로,
그 체제에 맞춰 재조율한 PPO, 그리고 난이도에 따라 로봇을 승급·강등시키는 게임식 지형 커리큘럼.
공개된 `legged_gym` / `rsl_rl` 코드가 2022~2026년의 폭발을 평범한 연구실에서 경제적으로 가능하게
만든 것이다. 과학적 주장은 좁고, 인과적 영향력은 막대하다. 그 둘을 분리해 두는 것이 정확히 이
위키가 존재하는 이유의 교정이다.

**Miki 2022에서 흥미로운 것은 등반이 아니라 기제다.** 어텐션 기반 순환 **믿음 상태(belief state)**
인코더가 고유수용감각과 외수용 높이 지도를 융합하고, 지도를 얼마나 믿을지에 대한 **적응적 게이팅
계수**를 학습한다 — 그래서 지도가 거짓말할 때(눈, 키 큰 풀, 물, 반사면) 제어기가 고유수용감각
로코모션으로 우아하게 후퇴하며, 언제 믿기를 멈출지에 대한 손으로 만든 규칙이 없다.

> [!warning] 피해야 할 과잉 인용 셋
> - **알프스 등반은 가이드북 시간에 대한 단일 계측 경로**이지 사람 등산객에 대한 벤치마크 비교가
>   아니다. 2.2 km, 고도 120 m, 76분 가이드북 추정치에 대해 78분.
> - **"몇 분 만에 걷기"는 GPU 하나에서의 벽시계 시간이다.** 선행 연구보다 시뮬레이션 경험을 훨씬
>   *더 많이* 소모하며, 실기계 학습 시간도 아니다.
> - **휴머노이드 거친 지형 논문은 프리프린트다.** Radosavovic 등의 심사 통과 *Science Robotics*
>   휴머노이드 결과는 **눈먼 평지~완만한 굴곡의 실외 보행**이고, 버클리 등산로와 샌프란시스코
>   언덕이 나오는 거친 지형 후속은 arXiv 프리프린트인데 출판된 것처럼 자주 인용된다.

### 4. 파쿠르의 대조, 그리고 그것이 가르치는 것

몇 달 간격의 두 논문, 반대되는 아키텍처, 반대되는 하드웨어, 둘 다 파쿠르라 불린다.

| | **ANYmal parkour** (Science Robotics 2024) | **Extreme Parkour** (ICRA 2024) |
|---|---|---|
| 아키텍처 | 계층적: 별도 RL 스킬 + 스킬을 고르는 내비게이션 정책 | 단일 모놀리식 네트워크, 깊이에서 행동으로 |
| 인식 | 가려지고 잡음 있는 깊이로부터 명시적 장애물 재구성 | 전방 깊이 카메라 하나, 종단간 |
| 하드웨어 | ANYmal, 약 50 kg 연구용 4족 | 저가 로봇, 부정확한 액추에이터 |
| 눈에 띄는 기제 | 상위 정책이 각 스킬의 **능력 범위**를 안다 | 학습된 내부 yaw 보상이 정책 스스로 **조준하게** 한다, 별도 계획기 없이 |

둘 다 손으로 만들거나 손으로 고른 장애물 코스 너머로 일반화됨을 보이지 못했다. 함께 읽을 가치가
있는 이유는 분야가 같은 시점에 조합과 모놀리식 사이에서 진짜로 미결정 상태임을 보여 주기
때문이고, 또 **ANYmal parkour가 로코모션이 내비게이션으로 건너가는 지점**이기 때문이다: 어떤
지형이 어떤 스킬을 허용하는지 추론하는 상위 정책은 스킬-어포던스 인지 계획이고, 그것이 이
페이지와 [[04-robotics/semantic-language-navigation|19번]] 사이의 실제 인터페이스다.

### 5. 2025~26년에 간 곳

무게 중심이 "X 위를 걸을 수 있는가"에서 **일반가·교차 embodiment 정책**과 지형 표현 학습으로
옮겨 갔다.

- **어텐션 기반 지도 인코딩**(Science Robotics, 2025)은 고유수용감각을 조건으로 하는 지형 지도
  인코더를 **RL 제어기 안에서 종단간으로** 학습해, 미래 발디딤을 위해 디딜 수 있는 영역에
  주의를 두는 법을 배운다 — 그리고 **12자유도 ANYmal-D와 23자유도 휴머노이드 둘 다**에서 실증하는
  것이 눈에 띄는 부분이다.
- **Parkour in the wild**(IJRR, 2026)는 지형별 전문가들을 DAgger로 하나의 일반가 깊이 입력 정책에
  증류한 뒤, 실제 3D 스캔을 포함해 확장된 지형에서 RL 파인튜닝한다 — ANYmal parkour의 스킬 계층을
  단일 확장 가능 정책으로 무너뜨린다.
- **이산 지형에서의 고속 제어**(Science Robotics, 2025)는 **계획기 + 학습기 하이브리드**다:
  휴리스틱·신경망 필터링을 곁들인 표본 기반 발디딤 최적화 + RL 추종기. 4 m/s의 디딤돌, 1.3 m 간극
  점프. 정밀 지형에 대해 추가 부분적으로 하이브리드 쪽으로 되돌아가는 증거로 인용할 만하다.
- **LocoFormer**(CoRL 2025, 최우수 논문 최종 후보)가 로코모션 파운데이션 모델에 가장 가깝다:
  정밀한 기구학 없이 처음 보는 레그드 *그리고 바퀴* 로봇을 위한 단일 정책. 절차적으로 생성된
  형태들에서 학습하며, 실제 새로움은 **에피소드 경계를 가로지르도록** 늘린 컨텍스트 창이다 —
  창발적인 에피소드 간 적응이 나와서, 앞선 에피소드의 넘어짐으로부터 배운다.

로코모션 파운데이션 모델에 합의는 없고, Miki-2022나 Rudin-2021 급의 2026년 결과도 없다. 그렇게
말하는 편이 프리프린트 하나를 지명하는 것보다 쓸모 있다.

### 6. 도구, 논문의 연대를 정하기 때문에

- **Isaac Gym Preview는 공식 지원 종료다** — NVIDIA 자신의 페이지가 더 이상 지원되지 않는 레거시
  소프트웨어라 부르고, `IsaacGymEnvs`·`OmniIsaacGymEnvs` 저장소는 2026년 4월 읽기 전용으로 보관
  처리되었다. 2026년 논문이 "Isaac Gym을 썼다"고 하면 죽은 프리뷰 릴리스 위에 있는 것이다.
- **Isaac Lab**이 후속이고, 2026년 8월 기준 안정 라인은 2.3.x, 3.0은 베타다.
- **MuJoCo Playground / MJX**가 신뢰할 만한 벤더 중립 대안이며 MJX가 학계 기본값이 된 이유다.
- **Newton** — Disney Research·Google DeepMind·NVIDIA 공동 개발, 2025년 9월 리눅스 재단에 기여 —
  이 둘 아래의 공유 물리 층이 되어 가고 있고 MuJoCo Warp를 백엔드로 통합한다. Isaac/MuJoCo 분열이
  솔버 층에서 수렴 중이다.

전체 그림과 라이선스 함정은
[[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]]을 보라.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 교사-학생 그림을 그리고 무엇이 특권적인지 댄다.
- [ ] Hwangbo 2019가 실제로 무엇을 실증했는지 말한다.
- [ ] "몇 분 만에 걷기"가 왜 샘플 효율 주장이 아닌지 설명한다.
- [ ] Miki의 게이팅 기제와 그것이 무엇을 막는지 서술한다.
- [ ] 두 파쿠르 아키텍처를 대고, 둘 다 보이지 못한 것을 말한다.

### 스스로 점검

1. 눈먼 로봇이 어떻게 보지 못하는 진흙에 적응하는가?
2. 2026년 논문이 Isaac Gym에서 학습한 로코모션 결과를 보고한다. 무엇을 짚겠는가?
3. 누군가 Miki 2022를 로봇이 이제 사람 등산객을 능가한다는 근거로 인용한다. 교정하라.
4. LocoFormer의 늘린 컨텍스트 창이 실제로 무엇을 사는가?
5. 프로젝트가 매니퓰레이터를 싣고 거친 지반을 가는 레그드 플랫폼을 필요로 한다. 이 페이지에서
   가장 가까운 선례는 무엇이고, 그것이 주지 않는 것은?

> [!tip]- 정답 · Answers
> 1. 학생이, 마찰계수와 지형 프로파일을 *볼 수 있었던* 교사로부터 증류되었고, 그 양들을 짧은 고유수용감각 이력 — 지난 몇 분의 일 초 동안 몸이 실제로 어떻게 움직였는가 — 에서 추론하는 법을 배웠기 때문이다. 진흙을 미리 예상할 수는 없지만 발이 한 번 들어가고 나면 최근 운동 이력이 무엇이 달라졌는지에 대해 정보를 담고, 정책은 정확히 그 추론으로 학습되었다. 눈이 멀었다는 것이 먼저 접촉해야 하는 이유이고, 증류가 접촉만으로 충분한 이유다.
> 2. Isaac Gym Preview가 지원 종료라는 점 — NVIDIA 자신의 페이지가 레거시이며 지원되지 않는다고 하고, 관련 환경 저장소들은 2026년 4월 읽기 전용으로 보관되었다. 결과를 무효화하지는 않지만 작업의 연대를 정하고 재현을 어렵게 만들며, 지금 시작하는 프로젝트는 Isaac Lab이나 MuJoCo MJX에 있어야 한다.
> 3. 비교 대상은 **단일 계측 알프스 경로** — 2.2 km, 고도 120 m — 를 그 경로의 **76분 가이드북 추정치**에 대해 78분에 완주한 것이다. 사람 등산객에 대한 벤치마크가 아니라 발표된 시간에 대한 한 경로이고, 로봇이 전체적으로는 조금 더 느렸다. 결과는 진심으로 인상적이고, 그것이 뒷받침하는 주장은 통상 귀속되는 것보다 좁다.
> 4. 에피소드 *안*이 아니라 에피소드를 *가로지르는* 적응. 컨텍스트 창이 에피소드 경계를 넘으면 정책이 앞선 시도에서 일어난 일 — 넘어짐을 포함해 — 을 조건으로 삼을 수 있어, 가중치 갱신 없이 한 배치 안에서 개선된다. 에피소드 안에서 고유수용감각 이력으로 적응하고 에피소드가 끝나면 초기화되는 RMA식 잠재 추정과는 다른 기제다.
> 5. **ANYmal parkour.** 상위 정책이 어떤 지형이 무엇을 허용하는지 추론하는 유일한 결과이고, 그것이 모바일 매니퓰레이터가 작업 공간에 도달하는 데 필요한 것이기 때문이다. 그것이 주지 않는 것은 매니퓰레이터 자체다: 팔도, 페이로드도, 팔을 실었을 때 동역학이 어떻게 달라지는지에 대한 설명도 없는, 정돈된 코스 위의 장애물 사이 내비게이션 결과다. 팔을 더할 때의 오차 예산 귀결은 [[04-robotics/navigation-mobile-manipulation|16. §4]]에 있다.

### 출처

- J. Hwangbo, J. Lee, A. Dosovitskiy, et al., "Learning agile and dynamic motor skills for legged robots," *Science Robotics*, vol. 4, no. 26, eaau5872, 2019 ([arXiv:1901.08652](https://arxiv.org/abs/1901.08652)).
- J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, M. Hutter, "Learning Quadrupedal Locomotion over Challenging Terrain," *Science Robotics*, vol. 5, no. 47, eabc5986, 2020 ([arXiv:2010.11251](https://arxiv.org/abs/2010.11251)) — privileged teacher-student.
- N. Rudin, D. Hoeller, P. Reist, M. Hutter, "Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning," CoRL 2021 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — `legged_gym` / `rsl_rl`.
- A. Kumar, Z. Fu, D. Pathak, J. Malik, "RMA," RSS 2021, DOI 10.15607/RSS.2021.XVII.011 ([arXiv:2107.04034](https://arxiv.org/abs/2107.04034)).
- T. Miki, J. Lee, J. Hwangbo, et al., "Learning robust perceptive locomotion for quadrupedal robots in the wild," *Science Robotics*, vol. 7, no. 62, eabk2822, 2022 ([arXiv:2201.08117](https://arxiv.org/abs/2201.08117)).
- D. Hoeller, N. Rudin, D. Sako, M. Hutter, "ANYmal parkour," *Science Robotics*, vol. 9, no. 88, eadi7566, 2024 ([arXiv:2306.14874](https://arxiv.org/abs/2306.14874)).
- X. Cheng, K. Shi, A. Agarwal, D. Pathak, "Extreme Parkour with Legged Robots," ICRA 2024, pp. 11443–11450 ([arXiv:2309.14341](https://arxiv.org/abs/2309.14341)); Z. Zhuang et al., "Robot Parkour Learning," CoRL 2023 oral ([arXiv:2309.05665](https://arxiv.org/abs/2309.05665)).
- I. Radosavovic, T. Xiao, B. Zhang, et al., "Real-world humanoid locomotion with reinforcement learning," *Science Robotics*, vol. 9, no. 89, eadi9579, 2024 ([arXiv:2303.03381](https://arxiv.org/abs/2303.03381)). 거친 지형 후속 [arXiv:2410.03654](https://arxiv.org/abs/2410.03654)는 **프리프린트**다.
- 2025~26: He, Zhang, Jenelten, et al., *Science Robotics*, vol. 10, no. 105, eadv3604, 2025 ([arXiv:2506.09588](https://arxiv.org/abs/2506.09588)); Rudin, He, Aurand, Hutter, "Parkour in the wild," *IJRR*, 2026, DOI 10.1177/02783649261455067 ([arXiv:2505.11164](https://arxiv.org/abs/2505.11164)); Kim, Oh, Park, et al., *Science Robotics*, vol. 10, no. 102, eads6192, 2025 ([arXiv:2506.02835](https://arxiv.org/abs/2506.02835)); Liu, Pathak, Agarwal, "LocoFormer," CoRL 2025 ([arXiv:2509.23745](https://arxiv.org/abs/2509.23745)).

**이 위키 안에서**

- **논문 노트** — [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]] · [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등 2022]] · [[01-canonical-papers/notes/9-navigation/rma|RMA]] · [[01-canonical-papers/notes/9-navigation/anymal-parkour|ANYmal Parkour]]
- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]] — 이 로봇들이 보내지는 곳
- [[04-robotics/convex-mpc-legged|레그드 로봇의 Convex MPC]] — 같은 문제의 모델 기반 쪽
- [[05-construction-robotics/sim-to-real|필드 로봇 Sim-to-Real]] — 여러 전략 중 하나로서의 교사-학생
- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — §6의 도구 현황
