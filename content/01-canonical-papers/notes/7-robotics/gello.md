---
title: "GELLO — A General, Low-Cost, and Intuitive Teleoperation Framework for Robot Manipulators"
authors: Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, Pieter Abbeel
affiliation: UC Berkeley
venue: IROS
year: 2024
arxiv: https://arxiv.org/abs/2309.13037
project: https://wuphilipp.github.io/gello_site/
tags: [paper, manipulation, teleoperation]
status: note-complete
last_verified: 2026-08-21
study-depth: Literacy
wiki-support: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if the demonstration rig becomes part of the experimental setup."
---

**Wu et al., IROS 2024** — [arXiv](https://arxiv.org/abs/2309.13037) · [Official](https://wuphilipp.github.io/gello_site/)

> [!note] Math on-ramp · 수학 준비물
> Only one idea: kinematic isomorphism. If the leader device has the follower's kinematics scaled down, joint angles map across directly — no inverse kinematics, no retargeting ([[04-robotics/teleoperation-demonstration|12. §4–§5]] for what those two cost).
> 발상 하나뿐이다: 기구학적 동형. 리더 장치가 팔로워의 기구학을 축소해 갖고 있으면 관절각이 그대로 넘어간다 — 역기구학도 리타게팅도 없다(그 둘의 비용은 [[04-robotics/teleoperation-demonstration|12. §4~§5]]).

## English

**One-line summary**: A recipe for building a leader device that is a scaled kinematic replica of the target arm, from 3D-printed parts and off-the-shelf motors, giving joint-space isomorphic teleoperation.

### Context

Demonstration collection was gated on interface cost and awkwardness — VR controllers and 3D spacemice give a 6-DoF pose that then has to be retargeted onto an arm with different kinematics, and every retargeting choice is a way for demonstrations to end up in badly-conditioned parts of the workspace.

### Method

Build the leader to *be* the follower, smaller. Joint angles then transfer directly, so the operator's proprioception maps onto the robot's configuration rather than only onto its tool pose. The parts are 3D-printed; the motors are commodity. The paper is a design and a recipe as much as a result.

### Results

A user study reports it beating VR controllers and 3D spacemice for demonstration collection.

> [!warning] Reading the claims · 주장 읽는 법
> Despite "Low-Cost" in the title, the **abstract states no dollar figure**, no demonstration counts, and no success rates. Its only number is that the recipe covers **three** commonly used arms — Franka, UR5, and xArm. Comparative claims in the abstract are stated without numbers. If you quote a GELLO price, it is a body or project-site figure; say so.
> 제목에 "Low-Cost"가 있지만 **초록에는 금액도, 시연 수도, 성공률도 없다.** 유일한 숫자는 이 레시피가 흔히 쓰는 팔 **셋** — Franka, UR5, xArm — 을 다룬다는 것이다. 초록의 비교 주장에는 수치가 붙어 있지 않다. GELLO의 가격을 인용한다면 본문이나 프로젝트 사이트의 수치이니 그렇게 밝혀라.

### Limitations & critique

- **One leader per follower.** The isomorphism that makes it good is also what makes it non-general across arms — you build a new leader for each robot.
- **No force feedback.** It is a unilateral interface ([[04-robotics/teleoperation-demonstration|12. §2]]), so the operator cannot feel contact and the data contains no force channel.
- Backdriving a replica is ergonomically tiring over long sessions, which matters when the point is throughput.

### Connections

- [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection §4]] — the interface spectrum
- [[01-canonical-papers/notes/4-vla/act|ACT / ALOHA]] — the puppeteering rig this generalises

### 읽고 나면 말할 수 있어야 하는 것

- [ ] Say what kinematic isomorphism removes, and why that improves the data rather than only the experience.
- [ ] Name the two things this interface does not provide.
- [ ] State where a GELLO cost figure comes from.

## 한국어

**한 줄 요약**: 3D 프린팅 부품과 기성 모터로 대상 팔의 축소 기구학 복제품인 리더 장치를 만드는 레시피. 관절 공간 동형 원격조작을 준다.

### 배경

시연 수집이 인터페이스의 비용과 어색함에 발목이 잡혀 있었다 — VR 컨트롤러와 3D 스페이스마우스는 6자유도 자세를 주고, 그것을 기구학이 다른 팔로 리타게팅해야 하며, 모든 리타게팅 선택은 시연이 작업 공간의 조건 나쁜 영역에 놓이게 되는 통로다.

### 방법

리더를 팔로워 *그 자체*로, 더 작게 만들어라. 그러면 관절각이 그대로 이전되므로 조작자의 고유수용감각이 공구 자세만이 아니라 로봇의 자세(configuration)에 대응된다. 부품은 3D 프린팅이고 모터는 범용품이다. 이 논문은 결과이자 설계이자 레시피다.

### 결과

사용자 연구에서 시연 수집에 대해 VR 컨트롤러와 3D 스페이스마우스를 앞선다고 보고한다.

> [!warning] 주장 읽는 법 · Reading the claim
> 제목에 "Low-Cost"가 있지만 **초록에는 금액도, 시연 수도, 성공률도 없다.** 유일한 숫자는 흔히 쓰는 팔 **셋**(Franka, UR5, xArm)을 다룬다는 것이다. GELLO의 가격을 인용한다면 본문이나 프로젝트 사이트의 수치이니 그렇게 밝혀라.
> Despite "Low-Cost" in the title, the abstract states no price, no demo counts, no success rates.

### 한계와 비판

- **팔로워마다 리더 하나.** 이것을 좋게 만드는 동형성이 동시에 팔을 가로질러 일반적이지 못하게 만든다 — 로봇마다 새 리더를 만들어야 한다.
- **힘 피드백이 없다.** 단방향 인터페이스이므로([[04-robotics/teleoperation-demonstration|12. §2]]) 조작자가 접촉을 느낄 수 없고 데이터에 힘 채널이 없다.
- 복제품을 손으로 미는 것은 긴 세션에서 인체공학적으로 피곤하고, 요점이 처리량일 때는 그것이 문제가 된다.

### 연결

- [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집 §4]] — 인터페이스 스펙트럼
- [[01-canonical-papers/notes/4-vla/act|ACT / ALOHA]] — 이것이 일반화하는 퍼펫티어링 장비

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 기구학적 동형이 무엇을 없애며, 그것이 왜 경험만이 아니라 데이터를 개선하는지 말한다.
- [ ] 이 인터페이스가 주지 않는 두 가지를 댄다.
- [ ] GELLO 비용 수치가 어디서 오는지 말한다.
