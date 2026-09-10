---
title: 24.2 Tactile Display Design
tags: [haptics, tactile, hri]
study-depth: Working
wiki-support: Working
depth-goal: "Choose a tactile actuation family from the perceptual variable, body site, bandwidth, workspace, and task—not from actuator novelty alone."
mastery-when: "Master transducer dynamics and psychophysical validation when the tactile display is the research contribution."
---

## English

### 1. Start from the information, not the actuator

A tactile display deliberately stimulates skin. A kinesthetic display primarily applies force or motion to a limb, although its handle also stimulates skin. Before choosing hardware, write the target variable: contact onset, direction, slip, roughness, local shape, friction, softness, or temperature. Then ask whether realism or discriminable communication is the goal.

| Display family | Controlled cue | Strength | Typical limitation |
|---|---|---|---|
| ERM “rumble” motor | coupled vibration frequency/amplitude | cheap, salient | slow envelope; frequency and amplitude coupled |
| LRA / voice coil / piezo | shaped vibration | faster, richer waveform | resonance, stroke, mounting dependence |
| tactor array | spatial-temporal pattern | direction and alerts | masking, wiring, body-site acuity |
| skin stretch / shear | tangential deformation | direction, slip, friction illusion | preload and no-slip contact must be controlled |
| pin/shape display | pressure distribution/local shape | spatial form | actuator density, bulk, bandwidth |
| variable-friction surface | friction during active scan | texture on flat screens | requires finger motion and tracking |
| Peltier thermal display | heat flow/temperature cue | material and temperature cues | slow dynamics, heat sinking, safety |

### 2. A waveform is not a percept

For a sinusoid $a(t)=A\sin(2\pi ft)$, the physical variables include frequency, amplitude, phase, duration, attack/decay envelope, body site, contact area, and preload. Perception depends on all of them. Equal motor voltage does not imply equal skin acceleration, and equal acceleration does not imply equal perceived magnitude across frequencies.

An eccentric rotating mass produces centrifugal force approximately proportional to $m r\omega^2$; changing speed changes both frequency and force amplitude. An LRA or voice-coil actuator offers more independent waveform control but is shaped by its own transfer function. Therefore characterize **the acceleration or skin displacement at the contact site**, not merely the command signal.

### 3. Spatial and temporal design

Two nearby stimuli can merge, mask one another, or create apparent motion depending on spacing and timing. Acuity differs sharply between fingertip, palm, forearm, torso, and hairy skin. A wearable array must be tested in its actual placement, under motion and workload. Use a small vocabulary of well-separated signals before increasing symbol count; multidimensional scaling or confusion matrices reveal which patterns users actually distinguish.

### 4. Contact, slip, and material cues

Humans regulate grip before gross slip using distributed pressure, skin stretch, vibration, and prior knowledge. A teleoperator that returns only normal force omits much of this evidence. Contact-location devices move a contact patch; shear devices deform skin without gross slip; vibration can reproduce impact transients; variable-friction displays alter tangential force during exploration. No single cue is “touch.”

For hard contact, a low-frequency force loop and a short high-frequency transient may be combined. This can improve perceived hardness without demanding an unrealistically stiff stable virtual spring, but the transient is open-loop energy and must remain within device and safety limits.

### 5. Design checklist

1. What physical event should the user detect or estimate?
2. Which skin site remains in reliable contact during the task?
3. What stimulus dimensions can the hardware control independently?
4. What is the measured transfer from command to skin?
5. Are patterns distinguishable under task workload, not just in isolation?
6. Does the cue improve a decision or task outcome, and what false alarms does it create?

> [!question]- Self-check · Answer
> **Why is a 250 Hz command not enough to specify a tactile stimulus?** The actuator and mounting determine delivered acceleration/displacement; preload, contact area, body site, waveform envelope, and individual sensitivity determine perception. Frequency is only one coordinate.

## 한국어

### 1. 액추에이터보다 정보에서 시작한다

Tactile display는 피부를 의도적으로 자극하고, kinesthetic display는 주로 사지에 힘이나 운동을 가한다. 하드웨어를 고르기 전에 전달할 변수가 접촉 시작·방향·미끄럼·거칠기·국소 형상·마찰·부드러움·온도 중 무엇인지 쓰고, 사실적인 재현과 구별 가능한 부호 중 어느 것이 목적인지 정한다.

ERM은 싸고 강하지만 주파수와 진폭이 결합되고, LRA·voice coil·piezo는 파형 제어가 좋지만 공진과 장착에 민감하다. Tactor array는 방향·알림, skin stretch는 전단·미끄럼, pin array는 국소 형상, variable-friction surface는 능동 스캔 중 질감, Peltier는 열 흐름을 다룬다. 각 방식은 다른 물리량을 표시한다.

### 2. 파형은 곧 지각이 아니다

$a(t)=A\sin(2\pi ft)$의 지각은 $f$와 $A$뿐 아니라 위상, 길이, attack/decay envelope, 피부 부위, 접촉 면적, 예압에 달린다. 같은 모터 전압이 같은 피부 가속도를 뜻하지 않고, 같은 가속도도 주파수에 따라 같은 크기로 느껴지지 않는다.

ERM의 원심력은 대략 $mr\omega^2$에 비례하므로 속도를 바꾸면 주파수와 힘이 함께 바뀐다. LRA나 voice coil도 장치 전달함수의 영향을 받는다. 명령값이 아니라 **접촉점의 가속도나 피부 변위**를 측정해야 한다.

### 3. 공간·시간 설계

가까운 자극은 간격과 타이밍에 따라 합쳐지거나 masking되거나 apparent motion을 만든다. 손끝·손바닥·팔·몸통의 공간 분해능은 크게 다르다. 실제 착용 위치와 움직임·workload 조건에서 검증한다. 신호 수를 늘리기 전에 작은 집합을 충분히 분리하고 confusion matrix나 MDS로 실제 지각 공간을 확인한다.

### 4. 접촉·미끄럼·재질

사람은 분포 압력, 피부 신장, 진동, prior를 사용해 gross slip 전에 파지력을 조절한다. 정상력만 반환하는 원격조작기는 이 정보의 상당 부분을 잃는다. 접촉 위치·전단·충격 진동·마찰 변조는 서로 대체재가 아니라 보완적 cue다. 단일 신호가 “촉각 전체”는 아니다.

### 5. 설계 질문

표시할 물리 사건, 지속 접촉 가능한 피부 부위, 독립 제어 가능한 자극 차원, command-to-skin 전달함수, workload 속 구별 가능성, 실제 결정과 과제 결과 개선을 차례로 확인한다.

> [!question]- 스스로 점검 · 정답
> **250 Hz 명령만으로 촉각 자극을 규정할 수 없는 이유는?** 액추에이터와 장착이 실제 가속도·변위를 결정하고, 예압·접촉 면적·피부 부위·envelope·개인차가 지각을 결정한다. 주파수는 한 축일 뿐이다.

