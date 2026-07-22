---
title: 1. Research Questions & Claims
tags: [research, claims, methodology]
---

## English

A topic names an area; a research question specifies an uncertain relationship that evidence can resolve. “Apply VLA to construction” is a direction. A useful question identifies the intervention, comparator, outcome, conditions, and scope.

> [!info] Depth target
> Turn a broad interest into a falsifiable question; separate research gaps from missing implementations; and align contribution and claim strength with evidence.

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

Topic은 영역의 이름이고 research question은 증거로 답할 수 있는 불확실한 관계다. “건설로봇에 VLA 적용”은 방향일 뿐이다. 좋은 질문은 조건, intervention, comparator, outcome과 scope를 명시하며 결과가 부정적일 수도 있어야 한다.

Research gap은 단순히 “아무도 안 했다”가 아니다. 설명되지 않은 실패, 맞지 않는 가정, 일반화 증거 부족, 비현실적 평가, 중요한 trade-off일 수 있다. Hypothesis, engineering objective, scientific/system/artifact contribution을 구분하고 descriptive·comparative·causal·generalization·mechanistic·safety claim마다 필요한 증거 강도를 맞춘다.

Claim–evidence 표를 실험 전에 작성하라. 무엇을 주장할지, 어떤 비교와 metric이 필요하며 어디까지 일반화하지 않을지를 먼저 적으면 결과가 나온 뒤 이야기를 바꾸는 것을 줄일 수 있다.
