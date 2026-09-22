---
title: 2. Modern Robotics Summary
study-depth: Literacy
depth-goal: "Understand the track structure and identify which robotics tool a paper assumes."
mastery-when: "Raise the chapters and tools used by the thesis to Working; master only the contribution-bearing subsystem."
---

Chapter summaries of *Modern Robotics* (Lynch & Park), covering ch. 2–6 and 8–13 —
read alongside the [[04-robotics/modern-robotics-book|book guide]]. Chapter 7
(closed-chain kinematics) is intentionally omitted: this wiki prioritizes open-chain
manipulation, control, and physical-AI literacy.

*Modern Robotics* (Lynch & Park)의 챕터 요약 (2–6장, 8–13장) —
[[04-robotics/modern-robotics-book|책 가이드]]와 함께 읽는다. 7장(폐쇄 사슬 기구학)은
의도적으로 생략했다: 이 위키는 개연쇄 조작·제어·physical AI 문해력을 우선한다.

## English

> [!note] First pass · 처음이라면
> This hub is a map, not a chapter, and teaches nothing by itself. Read the running-task arc and the study order below, then open ch.2 and work through ch.2–6, 8 and 9 in order, each alongside the book; every chapter derives its step on P2. Chapters 10–13 wait for the track pages the study order names.

Running task — **P2** carries a tool to a panel and makes controlled contact (wall stiffness of order **P3**, numbers frozen in [[02-foundations/lab-plants|0.6]]):

- C-space of the 2R (ch.2) → $T$ of the tip (ch.3) → FK at the frozen pose (ch.4) → $J$ (ch.5, already a lab) → the two IK branches that reach $(1,1)$ (ch.6).
- $M$ at rest (ch.8) → time a move (ch.9) → a path that does not promise force (ch.10) → PD vs inverse dynamics, then a $10\,\mathrm{N}$ contact (ch.11).
- Grasping the panel (ch.12) is a different question from pressing it; a wheeled base (ch.13) still cannot slide sideways into contact.

**Study order.** Chapters 2–6, 8 and 9 are read in sequence, each alongside the book. The last four are read with the track pages that use them: ch.10 with [[04-robotics/planning-decision-making|4. Planning & Decision-Making]], ch.11 after [[04-robotics/control-theory-ce397|5. Control Theory]], ch.12 with [[04-robotics/grasping|15. Grasping]], and ch.13 with [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]].

### Problem set · 과제

Tier C. Claim-reading. This hub is the map, not a chapter.

1. **Claim.** Which sentence is the claim that chapter 7 is omitted on purpose?
2. **Falsify.** What would falsify reading these summaries as a replacement for the book?
3. **Task.** Name the frozen pose of P2 and the panel point it is built to reach.

> [!tip]- Solutions
> 1. The intro: chapter 7 (closed-chain kinematics) is intentionally omitted because this wiki prioritizes open-chain manipulation — that sentence *is* the claim.
> 2. A problem on a chapter page that cannot be finished from that page, its prerequisites and 0.6 alone. Every chapter page here (ch.2–6 and 8–13) is marked wiki-support: Working, which is exactly the claim that no such problem exists, so one counter-example demotes that page to Literacy. What no page replaces is the book's breadth, and the pages say where they stop: D-H parameters (ch.4), the recursive Newton–Euler algorithm (ch.8), and closed chains (ch.7, omitted). ch.5 is the velocity lab, not this hub.
> 3. $\theta=(0^\circ,90^\circ)$, tip $(1,1)$. That is the panel point of the running task.

## 한국어

> [!note] 처음이라면 · First pass
> 이 허브는 장이 아니라 지도이고, 그 자체로는 아무것도 가르치지 않는다. 관통 과제의 흐름과 아래 학습 순서를 읽고, 2장을 펴서 2–6장, 8장, 9장을 차례로, 각각 책과 함께 읽어라. 모든 장이 자기 단계를 P2에서 유도한다. 10–13장은 학습 순서가 지목하는 트랙 페이지를 기다린다.

관통 과제 — **P2**가 도구를 패널까지 옮겨 힘을 조절하며 접촉한다(벽 강성은 **P3** 정도, 숫자는 [[02-foundations/lab-plants|0.6]]):

- 2R의 C-space(2장) → 말단의 $T$(3장) → 고정 자세 FK(4장) → $J$(5장, 이미 랩) → $(1,1)$에 닿는 IK 가지 둘(6장).
- 정지 $M$(8장) → 이동을 시간으로(9장) → 힘을 약속하지 않는 경로(10장) → PD 대 역동역학, 그다음 $10\,\mathrm{N}$ 접촉(11장).
- 패널을 잡는 것(12장)은 누르는 것과 다른 질문이고, 바퀴 베이스(13장)는 옆으로 미끄러져 접촉하지 못한다.

**학습 순서.** 2–6장, 8장, 9장은 차례로, 각각 책과 함께 읽는다. 나머지 네 장은 그것을 쓰는 트랙 페이지와 함께 읽는다. 10장은 [[04-robotics/planning-decision-making|4. 계획과 의사결정]]과 함께, 11장은 [[04-robotics/control-theory-ce397|5. 제어 이론]] 다음에, 12장은 [[04-robotics/grasping|15. 파지]]와 함께, 13장은 [[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 조작]]과 함께 읽는다.

### 과제 · Problem set

Tier C. 주장 읽기. 이 허브는 지도이지 챕터가 아니다.

1. **주장.** 7장을 고의로 생략했다는 주장은 어느 문장인가?
2. **반증.** 이 요약을 책의 대체로 읽는 주장을 깨는 것은?
3. **과제.** P2의 고정 자세와, 그것이 닿도록 만들어진 패널 점을 말하라.

> [!tip]- 정답 · Solutions
> 1. 도입: 7장(폐쇄 사슬 기구학)을 개연쇄 조작을 우선해 의도적으로 생략 — 그 문장이 곧 주장이다.
> 2. 어떤 장 페이지의 과제가 그 페이지, 선수 페이지, 0.6만으로는 끝나지 않는 것. 여기 모든 장 페이지(2–6장, 8–13장)는 wiki-support: Working으로 표시되어 있고, 그것이 바로 그런 과제가 없다는 주장이므로 반례 하나면 그 페이지는 Literacy로 내려간다. 어느 페이지도 대신하지 못하는 것은 책의 폭이고, 페이지들이 어디서 멈추는지 스스로 말한다. D-H 파라미터(4장), 재귀 뉴턴–오일러 알고리즘(8장), 폐쇄 사슬(7장, 생략). 5장은 속도 랩이지 이 허브가 아니다.
> 3. $\theta=(0^\circ,90^\circ)$, 말단 $(1,1)$. 관통 과제의 패널 점이다.
