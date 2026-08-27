---
title: 20. Video Representation & Action Understanding
tags: [robotics, perception, video, human]
study-depth: Working
depth-goal: "Read video-understanding papers without confusing recognition, localization, and anticipation; judge whether a reported number reflects temporal reasoning or scene bias."
mastery-when: "Raise to Mastery when a video backbone or anticipation formulation carries a thesis contribution."
---

## English

*The entrance to group J. Stands on [[02-foundations/linear-algebra|linear algebra]], probability and [[02-foundations/neural-network-basics|0.7]].
The questions a single frame cannot answer — what is happening, and what happens next.*

A single image answers *what is here*. Video is required to answer *what is happening* and *what happens next*. The second question is the one human-centered robotics actually needs, and it is the one most video benchmarks measure badly.

> [!info] Depth target
> Distinguish recognition, temporal localization, spatiotemporal detection, and anticipation; explain why a video model may need no temporal reasoning to score well; interpret backbone choices (two-stream, 3D CNN, video transformer) and the cost they impose; and read an evaluation critically enough to know whether the claimed capability was tested.

> [!note] Prerequisites
> [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/probability|Probability]] · [[02-foundations/neural-network-basics|Neural Network Basics]] · [[01-canonical-papers/notes/1-foundations/vit|ViT]] · [[01-canonical-papers/notes/2-computer-vision/video-understanding|Video Understanding (paper note)]]

> [!note] First pass · 처음이라면
> Read §1 — four tasks that get mixed up routinely — then §2 on scene bias, then §5's worked example of one number hiding a result. §3 and §6 are backbone and long-form detail for when a specific paper needs them.

### 1. Four tasks that are routinely conflated

| Task | Input | Output | Typical metric |
|---|---|---|---|
| Action recognition | trimmed clip | one label for the clip | top-1 / top-5 accuracy |
| Temporal action localization | untrimmed video | (start, end, label) segments | mAP at temporal IoU |
| Spatiotemporal detection | untrimmed video | per-frame boxes + action label | frame-mAP |
| **Action anticipation** | video up to $t$, **nothing after** | label of the action starting at $t+\tau$ | top-$k$ accuracy at anticipation time $\tau$ |

Anticipation is the only one of these that is causally constrained: the model may not see the moment it is predicting. Every claim about "predicting intent" belongs in this row, and a paper that reports recognition numbers has not demonstrated anticipation.

### 2. The scene-bias problem

Let $y$ be the action label and $x_1$ a single frame. Many datasets satisfy

$$I(y; x_1) \approx I(y; x_{1:T})$$

that is, one frame carries nearly all the label information. A kitchen frame implies *cooking*; a pool implies *swimming*. A model can therefore reach high accuracy with **no temporal reasoning at all**.

The standard diagnostic is to compare against a single-frame baseline, and to test on datasets built to break the shortcut — for example Something-Something, whose classes are defined by *how* an object moves ("pushing something from left to right" versus right to left) so that appearance alone is uninformative.

> [!warning] Reading rule
> If a video paper does not report a single-frame or shuffled-frame baseline, its temporal claim is unverified.

### 3. Backbone families

```mermaid
flowchart LR
    A["Two-stream<br/>RGB + optical flow"] --> B["3D CNN<br/>C3D, I3D"]
    B --> C["Factorized 3D<br/>SlowFast, (2+1)D"]
    C --> D["Video transformer<br/>TimeSformer, ViViT"]
    D --> E["Masked video pretraining<br/>VideoMAE"]
```

| Family | Idea | Cost | Weakness |
|---|---|---|---|
| Two-stream | appearance stream + precomputed optical flow stream | flow computation dominates | flow is expensive and brittle at low texture |
| 3D CNN (I3D) | inflate 2D kernels to 3D, pretrain on a large clip dataset | $O(T)$ memory over frames | fixed short temporal window |
| SlowFast | slow high-capacity pathway for semantics + fast low-capacity pathway for motion | cheaper than uniform 3D | two-pathway design is hand-set |
| Video transformer | attention over space-time tokens; often factorized into spatial then temporal | attention is $O(N^2)$ in tokens | data-hungry; long video is still hard |
| Masked video pretraining | reconstruct masked spacetime patches, then fine-tune | large pretraining cost, cheap fine-tune | pretraining data distribution leaks into results |

The practical consequence for a robotics application is temporal receptive field. Most of these models reason over **2–10 seconds**. Behaviour that unfolds over a minute — approach, hesitation, decision — is not inside the window, and a longer window is not free.

