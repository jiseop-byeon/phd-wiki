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

시간순 정렬 — 2012년 ImageNet에서 시작해 CNN 계열과 RNN 계열이 2017년 Transformer에서 합류하는 흐름. [[10-deep-learning/lineage|계보도]] 참고.

- [x] [[notes/lstm|LSTM]] — *Long Short-Term Memory* (Hochreiter & Schmidhuber, Neural Computation 1997)
- [x] [[notes/alexnet|**AlexNet**]] — *ImageNet Classification with Deep CNNs* (Krizhevsky et al., NeurIPS 2012)
- [x] [[notes/seq2seq|seq2seq]] — *Sequence to Sequence Learning* (Sutskever et al., NeurIPS 2014)
- [x] [[notes/bahdanau-attention|Bahdanau Attention]] — *NMT by Jointly Learning to Align and Translate* (ICLR 2015)
- [x] [[notes/vgg|VGG]] — *Very Deep Convolutional Networks* (Simonyan & Zisserman, ICLR 2015)
- [x] [[notes/adam|Adam]] — *A Method for Stochastic Optimization* (Kingma & Ba, ICLR 2015)
- [x] [[notes/batch-norm|Batch Normalization]] (Ioffe & Szegedy, ICML 2015)
- [x] [[notes/resnet|**ResNet**]] — *Deep Residual Learning* (He et al., CVPR 2016)
- [x] [[notes/attention-is-all-you-need|**Attention Is All You Need**]] (Vaswani et al., NeurIPS 2017)
- [x] [[notes/bert|BERT]] (Devlin et al., NAACL 2019)
- [x] [[notes/gpt-3|GPT-3]] — *Language Models are Few-Shot Learners* (Brown et al., NeurIPS 2020)
- [x] [[notes/scaling-laws|Scaling Laws]] (Kaplan et al., 2020) + Chinchilla (Hoffmann et al., 2022)
- [x] [[notes/vit|ViT]] — *An Image is Worth 16x16 Words* (Dosovitskiy et al., ICLR 2021)
- [x] [[notes/mae|MAE]] — *Masked Autoencoders Are Scalable Vision Learners* (He et al., CVPR 2022)
- [x] [[notes/lora|LoRA]] — *Low-Rank Adaptation* (Hu et al., ICLR 2022)
- [x] [[notes/instructgpt|InstructGPT/RLHF]] — *Training LMs to Follow Instructions* (Ouyang et al., NeurIPS 2022)

## 2. Computer Vision

- [ ] U-Net (Ronneberger et al., MICCAI 2015)
- [ ] Faster R-CNN (Ren et al., NeurIPS 2015)
- [ ] YOLO (Redmon et al., CVPR 2016)
- [ ] DETR — *End-to-End Object Detection with Transformers* (Carion et al., ECCV 2020)
- [ ] NeRF (Mildenhall et al., ECCV 2020)
- [ ] Swin Transformer (Liu et al., ICCV 2021)
- [ ] DINO (Caron et al., ICCV 2021) → DINOv2 (Oquab et al., 2023)
- [ ] SAM — *Segment Anything* (Kirillov et al., ICCV 2023)
- [ ] 3D Gaussian Splatting (Kerbl et al., SIGGRAPH 2023)
- [ ] Video understanding — I3D / SlowFast (2017–2019) — 시간적 인식, 로봇 비디오 이해의 기초
- [ ] Depth Anything (Yang et al., CVPR 2024)
- [ ] VGGT — *Visual Geometry Grounded Transformer* (Wang et al., CVPR 2025)

## 3. Vision-Language Models (VLM)

- [x] [[notes/clip|CLIP]] — *Learning Transferable Visual Models From Natural Language Supervision* (Radford et al., ICML 2021)
- [x] [[notes/flamingo|Flamingo]] (Alayrac et al., NeurIPS 2022)
- [x] [[notes/blip-2|BLIP-2]] (Li et al., ICML 2023)
- [x] [[notes/llava|LLaVA]] — *Visual Instruction Tuning* (Liu et al., NeurIPS 2023)
- [ ] Qwen-VL series (2023–) — representative open VLM line
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

- [ ] World Models (Ha & Schmidhuber, NeurIPS 2018)
- [ ] PlaNet (Hafner et al., ICML 2019)
- [ ] Dreamer → DreamerV2 → **DreamerV3** (Hafner et al., 2020–2023)
- [ ] JEPA position paper — *A Path Towards Autonomous Machine Intelligence* (LeCun, 2022)
- [ ] I-JEPA (Assran et al., CVPR 2023) → V-JEPA / V-JEPA 2 (2024–2025)
- [ ] Genie (Bruce et al., ICML 2024) → Genie 2 (2024)
- [ ] Sora technical report — *Video Generation Models as World Simulators* (OpenAI, 2024)
- [ ] NVIDIA Cosmos — world foundation models for physical AI (2025)

## 6. Diffusion & Generative Models

- [x] [[notes/vae|VAE]] — *Auto-Encoding Variational Bayes* (Kingma & Welling, ICLR 2014)
- [x] [[notes/gan|GAN]] (Goodfellow et al., NeurIPS 2014)
- [x] [[notes/ddpm|DDPM]] — *Denoising Diffusion Probabilistic Models* (Ho et al., NeurIPS 2020)
- [x] [[notes/score-sde|Score SDE]] — *Score-Based Generative Modeling through SDEs* (Song et al., ICLR 2021)
- [ ] DDIM (Song et al., ICLR 2021)
- [ ] Classifier-Free Guidance (Ho & Salimans, 2022)
- [ ] Latent Diffusion / Stable Diffusion (Rombach et al., CVPR 2022)
- [ ] ControlNet (Zhang et al., ICCV 2023)
- [ ] DiT — *Scalable Diffusion Models with Transformers* (Peebles & Xie, ICCV 2023)
- [ ] Flow Matching (Lipman et al., ICLR 2023)

## 7. Robotics & Control (textbook + key references)

- [ ] Modern Robotics (Lynch & Park) — chapter notes, not a paper
- [ ] LQR/LQG — classic references via textbook treatment
- [ ] MPC survey — e.g., Mayne et al., *Constrained MPC: Stability and Optimality* (Automatica 2000)
- [ ] MPC in legged robotics — representative paper (e.g., MIT Cheetah convex MPC, IROS 2018)

## 8. Construction Robotics

> To be populated as a separate curation task: start with recent surveys in
> *Automation in Construction* and ISARC proceedings, then branch into
> excavation automation, robotic assembly, site perception, and HRC on site.

- [ ] (survey collection pending)
