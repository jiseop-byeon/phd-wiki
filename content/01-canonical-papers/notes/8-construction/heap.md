---
title: "HEAP — The Autonomous Walking Excavator (Jud et al., 2021)"
authors: Dominic Jud, Simon Kerscher, Martin Wermelinger, Edo Jelavic, Pascal Egli, Philipp Leemann, Gabriel Hottiger, Marco Hutter
affiliation: ETH Zurich, Robotic Systems Lab
venue: Automation in Construction
year: 2021
pdf: https://doi.org/10.1016/j.autcon.2021.103783
project: https://rsl.ethz.ch/robots-media/heap.html
tags: [paper, construction, robotics]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Jud et al., Automation in Construction 2021** — [DOI](https://doi.org/10.1016/j.autcon.2021.103783) · [ETH OA PDF](https://www.research-collection.ethz.ch/server/api/core/bitstreams/62e1de57-8939-4701-8672-ec2bb55e1c5d/content) · [Official](https://rsl.ethz.ch/robots-media/heap.html)

## English

**One-line summary**: A Menzi Muck M545 walking excavator rebuilt for autonomy — force-controllable hydraulics, full-state sensing (GNSS-RTK/IMU/LiDAR), and chassis adaptation to arbitrary terrain — the reference *system* for research-grade heavy-machine autonomy.

**The system, concretely** (what a Working-level read should extract):

- **Base machine**: Menzi Muck M545, a ~12 t *walking* excavator — four individually
  articulated wheeled legs, so the chassis itself is a legged robot that must balance on
  slopes before the arm does anything.
- **Actuation retrofit**: the stock hydraulic pilot stage is replaced with electrically
  driven pilot valves; **servo valves + pressure sensors on the leg cylinders** enable
  *force* control of the chassis (active terrain adaptation), and the arm's cylinders get
  pressure sensing for end-effector force estimation — this is the hardware fact that
  makes force-based digging (the RSL line's founding move) possible at all.
- **Sensing**: dual-antenna GNSS-RTK for global pose, IMU, draw-wire cylinder encoders + link IMUs for joint state, cylinder pressures, and two cab-mounted Velodyne VLP-16 LiDARs building local terrain maps
  ([[04-robotics/state-estimation-slam|graph-based sensor fusion]] in later work).
- **Software structure**: terrain mapping → task-level planning (dig locations,
  free-form trench geometry) → arm trajectory/force planning → chassis force control —
  a classical [[04-robotics/robot-systems-deployment|sense–plan–control stack]]; nothing
  in the 2021 platform paper is learned.

**What it demonstrates, with the evidence character**: autonomous free-form trenching and
embankment/grading on real outdoor terrain (embankments at 0.03–0.05 m mean error); slope
operation via active chassis adaptation; tasks specified from geometric files and executed
autonomously on research worksites. The platform also supports teleoperation — a second,
identical machine was built and used for a remote UXO-clearance dig.
Later work on the same platform: the
[6 m dry-stone wall](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)
([[01-canonical-papers/notes/8-construction/dry-stone-wall|Science Robotics 2023 note]]),
[[01-canonical-papers/notes/8-construction/egli-rl|RL arm control]] (2020–22), and
[[01-canonical-papers/notes/8-construction/ext|ExT]]'s pretrain→fine-tune policies (2025).

**Limitations & open gaps the paper leaves** (and follow-ups attacked): heavily
instrumented research machines (two were built, but both bespoke) — *platform generality*
is untested (ExT's motivation); no learning in the loop (Egli's RL line); productivity was not benchmarked
against human operators (AES's contribution); and long-duration unattended operation was
out of scope.

**Why it matters for this wiki**: HEAP is what a *platform* investment buys — one
well-instrumented machine has carried a decade of research from classical control to
learning-based digging. The construction analogue of what ALOHA
([[01-canonical-papers/notes/4-vla/act|ACT]]) did for bimanual manipulation research.

## 한국어

**한 줄 요약**: 자율화를 위해 개조된 Menzi Muck M545 보행 굴착기 — 힘 제어 가능한 유압, 완전 상태 센싱(GNSS-RTK/IMU/LiDAR), 임의 지형에의 섀시 적응 — 연구급 중장비 자율성의 기준 *시스템*.

**시스템, 구체적으로** (Working 수준의 읽기가 뽑아내야 할 것):

- **베이스 기계**: Menzi Muck M545, 약 12톤 *보행* 굴착기 — 개별 관절이 있는 바퀴 달린
  다리 넷, 즉 섀시 자체가 팔이 무언가 하기 전에 경사에서 균형을 잡아야 하는 다리 로봇이다.
- **구동 개조**: 순정 유압 파일럿단을 전기 구동 파일럿 밸브로 교체; **다리 실린더의 서보
  밸브 + 압력 센서**가 섀시의 *힘* 제어(능동 지형 적응)를 가능하게 하고, 팔의 실린더에도
  압력 센싱이 붙어 말단 힘 추정이 된다 — 힘 기반 굴착(RSL 라인의 창립 수)을 애초에
  가능하게 한 하드웨어 사실이다.
- **센싱**: 전역 pose용 이중 안테나 GNSS-RTK, IMU, 관절 상태용 draw-wire 실린더 엔코더 +
  링크 IMU, 실린더 압력, 그리고 국소 지형 지도를 만드는 캡 장착 Velodyne VLP-16 두 대
  (후속 연구에서
  [[04-robotics/state-estimation-slam|그래프 기반 센서 융합]]).
- **소프트웨어 구조**: 지형 매핑 → 과제 수준 계획(굴착 위치, 자유 곡선 트렌치 기하) →
  팔 궤적/힘 계획 → 섀시 힘 제어 — 고전적
  [[04-robotics/robot-systems-deployment|sense–plan–control 스택]]이며, 2021 플랫폼
  논문에는 학습이 전혀 없다.

**보여준 것, 증거의 성격과 함께**: 실제 야외 현장에서의 자율 자유 곡선 트렌칭과
제방/정지 작업(제방 평균 오차 0.03~0.05 m); 능동 섀시 적응을 통한 경사 작업; 기하
파일로 지정된 과제를 연구 작업지에서 자율 실행. 플랫폼은 원격조작도 지원한다 — 동일한
두 번째 기계가 제작되어 원격 불발탄 제거 굴착에 사용됐다. 같은 플랫폼의 후속: [6m 돌담](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)
([[01-canonical-papers/notes/8-construction/dry-stone-wall|Science Robotics 2023 노트]]),
[[01-canonical-papers/notes/8-construction/egli-rl|RL 팔 제어]](2020–22),
[[01-canonical-papers/notes/8-construction/ext|ExT]]의 사전학습→파인튜닝 정책(2025).

**논문이 남긴 한계와 공백** (후속이 공략한 것): 무겁게 계측된 연구용 기계(두 대가 제작됐지만 모두 맞춤제작) — *플랫폼
일반성* 미검증(ExT의 동기); 루프에 학습 없음(Egli의 RL 라인); 인간 운전자 대비 생산성
미측정(AES의 기여); 장시간 무인 운영은 범위 밖.

**이 위키에서 중요한 이유**: HEAP은 *플랫폼* 투자가 무엇을 사는지 보여준다 — 계측이 잘 된
기계 한 대가 고전 제어에서 학습 기반 굴착까지 10년의 연구를 실어 날랐다. ALOHA
([[01-canonical-papers/notes/4-vla/act|ACT]])가 양팔 조작 연구에 한 일의 건설판이다.

### 연결

- 기초: [[04-robotics/mpc|MPC]], [[02-foundations/rl-basics|RL]] · 이전: [[01-canonical-papers/notes/8-construction/stentz-excavator|Stentz 1999]] · 다음: [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL]] → [[01-canonical-papers/notes/8-construction/dry-stone-wall|돌담]] → [[01-canonical-papers/notes/8-construction/ext|ExT]]
- 계보: [[05-construction-robotics/lineage|건설로봇 계보]] (4시대의 기준 시스템) · 스트림: [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> This paper's claim is a demonstration of an autonomous walking-excavator *system*, not a new learning method. It is fair to judge it by system/platform criteria — integration completeness, reusability, whether it enabled follow-up research — and by those criteria it is among the field's best. Be precise about "autonomous" too: autonomous task execution on research worksites, not validation of unsupervised commercial deployment.
>
> 이 논문의 주장은 "자율 보행 굴착기 시스템의 실증"이다 — 새로운 학습 방법론의 기여가 아니다. 시스템/플랫폼 논문의 기준(통합 완성도, 재사용성, 후속 연구를 가능하게 했는가)으로 평가해야 공정하고, 그 기준으로는 이 분야 최고 수준이다. "autonomous"의 운용적 의미도 정확히: 연구 작업지에서의 과제 자율 실행이지, 상업적 무감독 배치의 검증이 아니다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading (★)

- [ ] Say why the actuation retrofit (electric pilot valves, pressure sensing) is the precondition for force-based digging · 구동 개조(전기 파일럿 밸브, 압력 센싱)가 왜 힘 기반 굴착의 전제인지 말할 수 있다
- [ ] Walk through the sensing stack (GNSS-RTK/IMU/LiDAR/pressure) and the software structure (mapping → planning → force control) · 센싱 스택(GNSS-RTK/IMU/LiDAR/압력)과 소프트웨어 구조(매핑→계획→힘 제어)를 단계별로 말할 수 있다
- [ ] State the character of the evaluation precisely — autonomous execution on research worksites (embankments 0.03–0.05 m mean error), with teleoperation supported · 평가의 성격 — 연구 작업지에서의 자율 실행(제방 오차 0.03~0.05 m), 원격조작 지원 — 을 정확히 기술할 수 있다
- [ ] Pair the four gaps the paper left (generality, learning, productivity comparison, long unattended operation) with the follow-up that attacked each · 논문이 남긴 공백 4가지(일반성·학습·생산성 비교·장기 무인)와 각각을 공략한 후속을 짝지을 수 있다
