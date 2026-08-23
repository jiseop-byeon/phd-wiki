---
title: "Robotic assembly of timber joints using reinforcement learning"
authors: Aleksandra Anna Apolinarska, Matteo Pacher, Hui Li, et al.
affiliation: ETH Zurich (Gramazio Kohler Research), Autodesk Research
venue: Automation in Construction
year: 2021
doi: https://doi.org/10.1016/j.autcon.2021.103569
tags: [paper, construction, manipulation, sim-to-real, reinforcement-learning]
status: note-complete
last_verified: 2026-08-21
study-depth: Mastery
wiki-support: Literacy
depth-goal: "Critique the assumptions, reproduce or modify the method, and defend what its sim-to-real claim does and does not establish."
mastery-when: "Already at Mastery — this is the closest published result to the dissertation's core contribution."
---

**Apolinarska et al., *Automation in Construction* vol. 125, art. 103569, 2021** — [DOI 10.1016/j.autcon.2021.103569](https://doi.org/10.1016/j.autcon.2021.103569)

> [!note] Math on-ramp · 수학 준비물
> This is construction-scale peg-in-hole, so the prerequisites are the insertion ones: the wrench $\mathcal{F}$ and $\tau = J^\top\mathcal{F}$ ([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §3]]), and wedging versus jamming ([[04-robotics/force-compliance-control|13. §5]]). On the learning side, off-policy actor-critic ([[02-foundations/rl-basics|7. RL Basics §4]]) and the sim-to-real parameter gap ([[02-foundations/manipulator-kinematics-dynamics|10. §7]]).
> 건설 규모의 peg-in-hole이므로 선수 지식도 삽입의 것이다: 렌치 $\mathcal{F}$와 $\tau = J^\top\mathcal{F}$([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §3]]), 그리고 wedging 대 jamming([[04-robotics/force-compliance-control|13. §5]]). 학습 쪽은 오프폴리시 actor-critic([[02-foundations/rl-basics|7. RL 기초 §4]])과 sim-to-real 파라미터 격차([[02-foundations/manipulator-kinematics-dynamics|10. §7]]).

## English

**One-line summary**: A control policy trained entirely in simulation inserts a timber element into its mating joint on a real robot, guided by force/torque and pose, and generalises to tolerances and shape variations it never saw in training.

### Context

Architectural robotic fabrication has a long lineage of *placing* elements accurately —
that is the Gramazio Kohler line in
[[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]]. Placing is a
positioning problem, and it is solved by knowing where things are.

Timber **joinery** is a different problem. The paper's task is the **lap joint** — the
abstract reads "exemplified by assembly of lap joints for custom timber frames" — where a
member is slid into its mating counterpart across two bearing faces. The parts touch before
they are seated, the contact forces depend on misalignment, and the wood's dimensions vary
piece to piece because it is wood. That is the situation
[[04-robotics/force-compliance-control|13. §5]] describes — insertion, with wedging and
jamming available as failure modes — at building scale rather than at connector scale.

This paper is, as far as this wiki's survey found, **the closest published result to
contact-rich manipulation learning in construction**. That is why it sits at ★.

### Method

> [!tip] Key intuition
> Do not plan the insertion; learn a policy that reacts to what the joint is telling you.
> The force/torque reading during contact is a measurement of the misalignment, so a policy
> conditioned on it can correct errors that a position plan could not have anticipated.

<svg viewBox="0 0 560 234" style="max-width:100%;height:auto" role="img" aria-label="the policy is trained entirely in simulation and deployed on real hardware, with generalization tested on variations absent from training">
  <g fill="currentColor">
    <rect x="30" y="46" width="180" height="76" rx="4" fill-opacity="0.14"/>
    <rect x="350" y="46" width="180" height="76" rx="4" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="30" y="46" width="180" height="76" rx="4"/><rect x="350" y="46" width="180" height="76" rx="4"/>
  </g>
  <g stroke="currentColor" stroke-width="4" fill="none" opacity="0.85" marker-end="url(#arAp)">
    <line x1="216" y1="84" x2="342" y2="84"/>
  </g>
  <defs><marker id="arAp" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="120" y="70">simulation</text>
    <text x="120" y="90" font-size="10" opacity="0.85">the policy is trained here</text>
    <text x="120" y="108" font-size="10" opacity="0.85">&#8212; entirely</text>
    <text x="440" y="70">real hardware</text>
    <text x="440" y="90" font-size="10" opacity="0.85">the policy is deployed here</text>
    <text x="440" y="108" font-size="10" opacity="0.85">and tested here</text>
    <text x="279" y="76" font-size="10" opacity="0.85">transfer</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="156">Read the arrow direction, not just its existence. No real-robot training happened, so every real</text>
    <text x="20" y="172">success is a transfer result rather than a fine-tuning result &#8212; a stronger claim, and a rarer one.</text>
    <text x="20" y="196">And the generalization is stated over the right axis: tolerances and shape variations that were</text>
    <text x="20" y="212">absent from training, which is exactly what varies between two pieces of real timber.</text>
  </g>
