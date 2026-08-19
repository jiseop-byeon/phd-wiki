---
title: 3.5 Geometric Perception & Calibration
tags: [robotics, perception, calibration, geometry]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

[[02-foundations/se3-geometry|SE(3)]] is the language for *writing down* poses; geometric
perception is how a robot *obtains* them — how pixels, depths, and point clouds become
3D structure expressed in the right coordinate frame. Deep perception
([[03-deep-learning/index|Deep Learning]]) tells you *what* something is; geometric
perception tells you *where* it is, at *what scale*, in *which frame*.

> [!info] Depth target
> Read pose-estimation, visual-odometry/SLAM-front-end, calibration, and point-cloud
> papers without stalling on projection, intrinsics/extrinsics, registration, or
> reprojection error. Deriving multiview geometry (essential/fundamental matrices,
> bundle adjustment) is a working/mastery topic.

> [!note] Prerequisites
> [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/se3-geometry|3D Geometry & SE(3)]] · [[02-foundations/optimization|Optimization]] (least squares)

### 1. The pinhole camera model

A 3D point $p^{c}=(X,Y,Z)$ in the **camera frame** projects to pixel $(u,v)$:

$$u = f_x\frac{X}{Z}+c_x, \qquad v = f_y\frac{Y}{Z}+c_y$$

- **Intrinsics** $(f_x, f_y, c_x, c_y$, distortion$)$: properties of the camera itself —
  focal lengths in pixels and the principal point. Fixed once calibrated (until the lens
  is touched).
- **Extrinsics** $(R, t)$: the camera's pose relative to another frame (robot base,
  world) — the [[02-foundations/se3-geometry|SE(3)]] transform that moves points into the
  camera frame before projection.
- Division by $Z$ is the whole story of perspective: farther points move less in the
  image, and **absolute scale is lost** — a single image cannot tell a large-far object
  from a small-near one.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="pinhole projection: a small near object and a large far one land on the same pixels">
  <g stroke="currentColor" stroke-width="1.3"><line x1="150" y1="25" x2="150" y2="170"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="4 3"><line x1="60" y1="110.0" x2="440" y2="110.0"/></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <line x1="60" y1="110" x2="440" y2="26.4"/><line x1="60" y1="110" x2="440" y2="72.0"/>
  </g>
  <g stroke="currentColor" stroke-width="3.2">
    <line x1="150" y1="90.2" x2="150" y2="101.0"/>
    <line x1="250" y1="68.2" x2="250" y2="91.0"/>
    <line x1="420" y1="30.8" x2="420" y2="74.0"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="110" r="3.5"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="114">O</text>
    <text x="112" y="20">image plane</text>
    <text x="212" y="110">small and near</text>
    <text x="372" y="92">large and far</text>
    <text x="158" y="128">the same image on the sensor</text>
    <text x="25" y="192" opacity="0.85">u = f X / Z + c &#8212; dividing by Z is exactly what destroys absolute scale</text>
  </g>
</svg>



**Worked projection**: $f_x=f_y=600$ px, $(c_x,c_y)=(320,240)$, point
$p^{c}=(0.5, 0.2, 2.0)$ m. Then $u = 600\cdot 0.5/2.0+320=470$,
$v = 600\cdot 0.2/2.0+240=300$. Move the point twice as far
($Z=4$): $u=395, v=270$ — it slides toward the principal point.

### 2. Recovering depth

| Source | How depth appears | Main caution |
|---|---|---|
| Stereo | disparity $d$ between two views: $Z = f\,b/d$ (baseline $b$) | textureless/repetitive surfaces; error grows as $Z^2$ |
| RGB-D / ToF / structured light | sensor measures $Z$ per pixel | range limits, sunlight, reflective/dark materials |
| LiDAR | direct time-of-flight ranges | sparsity, motion distortion, weather |
| Learned monocular depth | network predicts $Z$ (often up to scale) | scale ambiguity; distribution shift — check the [[01-canonical-papers/notes/2-computer-vision/depth-anything\|Depth Anything]] claim scope |
| Triangulation | intersect rays from two known poses | needs baseline; degenerate for distant points and small baselines |

