---
title: Canonical Paper List
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

## 1. Deep Learning Foundations

시간순 정렬 — 2012년 ImageNet에서 시작해 CNN 계열과 RNN 계열이 2017년 Transformer에서 합류하는 흐름. [[03-deep-learning/lineage|계보도]] 참고.

- [x] [[notes/lstm|LSTM]] — *Long Short-Term Memory* (Hochreiter & Schmidhuber, Neural Computation 1997)
- [x] [[notes/alexnet|AlexNet]] — *ImageNet Classification with Deep CNNs* (Krizhevsky et al., NeurIPS 2012)
- [x] [[notes/seq2seq|seq2seq]] — *Sequence to Sequence Learning* (Sutskever et al., NeurIPS 2014)
- [x] [[notes/bahdanau-attention|Bahdanau Attention]] — *NMT by Jointly Learning to Align and Translate* (ICLR 2015)
- [x] [[notes/vgg|VGG]] — *Very Deep Convolutional Networks* (Simonyan & Zisserman, ICLR 2015)
- [x] [[notes/adam|Adam]] — *A Method for Stochastic Optimization* (Kingma & Ba, ICLR 2015)
- [x] [[notes/batch-norm|Batch Normalization]] (Ioffe & Szegedy, ICML 2015)
- [x] [[notes/resnet|ResNet]] — *Deep Residual Learning* (He et al., CVPR 2016)
- [x] [[notes/attention-is-all-you-need|Attention Is All You Need]] (Vaswani et al., NeurIPS 2017)
- [x] [[notes/bert|BERT]] (Devlin et al., NAACL 2019)
- [x] [[notes/gpt-3|GPT-3]] — *Language Models are Few-Shot Learners* (Brown et al., NeurIPS 2020)
- [x] [[notes/scaling-laws|Scaling Laws]] (Kaplan et al., 2020) + Chinchilla (Hoffmann et al., 2022)
- [x] [[notes/vit|ViT]] — *An Image is Worth 16x16 Words* (Dosovitskiy et al., ICLR 2021)
- [x] [[notes/mae|MAE]] — *Masked Autoencoders Are Scalable Vision Learners* (He et al., CVPR 2022)
- [x] [[notes/lora|LoRA]] — *Low-Rank Adaptation* (Hu et al., ICLR 2022)
- [x] [[notes/instructgpt|InstructGPT/RLHF]] — *Training LMs to Follow Instructions* (Ouyang et al., NeurIPS 2022)

## 2. Computer Vision

- [x] [[notes/u-net|U-Net]] (Ronneberger et al., MICCAI 2015)
- [x] [[notes/faster-r-cnn|Faster R-CNN]] (Ren et al., NeurIPS 2015)
- [x] [[notes/yolo|YOLO]] (Redmon et al., CVPR 2016)
- [x] [[notes/video-understanding|Video Understanding — I3D / SlowFast]] (2017–2019)
- [x] [[notes/detr|DETR]] — *End-to-End Object Detection with Transformers* (Carion et al., ECCV 2020)
- [x] [[notes/nerf|NeRF]] (Mildenhall et al., ECCV 2020)
- [x] [[notes/swin|Swin Transformer]] (Liu et al., ICCV 2021)
- [x] [[notes/dino|DINO → DINOv2]] (Caron et al., ICCV 2021 · Oquab et al., 2023)
- [x] [[notes/sam|SAM]] — *Segment Anything* (Kirillov et al., ICCV 2023)
- [x] [[notes/3d-gaussian-splatting|3D Gaussian Splatting]] (Kerbl et al., SIGGRAPH 2023)
- [x] [[notes/depth-anything|Depth Anything]] (Yang et al., CVPR 2024)
- [x] [[notes/vggt|VGGT]] — *Visual Geometry Grounded Transformer* (Wang et al., CVPR 2025)

## 3. Vision-Language Models (VLM)

- [x] [[notes/clip|CLIP]] — *Learning Transferable Visual Models From Natural Language Supervision* (Radford et al., ICML 2021)
- [x] [[notes/flamingo|Flamingo]] (Alayrac et al., NeurIPS 2022)
- [x] [[notes/blip-2|BLIP-2]] (Li et al., ICML 2023)
- [x] [[notes/llava|LLaVA]] — *Visual Instruction Tuning* (Liu et al., NeurIPS 2023)
- [x] [[notes/qwen-vl|Qwen-VL series]] (Qwen Team, 2023–2025) — representative open VLM line
- [ ] PaliGemma (2024) — representative small open VLM

## 4. Vision-Language-Action (VLA) / Robot Learning