</svg>

- **Signals**: robot movements are guided by **force/torque and pose data** while inserting
  a timber element into its mating counterpart. Force is not a monitor here — it is the
  input the policy acts on.
- **Learning**: an adapted **Ape-X DDPG** — distributed, off-policy actor-critic — trains
  the control policy.
- **Training location**: the policy is trained **entirely in simulation**.
- **Deployment**: it is then deployed successfully on the real system.

### Results

The result to hold onto is the generalisation statement, which the abstract makes directly:
the policy also generalises to situations in the real world **not seen in training, such as
tolerances and shape variations**.

That axis is the right one for this domain. Two pieces of timber cut to the same drawing
differ, and a policy that only worked at the tolerance it trained on would be a laboratory
curiosity. Generalising over tolerance is the difference between a demonstration and a
method.

> [!question] Reading the claim · 주장 읽는 법
> Two things to keep straight. **First, this is laboratory sim-to-real, not a construction
> site** — real hardware and real timber, in a controlled setting, which is the middle rung
> of [[05-construction-robotics/construction-manipulation|9. §3]]. **Second, "trained
> entirely in simulation" is a stronger claim than it looks**: there is no real-robot
> fine-tuning stage absorbing the reality gap, so the transfer is carrying the whole load.
> Compare [[01-canonical-papers/notes/8-construction/ext|ExT]], where the pretrained policy
> does the hardware transfer and the fine-tuning results are simulation studies — the same
> distinction, read the same way.
> 두 가지를 구분해 두어라. **첫째, 이것은 실험실 sim-to-real이지 건설 현장이 아니다** — 실제
> 하드웨어와 실제 목재를, 통제된 환경에서. [[05-construction-robotics/construction-manipulation|9. §3]]의
> 중간 단계다. **둘째, "전적으로 시뮬레이션에서 학습"은 보이는 것보다 강한 주장이다**:
> reality gap을 흡수하는 실기계 파인튜닝 단계가 없으므로 전이가 부하 전체를 지고 있다.
> 사전학습 정책이 실기계 전이를 하고 파인튜닝 결과는 시뮬 연구인
> [[01-canonical-papers/notes/8-construction/ext|ExT]]와 비교하라 — 같은 구분, 같은 독법이다.

### Limitations & critique

- **Check the platform's control mode in the paper's appendix** before building on this:
  whether the arm is torque-controlled or position-controlled changes what "force-guided"
  means ([[04-robotics/force-compliance-control|13. §2]]), and the policy was trained
  entirely in simulation, so the transfer story depends on it.
- **One joint family.** Timber joinery has a specific geometry; the method's reach across
  other construction insertions — pipe, panel, bolted connections — is an open question,
  not a demonstrated one.
- **Simulation fidelity is the whole dependency.** Training entirely in simulation means the
  contact model in the simulator is doing the work, and wood's compliance and friction are
  not the easiest things to simulate faithfully.
- **Lab, not site.** No base-pose error, no dust, no as-built deviation, no coworkers — the
  five things [[05-construction-robotics/construction-manipulation|9. §1]] says construction
  adds.

### Impact & follow-ups

For this wiki's [[07-research-program/index|research program]] this is the single most
directly relevant published result: the same problem shape as Paper 3 and Paper 4 of the
[[07-research-program/paper-arc|arc]], solved once, in a lab, on one joint family. The
obvious continuations — force-guided insertion on a different construction joint, with a
mobile base contributing pose error, or with tactile sensing added to the force channel —
are exactly the gaps the arc is built around.

### Connections

- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — the task matrix this sits in, and the evidence ladder
- [[04-robotics/force-compliance-control|13. Force & Compliance Control §5]] — insertion, wedging and jamming
- [[01-canonical-papers/notes/8-construction/ext|ExT]] — the same sim-to-real reading discipline in excavation
- [[05-construction-robotics/sim-to-real|Sim-to-Real for Field Robots]] — what transfer claims require

