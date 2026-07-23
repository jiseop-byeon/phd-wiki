---
title: 2. Labs Map
tags: [reference, construction]
---

## English

Who does construction robotics research, and what each group is known for. Links,
affiliations, and advisor genealogy verified as of 2026-07 (web survey of lab pages,
dissertations, and publication records).
(For companies see the [[05-construction-robotics/industry-deployment|industry & deployment map]];
for how these groups' work fits the field's history, see [[05-construction-robotics/lineage|the lineage page]].)

### The Michigan hub

One structural fact organizes the US map: **the University of Michigan CEE cluster is the
field's faculty-producing engine.** Eight of its PhD alumni now run their own
construction-robotics or robot-perception labs, and its two internal groups anchor two
complementary research programs.

| Lab / group | PI | Known for |
|---|---|---|
| [LIVE Lab](https://live.engin.umich.edu) + SICIS, Univ. of Michigan CEE | Vineet Kamat · Carol Menassa | the canonical manipulation-for-construction progression: vision-guided assembly (2015) → adaptive autonomy → learning-from-demonstration → closed-loop BIM digital twins → tactile handover → language-instructable robots |
| [DPM Lab](https://dpm.engin.umich.edu), Univ. of Michigan CEE | SangHyun Lee | worker-centered automation: EEG/EDA wearable biosensing, ergonomics vision, and feeding worker physiological state back into human-robot team control |

**Verified academic descendants running their own labs:**

| Descendant | Advisor(s) | Now at | Direction |
|---|---|---|---|
| Chen Feng | Kamat | [AI4CE Lab](https://ai4ce.github.io/), NYU Tandon | the strongest robot-learning lab natively in a civil-engineering orbit — DeepMapping, collaborative perception, NSF CAREER on construction-site robot navigation |
| Houtan Jebelli | S. Lee | [RAISE Lab](https://raiselab.cee.illinois.edu/), UIUC CEE | physiological computing → robot control: BCI teleoperation, intention-aware motion planning, legged/aerial inspection robots |
| Daeho Kim | S. Lee | [Construction Vision Lab](https://cvl.civmin.utoronto.ca/), Univ. of Toronto | co-robotic vision safety, synthetic training data (BlendCon) |
| Francis Baek | S. Lee | [HARMONIC Lab](https://harmoniclab.ce.gatech.edu/), Georgia Tech CEE | nervous-system-based HRC (EEG/wearables in the robot loop); new line: LMM agents on quadrupeds |
| Hongrui Yu | Kamat · Menassa | [Virginia Tech CEE](https://mlsoc.vt.edu/about/faculty-and-staff/hongrui-yu.html) | cloud-based imitation learning of construction skills, tactile handover |
| Ci-Jyun Liang | Kamat · Menassa | [CROSS Lab](https://you.stonybrook.edu/crosslab/), Stony Brook | learning-from-demonstration, robot pose estimation, XR safety |
| Xi Wang | Menassa · Kamat | [XIC Lab](https://www.xiclab.org/), Texas A&M | process-level digital twins as the HRC interface; multi-robot supervision |
| Somin Park | Kamat · Menassa | UT Arlington | natural-language / LLM+VR interfaces for worker-robot communication |

(Jebelli's own students continue the tree: Yizhi Liu → Syracuse — NSF-funded flying+legged
roof-inspection robots; Shayan Shayesteh → Appalachian State; M. Habibnezhad → LSU, postdoc edge.)

### Other US groups

| Lab / group | PI | Known for |
|---|---|---|
| [RICAL](https://rical.ce.gatech.edu/index.html), Georgia Tech CEE | Yong K. Cho | the cluster's most field-deployed autonomous mobile robots: SLAM-driven site scanning (2018), UAV+UGV teams, adaptive view planning, socially-aware navigation among workers; descendants at Mississippi State, UNLV, Monash |
| [RAAMAC](https://raamac.cee.illinois.edu), UIUC CEE | Mani Golparvar-Fard | computer-vision progress monitoring from site photos/BIM; spun out **Reconstruct Inc.**; descendants: Kevin Han (NC State — mobile robotic welding), Jacob Lin (NTU), Youngjib Ham (TAMU → SNU 2024) |
| [CARL](https://ccee.ncsu.edu/han/), NC State CCEE | Kevin Han | vision-based mobile robotic welding (UGV + arm, autonomous + HRI modes) |
| [SWARM](https://www.cmu.edu/cee/people/faculty/tang.html), CMU CEE | Pingbo Tang | spatiotemporal sensing & human-cyber-physical systems; Akinci's PhD student — the CMU sensing school |
| CMU CEE ([profile](https://www.cmu.edu/cee/people/faculty/akinci.html)) | Burcu Akinci | BIM + 3D imaging/sensing for facility histories; led a 2020–21 NSF *planning grant* for a National Institute for AI in Construction (institute itself not launched); **Dean of CMU Engineering from 2026-01**; CMU context: Fujitsu–CMU Physical AI Research Center opened 2026-04 |
| Univ. of Florida | Jing "Eric" Du | haptics-based robot teleoperation, human-robot shared perception, VR/AR HRC |
| Oregon State (CoRIS) | Joseph Louis | construction teleoperation and earthmoving-operations simulation |
| USC (legacy) | Behrokh Khoshnevis | **Contour Crafting** — the origin of construction 3D printing |
| UT Austin (adjacent groups) | Luis Sentis (HCRL), Mitch Pryor (NRG) | humanoid/whole-body control and field robotics — the robotics-side neighbors of a construction program |

Note: **CMU and UC Berkeley have no manipulation-focused construction-robotics lab in
civil engineering** — CMU CEE's strength is construction *sensing/AI* (Tang, Akinci), and
Berkeley's physical-AI strength sits entirely outside CEE (below). The robotics-side
excavation lineage at CMU (Stentz/Singh, 1990s) lives in the
[[05-construction-robotics/lineage|lineage page]].

### Europe

| Lab | PI | Known for |
|---|---|---|
| [Robotic Systems Lab](https://rsl.ethz.ch/), ETH Zurich | Marco Hutter | **the HEAP autonomous excavation line** — force-based digging (2017) → trenching → HEAP (2021) → sim-to-real RL hydraulics → the [6 m autonomous dry-stone wall](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html) (Science Robotics 2023) → ExT multitask pretraining (2025); spun out **Gravis Robotics** (Johns CEO, Jud CTO) |
| [Gramazio Kohler Research](https://gramaziokohler.arch.ethz.ch/), ETH Zurich | Fabio Gramazio · Matthias Kohler | robotic fabrication in architecture (In situ Fabricator, Mesh Mould, DFAB HOUSE, Semiramis); NCCR Digital Fabrication; the field's densest faculty tree: Dörfler → TUM, Parascho → EPFL, Hack → TU Braunschweig, Lloret-Fritschi → USI |
| [Professorship of Digital Fabrication](https://www.arc.ed.tum.de/en/df/professorship/), TUM | Kathrin Dörfler | collaborative on-site fabrication, AR-mediated timber assembly, mobile robots (GKR alumna); TUM's current center of gravity — Thomas Bock (STCR taxonomy, the field's standard reference books) emeritus since 2023 |
| [CRCL](https://www.crclcrclcrcl.org/), EPFL | Stefana Parascho | cooperative multi-robot assembly of full-scale structures (LightVault); GKR → Princeton → EPFL |
| [ICD](https://www.icd.uni-stuttgart.de/) + IntCDC, Univ. of Stuttgart | Achim Menges · Jan Knippers | the other German heavyweight: robotic timber/fiber fabrication pavilions, cyber-physical prefab (Cluster of Excellence IntCDC) |
| ITE, TU Braunschweig | Norman Hack | shotcrete 3D printing at structural scale (DFG TRR 277 Additive Manufacturing in Construction); GKR alumnus |
| UMIT/[Algoryx](https://www.algoryx.se/), Umeå Univ. | Martin Servin | RL + world models for autonomous wheel loaders with Komatsu/Epiroc — the Nordic counterpart to RSL's earthmoving-learning line |
| Imperial/UCL consortium | Mirko Kovac · Robert Stuart-Smith | **aerial additive manufacturing** — drones 3D-printing in flight (Nature 2022) |

### Asia

| Lab | PI | Known for |
|---|---|---|
| [IRiS Lab](https://iris.kaist.ac.kr/), KAIST CEE | Jee-Hwan Ryu | telerobotics + construction robotics (RA-L 2024 Best Paper); the Korean anchor of the ICRA construction-robotics community |
| [Construction API Lab](https://www.con-api.team/), National Taiwan Univ. | Jacob J. Lin | vision+BIM production monitoring moving into robot handover (Golparvar-Fard alumnus, Reconstruct co-founder) |
| SNU CEE | Youngjib Ham (2024–) · Changbum Ahn | vision/thermography diagnostics; wearable sensing (the Korean branch of the UIUC/UMich trees) |

### Manufacturing robotics (adjacent departments)

Construction's closest methodological sibling — structured-but-variable physical work.
These groups publish the manipulation/HRC methods construction researchers import:

| Lab | PI | Known for |
|---|---|---|
| [Manufacturing Futures Institute](https://engineering.cmu.edu/mfi/) + Robotics Institute, CMU | (multi-PI; Changliu Liu's safe-control/intent-prediction line most transferable) | AI for advanced manufacturing; the robotics muscle behind CMU's construction-AI push |
| [AUTOLab](https://autolab.berkeley.edu), UC Berkeley (IEOR/EECS) | Ken Goldberg | robust grasping & manipulation for warehouses/industrial automation |
| [BAIR](https://bair.berkeley.edu), UC Berkeley | Levine, Abbeel, et al. | the robot-learning engine room — [[01-canonical-papers/notes/4-vla/octo\|Octo]], much of the VLA lineage in this wiki |
| [Interactive Robotics Group](https://interactive.mit.edu), MIT | Julie Shah | human-robot teaming for manufacturing assembly — cross-training, human-aware motion planning; the HRC playbook construction borrows |

### How to use this map

- **Paper triage**: an unfamiliar paper usually traces to one of these clusters — the
  cluster tells you its assumptions (manipulation-LfD vs worker-sensing vs heavy-machine
  autonomy vs CV-monitoring vs fabrication).
- **Genealogy triage**: a surprising number of US papers trace to two intermarried family
  trees (UMich: Kamat/Menassa + S. Lee; UIUC: Golparvar-Fard) — knowing the tree predicts
  the methods and evaluation style.
- **Venue watch**: Automation in Construction, J. Computing in Civil Engineering, ISARC,
  and increasingly ICRA/IROS/Science Robotics.
- **For this wiki's direction**: ETH RSL defines the heavy-machine-learning frontier; the
  Michigan cluster defines the manipulation/HRC progression; BAIR/MIT-Shah supply learning
  and HRC methods; RAAMAC/RICAL define the perception baseline.

## 한국어

건설로봇 연구를 누가 하고, 각 그룹이 무엇으로 알려져 있는가. 링크·소속·**사제 계보**는
2026-07 기준으로 검증했다 (랩 페이지, 학위논문, 출판 기록 웹 조사).
(기업은 [[05-construction-robotics/industry-deployment|산업·배치 지도]], 이 그룹들의 작업이
분야 역사에서 어디에 놓이는지는 [[05-construction-robotics/lineage|계보 페이지]] 참고.)

### 미시간 허브

미국 지도를 조직하는 구조적 사실 하나: **미시간대 CEE 클러스터가 이 분야의 교수 배출
엔진이다.** 박사 졸업생 8명이 자기 건설로봇/로봇인식 랩을 운영하고, 내부의 두 그룹이
상호보완적인 두 연구 프로그램을 이끈다.

| 랩 / 그룹 | PI | 대표 분야 |
|---|---|---|
| [LIVE Lab](https://live.engin.umich.edu) + SICIS, 미시간대 CEE | Vineet Kamat · Carol Menassa | 건설 조작의 정전(正典)적 진행: 비전 유도 조립(2015) → 적응적 자율성 → 시연 학습 → 폐루프 BIM 디지털 트윈 → 촉각 전달 → 언어 지시 로봇 |
| [DPM Lab](https://dpm.engin.umich.edu), 미시간대 CEE | SangHyun Lee | 작업자 중심 자동화: EEG/EDA 웨어러블 바이오센싱, 인간공학 비전, 작업자 생리 상태를 인간-로봇 팀 제어에 피드백 |

**검증된 학술 계보 (자기 랩을 운영하는 제자들):**

| 제자 | 지도교수 | 현 소속 | 방향 |
|---|---|---|---|
| Chen Feng | Kamat | [AI4CE Lab](https://ai4ce.github.io/), NYU Tandon | 토목 궤도에서 가장 강한 로봇러닝 랩 — DeepMapping, 협력 인식, 건설 현장 로봇 항법 NSF CAREER |
| Houtan Jebelli | S. Lee | [RAISE Lab](https://raiselab.cee.illinois.edu/), UIUC CEE | 생리 신호 컴퓨팅 → 로봇 제어: BCI 원격조작, 의도 인식 모션 계획, 보행/비행 점검 로봇 |
| Daeho Kim | S. Lee | [Construction Vision Lab](https://cvl.civmin.utoronto.ca/), 토론토대 | 협동 로봇 비전 안전, 합성 학습 데이터(BlendCon) |
| Francis Baek | S. Lee | [HARMONIC Lab](https://harmoniclab.ce.gatech.edu/), Georgia Tech CEE | 신경계 기반 HRC (EEG/웨어러블을 로봇 루프에); 신규: 사족보행 로봇 위의 LMM 에이전트 |
| Hongrui Yu | Kamat · Menassa | [Virginia Tech CEE](https://mlsoc.vt.edu/about/faculty-and-staff/hongrui-yu.html) | 건설 기능의 클라우드 모방학습, 촉각 전달 |
| Ci-Jyun Liang | Kamat · Menassa | [CROSS Lab](https://you.stonybrook.edu/crosslab/), Stony Brook | 시연 학습, 로봇 자세 추정, XR 안전 |
| Xi Wang | Menassa · Kamat | [XIC Lab](https://www.xiclab.org/), Texas A&M | HRC 인터페이스로서의 공정 수준 디지털 트윈; 멀티로봇 감독 |
| Somin Park | Kamat · Menassa | UT Arlington | 작업자-로봇 소통을 위한 자연어/LLM+VR 인터페이스 |

(Jebelli의 제자들이 나무를 잇는다: Yizhi Liu → Syracuse — NSF 지원 비행+보행 지붕 점검
로봇; Shayan Shayesteh → Appalachian State; M. Habibnezhad → LSU, 포스닥 관계.)

### 그 외 미국 그룹

| 랩 / 그룹 | PI | 대표 분야 |
|---|---|---|
| [RICAL](https://rical.ce.gatech.edu/index.html), Georgia Tech CEE | Yong K. Cho | 클러스터에서 가장 현장 배치가 많은 자율 이동 로봇: SLAM 기반 현장 스캔(2018), UAV+UGV 팀, 적응적 뷰 계획, 작업자 사이의 사회적 항법; 제자들이 Mississippi State·UNLV·Monash에 |
| [RAAMAC](https://raamac.cee.illinois.edu), UIUC CEE | Mani Golparvar-Fard | 현장 사진/BIM 기반 CV 공정 모니터링; **Reconstruct Inc.** 창업; 제자: Kevin Han(NC State — 이동 로봇 용접), Jacob Lin(NTU), Youngjib Ham(TAMU → 2024 서울대) |
| [CARL](https://ccee.ncsu.edu/han/), NC State CCEE | Kevin Han | 비전 기반 이동 로봇 용접 (UGV+팔, 자율+HRI 모드) |
| [SWARM](https://www.cmu.edu/cee/people/faculty/tang.html), CMU CEE | Pingbo Tang | 시공간 센싱과 인간-사이버-물리 시스템; Akinci의 제자 — CMU 센싱 학파 |
| CMU CEE ([프로필](https://www.cmu.edu/cee/people/faculty/akinci.html)) | Burcu Akinci | BIM + 3D 이미징/센싱; 건설 AI 국가 연구소는 2020–21 NSF *기획 과제*였고 연구소 자체는 미설립; **2026년 1월부터 CMU 공대 학장**; CMU 맥락: Fujitsu–CMU Physical AI Research Center 2026-04 출범 |
| 플로리다대 | Jing "Eric" Du | 햅틱 기반 로봇 원격조작, 인간-로봇 공유 인식, VR/AR HRC |
| Oregon State (CoRIS) | Joseph Louis | 건설 원격조작과 토공 작업 시뮬레이션 |
| USC (유산) | Behrokh Khoshnevis | **Contour Crafting** — 건설 3D 프린팅의 기원 |
| UT Austin (인접 그룹) | Luis Sentis (HCRL), Mitch Pryor (NRG) | 휴머노이드/전신 제어와 필드 로보틱스 |

참고: **CMU와 UC 버클리의 토목공학과에는 조작 중심의 건설로봇 랩이 없다** — CMU 토목의
강점은 건설 *센싱/AI*(Tang, Akinci)이고, 버클리의 physical AI 역량은 전부 토목 밖에
있다(아래). CMU의 로보틱스 쪽 굴착 계보(Stentz/Singh, 1990년대)는
[[05-construction-robotics/lineage|계보 페이지]]에 있다.

### 유럽

| 랩 | PI | 대표 분야 |
|---|---|---|
| [Robotic Systems Lab](https://rsl.ethz.ch/), ETH 취리히 | Marco Hutter | **HEAP 자율 굴착 라인** — 힘 기반 굴착(2017) → 트렌칭 → HEAP(2021) → sim-to-real RL 유압 → [6m 자율 돌담](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)(Science Robotics 2023) → ExT 멀티태스크 사전학습(2025); **Gravis Robotics** 스핀아웃 (Johns CEO, Jud CTO) |
| [Gramazio Kohler Research](https://gramaziokohler.arch.ethz.ch/), ETH 취리히 | Fabio Gramazio · Matthias Kohler | 건축 로봇 패브리케이션 (In situ Fabricator, Mesh Mould, DFAB HOUSE, Semiramis); NCCR Digital Fabrication; 분야에서 가장 조밀한 교수 계보: Dörfler → TUM, Parascho → EPFL, Hack → TU Braunschweig, Lloret-Fritschi → USI |
| [Professorship of Digital Fabrication](https://www.arc.ed.tum.de/en/df/professorship/), TUM | Kathrin Dörfler | 협업 현장 패브리케이션, AR 매개 목조 조립, 모바일 로봇 (GKR 출신); TUM의 현재 중심 — Thomas Bock(STCR 분류, 표준 참고서)은 2023년 은퇴 |
| [CRCL](https://www.crclcrclcrcl.org/), EPFL | Stefana Parascho | 실규모 구조물의 협력 멀티로봇 조립 (LightVault); GKR → Princeton → EPFL |
| [ICD](https://www.icd.uni-stuttgart.de/) + IntCDC, 슈투트가르트대 | Achim Menges · Jan Knippers | 독일의 다른 한 축: 로봇 목조/섬유 파빌리온, 사이버-물리 프리팹 (IntCDC 엑설런스 클러스터) |
| ITE, TU Braunschweig | Norman Hack | 구조 스케일 숏크리트 3D 프린팅 (DFG TRR 277); GKR 출신 |
| UMIT/[Algoryx](https://www.algoryx.se/), 우메오대 | Martin Servin | Komatsu/Epiroc와 자율 휠로더 RL·월드모델 — RSL 토공 학습 라인의 북유럽 대응물 |
| Imperial/UCL 컨소시엄 | Mirko Kovac · Robert Stuart-Smith | **공중 적층 제조** — 비행 중 3D 프린팅하는 드론 (Nature 2022) |

### 아시아

| 랩 | PI | 대표 분야 |
|---|---|---|
| [IRiS Lab](https://iris.kaist.ac.kr/), KAIST 건설환경 | 류지환 | 텔레로보틱스 + 건설로봇 (RA-L 2024 Best Paper); ICRA 건설로봇 커뮤니티의 한국 앵커 |
| [Construction API Lab](https://www.con-api.team/), 국립대만대 | Jacob J. Lin | 비전+BIM 생산 모니터링에서 로봇 전달로 확장 중 (Golparvar-Fard 출신, Reconstruct 공동창업) |
| 서울대 건설환경 | Youngjib Ham (2024–) · Changbum Ahn | 비전/열화상 진단; 웨어러블 센싱 (UIUC/UMich 나무의 한국 가지) |

### 제조 로봇 (타 학과)

건설의 가장 가까운 방법론적 형제 — 구조화되어 있지만 변동이 있는 물리 작업.
건설 연구자들이 수입해 쓰는 조작/HRC 기법이 이 그룹들에서 나온다:

| 랩 | PI | 대표 분야 |
|---|---|---|
| [Manufacturing Futures Institute](https://engineering.cmu.edu/mfi/) + Robotics Institute, CMU | (복수 PI; Changliu Liu의 안전 제어/의도 예측 라인이 가장 이전 가능) | 첨단 제조 AI; CMU 건설 AI 추진의 로보틱스 근육 |
| [AUTOLab](https://autolab.berkeley.edu), UC 버클리 (IEOR/EECS) | Ken Goldberg | 창고/산업 자동화를 위한 강건한 파지와 조작 |
| [BAIR](https://bair.berkeley.edu), UC 버클리 | Levine, Abbeel 등 | 로봇 학습의 엔진룸 — [[01-canonical-papers/notes/4-vla/octo\|Octo]] 등 이 위키 VLA 계보의 산실 |
| [Interactive Robotics Group](https://interactive.mit.edu), MIT | Julie Shah | 제조 조립의 인간-로봇 팀워크 — 교차 훈련, 인간 인지 모션 계획; 건설이 빌려 쓰는 HRC 플레이북 |

### 이 지도를 쓰는 법

- **논문 분류**: 낯선 논문은 대개 이 클러스터 중 하나로 거슬러 올라간다 — 클러스터가 그
  논문의 가정(조작-LfD vs 작업자 센싱 vs 중장비 자율성 vs CV 모니터링 vs 패브리케이션)을
  알려준다.
- **계보 분류**: 놀랄 만큼 많은 미국 논문이 서로 얽힌 두 그루의 가계도(미시간:
  Kamat/Menassa + S. Lee; UIUC: Golparvar-Fard)로 거슬러 올라간다 — 나무를 알면 방법론과
  평가 스타일이 예측된다.
- **학회 감시**: Automation in Construction, J. Computing in Civil Engineering, ISARC,
  그리고 점점 ICRA/IROS/Science Robotics.
- **이 위키의 방향에서**: ETH RSL이 중장비 학습의 최전선을, 미시간 클러스터가 조작/HRC
  진행을 정의한다; BAIR/MIT-Shah가 학습·HRC 기법을 공급하고, RAAMAC/RICAL이 인식
  베이스라인을 정의한다.
