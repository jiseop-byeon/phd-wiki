---
title: "Learning Quadrupedal Locomotion over Challenging Terrain"
authors: Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, Marco Hutter
affiliation: ETH Zürich, KAIST, Intel Labs
venue: Science Robotics
year: 2020
journal-ref: "Science Robotics 5(47), eabc5986"
arxiv: https://arxiv.org/abs/2010.11251
tags: [paper, locomotion, legged, sim-to-real, rl]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if privileged-information distillation becomes a method you use rather than cite."
---

**Lee, Hwangbo, Wellhausen, Koltun & Hutter, *Science Robotics* 5(47), eabc5986, 2020** — [arXiv:2010.11251](https://arxiv.org/abs/2010.11251)

> [!note] Math on-ramp · 수학 준비물
> Policy-gradient RL and the notion of a partially observed state ([[02-foundations/rl-basics|7. RL Basics]]), plus what "privileged information" means in a teacher–student setup — the whole method is [[04-robotics/legged-locomotion|18. §2]].
> 정책 경사 RL과 부분 관측 상태의 개념([[02-foundations/rl-basics|7. RL 기초]]), 그리고 teacher–student 구조에서 "특권 정보"가 무엇인지가 필요하다 — 방법 전체가 [[04-robotics/legged-locomotion|18. §2]]다.

## English

**One-line summary**: Train a teacher in simulation with access to the true terrain, then distil it into a student that receives only **proprioception** — and the student walks through mud, snow, rubble and running water it never saw in training.

### Context

Legged controllers had been elaborate state machines: explicitly triggered motion primitives and reflexes, growing in complexity while never approaching animal robustness. The alternative — learn the controller — ran into the standard sim-to-real wall, since a policy that depends on perceiving the terrain inherits every failure of the perception.

### Method

> [!tip] Key intuition
> Let the teacher cheat, then make the student earn it. In simulation the terrain is known exactly, so a teacher can be trained on it directly. The student cannot see the terrain, so it must learn to **infer** the same quantities from how the body has just been moving.

The controller acts on **a stream of proprioceptive signals** — no cameras, no lidar. The paper's own phrase for what this buys is *radical robustness*, and it is achieved by training in a domain far simpler than the one it is deployed in.

### Results

Verbatim from the abstract: **zero-shot generalization from simulation to natural environments**, across **two generations** of ANYmal robots, retaining robustness under conditions **never encountered during training** — deformable terrain such as mud and snow, dynamic footholds such as rubble, and overground impediments such as thick vegetation and gushing water.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> **The abstract of this paper reports no numbers.** No success rate, no distance, no speed, no comparison table — the claim is qualitative and environmental. What makes it credible is the *breadth of demonstrated conditions*, not a metric. Cite it for "blind proprioceptive locomotion generalises to natural terrain", never for a percentage. The wiki's canonical-claim discipline exists partly because this paper is so often quoted with numbers it does not contain.
> **이 논문의 초록에는 숫자가 없다.** 성공률도, 거리도, 속도도, 비교표도 없다. 주장은 정성적이고 환경적이다. 신뢰를 만드는 것은 지표가 아니라 *실증된 조건의 폭*이다. "맹목적 고유수용 로코모션이 자연 지형으로 일반화한다"로 인용하고, 퍼센트로는 절대 인용하지 마라. 위키가 정본 주장 규율을 두는 이유 하나가, 이 논문이 담고 있지도 않은 숫자와 함께 너무 자주 인용되기 때문이다.

### Limitations & critique

- **Blind is robust and slow.** Without exteroception the robot must feel the terrain before adapting to it, which caps speed and energy efficiency. That limitation is the explicit premise of [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al. 2022]].
- **Locomotion, not navigation.** The policy keeps the body upright and moving; it does not decide where to go. Conflating the two is the most common misreading of this line of work.
- **The teacher's advantage must exist.** Privileged distillation requires a simulator in which the privileged quantity is both available and correct. For terrain geometry that holds; for contact friction and deformable ground it holds much less well.
- Robustness is demonstrated, not bounded. Nothing here tells you the conditions under which it fails.

### Impact & follow-ups

This is the paper that made **teacher–student privileged distillation** the default recipe in learned legged control, and the reason [[04-robotics/legged-locomotion|18]] is organised around that architecture rather than around gaits. [[01-canonical-papers/notes/9-navigation/rma|RMA]] reaches a similar place through online system identification instead of distillation; [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al.]] adds back the exteroception this paper deliberately removed.

**For construction**: rubble, mud and temporary works are exactly this paper's demonstrated regime, and a blind controller keeps working when dust defeats the depth sensor. The base mobility problem on a site is closer to solved than the manipulation problem on top of it.

### Connections

- [[04-robotics/legged-locomotion|18. Legged Locomotion]] — the concept page built on this architecture
- [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al. 2022]] — exteroception added back, robustly
- [[01-canonical-papers/notes/9-navigation/rma|RMA]] — adaptation instead of distillation
- [[02-foundations/rl-basics|7. RL Basics]] — the training machinery underneath

### After reading

- [ ] Explain what the teacher knows that the student does not, and how the student compensates.
- [ ] Say why removing exteroception increases robustness and decreases speed.
- [ ] State the difference between what this controller does and what "navigation" means.
- [ ] State what this paper's abstract does and does not contain.

