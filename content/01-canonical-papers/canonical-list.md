---
title: 1. Canonical Paper List
tags: [moc, papers]
---

## English

The reading backbone of this wiki: bible-tier and milestone papers per subarea, in rough
reading order. Check off as notes are written (one note per paper in `notes/`).
Recent-trend papers get appended over time via the tracking workflow.

## 한국어

이 위키의 중심이 되는 논문 목록: 분야별로 꼭 읽어야 할 기념비적 논문들을
대략적인 읽기 순서로 정리했다. 논문 노트를 작성하면 체크 표시를 남긴다
(`notes/`에 논문 하나당 노트 하나). 최신 논문은 트렌드를 따라가며 계속 추가한다.

---

**읽기 깊이 표시** ([[01-canonical-papers/how-to-read|0. How to Read Papers]] 참고):
★ 원문 정독 (방법·실험까지) · ◐ 노트 후 원문 훑기 · ○ 노트로 충분 (계보 이해)
— 이 기호는 **권장 읽기 분량**이지 숙련 수준이 아니다: ★를 정독해도 mastery(가정 비판·변형 설계)에 도달한 것은 아니다.

## 1. Deep Learning Foundations

시간순 정렬 — 2012년 ImageNet에서 시작해 CNN 계열과 RNN 계열이 2017년 Transformer에서 합류하는 흐름. [[03-deep-learning/lineage|계보도]] 참고.

- [x] ○ [[notes/1-foundations/lstm|LSTM]] — *Long Short-Term Memory* (Hochreiter & Schmidhuber, Neural Computation 1997)
- [x] ○ [[notes/1-foundations/alexnet|AlexNet]] — *ImageNet Classification with Deep CNNs* (Krizhevsky et al., NeurIPS 2012)
- [x] ○ [[notes/1-foundations/seq2seq|seq2seq]] — *Sequence to Sequence Learning* (Sutskever et al., NeurIPS 2014)
- [x] ○ [[notes/1-foundations/bahdanau-attention|Bahdanau Attention]] — *NMT by Jointly Learning to Align and Translate* (ICLR 2015)
- [x] ○ [[notes/1-foundations/vgg|VGG]] — *Very Deep Convolutional Networks* (Simonyan & Zisserman, ICLR 2015)
- [x] ◐ [[notes/1-foundations/adam|Adam]] — *A Method for Stochastic Optimization* (Kingma & Ba, ICLR 2015)
- [x] ◐ [[notes/1-foundations/batch-norm|Batch Normalization]] (Ioffe & Szegedy, ICML 2015)
- [x] ◐ [[notes/1-foundations/resnet|ResNet]] — *Deep Residual Learning* (He et al., CVPR 2016)
- [x] ★ [[notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]] (Vaswani et al., NeurIPS 2017)
- [x] ◐ [[notes/1-foundations/bert|BERT]] (Devlin et al., NAACL 2019)
- [x] ◐ [[notes/1-foundations/gpt-3|GPT-3]] — *Language Models are Few-Shot Learners* (Brown et al., NeurIPS 2020)
- [x] ◐ [[notes/1-foundations/scaling-laws|Scaling Laws]] (Kaplan et al., 2020) + Chinchilla (Hoffmann et al., 2022)
- [x] ◐ [[notes/1-foundations/vit|ViT]] — *An Image is Worth 16x16 Words* (Dosovitskiy et al., ICLR 2021)
- [x] ◐ [[notes/1-foundations/mae|MAE]] — *Masked Autoencoders Are Scalable Vision Learners* (He et al., CVPR 2022)
- [x] ◐ [[notes/1-foundations/lora|LoRA]] — *Low-Rank Adaptation* (Hu et al., ICLR 2022)
- [x] ◐ [[notes/1-foundations/instructgpt|InstructGPT/RLHF]] — *Training LMs to Follow Instructions* (Ouyang et al., NeurIPS 2022)

## 2. Computer Vision

