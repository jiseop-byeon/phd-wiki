---
title: 2. Labs Map
tags: [reference, construction]
study-depth: Literacy
depth-goal: "Explain the domain landscape, research lineage, actors, and deployment constraints."
mastery-when: "Raise the chosen construction task and system layer to Working or Mastery."
---

## English

Who does construction robotics research, and what each group is known for. Links,
affiliations, and advisor genealogy verified as of 2026-07 (web survey of lab pages,
dissertations, and publication records).
(For companies see the [[05-construction-robotics/industry-deployment|industry & deployment map]];
for how these groups' work fits the field's history, see [[05-construction-robotics/lineage|the lineage page]].)

> [!note] First pass · 처음이라면
> This page is a map. Read the sections on what separates these groups and how to use the map first, then look a group up when its name appears in a paper you are reading.

### The Michigan hub

One structural fact organizes this survey's US map: **the University of Michigan CEE cluster
contains the densest faculty-descendant cluster identified in this wiki's corpus.** Eight of its PhD alumni now run their own
construction-robotics or robot-perception labs, and its two internal groups anchor two
complementary research programs.

| Lab / group | PI | Known for |
|---|---|---|
| [LIVE Lab](https://live.engin.umich.edu) + SICIS, Univ. of Michigan CEE | Vineet Kamat · Carol Menassa | the canonical manipulation-for-construction progression: vision-guided assembly (2015) → adaptive autonomy → learning-from-demonstration → closed-loop BIM digital twins → tactile handover → language-instructable robots |
| [DPM Lab](https://dpm.engin.umich.edu), Univ. of Michigan CEE | SangHyun Lee | worker-centered automation: EEG (brain electrical activity) / EDA (electrodermal activity, i.e. skin conductance) wearable biosensing, ergonomics vision, and feeding worker physiological state back into human-robot team control |

**Verified academic descendants running their own labs:**

| Descendant | Advisor(s) | Now at | Direction |
|---|---|---|---|
| Chen Feng | Kamat | [AI4CE Lab](https://ai4ce.github.io/), NYU Tandon | a group directly overlapping this wiki's civil-engineering robot-learning path — DeepMapping, collaborative perception, NSF CAREER on construction-site robot navigation |
| Houtan Jebelli | S. Lee | [RAISE Lab](https://raiselab.cee.illinois.edu/), UIUC CEE | physiological computing → robot control: BCI (brain–computer interface) teleoperation, intention-aware motion planning, legged/aerial inspection robots |
| Daeho Kim | S. Lee | [Construction Vision Lab](https://cvl.civmin.utoronto.ca/), Univ. of Toronto | co-robotic vision safety, synthetic training data (BlendCon) |
| Francis Baek | S. Lee | [HARMONIC Lab](https://harmoniclab.ce.gatech.edu/), Georgia Tech CEE | nervous-system-based HRC (EEG/wearables in the robot loop); new line: LMM agents on quadrupeds |
| Hongrui Yu | Kamat · Menassa | [Virginia Tech CEE](https://mlsoc.vt.edu/about/faculty-and-staff/hongrui-yu.html) | cloud-based imitation learning of construction skills, tactile handover |
| Ci-Jyun Liang | Kamat · Menassa | [CROSS Lab](https://you.stonybrook.edu/crosslab/), Stony Brook | learning-from-demonstration, robot pose estimation, XR safety |
| Xi Wang | Menassa · Kamat | [XIC Lab](https://www.xiclab.org/), Texas A&M | process-level digital twins as the HRC interface; multi-robot supervision |
| Somin Park | Kamat · Menassa | UT Arlington | natural-language / LLM+VR interfaces for worker-robot communication |

(Jebelli's own students continue the tree: Yizhi Liu → Syracuse — NSF-funded flying+legged
roof-inspection robots; Shayan Shayesteh → Appalachian State; M. Habibnezhad → LSU, postdoc edge — a postdoc-mentorship link, unlike the PhD-advisor links elsewhere in this tree.)

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
| Columbia University (formerly UBC) | Zhengbo Zou | reinforcement and imitation learning for construction-robot control; safety-constrained RL for human–robot collaboration; e.g. Huang et al., *AutCon* 146, 2023, [DOI](https://doi.org/10.1016/j.autcon.2022.104691) |
| USC (legacy) | Behrokh Khoshnevis | **Contour Crafting** — the origin of construction 3D printing |
| UT Austin ME/ARL (adjacent groups) | Luis Sentis (HCRL), Mitch Pryor (NRG) | humanoid/whole-body control and field robotics |
| **UT Austin CS — Texas Robotics** | **Yuke Zhu** ([RPL](https://rpl.cs.utexas.edu/)), **Roberto Martín-Martín** (RobIn Lab) | **manipulation learning — the nearest on-path group to this program.** Both co-authored [[01-canonical-papers/notes/4-vla/robomimic\|robomimic]], whose own affiliation line reads "Stanford, UT Austin, NVIDIA"; Martín-Martín is also on [[01-canonical-papers/notes/4-vla/open-x-embodiment\|Open X-Embodiment]]. Martín-Martín's CS395T *Robot Manipulation and Learning* syllabus and reading list are public |
| UT Austin ECE | Lillian Chin | tactile sensor design and fabrication — adjacent, but sensor *building* is [[04-robotics/tactile-visuotactile\|out of this program's scope]] |

Note: **CMU and UC Berkeley have no manipulation-focused construction-robotics lab in
civil engineering** — CMU CEE's strength is construction *sensing/AI* (Tang, Akinci), and
Berkeley's physical-AI strength sits entirely outside CEE (below). The robotics-side
excavation lineage at CMU (Stentz/Singh, 1990s) lives in the
[[05-construction-robotics/lineage|lineage page]].

### Europe

| Lab | PI | Known for |
|---|---|---|
| [Robotic Systems Lab](https://rsl.ethz.ch/), ETH Zurich | Marco Hutter | **the HEAP autonomous excavation line** — force-based digging (2017) → trenching → HEAP (2021) → sim-to-real RL hydraulics → the [6 m autonomous dry-stone wall](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html) (Science Robotics 2023) → ExT multitask pretraining (2025); spun out **Gravis Robotics** (Johns CEO, Jud CTO) |
| [Gramazio Kohler Research](https://gramaziokohler.arch.ethz.ch/) (GKR), ETH Zurich | Fabio Gramazio · Matthias Kohler | robotic fabrication in architecture (In situ Fabricator, Mesh Mould, DFAB HOUSE, Semiramis); NCCR Digital Fabrication; the field's densest faculty tree: Dörfler → TUM, Parascho → EPFL, Hack → TU Braunschweig, Lloret-Fritschi → USI |
| [Professorship of Digital Fabrication](https://www.arc.ed.tum.de/en/df/professorship/), TUM | Kathrin Dörfler | collaborative on-site fabrication, AR-mediated timber assembly, mobile robots (GKR alumna); TUM's current center of gravity — Thomas Bock (STCR taxonomy, the field's standard reference books) emeritus since 2023 |
| [CRCL](https://www.crclcrclcrcl.org/), EPFL | Stefana Parascho | cooperative multi-robot assembly of full-scale structures (LightVault); GKR → Princeton → EPFL |
| [ICD](https://www.icd.uni-stuttgart.de/) + IntCDC, Univ. of Stuttgart | Achim Menges · Jan Knippers | the other German heavyweight: robotic timber/fiber fabrication pavilions, cyber-physical prefab (Cluster of Excellence IntCDC) |
| ITE, TU Braunschweig | Norman Hack | shotcrete 3D printing at structural scale (DFG TRR 277 Additive Manufacturing in Construction); GKR alumnus |
| UMIT/[Algoryx](https://www.algoryx.se/), Umeå Univ. | Martin Servin | RL + world models for autonomous wheel loaders with Komatsu/Epiroc — the Nordic counterpart to RSL's earthmoving-learning line |
| Imperial/UCL consortium | Mirko Kovac · Robert Stuart-Smith | **aerial additive manufacturing** — drones 3D-printing in flight (Nature 2022) |
| RWTH Aachen University | Sigrid Brell-Çokcan | teleoperated and semi-autonomous construction machines, especially for deconstruction; among the most prolific authors of 2021–2025; e.g. Lee and Brell-Çokcan, *Construction Robotics* 7, 2023, [DOI](https://doi.org/10.1007/s41693-023-00111-9) |
| University of Cambridge | Ioannis Brilakis | datasets and perception for construction robots: ConSLAM, excavator pose from synthetic data, crack segmentation on an unmanned wheeled robot; e.g. Trzeciak et al., *J. Computing in Civil Engineering* 37, 2023, [DOI](https://doi.org/10.1061/jccee5.cpeng-5212) |
| OTH Regensburg (formerly TU Munich) | Thomas Linner | construction-robotics education and, at TUM, the cable-driven curtain-wall installation robot (Iturralde et al., *AutCon* 138, 2022, [DOI](https://doi.org/10.1016/j.autcon.2022.104235)) |

### Asia and Oceania

*By volume this is now the largest region of the field ([[05-construction-robotics/lineage|lineage §5]]). The rows were checked against the affiliations printed on each group's own 2021–2025 papers, with one representative paper each. The six mainland institutions among the busiest of 2021–2025 were mapped after a recount that filtered out manufacturing robotics. Five have a group whose papers are construction work and whose lead author is printed with that institution — the rows from Zhejiang to Tsinghua below. Southeast University's $13$ papers spread over several small groups — BIM-to-ROS data exchange, vision-guided assembly of prefabricated components, cable-climbing repair robots, worker EEG — with no single lead, so it has no row. The heavy-machinery OEM programmes (XCMG and its orbit) are not mapped.*

| Lab | PI | Known for |
|---|---|---|
| [IRiS Lab](https://iris.kaist.ac.kr/), KAIST CEE | Jee-Hwan Ryu | telerobotics + construction robotics (RA-L 2024 Best Paper); the Korean anchor of the ICRA construction-robotics community |
| [Construction API Lab](https://www.con-api.team/), National Taiwan Univ. | Jacob J. Lin | vision+BIM production monitoring moving into robot handover (Golparvar-Fard alumnus, Reconstruct co-founder) |
| SNU CEE | Youngjib Ham (2024–) · Changbum Ahn | vision/thermography diagnostics; wearable sensing (the Korean branch of the UIUC/UMich trees) |
| Hong Kong Polytechnic University | Heng Li | worker and equipment-operator sensing turned toward robots: EEG fatigue of equipment operators, thermal-image hand gestures for worker–robot collaboration, excavator 3D pose (with Monash); e.g. Wu et al., *AEI* 56, 2023, [DOI](https://doi.org/10.1016/j.aei.2023.101939) |
| University of Hong Kong | Weisheng Lu | human–robot collaboration in modular, off-site construction and robot + BIM facility inspection; e.g. Fu et al., *AutCon* 158, 2024 (review), [DOI](https://doi.org/10.1016/j.autcon.2023.105196) |
| University of Hong Kong · City University of Hong Kong | Jia Pan · Xiaowei Luo | co-authors of the most-cited on-site human–robot collaboration paper of 2023, Zhang et al., *AutCon* 150, [DOI](https://doi.org/10.1016/j.autcon.2023.104812); Pan also co-authored Baidu's excavation-trajectory work |
| HKUST | Jack C. P. Cheng | BIM as the robot's map: coverage path planning for indoor robots, excavator full-body pose from onboard sensors; e.g. Chen et al., *AutCon* 158, 2024, [DOI](https://doi.org/10.1016/j.autcon.2023.105160) |
| HKUST | Yantao Yu | worker–robot collaboration: worker intentions from partial observations, multi-robot team composition, a 2014–2024 human-centric HRC review; e.g. Pan and Yu, *AutCon* 158, 2024, [DOI](https://doi.org/10.1016/j.autcon.2023.105184) |
| Baidu RAL | Liangjun Zhang | the AES autonomous excavator (*Science Robotics* 2021), excavation trajectory optimization and learning, TNES terrain mapping and excavation; see [[05-construction-robotics/lineage\|lineage, Era 4]] |
| Jilin University | Jixin Wang and colleagues | excavator trajectory generation from expert operators' skills; equipment activity recognition; e.g. Feng et al., *AutCon* 158, 2024, [DOI](https://doi.org/10.1016/j.autcon.2023.105247) |
| Monash University | Mehrdad Arashpour | vision-based excavator pose estimation trained on synthetic data with domain randomization; e.g. Assadzadeh et al., *AutCon* 134, 2022, [DOI](https://doi.org/10.1016/j.autcon.2021.104089) |
| Zhejiang University | Jiangpeng Shu | robotic assembly of structural components planned from BIM: task and motion planning, collision-free trajectories, polyhedron-bounded collision checks; e.g. Gao et al., *AutCon* 140, 2022, [DOI](https://doi.org/10.1016/j.autcon.2022.104370) |
| Zhejiang University | Huayong Yang · Bing Xu | hydraulic construction machinery: force-preloaded motion control of an excavation robot, excavator safety control, master–slave hydraulic manipulators with Chongqing's Min Cheng; e.g. Yang et al., *AutCon* 141, 2022, [DOI](https://doi.org/10.1016/j.autcon.2022.104402) |
| Tongji University | Philip F. Yuan | robotic timber and fabrication at architectural scale: band-saw cutting of double-curved glulam, cooperative fabrication of natural tree-fork structures, drone bricklaying; e.g. Chai et al., *AutCon* 124, 2021, [DOI](https://doi.org/10.1016/j.autcon.2021.103571) |
| Huazhong University of Science and Technology | Cheng Zhou · Lieyun Ding | automated earthwork machinery: complete-coverage planning for an autonomous bulldozer, an earthwork digital twin for bulldozer teleoperation, a review of deep learning for construction machinery; e.g. You et al., *Journal of Field Robotics* 40, 2023, [DOI](https://doi.org/10.1002/rob.22234) |
| Chongqing University | Min Cheng | teleoperated hydraulic manipulators: master–slave interfaces with visual and auditory aids, task-learned virtual fixtures, concrete-pump boom trajectories, with Zhejiang's fluid-power group; e.g. Cheng et al., *Journal of Field Robotics* 41, 2024, [DOI](https://doi.org/10.1002/rob.22386) |
| Tsinghua University | Hongling Guo | worker–robot collaboration on site: two-stage task allocation for multiple construction robots, digital-twin safety monitoring, semantic behaviour decisions; e.g. Ye et al., *AutCon* 165, 2024, [DOI](https://doi.org/10.1016/j.autcon.2024.105583) |

### Middle East

| Lab / group | PI | Known for |
|---|---|---|
| NYU Abu Dhabi | Borja García de Soto | multi-robot data collection on sites, IFC/BIM-guided robot navigation, a case study of an overhead-drilling robot in the UAE; e.g. Prieto et al., *Journal of Field Robotics* 41, 2024, [DOI](https://doi.org/10.1002/rob.22316) |

### Manufacturing robotics (adjacent departments)

Construction's closest methodological sibling — structured-but-variable physical work.
These groups publish the manipulation/HRC methods construction researchers import:

| Lab | PI | Known for |
|---|---|---|
| [Manufacturing Futures Institute](https://engineering.cmu.edu/mfi/) + Robotics Institute, CMU | (multi-PI; Changliu Liu's safe-control/intent-prediction line most transferable) | AI for advanced manufacturing; the robotics muscle behind CMU's construction-AI push |
| [AUTOLab](https://autolab.berkeley.edu), UC Berkeley (IEOR/EECS) | Ken Goldberg | robust grasping & manipulation for warehouses/industrial automation |
| [BAIR](https://bair.berkeley.edu), UC Berkeley | Levine, Abbeel, et al. | the robot-learning engine room — [[01-canonical-papers/notes/4-vla/octo\|Octo]], much of the VLA lineage in this wiki |
| [Interactive Robotics Group](https://interactive.mit.edu), MIT | Julie Shah | human-robot teaming for manufacturing assembly — cross-training, human-aware motion planning; the HRC playbook construction borrows |

### What separates these groups

The groups differ less by country than by what they put on the site:

| What they put on the site | Groups |
|---|---|
| field-deployed mobile or heavy-machine systems, from site scanning to an autonomous dry-stone wall | RICAL, RSL/HEAP |
| manipulation and learning methods | Michigan LIVE Lab line, the manufacturing labs, Texas Robotics |
| the human side — biosensing, teleoperation, and interfaces — rather than autonomy itself | DPM, RAISE, HARMONIC, the Florida and Oregon State groups |
| the ends of the pipeline: monitoring what was built, or designing robotic production of a structure | RAAMAC, CMU CEE, the fabrication institutes (GKR, ICD, TUM, CRCL) |

### Self-check

1. A paper uses EEG from a worker to slow a collaborative robot. Which cluster does it most likely trace to?
2. A paper reports an autonomous excavator trained with sim-to-real RL for hydraulic control. Which lab line fits, and which Nordic group works on the same problem for wheel loaders?
3. A paper builds a robotic timber pavilion with a cyber-physical prefabrication workflow. Which cluster, and which assumption from "How to use this map" does it carry?

> [!tip]- Answers
> 1. Worker-sensing: S. Lee's DPM Lab and its descendants (Jebelli's RAISE Lab, Baek's HARMONIC Lab).
> 2. ETH RSL's HEAP line; UMIT/Algoryx (Servin) is the wheel-loader counterpart.
> 3. Fabrication — Stuttgart ICD/IntCDC (Menges · Knippers); it assumes the fabrication framing, not manipulation-LfD or heavy-machine autonomy.

### How to use this map

- **Paper triage**: an unfamiliar paper usually traces to one of these clusters — the
  cluster tells you its assumptions (manipulation-LfD vs worker-sensing vs heavy-machine
  autonomy vs CV-monitoring vs fabrication).
- **Genealogy triage**: a surprising number of US papers trace to two intermarried family
  trees (UMich: Kamat/Menassa + S. Lee; UIUC: Golparvar-Fard) — knowing the tree predicts
  the methods and evaluation style.
- **Venue watch**: Automation in Construction, J. Computing in Civil Engineering, ISARC,
  and increasingly ICRA/IROS/Science Robotics.
- **For this wiki's direction**: ETH RSL anchors the selected heavy-machine-learning line; the
  Michigan cluster anchors the manipulation/HRC progression; BAIR/MIT-Shah supply learning
  and HRC methods; RAAMAC/RICAL provide the selected perception baselines.

## 한국어

건설로봇 연구를 누가 하고, 각 그룹이 무엇으로 알려져 있는가. 링크·소속·**사제 계보**는
2026-07 기준으로 검증했다 (랩 페이지, 학위논문, 출판 기록 웹 조사).
(기업은 [[05-construction-robotics/industry-deployment|산업·배치 지도]], 이 그룹들의 작업이
분야 역사에서 어디에 놓이는지는 [[05-construction-robotics/lineage|계보 페이지]] 참고.)

> [!note] 처음이라면 · First pass
> 이 페이지는 지도다. 그룹을 가르는 것과 이 지도를 쓰는 법을 먼저 읽고, 읽는 논문에 이름이 나올 때 그룹을 찾아본다.

### 미시간 허브

이 조사 코퍼스의 미국 지도를 조직하는 구조적 사실 하나: **미시간대 CEE 클러스터에서 이 위키가
확인한 교수 계보가 가장 조밀하다.** 박사 졸업생 8명이 자기 건설로봇/로봇인식 랩을 운영하고, 내부의 두 그룹이
상호보완적인 두 연구 프로그램을 이끈다.

| 랩 / 그룹 | PI | 대표 분야 |
|---|---|---|
| [LIVE Lab](https://live.engin.umich.edu) + SICIS, 미시간대 CEE | Vineet Kamat · Carol Menassa | 건설 조작의 정본이라 할 진행: 비전 유도 조립(2015) → 적응적 자율성 → 시연 학습 → 폐루프 BIM 디지털 트윈 → 촉각 전달 → 언어 지시 로봇 |
| [DPM Lab](https://dpm.engin.umich.edu), 미시간대 CEE | SangHyun Lee | 작업자 중심 자동화: EEG(뇌 전기 활동)/EDA(피부 전기 활동, 즉 피부 전도도) 웨어러블 바이오센싱, 인간공학 비전, 작업자 생리 상태를 인간-로봇 팀 제어에 피드백 |

**검증된 학술 계보 (자기 랩을 운영하는 제자들):**

| 제자 | 지도교수 | 현 소속 | 방향 |
|---|---|---|---|
| Chen Feng | Kamat | [AI4CE Lab](https://ai4ce.github.io/), NYU Tandon | 이 위키의 토목 기반 로봇러닝 경로와 직접 겹치는 그룹 — DeepMapping, 협력 인식, 건설 현장 로봇 항법 NSF CAREER |
| Houtan Jebelli | S. Lee | [RAISE Lab](https://raiselab.cee.illinois.edu/), UIUC CEE | 생리 신호 컴퓨팅 → 로봇 제어: BCI(뇌–컴퓨터 인터페이스) 원격조작, 의도 인식 모션 계획, 보행/비행 점검 로봇 |
| Daeho Kim | S. Lee | [Construction Vision Lab](https://cvl.civmin.utoronto.ca/), 토론토대 | 협동 로봇 비전 안전, 합성 학습 데이터(BlendCon) |
| Francis Baek | S. Lee | [HARMONIC Lab](https://harmoniclab.ce.gatech.edu/), Georgia Tech CEE | 신경계 기반 HRC (EEG/웨어러블을 로봇 루프에); 신규: 사족보행 로봇 위의 LMM 에이전트 |
| Hongrui Yu | Kamat · Menassa | [Virginia Tech CEE](https://mlsoc.vt.edu/about/faculty-and-staff/hongrui-yu.html) | 건설 기능의 클라우드 모방학습, 촉각 전달 |
| Ci-Jyun Liang | Kamat · Menassa | [CROSS Lab](https://you.stonybrook.edu/crosslab/), Stony Brook | 시연 학습, 로봇 자세 추정, XR 안전 |
| Xi Wang | Menassa · Kamat | [XIC Lab](https://www.xiclab.org/), Texas A&M | HRC 인터페이스로서의 공정 수준 디지털 트윈; 멀티로봇 감독 |
| Somin Park | Kamat · Menassa | UT Arlington | 작업자-로봇 소통을 위한 자연어/LLM+VR 인터페이스 |

(Jebelli의 제자들이 나무를 잇는다: Yizhi Liu → Syracuse — NSF 지원 비행+보행 지붕 점검
로봇; Shayan Shayesteh → Appalachian State; M. Habibnezhad → LSU, 포스닥 관계 — 이 나무의 다른 간선인 박사 지도 관계와 달리 포스닥 지도 관계다.)

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
| 컬럼비아대(전 UBC) | Zhengbo Zou | 건설 로봇 제어를 위한 강화학습과 모방학습, 인간–로봇 협업을 위한 안전 제약 강화학습. 예: Huang 외, *AutCon* 146, 2023, [DOI](https://doi.org/10.1016/j.autcon.2022.104691) |
| USC (유산) | Behrokh Khoshnevis | **Contour Crafting** — 건설 3D 프린팅의 기원 |
| UT Austin ME/ARL (인접 그룹) | Luis Sentis (HCRL), Mitch Pryor (NRG) | 휴머노이드/전신 제어와 필드 로보틱스 |
| **UT Austin CS — Texas Robotics** | **Yuke Zhu** ([RPL](https://rpl.cs.utexas.edu/)), **Roberto Martín-Martín** (RobIn Lab) | **조작 학습 — 이 프로그램 경로에 가장 가까운 그룹.** 둘 다 [[01-canonical-papers/notes/4-vla/robomimic\|robomimic]] 공저자이고, 그 노트의 affiliation 줄이 "Stanford, UT Austin, NVIDIA"다. Martín-Martín은 [[01-canonical-papers/notes/4-vla/open-x-embodiment\|Open X-Embodiment]]에도 참여. CS395T *Robot Manipulation and Learning* 강의계획서와 읽기 목록이 공개돼 있다 |
| UT Austin ECE | Lillian Chin | 촉각 센서 설계·제작 — 인접하지만 센서 *제작*은 [[04-robotics/tactile-visuotactile\|이 프로그램 범위 밖]] |

참고: **CMU와 UC 버클리의 토목공학과에는 조작 중심의 건설로봇 랩이 없다** — CMU 토목의
강점은 건설 *센싱/AI*(Tang, Akinci)이고, 버클리의 physical AI 역량은 전부 토목 밖에
있다(아래). CMU의 로보틱스 쪽 굴착 계보(Stentz/Singh, 1990년대)는
[[05-construction-robotics/lineage|계보 페이지]]에 있다.

### 유럽

| 랩 | PI | 대표 분야 |
|---|---|---|
| [Robotic Systems Lab](https://rsl.ethz.ch/), ETH 취리히 | Marco Hutter | **HEAP 자율 굴착 라인** — 힘 기반 굴착(2017) → 트렌칭 → HEAP(2021) → sim-to-real RL 유압 → [6m 자율 돌담](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)(Science Robotics 2023) → ExT 멀티태스크 사전학습(2025); **Gravis Robotics** 스핀아웃 (Johns CEO, Jud CTO) |
| [Gramazio Kohler Research](https://gramaziokohler.arch.ethz.ch/) (GKR), ETH 취리히 | Fabio Gramazio · Matthias Kohler | 건축 로봇 패브리케이션 (In situ Fabricator, Mesh Mould, DFAB HOUSE, Semiramis); NCCR Digital Fabrication; 분야에서 가장 조밀한 교수 계보: Dörfler → TUM, Parascho → EPFL, Hack → TU Braunschweig, Lloret-Fritschi → USI |
| [Professorship of Digital Fabrication](https://www.arc.ed.tum.de/en/df/professorship/), TUM | Kathrin Dörfler | 협업 현장 패브리케이션, AR 매개 목조 조립, 모바일 로봇 (GKR 출신); TUM의 현재 중심 — Thomas Bock(STCR 분류, 표준 참고서)은 2023년 은퇴 |
| [CRCL](https://www.crclcrclcrcl.org/), EPFL | Stefana Parascho | 실규모 구조물의 협력 멀티로봇 조립 (LightVault); GKR → Princeton → EPFL |
| [ICD](https://www.icd.uni-stuttgart.de/) + IntCDC, 슈투트가르트대 | Achim Menges · Jan Knippers | 독일의 다른 한 축: 로봇 목조/섬유 파빌리온, 사이버-물리 프리팹 (IntCDC 엑설런스 클러스터) |
| ITE, TU Braunschweig | Norman Hack | 구조 스케일 숏크리트 3D 프린팅 (DFG TRR 277); GKR 출신 |
| UMIT/[Algoryx](https://www.algoryx.se/), 우메오대 | Martin Servin | Komatsu/Epiroc와 자율 휠로더 RL·월드모델 — RSL 토공 학습 라인의 북유럽 대응물 |
| Imperial/UCL 컨소시엄 | Mirko Kovac · Robert Stuart-Smith | **공중 적층 제조** — 비행 중 3D 프린팅하는 드론 (Nature 2022) |
| 아헨공대 | Sigrid Brell-Çokcan | 원격조작·반자율 건설 기계, 특히 해체 작업. 2021–2025년 가장 많이 낸 저자 가운데 하나. 예: Lee와 Brell-Çokcan, *Construction Robotics* 7, 2023, [DOI](https://doi.org/10.1007/s41693-023-00111-9) |
| 케임브리지대 | Ioannis Brilakis | 건설 로봇을 위한 데이터셋과 인식: ConSLAM, 합성 데이터로 굴착기 자세, 무인 바퀴 로봇 위 균열 분할. 예: Trzeciak 외, *J. Computing in Civil Engineering* 37, 2023, [DOI](https://doi.org/10.1061/jccee5.cpeng-5212) |
| OTH 레겐스부르크(전 뮌헨공대) | Thomas Linner | 건설 로보틱스 교육, 그리고 뮌헨공대 시절의 케이블 구동 커튼월 설치 로봇(Iturralde 외, *AutCon* 138, 2022, [DOI](https://doi.org/10.1016/j.autcon.2022.104235)) |

### 아시아와 오세아니아

*양으로 보면 이제 분야에서 가장 큰 지역이다([[05-construction-robotics/lineage|계보 §5]]). 각 행은 그 그룹 자신의 2021–2025년 논문에 인쇄된 소속으로 확인했고, 대표 논문을 하나씩 달았다. 2021–2025년에 많이 낸 중국 본토 기관 여섯은 제조 로봇을 걸러 낸 재집계 뒤에 그룹으로 나눴다. 다섯 곳에는 논문이 건설 연구이고 주 저자가 그 기관 소속으로 인쇄된 그룹이 있다. 아래 저장대부터 칭화대까지의 행이다. 동남대의 $13$편은 여러 작은 그룹 — BIM과 ROS 사이 데이터 교환, 비전으로 안내하는 프리캐스트 부재 조립, 케이블을 오르는 보수 로봇, 작업자 EEG — 으로 흩어져 있고 뚜렷한 중심이 없어 행을 두지 않았다. 중장비 제조사 프로그램(XCMG와 그 주변)은 지도에 없다.*

| 랩 | PI | 대표 분야 |
|---|---|---|
| [IRiS Lab](https://iris.kaist.ac.kr/), KAIST 건설환경 | 류지환 | 텔레로보틱스 + 건설로봇 (RA-L 2024 Best Paper); ICRA 건설로봇 커뮤니티의 한국 앵커 |
| [Construction API Lab](https://www.con-api.team/), 국립대만대 | Jacob J. Lin | 비전+BIM 생산 모니터링에서 로봇 전달로 확장 중 (Golparvar-Fard 출신, Reconstruct 공동창업) |
| 서울대 건설환경 | Youngjib Ham (2024–) · Changbum Ahn | 비전/열화상 진단; 웨어러블 센싱 (UIUC/UMich 나무의 한국 가지) |
| 홍콩이공대 | Heng Li | 로봇으로 향한 작업자·장비 운전자 센싱: 장비 운전자의 EEG 피로, 작업자–로봇 협업을 위한 열화상 손 제스처, 굴착기 3D 자세(모나시대와 함께). 예: Wu 외, *AEI* 56, 2023, [DOI](https://doi.org/10.1016/j.aei.2023.101939) |
| 홍콩대 | Weisheng Lu | 모듈러·공장 제작 건설의 인간–로봇 협업, 로봇 + BIM 시설 점검. 예: Fu 외, *AutCon* 158, 2024(리뷰), [DOI](https://doi.org/10.1016/j.autcon.2023.105196) |
| 홍콩대 · 홍콩성시대 | Jia Pan · Xiaowei Luo | 2023년 가장 많이 인용된 현장 인간–로봇 협업 논문의 공저자, Zhang 외, *AutCon* 150, [DOI](https://doi.org/10.1016/j.autcon.2023.104812). Pan은 바이두의 굴착 궤적 연구에도 공저자로 참여 |
| 홍콩과기대 | Jack C. P. Cheng | 로봇의 지도로서의 BIM: 실내 로봇 커버리지 경로 계획, 탑재 센서로 굴착기 전신 자세 추정. 예: Chen 외, *AutCon* 158, 2024, [DOI](https://doi.org/10.1016/j.autcon.2023.105160) |
| 홍콩과기대 | Yantao Yu | 작업자–로봇 협업: 부분 관측에서 작업자 의도 학습, 다중 로봇 팀 구성, 2014–2024 인간 중심 HRC 리뷰. 예: Pan과 Yu, *AutCon* 158, 2024, [DOI](https://doi.org/10.1016/j.autcon.2023.105184) |
| 바이두 RAL | Liangjun Zhang | AES 자율 굴착기(*Science Robotics* 2021), 굴착 궤적 최적화와 학습, TNES 지형 매핑·굴착. [[05-construction-robotics/lineage\|계보, 4시대]] 참조 |
| 지린대 | Jixin Wang과 동료들 | 숙련 운전자 기술에서 굴착기 궤적 생성, 장비 작업 동작 인식. 예: Feng 외, *AutCon* 158, 2024, [DOI](https://doi.org/10.1016/j.autcon.2023.105247) |
| 모나시대 | Mehrdad Arashpour | 합성 데이터와 도메인 무작위화로 학습한 비전 기반 굴착기 자세 추정. 예: Assadzadeh 외, *AutCon* 134, 2022, [DOI](https://doi.org/10.1016/j.autcon.2021.104089) |
| 저장대 | Jiangpeng Shu | BIM에서 계획하는 구조 부재의 로봇 조립: 작업·동작 계획, 충돌 없는 궤적, 다면체로 감싼 충돌 검사. 예: Gao 외, *AutCon* 140, 2022, [DOI](https://doi.org/10.1016/j.autcon.2022.104370) |
| 저장대 | Huayong Yang · Bing Xu | 유압 건설 기계: 굴착 로봇의 힘 예압 운동 제어, 굴착기 안전 제어, 충칭대 Min Cheng과 함께한 마스터–슬레이브 유압 매니퓰레이터. 예: Yang 외, *AutCon* 141, 2022, [DOI](https://doi.org/10.1016/j.autcon.2022.104402) |
| 퉁지대 | Philip F. Yuan | 건축 규모의 로봇 목재·제작: 이중 곡면 집성재의 밴드쏘 절단, 자연 나무 갈래 구조의 협동 로봇 제작, 드론 벽돌 쌓기. 예: Chai 외, *AutCon* 124, 2021, [DOI](https://doi.org/10.1016/j.autcon.2021.103571) |
| 화중과기대 | Cheng Zhou · Lieyun Ding | 자동화 토공 기계: 자율 불도저의 전면 커버리지 계획, 불도저 원격조작을 위한 토공 디지털 트윈, 건설 기계 딥러닝 리뷰. 예: You 외, *Journal of Field Robotics* 40, 2023, [DOI](https://doi.org/10.1002/rob.22234) |
| 충칭대 | Min Cheng | 원격조작하는 유압 매니퓰레이터: 시각·청각을 보강한 마스터–슬레이브 인터페이스, 과제로 학습한 가상 고정구, 콘크리트 펌프 붐 궤적. 저장대 유압 그룹과 함께한다. 예: Cheng 외, *Journal of Field Robotics* 41, 2024, [DOI](https://doi.org/10.1002/rob.22386) |
| 칭화대 | Hongling Guo | 현장의 작업자–로봇 협업: 여러 건설 로봇의 2단계 작업 배분, 디지털 트윈 안전 모니터링, 의미 기반 행동 결정. 예: Ye 외, *AutCon* 165, 2024, [DOI](https://doi.org/10.1016/j.autcon.2024.105583) |

### 중동

| 랩 | PI | 대표 분야 |
|---|---|---|
| 뉴욕대 아부다비 | Borja García de Soto | 현장의 다중 로봇 데이터 수집, IFC/BIM을 따르는 로봇 내비게이션, UAE의 천장 드릴링 로봇 사례 연구. 예: Prieto 외, *Journal of Field Robotics* 41, 2024, [DOI](https://doi.org/10.1002/rob.22316) |

### 제조 로봇 (타 학과)

건설의 가장 가까운 방법론적 형제 — 구조화되어 있지만 변동이 있는 물리 작업.
건설 연구자들이 수입해 쓰는 조작/HRC 기법이 이 그룹들에서 나온다:

| 랩 | PI | 대표 분야 |
|---|---|---|
| [Manufacturing Futures Institute](https://engineering.cmu.edu/mfi/) + Robotics Institute, CMU | (복수 PI; Changliu Liu의 안전 제어/의도 예측 라인이 가장 이전 가능) | 첨단 제조 AI; CMU 건설 AI 추진의 로보틱스 근육 |
| [AUTOLab](https://autolab.berkeley.edu), UC 버클리 (IEOR/EECS) | Ken Goldberg | 창고/산업 자동화를 위한 강건한 파지와 조작 |
| [BAIR](https://bair.berkeley.edu), UC 버클리 | Levine, Abbeel 등 | 로봇 학습의 엔진룸 — [[01-canonical-papers/notes/4-vla/octo\|Octo]] 등 이 위키 VLA 계보의 산실 |
| [Interactive Robotics Group](https://interactive.mit.edu), MIT | Julie Shah | 제조 조립의 인간-로봇 팀워크 — 교차 훈련, 인간 인지 모션 계획; 건설이 빌려 쓰는 HRC 플레이북 |

### 그룹을 가르는 것

그룹들은 나라보다 현장에 무엇을 내놓는지로 갈린다:

| 현장에 내놓는 것 | 그룹 |
|---|---|
| 현장 스캔부터 자율 돌담까지, 현장 배치형 이동·중장비 시스템 | RICAL, RSL/HEAP |
| 조작·학습 기법 | 미시간 LIVE Lab 계열, 제조 로봇 랩, Texas Robotics |
| 자율성 자체보다 인간 쪽 — 바이오센싱, 원격조작, 인터페이스 | DPM, RAISE, HARMONIC, 플로리다대·Oregon State 그룹 |
| 파이프라인의 양 끝: 지어진 것을 모니터링하거나 구조물의 로봇 생산을 설계 | RAAMAC, CMU CEE, 패브리케이션 연구소(GKR, ICD, TUM, CRCL) |

### Self-check

1. 작업자의 EEG로 협동 로봇을 감속시키는 논문이다. 어느 클러스터에서 왔을 가능성이 가장 큰가?
2. 유압 제어를 sim-to-real RL로 학습한 자율 굴착기 논문이다. 어느 랩 계열이며, 휠로더에서 같은 문제를 다루는 북유럽 그룹은?
3. 사이버-물리 프리팹 공정으로 로봇 목조 파빌리온을 짓는 논문이다. 어느 클러스터이며, "이 지도를 쓰는 법"의 어떤 가정을 지니는가?

> [!tip]- Answers
> 1. 작업자 센싱: S. Lee의 DPM Lab과 제자들(Jebelli의 RAISE Lab, Baek의 HARMONIC Lab).
> 2. ETH RSL의 HEAP 라인; 휠로더 쪽 대응물은 UMIT/Algoryx(Servin).
> 3. 패브리케이션 — 슈투트가르트 ICD/IntCDC(Menges · Knippers); 조작-LfD나 중장비 자율성이 아닌 패브리케이션 틀의 가정을 지닌다.

### 이 지도를 쓰는 법

- **논문 분류**: 낯선 논문은 대개 이 클러스터 중 하나로 거슬러 올라간다 — 클러스터가 그
  논문의 가정(조작-LfD vs 작업자 센싱 vs 중장비 자율성 vs CV 모니터링 vs 패브리케이션)을
  알려준다.
- **계보 분류**: 놀랄 만큼 많은 미국 논문이 서로 얽힌 두 그루의 가계도(미시간:
  Kamat/Menassa + S. Lee; UIUC: Golparvar-Fard)로 거슬러 올라간다 — 나무를 알면 방법론과
  평가 스타일이 예측된다.
- **학회 감시**: Automation in Construction, J. Computing in Civil Engineering, ISARC,
  그리고 점점 ICRA/IROS/Science Robotics.
- **이 위키의 방향에서**: ETH RSL은 선택한 중장비 학습 계열을, 미시간 클러스터는 조작/HRC
  진행을 대표한다; BAIR/MIT-Shah가 학습·HRC 기법을 공급하고, RAAMAC/RICAL은 선택한 인식
  베이스라인을 제공한다.
