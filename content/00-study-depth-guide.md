---
title: 0. Study Depth Guide
tags: [curriculum, guide]
study-depth: Literacy
depth-goal: "Use this guide to assign the minimum depth for every topic before studying."
mastery-when: "The guide itself is not a mastery target; promote the selected contribution pages."
---

## English

This page sets the **recommended minimum depth for a construction Physical AI
researcher**. It is different from the ★·◐·○ marks in the paper list:

- **★·◐·○ = how much of that paper to read.**
- **Literacy / Working / Mastery = how well to use that knowledge.**

Every substantive page displays its recommended minimum and the condition for raising it
to Mastery. The recommendation is a starting profile, not a permanent label.

### The three depths

| Depth | Completion test | Use it for |
|---|---|---|
| **Literacy** | Explain the problem, vocabulary, inputs/outputs, central claim, evidence, and limitation | every adjacent field |
| **Working** | Select the method, follow its formulation or code, choose evaluation, and diagnose common failure | methods and system layers used in experiments |
| **Mastery** | Critique assumptions, reproduce or modify the method, design decisive experiments, and defend novelty | the thesis contribution and its closest dependency |

<svg viewBox="0 0 560 218" style="max-width:100%;height:auto" role="img" aria-label="two independent ladders: how much of a paper to read, and how well to command a topic">
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.5">
    <rect x="18" y="34" width="240" height="160" rx="4"/><rect x="282" y="34" width="258" height="160" rx="4"/>
  </g>
  <g fill="currentColor" opacity="0.10">
    <rect x="34" y="146" width="209" height="32" rx="3"/><rect x="52" y="106" width="191" height="32" rx="3"/><rect x="70" y="66" width="173" height="32" rx="3"/>
    <rect x="298" y="146" width="222" height="32" rx="3"/><rect x="316" y="106" width="204" height="32" rx="3"/><rect x="334" y="66" width="186" height="32" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.7">
    <rect x="34" y="146" width="209" height="32" rx="3"/><rect x="52" y="106" width="191" height="32" rx="3"/><rect x="70" y="66" width="173" height="32" rx="3"/>
    <rect x="298" y="146" width="222" height="32" rx="3"/><rect x="316" y="106" width="204" height="32" rx="3"/><rect x="334" y="66" width="186" height="32" rx="3"/>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="18" y="26">per PAPER: how much to read</text><text x="282" y="26">per TOPIC: how well to command it</text>
    <text x="44" y="166">&#9675; &nbsp;the note is enough</text><text x="62" y="126">&#9680; &nbsp;read the note, then skim the original</text><text x="80" y="86">&#9733; &nbsp;read the original in full</text>
    <text x="308" y="166">Literacy &#8212; explain it</text><text x="326" y="126">Working &#8212; use and diagnose it</text><text x="344" y="86">Mastery &#8212; critique and defend it</text>
    <text x="18" y="212" font-size="11" opacity="0.85">these two are independent: a Literacy topic can still contain a &#9733; paper</text>
  </g>
</svg>



> [!important] Mastery is contribution-dependent
> No fixed curriculum can declare every future thesis topic in advance. This guide assigns
> the common minimum. When a research question is selected, promote its contribution page
> and closest dependency to Mastery; do not promote an entire field.

### Two layers: recommended depth vs wiki support

`study-depth` on a page is the **recommended target** for this profile — how well *you*
should eventually command the topic. It is **not** a promise that the page alone gets you
there. Where the gap matters, pages carry a second field:

- **`wiki-support:`** — the depth this page *by itself* provides. Absent means the page
  supports its recommended depth. `wiki-support: Literacy` on a Working-recommended page
  means: this page gives you accurate reading fluency, and reaching Working requires the
  linked original sources, textbooks, or code — the page tells you which. Stating it
  explicitly is allowed even when it equals `study-depth`, and a value *above* `study-depth`
  means the page over-delivers: it will carry you past the depth this topic asks of you.

This split keeps recommendations honest without bloating every page to textbook length.

### Recommended profile

