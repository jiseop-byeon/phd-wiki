---
title: 2. Computer Vision
tags: [deep-learning, computer-vision, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Translate pixels into classification, detection, segmentation, depth, and 3D outputs while tracking geometry, tensor shapes, supervision, and metrics."
mastery-when: "Raise when visual representation, geometry, or perception evaluation carries the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/foundations/index|1. Learning Systems]], [[02-foundations/signal-processing|6. Signal Processing]], and [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]].

## English

> [!note] First pass
> Read §§1–3 and the task table. Do the problem set before opening the CV paper lineage.

### Running object: D2

**D2** is one grayscale $8\times8$ image. Divide it into non-overlapping $4\times4$ patches: a $2\times2$ grid, hence four patch tokens. Flattening gives 16 values per token; a learned projection $E\in\mathbb R^{16\times d}$ maps each to dimension $d$.

### 1. Two ways to impose visual structure

A convolution with kernel $k\times k$, stride $s$, padding $p$, and input size $n$ produces

$$n_{\text{out}}=\left\lfloor\frac{n+2p-k}{s}\right\rfloor+1.$$

For D2, a $3\times3$ kernel, stride 1, no padding gives $6\times6$. One input and four output channels require $4(3\cdot3+1)=40$ parameters including bias. Weight sharing makes the same detector act at every location.

A Vision Transformer instead makes four patch tokens, adds position information, and lets attention mix them. The inductive bias changes: convolution hard-codes locality and translation sharing; patch attention learns long-range interaction more directly but typically relies more heavily on data and pretraining.

### 2. The output defines the problem

| Task | Output | Typical metric | Metric caveat |
|---|---|---|---|
| classification | one label/distribution per image | top-1 accuracy | hides class imbalance |
| detection | boxes, labels, confidence | mAP over IoU thresholds | depends on matching and thresholds |
| segmentation | label/mask per pixel or object | IoU / mIoU | small classes can disappear in averages |
| monocular depth | depth per pixel | AbsRel, RMSE, $\delta$ | metric scale may be unknown |
| 3D reconstruction | camera/geometry/appearance | pose error, depth, rendering | photorealism is not geometric accuracy |

The architecture name does not define the claim. A backbone can feed several heads; inspect the output representation, loss, and evaluation protocol.

### 3. Geometry survives learning

Cropping, resizing, and augmentation change camera coordinates. A depth network may predict relative depth while a robot needs metres. A segmentation model can have excellent mIoU and still miss a thin cable that determines safety. For robotics, record frame, units, latency, confidence, and how the prediction enters a closed loop.

### 4. Reading the canonical line

Read [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]] and [[01-canonical-papers/notes/1-foundations/resnet|ResNet]] for learned hierarchies and optimization, [[01-canonical-papers/notes/1-foundations/vit|ViT]] for patch tokens, then the detection/segmentation/3D entries in the [[01-canonical-papers/canonical-list|canonical list]]. Ask what supervision and pretraining transfer, not merely which backbone is newer.

### Problem set

1. **Draw.** Draw D2 as pixels, four patches, four tokens, and one class token. Label shapes for $d=8$.
2. **Derive.** Compute output size and parameter count for a $3\times3$, stride-2, padding-1 convolution with 1 input and 8 output channels on D2.
3. **Interpret.** A monocular method halves photometric error but never reports metric depth or pose. Which robotics claim is unsupported?

> [!tip]- Solutions
> 1. Pixels $8\times8$; patches $4\times16$; projected tokens $4\times8$; with class token $5\times8$.
> 2. $\lfloor(8+2-3)/2\rfloor+1=4$, so $4\times4\times8$ output; parameters $8(3\cdot3+1)=80$.
> 3. Metric geometric accuracy—and therefore metric navigation/manipulation utility—has not been established.

### Exit check

Given a vision paper, state its output object, tensor shape, supervision, metric, geometric assumptions, and one failure hidden by the headline number.

## 한국어

> [!note] 처음이라면
> §1–3과 task 표를 읽는다. 과제를 한 뒤에 CV 논문 계보를 연다.

### 계속 쓰는 대상: D2

**D2**는 회색조 $8\times8$ 이미지다. 겹치지 않는 $4\times4$ 패치로 나누면 $2\times2$, 즉 토큰 4개다. 각 패치는 값 16개이고 $E\in\mathbb R^{16\times d}$가 $d$차원으로 투영한다.

### 1. 시각 구조를 넣는 두 방식

convolution의 출력 크기는 $n_{out}=\lfloor(n+2p-k)/s\rfloor+1$이다. D2에 $3\times3$, stride 1, padding 0이면 $6\times6$. 출력 channel 4개면 bias 포함 parameter는 $4(9+1)=40$개다. ViT는 패치 토큰과 위치 정보를 사용한다. convolution은 locality와 weight sharing을 강하게 넣고, attention은 먼 위치의 상호작용을 더 직접 학습한다.

### 2. 출력이 문제를 정의한다

| 과제 | 출력 | 대표 metric | 주의 |
|---|---|---|---|
| 분류 | 이미지당 label/분포 | top-1 accuracy | 클래스 불균형을 숨김 |
| 검출 | box, label, confidence | IoU 임계값 위의 mAP | matching과 임계값에 의존 |
| 분할 | pixel 또는 object mask | IoU / mIoU | 작은 클래스가 평균에서 사라질 수 있음 |
| 단안 depth | pixel당 깊이 | AbsRel, RMSE, $\delta$ | metric scale이 없을 수 있음 |
| 3D 복원 | camera/geometry/appearance | pose 오차, depth, rendering | photorealism은 기하 정확도가 아님 |

backbone 이름보다 출력 표현·loss·평가 protocol을 먼저 본다.

### 3. 학습 뒤에도 기하는 남는다

crop·resize·augmentation은 카메라 좌표를 바꾼다. 상대 depth는 metre가 아닐 수 있다. 높은 mIoU도 안전을 결정하는 얇은 cable을 놓칠 수 있다. 로봇에서는 frame·unit·latency·confidence와 폐루프 연결을 기록한다.

### 4. 계보 읽기

AlexNet·ResNet에서 표현과 최적화, ViT에서 patch token을 읽고 canonical list의 검출·분할·3D로 간다. 새 backbone 이름보다 어떤 supervision과 pretraining이 전이되는지 묻는다.

### 과제

1. $d=8$인 D2의 pixel→patch→token→class token shape를 그린다.
2. $3\times3$, stride 2, padding 1, 출력 channel 8개의 크기와 parameter 수를 구한다.
3. photometric error만 낮춘 monocular 방법이 증명하지 못한 로보틱스 주장은 무엇인가.

> [!tip]- 정답
> 1. $8\times8\rightarrow4\times16\rightarrow4\times8\rightarrow5\times8$.
> 2. 출력 $4\times4\times8$, parameter 80개.
> 3. metric 기하 정확도와 metric 작업 유용성.

### 통과 기준

CV 논문의 출력 대상·shape·supervision·metric·기하 가정과 headline 수치가 숨기는 실패 하나를 말할 수 있다.
