---
title: "Mobile ALOHA — Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation"
authors: Zipeng Fu, Tony Z. Zhao, Chelsea Finn
affiliation: Stanford University
venue: CoRL
year: 2024
arxiv: https://arxiv.org/abs/2401.02117
project: https://mobile-aloha.github.io
tags: [paper, manipulation, teleoperation, mobile-manipulation]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when mobile manipulation data collection is part of the thesis contribution."
---

**Fu, Zhao & Finn, CoRL 2024** — [arXiv](https://arxiv.org/abs/2401.02117) · [Official](https://mobile-aloha.github.io). Note the DBLP proceedings entry reads "…Manipulation **using** Low-Cost…" while arXiv reads "**with**" — cite whichever version you used.

> [!note] Math on-ramp · 수학 준비물
> You need action chunking and why it exists ([[01-canonical-papers/notes/4-vla/act|ACT]]), plus the idea of co-training: mixing a large existing dataset with a small new one so the small one does not have to carry the whole policy ([[02-foundations/ml-practice|9. ML Practice]]).
> 행동 청킹과 그것이 존재하는 이유([[01-canonical-papers/notes/4-vla/act|ACT]]), 그리고 co-training 발상이 필요하다: 큰 기존 데이터셋에 작은 새 데이터셋을 섞어, 작은 쪽이 정책 전체를 지지 않아도 되게 하는 것([[02-foundations/ml-practice|9. ML 실무]]).

## English

**One-line summary**: Put ALOHA's bimanual rig on a mobile base with the operator physically tethered to it, so whole-body demonstrations — base motion and both arms together — can be collected, then co-train with the existing static ALOHA data.

### Context

[[01-canonical-papers/notes/4-vla/act|ALOHA]] solved bimanual demonstration collection for a fixed workspace. Most useful tasks are not in a fixed workspace: opening a cabinet, wiping a counter, and carrying something across a room all require the base and the arms to move *together*, and demonstrating that needs an interface where the operator can drive both at once.

### Method

The operator is physically attached to the mobile base, so walking the base and puppeteering the arms happen in one coordinated motion — whole-body teleoperation without a separate base controller to think about.

The learning contribution is **co-training**: train on the new mobile-manipulation demonstrations together with the existing static ALOHA dataset, rather than on the new data alone.

### Results

From the **abstract**: "With **50 demonstrations** for each task, co-training can increase success rates by **up to 90%**."

> [!warning] Reading the claim · 핵심 주장 읽는 법
> That 90% is neither a 90% success rate nor a 1.9× multiplier: it is an **increase in percentage points**. The paper's own convention is to write a gain as the difference between two rates ("95% vs. 0%" for Call Elevator), and several no-co-training baselines sit at 0%, where a relative increase is undefined. Quote it as *up to a 90-point gain on the best task*, and read the per-task table rather than the headline. The widely circulated hardware cost is **not in the abstract** either; it comes from the body or the project site.

### Limitations & critique

- **Co-training's benefit depends on the static dataset existing.** The result is partly a statement about how much a prior dataset is worth, which is not transferable to a domain where no such dataset exists — construction, for instance.
- The operator being tethered to the base is ergonomically specific and does not scale to large sites or hazardous ones.
- Household-scale tasks; payloads and reach are far from construction requirements.
- No force channel, like every leader-arm rig ([[04-robotics/teleoperation-demonstration|12. §4]]).

### Connections

- [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]] — the class this belongs to: manipulable poses, reachability, base placement, error budget
- [[01-canonical-papers/notes/4-vla/act|ACT / ALOHA]] — the static predecessor
- [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection]] — the interface question
- [[07-research-program/paper-arc|7.1 Paper Arc]] — the paper 2 plus paper 4 combination this exemplifies

### After reading

- [ ] Say why base and arms must be demonstrated together rather than separately.
- [ ] State exactly what the 90% figure measures — a percentage-point gain over the no-co-training baseline, not a success rate.
- [ ] Name the assumption co-training depends on, and why it may not hold in construction.

## 한국어

**한 줄 요약**: ALOHA의 양팔 장비를 모바일 베이스에 올리고 조작자를 그 베이스에 물리적으로 묶어, 베이스 운동과 두 팔을 함께 하는 전신 시연을 수집한 뒤 기존 고정형 ALOHA 데이터와 co-training한다.

### 배경

[[01-canonical-papers/notes/4-vla/act|ALOHA]]는 고정된 작업 영역에서의 양팔 시연 수집을 풀었다. 쓸모 있는 작업 대부분은 고정된 작업 영역 안에 있지 않다: 수납장 열기, 조리대 닦기, 방을 가로질러 무언가 옮기기 — 전부 베이스와 팔이 *함께* 움직여야 하고, 그것을 시연하려면 조작자가 둘을 동시에 몰 수 있는 인터페이스가 필요하다.

### 방법

조작자가 모바일 베이스에 물리적으로 붙어 있어서, 베이스를 걸어 옮기는 것과 팔을 조종하는 것이 하나의 협응된 운동으로 일어난다 — 따로 생각할 베이스 컨트롤러 없는 전신 원격조작이다.

학습 쪽 기여는 **co-training**이다: 새 데이터만이 아니라 새 모바일 조작 시연을 기존 고정형 ALOHA 데이터셋과 함께 학습한다.

### 결과

**초록**에서: "각 과제에 대해 **시연 50개**로, co-training이 성공률을 **최대 90%까지** 높일 수 있다."

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 저 90%는 90% 성공률도 1.9배도 아니다. **퍼센트 포인트 증가**다. 논문 자신의 표기가 두 성공률의 차이(엘리베이터 호출 "95% vs. 0%")이고, co-training 없는 기준선 중 몇은 0%여서 상대 증가는 정의되지 않는다. *가장 좋은 과제에서 최대 90포인트 상승*으로 인용하고, 헤드라인 대신 과제별 표를 읽어라. 널리 떠도는 하드웨어 가격도 **초록에 없다** — 본문이나 프로젝트 사이트에서 온 것이다.

### 한계와 비판

- **Co-training의 이득은 고정형 데이터셋이 존재한다는 데 의존한다.** 이 결과는 부분적으로 선행 데이터셋이 얼마나 값어치 있는지에 관한 진술이고, 그런 데이터셋이 없는 도메인 — 예컨대 건설 — 으로는 이전되지 않는다.
- 조작자가 베이스에 묶이는 것은 인체공학적으로 특수하고, 넓은 현장이나 위험한 현장으로 확장되지 않는다.
- 가정 규모의 작업들이다. 페이로드와 도달 범위가 건설 요구와 한참 멀다.
- 모든 리더 암 장비가 그렇듯 힘 채널이 없다([[04-robotics/teleoperation-demonstration|12. §4]]).

### 연결

- [[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 매니퓰레이션]] — 이것이 속한 계열: 조작 가능한 자세, 도달성, base placement, 오차 예산
- [[01-canonical-papers/notes/4-vla/act|ACT / ALOHA]] — 고정형 선행 연구
- [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]] — 인터페이스 문제
- [[07-research-program/paper-arc|7.1 논문 arc]] — 이것이 예시하는 2편 + 4편 결합

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 베이스와 팔을 따로가 아니라 함께 시연해야 하는 이유를 말한다.
- [ ] 90%라는 수치가 정확히 무엇을 재는지 말한다 — co-training 없는 기준선 대비 퍼센트 포인트 상승이지 성공률이 아니다.
- [ ] Co-training이 의존하는 가정과, 건설에서 그것이 성립하지 않을 수 있는 이유를 댄다.
