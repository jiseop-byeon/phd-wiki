---
title: "Universal Manipulation Interface — In-The-Wild Robot Teaching Without In-The-Wild Robots"
authors: Cheng Chi, Zhenjia Xu, Chuer Pan, et al.
affiliation: Stanford University, Columbia University, Toyota Research Institute
venue: RSS
year: 2024
arxiv: https://arxiv.org/abs/2402.10329
pdf: https://arxiv.org/pdf/2402.10329
project: https://umi-gripper.github.io
tags: [paper, manipulation, teleoperation, imitation-learning]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when demonstration collection or the embodiment gap becomes part of the thesis contribution."
---

**Chi et al., RSS 2024** — [arXiv](https://arxiv.org/abs/2402.10329) · [PDF](https://arxiv.org/pdf/2402.10329) · [Official](https://umi-gripper.github.io)

> [!note] Math on-ramp · 수학 준비물
> You need SE(3) poses and relative versus absolute transforms ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]]) — the whole trick turns on expressing actions relative to the current gripper frame rather than in world coordinates. Add the embodiment gap and demonstration-quality vocabulary from [[04-robotics/teleoperation-demonstration|12. §4, §6]].
> SE(3) 자세와 상대 변환 대 절대 변환([[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]])이 필요하다 — 이 논문의 요령 전체가 행동을 월드 좌표가 아니라 현재 그리퍼 프레임 기준으로 표현하는 데 달려 있다. embodiment 격차와 시연 품질 어휘는 [[04-robotics/teleoperation-demonstration|12. §4, §6]].

## English

**One-line summary**: A handheld gripper with a camera lets a person demonstrate manipulation anywhere, with no robot present, and a matching policy interface makes the resulting data transfer to real robots.

### Context

Every demonstration-collection method before this needed the robot in the loop: a leader
arm ([[01-canonical-papers/notes/4-vla/act|ALOHA]]), a VR interface driving the follower, or
kinesthetic teaching on the arm itself. That ties data collection to robot availability,
robot workspace, and robot cost — and it confines the data to wherever the robot is, which
in practice means a lab.

The obvious alternative — let a human just do the task while a camera watches — creates the
**embodiment gap**: the demonstration was produced by a body with different kinematics,
different sensor placement, and different dynamics from the robot that must reproduce it.
UMI's claim is that the gap can be engineered away rather than learned away.

### Method

> [!tip] Key intuition
> Make the *interface* the constant. If the same gripper and the same camera are present
> both when the human demonstrates and when the robot executes, then most of the embodiment
> gap disappears by construction — what is left is latency and the arm behind the gripper.

