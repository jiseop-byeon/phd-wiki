---
title: "SLAM-Driven Robotic Mapping and Registration of 3D Point Clouds (Kim, Chen & Cho, 2018)"
authors: Pileun Kim, Jingdao Chen, Yong K. Cho
affiliation: Georgia Tech, Robotic Intelligent Construction Automation Lab (RICAL)
venue: Automation in Construction
year: 2018
doi: https://doi.org/10.1016/j.autcon.2018.01.009
project: https://rical.ce.gatech.edu/
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-24
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Kim, Chen & Cho, Automation in Construction 2018** — [DOI](https://doi.org/10.1016/j.autcon.2018.01.009) (paywalled) · [Lab](https://rical.ce.gatech.edu/)

## English

**One-line summary**: Robotics SLAM arrives on the construction-informatics side — a ground robot navigates a construction environment on its own, uses SLAM poses as the initial alignment, and automatically registers its laser scans into one site point cloud, removing the manual station setup and target placement of conventional laser scanning.

**Lineage position**: the moment the robotics literature's mapping stack (odometry, scan matching, registration) crosses into *Automation in Construction* — giving the scan-to-BIM pipeline an autonomous mobile front end. The line continues in the same group: a 2019 UAV+UGV cooperative mapping extension (Automation in Construction 106) and a 2025 adaptive view-planning system (JCCE 40) that is field-deployed.

**Method** (literacy level): a mobile robot carries a laser scanner; SLAM estimates the robot's pose as it drives between scan positions; those pose estimates serve as coarse initial transforms so that fine registration can lock consecutive dense scans into a common coordinate frame automatically. The contrast class is the surveyor's workflow — tripod stations, artificial targets, and manual registration in post-processing.

**Evidence**: demonstrated on a physical robot scanning construction-like indoor/outdoor environments — a testbed-scale validation that the SLAM-initialized registration pipeline produces a usable unified point cloud without human registration effort. Full-text numbers sit behind the Elsevier paywall (stated openly here); the strongest deployment evidence in this line belongs to the 2025 continuation, which reached real sites.

**Limitations**: 2018-era testbed environments, not active production sites; autonomy covers navigation-and-scanning, while scan planning (where to scan next) only becomes adaptive in the later work; drift and registration quality depend on environment geometry; the note's claims about exact accuracy are deliberately withheld because the paper is paywalled.

**Reading the claim**: "SLAM-driven" means SLAM supplies the *initialization* for registration — the map quality still rests on fine registration, not on SLAM alone. And keep the evidence ledger straight: the 2018 paper proves the pipeline on testbeds; field deployment is the 2025 descendant's evidence, not this paper's.

## 한국어

**한 줄 요약**: 로보틱스의 SLAM이 건설 정보학 쪽에 도착했다 — 지상 로봇이 건설 환경을 스스로 주행하고, SLAM 자세를 초기 정렬로 사용해 레이저 스캔들을 하나의 현장 포인트 클라우드로 자동 정합한다. 재래식 레이저 스캐닝의 수동 스테이션 설치와 타깃 배치를 제거한 것이다.

**계보에서의 위치**: 로보틱스 문헌의 매핑 스택(오도메트리, 스캔 매칭, 정합)이 *Automation in Construction*으로 건너온 순간 — scan-to-BIM 파이프라인에 자율 이동 앞단을 달아 준다. 같은 그룹에서 계보가 이어진다: 2019년 UAV+UGV 협력 매핑 확장(Automation in Construction 106), 그리고 실제 현장에 배치된 2025년 적응형 뷰 플래닝 시스템(JCCE 40).

**방법** (리터러시 수준): 이동 로봇이 레이저 스캐너를 싣고 다닌다; 스캔 위치 사이를 주행하는 동안 SLAM이 로봇 자세를 추정한다; 그 자세 추정값이 거친 초기 변환이 되어, 정밀 정합이 연속된 고밀도 스캔들을 공통 좌표계에 자동으로 고정할 수 있게 한다. 비교 대상은 측량사의 워크플로 — 삼각대 스테이션, 인공 타깃, 후처리에서의 수동 정합이다.

**증거**: 건설 유사 실내/실외 환경을 스캔하는 실물 로봇으로 실증했다 — SLAM 초기화 정합 파이프라인이 사람의 정합 작업 없이 쓸 만한 통합 포인트 클라우드를 만든다는 테스트베드 규모의 검증이다. 본문 수치는 Elsevier 페이월 뒤에 있다(여기 공개적으로 밝혀 둔다); 이 계보에서 가장 강한 배치 증거는 실제 현장까지 간 2025년 후속의 것이다.

**한계**: 2018년 시점의 테스트베드 환경이지, 가동 중인 생산 현장이 아니다; 자율성은 주행-및-스캔을 다루고, 스캔 계획(다음에 어디를 스캔할지)은 후속 연구에서야 적응형이 된다; 드리프트와 정합 품질은 환경 기하에 의존한다; 정확도 수치에 대한 주장은 논문이 페이월이라 의도적으로 비워 두었다.

**주장 읽는 법**: "SLAM-driven"은 SLAM이 정합의 *초기화*를 공급한다는 뜻이다 — 지도 품질은 여전히 SLAM 단독이 아니라 정밀 정합에 달려 있다. 그리고 증거 장부를 똑바로 두라: 2018년 논문은 테스트베드에서 파이프라인을 증명했고, 현장 배치는 이 논문이 아니라 2025년 후손의 증거다.

### 연결

- 스트림: [[05-construction-robotics/site-perception|5. 현장 인식·Scan-to-BIM 스트림]]
- 기초: [[04-robotics/state-estimation-slam|3. State Estimation]] · [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] SLAM 자세 추정이 정밀 정합의 초기값으로 쓰이는 파이프라인 구조를 말할 수 있다
- [ ] 재래식 스테이션 스캐닝 대비 무엇이 자동화되었는지(스테이션 설치·타깃·수동 정합) 말할 수 있다
- [ ] 2018 테스트베드 증거와 2019/2025 후속(UAV+UGV, 현장 배치 뷰 플래닝)의 증거 수준을 구분할 수 있다
- [ ] scan-to-BIM 파이프라인에서 이 논문이 차지하는 앞단(데이터 수집 자동화) 위치를 설명할 수 있다
