---
title: "GelSight — High-Resolution Robot Tactile Sensors for Estimating Geometry and Force"
authors: Wenzhen Yuan, Siyuan Dong, Edward H. Adelson
affiliation: MIT
venue: Sensors (MDPI)
year: 2017
doi: https://doi.org/10.3390/s17122762
tags: [paper, manipulation, tactile]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only if tactile sensing itself becomes the contribution — which the research program excludes."
---

**Yuan, Dong & Adelson, *Sensors*, vol. 17, no. 12, art. 2762, 2017** — [DOI](https://doi.org/10.3390/s17122762). The optical principle originates in M. K. Johnson and E. H. Adelson, "Retrographic sensing for the measurement of surface texture and shape," CVPR 2009, pp. 1070–1077.

> [!note] Math on-ramp · 수학 준비물
> Photometric stereo is the one idea to have: illuminate a surface from several known directions and infer its shape from how brightness varies. That is a computer-vision technique being used as a *touch* sensor, which is the whole trick — see [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]] for the imaging background.
> 광도 스테레오(photometric stereo) 하나만 알면 된다: 표면을 알려진 여러 방향에서 비추고 밝기가 어떻게 변하는지로 형상을 추론한다. 컴퓨터 비전 기법이 *촉각* 센서로 쓰이는 것이고 그것이 요령 전부다 — 영상 배경은 [[04-robotics/geometric-perception-calibration|3.5 기하 인식]].

## English

**One-line summary**: Put a camera behind a deformable elastomer with a reflective skin, and read the skin's deformed shape photometrically — a tactile sensor that measures *geometry* at high spatial resolution, with force inferred from the deformation.

### Context

Traditional tactile sensors measure force at a small number of points. That gives you *how hard* but almost nothing about *what shape* is pressing, and the shape is what tells you whether a part is seated, which edge is in contact, or where a screw thread sits.

### Method

> [!tip] Key intuition
> Turn touch into vision. If the contact deforms a surface you can see, then a camera is a tactile sensor with megapixel resolution — and all the machinery of computer vision becomes available to a problem that used to be electrical.

An elastomer slab with a reflective membrane takes on the shape of whatever is pressed into it; RGB illumination from several directions plus photometric stereo converts the membrane's appearance into a surface reconstruction. Lateral deformation of the gel gives shear and slip information on top of the normal shape.

### Results

> [!warning] Reading the claims · 주장 읽는 법
> **The abstract contains no numbers.** Its strongest statement is qualitative: the sensor measures geometry "with very high spatial resolution", in contrast to traditional tactile sensors that measure contact force. Every micron figure and sensing-area dimension quoted for GelSight comes from the body or from secondary sources — check there before citing one.
> **초록에 숫자가 하나도 없다.** 가장 강한 진술이 정성적이다: 접촉력을 재는 전통적 촉각 센서와 달리 이 센서는 "매우 높은 공간 해상도로" 기하를 잰다. GelSight에 대해 인용되는 마이크론 수치와 감지 면적은 전부 본문이나 2차 출처에서 온 것이다.

### Limitations & critique

- **It measures geometry; force is inferred.** This is the sentence to carry into every paper that uses one ([[04-robotics/tactile-visuotactile|14. §2]]) — a force claim built on a GelSight is a claim about an inference, not a transduction.
- **Camera rate is the ceiling.** A hard contact transition ends in a millisecond or two ([[04-robotics/force-compliance-control|13. §5]]), so this sensor informs the next decision rather than regulating the impact.
- The gel abrades and must be replaced, which matters for any long experiment and for a dusty site.
- Bulk: putting a camera and its optical path behind the fingertip constrains gripper design.

### Connections

- [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing]] — the concept page
- [[01-canonical-papers/notes/7-robotics/vision-and-touch|Making Sense of Vision and Touch]] — using tactile data in a policy

### After reading

- [ ] Say what a GelSight physically measures and what is inferred.
- [ ] Explain the latency consequence in one sentence.
- [ ] State where any GelSight resolution number you quote came from.

## 한국어

**한 줄 요약**: 반사막을 입힌 변형 엘라스토머 뒤에 카메라를 두고 막의 변형된 형상을 광도적으로 읽는다 — 높은 공간 해상도로 *기하*를 재고 힘은 변형에서 추론하는 촉각 센서.

### 배경

전통적 촉각 센서는 적은 수의 점에서 힘을 잰다. 그러면 *얼마나 세게*는 알 수 있지만 *어떤 형상*이 누르고 있는지는 거의 알 수 없고, 부재가 안착했는지, 어느 모서리가 닿았는지, 나사산이 어디 있는지를 말해 주는 것이 바로 그 형상이다.

### 방법

> [!tip] 핵심 직관
> 촉각을 비전으로 바꿔라. 접촉이 눈으로 볼 수 있는 표면을 변형시킨다면, 카메라가 메가픽셀 해상도의 촉각 센서가 된다 — 그리고 예전에는 전기의 문제였던 것에 컴퓨터 비전의 도구 전부가 쓸 수 있게 된다.

반사막을 입힌 엘라스토머 판이 눌린 대상의 형상을 그대로 받는다. 여러 방향의 RGB 조명과 광도 스테레오가 막의 겉모습을 표면 복원으로 바꾼다. 젤의 횡방향 변형이 법선 형상 위에 전단과 미끄러짐 정보를 더한다.

### 결과

> [!warning] 주장 읽는 법 · Reading the claim
> **초록에 숫자가 하나도 없다.** 가장 강한 진술이 정성적이다: 접촉력을 재는 전통적 촉각 센서와 달리 이 센서는 "매우 높은 공간 해상도로" 기하를 잰다. 인용되는 마이크론 수치와 감지 면적은 전부 본문이나 2차 출처에서 온 것이니, 인용 전에 거기서 확인하라.
> **The abstract contains no numbers** — every resolution figure quoted for GelSight is body-only or secondary.

### 한계와 비판

- **기하를 재고 힘은 추론한다.** 이 문장을 GelSight를 쓰는 모든 논문에 가지고 들어가야 한다([[04-robotics/tactile-visuotactile|14. §2]]) — GelSight 위에 세운 힘 주장은 변환이 아니라 추론에 관한 주장이다.
- **카메라 주기가 천장이다.** 단단한 접촉 천이는 1~2 밀리초에 끝나므로([[04-robotics/force-compliance-control|13. §5]]), 이 센서는 충격을 조절하는 것이 아니라 다음 결정에 정보를 준다.
- 젤이 마모되어 교체해야 한다. 긴 실험과 먼지 많은 현장에서 문제가 된다.
- 부피: 손끝 뒤에 카메라와 광학 경로를 두는 것이 그리퍼 설계를 제약한다.

### 연결

- [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱]] — 개념 페이지
- [[01-canonical-papers/notes/7-robotics/vision-and-touch|Making Sense of Vision and Touch]] — 촉각 데이터를 정책에 쓰는 법

### 읽고 나면 말할 수 있어야 하는 것

- [ ] GelSight가 물리적으로 무엇을 재고 무엇이 추론되는지 말한다.
- [ ] 지연이 낳는 귀결을 한 문장으로 설명한다.
- [ ] 인용하는 GelSight 해상도 수치가 어디서 왔는지 말한다.