- [x] ◐ [[notes/2-computer-vision/u-net|U-Net]] (Ronneberger et al., MICCAI 2015)
- [x] ○ [[notes/2-computer-vision/faster-r-cnn|Faster R-CNN]] (Ren et al., NeurIPS 2015)
- [x] ◐ [[notes/2-computer-vision/yolo|YOLO]] (Redmon et al., CVPR 2016)
- [x] ◐ [[notes/2-computer-vision/video-understanding|Video Understanding — I3D / SlowFast]] (2017–2019)
- [x] ◐ [[notes/2-computer-vision/detr|DETR]] — *End-to-End Object Detection with Transformers* (Carion et al., ECCV 2020)
- [x] ◐ [[notes/2-computer-vision/nerf|NeRF]] (Mildenhall et al., ECCV 2020)
- [x] ○ [[notes/2-computer-vision/swin|Swin Transformer]] (Liu et al., ICCV 2021)
- [x] ◐ [[notes/2-computer-vision/dino|DINO → DINOv2]] (Caron et al., ICCV 2021 · Oquab et al., 2023)
- [x] ★ [[notes/2-computer-vision/sam|SAM]] — *Segment Anything* (Kirillov et al., ICCV 2023)
- [x] ◐ [[notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]] (Kerbl et al., SIGGRAPH 2023)
- [x] ◐ [[notes/2-computer-vision/depth-anything|Depth Anything]] (Yang et al., CVPR 2024)
- [x] ★ [[notes/2-computer-vision/vggt|VGGT]] — *Visual Geometry Grounded Transformer* (Wang et al., CVPR 2025)

## 3. Vision-Language Models (VLM)

- [x] ★ [[notes/3-vlm/clip|CLIP]] — *Learning Transferable Visual Models From Natural Language Supervision* (Radford et al., ICML 2021)
- [x] ○ [[notes/3-vlm/flamingo|Flamingo]] (Alayrac et al., NeurIPS 2022)
- [x] ○ [[notes/3-vlm/blip-2|BLIP-2]] (Li et al., ICML 2023)
- [x] ◐ [[notes/3-vlm/llava|LLaVA]] — *Visual Instruction Tuning* (Liu et al., NeurIPS 2023)
- [x] ◐ [[notes/3-vlm/qwen-vl|Qwen-VL series]] (Qwen Team, 2023–2025) — representative open VLM line
- [x] ○ [[notes/3-vlm/paligemma|PaliGemma]] (Google, 2024) — 작은 오픈 VLM의 대표; π0의 백본

## 4. Vision-Language-Action (VLA) / Robot Learning

- [x] ◐ [[notes/4-vla/rt-1|RT-1]] — *Robotics Transformer* (Brohan et al., RSS 2023)
- [x] ★ [[notes/4-vla/rt-2|RT-2]] — *Vision-Language-Action Models* (Brohan et al., CoRL 2023)
- [x] ★ [[notes/4-vla/diffusion-policy|Diffusion Policy]] (Chi et al., RSS 2023)
- [x] ★ [[notes/4-vla/act|ACT / ALOHA]] — *Learning Fine-Grained Bimanual Manipulation* (Zhao et al., RSS 2023)
- [x] ◐ [[notes/4-vla/open-x-embodiment|Open X-Embodiment]] — the cross-embodiment dataset effort (ICRA 2024)
- [x] ◐ [[notes/4-vla/octo|Octo]] — open generalist robot policy (RSS 2024)
- [x] ◐ [[notes/4-vla/openvla|OpenVLA]] (Kim et al., CoRL 2024)
- [x] ★ [[notes/4-vla/pi0|π0]] — *A Vision-Language-Action Flow Model* (Physical Intelligence, 2024)
- [x] ★ [[notes/4-vla/gr00t-n1|GR00T N1]] — NVIDIA humanoid foundation model (2025)

## 5. World Models

- [x] ◐ [[notes/5-world-models/world-models|World Models]] (Ha & Schmidhuber, NeurIPS 2018)
- [x] ◐ [[notes/5-world-models/planet|PlaNet]] (Hafner et al., ICML 2019)
- [x] ★ [[notes/5-world-models/dreamer|Dreamer → DreamerV2 → DreamerV3]] (Hafner et al., 2020–2023, Nature 2025)
- [x] ◐ [[notes/5-world-models/jepa|JEPA line]] — LeCun 2022 position paper → I-JEPA (CVPR 2023) → V-JEPA / V-JEPA 2 (2024–2025)
- [x] ◐ [[notes/5-world-models/genie|Genie]] (Bruce et al., ICML 2024) → Genie 2 (2024)
- [x] ○ [[notes/5-world-models/sora|Sora]] — *Video Generation Models as World Simulators* (OpenAI, 2024)
- [x] ★ [[notes/5-world-models/cosmos|Cosmos]] — world foundation models for physical AI (NVIDIA, 2025)

