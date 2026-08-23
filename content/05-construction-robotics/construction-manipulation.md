---
title: 9. Construction Manipulation
tags: [construction-robotics, manipulation]
study-depth: Mastery
wiki-support: Working
depth-goal: "Map a construction task to the manipulation primitives, sensing, and control mode it needs; place any paper on the simulation–lab–site ladder; and pick a defensible core task."
mastery-when: "This is the intersection the research program is built on — the page exists to make a task choice defensible."
---

> [!abstract] Depth target · 깊이 목표
> **Mastery** — this is where the manipulation track and the construction domain meet, and
> the choice made here decides what the rest of the dissertation is about.
> **Mastery** — 매니퓰레이션 트랙과 건설 도메인이 만나는 지점이고, 여기서의 선택이 나머지
> 학위논문이 무엇에 관한 것인지를 결정한다.

> [!note] Before you start · 시작 전 점검
> You need the manipulation primitives and their control modes ([[04-robotics/force-compliance-control|13]], [[04-robotics/grasping|15]]), what touch adds ([[04-robotics/tactile-visuotactile|14. §1]]), and the construction assembly lineages ([[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]]).
> 조작 원시동작과 그 제어 모드([[04-robotics/force-compliance-control|13]], [[04-robotics/grasping|15]]), 촉각이 더하는 것([[04-robotics/tactile-visuotactile|14. §1]]), 건설 조립 계보([[05-construction-robotics/assembly-fabrication|조립·제작]])가 필요하다.

## English

### 1. Why construction manipulation is its own problem

[[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]] covers this
domain's *lineages* — who built what, and out of which research tradition. This page takes
the other cut: **what the robot's hand actually has to do**, task by task, and what each
task demands of the pages in the manipulation track.

The difference from factory manipulation is not that construction is harder in a vague way.
It is specific, and each item removes an assumption that factory robotics is allowed to make:

| Factory assumption | What construction supplies instead |
|---|---|
| The part is in a fixture, at a known pose | The part is where someone put it, within centimetres |
| The workpiece is rigid and dimensioned | Panels flex, rebar bundles shift, membranes drape |
| The environment is the same every cycle | Two instances of the same task differ; the building changes as it is built |
| The robot is bolted down | The base moved to get here, and its pose is part of the error budget |
| No one is inside the workspace | Trades are working alongside, and safety is regulated |
| $\mu$, mass, and geometry are known | Dust, moisture, and tolerance make all three uncertain |

Row 1 alone breaks hybrid position/force control, whose selection matrix assumes you know
which direction is normal to the surface ([[04-robotics/force-compliance-control|13. §3]]).
That is not a small caveat; it is why a factory controller does not transfer.

### 2. The task matrix

Construction tasks, decomposed into the manipulation primitives from the track. Read a row
as a specification: it says which pages a project on that task will need at depth.

| Task | Primitive | Decisive sensing | Control mode | Hardest uncertainty |
|---|---|---|---|---|
| **Anchor-bolt setting, overhead drilling** | drill, push | position + force; thrust | force along the bit axis | arm deflection under thrust; ceiling material varies |
| **Panel / curtain-wall installation** | grasp, transport, fit | vision + force | compliant fitting, low stiffness | part is large and flexible; base pose error dominates |
| **Drywall hanging** | grasp, hold, fasten | vision + force | position for hold, force for fastening | sheet flexes; overhead hold is a strength problem |
| **Drywall finishing** | sand, scrape | force / depth control | force normal to the surface | material removal depth is the spec, and it is sub-millimetre |
| **Rebar tying** | reach, wrap, cut | vision to find intersections | mostly position, light contact | mesh is non-rigid and shifts; thousands of repetitions |
| **Pipe / conduit fitting** | insert, align | force + tactile | impedance, low stiffness | wedging and jamming ([[04-robotics/force-compliance-control\|13. §5]]) |
| **Bolted steel connection** | align, insert, torque | force + torque | hybrid: position across, force along | heavy parts; the crane or base is compliant |
| **Timber joint assembly** | insert with interference | force/torque | learned or compliant insertion | tolerance and shape vary piece to piece |
| **Bricklaying, block placement** | grasp, place | vision | position | mostly a weight and cycle-time problem, not a contact problem |
| **Welding structural steel** | track a seam | vision + seam tracking | position along a tracked path | joint geometry varies; the work is hot and the standards are strict |

Two rows in that table are not contact-rich, and saying so is part of the point. Bricklaying
and most placement tasks are solved geometry with a payload problem attached; they belong to
the domain but not to this dissertation's core, by the admission test in
[[07-research-program/index|7. §7]].

### 3. The ladder — and the finding that should shape a topic choice

This wiki insists on distinguishing **simulation**, **laboratory or mock-up**, and **active
construction site**. Applied to contact-rich construction manipulation, that distinction
produces a striking result.

