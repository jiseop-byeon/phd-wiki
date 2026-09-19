---
title: 3.5 Geometric Perception & Calibration
tags: [robotics, perception, calibration, geometry]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

## English

*Group B. Stands on [[02-foundations/linear-algebra|linear algebra]], optimization and [[02-foundations/se3-geometry|SE(3)]]. This is how pixels and point clouds
become 3D in the right frame — every perception claim in groups H and J passes through here.*

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

> [!note] First pass · 처음이라면
> Read §1 (the pinhole model, with the projection written out), §5 (calibration — where most field failures actually start), §7. §2 to §4 are the machinery; read them when a paper's numbers depend on them.

### 1. The pinhole camera model

A 3D point $p^{c}=(X,Y,Z)$ in the **camera frame** projects to pixel $(u,v)$:

$$u = f_x\frac{X}{Z}+c_x, \qquad v = f_y\frac{Y}{Z}+c_y$$

**Where that comes from — similar triangles, and nothing else.** Put the optical centre at
the origin and the image plane at distance $f$ in front of it. The ray from the 3D point
$(X, Y, Z)$ to the centre crosses that plane at height $y$, and the two triangles it forms —
one from the centre to the plane, one from the centre to the point — are similar. So
$y/f = Y/Z$, giving $y = fY/Z$. The rest is bookkeeping: divide by the physical pixel pitch
to get pixels (which is why $f_x$ and $f_y$ differ when pixels are not square, and why focal
length is quoted *in pixels* rather than millimetres), then add $c_x, c_y$ to move the origin
from the optical axis to the image corner, where array indices start.

That is the whole model, and its shape carries the two facts everything downstream inherits.
The map is **not linear** — $Z$ sits in the denominator, which is why perspective needs
homogeneous coordinates before it can be a matrix at all — and it is **not invertible**,
since every point along one ray produces the same $(u,v)$. Recovering $Z$ is therefore not a
matter of a better camera; it needs a second constraint, which is what §2 is about.

- **Intrinsics** $(f_x, f_y, c_x, c_y$, distortion$)$: properties of the camera itself —
  focal lengths in pixels and the principal point. Fixed once calibrated (until the lens
  is touched).
- **Extrinsics** $(R, t)$: the [[02-foundations/se3-geometry|SE(3)]] transform $T_{cw}$ that moves points from another frame (robot base,
  world) into the camera frame before projection, $p^c = Rp^w + t$. The camera's *pose* in that frame is its inverse, $T_{wc}$, with the camera centre at $-R^\top t$: the centre is the point with $p^c=0$, so $0=Rp^w+t$ gives $p^w=-R^\top t$ (using $R^{-1}=R^\top$). Check which one a calibration file stores.
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
| Learned monocular depth | network predicts $Z$ (often only up to an unknown scale and shift, frequently in inverse depth $1/Z$, which stays bounded as points recede toward the far background) | scale ambiguity; distribution shift — check the [[01-canonical-papers/notes/2-computer-vision/depth-anything\|Depth Anything]] claim scope |
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
  <g font-size="11" fill="currentColor"><text x="30" y="240" opacity="0.9">Disparity is horizontal pixel displacement; it shrinks with the triangulation angle for far points.</text></g>
</svg>



### 2.5 Image features: detect, describe, match

**The idea in one sentence:** pick a few hundred points that can be found again in another image, give each a compact fingerprint, and pair fingerprints across images — those pairs are the correspondences every geometric step needs.

Why sparse points instead of every pixel? Stereo depth in §2 needs to know which right-image pixel shows the same point as a left-image pixel. Calibration in §5 needs target corners located to sub-pixel accuracy. Visual odometry and SLAM ([[04-robotics/state-estimation-slam|state estimation]]) track the same points across frames to constrain pose. A point is useful only if it is **repeatable** (detected again after the view changes) and **distinctive** (its neighbourhood does not resemble many others). The pipeline has three stages, and a paper can change any one of them.

**Detect: where the image changes in every direction.** Shift a small window by $(u,v)$ and measure how much its content changes. A first-order Taylor step gives $I(x+u,y+v)\approx I(x,y)+I_x u+I_y v$, so each pixel's difference is $I_x u+I_y v$ and its square $I_x^2u^2+2I_xI_y\,uv+I_y^2v^2$ is quadratic in $(u,v)$. Summing over the window therefore turns the change into a quadratic form:

$$E(u,v)=\sum_{x,y} w(x,y)\,\big(I(x+u,y+v)-I(x,y)\big)^2 \approx (u,v)\,M\,(u,v)^\top$$

so the whole behaviour is governed by one 2×2 matrix, the **structure tensor**. It sums the image gradients $I_x, I_y$ over the window with weights $w$ (a box or a Gaussian):

$$M=\sum_{x,y} w(x,y)\begin{pmatrix}I_x^2 & I_xI_y\\ I_xI_y & I_y^2\end{pmatrix}$$

Its eigenvalues $\lambda_1 \le \lambda_2$ are the change along the least- and most-varying shift directions, so they classify the window:

- **Flat**: both small — no shift changes anything.
- **Edge**: one large, one near zero — sliding along the edge changes nothing, so the point cannot be located along it (the aperture problem).
- **Corner**: both large — every shift is visible, so the point is pinned in 2D.

Harris and Stephens (Alvey Vision Conference, 1988) avoid the eigen-decomposition with the response

$$R=\det M-k\,(\operatorname{tr}M)^2=\lambda_1\lambda_2-k\,(\lambda_1+\lambda_2)^2$$

which works because the determinant and trace are the product and sum of the eigenvalues: $R$ is large and positive at a corner, negative on an edge and near zero in a flat region. $k$ is an empirical constant, commonly 0.04–0.06. Shi and Tomasi ("Good Features to Track", CVPR 1994) score the window by $\min(\lambda_1,\lambda_2)$ directly, which removes $k$. Either way, keep only local maxima above a threshold (non-maximum suppression).

**Scale: SIFT.** Harris is invariant to rotation but not to scale: a corner at one zoom level is a rounded curve at another. Lowe's SIFT (IJCV 2004) also searches over scale, in three steps.