| Area | Default | Raise to Mastery when… |
|---|---:|---|
| Engineering math, linear algebra, calculus, probability, optimization | Working | the thesis contribution is mathematical, probabilistic, or optimization-based |
| Information theory | Literacy | the objective or representation claim depends on KL, entropy, mutual information, or a variational bound |
| Signal processing, state estimation, calibration, SE(3) | Working | sensing, localization, or calibration is the claimed contribution |
| Deep-learning history and ecosystem maps | Literacy | never as a whole—promote the specific method instead |
| Perception, 3D geometry, point clouds | Working | perception or geometric reconstruction carries the novelty |
| VLM | Literacy; selected encoders at Working | multimodal grounding or semantic reasoning is modified |
| VLA, imitation learning, robot learning | Working | policy learning, action representation, or data mixture carries the novelty |
| Diffusion, flow matching, world models | Literacy broadly; directly used methods at Working | the generative objective, dynamics model, or planner is modified |
| Kinematics, dynamics, planning, control, robot systems | Working | the corresponding subsystem is modified or defended as novel |
| HRI and safety | Working for deployed field systems | interaction, safety assurance, or human factors is the contribution |
| Construction lineage, labs, industry map | Literacy | these are landscape maps, not implementation methods |
| Construction task streams and deployment evaluation | Working | the selected task, workflow, or field-deployment layer carries the novelty |
| Research practice | Working | throughout the project; mastery is demonstrated through defensible research |

### How to adjust the profile

1. Begin with each page's `study-depth`.
2. When a candidate problem appears, identify its **contribution layer** and one closest
   **dependency layer**.
3. Promote the contribution layer to Mastery and the dependency to at least Working.
4. Keep the rest at Literacy unless an experiment repeatedly fails there.
5. Revisit the decision after the first baseline and failure analysis.

Example: a construction-excavator VLA thesis might use **construction deployment,
action representation, and policy learning** at Mastery; **SE(3), perception, control,
and sim-to-real** at Working; and the remaining model families at Literacy.

### Profile: construction manipulation

The table above is the common minimum. This section is the **concrete profile** for the
program in [[07-research-program/index|7. Research Program]] — a T-shape: broad literacy
across physical AI, with one deep column where the contribution lives.

<svg viewBox="0 0 560 226" style="max-width:100%;height:auto" role="img" aria-label="four bands narrowing downward from a wide literacy band to a narrow mastery band">
  <g fill="currentColor">
    <rect x="30" y="36" width="500" height="32" rx="3" fill-opacity="0.06"/>
    <rect x="90" y="68" width="380" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="150" y="100" width="260" height="32" rx="3" fill-opacity="0.20"/>
    <rect x="195" y="132" width="170" height="46" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="30" y="36" width="500" height="32" rx="3"/><rect x="90" y="68" width="380" height="32" rx="3"/><rect x="150" y="100" width="260" height="32" rx="3"/><rect x="195" y="132" width="170" height="46" rx="3"/>
  </g>
  <g fill="currentColor" text-anchor="middle">
    <text x="280" y="51" font-size="10.5">Literacy &#8212; read the field and cite it correctly</text>
    <text x="280" y="63" font-size="9" opacity="0.8">world models &#183; diffusion internals &#183; generic VLM &#183; broader RL theory</text>
    <text x="280" y="83" font-size="10.5">Working &#8212; select, follow, evaluate, diagnose</text>
    <text x="280" y="95" font-size="9" opacity="0.8">navigation &#183; SLAM &#183; estimation &#183; HRI &#183; optimization &#183; control &#183; tooling</text>
    <text x="280" y="115" font-size="10.5">Working, raised to Mastery if the thesis needs it</text>
    <text x="280" y="127" font-size="9" opacity="0.8">tactile &#183; 3D perception &#183; VLA &#183; TAMP</text>
    <text x="280" y="148" font-size="10.5">Mastery</text>
    <text x="280" y="161" font-size="9" opacity="0.8">contact-rich manipulation</text>
    <text x="280" y="173" font-size="9" opacity="0.8">force control &#183; grasping &#183; dynamics &#183; demonstration collection</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="30" y="200">The bar narrows as the depth rises. Breadth is not the sacrifice made for depth &#8212; it is what lets</text>
    <text x="30" y="216">you recognise, from inside a narrow column, that something outside it has started to matter.</text>
  </g>
</svg>

| Depth | Areas | Why it earns that depth |
|---|---|---|
| **Mastery** | contact-rich manipulation; force, impedance and admittance control; grasping; manipulator dynamics and the operational-space bridge; imitation learning as used for manipulation; **teleoperation and demonstration collection** | the contribution and its closest dependency — the claims a defense has to survive |
| **Working, raised to Mastery if the thesis needs it** | tactile and visuotactile sensing; 3D perception; VLA; task and motion planning; mobile manipulation | each becomes the contribution only if the thesis turns that way; until then, enough to use and diagnose |
| **Working** | navigation; SLAM and localization; state estimation; HRI; RL; optimization; ROS 2 and simulation tooling | supporting pillars and shared infrastructure — integration matters here, novelty does not |
| **Literacy, raised to Working on demand** | broader RL theory; generic VLM topics; world models; diffusion internals; autonomy topics outside manipulation | read them accurately, cite them correctly, and notice when one starts to matter |

