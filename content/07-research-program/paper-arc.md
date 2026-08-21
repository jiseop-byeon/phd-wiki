---
title: 7.1 Paper Arc
tags: [research-program, guide]
study-depth: Working
wiki-support: Working
depth-goal: "Place a candidate project inside the arc, and say what it needs from the wiki and what it leaves for the next paper."
mastery-when: "This is a plan, not a method; it is revised by results rather than mastered."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — you should be able to say which paper in the arc a candidate project is,
> what it depends on, and what it deliberately postpones.
> **Working** — 후보 프로젝트가 arc의 몇 번째 논문인지, 무엇에 의존하며 무엇을 의도적으로
> 미루는지 말할 수 있어야 한다.

> [!note] Before you start · 시작 전 점검
> Read [[07-research-program/index|7. Research Program]] first — the pillars and the
> admission test defined there are what this page sequences.
> [[07-research-program/index|7. 연구 프로그램]]을 먼저 읽어라 — 거기서 정의한 기둥과 입장
> 시험을 이 페이지가 순서로 편성한다.

## English

### 1. Why an arc rather than five papers

Five unrelated competent papers and five papers that build one argument cost roughly the
same effort and are not worth the same. The arc buys three things a scattered portfolio
cannot:

- **Reuse.** Paper 3's hardware, dataset, and evaluation protocol become Paper 4's
  starting point. Scattered work re-pays the setup cost every time.
- **A defensible claim.** "I made construction robots better at contact-rich work" is a
  thesis; "I published in five areas" is a CV.
- **A place to put failures.** In an arc, a negative result is the motivation for the next
  paper. In a scattered portfolio it is a dead end.

The cost is real: an arc is harder to redirect. That is why the first paper should be the
one you can start with what you already have, and the commitment tightens later.

### 2. The arc

