---
title: 9. ML Practice & Evaluation
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/neural-network-basics|0.7]] (training, validation, hyperparameters) · [[02-foundations/probability|3. Probability §1]] (conditional probability, for precision/recall)
> [[02-foundations/neural-network-basics|0.7]](학습·검증·하이퍼파라미터) · [[02-foundations/probability|3. 확률 §1]](정밀도·재현율을 위한 조건부 확률)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Pages 1 to 8 were tools for reading a method. This page is the tool for reading the claim that the method
worked. Then [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Dynamics]] closes the track with the physics the manipulation work needs.*

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

<svg viewBox="0 0 470 216" style="max-width:100%;height:auto" role="img" aria-label="training and validation loss curves showing overfitting">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="50" y1="22" x2="50" y2="140"/><line x1="50" y1="140" x2="415" y2="140"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" stroke-dasharray="3 3"><line x1="220" y1="22" x2="220" y2="140"/></g>
  <path d="M50,36 C120,80 180,106 260,120 C320,128 375,132 410,133" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <path d="M50,34 C120,76 180,100 220,104 C285,110 345,86 410,58" fill="none" stroke="currentColor" stroke-width="1.9" stroke-dasharray="6 4"/>
  <g stroke="currentColor" stroke-width="1.9"><line x1="50" y1="164" x2="80" y2="164" stroke-dasharray="6 4"/><line x1="50" y1="182" x2="80" y2="182"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="14" y="30">loss</text>
    <text x="220" y="16" text-anchor="middle">early stopping</text>
    <text x="378" y="156">epochs &#8594;</text>
    <text x="88" y="168">validation loss &#8212; turns back up</text>
    <text x="88" y="186">training loss &#8212; keeps falling</text>
    <text x="50" y="208" opacity="0.85">right of the dashed line the model is memorizing, not generalizing</text>
  </g>
</svg>


- Regularization methods share one broad goal — *reduce harmful overfit* — but work through
  different mechanisms: weight decay (a Gaussian prior — [[02-foundations/probability|3. Probability §4]]),
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
| Language modeling | perplexity | $e^{\text{cross-entropy}}$ ([[02-foundations/information-theory\|5. Info Theory §2]]) |
| Translation/captioning | BLEU | n-gram overlap with references |
| Robotics | **success rate** | fraction of trials achieving the goal — plus *which* trials (seen/unseen) matters more than the number |
| Retrieval | recall@k | truth within top-k results |

**Worked example — why accuracy lies on imbalanced data.** A crack detector is run on
1,000 wall panels; 60 really have cracks. It flags 50 panels, of which 40 are real cracks.
Lay the four counts out:

| | predicted crack | predicted fine |
|---|---|---|
| **really cracked** | TP = 40 | FN = 20 |
| **really fine** | FP = 10 | TN = 930 |

- **Accuracy** $= \frac{TP+TN}{1000} = \frac{970}{1000} = 97.0\%$ — and a detector that
  simply says "fine" every single time scores $94.0\%$. Accuracy is nearly useless here.
- **Precision** $= \frac{TP}{TP+FP} = \frac{40}{50} = 0.80$ — of what you flagged, 80% was
  real. This is the number an inspector cares about: how often a dispatch is wasted.
- **Recall** $= \frac{TP}{TP+FN} = \frac{40}{60} = 0.67$ — of the real cracks, you caught
  two-thirds. **20 cracks were missed**, and that is the number a safety engineer cares about.
- **F1** $= \frac{2PR}{P+R} = \frac{2(0.8)(0.667)}{1.467} = 0.727$ — the harmonic mean, which
  stays low if *either* is low (an arithmetic mean would have hidden it at 0.73 vs a lopsided
  0.9/0.5 = 0.7).

The lesson to carry into every Results table: precision and recall trade against each other
through one threshold knob, so a paper reporting only the flattering one has told you half a
sentence. And in construction the asymmetry is real — a false alarm costs an inspection, a
missed crack can cost a structure.

- Read metrics adversarially: success rate on *what* distribution, of *how many* trials,
  with *what* variance? 9 successes in 10 trials has a wide confidence interval — report
  the counts and the uncertainty, not just "90%".

### 4. The grammar of experiments