<svg viewBox="0 0 560 232" style="max-width:100%;height:auto" role="img" aria-label="three rungs of evidence with most work on the lower two and almost nothing on an active site">
  <g fill="currentColor">
    <rect x="40" y="146" width="440" height="40" rx="3" fill-opacity="0.08"/>
    <rect x="88" y="98" width="392" height="40" rx="3" fill-opacity="0.16"/>
    <rect x="360" y="50" width="120" height="40" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="40" y="146" width="440" height="40" rx="3"/><rect x="88" y="98" width="392" height="40" rx="3"/><rect x="360" y="50" width="120" height="40" rx="3"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="52" y="163">simulation</text>
    <text x="52" y="178" font-size="9.5" opacity="0.75">unlimited trials, chosen physics</text>
    <text x="100" y="115">laboratory or mock-up</text>
    <text x="100" y="130" font-size="9.5" opacity="0.75">real contact, arranged conditions &#8212; where nearly all of this work sits</text>
    <text x="372" y="67">active site</text>
    <text x="372" y="82" font-size="9.5" opacity="0.75">nearly empty</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="208">Across a targeted search of drilling, drywall, rebar, facade, timber and welding, only two papers put a</text>
    <text x="20" y="224">manipulator on an active construction site &#8212; and one of them is from 2007. That gap is the opportunity.</text>
  </g>
</svg>

Two verified exceptions stand out. Feng et al. (2024) report a planar rebar-tying robot
validated first on a rebar-mesh demonstration platform and then applied in the field on the
Shenyang Hunnan Science and Technology City Phase IV project. Yu et al. (2007) built a
curtain-wall installation robot on an excavator base and tested it on a construction site —
the title says so — but it is nearly twenty years old.

Everything else that is technically strong stops at the lab or a mock-up, and several papers
with "on-site" in the title say plainly in their text that the work was done in a controlled
laboratory. The strongest overhead-drilling result states that a real-site demonstration is
still future work.

> [!important] What to do with that finding
> Read it as a research opportunity, not as permission to skip the rung. The reason the top
> rung is empty is that it is genuinely hard — access, safety, schedule, and a building that
> will not wait. A dissertation that reaches an active site with a contact-rich task is
> making a claim almost nobody else can make. A dissertation that *says* "on-site" about
> mock-up work is joining the pattern this page exists to name.

### 4. Anchor papers, by what they actually demonstrate

Sorted by rung rather than by fame, because that is the ordering that matters here.

**On an active site**

- **Feng et al. (2024)**, rebar-tying robot with two-stage recognition (depth camera plus
  industrial camera), driving on the rebar mesh. Verified on a demonstration platform and
  then in the field.
- **Yu et al. (2007)**, curtain-wall installation robot on an excavator base, tested on site.

**Real contact, laboratory or full-scale mock-up**

- **Apolinarska et al. (2021)** — timber joint assembly where a policy trained entirely in
  simulation is deployed on hardware, guided by force/torque and pose, and generalises to
  tolerances and shape variations not seen in training. This is construction-scale
  peg-in-hole, and it is the closest thing the field has to a contact-rich learning result.
- **Kindle et al. (RA-L 2025)** — deflection and backlash compensation on a 700 kg tracked
  drilling robot (the Hilti Jaibot platform), evaluated on seven datasets recorded under
  simulated site disturbances. The compliance problem of
  [[04-robotics/force-compliance-control|13]] stated in construction terms.
- **Iturralde et al. (2022)** — a cable-driven parallel robot installing curtain-wall
  modules, tested in two close-to-real demonstration buildings.
- **Chu, Jung et al. (2013)** — the two-part steel-beam bolting system; older, and the
  canonical academic reference for bolted connections.

**Read for framing, not as a manipulation result**

- **Brosque et al. (2023)** compares on-site and off-site drywall solutions on a real
  project — an economics and process evaluation, which is exactly what a manipulation paper
  cannot tell you.
- **Melenbrink, Werfel and Menges (2020)** is the survey to read first: organised by
  construction task rather than by technology, scoped to on-site autonomy, and its gap
  analysis still holds.

> [!warning] Two traps in this literature
> **Press demonstrations get cited as results.** The humanoid widely described as installing
> drywall has a peer-reviewed paper about its *joint design*; the drywall demonstration
> itself is a press video. **And commercial systems have no papers.** Jaibot, TyBot, Canvas
> and Okibo are products; their productivity figures are marketing. Cite them as products
> and say so — see [[05-construction-robotics/industry-deployment|Industry Deployment]].

### 5. Choosing a task, concretely

Apply the five criteria from [[07-research-program/paper-arc|7.1 §4]] to the matrix in §2.

