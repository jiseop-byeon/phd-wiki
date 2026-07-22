---
title: Glossary
tags: [reference]
---

빠르게 찾아보는 용어 사전. 새 용어를 만날 때마다 추가한다. (English term — 한국어 설명, 관련 노트 링크)

## 혼동하기 쉬운 쌍 · Confusable pairs

논문 독해에서 실제로 막히는 지점은 낯선 용어보다 비슷한 용어의 구분이다.

- **Probability vs Likelihood** — 확률은 파라미터를 고정하고 데이터를 변수로 본다; 우도는 데이터를 고정하고 파라미터의 함수로 본다. MLE의 "L"이 후자. → [[02-foundations/probability|확률 §4]]
- **Entropy vs Cross-entropy vs KL** — $H(p)$는 자기 자신의 불확실성; $H(p,q)$는 $p$를 $q$의 부호로 인코딩하는 비용; KL = 그 차이 = $H(p,q) - H(p)$. → [[02-foundations/information-theory|정보이론]]
- **Logits vs Probabilities** — softmax 이전의 실수 점수 vs 이후의 확률. 손실은 보통 logits에서 직접 계산한다(수치 안정성).
- **State vs Observation** — 상태는 과거를 요약하는 마르코프 변수(숨겨져 있을 수 있음); 관측은 센서가 실제로 주는 것. 둘이 다르면 POMDP다. → [[02-foundations/rl-basics|RL 기초 §1]]
- **Policy vs Controller** — 같은 역할(상태→행동)의 두 커뮤니티 용어. 정책은 학습 문맥, 제어기는 모델 기반 설계·안정성 보장 문맥에서 쓰인다. → [[04-robotics/modern-robotics/ch11-robot-control|MR 11장]]
- **World model vs Model-based RL** — 월드모델은 학습된 동역학 모델 그 자체; model-based RL은 그것을 계획/학습에 쓰는 방법론. → [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]]
- **VLM vs VLA** — VLM은 텍스트를 출력하고, VLA는 로봇 행동을 출력한다(대개 VLM 백본 + 행동 헤드). → [[01-canonical-papers/notes/4-vla/rt-2|RT-2]]
- **Behavior cloning vs Imitation learning vs Offline RL** — BC는 IL의 부분집합(시연의 지도학습); IL은 시연 활용 전반(DAgger, IRL 포함); offline RL은 보상 신호로 시연자 초과 성능을 노린다.
- **Diffusion vs Flow matching** — 같은 수송(노이즈→데이터)의 두 학습법: 디퓨전은 확률적 노이즈 제거 체인을, FM은 결정론적 속도장을 직접 회귀 — 경로가 곧아 추론 스텝이 적다. → [[01-canonical-papers/notes/6-diffusion/flow-matching|Flow Matching]]
- **Pose vs Configuration** — pose는 강체 하나의 SE(3) 위치·자세; configuration은 로봇 전체의 자유도(모든 관절각 포함). → [[02-foundations/se3-geometry|SE(3)]], [[04-robotics/modern-robotics/ch02-configuration-space|MR 2장]]
- **Space vs Body (Jacobian/twist)** — 같은 양을 어느 프레임에서 표현했는가의 차이; $[\text{Ad}_T]$로 변환된다. MR에서 가장 흔한 실수 지점. → [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장]]
- **LQR vs MPC** — LQR은 무제약·무한 지평의 닫힌형 해; MPC는 제약 처리·유한 지평·매 스텝 재풀이. → [[04-robotics/mpc|MPC]]
- **Open-loop vs Closed-loop** — 계획을 실행하는 동안 새 관측을 반영하는가; receding horizon은 closed-loop을 만드는 장치다.
- **Objective vs Metric** — 학습이 최소화하는 것 vs 평가에 쓰는 것. 둘은 자주 다르고(교차 엔트로피로 학습, mAP로 평가), 그 간극 자체가 논문의 논점일 때가 있다. → [[02-foundations/ml-practice|ML 실무 §3]]

## A–C