<svg viewBox="0 0 560 180" style="max-width:100%;height:auto" role="img" aria-label="five papers in sequence, with the last three shaded to show manipulation carrying the intellectual weight">
  <g fill="currentColor">
    <rect x="20" y="48" width="88" height="46" rx="3" fill-opacity="0.08"/>
    <rect x="126" y="48" width="88" height="46" rx="3" fill-opacity="0.10"/>
    <rect x="232" y="48" width="88" height="46" rx="3" fill-opacity="0.30"/>
    <rect x="338" y="48" width="88" height="46" rx="3" fill-opacity="0.30"/>
    <rect x="444" y="48" width="88" height="46" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.7">
    <rect x="20" y="48" width="88" height="46" rx="3"/><rect x="126" y="48" width="88" height="46" rx="3"/><rect x="232" y="48" width="88" height="46" rx="3"/><rect x="338" y="48" width="88" height="46" rx="3"/><rect x="444" y="48" width="88" height="46" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" opacity="0.6" marker-end="url(#arA)">
    <line x1="109" y1="71" x2="123" y2="71"/><line x1="215" y1="71" x2="229" y2="71"/><line x1="321" y1="71" x2="335" y2="71"/><line x1="427" y1="71" x2="441" y2="71"/>
  </g>
  <defs><marker id="arA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="64" y="36" font-size="10.5" opacity="0.75">paper 1</text><text x="170" y="36" font-size="10.5" opacity="0.75">paper 2</text><text x="276" y="36" font-size="10.5" opacity="0.75">paper 3</text><text x="382" y="36" font-size="10.5" opacity="0.75">paper 4</text><text x="488" y="36" font-size="10.5" opacity="0.75">paper 5</text>
    <text x="64" y="69">human-aware</text><text x="64" y="83">perception</text>
    <text x="170" y="69">navigation for</text><text x="170" y="83">mobile manipulation</text>
    <text x="276" y="69">core construction</text><text x="276" y="83">manipulation</text>
    <text x="382" y="69">contact-rich and</text><text x="382" y="83">learned manipulation</text>
    <text x="488" y="69">integrated</text><text x="488" y="83">system</text>
    <text x="64" y="112" font-size="10" opacity="0.8">HRI</text><text x="170" y="112" font-size="10" opacity="0.8">navigation</text><text x="276" y="112" font-size="10" opacity="0.8">manipulation</text><text x="382" y="112" font-size="10" opacity="0.8">manipulation</text><text x="488" y="112" font-size="10" opacity="0.8">all three</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="146">The first two use momentum you already have and buy the platform. The shaded three are where</text>
    <text x="20" y="162">manipulation becomes the intellectual center &#8212; that shift, not the paper count, is the dissertation.</text>
  </g>
</svg>

#### Paper 1 — Human-aware robotics

Worker-aware perception, motion or intent prediction, or safety-conscious planning.
Serves the HRI pillar and, in practice, is the paper you can start earliest, since it
depends on perception and study design rather than on a manipulation platform.

- Leans on: [[04-robotics/hri-safety|HRI & Safety]], [[05-construction-robotics/hrc-worker-centered|Worker-Centered HRC]], [[02-foundations/ml-practice|9. ML Practice]] for study design and error bars.
- Anchor reading: [[01-canonical-papers/notes/8-construction/lasota-shah|Lasota & Shah]] — and note carefully that its stronger companion result is a BMW *test environment*, not a deployed line. That distinction is the standard this arc holds itself to.
- Postpones: everything about contact.

#### Paper 2 — Navigation and mobile manipulation

Navigation, base placement, or a task-conditioned approach for a construction robot.
Serves the navigation pillar. Its real function in the arc is to **buy the platform**: by
the end, a mobile base can reach a workspace and hold a manipulation-ready pose.

- Leans on: [[04-robotics/state-estimation-slam|State Estimation & SLAM]], [[04-robotics/geometric-perception-calibration|Geometric Perception]], [[05-construction-robotics/site-perception|Site Perception]].
- Anchor reading: [[01-canonical-papers/notes/8-construction/cho-slam|Cho — construction SLAM]], [[01-canonical-papers/notes/8-construction/heap|HEAP]] as the extreme case of a mobile manipulator on a site.
- Postpones: new SLAM. The contribution is integration and task-conditioning, per the scope rule.

#### Paper 3 — Core construction manipulation

Assembly, insertion, fitting, fastening, or tool use on a real construction task. **This is
where the dissertation's center of gravity moves**, and the first paper that would be hard
for someone outside this program to have written.

- Leans on: [[04-robotics/contact-force-tactile|Contact, Force & Tactile]], [[04-robotics/force-compliance-control|Force & Compliance Control]], [[04-robotics/planning-decision-making|Planning]], [[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]], [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]].
- Anchor reading: [[01-canonical-papers/notes/8-construction/vision-guided-assembly|Vision-Guided Assembly]], [[01-canonical-papers/notes/8-construction/dry-stone-wall|Dry Stone Wall]].
- Choosing the task is the hardest decision in the arc; see §4.

#### Paper 4 — Contact-rich and learned manipulation

Tactile or force sensing, teleoperated demonstration collection, and imitation learning
applied to the Paper 3 task. Same platform, same task, harder conditions — which is
exactly why it is cheap to run and persuasive to read.

- Leans on: [[04-robotics/contact-force-tactile|Contact, Force & Tactile]], [[04-robotics/teleoperation-demonstration|Teleoperation & Demonstration Collection]] for the data pipeline, [[02-foundations/rl-basics|7. RL Basics §6]] for the imitation-versus-RL orientation.
- Anchor reading: [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]], [[01-canonical-papers/notes/4-vla/act|ACT]], [[01-canonical-papers/notes/8-construction/liang-lfd|Liang — learning from demonstration]], [[01-canonical-papers/notes/8-construction/yu-imitation|Yu — imitation]].

#### Paper 5 — Integrated human-aware mobile manipulation

Navigation, HRI, and manipulation in one real construction task. The dissertation's
demonstration: not a new component, but evidence that the components hold together under
site conditions.