**Stereo worked example**: $f=600$ px, baseline $b=0.12$ m, disparity $d=9$ px
→ $Z = 600\cdot 0.12/9 = 8$ m. One pixel of disparity error ($d=8$) gives $Z=9$ m —
a 12.5% jump at this range: depth error grows quadratically with distance.



<svg viewBox="0 0 620 246" style="max-width:100%;height:auto" role="img" aria-label="stereo: a near point splays the two rays, a far point makes them nearly parallel">
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="60" y1="190" x2="60" y2="172"/><line x1="140" y1="190" x2="140" y2="172"/>
    <line x1="360" y1="190" x2="360" y2="172"/><line x1="440" y1="190" x2="440" y2="172"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" opacity="0.8" fill="none">
    <line x1="60" y1="190" x2="100" y2="140"/><line x1="140" y1="190" x2="100" y2="140"/>
    <line x1="360" y1="190" x2="400" y2="70"/><line x1="440" y1="190" x2="400" y2="70"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="3.5"/><circle cx="140" cy="190" r="3.5"/>
    <circle cx="360" cy="190" r="3.5"/><circle cx="440" cy="190" r="3.5"/>
    <circle cx="100" cy="140" r="4.5"/><circle cx="400" cy="70" r="4.5"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="3 3">
    <line x1="60" y1="202" x2="140" y2="202"/><line x1="360" y1="202" x2="440" y2="202"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="30">NEAR</text><text x="400" y="30">FAR</text>
    <text x="100" y="48" font-size="10.5" opacity="0.85">Z = 2 m &#183; disparity 36 px</text>
    <text x="400" y="48" font-size="10.5" opacity="0.85">Z = 8 m &#183; disparity 9 px</text>
    <text x="100" y="218" font-size="10.5">baseline b</text><text x="400" y="218" font-size="10.5">baseline b</text>
  </g>
  <g font-size="11" fill="currentColor"><text x="30" y="240" opacity="0.9">Disparity is that angle &#8212; and a far point squeezes it toward zero.</text></g>
</svg>



### 3. Point clouds and frames

A depth image plus intrinsics back-projects to a **point cloud**:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. Every cloud lives in some frame — sensor, base,
map — and multi-sensor pipelines stand or fall on the **extrinsic calibration** between
those frames ([[04-robotics/robot-systems-deployment|the TF tree at runtime]]). A
plausible-looking cloud in the wrong frame produces systematic, learning-resistant errors.

### 4. Registration and ICP

**Registration** aligns two geometries (cloud-to-cloud, cloud-to-model, scan-to-BIM):
find $T \in SE(3)$ minimizing distances between corresponding points. **ICP** (iterative
closest point) alternates: (1) match each point to its nearest neighbor, (2) solve the
least-squares $T$ for those matches, (3) repeat.

- ICP is **local**: it converges to the nearest basin, so it needs a decent initial guess
  (odometry, a global feature match, or a human).
- **Degeneracies**: a flat wall slides along itself; a corridor slides lengthwise;
  symmetric objects flip. Papers reporting registration accuracy should say how initial
  poses were chosen and whether degenerate scenes were included.

### 5. Calibration

| Calibration | What it estimates | Typical method |
|---|---|---|
| Intrinsic | $f_x,f_y,c_x,c_y$, distortion | checkerboard/target views |
| Camera–camera (stereo) | relative $SE(3)$ + rectification | shared target views |
| Camera–LiDAR | extrinsic $SE(3)$ | target or mutual-feature alignment |
| Hand–eye (camera–robot) | sensor-to-end-effector or base transform | robot motion + target ($AX=XB$) |
| Temporal | clock offset / latency between sensors | correlation of motion signals |

The quality metric is usually **reprojection error**: project the estimated 3D points
through the estimated model and measure pixel distance to their detections. Low
reprojection error on the calibration set does **not** guarantee accuracy outside the
calibrated volume, range, or temperature.

### 6. Geometric + deep perception

