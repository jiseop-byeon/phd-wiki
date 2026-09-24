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
genealogies: technical eras, academic family trees, machine evolution, plus a measured picture of who publishes most today and how each stream moved since 2019) and
[[05-construction-robotics/labs|2. Labs Map]] (who does this research, verified 2026-07, with Asia, Oceania and the Middle East added 2026-09) —
then complete [[05-construction-robotics/site-engineering|2.5 Site Robotics as an Engineering System]]. It turns one work package into requirements, frames, uncertainty, safety, productivity, and an evidence ladder. Only then read by stream below. Curated papers live in
[[01-canonical-papers/canonical-list|section 8 of the canonical list]].

### The five research streams

Corpus-derived (2026-07 survey of ~120 papers from the mapped labs), not aspirational:
each stream has enough real published work to be read as a lineage. Every stream page is also a course page on one of 2.5's two site objects — S1, a 20 kg facade panel whose two holes are aligned to ±5 mm, and S2, a 5-tonne excavator's trench dug to a ±30 mm grade ([[05-construction-robotics/site-engineering|2.5]]) — with its picture, worked case and problem set; the session schedule at the end of this page orders them.

1. [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] —
   excavators, wheel loaders, fleets: dynamics, terrain interaction, MPC vs RL vs
   imitation, HEAP/AES/ExT; worked on S2's trench — grade error, valve latency, cutting force
2. [[05-construction-robotics/assembly-fabrication|4. Robotic Assembly & Fabrication]] —
   S1's two holes as a residual pair — yaw, spacing mismatch, acceptance on a fresh scan — then the three lineages (UMich, ETH GKR, mobile production)
3. [[05-construction-robotics/site-perception|5. Site Perception, Scan-to-BIM & Inspection]] —
   LiDAR/point clouds, registration to BIM, autonomous scanning robots, progress
   monitoring, inspection platforms; worked on S1's bracket hole — point spacing, registration, guarded acceptance
4. [[05-construction-robotics/hrc-worker-centered|6. HRC & Worker-Centered Robotics]] —
   physiological sensing in the robot loop, intention-aware planning, proximity safety,
   exoskeletons, teleoperation; worked on S1's lane and hold — separation with a relayed stop, the release test
5. [[05-construction-robotics/digital-twin-workflows|7. Digital Twins & BIM-Driven Workflows]] —
   the interface layer: process-level twins, BIM-to-robot task generation, closed-loop
   execution, task allocation; worked on S1's frame chain — error composition, staleness

Cross-cutting layers (not streams — every stream uses them):

- [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real for Field Robots]] — reality-gap
  sources, randomization, privileged learning, residuals, and transfer evidence, worked on S2's soil as a measured gap
- [[05-construction-robotics/industry-deployment|8. Industry & Deployment Map]] — who is
  commercializing what, at what autonomy level (verified 2026-07)
- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — the
  manipulation lens across the streams: task-to-primitive matrix, the simulation–lab–site
  ladder applied to contact-rich work, and how to choose a defensible core task
- [[05-construction-robotics/imitating-contact|10. Imitating Contact]] — the learning half on
  S1's last 40 mm: what behaviour cloning assumes and the compounding error it costs in
  millimetres, two demonstrators averaged into one mean, DAgger, impedance targets as the
  action, a residual bounded by the site, and how many trials a seating claim needs
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

### Session schedule · 학습 일정

One row is one 60–90-minute session; [[02-foundations/overview|0. Overview]] sets the unit and keeps the pacing table these counts feed. The track runs on S1 and S2, the two site objects frozen in [[05-construction-robotics/site-engineering|2.5]]. The three maps (1, 2, 8) take one session each; 2.5 comes before any stream; after it the streams 3–7 and the cross-cutting 7.5 may be taken in any order; 9 follows them because it builds on 4's two-hole geometry and 6's hold, and 10 reads last because it runs a learned policy on 9's pin; 10 also leans on robotics [[04-robotics/teleoperation-demonstration|12]], [[04-robotics/force-compliance-control|13]] and the [[04-robotics/capstone-panel-contact|capstone]], and on [[03-deep-learning/vla/index|VLA]] §2–§4 and §6. A **bold** row belongs to the Literacy pass.

