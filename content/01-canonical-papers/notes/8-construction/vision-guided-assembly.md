---
title: "Vision-Guided Autonomous Robotic Assembly and As-Built Scanning (Feng et al., 2015)"
authors: Chen Feng, Yong Xiao, Aaron Willette, Wes McGee, Vineet Kamat
affiliation: University of Michigan (Kamat lab + Taubman College FABLab)
venue: Automation in Construction 59
year: 2015
doi: https://doi.org/10.1016/j.autcon.2015.06.002
tags: [paper, construction, assembly, perception]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Feng et al., Automation in Construction 2015** — [DOI](https://doi.org/10.1016/j.autcon.2015.06.002)

## English

**One-line summary**: A mobile construction manipulator localizes itself at an unstructured work face, uses marker-based vision to assemble components autonomously, and scans the result back into an as-built model — closing the design→build→verify geometry loop on a construction task in 2015.

**Lineage position**: this is the anchor paper of the Michigan (Kamat/Menassa) construction-manipulation lineage — the line that continues through [[01-canonical-papers/notes/8-construction/lundeen-2019|Lundeen's geometrically adaptive task execution (2019)]] and [[01-canonical-papers/notes/8-construction/liang-lfd|Liang's learning-from-demonstration (2020)]], and whose first author Chen Feng now runs NYU's AI4CE lab. It names the structural fact that separates construction robotics from manufacturing: the **reversed spatial relationship** — the manipulator must travel to and register against a large static structure, rather than a fixtured product arriving at a fixed robot.

**Method**: the workflow chains four stages — (1) design model specifies target geometry; (2) the mobile platform localizes at the work face using fiducial-marker-based vision metrology, recovering the robot-to-workpiece transform without factory fixturing; (3) vision-guided manipulation places prepared components against the target geometry; (4) the same sensing scans the assembled result into an as-built model that can be compared against design intent. Every stage is 2015-era classical vision — printed fiducial markers, calibrated cameras — not learned perception.

**Evidence**: the demonstration is a physical mobile-manipulator assembly cell executing the full loop — mobile localization, autonomous component placement, and as-built scanning — on real hardware with prepared components. The contribution the field kept is the *architecture*: it is the earliest complete instance of the design → mobile registration → manipulation → as-built verification cycle that later Michigan work (and today's [[01-canonical-papers/notes/8-construction/bim-digital-twin|BIM-driven digital-twin workflows]]) elaborates.

**Limitations**: marker-based metrology and prepared components deliberately remove most site uncertainty — the paper solves registration and closure, not perception in clutter. Component variety, tolerance recovery when parts do not fit, and marker-free localization are all left to successors (Lundeen 2019 addresses as-built geometric adaptation directly).

> [!question] Reading the claim
> "Autonomous robotic assembly" here means autonomous within a marker-instrumented, prepared-component workflow. Treat the paper as the foundational integrated loop — the first complete design→build→verify cycle on a mobile construction manipulator — not as evidence that unstructured site assembly was solved in 2015. The fiducial markers are the load-bearing assumption: every later paper in this lineage can be read as removing one of them.

## 한국어

**한 줄 요약**: 모바일 건설 매니퓰레이터가 비정형 작업면에서 스스로 위치를 정합하고, 마커 기반 비전으로 부품을 자율 조립한 뒤, 결과를 as-built 모델로 다시 스캔한다 — 2015년에 건설 과제에서 설계→시공→검증 기하 루프를 닫았다.

**계보에서의 위치**: 미시간(Kamat/Menassa) 건설 조작 계보의 앵커 논문이다 — 이 라인은 [[01-canonical-papers/notes/8-construction/lundeen-2019|Lundeen의 기하 적응형 과제 실행(2019)]]과 [[01-canonical-papers/notes/8-construction/liang-lfd|Liang의 시연 학습(2020)]]으로 이어지고, 제1저자 Chen Feng은 현재 NYU AI4CE 랩을 이끈다. 건설 로봇을 제조업과 가르는 구조적 사실에 이름을 붙였다: **역전된 공간 관계(reversed spatial relationship)** — 고정된 로봇에 지그로 고정된 제품이 오는 것이 아니라, 매니퓰레이터가 크고 정적인 구조물로 이동해 정합해야 한다.

**방법**: 워크플로는 네 단계를 잇는다 — (1) 설계 모델이 목표 기하를 지정한다; (2) 모바일 플랫폼이 피두셜 마커 기반 비전 계측으로 작업면에서 위치를 정합해, 공장식 지그 없이 로봇-작업물 변환을 복원한다; (3) 비전 유도 조작이 준비된 부품을 목표 기하에 맞춰 배치한다; (4) 같은 센싱이 조립 결과를 as-built 모델로 스캔해 설계 의도와 비교할 수 있게 한다. 모든 단계가 2015년대의 고전 비전 — 인쇄된 피두셜 마커, 캘리브레이션된 카메라 — 이며 학습 기반 인식이 아니다.

**증거**: 시연은 실제 하드웨어에서 준비된 부품으로 전체 루프 — 모바일 정합, 자율 부품 배치, as-built 스캔 — 를 실행하는 물리적 모바일 매니퓰레이터 조립 셀이다. 분야가 간직한 기여는 *아키텍처*다: 설계 → 이동 정합 → 조작 → as-built 검증 사이클의 최초 완결 사례이며, 이후 미시간 연구(그리고 오늘날의 [[01-canonical-papers/notes/8-construction/bim-digital-twin|BIM 기반 디지털 트윈 워크플로]])가 이를 정교화한다.

**한계**: 마커 기반 계측과 준비된 부품은 현장 불확실성 대부분을 의도적으로 제거한다 — 이 논문이 푸는 것은 정합과 루프 닫기이지, 어수선한 환경에서의 인식이 아니다. 부품 다양성, 부품이 맞지 않을 때의 공차 복구, 마커 없는 정합은 모두 후속 연구의 몫이다(Lundeen 2019가 as-built 기하 적응을 직접 다룬다).

> [!question] 핵심 주장 읽는 법
> 여기서 "자율 로봇 조립"은 마커가 설치되고 부품이 준비된 워크플로 안에서의 자율을 뜻한다. 이 논문은 기초적 통합 루프 — 모바일 건설 매니퓰레이터에서 최초의 완결된 설계→시공→검증 사이클 — 로 읽어야지, 2015년에 비정형 현장 조립이 풀렸다는 증거로 읽으면 안 된다. 피두셜 마커가 하중을 받는 가정이다: 이 계보의 이후 논문들은 각각 그 가정 하나씩을 제거하는 것으로 읽을 수 있다.

### 연결

- 다음: [[01-canonical-papers/notes/8-construction/lundeen-2019|Lundeen 2019]] (기하 적응) · [[01-canonical-papers/notes/8-construction/liang-lfd|Liang LfD]] (시연 학습)
- 스트림: [[05-construction-robotics/assembly-fabrication|조립·패브리케이션 스트림]] · [[05-construction-robotics/site-perception|현장 인식]]
- 계보: [[05-construction-robotics/lineage|건설로봇 계보]] (Kamat/Menassa → Feng(NYU AI4CE)·Yu(VT)·Liang(Stony Brook))

### 읽고 나면 말할 수 있어야 하는 것 · After reading (★)

- [ ] 설계 → 모바일 정합 → 비전 유도 조작 → as-built 스캔의 4단계 루프를 재구성하고, 각 단계에서 어떤 변환/모델이 추정되는지 말할 수 있다
- [ ] 제조와 건설의 reversed spatial relationship이 무엇이고, 왜 이것이 고정 셀 로봇 공학의 가정을 무너뜨리는지 설명할 수 있다
- [ ] 피두셜 마커 기반 계측이 자율성 주장에 어떤 조건을 다는지, 그리고 마커가 제거하는 불확실성이 정확히 무엇인지 말할 수 있다
- [ ] 이 논문이 미시간 계보(Lundeen, Liang, Yu)와 오늘날 BIM 디지털 트윈 워크플로의 출발점인 이유를 계보 위에서 설명할 수 있다
