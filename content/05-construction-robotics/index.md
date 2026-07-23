---
title: 5. Construction
cssclasses: [curated-folder-index]
study-depth: Literacy
depth-goal: "Explain the domain landscape, research lineage, actors, and deployment constraints."
mastery-when: "Raise the chosen construction task and system layer to Working or Mastery."
---

## English

Map of content for construction (and adjacent manufacturing) robotics — the lab's core
domain. The literature spans four disciplines, so it is scattered across their venues:

- **Civil engineering**: Automation in Construction, Journal of Computing in Civil Engineering, ISARC
- **Computer science / robotics**: ICRA, IROS, CoRL, RSS, T-RO, RA-L, Science Robotics
- **Mechanical engineering**: field robotics venues, Journal of Field Robotics
- **Electrical engineering**: control and systems venues

Start with the two maps — [[05-construction-robotics/lineage|1. Research Lineage]] (three
genealogies: technical eras, academic family trees, machine evolution) and
[[05-construction-robotics/labs|2. Labs Map]] (who does this research, verified 2026-07) —
then read by stream below. Curated papers live in
[[01-canonical-papers/canonical-list|section 8 of the canonical list]].

### The five research streams

Corpus-derived (2026-07 survey of ~120 papers from the mapped labs), not aspirational:
each stream has enough real published work to be read as a lineage.

1. [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] —
   excavators, wheel loaders, fleets: dynamics, terrain interaction, MPC vs RL vs
   imitation, HEAP/AES/ExT
2. [[05-construction-robotics/assembly-fabrication|4. Robotic Assembly & Fabrication]] —
   manipulation on site (UMich line), architectural fabrication (ETH GKR line), welding,
   bricklaying, 3D printing
3. [[05-construction-robotics/site-perception|5. Site Perception, Scan-to-BIM & Inspection]] —
   LiDAR/point clouds, registration to BIM, autonomous scanning robots, progress
   monitoring, inspection platforms
4. [[05-construction-robotics/hrc-worker-centered|6. HRC & Worker-Centered Robotics]] —
   physiological sensing in the robot loop, intention-aware planning, proximity safety,
   exoskeletons, teleoperation
5. [[05-construction-robotics/digital-twin-workflows|7. Digital Twins & BIM-Driven Workflows]] —
   the interface layer: process-level twins, BIM-to-robot task generation, closed-loop
   execution, task allocation

Cross-cutting layers (not streams — every stream uses them):

- [[05-construction-robotics/sim-to-real|Sim-to-Real for Field Robots]] — reality-gap
  sources, randomization, privileged learning, residuals, and transfer evidence
- [[05-construction-robotics/industry-deployment|8. Industry & Deployment Map]] — who is
  commercializing what, at what autonomy level (verified 2026-07)
- The **reading frame** below — how to evaluate any paper from any stream

### Reading frame for construction-robotics papers

Reading only architecture and benchmarks — the deep-learning habit — cannot evaluate this
field's papers: site conditions and system integration are the substance. Fill in these
axes for every paper:

| Axis | What to ask |
|---|---|
| Task | excavation, assembly, inspection, manipulation — and which step of the real workflow |
| Embodiment | excavator, arm, mobile manipulator, drone — payload and reach |
| Perception | LiDAR, vision, BIM, GNSS — under what conditions (dust, light, vibration) |
| Representation | map, digital twin, task state — what is maintained, how |
| Planning & control | classical (MPC etc.) or learned, at what rate |
| Autonomy & human role | fully autonomous, teleop-assisted — who resets |
| Deployment & safety | lab mockup or real site — what safeguards and assumptions |
| Evaluation realism | how many trials, what weather/site variation, closed-loop? |
| Sim-to-real & scalability | simulation gap, cost per machine/site |
| Failure attribution | where did failures originate (hardware/perception/planning/control) and how were they counted |
| Productivity comparison | was speed/cost compared against humans or existing equipment, or absolute numbers only |

This frame separates "an impressive demo" from "a deployable system." It applies the
[[04-robotics/hri-safety|HRI & safety]], [[04-robotics/robot-systems-deployment|robot systems]],
and [[06-research-practice/failure-analysis-system-evaluation|failure analysis]] pages to
this field's specific literature.

## 한국어

건설(및 인접 제조) 로봇 연구를 정리하는 공간 — 우리 랩의 핵심 연구 분야. 문헌이 네 개
분과에 걸쳐 있어 학회와 저널 곳곳에 흩어져 있다:

- **건설/토목**: Automation in Construction, J. of Computing in Civil Engineering, ISARC
- **컴퓨터과학/로보틱스**: ICRA, IROS, CoRL, RSS, T-RO, RA-L, Science Robotics
- **기계공학**: Journal of Field Robotics 등 필드 로보틱스 계열
- **전기전자**: 제어·시스템 계열

두 개의 지도에서 시작하라 — [[05-construction-robotics/lineage|1. Research Lineage]](세
가지 계보: 기술 시대, 학술 가계도, 기계 진화)와
[[05-construction-robotics/labs|2. Labs Map]](누가 이 연구를 하는가, 2026-07 검증) —
그다음 아래 스트림별로 읽는다. 큐레이션된 논문은
[[01-canonical-papers/canonical-list|핵심 논문 리스트 8번 섹션]]에 있다.

### 다섯 개의 연구 스트림

희망 사항이 아니라 코퍼스에서 도출했다(매핑된 랩들의 논문 ~120편, 2026-07 조사): 각
스트림은 계보로 읽을 수 있을 만큼의 실제 출판물을 갖고 있다.

1. [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] —
   굴착기, 휠로더, 선단: 동역학, 지반 상호작용, MPC vs RL vs 모방, HEAP/AES/ExT
2. [[05-construction-robotics/assembly-fabrication|4. Robotic Assembly & Fabrication]] —
   현장 조작(미시간 라인), 건축 패브리케이션(ETH GKR 라인), 용접, 조적, 3D 프린팅
3. [[05-construction-robotics/site-perception|5. Site Perception, Scan-to-BIM & Inspection]] —
   LiDAR/포인트 클라우드, BIM 정합, 자율 스캔 로봇, 공정 모니터링, 점검 플랫폼
4. [[05-construction-robotics/hrc-worker-centered|6. HRC & Worker-Centered Robotics]] —
   로봇 루프 안의 생리 신호 센싱, 의도 인식 계획, 근접 안전, 외골격, 원격조작
5. [[05-construction-robotics/digital-twin-workflows|7. Digital Twins & BIM-Driven Workflows]] —
   인터페이스 층: 공정 수준 트윈, BIM→로봇 과제 생성, 폐루프 실행, 과제 할당

횡단층 (스트림이 아니라 — 모든 스트림이 사용):

- [[05-construction-robotics/sim-to-real|필드 로봇 Sim-to-Real]] — reality gap, 도메인
  랜덤화, privileged learning, 잔차, 전이 증거
- [[05-construction-robotics/industry-deployment|8. Industry & Deployment Map]] — 누가
  무엇을 어떤 자율성 수준으로 상업화하는가 (2026-07 검증)
- 아래의 **읽기 틀** — 어느 스트림의 논문이든 평가하는 법

### 건설로봇 논문 읽기 틀 · Reading frame

딥러닝 논문처럼 구조와 벤치마크만 읽으면 이 분야 논문은 평가할 수 없다 — 현장 조건과
시스템 통합이 본질이기 때문이다. 논문마다 다음 축을 채워 가며 읽어라:

| 축 | 물어볼 것 |
|---|---|
| 작업 | 굴착·조립·점검·조작 중 무엇이고, 실제 공정의 어느 단계인가 |
| 신체 | 굴착기·팔·모바일 매니퓰레이터·드론 — 페이로드와 도달 범위는 |
| 인식 | LiDAR·비전·BIM·GNSS 중 무엇을 어떤 조건(먼지·조명·진동)에서 |
| 표현 | 지도·디지털 트윈·작업 상태 — 무엇을 어떻게 유지하나 |
| 계획·제어 | 고전(MPC 등)인가 학습인가, 주기는 얼마인가 |
| 자율 수준·인간 개입 | 완전 자율인가, 원격조작 보조인가, 리셋은 누가 하나 |
| 배포 환경·안전 | 실험실 목업인가 실제 현장인가, 안전 장치와 가정은 |
| 평가의 현실성 | 몇 회 시행, 어떤 날씨·현장 변동, 폐루프인가 |
| sim-to-real·확장성 | 시뮬레이션 격차와 기계·현장당 비용은 |
| 실패 분석 | 실패가 하드웨어·인식·계획·제어 중 어디서 났고, 어떻게 집계됐나 |
| 생산성 비교 | 작업 속도·비용이 사람·기존 장비와 비교됐나, 아니면 절대치만 보고했나 |

이 틀로 읽으면 "인상적인 데모"와 "배포 가능한 시스템"이 구분된다. 이 틀은
[[04-robotics/hri-safety|HRI·안전]], [[04-robotics/robot-systems-deployment|로봇 시스템]],
[[06-research-practice/failure-analysis-system-evaluation|실패 분석]] 페이지를 이 분야
문헌에 적용한 것이다.