- Leans on: everything above, plus [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]] and [[05-construction-robotics/sim-to-real|Sim-to-Real]].
- Anchor reading: [[01-canonical-papers/notes/8-construction/ext|ExT]] and [[01-canonical-papers/notes/4-vla/pi0|π0]] — for how integrated systems report what was tested on hardware versus in simulation.
- The failure mode to avoid: an integration paper with no claim. If it cannot state what is
  now possible that was not possible before, it is a demo, not a paper.

### 3. The alternative ordering

A second sequence puts perception first and language last:
perception for construction manipulation → contact-rich manipulation → visuotactile and
force-aware manipulation → learning from demonstration → a construction VLA driven by
natural language.

| | Arc above (HRI-first) | Alternative (perception-first) |
|---|---|---|
| Starts from | existing HRI and navigation momentum | a perception result |
| Manipulation begins at | paper 3 | paper 2 |
| Ends with | an integrated site demonstration | a language-driven system |
| Best when | there is prior work to build on and a platform to acquire | a manipulation platform is already available |

The arcs agree on the important thing — **the last three papers make manipulation the
intellectual center** — and differ on how the first two are spent. The choice should be
made on what already exists, not on which sounds better.

### 4. Choosing the Paper 3 task

Everything downstream depends on this choice, so it deserves explicit criteria. A good
core task is one where:

1. **Contact is essential**, not incidental — vision alone cannot verify success.
2. **The tolerance is real** — there is a right and a wrong outcome measurable in
   millimeters or newtons, not in a preference survey.
3. **A human currently does it** at scale, so a baseline and a motivation both exist.
4. **One instance is repeatable** in a lab, and the variation between instances is what
   makes it hard — that is the sim-to-lab-to-site ladder this wiki insists on.
5. **Failure is not catastrophic**, so real-robot experiments can actually be run.

Panel fitting, anchor-bolt fastening, drywall installation, pipe insertion, and rebar
tying all satisfy most of these; overhead drilling and cutting fail criterion 5 in most
university lab settings.

### 5. Year-by-year focus

A four-year shape, in which the research objective — not the coursework — is what each
year is judged by.

| Year | Study focus | Research objective |
|---|---|---|
| 1 | robotics math, modeling and control, C++, manipulation simulation; continue existing HRI/navigation work | **identify the concrete construction manipulation problem** the dissertation is built around |
| 2 | manipulation, manipulation learning, contact-rich tasks, teleoperation foundations | the first strong manipulation-centered contribution |
| 3 | manipulation with tactile/force, with HRI, with navigation; robot learning and VLA as needed | the strongest dissertation chapters, plus real-world deployment |
| 4 | integrated system | final publications, writing, defense |

Year 1's objective is a *decision*, not a paper — and it is the one most often skipped.
A year spent studying broadly without converging on a problem is the standard way a
four-year plan becomes a six-year one.

### 6. How to tell the arc is failing

- Two consecutive papers that do not share hardware, data, or evaluation protocol.
- A paper you cannot place in the diagram above.
- Paper 3 slipping past Year 2 — the arc has not started, only its prologue.
- An integration paper that demonstrates rather than claims.

### After reading

- [ ] Name the five papers and the pillar each serves.
- [ ] Say which paper the current project is, and what it postpones.
- [ ] Apply the five Paper-3 criteria to a candidate construction task.
- [ ] State what would have to be true for the arc to be judged as failing.

### Self-check

1. Why does the arc put the manipulation paper third rather than first?
2. Paper 4 uses the same platform and task as Paper 3. Is that a weakness?
3. A candidate core task is "robot spray-paints a wall". Test it against §4.
4. What distinguishes Paper 5 from a demo video?

> [!tip]- Answers
> 1. Because papers 1 and 2 can start with momentum and equipment that already exist, while paper 3 needs a manipulation platform, a chosen task, and contact instrumentation. Putting manipulation first risks a year with no publishable result while the platform is assembled. The order is a scheduling decision, not a statement that manipulation matters less.
> 2. No — it is the point. Sharing the platform and task makes paper 4 cheap to run and makes the comparison against paper 3 clean, so the claim "tactile/force feedback improved robustness" is measured against a baseline you own rather than against someone else's numbers on another setup.
> 3. Contact is incidental — spraying is nearly non-contact, so criterion 1 fails, and success is judged visually, which weakens criterion 2. It is a legitimate construction robotics problem but it is not a contact-rich manipulation problem, so it does not serve this program's core claim.
> 4. A claim. Paper 5 must state what is now possible that was not before, with an evaluation that could have come out the other way. Without that, integration is engineering — worth doing, not worth a chapter's novelty argument.

