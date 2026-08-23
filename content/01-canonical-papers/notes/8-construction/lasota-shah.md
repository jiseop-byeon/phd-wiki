---
title: "Human-Aware Motion Planning in Close-Proximity HRC (Lasota & Shah, 2015)"
authors: Przemyslaw A. Lasota, Julie A. Shah
affiliation: MIT, Interactive Robotics Group
venue: Human Factors
year: 2015
pdf: https://journals.sagepub.com/doi/pdf/10.1177/0018720814565188
companion: https://dspace.mit.edu/bitstream/handle/1721.1/124626/2018_Unhelkar_Lasota_Shah_etal_RA_Letters.pdf
tags: [paper, hrc]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Lasota & Shah**, "Analyzing the Effects of Human-Aware Motion Planning on Close-Proximity Human–Robot Collaboration," *Human Factors* 2015 — [PDF](https://journals.sagepub.com/doi/pdf/10.1177/0018720814565188) · [2018 RA-L companion](https://dspace.mit.edu/bitstream/handle/1721.1/124626/2018_Unhelkar_Lasota_Shah_etal_RA_Letters.pdf)

> [!note] Math on-ramp · 수학 준비물
> [[04-robotics/hri-safety|11. HRI & Safety §7–§8]] — this is a human-study paper, so its evidence stands or falls on within/between-subject design, counterbalancing, and the pairing of subjective with objective measures. That section is the checklist.
> [[04-robotics/hri-safety|11. HRI·안전 §7~§8]] — 인간 실험 논문이므로 증거의 성패가 피험자 내/간 설계, 균형화, 주관·객관 측정의 병행에 달려 있다. 그 절이 체크리스트다.

## English

**One-line summary**: When a robot plans its motion *around a prediction of the human's motion*, both objective fluency and subjective experience improve simultaneously — the manufacturing-HRC result that construction's worker-centered stream keeps importing.

**Method**: a controlled shared-workspace experiment — human and robot performing a collaborative placement task in close proximity, with the robot running either a standard or a human-aware motion planner (one that adapts trajectories to predicted human actions). Motion capture provides objective fluency metrics; questionnaires provide subjective ones.

**Evidence (with numbers)**: with the human-aware planner, tasks completed **5.57% faster**, concurrent human-robot motion rose **19.9%**, human idle time fell **2.96%**, robot idle time fell **17.3%**, and human-robot separation distance grew **15.1%**. Subjectively, participants agreed significantly more strongly that the robot stayed out of their way, that they felt safer and more comfortable, and that they trusted it as a teammate. The 2018 RA-L companion (Lasota, Unhelkar, ..., Shah, "Human-Aware Robotic Assistant for Collaborative Assembly," RA-L 3(3)) carried the idea toward practice: a human-aware robotic assistant **fielded in a BMW test environment replicating final-assembly work** — the authors themselves note the demonstration is *not* representative of a real factory deployment.

**Testbed vs site, autonomy**: 2015 is a lab experiment; 2018 moves to a BMW *test environment* replicating final assembly — which the authors themselves state is **not** representative of a deployed line — and neither is a construction site. The robot is autonomous at the motion level inside a collaborative cell; the human is a co-worker in the shared workspace, not an operator.

**What construction borrows, and what does not transfer**: construction borrows the metric vocabulary (fluency, concurrent motion, idle time, separation distance, perceived safety) and the twin finding — motion-level adaptation pays off in productivity *and* comfort at once, so safety and efficiency are not a trade-off. What does not transfer is the setting that made the result cheap to obtain: a fixed workcell, a repeatable task, reliable human tracking, a stable floor. Construction sites are unstructured and tasks are quasi-repetitive, which is why [[05-construction-robotics/hrc-worker-centered|stream 6]] must re-derive these results under site constraints rather than cite them.

## 한국어

**한 줄 요약**: 로봇이 *인간 동작의 예측을 중심으로* 모션을 계획하면 객관적 유창성과 주관적 경험이 동시에 개선된다 — 건설의 작업자 중심 스트림이 계속 수입하는 제조업 HRC의 결과.

**방법**: 통제된 공유 작업공간 실험 — 인간과 로봇이 근접 거리에서 협업 배치 과제를 수행하며, 로봇은 표준 모션 플래너 또는 인간 인지 모션 플래너(예측된 인간 행동에 궤적을 적응시키는 플래너)를 사용한다. 모션 캡처가 객관적 유창성 지표를, 설문이 주관적 지표를 제공한다.

**증거 (수치와 함께)**: 인간 인지 플래너에서 과제 완료가 **5.57% 빨라졌고**, 인간-로봇 동시 동작이 **19.9% 증가**, 인간 유휴 시간이 **2.96% 감소**, 로봇 유휴 시간이 **17.3% 감소**, 인간-로봇 이격 거리가 **15.1% 증가**했다. 주관적으로 참가자들은 로봇이 방해되지 않았고, 더 안전하고 편안하게 느꼈으며, 팀 동료로서 더 신뢰했다는 데 유의하게 더 강하게 동의했다. 2018 RA-L 자매 논문(Lasota, Unhelkar, ..., Shah, "Human-Aware Robotic Assistant for Collaborative Assembly," RA-L 3(3))은 이 아이디어를 실전 쪽으로 가져갔다: 인간 인지 로봇 어시스턴트를 **최종 조립 작업을 재현한 BMW 테스트 환경에 투입**했다 — 저자들 스스로 이 시연이 실제 공장 배치를 대표하지 *않는다*고 명시한다.

**테스트베드 대 현장, 자율성**: 2015는 실험실 실험이고, 2018은 최종 조립을 모사한 BMW *테스트 환경*으로 옮겨간다 — 저자들 스스로 배치된 라인을 대표하지 **않는다**고 밝히고 있고, 둘 중 어느 것도 건설 현장은 아니다. 로봇은 협업 셀 안에서 모션 수준의 자율성을 갖고, 인간은 운전자가 아니라 공유 작업공간의 동료다.

**건설이 빌려오는 것과 이전되지 않는 것**: 건설이 빌려오는 것은 지표 어휘(유창성, 동시 동작, 유휴 시간, 이격 거리, 체감 안전)와 쌍둥이 발견 — 모션 수준 적응이 생산성*과* 편안함에 동시에 이득이 되므로 안전과 효율이 트레이드오프가 아니라는 것이다. 이전되지 않는 것은 이 결과를 값싸게 만든 환경이다: 고정된 워크셀, 반복 가능한 과제, 신뢰할 수 있는 인간 추적, 안정된 바닥. 건설 현장은 비구조적이고 과제는 준반복적이라, [[05-construction-robotics/hrc-worker-centered|stream 6]]은 이 결과를 인용하는 대신 현장 제약 아래서 다시 유도해야 한다.

### 연결

- 스트림: [[05-construction-robotics/hrc-worker-centered|stream 6]] (건설 HRC가 수입하는 기준선)
- 기초: [[04-robotics/hri-safety|11. HRI & Safety]] (인간 인지 계획과 안전 지표의 원류)

> [!question] 핵심 주장 읽는 법 · Reading the claim
> The numbers (5.57%, 19.9%, …) come from a controlled laboratory task — what transfers to construction is the direction, not the magnitude: "human-aware planning improves objective fluency and subjective safety *at the same time*." That direction is robust; the magnitudes are task-specific and must be re-measured on unstructured sites. Keep the 2018 fielding distinct as well: a manufacturing test environment, not a construction site.
>
> 수치(5.57%, 19.9%, ...)는 통제된 실험실 과제의 것이다 — 건설로 가져갈 것은 크기가 아니라 방향이다: "인간 인지 계획은 객관적 유창성과 주관적 안전감을 *동시에* 개선한다." 이 방향은 강건하지만, 크기는 과제 특정적이며 비구조적 현장에서는 재측정되어야 한다. 2018 배치도 제조업 현장이지 건설 현장이 아님을 구분하라.

### 읽고 나면 말할 수 있어야 하는 것 · After reading (◐)

- [ ] Name the fluency metrics (concurrent motion, idle time, separation distance) · 유창성 지표들(동시 동작, 유휴 시간, 이격 거리)을 이름과 함께 말할 수 있다
- [ ] State the twin finding — objective and subjective measures improve together — with its numbers · 쌍둥이 발견, 즉 객관적 지표와 주관적 지표가 함께 개선된다는 사실을 수치와 함께 말할 수 있다
- [ ] Separate what construction can borrow from this result from what does not transfer · 건설이 이 결과에서 빌려올 수 있는 것과 이전되지 않는 것을 구분할 수 있다
- [ ] State what the 2018 companion added (fielding in a BMW test environment) and its limits (a test environment, not a real factory; manufacturing, not construction) · 2018 자매 논문이 더한 것(BMW 테스트 환경 투입)과 그 한계(테스트 환경이지 실제 공장이 아니며, 제조업이지 건설이 아님)를 말할 수 있다
