---
title: 1. Research Questions & Claims
tags: [research, claims, methodology]
---

## English

A topic names an area; a research question specifies an uncertain relationship that evidence can resolve. “Apply VLA to construction” is a direction. A useful question identifies the intervention, comparator, outcome, conditions, and scope.

> [!info] Depth target
> Turn a broad interest into a falsifiable question; separate research gaps from missing implementations; and align contribution and claim strength with evidence.

> [!note] Prerequisites
> [[01-canonical-papers/how-to-read|How to Read Papers]] · [[02-foundations/ml-practice|ML Practice & Evaluation]]

### 1. Topic → problem → question

| Level | Example |
|---|---|
| Topic | VLA for construction manipulation |
| Problem | scarce demonstrations limit adaptation to new material layouts |
| Question | Under a fixed demonstration budget, does action-chunk fine-tuning of a pretrained VLA improve closed-loop success on held-out layouts over vision-only behavior cloning? |

The final question states a condition, intervention, comparator, outcome, and test distribution. It can be answered negatively.

### 2. A gap is not merely “nobody has done this”

A defensible gap may be an unexplained failure, incompatible assumptions, missing evidence, poor generalization, unrealistic evaluation, or a theoretically/operationally important trade-off. Adding a model to a new dataset is an engineering activity unless it tests a consequential question.

### 3. Hypotheses and contributions

- **Hypothesis:** expected relationship that can be tested.
- **Engineering objective:** system capability to build.
- **Scientific contribution:** new knowledge supported by evidence.
- **System contribution:** integration or capability whose novelty may lie in architecture, deployment, or evaluation.
- **Artifact contribution:** useful code, dataset, benchmark, or platform.

A project can contribute a system without inventing a new algorithm, but must identify what knowledge or capability the system establishes beyond assembly effort.

### 4. Claim types

| Claim | Required caution |
|---|---|
| Descriptive | what was observed in the studied sample |
| Comparative | performance relative to a defined baseline and setting |
| Causal | alternative explanations must be controlled or modeled |
| Generalization | target distribution and shift must be defined |
| Mechanistic | evidence must isolate why the method works |
| Safety/reliability | exposure, severity, rare failures, and system boundaries matter |

“Ablation improves performance when component X is present” supports a scoped dependency; it does not prove the author's complete causal story.

### 5. Scope and assumptions

Write the population, environment, embodiment, sensors, data regime, task, intervention policy, and evaluation horizon. Assumptions are not weaknesses by default; hidden assumptions are.

### 6. Worked rewrite

Weak: **Can world models improve construction robots?**

Stronger: **For autonomous excavation in variable soil, does a learned latent dynamics model reduce bucket-path tracking error and recovery interventions relative to model-free behavior cloning when both use the same demonstrations and MPC safety constraints?**

This still needs operational definitions for soil variation, intervention, and the world-model planning procedure.

### 7. Claim–evidence table

Before experiments, make this table:

| Intended claim | Necessary comparison | Metric | Boundary |
|---|---|---|---|
| better data efficiency | same model/evaluation at several data budgets | learning curve and uncertainty | tested tasks/layouts only |
| better recovery | matched failure perturbations | recovery success/time | specified failure types |
| safer operation | comparable exposure and hazard definitions | violations, near misses, severity | not certification |

### After reading

- Convert a topic into a falsifiable question.
- Explain why absence of prior implementation is not automatically a research gap.
- Distinguish hypothesis, engineering objective, and contribution.
- Match claim type to the evidence it requires.
- State scope and assumptions before using words such as robust or general.

### Self-check

1. Rewrite “Does diffusion help robot planning?” as a testable question.
2. Why can a larger benchmark score fail to establish the claimed mechanism?
3. What would falsify a data-efficiency claim?

> [!tip]- Answers
> 1. Specify task/distribution, diffusion intervention, matched comparator, data budgets, metric, and closed-loop conditions. 2. Several components or data changes may differ; score alone does not isolate cause. 3. No advantage across predeclared low-data budgets under matched compute/model/evaluation, or an advantage explained by unequal data or tuning.

## 한국어

Topic은 영역의 이름이고, research question은 증거가 해소할 수 있는 불확실한 관계를
명시한다. "건설에 VLA 적용"은 방향이다. 쓸모 있는 질문은 개입(intervention), 비교
대상(comparator), 결과(outcome), 조건, 범위를 짚는다.

> [!info] 깊이 목표
> 넓은 관심을 반증 가능한 질문으로 바꾼다; research gap과 "아직 구현이 없음"을 구분한다;
> 기여와 주장 강도를 증거에 맞춘다.

> [!note] 선수 지식
> [[01-canonical-papers/how-to-read|How to Read Papers]] · [[02-foundations/ml-practice|ML 실무와 평가]]

### 1. Topic → problem → question