- **Baseline**: what you must beat (and it must be *tuned* — weak baselines are the
  field's chronic sin). **Ablation**: remove one component to show it mattered — the
  evidence connecting method to result. **SOTA**: state of the art; impressive but
  fragile — benchmark-specific and often compute-confounded.
- Fair comparison checklist when reading: same data? same compute/params? same evaluation
  protocol? tuned baselines? If a table doesn't answer these, the numbers are decoration.
- Seeds and variance: deep learning results wobble across random seeds; serious reporting
  states the number of runs and an uncertainty measure fit to the experiment (std, standard
  error, CI, or paired tests). **Know which one you are looking at**: the standard deviation
  $\sigma$ says how much *individual runs* scatter and does not shrink as you add runs; the
  standard error $\sigma/\sqrt{n}$ says how well the *mean* is pinned down and does. At
  $n = 4$ they differ by a factor of 2, so a paper plotting the smaller one gets visually
  tighter error bars for free — check the caption before comparing two papers' bars — robotics papers report over several *rollouts and scenes*.

### 5. Evaluation pitfalls to watch for in papers

- **Cherry-picking**: qualitative figures show the best runs — ask what the *median* rollout looks like.
- **Statistical vs practical significance**: error-bar overlap alone does not settle significance — check what the bars represent (std? standard error? CI?), the number of runs, and pairedness. A +0.3%p gain may be noise or may matter (on a saturated benchmark); +5%p from one seed can be luck. Ask for variance first.
- **Oracle information**: does the method quietly use ground-truth state, perfect calibration, or human resets that deployment won't have?
- **Open-loop vs closed-loop evaluation**: predicting a good trajectory offline (open-loop) is far easier than executing under feedback with compounding errors (closed-loop) — robotics numbers are only comparable within the same regime.
- **Episode definition**: "success rate" depends on time limits, reset conditions, and what counts as success — two papers' 80% can mean different things.
- **Benchmark saturation**: near-ceiling benchmarks reward overfitting to quirks; gains there generalize least.

### 6. The training recipe, as vocabulary

An experimental section spends a paragraph on how the model was trained, in terms this wiki's
optimization page does not name. You are not reproducing the run — but these decide whether a
reported number is a property of the *method* or of the *recipe*, and an ablation that changes
one of them is not comparing what it claims.

| Term | What it is | Why it appears in the claim |
|---|---|---|
| **Learning-rate schedule** | the step size varies over training — a linear **warmup** for the first few % of steps, then **cosine decay**, usually to ~10% of peak rather than to zero | warmup stabilises Adam's early second-moment estimate and large-batch training; post-norm stacks additionally collapse without it (Xiong et al. 2020 measure BLEU 8.45 vs ~34). The final LR moves the last points of accuracy, so "same architecture, different schedule" is not a fair comparison |
| **Weight decay / AdamW** | AdamW shrinks weights directly, $w \leftarrow w(1-\eta\lambda)$, *decoupled* from the adaptive step — it is not an L2 term in the loss at all | the Gaussian-prior reading in [[02-foundations/probability\|3. Probability §4]] is an L2 penalty, and that equals weight decay **for SGD**. Under Adam the adaptive denominator distorts it per-coordinate, which is the whole reason AdamW exists |
| **Gradient accumulation** | average gradients over several forward passes before stepping, to simulate a batch the hardware cannot hold | it reproduces a large batch **only for losses that decompose per example**. It does *not* work for a contrastive loss: 8 × 512 gives 511 negatives, not 4095, which is why [[01-canonical-papers/notes/3-vlm/clip\|CLIP]]-style training needs cross-device all-gather instead. A paper's "batch size 4096" may be 8 × 512 — check which kind of loss it is |
| **Mixed precision** (fp16/bf16) | compute in 16 bits with an fp32 master copy of the weights. **fp16 additionally needs loss scaling**; **bf16 does not** | roughly halves memory and raises throughput. bf16 trades mantissa for fp32's exponent range — which is exactly why it drops loss scaling and why large models train stably in 16 bits |
| **EMA of weights** | keep a slowly-moving average of the parameters and *evaluate that*, not the live weights | a free fraction of a point on many benchmarks. Diffusion papers use it almost universally (DDPM: decay 0.9999); policy papers vary and often only the **code** reveals it — Diffusion Policy uses it in its configs without mentioning it in the paper. Distinct from the EMA *teacher* of [[01-canonical-papers/notes/2-computer-vision/dino\|DINO]], which is a target network, not an evaluation trick |
| **Initialization** | Xavier/He scaling keeps activation variance stable across depth | rarely load-bearing now that normalization layers exist, but named when a paper trains without them |

> [!warning] Recipe differences masquerading as method differences
> The most common unfair comparison in this literature is a new method trained with a modern
> recipe against a baseline reproduced with the original one. **Check that the baseline's
> schedule, optimizer, precision and epoch budget match the proposed method's** before
> believing a margin — and note that when they do match, the honest papers say so explicitly.

### Self-check

1. A model picks its best checkpoint by test accuracy. What went wrong, and in which
   direction is the reported number biased?
2. Precision 0.9 / recall 0.3 crack detector: what does it miss, and when is that
   acceptable on a construction site?
3. Why is FID computed on *features* (Inception embeddings) instead of pixels?
4. In a VLA paper, "76% success on unseen instructions" — list three questions you'd ask
   before believing it matters.

> [!tip]- Answers
> 1. The test set was used as a validation set — the reported number is biased upward (optimistic); true generalization is lower.
> 2. It misses 70% of real cracks (recall 0.3). Acceptable as a first-pass screen where false positives are costly and a detailed inspection follows; unacceptable if this detector alone drives safety decisions.
> 3. Pixel distance ignores perceptual quality (a one-pixel shift is punished heavily) — Inception feature space reflects semantic similarity, so distribution distance is measured there.
> 4. ① How many trials, with what variance? ② What does "unseen" mean (new objects? new instructions? new scenes?) ③ Against which baseline, and is there failure analysis?

### From reading experiments to designing them

Continue with [[06-research-practice/index|Research Practice]] for research questions, controlled robot experiments, failure diagnosis, reproducibility, and peer review.

## 한국어

*1~8번은 방법을 읽는 도구였다. 이 페이지는 그 방법이 통했다는 주장을 읽는 도구다.
그다음 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 동역학]]이 매니퓰레이션에 필요한 물리로 트랙을 닫는다.*

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