### Sources

- This page is a plan, not a citable result. Its anchor readings are indexed in
  [[01-canonical-papers/canonical-list|the canonical paper list]]; the task and deployment
  vocabulary comes from [[05-construction-robotics/index|Construction Robotics]].
- [[06-research-practice/research-questions-claims|Research Questions & Claims]] — how to
  turn each arc entry into a defensible claim.

## 한국어

### 1. 왜 논문 다섯 편이 아니라 arc인가

서로 무관한 준수한 논문 다섯 편과 하나의 논증을 쌓는 논문 다섯 편은 대략 같은 노력이 들지만
같은 가치가 아니다. arc는 흩어진 포트폴리오가 살 수 없는 세 가지를 산다:

- **재사용.** 3편의 하드웨어·데이터셋·평가 프로토콜이 4편의 출발점이 된다. 흩어진 연구는
  셋업 비용을 매번 다시 치른다.
- **방어 가능한 주장.** "건설 로봇이 접촉 많은 작업을 더 잘하게 만들었다"는 학위논문이고,
  "다섯 분야에 출판했다"는 이력서다.
- **실패를 둘 자리.** arc에서는 부정적 결과가 다음 논문의 동기가 된다. 흩어진 포트폴리오에서는
  막다른 길이다.

비용도 실재한다: arc는 방향을 틀기 어렵다. 그래서 첫 논문은 **이미 가진 것으로 시작할 수 있는
것**이어야 하고, 구속은 뒤로 갈수록 강해진다.

### 2. Arc

