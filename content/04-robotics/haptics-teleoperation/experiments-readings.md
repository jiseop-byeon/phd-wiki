---
title: 24.6 Experiments & Reading Map
tags: [haptics, research-practice, reading-guide]
study-depth: Working
wiki-support: Working
depth-goal: "Design a haptics study whose manipulation, measurements, statistical unit, safety controls, and claims line up."
mastery-when: "Master psychometric/statistical models and protocol validation when human evidence carries the thesis claim."
---

## English

### 1. From an idea to a claim

Write the causal chain before building the interface:

$$\text{actuator command}\rightarrow\text{delivered mechanical stimulus}\rightarrow\text{perception/action}\rightarrow\text{task outcome}.$$

Each arrow needs a measurement. A motor command is not a measured skin stimulus; a questionnaire is not controller performance; faster completion does not identify which cue caused the improvement. A strong study combines physical calibration, behavioral outcomes, and subjective reports.

### 2. Minimal protocol

1. **Question and estimand:** “Does shear cue A reduce peak contact force relative to vibration B for novice operators?” is testable; “Is haptics better?” is not.
2. **Participants and exclusions:** population, handedness if relevant, sensorimotor conditions, prior experience, stopping criteria.
3. **Conditions:** feedback mode, delay, gain, task difficulty, and any secondary workload.
4. **Design:** within-subject designs reduce between-person variance; counterbalance order and include enough practice to separate learning from treatment.
5. **Primary outcome:** choose before seeing results—peak force, path error, success, time, detection threshold, or calibrated confidence.
6. **Instrumentation:** synchronize haptic state, command, measured force, events, video, and survey identifiers; document clocks and missing packets.
7. **Analysis unit:** trials nested within participants are not independent participants. Report participant count, repetitions, exclusions, uncertainty, and effect size.
8. **Ethics and safety:** informed consent, voluntary withdrawal, privacy/de-identification, fatigue breaks, hardware stops, and incident handling belong in the design, not an appendix added later.

NASA-TLX measures six self-reported workload dimensions—mental, physical, temporal demand, perceived performance, effort, and frustration. It complements objective data; it does not reveal the physical cause of workload. Use the official scoring procedure appropriate to raw or weighted TLX and report which variant was used.

### 3. Evidence ladder

| Evidence | Supports | Does not yet support |
|---|---|---|
| actuator bench response | delivered device dynamics | human detectability or usefulness |
| psychophysical threshold | cue detectability under tested conditions | better task control |
| controlled task improvement | causal effect in that protocol | field deployment generality |
| representative workload study | performance under a closer context | long-term adoption or safety |
| field/longitudinal study | operational behavior over time | mechanism without additional controls |

### 4. Annotated reading sequence

