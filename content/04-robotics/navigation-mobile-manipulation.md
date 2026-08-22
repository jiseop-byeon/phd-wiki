---
title: 16. Navigation & Mobile Manipulation
tags: [robotics, navigation, mobile-manipulation]
study-depth: Working
wiki-support: Working
depth-goal: "Say what a mobile manipulator's navigation goal actually is, choose a base pose defensibly, and read a mobile-manipulation paper's error budget."
mastery-when: "The research program keeps this at Working — it is a supporting pillar, and integration rather than novelty is what it contributes."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to integrate, diagnose and evaluate. The
> [[07-research-program/index|research program]] deliberately does *not* promote this to
> Mastery: new SLAM is not the contribution.
> **Working** — 통합하고, 진단하고, 평가할 만큼. [[07-research-program/index|연구 프로그램]]은
> 의도적으로 이것을 Mastery로 올리지 *않는다*: 새 SLAM은 기여가 아니다.

> [!note] Before you start · 시작 전 점검
> You need localization and mapping ([[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]]), configuration space and planning ([[04-robotics/planning-decision-making|4. Planning & Decision-Making]]), and the manipulability ellipsoid ([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §4]]) — which turns out to be the quantity that decides where a base should stop.
> 위치 추정과 지도 작성([[04-robotics/state-estimation-slam|3. 상태 추정·위치추정·SLAM]]), 자세 공간과 계획([[04-robotics/planning-decision-making|4. 계획·의사결정]]), 그리고 가조작성 타원체([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §4]])가 필요하다 — 베이스를 어디에 세울지를 결정하는 양이 결국 그것이다.

## English

### 1. The goal is a pose, not a point

A navigation stack built for a delivery robot answers "get to this location". A mobile
manipulator needs a different answer: **get to a configuration from which the arm can do the
task**. Those come apart immediately. A base one metre from the wall may put the target
outside the arm's reach; a base flush against it may put the arm at the edge of its
workspace where the manipulability ellipsoid has collapsed
([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §4]]) and it can barely
move in the direction the task needs.

So the navigation goal is not a point on a map. It is a set of base poses from which the
whole task — not one waypoint, the whole reach — is comfortably executable, and computing
that set is the subject of §3.

This is also why the research program treats navigation as a supporting pillar. What it
must deliver is *arrival in a workable configuration*, repeatedly, on a site that changed
since yesterday. That is an integration problem with real difficulty and no need for a new
SLAM algorithm.

### 2. Reachability and capability

Start from the arm alone. For a fixed base, which end-effector poses are achievable, and
how well?

**Reachability map**: discretise the workspace into voxels and record, for each, whether the
end-effector can reach it. **Capability map** (Zacharias, Borst and Hirzinger, IROS 2007)
goes further and records *from which directions* — because reaching a point from above and
reaching it from the side are different feasibility questions, and an arm's workspace is
strongly anisotropic. Making that directional structure explicit and inspectable is the
contribution, and it is the ancestor of everything in §3.

### 3. Base placement — inverting the question

Given a task pose, where should the base stand? The standard answer is to **invert the
reachability map**: a forward map says "from this base pose, these targets are reachable";
inverting it gives a distribution over base poses from which a given target is reachable, so
you can sample and score candidates directly. That is Vahrenkamp, Asfour and Dillmann's
inverse-reachability formulation (ICRA 2013), and it is what the field cites for this
question.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="the set of valid base positions around a task target is an annulus, further cut by conditioning and by obstacles">
  <g fill="currentColor">
    <path d="M 196 116 m -94 0 a 94 94 0 1 0 188 0 a 94 94 0 1 0 -188 0 Z M 196 116 m -37 0 a 37 37 0 1 0 74 0 a 37 37 0 1 0 -74 0 Z" fill-rule="evenodd" fill-opacity="0.10"/>
    <path d="M 196 116 m -80 0 a 80 80 0 1 0 160 0 a 80 80 0 1 0 -160 0 Z M 196 116 m -51 0 a 51 51 0 1 0 102 0 a 51 51 0 1 0 -102 0 Z" fill-rule="evenodd" fill-opacity="0.22"/>
    <rect x="192" y="24" width="128" height="22" rx="2" fill-opacity="0.55"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <circle cx="196" cy="116" r="94"/><circle cx="196" cy="116" r="80"/><circle cx="196" cy="116" r="51"/><circle cx="196" cy="116" r="37"/>
  </g>
  <g fill="currentColor"><circle cx="196" cy="116" r="5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="204" y="113">task pose</text>
    <text x="330" y="40">obstacle: removes part of the set</text>
    <text x="330" y="96">outer ring: reachable but</text>
    <text x="330" y="110">poorly conditioned</text>
    <text x="330" y="136">shaded band: reachable AND</text>
    <text x="330" y="150">well conditioned &#8212; stand here</text>
    <text x="330" y="176">inner disc: too close, the arm</text>
    <text x="330" y="190">cannot fold that far</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="238">The valid set is an annulus, not a disc &#8212; and the useful part of it is narrower still. Every metre of</text>
    <text x="20" y="254">base-pose uncertainty eats into a band that was only a few tens of centimetres wide to begin with.</text>
  </g>