<svg viewBox="0 0 560 246" style="max-width:100%;height:auto" role="img" aria-label="the same gripper and camera held by a human during collection and by a robot at deployment, with the three remaining gaps listed">
  <g fill="currentColor">
    <rect x="30" y="46" width="210" height="92" rx="4" fill-opacity="0.08"/>
    <rect x="320" y="46" width="210" height="92" rx="4" fill-opacity="0.08"/>
    <rect x="68" y="86" width="134" height="40" rx="3" fill-opacity="0.34"/>
    <rect x="358" y="86" width="134" height="40" rx="3" fill-opacity="0.34"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="30" y="46" width="210" height="92" rx="4"/><rect x="320" y="46" width="210" height="92" rx="4"/>
    <rect x="68" y="86" width="134" height="40" rx="3"/><rect x="358" y="86" width="134" height="40" rx="3"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="135" y="40">collection: a person, anywhere</text>
    <text x="425" y="40">deployment: a robot arm</text>
    <text x="135" y="102">handheld gripper</text><text x="135" y="117" font-size="9.5">+ fisheye camera</text>
    <text x="425" y="102">the same gripper</text><text x="425" y="117" font-size="9.5">+ the same camera</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.8" marker-end="url(#arU)">
    <line x1="248" y1="106" x2="314" y2="106"/>
  </g>
  <defs><marker id="arU" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="9.5" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="280" y="100">data</text>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="30" y="166">What stays constant: the gripper geometry and the camera&#8217;s view of the contact.</text>
    <text x="30" y="184">What still differs, and how each is closed:</text>
    <text x="44" y="202" font-size="10">&#183; where the demonstrator stood &#8594; actions expressed relative to the gripper, not the world</text>
    <text x="44" y="218" font-size="10">&#183; the robot&#8217;s control delay &#8594; latency matched at inference time</text>
    <text x="44" y="234" font-size="10">&#183; no external motion capture &#8594; 6-DoF pose from IMU-aided visual SLAM on the same camera</text>
  </g>
</svg>

The hardware is a handheld parallel-jaw gripper carrying a **fisheye camera**, side
**mirrors** that give the single camera implicit stereo, and an **IMU** whose readings aid
visual SLAM so the device recovers its own 6-DoF trajectory without external tracking.

The interface half matters as much as the hardware:

- **Relative-trajectory actions.** The policy predicts motion in the current gripper frame
  rather than absolute world poses, so it does not matter where the demonstrator was
  standing or where the robot's base ends up.
- **Inference-time latency matching.** The robot's control and perception delays are
  compensated at execution so the policy sees the temporal relationship it was trained on.

Together these make the learned policies **hardware-agnostic** in the specific sense that
matters: the same demonstration data drives different arms.

### Results

> [!warning] Reading the claim · 핵심 주장 읽는 법
> **The abstract of this paper contains no numbers at all.** Every success rate, episode
> count, and collection-speed figure that circulates for UMI comes from the body, the
> project page, or secondary write-ups. That is not a criticism of the paper — it is a
> warning about how you cite it. When you quote a UMI number, say which part of the paper it
> came from, and check it there.

The demonstrated capability is the paper's real result: dynamic, bimanual, precise and
long-horizon tasks learned from in-the-wild demonstrations and deployed on real arms, with
zero-shot generalisation to environments and objects not seen during collection.

### Limitations & critique

- **The gripper is the interface, so the gripper is the constraint.** Anything a
  parallel-jaw gripper with that geometry cannot do is outside the method.
- **Force is absent.** The device records vision and pose, not contact force — so the
  contact-rich distinctions of [[04-robotics/tactile-visuotactile|14. §1]] are not in the
  data at all. A policy trained this way is choosing trajectories, not regulating contact.
- **SLAM is a dependency, not a detail.** Pose comes from visual SLAM on a moving handheld
  camera; texture-poor or dusty scenes degrade exactly the signal the actions are expressed in.
- Latency matching compensates a *modelled* delay; a variable one is harder.

### Impact & follow-ups

UMI reframed demonstration collection from "operate the robot well" to "produce data
cheaply, anywhere", which is the reframing [[04-robotics/teleoperation-demonstration|12. §1]]
is built around. Its practical descendant question — how much of the embodiment gap can be
closed by hardware rather than by learning — is now a standard design axis for data
collection rigs.

**For construction**: this is the one demonstration method that can leave the building.
Panel fitting, bolt fastening and pipe insertion happen where the building is, and a
handheld device can be carried there while a robot cannot. The missing force channel is the
gap a construction adaptation would need to close.

### Connections

- [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection]] — the interface spectrum this sits at one end of
- [[01-canonical-papers/notes/4-vla/act|ACT / ALOHA]] — the leader-arm approach at the other end
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — the policy class typically trained on this data
- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — where field data collection would matter

### After reading

- [ ] Explain the embodiment gap and name the three things UMI does to close it.
- [ ] Say why relative-trajectory actions matter more than they sound like they should.
- [ ] Name the modality the device does not record, and what that costs.
- [ ] State where a UMI number you want to quote actually comes from.

## 한국어

**한 줄 요약**: 카메라를 단 휴대형 그리퍼로 로봇 없이 어디서나 조작을 시연하고, 짝을 이루는 정책 인터페이스가 그 데이터를 실제 로봇으로 옮긴다.

### 배경

