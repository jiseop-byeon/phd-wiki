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

**Cutaneous cue**는 피부 변형에서, **kinesthetic/proprioceptive cue**는 사지 운동 중 근육·힘줄·관절과 피부 신장에서 나온다. 햅틱 지각은 이 둘을 운동 명령, 시각, 청각과 결합한다. 수동 자극은 주어진 신호가 무엇을 느끼게 하는지 묻고, 능동 촉각은 사람이 탐색 동작도 선택한다. 질감·경도·온도·무게·정확한 형상은 서로 다른 탐색 동작을 요구하므로 장치는 실제 과제가 요구하는 움직임으로 평가해야 한다.

Merkel(SA-I)은 지속 압력과 경계, Meissner(RA-I)는 저주파 과도응답과 미끄럼 시작, Ruffini(SA-II)는 피부 신장, Pacinian(RA-II)은 고주파 진동과 충격에 특히 유용하다. 하지만 주파수 대역은 겹치며 접촉 면적·부위·예압·파형에 따라 달라진다. “250 Hz가 최적”이라는 문장만으로는 조건이 부족하다.

### 2. Threshold·PSE·JND

Psychometric function은 물리 자극 $x$를 반응 확률에 대응시킨다. 중간점은 PSE가 될 수 있다. 2대안 비교에서 흔한 정의 하나는 $\mathrm{JND}=(x_{75}-x_{25})/2$이지만, yes/no 검출이나 다른 선택 과제에는 chance level과 기준이 다르다. 50% threshold라는 말은 반응 과제를 밝힌 뒤에만 의미가 있다.

Weber 법칙 $\Delta I/I\approx k$는 기준 세기가 커질수록 구별 가능한 절대 변화도 커진다는 국소 경험식이다. 예를 들어 5 N 부근의 JND가 8%라면 눈에 띌 변화의 첫 추정은 0.4 N이다. 모든 참가자가 5.4 N을 반드시 구별한다는 뜻은 아니다.

### 3. 실험 설계

빠른 threshold 추정에는 staircase, 전체 곡선에는 constant stimuli, 감각 매칭에는 adjustment가 적합하다. 인터페이스 비교는 within-subject 설계가 효율적이지만 학습·피로·순서 효과를 counterbalancing해야 한다. hit뿐 아니라 false alarm도 측정하고, 선호도만 묻지 말고 접촉력·운동·지연·과제 성공을 함께 기록한다.

### 4. 다감각과 workload

분산을 아는 Gaussian 추정치라는 가정에서는 위 식처럼 precision weighting이 가능하다. 이것은 모든 상황의 감각 우세 법칙이 아니다. 신뢰도·시간 정렬·과제 관련성·prior·주의·충돌이 감각 융합을 결정한다. 시각 경고를 촉각으로 옮겼다고 workload가 자동으로 줄지도 않는다.

> [!question]- 스스로 점검 · 정답
> **더 선명한 진동이 원격조작 성능을 높이지 못할 수 있는 이유는?** 검출 가능성은 한 단계일 뿐이다. 신호가 늦거나, 잘못된 상태를 부호화하거나, 시각과 충돌하거나, 주의를 소모하거나, 실행 가능한 결정을 바꾸지 못할 수 있다. 지각·제어 행동·과제 결과를 분리해 측정해야 한다.