- **Action chunking (행동 청킹)** — 행동을 하나씩이 아니라 수십 스텝 덩어리로 예측해 복합 오차를 줄이는 기법. → [[01-canonical-papers/notes/4-vla/act|ACT]], [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]
- **Advantage (어드밴티지)** — $A = Q - V$. 어떤 행동이 그 상태의 평균적 선택보다 얼마나 나은가. → [[02-foundations/rl-basics|RL 기초]]
- **Attention (어텐션)** — 쿼리(Q)와 키(K)의 유사도로 값(V)을 가중합하는 연산. 시퀀스 안의 임의의 두 위치를 한 번에 연결한다. → [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]
- **Autoregressive (자기회귀)** — 이전 출력들을 조건으로 다음 토큰을 하나씩 생성. GPT 계열, 다수의 VLA가 이 방식. → [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]
- **Bellman equation (벨만 방정식)** — 오늘의 가치 = 보상 + 할인된 내일의 가치라는 고정점 방정식. 모든 RL의 뿌리. → [[02-foundations/rl-basics|RL 기초]]
- **BLEU** — 기계번역 품질 지표. 생성문과 참조 번역의 n-gram 겹침을 측정.
- **CFG (Classifier-Free Guidance)** — 조건부/무조건부 예측의 차이 방향으로 외삽해 조건 충실도를 높이는 샘플링 기법. → [[01-canonical-papers/notes/6-diffusion/classifier-free-guidance|CFG]]
- **Condition number (조건수)** — $\lambda_{max}/\lambda_{min}$. 최적화 문제의 난이도 그 자체. → [[02-foundations/linear-algebra|선형대수]]
- **Contrastive learning (대조학습)** — 짝이 맞는 쌍은 가깝게, 아닌 쌍은 멀게 임베딩을 학습. → [[01-canonical-papers/notes/3-vlm/clip|CLIP]], [[02-foundations/information-theory|InfoNCE]]
- **Cross-entropy (교차 엔트로피)** — $-E_p[\log q]$. 분류·언어모델의 표준 손실이며 그 정체는 MLE. → [[02-foundations/information-theory|정보이론]]
- **CVAE** — 조건부 VAE. 조건이 주어졌을 때의 다양한 출력 분포를 잠재변수로 담는다. → [[01-canonical-papers/notes/4-vla/act|ACT]]

## D–I

- **Diffusion model (디퓨전 모델)** — 데이터에 노이즈를 점진적으로 섞는 고정 과정을 학습으로 되돌려 생성하는 모델. → [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]
- **DiT (Diffusion Transformer)** — 디퓨전의 U-Net을 잠재 패치 위의 Transformer로 교체한 백본. π0·GR00T 행동 헤드의 구조. → [[01-canonical-papers/notes/6-diffusion/dit|DiT]]
- **ELBO (증거 하한)** — $E_q[\log p(x|z)] - D_{KL}(q\|p)$. VAE·디퓨전·월드모델 학습의 목적함수. → [[02-foundations/information-theory|정보이론 §5]]
- **EMA teacher** — 학생 가중치의 지수이동평균으로 만든 교사. 자기지도(DINO)와 RL 타깃망의 안정화 장치. → [[01-canonical-papers/notes/2-computer-vision/dino|DINO]]
- **Embedding (임베딩)** — 토큰·이미지 패치 등 이산 입력을 연속 벡터 공간으로 옮긴 표현.
- **FiLM** — 조건 신호로 특징맵의 스케일·이동을 변조하는 조건화 기법. → [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]
- **Fine-tuning (파인튜닝)** — 사전학습 모델을 특정 작업 데이터로 추가 학습. → [[01-canonical-papers/notes/1-foundations/bert|BERT]], [[01-canonical-papers/notes/1-foundations/lora|LoRA]]
- **Flow matching** — 노이즈→데이터 확률 경로의 속도장을 직접 회귀하는 생성 학습법. π0의 행동 생성 엔진. → [[01-canonical-papers/notes/6-diffusion/flow-matching|Flow Matching]]
- **Gaussian splatting** — 장면을 수백만 개의 3D 가우시안으로 표현하고 래스터라이즈하는 실시간 3D 표현. → [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3DGS]]
- **Imitation learning (모방 학습)** — 전문가 시연으로 정책을 지도학습. 로봇 매니퓰레이션의 주류. → [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]
- **InfoNCE** — 배치 안의 다른 샘플들을 "클래스"로 쓰는 대조 손실. 상호 정보량의 하한. → [[02-foundations/information-theory|정보이론 §4]]

## K–P