> [!important] Mastery here is narrower than "manipulation"
> This profile does **not** promote all of manipulation to Mastery. Kinematics, inverse
> kinematics, and trajectory generation stay at Working: they are prerequisites to use
> fluently, not claims to defend. What is promoted is the contact-bearing core — what
> happens when the robot touches something — plus [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]],
> which is promoted only because force control is unreadable without it.

The admission test for moving anything up a row:

> **Does this directly improve the construction manipulation research question?**

If the honest answer is "it would be interesting", the answer is no.

## 한국어

이 페이지는 **건설 Physical AI 연구자에게 권장하는 최소 학습 깊이**를 정한다.
논문 목록의 ★·◐·○와는 역할이 다르다.

- **★·◐·○ = 그 논문을 얼마나 읽을 것인가**
- **Literacy / Working / Mastery = 그 지식을 어느 수준으로 사용할 것인가**

모든 주요 페이지는 권장 최소 깊이와 Mastery로 올려야 하는 조건을 표시한다.
이 값은 출발점이지 영구적인 등급이 아니다.

### 세 가지 깊이

| 깊이 | 완료 기준 | 적용 범위 |
|---|---|---|
| **Literacy · 독해** | 문제·용어·입출력·핵심 주장·근거·한계를 설명한다 | 모든 인접 분야 |
| **Working · 실무** | 방법을 선택하고 정식화/코드를 따라가며 평가와 실패 원인을 판단한다 | 실험에서 직접 쓰는 방법과 시스템 층 |
| **Mastery · 숙달** | 가정을 비판하고 재현·변형하며 결정적 실험과 novelty를 방어한다 | 논문의 기여 영역과 가장 가까운 의존 영역 |

<svg viewBox="0 0 560 218" style="max-width:100%;height:auto" role="img" aria-label="독립적인 두 사다리: 논문을 얼마나 읽는가, 주제를 얼마나 다루는가">
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.5">
    <rect x="18" y="34" width="240" height="160" rx="4"/><rect x="282" y="34" width="258" height="160" rx="4"/>
  </g>
  <g fill="currentColor" opacity="0.10">
    <rect x="34" y="146" width="209" height="32" rx="3"/><rect x="52" y="106" width="191" height="32" rx="3"/><rect x="70" y="66" width="173" height="32" rx="3"/>
    <rect x="298" y="146" width="222" height="32" rx="3"/><rect x="316" y="106" width="204" height="32" rx="3"/><rect x="334" y="66" width="186" height="32" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.7">
    <rect x="34" y="146" width="209" height="32" rx="3"/><rect x="52" y="106" width="191" height="32" rx="3"/><rect x="70" y="66" width="173" height="32" rx="3"/>
    <rect x="298" y="146" width="222" height="32" rx="3"/><rect x="316" y="106" width="204" height="32" rx="3"/><rect x="334" y="66" width="186" height="32" rx="3"/>
  </g>
  <g font-size="11.5" fill="currentColor">
    <text x="18" y="26">논문 단위: 얼마나 읽는가</text><text x="282" y="26">주제 단위: 얼마나 다루는가</text>
    <text x="44" y="166">&#9675; &nbsp;노트로 충분</text><text x="62" y="126">&#9680; &nbsp;노트를 읽고 원문은 훑기</text><text x="80" y="86">&#9733; &nbsp;원문 전체를 읽기</text>
    <text x="308" y="166">Literacy &#8212; 설명할 수 있다</text><text x="326" y="126">Working &#8212; 쓰고 진단할 수 있다</text><text x="344" y="86">Mastery &#8212; 비판하고 방어할 수 있다</text>
    <text x="18" y="212" font-size="11" opacity="0.85">둘은 독립이다: Literacy 주제 안에도 &#9733; 논문이 있을 수 있다</text>
  </g>
</svg>



> [!important] Mastery는 연구 기여에 따라 정한다
> 미래의 논문 주제를 커리큘럼이 미리 확정할 수는 없다. 이 가이드는 공통 최소값을
> 배정한다. 연구 질문이 정해지면 **기여 페이지와 가장 가까운 의존 페이지**만
> Mastery로 올리고, 분야 전체를 Mastery로 올리지 않는다.