| # | Page and sections | Activity | Check that ends the session |
|---:|---|---|---|
| **1** | [[05-construction-robotics/lineage\|1]] all | first pass | The three genealogies and the measured field of §5–§6: which stream grew fastest since 2019, and which three reviews you would read first for your own stream. |
| **2** | [[05-construction-robotics/labs\|2]] all | first pass | Two groups per stream you would follow, each placed by what it builds and where it publishes. |
| **3** | [[05-construction-robotics/site-engineering\|2.5]] object, diagram | first pass | S1 and S2 read off their tables; the picture's stacked budget, $5.5$ mm linear against $2.69$ mm root-sum-square and the $\pm5$ mm tolerance; the $200$-minute day bracketed at $3.0$ and $2.4$ panels/h. |
| **4** | 2.5 §1–3 | first pass | The five phases of the work package, each with its safe state (§1, §3); the independence that root-sum-square assumes (§2); the time condition, $0.64$ m on 11's cell and $0.80$ m on S1's slower base (§3). |
| 5 | 2.5 §4, worked case | worked case by hand | Effective throughput $2.4$ against $3.0$ panels/h, $40$ min of overhead; the allocations read as two-sigma bounds miss about 1 in $4{,}900$, read as one-sigma about 1 in $16$; longer days approach but never pass $2.67$ panels/h. |
| 6 | 2.5 §5–6, self-check, problem set | problem set | The seven protocol items written for S1 (§5); Solutions: a $3$ mm base term gives $6.5$ and $3.50$ mm, and the $20$-panel day $468$ min, $2.56$ panels/h. |
| **7** | [[05-construction-robotics/earthmoving-heavy-machinery\|3]] object, diagram | first pass | S2's arm at the drawing pose; per-link tip bounds $4.36$, $2.27$ and $1.05$ mm, $27.7$ mm linear against $20.6$ mm root-sum-square and the $\pm30$ mm grade; a stop sent at the grade ending $45$ mm below it. |
| **8** | 3 §1–2 | first pass | Latency as a distance, from HEAP's valves, $35$ ms against $680$ and $850$ ms (§1); the cutting force $k_c w d=3.6$ kN for a $0.1$ m slice, and what soil twice as hard does under position and under force control (§2). |
| 9 | 3 §3, worked case | worked case by hand | The chain from satellites to the bucket tip (§3); $2.3$ mm left under the linear budget, a finishing pass at $15$ mm/s (linear) or $63$ mm/s (root-sum-square), and a valve delay that must be known to $7.7$ ms. |
| 10 | 3 §4–7 | first pass | HEAP's embankments at $0.03$ and $0.05$ m average error (§4); who watches the machine (§5); one machine-hour as $21.42$ bank, $26.8$ loose or $31.5$ nominal m³ (§6). |
| 11 | 3 self-check, problem set | problem set | Solutions: joint encoders push the linear total to $32.0$ mm; a delay known to $\pm0.03$ s fails linearly at $36.7$ mm and passes at $22.5$ mm root-sum-square; S2 at $18.21$ m³/h, $39.5$ min. |
| **12** | [[05-construction-robotics/assembly-fabrication\|4]] object, diagram | first pass | Holes A $(3,0)$ and B $(4,12)$ mm from one scan; the diamond $\lvert t\rvert+200\lvert\theta\rvert\le5$ of placements both holes accept. |
| 13 | 4 §1–5 | first pass | Why site assembly is not factory assembly, the three lineages, and one anchor system read with §3's extraction list. |
| **14** | 4 §6–8, worked case | worked case by hand | Means $(3.5,6)$ and differences $(1,12)$; translation alone leaves $\mp6$ mm; a yaw of $0.0299$ rad lands both holes at $\mp0.59$ mm, half the $1.18$ mm spacing mismatch; acceptance on a fresh scan. |
| 15 | 4 self-check, problem set | problem set | Solutions: holes $500$ mm apart need a yaw of $0.026$ rad against $0.020$ allowed, and a spacing mismatch of $11.17$ mm means retreat and report. |
| **16** | [[05-construction-robotics/site-perception\|5]] object, diagram | first pass | S1's bracket hole on the $3$ mm beam grid: $24$ edge points and the fitted centre's $0.91$ mm two-sigma circle; the centre's error against station range, crossing the $1$ mm map term at $11.4$ m. |
| **17** | 5 §1–2 | first pass | The site-perception stack, point spacing and a scan point's error defined on the station (§1); the four recurring problems (§2). |
| 18 | 5 §3–4, worked case | worked case by hand | A scan point's $1.00$ mm, the centre's $0.289$ mm and registration's $0.354$ mm, $0.913$ mm at two sigma; $16$ edge points needed; the guarded acceptance limit $4.09$ mm, and a $0.8\%$ chance that a hole measured at $3.9$ mm is out. |
| 19 | 5 §5, problem set 3 | lab and sweep | The Monte Carlo lab: the simulated map term first fails at $11.5$ m, and past it the verdict flips with range. |
| 20 | 5 self-check, problem set 1–2, 4 | problem set | Solutions: at $15$ m the spacing is $4.5$ mm, $16$ edge points, $1.27$ mm at two sigma, over the map term; with the target error doubled no range meets it. |
| **21** | [[05-construction-robotics/hrc-worker-centered\|6]] object, diagram, worked case | first pass + worked case by hand | $S_p=1.30$ m in clear air, the walker $61.5\%$ of it, $1.50$ m in dust and $3.40$ m through a relayed stop; the corner speed $0.5$, $0.17$ m/s or none; the hold's $2.5$ N push and the release test's $3.92$ mm sink. |
| **22** | 6 §1–3 | first pass | Closed-loop adaptive HRC defined on S1 (§1); the research lines, and which claims need care (§2–§3). |
| 23 | 6 §4–6 | first pass | Exposure arithmetic: $320$ passes a month bound the rate at $0.93\%$ per pass, and 1 in $10^4$ takes $29{,}956$ passes (§4); the stop chain and the occlusion-limited speed (§6). |
| 24 | 6 §7–8 | first pass | The hold, soft for the worker and stiff for the panel, and why one bolt fails the release test (§7); the one-way license, under which a worker-state estimate may tighten the robot's bounds but never widen them (§8). |
| 25 | 6 self-check, problem set | problem set | Solutions: the lane at $2.0$ m/s; braking at $1.25$ m/s² raises the corner speed from $0.17$ to $0.44$ m/s; $K_x\le1{,}000$ N/m for a $5$ N push; a doubled $K_z$ sinks $1.96$ mm. |
| **26** | [[05-construction-robotics/digital-twin-workflows\|7]] object, diagram | first pass | S1's hole A carried from BIM to site control, robot base and tool; a command aimed at the design coordinate misses by $6.56$ mm and one aimed at the twin's scanned hole by $2.66$ mm, against $\pm5$ mm; staleness crosses the map term at $14.5$ min. |
| **27** | 7 §1–2 | first pass | The closed workflow and error composition along a frame chain (§1); digital model, shadow and twin told apart by which data flows are automated (§2). |
| 28 | 7 §3, worked case | worked case by hand | Hole A at $(1.200,\,0.200)$ m in the base frame; tie $0.64$ mm and base $1.00$ mm at one sigma, the tie alone $1.28$ mm at two sigma; with the tie counted, hole A is not accepted ($8.1\%$ out); drift $0.36$ mm/h and a staleness bound of $14.5$ min. |
| 29 | 7 §4–5, self-check, problem set | problem set | Solutions: a $100$ m control lever makes the tie $2.24$ mm; counted in the conformity check it leaves hole A out with probability $18\%$; a $0.5$ K/h morning moves the staleness crossing to $43.5$ min. |
| **30** | [[05-construction-robotics/sim-to-real\|7.5]] object, diagram | first pass | Slice depth against $k_c$ for three controllers: the fixed $3.6$ kN cuts $0.100$ m at $60$ kPa and $0.075$ m at $80$; the adaptive one holds $0.100$ m; $82.3\%$ of sites fall inside $40$–$80$ kPa. |
| **31** | 7.5 §1–3 | first pass | The reality gap as a measured ratio, $\rho=0.75$ on the harder site (§1); domain randomization defined with its objective (§2); zero-shot transfer and the deployment ladder (§3). |
| 32 | 7.5 §4–6 | first pass | Reading transfer evidence (§4–§5); randomization coverage $0.823$ of the site distribution, and the blind controller's $2.4$ kN cutting $0.050$ m at $80$ kPa (§6). |
| 33 | 7.5 §7–8, worked case | worked case by hand | Four probe passes identify $k_c$ to $\pm4.9$ kPa (§7); the grade-safe residual bound of $1.08$ kN (§8); on the harder site $16.07$ m³/h and $44.8$ min against $21.42$ and $33.6$. |
| 34 | 7.5 §9, problem set 3 | lab and sweep | The Monte Carlo lab: coverage and productivity against the randomization range; problem 3's fits, biased by $+49.7$ mm from one depth and recovering $80.0\pm6.9$ kPa from two. |
| 35 | 7.5 self-check, problem set 1–2, 4 | problem set | Solutions: the $45$ kPa site; the twelve-parameter claim at $0.95^{12}=0.540$. |
| **36** | [[05-construction-robotics/industry-deployment\|8]] all | first pass | For one company per stream, the autonomy level it actually ships and the evidence behind it, set against the rung of 2.5 §5. |
| **37** | [[05-construction-robotics/construction-manipulation\|9]] object, diagram | first pass | S1's pin and hole, $D=18$ and $d=16$ mm with a $4$ mm lead-in; the error circle drawn against the lead-in. |
| 38 | 9 §1–3 | first pass | Why construction manipulation is its own problem, the task matrix, and the finding the ladder shows (§3). |
| **39** | 9 worked case | worked case by hand | Capture $0.988$ per hole and $0.976$ per panel; a $95$th-percentile error of $3.29$ mm; a side force of $329$ N stiff against $1.6$ N compliant; a vertical stiffness of $9{,}810$ N/m. |
| 40 | 9 §4–6, problem set 3 | lab and sweep | Anchor papers by what they demonstrate, and a task chosen concretely (§4–§6); the base-error sweep: panel capture first falls below $90\%$ at $3$ mm, and the lead-in grows about $1.3$ mm per millimetre. |
| 41 | 9 self-check, problem set 1–2, 4 | problem set | Solutions: $\sigma=1.75$ mm at a $3$ mm base term, a $5.31$ mm lead-in, $K\ge19{,}620$ N/m, wedging from $10.6^\circ$, and $124$ straight successes to rule out $2.4\%$. |
| **42** | [[05-construction-robotics/imitating-contact\|10]] object, diagram | first pass | S1's last $40$ mm as a learning problem: a creep of $0.2$ mm per step ($8$ mm uncorrected) and the operator's corridor $[-0.12,\ 0.92]$ mm; a cloned policy's errors at $24$ and $9$ mm end $6.0$ and $3.0$ mm off, so it seats $0.98^{25}=0.603$. |
| 43 | 10 §1–3 | first pass | The three seating conditions (§1); behaviour cloning's conditions and a cloned gain of $0.054$ against the operator's $0.5$ (§2); compounding error, $12.84$ steps adrift against a bound of $32$, horizons $27$ and $750$ (§3). |
| 44 | 10 §4–5 | first pass | Two routes averaged into $-12.5$ mm and a switch probability of $0.478$ (§4); DAgger at $40$ min a round, two rounds reaching $0.980$ against $0.960$ for $16$ h of demonstrations (§5). |
| **45** | 10 §6–8, worked case | worked case by hand | $329$ N stiff against $1.6$ N compliant, and the $19.6$ mm anchor at the handover (§6); the residual's worst case $2.33$ mm and $B\le0.43$ (§7); Wilson $[0.764,\ 0.991]$ for $19/20$ and $59$ straight successes (§8); the trail $0.446$, $0.603$, $1.000$, $2.33$ mm. |
| 46 | 10 §9, problem set 3 | lab and sweep | Mistakes on $0.0225$ of the operator's states against $0.233$ of the policy's own; BC $0.875$, DAgger $0.950$–$0.995$, residual $1.000$; the corpus sweep $0.556$–$0.960$; BC from the site's start $0.656$; problem 3: first below $90\%$ at $T=40$. |
| 47 | 10 self-check, problem set 1–2, 4 | problem set | Solutions: $\epsilon=0.01$ over $60$ mm gives $0.636$; a $0.3$ mm creep gives $0.535$ and $B\le0.36$; $38/40$ gives $[0.835,\ 0.986]$; the $20$-trial claim is compatible with $23.6\%$ failure. |