### 4. Anticipation, formally

Let observations run to time $t$ and let the anticipation horizon be $\tau$. The model estimates

$$p\big(y_{t+\tau} \mid x_{1:t}\big)$$

Three properties follow that recognition does not have:

1. **The target is uncertain, not merely unknown.** Multiple futures are legitimately possible from the same past. A model forced to output a single label is being scored on a task that has no single answer.
2. **Accuracy decreases with $\tau$.** Any anticipation result must be reported as a curve over $\tau$, not one number.
3. **Earlier is worth more, and worth less.** A warning at $\tau=2\,\mathrm{s}$ is actionable and unreliable; at $\tau=0.2\,\mathrm{s}$ it is reliable and useless. This trade-off is the actual research object.

### 5. Worked example: why one number hides the result

Two anticipation models are reported at $\tau = 1\,\mathrm{s}$:

| Model | Acc @ $\tau=0.5$ | Acc @ $\tau=1.0$ | Acc @ $\tau=2.0$ |
|---|---|---|---|
| A | 0.86 | **0.71** | 0.42 |
| B | 0.74 | **0.70** | 0.63 |

Reported at $\tau = 1\,\mathrm{s}$ alone, A "wins" by one point. But B degrades far more slowly, and for any system that must act on the prediction, the useful operating point is the largest $\tau$ that still clears a decision threshold. At threshold 0.6, A is usable to about $\tau \approx 1.3\,\mathrm{s}$ and B to about $\tau \approx 2.1\,\mathrm{s}$. B is the better model for deployment and the worse model in the table.

### 6. Long-form video

Beyond roughly a minute, dense attention over frames becomes infeasible and the interesting structure is no longer motion but **event order and reference**: what happened earlier that explains what is happening now. Approaches compress into memory, retrieve relevant moments, or operate on captions rather than pixels. Treat any claim of "long video understanding" as a claim about *what was retained*, and check that.

### 7. What this gives the intent pipeline

Video understanding supplies the temporal representation that everything downstream consumes:

- [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]] extracts the human-specific channel from that representation.
- [[04-robotics/egocentric-perception|22. Egocentric & First-Person Perception]] changes the viewpoint and therefore what is observable.
- [[04-robotics/human-intent-prediction|23. Human Intent & Trajectory Prediction]] is anticipation with a decision attached.

### 8. Reading claims and evaluations

| Paper phrase | Check before accepting it |
|---|---|
| state-of-the-art on action recognition | single-frame baseline; is the dataset scene-biased |
| understands temporal dynamics | shuffled-frame or reversed-clip ablation |
| anticipates actions | does the input window strictly exclude $t+\tau$; is a $\tau$ curve given |
| real-time | frames per second at what resolution, on what hardware, including preprocessing (optical flow is not free) |
| long-form | what is the actual temporal span; what is discarded to fit memory |
| generalizes | evaluated across recording setups, or only across held-out clips of the same setup |

### After reading

You should be able to:

- separate recognition, localization, detection, and anticipation, and say which one a paper actually evaluated;
- explain scene bias and name the ablation that exposes it;
- state the temporal receptive field of a backbone family and why it matters for a minute-long behaviour;
- write the anticipation objective and explain why one accuracy number is insufficient;
- identify preprocessing cost hidden inside a "real-time" claim.

> [!tip] Going deeper · 더 깊이
> No textbook; the backbone lineage in §3 is the reading list, in order. Carreira & Zisserman (CVPR 2017) for inflating 2D filters into 3D and for Kinetics as the pretraining corpus that reorganized everything after it. SlowFast (ICCV 2019) for the two-pathway answer to temporal resolution. TimeSformer (ICML 2021) for the attention formulation. VideoMAE for self-supervised pretraining. Read them for what each one had to give up, not for their headline accuracies — the scene-bias problem in §2 is why those accuracies are hard to compare across the four.

### Self-check

1. A model reports 92% on an action dataset. What single experiment most efficiently tests whether it uses temporal information?
2. Why is anticipation not simply recognition applied to a shifted window?
3. A construction-site behaviour of interest takes 45 seconds. Which backbone families are structurally unable to model it end-to-end, and what is the usual workaround?
4. Give an operating condition under which a lower-accuracy anticipation model is the correct choice.