### 두 층: 권장 깊이 vs 위키 지원 깊이

페이지의 `study-depth`는 이 프로필의 **권장 목표** — *당신*이 결국 그 주제를 어느 수준까지
다뤄야 하는가 — 다. 페이지 하나가 거기까지 데려다준다는 약속이 **아니다**. 격차가 중요한
곳에는 두 번째 필드가 붙는다:

- **`wiki-support:`** — 이 페이지가 *자체적으로* 제공하는 깊이. 없으면 페이지가 권장
  깊이를 지원한다는 뜻. Working 권장 페이지의 `wiki-support: Literacy`는: 이 페이지는
  정확한 읽기 유창성을 주고, Working 도달에는 링크된 원 자료·교재·코드가 필요하며 —
  페이지가 어떤 자료인지 알려준다는 뜻이다. `study-depth`와 같은 값을 명시해도 되고,
  `study-depth`보다 *높은* 값은 페이지가 더 준다는 뜻이다 — 이 주제가 요구하는 깊이보다
  더 멀리 데려간다.

이 분리가 모든 페이지를 교재 길이로 불리지 않으면서 권장을 정직하게 유지한다.

### 권장 프로필

| 영역 | 기본 깊이 | Mastery가 필요한 경우 |
|---|---:|---|
| 공업수학·선형대수·미적분·확률·최적화 | Working | 수학적 정식화·추정·최적화가 기여일 때 |
| 정보이론 | Literacy | KL·엔트로피·상호정보량·변분 경계가 주장에 직접 필요할 때 |
| 신호처리·상태추정·보정·SE(3) | Working | 센싱·위치추정·보정이 기여일 때 |
| 딥러닝 역사·생태계 지도 | Literacy | 전체가 아니라 실제 사용하는 방법만 승격 |
| 인식·3D 기하·포인트 클라우드 | Working | 인식이나 기하 복원이 novelty일 때 |
| VLM | Literacy, 선택한 encoder는 Working | 멀티모달 grounding이나 의미 추론을 수정할 때 |
| VLA·모방학습·로봇러닝 | Working | 정책·행동 표현·데이터 혼합이 기여일 때 |
| 디퓨전·flow matching·world model | 넓게 Literacy, 직접 쓰는 방법은 Working | 생성 목적함수·동역학 모델·planner를 수정할 때 |
| 기구학·동역학·계획·제어·로봇 시스템 | Working | 해당 subsystem이 novelty일 때 |
| HRI·안전 | 현장 배치 연구에서는 Working | 상호작용·안전 보증·human factors가 기여일 때 |
| 건설 계보·랩·산업 지도 | Literacy | 구현 방법이 아닌 분야 지도 |
| 건설 작업 스트림·현장 평가 | Working | 선택한 작업·workflow·배치 층이 기여일 때 |
| Research Practice | Working | 프로젝트 전체에서 적용하며, 숙달은 실제 연구로 증명 |

### 깊이를 조절하는 방법

1. 각 페이지의 `study-depth`에서 시작한다.
2. 연구 후보가 생기면 **기여 층**과 가장 가까운 **의존 층** 하나를 고른다.
3. 기여 층은 Mastery, 의존 층은 최소 Working으로 올린다.
4. 나머지는 실험 실패가 반복되기 전까지 Literacy로 유지한다.
5. 첫 baseline과 실패 분석 뒤 다시 조정한다.

예를 들어 건설 굴착기 VLA 논문이라면 건설 현장 평가·행동 표현·정책 학습은
Mastery, SE(3)·인식·제어·sim-to-real은 Working, 나머지 모델 계열은 Literacy가
될 수 있다.

### 프로파일: 건설 매니퓰레이션

위의 표는 공통 최소치다. 이 절은 [[07-research-program/index|7. 연구 프로그램]]의
프로그램에 대한 **구체적 프로파일**이다 — T자 형태: physical AI 전반에 걸친 넓은 Literacy,
그리고 기여가 사는 깊은 기둥 하나.