### After reading

- [ ] Say why timber joinery is an insertion problem and not a placement problem.
- [ ] State what "trained entirely in simulation" rules out, and why that makes the claim stronger.
- [ ] Name the generalisation axis and say why it is the right one for this domain.
- [ ] Place this paper on the simulation–lab–site ladder and defend the placement.

## 한국어

**한 줄 요약**: 전적으로 시뮬레이션에서 학습한 제어 정책이 힘/토크와 자세를 안내 삼아 실제 로봇에서 목재 부재를 짝 접합부에 삽입하며, 학습에서 본 적 없는 공차와 형상 변동에도 일반화한다.

### 배경

건축 로봇 제작에는 부재를 정확히 *놓는* 긴 계보가 있다 —
[[05-construction-robotics/assembly-fabrication|조립·제작]]의 Gramazio Kohler 라인이 그것이다.
놓기는 위치 문제이고, 무엇이 어디 있는지 알면 풀린다.

목재 **접합**은 다른 문제다. 논문의 과제는 **겹침 이음**(lap joint)이고 — 초록은 "맞춤형 목조
프레임의 겹침 이음 조립으로 예시한다"고 쓴다 — 부재가 두 접촉면을 따라 짝 부재에 미끄러져
들어간다. 부재들이 안착하기 전에 닿고, 접촉력이 정렬 오차에 의존하며, 나무이기 때문에
치수가 부재마다 다르다.
[[04-robotics/force-compliance-control|13. §5]]가 묘사하는 상황 — 삽입, 그리고 실패 모드로
준비된 wedging과 jamming — 이 커넥터 규모가 아니라 건물 규모에서 벌어지는 것이다.

이 논문은, 이 위키가 조사한 범위에서 **건설에서의 접촉 다량 조작 학습에 가장 가까운 발표된
결과**다. ★인 이유가 그것이다.

### 방법

> [!tip] 핵심 직관
> 삽입을 계획하지 말고, 접합부가 말해 주는 것에 반응하는 정책을 학습하라. 접촉 중의 힘/토크
> 측정값이 곧 정렬 오차의 측정이므로, 그것을 조건으로 하는 정책은 위치 계획이 예상할 수
> 없었던 오차를 교정할 수 있다.

<svg viewBox="0 0 560 234" style="max-width:100%;height:auto" role="img" aria-label="정책은 전적으로 시뮬레이션에서 학습되고 실제 하드웨어에 배치되며, 학습에 없던 변동으로 일반화가 검증된다">
  <g fill="currentColor">
    <rect x="30" y="46" width="180" height="76" rx="4" fill-opacity="0.14"/>
    <rect x="350" y="46" width="180" height="76" rx="4" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="30" y="46" width="180" height="76" rx="4"/><rect x="350" y="46" width="180" height="76" rx="4"/>
  </g>
  <g stroke="currentColor" stroke-width="4" fill="none" opacity="0.85" marker-end="url(#arApk)">
    <line x1="216" y1="84" x2="342" y2="84"/>
  </g>
  <defs><marker id="arApk" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="120" y="70">시뮬레이션</text>
    <text x="120" y="90" font-size="10" opacity="0.85">정책이 여기서 학습된다</text>
    <text x="120" y="108" font-size="10" opacity="0.85">&#8212; 전적으로</text>
    <text x="440" y="70">실제 하드웨어</text>
    <text x="440" y="90" font-size="10" opacity="0.85">정책이 여기 배치되고</text>
    <text x="440" y="108" font-size="10" opacity="0.85">여기서 검증된다</text>
    <text x="279" y="76" font-size="10" opacity="0.85">전이</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="156">화살표가 있다는 것만이 아니라 방향을 읽어라. 실기계 학습이 전혀 없었으므로, 실제에서의 모든</text>
    <text x="20" y="172">성공은 파인튜닝 결과가 아니라 전이 결과다 &#8212; 더 강한 주장이고, 더 드문 주장이다.</text>
    <text x="20" y="196">그리고 일반화가 옳은 축에서 진술된다: 학습에 없던 공차와 형상 변동 &#8212; 실제 목재 두 조각</text>
    <text x="20" y="212">사이에서 달라지는 것이 정확히 그것이다.</text>
  </g>
</svg>

- **신호**: 목재 부재를 짝 부재에 삽입하는 동안 로봇의 운동이 **힘/토크와 자세 데이터**로
  안내된다. 여기서 힘은 감시 장치가 아니라 정책이 그 위에서 행동하는 입력이다.