- **KKT 조건** — 제약 최적화의 1차 최적성 조건: 정상성, 원/쌍대 가능성, 상보 여유성. → [[02-foundations/optimization|최적화 §4]]
- **KL divergence** — $E_p[\log p/q]$. 진실이 $p$일 때 $q$를 쓰는 추가 비용. VAE 정규화·RLHF 페널티·증류의 수학. → [[02-foundations/information-theory|정보이론 §3]]
- **Latent action (잠재 행동)** — 라벨 없는 비디오의 프레임 사이에서 비지도로 발견된 행동 표현. → [[01-canonical-papers/notes/5-world-models/genie|Genie]]
- **LayerNorm** — 샘플별 특징 차원 정규화. Transformer의 기본 구성 요소. → [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]] (비교)
- **LoRA** — 얼린 가중치에 저랭크 업데이트 $\Delta W = BA$만 학습하는 파라미터 효율 파인튜닝. → [[01-canonical-papers/notes/1-foundations/lora|LoRA]]
- **MLE (최대우도추정)** — $\arg\max_\theta \log p(x|\theta)$. 교차 엔트로피와 MSE 손실의 기원. → [[02-foundations/probability|확률 §4]]
- **MPC (Model Predictive Control)** — 매 주기 유한 지평 최적 제어를 풀고 첫 입력만 적용하는 제어. → [[04-robotics/mpc|MPC]], [[02-foundations/optimization|최적화 §5]]
- **Multi-head attention** — 어텐션을 여러 저차원 부분공간에서 병렬 수행해 서로 다른 관계를 학습. → [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]
- **NeRF** — (위치, 시선) → (색, 밀도) MLP와 볼륨 렌더링으로 장면을 표현하는 암시적 3D. → [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]
- **Positional encoding (위치 인코딩)** — 순서를 모르는 어텐션에 위치 정보를 주입하는 방법. NeRF의 고주파 표현에도 쓰인다.
- **PPO** — 정책 비율을 클리핑해 신뢰 영역을 흉내 내는 정책 그래디언트. RLHF 속의 알고리즘. → [[02-foundations/rl-basics|RL 기초 §4]]
- **Pseudo-label (의사 라벨)** — 교사 모델의 예측을 라벨 삼아 무라벨 데이터로 학생을 학습. → [[01-canonical-papers/notes/2-computer-vision/depth-anything|Depth Anything]]

## Q–Z

- **Q-Former** — 학습된 쿼리로 이미지를 소수 토큰으로 증류하는 연결 모듈. → [[01-canonical-papers/notes/3-vlm/blip-2|BLIP-2]]
- **Receding horizon** — 지평을 앞으로 밀며 계획을 반복 갱신하는 MPC/정책의 실행 구조. → [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]
- **RLHF** — 인간 선호로 보상 모델을 배우고 RL로 정책을 정렬하는 3단계 레시피. → [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]]
- **RSSM** — 결정론적+확률적 상태를 함께 갖는 순환 상태공간 모델. 월드모델의 표준 백본. → [[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]]
- **Scaling law (스케일링 법칙)** — 손실이 파라미터·데이터·연산의 거듭제곱 법칙을 따른다는 경험 법칙. → [[01-canonical-papers/notes/1-foundations/scaling-laws|Scaling Laws]]
- **Self-attention** — 한 시퀀스가 자기 자신을 참조하는 어텐션 (Q, K, V가 같은 시퀀스에서). → [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]
- **SfM (Structure from Motion)** — 여러 사진에서 카메라 자세와 성긴 3D 구조를 복원하는 고전 파이프라인. → [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]] (이를 feed-forward로 대체)
- **Skip connection** — 입력을 출력에 더하거나 이어붙여 그래디언트 고속도로를 만드는 연결. → [[01-canonical-papers/notes/1-foundations/resnet|ResNet]], [[01-canonical-papers/notes/2-computer-vision/u-net|U-Net]]
- **Stop-gradient** — 역전파를 의도적으로 차단하는 연산. 논문 그림의 점선 화살표. → [[02-foundations/calculus-backprop|미적분·역전파 §5]]
- **TD error** — $r + \gamma V(s') - V(s)$. RL의 만능 학습 신호. → [[02-foundations/rl-basics|RL 기초 §3]]
- **Teleoperation (원격조작)** — 사람이 장치로 로봇을 조종해 시연 데이터를 만드는 방법. → [[01-canonical-papers/notes/4-vla/act|ALOHA]]
- **VLA (Vision-Language-Action)** — 시각·언어 입력에서 로봇 행동을 직접 출력하는 모델. → [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/pi0|π0]]
- **VQ (Vector Quantization)** — 연속 표현을 코드북의 이산 코드로 양자화. 토크나이저의 핵심. → [[01-canonical-papers/notes/5-world-models/genie|Genie]], [[01-canonical-papers/notes/6-diffusion/latent-diffusion|VQGAN]]
- **World model (월드모델)** — 환경의 다음 상태를 예측하도록 학습된 모델. 상상 속 계획·학습을 가능하게 한다. → [[01-canonical-papers/notes/5-world-models/world-models|World Models]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]]
- **Zero convolution** — 0으로 초기화된 연결층. 학습 시작 시 no-op을 보장하는 안전장치. → [[01-canonical-papers/notes/6-diffusion/controlnet|ControlNet]]
- **Zero-shot** — 해당 작업의 학습 예시 없이 바로 수행하는 능력. → [[01-canonical-papers/notes/3-vlm/clip|CLIP]], [[01-canonical-papers/notes/2-computer-vision/sam|SAM]]