<svg viewBox="0 0 470 216" style="max-width:100%;height:auto" role="img" aria-label="과적합을 보여주는 학습·검증 손실 곡선">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="50" y1="22" x2="50" y2="140"/><line x1="50" y1="140" x2="415" y2="140"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.55" stroke-dasharray="3 3"><line x1="220" y1="22" x2="220" y2="140"/></g>
  <path d="M50,36 C120,80 180,106 260,120 C320,128 375,132 410,133" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <path d="M50,34 C120,76 180,100 220,104 C285,110 345,86 410,58" fill="none" stroke="currentColor" stroke-width="1.9" stroke-dasharray="6 4"/>
  <g stroke="currentColor" stroke-width="1.9"><line x1="50" y1="164" x2="80" y2="164" stroke-dasharray="6 4"/><line x1="50" y1="182" x2="80" y2="182"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="14" y="30">손실</text>
    <text x="220" y="16" text-anchor="middle">조기 종료</text>
    <text x="378" y="156">에폭 &#8594;</text>
    <text x="88" y="168">검증 손실 &#8212; 다시 올라간다</text>
    <text x="88" y="186">학습 손실 &#8212; 계속 내려간다</text>
    <text x="50" y="208" opacity="0.85">점선의 오른쪽에서 모델은 일반화가 아니라 암기를 하고 있다</text>
  </g>
</svg>


- "정규화"라 불리는 방법들은 *해로운 과적합을 줄인다*는 넓은 목표를 공유하지만, 작동
  기제는 서로 다르다: weight decay(가우시안 사전 — [[02-foundations/probability|3. 확률 §4]]),
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
| 언어모델 | perplexity | $e^{\text{교차 엔트로피}}$ ([[02-foundations/information-theory\|5. 정보이론 §2]]) |
| 번역/캡셔닝 | BLEU | 참조문과의 n-gram 겹침 |
| 로보틱스 | **success rate** | 목표 달성 시행 비율 — 숫자보다 *어떤* 시행(seen/unseen)인지가 더 중요 |
| 검색 | recall@k | 정답이 상위 k개 안 |

**계산 예제 — 불균형 데이터에서 정확도가 거짓말하는 이유.** 벽체 패널 1,000장에 균열
감지기를 돌렸고, 실제 균열은 60장에 있다. 감지기는 50장을 플래그했고 그중 40장이 진짜였다.
네 숫자를 늘어놓으면:

| | 균열로 예측 | 정상으로 예측 |
|---|---|---|
| **실제 균열** | TP = 40 | FN = 20 |
| **실제 정상** | FP = 10 | TN = 930 |

- **정확도(accuracy)** $= \frac{TP+TN}{1000} = \frac{970}{1000} = 97.0\%$ — 그런데 무조건
  "정상"이라고만 답하는 감지기도 $94.0\%$가 나온다. 여기서 정확도는 거의 무용하다.
