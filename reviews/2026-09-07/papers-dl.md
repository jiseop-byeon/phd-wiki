# 한국어 위키 학습성 정독 감사 — Papers / Deep Learning

- 감사일: 2026-09-07
- 범위: `content/01-canonical-papers/notes/1-foundations/` 전체, `2-computer-vision/` 전체, `3-vlm/` 전체, `content/03-deep-learning/` 전체
- 완독: **43/43 Markdown, 5,277줄**. 모든 파일을 줄 번호와 함께 처음부터 끝까지 읽었다. 헤딩 스캔이나 샘플링으로 대체하지 않았다.
- 비변경 원칙: 콘텐츠는 수정하지 않았고 이 보고서만 생성했다.
- 사실 검증 범위: 원 논문 전수 fact-check는 하지 않았다. 본문 내부의 식·설명·한영 대응으로 확정 가능한 것은 `본문 확인`, 원 출처 재확인이 필요한 것은 `추가검증 필요`로 구분했다.

## 결론

이 범위는 공업수학 경험이 있지만 ML/로봇을 처음 배우는 공대생에게 **Physical AI 논문 문해력의 훌륭한 1차 뼈대**를 제공한다. 대부분의 노트가 (1) 문제, (2) 핵심 메커니즘, (3) 무엇을 측정했는지, (4) 실험 범위 밖으로 일반화하면 안 되는 지점을 짧게 분리한다. 특히 attention의 축별 shape 설명, PPO clip의 부호별 그림, LoRA 파라미터 산수, 상대 깊이/미터 깊이 및 렌더링/매핑 구분은 초보자가 논문의 주장을 과대해석하지 않도록 잘 설계돼 있다.

다만 현재 상태만으로 모든 `Working` 표기 문서를 실제 Working 수준으로 끌어올린다고 보기는 어렵다. 식의 역할을 잘못 이름 붙이는 곳(Adam), 초보에게 중의적으로 읽힐 수 있는 용어 표현(negative pair), 구조적 가능성과 일반적 사용법을 혼동하는 단정(BERT, NeRF, PaliGemma), 그리고 계보도의 인과 압축이 남아 있다. 아래 P1을 먼저 고치면 전체 트랙은 **Literacy 달성에는 충분하고, 선택 영역 Working으로 가는 발판으로도 적절**하다. Working은 노트 독해 뒤 해당 논문의 입력·출력 텐서/손실/평가 프로토콜을 한 번 재현하거나 진단하는 활동이 별도로 필요하다.

## 발견 사항

### papers-dl-001 — Adam의 2차 모멘트를 variance로 부름

- 우선순위: **P1 학습차단/사실문제**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/adam.md:35` — “step each parameter by mean/√(variance)”; `:79` — “평균/√(분산)”
- 문제: 바로 아래 식의 $v_t$는 평균을 뺀 분산이 아니라 **그래디언트 제곱의 지수이동평균(uncentered second moment/RMS scale)**이다. 초보자는 Adam이 통계적 분산을 계산한다고 오해하고, 상수 그래디언트에서도 분모가 0이어야 한다고 잘못 추론할 수 있다.
- 구체적 수정: 영어는 “mean divided by the root of the uncentered second moment (an RMS-like scale)”, 한국어는 “1차 모멘트를 그래디언트 제곱 평균의 제곱근(RMS형 스케일)으로 나눈다; 평균을 뺀 분산은 아니다”로 교체. $g_t=c$인 한 줄 예를 덧붙이면 식의 역할이 선명해진다.
- 근거 신뢰도: **본문 확인**(같은 파일 `:37`, `:81`의 정의와 직접 모순).

### papers-dl-002 — “음성 쌍”의 audio 중의성 예방

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/mae.md:79` — “음성 쌍도”; `content/01-canonical-papers/notes/2-computer-vision/dino.md:86` — “큰 배치의 음성 쌍”, `:98` — “음성 쌍도”; `content/01-canonical-papers/notes/3-vlm/clip.md:141` — aria-label의 “나머지는 전부 음성”, `:171` — “음성 N²−N개”
- 문제: “음성 쌍”은 positive/negative의 대비에서 쓰이는 통용 번역일 수 있으므로 오역이나 한영 불일치로 확정할 수 없다. 다만 ML을 처음 배우는 독자는 음성(audio) 데이터 쌍으로 읽을 수 있어, 대조학습의 positive/negative 의미를 처음 소개하는 자리에서는 중의성이 있다.
- 구체적 수정: 초회에 “음의 쌍(negative pair, 비정답/불일치 쌍)”으로 병기하고 이후 “음의 쌍”으로 통일. CLIP 그림은 공간이 허용되면 “음의 쌍(불일치) N²−N개”로 쓴다.
- 근거 신뢰도: **본문 확인**(중의성 확인); **오역 판정 철회**.

