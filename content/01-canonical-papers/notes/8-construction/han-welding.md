---
title: "Vision-Based Construction Robot for Real-Time Automated Welding with HRI (Lee & Han, 2024)"
authors: Doyun Lee, Kevin Han
affiliation: NC State University, Construction Automation and Robotics Lab (CARL)
venue: Automation in Construction
year: 2024
doi: https://doi.org/10.1016/j.autcon.2024.105699
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Lee & Han, Automation in Construction 2024** — [DOI](https://doi.org/10.1016/j.autcon.2024.105699)

## English

**One-line summary**: A UGV-mounted robot arm detects weld joints with vision and welds them in real time, shipping with two operating modes — fully automated *and* a human-robot-interaction mode that keeps the worker in the loop.

**Lineage position**: construction computer vision growing hands — Kevin Han is a Golparvar-Fard PhD descendant, so this is the vision-and-monitoring lineage arriving at physical manipulation. Method (literacy level): camera-based weld-joint detection localizes the seam, the arm executes the weld trajectory in real time, and mode selection decides whether the robot proceeds autonomously or defers to human interaction. Evidence: real hardware welding experiments (testbed scale, not an active construction site); a follow-up in JCEM 151(5) 2025 adds the autonomous navigation and positioning the 2024 paper leaves to the human.

**Limitations**: testbed validation on prepared joints, not production steelwork; autonomy covers detect-and-weld — getting the UGV to the joint is the 2025 follow-up's problem; the dual-mode design is itself a concession that full autonomy is not yet trusted for a safety-critical hot-work task, which makes the paper an honest data point on the autonomy/intervention frontier.

## 한국어

**한 줄 요약**: UGV에 탑재된 로봇 팔이 비전으로 용접 이음부를 탐지해 실시간으로 용접한다 — 완전 자동 모드 *그리고* 작업자를 루프에 남기는 인간-로봇 상호작용(HRI) 모드, 두 가지 운용 모드를 갖췄다.

**계보에서의 위치**: 건설 컴퓨터 비전에 손이 자라는 순간 — Kevin Han은 Golparvar-Fard의 박사 제자이므로, 이것은 비전·모니터링 계보가 물리적 조작에 도착한 것이다. 방법 (리터러시 수준): 카메라 기반 용접 이음부 탐지가 이음선을 위치 추정하고, 팔이 실시간으로 용접 궤적을 수행하며, 모드 선택이 로봇의 자율 진행과 인간 상호작용 위임을 결정한다. 증거: 실물 하드웨어 용접 실험(테스트베드 규모이지, 가동 중인 건설 현장이 아니다); JCEM 151(5) 2025 후속이 2024년 논문에서 사람 몫이던 자율 주행·위치잡기를 추가한다.

**한계**: 준비된 이음부에서의 테스트베드 검증이지, 생산 철골 작업이 아니다; 자율성은 탐지-용접을 다루고, UGV를 이음부까지 데려가는 것은 2025년 후속의 문제다; 이중 모드 설계 자체가 안전 결정적 화기 작업에 완전 자율이 아직 신뢰받지 못한다는 양보이며, 그래서 이 논문은 자율/개입 경계에 대한 정직한 데이터 포인트다.

### 연결

- 스트림: [[05-construction-robotics/assembly-fabrication|4. 조립·시공 스트림]]
- 계보: Golparvar-Fard → Kevin Han (NC State CARL) — [[05-construction-robotics/lineage|건설로봇 계보]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading (○)

- [ ] Describe the vision seam-detection → real-time welding execution pipeline and the difference between the two operating modes · 비전 이음부 탐지 → 실시간 용접 실행의 파이프라인과 두 운용 모드의 차이를 말할 수 있다
- [ ] State the division of labour between the 2024 testbed evidence and the 2025 JCEM follow-up on autonomous navigation and positioning · 테스트베드 증거(2024)와 자율 주행·위치잡기 후속(2025 JCEM)의 분업을 말할 수 있다
- [ ] Place this paper as the Golparvar-Fard vision lineage extending into manipulation · 이 논문을 Golparvar-Fard 비전 계보가 조작으로 확장된 사례로 자리매김할 수 있다