<svg viewBox="0 0 560 226" style="max-width:100%;height:auto" role="img" aria-label="넓은 Literacy 띠에서 좁은 Mastery 띠로 아래로 갈수록 좁아지는 네 개의 띠">
  <g fill="currentColor">
    <rect x="30" y="36" width="500" height="32" rx="3" fill-opacity="0.06"/>
    <rect x="90" y="68" width="380" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="150" y="100" width="260" height="32" rx="3" fill-opacity="0.20"/>
    <rect x="195" y="132" width="170" height="46" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="30" y="36" width="500" height="32" rx="3"/><rect x="90" y="68" width="380" height="32" rx="3"/><rect x="150" y="100" width="260" height="32" rx="3"/><rect x="195" y="132" width="170" height="46" rx="3"/>
  </g>
  <g fill="currentColor" text-anchor="middle">
    <text x="280" y="51" font-size="10.5">Literacy &#8212; 분야를 읽고 정확히 인용한다</text>
    <text x="280" y="63" font-size="9" opacity="0.8">월드모델 &#183; 디퓨전 내부 &#183; 일반 VLM &#183; 넓은 RL 이론</text>
    <text x="280" y="83" font-size="10.5">Working &#8212; 선택하고, 따라가고, 평가하고, 진단한다</text>
    <text x="280" y="95" font-size="9" opacity="0.8">내비게이션 &#183; SLAM &#183; 상태추정 &#183; HRI &#183; 최적화 &#183; 제어 &#183; 도구</text>
    <text x="280" y="115" font-size="10.5">Working, 논문이 요구하면 Mastery로</text>
    <text x="280" y="127" font-size="9" opacity="0.8">촉각 &#183; 3D 인식 &#183; VLA &#183; TAMP</text>
    <text x="280" y="148" font-size="10.5">Mastery</text>
    <text x="280" y="161" font-size="9" opacity="0.8">접촉 다량 매니퓰레이션</text>
    <text x="280" y="173" font-size="9" opacity="0.8">힘 제어 &#183; 파지 &#183; 동역학 &#183; 시연 수집</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="30" y="200">깊이가 올라갈수록 폭은 좁아진다. 폭은 깊이를 위해 치르는 대가가 아니다 &#8212; 좁은 기둥 안에서도</text>
    <text x="30" y="216">바깥의 무언가가 중요해지기 시작했음을 알아보게 해 주는 것이 폭이다.</text>
  </g>
</svg>

| 깊이 | 영역 | 왜 그 깊이인가 |
|---|---|---|
| **Mastery** | 접촉 다량 매니퓰레이션; 힘·임피던스·어드미턴스 제어; 파지; 매니퓰레이터 동역학과 작업 공간 다리; 조작에 쓰는 모방학습; **원격조작과 시연 수집** | 기여와 그 가장 가까운 의존 층 — 디펜스에서 살아남아야 하는 주장들 |
| **Working, 논문이 요구하면 Mastery로** | 촉각·시촉각 센싱; 3D 인식; VLA; 과제·모션 계획(TAMP); 모바일 조작 | 논문이 그쪽으로 틀 때만 기여가 된다. 그전까지는 쓰고 진단할 만큼 |
| **Working** | 내비게이션; SLAM·위치추정; 상태 추정; HRI; RL; 최적화; ROS 2와 시뮬레이션 도구 | 보조 기둥과 공용 인프라 — 여기서는 통합이 중요하고 novelty는 중요하지 않다 |
| **Literacy, 필요하면 Working으로** | 넓은 RL 이론; 일반 VLM 주제; 월드모델; 디퓨전 내부; 조작 밖의 자율성 주제 | 정확히 읽고, 정확히 인용하고, 그중 하나가 중요해지기 시작하는 순간을 알아차린다 |

> [!important] 여기서의 Mastery는 "매니퓰레이션"보다 좁다
> 이 프로파일은 매니퓰레이션 전체를 Mastery로 올리지 **않는다**. 기구학, 역기구학, 궤적
> 생성은 Working에 남는다: 유창하게 *써야 하는* 선수 지식이지 *방어할* 주장이 아니다.
> 승격되는 것은 접촉을 지는 핵심 — 로봇이 무언가에 닿을 때 일어나는 일 — 과
> [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]]이며,
> 후자는 오직 그것 없이는 힘 제어를 읽을 수 없기 때문에 승격된다.

한 칸 올리려 할 때의 입장 시험:

> **이것이 건설 조작 연구 질문을 직접 개선하는가?**

정직한 답이 "흥미로울 것 같다"라면, 답은 아니오다.

### Connections · 연결

- [[01-canonical-papers/how-to-read|How to Read Papers]] · [[01-canonical-papers/canonical-list|Canonical Paper List]] · [[08-research-radar/index|Research Radar]]