| Task | Contact essential? | Real tolerance? | Done at scale by hand? | Lab-repeatable? | Failure survivable? |
|---|---|---|---|---|---|
| Anchor-bolt setting | yes | yes, mm | yes | yes | overhead work — needs care |
| Panel fitting | yes | yes, mm | yes | yes | yes |
| Drywall finishing | yes | yes, sub-mm depth | yes | yes | yes |
| Rebar tying | partly | loose | yes, enormously | yes | yes |
| Pipe insertion | yes | yes | yes | yes | yes |
| Bricklaying | no | loose | yes | yes | yes |
| Overhead drilling | yes | yes | yes | yes | dust and falling debris |

Panel fitting, drywall finishing, and pipe insertion clear all five. Rebar tying clears the
scale criterion by a wide margin but is only lightly contact-rich, which makes it a superb
*deployment* target and a weak *contact-manipulation* contribution — and note that it is
also the one task with a site-verified result, which is not a coincidence.

### 6. What this domain gives back to the manipulation literature

The relationship runs both ways, and this is the part to say in an introduction. Construction
supplies problems that general manipulation research has no clean way to pose:

- **Unknown, drifting friction** — the $\mu$ that every grasp result in
  [[04-robotics/grasping|15. §2–§4]] takes as given.
- **Non-rigid parts at structural scale** — a 2.4 m sheet is not a rigid body, so closure is
  not even defined on it.
- **A workspace that changes because the robot changed it** — the building is the workpiece.
- **Tolerance stacks that no fixture absorbs** — base pose error, part placement error, and
  as-built deviation all land on the same contact.

Each is a defensible robustness claim rather than a domain excuse. That is the difference
the [[07-research-program/index|research program]] is built on.

### After reading

- [ ] Map a named construction task to its primitive, sensing, and control mode.
- [ ] Place any paper in this area on the simulation–lab–site ladder, and say what evidence put it there.
- [ ] Name the two site-verified contact-rich results and what they did.
- [ ] Apply the five task-selection criteria and reject at least one tempting task.
- [ ] State two things construction gives back to general manipulation research.

### Self-check

1. Why does hybrid position/force control fail on a construction panel-fitting task that it
   would handle in a factory?
2. A paper's title contains "on-site". What do you check before believing it?
3. Rebar tying is the only task in §2 with a site-verified robot. Why is it *still* a weak
   choice for this dissertation's core contribution?
4. A vendor reports 300 holes per day for a drilling robot. How should that appear in a
   literature review?
5. Which two rows of §2 would you cut first if the dissertation needed narrowing, and why?

> [!tip]- Answers
> 1. Because its selection matrix assigns force control to the direction it believes is normal to the surface, and that belief comes from a model. In a fixture the part is where the model says; on site it is within a centimetre or two of there, so force control ends up acting partly along the surface and position control partly into it — the exact fighting the architecture exists to prevent ([[04-robotics/force-compliance-control|13. §3]]).
> 2. The methods and experiments sections, for a sentence naming where the work actually happened. Several papers in this area carry "on-site" in the title and state in their own text that the development and validation were done in a controlled laboratory. The title describes the ambition; the experimental section describes the evidence.
> 3. Because the contact is light. The hard parts of rebar tying are perception (finding intersections on a shifting non-rigid mesh), coverage planning, and doing it thousands of times reliably — which makes it an excellent deployment and autonomy result, but the contribution would not be about contact. Under the admission test it serves the program's *navigation and deployment* pillars more than its manipulation core.
> 4. As a product claim with its source named, never as a result. Jaibot, TyBot, Canvas and Okibo have no peer-reviewed papers of their own, so their productivity figures are marketing that has not been through review. They are legitimate evidence that a market exists and that the task is worth automating — which is a different claim from a measured one.
> 5. Bricklaying and block placement, because they fail the contact-essential criterion — they are solved geometry with a payload attached — and welding, because its standards, heat, and qualification requirements add an entire regulatory apparatus orthogonal to the manipulation contribution. Cutting them costs the dissertation no core claim.

### Sources

**Site-verified**

- R. Feng, Y. Jia, T. Wang, H. Gan, "Research on the System Design and Target Recognition Method of the Rebar-Tying Robot," *Buildings*, vol. 14, no. 3, art. 838, 2024. DOI 10.3390/buildings14030838. Open access. Its abstract states validation on a rebar-mesh demonstration platform followed by application on the Shenyang Hunnan Science and Technology City Phase IV project.
- S. N. Yu, S. Y. Lee, C. S. Han, K. Y. Lee, S. H. Lee, "Development of the curtain wall installation robot: Performance and efficiency tests at a construction site," *Autonomous Robots*, vol. 22, no. 3, pp. 281–291, 2007. DOI 10.1007/s10514-006-9019-2.

**Laboratory or mock-up**