**Totals.** 47 sessions for the Working pass, 21 of them bold. A Literacy pass is the bold rows, or one session a page — 12 — when only each object and worked case are read. Plan on up to a fifth more for problems redone and labs debugged.

## 한국어

건설(및 인접 제조) 로봇 연구를 정리하는 공간 — 우리 랩의 핵심 연구 분야. 문헌이 네 개
분과에 걸쳐 있어 학회와 저널 곳곳에 흩어져 있다:

- **건설/토목**: Automation in Construction, J. of Computing in Civil Engineering, ISARC
- **컴퓨터과학/로보틱스**: ICRA, IROS, CoRL, RSS, T-RO, RA-L, Science Robotics
- **기계공학**: Journal of Field Robotics 등 필드 로보틱스 계열
- **전기전자**: 제어·시스템 계열

두 개의 지도에서 시작하라 — [[05-construction-robotics/lineage|1. Research Lineage]](세
가지 계보: 기술 시대, 학술 가계도, 기계 진화, 그리고 지금 누가 가장 많이 내고 흐름마다 2019년 이후 어떻게 움직였는지 잰 그림)와
[[05-construction-robotics/labs|2. Labs Map]](누가 이 연구를 하는가, 2026-07 검증, 아시아·오세아니아·중동은 2026-09에 추가) —
그다음 [[05-construction-robotics/site-engineering|2.5 Site Robotics as an Engineering System]]을 마친다. 하나의 작업 package를 요구조건·frame·불확실성·안전·생산성·증거 사다리로 바꾸는 교과다. 그 뒤 아래 스트림별로 읽는다. 큐레이션된 논문은
[[01-canonical-papers/canonical-list|핵심 논문 리스트 8번 섹션]]에 있다.

