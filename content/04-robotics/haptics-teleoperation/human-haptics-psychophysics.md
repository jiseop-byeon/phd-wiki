---
title: 24.1 Human Haptics & Psychophysics
tags: [haptics, psychophysics, hri]
study-depth: Working
wiki-support: Working
depth-goal: "Translate a touch claim into a stimulus, receptor/site, task, psychometric measure, and uncertainty statement."
mastery-when: "Master staircase design, psychometric modeling, and multisensory inference when human perception is the thesis contribution."
---

## English

### 1. Touch is an active sensing loop

**Cutaneous** cues arise from skin deformation; **kinesthetic/proprioceptive** cues arise from muscles, tendons, joints, and skin stretch during limb motion. Haptic perception combines both with motor commands and often with vision and sound. Passive stimulation asks what a delivered cue evokes; active touch also lets the person choose an exploratory motion. Texture, hardness, temperature, weight, and exact shape invite different exploratory procedures, so a device should be evaluated with the movement the target task actually requires.

The common receptor labels are useful but approximate:

| Afferent class | Adaptation/field | Especially informative about |
|---|---|---|
| SA-I / Merkel | slow, small field | sustained pressure, edges, coarse form |
| RA-I / Meissner | rapid, small field | low-frequency transients, slip onset |
| SA-II / Ruffini | slow, large field | skin stretch, hand configuration |
| RA-II / Pacinian | rapid, large field | high-frequency vibration and impacts |

Frequency bands overlap and depend on contactor size, site, preload, and waveform. A statement such as “250 Hz is optimal” is incomplete without those conditions.

### 2. Threshold, PSE, and JND

A **psychometric function** maps physical stimulus $x$ to response probability, for example $P(\text{comparison judged stronger}\mid x)$. Its midpoint can define the **point of subjective equality** (PSE). In a two-alternative comparison, one common convention is

$$\mathrm{JND}=\frac{x_{75}-x_{25}}{2}.$$

This is not a universal definition: yes/no detection, $n$-alternative choice, and fitted functions use different chance levels and threshold criteria. A 50% threshold is meaningful only after the response task is specified.

**Weber's law** is the local empirical approximation $\Delta I/I\approx k$. It predicts that the absolute increment needed for discrimination grows with the reference intensity. Integrating equal relative increments motivates Fechner's logarithmic scale, but neither law is exact across all intensities or modalities.

Worked interpretation: if a force JND is 8% near 5 N, a first estimate of a noticeable increment is $0.08(5)=0.4$ N. This does not prove that every participant notices 5.4 N; it describes a criterion-dependent population response near that operating point.

### 3. Choosing an experiment

| Question | Useful method | Main risk |
|---|---|---|
| find an approximate threshold quickly | staircase / adaptive up–down | convergence depends on rule and lapses |
| estimate a full psychometric curve | constant stimuli | many trials; order and fatigue |
| let users match a sensation | adjustment | response and anchoring bias |
| compare two interfaces | within-subject counterbalanced study | carryover and learning |

Measure false alarms as well as hits. Signal-detection analysis separates sensitivity from response criterion. Randomize condition order, include training, predefine exclusions, and record contact force, motion, latency, and task success rather than relying only on preference.

### 4. Multisensory and workload claims

Under particular Gaussian/noise assumptions, two estimates with variances $\sigma_v^2$ and $\sigma_h^2$ combine by precision weighting:

$$\hat x=\frac{\sigma_v^{-2}x_v+\sigma_h^{-2}x_h}{\sigma_v^{-2}+\sigma_h^{-2}}.$$

This is a model, not a universal law of sensory dominance. Reliability, temporal alignment, task relevance, priors, attention, and conflict determine whether cues fuse, compete, or remain separate. Likewise, moving a warning from vision to touch does not automatically reduce workload; representative multitask testing is necessary.

> [!question]- Self-check · Answer
> **Why can a clearer vibration fail to improve a teleoperation task?** Detectability is only one link. The cue may arrive late, encode the wrong state, conflict with vision, consume attention, or fail to change an actionable decision. Test perception, control behavior, and task outcome separately.

## 한국어

### 1. 촉각은 능동 센싱 루프다

**Cutaneous** cue는 피부 변형에서, **kinesthetic·proprioceptive** cue는 사지가 움직일 때 근육·힘줄·관절과 피부 신장에서 나온다. 햅틱 지각은 이 둘을 운동 명령과, 흔히 시각·청각과도 결합한다. 수동 자극은 주어진 cue가 무엇을 불러일으키는지 묻고, 능동 촉각은 사람이 탐색 동작까지 고른다. 질감, 경도, 온도, 무게, 정확한 형상은 서로 다른 탐색 절차를 부르므로, 장치는 목표 과제가 실제로 요구하는 움직임으로 평가해야 한다.