</svg>

Two practical points the figure is making:

- **Nearer is not better.** Too close and the arm cannot fold enough to reach; too far and it
  is extended, near-singular, and weak in exactly the direction a contact task needs
  ([[02-foundations/manipulator-kinematics-dynamics|10. §6]] on why an extended arm is also
  effectively heavier).
- **The usable band is narrow**, so base-pose error is not a rounding error — it is a
  direct consumer of the margin.

> [!note] There is no survey of this · 이 주제에는 서베이가 없다
> A search for a survey or systematic review of base placement for mobile manipulation
> found none. Do not cite one. The citable references are the primary methods —
> Zacharias et al. 2007 for capability maps, Vahrenkamp et al. 2013 for inverse
> reachability, and Makhal and Goins' Reuleaux (IRC 2018) for the open-source tooling.
> 모바일 조작의 base placement에 대한 서베이나 체계적 리뷰를 찾았으나 없었다. 없는 것을
> 인용하지 마라. 인용 가능한 것은 1차 방법들이다.

### 4. The error budget is where mobile manipulation actually differs

A fixed arm has one source of end-effector error: the arm. A mobile manipulator has at least
four, and they add at the contact:

| Source | Typical scale | Notes |
|---|---|---|
| Base localization | centimetres | worse on a site than in a mapped building |
| Base mechanical settling | millimetres | tracks and soft ground move under load |
| Arm kinematic error | sub-millimetre to millimetres | plus deflection under load ([[01-canonical-papers/notes/8-construction/kindle-jaibot\|Kindle et al.]]) |
| Workpiece position | centimetres | the part is where someone put it |

Two consequences. First, **a task with a millimetre tolerance cannot be met open-loop by a
mobile manipulator** — the budget does not close, which is why contact and vision servoing
are not optional extras but the mechanism. Second, the honest way to read a mobile
manipulation paper is to ask which of these four it measured and which it assumed away.

The reference treatment of why mobility and manipulation do not simply concatenate is
Brock, Park and Toussaint's *Mobility and Manipulation* chapter in the *Springer Handbook of
Robotics* — whole-body control, redundancy resolution, and the interaction between
navigation and manipulation constraints.

> [!warning] Another absence worth knowing
> There is **no recent survey of mobile manipulation** in the *Annual Review of Control,
> Robotics, and Autonomous Systems*, and none by the authors it is often attributed to. The
> Springer Handbook chapter (2016) remains the reference treatment despite its age. If you
> need something recent and are willing to accept a narrow scope, there is a 2025
> *Frontiers in Robotics and AI* mini-review scoped to **variable autonomy** in hazardous
> domains — which is a different subject wearing a similar name.

### 5. Localizing on a site that keeps changing

Construction breaks the assumption most localization systems rest on: that the map is
static. The building is the workpiece, so yesterday's map is wrong by construction — and
the parts that changed are the parts you are working on.

Three responses appear in the literature:

- **An external measurement device.** Ercan et al. (ISARC 2019) localize a mobile
  construction robot with a robotic total station, so end-effector accuracy survives
  repeated base repositioning. Validated in a large-scale outdoor experiment. This is the
  pragmatic answer and it comes from the same lab lineage as the In situ Fabricator.
- **Anchoring to a reference model.** SLAM2REF (Vega-Torres, Braun and Borrmann,
  *Construction Robotics*, 2024) registers LiDAR-inertial sessions against an existing
  BIM or reference point cloud, giving drift-free poses and map extension across repeat
  visits. Evaluated on the ConSLAM real-site dataset rather than in a live robot trial.