<svg viewBox="0 0 560 180" style="max-width:100%;height:auto" role="img" aria-label="순서대로 놓인 논문 다섯 편, 뒤의 세 편은 매니퓰레이션이 지적 무게를 지는 것을 음영으로 표시">
  <g fill="currentColor">
    <rect x="20" y="48" width="88" height="46" rx="3" fill-opacity="0.08"/>
    <rect x="126" y="48" width="88" height="46" rx="3" fill-opacity="0.10"/>
    <rect x="232" y="48" width="88" height="46" rx="3" fill-opacity="0.30"/>
    <rect x="338" y="48" width="88" height="46" rx="3" fill-opacity="0.30"/>
    <rect x="444" y="48" width="88" height="46" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.7">
    <rect x="20" y="48" width="88" height="46" rx="3"/><rect x="126" y="48" width="88" height="46" rx="3"/><rect x="232" y="48" width="88" height="46" rx="3"/><rect x="338" y="48" width="88" height="46" rx="3"/><rect x="444" y="48" width="88" height="46" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" opacity="0.6" marker-end="url(#arAk)">
    <line x1="109" y1="71" x2="123" y2="71"/><line x1="215" y1="71" x2="229" y2="71"/><line x1="321" y1="71" x2="335" y2="71"/><line x1="427" y1="71" x2="441" y2="71"/>
  </g>
  <defs><marker id="arAk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="64" y="36" font-size="10.5" opacity="0.75">1편</text><text x="170" y="36" font-size="10.5" opacity="0.75">2편</text><text x="276" y="36" font-size="10.5" opacity="0.75">3편</text><text x="382" y="36" font-size="10.5" opacity="0.75">4편</text><text x="488" y="36" font-size="10.5" opacity="0.75">5편</text>
    <text x="64" y="69">작업자 인지</text><text x="64" y="83">인식</text>
    <text x="170" y="69">모바일 조작을</text><text x="170" y="83">위한 내비게이션</text>
    <text x="276" y="69">핵심 건설</text><text x="276" y="83">조작</text>
    <text x="382" y="69">접촉 다량·</text><text x="382" y="83">학습 조작</text>
    <text x="488" y="69">통합</text><text x="488" y="83">시스템</text>
    <text x="64" y="112" font-size="10" opacity="0.8">HRI</text><text x="170" y="112" font-size="10" opacity="0.8">내비게이션</text><text x="276" y="112" font-size="10" opacity="0.8">매니퓰레이션</text><text x="382" y="112" font-size="10" opacity="0.8">매니퓰레이션</text><text x="488" y="112" font-size="10" opacity="0.8">셋 모두</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="146">앞의 둘은 이미 가진 관성을 쓰고 플랫폼을 산다. 음영 처리된 셋이 매니퓰레이션이 지적 중심이</text>
    <text x="20" y="162">되는 곳이다 &#8212; 논문 편수가 아니라 그 이동이 학위논문이다.</text>
  </g>
</svg>

#### 1편 — 작업자 인지 로보틱스

작업자 인지 인식, 동작·의도 예측, 또는 안전을 고려한 계획. HRI 기둥에 기여하며, 실제로는
가장 일찍 시작할 수 있는 논문이다. 조작 플랫폼이 아니라 인식과 연구 설계에 의존하기 때문이다.

- 기대는 곳: [[04-robotics/hri-safety|HRI·안전]], [[05-construction-robotics/hrc-worker-centered|작업자 중심 HRC]], 연구 설계와 오차 막대는 [[02-foundations/ml-practice|9. ML 실무]].
- 앵커 읽기: [[01-canonical-papers/notes/8-construction/lasota-shah|Lasota & Shah]] — 그리고 더 강한 후속 결과가 실제 라인이 아니라 BMW *테스트 환경*이라는 점을 정확히 기억할 것. 이 구분이 이 arc가 스스로에게 적용하는 기준이다.
- 미루는 것: 접촉에 관한 모든 것.

#### 2편 — 내비게이션과 모바일 조작

건설 로봇의 내비게이션, base placement, 또는 과제 조건부 접근. 내비게이션 기둥에 기여한다.
arc에서의 실제 기능은 **플랫폼을 사는 것**이다: 끝날 무렵 모바일 베이스가 작업 공간에
도달하고 조작 가능한 자세를 유지할 수 있어야 한다.

- 기대는 곳: [[04-robotics/state-estimation-slam|상태 추정·SLAM]], [[04-robotics/geometric-perception-calibration|기하 인식]], [[05-construction-robotics/site-perception|현장 인식]].
- 앵커 읽기: [[01-canonical-papers/notes/8-construction/cho-slam|Cho — 건설 SLAM]], 현장 모바일 매니퓰레이터의 극단 사례로서 [[01-canonical-papers/notes/8-construction/heap|HEAP]].
- 미루는 것: 새 SLAM. 범위 규칙에 따라 기여는 통합과 과제 조건부화다.

#### 3편 — 핵심 건설 조작

실제 건설 작업에서의 조립·삽입·끼움·체결·공구 사용. **여기서 학위논문의 무게 중심이
이동한다**, 그리고 이 프로그램 밖의 사람이 쓰기 어려운 첫 번째 논문이다.

- 기대는 곳: [[04-robotics/contact-force-tactile|접촉·힘·촉각]], [[04-robotics/force-compliance-control|힘·컴플라이언스 제어]], [[04-robotics/planning-decision-making|계획]], [[05-construction-robotics/assembly-fabrication|조립·제작]], [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]].
- 앵커 읽기: [[01-canonical-papers/notes/8-construction/vision-guided-assembly|비전 유도 조립]], [[01-canonical-papers/notes/8-construction/dry-stone-wall|건식 석벽]].
- 작업 선택이 arc에서 가장 어려운 결정이다. §4를 보라.

#### 4편 — 접촉 다량·학습 조작

촉각 또는 힘 센싱, 원격조작 시연 수집, 그리고 3편의 작업에 적용한 모방학습. 같은 플랫폼,
같은 작업, 더 어려운 조건 — 바로 그래서 돌리기 싸고 읽기 설득력 있다.

