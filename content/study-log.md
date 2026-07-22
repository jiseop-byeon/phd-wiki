---
title: Study Log
tags: [log]
---

무엇을 읽고 공부했는지 기록하는 일지. 일주일에 한 번이라도 좋으니 꾸준히 남긴다.
나중에 다시 보면 "그때 내가 뭘 몰랐는지"가 보여서 복습 지점을 찾기 좋다.

## 2026-07

### 2026-07-22

- 위키 개설: Obsidian + Quartz + GitHub Pages 구축
- 첫 논문 노트 작성: [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]]
- 기초 1차 배치 (2012→2016 연대순): [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/vgg|VGG]], [[01-canonical-papers/notes/1-foundations/bahdanau-attention|Bahdanau Attention]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]
- 계보도에 2012–2017 구간 추가 (CNN 갈래 + RNN 갈래 → Transformer 합류)
- 다음 읽을 것: Adam, BatchNorm, seq2seq, LSTM 또는 바로 ViT/CLIP
- 기초 섹션 완주 + Transformer 이후 진출 (총 12편 추가):
  기초 마무리 — [[01-canonical-papers/notes/1-foundations/lstm|LSTM]], [[01-canonical-papers/notes/1-foundations/seq2seq|seq2seq]], [[01-canonical-papers/notes/1-foundations/adam|Adam]], [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]
  Transformer 이후 — [[01-canonical-papers/notes/1-foundations/bert|BERT]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]], [[01-canonical-papers/notes/1-foundations/scaling-laws|Scaling Laws+Chinchilla]], [[01-canonical-papers/notes/1-foundations/vit|ViT]], [[01-canonical-papers/notes/1-foundations/mae|MAE]], [[01-canonical-papers/notes/1-foundations/lora|LoRA]], [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]], [[01-canonical-papers/notes/3-vlm/clip|CLIP]]
- VGGT(CVPR 2025 Best Paper) 확인 후 CV 섹션에 추가
- 다음: VLM 계열 (Flamingo, BLIP-2, LLaVA) 또는 디퓨전 계열 (VAE, GAN, DDPM)
- 노트 형식 개선: 모든 노트 첫 줄에 "저자, 학회 연도 — arXiv·PDF·Code" 표기; 폴더명 `01-canonical-papers`로 변경
- VLM 배치 완료: [[01-canonical-papers/notes/3-vlm/flamingo|Flamingo]], [[01-canonical-papers/notes/3-vlm/blip-2|BLIP-2]], [[01-canonical-papers/notes/3-vlm/llava|LLaVA]] — CLIP→연결자 설계 경쟁→지시 튜닝의 흐름; 다음은 VLA로 가는 관문 통과
- 다음: 디퓨전 계열 (VAE, GAN, DDPM, Score SDE) 또는 바로 VLA (RT-1, RT-2, Diffusion Policy)
- 기초 정리 페이지 3편 (reference 자료를 내 언어로 재구성): [[02-foundations/optimization|최적화]], [[02-foundations/probability|확률과 랜덤 프로세스]], [[02-foundations/signal-processing|신호처리]]
- 디퓨전 기초 배치: [[01-canonical-papers/notes/6-diffusion/vae|VAE]], [[01-canonical-papers/notes/6-diffusion/gan|GAN]], [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]], [[01-canonical-papers/notes/6-diffusion/score-sde|Score SDE]] — VAE(안정·흐릿) vs GAN(선명·불안정)의 긴장을 DDPM이 해소하고 Score SDE가 이론으로 통합
- 다음: VLA 진입 (RT-1, RT-2, Diffusion Policy, ACT) — 디퓨전 수학 준비 완료
- VLA 1차 배치: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]], [[01-canonical-papers/notes/4-vla/act|ACT/ALOHA]] — 로봇 데이터 스케일링(RT-1) → 웹 지식 전이(RT-2) → 다봉 행동 분포(DP) → 행동 청킹(ACT)
- 다음: VLA 2차 (Open X-Embodiment, Octo, OpenVLA, π0, GR00T N1)로 VLA 섹션 완주
- 기초 섹션 확장 (4편 추가, 총 7편 체계 완성): [[02-foundations/linear-algebra|선형대수]], [[02-foundations/calculus-backprop|미적분과 역전파]], [[02-foundations/information-theory|정보이론]], [[02-foundations/rl-basics|강화학습 기초]] — 위키의 모든 논문을 읽기에 충분한 배경 세트
- VLA 섹션 완주 (5편): [[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]], [[01-canonical-papers/notes/4-vla/octo|Octo]], [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]], [[01-canonical-papers/notes/4-vla/pi0|π0]], [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] — 데이터 풀링 → 오픈 모듈식 정책 → 오픈 VLA → flow matching 융합 → 휴머노이드 데이터 피라미드
- 다음: 월드모델 섹션 (World Models, PlaNet, Dreamer, JEPA, Genie, Sora, Cosmos)
- sudoremove.com 점검: 내용 상충 없음 확인; 배울 점으로 생태계 카탈로그 채택 → [[03-deep-learning/physical-ai-ecosystem|Physical AI Ecosystem]] 페이지 신설
- 선형대수 페이지에 제어이론 연결 섹션 추가 (상태공간, 고유값=안정성, 가제어성 랭크 조건)
- 월드모델 섹션 완주 (7편): [[01-canonical-papers/notes/5-world-models/world-models|World Models]], [[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer v1–3]], [[01-canonical-papers/notes/5-world-models/jepa|JEPA 계열]], [[01-canonical-papers/notes/5-world-models/genie|Genie]], [[01-canonical-papers/notes/5-world-models/sora|Sora]], [[01-canonical-papers/notes/5-world-models/cosmos|Cosmos]] — 꿈속 훈련 → RSSM → 상상 속 actor-critic → 표현 공간 예측(반대 진영) → 인터넷 비디오에서 행동 발견 → 시뮬레이터 가설 → 인프라화
- 다음 후보: CV 나머지 (U-Net~VGGT) 또는 디퓨전 나머지 (DDIM, CFG, LDM, ControlNet, DiT, Flow Matching) 또는 건설로봇 서베이 수집
- CV 섹션 완주 (12편): U-Net, Faster R-CNN, YOLO, I3D/SlowFast, DETR, NeRF, Swin, DINO/DINOv2, SAM, 3DGS, Depth Anything, VGGT
- 디퓨전 섹션 완주 (6편): DDIM, CFG, Latent Diffusion, ControlNet, DiT, Flow Matching — 딥러닝 파트(섹션 1~6) 논문 노트 전부 완료 (총 58편)
- 방침: foundations 페이지들을 제어이론 교재 수준의 깊이로 증보하기로 함 (다음 작업)
- 남은 큰 덩어리: ① foundations 심화 증보 ② 건설로봇 서베이 수집(섹션 8) ③ 로보틱스/제어 노트(섹션 7)
- foundations 심화 증보 완료: 7개 페이지 전부 교재 수준으로 — 유도(정규방정식, KL 비음수성, 벨만, 정책 그래디언트), 계산 예제(2층 역전파, 합성곱, 베이즈 진단, KKT 투영, MPC-QP 정식화), 스스로 점검 문제 추가
- 남은 큰 덩어리: ① 건설로봇 서베이 수집(섹션 8) ② 로보틱스/제어 노트(섹션 7: Modern Robotics 챕터, LQR, MPC)