### 다섯 개의 연구 스트림

희망 사항이 아니라 코퍼스에서 도출했다(매핑된 랩들의 논문 ~120편, 2026-07 조사): 각
스트림은 계보로 읽을 수 있을 만큼의 실제 출판물을 갖고 있다. 스트림 페이지는 모두 2.5의 두 현장 대상 — S1은 두 구멍을 ±5 mm로 맞추는 20 kg 외장 패널, S2는 5톤급 굴착기가 ±30 mm 고저로 파는 트렌치([[05-construction-robotics/site-engineering|2.5]]) — 가운데 하나 위에 선 과목 페이지이기도 해서, 그림, 끝까지 한 계산, 과제를 갖췄다. 이 페이지 끝의 학습 일정이 순서를 정한다.

1. [[05-construction-robotics/earthmoving-heavy-machinery|3. Earthmoving & Heavy-Machine Autonomy]] —
   굴착기, 휠로더, 선단: 동역학, 지반 상호작용, MPC vs RL vs 모방, HEAP/AES/ExT. S2의 트렌치로 계산한다 — 고저 오차, 밸브 지연, 절삭력
2. [[05-construction-robotics/assembly-fabrication|4. Robotic Assembly & Fabrication]] —
   잔차 쌍으로 본 S1의 두 구멍 — 요, 간격 불일치, 새 스캔으로 받아들이기 — 그다음 세 계보(미시간, ETH GKR, 모바일 생산)
3. [[05-construction-robotics/site-perception|5. Site Perception, Scan-to-BIM & Inspection]] —
   LiDAR/포인트 클라우드, BIM 정합, 자율 스캔 로봇, 공정 모니터링, 점검 플랫폼. S1의 브래킷 구멍으로 계산한다 — 점 간격, 정합, 보호 대역을 둔 합격 판정