- 기대는 곳: [[04-robotics/contact-force-tactile|접촉·힘·촉각]], 데이터 파이프라인은 [[04-robotics/teleoperation-demonstration|원격조작과 시연 수집]], 모방 대 RL 방향 잡기는 [[02-foundations/rl-basics|7. RL 기초 §6]].
- 앵커 읽기: [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]], [[01-canonical-papers/notes/4-vla/act|ACT]], [[01-canonical-papers/notes/8-construction/liang-lfd|Liang — 시연 학습]], [[01-canonical-papers/notes/8-construction/yu-imitation|Yu — 모방]].

#### 5편 — 통합된 작업자 인지 모바일 조작

하나의 실제 건설 작업에서의 내비게이션 + HRI + 조작. 학위논문의 실증이다: 새 구성 요소가
아니라, 구성 요소들이 현장 조건에서 함께 버틴다는 증거.

- 기대는 곳: 위의 전부, 그리고 [[04-robotics/robot-systems-deployment|로봇 시스템·배치]]와 [[05-construction-robotics/sim-to-real|Sim-to-Real]].
- 앵커 읽기: [[01-canonical-papers/notes/8-construction/ext|ExT]]와 [[01-canonical-papers/notes/4-vla/pi0|π0]] — 통합 시스템이 무엇을 실기계에서, 무엇을 시뮬레이션에서 검증했다고 보고하는지의 본보기.
- 피해야 할 실패: 주장 없는 통합 논문. 전에는 불가능했고 지금은 가능한 것이 무엇인지 말하지
  못하면 그것은 논문이 아니라 데모다.

### 3. 대안 순서

두 번째 순서는 인식을 앞에, 언어를 뒤에 둔다: 건설 조작을 위한 인식 → 접촉 다량 조작 →
시촉각·힘 인지 조작 → 시연 학습 → 자연어로 구동되는 건설 VLA.

| | 위의 arc (HRI 우선) | 대안 (인식 우선) |
|---|---|---|
| 출발점 | 기존 HRI·내비게이션 관성 | 인식 결과 |
| 조작 시작 | 3편 | 2편 |
| 끝맺음 | 통합 현장 실증 | 언어 구동 시스템 |
| 유리한 조건 | 쌓을 선행 연구가 있고 플랫폼을 확보해야 할 때 | 조작 플랫폼이 이미 있을 때 |

두 arc는 중요한 지점에서 일치한다 — **뒤의 세 편이 매니퓰레이션을 지적 중심으로 만든다** —
그리고 앞의 두 편을 어디에 쓰는지에서 갈린다. 선택은 어느 쪽이 그럴듯한지가 아니라 **이미
무엇이 있는지**로 해야 한다.

### 4. 3편의 작업 고르기

이후 전부가 이 선택에 의존하므로 명시적 기준이 필요하다. 좋은 핵심 작업은:

1. **접촉이 본질적**이고 부수적이지 않다 — 비전만으로 성공을 검증할 수 없다.
2. **공차가 실재한다** — 선호도 설문이 아니라 밀리미터나 뉴턴으로 잴 수 있는 옳고 그름이 있다.
3. **지금 사람이 대규모로 하고 있다** — 베이스라인과 동기가 함께 존재한다.
4. **한 사례는 실험실에서 반복 가능**하고, 사례 간 변동이 어려움의 원천이다 — 이 위키가
   고수하는 시뮬→실험실→현장 사다리가 바로 이것이다.
5. **실패가 파국적이지 않다** — 그래야 실기계 실험을 실제로 돌릴 수 있다.

패널 끼움, 앵커 볼트 체결, 드라이월 설치, 배관 삽입, 철근 결속은 대체로 이 기준들을 만족한다.
천장 드릴링과 절단은 대학 실험실 환경에서 대체로 5번에서 걸린다.

### 5. 연도별 초점

4년 형태이며, 각 연도를 판정하는 것은 수강 과목이 아니라 연구 목표다.