Modern pipelines mix the two: a network detects or segments
([[01-canonical-papers/notes/2-computer-vision/sam|SAM]]), matches features, or predicts
depth/pose; geometry turns those into metric structure and enforces consistency
(triangulation, [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]-style feed-forward
geometry, [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3DGS]] rendering losses).
When reading, ask: *which stage is learned, which is geometric, and where does metric
scale enter?* (calibrated stereo/LiDAR, known object size, or not at all).

### 7. Reading claims and evaluations

| Paper phrase | Check before accepting it |
|---|---|
| "accurate 6-DoF pose" | error metric (ADD? rotation/translation split?), object symmetry handling, occlusion levels |
| "metric depth" | where scale comes from; evaluation range; indoor-vs-outdoor shift |
| "robust registration" | initialization protocol, degenerate-scene fraction, outlier rates |
| "calibration-free" | what is actually assumed (often: intrinsics still known) |
| "real-time reconstruction" | hardware, resolution, drift over long sequences |

> [!warning] Reading the claim
> Sub-pixel reprojection error and beautiful reconstructions do not by themselves mean
> the *pose is right in the robot's base frame* — that also requires correct extrinsics
> and time synchronization, which many papers hold fixed and out of scope.

### After reading

- Project a 3D point through a pinhole model by hand.
- Distinguish intrinsics from extrinsics and say when each changes.
- Explain why monocular vision loses scale and where scale re-enters.
- Explain ICP's loop and why it needs initialization.
- Name the calibrations a camera+LiDAR+arm system needs.
- Interpret reprojection error without over-trusting it.

### Self-check

1. With the worked intrinsics, where does $p^{c}=(-0.3, 0.1, 1.5)$ project?
2. Stereo at $f=600$, $b=0.12$: what disparity corresponds to $Z=24$ m, and why is that a problem?
3. Why can ICP fail in a long empty corridor even with perfect data?
4. A paper fuses LiDAR and camera "without calibration" — what is it most likely still assuming?

> [!tip]- Answers
> 1. $u = 600(-0.3)/1.5+320 = 200$, $v = 600(0.1)/1.5+240 = 280$.
> 2. $d = fb/Z = 600\cdot0.12/24 = 3$ px — a ±1 px error spans 18–36 m; long-range stereo depth is fragile.
> 3. Translation along the corridor axis barely changes point-to-nearest-point distances — a degenerate (unobservable) direction.
> 4. Known intrinsics, and usually a rough extrinsic initialization or joint optimization that still needs overlap and synchronized timestamps.

### Sources