- **정밀도(precision)** $= \frac{TP}{TP+FP} = \frac{40}{50} = 0.80$ — 플래그한 것 중 80%가
  진짜였다. 점검자가 신경 쓰는 숫자다: 출동이 얼마나 헛되는가.
- **재현율(recall)** $= \frac{TP}{TP+FN} = \frac{40}{60} = 0.67$ — 실제 균열 중 3분의 2를
  잡았다. **균열 20개를 놓쳤고**, 이것이 안전 담당자가 신경 쓰는 숫자다.
- **F1** $= \frac{2PR}{P+R} = \frac{2(0.8)(0.667)}{1.467} = 0.727$ — 조화평균이라 *둘 중
  하나만* 낮아도 낮게 유지된다(산술평균이었다면 0.9와 0.5처럼 한쪽으로 쏠린 경우도 0.7로
  가려줬을 것이다).

모든 Results 표에 들고 갈 교훈: 정밀도와 재현율은 문턱값 하나로 서로 맞바꾸는 값이므로,
유리한 쪽만 보고한 논문은 문장의 절반만 말한 것이다. 그리고 건설에서는 이 비대칭이 실제다 —
오경보는 점검 한 번을 낭비하지만, 놓친 균열은 구조물을 대가로 할 수 있다.

- 지표는 적대적으로 읽어라: *어떤* 분포에서, *몇 번의* 시행으로, *분산은* 얼마인 success
  rate인가? 10회 중 9회 성공은 신뢰구간이 넓다 — "90%"만이 아니라 횟수와 불확실성을
  함께 봐야 한다.

### 4. 실험의 문법

- **베이스라인**: 이겨야 하는 대상(그리고 *튜닝된* 것이어야 한다 — 약한 베이스라인은 이
  분야의 고질병). **절제 실험**(ablation): 구성 요소 하나를 빼서 그것이 중요했음을 보이기
  — 방법과 결과를 잇는 증거. **SOTA**: 최고 성능; 인상적이지만 취약하다 — 벤치마크
  특정적이고 연산량과 교락되기 일쑤.
- 읽을 때의 공정 비교 체크리스트: 같은 데이터? 같은 연산/파라미터? 같은 평가 프로토콜?
  튜닝된 베이스라인? 표가 이에 답하지 않으면 그 숫자는 장식이다.
- 시드와 분산: 딥러닝 결과는 랜덤 시드에 따라 흔들린다; 진지한 보고는 실행 횟수와 실험에
  맞는 불확실성 지표(표준편차·표준오차·신뢰구간·짝지은 검정)를 명시한다 — 로보틱스
  논문은 여러 *롤아웃과 장면*에 걸쳐 보고한다. **지금 보는 것이 어느 쪽인지 알아야 한다**:
  표준편차 $\sigma$는 *개별 실행*이 얼마나 흩어지는지를 말하고 실행을 늘려도 줄지 않는다.
  표준오차 $\sigma/\sqrt{n}$은 *평균*이 얼마나 단단히 고정됐는지를 말하고 줄어든다.
  $n = 4$면 둘이 2배 차이이므로, 작은 쪽을 그린 논문은 공짜로 더 좁은 오차 막대를 얻는다 —
  두 논문의 막대를 비교하기 전에 캡션을 확인하라.

### 5. 논문에서 경계할 평가 함정

- **체리피킹**: 정성적 그림은 최고 실행을 보여준다 — *중앙값* 롤아웃은 어떤지 물어라.
- **통계적 vs 실질적 유의성**: 오차 막대 겹침만으로 유의성을 판정할 수 없다 — 막대가 무엇인지(표준편차? 표준오차? 신뢰구간?), 실행 횟수, 짝지음 여부를 확인하라. +0.3%p는 노이즈일 수도, (포화된 벤치마크에서는) 의미 있을 수도 있다; 시드 하나의 +5%p는 운일 수 있다. 분산부터 확인하라.
- **오라클 정보**: 배포 환경에는 없을 실측 상태, 완벽한 캘리브레이션, 사람의 리셋을 조용히 쓰고 있지 않은가?
- **개루프 vs 폐루프 평가**: 오프라인에서 좋은 궤적을 예측하는 것(개루프)은 피드백과 복합 오차 아래에서 실행하는 것(폐루프)보다 훨씬 쉽다 — 로보틱스 수치는 같은 체제 안에서만 비교 가능하다.
- **에피소드 정의**: "성공률"은 시간 제한, 리셋 조건, 성공의 정의에 의존한다 — 두 논문의 80%는 다른 것을 의미할 수 있다.
- **벤치마크 포화**: 천장 근처의 벤치마크는 그 벤치마크의 버릇에 과적합하는 것을 보상한다 — 거기서의 이득이 가장 일반화되지 않는다.

