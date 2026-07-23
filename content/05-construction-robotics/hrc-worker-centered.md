---
title: 6. HRC & Worker-Centered Robotics
tags: [construction, hri, safety, workers]
---

## English

Construction HRC studies a robot and a worker as one changing system. The distinctive
question is not only whether the robot avoids collision, but whether it can infer,
communicate, allocate, and recover without increasing cognitive or physical burden.

> [!note] Prerequisites
> [[04-robotics/hri-safety|HRI & Safety]] · [[02-foundations/signal-processing|Signal Processing]] ·
> [[04-robotics/planning-decision-making|Planning]] · [[06-research-practice/experimental-design-reproducibility|Experimental Design]]

### 1. The worker-in-the-loop stack

1. **Sense** motion, gaze, speech, EEG/EDA/EMG, workload, or proximity.
2. **Infer** intent, fatigue, stress, trust, or task phase—with uncertainty.
3. **Decide** robot speed, path, task allocation, assistance, or handover.
4. **Communicate** prediction and intent in a form the worker can understand.
5. **Evaluate** safety, productivity, workload, trust, and adaptation over time.

Wearable classification alone is worker sensing. It becomes worker-centered robotics
only when the estimate changes robot behavior and that closed loop is evaluated.

### 2. Main research lines

- The **Michigan DPM → UIUC/Georgia Tech/Toronto diaspora** connects physiological
  computing to intention-aware planning, BCI/teleoperation, co-robotic safety, and LMM-
  mediated field robots.
- The **Michigan LIVE/SICIS → VT/Stony Brook/TAMU** line connects adaptive autonomy,
  learning from demonstration, tactile handover, digital twins, and multi-robot supervision.
- The **MIT Shah manufacturing line** supplies cross-training, role allocation, legible
  motion, and human-aware planning methods that construction imports.

### 3. Claims that require care

- A biosignal correlate is not a causal state estimate; labels may come from self-report.
- Intent prediction accuracy does not show safer motion unless integrated and tested.
- Reduced completion time can hide increased workload or reduced situation awareness.
- A small laboratory participant sample supports a controlled human study, not a claim
  about all trades, ages, expertise levels, PPE, noise, and weather.
- “Shared autonomy” must state who has authority, how conflicts are resolved, and how the
  worker stops or overrides the robot.

### 4. Evaluation

Report participant population, task realism, counterbalancing, learning/order effects,
sensor failure, false alarms, intervention authority, near misses, workload/trust
instruments, and productivity. Safety outcomes are rare events; absence of collision in
a small study is not evidence of low operational risk.

> [!warning] Reading the claim
> Separate **sensed state**, **inferred construct**, **robot response**, and **measured
> human outcome**. Many papers establish only the first two links. A complete HRC claim
> needs the full causal chain—or must label itself as a component study.

### After reading

- Distinguish worker sensing from closed-loop worker-centered robotics.
- Trace a claim from measurement through inference and robot action to human outcome.
- Identify authority, override, and recovery in shared autonomy.
- Explain why a collision-free small study does not validate operational safety.

### Sources

- [ACM/IEEE International Conference on Human-Robot Interaction](https://humanrobotinteraction.org/)
- [MIT Interactive Robotics Group](https://interactive.mit.edu/)
- [[05-construction-robotics/labs|Labs Map]] — verified Michigan academic genealogy

## 한국어

건설 HRC는 로봇과 작업자를 하나의 변하는 시스템으로 본다. 충돌 회피뿐 아니라 인지·소통·
과제 배분·복구가 작업자의 인지·신체 부담을 늘리지 않는지가 핵심이다.

> [!note] 선수지식
> [[04-robotics/hri-safety|HRI와 안전]] · [[02-foundations/signal-processing|신호처리]] ·
> [[04-robotics/planning-decision-making|계획]] · [[06-research-practice/experimental-design-reproducibility|실험 설계]]

### 1. 작업자 폐루프

1. 움직임·시선·말·EEG/EDA/EMG·작업부하·근접을 **센싱**한다.
2. 의도·피로·스트레스·신뢰·작업 단계를 불확실성과 함께 **추론**한다.
3. 로봇 속도·경로·과제 배분·지원·전달을 **결정**한다.
4. 작업자가 이해할 수 있게 로봇의 예측과 의도를 **소통**한다.
5. 안전·생산성·부하·신뢰·장기 적응을 **평가**한다.

웨어러블 분류만 하면 작업자 센싱이다. 추정값이 로봇 행동을 바꾸고 폐루프를 평가해야 작업자
중심 로보틱스가 된다.

### 2. 연구 계보

- **미시간 DPM → UIUC·GT·토론토**: 생리 컴퓨팅에서 의도 인식 계획, BCI/원격조작,
  co-robotic 안전, LMM 필드 로봇으로.
- **미시간 LIVE/SICIS → VT·Stony Brook·TAMU**: 적응적 자율성, 시연 학습, 촉각 전달,
  디지털 트윈, 멀티로봇 감독으로.
- **MIT Shah 제조 HRC**: 교차 훈련, 역할 배분, 읽기 쉬운 움직임, 인간 인지 계획을 공급한다.

### 3. 조심해서 읽을 주장

- 바이오신호 상관관계는 인과적 상태 추정이 아니며 라벨이 자기보고일 수 있다.
- 의도 예측 정확도만으로 더 안전한 모션을 보인 것은 아니다.
- 시간 단축이 작업부하 증가나 상황 인식 저하를 숨길 수 있다.
- 작은 실험실 표본은 모든 직종·숙련도·PPE·소음·날씨로 일반화되지 않는다.
- Shared autonomy는 권한, 충돌 해결, 정지·override 주체를 명시해야 한다.

### 4. 평가

참가자 집단, 과제 현실성, 순서 효과, 센서 실패, 오경보, 개입 권한, near miss, 작업부하·
신뢰 측정, 생산성을 보고해야 한다. 안전 사고는 희귀하므로 작은 연구의 무충돌은 낮은 현장
위험의 증거가 아니다.

> [!warning] 주장 읽기
> **측정 상태 → 추론 구성개념 → 로봇 반응 → 인간 결과**를 분리하라. 많은 논문은 첫 두
> 연결만 보인다. 완전한 HRC 주장은 전체 사슬이 필요하며, 아니면 구성요소 연구라고 범위를
> 제한해야 한다.

### 읽고 나면 말할 수 있어야 하는 것

- 작업자 센싱과 폐루프 작업자 중심 로보틱스를 구분한다.
- 측정부터 추론·로봇 행동·인간 결과까지 주장을 추적한다.
- 공유 자율성의 권한·override·복구를 찾는다.
- 작은 무충돌 연구가 운용 안전을 검증하지 못하는 이유를 설명한다.

### 출처

- [ACM/IEEE HRI](https://humanrobotinteraction.org/)
- [MIT Interactive Robotics Group](https://interactive.mit.edu/)
- [[05-construction-robotics/labs|Labs Map]] — 검증된 미시간 학술 계보
