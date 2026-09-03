---
title: "ViNT and NoMaD — A Foundation Model for Visual Navigation, and Its Diffusion Successor"
authors: "ViNT: Dhruv Shah, Ajay Sridhar, Nitish Dashora, Kyle Stachowicz, Kevin Black, Noriaki Hirose, Sergey Levine · NoMaD: Ajay Sridhar, Dhruv Shah, Catherine Glossop, Sergey Levine"
affiliation: UC Berkeley
venue: "CoRL 2023 (ViNT, oral) · ICRA 2024 (NoMaD)"
year: 2023
arxiv: https://arxiv.org/abs/2306.14846
project: https://general-navigation-models.github.io/
tags: [paper, navigation, foundation-model, diffusion, cross-embodiment]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if cross-embodiment pretraining is a claim the thesis makes."
---

**Shah, Sridhar et al., CoRL 2023 (oral)** — [arXiv:2306.14846](https://arxiv.org/abs/2306.14846) · **Sridhar, Shah, Glossop & Levine, ICRA 2024** — [arXiv:2310.07896](https://arxiv.org/abs/2310.07896) · [Project](https://general-navigation-models.github.io/)

> [!note] Math on-ramp · 수학 준비물
> Goal-conditioned policies, and diffusion as a policy class ([[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]). One extra idea for NoMaD: *masking* the goal at training time so one model covers both goal-directed and goal-free behaviour.
> 목표 조건부 정책, 그리고 정책 계열로서의 확산([[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]). NoMaD를 위한 발상 하나 더: 학습 시 목표를 *가려서*(mask) 하나의 모델이 목표 지향 행동과 목표 없는 행동을 모두 담게 하기.

## English

**One-line summary**: Train one goal-reaching Transformer on navigation data from **many different robots**, and it outperforms specialists trained on any single dataset — then replace its action head with a **goal-masked diffusion policy** so the same model both explores and goes somewhere.

### Context

Navigation had no foundation model. Every dataset was collected on one platform, and every policy was trained for it. The insight ViNT builds on is that a **general goal-reaching objective** can be applied to *any* navigation dataset regardless of platform, which is what makes cross-embodiment pretraining possible at all.

### Method — ViNT

> [!tip] Key intuition · 핵심 직관
> A common goal-reaching objective makes navigation experience from different platforms share a training interface. NoMaD’s goal masking then teaches the action model to handle both present and absent goals, so exploration is part of the learned conditioning scheme rather than an entirely separate controller.

A Transformer trained with a general goal-reaching objective on a number of existing navigation datasets — **hundreds of hours of robotic navigation from a variety of robotic platforms**. The architecture is chosen for adaptability: it is meant to be adapted efficiently to downstream navigational tasks rather than used as-is. Two augmentations extend it: **diffusion-based subgoal proposals** for exploring novel environments, and long-range heuristics that let it solve **kilometre-scale** navigation.

### Method — NoMaD

Navigation needs two behaviours that are usually built separately: task-oriented navigation to a located goal, and task-agnostic exploration when the goal has not been found. NoMaD unifies them in a **single diffusion policy** — a Transformer encoder with a diffusion decoder — by **masking the goal** during training, so the absence of a goal is a normal input rather than a different mode. Real-world results report better navigation in unseen environments than the alternatives, with **smaller models and lower collision rates**.

### Results

**What it measured.** The abstract reports no quantitative result as an exact comparative performance score for either [ViNT](https://arxiv.org/abs/2306.14846) or [NoMaD](https://arxiv.org/abs/2310.07896). Their descriptions of data scale, navigation extent, and comparator count are not numerical success or collision rates.

ViNT: **positive transfer** — outperforming specialist models trained on singular datasets. NoMaD: improved unseen-environment navigation, smaller model, fewer collisions.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> "Positive transfer" is the paper's real, checkable claim and it is the interesting one — it says pooling across embodiments *helped* rather than merely not hurting. **No percentage appears in either abstract.** Note also what the datasets are: hundreds of hours of *wheeled and legged research platforms in mostly outdoor and campus settings*, which bounds what the "foundation" covers.

### Limitations & critique

- **Goal-reaching is image-goal, not language-goal.** These models go to a place that looks like a picture. Instruction following is a different task — see [[01-canonical-papers/notes/9-navigation/navid|NaVid]].
- **Cross-embodiment across similar embodiments.** The platforms differ in wheelbase and camera height, not in kind. Nothing here says a policy pooled over ground robots transfers to a 20-tonne machine.
- **Diffusion costs inference time.** NoMaD reports smaller models, which helps, but a denoising loop in a navigation controller is still a timing commitment ([[04-robotics/robot-systems-deployment|10. §2]]).
- Collision rate is a good metric and a low bar: it says the robot did not hit anything, not that it went anywhere useful.

### Impact & follow-ups

Together these two are the reference for **navigation foundation models**, and NoMaD's goal-masking trick is the tidiest existing answer to the explore/exploit split that most navigation stacks handle with a mode switch. Read as a pair: ViNT establishes that pooling works, NoMaD establishes what to do with the pooled model.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation]] — where these sit among navigation approaches
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — the same policy class in manipulation
- [[01-canonical-papers/notes/4-vla/open-x-embodiment|Open X-Embodiment]] — the manipulation-side cross-embodiment pooling argument
- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — the outdoor setting most of the data comes from

### After reading

- [ ] State what makes a navigation dataset usable for ViNT regardless of which robot produced it.
- [ ] Explain goal masking and what problem it removes.
- [ ] Say precisely what "positive transfer" claims.
- [ ] Name the kind of goal these models accept, and the kind they do not.

## 한국어

**한 줄 요약**: **여러 다른 로봇**의 내비게이션 데이터로 목표 도달 Transformer 하나를 학습시키면, 단일 데이터셋으로 학습한 전문 모델들을 능가한다. 그다음 행동 헤드를 **목표를 가린 확산 정책**으로 바꾸면 같은 모델이 탐색도 하고 어딘가로 가기도 한다.

### 배경

내비게이션에는 파운데이션 모델이 없었다. 모든 데이터셋이 하나의 플랫폼에서 수집되었고, 모든 정책이 그 플랫폼을 위해 학습되었다. ViNT가 딛고 선 통찰은 **일반적 목표 도달 목적함수**가 플랫폼과 무관하게 *어떤* 내비게이션 데이터셋에도 적용될 수 있다는 것이고, 그것이 애초에 신체 교차 사전학습을 가능하게 한다.

### 방법 — ViNT

> [!tip] 핵심 직관 · Key intuition
> 공통 목표 도달 목적이 다른 플랫폼의 항법 경험을 같은 학습 인터페이스로 묶는다. NoMaD의 목표 마스킹은 목표가 있거나 없는 경우를 행동 모델에 가르친다. 탐색이 완전히 별도 제어기보다 학습한 조건화 방식의 일부가 된다.

일반적 목표 도달 목적함수로, 기존의 여러 내비게이션 데이터셋 — **다양한 로봇 플랫폼에서 온 수백 시간의 로봇 주행** — 위에서 학습한 Transformer다. 구조는 적응성을 보고 골랐다: 그대로 쓰는 것이 아니라 하류 내비게이션 과제에 효율적으로 적응시키도록 만들어졌다. 두 가지 증강이 이를 확장한다: 새로운 환경 탐색을 위한 **확산 기반 부분 목표 제안**, 그리고 **킬로미터 규모** 내비게이션을 풀게 해주는 장거리 휴리스틱.

### 방법 — NoMaD

내비게이션에는 보통 따로 만드는 두 행동이 필요하다: 위치를 찾은 목표로 가는 과제 지향 주행, 그리고 목표를 아직 찾지 못했을 때의 과제 불가지론적 탐색. NoMaD는 학습 중에 **목표를 가림으로써** 둘을 **하나의 확산 정책** — Transformer 인코더에 확산 디코더 — 으로 통합한다. 목표의 부재가 다른 모드가 아니라 정상적인 입력이 되는 것이다. 실제 환경 결과는 처음 보는 환경에서 대안들보다 나은 주행을, **더 작은 모델과 더 낮은 충돌률**과 함께 보고한다.

### 결과

**무엇을 쟀는가.** [ViNT](https://arxiv.org/abs/2306.14846)와 [NoMaD](https://arxiv.org/abs/2310.07896) 초록에 정확한 비교 성능 점수는 없다. 데이터 규모, 이동 범위, 비교 방법 수를 설명하지만 성공률이나 충돌률의 수치는 제시하지 않는다.

ViNT: **positive transfer** — 단일 데이터셋으로 학습한 전문 모델을 능가한다. NoMaD: 처음 보는 환경에서의 주행 개선, 더 작은 모델, 더 적은 충돌.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "positive transfer"가 논문의 실제로 확인 가능한 주장이고 흥미로운 주장이다 — 신체를 가로질러 데이터를 합치는 것이 해가 되지 않은 정도가 아니라 *도움이 되었다*는 말이다. **두 초록 어디에도 퍼센트는 없다.** 데이터셋이 무엇인지도 짚어야 한다: 대체로 야외와 캠퍼스 환경의 *바퀴형·다리형 연구 플랫폼* 수백 시간이고, 그것이 이 "파운데이션"이 덮는 범위를 한정한다.

### 한계와 비판

- **목표 도달은 이미지 목표이지 언어 목표가 아니다.** 이 모델들은 사진처럼 보이는 곳으로 간다. 지시 따르기는 다른 과제다 — [[01-canonical-papers/notes/9-navigation/navid|NaVid]]를 보라.
- **비슷한 신체들을 가로지르는 신체 교차다.** 플랫폼들은 축거와 카메라 높이가 다르지 종류가 다르지 않다. 지상 로봇들에 걸쳐 합친 정책이 20톤 기계로 전이된다는 말은 여기에 없다.
- **확산은 추론 시간을 쓴다.** NoMaD가 더 작은 모델을 보고하는 것이 도움이 되지만, 내비게이션 제어기 안의 잡음 제거 루프는 여전히 타이밍 약속이다([[04-robotics/robot-systems-deployment|10. §2]]).
- 충돌률은 좋은 지표이자 낮은 기준선이다: 로봇이 아무것도 들이받지 않았다는 말이지, 쓸모 있는 곳에 갔다는 말이 아니다.

### 영향과 후속 연구

이 둘이 함께 **내비게이션 파운데이션 모델**의 기준점이고, NoMaD의 목표 가리기 요령은 대부분의 내비게이션 스택이 모드 전환으로 다루는 탐색/활용 분리에 대한 현존하는 가장 깔끔한 답이다. 짝으로 읽어라: ViNT가 합치는 것이 통한다는 것을 세우고, NoMaD가 합친 모델로 무엇을 할지를 세운다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션]] — 내비게이션 접근들 사이에서 이들이 놓이는 자리
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — 매니퓰레이션에서의 같은 정책 계열
- [[01-canonical-papers/notes/4-vla/open-x-embodiment|Open X-Embodiment]] — 매니퓰레이션 쪽의 신체 교차 통합 논증
- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율주행]] — 데이터 대부분이 오는 야외 환경

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 어떤 로봇이 만들었든 내비게이션 데이터셋을 ViNT에 쓸 수 있게 만드는 것이 무엇인지 말한다.
- [ ] 목표 가리기를 설명하고 그것이 없애는 문제를 말한다.
- [ ] "positive transfer"가 정확히 무엇을 주장하는지 말한다.
- [ ] 이 모델들이 받는 목표의 종류와 받지 않는 종류를 댄다.
