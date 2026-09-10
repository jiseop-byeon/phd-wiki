---
title: 24.7 Experiments & Reading Map
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

### 5. How the supplied course materials were selected

| Local material class | Public learning use |
|---|---|
| syllabus and lecture decks | track scope, prerequisite map, concepts, and version caveats |
| MATLAB templates and Jacobian script | original derivations and implementation checklist; no submitted solution copied |
| Hapkit slides and seven STL parts | device architecture, assembly reasoning, calibration and safety; original files remain private |
| assignments and student drafts | identify required competencies and common mistakes; no answer key or personal work published |
| project options/rubric | transferable project-design and evaluation criteria; private contacts and unverified claims excluded |
| consent, recruitment, pre/post surveys | ethics, eligibility, workload, privacy, and measurement design; no form copied or treated as a reusable approval |
| licensed readings | annotated concepts and official DOI/publisher links; PDFs remain private |

The packet covers the first half of a full haptics course particularly well. It does not contain all later lecture/lab materials named in the syllabus—such as the complete CHAI3D, advanced teleoperation, and ROS sequence—so this guide links the missing implementation bridge but does not claim to reconstruct unseen lectures.

> [!question]- Self-check · Answer
> **A within-subject study has 20 people and 30 trials per person. Is $n=600$?** Not for a participant-level treatment claim. Trials are nested/repeated observations. Analyze that dependence, for example with participant-level summaries or a hierarchical/mixed model; report both 20 participants and 600 trials.

## 한국어

### 1. 아이디어에서 주장까지

제작 전에 **actuator command → 실제 전달 자극 → 지각/행동 → 과제 결과**의 인과 사슬을 쓴다. 각 화살표에 측정이 필요하다. 모터 명령은 피부 자극 측정값이 아니고, 설문은 제어기 성능이 아니며, 수행시간 감소만으로 어떤 cue가 원인인지 알 수 없다.

### 2. 최소 프로토콜

구체적인 estimand, 참가자 집단과 제외 기준, feedback/delay/gain 조건, counterbalanced design, 사전 지정 primary outcome, clock가 맞는 로그, 올바른 분석 단위, 동의·철회·privacy·fatigue·hardware stop을 정한다. Trial은 participant 안에 nested되므로 반복 trial 수를 독립 참가자 수처럼 세면 안 된다.

NASA-TLX는 mental·physical·temporal demand, perceived performance, effort, frustration의 여섯 자기보고 차원이다. 객관 데이터의 보완물이며 workload의 물리 원인을 직접 밝히지 않는다. Raw/weighted 중 어떤 절차를 썼는지 보고한다.

### 3. 증거의 단계

Bench response는 장치 동역학, psychophysical threshold는 특정 조건의 검출 가능성, controlled task는 해당 protocol의 인과 효과, representative workload는 더 가까운 맥락의 성능, field/longitudinal study는 시간에 따른 운용 행동을 지지한다. 각 단계가 다음 단계의 일반화를 자동으로 보장하지 않는다.

### 4. 읽기 순서

위 영어 목록의 7개 자료를 순서대로 읽는다. Hannaford–Okamura로 전체 지도를 잡고, Hayward–MacLean으로 hardware/software를 연결하고, MacLean으로 인간 중심 설계를 익힌다. 그 뒤 Weir–Colgate → Gillespie–Cutkosky → Hannaford–Ryu로 virtual wall과 passivity를 깊게 읽고, Raju–Verghese–Sheridan으로 2-port 원격조작을 연결한다.

### 5. 과목 자료 선별 원칙

강의·syllabus는 개념과 범위, MATLAB과 과제는 필요한 역량과 흔한 오류, Hapkit 자료는 제작·보정·안전, 프로젝트·설문·동의서는 연구 설계와 윤리, 논문은 핵심 개념과 공식 출처에 사용했다. 학생 답안·개인 연락처·출입 정보·저작권 원본은 공개하지 않는다.

과목 폴더에는 syllabus가 예고한 후반 CHAI3D·고급 teleoperation·ROS 강의/실습 전체가 들어 있지 않다. 이 페이지는 공개 공식 문서로 구현 진입로를 보완하지만 보지 못한 강의를 복원했다고 주장하지 않는다.

> [!question]- 스스로 점검 · 정답
> **20명이 각 30 trial을 수행하면 $n=600$인가?** 참가자 수준의 treatment claim에서는 아니다. Trial은 참가자 안의 반복 관측이다. Participant summary나 hierarchical/mixed model로 의존성을 처리하고 20 participants와 600 trials를 모두 보고한다.