### 6. 학습 레시피, 어휘로서

실험 절은 모델을 어떻게 학습시켰는지에 한 문단을 쓰는데, 그 용어들을 이 위키의 최적화
페이지는 다루지 않는다. 우리가 그 실행을 재현하는 것은 아니다 — 그러나 이것들이 보고된
숫자가 *방법*의 성질인지 *레시피*의 성질인지를 가르고, 이 중 하나를 바꾼 절제 실험은 자기가
주장하는 것을 비교하고 있지 않다.

| 용어 | 무엇인가 | 왜 주장에 등장하는가 |
|---|---|---|
| **학습률 스케줄** | 학습 도중 스텝 크기가 변한다 — 처음 몇 % 스텝의 선형 **warmup**, 그다음 0을 향한 **cosine decay** | post-norm Transformer는 warmup 없이는 아예 학습되지 않는다. 마지막 학습률이 정확도 끝자리 몇 점을 좌우하므로 "같은 구조, 다른 스케줄"은 공정한 비교가 아니다 |
| **Weight decay / AdamW** | 0을 향한 L2 당김. AdamW는 그것을 그래디언트에 접어 넣지 않고 적응 스텝과 *분리해서* 적용한다 | [[02-foundations/probability\|3. 확률 §4]]의 가우시안 사전 해석은 평범한 Adam 판본이다. 논문이 실제로 쓰는 것은 AdamW다 |
| **그래디언트 누적** | 하드웨어가 담을 수 없는 배치를 흉내 내려고 여러 번의 순전파 그래디언트를 더한 뒤 한 번 스텝 | 논문의 "배치 크기 4096"이 8 × 512일 수 있다. 방법이 배치에 민감할 때 중요하다 — 특히 대조 손실([[01-canonical-papers/notes/3-vlm/clip\|CLIP]]과 SigLIP) |
| **혼합 정밀도**(fp16/bf16) | 16비트로 계산하되 가중치의 fp32 마스터 사본을 둔다. **fp16은 손실 스케일링이 추가로 필요하고, bf16은 필요 없다** | 메모리를 대략 절반으로 줄이고 처리량을 올린다. bf16은 가수를 fp32의 지수 범위와 맞바꾼 것이고, 그래서 손실 스케일링을 버릴 수 있으며 큰 모델이 16비트에서 안정적으로 학습된다 |
| **가중치 EMA** | 파라미터의 느리게 움직이는 평균을 유지하고, 살아 있는 가중치가 아니라 *그것을* 평가한다 | 여러 벤치마크에서 공짜로 얻는 소수점 몇 자리. 확산 모델은 거의 예외 없이 쓰고(DDPM: 감쇠 0.9999), 정책 논문은 제각각이라 **코드**에서야 드러나는 일이 많다 — Diffusion Policy는 논문에 쓰지 않은 채 설정 파일에서 쓴다. [[01-canonical-papers/notes/2-computer-vision/dino\|DINO]]의 EMA *교사*와는 다르다 — 그쪽은 타깃 네트워크이지 평가 요령이 아니다 |
| **초기화** | Xavier/He 스케일링이 깊이에 걸쳐 활성 분산을 안정시킨다 | 정규화 층이 있는 지금은 결정적인 경우가 드물지만, 정규화 없이 학습하는 논문은 이것을 명시한다 |

> [!warning] 방법 차이로 위장한 레시피 차이
> 이 문헌에서 가장 흔한 불공정 비교는, 새 방법은 현대적 레시피로 학습시키고 베이스라인은
> 원래 레시피로 재현하는 것이다. 격차를 믿기 전에 **베이스라인의 스케줄·옵티마이저·정밀도·
> 에폭 예산이 제안 방법과 일치하는지 확인하라** — 그리고 일치할 때는 정직한 논문들이 그렇다고
> 명시한다는 점도 함께 기억하라.

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

### 실험을 읽는 것에서 설계하는 것으로

연구 질문·통제된 로봇 실험·실패 진단·재현성·peer review는 [[06-research-practice/index|Research Practice]]로 이어진다.
