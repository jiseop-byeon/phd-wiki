---
title: 9. ML Practice & Evaluation
tags: [foundations]
---

> [[02-foundations/overview|0. Overview]] — 이 페이지에 필요한 사전 수학과 연결 지도 · prerequisites & connection map

## English

The craft knowledge every paper assumes: how models are trained, validated, and — above
all — *measured*. This page is the decoder for every "Results" table in the wiki.

### 1. Data splits — the one sacred rule

- **Train / validation / test**: fit on train; tune hyperparameters and pick checkpoints
  on validation; touch test **once**, at the end. Every time a decision is influenced by
  test performance, the test set silently becomes a validation set — and reported numbers
  inflate.
- **Distribution shift**: test data from a different distribution than train (new site,
  new robot, new lighting) — the *actual* condition of robotics. This is why papers report
  "seen/unseen" splits ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]]) and OOD evaluations, and
  why [[01-canonical-papers/notes/3-vlm/clip|CLIP]]'s robustness results mattered so much.
- Data leakage: test information sneaking into training (duplicates, temporal overlap,
  pretraining contamination — the [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] paper's own
  headache). First thing to suspect when numbers look too good.

### 2. Overfitting and the regularization umbrella

- **Overfitting**: train loss ↓ while validation loss ↑ — memorizing instead of
  generalizing. **Underfitting**: both stay high. Diagnose with **learning curves** before
  anything else.
- Everything called "regularization" is one idea — *restrict or perturb the model so it
  can't just memorize*: weight decay (a Gaussian prior — [[02-foundations/probability|3. Probability §4]]),
  dropout ([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]), data augmentation
  ([[01-canonical-papers/notes/1-foundations/vgg|VGG]] onward), early stopping, and — the modern twist —
  *more data instead of more constraints* ([[01-canonical-papers/notes/1-foundations/scaling-laws|scaling laws]]).

### 3. The metrics dictionary (read any Results table)

| Task | Metric | What it means |
|---|---|---|
| Classification | accuracy, top-5 | fraction correct (top-5: truth within 5 guesses — ImageNet convention) |
| Classification (imbalanced) | precision / recall / F1 | of flagged, how many real / of real, how many caught / their harmonic mean |
| Detection | **IoU**, **mAP** | box overlap ratio; mean average precision over classes & IoU thresholds |
| Segmentation | mIoU | IoU averaged over classes |
| Generation (image) | **FID** | distribution distance between generated and real features — lower is better |
| Language modeling | perplexity | $e^{\text{cross-entropy}}$ ([[02-foundations/information-theory|5. Info Theory §2]]) |
| Translation/captioning | BLEU | n-gram overlap with references |
| Robotics | **success rate** | fraction of trials achieving the goal — plus *which* trials (seen/unseen) matters more than the number |
| Retrieval | recall@k | truth within top-k results |

- Read metrics adversarially: success rate on *what* distribution, of *how many* trials,
  with *what* variance? A 90% on 10 trials is a coin with extra steps.

### 4. The grammar of experiments

