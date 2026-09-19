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

Running task — **P2** carries a tool to a panel and makes controlled contact (wall stiffness of order **P3**, numbers frozen in [[02-foundations/lab-plants|0.6]]):

- C-space of the 2R (ch.2) → $T$ of the tip (ch.3) → FK at the frozen pose (ch.4) → $J$ (ch.5, already a lab) → the two IK branches that reach $(1,1)$ (ch.6).
- $M$ at rest (ch.8) → time a move (ch.9) → a path that does not promise force (ch.10) → PD vs inverse dynamics, then a $10\,\mathrm{N}$ contact (ch.11).
- Grasping the panel (ch.12) is a different question from pressing it; a wheeled base (ch.13) still cannot slide sideways into contact.

### Problem set · 과제

Tier C. Claim-reading. This hub is the map, not a chapter.

1. **Claim.** Which sentence is the claim that chapter 7 is omitted on purpose?
2. **Falsify.** What would falsify reading these summaries as a replacement for the book on a chapter marked Literacy?
3. **Task.** Name the frozen pose of P2 and the panel point it is built to reach.

> [!tip]- Solutions
> 1. The intro: chapter 7 (closed-chain kinematics) is intentionally omitted because this wiki prioritizes open-chain manipulation — that sentence *is* the claim.
> 2. Completing a chapter's problem set from the summary alone when the summary never derived the object (wiki-support was Literacy). Raising a chapter to Working means the set *is* completable here; ch.5 is the velocity lab, not this hub.
> 3. $\theta=(0^\circ,90^\circ)$, tip $(1,1)$. That is the panel point of the running task.

## 한국어

관통 과제 — **P2**가 도구를 패널까지 옮겨 힘을 조절하며 접촉한다(벽 강성은 **P3** 정도, 숫자는 [[02-foundations/lab-plants|0.6]]):

- 2R의 C-space(2장) → 말단의 $T$(3장) → 고정 자세 FK(4장) → $J$(5장, 이미 랩) → $(1,1)$에 닿는 IK 가지 둘(6장).
- 정지 $M$(8장) → 이동을 시간으로(9장) → 힘을 약속하지 않는 경로(10장) → PD 대 역동역학, 그다음 $10\,\mathrm{N}$ 접촉(11장).
- 패널을 잡는 것(12장)은 누르는 것과 다른 질문이고, 바퀴 베이스(13장)는 옆으로 미끄러져 접촉하지 못한다.

### 과제 · Problem set

Tier C. 주장 읽기. 이 허브는 지도이지 챕터가 아니다.

1. **주장.** 7장을 고의로 생략했다는 주장은 어느 문장인가?
2. **반증.** Literacy로 표시된 장에서 이 요약을 책의 대체로 읽는 주장을 깨는 것은?
3. **과제.** P2의 고정 자세와, 그것이 닿도록 만들어진 패널 점을 말하라.

> [!tip]- 정답 · Solutions
> 1. 도입: 7장(폐쇄 사슬 기구학)을 개연쇄 조작을 우선해 의도적으로 생략 — 그 문장이 곧 주장이다.
> 2. 요약이 대상을 유도하지 않았는데 요약만으로 그 장 과제를 끝내는 것(wiki-support가 Literacy였던 이유). Working으로 올린 장은 여기서 과제가 끝난다. 5장은 속도 랩이지 이 허브가 아니다.
> 3. $\theta=(0^\circ,90^\circ)$, 말단 $(1,1)$. 관통 과제의 패널 점이다.