> [!tip]- Answers
> 1. Retrain or evaluate a single-frame baseline on the same split; if it is close, the dataset is scene-biased. Frame shuffling is a cheaper approximation. 2. Because the label window is excluded from the input, so the mapping is one-to-many over legitimate futures; the model estimates a distribution, not a deterministic label. 3. Fixed-window 3D CNNs and standard video transformers (2–10 s receptive field); the workaround is hierarchical or memory-based aggregation over clip-level features. 4. When the decision requires a longer horizon than the higher-accuracy model can sustain above the action threshold — see §5.

### Sources

**Backbones — verified citations**

- J. Carreira and A. Zisserman, "Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset," *CVPR 2017*, pp. 4724–4733. [arXiv:1705.07750](https://arxiv.org/abs/1705.07750) — inflates 2D ImageNet filters into 3D (I3D) and introduces Kinetics-400 as the pretraining corpus. Note the title does not contain "I3D".
- C. Feichtenhofer, H. Fan, J. Malik, and K. He, "SlowFast Networks for Video Recognition," *ICCV 2019*, pp. 6202–6211. [arXiv:1812.03982](https://arxiv.org/abs/1812.03982) — a slow spatial pathway and a fast, low-capacity temporal pathway with lateral fusion.
- G. Bertasius, H. Wang, and L. Torresani, "Is Space-Time Attention All You Need for Video Understanding?", *ICML 2021*. [arXiv:2102.05095](https://arxiv.org/abs/2102.05095) — the paper the community calls TimeSformer; "divided space-time attention" is the winning variant. The name appears nowhere in the title.
- Z. Tong, Y. Song, J. Wang, and L. Wang, "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training," *NeurIPS 2022*. [arXiv:2203.12602](https://arxiv.org/abs/2203.12602) — tube masking at 90–95% works on 3k–4k-video datasets with no extra data.
- L. Wang, B. Huang, Z. Zhao, et al., "VideoMAE V2: Scaling Video Masked Autoencoders with Dual Masking," *CVPR 2023*. [arXiv:2303.16727](https://arxiv.org/abs/2303.16727) — a scaling paper, not a new objective: dual masking makes billion-parameter video ViTs trainable.

**Benchmarks**

- R. Goyal, S. Ebrahimi Kahou, V. Michalski, et al., "The 'something something' video database for learning and evaluating visual common sense," *ICCV 2017*. [arXiv:1706.04261](https://arxiv.org/abs/1706.04261) — over 100,000 videos across 174 caption-template classes.

> [!warning] Cite this dataset for what it claims
> The paper's own framing is **physical common sense**, not "temporal reasoning": it argues that
> networks lack common-sense knowledge about the physical world and that most labelled video
> datasets encode high-level concepts rather than the physical detail of actions. The
> temporal-reasoning reading is a downstream community characterisation — accurate in effect,
> since the caption-template classes make appearance cues insufficient, but not the authors'
> words. Cite "visual common sense" if you are quoting the paper.

## 한국어

*J군의 입구다. [[02-foundations/linear-algebra|선형대수]]·확률과 [[02-foundations/neural-network-basics|0.7]] 위에 선다.
한 장의 이미지로는 답할 수 없는 질문들 — 무슨 일이 일어나는가, 그리고 다음에 무엇이 일어나는가.*

한 장의 이미지는 *무엇이 있는가*에 답한다. *무슨 일이 일어나는가*와 *다음에 무엇이 일어나는가*는 비디오가 있어야 답할 수 있다. 인간 중심 로보틱스가 실제로 필요로 하는 건 두 번째 질문이고, 대부분의 비디오 벤치마크가 제대로 측정하지 못하는 것도 그것이다.

> [!info] 깊이 목표
> 인식·시간적 위치추정·시공간 검출·예측(anticipation)을 구분한다; 비디오 모델이 시간 추론
> 없이도 높은 점수를 낼 수 있는 이유를 설명한다; 백본 선택(two-stream, 3D CNN, 비디오 트랜스포머)과
> 그 비용을 해석한다; 주장한 능력이 실제로 검증됐는지 판단할 만큼 평가를 비판적으로 읽는다.

> [!note] 선수 지식
> [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/probability|확률]] · [[02-foundations/neural-network-basics|신경망 기초]] · [[01-canonical-papers/notes/1-foundations/vit|ViT]] · [[01-canonical-papers/notes/2-computer-vision/video-understanding|Video Understanding (논문 노트)]]

> [!note] 처음이라면 · First pass
> 먼저 §1 — 습관적으로 뒤섞이는 네 과제 — 그다음 장면 편향인 §2, 그다음 숫자 하나가 결과를 가리는 §5의 예제. §3·§6은 백본과 롱폼 세부이니 특정 논문이 요구할 때 보라.

### 1. 습관적으로 뒤섞이는 네 가지 과제

| 과제 | 입력 | 출력 | 대표 지표 |
|---|---|---|---|
| 행동 인식 | 잘린 클립 | 클립 하나의 레이블 | top-1 / top-5 정확도 |
| 시간적 행동 위치추정 | 안 자른 영상 | (시작, 끝, 레이블) 구간 | 시간 IoU 기준 mAP |
| 시공간 검출 | 안 자른 영상 | 프레임별 박스 + 행동 레이블 | frame-mAP |
| **행동 예측(anticipation)** | $t$까지의 영상, **이후는 없음** | $t+\tau$에 시작될 행동 | 예측 시점 $\tau$에서의 top-$k$ |

이 중 인과적으로 제약된 것은 anticipation뿐이다 — 모델은 자기가 예측하는 순간을 볼 수 없다. "의도를 예측한다"는 모든 주장은 이 행에 속하고, 인식 수치를 보고한 논문은 예측을 입증한 것이 아니다.

### 2. 장면 편향(scene bias) 문제

레이블을 $y$, 한 프레임을 $x_1$이라 하면 많은 데이터셋이

$$I(y; x_1) \approx I(y; x_{1:T})$$

를 만족한다 — 즉 한 프레임이 레이블 정보의 거의 전부를 담는다. 주방 프레임은 *요리*를, 수영장은 *수영*을 함의한다. 그래서 모델은 **시간 추론을 전혀 하지 않고도** 높은 정확도에 도달할 수 있다.

표준 진단은 단일 프레임 베이스라인과의 비교, 그리고 이 지름길을 막도록 설계된 데이터셋에서의 평가다 — 예를 들어 Something-Something은 클래스를 물체가 *어떻게* 움직이는지로 정의해서("왼쪽에서 오른쪽으로 밀기" vs 반대) 외형만으로는 판별이 안 되게 만들었다.

> [!warning] 읽기 규칙
> 비디오 논문이 단일 프레임 또는 프레임 셔플 베이스라인을 보고하지 않으면, 그 시간적 주장은 검증되지 않은 것이다.

### 3. 백본 계보

```mermaid
flowchart LR
    A["Two-stream<br/>RGB + optical flow"] --> B["3D CNN<br/>C3D, I3D"]
    B --> C["분해된 3D<br/>SlowFast, (2+1)D"]
    C --> D["비디오 트랜스포머<br/>TimeSformer, ViViT"]
    D --> E["마스킹 사전학습<br/>VideoMAE"]
```

| 계열 | 아이디어 | 비용 | 약점 |
|---|---|---|---|
| Two-stream | 외형 스트림 + 미리 계산한 optical flow 스트림 | flow 계산이 지배적 | flow가 비싸고 저텍스처에서 불안정 |
| 3D CNN (I3D) | 2D 커널을 3D로 팽창, 대규모 클립 데이터로 사전학습 | 프레임 수에 $O(T)$ 메모리 | 고정된 짧은 시간 창 |
| SlowFast | 의미용 느린 고용량 경로 + 움직임용 빠른 저용량 경로 | 균일 3D보다 저렴 | 두 경로 설계가 수작업 |
| 비디오 트랜스포머 | 시공간 토큰에 대한 어텐션, 보통 공간→시간으로 분해 | 토큰 수에 $O(N^2)$ | 데이터 요구량 큼, 긴 영상은 여전히 난제 |
| 마스킹 사전학습 | 마스킹된 시공간 패치 복원 후 미세조정 | 사전학습 비용 큼, 미세조정은 저렴 | 사전학습 데이터 분포가 결과에 스며듦 |

로보틱스 응용에서 실질적 귀결은 **시간 수용 영역**이다. 위 모델 대부분이 **2–10초**를 추론한다. 접근–망설임–결정처럼 1분에 걸쳐 펼쳐지는 행동은 그 창 안에 없고, 창을 늘리는 건 공짜가 아니다.

### 4. Anticipation의 정식화

관측이 $t$까지 있고 예측 지평이 $\tau$일 때 모델은

$$p\big(y_{t+\tau} \mid x_{1:t}\big)$$

를 추정한다. 인식에는 없는 성질 세 가지가 따라온다:

1. **목표가 단지 미지가 아니라 불확실하다.** 같은 과거에서 여러 미래가 정당하게 가능하다. 레이블 하나를 강제로 출력하는 모델은 정답이 하나가 아닌 과제로 채점되고 있는 것이다.
2. **$\tau$가 커지면 정확도가 떨어진다.** 모든 anticipation 결과는 숫자 하나가 아니라 $\tau$에 대한 곡선으로 보고돼야 한다.
3. **이를수록 값지고, 동시에 값싸다.** $\tau=2\,\mathrm{s}$의 경고는 조치 가능하지만 부정확하고, $\tau=0.2\,\mathrm{s}$는 정확하지만 쓸모없다. **이 트레이드오프 자체가 연구 대상이다.**

### 5. 예제: 숫자 하나가 결과를 가리는 방식

두 예측 모델을 $\tau = 1\,\mathrm{s}$에서 보고했다:

| 모델 | $\tau=0.5$ | $\tau=1.0$ | $\tau=2.0$ |
|---|---|---|---|
| A | 0.86 | **0.71** | 0.42 |
| B | 0.74 | **0.70** | 0.63 |

$\tau=1\,\mathrm{s}$만 보면 A가 1점 이긴다. 그러나 B는 훨씬 천천히 나빠지고, 예측을 근거로 **행동해야 하는** 시스템에서 유용한 동작점은 결정 임계값을 넘기는 가장 큰 $\tau$다. 임계값 0.6에서 A는 $\tau \approx 1.3\,\mathrm{s}$까지, B는 $\tau \approx 2.1\,\mathrm{s}$까지 쓸 수 있다. **B가 배포에 더 나은 모델이고 표에서는 더 나쁜 모델이다.**

### 6. 롱폼 비디오

대략 1분을 넘어서면 프레임 전체에 대한 밀집 어텐션이 불가능해지고, 흥미로운 구조는 더 이상 움직임이 아니라 **사건의 순서와 참조**가 된다 — 지금 벌어지는 일을 설명하는 앞선 사건이 무엇인가. 접근법은 메모리로 압축하거나, 관련 순간을 검색하거나, 픽셀 대신 캡션 위에서 작동한다. "롱폼 이해" 주장은 **무엇을 남겼는가**에 대한 주장으로 취급하고 그것을 확인하라.

### 7. 의도 파이프라인에 주는 것

비디오 이해는 하위 전부가 소비하는 시간 표현을 공급한다:

- [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]]이 그 표현에서 사람 채널을 뽑는다.
- [[04-robotics/egocentric-perception|22. 자기중심·1인칭 인지]]는 시점을 바꿔 관측 가능한 것 자체를 바꾼다.
- [[04-robotics/human-intent-prediction|23. 인간 의도·궤적 예측]]은 결정이 붙은 anticipation이다.

### 8. 주장과 평가 읽기

| 논문 문구 | 받아들이기 전에 확인할 것 |
|---|---|
| action recognition SOTA | 단일 프레임 베이스라인; 데이터셋이 장면 편향인가 |
| 시간 동역학을 이해한다 | 프레임 셔플·역재생 ablation |
| 행동을 예측한다 | 입력 창이 $t+\tau$를 엄격히 배제하는가; $\tau$ 곡선이 있는가 |
| real-time | 어떤 해상도·하드웨어에서 몇 fps인가, 전처리 포함인가 (optical flow는 공짜가 아니다) |
| long-form | 실제 시간 범위가 얼마인가; 메모리를 맞추려 무엇을 버렸는가 |
| 일반화된다 | 촬영 설정을 가로질러 평가했는가, 같은 설정의 held-out 클립뿐인가 |

### 읽고 나면 말할 수 있어야 하는 것

다음을 할 수 있어야 한다:

- 인식·위치추정·검출·예측을 구분하고 논문이 실제로 평가한 것이 무엇인지 말한다;
- 장면 편향을 설명하고 그것을 드러내는 ablation을 지목한다;
- 백본 계열의 시간 수용 영역을 말하고 1분짜리 행동에 왜 문제인지 설명한다;
- anticipation 목적함수를 쓰고 정확도 하나로 부족한 이유를 설명한다;
- "real-time" 주장 안에 숨은 전처리 비용을 찾아낸다.

> [!tip] 더 깊이 · Going deeper
> 교과서는 없고, §3의 백본 계보가 곧 읽기 목록이며 순서대로다. Carreira & Zisserman(CVPR 2017)은 2D 필터를 3D로 부풀리는 것과, 이후 전부를 재편한 사전학습 말뭉치로서의 Kinetics를 위해. SlowFast(ICCV 2019)는 시간 해상도에 대한 두 경로 해답을 위해. TimeSformer(ICML 2021)는 어텐션 정식화를 위해. VideoMAE는 자기지도 사전학습을 위해. 표제 정확도가 아니라 *각각이 무엇을 포기해야 했는지*를 보며 읽어라 — §2의 장면 편향 문제가 바로 그 정확도들을 넷 사이에서 비교하기 어렵게 만드는 이유다.

### 스스로 점검

1. 어떤 모델이 행동 데이터셋에서 92%를 보고했다. 시간 정보를 쓰는지 가장 효율적으로 검증하는 실험 하나는?
2. anticipation이 창을 옮긴 인식이 아닌 이유는?
3. 관심 있는 현장 행동이 45초 걸린다. 어떤 백본 계열이 구조적으로 end-to-end 모델링이 불가능하고, 통상적 우회는?
4. 정확도가 낮은 예측 모델이 올바른 선택이 되는 운용 조건 하나를 들라.

> [!tip]- 정답
> 1. 같은 split에서 단일 프레임 베이스라인을 평가한다; 근접하면 장면 편향이다. 프레임 셔플이 더 싼 근사다. 2. 레이블 구간이 입력에서 배제되므로 정당한 여러 미래에 대해 일대다 사상이 된다; 모델은 결정적 레이블이 아니라 분포를 추정한다. 3. 고정 창 3D CNN과 표준 비디오 트랜스포머(2–10초 수용 영역); 우회는 클립 단위 특징 위의 계층적·메모리 기반 집계다. 4. 결정에 필요한 지평이, 정확도 높은 모델이 임계값 위에서 유지할 수 있는 $\tau$보다 길 때 — §5 참조.

### 출처

**백본 — 검증된 인용**

- J. Carreira and A. Zisserman, "Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset," *CVPR 2017*, pp. 4724–4733. [arXiv:1705.07750](https://arxiv.org/abs/1705.07750) — 2D ImageNet 필터를 3D로 부풀려(inflate) I3D를 만들고, 사전학습 코퍼스로 Kinetics-400을 함께 낸다. 제목에 "I3D"는 없다.
- C. Feichtenhofer, H. Fan, J. Malik, and K. He, "SlowFast Networks for Video Recognition," *ICCV 2019*, pp. 6202–6211. [arXiv:1812.03982](https://arxiv.org/abs/1812.03982) — 공간 의미를 담는 느린 경로와 용량이 작고 빠른 시간 경로를 측면 융합한다.
- G. Bertasius, H. Wang, and L. Torresani, "Is Space-Time Attention All You Need for Video Understanding?", *ICML 2021*. [arXiv:2102.05095](https://arxiv.org/abs/2102.05095) — 흔히 TimeSformer로 불리는 논문. "divided space-time attention"이 가장 좋은 변형이다. 그 이름은 제목에 등장하지 않는다.
- Z. Tong, Y. Song, J. Wang, and L. Wang, "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training," *NeurIPS 2022*. [arXiv:2203.12602](https://arxiv.org/abs/2203.12602) — 90–95% 비율의 tube masking이 추가 데이터 없이 3k–4k 규모 데이터셋에서 작동한다.
- L. Wang, B. Huang, Z. Zhao, et al., "VideoMAE V2: Scaling Video Masked Autoencoders with Dual Masking," *CVPR 2023*. [arXiv:2303.16727](https://arxiv.org/abs/2303.16727) — 새로운 목적함수가 아니라 스케일링 논문이다. dual masking으로 10억 파라미터급 video ViT 학습이 가능해진다.

**벤치마크**

- R. Goyal, S. Ebrahimi Kahou, V. Michalski, et al., "The 'something something' video database for learning and evaluating visual common sense," *ICCV 2017*. [arXiv:1706.04261](https://arxiv.org/abs/1706.04261) — 174개 캡션 템플릿 클래스, 10만 개 이상의 비디오.

> [!warning] 이 데이터셋은 주장한 대로 인용하라
> 논문 자신의 표현은 "시간 추론"이 아니라 **물리적 상식**이다. 신경망이 물리 세계에 대한
> 상식적 지식을 결여하고 있고, 라벨링된 비디오 데이터셋 대부분이 행동과 장면의 물리적
> 세부가 아니라 고수준 개념을 담고 있다고 논한다. 시간 추론이라는 독법은 이후 커뮤니티가
> 붙인 성격 규정이다 — 캡션 템플릿 클래스가 외형 단서를 불충분하게 만들므로 효과 면에서는
> 맞지만, 저자들의 표현은 아니다. 논문을 인용하는 것이라면 "visual common sense"를 써라.