- **Accepting drift and closing the loop at the task.** If the contact stage can correct
  centimetres, localization only has to get you into the band of §3.

For the landscape, Yarovoi and Cho's 2024 review of SLAM for construction robotics
(*Automation in Construction*) is the survey that does exist here.

### 6. Reading a mobile-manipulation paper

| Question | What a vague answer hides |
|---|---|
| Was the base **repositioned** between trials, or placed once? | Placing once removes the hardest error source |
| How was the base pose measured — and by what, that the robot did not have? | External tracking makes a result a lower bound on difficulty |
| Is the task tolerance stated, and does the error budget close? | Without both, "successful" is undefined |
| Static map or changing environment? | The construction case is the second |
| Whole-body control, or navigate-then-manipulate? | Sequential is easier and far more common than the phrasing suggests |
| Benchmark: simulation, real, or both? | HomeRobot ships both; BEHAVIOR-1K is simulation only |

### After reading

- [ ] State the navigation goal for a mobile manipulator in one sentence.
- [ ] Explain why the valid base region is an annulus and why its useful part is narrower.
- [ ] List the four error sources and say which one construction makes worst.
- [ ] Name two ways to localize on a site whose map keeps changing.
- [ ] Say what does not exist in this literature, so you do not cite it.

### Self-check

1. A team parks the base as close to the wall as possible "to maximise reach". What is wrong?
2. The task needs 2 mm placement accuracy. Your base localizes to ±3 cm. What follows?
3. Why is a static-map SLAM benchmark a poor predictor of construction-site performance?
4. A paper reports 95% success on a mobile manipulation task, with base poses recorded by an
   external motion-capture system. What does the number mean?
5. You want to cite a survey of base placement. What do you do?

> [!tip]- Answers
> 1. Reach is not the binding constraint; conditioning is. Flush against the wall the arm is folded or extended near the edge of its workspace, where the manipulability ellipsoid has flattened and the arm is weak and imprecise in some direction — often the very direction the task pushes. The right target is the shaded band of §3, not the outer limit of reach.
> 2. That open-loop execution cannot meet the tolerance — a ±3 cm base error alone is fifteen times the requirement, before the arm and the workpiece contribute. Something must close the loop at the task: visual servoing onto a feature of the workpiece, or a compliant contact stage that finds the feature mechanically ([[04-robotics/force-compliance-control|13. §5]]). This is not a weakness to apologise for; it is the design.
> 3. Because it measures the wrong difficulty. A static map benchmark rewards accurate registration to a scene that stays put, while a construction site changes *because the robot and the trades are changing it*, and the changed regions are exactly the work areas. A system that scores well on the first can drift badly on the second.
> 4. That the *manipulation* worked given accurate base poses. External motion capture supplies a pose the robot would not have on a site, so the result is a lower bound on the real difficulty — the navigation and localization contribution has been measured out of the experiment. It is a legitimate way to isolate a manipulation claim, as long as the paper says so and you read it that way.
> 5. Cite the primary methods instead — Zacharias et al. 2007 for capability maps and Vahrenkamp et al. 2013 for inverse reachability — because no such survey was found to exist. Writing "no survey of this exists; the primary references are…" is accurate and shows you looked.

### Sources

