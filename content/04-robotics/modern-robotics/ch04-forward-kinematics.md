---
title: "MR Ch.4 — Forward Kinematics"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.4** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

## English

**Core question**: given joint angles $\theta$, where is the end-effector?

- **Product of Exponentials (PoE)** — the chapter's one big formula:
  $$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$
  Read right-to-left: start from the home pose $M$, then each joint screws the whole chain
  downstream of it. Two ingredients only: home pose + one screw axis per joint (in the
  fixed frame, at home position).
- **Body form**: $T(\theta) = M\, e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}$
  with axes expressed in the end-effector frame — same content, different bookkeeping.
- **Vs Denavit-Hartenberg**: D-H needs per-link frame conventions (and endless convention
  bugs); PoE needs no intermediate frames at all. MR's pedagogical bet — and modern
  software's (many simulators/libraries are PoE-native).
- Worked intuition: a 3R planar arm — each $e^{[\mathcal{S}_i]\theta_i}$ rotates everything
  after joint $i$; freezing $\theta_{i+1..n}$ shows the formula *is* the mechanism.

**Wiki connections**: FK is the deterministic core inside every simulator and every
digital-twin update ([[05-construction-robotics/index|construction]]); VLA policies that
output joint chunks ([[01-canonical-papers/notes/4-vla/pi0|π0]]) rely on FK to interpret them in
task space.

## 한국어

**핵심 질문**: 관절 각 $\theta$가 주어지면 말단은 어디에 있는가?

- **지수 곱 공식 (PoE)** — 이 장의 단 하나의 큰 공식:
  $$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$
  오른쪽에서 왼쪽으로 읽어라: 홈 자세 $M$에서 시작해, 각 관절이 자기 하류의 사슬 전체를
  스크류로 돌린다. 재료는 둘뿐: 홈 자세 + 관절당 스크류 축 하나(고정 프레임, 홈 위치 기준).
- **바디 형식**: 축을 말단 프레임에서 표현한
  $T(\theta) = M\, e^{[\mathcal{B}_1]\theta_1}\cdots e^{[\mathcal{B}_n]\theta_n}$ —
  내용은 같고 장부 정리만 다르다.
- **D-H 대비**: D-H는 링크마다 프레임 규약이 필요하고(그리고 끝없는 규약 버그), PoE는 중간
  프레임이 아예 필요 없다. MR의 교육적 베팅이자 현대 소프트웨어의 선택이다(많은
  시뮬레이터/라이브러리가 PoE 네이티브).
- 직관 연습: 평면 3R 팔 — 각 $e^{[\mathcal{S}_i]\theta_i}$가 관절 $i$ 이후의 전부를 돌린다;
  $\theta_{i+1..n}$을 얼려 보면 공식이 *곧* 기구임이 보인다.

**위키 연결**: FK는 모든 시뮬레이터와 디지털 트윈 갱신([[05-construction-robotics/index|건설]])
안의 결정론적 핵심이고, 관절 청크를 출력하는 VLA 정책([[01-canonical-papers/notes/4-vla/pi0|π0]])을
작업 공간에서 해석하는 데 FK가 쓰인다.