- [x] [[notes/rt-1|RT-1]] — *Robotics Transformer* (Brohan et al., RSS 2023)
- [x] [[notes/rt-2|RT-2]] — *Vision-Language-Action Models* (Brohan et al., CoRL 2023)
- [x] [[notes/diffusion-policy|Diffusion Policy]] (Chi et al., RSS 2023)
- [x] [[notes/act|ACT / ALOHA]] — *Learning Fine-Grained Bimanual Manipulation* (Zhao et al., RSS 2023)
- [x] [[notes/open-x-embodiment|Open X-Embodiment]] — the cross-embodiment dataset effort (ICRA 2024)
- [x] [[notes/octo|Octo]] — open generalist robot policy (RSS 2024)
- [x] [[notes/openvla|OpenVLA]] (Kim et al., CoRL 2024)
- [x] [[notes/pi0|π0]] — *A Vision-Language-Action Flow Model* (Physical Intelligence, 2024)
- [x] [[notes/gr00t-n1|GR00T N1]] — NVIDIA humanoid foundation model (2025)

## 5. World Models

- [x] [[notes/world-models|World Models]] (Ha & Schmidhuber, NeurIPS 2018)
- [x] [[notes/planet|PlaNet]] (Hafner et al., ICML 2019)
- [x] [[notes/dreamer|Dreamer → DreamerV2 → DreamerV3]] (Hafner et al., 2020–2023, Nature 2025)
- [x] [[notes/jepa|JEPA line]] — LeCun 2022 position paper → I-JEPA (CVPR 2023) → V-JEPA / V-JEPA 2 (2024–2025)
- [x] [[notes/genie|Genie]] (Bruce et al., ICML 2024) → Genie 2 (2024)
- [x] [[notes/sora|Sora]] — *Video Generation Models as World Simulators* (OpenAI, 2024)
- [x] [[notes/cosmos|Cosmos]] — world foundation models for physical AI (NVIDIA, 2025)

## 6. Diffusion & Generative Models

- [x] [[notes/vae|VAE]] — *Auto-Encoding Variational Bayes* (Kingma & Welling, ICLR 2014)
- [x] [[notes/gan|GAN]] (Goodfellow et al., NeurIPS 2014)
- [x] [[notes/ddpm|DDPM]] — *Denoising Diffusion Probabilistic Models* (Ho et al., NeurIPS 2020)
- [x] [[notes/score-sde|Score SDE]] — *Score-Based Generative Modeling through SDEs* (Song et al., ICLR 2021)
- [x] [[notes/ddim|DDIM]] (Song et al., ICLR 2021)
- [x] [[notes/classifier-free-guidance|Classifier-Free Guidance]] (Ho & Salimans, 2022)
- [x] [[notes/latent-diffusion|Latent Diffusion / Stable Diffusion]] (Rombach et al., CVPR 2022)
- [x] [[notes/controlnet|ControlNet]] (Zhang et al., ICCV 2023)
- [x] [[notes/dit|DiT]] — *Scalable Diffusion Models with Transformers* (Peebles & Xie, ICCV 2023)
- [x] [[notes/flow-matching|Flow Matching]] (Lipman et al., ICLR 2023)

## 7. Robotics & Control (textbook + key references)

- [x] [[04-robotics/modern-robotics-book|Modern Robotics]] (Lynch & Park) — study guide with free official PDF & course links
- [x] [[04-robotics/lqr-lqg|LQR/LQG]] — study guide (Underactuated Robotics, Stanford EE363)
- [x] [[04-robotics/mpc|MPC]] — study guide + Mayne et al., *Constrained MPC* (Automatica 2000)
- [x] [[04-robotics/convex-mpc-legged|Convex MPC for legged robots]] — MIT Cheetah (IROS 2018 + open-access follow-up)

## 8. Construction Robotics

계보와 랩 지도: [[05-construction-robotics/lineage|Construction Robotics Lineage]] · [[05-construction-robotics/labs|Labs]]

- [ ] Bock — *The future of construction automation* ([Automation in Construction, 2015](https://doi.org/10.1016/j.autcon.2015.07.022)) — 분야 조감의 표준 서베이
- [ ] Davila Delgado et al. — *Robotics and automated systems in construction* ([J. Building Engineering, 2019](https://doi.org/10.1016/j.jobe.2019.100868)) — 도입 장벽 분석
- [ ] Jud et al. — *HEAP: the autonomous walking excavator* ([ETH RSL](https://rsl.ethz.ch/robots-media/heap.html)) — 학습 시대 중장비 자율성의 기준 시스템
- [ ] ETH — autonomous dry-stone wall construction ([project](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)) — 비정형 재료 조작의 이정표
- [ ] (심화 서베이·개별 논문은 읽으며 추가)