- [Szeliski, *Computer Vision: Algorithms and Applications* (free official PDF)](https://szeliski.org/Book/)
- [OpenCV camera calibration tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [KITTI sensor setup — a real calibrated multi-sensor rig](https://www.cvlibs.net/datasets/kitti/setup.php)

## 한국어

[[02-foundations/se3-geometry|SE(3)]]가 pose를 *적는* 언어라면, 기하학적 인식은 로봇이
pose를 *얻는* 방법이다 — 픽셀, 깊이, 포인트 클라우드가 올바른 좌표계의 3D 구조가 되는
과정. 딥 인식([[03-deep-learning/index|딥러닝]])이 무엇*인지*를 알려준다면, 기하학적
인식은 그것이 *어디에*, *어떤 스케일로*, *어느 프레임에* 있는지를 알려준다.

> [!info] 깊이 목표
> Pose 추정, visual odometry/SLAM front end, 보정, 포인트 클라우드 논문을 projection,
> intrinsics/extrinsics, registration, reprojection error에서 막히지 않고 읽는다.
> 다시점 기하의 유도(essential/fundamental matrix, bundle adjustment)는 실무/숙달
> 단계의 주제다.

> [!note] 선수 지식
> [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/se3-geometry|3D 기하와 SE(3)]] · [[02-foundations/optimization|최적화]] (최소제곱)

### 1. 핀홀 카메라 모델

**카메라 프레임**의 3D 점 $p^{c}=(X,Y,Z)$는 픽셀 $(u,v)$로 투영된다:

$$u = f_x\frac{X}{Z}+c_x, \qquad v = f_y\frac{Y}{Z}+c_y$$

- **Intrinsics** $(f_x, f_y, c_x, c_y$, 왜곡$)$: 카메라 자체의 성질 — 픽셀 단위 초점
  거리와 주점. 한 번 보정하면 (렌즈를 건드리기 전까지) 고정.
- **Extrinsics** $(R, t)$: 다른 프레임(로봇 베이스, 월드)에 대한 카메라의 pose —
  투영 전에 점을 카메라 프레임으로 옮기는 [[02-foundations/se3-geometry|SE(3)]] 변환.
- $Z$로 나누는 것이 원근의 전부다: 먼 점일수록 이미지에서 덜 움직이고, **절대
  스케일이 사라진다** — 이미지 한 장으로는 크고 먼 물체와 작고 가까운 물체를 구분할
  수 없다.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="핀홀 투영: 작고 가까운 물체와 크고 먼 물체가 같은 픽셀에 맺힌다">
  <g stroke="currentColor" stroke-width="1.3"><line x1="150" y1="25" x2="150" y2="170"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="4 3"><line x1="60" y1="110.0" x2="440" y2="110.0"/></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <line x1="60" y1="110" x2="440" y2="26.4"/><line x1="60" y1="110" x2="440" y2="72.0"/>
  </g>
  <g stroke="currentColor" stroke-width="3.2">
    <line x1="150" y1="90.2" x2="150" y2="101.0"/>
    <line x1="250" y1="68.2" x2="250" y2="91.0"/>
    <line x1="420" y1="30.8" x2="420" y2="74.0"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="110" r="3.5"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="114">O</text>
    <text x="112" y="20">이미지 평면</text>
    <text x="212" y="110">작고 가깝다</text>
    <text x="372" y="92">크고 멀다</text>
    <text x="158" y="128">센서 위에서는 같은 상</text>
    <text x="25" y="192" opacity="0.85">u = f X / Z + c &#8212; Z로 나누는 그 한 번이 절대 스케일을 지운다</text>
  </g>
</svg>



**투영 계산 예제**: $f_x=f_y=600$ px, $(c_x,c_y)=(320,240)$, 점
$p^{c}=(0.5, 0.2, 2.0)$ m이면 $u = 600\cdot 0.5/2.0+320=470$,
$v = 600\cdot 0.2/2.0+240=300$. 점을 두 배 멀리 보내면($Z=4$): $u=395, v=270$ —
주점 쪽으로 미끄러진다.

### 2. 깊이 복원

| 방법 | 깊이가 나타나는 방식 | 주된 주의점 |
|---|---|---|
| 스테레오 | 두 시점 간 시차 $d$: $Z = f\,b/d$ (기선 $b$) | 무늬 없는/반복 표면; 오차가 $Z^2$로 증가 |
| RGB-D / ToF / 구조광 | 센서가 픽셀별 $Z$ 측정 | 거리 한계, 햇빛, 반사/어두운 재질 |
| LiDAR | 직접 time-of-flight 거리 | 희소성, 운동 왜곡, 날씨 |
| 학습된 단안 깊이 | 네트워크가 $Z$ 예측 (대개 스케일 모호) | 스케일 모호성; 분포 이동 — [[01-canonical-papers/notes/2-computer-vision/depth-anything\|Depth Anything]]의 주장 범위 확인 |
| 삼각측량 | 알려진 두 pose에서 광선 교차 | 기선 필요; 먼 점·짧은 기선에서 퇴화 |

**스테레오 계산 예제**: $f=600$ px, 기선 $b=0.12$ m, 시차 $d=9$ px
→ $Z = 600\cdot 0.12/9 = 8$ m. 시차 1픽셀 오차($d=8$)면 $Z=9$ m — 이 거리에서 12.5%
튄다: 깊이 오차는 거리에 제곱으로 자란다.

<svg viewBox="0 0 620 246" style="max-width:100%;height:auto" role="img" aria-label="스테레오: 가까운 점은 두 광선을 크게 벌리고, 먼 점은 거의 나란하게 만든다">
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="60" y1="190" x2="60" y2="172"/><line x1="140" y1="190" x2="140" y2="172"/>
    <line x1="360" y1="190" x2="360" y2="172"/><line x1="440" y1="190" x2="440" y2="172"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" opacity="0.8" fill="none">
    <line x1="60" y1="190" x2="100" y2="140"/><line x1="140" y1="190" x2="100" y2="140"/>
    <line x1="360" y1="190" x2="400" y2="70"/><line x1="440" y1="190" x2="400" y2="70"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="3.5"/><circle cx="140" cy="190" r="3.5"/>
    <circle cx="360" cy="190" r="3.5"/><circle cx="440" cy="190" r="3.5"/>
    <circle cx="100" cy="140" r="4.5"/><circle cx="400" cy="70" r="4.5"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="3 3">
    <line x1="60" y1="202" x2="140" y2="202"/><line x1="360" y1="202" x2="440" y2="202"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="30">가깝다</text><text x="400" y="30">멀다</text>
    <text x="100" y="48" font-size="10.5" opacity="0.85">Z = 2 m &#183; 시차 36 px</text>
    <text x="400" y="48" font-size="10.5" opacity="0.85">Z = 8 m &#183; 시차 9 px</text>
    <text x="100" y="218" font-size="10.5">베이스라인 b</text><text x="400" y="218" font-size="10.5">베이스라인 b</text>
  </g>
  <g font-size="11" fill="currentColor"><text x="30" y="240" opacity="0.9">시차가 곧 그 각도다 &#8212; 그리고 먼 점은 그 각도를 0 쪽으로 눌러버린다.</text></g>
</svg>



### 3. 포인트 클라우드와 프레임

깊이 이미지 + intrinsics를 역투영하면 **포인트 클라우드**가 된다:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. 모든 클라우드는 어떤 프레임(센서·베이스·맵)에
산다 — 다중 센서 파이프라인은 그 프레임들 사이의 **extrinsic 보정**에 성패가 달려 있다
([[04-robotics/robot-systems-deployment|런타임에서는 TF 트리]]). 그럴듯해 보여도 틀린
프레임의 클라우드는 학습으로 잘 고쳐지지 않는 계통 오차를 만든다.

### 4. Registration과 ICP

**Registration**은 두 기하(클라우드-클라우드, 클라우드-모델, 스캔-BIM)를 정렬한다:
대응점 사이 거리를 최소화하는 $T \in SE(3)$를 찾는다. **ICP**(iterative closest
point)는 반복한다: (1) 각 점을 최근접 이웃과 짝짓고, (2) 그 짝에 대한 최소제곱 $T$를
풀고, (3) 반복.

- ICP는 **국소적**이다: 가장 가까운 골짜기로 수렴하므로 괜찮은 초기 추정(odometry,
  전역 특징 매칭, 사람)이 필요하다.
- **퇴화**: 평평한 벽은 스스로를 따라 미끄러지고, 복도는 길이 방향으로 미끄러지고,
  대칭 물체는 뒤집힌다. Registration 정확도를 보고하는 논문은 초기 pose를 어떻게
  골랐고 퇴화 장면이 포함됐는지 말해야 한다.

### 5. 보정

| 보정 | 추정 대상 | 전형적 방법 |
|---|---|---|
| Intrinsic | $f_x,f_y,c_x,c_y$, 왜곡 | 체커보드/타깃 촬영 |
| 카메라–카메라 (스테레오) | 상대 $SE(3)$ + 정렬(rectification) | 공유 타깃 촬영 |
| 카메라–LiDAR | extrinsic $SE(3)$ | 타깃 또는 상호 특징 정렬 |
| Hand–eye (카메라–로봇) | 센서–말단 또는 베이스 변환 | 로봇 운동 + 타깃 ($AX=XB$) |
| 시간 | 센서 간 클럭 오프셋/지연 | 운동 신호의 상관 |

품질 지표는 대개 **reprojection error**다: 추정된 3D 점을 추정된 모델로 투영해 검출
위치와의 픽셀 거리를 잰다. 보정 세트에서 낮은 reprojection error가 보정된 부피·거리·
온도 밖에서의 정확도를 보장하지는 **않는다**.

### 6. 기하학적 인식 + 딥 인식

현대 파이프라인은 둘을 섞는다: 네트워크가 검출·분할
([[01-canonical-papers/notes/2-computer-vision/sam|SAM]])하거나, 특징을 매칭하거나,
깊이/pose를 예측하고; 기하가 그것을 미터법 구조로 바꾸고 일관성을 강제한다
(삼각측량, [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]식 feed-forward 기하,
[[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3DGS]] 렌더링 손실).
읽을 때 물어라: *어느 단계가 학습이고 어느 단계가 기하이며, 미터 스케일은 어디서
들어오는가?* (보정된 스테레오/LiDAR, 알려진 물체 크기, 또는 아예 없음).

### 7. 주장과 평가 읽기

| 논문 표현 | 받아들이기 전에 확인할 것 |
|---|---|
| "accurate 6-DoF pose" | 오차 지표(ADD? 회전/병진 분리?), 대칭 처리, 가림 수준 |
| "metric depth" | 스케일의 출처; 평가 거리 범위; 실내-실외 이동 |
| "robust registration" | 초기화 프로토콜, 퇴화 장면 비율, outlier 비율 |
| "calibration-free" | 실제로 가정하는 것 (대개: intrinsics는 여전히 앎) |
| "real-time reconstruction" | 하드웨어, 해상도, 긴 시퀀스에서의 drift |

> [!warning] 주장 읽는 법 · Reading the claim
> 서브픽셀 reprojection error와 아름다운 복원이 그 자체로 *로봇 베이스 프레임에서
> pose가 맞다*는 뜻은 아니다 — 그러려면 올바른 extrinsics와 시간 동기화도 필요한데,
> 많은 논문이 이를 고정된 범위 밖 가정으로 둔다.

### 읽고 나면 말할 수 있어야 하는 것

- 핀홀 모델로 3D 점을 손으로 투영할 수 있다
- intrinsics와 extrinsics를 구분하고 각각 언제 바뀌는지 말할 수 있다
- 단안 비전이 스케일을 잃는 이유와 스케일이 다시 들어오는 지점을 설명할 수 있다
- ICP의 루프와 초기화가 필요한 이유를 설명할 수 있다
- 카메라+LiDAR+로봇팔 시스템에 필요한 보정들을 나열할 수 있다
- reprojection error를 과신하지 않고 해석할 수 있다

### 스스로 점검

1. 위의 intrinsics로 $p^{c}=(-0.3, 0.1, 1.5)$는 어디에 투영되는가?
2. $f=600$, $b=0.12$의 스테레오에서 $Z=24$ m에 해당하는 시차는? 그것이 왜 문제인가?
3. 데이터가 완벽해도 길고 빈 복도에서 ICP가 실패할 수 있는 이유는?
4. "보정 없이" LiDAR와 카메라를 융합한다는 논문이 여전히 가정하고 있을 가능성이 큰 것은?

> [!tip]- 정답 · Answers
> 1. $u = 600(-0.3)/1.5+320 = 200$, $v = 600(0.1)/1.5+240 = 280$.
> 2. $d = fb/Z = 600\cdot0.12/24 = 3$ px — ±1 px 오차가 18–36 m를 오간다; 원거리 스테레오 깊이는 취약하다.
> 3. 복도 축 방향의 병진은 점-최근접점 거리를 거의 바꾸지 않는다 — 퇴화된(관측 불가능한) 방향.
> 4. 알려진 intrinsics, 그리고 대개 대략적인 extrinsic 초기화 또는 겹침과 동기화된 타임스탬프를 여전히 요구하는 공동 최적화.

### 출처

- [Szeliski, *Computer Vision: Algorithms and Applications* (공식 무료 PDF)](https://szeliski.org/Book/)
- [OpenCV 카메라 보정 튜토리얼](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [KITTI 센서 구성 — 실제 보정된 다중 센서 리그](https://www.cvlibs.net/datasets/kitti/setup.php)