| 수준 | 예 |
|---|---|
| Topic | 건설 매니퓰레이션을 위한 VLA |
| Problem | 부족한 시연이 새로운 자재 배치에의 적응을 제한한다 |
| Question | 고정된 시연 예산 아래, 사전학습 VLA의 action-chunk 파인튜닝이 held-out 배치에서 vision-only 행동 복제보다 폐루프 성공률을 높이는가? |

최종 질문은 조건, 개입, 비교 대상, 결과, 시험 분포를 명시한다. **부정적으로도 답할 수
있어야 한다.**

### 2. Gap은 "아무도 안 했다"가 아니다

방어 가능한 gap은 설명되지 않은 실패, 양립 불가능한 가정, 빠진 증거, 나쁜 일반화,
비현실적 평가, 이론적·운용적으로 중요한 트레이드오프일 수 있다. 새 데이터셋에 모델을
얹는 것은 중대한 질문을 시험하지 않는 한 엔지니어링 활동이다.

### 3. 가설과 기여

- **가설:** 시험 가능한 기대 관계.
- **엔지니어링 목표:** 구축할 시스템 능력.
- **과학적 기여:** 증거가 지지하는 새 지식.
- **시스템 기여:** 구조·배포·평가에 신규성이 있을 수 있는 통합·능력.
- **산출물 기여:** 유용한 코드, 데이터셋, 벤치마크, 플랫폼.

새 알고리즘 없이 시스템으로 기여할 수 있다 — 단 조립 노력 너머에 그 시스템이 어떤
지식·능력을 확립하는지 밝혀야 한다.

### 4. 주장의 유형

| 주장 | 요구되는 주의 |
|---|---|
| 기술적(descriptive) | 연구된 표본에서 관찰된 것 |
| 비교적 | 정의된 베이스라인·설정 대비 성능 |
| 인과적 | 대안 설명이 통제·모델링돼야 함 |
| 일반화 | 대상 분포와 이동(shift)이 정의돼야 함 |
| 기전적(mechanistic) | 방법이 *왜* 통하는지 분리하는 증거 |
| 안전/신뢰성 | 노출, 심각도, 희귀 실패, 시스템 경계가 중요 |

"구성요소 X가 있을 때 절제 실험 성능이 오른다"는 범위가 한정된 의존성을 지지할 뿐,
저자의 완전한 인과 이야기를 증명하지 않는다.

### 5. 범위와 가정

모집단, 환경, embodiment, 센서, 데이터 체제, 과제, 개입 정책, 평가 지평을 적어라.
가정은 그 자체로 약점이 아니다 — **숨긴 가정**이 약점이다.

### 6. 고쳐 쓰기 예제

약함: **월드모델이 건설로봇을 개선할 수 있는가?**

더 강함: **가변 토질의 자율 굴착에서, 학습된 잠재 동역학 모델이 같은 시연과 MPC 안전
제약을 쓰는 model-free 행동 복제 대비 버킷 경로 추종 오차와 회복 개입을 줄이는가?**

이것도 토질 변동, 개입, 월드모델 계획 절차의 조작적 정의가 더 필요하다.

### 7. 주장–증거 표

실험 전에 이 표를 만들어라:

| 의도한 주장 | 필요한 비교 | 지표 | 경계 |
|---|---|---|---|
| 더 나은 데이터 효율 | 여러 데이터 예산에서 같은 모델/평가 | 학습 곡선과 불확실성 | 시험한 과제/배치에 한정 |
| 더 나은 회복 | 짝지은 실패 교란 | 회복 성공/시간 | 명시된 실패 유형 |
| 더 안전한 운용 | 대등한 노출과 hazard 정의 | 위반, near miss, 심각도 | 인증이 아님 |

### 읽고 나면 말할 수 있어야 하는 것

- topic을 반증 가능한 질문으로 변환할 수 있다
- 선행 구현의 부재가 자동으로 research gap이 아닌 이유를 설명할 수 있다
- 가설·엔지니어링 목표·기여를 구분할 수 있다
- 주장 유형을 그것이 요구하는 증거와 짝지을 수 있다
- robust·general 같은 단어를 쓰기 전에 범위와 가정을 명시할 수 있다

### 스스로 점검

1. "디퓨전이 로봇 계획에 도움이 되는가?"를 시험 가능한 질문으로 다시 써라.
2. 더 큰 벤치마크 점수가 주장한 기전을 확립하지 못할 수 있는 이유는?
3. 데이터 효율 주장을 반증하는 것은 무엇인가?

> [!tip]- 정답 · Answers
> 1. 과제/분포, 디퓨전 개입, 짝지은 비교 대상, 데이터 예산, 지표, 폐루프 조건을 명시한다.
> 2. 여러 구성요소나 데이터가 함께 달라졌을 수 있다 — 점수만으로는 원인을 분리하지 못한다.
> 3. 미리 선언한 저데이터 예산들에서 대등한 컴퓨트/모델/평가 아래 이점이 없거나, 이점이 불평등한 데이터·튜닝으로 설명되는 것.