## 한국어

**한 줄 요약**: 시뮬레이션에서 실제 지형을 아는 교사를 학습시킨 뒤, **고유수용 감각만** 받는 학생으로 증류한다. 그 학생이 학습 중에 본 적 없는 진흙·눈·잔해·흐르는 물을 걸어서 통과한다.

### 배경

레그드 제어기는 정교한 상태 기계였다: 명시적으로 촉발되는 운동 원형과 반사들이 복잡도만 키우면서 동물의 강건함에는 끝내 닿지 못했다. 대안 — 제어기를 학습한다 — 은 표준적인 sim-to-real 벽에 부딪혔다. 지형을 인지해야 하는 정책은 그 인지의 모든 실패를 물려받기 때문이다.

### 방법

> [!tip] 핵심 직관
> 교사에게는 반칙을 허용하고, 학생에게는 그것을 벌게 하라. 시뮬레이션에서는 지형이 정확히 알려져 있으므로 교사를 그 위에서 바로 학습시킬 수 있다. 학생은 지형을 볼 수 없으므로, 몸이 방금 어떻게 움직였는지에서 같은 양들을 **추론**하는 법을 배워야 한다.

제어기는 **고유수용 신호의 흐름** 위에서 동작한다 — 카메라도 라이다도 없다. 이것이 사는 것을 논문 자신은 *radical robustness*(근본적 강건함)라 부르고, 배포되는 곳보다 훨씬 단순한 영역에서 학습하는 것으로 그것을 달성한다.

### 결과

초록 그대로: **시뮬레이션에서 자연 환경으로의 zero-shot 일반화**, ANYmal **두 세대**에 걸쳐, **학습 중 한 번도 마주친 적 없는** 조건에서도 강건함 유지 — 진흙과 눈 같은 변형 지형, 잔해 같은 동적 디딤면, 무성한 식생과 쏟아지는 물 같은 지상 방해물.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> **이 논문의 초록에는 숫자가 없다.** 성공률도, 거리도, 속도도, 비교표도 없다. 주장은 정성적이고 환경적이다. 신뢰를 만드는 것은 지표가 아니라 *실증된 조건의 폭*이다. "맹목적 고유수용 로코모션이 자연 지형으로 일반화한다"로 인용하고, 퍼센트로는 절대 인용하지 마라.
> The abstract reports no numbers at all — the claim is qualitative and environmental, and its credibility comes from the breadth of demonstrated conditions.

### 한계와 비판

- **눈이 없으면 강건하고 느리다.** 외수용 감각이 없으면 로봇은 적응하기 전에 지형을 발로 더듬어야 하고, 그것이 속도와 에너지 효율의 상한을 정한다. 그 한계가 [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등 2022]]의 명시적 전제다.
- **로코모션이지 내비게이션이 아니다.** 정책은 몸을 세우고 움직이게 할 뿐, 어디로 갈지는 정하지 않는다. 둘을 섞는 것이 이 계보에 대한 가장 흔한 오독이다.
- **교사의 우위가 실제로 존재해야 한다.** 특권 증류는 특권 정보가 가용하고 *동시에* 정확한 시뮬레이터를 요구한다. 지형 기하는 그렇지만, 접촉 마찰과 변형 지반은 훨씬 덜 그렇다.
- 강건함은 실증되었지 한정되지 않았다. 어떤 조건에서 실패하는지는 여기서 알 수 없다.

### 영향과 후속 연구

**teacher–student 특권 증류**를 학습 기반 레그드 제어의 기본 레시피로 만든 논문이고, [[04-robotics/legged-locomotion|18]]이 보행 양식이 아니라 이 아키텍처를 중심으로 짜인 이유다. [[01-canonical-papers/notes/9-navigation/rma|RMA]]는 증류 대신 온라인 시스템 식별로 비슷한 자리에 도달하고, [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등]]은 이 논문이 의도적으로 뺀 외수용 감각을 다시 넣는다.

**건설의 경우**: 잔해·진흙·가설물은 정확히 이 논문이 실증한 영역이고, 먼지가 깊이 센서를 무력화해도 맹목 제어기는 계속 작동한다. 현장에서 베이스 이동 문제는 그 위에 얹히는 조작 문제보다 훨씬 더 풀려 있다.

### 연결

- [[04-robotics/legged-locomotion|18. 레그드 로코모션]] — 이 아키텍처 위에 세운 개념 페이지
- [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등 2022]] — 외수용 감각을 강건하게 되돌려 넣기
- [[01-canonical-papers/notes/9-navigation/rma|RMA]] — 증류 대신 적응
- [[02-foundations/rl-basics|7. RL 기초]] — 그 아래의 학습 기구

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 교사가 알고 학생이 모르는 것이 무엇이고, 학생이 그것을 어떻게 벌충하는지 설명한다.
- [ ] 외수용 감각을 빼는 것이 왜 강건함을 올리고 속도를 낮추는지 말한다.
- [ ] 이 제어기가 하는 일과 "내비게이션"의 차이를 말한다.
- [ ] 이 논문 초록에 무엇이 있고 무엇이 없는지 말한다.