- **학습**: 변형한 **Ape-X DDPG** — 분산 오프폴리시 actor-critic — 로 제어 정책을 학습한다.
- **학습 장소**: 정책은 **전적으로 시뮬레이션에서** 학습된다.
- **배치**: 그다음 실제 시스템에 성공적으로 배치된다.

### 결과

붙잡아 둘 결과는 초록이 직접 말하는 일반화 진술이다: 정책이 **학습에서 보지 못한, 공차와
형상 변동 같은** 실세계 상황에도 일반화한다는 것.

이 도메인에서는 그 축이 옳은 축이다. 같은 도면으로 자른 목재 두 조각은 서로 다르고, 학습한
공차에서만 동작하는 정책은 실험실의 진기한 물건일 뿐이다. 공차를 가로질러 일반화하는 것이
실증과 방법의 차이다.

> [!question] 주장 읽는 법 · Reading the claim
> 두 가지를 구분해 두어라. **첫째, 이것은 실험실 sim-to-real이지 건설 현장이 아니다** — 실제
> 하드웨어와 실제 목재를, 통제된 환경에서.
> [[05-construction-robotics/construction-manipulation|9. §3]]의 중간 단계다.
> **둘째, "전적으로 시뮬레이션에서 학습"은 보이는 것보다 강한 주장이다**: reality gap을
> 흡수하는 실기계 파인튜닝 단계가 없으므로 전이가 부하 전체를 지고 있다. 사전학습 정책이
> 실기계 전이를 하고 파인튜닝 결과는 시뮬 연구인 [[01-canonical-papers/notes/8-construction/ext|ExT]]와
> 비교하라 — 같은 구분, 같은 독법이다.
> This is laboratory sim-to-real, not a site; and "trained entirely in simulation" means no
> real-robot fine-tuning absorbed the reality gap.

### 한계와 비판

- 여기서 확인한 출처들에는 **로봇 플랫폼이 명시되어 있지 않다.** 팔이 토크 제어인지 위치
  제어인지가 "힘으로 안내되는"의 의미를 바꾸므로 중요하다([[04-robotics/force-compliance-control|13. §2]]).
  이 위에 무언가를 쌓기 전에 논문에서 확인하라.
- **접합 계열 하나.** 목재 접합에는 특정한 기하가 있다. 다른 건설 삽입 — 배관, 패널, 볼트
  접합 — 으로의 확장은 실증된 것이 아니라 열린 질문이다.
- **시뮬레이션 충실도가 의존성 전부다.** 전적으로 시뮬레이션에서 학습한다는 것은 시뮬레이터의
  접촉 모델이 그 일을 다 한다는 뜻이고, 나무의 컴플라이언스와 마찰은 충실하게 시뮬레이션하기
  쉬운 축에 들지 않는다.
- **현장이 아니라 실험실.** 베이스 자세 오차도, 분진도, 시공 편차도, 동료 작업자도 없다 —
  [[05-construction-robotics/construction-manipulation|9. §1]]이 건설이 더한다고 말하는 다섯 가지.

### 영향과 후속 연구

이 위키의 [[07-research-program/index|연구 프로그램]]에는 가장 직접적으로 관련된 발표 결과다:
[[07-research-program/paper-arc|arc]]의 3편·4편과 같은 문제 형태를, 실험실에서, 하나의 접합
계열에 대해 한 번 푼 것. 명백한 연장 — 다른 건설 접합에서의 힘 유도 삽입, 자세 오차를 보태는
모바일 베이스와 함께, 또는 힘 채널에 촉각을 더해서 — 이 정확히 arc가 딛고 선 공백들이다.

### 연결

- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 이것이 놓이는 작업 매트릭스와 증거 사다리
- [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어 §5]] — 삽입, wedging과 jamming
- [[01-canonical-papers/notes/8-construction/ext|ExT]] — 굴착에서의 같은 sim-to-real 독법
- [[05-construction-robotics/sim-to-real|필드 로봇 Sim-to-Real]] — 전이 주장에 필요한 것

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 목재 접합이 왜 놓기 문제가 아니라 삽입 문제인지 말한다.
- [ ] "전적으로 시뮬레이션에서 학습"이 무엇을 배제하며 그것이 왜 주장을 강하게 만드는지 말한다.
- [ ] 일반화의 축을 대고 그것이 왜 이 도메인에 옳은 축인지 말한다.
- [ ] 이 논문을 시뮬–실험실–현장 사다리에 놓고 그 배치를 방어한다.