4. [[05-construction-robotics/hrc-worker-centered|6. HRC & Worker-Centered Robotics]] —
   로봇 루프 안의 생리 신호 센싱, 의도 인식 계획, 근접 안전, 외골격, 원격조작. S1의 통로와 지지로 계산한다 — 중계 정지가 있는 이격 거리, 해제 시험
5. [[05-construction-robotics/digital-twin-workflows|7. Digital Twins & BIM-Driven Workflows]] —
   인터페이스 층: 공정 수준 트윈, BIM→로봇 과제 생성, 폐루프 실행, 과제 할당. S1의 좌표 사슬로 계산한다 — 오차 합성, 상태의 나이

횡단층 (스트림이 아니라 — 모든 스트림이 사용):

- [[05-construction-robotics/sim-to-real|7.5 필드 로봇 Sim-to-Real]] — reality gap, 도메인
  랜덤화, privileged learning, 잔차, 전이 증거. S2의 흙으로 격차를 잰다
- [[05-construction-robotics/industry-deployment|8. Industry & Deployment Map]] — 누가
  무엇을 어떤 자율성 수준으로 상업화하는가 (2026-07 검증)
- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 스트림을
  가로지르는 조작의 렌즈: 작업–원시동작 매트릭스, 접촉이 많은 작업에 적용한 시뮬–실험실–현장
  사다리, 그리고 방어 가능한 핵심 작업 고르기
- [[05-construction-robotics/imitating-contact|10. 접촉 모방]] — S1의 마지막 40 mm에서 본
  학습 절반: 행동 복제가 가정하는 것과 그것이 밀리미터로 치르는 복합 오차, 시연자 둘이
  평균 하나로 뭉개지는 것, DAgger, 행동으로서의 임피던스 목표, 현장이 한계를 긋는 잔차,
  안착 주장에 필요한 시행 수
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

### 학습 일정 · Session schedule

한 행이 60–90분 학습 회차 하나다. 그 단위와, 이 회차 수가 들어가는 페이스 표는 [[02-foundations/overview|0. Overview]]에 있다. 이 트랙은 [[05-construction-robotics/site-engineering|2.5]]에서 고정한 두 현장 대상 S1과 S2로 돌아간다. 지도 셋(1, 2, 8)은 각각 한 회차이고, 2.5는 어느 흐름보다 먼저 한다. 그 뒤로 흐름 3–7과 가로지르는 7.5는 어떤 순서로 해도 되고, 9는 4의 두 구멍 기하와 6의 지지 위에 서므로 그 뒤에 읽고, 10은 9의 핀 위에서 학습된 정책을 돌리므로 마지막에 읽는다. 10은 로보틱스의 [[04-robotics/teleoperation-demonstration|12]], [[04-robotics/force-compliance-control|13]], [[04-robotics/capstone-panel-contact|캡스톤]]과 [[03-deep-learning/vla/index|VLA]] §2–§4, §6에도 기댄다. **굵은** 행이 Literacy 통과에 속한다.

