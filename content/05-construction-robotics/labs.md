---
title: Construction Robotics Labs
tags: [reference, construction]
---

## English

Who does construction robotics research, and what each group is known for. Links verified.
(For companies see [[03-deep-learning/physical-ai-ecosystem|the ecosystem page]]; for how
these groups' work fits the field's history, see [[05-construction-robotics/lineage|the lineage page]].)

### United States

| Lab / group | PI | Known for |
|---|---|---|
| [RICAL](https://rical.ce.gatech.edu/index.html), Georgia Tech CEE | Yong K. Cho | field-task robotization: construction ops, infrastructure maintenance, worker safety; LiDAR/scan automation |
| [HARMONIC Lab](https://harmoniclab.ce.gatech.edu/), Georgia Tech | Francis Baek | vision-based localization, GAN data augmentation, worker safety/ergonomics, human-robot team dynamics |
| [RAAMAC](https://raamac.cee.illinois.edu), UIUC CEE | Mani Golparvar-Fard | computer-vision progress monitoring from site photos/BIM; spun out **Reconstruct Inc.** |
| RAISE Lab ([profile](https://cee.illinois.edu/directory/profile/hjebelli)), UIUC CEE | Houtan Jebelli | construction robotics + physiological computing, human-robot interaction on site |
| [LIVE Lab](https://live.engin.umich.edu) & CEE robotics group, Univ. of Michigan | Vineet Kamat, Carol Menassa | human-robot collaboration on site, worker-assist robots, digital twins; one of the largest US construction-automation programs |
| [DPM Lab](https://dpm.engin.umich.edu), Univ. of Michigan | SangHyun Lee | worker-centered construction automation: wearable biosensing, safety/productivity analytics, robots-for-humans |
| [Yu Research Group](https://hyu-bot.github.io/YuResearchPortfolio/research/), Virginia Tech | Hongrui Yu | imitation learning for construction skills, human-robot handover, digital-twin HRC workflows |
| [XIC Lab](https://www.xiclab.org/), Texas A&M (Construction Science) | Xi Wang | human-robot collaboration in construction (field-defining survey), process-level digital twins |
| [SWARM Lab](https://cee.engineering.cmu.edu/directory/bios/tang-pingbo.html), CMU CEE | Pingbo Tang | spatiotemporal sensing & human-cyber-physical systems for construction/infrastructure |
| CMU CEE ([profile](https://www.cmu.edu/cee/people/faculty/akinci.html)) | Burcu Akinci | BIM + 3D imaging/sensing for facility histories; co-designing a National Institute for AI in Construction; now Dean of Engineering |
| [CIFE](https://cife.stanford.edu), Stanford | (center, multi-PI) | the long-running home of VDC/BIM research — the digital-model side that site robots consume |
| USC (legacy) | Behrokh Khoshnevis | **Contour Crafting** — the origin of construction 3D printing |
| UT Austin (adjacent groups) | Luis Sentis (HCRL), Mitch Pryor (NRG) | humanoid/whole-body control and field robotics — the robotics-side neighbors of a construction program |

Note: **CMU and UC Berkeley have no manipulation-focused construction-robotics lab in
civil engineering** — CMU CEE's strength is construction *sensing/AI* (Tang, Akinci), and
Berkeley's physical-AI strength sits entirely outside CEE (below).

### Europe / global reference

| Lab | PI | Known for |
|---|---|---|
| [Robotic Systems Lab](https://rsl.ethz.ch/robots-media/heap.html), ETH Zurich | Marco Hutter | **HEAP autonomous walking excavator**, ANYmal; the [6m autonomous dry-stone wall](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html) — the reference system for learning-era heavy-machine autonomy |
| [Gramazio Kohler Research](https://gramaziokohler.arch.ethz.ch/), ETH Zurich | Fabio Gramazio, Matthias Kohler | robotic fabrication in architecture; the world's first architectural robotics lab; NCCR Digital Fabrication |
| TU Munich (legacy) | Thomas Bock | the STCR taxonomy and the field's standard reference books/surveys |

### Manufacturing robotics (adjacent departments)

Construction's closest methodological sibling — structured-but-variable physical work.
These groups publish the manipulation/HRC methods construction researchers import:

| Lab | PI | Known for |
|---|---|---|
| [Manufacturing Futures Institute](https://engineering.cmu.edu/mfi/) + Robotics Institute, CMU | (multi-PI) | AI for advanced manufacturing; the robotics muscle behind CMU's construction-AI push |
| [AUTOLab](https://autolab.berkeley.edu), UC Berkeley (IEOR/EECS) | Ken Goldberg | robust grasping & manipulation for warehouses/industrial automation |
| [BAIR](https://bair.berkeley.edu), UC Berkeley | Levine, Abbeel, et al. | the robot-learning engine room — [[01-canonical-papers/notes/4-vla/octo|Octo]], much of the VLA lineage in this wiki |
| [Interactive Robotics Group](https://interactive.mit.edu), MIT | Julie Shah | human-robot teaming for manufacturing assembly (from Boeing aerospace lines) — the HRC playbook construction borrows |

### How to use this map

- **Paper triage**: an unfamiliar paper usually traces to one of these clusters — the
  cluster tells you its assumptions (CV-monitoring vs fabrication vs heavy-machine autonomy
  vs HRC vs worker-sensing).
- **Venue watch**: Automation in Construction, J. Computing in Civil Engineering, ISARC,
  and increasingly ICRA/IROS.
- **For this wiki's direction**: ETH RSL and the Michigan cluster are the closest
  methodological neighbors; BAIR/MIT-Shah supply the learning/HRC methods; RAAMAC/RICAL
  define the perception baseline. The research-stream analysis lives in
  [[05-construction-robotics/lineage|the lineage page]].

## 한국어

건설로봇 연구를 누가 하고, 각 그룹이 무엇으로 알려져 있는가. 링크는 검증했다.
(기업은 [[03-deep-learning/physical-ai-ecosystem|생태계 페이지]], 이 그룹들의 작업이 분야
역사에서 어디에 놓이는지는 [[05-construction-robotics/lineage|계보 페이지]] 참고.)

### 미국

| 랩 / 그룹 | PI | 대표 분야 |
|---|---|---|
| [RICAL](https://rical.ce.gatech.edu/index.html), Georgia Tech 토목환경 | Yong K. Cho | 현장 작업 로봇화: 시공 운영, 인프라 유지보수, 작업자 안전; LiDAR/스캔 자동화 |
| [HARMONIC Lab](https://harmoniclab.ce.gatech.edu/), Georgia Tech | Francis Baek | 비전 기반 위치 추정, GAN 데이터 증강, 작업자 안전/인간공학, 인간-로봇 팀 역학 |
| [RAAMAC](https://raamac.cee.illinois.edu), UIUC 토목환경 | Mani Golparvar-Fard | 현장 사진/BIM 기반 CV 공정 모니터링; **Reconstruct Inc.** 창업 |
| RAISE Lab ([프로필](https://cee.illinois.edu/directory/profile/hjebelli)), UIUC 토목환경 | Houtan Jebelli | 건설로봇 + 생리 신호 컴퓨팅, 현장 인간-로봇 상호작용 |
| [LIVE Lab](https://live.engin.umich.edu) 및 CEE 로보틱스 그룹, 미시간대 | Vineet Kamat, Carol Menassa | 현장 인간-로봇 협업, 작업자 보조 로봇, 디지털 트윈; 미국 최대급 건설 자동화 프로그램 |
| [DPM Lab](https://dpm.engin.umich.edu), 미시간대 | SangHyun Lee | 작업자 중심 건설 자동화: 웨어러블 바이오센싱, 안전/생산성 분석 |
| [Yu Research Group](https://hyu-bot.github.io/YuResearchPortfolio/research/), Virginia Tech | Hongrui Yu | 건설 기술의 모방학습, 인간-로봇 물체 전달, 디지털 트윈 HRC 워크플로 |
| [XIC Lab](https://www.xiclab.org/), Texas A&M (Construction Science) | Xi Wang | 건설 HRC(분야를 정의한 서베이), 공정 수준 디지털 트윈 |
| [SWARM Lab](https://cee.engineering.cmu.edu/directory/bios/tang-pingbo.html), CMU 토목환경 | Pingbo Tang | 건설/인프라의 시공간 센싱과 인간-사이버-물리 시스템 |
| CMU 토목환경 ([프로필](https://www.cmu.edu/cee/people/faculty/akinci.html)) | Burcu Akinci | BIM + 3D 이미징/센싱; 건설 AI 국가 연구소 설계 참여; 현 공대 학장 |
| [CIFE](https://cife.stanford.edu), Stanford | (센터, 복수 PI) | VDC/BIM 연구의 오랜 본산 |
| USC (유산) | Behrokh Khoshnevis | **Contour Crafting** — 건설 3D 프린팅의 기원 |
| UT Austin (인접 그룹) | Luis Sentis (HCRL), Mitch Pryor (NRG) | 휴머노이드/전신 제어와 필드 로보틱스 |

참고: **CMU와 UC 버클리의 토목공학과에는 조작(manipulation) 중심의 건설로봇 랩이 없다** —
CMU 토목의 강점은 건설 *센싱/AI*(Tang, Akinci)이고, 버클리의 physical AI 역량은 전부
토목 밖에 있다(아래).

### 유럽 / 글로벌 기준점

| 랩 | PI | 대표 분야 |
|---|---|---|
| [Robotic Systems Lab](https://rsl.ethz.ch/robots-media/heap.html), ETH 취리히 | Marco Hutter | **HEAP 자율 보행 굴착기**, ANYmal; [6m 자율 돌담](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html) |
| [Gramazio Kohler Research](https://gramaziokohler.arch.ethz.ch/), ETH 취리히 | Fabio Gramazio, Matthias Kohler | 건축의 로봇 패브리케이션; 세계 최초 건축 로보틱스 랩; NCCR Digital Fabrication |
| TU 뮌헨 (유산) | Thomas Bock | STCR 분류 체계와 표준 참고서·서베이 |

### 제조 로봇 (타 학과)

건설의 가장 가까운 방법론적 형제 — 구조화되어 있지만 변동이 있는 물리 작업.
건설 연구자들이 수입해 쓰는 조작/HRC 기법이 이 그룹들에서 나온다:

| 랩 | PI | 대표 분야 |
|---|---|---|
| [Manufacturing Futures Institute](https://engineering.cmu.edu/mfi/) + Robotics Institute, CMU | (복수 PI) | 첨단 제조를 위한 AI; CMU 건설 AI 추진의 로보틱스 근육 |
| [AUTOLab](https://autolab.berkeley.edu), UC 버클리 (IEOR/EECS) | Ken Goldberg | 창고/산업 자동화를 위한 강건한 파지와 조작 |
| [BAIR](https://bair.berkeley.edu), UC 버클리 | Levine, Abbeel 등 | 로봇 학습의 엔진룸 — [[01-canonical-papers/notes/4-vla/octo|Octo]] 등 이 위키 VLA 계보의 산실 |
| [Interactive Robotics Group](https://interactive.mit.edu), MIT | Julie Shah | 제조 조립의 인간-로봇 팀워크(보잉 항공 라인 출신) — 건설이 빌려 쓰는 HRC 플레이북 |

### 이 지도를 쓰는 법

- **논문 분류**: 낯선 논문은 대개 이 클러스터 중 하나로 거슬러 올라간다 — 클러스터가 그
  논문의 가정(CV 모니터링 vs 패브리케이션 vs 중장비 자율성 vs HRC vs 작업자 센싱)을
  알려준다.
- **학회 감시**: Automation in Construction, J. Computing in Civil Engineering, ISARC,
  그리고 점점 ICRA/IROS.
- **이 위키의 방향에서**: ETH RSL과 미시간 클러스터가 방법론적으로 가장 가까운 이웃이고,
  BAIR/MIT-Shah가 학습/HRC 기법을 공급하며, RAAMAC/RICAL이 인식 베이스라인을 정의한다.
  연구 흐름 분석은 [[05-construction-robotics/lineage|계보 페이지]]에 있다.
