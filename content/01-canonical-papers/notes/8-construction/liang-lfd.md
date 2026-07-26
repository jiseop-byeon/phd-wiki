---
title: "Teaching Robots Quasi-Repetitive Construction Tasks by Demonstration (Liang et al., 2020)"
authors: Ci-Jyun Liang, Vineet R. Kamat, Carol C. Menassa
affiliation: University of Michigan
venue: Automation in Construction
year: 2020
pdf: https://doi.org/10.1016/j.autcon.2020.103370
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Liang, Kamat & Menassa, Automation in Construction 2020** — [DOI](https://doi.org/10.1016/j.autcon.2020.103370)

## English

**One-line summary**: Imitation learning enters construction — human demonstrations (3,000 virtual + 85 real) teach a manipulator quasi-repetitive tasks, reaching **78% success** on a ceiling-tile installation testbed; the generalized-cylinder trajectory representation arrived in the 2022 JCCE follow-up (82.0% vs 71.3%).

**Method**: learning from demonstration (LfD) from a mix of virtual (VR) and physical demonstrations. The follow-up (Liang et al., JCCE 2022) added the *generalized cylinder* representation — a tube of admissible trajectories around the demonstrated path — so the robot can vary execution within the tube instead of replaying one trajectory (82.0% vs 71.3% in that paper's comparison). "Quasi-repetitive" names the construction task class this fits: tasks that repeat, but with per-instance geometric variation (each tile, stud, or panel slightly different), too variable for fixed automation yet too repetitive to justify per-instance programming.

**Evidence (with numbers)**: ceiling-tile installation on a lab testbed, **78% task success**. This is a **testbed, not a site**; after the demonstration phase the robot executes autonomously, with the human's role reduced to demonstrator.

**Reading it with [[02-foundations/rl-basics|RL 기초 §6]]**: this is behavioral-cloning territory, and the 78% ceiling is what compounding error looks like in practice — states outside the demonstrated tube carry no supervision, so drift goes uncorrected (covariate shift). The line's next move, [[yu-imitation|Yu]]'s cloud/VR hierarchical IL, attacks exactly these two walls: demonstration cost and brittleness off the demonstrated states.

**Limitations**: a single task family; trajectory-level imitation without a visual policy; 78% is a proof of feasibility, not deployment readiness. Ci-Jyun Liang now leads the CROSS Lab at Stony Brook, continuing the line as faculty.

## 한국어

**한 줄 요약**: 모방학습이 건설에 들어온다 — 인간 시연(가상 3,000 + 실제 85)이 매니퓰레이터에게 준반복 과제를 가르쳐 천장 타일 설치 테스트베드에서 **78% 성공**에 도달한다; 일반화 원통(generalized cylinder) 궤적 표현은 2022 JCCE 후속에서 도입됐다(82.0% vs 71.3%).

**방법**: 가상(VR)과 실제 시연을 혼합한 시연 학습(LfD). 후속 연구(Liang et al., JCCE 2022)가 *일반화 원통* 표현 — 시연 경로 주위의 허용 궤적 튜브 — 을 더해, 로봇이 한 궤적을 재생하는 대신 튜브 안에서 실행을 변주할 수 있게 했다(그 논문의 비교에서 82.0% vs 71.3%). "준반복(quasi-repetitive)"은 이것이 맞는 건설 과제 부류의 이름이다: 반복되지만 개체별 기하 변동이 있는 과제(타일·스터드·패널 하나하나가 조금씩 다름) — 고정 자동화에는 너무 가변적이고, 개체별 프로그래밍에는 너무 반복적이다.

**증거 (수치와 함께)**: 실험실 테스트베드의 천장 타일 설치, **과제 성공률 78%**. 이것은 **현장이 아니라 테스트베드**다; 시연 단계 이후 로봇은 자율적으로 실행하며, 인간의 역할은 시연자로 줄어든다.

**[[02-foundations/rl-basics|RL 기초 §6]]으로 읽기**: 이것은 행동 복제(BC)의 영토이고, 78%라는 천장은 오차 누적이 실전에서 어떤 모습인지 보여준다 — 시연된 튜브 밖의 상태에는 감독이 없으므로 이탈이 교정되지 않는다(공변량 이동). 계열의 다음 수인 [[yu-imitation|Yu]]의 클라우드/VR 계층적 모방학습은 정확히 이 두 벽 — 시연 비용과 시연 상태 밖의 취약성 — 을 공략한다.

**한계**: 단일 과제 부류; 시각 정책 없는 궤적 수준 모방; 78%는 실현 가능성의 증명이지 배치 준비가 아니다. Ci-Jyun Liang은 현재 Stony Brook의 CROSS Lab을 이끌며 교수로서 이 계열을 잇고 있다.

### 연결

- 이전: [[lundeen-2019|Lundeen]] (기하 적응) · 다음: [[yu-imitation|Yu]] (클라우드/VR 계층적 모방학습)
- 기초: [[02-foundations/rl-basics|RL 기초 §6]] (BC, 공변량 이동, 오차 누적)
- 계보: Kamat/Menassa → Liang(Stony Brook CROSS Lab) · [[05-construction-robotics/lineage|건설로봇 계보]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 78% is an entry proof on a testbed, not deployment readiness — read it as "LfD is feasible for this class of construction task", and read the gap to 100% as a miniature lecture on covariate shift. This paper's historical weight is in its position rather than its number: it is the first term of the construction robot-learning line (demonstration to hierarchy to skill library).
>
> 78%는 테스트베드 위의 진입 증명이지 배치 준비도가 아니다 — "건설 과제 부류에 LfD가 실현 가능하다"로 읽고, 100%와의 간극은 공변량 이동 강의의 축소판으로 읽어라. 이 논문의 역사적 의미는 수치보다 위치에 있다: 건설 로봇 학습 계열(시연 → 계층 → 스킬 라이브러리)의 첫 항이다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading (◐)

- [ ] Explain what a "quasi-repetitive task" is and why it is the right task class for LfD · "준반복 과제"가 무엇이고 왜 LfD에 맞는 과제 부류인지 설명할 수 있다
- [ ] Say how the generalized-cylinder representation differs from simple trajectory replay · 일반화 원통 표현이 단순 궤적 재생과 어떻게 다른지 말할 수 있다
- [ ] Interpret the 78% success rate in the vocabulary of BC and covariate shift · 78% 성공률을 BC/공변량 이동의 어휘로 해석할 수 있다
- [ ] Say why this paper is the *entry point of learning* in the Michigan line (Feng → Lundeen → Liang → Yu) · 미시간 계열(Feng → Lundeen → Liang → Yu)에서 이 논문이 "학습의 진입점"인 이유를 말할 수 있다