- *Detect across scale.* It blurs the image with Gaussians of increasing $\sigma$, subtracts neighbouring levels (the difference of Gaussians, a cheap approximation of the scale-normalized Laplacian — a blob detector whose response peaks when the blur width is comparable to the blob's size), and keeps points that are extrema among their 26 neighbours in space and scale.
- *Reject.* Low-contrast points and edge-like points are discarded; the edge test uses a 2×2 Hessian eigenvalue ratio, the same logic as above.
- *Describe.* Each keypoint receives a dominant gradient orientation, and the descriptor is computed in that rotated, scaled frame: a 4×4 grid of cells around the point, each holding an 8-bin histogram of gradient orientations, gives 4·4·8 = 128 numbers. The vector is normalized to reduce illumination effects and compared by Euclidean distance.

**Binary: ORB.** SIFT descriptors are floating-point and comparatively costly. ORB (Rublee et al., ICCV 2011) replaces each stage with a cheaper one.

- *Detect:* the FAST corner test (a quick comparison of pixels on a circle around the candidate), ranked by the Harris score.
- *Orient:* an angle from the patch's intensity centroid.
- *Describe:* a rotated ("steered") BRIEF descriptor, 256 pairwise intensity comparisons stored as bits.

Two descriptors are compared by **Hamming distance** — XOR, then count the set bits — which costs a few CPU instructions. ORB-SLAM (Mur-Artal et al., IEEE T-RO 2015) uses ORB for tracking, mapping, relocalization and loop closing because it can be extracted and matched at frame rate on a CPU, is rotation-invariant and tolerates moderate viewpoint change. ORB itself is not scale-invariant, so it is extracted over an image pyramid.

**Match: nearest neighbour, then filter.** For each descriptor in image A, find the nearest descriptor in image B. Raw nearest neighbours contain many wrong pairs, so three filters follow:

1. **Ratio test** (Lowe 2004): accept only if $d_1/d_2 < 0.8$, where $d_1, d_2$ are the distances to the nearest and second-nearest candidates. A distinctive point has a clear winner; a point on a repeated pattern has two near-equal candidates. On his data, Lowe reports that 0.8 removed about 90% of false matches while discarding under 5% of correct ones.
2. **Mutual check**: keep $a\leftrightarrow b$ only if $a$ is also $b$'s nearest neighbour in the reverse direction.
3. **Geometric verification**: survivors must agree with one camera motion. RANSAC (Fischler & Bolles, CACM 1981) repeatedly fits a model — a fundamental or essential matrix, a homography, or a PnP pose — to a random minimal sample and keeps the model with the most inliers; the sample-count arithmetic is worked in [[02-foundations/algorithms/robotics-ai-problems|11.8 §3 RANSAC line fitting]]. The warning from ICP in §4 carries over: least squares on wrong correspondences is confidently wrong.

**Learned features.** SuperPoint (DeTone et al., CVPR Workshops 2018) trains one network to output keypoints and descriptors. SuperGlue (Sarlin et al., CVPR 2020) replaces nearest-neighbour-plus-ratio with a graph neural network that matches the two point sets jointly. LoFTR (Sun et al., CVPR 2021) drops the detector and matches dense transformer features, aiming at low-texture regions where detectors find few points. Each paper reports stronger matching under large viewpoint and illumination change on its benchmarks. Classic features can still be the right call. Weigh the compute budget and frame rate on an embedded robot computer, and whether the training data resembled your scenes. Textureless or repetitive construction surfaces — bare drywall, formwork, rebar grids, identical façade panels — are hard for every method, so test on your own sequences rather than trusting a benchmark ranking.

> [!example] Worked example · 계산 예제
> Take three 5×5 patches with intensities 0 or 10. Use central differences, $I_x=(I_{x+1}-I_{x-1})/2$, on the inner 3×3 pixels, with $w=1$ and $k=0.05$.
> - **Flat** (all 10): every gradient is 0, so $M=0$, $\lambda=(0,0)$ and $R=0$.
> - **Edge** (left two columns 0, the rest 10): $I_x=5$ at 6 pixels and $I_y=0$, so $M=\begin{pmatrix}150&0\\0&0\end{pmatrix}$, $\lambda=(0,150)$ and $R=0-0.05\cdot150^2=-1125$.
> - **Corner** (bright lower-right 3×3 block): $I_x=5$ at 4 pixels, $I_y=5$ at 4, both at 1, so $M=\begin{pmatrix}100&25\\25&100\end{pmatrix}$, $\lambda=(75,125)$ and $R=9375-0.05\cdot200^2=7375$.
>
> The signs follow the rule — flat 0, edge negative, corner positive — and the Shi–Tomasi scores are 0, 0 and 75.
>
> **Ratio test.** A descriptor's three nearest candidates lie at distances 0.20, 0.23 and 0.61. Since $0.20/0.23=0.87>0.8$, reject the match even though 0.20 is the best: two similar candidates usually mean repeated structure. The third distance plays no role. Had the second been 0.45, $0.20/0.45=0.44$ would pass.

The same response on a synthetic image, with a check that the corner pixel scores highest:

```python
import numpy as np

def harris(img, k=0.05):
    Iy, Ix = np.gradient(img.astype(float))          # axis 0 is y (rows), axis 1 is x
    def box3(a):                                     # window sum with w = 1 on a 3x3 patch
        p = np.pad(a, 1)
        return sum(p[i:i + a.shape[0], j:j + a.shape[1]] for i in range(3) for j in range(3))
    Sxx, Syy, Sxy = box3(Ix * Ix), box3(Iy * Iy), box3(Ix * Iy)
    return Sxx * Syy - Sxy**2 - k * (Sxx + Syy)**2   # det M - k (tr M)^2 at every pixel

img = np.zeros((20, 20))
img[10:, 10:] = 1.0                                  # one bright quadrant, corner at (10, 10)
R = harris(img)
r, c = np.unravel_index(np.argmax(R), R.shape)
print(r, c, round(R.max(), 3), round(R[15, 10], 3), R[3, 3])   # 10 10 0.738 -0.112 0.0
assert (r, c) == (10, 10) and R[15, 10] < 0 and R[3, 3] == 0     # corner > 0, edge < 0, flat 0
```

> [!warning] Reading matching claims · 매칭 주장 읽기
> - A match count is not accuracy. Look for the inlier ratio after geometric verification and the downstream pose error.
> - Note the ratio threshold, the RANSAC pixel threshold and the model (F, E, H or PnP); results move with all of them.
> - Repeated structure can yield matches that are consistently wrong: a set shifted by one façade panel still fits a single motion and passes RANSAC. This is the §4 warning in image form.
> - Harris and FAST are not scale-invariant on their own; check how scale is handled (pyramid or scale space).
> - For learned matchers, check the training data, input resolution, GPU and whether reported timing includes detection.

### 3. Point clouds and frames

A depth image plus intrinsics back-projects to a **point cloud**:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. Every cloud lives in some frame — sensor, base,
map — and multi-sensor pipelines stand or fall on the **extrinsic calibration** between
those frames ([[04-robotics/robot-systems-deployment|the TF tree at runtime]]). A
plausible-looking cloud in the wrong frame produces systematic, learning-resistant errors.

### 4. Registration and ICP

**Registration** aligns two geometries: a scan with another scan, a point cloud with a part model, or a site scan with BIM. The unknown is a rigid transform $T\in SE(3)$. Before optimizing it, ask which points are supposed to represent the same surface.

**ICP** (iterative closest point) alternates two problems: match points under the current transform, then update the transform while holding those matches fixed. For ordinary rigid **point-to-point** least squares, the fixed-correspondence update has a closed-form SVD solution. **Point-to-plane** variants commonly use linearized least squares. Gauss–Newton or Levenberg–Marquardt is therefore not a defining requirement of every ICP update ([[02-foundations/optimization|4. Optimization §3.5]]).

Imagine aligning a scan of one wall panel to a model containing several similar panels. A bad initial transform may match the scan to the neighboring panel. Even an exact least-squares solution for those matches can reinforce the wrong alignment. **This is why ICP is local:** correspondence selection and pose depend on each other, and alternating improvements do not search every assignment. Use an initial estimate from odometry or global matching and inspect overlap and outliers. See the [MIT geometric pose-estimation derivation](https://manipulation.mit.edu/pose.html).

Degeneracy depends on the measured geometry and objective. Point-to-plane residuals on a featureless planar patch cannot constrain translation along the plane or rotation about its normal. Distinct boundaries or point correspondences can supply additional information. Thus “a wall is degenerate” is shorthand for an insufficient measurement model, not a universal statement about every wall scan.

> [!question] Check the correspondence · 대응점 확인
> Does a small ICP residual prove the pose is correct? **Answer:** no. Repeated panels may fit well at the wrong location. Check initialization, independent landmarks and the unconstrained directions, not only the final residual.

### 5. Calibration

| Calibration | What it estimates | Typical method |
|---|---|---|
| Intrinsic | $f_x,f_y,c_x,c_y$, distortion | checkerboard/target views |
| Camera–camera (stereo) | relative $SE(3)$ + rectification | shared target views |
| Camera–LiDAR | extrinsic $SE(3)$ | target or mutual-feature alignment |
| Hand–eye (camera–robot) | sensor-to-end-effector or base transform | robot motion + target ($AX=XB$) |
| Temporal | clock offset / latency between sensors | correlation of motion signals |

In the hand–eye equation $AX=XB$ for a wrist-mounted camera, $A$ is the gripper's motion between two robot poses (known from the joint encoders), $B$ is the camera's motion between the same two poses (measured from the target), and $X$ is the unknown camera-to-gripper transform. Each pair of poses gives one equation, and several pairs with different rotation axes pin $X$ down.

The quality metric is usually **reprojection error**: project the estimated 3D points
through the estimated model and measure pixel distance to their detections. Low
reprojection error on the calibration set does **not** guarantee accuracy outside the
calibrated volume, range, or temperature, because the model was fitted only at the target positions, distances and conditions actually observed; outside them it is extrapolating, not obeying a physical law.

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

> [!warning] Reading the claim · 핵심 주장 읽는 법
> Sub-pixel reprojection error and beautiful reconstructions do not by themselves mean
> the *pose is right in the robot's base frame* — that also requires correct extrinsics
> and time synchronization, which many papers hold fixed and out of scope.

### 7.5 From seeing an error to correcting it: visual servoing

Perception does not close a robot loop until an image or pose error becomes a velocity
command. **PBVS** estimates two poses, forms a pose error such as
$\xi=\operatorname{Log}(T_{current}^{-1}T_{desired})^\vee$, and commands a twist that reduces
$\xi$. Its accuracy inherits calibration and pose-estimation errors. **IBVS** stays in the
image: for image features $s$, $\dot s=L_s v_c$, where the image Jacobian $L_s$ depends on
feature depth; a local law such as $v_c=-\lambda L_s^+(s-s^*)$ reduces pixel error. IBVS can
be less sensitive to full pose reconstruction but still needs depth estimates and a
well-conditioned feature geometry. Neither equation alone guarantees visibility, actuator
limits, global convergence, or collision avoidance. Read a "closed-loop perception" claim
by identifying the error, Jacobian, control rate, depth source, and recovery outside the
local basin.

### After reading

- Project a 3D point through a pinhole model by hand.
- Distinguish intrinsics from extrinsics and say when each changes.
- Explain why monocular vision loses scale and where scale re-enters.
- Explain ICP's loop and why it needs initialization.
- Name the calibrations a camera+LiDAR+arm system needs.
- Interpret reprojection error without over-trusting it.
- Distinguish PBVS from IBVS and identify where pose, calibration, depth and the image Jacobian enter the loop.
- Explain why corners, not edges, are matched, and filter matches with the ratio test, a mutual check and RANSAC.

> [!tip] Going deeper · 더 깊이
> Szeliski's [*Computer Vision: Algorithms and Applications*](https://szeliski.org/Book/) is free and covers this page's whole span; when you need multi-view geometry stated as theorems — essential and fundamental matrices, triangulation, bundle adjustment — Hartley and Zisserman's *Multiple View Geometry in Computer Vision* is the reference the field cites.

### Self-check

1. With the worked intrinsics, where does $p^{c}=(-0.3, 0.1, 1.5)$ project?
2. Stereo at $f=600$, $b=0.12$: what disparity corresponds to $Z=24$ m, and why is that a problem?
3. Why can ICP fail in a long empty corridor even with perfect data?
4. A paper fuses LiDAR and camera "without calibration" — what is it most likely still assuming?
5. A window has $\sum I_x^2=40$, $\sum I_y^2=2$ and $\sum I_xI_y=0$. With $k=0.05$, what are the Harris response and the Shi–Tomasi score, and what kind of point is it?
6. On a wall of identical panels, an ORB descriptor's nearest candidate is 32 bits away and the second is 36. Does it pass a 0.8 ratio test, and what must catch a wrong match that survives the filters?

> [!tip]- Answers
> 1. $u = 600(-0.3)/1.5+320 = 200$, $v = 600(0.1)/1.5+240 = 280$.
> 2. $d = fb/Z = 600\cdot0.12/24 = 3$ px — a ±1 px error spans 18–36 m; long-range stereo depth is fragile.
> 3. Translation along the corridor axis barely changes point-to-nearest-point distances — a degenerate (unobservable) direction.
> 4. Known intrinsics, and usually a rough extrinsic initialization or joint optimization that still needs overlap and synchronized timestamps.
> 5. The eigenvalues are 40 and 2, so $R=80-0.05\cdot42^2=-8.2<0$ and $\min\lambda=2$. It is an edge: intensity changes along $x$ only, so the point is poorly located along the edge direction $y$.
> 6. No: $32/36=0.89>0.8$, so reject it — near-equal candidates suggest the neighbouring panel. A wrong match that survives must be caught by geometric verification (RANSAC), and a set shifted by one whole panel can pass even that, so check against odometry or independent landmarks.

### Problem set · 과제

Tier B. **P5** as a range to a wall ([[02-foundations/lab-plants|0.6]]). One hand–eye number: camera $4\,\mathrm{cm}$ behind the P2 tip. No simulator.

1. **Draw.** Wrist camera looking along $+x$ at the panel. Mark P5's prior and measurement on that ray, and the $4\,\mathrm{cm}$ camera-to-tip offset.
2. **Derive.** Scalar Kalman of P5: $K$, fused range, $P^+$. If that fused number is camera-to-wall, what is tip-to-wall after the $4\,\mathrm{cm}$?
3. **Interpret.** In $AX=XB$, which of $A,B,X$ is the $4\,\mathrm{cm}$? Why a $1\,\mathrm{px}$ reprojection error does not certify that number.

> [!tip]- Solutions
> 1. Ray from camera through the tip to the wall. Prior $10\,\mathrm{cm}$, $z=12\,\mathrm{cm}$, camera behind the tip.
> 2. $K=4/(4+1)=0.8$, fused $11.6\,\mathrm{cm}$, $P^+=0.8$. Tip-to-wall $11.6-4=7.6\,\mathrm{cm}$.
> 3. $X$ is the unknown camera-to-gripper transform; $4\,\mathrm{cm}$ is one translation component of $X$. $A$ is gripper motion, $B$ is camera motion. Reprojection can be small while $X$ is still wrong outside the calibrated volume (§5).

### Sources

- [Szeliski, *Computer Vision: Algorithms and Applications* (free official PDF)](https://szeliski.org/Book/)
- [OpenCV camera calibration tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [KITTI sensor setup — a real calibrated multi-sensor rig](https://www.cvlibs.net/datasets/kitti/setup.php)
- Harris, C. & Stephens, M. "A combined corner and edge detector." *Proceedings of the 4th Alvey Vision Conference*, 1988.
- Shi, J. & Tomasi, C. "Good features to track." *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 1994.
- Lowe, D. G. "Distinctive image features from scale-invariant keypoints." *International Journal of Computer Vision* 60(2), 2004. doi:10.1023/B:VISI.0000029664.99615.94
- Rublee, E., Rabaud, V., Konolige, K. & Bradski, G. "ORB: An efficient alternative to SIFT or SURF." *IEEE International Conference on Computer Vision (ICCV)*, 2011.
- Mur-Artal, R., Montiel, J. M. M. & Tardós, J. D. "ORB-SLAM: A versatile and accurate monocular SLAM system." *IEEE Transactions on Robotics* 31(5), 2015. doi:10.1109/TRO.2015.2463671
- Fischler, M. A. & Bolles, R. C. "Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography." *Communications of the ACM* 24(6), 1981. doi:10.1145/358669.358692
- DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperPoint: Self-supervised interest point detection and description." *CVPR Workshops*, 2018.
- Sarlin, P.-E., DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperGlue: Learning feature matching with graph neural networks." *CVPR*, 2020.
- Sun, J., Shen, Z., Wang, Y., Bao, H. & Zhou, X. "LoFTR: Detector-free local feature matching with transformers." *CVPR*, 2021.

## 한국어

*B군이다. [[02-foundations/linear-algebra|선형대수]]·최적화와 [[02-foundations/se3-geometry|SE(3)]] 위에 선다. 픽셀과 점군이 올바른 좌표계의
3D가 되는 과정이고, H군과 J군의 인식 주장이 전부 여기를 통과한다.*

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

> [!note] 처음이라면 · First pass
> 먼저 §1(핀홀 모델, 투영식까지), §5(보정 — 현장 실패가 실제로 시작되는 곳), §7. §2~§4는 기계장치이고, 논문의 숫자가 거기 기댈 때 읽어라.

### 1. 핀홀 카메라 모델

**카메라 프레임**의 3D 점 $p^{c}=(X,Y,Z)$는 픽셀 $(u,v)$로 투영된다:

$$u = f_x\frac{X}{Z}+c_x, \qquad v = f_y\frac{Y}{Z}+c_y$$

**이것이 어디서 오는가 — 닮은꼴 삼각형, 그게 전부다.** 광학 중심을 원점에 두고 이미지 평면을
그 앞 거리 $f$에 둔다. 3D 점 $(X, Y, Z)$에서 중심으로 가는 광선이 그 평면을 높이 $y$에서
지나는데, 그 광선이 만드는 두 삼각형 — 중심에서 평면까지, 중심에서 점까지 — 이 닮은꼴이다.
그래서 $y/f = Y/Z$, 즉 $y = fY/Z$다. 나머지는 장부 정리다. 물리적 픽셀 피치로 나눠 픽셀 단위로
바꾸고(픽셀이 정사각이 아니면 $f_x$와 $f_y$가 달라지는 이유이고, 초점 거리를 밀리미터가 아니라
*픽셀 단위*로 적는 이유다), $c_x, c_y$를 더해 원점을 광축에서 배열 인덱스가 시작하는 이미지
모서리로 옮긴다.

모델은 그게 전부이고, 그 모양이 뒤따르는 전부가 물려받는 두 사실을 지고 있다. 이 사상은
**선형이 아니다** — $Z$가 분모에 있고, 그래서 원근이 행렬이 되려면 먼저 동차 좌표가 필요하다 —
그리고 **가역이 아니다**. 한 광선 위의 모든 점이 같은 $(u,v)$를 주기 때문이다. 그러므로 $Z$를
되찾는 것은 더 좋은 카메라의 문제가 아니라 두 번째 제약이 필요한 문제이고, §2가 그것에 관한
것이다.

- **Intrinsics** $(f_x, f_y, c_x, c_y$, 왜곡$)$: 카메라 자체의 성질 — 픽셀 단위 초점
  거리와 주점. 한 번 보정하면 (렌즈를 건드리기 전까지) 고정.
- **Extrinsics** $(R, t)$: 투영 전에 다른 프레임(로봇 베이스, 월드)의 점을 카메라 프레임으로 옮기는 [[02-foundations/se3-geometry|SE(3)]] 변환 $T_{cw}$, $p^c = Rp^w + t$다.
  그 프레임에서의 카메라 *pose*는 그 역 $T_{wc}$이고 카메라 중심은 $-R^\top t$다. 중심은 $p^c=0$인 점이므로 $0=Rp^w+t$에서 $p^w=-R^\top t$가 나온다($R^{-1}=R^\top$ 사용). 보정 파일이 어느 쪽을 저장하는지 확인하라.
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
| 학습된 단안 깊이 | 네트워크가 $Z$ 예측 (대개 스케일과 오프셋이 미정, 흔히 역깊이 $1/Z$ 공간. 먼 배경으로 갈수록 $1/Z$는 0 근처에 머물러 유계다) | 스케일 모호성; 분포 이동 — [[01-canonical-papers/notes/2-computer-vision/depth-anything\|Depth Anything]]의 주장 범위 확인 |
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
  <g font-size="11" fill="currentColor"><text x="30" y="240" opacity="0.9">시차는 수평 픽셀 이동량이며, 먼 점에서는 삼각측량 각도와 함께 작아진다.</text></g>
</svg>



### 2.5 이미지 특징: 검출, 기술, 매칭

**한 문장으로:** 다른 이미지에서 다시 찾을 수 있는 점 수백 개를 고르고, 점마다 짧은 지문을 붙이고, 이미지 사이에서 지문을 짝짓는다. 그 짝이 모든 기하 단계가 필요로 하는 대응점이다.

왜 모든 픽셀이 아니라 드문드문한 점인가? §2의 스테레오 깊이는 왼쪽 이미지의 픽셀이 오른쪽 어느 픽셀과 같은 점인지 알아야 한다. §5의 보정은 타깃 모서리를 서브픽셀 정확도로 찾아야 한다. Visual odometry와 SLAM([[04-robotics/state-estimation-slam|상태 추정]])은 같은 점을 프레임마다 추적해 pose를 제약한다. 점이 쓸모 있으려면 **반복성**(시점이 바뀌어도 다시 검출됨)과 **변별성**(주변이 다른 많은 곳과 닮지 않음)을 갖춰야 한다. 파이프라인은 세 단계이고, 논문은 그중 어느 단계든 바꿀 수 있다.

**검출: 모든 방향으로 변하는 곳.** 작은 창을 $(u,v)$만큼 옮기고 내용이 얼마나 바뀌는지 잰다. 1차 테일러 전개로 $I(x+u,y+v)\approx I(x,y)+I_x u+I_y v$이므로 픽셀마다 차이는 $I_x u+I_y v$이고, 그 제곱 $I_x^2u^2+2I_xI_y\,uv+I_y^2v^2$은 $(u,v)$의 이차식이다. 따라서 창 전체에서 더하면 변화가 이차 형식이 된다.

$$E(u,v)=\sum_{x,y} w(x,y)\,\big(I(x+u,y+v)-I(x,y)\big)^2 \approx (u,v)\,M\,(u,v)^\top$$

그래서 전체 거동은 2×2 행렬 하나, 곧 **구조 텐서** 하나가 정한다. 창 안의 영상 기울기 $I_x, I_y$를 가중치 $w$(상자 또는 가우시안)로 더한 것이다.

$$M=\sum_{x,y} w(x,y)\begin{pmatrix}I_x^2 & I_xI_y\\ I_xI_y & I_y^2\end{pmatrix}$$

고윳값 $\lambda_1 \le \lambda_2$는 가장 덜 변하는 이동 방향과 가장 많이 변하는 이동 방향의 변화량이므로, 창을 이렇게 분류한다.

- **평탄**: 둘 다 작다 — 어느 쪽으로 옮겨도 변화가 없다.
- **에지**: 하나는 크고 하나는 거의 0이다 — 에지를 따라 미끄러지면 변화가 없으므로 그 방향으로는 위치를 정할 수 없다(aperture 문제).
- **코너**: 둘 다 크다 — 어떤 이동도 드러나므로 점이 2D로 고정된다.

Harris와 Stephens(Alvey Vision Conference, 1988)는 고윳값 분해 없이 다음 응답을 쓴다.

$$R=\det M-k\,(\operatorname{tr}M)^2=\lambda_1\lambda_2-k\,(\lambda_1+\lambda_2)^2$$

행렬식과 대각합이 고윳값의 곱과 합이기 때문에 이 식이 통한다. $R$은 코너에서 크고 양수, 에지에서 음수, 평탄한 영역에서 0 근처다. $k$는 경험적 상수로 흔히 0.04–0.06을 쓴다. Shi와 Tomasi("Good Features to Track", CVPR 1994)는 $\min(\lambda_1,\lambda_2)$를 직접 점수로 써서 $k$를 없앤다. 어느 쪽이든 문턱값을 넘는 국소 최댓값만 남긴다(non-maximum suppression).

**스케일: SIFT.** Harris는 회전에는 불변이지만 스케일에는 불변이 아니다. 한 배율의 코너가 다른 배율에서는 둥근 곡선이다. Lowe의 SIFT(IJCV 2004)는 스케일 방향으로도 탐색하며, 세 단계로 이루어진다.

- *스케일에 걸쳐 검출.* $\sigma$를 키워 가며 가우시안으로 흐리게 한 뒤 이웃 단계끼리 빼고(difference of Gaussians, 스케일 정규화 라플라시안의 값싼 근사 — 흐림 폭이 덩어리 크기와 비슷할 때 응답이 가장 커지는 blob 검출기), 공간과 스케일의 이웃 26개 가운데 극값인 점을 남긴다.
- *버리기.* 대비가 낮은 점과 에지 같은 점은 버리는데, 에지 판정은 위와 같은 논리로 2×2 헤시안의 고윳값 비를 쓴다.
- *기술.* 키포인트마다 지배적인 기울기 방향을 붙이고, 그 회전·스케일 좌표계에서 기술자를 계산한다. 점 주위를 4×4 칸으로 나누고 칸마다 기울기 방향의 8구간 히스토그램을 만들면 4·4·8 = 128개의 수가 된다. 조명 영향을 줄이도록 정규화하고 유클리드 거리로 비교한다.

**이진: ORB.** SIFT 기술자는 실수 벡터이고 계산이 비교적 무겁다. ORB(Rublee 외, ICCV 2011)는 각 단계를 더 값싼 것으로 바꾼다.

- *검출:* FAST 코너 검사(후보 주위 원 위의 픽셀을 빠르게 비교)를 Harris 점수로 순위를 매겨 쓴다.
- *방향:* 패치의 밝기 중심(intensity centroid)으로 각도를 정한다.
- *기술:* 회전시킨(steered) BRIEF 기술자, 곧 픽셀 쌍의 밝기 비교 256개를 비트로 저장한 것이다.

두 기술자는 **해밍 거리**, 곧 XOR 후 켜진 비트 수로 비교하며 CPU 명령 몇 개면 계산된다. ORB-SLAM(Mur-Artal 외, IEEE T-RO 2015)이 추적·지도 작성·재위치 추정·루프 닫기에 모두 ORB를 쓰는 이유는 CPU에서 프레임 속도로 추출·매칭할 수 있고, 회전에 불변이며, 적당한 시점 변화를 견디기 때문이다. ORB 자체는 스케일 불변이 아니어서 이미지 피라미드 위에서 추출한다.

**매칭: 최근접 이웃, 그다음 거르기.** 이미지 A의 기술자마다 이미지 B에서 가장 가까운 기술자를 찾는다. 날것의 최근접 짝에는 틀린 쌍이 많아서 세 가지 거르기가 뒤따른다.

1. **비율 검사**(Lowe 2004): 가장 가까운 후보와 두 번째 후보까지의 거리를 $d_1, d_2$라 할 때 $d_1/d_2 < 0.8$일 때만 받아들인다. 변별력 있는 점에는 확실한 1등이 있고, 반복 패턴 위의 점에는 거의 같은 후보가 둘 있다. Lowe는 자신의 데이터에서 0.8이 틀린 매칭의 약 90%를 없애면서 맞는 매칭은 5% 미만만 버렸다고 보고한다.
2. **상호 검사**: 역방향으로도 $a$가 $b$의 최근접 이웃일 때만 $a\leftrightarrow b$를 남긴다.
3. **기하 검증**: 남은 짝은 하나의 카메라 운동과 맞아야 한다. RANSAC(Fischler & Bolles, CACM 1981)은 무작위 최소 표본에 모델 — fundamental 또는 essential 행렬, homography, PnP pose — 을 맞추기를 반복하고 인라이어가 가장 많은 모델을 남긴다. 표본 수 계산은 [[02-foundations/algorithms/robotics-ai-problems|11.8 §3 RANSAC 직선 맞춤]]에서 직접 해 본다. §4의 ICP 경고가 그대로 적용된다. 틀린 대응에 대한 최소제곱은 자신 있게 틀린다.

**학습된 특징.** SuperPoint(DeTone 외, CVPR Workshops 2018)는 한 네트워크가 키포인트와 기술자를 함께 출력하도록 학습한다. SuperGlue(Sarlin 외, CVPR 2020)는 최근접 이웃과 비율 검사를 두 점 집합을 한꺼번에 짝짓는 그래프 신경망으로 바꾼다. LoFTR(Sun 외, CVPR 2021)은 검출기를 없애고 트랜스포머 특징을 조밀하게 매칭해, 검출기가 점을 거의 찾지 못하는 저텍스처 영역을 겨냥한다. 각 논문은 자기 벤치마크의 큰 시점·조명 변화에서 더 강한 매칭을 보고한다. 그래도 고전 특징이 맞는 선택일 수 있다. 임베디드 로봇 컴퓨터의 연산 예산과 프레임 속도, 학습 데이터가 내 장면과 닮았는지를 따져라. 맨 석고보드, 거푸집, 철근 격자, 똑같은 외벽 패널처럼 무늬가 없거나 반복되는 건설 현장 표면은 어떤 방법에도 어렵다. 벤치마크 순위를 믿기보다 자기 시퀀스에서 시험하라.

> [!example] 계산 예제 · Worked example
> 밝기가 0 또는 10인 5×5 패치 세 개를 잡는다. 안쪽 3×3 픽셀에서 중앙 차분 $I_x=(I_{x+1}-I_{x-1})/2$를 쓰고, $w=1$, $k=0.05$로 둔다.
> - **평탄** (전부 10): 기울기가 모두 0이므로 $M=0$, $\lambda=(0,0)$, $R=0$이다.
> - **에지** (왼쪽 두 열 0, 나머지 10): $I_x=5$인 픽셀이 6개이고 $I_y=0$이므로 $M=\begin{pmatrix}150&0\\0&0\end{pmatrix}$, $\lambda=(0,150)$, $R=0-0.05\cdot150^2=-1125$다.
> - **코너** (오른쪽 아래 3×3 블록만 밝음): $I_x=5$인 픽셀 4개, $I_y=5$인 픽셀 4개, 둘 다인 픽셀 1개이므로 $M=\begin{pmatrix}100&25\\25&100\end{pmatrix}$, $\lambda=(75,125)$, $R=9375-0.05\cdot200^2=7375$다.
>
> 부호가 규칙대로다 — 평탄 0, 에지 음수, 코너 양수. Shi–Tomasi 점수는 0, 0, 75다.
>
> **비율 검사.** 어떤 기술자의 가장 가까운 후보 세 개가 거리 0.20, 0.23, 0.61에 있다. $0.20/0.23=0.87>0.8$이므로 0.20이 1등인데도 매칭을 버린다. 비슷한 후보가 둘이면 대개 반복 구조다. 세 번째 거리는 아무 역할도 하지 않는다. 두 번째가 0.45였다면 $0.20/0.45=0.44$로 통과했을 것이다.

같은 응답을 합성 이미지에 계산하고, 코너 픽셀의 점수가 가장 큰지 확인하는 코드다.

```python
import numpy as np

def harris(img, k=0.05):
    Iy, Ix = np.gradient(img.astype(float))          # axis 0 is y (rows), axis 1 is x
    def box3(a):                                     # window sum with w = 1 on a 3x3 patch
        p = np.pad(a, 1)
        return sum(p[i:i + a.shape[0], j:j + a.shape[1]] for i in range(3) for j in range(3))
    Sxx, Syy, Sxy = box3(Ix * Ix), box3(Iy * Iy), box3(Ix * Iy)
    return Sxx * Syy - Sxy**2 - k * (Sxx + Syy)**2   # det M - k (tr M)^2 at every pixel

img = np.zeros((20, 20))
img[10:, 10:] = 1.0                                  # one bright quadrant, corner at (10, 10)
R = harris(img)
r, c = np.unravel_index(np.argmax(R), R.shape)
print(r, c, round(R.max(), 3), round(R[15, 10], 3), R[3, 3])   # 10 10 0.738 -0.112 0.0
assert (r, c) == (10, 10) and R[15, 10] < 0 and R[3, 3] == 0     # corner > 0, edge < 0, flat 0
```

> [!warning] 매칭 주장 읽기 · Reading matching claims
> - 매칭 개수는 정확도가 아니다. 기하 검증 뒤의 인라이어 비율과 그다음 단계의 pose 오차를 찾아라.
> - 비율 문턱값, RANSAC 픽셀 문턱값, 모델(F, E, H, PnP)을 적어 두라. 결과가 이 모두에 따라 움직인다.
> - 반복 구조는 일관되게 틀린 매칭을 만들 수 있다. 외벽 패널 한 칸만큼 밀린 매칭 집합도 하나의 운동에 맞아 RANSAC을 통과한다. 이미지 버전의 §4 경고다.
> - Harris와 FAST는 그 자체로 스케일 불변이 아니다. 스케일을 어떻게 다루는지(피라미드인지 스케일 공간인지) 확인하라.
> - 학습된 매처라면 학습 데이터, 입력 해상도, GPU, 보고된 시간에 검출이 포함되는지 확인하라.

### 3. 포인트 클라우드와 프레임

깊이 이미지 + intrinsics를 역투영하면 **포인트 클라우드**가 된다:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. 모든 클라우드는 어떤 프레임(센서·베이스·맵)에
산다 — 다중 센서 파이프라인은 그 프레임들 사이의 **extrinsic 보정**에 성패가 달려 있다
([[04-robotics/robot-systems-deployment|런타임에서는 TF 트리]]). 그럴듯해 보여도 틀린
프레임의 클라우드는 학습으로 잘 고쳐지지 않는 계통 오차를 만든다.

### 4. Registration과 ICP

**Registration**은 두 기하를 정렬한다. 스캔끼리, 점군과 부품 모델, 현장 스캔과 BIM이 대상이다. 미지수는 강체 변환 $T\in SE(3)$다. 최적화하기 전에 어떤 점끼리 같은 표면을 나타내는지부터 물어야 한다.

**ICP**(iterative closest point)는 현재 변환으로 대응점을 고른 뒤, 그 대응을 고정하고 변환을 갱신한다. 일반적인 강체 **점대점** 최소제곱의 고정 대응 갱신은 SVD로 닫힌 형태의 해를 구한다. **점대평면** 방식은 흔히 선형화한 최소제곱을 쓴다. 따라서 모든 ICP 갱신에 Gauss–Newton이나 Levenberg–Marquardt가 필수인 것은 아니다([[02-foundations/optimization|4. 최적화 §3.5]]).

비슷한 패널이 반복되는 벽 모델에 스캔을 맞춘다고 하자. 초기 변환이 틀리면 옆 패널의 점과 짝지을 수 있다. 그 대응에 대해 최소제곱을 정확히 풀어도 잘못된 정렬을 강화할 수 있다. **ICP가 국소적인 이유**는 대응 선택과 자세가 서로 의존하며, 번갈아 개선한다고 모든 대응을 탐색하지는 않기 때문이다. odometry나 전역 매칭으로 초기값을 얻고 겹치는 영역과 이상점을 확인한다. [MIT 기하 자세 추정 유도](https://manipulation.mit.edu/pose.html)를 함께 보라.

퇴화는 기하와 목적함수에 달렸다. 특징 없는 평면의 점대평면 잔차로는 평면을 따르는 병진과 법선 둘레 회전을 제약할 수 없다. 뚜렷한 경계나 점 대응은 추가 정보를 줄 수 있다. “벽은 퇴화한다”는 말은 측정 모델의 정보 부족을 줄여 부르는 것이지, 모든 벽 스캔의 보편적 성질은 아니다.

> [!question] 대응점 확인 · Check the correspondence
> ICP 잔차가 작으면 자세도 맞는가? **답:** 아니다. 반복 패널은 틀린 위치에서도 잘 맞는다. 최종 잔차뿐 아니라 초기값, 독립 랜드마크, 제약되지 않는 방향을 확인한다.

### 5. 보정

| 보정 | 추정 대상 | 전형적 방법 |
|---|---|---|
| Intrinsic | $f_x,f_y,c_x,c_y$, 왜곡 | 체커보드/타깃 촬영 |
| 카메라–카메라 (스테레오) | 상대 $SE(3)$ + 정렬(rectification) | 공유 타깃 촬영 |
| 카메라–LiDAR | extrinsic $SE(3)$ | 타깃 또는 상호 특징 정렬 |
| Hand–eye (카메라–로봇) | 센서–말단 또는 베이스 변환 | 로봇 운동 + 타깃 ($AX=XB$) |
| 시간 | 센서 간 클럭 오프셋/지연 | 운동 신호의 상관 |

손목에 단 카메라의 hand–eye 방정식 $AX=XB$에서 $A$는 두 로봇 자세 사이의 그리퍼 운동(관절 엔코더로 안다), $B$는 같은 두 자세 사이의 카메라 운동(타깃으로 측정한다), $X$는 모르는 카메라–그리퍼 변환이다. 자세 한 쌍이 방정식 하나를 주고, 회전축이 서로 다른 여러 쌍이 모여야 $X$가 정해진다.

품질 지표는 대개 **reprojection error**다: 추정된 3D 점을 추정된 모델로 투영해 검출
위치와의 픽셀 거리를 잰다. 보정 세트에서 낮은 reprojection error가 보정된 부피·거리·
온도 밖에서의 정확도를 보장하지는 **않는다**. 모델은 타깃을 실제로 관측한 위치·거리·조건에서만 맞춰졌으므로, 그 밖에서는 물리 법칙을 따르는 것이 아니라 외삽하고 있을 뿐이다.

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

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 서브픽셀 reprojection error와 아름다운 복원이 그 자체로 *로봇 베이스 프레임에서
> pose가 맞다*는 뜻은 아니다 — 그러려면 올바른 extrinsics와 시간 동기화도 필요한데,
> 많은 논문이 이를 고정된 범위 밖 가정으로 둔다.

### 7.5 오차를 보고 고치는 명령으로: visual servoing

이미지나 pose 오차가 속도 명령이 되어야 인식이 로봇 루프를 닫는다. **PBVS**는 두 자세를
추정해 $\xi=\operatorname{Log}(T_{current}^{-1}T_{desired})^\vee$ 같은 pose error를 만들고,
$\xi$를 줄이는 twist를 명령한다. 정확도는 보정과 pose 추정 오차를 물려받는다. **IBVS**는
이미지에 남는다. 특징 $s$에 대해 $\dot s=L_s v_c$이고 image Jacobian $L_s$는 특징 깊이에
의존한다. $v_c=-\lambda L_s^+(s-s^*)$ 같은 국소 법칙이 픽셀 오차를 줄인다. IBVS는 완전한
pose 복원에 덜 민감할 수 있지만 여전히 깊이 추정과 조건이 좋은 특징 기하가 필요하다. 어느 식도
시야 유지, 구동기 한계, 전역 수렴, 충돌 회피를 혼자 보장하지 않는다. "closed-loop perception"
주장은 오차·야코비안·제어 주기·깊이 출처와 국소 수렴 영역 밖의 회복을 확인해 읽는다.

### 읽고 나면 말할 수 있어야 하는 것

- 핀홀 모델로 3D 점을 손으로 투영할 수 있다
- intrinsics와 extrinsics를 구분하고 각각 언제 바뀌는지 말할 수 있다
- 단안 비전이 스케일을 잃는 이유와 스케일이 다시 들어오는 지점을 설명할 수 있다
- ICP의 루프와 초기화가 필요한 이유를 설명할 수 있다
- 카메라+LiDAR+로봇팔 시스템에 필요한 보정들을 나열할 수 있다
- reprojection error를 과신하지 않고 해석할 수 있다
- PBVS와 IBVS를 구분하고 pose·보정·깊이·image Jacobian이 루프 어디에 들어가는지 말할 수 있다
- 에지가 아니라 코너를 매칭하는 이유를 설명하고, 비율 검사·상호 검사·RANSAC으로 매칭을 거를 수 있다

> [!tip] 더 깊이 · Going deeper
> Szeliski의 [*Computer Vision: Algorithms and Applications*](https://szeliski.org/Book/)이 무료이고 이 페이지의 범위를 전부 덮는다. 다시점 기하를 정리로 봐야 할 때 — essential·fundamental 행렬, 삼각측량, 번들 조정 — 는 Hartley·Zisserman의 *Multiple View Geometry in Computer Vision*이 이 분야가 인용하는 참고서다.

### 스스로 점검

1. 위의 intrinsics로 $p^{c}=(-0.3, 0.1, 1.5)$는 어디에 투영되는가?
2. $f=600$, $b=0.12$의 스테레오에서 $Z=24$ m에 해당하는 시차는? 그것이 왜 문제인가?
3. 데이터가 완벽해도 길고 빈 복도에서 ICP가 실패할 수 있는 이유는?
4. "보정 없이" LiDAR와 카메라를 융합한다는 논문이 여전히 가정하고 있을 가능성이 큰 것은?
5. 어떤 창에서 $\sum I_x^2=40$, $\sum I_y^2=2$, $\sum I_xI_y=0$이다. $k=0.05$일 때 Harris 응답과 Shi–Tomasi 점수는 얼마이고, 어떤 종류의 점인가?
6. 똑같은 패널이 반복되는 벽에서 ORB 기술자의 가장 가까운 후보가 32비트, 두 번째가 36비트 떨어져 있다. 0.8 비율 검사를 통과하는가? 거르기를 통과한 틀린 매칭은 무엇이 잡아야 하는가?

> [!tip]- 정답 · Answers
> 1. $u = 600(-0.3)/1.5+320 = 200$, $v = 600(0.1)/1.5+240 = 280$.
> 2. $d = fb/Z = 600\cdot0.12/24 = 3$ px — ±1 px 오차가 18–36 m를 오간다; 원거리 스테레오 깊이는 취약하다.
> 3. 복도 축 방향의 병진은 점-최근접점 거리를 거의 바꾸지 않는다 — 퇴화된(관측 불가능한) 방향.
> 4. 알려진 intrinsics, 그리고 대개 대략적인 extrinsic 초기화 또는 겹침과 동기화된 타임스탬프를 여전히 요구하는 공동 최적화.
> 5. 고윳값이 40과 2이므로 $R=80-0.05\cdot42^2=-8.2<0$이고 $\min\lambda=2$다. 에지다. 밝기가 $x$ 방향으로만 바뀌므로 에지 방향인 $y$로는 위치가 잘 정해지지 않는다.
> 6. 통과하지 못한다. $32/36=0.89>0.8$이므로 버린다 — 거의 같은 후보는 옆 패널일 가능성을 뜻한다. 거르기를 통과한 틀린 매칭은 기하 검증(RANSAC)이 잡아야 하는데, 패널 한 칸만큼 통째로 밀린 집합은 그것마저 통과할 수 있으니 odometry나 독립 랜드마크와 대조하라.

### 과제 · Problem set

Tier B. 벽에 대한 거리로 **P5**([[02-foundations/lab-plants|0.6]]). hand–eye 숫자 하나: 카메라가 P2 말단보다 $4\,\mathrm{cm}$ 뒤. 시뮬레이터 없음.

1. **그리기.** 손목 카메라가 $+x$로 패널을 본다. 그 광선 위에 P5의 사전과 측정, 카메라–말단 $4\,\mathrm{cm}$.
2. **유도.** P5의 스칼라 칼만: $K$, 융합 거리, $P^+$. 융합이 카메라–벽이면 $4\,\mathrm{cm}$ 뒤 말단–벽은?
3. **해석.** $AX=XB$에서 $A,B,X$ 중 $4\,\mathrm{cm}$는 어느 것인가? $1\,\mathrm{px}$ reprojection error가 그 숫자를 보증하지 않는 이유는?

> [!tip]- 정답 · Solutions
> 1. 카메라에서 말단을 지나 벽으로 가는 광선. 사전 $10\,\mathrm{cm}$, $z=12\,\mathrm{cm}$.
> 2. $K=0.8$, 융합 $11.6\,\mathrm{cm}$, $P^+=0.8$. 말단–벽 $7.6\,\mathrm{cm}$.
> 3. $X$가 모르는 카메라–그리퍼 변환이고 $4\,\mathrm{cm}$는 $X$의 병진 성분 하나. $A$는 그리퍼 운동, $B$는 카메라 운동. 보정 부피 밖에서 $X$가 틀려도 reprojection은 작을 수 있다(§5).

### 출처

- [Szeliski, *Computer Vision: Algorithms and Applications* (공식 무료 PDF)](https://szeliski.org/Book/)
- [OpenCV 카메라 보정 튜토리얼](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [KITTI 센서 구성 — 실제 보정된 다중 센서 리그](https://www.cvlibs.net/datasets/kitti/setup.php)
- Harris, C. & Stephens, M. "A combined corner and edge detector." *Proceedings of the 4th Alvey Vision Conference*, 1988.
- Shi, J. & Tomasi, C. "Good features to track." *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 1994.
- Lowe, D. G. "Distinctive image features from scale-invariant keypoints." *International Journal of Computer Vision* 60(2), 2004. doi:10.1023/B:VISI.0000029664.99615.94
- Rublee, E., Rabaud, V., Konolige, K. & Bradski, G. "ORB: An efficient alternative to SIFT or SURF." *IEEE International Conference on Computer Vision (ICCV)*, 2011.
- Mur-Artal, R., Montiel, J. M. M. & Tardós, J. D. "ORB-SLAM: A versatile and accurate monocular SLAM system." *IEEE Transactions on Robotics* 31(5), 2015. doi:10.1109/TRO.2015.2463671
- Fischler, M. A. & Bolles, R. C. "Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography." *Communications of the ACM* 24(6), 1981. doi:10.1145/358669.358692
- DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperPoint: Self-supervised interest point detection and description." *CVPR Workshops*, 2018.
- Sarlin, P.-E., DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperGlue: Learning feature matching with graph neural networks." *CVPR*, 2020.
- Sun, J., Shen, Z., Wang, Y., Bao, H. & Zhou, X. "LoFTR: Detector-free local feature matching with transformers." *CVPR*, 2021.