- A. A. Apolinarska, M. Pacher, H. Li, et al., "Robotic assembly of timber joints using reinforcement learning," *Automation in Construction*, vol. 125, art. 103569, 2021. DOI 10.1016/j.autcon.2021.103569. Sim-to-real, force/torque-guided insertion.
- J. Kindle, M. Loetscher, A. Alessandretti, C. Cadena, M. Hutter, "Enhancing Robotic Precision in Construction: A Modular Factor Graph-Based Framework to Deflection and Backlash Compensation Using High-Accuracy Accelerometers," [arXiv:2501.14280](https://arxiv.org/abs/2501.14280); accepted to IEEE RA-L, November 2024. Uses a 700 kg tracked drilling robot identified as the Hilti Jaibot.
- K. Iturralde, M. Feucht, D. Illner, et al., "Cable-driven parallel robot for curtain wall module installation," *Automation in Construction*, vol. 138, art. 104235, 2022. DOI 10.1016/j.autcon.2022.104235. Tested in two close-to-real demonstration buildings.
- B. Chu, K. Jung, M.-T. Lim, D. Hong, "Robot-based construction automation: An application to steel beam assembly (Part I)," *Automation in Construction*, vol. 32, pp. 46–61, 2013, with Part II by K. Jung, B. Chu, D. Hong, pp. 62–79.
- P. D'Amours, S. Faucher, F. Ferland, A. Girard, "Drywall finishing with collaborative robot arm in off-site construction," *Proc. 42nd ISARC*, 2025, pp. 1567–1570. DOI 10.22260/ISARC2025/0204.

**Framing and surveys**

- N. Melenbrink, J. Werfel, A. Menges, "On-site autonomous construction robots: Towards unsupervised building," *Automation in Construction*, vol. 119, art. 103312, 2020. DOI 10.1016/j.autcon.2020.103312 — the survey to read first.
- C. Brosque, J. T. Hawkins, T. Dong, J. Örn, M. Fischer, "Comparison of on-site and off-site robot solutions to the traditional framing and drywall installation tasks," *Construction Robotics*, vol. 7, no. 1, pp. 19–39, 2023. DOI 10.1007/s41693-023-00093-8 — a process and economics evaluation on a real project.
- Z. Ren, J. I. Kim, "The Role of AI in On-Site Construction Robotics: A State-of-the-Art Review Using the Sense–Think–Act Framework," *Buildings*, vol. 15, no. 13, art. 2374, 2025 — the most recent learning-centric review.

**Within this wiki**

- [[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]] — the lineages behind these systems.
- [[05-construction-robotics/industry-deployment|Industry Deployment]] — the commercial systems that have no papers.
- [[07-research-program/paper-arc|7.1 Paper Arc §4]] — the five criteria applied in §5.
- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — the tools these tasks would be studied with, and the benchmark and dataset absences that go with them.

## 한국어

### 1. 건설 조작이 자기만의 문제인 이유

[[05-construction-robotics/assembly-fabrication|조립·제작]]은 이 도메인의 *계보*를 다룬다 —
누가 무엇을 만들었고 어느 연구 전통에서 나왔는가. 이 페이지는 다른 단면을 자른다:
**로봇의 손이 실제로 무엇을 해야 하는가**를 작업별로, 그리고 각 작업이 매니퓰레이션 트랙의
페이지들에 무엇을 요구하는지를.

공장 조작과의 차이는 건설이 막연히 더 어렵다는 것이 아니다. 구체적이며, 각 항목이 공장
로보틱스에게는 허용된 가정을 하나씩 없앤다:

| 공장의 가정 | 건설이 대신 주는 것 |
|---|---|
| 부재가 지그에 알려진 자세로 있다 | 부재는 누군가 놓은 자리에, 센티미터 오차로 있다 |
| 작업물은 강체이고 치수가 정해져 있다 | 패널은 휘고, 철근 다발은 어긋나고, 멤브레인은 늘어진다 |
| 환경이 매 사이클 같다 | 같은 작업의 두 사례가 다르고, 건물은 지어지면서 변한다 |
| 로봇이 바닥에 볼트로 고정되어 있다 | 베이스가 여기까지 이동해 왔고, 그 자세가 오차 예산의 일부다 |
| 작업 공간 안에 아무도 없다 | 다른 공종이 옆에서 일하고, 안전이 규제된다 |
| $\mu$, 질량, 기하를 안다 | 분진·습기·공차가 셋 다 불확실하게 만든다 |

1행 하나만으로도 하이브리드 위치/힘 제어가 깨진다. 그 선택 행렬은 어느 방향이 표면에
수직인지 안다고 가정하기 때문이다([[04-robotics/force-compliance-control|13. §3]]).
작은 단서가 아니라, 공장 제어기가 이전되지 않는 이유다.

### 2. 작업 매트릭스

건설 작업을 트랙의 조작 원시동작으로 분해한 것. 각 행을 명세로 읽어라 — 그 작업을 하는
프로젝트가 어느 페이지들을 깊이 필요로 할지를 말해 준다.

| 작업 | 원시동작 | 결정적 센싱 | 제어 모드 | 가장 어려운 불확실성 |
|---|---|---|---|---|
| **앵커 볼트 설치, 천장 드릴링** | 드릴, 밀기 | 위치 + 힘, 추력 | 비트 축 방향의 힘 | 추력에 의한 팔 변형, 천장 재료의 편차 |
| **패널·커튼월 설치** | 파지, 운반, 끼움 | 비전 + 힘 | 낮은 강성의 유연 끼움 | 부재가 크고 휜다, 베이스 자세 오차가 지배적 |
| **드라이월 시공** | 파지, 지지, 체결 | 비전 + 힘 | 지지는 위치, 체결은 힘 | 시트가 휜다, 머리 위 지지는 힘의 문제 |
| **드라이월 마감** | 샌딩, 긁기 | 힘 / 깊이 제어 | 표면 법선 방향의 힘 | 제거 깊이가 명세인데 밀리미터 이하다 |
| **철근 결속** | 도달, 감기, 절단 | 교차점을 찾는 비전 | 대체로 위치, 가벼운 접촉 | 메시가 비강체이고 어긋난다, 수천 번의 반복 |
| **배관·전선관 끼움** | 삽입, 정렬 | 힘 + 촉각 | 낮은 강성 임피던스 | wedging과 jamming([[04-robotics/force-compliance-control\|13. §5]]) |
| **볼트 강접합** | 정렬, 삽입, 조임 | 힘 + 토크 | 하이브리드: 가로는 위치, 축은 힘 | 부재가 무겁고, 크레인이나 베이스가 유연하다 |
| **목재 접합 조립** | 억지 끼움 삽입 | 힘/토크 | 학습 또는 유연 삽입 | 공차와 형상이 부재마다 다르다 |
| **조적, 블록 쌓기** | 파지, 놓기 | 비전 | 위치 | 접촉 문제라기보다 무게와 사이클 타임 문제 |
| **강구조 용접** | 이음선 추적 | 비전 + seam tracking | 추적된 경로를 따르는 위치 | 이음 기하가 변하고, 뜨겁고, 기준이 엄격하다 |

그 표의 두 행은 접촉이 많지 않고, 그렇게 말하는 것 자체가 요점의 일부다. 조적과 대부분의
놓기 작업은 페이로드 문제가 붙은 풀린 기하다. 도메인에는 속하지만 [[07-research-program/index|7. §7]]의
입장 시험에 따르면 이 학위논문의 핵심에는 속하지 않는다.

### 3. 사다리 — 그리고 주제 선택을 바꿔야 할 발견

이 위키는 **시뮬레이션**, **실험실 또는 목업**, **가동 중인 건설 현장**을 구분할 것을 고수한다.
접촉 다량 건설 조작에 그 구분을 적용하면 눈에 띄는 결과가 나온다.

<svg viewBox="0 0 560 232" style="max-width:100%;height:auto" role="img" aria-label="증거의 세 단계, 아래 두 칸에 대부분이 몰려 있고 가동 중 현장은 거의 비어 있다">
  <g fill="currentColor">
    <rect x="40" y="146" width="440" height="40" rx="3" fill-opacity="0.08"/>
    <rect x="88" y="98" width="392" height="40" rx="3" fill-opacity="0.16"/>
    <rect x="360" y="50" width="120" height="40" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="40" y="146" width="440" height="40" rx="3"/><rect x="88" y="98" width="392" height="40" rx="3"/><rect x="360" y="50" width="120" height="40" rx="3"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="52" y="163">시뮬레이션</text>
    <text x="52" y="178" font-size="9.5" opacity="0.75">무한한 시행, 고른 물리</text>
    <text x="100" y="115">실험실 또는 목업</text>
    <text x="100" y="130" font-size="9.5" opacity="0.75">실제 접촉, 마련된 조건 &#8212; 이 연구의 거의 전부가 여기 있다</text>
    <text x="372" y="67">가동 중 현장</text>
    <text x="372" y="82" font-size="9.5" opacity="0.75">거의 비어 있다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="208">드릴링·드라이월·철근·파사드·목재·용접을 겨냥해 찾아본 결과, 가동 중인 건설 현장에 매니퓰레이터를</text>
    <text x="20" y="224">올린 논문은 둘뿐이고 그중 하나는 2007년 것이다. 그 공백이 기회다.</text>
  </g>
</svg>

검증된 예외 둘이 두드러진다. Feng 등(2024)은 평면형 철근 결속 로봇을 철근 메시 실증
플랫폼에서 먼저 검증한 뒤 선양 훈난 과학기술도시 4기 현장에 적용했다고 보고한다. Yu 등(2007)은
굴착기 베이스 위에 커튼월 설치 로봇을 만들어 건설 현장에서 시험했다 — 제목이 그렇게 말한다 —
그러나 스무 해 가까이 된 연구다.

기술적으로 강한 나머지는 전부 실험실이나 목업에서 멈추고, "on-site"를 제목에 단 여러 논문이
본문에서는 통제된 실험실 환경에서 수행했다고 분명히 말한다. 가장 강한 천장 드릴링 결과는
실제 현장 실증이 아직 향후 과제라고 밝힌다.

> [!important] 이 발견을 어떻게 쓸 것인가
> 연구 기회로 읽되, 단계를 건너뛰어도 된다는 허가로 읽지 마라. 맨 위 칸이 비어 있는 이유는
> 그것이 정말로 어렵기 때문이다 — 출입, 안전, 공정, 그리고 기다려 주지 않는 건물. 접촉 다량
> 작업으로 가동 중인 현장에 도달한 학위논문은 거의 아무도 할 수 없는 주장을 하는 것이다.
> 목업 작업을 두고 "on-site"라고 *말하는* 학위논문은, 이 페이지가 지목하려고 존재하는 그
> 패턴에 합류하는 것이다.

### 4. 앵커 논문 — 실제로 무엇을 실증했는가로 정렬

명성이 아니라 사다리 단계로 정렬한다. 여기서는 그 순서가 중요하기 때문이다.

**가동 중인 현장에서**

- **Feng 등(2024)** — 깊이 카메라와 산업용 카메라를 결합한 2단 인식으로 철근 메시 위를 주행하는
  철근 결속 로봇. 실증 플랫폼에서 검증한 뒤 현장에 적용.
- **Yu 등(2007)** — 굴착기 베이스 위의 커튼월 설치 로봇. 현장에서 시험.

**실제 접촉, 실험실 또는 실물 크기 목업**

- **Apolinarska 등(2021)** — 목재 접합 조립. 전적으로 시뮬레이션에서 학습한 정책을 힘/토크와
  자세를 안내 삼아 실기계에 배치하고, 학습에서 보지 못한 공차와 형상 변동에도 일반화한다.
  건설 규모의 peg-in-hole이며, 이 분야가 가진 접촉 다량 학습 결과에 가장 가까운 것이다.
- **Kindle 등(RA-L 2025)** — 700 kg 궤도형 드릴링 로봇(Hilti Jaibot 플랫폼)에서의 변형·백래시 보상.
  현장 교란을 모사한 조건에서 기록한 데이터셋 일곱 개로 평가했다.
  [[04-robotics/force-compliance-control|13번]]의 컴플라이언스 문제를 건설의 언어로 진술한 것.
- **Iturralde 등(2022)** — 커튼월 모듈을 설치하는 케이블 구동 병렬 로봇. 실물에 가까운 실증
  건물 두 곳에서 시험.
- **Chu, Jung 등(2013)** — 2부작 강재 보 볼팅 시스템. 오래됐지만 볼트 접합의 정본 학술 참고다.

**결과가 아니라 틀로 읽을 것**

- **Brosque 등(2023)** 은 실제 프로젝트에서 현장 방식과 오프사이트 방식을 비교한다 — 경제성·공정
  평가이며, 조작 논문이 결코 말해 줄 수 없는 바로 그것이다.
- **Melenbrink, Werfel, Menges(2020)** 가 먼저 읽을 서베이다: 기술이 아니라 건설 작업으로
  구성되어 있고, 오프사이트가 아니라 현장 자율성으로 범위가 정해져 있으며, 그 공백 분석은
  여전히 유효하다.

> [!warning] 이 문헌의 두 가지 함정
> **보도용 시연이 결과로 인용된다.** 드라이월을 시공한다고 널리 소개된 휴머노이드는
> *관절 설계*에 관한 심사 논문을 가지고 있고, 드라이월 시연 자체는 보도 영상이다.
> **그리고 상용 시스템에는 논문이 없다.** Jaibot, TyBot, Canvas, Okibo는 제품이고 그 생산성
> 수치는 마케팅이다. 제품으로 인용하고 그렇다고 밝혀라 —
> [[05-construction-robotics/industry-deployment|산업 배치]]를 보라.

### 5. 작업 고르기, 구체적으로

[[07-research-program/paper-arc|7.1 §4]]의 다섯 기준을 §2의 매트릭스에 적용한다.

| 작업 | 접촉이 본질적? | 실재하는 공차? | 사람이 대규모로? | 실험실 반복 가능? | 실패가 견딜 만한가? |
|---|---|---|---|---|---|
| 앵커 볼트 설치 | 예 | 예, mm | 예 | 예 | 머리 위 작업 — 주의 필요 |
| 패널 끼움 | 예 | 예, mm | 예 | 예 | 예 |
| 드라이월 마감 | 예 | 예, mm 이하 깊이 | 예 | 예 | 예 |
| 철근 결속 | 부분적 | 느슨 | 예, 엄청나게 | 예 | 예 |
| 배관 삽입 | 예 | 예 | 예 | 예 | 예 |
| 조적 | 아니오 | 느슨 | 예 | 예 | 예 |
| 천장 드릴링 | 예 | 예 | 예 | 예 | 분진과 낙하물 |

패널 끼움, 드라이월 마감, 배관 삽입이 다섯 기준을 모두 통과한다. 철근 결속은 규모 기준을
압도적으로 통과하지만 접촉이 가벼워서, 훌륭한 *배치* 목표이자 약한 *접촉 조작* 기여가 된다 —
그리고 그것이 현장 검증 결과를 가진 유일한 작업이라는 점은 우연이 아니다.

### 6. 이 도메인이 매니퓰레이션 문헌에 되돌려주는 것

관계는 양방향이고, 이것이 서론에 쓸 부분이다. 건설은 일반 조작 연구가 깔끔하게 제기할 방법이
없는 문제들을 공급한다:

- **알 수 없고 변하는 마찰** — [[04-robotics/grasping|15. §2~§4]]의 모든 파지 결과가 주어진
  것으로 놓는 그 $\mu$.
- **구조 규모의 비강체 부재** — 2.4 m 시트는 강체가 아니므로 closure가 정의조차 되지 않는다.
- **로봇이 바꿔 놓아서 변한 작업 공간** — 건물이 곧 작업물이다.
- **어떤 지그도 흡수하지 않는 공차 누적** — 베이스 자세 오차, 부재 배치 오차, 시공 편차가
  모두 같은 접촉 위에 떨어진다.

각각은 도메인을 핑계 삼는 것이 아니라 방어 가능한 견고성 주장이다. [[07-research-program/index|연구 프로그램]]이
딛고 선 차이가 그것이다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 지명된 건설 작업을 원시동작·센싱·제어 모드로 대응시킨다.
- [ ] 이 분야의 논문을 시뮬레이션–실험실–현장 사다리에 놓고, 어떤 근거로 거기 놓았는지 말한다.
- [ ] 현장 검증된 접촉 결과 둘을 대고 무엇을 했는지 말한다.
- [ ] 작업 선정 다섯 기준을 적용해, 끌리는 작업 하나를 최소한 탈락시킨다.
- [ ] 건설이 일반 조작 연구에 되돌려주는 것 둘을 말한다.

### 스스로 점검

1. 공장에서라면 처리했을 패널 끼움 작업에서 하이브리드 위치/힘 제어가 왜 건설에서는 실패하는가?
2. 어떤 논문의 제목에 "on-site"가 들어 있다. 믿기 전에 무엇을 확인하는가?
3. 철근 결속은 §2에서 현장 검증 로봇이 있는 유일한 작업이다. 그런데도 왜 이 학위논문의 핵심
   기여로는 약한 선택인가?
4. 어떤 업체가 드릴링 로봇의 하루 300공을 보고한다. 문헌 검토에 어떻게 실려야 하는가?
5. 학위논문을 좁혀야 한다면 §2의 어느 두 행을 먼저 잘라내겠는가, 그리고 왜인가?

> [!tip]- 정답 · Answers
> 1. 선택 행렬이 표면에 수직이라고 *믿는* 방향에 힘 제어를 배정하는데 그 믿음이 모델에서 오기 때문이다. 지그에서는 부재가 모델이 말하는 자리에 있지만 현장에서는 1~2 cm 안쪽 어딘가에 있으므로, 힘 제어가 부분적으로 표면을 따라, 위치 제어가 부분적으로 표면 안으로 작용하게 된다 — 그 아키텍처가 막으려고 존재하는 바로 그 싸움이다([[04-robotics/force-compliance-control|13. §3]]).
> 2. 방법과 실험 절에서 작업이 실제로 어디서 이루어졌는지를 지명한 문장을 확인한다. 이 분야의 여러 논문이 제목에 "on-site"를 달고 본문에서는 개발과 검증을 통제된 실험실에서 했다고 밝힌다. 제목은 포부를 말하고, 실험 절이 증거를 말한다.
> 3. 접촉이 가볍기 때문이다. 철근 결속의 어려운 부분은 인식(어긋나는 비강체 메시 위에서 교차점 찾기), 커버리지 계획, 그리고 수천 번을 신뢰성 있게 해내는 것이다 — 훌륭한 배치·자율성 결과가 되지만 기여가 접촉에 관한 것이 되지 않는다. 입장 시험에 따르면 이 프로그램의 매니퓰레이션 핵심보다 *내비게이션·배치* 기둥에 더 기여한다.
> 4. 결과가 아니라 출처를 밝힌 제품 주장으로. Jaibot, TyBot, Canvas, Okibo는 자기 심사 논문이 없으므로 그 생산성 수치는 심사를 거치지 않은 마케팅이다. 시장이 존재하고 그 작업이 자동화할 가치가 있다는 정당한 증거이긴 하다 — 측정된 주장과는 다른 주장이다.
> 5. 조적·블록 쌓기는 접촉 본질성 기준에서 탈락하기 때문이고(페이로드가 붙은 풀린 기하다), 용접은 기준·열·자격 요건이 조작 기여와 직교하는 규제 장치 전체를 끌고 오기 때문이다. 둘을 잘라도 학위논문은 어떤 핵심 주장도 잃지 않는다.

### 출처

**현장 검증**

- R. Feng, Y. Jia, T. Wang, H. Gan, "Research on the System Design and Target Recognition Method of the Rebar-Tying Robot," *Buildings*, vol. 14, no. 3, art. 838, 2024. DOI 10.3390/buildings14030838. 오픈 액세스. 초록이 철근 메시 실증 플랫폼 검증과 이어진 선양 훈난 과학기술도시 4기 현장 적용을 명시한다.
- S. N. Yu, S. Y. Lee, C. S. Han, K. Y. Lee, S. H. Lee, "Development of the curtain wall installation robot: Performance and efficiency tests at a construction site," *Autonomous Robots*, vol. 22, no. 3, pp. 281–291, 2007. DOI 10.1007/s10514-006-9019-2.

**실험실 또는 목업**

- A. A. Apolinarska, M. Pacher, H. Li, et al., "Robotic assembly of timber joints using reinforcement learning," *Automation in Construction*, vol. 125, art. 103569, 2021. DOI 10.1016/j.autcon.2021.103569. Sim-to-real, 힘/토크 유도 삽입.
- J. Kindle, M. Loetscher, A. Alessandretti, C. Cadena, M. Hutter, "Enhancing Robotic Precision in Construction: A Modular Factor Graph-Based Framework to Deflection and Backlash Compensation Using High-Accuracy Accelerometers," [arXiv:2501.14280](https://arxiv.org/abs/2501.14280); 2024년 11월 IEEE RA-L 게재 확정. Hilti Jaibot으로 식별되는 700 kg 궤도형 드릴링 로봇을 사용한다.
- K. Iturralde, M. Feucht, D. Illner, et al., "Cable-driven parallel robot for curtain wall module installation," *Automation in Construction*, vol. 138, art. 104235, 2022. DOI 10.1016/j.autcon.2022.104235. 실물에 가까운 실증 건물 두 곳에서 시험.
- B. Chu, K. Jung, M.-T. Lim, D. Hong, "Robot-based construction automation: An application to steel beam assembly (Part I)," *Automation in Construction*, vol. 32, pp. 46–61, 2013. Part II는 K. Jung, B. Chu, D. Hong, pp. 62–79.
- P. D'Amours, S. Faucher, F. Ferland, A. Girard, "Drywall finishing with collaborative robot arm in off-site construction," *Proc. 42nd ISARC*, 2025, pp. 1567–1570. DOI 10.22260/ISARC2025/0204.

**틀과 서베이**

- N. Melenbrink, J. Werfel, A. Menges, "On-site autonomous construction robots: Towards unsupervised building," *Automation in Construction*, vol. 119, art. 103312, 2020. DOI 10.1016/j.autcon.2020.103312 — 먼저 읽을 서베이.
- C. Brosque, J. T. Hawkins, T. Dong, J. Örn, M. Fischer, "Comparison of on-site and off-site robot solutions to the traditional framing and drywall installation tasks," *Construction Robotics*, vol. 7, no. 1, pp. 19–39, 2023. DOI 10.1007/s41693-023-00093-8 — 실제 프로젝트에서의 공정·경제성 평가.
- Z. Ren, J. I. Kim, "The Role of AI in On-Site Construction Robotics: A State-of-the-Art Review Using the Sense–Think–Act Framework," *Buildings*, vol. 15, no. 13, art. 2374, 2025 — 가장 최근의 학습 중심 리뷰.

**이 위키 안에서**

- [[05-construction-robotics/assembly-fabrication|조립·제작]] — 이 시스템들 뒤의 계보.
- [[05-construction-robotics/industry-deployment|산업 배치]] — 논문이 없는 상용 시스템들.
- [[07-research-program/paper-arc|7.1 논문 arc §4]] — §5에서 적용한 다섯 기준.
- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — 이 작업들을 연구할 도구와, 그에 딸린 벤치마크·데이터셋의 부재.