- **Baseline**: what you must beat (and it must be *tuned* — weak baselines are the
  field's chronic sin). **Ablation**: remove one component to show it mattered — the
  evidence connecting method to result. **SOTA**: state of the art; impressive but
  fragile — benchmark-specific and often compute-confounded.
- Fair comparison checklist when reading: same data? same compute/params? same evaluation
  protocol? tuned baselines? If a table doesn't answer these, the numbers are decoration.
- Seeds and variance: deep learning results wobble across random seeds; serious papers
  report mean ± std over several seeds — robotics papers over several *rollouts and scenes*.

### Self-check

1. A model picks its best checkpoint by test accuracy. What went wrong, and in which
   direction is the reported number biased?
2. Precision 0.9 / recall 0.3 crack detector: what does it miss, and when is that
   acceptable on a construction site?
3. Why is FID computed on *features* (Inception embeddings) instead of pixels?
4. In a VLA paper, "76% success on unseen instructions" — list three questions you'd ask
   before believing it matters.

## 한국어

모든 논문이 전제하는 장인적 지식: 모델을 어떻게 학습·검증하고, 무엇보다 어떻게 *재는가*.
이 페이지는 위키의 모든 "Results" 표를 읽는 해독기다.

### 1. 데이터 분할 — 단 하나의 신성한 규칙

- **Train / validation / test**: train으로 적합하고, validation으로 하이퍼파라미터 튜닝과
  체크포인트 선택을 하고, test는 맨 끝에 **한 번만** 만진다. 결정이 test 성능의 영향을
  받는 순간 test는 조용히 validation이 되고 — 보고 수치는 부풀려진다.
- **분포 이동**: train과 다른 분포의 test(새 현장, 새 로봇, 새 조명) — 로보틱스의 *실제*
  조건이다. 논문들이 "seen/unseen" 분할([[01-canonical-papers/notes/4-vla/rt-1|RT-1]])과 OOD
  평가를 보고하는 이유이고, [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 강건성 결과가 그토록
  중요했던 이유다.
- 데이터 누수: test 정보가 학습에 스며드는 것(중복, 시간적 겹침, 사전학습 오염 —
  [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] 논문 스스로의 골칫거리). 숫자가 너무 좋아 보일
  때 첫 번째로 의심할 것.

### 2. 과적합과 정규화라는 우산

- **과적합**: train 손실은 ↓인데 validation 손실이 ↑ — 일반화 대신 암기. **과소적합**:
  둘 다 높음. 무엇보다 먼저 **학습 곡선**으로 진단하라.
- "정규화"라 불리는 모든 것은 하나의 아이디어다 — *모델이 그냥 암기할 수 없도록 제약하거나
  교란하라*: weight decay(가우시안 사전 — [[02-foundations/probability|3. 확률 §4]]),
  dropout([[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]]), 데이터 증강
  ([[01-canonical-papers/notes/1-foundations/vgg|VGG]] 이후), early stopping, 그리고 현대적 반전 —
  *제약 대신 더 많은 데이터*([[01-canonical-papers/notes/1-foundations/scaling-laws|스케일링 법칙]]).

### 3. 지표 사전 (어떤 Results 표든 읽기)

| 과제 | 지표 | 의미 |
|---|---|---|
| 분류 | accuracy, top-5 | 맞춘 비율 (top-5: 정답이 5개 후보 안 — ImageNet 관례) |
| 분류 (불균형) | precision / recall / F1 | 표시한 것 중 진짜 비율 / 진짜 중 잡아낸 비율 / 둘의 조화평균 |
| 검출 | **IoU**, **mAP** | 박스 겹침 비율; 클래스·IoU 문턱에 걸친 평균 정밀도 |
| 분할 | mIoU | 클래스 평균 IoU |
| 생성 (이미지) | **FID** | 생성/실제 특징 분포 사이 거리 — 낮을수록 좋다 |
| 언어모델 | perplexity | $e^{\text{교차 엔트로피}}$ ([[02-foundations/information-theory|5. 정보이론 §2]]) |
| 번역/캡셔닝 | BLEU | 참조문과의 n-gram 겹침 |
| 로보틱스 | **success rate** | 목표 달성 시행 비율 — 숫자보다 *어떤* 시행(seen/unseen)인지가 더 중요 |
| 검색 | recall@k | 정답이 상위 k개 안 |

- 지표는 적대적으로 읽어라: *어떤* 분포에서, *몇 번의* 시행으로, *분산은* 얼마인 success
  rate인가? 10회 시행의 90%는 절차를 거친 동전 던지기다.

### 4. 실험의 문법

- **베이스라인**: 이겨야 하는 대상(그리고 *튜닝된* 것이어야 한다 — 약한 베이스라인은 이
  분야의 고질병). **절제 실험(ablation)**: 구성 요소 하나를 빼서 그것이 중요했음을 보이기
  — 방법과 결과를 잇는 증거. **SOTA**: 최고 성능; 인상적이지만 취약하다 — 벤치마크
  특정적이고 연산량과 교락되기 일쑤.
- 읽을 때의 공정 비교 체크리스트: 같은 데이터? 같은 연산/파라미터? 같은 평가 프로토콜?
  튜닝된 베이스라인? 표가 이에 답하지 않으면 그 숫자는 장식이다.
- 시드와 분산: 딥러닝 결과는 랜덤 시드에 따라 흔들린다; 진지한 논문은 여러 시드의 평균 ±
  표준편차를, 로보틱스 논문은 여러 *롤아웃과 장면*에 걸쳐 보고한다.

### 스스로 점검

1. 어떤 모델이 test 정확도로 최적 체크포인트를 골랐다. 무엇이 잘못됐고, 보고 수치는 어느
   방향으로 편향되는가?
2. Precision 0.9 / recall 0.3인 균열 감지기: 무엇을 놓치고, 건설 현장에서 그것이 언제
   용인 가능한가?
3. FID는 왜 픽셀이 아니라 *특징*(Inception 임베딩)에서 계산하는가?
4. VLA 논문의 "unseen 지시 76% 성공" — 믿기 전에 물어야 할 질문 세 개를 들어라.

> [!tip]- 스스로 점검 정답 · Answers
> 1. 테스트가 검증 집합 역할을 해버렸다 — 보고 수치는 위로(낙관적으로) 편향되고, 실제 일반화 성능은 그보다 낮다.
> 2. 진짜 균열의 70%를 놓친다(재현율 0.3). 오탐 처리 비용이 크고 뒤에 정밀 점검이 따로 있는 1차 스크리닝이면 용인 가능; 이 감지기 하나로 안전 결정을 내린다면 불가.
> 3. 픽셀 거리는 지각 품질과 무관하다(한 픽셀 평행이동에도 크게 벌점) — Inception 특징 공간이 의미적 유사성을 반영하기 때문에 특징 분포 거리로 잰다.
> 4. ① 몇 회 시행이고 분산은 얼마인가 ② "unseen"의 정의는(새 물체? 새 지시문? 새 장면?) ③ 어떤 베이스라인 대비이며 실패 사례 분석이 있는가.