### papers-dl-003 — BERT encoder-only를 “텍스트 생성 불가”로 절대화

- 우선순위: **P1 학습차단/사실문제**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/bert.md:49` — “cannot generate text”; `:87` — “텍스트 생성 불가”; `:105` — “it cannot generate”
- 문제: BERT는 **좌→우 자기회귀 생성용으로 설계되지 않았고 직접적인 생성 인터페이스가 없다**가 정확하다. 마스크 반복 채움 등으로 문자열을 생성하는 것 자체가 논리적으로 불가능한 것은 아니다. 구조적 불가능과 표준 사용법을 섞으면 encoder/decoder와 attention mask의 역할을 잘못 배운다.
- 구체적 수정: 세 곳 모두 “not natively an autoregressive generator / 좌→우 자유 생성에 직접 맞지 않는다”로 바꾸고, “양방향 attention은 현재 위치의 정답 토큰을 그대로 둔 next-token objective와 양립하지 않는다”를 한 문장 추가.
- 근거 신뢰도: **본문 확인**(같은 파일 `:30–40`, `:68–78`의 MLM 설명으로 판별 가능).

### papers-dl-004 — Depth Anything 요약이 상대 깊이와 미터 깊이를 한 능력처럼 약속

- 우선순위: **P1 학습차단/사실문제**
- 위치·인용: `content/01-canonical-papers/notes/2-computer-vision/depth-anything.md:27` — “robust metric/relative depth for any image”; `:81` — “어떤 이미지에서든 강건한 상대/절대 깊이”
- 문제: 같은 문서 `:47–48`, `:59–60`, `:101–114`는 사전학습이 affine-invariant 상대 깊이이고 metric head는 벤치마크별 fine-tuning이며 단안 스케일 모호성이 남는다고 정확히 설명한다. 첫 요약은 이 중요한 조건을 지워 로봇 기하에 바로 쓸 수 있다는 오해를 만든다.
- 구체적 수정: “광범위한 이미지에서 강건한 **상대 깊이**를 제공하며, 미터 깊이는 대상 도메인별 head/fine-tuning과 보정이 필요하다”로 양언어 요약을 교체.
- 근거 신뢰도: **본문 확인**(동일 문서 내부의 명시적 조건과 모순).

### papers-dl-005 — NeRF의 spectral bias를 표현 불가능성으로 바꿈

- 우선순위: **P1 학습차단/사실문제**
- 위치·인용: `content/01-canonical-papers/notes/2-computer-vision/nerf.md:136` — “high frequencies cannot be represented without positional encoding · 위치 인코딩 없이는 고주파를 못 그리는 이유”
- 문제: 같은 파일 `:43–46`, `:98–99`는 좌표 MLP가 고주파를 **더 느리게 맞추는 최적화 편향**이라고 설명한다. 충분한 용량의 MLP가 고주파를 표현할 수 없다는 뜻이 아니다. 표현력과 학습 동역학을 구분하는 것은 논문 문해력의 핵심이다.
- 구체적 수정: 체크 항목을 “왜 raw-coordinate MLP가 고주파를 학습하기 어렵고, Fourier positional encoding이 최적화를 돕는지”로 교체. 본문의 “cannot otherwise”도 “otherwise learns them poorly/slowly under this setup”으로 완화.
- 근거 신뢰도: **본문 확인**.

### papers-dl-006 — PaliGemma의 prefix-LM 장점을 causal LM의 시각 접근 불가로 설명

- 우선순위: **P1 학습차단/사실문제**
- 위치·인용: `content/01-canonical-papers/notes/3-vlm/paligemma.md:39–41` — “the ‘question’ can see the whole image, unlike a purely causal LM”; `:72–74` — “순수 인과 LM과 달리 ‘질문’이 이미지 전체를 볼 수 있다”
- 문제: 이미지 토큰이 질문보다 앞에 놓이면 순수 causal LM의 질문 토큰도 이전 이미지 토큰 전체를 볼 수 있다. prefix-LM의 차이는 **이미지+프롬프트 접두부 내부를 양방향으로 섞을 수 있고, 생성 답변만 causal이라는 mask 구조**다.
- 구체적 수정: 대비 문장을 “pure causal에서는 접두부의 각 토큰이 이전 토큰만 보지만, prefix-LM에서는 이미지+프롬프트 접두부가 서로 양방향으로 상호작용한다”로 교체하고 4×4 attention-mask 미니 예를 추가.
- 근거 신뢰도: **추가검증 필요**(mask 정의를 원 논문/공식 구현에서 재확인 권장).

### papers-dl-007 — vanilla policy-gradient 배치 재사용 설명과 GAE 편향 조건을 정교화할 필요

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/ppo.md:30` — “allow exactly one gradient step per batch”; `:119` — “정확히 한 번의 그래디언트 스텝만 허용”; `:83`, `:172` — “$\lambda=1$: unbiased, high variance / 무편향, 고분산”
- 문제: `:28–30`의 주어는 PPO가 아니라 **PPO 이전의 standard/vanilla policy gradients**다. PPO 원 논문의 [공식 abstract](https://arxiv.org/abs/1707.06347)도 standard policy gradient의 샘플당 한 번 갱신과 PPO의 여러 minibatch epoch를 직접 대비한다. 따라서 PPO가 배치를 재사용한다는 설명은 맞고, 이 문장이 PPO 자체를 “한 step 알고리즘”으로 정의하는 것도 아니다. 개선점은 “정확히 한 번만 허용”을 절대 규칙처럼 읽히지 않게 하고, 저자들이 대비한 표준적 사용 문맥임을 한정하는 정도다. 별도로, $\lambda=1$의 무편향은 완전한 Monte Carlo return 또는 올바른 종단 처리 같은 조건이 있어야 하며 truncated rollout에서는 자동으로 성립하지 않는다.
- 구체적 수정: “standard policy gradient는 통상 수집 샘플당 한 번 갱신하는 반면, PPO 목적함수는 같은 배치에서 여러 minibatch epoch를 안정적으로 수행하도록 설계됐다”로 한정한다. GAE 뒤에는 “유한 rollout에서 bootstrap하거나 value가 부정확하면 $\lambda=1$도 엄밀히 무편향이라고 단정할 수 없다”를 추가하고, 한국어에도 GAE가 PPO 자체의 신규 기여가 아니라 2015 estimator라는 영어의 귀속 문장을 복원한다.
- 근거 신뢰도: **원 출처 확인**(PPO abstract의 standard PG 대 PPO 대비); GAE의 엄밀한 편향 조건은 **추가검증 필요**.

### papers-dl-008 — Faster R-CNN의 “end-to-end”가 뜻하는 범위를 한정할 필요

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/01-canonical-papers/notes/2-computer-vision/faster-r-cnn.md:25` — “making detection fully end-to-end learnable”; `:69` — “검출을 완전히 end-to-end 학습 가능하게”
- 문제: “end-to-end”는 모든 연산이 일체로 미분 가능하다는 좁은 뜻뿐 아니라, 수작업 Selective Search를 학습 RPN으로 바꾸어 proposal과 detection task를 공동 학습한다는 통용 의미로도 읽힌다. 따라서 현재 요약을 사실 오류로 단정할 수는 없다. 다만 원 논문의 alternating/approximate joint training과 NMS가 남는다는 조건을 생략하면, 뒤의 DETR “end-to-end set prediction”과 차이가 흐려질 수 있다.
- 구체적 수정: 요약은 유지 가능하되 Method에 “여기서 end-to-end는 수작업 proposal 제거와 공유 특징의 공동 학습을 뜻하며, 원 논문에는 alternating/approximate joint training 변형과 NMS가 남는다”를 추가한다.
- 근거 신뢰도: **추가검증 필요**(원 논문의 4-step alternating/approximate joint training 절 재확인 권장).

### papers-dl-009 — LoRA의 한영 on-ramp가 서로 다른 개념을 가르침

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/lora.md:22` — “does not SVD-approximate a finished update”; `:23` — “$\Delta W$를 얇은 행렬 둘의 곱으로 근사해도 된다”
- 문제: 영어는 사후 SVD 근사와 처음부터 low-rank로 parameterize하는 것을 정확히 구분하지만 한국어는 다시 “근사”로 표현한다. Working 수준에서는 이 차이가 구현·학습 파라미터 이해에 중요하다.
- 구체적 수정: 한국어를 “완성된 $\Delta W$를 사후 SVD 근사하는 것이 아니라, 처음부터 $\Delta W=BA$로 파라미터화해 $A,B$를 직접 학습한다”로 교체. `:170`의 “저계수/계수”도 “저랭크/랭크”로 통일.
- 근거 신뢰도: **본문 확인**.

### papers-dl-010 — ViT 직관이 유연성과 데이터 임계값을 보편 법칙처럼 단정

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/vit.md:36` — “strictly more flexible… above it, the learned prior wins”; `:78` — “엄격히 더 유연하다… 그 위면 학습된 사전 지식이 이긴다”
- 문제: 실험은 특정 모델·학습 레시피·데이터 규모에서의 성능 교차를 보였지, Transformer가 CNN보다 엄밀한 함수 클래스 상위집합이거나 단일 보편 임계값이 있음을 증명하지 않았다.
- 구체적 수정: “지역성·평행이동 등변성을 덜 하드코딩해 더 많은 것을 데이터에서 배울 여지가 있지만, 그 대가로 데이터와 최적화가 더 필요했다. 이 논문의 설정에서는 대규모 사전학습에서 우세했다”로 조건화.
- 근거 신뢰도: **본문 확인**(같은 파일의 `:44–45`, `:50`, `:59`가 실험 조건을 제한).

### papers-dl-011 — 계보도의 화살표 규칙과 큰 그림이 충돌

- 우선순위: **P1 학습경로 문제**
- 위치·인용: `content/03-deep-learning/lineage.md:14–16` — “solid arrows = a strong technical or architectural predecessor”; `:24` — “AlexNet → Transformer”; `:36–38` — “scale (2012) met tokenization (2017)”; 한국어 대응 `:126–127`, `:134`, `:146–148`
- 문제: 범례대로라면 AlexNet이 Transformer의 강한 직접 기술/구조 선행처럼 읽힌다. 상세 지도 `:41–56`은 실제로 CNN과 RNN 계열을 분리하고 ResNet→Transformer를 점선 영향으로 그려 더 정확하다. 또 Transformer의 핵심을 “tokenization”으로 이름 붙이면 이미 존재하던 토큰화와 attention architecture를 혼동한다.
- 구체적 수정: 큰 그림 AlexNet→Transformer를 점선 “현대 DL의 scale/compute 전제”로 바꾸거나 중간에 두 병렬 가지를 둔다. “tokenization (2017)”은 “attention-based sequence modeling / 어텐션 기반 시퀀스 모델링”으로 교체. 큰 그림은 상세 그림의 범례를 따라야 한다.
- 근거 신뢰도: **본문 확인**(같은 문서의 범례와 상세도가 직접 충돌).

### papers-dl-012 — Scaling-law의 실험 결과를 “증명”이라 부름

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/scaling-laws.md:154` — “증명: … Chinchilla 70B가 Gopher 280B를 전면적으로 이겼다”
- 문제: 이는 compute-matched 실험 증거이지 수학적 증명도, 모든 분포에서의 보편 증명도 아니다. 논문 읽기 훈련에서는 evidence와 proof의 구분이 중요하다.
- 구체적 수정: “핵심 실험 증거:”로 교체하고 “같은 연산 예산·해당 데이터/모델 계열에서”를 붙인다. 영어 `:78`의 “Proof:”도 같은 방식으로 바꾸면 양언어가 일치한다.
- 근거 신뢰도: **본문 확인**.

### papers-dl-013 — U-Net skip이 gradient가 아니라 resolution만 나른다는 양자택일

- 우선순위: **P3 선택 개선**
- 위치·인용: `content/01-canonical-papers/notes/2-computer-vision/u-net.md:20–21` — “carry resolution rather than gradient / 그래디언트가 아니라 해상도를 나른다”
- 문제: U-Net skip의 대표 목적은 고해상도 encoder feature 전달이 맞지만, 그 경로로 gradient도 흐른다. “무엇을 나른다”와 “왜 설계했는가”를 섞은 표현이다.
- 구체적 수정: “주된 설계 목적은 ResNet의 residual optimization과 달리 고해상도 localization feature를 전달하는 것이며, 물론 역전파 경로도 제공한다”로 교체.
- 근거 신뢰도: **본문 확인**.

### papers-dl-014 — InstructGPT 수학 준비물의 한영 정보 불일치

- 우선순위: **P3 선택 개선**
- 위치·인용: `content/01-canonical-papers/notes/1-foundations/instructgpt.md:20` — “reward model standing in for the environment”; `:21` — “KL 페널티는 … 정보이론 §3”
- 문제: 두 문장이 번역 대응이 아니며 영어에는 KL 선수 링크가, 한국어에는 reward-model-as-environment 연결이 빠져 있다. 양언어를 교차 읽는 초보가 서로 다른 준비물을 받는다.
- 구체적 수정: 양쪽 모두 “3단계는 reward model을 환경 보상처럼 쓰는 PPO이며, KL penalty 해석은 정보이론 §3” 두 문장으로 맞춘다.
- 근거 신뢰도: **본문 확인**.

## 잘 된 부분

- `attention-is-all-you-need.md`: $QK^\top$의 축별 shape, $T\times T$가 정확히 어디서 생기며 왜 $O(T^2)$인지까지 연결한다. 원형 2017 블록과 최신 LLM/ViT 변형을 분리한 점도 Physical AI 논문 독해에 직접 유용하다.
- `ppo.md`, `sac.md`: 알고리즘 이름을 보상·관측·안전 설계와 분리하고, on/off-policy의 데이터 사용 차이를 실제 하드웨어 비용으로 연결한다. 위 P1의 문구만 고치면 좋은 Working 진입점이다.
- `3d-gaussian-splatting.md`, `depth-anything.md`, `vggt.md`: 렌더링 속도와 온라인 매핑, 상대 깊이와 metric geometry, feed-forward 추론과 정밀 최적화를 반복해서 분리한다. 로봇 연구의 과장된 claim을 읽는 훈련으로 좋다.
- `clip.md`, `blip-2.md`, `llava.md`: shared embedding, learned-query bottleneck, linear connector를 서로 비교하여 “모델 이름”이 아니라 정보 병목과 학습 대상 파라미터로 구조를 읽게 한다.
- 각 논문의 `What it measured`와 `Reading the claim`은 결과 수치·실험 범위·일반화 주장을 분리하는 좋은 습관을 만든다.

## 학습 경로 판단과 최소 보완

현재 canonical-list의 연대순은 계보 파악에는 좋지만 초보 실습 순서로는 일부 왕복이 생긴다(예: PPO/SAC가 foundation 말미에, PointNet이 최신 3D 문서 뒤에 위치). 신규 과목을 늘릴 필요는 없다. 다음처럼 **기존 페이지를 묶어 읽는 안내 4줄**만 index에 추가하는 편이 효율적이다.

1. 공통 코어: Adam/BatchNorm/ResNet → Transformer → ViT → CLIP.
2. 언어/VLM 선택: seq2seq→Bahdanau→BERT/GPT-3→InstructGPT→Flamingo→BLIP-2→LLaVA/PaliGemma/Qwen.
3. 로봇 지각 선택: U-Net/Faster R-CNN/YOLO/DETR/SAM + PointNet/NeRF/3DGS/Depth Anything/VGGT.
4. 제어 선택: PPO와 SAC를 RL 기초 페이지와 함께 읽고, 이후 실제 VLA/로봇 시스템 문서에서 관측·행동·보상·평가를 추적.

Working 판정은 “노트를 읽었다”가 아니라 선택 영역에서 (a) 입력/출력 shape, (b) 손실의 각 항, (c) train/eval 차이, (d) 실험의 독립변수·대조군·지표, (e) 실패 가정을 자기 말로 설명할 수 있을 때로 제한하면 좋다. 별도 문제집을 만들 필요 없이 기존 `After reading` 체크리스트에서 한 항목을 실제 논문의 표/그림에 대조하는 정도면 충분하다.

## 파일별 완독 상태 및 발견 ID

| 파일 | 상태 | 발견 ID |
|---|---|---|
| `content/01-canonical-papers/notes/1-foundations/adam.md` | 완독·수정 필요 | papers-dl-001 |
| `content/01-canonical-papers/notes/1-foundations/alexnet.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/attention-is-all-you-need.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/bahdanau-attention.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/batch-norm.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/bert.md` | 완독·수정 필요 | papers-dl-003 |
| `content/01-canonical-papers/notes/1-foundations/gpt-3.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/index.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/instructgpt.md` | 완독·선택 개선 | papers-dl-014 |
| `content/01-canonical-papers/notes/1-foundations/lora.md` | 완독·개선 권장 | papers-dl-009 |
| `content/01-canonical-papers/notes/1-foundations/lstm.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/mae.md` | 완독·개선 권장 | papers-dl-002 |
| `content/01-canonical-papers/notes/1-foundations/ppo.md` | 완독·개선 권장 | papers-dl-007 |
| `content/01-canonical-papers/notes/1-foundations/resnet.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/sac.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/scaling-laws.md` | 완독·개선 권장 | papers-dl-012 |
| `content/01-canonical-papers/notes/1-foundations/seq2seq.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/vgg.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/1-foundations/vit.md` | 완독·개선 권장 | papers-dl-010 |
| `content/01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/depth-anything.md` | 완독·수정 필요 | papers-dl-004 |
| `content/01-canonical-papers/notes/2-computer-vision/detr.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/dino.md` | 완독·개선 권장 | papers-dl-002 |
| `content/01-canonical-papers/notes/2-computer-vision/faster-r-cnn.md` | 완독·개선 권장 | papers-dl-008 |
| `content/01-canonical-papers/notes/2-computer-vision/index.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/nerf.md` | 완독·수정 필요 | papers-dl-005 |
| `content/01-canonical-papers/notes/2-computer-vision/pointnet.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/sam.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/swin.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/u-net.md` | 완독·선택 개선 | papers-dl-013 |
| `content/01-canonical-papers/notes/2-computer-vision/vggt.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/video-understanding.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/2-computer-vision/yolo.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/3-vlm/blip-2.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/3-vlm/clip.md` | 완독·개선 권장 | papers-dl-002 |
| `content/01-canonical-papers/notes/3-vlm/flamingo.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/3-vlm/index.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/3-vlm/llava.md` | 완독·양호 | — |
| `content/01-canonical-papers/notes/3-vlm/paligemma.md` | 완독·수정 필요 | papers-dl-006 |
| `content/01-canonical-papers/notes/3-vlm/qwen-vl.md` | 완독·양호 | — |
| `content/03-deep-learning/index.md` | 완독·양호(최소 경로 안내 권장) | — |
| `content/03-deep-learning/lineage.md` | 완독·수정 필요 | papers-dl-011 |
| `content/03-deep-learning/physical-ai-ecosystem.md` | 완독·양호(시점 의존 표임을 유지) | — |

## 우선 처리 순서

1. papers-dl-001, 003~006, 011: 핵심 식·구조·학습 경로의 오개념을 먼저 제거.
2. papers-dl-002, 007~010, 012: 용어 중의성, 방법 범위, 한영 일치와 evidence 표현을 정교화.
3. papers-dl-013, 014: 읽기 흐름을 다듬는 선택 개선.
