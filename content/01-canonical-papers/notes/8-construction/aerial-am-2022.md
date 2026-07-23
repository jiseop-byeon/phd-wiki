---
title: "Aerial Additive Manufacturing with Multiple Autonomous Robots (Zhang et al., 2022)"
authors: Zhang et al. (Mirko Kovac & Robert Stuart-Smith consortium)
affiliation: Imperial College London, UCL, Empa, University of Bath
venue: Nature
year: 2022
pdf: https://www.nature.com/articles/s41586-022-04988-4
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-24
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Zhang et al., Nature 2022** — [Nature (open link)](https://www.nature.com/articles/s41586-022-04988-4)

## English

**One-line summary**: A team of drones 3D-prints *during flight* — BuilDrones deposit material while ScanDrones measure print quality — a wasp-inspired multi-robot framework that reached Nature by demonstrating manufacturing in a regime (unbounded, at-height, hard-to-access) where ground robots cannot go.

**Lineage position**: the aerial outlier in the [[05-construction-robotics/assembly-fabrication|assembly-fabrication stream]] — where gantry and arm-based construction printing scale by machine size, Aerial-AM scales by *population*: the framework adapts robot tasks and team size to the print geometry during a mission. Method (literacy level): a multi-robot printing and path-planning framework runs autonomous printing under human supervision; a generic model-predictive-control scheme flies the printing trajectories; a dynamically self-aligning delta manipulator on the BuilDrone cancels airframe motion at the nozzle.

**Evidence with numbers**: the delta manipulator brings manufacturing accuracy to **5 mm**; proof-of-concept prints include a **2.05 m** cylinder of **72 layers** of rapid-curing insulation foam and a **0.18 m** cylinder of **28 layers** of structural pseudoplastic cementitious material; **four** cementitious–polymeric composite mixtures were developed for continuous deposition in flight; plus a light-trail virtual print of a dome-like geometry and multi-robot simulations.

**Limitations**: lab-scale demonstrations, not a construction site; payload and deposition rate per drone are far from structural construction throughput; autonomy runs *under human supervision*; 5 mm accuracy holds for geometry with precise trajectory requirements, not arbitrary structures. Read it as an existence proof for in-flight manufacturing, not a near-term site technology.

## 한국어

**한 줄 요약**: 드론 팀이 *비행 중에* 3D 프린팅을 한다 — BuilDrone이 재료를 적층하는 동안 ScanDrone이 인쇄 품질을 측정한다 — 지상 로봇이 갈 수 없는 영역(무한 작업 공간, 고소, 접근 곤란 지점)에서의 제조를 실증해 Nature에 오른, 말벌에서 영감을 받은 멀티로봇 프레임워크다.

**계보에서의 위치**: [[05-construction-robotics/assembly-fabrication|조립·시공 스트림]]의 공중 이단아 — 갠트리·팔 기반 건설 프린팅이 기계 크기로 스케일할 때, Aerial-AM은 *개체 수*로 스케일한다: 프레임워크가 임무 중 인쇄 기하에 맞춰 로봇 과제와 팀 규모를 조정한다. 방법 (리터러시 수준): 멀티로봇 프린팅·경로 계획 프레임워크가 인간 감독 하에 자율 프린팅을 수행한다; 범용 모델 예측 제어(MPC) 방식이 프린팅 궤적을 비행한다; BuilDrone의 동적 자가 정렬 델타 매니퓰레이터가 노즐에서 기체 흔들림을 상쇄한다.

**수치가 있는 증거**: 델타 매니퓰레이터가 제조 정확도를 **5 mm**까지 끌어올린다; 개념 증명 인쇄물로 속경화 단열 폼 **72개 층**의 **2.05 m** 원통과 구조용 의소성 시멘트계 재료 **28개 층**의 **0.18 m** 원통이 있다; 비행 중 연속 적층에 적합한 시멘트-폴리머 복합 배합 **4종**을 개발했다; 돔형 기하의 라이트 트레일 가상 인쇄와 멀티로봇 시뮬레이션도 있다.

**한계**: 실험실 규모 실증이지, 건설 현장이 아니다; 드론당 페이로드와 적층 속도는 구조체 시공 처리량과 거리가 멀다; 자율성은 *인간 감독 하*에서 운용된다; 5 mm 정확도는 정밀 궤적 요건이 있는 기하에서 성립하는 것이지, 임의 구조물이 아니다. 비행 중 제조의 존재 증명으로 읽어야지, 가까운 시일의 현장 기술로 읽으면 안 된다.

### 연결

- 스트림: [[05-construction-robotics/assembly-fabrication|4. 조립·시공 스트림]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] BuilDrone/ScanDrone 분업과 "개체 수로 스케일한다"는 프레임워크의 핵심을 말할 수 있다
- [ ] 델타 매니퓰레이터가 왜 필요했고 5 mm 정확도가 어떤 조건의 수치인지 말할 수 있다
- [ ] 실험실 규모 존재 증명과 현장 기술 사이의 간극(페이로드, 처리량, 감독)을 지적할 수 있다