이전의 모든 시연 수집 방법은 로봇을 루프 안에 두어야 했다: 리더 암([[01-canonical-papers/notes/4-vla/act|ALOHA]]),
팔로워를 구동하는 VR 인터페이스, 또는 팔을 직접 잡고 가르치는 직접 교시. 그러면 데이터 수집이
로봇의 가용성·작업 공간·비용에 묶이고, 데이터가 로봇이 있는 곳 — 실전에서는 실험실 — 에
갇힌다.

명백한 대안 — 사람이 그냥 작업하는 것을 카메라가 보게 하기 — 은 **embodiment 격차**를 만든다:
시연을 만든 몸이 그것을 재현해야 하는 로봇과 기구학도, 센서 배치도, 동역학도 다르다. UMI의
주장은 그 격차를 학습으로 없애는 대신 **설계로 없앨 수 있다**는 것이다.

### 방법

> [!tip] 핵심 직관
> *인터페이스*를 상수로 만들어라. 사람이 시연할 때와 로봇이 실행할 때 같은 그리퍼와 같은
> 카메라가 있다면, embodiment 격차의 대부분이 구조적으로 사라진다 — 남는 것은 지연과 그리퍼
> 뒤에 달린 팔뿐이다.

<svg viewBox="0 0 560 246" style="max-width:100%;height:auto" role="img" aria-label="수집 때는 사람이, 배치 때는 로봇이 드는 같은 그리퍼와 카메라, 그리고 남는 격차 셋">
  <g fill="currentColor">
    <rect x="30" y="46" width="210" height="92" rx="4" fill-opacity="0.08"/>
    <rect x="320" y="46" width="210" height="92" rx="4" fill-opacity="0.08"/>
    <rect x="68" y="86" width="134" height="40" rx="3" fill-opacity="0.34"/>
    <rect x="358" y="86" width="134" height="40" rx="3" fill-opacity="0.34"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="30" y="46" width="210" height="92" rx="4"/><rect x="320" y="46" width="210" height="92" rx="4"/>
    <rect x="68" y="86" width="134" height="40" rx="3"/><rect x="358" y="86" width="134" height="40" rx="3"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="135" y="40">수집: 사람이, 어디서나</text>
    <text x="425" y="40">배치: 로봇 팔이</text>
    <text x="135" y="102">휴대형 그리퍼</text><text x="135" y="117" font-size="9.5">+ 어안 카메라</text>
    <text x="425" y="102">같은 그리퍼</text><text x="425" y="117" font-size="9.5">+ 같은 카메라</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.8" marker-end="url(#arUk)">
    <line x1="248" y1="106" x2="314" y2="106"/>
  </g>
  <defs><marker id="arUk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="9.5" fill="currentColor" opacity="0.8" text-anchor="middle">
    <text x="280" y="100">데이터</text>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="30" y="166">그대로 유지되는 것: 그리퍼의 기하와, 카메라가 보는 접촉의 시야.</text>
    <text x="30" y="184">여전히 다른 것과, 각각을 닫는 방법:</text>
    <text x="44" y="202" font-size="10">&#183; 시연자가 서 있던 위치 &#8594; 행동을 월드가 아니라 그리퍼 기준 상대로 표현</text>
    <text x="44" y="218" font-size="10">&#183; 로봇의 제어 지연 &#8594; 추론 시점에 지연을 정합</text>
    <text x="44" y="234" font-size="10">&#183; 외부 모션 캡처 없음 &#8594; 같은 카메라의 IMU 보조 시각 SLAM으로 6자유도 자세</text>
  </g>
</svg>

하드웨어는 **어안 카메라**, 카메라 하나로 암묵적 스테레오를 만드는 옆면 **거울**, 그리고
시각 SLAM을 보조해 외부 추적 없이 장치 자신의 6자유도 궤적을 복원하게 하는 **IMU**를 실은
휴대형 평행 조 그리퍼다.

인터페이스 쪽 절반이 하드웨어만큼 중요하다:

- **상대 궤적 행동.** 정책이 절대 월드 자세가 아니라 현재 그리퍼 프레임에서의 운동을
  예측하므로, 시연자가 어디에 서 있었는지도 로봇 베이스가 어디에 놓이는지도 상관없어진다.
- **추론 시점의 지연 정합.** 실행 시 로봇의 제어·인식 지연을 보상해, 정책이 학습할 때 본
  시간 관계를 그대로 보게 한다.

이 둘이 합쳐져 정책을 정확히 중요한 의미에서 **하드웨어 불가지론적**으로 만든다: 같은 시연
데이터가 서로 다른 팔을 구동한다.

### 결과

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> **이 논문의 초록에는 숫자가 하나도 없다.** UMI에 대해 떠도는 성공률·에피소드 수·수집 속도
> 수치는 전부 본문, 프로젝트 페이지, 또는 2차 요약에서 온 것이다. 논문에 대한 비판이 아니라
> *인용 방식*에 대한 경고다. UMI의 숫자를 인용할 때는 논문의 어느 부분에서 왔는지 밝혀라.

이 논문의 진짜 결과는 실증된 능력 자체다: 야생에서 모은 시연으로 학습해 실제 팔에 배치한
동적·양팔·정밀·긴 지평 작업들, 그리고 수집 때 보지 못한 환경과 물체로의 zero-shot 일반화.

### 한계와 비판

- **그리퍼가 인터페이스이므로 그리퍼가 제약이다.** 그 기하의 평행 조 그리퍼가 할 수 없는
  것은 전부 이 방법 바깥이다.
- **힘이 없다.** 장치는 비전과 자세를 기록하지 접촉력을 기록하지 않는다 — 그래서
  [[04-robotics/tactile-visuotactile|14. §1]]이 세우는 접촉 상태의 구분이 데이터에 아예 없다.
  이렇게 학습한 정책은 접촉을 조절하는 것이 아니라 궤적을 고르는 것이다.
- **SLAM은 세부가 아니라 의존성이다.** 자세가 움직이는 휴대형 카메라의 시각 SLAM에서 오므로,
  질감이 부족하거나 먼지가 많은 장면은 하필 행동이 표현되는 그 신호를 저하시킨다.
- 지연 정합은 *모델링된* 지연을 보상한다. 변동하는 지연은 더 어렵다.

### 영향과 후속 연구

UMI는 시연 수집을 "로봇을 잘 조종하는 것"에서 "어디서나 싸게 데이터를 만드는 것"으로
재프레이밍했고, 그것이 [[04-robotics/teleoperation-demonstration|12. §1]]이 딛고 선
재프레이밍이다. 그 실용적 후손 질문 — embodiment 격차의 얼마만큼을 학습이 아니라 하드웨어로
닫을 수 있는가 — 은 이제 수집 장비 설계의 표준 축이다.

**건설의 경우**: 건물 밖으로 나갈 수 있는 유일한 시연 방법이다. 패널 끼움, 볼트 체결, 배관
삽입은 건물이 있는 곳에서 일어나고, 휴대형 장치는 거기까지 들고 갈 수 있지만 로봇은 못 간다.
빠져 있는 힘 채널이 건설용으로 변형할 때 닫아야 할 격차다.

### 연결

- [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]] — 이것이 한쪽 끝에 놓이는 인터페이스 스펙트럼
- [[01-canonical-papers/notes/4-vla/act|ACT / ALOHA]] — 반대쪽 끝의 리더 암 방식
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — 이 데이터로 보통 학습하는 정책 계열
- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 현장 데이터 수집이 중요해지는 곳

### 읽고 나면 말할 수 있어야 하는 것

- [ ] embodiment 격차를 설명하고 UMI가 그것을 닫는 세 가지를 댄다.
- [ ] 상대 궤적 행동이 왜 들리는 것보다 중요한지 말한다.
- [ ] 장치가 기록하지 않는 모달리티와 그 대가를 댄다.
- [ ] 인용하려는 UMI 숫자가 실제로 어디서 왔는지 말한다.
