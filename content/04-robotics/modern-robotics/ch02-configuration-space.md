---
title: "MR Ch.02 — Configuration Space"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.2** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

## English

**Core question**: what is the space of all possible "positions" of a robot, and what shape is it?

- **Configuration** = a complete specification of every point of the robot; the minimum
  number of coordinates needed = **degrees of freedom (dof)**. C-space = the set of all
  configurations.
- **Grübler's formula**: for a mechanism of $N$ links and $J$ joints with joint freedoms $f_i$:
  $\text{dof} = m(N - 1 - J) + \sum_i f_i$ ($m = 3$ planar, $6$ spatial). Worked: the planar
  four-bar → $3(4-1-4)+4 = 1$ dof — one number describes the whole mechanism.
- **Topology matters**: a 2R arm's C-space is a torus ($T^2 = S^1 \times S^1$), not a plane —
  angles wrap. This is exactly why naive angle regression breaks
  ([[02-foundations/se3-geometry|8. SE(3) §2]]) and why "C-space distance" needs care.
- Representations: **explicit** (minimal coordinates, may have singularities) vs
  **implicit** (embed in higher-dim space + constraints — like rotation matrices with
  $R^\top R = I$). MR consistently chooses implicit — the same choice modern robot
  learning makes.
- **Task space vs C-space**: where the tool lives vs where the robot lives; the map
  between them is kinematics (ch.4–6).
- Constraints: **holonomic** (reduce C-space dimension) vs **nonholonomic** (restrict
  velocities, not positions — a car can reach any pose but can't slide sideways).

**Wiki connections**: C-space is the "state" half of every
[[02-foundations/rl-basics|MDP]] for robots; VLA action spaces are coordinates on it.

## 한국어

**핵심 질문**: 로봇의 가능한 "자세" 전체의 공간은 무엇이고, 그 모양은 어떠한가?

- **컨피규레이션** = 로봇 모든 점의 완전한 지정; 필요한 최소 좌표 수 = **자유도(dof)**.
  C-space = 모든 컨피규레이션의 집합.
- **그뤼블러 공식**: 링크 $N$개, 관절 $J$개, 관절 자유도 $f_i$인 기구에서
  $\text{dof} = m(N - 1 - J) + \sum_i f_i$ ($m = 3$ 평면, $6$ 공간). 계산 예: 평면 4절
  링크 → $3(4-1-4)+4 = 1$ 자유도 — 숫자 하나가 기구 전체를 기술한다.
- **위상이 중요하다**: 2R 팔의 C-space는 평면이 아니라 원환면($T^2 = S^1 \times S^1$) —
  각도는 감긴다. 순진한 각도 회귀가 깨지는 정확한 이유이고
  ([[02-foundations/se3-geometry|8. SE(3) §2]]), "C-space 거리"에 주의가 필요한 이유다.
- 표현: **명시적**(최소 좌표, 특이점 가능) vs **암시적**(고차원에 묻고 제약 추가 —
  $R^\top R = I$인 회전 행렬처럼). MR은 일관되게 암시적을 고른다 — 현대 로봇 학습과 같은
  선택이다.
- **작업 공간 vs C-space**: 도구가 사는 곳 vs 로봇이 사는 곳; 둘 사이의 사상이
  기구학이다(4~6장).
- 제약: **홀로노믹**(C-space 차원을 줄임) vs **비홀로노믹**(위치가 아니라 속도를 제한 —
  자동차는 어느 자세든 도달하지만 옆으로 미끄러지지는 못한다).

**위키 연결**: C-space는 로봇 [[02-foundations/rl-basics|MDP]]의 "상태" 절반이고, VLA 행동
공간은 그 위의 좌표다.