| # | 페이지와 절 | 활동 | 회차를 끝내는 확인 |
|---:|---|---|---|
| **1** | [[05-construction-robotics/lineage\|1]] 전체 | 첫 읽기 | 세 계보와 §5–§6에서 잰 분야: 2019년 이후 가장 빨리 자란 흐름, 그리고 자기 흐름에서 먼저 읽을 리뷰 셋. |
| **2** | [[05-construction-robotics/labs\|2]] 전체 | 첫 읽기 | 흐름마다 따라갈 그룹 둘을, 무엇을 만들고 어디에 내는지로 자리매김한다. |
| **3** | [[05-construction-robotics/site-engineering\|2.5]] 대상, 과제 그림 | 첫 읽기 | 표에서 S1과 S2를 읽는다. 그림의 쌓인 예산: 선형 합 $5.5$ mm 대 제곱합 제곱근 $2.69$ mm, 그리고 $\pm5$ mm 허용오차. $3.0$과 $2.4$ 패널/h로 묶인 $200$분의 하루. |
| **4** | 2.5 §1–3 | 첫 읽기 | 작업 묶음의 다섯 단계와 단계마다의 안전 상태(§1, §3). 제곱합 제곱근이 가정하는 독립성(§2). 시간 조건: 11의 셀에서 $0.64$ m, 더 느리게 서는 S1 베이스에서 $0.80$ m(§3). |
| 5 | 2.5 §4, 대상으로 한 번 끝까지 | 손 계산 | 유효 처리량 $2.4$ 대 $3.0$ 패널/h, 부대 시간 $40$분. 배분을 2시그마로 읽으면 약 $4{,}900$번에 한 번, 1시그마로 읽으면 약 $16$번에 한 번 놓친다. 하루를 늘려도 $2.67$ 패널/h에 다가갈 뿐 넘지 못한다. |
| 6 | 2.5 §5–6, 스스로 점검, 과제 | 과제 | S1에 맞춰 쓴 프로토콜 일곱 항목(§5). 정답과 대조: 베이스 항 $3$ mm면 $6.5$와 $3.50$ mm, $20$장의 하루는 $468$분, $2.56$ 패널/h. |
| **7** | [[05-construction-robotics/earthmoving-heavy-machinery\|3]] 대상, 과제 그림 | 첫 읽기 | 그리는 자세의 S2 팔. 링크마다 날 끝 한계 $4.36$, $2.27$, $1.05$ mm, 선형 $27.7$ mm 대 제곱합 제곱근 $20.6$ mm, 그리고 $\pm30$ mm 고저. 고저에서 보낸 정지가 그 $45$ mm 아래에서 끝난다. |
| **8** | 3 §1–2 | 첫 읽기 | HEAP의 밸브로 본 거리로서의 지연, $35$ ms 대 $680$·$850$ ms(§1). $0.1$ m 절편의 절삭력 $k_c w d=3.6$ kN, 그리고 두 배 단단한 흙이 위치 제어와 힘 제어에서 각각 하는 일(§2). |
| 9 | 3 §3, 대상으로 한 번 끝까지 | 손 계산 | 위성에서 버킷 날 끝까지의 사슬(§3). 선형 예산에 남는 $2.3$ mm, 마무리 패스 $15$ mm/s(선형) 또는 $63$ mm/s(제곱합 제곱근), 그리고 $7.7$ ms까지 알아야 하는 밸브 지연. |
| 10 | 3 §4–7 | 첫 읽기 | 평균 오차 $0.03$과 $0.05$ m인 HEAP의 제방(§4). 누가 기계를 지켜보는가(§5). 같은 한 시간이 자연 상태 $21.42$, 흐트러진 $26.8$, 공칭 $31.5$ m³(§6). |
| 11 | 3 스스로 점검, 과제 | 과제 | 정답과 대조: 관절 엔코더면 선형 합이 $32.0$ mm. 지연을 $\pm0.03$ s로만 알면 선형으로 $36.7$ mm라 실패, 제곱합 제곱근 $22.5$ mm로 통과. S2는 $18.21$ m³/h, $39.5$분. |
| **12** | [[05-construction-robotics/assembly-fabrication\|4]] 대상, 과제 그림 | 첫 읽기 | 스캔 한 번의 구멍 A $(3,0)$와 B $(4,12)$ mm. 두 구멍이 모두 받아들이는 배치의 마름모 $\lvert t\rvert+200\lvert\theta\rvert\le5$. |
| 13 | 4 §1–5 | 첫 읽기 | 현장 조립이 공장 조립이 아닌 이유, 세 계보, 그리고 §3의 추출 목록으로 읽은 앵커 시스템 하나. |
| **14** | 4 §6–8, 대상으로 한 번 끝까지 | 손 계산 | 평균 $(3.5,6)$과 차이 $(1,12)$. 평행이동만으로는 $\mp6$ mm가 남는다. 요 $0.0299$ rad로 두 구멍이 $\mp0.59$ mm에 놓이는데, 간격 불일치 $1.18$ mm의 절반이다. 새 스캔으로 받아들인다. |
| 15 | 4 스스로 점검, 과제 | 과제 | 정답과 대조: $500$ mm 떨어진 구멍은 허용 $0.020$ rad에 대해 요 $0.026$ rad가 필요하고, 간격 불일치 $11.17$ mm는 물러나서 보고하라는 뜻이다. |
| **16** | [[05-construction-robotics/site-perception\|5]] 대상, 과제 그림 | 첫 읽기 | $3$ mm 빔 격자 위의 S1 브래킷 구멍: 가장자리 점 $24$개와 맞춘 중심의 2시그마 원 $0.91$ mm. 스테이션 거리에 따른 중심 오차가 $11.4$ m에서 $1$ mm 지도 항을 넘는다. |
| **17** | 5 §1–2 | 첫 읽기 | 현장 인식 스택, 그리고 스테이션 위에서 정의한 점 간격과 스캔 점 하나의 오차(§1). 반복되는 네 문제(§2). |
| 18 | 5 §3–4, 대상으로 한 번 끝까지 | 손 계산 | 스캔 점 $1.00$ mm, 중심 $0.289$ mm, 정합 $0.354$ mm, 2시그마로 $0.913$ mm. 필요한 가장자리 점 $16$개. 보호 대역을 둔 합격 한계 $4.09$ mm, 그리고 $3.9$ mm로 잰 구멍이 허용오차 밖일 확률 $0.8\%$. |
| 19 | 5 §5, 과제 3 | 실습과 스윕 | 몬테카를로 실습: 시뮬레이션한 지도 항은 $11.5$ m에서 처음 실패하고, 그 너머에서는 거리에 따라 판정이 뒤집힌다. |
| 20 | 5 스스로 점검, 과제 1–2, 4 | 과제 | 정답과 대조: $15$ m에서 점 간격 $4.5$ mm, 가장자리 점 $16$개, 2시그마 $1.27$ mm로 지도 항을 넘는다. 표적 오차를 두 배로 하면 어느 거리도 맞추지 못한다. |
| **21** | [[05-construction-robotics/hrc-worker-centered\|6]] 대상, 과제 그림, 대상으로 한 번 끝까지 | 첫 읽기 + 손 계산 | 맑은 공기에서 $S_p=1.30$ m(보행자 몫 $61.5\%$), 먼지 속 $1.50$ m, 중계 정지로 $3.40$ m. 모퉁이 속도 $0.5$, $0.17$ m/s, 또는 없음. 지지의 $2.5$ N 밀기와 해제 시험의 $3.92$ mm 처짐. |
| **22** | 6 §1–3 | 첫 읽기 | S1 위에서 정의한 폐루프 적응형 HRC(§1). 연구 계보와 조심해서 읽을 주장(§2–§3). |
| 23 | 6 §4–6 | 첫 읽기 | 노출 산수: 한 달 $320$회 통과로는 통과당 비율 상한이 $0.93\%$이고, $10^4$번에 한 번을 보이려면 $29{,}956$회가 든다(§4). 정지 사슬과 가려짐으로 제한된 속도(§6). |
| 24 | 6 §7–8 | 첫 읽기 | 작업자에게는 부드럽고 패널에는 단단한 지지, 그리고 볼트 하나로는 해제 시험을 통과하지 못하는 이유(§7). 작업자 상태 추정이 로봇의 한계를 좁힐 수는 있어도 넓힐 수는 없다는 일방향 허가(§8). |
| 25 | 6 스스로 점검, 과제 | 과제 | 정답과 대조: $2.0$ m/s의 차선. $1.25$ m/s² 제동이면 모퉁이 속도가 $0.17$에서 $0.44$ m/s로 오른다. $5$ N 밀기에는 $K_x\le1{,}000$ N/m. $K_z$를 두 배로 하면 처짐 $1.96$ mm. |
| **26** | [[05-construction-robotics/digital-twin-workflows\|7]] 대상, 과제 그림 | 첫 읽기 | BIM에서 현장 기준점, 로봇 베이스, 공구로 옮겨 가는 S1의 구멍 A. 설계 좌표를 겨눈 명령은 $6.56$ mm, 트윈이 스캔한 구멍을 겨눈 명령은 $2.66$ mm 빗나가고, 허용오차는 $\pm5$ mm다. 상태의 나이가 $14.5$분에 지도 항을 넘는다. |
| **27** | 7 §1–2 | 첫 읽기 | 닫힌 워크플로와 좌표 사슬을 따라 합성되는 오차(§1). 어느 데이터 흐름이 자동화되었는가로 가르는 디지털 모델·섀도·트윈(§2). |
| 28 | 7 §3, 대상으로 한 번 끝까지 | 손 계산 | 베이스 좌표계에서 구멍 A는 $(1.200,\,0.200)$ m. 1시그마로 기준점 연결 $0.64$ mm, 베이스 $1.00$ mm이고, 기준점 연결만으로 2시그마 $1.28$ mm다. 연결 오차를 넣으면 구멍 A는 합격하지 못한다(밖일 확률 $8.1\%$). 표류 $0.36$ mm/h, 상태 나이 한계 $14.5$분. |
| 29 | 7 §4–5, 스스로 점검, 과제 | 과제 | 정답과 대조: $100$ m 기준점 지레면 연결 오차가 $2.24$ mm. 적합성 판정에 넣으면 구멍 A가 밖일 확률 $18\%$. 시간당 $0.5$ K 오르는 아침이면 상태 나이 교차가 $43.5$분으로 늦춰진다. |
| **30** | [[05-construction-robotics/sim-to-real\|7.5]] 대상, 과제 그림 | 첫 읽기 | 세 제어기의 $k_c$에 대한 절편 깊이: 고정 $3.6$ kN은 $60$ kPa에서 $0.100$ m, $80$에서 $0.075$ m. 적응형은 $0.100$ m를 지킨다. 현장의 $82.3\%$가 $40$–$80$ kPa 안에 든다. |
| **31** | 7.5 §1–3 | 첫 읽기 | 측정한 비율로서의 reality gap, 더 단단한 현장에서 $\rho=0.75$(§1). 목적함수와 함께 정의한 domain randomization(§2). zero-shot 전이와 배치 사다리(§3). |
| 32 | 7.5 §4–6 | 첫 읽기 | 전이 증거 읽기(§4–§5). 현장 분포의 $0.823$을 덮는 randomization 범위, 그리고 $80$ kPa에서 $0.050$ m를 깎는 블라인드 제어기의 $2.4$ kN(§6). |
| 33 | 7.5 §7–8, 대상으로 한 번 끝까지 | 손 계산 | 시험 굴착 네 번으로 $k_c$를 $\pm4.9$ kPa까지 식별한다(§7). 고저를 지키는 잔차 한계 $1.08$ kN(§8). 더 단단한 현장에서 $21.42$와 $33.6$ 대신 $16.07$ m³/h, $44.8$분. |
| 34 | 7.5 §9, 과제 3 | 실습과 스윕 | 몬테카를로 실습: randomization 범위에 따른 커버리지와 생산성. 과제 3의 적합은 깊이 하나로는 $+49.7$ mm 치우치고, 둘로는 $80.0\pm6.9$ kPa를 되찾는다. |
| 35 | 7.5 스스로 점검, 과제 1–2, 4 | 과제 | 정답과 대조: $45$ kPa 현장. 열두 파라미터 주장은 $0.95^{12}=0.540$. |
| **36** | [[05-construction-robotics/industry-deployment\|8]] 전체 | 첫 읽기 | 흐름마다 회사 하나씩, 실제로 내놓는 자율 수준과 그 뒤의 증거를 2.5 §5의 사다리 단과 견준다. |
| **37** | [[05-construction-robotics/construction-manipulation\|9]] 대상, 과제 그림 | 첫 읽기 | S1의 핀과 구멍, $D=18$, $d=16$ mm, 리드인 $4$ mm. 리드인에 대어 그린 오차 원. |
| 38 | 9 §1–3 | 첫 읽기 | 건설 조작이 자기만의 문제인 이유, 작업 매트릭스, 그리고 사다리가 보여 주는 발견(§3). |
| **39** | 9 대상으로 한 번 끝까지 | 손 계산 | 구멍당 포착 $0.988$, 패널당 $0.976$. $95$번째 백분위 오차 $3.29$ mm. 옆 힘은 단단한 팔 $329$ N 대 유연한 팔 $1.6$ N. 수직 강성 $9{,}810$ N/m. |
| 40 | 9 §4–6, 과제 3 | 실습과 스윕 | 실제로 실증한 것으로 정렬한 앵커 논문과 구체적으로 고른 작업(§4–§6). 베이스 오차 훑기: 패널 포착은 $3$ mm에서 처음 $90\%$ 아래로 떨어지고, 리드인은 1밀리미터마다 약 $1.3$ mm 커져야 한다. |
| 41 | 9 스스로 점검, 과제 1–2, 4 | 과제 | 정답과 대조: 베이스 항 $3$ mm에서 $\sigma=1.75$ mm, 리드인 $5.31$ mm, $K\ge19{,}620$ N/m, $10.6^\circ$부터 쐐기 걸림, $2.4\%$를 배제하는 $124$번 연속 성공. |
| **42** | [[05-construction-robotics/imitating-contact\|10]] 대상, 과제 그림 | 첫 읽기 | 학습 문제로서의 S1 마지막 $40$ mm: 스텝당 크리프 $0.2$ mm(보정하지 않으면 $8$ mm)와 조작자의 회랑 $[-0.12,\ 0.92]$ mm. 복제한 정책의 오류가 $24$ mm와 $9$ mm에서 나면 $6.0$ mm와 $3.0$ mm 벗어나 끝나므로, 안착 확률은 $0.98^{25}=0.603$이다. |
| 43 | 10 §1–3 | 첫 읽기 | 안착의 세 조건(§1). 행동 복제의 조건과, 조작자의 $0.5$에 대한 복제 이득 $0.054$(§2). 복합 오차: 표류 $12.84$스텝 대 상한 $32$, 지평 $27$과 $750$(§3). |
| 44 | 10 §4–5 | 첫 읽기 | 두 경로가 평균 $-12.5$ mm로 뭉개지는 것과 전환 확률 $0.478$(§4). 라운드당 $40$분인 DAgger: 두 라운드의 $0.980$ 대 시연 $16$ h의 $0.960$(§5). |
| **45** | 10 §6–8, 대상으로 한 번 끝까지 | 손 계산 | 단단한 팔 $329$ N 대 유연한 팔 $1.6$ N, 하중을 넘길 때의 고정점 $19.6$ mm(§6). 잔차의 최악 $2.33$ mm와 $B\le0.43$(§7). $19/20$의 Wilson $[0.764,\ 0.991]$, 연속 성공 $59$번(§8). 계산의 흐름 $0.446$, $0.603$, $1.000$, $2.33$ mm. |
| 46 | 10 §9, 과제 3 | 실습과 스윕 | 조작자 상태의 $0.0225$ 대 정책 자신의 상태의 $0.233$에서 나는 실수. BC $0.875$, DAgger $0.950$–$0.995$, 잔차 $1.000$. 코퍼스 훑기 $0.556$–$0.960$. 현장 출발점에서의 BC $0.656$. 과제 3: $T=40$에서 처음 $90\%$ 아래. |
| 47 | 10 스스로 점검, 과제 1–2, 4 | 과제 | 정답과 대조: $60$ mm에서 $\epsilon=0.01$이면 $0.636$, 크리프 $0.3$ mm면 $0.535$와 $B\le0.36$, $38/40$은 $[0.835,\ 0.986]$, $20$회 주장은 실패율 $23.6\%$와 양립한다. |

**합계.** Working 통과는 47회이고 그중 굵은 회차가 21회다. Literacy 통과는 굵은 회차만 하는 것이고, 대상과 끝까지 계산만 읽으면 페이지당 1회로 12회다. 다시 푸는 과제와 실습 디버깅을 위해 최대 5분의 1을 더 잡는다.