| 연차 | 학습 초점 | 연구 목표 |
|---|---|---|
| 1 | 로보틱스 수학, 모델링과 제어, C++, 조작 시뮬레이션; 기존 HRI/내비게이션 연구 지속 | **학위논문이 기댈 구체적인 건설 조작 문제를 확정한다** |
| 2 | 매니퓰레이션, 조작 학습, 접촉 다량 작업, 원격조작 기초 | 첫 번째 강한 조작 중심 기여 |
| 3 | 조작 + 촉각/힘, 조작 + HRI, 조작 + 내비게이션; 필요한 만큼의 로봇러닝·VLA | 가장 강한 학위논문 장들, 그리고 실세계 배치 |
| 4 | 통합 시스템 | 최종 논문, 집필, 디펜스 |

1년차의 목표는 논문이 아니라 **결정**이며, 가장 자주 건너뛰는 것이기도 하다. 문제로 수렴하지
않은 채 넓게 공부한 1년은 4년 계획이 6년 계획이 되는 표준적인 경로다.

### 6. Arc가 실패하고 있다는 신호

- 하드웨어도, 데이터도, 평가 프로토콜도 공유하지 않는 논문이 연속 두 편.
- 위 그림 어디에도 놓을 수 없는 논문.
- 3편이 2년차를 넘겨 밀리는 것 — arc가 시작되지 않았고 서막만 있는 상태다.
- 주장하지 않고 실연만 하는 통합 논문.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 다섯 편과 각각이 기여하는 기둥을 댄다.
- [ ] 현재 프로젝트가 몇 편인지, 무엇을 미루고 있는지 말한다.
- [ ] 후보 건설 작업에 3편의 다섯 기준을 적용한다.
- [ ] arc가 실패로 판정되려면 무엇이 참이어야 하는지 말한다.

### 스스로 점검

1. arc는 왜 조작 논문을 첫 번째가 아니라 세 번째에 두는가?
2. 4편은 3편과 같은 플랫폼·같은 작업을 쓴다. 이것은 약점인가?
3. 후보 핵심 작업이 "로봇이 벽에 스프레이 도장을 한다"이다. §4로 검증하라.
4. 5편을 데모 영상과 구분하는 것은 무엇인가?

> [!tip]- 정답 · Answers
> 1. 1·2편은 이미 있는 관성과 장비로 시작할 수 있지만, 3편은 조작 플랫폼·선정된 작업·접촉 계측이 필요하기 때문이다. 조작을 맨 앞에 두면 플랫폼을 갖추는 동안 출판 가능한 결과 없이 1년을 보낼 위험이 있다. 순서는 일정 결정이지 매니퓰레이션이 덜 중요하다는 뜻이 아니다.
> 2. 아니다 — 그것이 핵심이다. 플랫폼과 작업을 공유하면 4편을 돌리는 비용이 싸지고 3편과의 비교가 깨끗해진다. 그래서 "촉각/힘 피드백이 견고성을 높였다"는 주장이 남의 셋업에서 나온 숫자가 아니라 자신이 소유한 베이스라인에 대해 측정된다.
> 3. 접촉이 부수적이다 — 도장은 거의 비접촉이므로 1번이 무너지고, 성공을 시각으로 판정하므로 2번도 약해진다. 정당한 건설 로보틱스 문제이긴 하지만 접촉 다량 조작 문제가 아니므로 이 프로그램의 핵심 주장에 기여하지 않는다.
> 4. 주장이다. 5편은 전에는 불가능했고 지금은 가능한 것을 말해야 하며, 그 평가는 반대 결과가 나올 수도 있었어야 한다. 그것이 없으면 통합은 공학이다 — 할 가치는 있지만 한 장(章)의 novelty 논증이 될 가치는 없다.

### 출처

- 이 페이지는 계획이며 인용 가능한 결과가 아니다. 앵커 읽기는
  [[01-canonical-papers/canonical-list|핵심 논문 리스트]]에 색인되어 있고, 작업·배치 용어는
  [[05-construction-robotics/index|Construction Robotics]]에서 온다.
- [[06-research-practice/research-questions-claims|연구 질문과 주장]] — arc의 각 항목을
  방어 가능한 주장으로 바꾸는 법.
