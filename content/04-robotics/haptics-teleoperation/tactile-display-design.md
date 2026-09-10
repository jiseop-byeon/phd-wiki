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

### 1. 액추에이터가 아니라 정보에서 시작한다

Tactile display는 피부를 의도적으로 자극한다. Kinesthetic display는 주로 사지에 힘이나 운동을 가하지만, 그 손잡이도 피부를 자극한다. 하드웨어를 고르기 전에 목표 변수를 적어라. 접촉 시작, 방향, 미끄럼, 거칠기, 국소 형상, 마찰, 부드러움, 온도 중 무엇인가. 그다음 사실적 재현이 목적인지 구별 가능한 전달이 목적인지 물어라.

| 디스플레이 계열 | 제어하는 cue | 강점 | 통상적 한계 |
|---|---|---|---|
| ERM "럼블" 모터 | 결합된 진동 주파수·진폭 | 싸고 뚜렷함 | 느린 포락선. 주파수와 진폭이 묶임 |
| LRA · voice coil · 피에조 | 성형된 진동 | 더 빠르고 풍부한 파형 | 공진, 스트로크, 장착 의존성 |
| Tactor 배열 | 시공간 패턴 | 방향과 경보 | masking, 배선, 부위별 예민도 |
| 피부 신장 · 전단 | 접선 방향 변형 | 방향, 미끄럼, 마찰 착시 | 예압과 미끄러지지 않는 접촉을 통제해야 함 |
| 핀 · 형상 디스플레이 | 압력 분포 · 국소 형상 | 공간적 형태 | 액추에이터 밀도, 부피, 대역폭 |
| 가변 마찰 표면 | 능동 스캔 중의 마찰 | 평평한 화면 위의 질감 | 손가락 운동과 추적이 필요 |
| 펠티에 열 디스플레이 | 열 흐름 · 온도 cue | 재질과 온도 cue | 느린 동역학, 방열, 안전 |

### 2. 파형은 지각이 아니다

사인파 $a(t)=A\sin(2\pi ft)$에서 물리 변수는 주파수, 진폭, 위상, 지속 시간, attack·decay 포락선, 신체 부위, 접촉 면적, 예압을 포함한다. 지각은 그 전부에 달려 있다. 같은 모터 전압이 같은 피부 가속도를 뜻하지 않고, 같은 가속도가 주파수를 가로질러 같은 지각 크기를 뜻하지도 않는다.

편심 회전 질량은 대략 $mr\omega^2$에 비례하는 원심력을 만든다. 속도를 바꾸면 주파수와 힘 진폭이 함께 바뀐다. LRA나 voice coil 액추에이터는 파형을 더 독립적으로 제어하게 해 주지만 자기 전달함수에 의해 성형된다. 그러므로 명령 신호가 아니라 **접촉점에서의 가속도나 피부 변위**를 특성화하라.

### 3. 공간과 시간 설계

가까운 두 자극은 간격과 타이밍에 따라 합쳐지거나, 서로를 masking하거나, apparent motion을 만든다. 예민도는 손끝, 손바닥, 팔뚝, 몸통, 털 있는 피부 사이에서 크게 다르다. 착용형 배열은 실제 착용 위치에서, 움직임과 workload 아래에서 시험해야 한다. 기호 수를 늘리기 전에 충분히 떨어진 신호의 작은 어휘부터 쓰라. 다차원 척도법이나 혼동 행렬이 사용자가 실제로 구별하는 패턴을 드러낸다.

### 4. 접촉, 미끄럼, 재질 cue

사람은 분포된 압력, 피부 신장, 진동, 사전 지식을 써서 큰 미끄럼이 나기 전에 파지력을 조절한다. 정상력만 돌려주는 원격조작기는 이 증거의 상당 부분을 빠뜨린다. 접촉 위치 장치는 접촉 패치를 움직이고, 전단 장치는 큰 미끄럼 없이 피부를 변형시키며, 진동은 충격 과도를 재현할 수 있고, 가변 마찰 디스플레이는 탐색 중 접선력을 바꾼다. 어느 한 cue도 "촉각"이 아니다.

단단한 접촉에는 저주파 힘 루프와 짧은 고주파 과도를 결합할 수 있다. 이렇게 하면 비현실적으로 뻣뻣한 안정 가상 스프링을 요구하지 않고도 지각되는 경도를 높일 수 있다. 다만 그 과도는 개루프 에너지이므로 장치와 안전의 한계 안에 머물러야 한다.

### 5. 설계 체크리스트

1. 사용자가 검출하거나 추정해야 할 물리적 사건은 무엇인가?
2. 과제 중에 믿을 만한 접촉을 유지하는 피부 부위는 어디인가?
3. 하드웨어가 독립적으로 제어할 수 있는 자극 차원은 무엇인가?
4. 명령에서 피부까지의 측정된 전달은 무엇인가?
5. 패턴이 고립된 상태가 아니라 과제 workload 아래에서 구별되는가?
6. 그 cue가 결정이나 과제 결과를 개선하는가, 그리고 어떤 오경보를 만드는가?

> [!question]- 스스로 점검 · 정답
> **250 Hz라는 명령만으로 촉각 자극을 규정할 수 없는 이유는?** 액추에이터와 장착이 전달되는 가속도·변위를 정하고, 예압·접촉 면적·신체 부위·파형 포락선·개인 감수성이 지각을 정한다. 주파수는 좌표 하나일 뿐이다.
