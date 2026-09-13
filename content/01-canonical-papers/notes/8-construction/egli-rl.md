---
title: "RL for Hydraulic Excavator Arms — the Actuator-Model Route to Sim-to-Real (Egli & Hutter, 2022)"
authors: Pascal Egli, Marco Hutter (soil-adaptive sibling adds Dominique Gaschen, Simon Kerscher, Dominic Jud)
affiliation: ETH Zurich, Robotic Systems Lab
venue: IEEE Robotics and Automation Letters
year: 2022
doi: https://doi.org/10.1109/LRA.2022.3152865  # general-approach paper (RA-L 2022)
pdf: https://www.research-collection.ethz.ch/server/api/core/bitstreams/95ef5691-11e8-4a86-b02d-6f0e2501de9b/content  # soil-adaptive sibling's ETH OA PDF
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Egli & Hutter, IEEE RA-L 2022 (+ soil-adaptive sibling, RA-L/IROS 2022)** — [DOI](https://doi.org/10.1109/LRA.2022.3152865) · [Soil-adaptive OA PDF](https://www.research-collection.ethz.ch/server/api/core/bitstreams/95ef5691-11e8-4a86-b02d-6f0e2501de9b/content)

> [!note] Math on-ramp · 수학 준비물
> [[02-foundations/rl-basics|7. RL Basics §7–§9]] and [[05-construction-robotics/sim-to-real|Sim-to-Real §2]]. The paper's real contribution is upstream of the policy: a learned actuator model that makes the *simulator* faithful. Read "zero-shot" with that section's warning in hand.
> [[02-foundations/rl-basics|7. RL 기초 §7~§9]]와 [[05-construction-robotics/sim-to-real|Sim-to-Real §2]]. 이 논문의 진짜 기여는 정책보다 위쪽에 있다: *시뮬레이터*를 충실하게 만드는 학습된 액추에이터 모델. "zero-shot"은 그 절의 경고를 손에 들고 읽어라.

## English

**One-line summary**: RL policies drive a real hydraulic excavator arm **without fine-tuning** because the training simulation embeds a *neural-network model of the valve/actuator dynamics* learned from machine data — and the soil-adaptive sibling paper applies RL on the same machine to bucket filling that adapts online across soils without ever identifying soil parameters. The sibling does not reuse the learned actuator model: its policy outputs joint velocities, and conventional valve-flow controllers track them.

**Lineage position**: the learning bridge on the [[01-canonical-papers/notes/8-construction/heap|HEAP]] platform — after the platform paper established force-controllable hydraulics and full-state sensing, this pair shows how *learned* control gets onto that iron, and it is the direct methodological ancestor of [[01-canonical-papers/notes/8-construction/ext|ExT]]. It ports RSL's legged-robot actuator-net trick (Hwangbo et al. 2019, ANYmal) to hydraulics.

> [!tip] Key intuition · 핵심 직관
> The learned actuator model puts measured hydraulic behavior inside the simulator where the policy learns. That targets a specific mismatch between valve commands and motion; the soil-adaptive variant has no memory; it reacts to measured joint torques and its own previous command, so changing resistance shows up directly in what it observes.

**Method** (literacy level): hydraulic valves are the sim-to-real bottleneck — dead bands, delays, and flow nonlinearities that analytic simulators get wrong. So: (1) log real machine data and train a NN actuator model mapping valve commands to joint motion; (2) wrap that model into the training simulator; (3) train an RL policy that outputs **pilot-stage valve commands** directly; (4) deploy on the real machine as-is. The soil-adaptive sibling works differently. It trains bucket filling in simulation against an analytic FEE (fundamental equation of earthmoving) soil model, sampling soil parameters uniformly each episode: cohesion 0–105 kPa, adhesion 0 up to the cohesion, internal friction angle 0.3–0.8 rad, unit weight 17–22 kN/m³, soil–bucket friction angle 0.2–0.4 rad, cavity pressure factor 0–300, and soil height 0.5–2.0 m below the cabin (Table I, §III-D). The policy is a plain two-layer MLP (128, 128) with no recurrence. It adapts because its 27 observations include arm joint torques, estimated from cylinder pressures, and the previous velocity command (Table III). It outputs four joint velocities, which PID plus feed-forward valve-flow controllers track on the machine (§IV-B). Training took about 200 M samples, roughly 7 h.

**Evidence**: the general-approach policy runs on the real Menzi Muck M545 (HEAP) with **zero fine-tuning** — the headline demonstration that the NN actuator model closes the hydraulic reality gap. The soil-adaptive results (RA-L 7(4):9778–9785 + IROS 2022) show bucket filling transferring from FEE-simulated soil to real digging on the same M545. The test site's soil was relatively soft, so the authors buried a block of granite to emulate extremely hard soil; a related journal paper — Egli, Terenzi & Hutter, "Reinforcement learning-based bucket filling for autonomous excavation," *IEEE T-FR* vol. 1, pp. 170–191, 2024 — carries the bucket-filling line further, under a different coauthor set.

**Limitations**: one machine class — everything is on the instrumented M545, and the actuator model must be re-learned per machine; testbed-vs-site: ETH test pits and controlled digging, not production sites; autonomy covers the *arm skill* (trajectory following, bucket filling) — where to dig, task sequencing, and site logistics remain outside; interventions are those of a supervised research trial, not reported field-duty statistics.

> [!question] Reading the claim · 핵심 주장 읽는 법
> "a general approach" claims generality across *arm motions and tasks on a hydraulically actuated machine, given its learned actuator model* — read it as a reusable sim-to-real recipe for hydraulics, not as machine-general or site-general autonomy. Likewise "soil-adaptive" means online adaptation across the soils tested without parameter identification — evidence of a mechanism, not proof of all-soil generality.

## 한국어

**한 줄 요약**: RL 정책이 실제 유압 굴착기 팔을 **파인튜닝 없이** 구동한다 — 학습 시뮬레이션에 기계 데이터로 학습한 *밸브/액추에이터 동역학의 신경망 모델*이 내장되어 있기 때문이다 — 그리고 자매 논문(soil-adaptive)은 같은 기계에서 RL을 버킷 채우기에 적용해, 토질 파라미터를 한 번도 식별하지 않고 토질 간 온라인으로 적응한다. 자매 논문은 학습된 액추에이터 모델을 다시 쓰지 않는다: 정책은 관절 속도를 출력하고, 기존 방식의 밸브 유량 제어기가 이를 추종한다.

**계보에서의 위치**: [[01-canonical-papers/notes/8-construction/heap|HEAP]] 플랫폼 위의 학습 다리 — 플랫폼 논문이 힘 제어 가능한 유압과 완전 상태 센싱을 확립한 뒤, 이 두 편은 *학습된* 제어가 그 쇳덩이에 어떻게 올라가는지 보여주며, [[01-canonical-papers/notes/8-construction/ext|ExT]]의 직계 방법론적 조상이다. RSL의 4족 로봇 액추에이터 넷 트릭(Hwangbo et al. 2019, ANYmal)을 유압으로 이식한 것이다.

> [!tip] 핵심 직관 · Key intuition
> 학습한 구동기 모델이 측정한 유압 행동을 정책 학습 시뮬레이터에 넣는다. 밸브 명령과 동작 사이의 특정 불일치를 겨냥한다. 토질 적응 변형에는 기억이 없다. 측정한 관절 토크와 자신의 직전 명령에 반응하므로, 변하는 저항이 관측값에 바로 드러난다.

**방법** (리터러시 수준): 유압 밸브가 sim-to-real의 병목이다 — 데드밴드, 지연, 유량 비선형성은 해석적 시뮬레이터가 틀리게 만드는 것들이다. 그래서: (1) 실기계 데이터를 기록해 밸브 명령→관절 운동을 매핑하는 NN 액추에이터 모델을 학습하고; (2) 그 모델을 학습 시뮬레이터에 내장하고; (3) **파일럿단 밸브 명령**을 직접 출력하는 RL 정책을 학습하고; (4) 실기계에 그대로 배치한다. 자매 논문은 방식이 다르다. 해석적 FEE(토공 기본 방정식) 토양 모델에 대해 시뮬레이션에서 버킷 채우기를 학습하며, 매 에피소드마다 토질 파라미터를 균등 분포로 뽑는다: 점착력 0–105 kPa, 부착력 0부터 점착력까지, 내부 마찰각 0.3–0.8 rad, 단위중량 17–22 kN/m³, 토양–버킷 마찰각 0.2–0.4 rad, 공동 압력 계수 0–300, 토양 높이는 운전실 아래 0.5–2.0 m다(표 I, §III-D). 정책은 순환 구조가 없는 평범한 2층 MLP(128, 128)다. 적응할 수 있는 이유는 27개 관측값에 실린더 압력으로 추정한 팔 관절 토크와 직전 속도 명령이 들어 있기 때문이다(표 III). 출력은 관절 속도 4개이고, 기계에서는 PID와 피드포워드를 결합한 밸브 유량 제어기가 이를 추종한다(§IV-B). 학습에는 약 2억 샘플, 대략 7시간이 들었다.

**증거**: 일반 접근 정책이 실제 Menzi Muck M545(HEAP)에서 **파인튜닝 제로**로 동작한다 — NN 액추에이터 모델이 유압의 현실 격차를 닫는다는 대표 실증이다. Soil-adaptive 결과(RA-L 7(4):9778–9785 + IROS 2022)는 FEE 시뮬레이션 토양에서 학습한 버킷 채우기가 같은 M545의 실제 굴착으로 전이됨을 보인다. 시험장 토양이 비교적 무르기 때문에 저자들은 극도로 단단한 토양을 흉내 내려고 화강암 덩어리를 묻었다; 관련 저널 논문 — Egli, Terenzi, Hutter, "Reinforcement learning-based bucket filling for autonomous excavation," *IEEE T-FR* vol. 1, pp. 170–191, 2024 — 이 버킷 채우기 갈래를 이어가지만 공저자 구성이 다르다.

**한계**: 단일 기계 클래스 — 모든 것이 계측된 M545 위에서 이뤄지고, 액추에이터 모델은 기계마다 다시 학습해야 한다; 테스트베드 대 현장: ETH 시험 구덩이와 통제된 굴착이지, 생산 현장이 아니다; 자율성은 *팔 스킬*(궤적 추종, 버킷 채우기)을 다룬다 — 어디를 팔지, 작업 순서, 현장 물류는 밖에 있다; 개입은 감독된 연구 시험의 수준이지, 보고된 현장 운용 통계가 아니다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "a general approach"는 *학습된 액추에이터 모델이 주어진 유압 기계 위에서의 팔 동작·과제 전반*에 대한 일반성 주장이다 — 유압 기계를 위한 재사용 가능한 sim-to-real 레시피로 읽어야지, 기계 일반·현장 일반 자율성으로 읽으면 안 된다. 마찬가지로 "soil-adaptive"는 파라미터 식별 없이 시험된 토질들 간 온라인 적응을 뜻한다 — 메커니즘의 증거이지, 모든 토질에 대한 일반성 증명이 아니다.

### 연결

- 이전: [[01-canonical-papers/notes/8-construction/heap|HEAP]] · 다음: [[01-canonical-papers/notes/8-construction/ext|ExT]]
- 스트림: [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 자율화]] · [[05-construction-robotics/sim-to-real|sim-to-real 가이드]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading (◐)

- [ ] Say why hydraulic valve dynamics are the sim-to-real bottleneck, and how a neural actuator model resolves it · 유압 밸브 동역학이 왜 sim-to-real의 병목이고, NN 액추에이터 모델이 이를 어떻게 푸는지 말할 수 있다
- [ ] State the policy's inputs and outputs (machine state → pilot-stage valve commands) and what "zero real-machine fine-tuning" means · 정책의 입출력(기계 상태 → 파일럿단 밸브 명령)과 "실기계 파인튜닝 제로"의 의미를 말할 수 있다
- [ ] Separate the mechanism from the limits of the soil-adaptive paper's "adaptation without parameter identification" claim · soil-adaptive 논문의 "파라미터 식별 없는 적응" 주장의 메커니즘과 한계를 구분할 수 있다
- [ ] Explain the lineage HEAP (platform) → Egli RL (skill learning) → ExT (pretraining framework) · HEAP(플랫폼) → Egli RL(스킬 학습) → ExT(사전학습 프레임워크)로 이어지는 계보를 설명할 수 있다
