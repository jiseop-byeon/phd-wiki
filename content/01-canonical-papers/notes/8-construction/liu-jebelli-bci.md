---
title: "Brain-Computer Interface Teleoperation of Construction Robots (Liu, Habibnezhad & Jebelli, 2021)"
authors: Yizhi Liu, Mahmoud Habibnezhad, Houtan Jebelli
affiliation: Pennsylvania State University
venue: Automation in Construction
year: 2021
pdf: https://doi.org/10.1016/j.autcon.2020.103523
sibling: https://doi.org/10.1016/j.autcon.2021.103556
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Liu, Habibnezhad & Jebelli, Automation in Construction 2021** — [DOI](https://doi.org/10.1016/j.autcon.2020.103523) · [Sibling paper](https://doi.org/10.1016/j.autcon.2021.103556)

> [!note] Math on-ramp · 수학 준비물
> [[02-foundations/signal-processing|6. Signal Processing §2 and §4]] (EEG is a sampled, heavily filtered signal — sampling rate and filter lag are not incidental here) and [[04-robotics/hri-safety|11. HRI & Safety §2]] for what "hands-free teleoperation" places in the loop.
> [[02-foundations/signal-processing|6. 신호처리 §2·§4]](EEG는 샘플링되고 강하게 필터링된 신호이며, 여기서 샘플링 레이트와 필터 지연은 부수적인 것이 아니다)와, "핸즈프리 원격조작"이 루프에 무엇을 놓는지는 [[04-robotics/hri-safety|11. HRI·안전 §2]].

## English

**One-line summary**: A wearable EEG headset decodes a worker's brainwaves into robot commands, giving hands-free teleoperation of a construction robot — the founding pair of the worker-centered BCI line, where the *interface* is the contribution and the human stays the controller.

> [!tip] Key intuition · 핵심 직관
> The interface converts selected EEG patterns into a restricted command channel while the worker remains the decision maker. Its value comes from providing a hands-free way to issue those commands, so decoding and operator burden matter as much as the robot’s eventual motion.

**Context.** This is a worker-interface question: how can a person issue robot commands when their hands are occupied? Read it through command-channel quality and operator burden before interpreting it as autonomous robotics.

**Method**: EEG signals from a wearable headset are filtered, features extracted, and classified into discrete robot commands, so a worker whose hands are occupied (or who must keep distance from a hazard) can still direct the machine. The sibling paper ([AutCon 124, 2021](https://doi.org/10.1016/j.autcon.2021.103556)) extends the channel from one-way command to *collaboration*: brainwave-derived worker states feed back into how the robot behaves. The current front of the line is Liu & Jebelli's intention-aware robot motion planning ([CACAIE 39(15), 2024](https://doi.org/10.1111/mice.13129), paywalled) — the robot begins to *anticipate* the worker rather than merely obey.

**Evidence**: two tasks (§6–§7). *Offline*, **12 subjects** did motor-imagery trials (imagine right hand, left hand, or feet for right, left, stop) wearing a 32-channel Emotiv Flex headset at 128 Hz; a filter-bank CSP and SVM ensemble classified the three commands with **79.1% ± 1.85%** accuracy across the 12 datasets (Table 1, Fig. 9). A screening rule executes a command only when two consecutive predictions agree, which the authors calculate raises the reliability of executed commands to 93.5%. That is the source of the abstract's "90% accuracy"; the classifier itself is 79.1%. *Online*, the subject steered a HUSKY A200 ground robot point to point, in line of sight, while laying bricks with both hands: 30 right-control and 30 left-control missions and 60 remote stops, with success rates of 90.0%, 83.3% and 85% (Fig. 11). This is a **staged task, not a site**: no field deployment, and no claim of one. On the autonomy spectrum this is the *opposite* pole from autonomous excavation — the human is always in the loop, and the research question is the quality of the channel, not the removal of the human.

**Limitations**: EEG on a real construction site faces sweat, motion artifacts, helmets, and electrical noise that a lab testbed does not; command bandwidth of classified brainwave signals is low compared to a joystick; the paper does not discuss calibration or cross-user transfer. It reports accuracy per subject dataset and the online missions for "the subject", so whether one model serves a new worker is not shown. The line's own trajectory (teleop → brainwave-driven collaboration → intention-aware planning) is a tacit admission that raw BCI command is a bottleneck and shared control is the destination.

**Lineage**: Houtan Jebelli is a SangHyun Lee PhD (UMich 2019) — this is the wearable-sensing/worker-physiology school applied to robot control. Yizhi Liu is now Syracuse faculty, carrying the line forward.

> [!question] Reading the claim · 핵심 주장 읽는 법
> "Hands-free teleoperation" is an interface claim on a testbed — judge it by HCI/human-factors criteria (channel quality, operator burden, safety distance), not as a robot-autonomy contribution. This paper's real value lies less in any single result than in the worker-centered research programme it opened: from command, to collaboration, to intention prediction.

## 한국어

**한 줄 요약**: 착용형 EEG 헤드셋이 작업자의 뇌파를 로봇 명령으로 해독해 건설 로봇의 핸즈프리 원격조종을 가능하게 한다 — 작업자 중심 BCI 계열의 창립 논문 쌍으로, 기여는 *인터페이스*이고 인간이 계속 제어자로 남는다.

> [!tip] 핵심 직관 · Key intuition
> 인터페이스는 작업자가 결정권을 가진 상태에서 선택한 EEG 패턴을 제한된 명령 채널로 바꾼다. 손을 쓰지 않고 명령할 수 있다는 데 가치가 있다. 최종 로봇 동작만큼 해독과 운전자 부담이 중요하다.

**맥락.** 손을 쓰기 어려운 사람이 어떻게 로봇에 명령할지 묻는 작업자 인터페이스 연구다. 자율 로보틱스로 해석하기 전에 명령 채널의 품질과 운전자 부담으로 읽는다.

**방법**: 착용형 헤드셋의 EEG 신호를 필터링하고 특징을 추출해 이산적 로봇 명령으로 분류한다 — 손이 자유롭지 않거나 위험 요소와 거리를 유지해야 하는 작업자도 기계를 지시할 수 있다. 자매 논문([AutCon 124, 2021](https://doi.org/10.1016/j.autcon.2021.103556))은 이 채널을 일방향 명령에서 *협업*으로 확장한다: 뇌파에서 유도한 작업자 상태가 로봇의 행동 방식에 피드백된다. 이 계열의 현재 최전선은 Liu & Jebelli의 의도 인지 로봇 모션 계획([CACAIE 39(15), 2024](https://doi.org/10.1111/mice.13129), 유료) — 로봇이 단순히 복종하는 것을 넘어 작업자를 *예측*하기 시작한다.

**증거**: 과제는 둘이다(§6~§7). *오프라인*에서는 **피험자 12명**이 32채널 Emotiv Flex 헤드셋(128 Hz)을 쓰고 운동 심상 시행(오른손·왼손·발을 상상해 오른쪽·왼쪽·정지)을 했다. 필터 뱅크 CSP와 SVM 앙상블이 세 명령을 12개 데이터셋에 걸쳐 **79.1% ± 1.85%** 정확도로 분류했다(표 1, 그림 9). 연속된 두 예측이 일치할 때만 명령을 실행하는 선별 규칙을 두면, 저자들의 계산으로 실행되는 명령의 신뢰도가 93.5%로 오른다. 초록의 "90% 정확도"는 여기서 나온 것이고, 분류기 자체는 79.1%다. *온라인*에서는 피험자가 두 손으로 벽돌을 쌓으면서 시야 안의 HUSKY A200 지상 로봇을 지점에서 지점으로 조종했다: 오른쪽 조종 30회, 왼쪽 조종 30회, 원격 정지 60회이고 성공률은 각각 90.0%, 83.3%, 85%다(그림 11). 이것은 **현장이 아니라 연출된 과제**다: 필드 배치도 없고 그런 주장도 없다. 자율성 스펙트럼에서 이것은 자율 굴착의 *반대* 극이다 — 인간이 항상 루프 안에 있고, 연구 질문은 인간의 제거가 아니라 채널의 품질이다.

**한계**: 실제 건설 현장의 EEG는 실험실 테스트베드에 없는 땀, 동작 아티팩트, 안전모, 전기 노이즈를 마주한다; 분류된 뇌파 신호의 명령 대역폭은 조이스틱에 비해 낮다; 논문은 보정이나 사용자 간 전이를 다루지 않는다. 정확도를 피험자 데이터셋별로 보고하고 온라인 과제는 "the subject"에 대해 보고하므로, 한 모델이 새 작업자에게 통하는지는 보여주지 않는다. 계열 자체의 궤적(원격조종 → 뇌파 기반 협업 → 의도 인지 계획)은 원시 BCI 명령이 병목이고 공유 제어가 종착지라는 암묵적 인정이다.

**계보**: Houtan Jebelli는 SangHyun Lee의 박사 제자(UMich 2019) — 착용형 센싱/작업자 생리학 학파가 로봇 제어에 적용된 것이다. Yizhi Liu는 현재 Syracuse 교수로 이 계열을 이어가고 있다.

### 연결

- 스트림: [[05-construction-robotics/hrc-worker-centered|stream 6]] (작업자 중심 HRC의 BCI 갈래)
- 계보: SangHyun Lee → Jebelli(UIUC) → Yizhi Liu(Syracuse) · [[05-construction-robotics/lineage|건설로봇 계보]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "hands-free teleoperation"은 테스트베드 위의 인터페이스 주장이다 — 로봇 자율성 기여가 아니라 HCI/인간공학 기여의 기준(채널 품질, 작업자 부담, 안전 거리)으로 평가해야 한다. 이 논문의 진짜 가치는 개별 결과보다 그것이 연 작업자 중심 연구 프로그램 — 명령에서 협업으로, 협업에서 의도 예측으로 — 에 있다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading (◐)

- [ ] Walk through the EEG → feature extraction → classification → robot command pipeline stage by stage · EEG → 특징 추출 → 분류 → 로봇 명령 파이프라인을 단계별로 말할 수 있다
- [ ] Explain why this is teleoperation rather than autonomy, and locate it on the autonomy spectrum · 이것이 자율성이 아니라 원격조종인 이유와 자율성 스펙트럼상의 위치를 설명할 수 있다
- [ ] State the gap between testbed EEG and site EEG (noise, bandwidth, calibration) · 테스트베드 EEG와 현장 EEG 사이의 간극(노이즈, 대역폭, 보정)을 말할 수 있다
- [ ] Explain why the line's trajectory (teleoperation → EEG collaboration → intention-aware planning) converges on shared control · 계열의 궤적(원격조종 → 뇌파 협업 → 의도 인지 계획)이 왜 공유 제어로 수렴하는지 설명할 수 있다