흔히 쓰는 수용기 이름표는 유용하지만 근사다.

| 구심신경 부류 | 적응·수용장 | 특히 잘 알려 주는 것 |
|---|---|---|
| SA-I / Merkel | 느림, 작은 수용장 | 지속 압력, 경계, 거친 형태 |
| RA-I / Meissner | 빠름, 작은 수용장 | 저주파 과도, 미끄럼 시작 |
| SA-II / Ruffini | 느림, 큰 수용장 | 피부 신장, 손 자세 |
| RA-II / Pacinian | 빠름, 큰 수용장 | 고주파 진동과 충격 |

주파수 대역은 서로 겹치고 접촉자 크기, 부위, 예압, 파형에 따라 달라진다. "250 Hz가 최적"이라는 진술은 그 조건들 없이는 불완전하다.

### 2. 임계값, PSE, JND

**심리측정 함수**는 물리 자극 $x$를 반응 확률로 사상한다. 예를 들어 $P(\text{비교 자극이 더 강하다고 판정}\mid x)$이다. 그 중간점이 **주관적 등가점**(PSE)을 정의할 수 있다. 2대안 비교에서 흔한 관례 하나는 이것이다.

$$\mathrm{JND}=\frac{x_{75}-x_{25}}{2}.$$

이것은 보편적 정의가 아니다. yes/no 검출, $n$대안 선택, 적합된 함수는 각각 다른 chance level과 임계 기준을 쓴다. 50% 임계값이라는 말은 반응 과제를 명시한 뒤에만 의미를 갖는다.

**Weber 법칙**은 국소적인 경험 근사 $\Delta I/I\approx k$다. 구별에 필요한 절대 증가량이 기준 세기와 함께 커진다고 예측한다. 같은 상대 증가량을 적분하면 Fechner의 로그 척도가 동기를 얻지만, 두 법칙 중 어느 것도 모든 세기와 모든 감각 양상에서 정확하지는 않다.

계산해 읽기: 5 N 부근에서 힘 JND가 8%라면 알아챌 만한 증가량의 첫 추정은 $0.08(5)=0.4$ N이다. 이것은 모든 참가자가 5.4 N을 알아챈다는 증명이 아니라, 그 작동점 부근에서 기준에 의존하는 모집단 반응을 서술한 것이다.

### 3. 실험 고르기

| 질문 | 쓸 만한 방법 | 주된 위험 |
|---|---|---|
| 대략의 임계값을 빨리 찾기 | staircase · 적응적 up–down | 수렴이 규칙과 실수율에 달림 |
| 전체 심리측정 곡선 추정 | constant stimuli | 시행이 많고 순서·피로가 개입 |
| 사용자가 감각을 맞추게 하기 | adjustment | 반응 편향과 anchoring |
| 두 인터페이스 비교 | within-subject counterbalanced | 이월 효과와 학습 |

hit뿐 아니라 false alarm도 재라. 신호 검출 분석이 민감도와 반응 기준을 분리해 준다. 조건 순서를 무작위화하고, 훈련을 넣고, 제외 기준을 미리 정하고, 선호도에만 기대지 말고 접촉력·운동·지연·과제 성공을 기록하라.

### 4. 다감각과 workload 주장

특정한 가우시안·잡음 가정 아래에서 분산이 $\sigma_v^2$와 $\sigma_h^2$인 두 추정치는 정밀도 가중으로 결합된다.

$$\hat x=\frac{\sigma_v^{-2}x_v+\sigma_h^{-2}x_h}{\sigma_v^{-2}+\sigma_h^{-2}}.$$

이것은 모델이지 감각 우세의 보편 법칙이 아니다. 신뢰도, 시간 정렬, 과제 관련성, prior, 주의, 충돌이 cue가 융합할지 경쟁할지 따로 남을지를 결정한다. 마찬가지로 경고를 시각에서 촉각으로 옮긴다고 workload가 자동으로 줄지 않는다. 대표성 있는 다중 과제 시험이 필요하다.

> [!question]- 스스로 점검 · 정답
> **더 선명한 진동이 원격조작 과제를 개선하지 못할 수 있는 이유는?** 검출 가능성은 사슬의 한 고리일 뿐이다. cue가 늦게 도착하거나, 틀린 상태를 부호화하거나, 시각과 충돌하거나, 주의를 소모하거나, 실행 가능한 결정을 바꾸지 못할 수 있다. 지각과 제어 행동과 과제 결과를 따로 시험하라.