1. **Hannaford & Okamura, “Haptics,” Springer Handbook of Robotics, 2nd ed., 2016.** The compact field map: human sensing → device design → rendering → stability → tactile displays. [Official chapter page](https://handbookofrobotics.org/view-chapter/42), [DOI](https://doi.org/10.1007/978-3-319-32552-1_42).
2. **Hayward & MacLean, “Do It Yourself Haptics: Part I,” IEEE RAM 14(4), 2007.** The best hardware-to-software bridge: transducers, impedance/admittance, DC motors, mechanisms, quantization, real-time loops, and practical limitations. [DOI](https://doi.org/10.1109/M-RA.2007.907921).
3. **MacLean, “Haptic Interaction Design for Everyday Interfaces,” RHFE 4(1), 2008.** Read for active touch, multisensory attention, haptic icons, shared control, and why technical realism is not the same as usefulness. [DOI](https://doi.org/10.1518/155723408X342826).
4. **Weir & Colgate, “Stability of Haptic Displays.”** Read the virtual-wall energy derivation, Z-width, quantization, virtual coupling, and PO/PC sections; treat later circuit implementations as specialized depth.
5. **Gillespie & Cutkosky, “Stable User-Specific Haptic Rendering of the Virtual Wall,” ASME IMECE, 1996.** A sampled, switched wall is not merely an LTI spring. The half-sample predictor and threshold-crossing correction depend on a limited high-frequency human/device model; the early experiment was qualitative. [DOI](https://doi.org/10.1115/IMECE1996-0362).
6. **Hannaford & Ryu, “Time-Domain Passivity Control of Haptic Interfaces,” IEEE TRA 18(1), 2002.** Follow the power sign, energy observer, and adaptive dissipative element. The method avoids an exact environment model but still faces noise, zero velocity, saturation, and performance tradeoffs. [DOI](https://doi.org/10.1109/70.988969).
7. **Raju, Verghese & Sheridan, “Design Issues in 2-Port Network Models of Bilateral Remote Manipulation,” ICRA 1989.** A classic bridge from desired port impedances and human/task models to stable gain selection. Its guarantee is over the specified passive termination class and model assumptions. [DOI](https://doi.org/10.1109/ROBOT.1989.100162).
8. **Colonnese & Okamura, “Stability and quantization-error analysis of haptic rendering of virtual stiffness and damping,” IJRR 35(9):1103–1120, 2016** (online 2015). The one paper that puts sampling, position quantization, time delay, and the velocity-estimate low-pass filter into a single one-DOF model and derives the tradeoffs between them, including sufficient conditions for quantization-error passivity and necessary conditions for the absence of (malicious- and uncoupled-touch) limit cycles. Verified on a Phantom Premium 1.5; the abstract states no numerical result. Cite the volume, not the year alone — it appeared online in 2015 and in print in 2016. [DOI](https://doi.org/10.1177/0278364915596234).

### 5. How the supplied course materials were selected

| Local material class | Public learning use |
|---|---|
| syllabus and lecture decks | track scope, prerequisite map, concepts, and version caveats |
| MATLAB templates and Jacobian script | original derivations and implementation checklist; no submitted solution copied |
| Hapkit slides and mechanical files | transmission and sensing reasoning in 24.3–24.4; build instructions and original files are not published |
| assignments and student drafts | identify required competencies and common mistakes; no answer key or personal work published |
| project options/rubric | transferable project-design and evaluation criteria; private contacts and unverified claims excluded |
| consent, recruitment, pre/post surveys | ethics, eligibility, workload, privacy, and measurement design; no form copied or treated as a reusable approval |
| licensed readings | annotated concepts and official DOI/publisher links; PDFs remain private |

The packet covers the first half of a full haptics course particularly well. It does not contain all later lecture/lab materials named in the syllabus—such as the complete CHAI3D, advanced teleoperation, and ROS sequence—so this guide does not reconstruct those lectures or claim to cover them.

> [!question]- Self-check · Answer
> **A within-subject study has 20 people and 30 trials per person. Is $n=600$?** Not for a participant-level treatment claim. Trials are nested/repeated observations. Analyze that dependence, for example with participant-level summaries or a hierarchical/mixed model; report both 20 participants and 600 trials.

## 한국어

### 1. 아이디어에서 주장까지

인터페이스를 만들기 전에 인과 사슬을 먼저 쓴다.

$$\text{액추에이터 명령}\rightarrow\text{실제 전달된 역학 자극}\rightarrow\text{지각·행동}\rightarrow\text{과제 결과}.$$

화살표마다 측정이 필요하다. 모터 명령은 측정된 피부 자극이 아니고, 설문은 제어기 성능이 아니며, 수행 시간이 줄었다는 것만으로 어떤 cue가 그 개선을 일으켰는지 알 수 없다. 강한 연구는 물리적 보정, 행동 결과, 주관 보고 셋을 함께 놓는다.

### 2. 최소 프로토콜

1. **질문과 estimand:** "전단 cue A가 초보 조작자에게서 진동 B 대비 최대 접촉력을 줄이는가"는 검정 가능하고, "햅틱이 더 나은가"는 아니다.
2. **참가자와 제외:** 모집단, 필요하면 손잡이, 감각운동 조건, 사전 경험, 중단 기준.
3. **조건:** 피드백 방식, 지연, 이득, 과제 난이도, 부가 workload.
4. **설계:** within-subject는 사람 간 분산을 줄인다. 순서를 counterbalance하고, 학습을 처치와 분리할 만큼 연습을 넣는다.
5. **주 결과 지표:** 결과를 보기 전에 고른다 — 최대 힘, 경로 오차, 성공, 시간, 검출 임계값, 또는 보정된 확신도.
6. **계측:** 햅틱 상태, 명령, 측정된 힘, 이벤트, 영상, 설문 식별자를 동기화한다. 시계와 유실 패킷을 문서화한다.
7. **분석 단위:** 참가자 안에 nested된 trial은 독립 참가자가 아니다. 참가자 수, 반복 수, 제외, 불확실성, 효과 크기를 보고한다.
8. **윤리와 안전:** 사전 동의, 자발적 철회, 개인정보 비식별, 피로 휴식, 하드웨어 정지, 사고 처리는 나중에 붙이는 부록이 아니라 설계에 속한다.

NASA-TLX는 정신적·신체적·시간적 요구, 지각된 수행, 노력, 좌절의 여섯 자기보고 workload 차원을 잰다. 객관 데이터를 보완할 뿐 workload의 물리적 원인을 드러내지는 않는다. raw와 weighted 중 해당하는 공식 채점 절차를 쓰고 어느 쪽을 썼는지 보고한다.

### 3. 증거의 사다리

| 증거 | 지지하는 것 | 아직 지지하지 못하는 것 |
|---|---|---|
| 액추에이터 벤치 응답 | 전달된 장치 동역학 | 사람의 검출 가능성이나 유용성 |
| 심리물리 임계값 | 시험한 조건에서 cue의 검출 가능성 | 더 나은 과제 제어 |
| 통제된 과제 개선 | 그 프로토콜 안에서의 인과 효과 | 현장 배치로의 일반화 |
| 대표성 있는 workload 연구 | 더 가까운 맥락에서의 수행 | 장기 채택이나 안전 |
| 현장·종단 연구 | 시간에 걸친 운용 행동 | 추가 통제 없이는 기전 |

### 4. 주석 달린 읽기 순서

1. **Hannaford & Okamura, "Haptics," Springer Handbook of Robotics 2판, 2016.** 압축된 분야 지도다. 인간 감각 → 장치 설계 → 렌더링 → 안정성 → 촉각 디스플레이. [공식 장 페이지](https://handbookofrobotics.org/view-chapter/42), [DOI](https://doi.org/10.1007/978-3-319-32552-1_42).
2. **Hayward & MacLean, "Do It Yourself Haptics: Part I," IEEE RAM 14(4), 2007.** 하드웨어와 소프트웨어를 잇는 최고의 다리다. 변환기, 임피던스/어드미턴스, DC 모터, 기구, 양자화, 실시간 루프, 그리고 실제 한계. [DOI](https://doi.org/10.1109/M-RA.2007.907921).
3. **MacLean, "Haptic Interaction Design for Everyday Interfaces," RHFE 4(1), 2008.** 능동적 촉각, 다감각 주의, haptic icon, shared control, 그리고 기술적 사실성이 유용성과 같지 않은 이유를 읽어라. [DOI](https://doi.org/10.1518/155723408X342826).
4. **Weir & Colgate, "Stability of Haptic Displays."** 가상 벽의 에너지 유도, Z-width, 양자화, virtual coupling, PO/PC 절을 읽어라. 뒤의 회로 구현은 전문 심화로 다룬다.
5. **Gillespie & Cutkosky, "Stable User-Specific Haptic Rendering of the Virtual Wall," ASME IMECE, 1996.** 샘플링되고 스위칭되는 벽은 그냥 LTI 스프링이 아니다. 반 샘플 예측기와 임계 통과 보정은 제한된 고주파 인간·장치 모델에 기대며, 초기 실험은 정성적이었다. [DOI](https://doi.org/10.1115/IMECE1996-0362).
6. **Hannaford & Ryu, "Time-Domain Passivity Control of Haptic Interfaces," IEEE TRA 18(1), 2002.** 일률의 부호, 에너지 관측기, 적응적 소산 요소를 따라가라. 이 방법은 정확한 환경 모델을 피하지만 잡음, 영속도, 포화, 성능 절충은 여전히 남는다. [DOI](https://doi.org/10.1109/70.988969).
7. **Raju, Verghese & Sheridan, "Design Issues in 2-Port Network Models of Bilateral Remote Manipulation," ICRA 1989.** 원하는 포트 임피던스와 인간·과제 모델에서 안정한 이득 선택으로 가는 고전적 다리다. 그 보장은 명시한 수동적 termination 부류와 모델 가정 위에서만 성립한다. [DOI](https://doi.org/10.1109/ROBOT.1989.100162).
8. **Colonnese & Okamura, "Stability and quantization-error analysis of haptic rendering of virtual stiffness and damping," IJRR 35(9):1103–1120, 2016**(온라인 2015). 샘플링, 위치 양자화, 시간 지연, 속도 추정용 저역통과 필터를 1자유도 모델 하나에 함께 넣고 그 사이의 절충을 유도한 논문이다. 양자화 오차 수동성의 충분조건과, (malicious·uncoupled touch) 극한 주기가 없기 위한 필요조건을 함께 제시한다. Phantom Premium 1.5로 검증했고, 초록에는 수치 결과가 없다. 연도만 쓰지 말고 권호를 써라 — 2015년에 온라인, 2016년에 지면으로 나왔다. [DOI](https://doi.org/10.1177/0278364915596234).

### 5. 제공된 과목 자료를 어떻게 선별했는가

| 로컬 자료 부류 | 공개 학습 용도 |
|---|---|
| syllabus와 강의 슬라이드 | 트랙 범위, 선수 지식 지도, 개념, 판본 단서 |
| MATLAB 템플릿과 야코비안 스크립트 | 독자적 유도와 구현 체크리스트. 제출 답안은 옮기지 않음 |
| Hapkit 슬라이드와 기구 파일 | 24.3–24.4의 전동·센싱 논리. 제작 지침과 원본 파일은 공개하지 않음 |
| 과제와 학생 초안 | 필요한 역량과 흔한 오류 식별. 정답지나 개인 작업물은 공개하지 않음 |
| 프로젝트 선택지와 평가표 | 이전 가능한 프로젝트 설계·평가 기준. 사적 연락처와 미검증 주장은 제외 |
| 동의서, 모집 자료, 사전·사후 설문 | 윤리, 참가 자격, workload, 개인정보, 측정 설계. 양식을 옮기거나 재사용 가능한 승인으로 취급하지 않음 |
| 라이선스 읽기 자료 | 주석 단 개념과 공식 DOI·출판사 링크. PDF는 비공개 |

이 자료 묶음은 햅틱 과목 전반부를 특히 잘 덮는다. syllabus가 예고한 후반 강의·실습 자료 전부 — 완전한 CHAI3D, 고급 원격조작, ROS 순서 같은 것 — 를 담고 있지는 않다. 그래서 이 안내는 그 강의들을 복원하지 않으며, 다룬다고 주장하지도 않는다.

> [!question]- 스스로 점검 · 정답
> **within-subject 연구에서 20명이 각 30 trial을 했다면 $n=600$인가?** 참가자 수준의 처치 주장에서는 아니다. trial은 참가자 안에 nested된 반복 관측이다. 참가자별 요약이나 위계·혼합 모델로 그 의존성을 다루고, 참가자 20명과 trial 600회를 모두 보고하라.