## 6. Diffusion & Generative Models

- [x] ◐ [[notes/6-diffusion/vae|VAE]] — *Auto-Encoding Variational Bayes* (Kingma & Welling, ICLR 2014)
- [x] ○ [[notes/6-diffusion/gan|GAN]] (Goodfellow et al., NeurIPS 2014)
- [x] ★ [[notes/6-diffusion/ddpm|DDPM]] — *Denoising Diffusion Probabilistic Models* (Ho et al., NeurIPS 2020)
- [x] ◐ [[notes/6-diffusion/score-sde|Score SDE]] — *Score-Based Generative Modeling through SDEs* (Song et al., ICLR 2021)
- [x] ◐ [[notes/6-diffusion/ddim|DDIM]] (Song et al., ICLR 2021)
- [x] ◐ [[notes/6-diffusion/classifier-free-guidance|Classifier-Free Guidance]] (Ho & Salimans, 2022)
- [x] ◐ [[notes/6-diffusion/latent-diffusion|Latent Diffusion / Stable Diffusion]] (Rombach et al., CVPR 2022)
- [x] ○ [[notes/6-diffusion/controlnet|ControlNet]] (Zhang et al., ICCV 2023)
- [x] ◐ [[notes/6-diffusion/dit|DiT]] — *Scalable Diffusion Models with Transformers* (Peebles & Xie, ICCV 2023)
- [x] ★ [[notes/6-diffusion/flow-matching|Flow Matching]] (Lipman et al., ICLR 2023)

## 7. Robotics & Control (textbook + key references)

- [x] ★ [[04-robotics/modern-robotics-book|Modern Robotics]] (Lynch & Park) — study guide with free official PDF & course links
- [x] ◐ [[04-robotics/lqr-lqg|LQR/LQG]] — study guide (Underactuated Robotics, Stanford EE363)
- [x] ◐ [[04-robotics/mpc|MPC]] — study guide + Mayne et al., *Constrained MPC* (Automatica 2000)
- [x] ○ [[04-robotics/convex-mpc-legged|Convex MPC for legged robots]] — MIT Cheetah (IROS 2018 + open-access follow-up)
- [x] ◐ [[04-robotics/state-estimation-slam|State Estimation, Localization & SLAM]] — study guide (Probabilistic Robotics 기반)
- [x] ◐ [[04-robotics/planning-decision-making|Planning & Decision-Making]] — study guide (search·sampling·trajectory optimization·TAMP)
- [x] ◐ [[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] — study guide (MR 12장 연장)
- [x] ◐ [[04-robotics/robot-systems-deployment|Robot Systems, Embodiment & Deployment]] — study guide (timing·frames·middleware·failure)
- [x] ◐ [[04-robotics/hri-safety|Human–Robot Interaction & Safety]] — study guide (autonomy levels·human studies·hazard/risk)

## 8. Construction Robotics

계보와 랩 지도: [[05-construction-robotics/lineage|Construction Robotics Lineage]] · [[05-construction-robotics/labs|Labs]]

- [x] ◐ [[notes/8-construction/bock-2015|Bock — *The future of construction automation*]] (Automation in Construction, 2015) — 분야 조감의 표준 서베이
- [x] ◐ [[notes/8-construction/davila-delgado-2019|Davila Delgado et al. — 도입 장벽 분석]] (J. Building Engineering, 2019)
- [x] ★ [[notes/8-construction/heap|HEAP — the autonomous walking excavator]] (Jud et al., Automation in Construction 2021) — 중장비 자율성의 기준 시스템 (돌담 프로젝트 포함)
- [x] ★ [[notes/8-construction/ext|ExT — 굴착의 사전학습→파인튜닝]] (Zhai, Terenzi et al., ETH RSL 2025) — physical AI가 건설 기계에 진입한 최전선
- [ ] ○ ICRA Construction Robotics Workshop ([2024](https://construction-robots.github.io/index2024.html)) — ExACT(굴착기 ACT) 등; 이 교차점의 커뮤니티
- [ ] (심화 서베이·개별 논문은 읽으며 추가)