- F. Zacharias, C. Borst, G. Hirzinger, "Capturing robot workspace structure: representing robot capabilities," IROS 2007, pp. 3229–3236 — the capability map.
- N. Vahrenkamp, T. Asfour, R. Dillmann, "Robot placement based on reachability inversion," ICRA 2013, pp. 1970–1975 — the standard base-placement formulation.
- A. Makhal, A. K. Goins, "Reuleaux: Robot Base Placement by Reachability Analysis," IRC 2018, pp. 137–142 ([arXiv:1710.01328](https://arxiv.org/abs/1710.01328)) — the open-source tooling.
- O. Brock, J. Park, M. Toussaint, "Mobility and Manipulation," ch. 40 in *Springer Handbook of Robotics*, 2nd ed., pp. 1007–1036, 2016 — the reference treatment.
- S. Ercan, S. Meier, F. Gramazio, M. Kohler, "Automated Localization of a Mobile Construction Robot with an External Measurement Device," ISARC 2019, pp. 929–936.
- M. A. Vega-Torres, A. Braun, A. Borrmann, "SLAM2REF: advancing long-term mapping with 3D LiDAR and reference map integration," *Construction Robotics*, vol. 8, no. 2, art. 13, 2024 ([arXiv:2408.15948](https://arxiv.org/abs/2408.15948)).
- A. Yarovoi, Y. K. Cho, "Review of simultaneous localization and mapping (SLAM) for construction robotics applications," *Automation in Construction*, vol. 162, art. 105344, 2024.
- Benchmarks: S. Yenamandra et al., "HomeRobot: Open-Vocabulary Mobile Manipulation," CoRL 2023, PMLR vol. 229, pp. 1975–2011 — **simulation and real robot**. C. Li et al., "BEHAVIOR-1K," CoRL 2022, PMLR vol. 205, pp. 80–93 — **simulation only**.

**Within this wiki**

- [[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]] — the estimation machinery
- [[05-construction-robotics/site-perception|Site Perception, Scan-to-BIM & Inspection]] — the domain's perception layer
- [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA]] — demonstration collection for mobile manipulation

## 한국어

### 1. 목표는 점이 아니라 자세다

배송 로봇용으로 만든 내비게이션 스택은 "이 위치로 가라"에 답한다. 모바일 매니퓰레이터에는
다른 답이 필요하다: **팔이 그 작업을 할 수 있는 자세(configuration)로 가라.** 이 둘은 곧바로
갈라진다. 벽에서 1 m 떨어진 베이스는 대상을 팔의 도달 범위 밖에 둘 수 있고, 벽에 바짝 붙인
베이스는 팔을 작업 공간 가장자리에 두어 가조작성 타원체가 붕괴한
([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §4]]) 자리에서 정작 작업이
필요로 하는 방향으로 거의 움직이지 못하게 만든다.

그러므로 내비게이션 목표는 지도 위의 점이 아니다. **전체 작업이** — 웨이포인트 하나가 아니라
도달 전체가 — 여유 있게 실행 가능한 베이스 자세들의 집합이고, 그 집합을 계산하는 것이 §3의
주제다.

연구 프로그램이 내비게이션을 보조 기둥으로 두는 이유이기도 하다. 그것이 내놓아야 할 것은
어제와 달라진 현장에서 *작업 가능한 자세로의 도달*을 반복적으로 해내는 것이다. 실제로 어려운
통합 문제이고, 새 SLAM 알고리즘은 필요 없다.

### 2. 도달성과 능력

팔 하나에서 시작하자. 베이스가 고정되어 있을 때 어떤 말단 자세가 달성 가능하고, 얼마나 잘
달성되는가?

**도달성 지도(reachability map)**: 작업 공간을 복셀로 나누고 각각에 말단이 도달할 수 있는지를
기록한다. **능력 지도(capability map)**(Zacharias, Borst, Hirzinger, IROS 2007)는 한 걸음 더
나아가 *어느 방향에서* 도달 가능한지를 기록한다. 어떤 점에 위에서 닿는 것과 옆에서 닿는 것은
다른 가능성 문제이고, 팔의 작업 공간은 강하게 비등방적이기 때문이다. 그 방향 구조를 명시적이고
들여다볼 수 있게 만든 것이 기여이며, §3의 모든 것의 조상이다.

### 3. Base placement — 질문 뒤집기

작업 자세가 주어졌을 때 베이스는 어디에 서야 하는가? 표준적인 답은 **도달성 지도를 뒤집는**
것이다: 순방향 지도가 "이 베이스 자세에서는 이 대상들에 닿을 수 있다"고 말한다면, 그것을
뒤집으면 주어진 대상에 닿을 수 있는 베이스 자세들의 분포가 나오고, 후보를 직접 샘플링해
점수를 매길 수 있다. Vahrenkamp, Asfour, Dillmann의 inverse-reachability 정식화(ICRA 2013)가
그것이고, 이 질문에 대해 분야가 인용하는 것이 그것이다.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="작업 대상 둘레의 유효한 베이스 위치 집합은 고리 모양이며, 조건수와 장애물이 그것을 더 잘라낸다">
  <g fill="currentColor">
    <path d="M 196 116 m -94 0 a 94 94 0 1 0 188 0 a 94 94 0 1 0 -188 0 Z M 196 116 m -37 0 a 37 37 0 1 0 74 0 a 37 37 0 1 0 -74 0 Z" fill-rule="evenodd" fill-opacity="0.10"/>
    <path d="M 196 116 m -80 0 a 80 80 0 1 0 160 0 a 80 80 0 1 0 -160 0 Z M 196 116 m -51 0 a 51 51 0 1 0 102 0 a 51 51 0 1 0 -102 0 Z" fill-rule="evenodd" fill-opacity="0.22"/>
    <rect x="192" y="24" width="128" height="22" rx="2" fill-opacity="0.55"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <circle cx="196" cy="116" r="94"/><circle cx="196" cy="116" r="80"/><circle cx="196" cy="116" r="51"/><circle cx="196" cy="116" r="37"/>
  </g>
  <g fill="currentColor"><circle cx="196" cy="116" r="5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="204" y="113">작업 자세</text>
    <text x="330" y="40">장애물: 집합의 일부를 없앤다</text>
    <text x="330" y="96">바깥 고리: 닿지만</text>
    <text x="330" y="110">조건이 나쁘다</text>
    <text x="330" y="136">음영 띠: 닿고 &#8212; 그리고 &#8212;</text>
    <text x="330" y="150">조건도 좋다. 여기 서라</text>
    <text x="330" y="176">안쪽 원: 너무 가까워</text>
    <text x="330" y="190">팔이 그만큼 접히지 못한다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="238">유효 집합은 원판이 아니라 고리이고 &#8212; 쓸 만한 부분은 그보다도 좁다. 베이스 자세 불확실성 1 m마다,</text>
    <text x="20" y="254">애초에 수십 센티미터밖에 안 되던 띠를 그만큼씩 갉아먹는다.</text>
  </g>
</svg>

그림이 말하는 실용적 요점 둘:

- **가까울수록 좋은 것이 아니다.** 너무 가까우면 팔이 충분히 접히지 못해 닿을 수 없고, 너무
  멀면 뻗은 자세라 특이점에 가깝고 하필 접촉 작업이 필요로 하는 방향으로 약하다
  ([[02-foundations/manipulator-kinematics-dynamics|10. §6]] — 뻗은 팔이 실효적으로 더 무겁기도
  한 이유).
- **쓸 만한 띠가 좁으므로**, 베이스 자세 오차는 반올림 오차가 아니라 여유를 직접 소비한다.

> [!note] 이 주제에는 서베이가 없다 · There is no survey of this
> 모바일 조작의 base placement에 대한 서베이나 체계적 리뷰를 찾았으나 **없었다.** 없는 것을
> 인용하지 마라. 인용 가능한 것은 1차 방법들이다 — 능력 지도는 Zacharias 등 2007, inverse
> reachability는 Vahrenkamp 등 2013, 오픈소스 도구는 Makhal과 Goins의 Reuleaux(IRC 2018).

### 4. 모바일 조작이 실제로 달라지는 곳은 오차 예산이다

고정된 팔은 말단 오차의 원천이 하나다: 팔. 모바일 매니퓰레이터는 최소 넷이고, 그것들이 접촉
지점에서 더해진다:

| 원천 | 통상 규모 | 비고 |
|---|---|---|
| 베이스 위치추정 | 센티미터 | 지도가 있는 건물보다 현장에서 더 나쁘다 |
| 베이스의 기계적 정착 | 밀리미터 | 궤도와 무른 지반이 하중을 받아 움직인다 |
| 팔의 기구학 오차 | 밀리미터 이하~밀리미터 | 여기에 하중 하의 변형([[01-canonical-papers/notes/8-construction/kindle-jaibot\|Kindle 등]]) |
| 작업물 위치 | 센티미터 | 부재는 누군가 놓은 자리에 있다 |

귀결 둘. 첫째, **밀리미터 공차의 작업을 모바일 매니퓰레이터가 개루프로 맞출 수 없다** — 예산이
닫히지 않는다. 접촉과 비전 서보잉이 선택적 부가물이 아니라 기제인 이유가 그것이다. 둘째, 모바일
조작 논문을 읽는 정직한 방법은 이 넷 중 무엇을 측정했고 무엇을 가정으로 없앴는지 묻는 것이다.

이동과 조작이 그냥 이어 붙는 것이 아닌 이유에 대한 기준 서술은 Brock, Park, Toussaint의
*Springer Handbook of Robotics* "Mobility and Manipulation" 장이다 — 전신 제어, 여유 자유도
해소, 그리고 내비게이션 제약과 조작 제약의 상호작용.

> [!warning] 알아 둘 또 하나의 부재
> *Annual Review of Control, Robotics, and Autonomous Systems*에 **최근의 모바일 조작 서베이가
> 없고**, 흔히 그것으로 귀속되는 저자들의 것도 없다. Springer Handbook 장(2016)이 나이에도
> 불구하고 여전히 기준 서술이다. 최근 것이 필요하고 좁은 범위를 감수할 수 있다면, **가변
> 자율성**을 다룬 2025년 *Frontiers in Robotics and AI* 미니 리뷰가 있다 — 비슷한 이름을 쓴
> 다른 주제다.

### 5. 계속 변하는 현장에서 위치 잡기

건설은 대부분의 위치추정 시스템이 딛고 선 가정을 깬다: 지도가 정적이라는 가정. 건물이
작업물이므로 어제의 지도는 구조적으로 틀려 있고 — 변한 부분이 바로 지금 작업하는 부분이다.

문헌에 나타나는 대응 셋:

- **외부 측정 장치.** Ercan 등(ISARC 2019)은 로봇 토털 스테이션으로 모바일 건설 로봇의 위치를
  잡아, 베이스를 반복해서 옮겨도 말단 정확도가 살아남게 한다. 대규모 실외 실험으로 검증했다.
  실용적인 답이고, In situ Fabricator와 같은 랩 계보에서 나왔다.
- **참조 모델에 정박하기.** SLAM2REF(Vega-Torres, Braun, Borrmann, *Construction Robotics*,
  2024)는 LiDAR-관성 세션을 기존 BIM이나 참조 포인트 클라우드에 정합해, 드리프트 없는 자세와
  반복 방문에 걸친 지도 확장을 준다. 실기계 현장 시험이 아니라 ConSLAM 실제 현장 데이터셋으로
  평가했다.
- **드리프트를 받아들이고 작업에서 루프를 닫기.** 접촉 단계가 센티미터를 교정할 수 있다면,
  위치추정은 §3의 띠 안에만 데려다주면 된다.

분야 조감으로는 Yarovoi와 Cho의 2024년 건설 로보틱스 SLAM 리뷰(*Automation in Construction*)가
여기서는 실제로 존재하는 서베이다.

### 6. 모바일 조작 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 시행 사이에 베이스를 **다시 배치했는가**, 한 번만 놓았는가? | 한 번만 놓으면 가장 어려운 오차 원천이 사라진다 |
| 베이스 자세를 무엇으로 쟀는가 — 로봇에게는 없는 무엇으로? | 외부 추적은 결과를 난이도의 하한으로 만든다 |
| 작업 공차가 명시되어 있고, 오차 예산이 닫히는가? | 둘 다 없으면 "성공"이 정의되지 않는다 |
| 정적 지도인가 변하는 환경인가? | 건설의 경우는 후자다 |
| 전신 제어인가, 이동한 뒤 조작인가? | 순차 방식이 더 쉽고, 표현이 시사하는 것보다 훨씬 흔하다 |
| 벤치마크: 시뮬레이션인가, 실제인가, 둘 다인가? | HomeRobot은 둘 다, BEHAVIOR-1K는 시뮬레이션만 |

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 모바일 매니퓰레이터의 내비게이션 목표를 한 문장으로 말한다.
- [ ] 유효 베이스 영역이 왜 고리이며 쓸 만한 부분은 왜 더 좁은지 설명한다.
- [ ] 오차 원천 넷을 대고 건설이 어느 것을 가장 나쁘게 만드는지 말한다.
- [ ] 지도가 계속 변하는 현장에서 위치를 잡는 두 방법을 댄다.
- [ ] 이 문헌에 존재하지 않는 것을 말해서, 그것을 인용하지 않는다.

### 스스로 점검

1. 어떤 팀이 "도달 범위를 최대화하려고" 베이스를 벽에 최대한 붙여 세운다. 무엇이 잘못되었는가?
2. 작업에 2 mm 배치 정확도가 필요하다. 베이스는 ±3 cm로 위치를 잡는다. 무엇이 따라 나오는가?
3. 정적 지도 SLAM 벤치마크가 왜 건설 현장 성능의 나쁜 예측자인가?
4. 어떤 논문이 모바일 조작 과제에서 95% 성공을 보고하는데, 베이스 자세는 외부 모션 캡처로
   기록했다. 그 숫자는 무엇을 뜻하는가?
5. Base placement 서베이를 인용하고 싶다. 어떻게 하겠는가?

> [!tip]- 정답 · Answers
> 1. 구속 조건은 도달 범위가 아니라 조건수다. 벽에 바짝 붙이면 팔이 접히거나 작업 공간 가장자리 가까이 뻗은 자세가 되고, 거기서는 가조작성 타원체가 납작해져 어떤 방향으로 약하고 부정확하다 — 흔히 하필 작업이 미는 그 방향이다. 목표는 도달 한계선이 아니라 §3의 음영 띠다.
> 2. 개루프 실행으로는 공차를 맞출 수 없다는 것 — ±3 cm의 베이스 오차만으로도 요구치의 열다섯 배이고, 팔과 작업물이 기여하기도 전이다. 무언가가 작업에서 루프를 닫아야 한다: 작업물의 특징에 대한 비전 서보잉이나, 특징을 기계적으로 찾아 들어가는 유연 접촉 단계([[04-robotics/force-compliance-control|13. §5]]). 변명할 약점이 아니라 그것이 설계다.
> 3. 틀린 난이도를 재기 때문이다. 정적 지도 벤치마크는 가만히 있는 장면에 정확히 정합하는 것을 보상하는데, 건설 현장은 *로봇과 다른 공종이 그것을 바꾸고 있기 때문에* 변하고, 변한 영역이 정확히 작업 영역이다. 앞의 것에서 좋은 점수를 받는 시스템이 뒤의 것에서는 크게 표류할 수 있다.
> 4. 정확한 베이스 자세가 주어졌을 때 *조작*이 동작했다는 것. 외부 모션 캡처는 현장에서 로봇이 갖지 못할 자세를 공급하므로, 결과는 실제 난이도의 하한이다 — 내비게이션과 위치추정의 기여가 실험에서 빠져 있다. 조작 주장을 분리하는 정당한 방법이다. 논문이 그렇게 밝히고 독자가 그렇게 읽는다면.
> 5. 대신 1차 방법을 인용하라 — 능력 지도는 Zacharias 등 2007, inverse reachability는 Vahrenkamp 등 2013 — 그런 서베이가 존재하지 않는 것으로 확인되었기 때문이다. "이 주제의 서베이는 없으며 1차 참고문헌은…"이라고 쓰는 것이 정확하고, 찾아봤다는 것을 보여 준다.

### 출처

- F. Zacharias, C. Borst, G. Hirzinger, "Capturing robot workspace structure: representing robot capabilities," IROS 2007, pp. 3229–3236 — 능력 지도.
- N. Vahrenkamp, T. Asfour, R. Dillmann, "Robot placement based on reachability inversion," ICRA 2013, pp. 1970–1975 — 표준적인 base placement 정식화.
- A. Makhal, A. K. Goins, "Reuleaux: Robot Base Placement by Reachability Analysis," IRC 2018, pp. 137–142 ([arXiv:1710.01328](https://arxiv.org/abs/1710.01328)) — 오픈소스 도구.
- O. Brock, J. Park, M. Toussaint, "Mobility and Manipulation," *Springer Handbook of Robotics* 2판 40장, pp. 1007–1036, 2016 — 기준 서술.
- S. Ercan, S. Meier, F. Gramazio, M. Kohler, "Automated Localization of a Mobile Construction Robot with an External Measurement Device," ISARC 2019, pp. 929–936.
- M. A. Vega-Torres, A. Braun, A. Borrmann, "SLAM2REF: advancing long-term mapping with 3D LiDAR and reference map integration," *Construction Robotics*, vol. 8, no. 2, art. 13, 2024 ([arXiv:2408.15948](https://arxiv.org/abs/2408.15948)).
- A. Yarovoi, Y. K. Cho, "Review of simultaneous localization and mapping (SLAM) for construction robotics applications," *Automation in Construction*, vol. 162, art. 105344, 2024.
- 벤치마크: S. Yenamandra et al., "HomeRobot: Open-Vocabulary Mobile Manipulation," CoRL 2023, PMLR vol. 229, pp. 1975–2011 — **시뮬레이션과 실기계 둘 다**. C. Li et al., "BEHAVIOR-1K," CoRL 2022, PMLR vol. 205, pp. 80–93 — **시뮬레이션만**.

**이 위키 안에서**

- [[04-robotics/state-estimation-slam|3. 상태 추정·위치추정·SLAM]] — 추정 기계 장치
- [[05-construction-robotics/site-perception|현장 인식·Scan-to-BIM·점검]] — 도메인의 인식 층
- [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA]] — 모바일 조작의 시연 수집
