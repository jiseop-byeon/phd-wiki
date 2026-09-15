---
title: 11.8 Robotics & AI Implementation Problems
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Implement each of the ten problems from a blank file in about 20 minutes, test it with a property check, and answer the standard follow-up questions about where the method breaks."
mastery-when: "Raise to Mastery only if one of these components (a planner, an estimator, an IK solver, an attention kernel) is the part of your research you must make faster or more robust than the library version."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/graph-algorithms|11.6 Graph Algorithms & Search]] (A*) · [[02-foundations/algorithms/data-structures|11.2 Core Data Structures]] (heaps, KD-trees) · [[02-foundations/probability|3. Probability & Random Processes]] (Gaussians, Bayes' rule) · [[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]] (rotations, poses) · [[04-robotics/state-estimation-slam|3. State Estimation]] (Kalman and particle filters) · [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] (FK, Jacobian) · [[04-robotics/control-theory-ce397|5. Control Theory]] (PID) · [[02-foundations/calculus-backprop|2. Calculus & Backprop]] (gradients) · basic NumPy broadcasting
> [[02-foundations/algorithms/graph-algorithms|11.6 그래프 알고리즘과 탐색]](A*) · [[02-foundations/algorithms/data-structures|11.2 핵심 자료구조]](힙, KD-tree) · [[02-foundations/probability|3. 확률과 랜덤 프로세스]](가우시안, 베이즈 규칙) · [[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]](회전, 자세) · [[04-robotics/state-estimation-slam|3. 상태 추정]](칼만·입자 필터) · [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학]](순기구학, 야코비안) · [[04-robotics/control-theory-ce397|5. 제어 이론]](PID) · [[02-foundations/calculus-backprop|2. 미적분과 역전파]](그래디언트) · NumPy 브로드캐스팅 기초

## English

*The last page of the algorithms track, and the one closest to a lab interview. Each problem links back to the page that owns its theory; this page owns only the from-blank implementation, the traps, and the follow-up questions.*

A research-lab coding round rarely asks for a clever puzzle. It asks you to write, in 20 to 40 minutes, a small piece of the code your future lab already runs: a planner, a filter step, an inverse-kinematics solve, an attention layer. The interviewer is checking three things at once. Can you state the idea before typing? Does your code survive the input that breaks the naive version (an unreachable goal, a rotation near 180°, logits of 1000)? And when they push with "what if…", do you know where the method stops working? The ten problems below are the ones that come up most, each written so that it runs, with the tests kept in a separate file.

Every section has the same seven parts: **the prompt** as an interviewer might say it, **what is really being tested**, **the key idea**, **an implementation** of at most 35 lines (standard library plus NumPy), **complexity**, **follow-up questions** with short answers, and **the theory link**.

> [!note] First pass · 처음이라면
> If a robotics interview is next week, do §1, §4, §6 and §8 first: planning, filtering, kinematics and frames are asked in almost every lab. If the lab is closer to learning, swap §6 for §9 and §10.

### 1. Grid A* with path reconstruction

**The prompt.** *"Here is an occupancy grid, a start cell and a goal cell. The robot can move to any of its eight neighbours; diagonal steps cost √2. Return the cheapest path, or say there is none."*

**What they are really testing.** Whether you can write a priority-queue search without the three classic bugs: testing the goal when a cell is pushed instead of when it is popped, a heuristic that overestimates for this move set, and diagonal moves that slip between two obstacles touching at a corner. Returning the path, not just the cost, checks that you know to store parent pointers.

**Key idea.** Expand cells in order of $f = g + h$, where $g$ is the cost found so far and $h$ is a lower bound on the cost still to go. For 8-connected moves with diagonal cost √2 the right $h$ is the octile distance, which is the exact cost on an empty grid and therefore consistent. With a consistent $h$ the first time a cell is popped its $g$ is final, so a closed set is safe and each cell is expanded once.

```python
import heapq, math

MOVES = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]

def astar(grid, start, goal):
    """grid[r][c] == 1 is blocked; 8-connected, straight 1, diagonal sqrt(2). Returns (path, cost)."""
    def free(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 0
    def h(cell):                                   # octile distance: consistent for these moves
        dr, dc = abs(cell[0] - goal[0]), abs(cell[1] - goal[1])
        return max(dr, dc) + (math.sqrt(2) - 1) * min(dr, dc)
    if not (free(*start) and free(*goal)):
        return None, math.inf
    g, parent, closed = {start: 0.0}, {start: None}, set()
    heap = [(h(start), h(start), start)]           # (f, h, cell): equal f prefers smaller h
    while heap:
        _, _, cell = heapq.heappop(heap)
        if cell in closed:
            continue                               # stale duplicate (lazy deletion)
        if cell == goal:                           # goal test on pop, not on push
            path = []
            while cell is not None:                # walk parent pointers back to start
                path.append(cell)
                cell = parent[cell]
            return path[::-1], g[goal]
        closed.add(cell)
        r, c = cell
        for dr, dc in MOVES:
            nxt, ng = (r + dr, c + dc), g[cell] + math.hypot(dr, dc)
            if not free(*nxt) or (dr and dc and not (free(r + dr, c) and free(r, c + dc))):
                continue                           # blocked, or a diagonal that cuts a corner
            if nxt not in closed and ng < g.get(nxt, math.inf):
                g[nxt], parent[nxt] = ng, cell
                heapq.heappush(heap, (ng + h(nxt), h(nxt), nxt))
    return None, math.inf

grid = [list(map(int, row)) for row in ("00000", "01100", "00000")]
print(astar(grid, (2, 0), (0, 4)))
```

On that grid the wall occupies row 1, columns 1–2, so the path runs along the bottom and takes one diagonal step, (2, 3) to (1, 4), for a cost of $4 + \sqrt 2$. The step from (2, 2) to (1, 3) is refused, because it would squeeze past the corner of the wall at (1, 2).

**Complexity.** With $n$ free cells there are at most $8n$ edges, so at most $8n$ heap pushes. Each push or pop costs $O(\log n)$, giving $O(n \log n)$ time and $O(n)$ memory for `g`, `parent` and the heap. The heap can hold stale duplicates; skipping them on pop is cheaper than a decrease-key operation, which `heapq` does not have.

**Follow-ups they ask.**
- *Why not Manhattan distance here?* It overestimates a diagonal move: one diagonal step costs √2 ≈ 1.41 but Manhattan says 2. An overestimating $h$ can return a longer path.
- *The grid has per-cell traversal costs.* Use $g$ + cost of the entered cell, and scale $h$ by the smallest cost any cell can have, so it remains a lower bound.
- *It is too slow on a 4000 × 4000 map.* Weighted A* ($g + \varepsilon h$, cost at most $\varepsilon$ times optimal), jump point search on uniform-cost grids, a coarser grid or hierarchy, and a bidirectional search are the standard answers. Also check the constant factors: tuples in a dict are slow, and a flat NumPy array indexed by `r * cols + c` is faster.
- *The map changes as the robot drives.* Replanning from scratch is fine for small maps. Incremental planners such as D* Lite repair the previous search instead.
- *Is the result a good robot path?* It is optimal on the grid, not in the plane: it is a staircase that hugs obstacles. Inflate obstacles by the robot radius first and smooth the path afterwards.

**Theory.** The correctness argument (consistency, reduced costs, tie-breaking) is in [[02-foundations/algorithms/graph-algorithms|11.6 §6]]; what a planner does with the path is in [[04-robotics/planning-decision-making|4. Planning & Decision-Making §3]].

### 2. Nearest neighbours: vectorized brute force and a KD-tree

**The prompt.** *"Given $n$ points in 3-D and $m$ query points, find each query's nearest point. First the simplest correct version, then something faster."*

**What they are really testing.** NumPy fluency (broadcasting without a Python loop, and without building an $m \times n \times d$ array), knowing that a partial selection is cheaper than a sort, and whether you understand *why* a KD-tree prunes, and when it stops helping.

**Key idea.** For brute force, expand the squared distance: $\lVert q - p\rVert^2 = \lVert q\rVert^2 - 2\,q^\top p + \lVert p\rVert^2$, so one matrix product gives all $m \times n$ distances. For a KD-tree, split the points at the median of the widest coordinate, recursively. At query time, descend into the side containing the query first, then visit the other side only if the splitting plane is closer than the best distance found so far, since every point beyond the plane is at least that far away.

```python
import numpy as np

def knn_brute(P, Q, k=1):
    """P: (n, d) points, Q: (m, d) queries. Returns (m, k) indices and squared distances, nearest first."""
    d2 = (Q**2).sum(1)[:, None] - 2.0 * Q @ P.T + (P**2).sum(1)[None, :]   # (m, n)
    np.maximum(d2, 0.0, out=d2)                     # round-off can make ~0 slightly negative
    idx = np.argpartition(d2, k - 1, axis=1)[:, :k] # the k smallest per row, unordered: O(n)
    dk = np.take_along_axis(d2, idx, axis=1)
    order = np.argsort(dk, axis=1)
    return np.take_along_axis(idx, order, 1), np.take_along_axis(dk, order, 1)

def kd_build(P, idx, leaf=16):
    """Nodes are ('leaf', indices) or ('split', axis, value, left, right)."""
    if len(idx) <= leaf:
        return ("leaf", idx)
    axis = int(np.argmax(np.ptp(P[idx], axis=0)))  # split the widest dimension
    mid = len(idx) // 2
    idx = idx[np.argpartition(P[idx, axis], mid)]  # median in O(n), not a full sort
    left, right = kd_build(P, idx[:mid], leaf), kd_build(P, idx[mid:], leaf)
    return ("split", axis, P[idx[mid], axis], left, right)

def kd_nearest(node, P, q, best=(np.inf, -1)):
    """Returns (squared distance, index) of the point in P nearest to q."""
    if node[0] == "leaf":
        pts = node[1]
        d2 = ((P[pts] - q) ** 2).sum(1)
        i = int(np.argmin(d2))
        return min(best, (d2[i], int(pts[i])))
    _, axis, value, left, right = node
    diff = q[axis] - value
    near, far = (left, right) if diff < 0 else (right, left)
    best = kd_nearest(near, P, q, best)
    if diff * diff < best[0]:                       # the ball around q crosses the plane
        best = kd_nearest(far, P, q, best)
    return best

rng = np.random.default_rng(0)
P = rng.random((10_000, 3)); q = rng.random(3)
tree = kd_build(P, np.arange(len(P)))
print(kd_nearest(tree, P, q)[1], knn_brute(P, q[None, :], k=1)[0][0, 0])
```

**Complexity.** Brute force: $O(mnd)$ time and an $m \times n$ distance matrix, so process queries in chunks when $mn$ is large. `argpartition` selects the $k$ smallest in $O(n)$ per row, and only those $k$ are sorted. KD-tree build: each level does $O(n)$ work (median by `argpartition`, spread by `ptp`) over $O(\log n)$ levels, so $O(n \log n)$. A query is $O(\log n)$ expected in low dimension on well-spread data and $O(n)$ in the worst case.

**Follow-ups they ask.**
- *What is the `np.maximum` line for?* The expanded form can produce $-10^{-12}$ for a point equal to the query; clip at zero before a square root.
- *k nearest instead of one?* Keep a max-heap of the best $k$; prune with the distance to the $k$-th best.
- *Radius search?* Same descent; prune a side when the plane is farther than the radius.
- *When would you not use a KD-tree?* For 512-D embeddings (pruning fails, use approximate methods such as HNSW), for a fixed radius at a known scale (a voxel hash grid is expected $O(1)$), and for a one-off batch small enough that the vectorized brute force finishes first.
- *Would you write this in production?* No: use `scipy.spatial.cKDTree`, `nanoflann`, or the KD-tree inside Open3D or PCL. Writing it once is how you learn what their `leaf_size` and approximate-search parameters trade.
- *The tree must grow, as in RRT.* Insert into leaves and rebuild when unbalanced, or keep a few trees of doubling size.

**Theory.** Why pruning works and why it fails in high dimension: [[02-foundations/algorithms/data-structures|11.2 §8]].

### 3. RANSAC line fitting

**The prompt.** *"A 2-D laser scan of a wall has 40 % of its points on clutter. Fit the wall's line. How many random samples do you need?"*

**What they are really testing.** That you know least squares breaks with gross outliers, that you pick a *minimal* sample (two points for a line), that you can derive the iteration count rather than recite it, and that you finish with a refit on the inliers.

**Key idea.** Repeatedly fit a line to two random points and count the points within a distance threshold; keep the line with the most inliers, then refit it by total least squares on those inliers. How many repetitions? If a fraction $w$ of points are inliers, one sample of $s$ points is all inliers with probability $w^s$, so all $k$ independent samples are contaminated with probability $(1 - w^s)^k$. Requiring that to be at most $1 - p$ and taking logarithms gives the count, where the inequality flips because both logarithms are negative:

$$k = \left\lceil \frac{\log(1 - p)}{\log(1 - w^{s})} \right\rceil$$

```python
import math
import numpy as np

def ransac_iterations(p, w, s):
    """Samples k so that, with probability p, at least one size-s sample is all inliers (inlier ratio w)."""
    return math.ceil(math.log(1 - p) / math.log(1 - w**s))

def ransac_line(pts, thresh, k, rng):
    """pts: (N, 2). Line n . x = c with unit normal n. Returns (n, c, inlier mask) or None."""
    best = np.zeros(len(pts), dtype=bool)
    for _ in range(k):
        i, j = rng.choice(len(pts), size=2, replace=False)   # minimal sample: s = 2
        t = pts[j] - pts[i]
        if np.hypot(*t) < 1e-12:
            continue                                         # coincident points: no line
        n = np.array((-t[1], t[0])) / np.hypot(*t)
        inliers = np.abs(pts @ n - n @ pts[i]) < thresh      # perpendicular distances
        if inliers.sum() > best.sum():
            best = inliers
    if best.sum() < 2:
        return None
    X = pts[best]                                            # refit on the consensus set:
    mu = X.mean(axis=0)                                      # total least squares, the normal is
    n = np.linalg.svd(X - mu)[2][-1]                         # the least-variance direction
    return n, n @ mu, np.abs(pts @ n - n @ mu) < thresh

rng = np.random.default_rng(1)
x = rng.uniform(0, 10, 60)
line = np.column_stack([x, 0.5 * x + 1 + rng.normal(0, 0.05, 60)])   # y = 0.5 x + 1
outliers = rng.uniform(0, 10, (40, 2))
n, c, mask = ransac_line(np.vstack([line, outliers]), 0.2, ransac_iterations(0.99, 0.6, 2), rng)
print(ransac_iterations(0.99, 0.6, 2), -n[0] / n[1], c / n[1], mask[:60].mean())
```

> [!example] Worked example · 계산 예제
> With $p = 0.99$ and half the points outliers ($w = 0.5$): a line ($s = 2$) needs $\log 0.01 / \log 0.75 = 16.0$, so **17** samples; a plane ($s = 3$) needs **35**; the 8-point fundamental-matrix estimate ($s = 8$) needs **1177**. The inlier ratio matters as much as $s$: a plane with $w = 0.3$ needs **169**. The test file checks each value and then simulates 20 000 runs of $k$ samples, confirming the success rate matches $1 - (1 - w^s)^k \ge p$ and that $k - 1$ samples fall short.

**Complexity.** $O(kN)$: each of $k$ iterations scores all $N$ points. The refit is $O(N)$. Note that $k$ does not depend on $N$, only on $w$, $s$ and $p$, which is why RANSAC scales to large clouds.

**Follow-ups they ask.**
- *You do not know $w$.* Start with a pessimistic $w$, and every time a better consensus set appears, update $w$ to its inlier fraction and recompute $k$. The loop usually ends far earlier.
- *How do you choose the threshold?* From the noise: for Gaussian noise of standard deviation $\sigma$ on a point-to-line distance, a threshold near $1.96\sigma$ keeps about 95 % of true inliers.
- *Why refit, and why total least squares?* The two-point line uses only two noisy points. Ordinary least squares on $y$ fails for vertical lines; the smallest singular vector of the centred inliers gives the normal for any orientation.
- *Several walls?* Fit one line, remove its inliers, repeat (sequential RANSAC), or use a multi-model method.
- *Better scoring?* MSAC and MLESAC score inliers by their residuals instead of counting them, which breaks ties between lines that capture the same number of points.
- *The formula assumed independent samples with replacement.* True; sampling without replacement from a finite set is slightly better, so the formula is a mild overestimate.

**Theory.** Registration and why geometric pipelines must handle outliers before optimizing: [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration §4]].

### 4. One linear Kalman filter step

**The prompt.** *"A target moves along a line at roughly constant velocity. You get noisy position readings every 0.1 s. Write one predict and one update step of a Kalman filter."*

**What they are really testing.** Getting the shapes right, writing $Q$ from a physical noise model instead of `np.eye(2) * 0.01`, not calling `np.linalg.inv`, and knowing why the textbook covariance update drifts and what the Joseph form fixes.

**Key idea.** The notation follows [[04-robotics/state-estimation-slam|3. State Estimation §5]] and [[02-foundations/probability|3. Probability §5]]: state $x = (\text{position}, \text{velocity})$, dynamics $A$, process noise covariance $Q$, measurement matrix $H$ (written $C$ on the probability page), measurement noise $R$, and estimate covariance $P$. Predict pushes the Gaussian through the dynamics: $x^- = Ax$ and $P^- = AP A^\top + Q$. Update conditions on the reading $z$: innovation $y = z - Hx^-$, its covariance $S = HP^-H^\top + R$, gain $K = P^-H^\top S^{-1}$, then $x = x^- + Ky$. For the covariance, use the Joseph form, which is symmetric and positive semidefinite by construction because it is a sum of two congruences, terms of the form $MXM^\top$ with $X$ symmetric positive semidefinite, each of which is again symmetric positive semidefinite since $v^\top MXM^\top v = (M^\top v)^\top X (M^\top v) \ge 0$:

$$P = (I - KH)\,P^-\,(I - KH)^\top + K R K^\top$$

For a white acceleration of standard deviation $\sigma_a$ held over each step, the state changes by $G a$ with $G = (\tfrac12 \Delta t^2, \Delta t)^\top$, so $Q = \sigma_a^2 G G^\top$.

```python
import numpy as np

def cv_model(dt, sigma_a, sigma_z):
    """Constant velocity, state x = [position, velocity]; a white acceleration drives it."""
    A = np.array([ [1.0, dt], [0.0, 1.0] ])
    G = np.array([ [0.5 * dt**2], [dt] ])        # how one acceleration sample enters x
    Q = sigma_a**2 * (G @ G.T)
    H = np.array([ [1.0, 0.0] ])                 # we measure position only
    R = np.array([ [sigma_z**2] ])
    return A, Q, H, R

def kf_predict(x, P, A, Q):
    return A @ x, A @ P @ A.T + Q

def kf_update(x, P, z, H, R):
    y = z - H @ x                                # innovation, shape (1,)
    S = H @ P @ H.T + R                          # innovation covariance, (1, 1)
    K = np.linalg.solve(S, H @ P).T              # K = P H^T S^-1 without an explicit inverse
    I_KH = np.eye(len(x)) - K @ H
    P = I_KH @ P @ I_KH.T + K @ R @ K.T          # Joseph form: symmetric, PSD, any gain K
    return x + K @ y, P

A, Q, H, R = cv_model(dt=0.1, sigma_a=0.5, sigma_z=0.3)
x, P = np.array([0.0, 1.0]), np.eye(2)
x, P = kf_predict(x, P, A, Q)
x, P = kf_update(x, P, np.array([0.12]), H, R)
print(x.round(4), P.round(4))
```

> [!example] Worked example · 계산 예제
> The scalar case from the state-estimation page, run through this code: predicted position $10$ with variance $4$, a reading $z = 12$ with $R = 1$, $H = (1, 0)$. Then $S = 5$, $K = (0.8, 0)^\top$, the position becomes $10 + 0.8 \cdot 2 = 11.6$ and its variance $(1 - 0.8)^2 \cdot 4 + 0.8^2 \cdot 1 = 0.8$, the same $0.8$ that $(1-K)P^-$ gives, as it must for the optimal gain. The test file asserts these numbers and also runs 3000 steps on simulated data: the filtered position error is less than half the raw measurement error, and the average normalized estimation error squared is close to 2, the state dimension, which is what a consistent filter should show.

**Complexity.** For state dimension $n$ and measurement dimension $m$: $O(n^3)$ for the covariance products and $O(m^3)$ for the solve with $S$, per step. Here both are constants.

**Follow-ups they ask.**
- *Why not `P = (I - K H) @ P`?* It is correct only for the exact optimal gain and in exact arithmetic. Round-off makes it lose symmetry and eventually positive definiteness. The Joseph form stays valid for any gain, including a suboptimal one. The cheap alternative is symmetrizing, `P = 0.5 * (P + P.T)`.
- *Why `solve` instead of `inv`?* It is cheaper and more accurate. For larger problems use a Cholesky factorization of $S$.
- *A measurement is an outlier.* Gate it: accept only if $y^\top S^{-1} y$ is below a chi-square threshold (3.84 for one dimension at 95 %).
- *A reading is missing, or two sensors arrive at different rates.* Skip the update when nothing arrives; predict to each measurement's timestamp and update with that sensor's $H$ and $R$.
- *How do you tune $Q$ and $R$?* $R$ from a static sensor log; $Q$ from the physics of how much the target can accelerate, then check consistency (normalized innovations should average to $m$).
- *The model is nonlinear.* EKF: linearize $f$ and $h$ at the current estimate and use their Jacobians in place of $A$ and $H$.

**Theory.** Where predict and update come from: [[04-robotics/state-estimation-slam|3. State Estimation §4]], and the Gaussian identities behind them in [[02-foundations/probability|3. Probability §5]].

### 5. Particle filter resampling

**The prompt.** *"Your particle filter has $M$ weighted particles. Implement resampling. Why is the simple way not the best way, and when should you resample at all?"*

**What they are really testing.** Whether you know resampling's purpose (fighting weight degeneracy) and its cost (losing diversity), the effective sample size criterion, the difference between multinomial and systematic resampling, and numerical care with likelihoods that underflow.

**Key idea.** Multinomial resampling draws $M$ independent indices from the weights, so a particle with weight $w_i$ gets a random number of copies with mean $M w_i$ and binomial spread. Systematic resampling uses one random offset $u_0 \in [0, 1)$ and the $M$ evenly spaced pointers $u_m = (u_0 + m)/M$, each picking the particle whose cumulative-weight interval contains it. Each $u_m$ is uniform on its own, so every copy count still has mean $M w_i$, but the count is always $\lfloor M w_i\rfloor$ or $\lceil M w_i\rceil$, which removes most of the randomness. Resample only when the effective sample size $M_{\text{eff}} = 1/\sum_i w_i^2$ falls below a threshold, commonly $M/2$.

```python
import numpy as np

def normalize_log_weights(logw):
    """Log-likelihoods -> normalized weights, without underflow (subtract the max first)."""
    w = np.exp(logw - logw.max())
    return w / w.sum()

def effective_sample_size(w):
    return 1.0 / np.sum(w**2)                    # M for uniform weights, 1 if one particle has all

def multinomial_resample(w, rng):
    """M independent draws from the categorical distribution w."""
    return rng.choice(len(w), size=len(w), p=w)

def systematic_resample(w, rng):
    """One uniform offset, M evenly spaced pointers through the cumulative weights."""
    M = len(w)
    cdf = np.cumsum(w)
    cdf[-1] = 1.0                                # round-off must not leave a pointer past the end
    u = (rng.random() + np.arange(M)) / M        # u_m = (u_0 + m) / M, u_0 ~ U[0, 1)
    return np.searchsorted(cdf, u, side="right") # index i with cdf[i-1] <= u < cdf[i]

def resample_if_needed(particles, w, rng, threshold=0.5):
    if effective_sample_size(w) < threshold * len(w):
        idx = systematic_resample(w, rng)
        particles, w = particles[idx], np.full(len(w), 1.0 / len(w))
    return particles, w

rng = np.random.default_rng(0)
w = normalize_log_weights(np.array([-1000.0, -1001.0, -1003.0, -1010.0]))
print(w.round(4), effective_sample_size(w).round(3), np.bincount(systematic_resample(w, rng), minlength=4))
```

> [!example] Worked example · 계산 예제
> Weights $(0.10, 0.45, 0.35, 0.10)$ give cumulative sums $(0.10, 0.55, 0.90, 1.00)$. With $u_0 = 0.8$ the pointers are $0.20, 0.45, 0.70, 0.95$, which land in particles $1, 1, 2, 3$: copy counts $(0, 2, 1, 1)$ against expectations $(0.4, 1.8, 1.4, 0.4)$, each a floor or ceiling. The test file runs 40 000 resamplings of random weights and checks three things: the mean count of every particle matches $M w_i$ for both schemes, every systematic count is a floor or ceiling, and the total variance of the systematic counts is below the multinomial one.

**Complexity.** Both schemes as written are $O(M \log M)$, a binary search per draw. Because the systematic pointers are already sorted, a two-pointer walk through the cumulative sum makes it $O(M)$. ESS is $O(M)$.

**Follow-ups they ask.**
- *Why resample at all?* Without it, after a few updates almost all weight sits on one particle and the other particles cost compute while contributing nothing.
- *Then why not every step?* Resampling duplicates particles; with little process noise the copies stay identical and the set collapses to a few distinct states (sample impoverishment). Resampling adaptively, and adding a small jitter after it, reduces this.
- *Why log weights?* A product of many likelihoods underflows to zero in float64. Keep log weights and subtract the maximum before exponentiating.
- *Is systematic always better?* In practice it has lower variance and is the standard choice; it is not a theorem for every particle ordering. Stratified and residual resampling are the other common options.
- *How many particles?* The number needed grows quickly with state dimension, which is why particle filters live in 2-D and 3-D localization, and why adaptive schemes such as KLD-sampling vary $M$ with how spread the belief is.

**Theory.** Particle filters among the other estimator families, and particle depletion: [[04-robotics/state-estimation-slam|3. State Estimation §5]].

### 6. Two-link planar arm: FK, analytic IK, one damped IK step

**The prompt.** *"A planar arm has link lengths $L_1$ and $L_2$. Write forward kinematics. Then solve inverse kinematics for a target $(x, y)$: give both solutions, and handle targets it cannot reach. Finally, take one numerical IK step that does not blow up at a singularity."*

**What they are really testing.** Using `atan2` rather than `arccos` or `arctan` alone, knowing there are zero, one or two solutions, clipping round-off at the workspace boundary, and knowing why the plain Jacobian inverse fails when the arm is straight.

**Key idea.** Forward kinematics is the sum of two rotated links, as in Lynch and Park's two-link example. For the inverse, the law of cosines gives $\cos\theta_2 = (x^2 + y^2 - L_1^2 - L_2^2)/(2L_1L_2)$. If it lies outside $[-1, 1]$, the target is outside the annulus $\lvert L_1 - L_2\rvert \le r \le L_1 + L_2$ and there is no solution. Otherwise $\sin\theta_2 = \pm\sqrt{1 - \cos^2\theta_2}$ picks the branch, and $\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin\theta_2, L_1 + L_2\cos\theta_2)$. Branch names vary between books; the sign of $\theta_2$ is the unambiguous label, and here $\theta_2 \ge 0$ is called elbow-down (righty), as in Modern Robotics.

The numerical step is a separate idea. With tip error $e = (x, y)_{\text{target}} - \text{FK}(\theta)$, the damped least-squares step is $\Delta\theta = J^\top (JJ^\top + \lambda^2 I)^{-1} e$. When the arm is straight or folded, $J$ loses rank and $J^{-1}$ does not exist; for $\lambda > 0$ the matrix $JJ^\top + \lambda^2 I$ is always invertible, so the step stays finite (see the follow-ups).

```python
import numpy as np

def fk(theta, L1=1.0, L2=1.0):
    t1, t2 = theta
    return np.array([L1 * np.cos(t1) + L2 * np.cos(t1 + t2), L1 * np.sin(t1) + L2 * np.sin(t1 + t2)])

def ik(x, y, L1=1.0, L2=1.0, elbow="down"):
    """Analytic IK. 'down' (righty) has theta2 >= 0, 'up' (lefty) theta2 <= 0. None if unreachable."""
    c2 = (x * x + y * y - L1 * L1 - L2 * L2) / (2 * L1 * L2)   # law of cosines
    if abs(c2) > 1 + 1e-9:
        return None                              # outside the annulus |L1 - L2| <= r <= L1 + L2
    c2 = np.clip(c2, -1.0, 1.0)                  # a boundary target must not give sqrt(-1e-16)
    s2 = np.sqrt(1 - c2 * c2) * (1.0 if elbow == "down" else -1.0)
    t1 = np.arctan2(y, x) - np.arctan2(L2 * s2, L1 + L2 * c2)
    return np.array([t1, np.arctan2(s2, c2)])

def jacobian(theta, L1=1.0, L2=1.0):
    t1, t2 = theta
    s1, c1, s12, c12 = np.sin(t1), np.cos(t1), np.sin(t1 + t2), np.cos(t1 + t2)
    return np.array([ [-L1 * s1 - L2 * s12, -L2 * s12], [L1 * c1 + L2 * c12, L2 * c12] ])

def dls_step(theta, target, lam=0.1, L1=1.0, L2=1.0):
    """One damped-least-squares step: dtheta = J^T (J J^T + lam^2 I)^-1 e."""
    J, e = jacobian(theta, L1, L2), target - fk(theta, L1, L2)
    return theta + J.T @ np.linalg.solve(J @ J.T + lam**2 * np.eye(2), e)

target = np.array([-1.0, 1.0])
for elbow in ("down", "up"):
    th = ik(*target, elbow=elbow)
    print(elbow, np.degrees(th).round(1), fk(th).round(6))
print(ik(2.5, 0.0))                              # None: beyond reach
print(np.degrees(dls_step(np.radians([45.0, 90.0]), target, lam=0.0)).round(1))
```

The last line reproduces the hand iteration on [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6 §3]]: from $(45°, 90°)$ toward $(-1, 1)$, one undamped step lands at $(68.7°, 123.6°)$. The two analytic solutions for that target are $(90°, 90°)$ and $(180°, -90°)$.

**Complexity.** All $O(1)$. For an $n$-joint arm with an $m$-dimensional task, one damped step costs $O(m^2 n + m^3)$: form $JJ^\top$ and solve an $m \times m$ system.

**Follow-ups they ask.**
- *Where are the singularities?* $\det J = L_1 L_2 \sin\theta_2$, so at $\theta_2 = 0$ (straight) and $\theta_2 = \pi$ (folded). There the arm cannot move its tip along the link direction, and $J^{-1}$ is infinite.
- *What does $\lambda$ trade?* Accuracy for bounded joint steps. Near a singularity, damping keeps $\Delta\theta$ finite but the step no longer reaches the target in the linear model. Choose $\lambda$ small, or increase it only as the smallest singular value of $J$ shrinks.
- *Why $J^\top(JJ^\top + \lambda^2 I)^{-1}$ and not $(J^\top J + \lambda^2 I)^{-1}J^\top$?* They are equal. The first solves an $m \times m$ system, cheaper when the arm is redundant ($n > m$).
- *Which of the two analytic solutions do you send?* The one within joint limits and closest to the current configuration, measuring angle differences with wrap-around.
- *Target exactly at the base with $L_1 = L_2$?* Infinitely many solutions: any $\theta_1$ with $\theta_2 = \pi$. The code returns one; say so.
- *Numerical IK does not converge.* Distinguish unreachable, a bad initial guess, a singularity, and an iteration budget. One failed local search does not prove there is no solution.

**Theory.** Analytic versus numerical IK, Newton–Raphson, and damped least squares: [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6 §4]]; the forward-kinematics and Jacobian results this builds on: [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §1]].

### 7. Discrete PID with derivative on measurement and anti-windup

**The prompt.** *"Write a PID controller that runs at 100 Hz on a real motor. The actuator saturates. Test it on a first-order plant."*

**What they are really testing.** Whether you know the three fixes that separate a textbook PID from one that runs on hardware: take the derivative of the measurement, not the error, so a setpoint step does not produce a spike; low-pass the derivative, because differentiating noise amplifies it; and stop integrating while the output is saturated in the direction the error pushes, which is anti-windup.

**Key idea.** The control law from [[04-robotics/control-theory-ce397|5. Control Theory §7]] is $u = K_p e + K_i \int e\,dt + K_d \dot e$ with $e = r - y$. For a constant setpoint $\dot e = -\dot y$, so replacing $K_d\dot e$ by $-K_d\dot y$ changes nothing between setpoint changes and removes the kick at them. Clamp $u$ to the actuator range, and commit the integrator update only when it would not drive $u$ further into the limit (conditional integration). The plant $\tau\dot y = -y + Ku$ under a zero-order hold is simulated exactly by $y_{k+1} = a y_k + K(1 - a)u_k$ with $a = e^{-\Delta t/\tau}$.

```python
import math

class PID:
    """Discrete PID: derivative on measurement, filtered D, clamped output, conditional integration."""
    def __init__(self, kp, ki, kd, dt, u_min, u_max, tau_d=0.0):
        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt
        self.u_min, self.u_max = u_min, u_max
        self.alpha = dt / (tau_d + dt)           # first-order low-pass on the derivative
        self.i_term, self.d_filt, self.y_prev = 0.0, 0.0, None

    def update(self, r, y):
        e = r - y
        dy = 0.0 if self.y_prev is None else (y - self.y_prev) / self.dt
        self.y_prev = y
        self.d_filt += self.alpha * (dy - self.d_filt)
        i_next = self.i_term + self.ki * e * self.dt           # stores Ki * integral, not the integral
        u_raw = self.kp * e + i_next - self.kd * self.d_filt   # minus: D acts on y, not on e
        u = min(self.u_max, max(self.u_min, u_raw))
        pushing_further = (u_raw > self.u_max and e > 0) or (u_raw < self.u_min and e < 0)
        if not pushing_further:                                # anti-windup: freeze I while it
            self.i_term = i_next                               # would drive deeper into the limit
        return u

def simulate(pid, r=1.0, tau=0.5, gain=1.0, steps=600):
    """First-order plant tau * dy/dt = -y + gain * u, discretized exactly under zero-order hold."""
    a, y, ys = math.exp(-pid.dt / tau), 0.0, []
    for _ in range(steps):
        u = pid.update(r, y)
        y = a * y + gain * (1 - a) * u
        ys.append(y)
    return ys

ys = simulate(PID(kp=2.0, ki=4.0, kd=0.05, dt=0.01, u_min=0.0, u_max=1.5, tau_d=0.02))
print(round(max(ys), 4), round(ys[-1], 4))
```

**Complexity.** $O(1)$ time and memory per update.

**Follow-ups they ask.**
- *Show that anti-windup matters.* The test file runs $K_p = 1$, $K_i = 5$ with limits $\pm 1.2$ on that plant. The version above overshoots the setpoint by about 4 %; the same controller integrating unconditionally overshoots by about 15 %, because the integral it accumulated during saturation must be unwound by negative error.
- *Show derivative on measurement matters.* With $K_d = 1$ and $\Delta t = 0.01$, a unit setpoint step through derivative-on-error adds $K_d \cdot 1/\Delta t = 100$ to one sample. The code above adds nothing, and the test checks it.
- *Other anti-windup schemes?* Back-calculation feeds the difference between saturated and unsaturated output back into the integrator with a tracking time constant. It unwinds more smoothly than clamping.
- *Why store $K_i\int e$ rather than $\int e$?* Changing $K_i$ online then does not make the output jump (bumpless gain change).
- *How do you choose the derivative filter?* A time constant of roughly $T_d/N$ with $T_d = K_d/K_p$ and $N$ between about 5 and 20. Its lag reduces phase margin, so do not filter harder than the noise requires.
- *The loop period jitters.* Measure the actual $\Delta t$ each call, and guard against $\Delta t = 0$.

**Theory.** What each term does to the closed loop, integral windup, and phase margin: [[04-robotics/control-theory-ce397|5. Control Theory §7]].

### 8. Rigid transforms and rotation-matrix-to-quaternion conversion

**The prompt.** *"Compose and invert 4 × 4 poses. Then convert a rotation matrix to a unit quaternion in a way that never divides by zero, and test it."*

**What they are really testing.** Frame discipline ($T_{AC} = T_{AB}T_{BC}$), the closed-form inverse, the quaternion convention you are using, and whether you know the common one-line conversion fails near 180°.

**Key idea.** The inverse of a pose is $(R, p)^{-1} = (R^\top, -R^\top p)$, from [[02-foundations/se3-geometry|8. SE(3) §3]]. For quaternions this page uses that page's scalar-first order $q = (w, x, y, z)$, the same as Modern Robotics' $(q_0, q_1, q_2, q_3)$. The diagonal of $R$ determines every squared component. For a unit quaternion $R_{11} = 1 - 2(y^2 + z^2)$, $R_{22} = 1 - 2(x^2 + z^2)$ and $R_{33} = 1 - 2(x^2 + y^2)$, so $\operatorname{tr}R = 3 - 4(x^2 + y^2 + z^2) = 4w^2 - 1$. Hence $4w^2 = 1 + \operatorname{tr}R$ and $4x^2 = 1 + 2R_{11} - \operatorname{tr}R$, and likewise for $y$ and $z$. The familiar formula computes $w$ this way and then divides the off-diagonal differences by $4w$. Near a 180° rotation $w \to 0$ and that division is unstable. The fix is to solve for the *largest* component first. Because the four squares sum to 1, the largest has $\lvert q_i\rvert \ge 1/2$, so every division is by at least 2. The other three components then come from sums or differences of symmetric off-diagonal pairs.

```python
import numpy as np

def make_T(R, p):
    T = np.eye(4)
    T[:3, :3], T[:3, 3] = R, p
    return T

def inv_T(T):
    """Closed-form inverse: (R, p)^-1 = (R^T, -R^T p). Never np.linalg.inv on a pose."""
    R, p = T[:3, :3], T[:3, 3]
    return make_T(R.T, -R.T @ p)

Rz90 = np.array([ [0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0] ])
T_AB = make_T(Rz90, [2.0, 0.0, 0.0])             # base in world
T_BC = make_T(np.eye(3), [1.0, 0.0, 0.0])        # camera in base
T_AC = T_AB @ T_BC                               # subscripts cancel: A<-B<-C
print(T_AC[:3, 3], np.allclose(inv_T(T_AC) @ T_AC, np.eye(4)))
```

```python
import numpy as np

def quat_to_rot(q):
    """Unit quaternion q = (w, x, y, z), scalar first, to a rotation matrix."""
    w, x, y, z = q
    return np.array([ [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                      [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                      [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)] ])

def rot_to_quat(R):
    """Rotation matrix to unit quaternion (w, x, y, z) with w >= 0. Solves for the largest
    component first, so no division by a number near zero (the trace-only formula fails near 180 deg)."""
    t = np.trace(R)
    four_sq = np.array([1 + t, 1 + 2 * R[0, 0] - t, 1 + 2 * R[1, 1] - t, 1 + 2 * R[2, 2] - t])  # 4 q_i^2
    i = int(np.argmax(four_sq))
    s = 2.0 * np.sqrt(four_sq[i])                # s = 4 |q_i|
    sums = {"xy": R[0, 1] + R[1, 0], "xz": R[0, 2] + R[2, 0], "yz": R[1, 2] + R[2, 1]}
    difs = {"x": R[2, 1] - R[1, 2], "y": R[0, 2] - R[2, 0], "z": R[1, 0] - R[0, 1]}  # each = 4 w q_axis
    q = {0: [s / 4, difs["x"] / s, difs["y"] / s, difs["z"] / s],
         1: [difs["x"] / s, s / 4, sums["xy"] / s, sums["xz"] / s],
         2: [difs["y"] / s, sums["xy"] / s, s / 4, sums["yz"] / s],
         3: [difs["z"] / s, sums["xz"] / s, sums["yz"] / s, s / 4]}[i]
    q = np.array(q) / np.linalg.norm(q)          # absorb round-off from a slightly non-orthogonal R
    return q if q[0] >= 0 else -q                # q and -q are the same rotation: pick one

theta = np.radians(179.9)                        # near 180 deg, where w = cos(theta/2) ~ 0
q = np.array([np.cos(theta / 2), 0.0, np.sin(theta / 2), 0.0])
print(rot_to_quat(quat_to_rot(q)).round(6), q.round(6))
```

**Complexity.** $O(1)$. Inverting with `np.linalg.inv` is also $O(1)$ at this size, but it ignores structure, is slower, and returns a matrix whose rotation block is not exactly orthonormal.

**How it is tested.** Random rotations are generated by normalizing a 4-D Gaussian vector, which gives a uniformly random unit quaternion. For 20 000 of them the test converts to a matrix and back and checks the result equals $q$ or $-q$ and has $w \ge 0$. It checks angles of $\pi$, $\pi - 10^{-9}$ and $\pi - 10^{-4}$ about each axis, compares against quaternions built independently from axis-angle through Rodrigues' formula, and checks that `inv_T` matches the general inverse and that $(T_aT_b)^{-1} = T_b^{-1}T_a^{-1}$.

**Follow-ups they ask.**
- *Which order do libraries use?* Not the same one. Eigen's constructor takes $(w, x, y, z)$ but stores $(x, y, z, w)$; ROS messages and SciPy's default are scalar-last. Most quaternion bugs are an order mismatch, so name the order in every function signature.
- *Why flip to $w \ge 0$?* $q$ and $-q$ are the same rotation. A canonical sign makes outputs comparable and keeps a learned regression target from jumping. It does not make the representation continuous at $w = 0$.
- *Angle between two orientations?* $2\arccos\lvert\langle q_1, q_2\rangle\rvert$; the absolute value handles the double cover.
- *Your integrated rotation matrix drifts from orthonormal.* Project it back with an SVD ($R \leftarrow UV^\top$) or keep a quaternion and renormalize it.
- *How do you compose quaternions?* The Hamilton product $q_1 \otimes q_2$ corresponds to $R_1R_2$ in this convention. Check it numerically against the matrices, as for everything else here.

**Theory.** The four rotation representations and pose composition: [[02-foundations/se3-geometry|8. SE(3) §2]] and [[02-foundations/se3-geometry|8. SE(3) §3]].

### 9. Stable softmax, log-softmax and cross-entropy, with a gradient check

**The prompt.** *"Implement softmax and a cross-entropy loss from logits in NumPy, with its gradient. It must not return NaN for logits in the thousands. Prove the gradient is right."*

**What they are really testing.** The shift trick, never computing `log(softmax(z))`, the $p - y$ gradient including the $1/N$ of a mean loss, and knowing how to write a finite-difference gradient check and pick its step size.

**Key idea.** Softmax is unchanged when a constant is subtracted from every logit, so subtract the maximum: the largest exponent becomes $e^0 = 1$ and nothing overflows. Log-softmax is then $z_j - \log\sum_k e^{z_k}$ (log-sum-exp), computed without ever taking the log of a number that has rounded to zero. For a mean cross-entropy over $N$ examples the gradient with respect to the logits is $(p - y)/N$, derived on [[02-foundations/calculus-backprop|2. Calculus & Backprop §4]].

```python
import numpy as np

def log_softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)      # shift invariance: largest logit becomes 0, no overflow
    return z - np.log(np.exp(z).sum(axis=axis, keepdims=True))   # log-sum-exp

def softmax(z, axis=-1):
    return np.exp(log_softmax(z, axis))

def cross_entropy(logits, labels):
    """logits (N, C), integer labels (N,). Returns mean loss and dL/dlogits, shape (N, C)."""
    N = logits.shape[0]
    lp = log_softmax(logits)
    loss = -lp[np.arange(N), labels].mean()      # never log(softmax(z)): softmax can round to 0
    grad = np.exp(lp)
    grad[np.arange(N), labels] -= 1.0            # p - y, one row per example
    return loss, grad / N                        # the 1/N from the mean

def numerical_grad(f, z, eps=1e-6):
    """Central differences, one coordinate at a time. Use float64."""
    g = np.zeros_like(z)
    for i in np.ndindex(z.shape):
        old = z[i]
        z[i] = old + eps; f_plus = f(z)
        z[i] = old - eps; f_minus = f(z)
        z[i] = old
        g[i] = (f_plus - f_minus) / (2 * eps)
    return g

rng = np.random.default_rng(0)
logits, labels = rng.normal(size=(4, 5)), np.array([0, 3, 1, 4])
loss, grad = cross_entropy(logits, labels)
num = numerical_grad(lambda z: cross_entropy(z, labels)[0], logits.copy())
print(np.abs(grad - num).max() / np.abs(grad).max(), softmax(np.array([1000.0, 0.0])))
```

**Complexity.** $O(NC)$ time and memory. The gradient check costs two loss evaluations per parameter, $O(N^2C^2)$ here, so run it only on tiny inputs.

**Follow-ups they ask.**
- *How do you pick `eps`?* Central differences have truncation error $O(\varepsilon^2)$ and round-off error $O(\delta/\varepsilon)$, with $\delta$ near machine precision, so in float64 $\varepsilon$ of $10^{-5}$ to $10^{-6}$ balances them. Report the relative error; below about $10^{-7}$ is a pass. In float32 the check is unreliable.
- *Why does $\partial L/\partial z = p - y$ matter in practice?* It never divides by $p$. Computing softmax and then the derivative of $-\log p$ separately does, and fails when $p$ underflows. That is why frameworks fuse the two into one operation.
- *Binary classification?* Use the logit directly: $\log(1 + e^{-z})$ computed as `np.logaddexp(0, -z)`, not `sigmoid` followed by `log`.
- *Temperature?* Divide logits by $T$ before the softmax; the gradient gains a factor $1/T$.
- *Ignoring padded labels?* Mask those rows out of both the loss and the gradient, and divide by the number of real labels, not by $N$.

**Theory.** The softmax–cross-entropy gradient and its place in classification heads and attention: [[02-foundations/calculus-backprop|2. Calculus & Backprop §4]].

### 10. Causal scaled dot-product self-attention

**The prompt.** *"Write a single-head causal self-attention layer in NumPy for a batch of sequences. State the shape of every tensor. Show that no position attends to the future."*

**What they are really testing.** Shapes and axis order under batching, applying the mask *before* the softmax, the $\sqrt{d_k}$ scale, and knowing the $O(T^2)$ memory cost and what happens at generation time.

**Key idea.** From the [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Attention note]]: $\operatorname{Attention}(Q, K, V) = \operatorname{softmax}(QK^\top/\sqrt{d_k})\,V$. Projections turn $X$ of shape $(B, T, d_{\text{model}})$ into $Q, K$ of shape $(B, T, d_k)$ and $V$ of shape $(B, T, d_v)$. The score table has shape $(B, T, T)$, where row $t$ is query position $t$. A causal model may not use positions $s > t$, so set those scores to $-\infty$ before the softmax. They become exactly zero weight, and the remaining weights in each row still sum to one.

```python
import numpy as np

def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)      # -inf entries stay -inf and become exactly 0
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

def causal_self_attention(X, Wq, Wk, Wv):
    """X: (B, T, d_model). Wq, Wk: (d_model, d_k). Wv: (d_model, d_v).
    Returns output (B, T, d_v) and weights (B, T, T); row t = query t, column s = key s."""
    Q, K, V = X @ Wq, X @ Wk, X @ Wv             # (B, T, d_k), (B, T, d_k), (B, T, d_v)
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(Q.shape[-1])     # (B, T, T)
    T = X.shape[1]
    future = np.triu(np.ones((T, T), dtype=bool), k=1)           # True where s > t
    scores = np.where(future, -np.inf, scores)   # mask before softmax, never after
    weights = softmax(scores, axis=-1)           # each row sums to 1 over s <= t
    return weights @ V, weights

rng = np.random.default_rng(0)
B, T, d_model, d_k = 2, 5, 16, 8
X = rng.normal(size=(B, T, d_model))
Wq, Wk, Wv = (rng.normal(size=(d_model, d_k)) / np.sqrt(d_model) for _ in range(3))
out, W = causal_self_attention(X, Wq, Wk, Wv)
print(out.shape, W.shape, W[0].round(2))
```

**Complexity.** Time $O(BT^2d_k + BTd_{\text{model}}d_k)$ and memory $O(BT^2)$ for the score table, which dominates for long sequences.

**How it is tested.** Every weight above the diagonal is exactly zero and every row sums to one. Changing the inputs at positions 3 and later leaves the outputs at positions 0–2 unchanged. The output matches an explicit loop over positions.

**Follow-ups they ask.**
- *Why divide by $\sqrt{d_k}$?* If query and key components are independent with unit variance, their dot product has variance $d_k$: with zero-mean components each product $q_i k_i$ has variance $1 \cdot 1 = 1$, and the variances of $d_k$ independent terms add. Unscaled scores grow with dimension and push the softmax into saturation, where gradients vanish.
- *Why $-\infty$ and not a large negative number?* $-\infty$ gives exactly zero. A finite $-10^9$ also works in float32 but overflows in float16, so frameworks use the dtype's minimum. If a whole row is masked, as with a fully padded sequence, $-\infty$ gives NaN; handle such rows explicitly.
- *Multi-head?* Project to $h$ heads, reshape to $(B, h, T, d_k)$, run the same function over the head axis, then concatenate and apply an output projection.
- *Generating one token at a time?* Cache the keys and values of past positions (KV cache). Each new token then needs one query against $t$ cached keys, $O(t)$ rather than recomputing the whole $O(t^2)$ table. The causal mask is implicit.
- *The sequence is 100 000 tokens.* The $T \times T$ table does not fit. Exact attention in blocks that never materializes it (FlashAttention) is the usual answer; sparse or linear attention changes the model.
- *Padding and causal masks together?* Combine them with a logical OR before the softmax, and broadcast the padding mask over the query axis.

**Theory.** What attention computes, multi-head attention, and the blocks used now: [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]].

### How to practise these

1. **Write each one from a blank file in 20 minutes**, speaking as you go: the idea, the invariant, the shapes. Run it on a hand-made input whose answer you know.
2. **Then write the test before you look at this page.** A property test (brute force equals KD-tree, systematic counts are floors or ceilings, round trip on random rotations) catches what an example cannot.
3. **Then extend it by one follow-up**: k nearest neighbours, adaptive RANSAC, a gated Kalman update, back-calculation anti-windup, multi-head attention.
4. **Revisit two problems a week** without notes. If one takes more than 25 minutes, you remember the shape of the code but not the reason, so reread its theory link.
5. **Say what you would use in production.** For each, name the library (SciPy, Open3D, Eigen, a framework's fused cross-entropy) and one parameter you would now understand.

### Self-check

1. Your A* is correct on 4-connected grids, but after switching to 8-connected moves with diagonal cost √2 it sometimes returns a path longer than optimal. What is the most likely bug?
2. A vectorized nearest-neighbour search sometimes reports a squared distance of $-2 \times 10^{-13}$ and `np.sqrt` returns NaN. Why, and what is the fix?
3. For a plane fit with 30 % inliers and $p = 0.99$, how many RANSAC samples do you need, and how many if inliers are 60 %?
4. Why does the Joseph-form covariance update remain correct if you deliberately use a suboptimal gain, while $(I - KH)P^-$ does not?
5. Weights are $(0.25, 0.25, 0.25, 0.25)$. What is the effective sample size, what does systematic resampling return, and should you resample?
6. For $L_1 = 1$, $L_2 = 0.5$, is the target $(0.3, 0)$ reachable? Give the reason in one line.
7. A PID's integrator has wound up during a long saturation. Describe what the output does when the error changes sign, and which line of §7 prevents it.
8. `rot_to_quat` must convert a rotation of 180° about the $x$-axis. Which branch runs, and what does the trace-only formula do on the same input?
9. A cross-entropy gradient check passes in float64 with `eps = 1e-6` but fails in float32. Is the gradient wrong?
10. In causal attention, what is the weight matrix's first row, and why?

> [!tip]- Answers
> 1. The heuristic. Manhattan distance overestimates a diagonal step (2 against √2), so it is inadmissible for that move set. Use the octile distance. The other candidate is a diagonal that cuts between two blocked cells, but that gives an invalid path, not a longer one.
> 2. The expansion $\lVert q\rVert^2 - 2q^\top p + \lVert p\rVert^2$ subtracts nearly equal numbers when $q$ is close to $p$, and round-off can go below zero. Clip at zero, as `np.maximum(d2, 0.0, out=d2)` does, before any square root.
> 3. $s = 3$. With $w = 0.3$, $w^3 = 0.027$ and $k = \lceil \log 0.01 / \log 0.973\rceil = 169$. With $w = 0.6$, $w^3 = 0.216$ and $k = \lceil 4.605/0.2433\rceil = 19$.
> 4. The Joseph form is the covariance of $x^- + K(z - Hx^-)$ computed directly for whatever $K$ is used: the prior error passes through $(I - KH)$ and the measurement noise through $K$. The short form was derived by substituting the optimal $K$ into that expression, so it is only equal to the true covariance for that gain, and even then round-off breaks its symmetry.
> 5. $M_{\text{eff}} = 1/(4 \cdot 0.0625) = 4 = M$. Systematic resampling returns each particle exactly once, since $M w_i = 1$ is its own floor and ceiling. You should not resample: the ESS is already at its maximum, so resampling would return the same set and could only add noise in general.
> 6. No. The reachable annulus is $0.5 \le r \le 1.5$ and $r = 0.3 < \lvert L_1 - L_2\rvert$.
> 7. The integral term stays large after the error reverses, so the output remains saturated until negative error has integrated it back down, which produces a large overshoot. The `pushing_further` test stops integration while the output is at a limit and the error pushes further into it.
> 8. $\operatorname{tr}R = -1$, so $4w^2 = 0$ and $4x^2 = 1 + 2 - (-1) = 4$. The $x$ branch runs, with $s = 4$, giving $q = (0, 1, 0, 0)$. The trace-only formula computes $w = 0$ and then divides by $4w = 0$, producing inf or NaN.
> 9. Probably not. In float32 the round-off error of about $10^{-7}$ divided by $\varepsilon = 10^{-6}$ is comparable to the derivative itself. Run the check in float64. That the implementation passes there is the evidence.
> 10. $(1, 0, \dots, 0)$. Position 0 may attend only to itself, so after masking its softmax has a single finite entry, which receives all the weight.

### Sources

- Hart, P. E., Nilsson, N. J. & Raphael, B. "A formal basis for the heuristic determination of minimum cost paths." *IEEE Transactions on Systems Science and Cybernetics* 4(2), 1968. doi:10.1109/TSSC.1968.300136
- Bentley, J. L. "Multidimensional binary search trees used for associative searching." *Communications of the ACM* 18(9), 1975. doi:10.1145/361002.361007
- Friedman, J. H., Bentley, J. L. & Finkel, R. A. "An algorithm for finding best matches in logarithmic expected time." *ACM Transactions on Mathematical Software* 3(3), 1977.
- Fischler, M. A. & Bolles, R. C. "Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography." *Communications of the ACM* 24(6), 1981. doi:10.1145/358669.358692
- Torr, P. H. S. & Zisserman, A. "MLESAC: A new robust estimator with application to estimating image geometry." *Computer Vision and Image Understanding* 78(1), 2000.
- Kalman, R. E. "A new approach to linear filtering and prediction problems." *Journal of Basic Engineering* 82(1), 1960. doi:10.1115/1.3662552
- Bucy, R. S. & Joseph, P. D. *Filtering for Stochastic Processes with Applications to Guidance*. Interscience, 1968 (the Joseph-form covariance update).
- Gordon, N. J., Salmond, D. J. & Smith, A. F. M. "Novel approach to nonlinear/non-Gaussian Bayesian state estimation." *IEE Proceedings F (Radar and Signal Processing)* 140(2), 1993. doi:10.1049/ip-f-2.1993.0015
- Douc, R., Cappé, O. & Moulines, E. "Comparison of resampling schemes for particle filtering." *International Symposium on Image and Signal Processing and Analysis (ISPA)*, 2005.
- Thrun, S., Burgard, W. & Fox, D. *Probabilistic Robotics*. MIT Press, 2005 — the Kalman filter, the particle filter, and its low-variance (systematic) resampler.
- Lynch, K. M. & Park, F. C. *Modern Robotics: Mechanics, Planning, and Control*. Cambridge University Press, 2017 — the two-link inverse kinematics (ch. 6), rigid-body motions (ch. 3), and unit quaternions (Appendix B).
- Wampler, C. W. "Manipulator inverse kinematic solutions based on vector formulations and damped least-squares methods." *IEEE Transactions on Systems, Man, and Cybernetics* 16(1), 1986.
- Nakamura, Y. & Hanafusa, H. "Inverse kinematic solutions with singularity robustness for robot manipulator control." *Journal of Dynamic Systems, Measurement, and Control* 108(3), 1986.
- Åström, K. J. & Hägglund, T. *Advanced PID Control*. ISA, 2006 — derivative on measurement, derivative filtering, anti-windup.
- Shoemake, K. "Animating rotation with quaternion curves." *Computer Graphics (SIGGRAPH '85)* 19(3), 1985.
- Goodfellow, I., Bengio, Y. & Courville, A. *Deep Learning*. MIT Press, 2016 — ch. 4, numerical computation and the stable softmax.
- Vaswani, A. et al. "Attention is all you need." *Advances in Neural Information Processing Systems 30 (NeurIPS)*, 2017.
- Dao, T., Fu, D. Y., Ermon, S., Rudra, A. & Ré, C. "FlashAttention: Fast and memory-efficient exact attention with IO-awareness." *Advances in Neural Information Processing Systems 35 (NeurIPS)*, 2022.

## 한국어

*알고리즘 트랙의 마지막 페이지이고, 연구실 인터뷰에 가장 가까운 페이지다. 문제마다 이론을 맡은 페이지로 링크를 걸어 두었다. 이 페이지가 맡는 것은 빈 파일에서 짜는 구현, 함정, 그리고 꼬리 질문뿐이다.*

연구실 코딩 면접은 기발한 퍼즐을 잘 내지 않는다. 대신 20–40분 안에, 들어갈 연구실이 이미 돌리고 있는 코드의 작은 조각을 짜 보라고 한다. 플래너, 필터 한 스텝, 역기구학 풀이, 어텐션 층 같은 것들이다. 면접관은 세 가지를 동시에 본다. 타이핑 전에 아이디어를 말할 수 있는가? 순진한 구현을 깨뜨리는 입력(도달할 수 없는 목표, 180° 근처의 회전, 1000짜리 로짓)에도 코드가 살아남는가? "그러면 이런 경우는?" 하고 밀어붙일 때, 방법이 어디서 무너지는지 아는가? 아래 열 문제는 가장 자주 나오는 것들이다. 모든 코드는 그대로 실행되고, 테스트는 별도 파일에 두었다.

모든 절은 같은 일곱 부분으로 되어 있다: 면접관이 말할 법한 **문제**, **실제로 보는 것**, **핵심 아이디어**, 35줄 이하의 **구현** (표준 라이브러리와 NumPy), **복잡도**, 짧은 답을 붙인 **꼬리 질문**, 그리고 **이론 링크**.

> [!note] 처음이라면 · First pass
> 다음 주에 로보틱스 면접이 있다면 §1, §4, §6, §8부터 하라. 계획, 필터링, 기구학, 좌표계는 거의 모든 연구실이 묻는다. 학습 쪽에 가까운 연구실이라면 §6 대신 §9와 §10을 하라.

### 1. 경로 복원까지 하는 격자 A*

**문제.** *"점유 격자와 시작 칸, 목표 칸이 있다. 로봇은 여덟 이웃 어디로든 갈 수 있고, 대각 이동은 √2의 비용이 든다. 가장 싼 경로를 돌려주고, 없으면 없다고 하라."*

**실제로 보는 것.** 우선순위 큐 탐색을 고전적인 세 버그 없이 짤 수 있는가. 칸을 꺼낼 때가 아니라 넣을 때 목표를 검사하는 것, 이 이동 집합에서 과대추정하는 휴리스틱, 모서리로 맞닿은 두 장애물 사이를 대각으로 빠져나가는 것이다. 비용만이 아니라 경로를 돌려달라는 것은 부모 포인터를 저장할 줄 아는지 보려는 것이다.

**핵심 아이디어.** $g$를 지금까지 찾은 비용, $h$를 남은 비용의 하한이라 할 때 $f = g + h$ 순서로 칸을 확장한다. 대각 비용이 √2인 8-연결 이동에 맞는 $h$는 옥타일 거리다. 빈 격자에서 정확한 비용이므로 일관적이다. 일관된 $h$에서는 칸을 처음 꺼내는 순간 그 $g$가 확정되므로 닫힌 집합을 써도 안전하고, 각 칸은 한 번만 확장된다.

```python
import heapq, math

MOVES = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]

def astar(grid, start, goal):
    """grid[r][c] == 1 is blocked; 8-connected, straight 1, diagonal sqrt(2). Returns (path, cost)."""
    def free(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 0
    def h(cell):                                   # octile distance: consistent for these moves
        dr, dc = abs(cell[0] - goal[0]), abs(cell[1] - goal[1])
        return max(dr, dc) + (math.sqrt(2) - 1) * min(dr, dc)
    if not (free(*start) and free(*goal)):
        return None, math.inf
    g, parent, closed = {start: 0.0}, {start: None}, set()
    heap = [(h(start), h(start), start)]           # (f, h, cell): equal f prefers smaller h
    while heap:
        _, _, cell = heapq.heappop(heap)
        if cell in closed:
            continue                               # stale duplicate (lazy deletion)
        if cell == goal:                           # goal test on pop, not on push
            path = []
            while cell is not None:                # walk parent pointers back to start
                path.append(cell)
                cell = parent[cell]
            return path[::-1], g[goal]
        closed.add(cell)
        r, c = cell
        for dr, dc in MOVES:
            nxt, ng = (r + dr, c + dc), g[cell] + math.hypot(dr, dc)
            if not free(*nxt) or (dr and dc and not (free(r + dr, c) and free(r, c + dc))):
                continue                           # blocked, or a diagonal that cuts a corner
            if nxt not in closed and ng < g.get(nxt, math.inf):
                g[nxt], parent[nxt] = ng, cell
                heapq.heappush(heap, (ng + h(nxt), h(nxt), nxt))
    return None, math.inf

grid = [list(map(int, row)) for row in ("00000", "01100", "00000")]
print(astar(grid, (2, 0), (0, 4)))
```

이 격자에서는 벽이 1행의 1–2열을 막고 있어서, 경로는 아래쪽 줄을 따라가다 (2, 3)에서 (1, 4)로 대각 한 걸음을 내딛는다. 비용은 $4 + \sqrt 2$다. (2, 2)에서 (1, 3)으로 가는 걸음은 (1, 2)에 있는 벽의 모서리를 비집고 지나가므로 거부된다.

**복잡도.** 빈 칸이 $n$개면 간선은 최대 $8n$개이고 힙 삽입도 최대 $8n$번이다. 삽입과 추출이 각각 $O(\log n)$이므로 시간은 $O(n \log n)$, `g`, `parent`, 힙을 위한 메모리는 $O(n)$이다. 힙에는 낡은 중복 항목이 남을 수 있다. `heapq`에는 decrease-key가 없으니, 꺼낼 때 건너뛰는 편이 더 싸다.

**꼬리 질문.**
- *여기서 왜 맨해튼 거리가 아닌가?* 대각 이동을 과대추정한다. 대각 한 걸음은 √2 ≈ 1.41인데 맨해튼은 2라고 한다. 과대추정하는 $h$는 더 긴 경로를 돌려줄 수 있다.
- *칸마다 통과 비용이 다르다.* $g$에 들어가는 칸의 비용을 더하고, $h$에는 어떤 칸이 가질 수 있는 가장 작은 비용을 곱해 여전히 하한이 되게 한다.
- *4000 × 4000 지도에서 너무 느리다.* 가중 A*($g + \varepsilon h$, 비용은 최적의 $\varepsilon$배 이하), 균일 비용 격자에서의 jump point search, 더 거친 격자나 계층 구조, 양방향 탐색이 표준 답이다. 상수 인자도 확인하라. 딕셔너리 안의 튜플은 느리고, `r * cols + c`로 색인하는 평평한 NumPy 배열이 빠르다.
- *로봇이 달리는 동안 지도가 바뀐다.* 작은 지도라면 처음부터 다시 계획해도 된다. D* Lite 같은 점진적 플래너는 이전 탐색을 수선한다.
- *결과가 좋은 로봇 경로인가?* 격자 위에서 최적일 뿐 평면에서 최적은 아니다. 장애물에 붙어 가는 계단 모양이다. 먼저 장애물을 로봇 반경만큼 부풀리고, 나중에 경로를 매끄럽게 하라.

**이론.** 정당성 논증(일관성, 축소 비용, 동점 처리)은 [[02-foundations/algorithms/graph-algorithms|11.6 §6]]에, 플래너가 경로로 무엇을 하는지는 [[04-robotics/planning-decision-making|4. 계획과 의사결정 §3]]에 있다.

### 2. 최근접점: 벡터화한 전수 탐색과 KD-tree

**문제.** *"3차원 점 $n$개와 질의점 $m$개가 있다. 각 질의의 최근접점을 찾아라. 먼저 가장 단순하면서 맞는 버전, 그다음 더 빠른 것."*

**실제로 보는 것.** NumPy를 다루는 솜씨(파이썬 루프 없이, 그리고 $m \times n \times d$ 배열을 만들지 않고 브로드캐스팅하기), 부분 선택이 정렬보다 싸다는 것을 아는지, KD-tree가 *왜* 가지를 치는지와 언제 그 이점이 사라지는지 이해하는지다.

**핵심 아이디어.** 전수 탐색에서는 거리 제곱을 전개한다. $\lVert q - p\rVert^2 = \lVert q\rVert^2 - 2\,q^\top p + \lVert p\rVert^2$이므로 행렬 곱 한 번으로 $m \times n$개의 거리를 모두 얻는다. KD-tree는 가장 넓게 퍼진 좌표의 중앙값에서 점들을 재귀적으로 나눈다. 질의할 때는 질의점이 속한 쪽으로 먼저 내려가고, 분할 평면이 지금까지의 최선 거리보다 가까울 때만 반대쪽을 방문한다. 평면 너머의 모든 점은 적어도 평면까지의 거리만큼 떨어져 있기 때문이다.

```python
import numpy as np

def knn_brute(P, Q, k=1):
    """P: (n, d) points, Q: (m, d) queries. Returns (m, k) indices and squared distances, nearest first."""
    d2 = (Q**2).sum(1)[:, None] - 2.0 * Q @ P.T + (P**2).sum(1)[None, :]   # (m, n)
    np.maximum(d2, 0.0, out=d2)                     # round-off can make ~0 slightly negative
    idx = np.argpartition(d2, k - 1, axis=1)[:, :k] # the k smallest per row, unordered: O(n)
    dk = np.take_along_axis(d2, idx, axis=1)
    order = np.argsort(dk, axis=1)
    return np.take_along_axis(idx, order, 1), np.take_along_axis(dk, order, 1)

def kd_build(P, idx, leaf=16):
    """Nodes are ('leaf', indices) or ('split', axis, value, left, right)."""
    if len(idx) <= leaf:
        return ("leaf", idx)
    axis = int(np.argmax(np.ptp(P[idx], axis=0)))  # split the widest dimension
    mid = len(idx) // 2
    idx = idx[np.argpartition(P[idx, axis], mid)]  # median in O(n), not a full sort
    left, right = kd_build(P, idx[:mid], leaf), kd_build(P, idx[mid:], leaf)
    return ("split", axis, P[idx[mid], axis], left, right)

def kd_nearest(node, P, q, best=(np.inf, -1)):
    """Returns (squared distance, index) of the point in P nearest to q."""
    if node[0] == "leaf":
        pts = node[1]
        d2 = ((P[pts] - q) ** 2).sum(1)
        i = int(np.argmin(d2))
        return min(best, (d2[i], int(pts[i])))
    _, axis, value, left, right = node
    diff = q[axis] - value
    near, far = (left, right) if diff < 0 else (right, left)
    best = kd_nearest(near, P, q, best)
    if diff * diff < best[0]:                       # the ball around q crosses the plane
        best = kd_nearest(far, P, q, best)
    return best

rng = np.random.default_rng(0)
P = rng.random((10_000, 3)); q = rng.random(3)
tree = kd_build(P, np.arange(len(P)))
print(kd_nearest(tree, P, q)[1], knn_brute(P, q[None, :], k=1)[0][0, 0])
```

**복잡도.** 전수 탐색은 시간 $O(mnd)$에 $m \times n$ 거리 행렬이 필요하므로, $mn$이 크면 질의를 묶음으로 나눠 처리한다. `argpartition`은 행마다 $O(n)$에 가장 작은 $k$개를 고르고, 그 $k$개만 정렬한다. KD-tree 구축은 각 층에서 $O(n)$ 일(`argpartition`으로 중앙값, `ptp`로 퍼짐)을 $O(\log n)$층에 걸쳐 하므로 $O(n \log n)$이다. 질의는 저차원의 고르게 퍼진 데이터에서 기대 $O(\log n)$, 최악 $O(n)$이다.

**꼬리 질문.**
- *`np.maximum` 줄은 왜 있나?* 전개식은 질의점과 같은 점에 대해 $-10^{-12}$ 같은 값을 낼 수 있다. 제곱근을 취하기 전에 0에서 자른다.
- *하나가 아니라 k개?* 최선 $k$개를 최대 힙에 담고, $k$번째 최선까지의 거리로 가지를 친다.
- *반경 탐색?* 같은 방식으로 내려가고, 평면이 반경보다 멀면 그쪽을 버린다.
- *KD-tree를 쓰지 않을 때는?* 512차원 임베딩(가지치기가 실패하니 HNSW 같은 근사 방법), 알려진 척도의 고정 반경(복셀 해시 격자가 기대 $O(1)$), 벡터화한 전수 탐색이 먼저 끝날 만큼 작은 일회성 묶음이다.
- *실무에서도 직접 짜겠는가?* 아니다. `scipy.spatial.cKDTree`, `nanoflann`, Open3D나 PCL 안의 KD-tree를 쓴다. 한 번 직접 짜 보는 것은 그 라이브러리들의 `leaf_size`와 근사 탐색 파라미터가 무엇을 맞바꾸는지 배우는 방법이다.
- *RRT처럼 트리가 계속 자라야 한다.* 잎에 삽입하고 균형이 무너지면 다시 짓거나, 크기가 두 배씩 커지는 트리 몇 개를 유지한다.

**이론.** 가지치기가 왜 통하고 고차원에서 왜 실패하는지: [[02-foundations/algorithms/data-structures|11.2 §8]].

### 3. RANSAC 직선 맞춤

**문제.** *"벽을 찍은 2차원 레이저 스캔의 점 40 %가 잡동사니 위에 있다. 벽의 직선을 맞춰라. 무작위 표본은 몇 번 뽑아야 하나?"*

**실제로 보는 것.** 큰 이상치가 있으면 최소제곱이 무너진다는 것을 아는지, *최소* 표본(직선이면 두 점)을 고르는지, 반복 횟수를 외우는 대신 유도할 수 있는지, 마지막에 인라이어로 다시 맞추는지다.

**핵심 아이디어.** 무작위 두 점으로 직선을 만들고 거리 임계값 안에 드는 점을 세는 일을 반복한다. 인라이어가 가장 많은 직선을 남긴 뒤, 그 인라이어들에 전체 최소제곱(total least squares)으로 다시 맞춘다. 몇 번 반복하나? 점 중 비율 $w$가 인라이어라면 $s$개짜리 표본 하나가 모두 인라이어일 확률은 $w^s$이고, 그래서 독립 표본 $k$개가 모두 오염될 확률은 $(1 - w^s)^k$다. 이것이 $1 - p$ 이하가 되도록 요구하고 로그를 취하면 아래 횟수가 나온다. 두 로그가 모두 음수이기 때문에 부등호 방향이 뒤집힌다.

$$k = \left\lceil \frac{\log(1 - p)}{\log(1 - w^{s})} \right\rceil$$

```python
import math
import numpy as np

def ransac_iterations(p, w, s):
    """Samples k so that, with probability p, at least one size-s sample is all inliers (inlier ratio w)."""
    return math.ceil(math.log(1 - p) / math.log(1 - w**s))

def ransac_line(pts, thresh, k, rng):
    """pts: (N, 2). Line n . x = c with unit normal n. Returns (n, c, inlier mask) or None."""
    best = np.zeros(len(pts), dtype=bool)
    for _ in range(k):
        i, j = rng.choice(len(pts), size=2, replace=False)   # minimal sample: s = 2
        t = pts[j] - pts[i]
        if np.hypot(*t) < 1e-12:
            continue                                         # coincident points: no line
        n = np.array((-t[1], t[0])) / np.hypot(*t)
        inliers = np.abs(pts @ n - n @ pts[i]) < thresh      # perpendicular distances
        if inliers.sum() > best.sum():
            best = inliers
    if best.sum() < 2:
        return None
    X = pts[best]                                            # refit on the consensus set:
    mu = X.mean(axis=0)                                      # total least squares, the normal is
    n = np.linalg.svd(X - mu)[2][-1]                         # the least-variance direction
    return n, n @ mu, np.abs(pts @ n - n @ mu) < thresh

rng = np.random.default_rng(1)
x = rng.uniform(0, 10, 60)
line = np.column_stack([x, 0.5 * x + 1 + rng.normal(0, 0.05, 60)])   # y = 0.5 x + 1
outliers = rng.uniform(0, 10, (40, 2))
n, c, mask = ransac_line(np.vstack([line, outliers]), 0.2, ransac_iterations(0.99, 0.6, 2), rng)
print(ransac_iterations(0.99, 0.6, 2), -n[0] / n[1], c / n[1], mask[:60].mean())
```

> [!example] 계산 예제 · Worked example
> $p = 0.99$이고 점의 절반이 이상치($w = 0.5$)라면, 직선($s = 2$)은 $\log 0.01 / \log 0.75 = 16.0$이므로 17번, 평면($s = 3$)은 35번, 8점 기초 행렬 추정($s = 8$)은 1177번이 필요하다. 인라이어 비율은 $s$만큼 중요하다. $w = 0.3$인 평면은 169번이 필요하다. 테스트 파일은 각 값을 확인한 뒤 $k$번 표본 추출을 20 000번 모의 실행해, 성공률이 $1 - (1 - w^s)^k \ge p$와 맞고 $k - 1$번으로는 모자란다는 것을 확인한다.

**복잡도.** $O(kN)$이다. $k$번의 반복마다 $N$개 점을 모두 채점한다. 재맞춤은 $O(N)$이다. $k$가 $N$이 아니라 $w$, $s$, $p$에만 달려 있다는 점에 주목하라. RANSAC이 큰 점군으로 확장되는 이유다.

**꼬리 질문.**
- *$w$를 모른다.* 비관적인 $w$로 시작하고, 더 나은 합의 집합이 나올 때마다 그 인라이어 비율로 $w$를 갱신해 $k$를 다시 계산한다. 보통 루프가 훨씬 일찍 끝난다.
- *임계값은 어떻게 고르나?* 잡음에서 정한다. 점-직선 거리에 표준편차 $\sigma$의 가우시안 잡음이 있다면 $1.96\sigma$ 근처의 임계값이 참 인라이어의 약 95 %를 남긴다.
- *왜 다시 맞추고, 왜 전체 최소제곱인가?* 두 점짜리 직선은 잡음 낀 점 두 개만 쓴다. $y$에 대한 일반 최소제곱은 수직선에서 실패한다. 중심을 뺀 인라이어의 가장 작은 특이벡터는 어떤 방향이든 법선을 준다.
- *벽이 여러 개다.* 직선 하나를 맞추고 그 인라이어를 지운 뒤 반복하거나(순차 RANSAC), 다중 모델 방법을 쓴다.
- *더 나은 채점?* MSAC과 MLESAC은 인라이어를 세는 대신 잔차로 채점해, 같은 수의 점을 잡는 직선들 사이의 동점을 가른다.
- *공식은 복원 추출로 뽑은 독립 표본을 가정했다.* 맞다. 유한 집합에서 비복원 추출하면 조금 더 유리하므로, 공식은 약간 과대추정이다.

**이론.** 정합, 그리고 기하 파이프라인이 최적화 전에 이상치를 처리해야 하는 이유: [[04-robotics/geometric-perception-calibration|3.5 기하 인식과 보정 §4]].

### 4. 선형 칼만 필터 한 스텝

**문제.** *"표적이 거의 등속으로 직선 위를 움직인다. 0.1초마다 잡음 낀 위치 측정이 들어온다. 칼만 필터의 예측 한 번과 갱신 한 번을 짜라."*

**실제로 보는 것.** 모양을 맞게 쓰는지, $Q$를 `np.eye(2) * 0.01` 대신 물리적 잡음 모델에서 쓰는지, `np.linalg.inv`를 부르지 않는지, 교과서의 공분산 갱신이 왜 표류하고 Joseph 형태가 무엇을 고치는지 아는지다.

**핵심 아이디어.** 표기는 [[04-robotics/state-estimation-slam|3. 상태 추정 §5]]와 [[02-foundations/probability|3. 확률 §5]]를 따른다. 상태 $x = (\text{위치}, \text{속도})$, 동역학 $A$, 과정 잡음 공분산 $Q$, 측정 행렬 $H$(확률 페이지에서는 $C$), 측정 잡음 $R$, 추정 공분산 $P$다. 예측은 가우시안을 동역학에 통과시킨다: $x^- = Ax$, $P^- = AP A^\top + Q$. 갱신은 측정 $z$로 조건화한다: 혁신 $y = z - Hx^-$, 그 공분산 $S = HP^-H^\top + R$, 이득 $K = P^-H^\top S^{-1}$, 그리고 $x = x^- + Ky$. 공분산은 Joseph 형태로 갱신한다. 두 합동 변환의 합이기 때문에 구조상 대칭이고 양의 준정부호다. 합동 변환이란 $X$가 대칭 양의 준정부호일 때 $MXM^\top$ 꼴의 항이며, $v^\top MXM^\top v = (M^\top v)^\top X (M^\top v) \ge 0$이므로 역시 대칭 양의 준정부호다.

$$P = (I - KH)\,P^-\,(I - KH)^\top + K R K^\top$$

한 스텝 동안 유지되는 표준편차 $\sigma_a$의 백색 가속도라면 상태는 $G a$만큼 바뀌고 $G = (\tfrac12 \Delta t^2, \Delta t)^\top$이다. 그래서 $Q = \sigma_a^2 G G^\top$이다.

```python
import numpy as np

def cv_model(dt, sigma_a, sigma_z):
    """Constant velocity, state x = [position, velocity]; a white acceleration drives it."""
    A = np.array([ [1.0, dt], [0.0, 1.0] ])
    G = np.array([ [0.5 * dt**2], [dt] ])        # how one acceleration sample enters x
    Q = sigma_a**2 * (G @ G.T)
    H = np.array([ [1.0, 0.0] ])                 # we measure position only
    R = np.array([ [sigma_z**2] ])
    return A, Q, H, R

def kf_predict(x, P, A, Q):
    return A @ x, A @ P @ A.T + Q

def kf_update(x, P, z, H, R):
    y = z - H @ x                                # innovation, shape (1,)
    S = H @ P @ H.T + R                          # innovation covariance, (1, 1)
    K = np.linalg.solve(S, H @ P).T              # K = P H^T S^-1 without an explicit inverse
    I_KH = np.eye(len(x)) - K @ H
    P = I_KH @ P @ I_KH.T + K @ R @ K.T          # Joseph form: symmetric, PSD, any gain K
    return x + K @ y, P

A, Q, H, R = cv_model(dt=0.1, sigma_a=0.5, sigma_z=0.3)
x, P = np.array([0.0, 1.0]), np.eye(2)
x, P = kf_predict(x, P, A, Q)
x, P = kf_update(x, P, np.array([0.12]), H, R)
print(x.round(4), P.round(4))
```

> [!example] 계산 예제 · Worked example
> 상태 추정 페이지의 스칼라 예제를 이 코드로 돌려 보자. 예측 위치 $10$, 분산 $4$, 측정 $z = 12$, $R = 1$, $H = (1, 0)$. 그러면 $S = 5$, $K = (0.8, 0)^\top$이고, 위치는 $10 + 0.8 \cdot 2 = 11.6$, 분산은 $(1 - 0.8)^2 \cdot 4 + 0.8^2 \cdot 1 = 0.8$이 된다. 최적 이득이니 당연히 $(1-K)P^-$가 주는 $0.8$과 같다. 테스트 파일은 이 숫자들을 확인하고, 모의 데이터로 3000스텝도 돌린다. 필터링한 위치 오차는 원래 측정 오차의 절반보다 작고, 정규화 추정 오차 제곱의 평균은 상태 차원인 2에 가깝다. 일관된 필터라면 그래야 한다.

**복잡도.** 상태 차원 $n$, 측정 차원 $m$일 때 스텝마다 공분산 곱에 $O(n^3)$, $S$로 푸는 데 $O(m^3)$이다. 여기서는 둘 다 상수다.

**꼬리 질문.**
- *왜 `P = (I - K H) @ P`가 아닌가?* 정확한 최적 이득과 정확한 산술에서만 맞는다. 반올림 오차 때문에 대칭성을, 결국에는 양의 정부호성을 잃는다. Joseph 형태는 최적이 아닌 이득을 포함해 어떤 이득에서도 유효하다. 싼 대안은 `P = 0.5 * (P + P.T)`로 대칭화하는 것이다.
- *왜 `inv` 대신 `solve`인가?* 더 싸고 더 정확하다. 문제가 크면 $S$의 Cholesky 분해를 쓴다.
- *측정 하나가 이상치다.* 게이팅한다. $y^\top S^{-1} y$가 카이제곱 임계값(1차원 95 %에서 3.84)보다 작을 때만 받아들인다.
- *측정이 빠졌거나, 두 센서가 다른 주기로 들어온다.* 아무것도 오지 않으면 갱신을 건너뛴다. 각 측정의 타임스탬프까지 예측하고, 그 센서의 $H$와 $R$로 갱신한다.
- *$Q$와 $R$은 어떻게 맞추나?* $R$은 정지 상태 센서 로그에서, $Q$는 표적이 얼마나 가속할 수 있는지에 대한 물리에서 정하고, 일관성을 확인한다(정규화 혁신의 평균이 $m$ 근처여야 한다).
- *모델이 비선형이다.* EKF: 현재 추정에서 $f$와 $h$를 선형화하고, 그 야코비안을 $A$와 $H$ 자리에 쓴다.

**이론.** 예측과 갱신이 어디서 오는지는 [[04-robotics/state-estimation-slam|3. 상태 추정 §4]]에, 그 뒤의 가우시안 항등식은 [[02-foundations/probability|3. 확률 §5]]에 있다.

### 5. 입자 필터 재표본추출

**문제.** *"입자 필터에 가중치가 붙은 입자 $M$개가 있다. 재표본추출을 구현하라. 단순한 방법이 왜 최선이 아니며, 애초에 언제 재표본추출해야 하나?"*

**실제로 보는 것.** 재표본추출의 목적(가중치 퇴화와 싸우기)과 비용(다양성 상실)을 아는지, 유효 표본 크기 기준, 다항 재표본추출과 체계적 재표본추출의 차이, 언더플로하는 우도를 수치적으로 조심스럽게 다루는지다.

**핵심 아이디어.** 다항(multinomial) 재표본추출은 가중치에서 독립적으로 색인 $M$개를 뽑는다. 그래서 가중치 $w_i$인 입자의 복사 수는 평균이 $M w_i$이고 이항 분포만큼 흩어진다. 체계적(systematic) 재표본추출은 무작위 오프셋 하나 $u_0 \in [0, 1)$와 고르게 벌어진 포인터 $M$개 $u_m = (u_0 + m)/M$를 쓰고, 각 포인터는 자기가 속한 누적 가중치 구간의 입자를 고른다. 각 $u_m$은 그 자체로 균등 분포이므로 복사 수의 평균은 여전히 $M w_i$지만, 복사 수는 항상 $\lfloor M w_i\rfloor$ 아니면 $\lceil M w_i\rceil$이어서 무작위성의 대부분이 사라진다. 유효 표본 크기 $M_{\text{eff}} = 1/\sum_i w_i^2$가 임계값(흔히 $M/2$) 아래로 떨어질 때만 재표본추출한다.

```python
import numpy as np

def normalize_log_weights(logw):
    """Log-likelihoods -> normalized weights, without underflow (subtract the max first)."""
    w = np.exp(logw - logw.max())
    return w / w.sum()

def effective_sample_size(w):
    return 1.0 / np.sum(w**2)                    # M for uniform weights, 1 if one particle has all

def multinomial_resample(w, rng):
    """M independent draws from the categorical distribution w."""
    return rng.choice(len(w), size=len(w), p=w)

def systematic_resample(w, rng):
    """One uniform offset, M evenly spaced pointers through the cumulative weights."""
    M = len(w)
    cdf = np.cumsum(w)
    cdf[-1] = 1.0                                # round-off must not leave a pointer past the end
    u = (rng.random() + np.arange(M)) / M        # u_m = (u_0 + m) / M, u_0 ~ U[0, 1)
    return np.searchsorted(cdf, u, side="right") # index i with cdf[i-1] <= u < cdf[i]

def resample_if_needed(particles, w, rng, threshold=0.5):
    if effective_sample_size(w) < threshold * len(w):
        idx = systematic_resample(w, rng)
        particles, w = particles[idx], np.full(len(w), 1.0 / len(w))
    return particles, w

rng = np.random.default_rng(0)
w = normalize_log_weights(np.array([-1000.0, -1001.0, -1003.0, -1010.0]))
print(w.round(4), effective_sample_size(w).round(3), np.bincount(systematic_resample(w, rng), minlength=4))
```

> [!example] 계산 예제 · Worked example
> 가중치 $(0.10, 0.45, 0.35, 0.10)$의 누적합은 $(0.10, 0.55, 0.90, 1.00)$이다. $u_0 = 0.8$이면 포인터는 $0.20, 0.45, 0.70, 0.95$이고, 입자 $1, 1, 2, 3$에 떨어진다. 복사 수 $(0, 2, 1, 1)$을 기댓값 $(0.4, 1.8, 1.4, 0.4)$와 비교하면 모두 내림 아니면 올림이다. 테스트 파일은 무작위 가중치로 재표본추출을 40 000번 돌려 세 가지를 확인한다. 두 방식 모두 각 입자의 평균 복사 수가 $M w_i$와 맞고, 체계적 방식의 복사 수는 모두 내림이나 올림이며, 체계적 방식 복사 수의 전체 분산이 다항 방식보다 작다.

**복잡도.** 여기 쓴 두 방식은 뽑을 때마다 이진 탐색을 하므로 $O(M \log M)$이다. 체계적 방식의 포인터는 이미 정렬되어 있으니 누적합을 두 포인터로 훑으면 $O(M)$이 된다. ESS는 $O(M)$이다.

**꼬리 질문.**
- *애초에 왜 재표본추출하나?* 하지 않으면 몇 번의 갱신 뒤 거의 모든 가중치가 입자 하나에 몰리고, 나머지 입자는 계산만 먹고 아무 기여도 하지 않는다.
- *그러면 왜 매 스텝 하지 않나?* 재표본추출은 입자를 복제한다. 과정 잡음이 작으면 복사본들이 똑같이 남아 집합이 몇 개의 서로 다른 상태로 무너진다(표본 빈곤화). 적응적으로 재표본추출하고, 그 뒤에 작은 흔들림을 더하면 줄어든다.
- *왜 로그 가중치인가?* 많은 우도의 곱은 float64에서도 0으로 언더플로한다. 로그 가중치를 유지하고, 지수를 취하기 전에 최댓값을 뺀다.
- *체계적 방식이 항상 더 나은가?* 실제로는 분산이 더 작고 표준적인 선택이지만, 모든 입자 순서에 대해 성립하는 정리는 아니다. 층화(stratified)와 잔차(residual) 재표본추출이 다른 흔한 선택지다.
- *입자는 몇 개?* 필요한 수가 상태 차원에 따라 빠르게 커진다. 입자 필터가 2–3차원 위치 추정에서 쓰이는 이유이고, KLD-sampling 같은 적응 방식이 믿음이 얼마나 퍼졌는지에 따라 $M$을 바꾸는 이유다.

**이론.** 다른 추정기 계열 속의 입자 필터, 그리고 입자 고갈: [[04-robotics/state-estimation-slam|3. 상태 추정 §5]].

### 6. 2링크 평면 팔: 순기구학, 해석적 역기구학, 감쇠 IK 한 스텝

**문제.** *"링크 길이가 $L_1$, $L_2$인 평면 팔이 있다. 순기구학을 짜라. 그다음 목표 $(x, y)$에 대한 역기구학을 풀어 두 해를 모두 주고, 닿지 않는 목표도 처리하라. 마지막으로, 특이점에서 폭발하지 않는 수치 IK 한 스텝을 밟아라."*

**실제로 보는 것.** `arccos`나 `arctan` 하나가 아니라 `atan2`를 쓰는지, 해가 0개, 1개, 2개일 수 있음을 아는지, 작업공간 경계에서 반올림 오차를 잘라내는지, 팔이 곧게 펴졌을 때 야코비안 역행렬이 왜 실패하는지 아는지다.

**핵심 아이디어.** 순기구학은 Lynch와 Park의 2링크 예제처럼 회전한 두 링크의 합이다. 역기구학에서는 코사인 법칙이 $\cos\theta_2 = (x^2 + y^2 - L_1^2 - L_2^2)/(2L_1L_2)$를 준다. 이 값이 $[-1, 1]$ 밖이면 목표는 고리 영역 $\lvert L_1 - L_2\rvert \le r \le L_1 + L_2$ 밖에 있고 해가 없다. 그렇지 않으면 $\sin\theta_2 = \pm\sqrt{1 - \cos^2\theta_2}$가 가지를 고르고, $\theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin\theta_2, L_1 + L_2\cos\theta_2)$다. 가지 이름은 책마다 다르다. 모호하지 않은 이름표는 $\theta_2$의 부호이고, 여기서는 Modern Robotics를 따라 $\theta_2 \ge 0$을 elbow-down(righty)이라 부른다.

수치 스텝은 별개의 아이디어다. 끝점 오차를 $e = (x, y)_{\text{target}} - \text{FK}(\theta)$라 하면 감쇠 최소제곱 스텝은 $\Delta\theta = J^\top (JJ^\top + \lambda^2 I)^{-1} e$다. 팔이 곧게 펴지거나 접히면 $J$의 계수가 떨어져 $J^{-1}$이 존재하지 않는다. $\lambda > 0$이면 $JJ^\top + \lambda^2 I$는 항상 역행렬이 있으므로 스텝이 유한하게 유지된다(후속 질문 참고).

```python
import numpy as np

def fk(theta, L1=1.0, L2=1.0):
    t1, t2 = theta
    return np.array([L1 * np.cos(t1) + L2 * np.cos(t1 + t2), L1 * np.sin(t1) + L2 * np.sin(t1 + t2)])

def ik(x, y, L1=1.0, L2=1.0, elbow="down"):
    """Analytic IK. 'down' (righty) has theta2 >= 0, 'up' (lefty) theta2 <= 0. None if unreachable."""
    c2 = (x * x + y * y - L1 * L1 - L2 * L2) / (2 * L1 * L2)   # law of cosines
    if abs(c2) > 1 + 1e-9:
        return None                              # outside the annulus |L1 - L2| <= r <= L1 + L2
    c2 = np.clip(c2, -1.0, 1.0)                  # a boundary target must not give sqrt(-1e-16)
    s2 = np.sqrt(1 - c2 * c2) * (1.0 if elbow == "down" else -1.0)
    t1 = np.arctan2(y, x) - np.arctan2(L2 * s2, L1 + L2 * c2)
    return np.array([t1, np.arctan2(s2, c2)])

def jacobian(theta, L1=1.0, L2=1.0):
    t1, t2 = theta
    s1, c1, s12, c12 = np.sin(t1), np.cos(t1), np.sin(t1 + t2), np.cos(t1 + t2)
    return np.array([ [-L1 * s1 - L2 * s12, -L2 * s12], [L1 * c1 + L2 * c12, L2 * c12] ])

def dls_step(theta, target, lam=0.1, L1=1.0, L2=1.0):
    """One damped-least-squares step: dtheta = J^T (J J^T + lam^2 I)^-1 e."""
    J, e = jacobian(theta, L1, L2), target - fk(theta, L1, L2)
    return theta + J.T @ np.linalg.solve(J @ J.T + lam**2 * np.eye(2), e)

target = np.array([-1.0, 1.0])
for elbow in ("down", "up"):
    th = ik(*target, elbow=elbow)
    print(elbow, np.degrees(th).round(1), fk(th).round(6))
print(ik(2.5, 0.0))                              # None: beyond reach
print(np.degrees(dls_step(np.radians([45.0, 90.0]), target, lam=0.0)).round(1))
```

마지막 줄은 [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장 §3]]의 손 계산 반복을 재현한다. $(45°, 90°)$에서 $(-1, 1)$을 향해 감쇠 없이 한 스텝을 밟으면 $(68.7°, 123.6°)$에 도착한다. 그 목표에 대한 두 해석해는 $(90°, 90°)$와 $(180°, -90°)$다.

**복잡도.** 모두 $O(1)$이다. 관절 $n$개, 작업 차원 $m$인 팔이라면 감쇠 스텝 하나는 $JJ^\top$을 만들고 $m \times m$ 계를 푸는 데 $O(m^2 n + m^3)$이다.

**꼬리 질문.**
- *특이점은 어디인가?* $\det J = L_1 L_2 \sin\theta_2$이므로 $\theta_2 = 0$(펴짐)과 $\theta_2 = \pi$(접힘)이다. 거기서 팔은 끝점을 링크 방향으로 움직일 수 없고 $J^{-1}$은 무한대다.
- *$\lambda$는 무엇을 맞바꾸나?* 정확도를 내주고 유계인 관절 스텝을 얻는다. 특이점 근처에서 감쇠는 $\Delta\theta$를 유한하게 유지하지만, 선형 모델 안에서도 스텝이 더는 목표에 닿지 않는다. $\lambda$를 작게 두거나, $J$의 가장 작은 특이값이 줄어들 때만 키운다.
- *왜 $(J^\top J + \lambda^2 I)^{-1}J^\top$이 아니라 $J^\top(JJ^\top + \lambda^2 I)^{-1}$인가?* 둘은 같다. 앞의 것은 $m \times m$ 계를 풀어서, 팔이 여유 자유도를 가질 때($n > m$) 더 싸다.
- *두 해석해 중 무엇을 보내나?* 관절 한계 안에 있고 현재 자세에 가장 가까운 것이다. 각도 차이는 한 바퀴 감김을 고려해 잰다.
- *$L_1 = L_2$인데 목표가 정확히 베이스 위다.* 해가 무한히 많다. $\theta_2 = \pi$이면 어떤 $\theta_1$이든 된다. 코드는 하나를 돌려주니, 그렇다고 말하라.
- *수치 IK가 수렴하지 않는다.* 닿지 않는 목표, 나쁜 초기 추정, 특이점, 반복 예산 소진을 구별하라. 국소 탐색 한 번의 실패가 해가 없다는 증명은 아니다.

**이론.** 해석적 IK와 수치 IK, 뉴턴–랩슨, 감쇠 최소제곱은 [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장 §4]]에, 이 문제가 딛고 선 순기구학과 야코비안 결과는 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학과 동역학 §1]]에 있다.

### 7. 측정값 미분과 안티와인드업을 갖춘 이산 PID

**문제.** *"실제 모터에서 100 Hz로 도는 PID 제어기를 짜라. 구동기는 포화된다. 1차 플랜트에서 시험하라."*

**실제로 보는 것.** 교과서 PID와 하드웨어에서 도는 PID를 가르는 세 가지 수정을 아는지다. 오차가 아니라 측정값을 미분해 설정값 계단이 튀는 값을 만들지 않게 하기, 잡음을 미분하면 증폭되니 미분 항에 저역통과 필터 걸기, 출력이 오차가 미는 방향으로 포화되어 있는 동안 적분 멈추기(안티와인드업)다.

**핵심 아이디어.** [[04-robotics/control-theory-ce397|5. 제어 이론 §7]]의 제어 법칙은 $e = r - y$일 때 $u = K_p e + K_i \int e\,dt + K_d \dot e$다. 설정값이 일정하면 $\dot e = -\dot y$이므로, $K_d\dot e$를 $-K_d\dot y$로 바꿔도 설정값이 바뀌는 순간 사이에는 아무것도 달라지지 않고, 바뀌는 순간의 튐만 사라진다. $u$를 구동기 범위로 자르고, 적분기 갱신은 $u$를 한계 쪽으로 더 밀지 않을 때만 반영한다(조건부 적분). 영차 유지 아래의 플랜트 $\tau\dot y = -y + Ku$는 $a = e^{-\Delta t/\tau}$일 때 $y_{k+1} = a y_k + K(1 - a)u_k$로 정확히 모사된다.

```python
import math

class PID:
    """Discrete PID: derivative on measurement, filtered D, clamped output, conditional integration."""
    def __init__(self, kp, ki, kd, dt, u_min, u_max, tau_d=0.0):
        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt
        self.u_min, self.u_max = u_min, u_max
        self.alpha = dt / (tau_d + dt)           # first-order low-pass on the derivative
        self.i_term, self.d_filt, self.y_prev = 0.0, 0.0, None

    def update(self, r, y):
        e = r - y
        dy = 0.0 if self.y_prev is None else (y - self.y_prev) / self.dt
        self.y_prev = y
        self.d_filt += self.alpha * (dy - self.d_filt)
        i_next = self.i_term + self.ki * e * self.dt           # stores Ki * integral, not the integral
        u_raw = self.kp * e + i_next - self.kd * self.d_filt   # minus: D acts on y, not on e
        u = min(self.u_max, max(self.u_min, u_raw))
        pushing_further = (u_raw > self.u_max and e > 0) or (u_raw < self.u_min and e < 0)
        if not pushing_further:                                # anti-windup: freeze I while it
            self.i_term = i_next                               # would drive deeper into the limit
        return u

def simulate(pid, r=1.0, tau=0.5, gain=1.0, steps=600):
    """First-order plant tau * dy/dt = -y + gain * u, discretized exactly under zero-order hold."""
    a, y, ys = math.exp(-pid.dt / tau), 0.0, []
    for _ in range(steps):
        u = pid.update(r, y)
        y = a * y + gain * (1 - a) * u
        ys.append(y)
    return ys

ys = simulate(PID(kp=2.0, ki=4.0, kd=0.05, dt=0.01, u_min=0.0, u_max=1.5, tau_d=0.02))
print(round(max(ys), 4), round(ys[-1], 4))
```

**복잡도.** 갱신마다 시간과 메모리 모두 $O(1)$이다.

**꼬리 질문.**
- *안티와인드업이 중요하다는 것을 보여라.* 테스트 파일은 그 플랜트에서 $K_p = 1$, $K_i = 5$, 한계 $\pm 1.2$로 돌린다. 위 버전은 설정값을 약 4 % 넘어서고, 조건 없이 적분하는 같은 제어기는 약 15 % 넘어선다. 포화 동안 쌓인 적분을 음의 오차로 되감아야 하기 때문이다.
- *측정값 미분이 중요하다는 것을 보여라.* $K_d = 1$, $\Delta t = 0.01$에서 단위 설정값 계단은 오차 미분을 통해 한 샘플에 $K_d \cdot 1/\Delta t = 100$을 더한다. 위 코드는 아무것도 더하지 않고, 테스트가 이를 확인한다.
- *다른 안티와인드업 방식은?* 역계산(back-calculation)은 포화된 출력과 포화 전 출력의 차이를 추종 시정수와 함께 적분기로 되먹인다. 자르기보다 부드럽게 되감긴다.
- *왜 $\int e$가 아니라 $K_i\int e$를 저장하나?* 그러면 실행 중에 $K_i$를 바꿔도 출력이 튀지 않는다(무충격 이득 변경).
- *미분 필터는 어떻게 고르나?* $T_d = K_d/K_p$이고 $N$이 대략 5–20일 때 시정수 약 $T_d/N$이다. 필터의 지연은 위상 여유를 깎으니, 잡음이 요구하는 이상으로 세게 거르지 마라.
- *루프 주기가 흔들린다.* 호출마다 실제 $\Delta t$를 재고, $\Delta t = 0$을 막아라.

**이론.** 각 항이 폐루프에 하는 일, 적분 와인드업, 위상 여유: [[04-robotics/control-theory-ce397|5. 제어 이론 §7]].

### 8. 강체 변환과 회전 행렬에서 쿼터니언으로의 변환

**문제.** *"4 × 4 자세를 합성하고 역을 구하라. 그다음 회전 행렬을 단위 쿼터니언으로, 절대 0으로 나누지 않는 방식으로 바꾸고 테스트하라."*

**실제로 보는 것.** 좌표계 규율($T_{AC} = T_{AB}T_{BC}$), 닫힌 형태의 역, 자기가 쓰는 쿼터니언 규약, 흔한 한 줄짜리 변환이 180° 근처에서 실패한다는 것을 아는지다.

**핵심 아이디어.** 자세의 역은 [[02-foundations/se3-geometry|8. SE(3) §3]]에 있듯 $(R, p)^{-1} = (R^\top, -R^\top p)$다. 쿼터니언은 그 페이지의 스칼라 우선 순서 $q = (w, x, y, z)$를 쓴다. Modern Robotics의 $(q_0, q_1, q_2, q_3)$와 같다. $R$의 대각 성분이 모든 성분의 제곱을 정한다. 단위 쿼터니언에서 $R_{11} = 1 - 2(y^2 + z^2)$, $R_{22} = 1 - 2(x^2 + z^2)$, $R_{33} = 1 - 2(x^2 + y^2)$이므로 $\operatorname{tr}R = 3 - 4(x^2 + y^2 + z^2) = 4w^2 - 1$이다. 따라서 $4w^2 = 1 + \operatorname{tr}R$, $4x^2 = 1 + 2R_{11} - \operatorname{tr}R$이고, $y$와 $z$도 마찬가지다. 익숙한 공식은 $w$를 이렇게 구한 뒤 비대각 차이를 $4w$로 나눈다. 180° 회전 근처에서는 $w \to 0$이라 그 나눗셈이 불안정하다. 해결책은 *가장 큰* 성분부터 구하는 것이다. 네 제곱의 합이 1이므로 가장 큰 성분은 $\lvert q_i\rvert \ge 1/2$이고, 모든 나눗셈의 분모가 적어도 2다. 나머지 세 성분은 대칭인 비대각 쌍의 합이나 차에서 나온다.

```python
import numpy as np

def make_T(R, p):
    T = np.eye(4)
    T[:3, :3], T[:3, 3] = R, p
    return T

def inv_T(T):
    """Closed-form inverse: (R, p)^-1 = (R^T, -R^T p). Never np.linalg.inv on a pose."""
    R, p = T[:3, :3], T[:3, 3]
    return make_T(R.T, -R.T @ p)

Rz90 = np.array([ [0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0] ])
T_AB = make_T(Rz90, [2.0, 0.0, 0.0])             # base in world
T_BC = make_T(np.eye(3), [1.0, 0.0, 0.0])        # camera in base
T_AC = T_AB @ T_BC                               # subscripts cancel: A<-B<-C
print(T_AC[:3, 3], np.allclose(inv_T(T_AC) @ T_AC, np.eye(4)))
```

```python
import numpy as np

def quat_to_rot(q):
    """Unit quaternion q = (w, x, y, z), scalar first, to a rotation matrix."""
    w, x, y, z = q
    return np.array([ [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                      [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                      [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)] ])

def rot_to_quat(R):
    """Rotation matrix to unit quaternion (w, x, y, z) with w >= 0. Solves for the largest
    component first, so no division by a number near zero (the trace-only formula fails near 180 deg)."""
    t = np.trace(R)
    four_sq = np.array([1 + t, 1 + 2 * R[0, 0] - t, 1 + 2 * R[1, 1] - t, 1 + 2 * R[2, 2] - t])  # 4 q_i^2
    i = int(np.argmax(four_sq))
    s = 2.0 * np.sqrt(four_sq[i])                # s = 4 |q_i|
    sums = {"xy": R[0, 1] + R[1, 0], "xz": R[0, 2] + R[2, 0], "yz": R[1, 2] + R[2, 1]}
    difs = {"x": R[2, 1] - R[1, 2], "y": R[0, 2] - R[2, 0], "z": R[1, 0] - R[0, 1]}  # each = 4 w q_axis
    q = {0: [s / 4, difs["x"] / s, difs["y"] / s, difs["z"] / s],
         1: [difs["x"] / s, s / 4, sums["xy"] / s, sums["xz"] / s],
         2: [difs["y"] / s, sums["xy"] / s, s / 4, sums["yz"] / s],
         3: [difs["z"] / s, sums["xz"] / s, sums["yz"] / s, s / 4]}[i]
    q = np.array(q) / np.linalg.norm(q)          # absorb round-off from a slightly non-orthogonal R
    return q if q[0] >= 0 else -q                # q and -q are the same rotation: pick one

theta = np.radians(179.9)                        # near 180 deg, where w = cos(theta/2) ~ 0
q = np.array([np.cos(theta / 2), 0.0, np.sin(theta / 2), 0.0])
print(rot_to_quat(quat_to_rot(q)).round(6), q.round(6))
```

**복잡도.** $O(1)$이다. 이 크기에서 `np.linalg.inv`도 $O(1)$이지만 구조를 무시하고, 더 느리고, 회전 블록이 정확히 정규직교가 아닌 행렬을 돌려준다.

**테스트 방법.** 4차원 가우시안 벡터를 정규화하면 균등한 무작위 단위 쿼터니언이 되므로, 이것으로 무작위 회전을 만든다. 20 000개에 대해 행렬로 바꿨다가 되돌려 결과가 $q$ 또는 $-q$이고 $w \ge 0$인지 확인한다. 각 축에 대해 $\pi$, $\pi - 10^{-9}$, $\pi - 10^{-4}$ 각도를 확인하고, 로드리게스 공식으로 축-각도에서 따로 만든 쿼터니언과 비교하며, `inv_T`가 일반 역행렬과 같고 $(T_aT_b)^{-1} = T_b^{-1}T_a^{-1}$인지 확인한다.

**꼬리 질문.**
- *라이브러리는 어떤 순서를 쓰나?* 같지 않다. Eigen의 생성자는 $(w, x, y, z)$를 받지만 $(x, y, z, w)$로 저장하고, ROS 메시지와 SciPy의 기본값은 스칼라가 마지막이다. 쿼터니언 버그 대부분은 순서 불일치이니, 모든 함수 시그니처에 순서를 적어라.
- *왜 $w \ge 0$으로 뒤집나?* $q$와 $-q$는 같은 회전이다. 부호를 정해 두면 출력끼리 비교할 수 있고, 학습 회귀 목표가 튀지 않는다. 다만 $w = 0$에서 표현이 연속이 되지는 않는다.
- *두 자세 사이의 각도는?* $2\arccos\lvert\langle q_1, q_2\rangle\rvert$다. 절댓값이 이중 덮개를 처리한다.
- *적분한 회전 행렬이 정규직교에서 벗어난다.* SVD로 다시 사영하거나($R \leftarrow UV^\top$), 쿼터니언을 유지하며 재정규화한다.
- *쿼터니언은 어떻게 합성하나?* 이 규약에서 해밀턴 곱 $q_1 \otimes q_2$가 $R_1R_2$에 대응한다. 다른 모든 것처럼 행렬과 수치적으로 대조해 확인하라.

**이론.** 네 가지 회전 표현과 자세 합성: [[02-foundations/se3-geometry|8. SE(3) §2]], [[02-foundations/se3-geometry|8. SE(3) §3]].

### 9. 안정적인 softmax, log-softmax, 교차 엔트로피, 그리고 그래디언트 검사

**문제.** *"NumPy로 로짓에서 softmax와 교차 엔트로피 손실, 그리고 그 그래디언트를 구현하라. 수천 단위 로짓에서도 NaN을 내면 안 된다. 그래디언트가 맞다는 것을 보여라."*

**실제로 보는 것.** 이동 기법, `log(softmax(z))`를 절대 계산하지 않는 것, 평균 손실의 $1/N$까지 포함한 $p - y$ 그래디언트, 유한 차분 그래디언트 검사를 짜고 그 간격을 고를 줄 아는지다.

**핵심 아이디어.** 모든 로짓에서 같은 상수를 빼도 softmax는 변하지 않으므로 최댓값을 뺀다. 가장 큰 지수는 $e^0 = 1$이 되고 아무것도 넘치지 않는다. 그러면 log-softmax는 $z_j - \log\sum_k e^{z_k}$(log-sum-exp)이고, 0으로 반올림된 수의 로그를 취하는 일이 없다. $N$개 예제에 대한 평균 교차 엔트로피의 로짓 그래디언트는 $(p - y)/N$이며, [[02-foundations/calculus-backprop|2. 미적분과 역전파 §4]]에서 유도한다.

```python
import numpy as np

def log_softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)      # shift invariance: largest logit becomes 0, no overflow
    return z - np.log(np.exp(z).sum(axis=axis, keepdims=True))   # log-sum-exp

def softmax(z, axis=-1):
    return np.exp(log_softmax(z, axis))

def cross_entropy(logits, labels):
    """logits (N, C), integer labels (N,). Returns mean loss and dL/dlogits, shape (N, C)."""
    N = logits.shape[0]
    lp = log_softmax(logits)
    loss = -lp[np.arange(N), labels].mean()      # never log(softmax(z)): softmax can round to 0
    grad = np.exp(lp)
    grad[np.arange(N), labels] -= 1.0            # p - y, one row per example
    return loss, grad / N                        # the 1/N from the mean

def numerical_grad(f, z, eps=1e-6):
    """Central differences, one coordinate at a time. Use float64."""
    g = np.zeros_like(z)
    for i in np.ndindex(z.shape):
        old = z[i]
        z[i] = old + eps; f_plus = f(z)
        z[i] = old - eps; f_minus = f(z)
        z[i] = old
        g[i] = (f_plus - f_minus) / (2 * eps)
    return g

rng = np.random.default_rng(0)
logits, labels = rng.normal(size=(4, 5)), np.array([0, 3, 1, 4])
loss, grad = cross_entropy(logits, labels)
num = numerical_grad(lambda z: cross_entropy(z, labels)[0], logits.copy())
print(np.abs(grad - num).max() / np.abs(grad).max(), softmax(np.array([1000.0, 0.0])))
```

**복잡도.** 시간과 메모리 모두 $O(NC)$다. 그래디언트 검사는 파라미터마다 손실을 두 번 계산하므로 여기서는 $O(N^2C^2)$이고, 아주 작은 입력에서만 돌린다.

**꼬리 질문.**
- *`eps`는 어떻게 고르나?* 중앙 차분의 절단 오차는 $O(\varepsilon^2)$, 반올림 오차는 기계 정밀도 근처의 $\delta$에 대해 $O(\delta/\varepsilon)$이다. 그래서 float64에서는 $10^{-5}$–$10^{-6}$ 정도의 $\varepsilon$이 둘을 맞춘다. 상대 오차를 보고하고, 대략 $10^{-7}$ 아래면 통과다. float32에서는 검사를 믿을 수 없다.
- *$\partial L/\partial z = p - y$가 실제로 왜 중요한가?* $p$로 나누지 않는다. softmax를 구한 뒤 $-\log p$의 미분을 따로 계산하면 $p$로 나누게 되고, $p$가 언더플로하면 실패한다. 프레임워크가 둘을 하나의 연산으로 합치는 이유다.
- *이진 분류는?* 로짓을 직접 쓴다. `sigmoid` 다음 `log`가 아니라 `np.logaddexp(0, -z)`로 $\log(1 + e^{-z})$를 계산한다.
- *온도는?* softmax 전에 로짓을 $T$로 나눈다. 그래디언트에 $1/T$ 인자가 붙는다.
- *패딩 레이블은 무시해야 한다.* 그 행들을 손실과 그래디언트 모두에서 가리고, $N$이 아니라 실제 레이블 수로 나눈다.

**이론.** softmax–교차 엔트로피 그래디언트, 그리고 분류 헤드와 어텐션에서의 자리: [[02-foundations/calculus-backprop|2. 미적분과 역전파 §4]].

### 10. 인과 스케일드 닷프로덕트 셀프 어텐션

**문제.** *"NumPy로 시퀀스 배치에 대한 단일 헤드 인과 셀프 어텐션 층을 짜라. 모든 텐서의 모양을 말하라. 어떤 위치도 미래를 보지 않는다는 것을 보여라."*

**실제로 보는 것.** 배치에서의 모양과 축 순서, softmax *전에* 마스크를 거는 것, $\sqrt{d_k}$ 스케일, $O(T^2)$ 메모리 비용과 생성 시점에 무슨 일이 일어나는지 아는지다.

**핵심 아이디어.** [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|어텐션 노트]]에서: $\operatorname{Attention}(Q, K, V) = \operatorname{softmax}(QK^\top/\sqrt{d_k})\,V$. 투영이 모양 $(B, T, d_{\text{model}})$의 $X$를 모양 $(B, T, d_k)$의 $Q, K$와 모양 $(B, T, d_v)$의 $V$로 바꾼다. 점수 표의 모양은 $(B, T, T)$이고, 행 $t$가 질의 위치 $t$다. 인과 모델은 $s > t$인 위치를 쓸 수 없으므로 softmax 전에 그 점수를 $-\infty$로 둔다. 그러면 가중치가 정확히 0이 되고, 각 행의 나머지 가중치는 여전히 합이 1이다.

```python
import numpy as np

def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)      # -inf entries stay -inf and become exactly 0
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

def causal_self_attention(X, Wq, Wk, Wv):
    """X: (B, T, d_model). Wq, Wk: (d_model, d_k). Wv: (d_model, d_v).
    Returns output (B, T, d_v) and weights (B, T, T); row t = query t, column s = key s."""
    Q, K, V = X @ Wq, X @ Wk, X @ Wv             # (B, T, d_k), (B, T, d_k), (B, T, d_v)
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(Q.shape[-1])     # (B, T, T)
    T = X.shape[1]
    future = np.triu(np.ones((T, T), dtype=bool), k=1)           # True where s > t
    scores = np.where(future, -np.inf, scores)   # mask before softmax, never after
    weights = softmax(scores, axis=-1)           # each row sums to 1 over s <= t
    return weights @ V, weights

rng = np.random.default_rng(0)
B, T, d_model, d_k = 2, 5, 16, 8
X = rng.normal(size=(B, T, d_model))
Wq, Wk, Wv = (rng.normal(size=(d_model, d_k)) / np.sqrt(d_model) for _ in range(3))
out, W = causal_self_attention(X, Wq, Wk, Wv)
print(out.shape, W.shape, W[0].round(2))
```

**복잡도.** 시간 $O(BT^2d_k + BTd_{\text{model}}d_k)$, 점수 표를 위한 메모리 $O(BT^2)$이다. 긴 시퀀스에서는 이 메모리가 지배한다.

**테스트 방법.** 대각선 위의 모든 가중치가 정확히 0이고 모든 행의 합이 1이다. 위치 3 이후의 입력을 바꿔도 위치 0–2의 출력은 변하지 않는다. 출력은 위치마다 도는 명시적 루프의 결과와 같다.

**꼬리 질문.**
- *왜 $\sqrt{d_k}$로 나누나?* 질의와 키의 성분이 독립이고 분산이 1이라면 내적의 분산은 $d_k$다. 성분의 평균이 0이면 곱 $q_i k_i$ 하나의 분산이 $1 \cdot 1 = 1$이고, 독립인 $d_k$개 항의 분산은 더해지기 때문이다. 스케일하지 않은 점수는 차원과 함께 커져 softmax를 포화 영역으로 밀고, 거기서는 그래디언트가 사라진다.
- *왜 큰 음수가 아니라 $-\infty$인가?* $-\infty$는 정확히 0을 준다. 유한한 $-10^9$도 float32에서는 되지만 float16에서는 넘치므로, 프레임워크는 그 dtype의 최솟값을 쓴다. 한 행 전체가 가려지면(완전히 패딩된 시퀀스처럼) $-\infty$는 NaN을 주니, 그런 행은 따로 처리하라.
- *멀티헤드는?* $h$개 헤드로 투영하고 $(B, h, T, d_k)$로 모양을 바꾼 뒤 헤드 축에 같은 함수를 돌리고, 이어 붙여 출력 투영을 적용한다.
- *토큰을 하나씩 생성한다면?* 지난 위치들의 키와 값을 캐시한다(KV 캐시). 새 토큰마다 캐시된 키 $t$개에 대한 질의 하나만 필요하므로, 전체 $O(t^2)$ 표를 다시 계산하는 대신 $O(t)$다. 인과 마스크는 암묵적이다.
- *시퀀스가 100 000 토큰이다.* $T \times T$ 표가 메모리에 들어가지 않는다. 표를 만들지 않고 블록 단위로 계산하는 정확한 어텐션(FlashAttention)이 보통의 답이다. 희소 어텐션이나 선형 어텐션은 모델 자체를 바꾼다.
- *패딩 마스크와 인과 마스크를 함께?* softmax 전에 논리 OR로 합치고, 패딩 마스크는 질의 축으로 브로드캐스트한다.

**이론.** 어텐션이 계산하는 것, 멀티헤드 어텐션, 요즘 쓰이는 블록: [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]].

### 연습하는 법

1. **각 문제를 빈 파일에서 20분 안에 짜라.** 짜면서 아이디어, 불변식, 모양을 소리 내어 말하라. 답을 아는 손수 만든 입력으로 돌려 보라.
2. **그다음, 이 페이지를 보기 전에 테스트를 먼저 써라.** 성질 테스트(전수 탐색과 KD-tree가 같다, 체계적 복사 수는 내림이나 올림이다, 무작위 회전에서 왕복한다)는 예제 하나로는 못 잡는 것을 잡는다.
3. **그다음, 꼬리 질문 하나만큼 확장하라.** k-최근접, 적응형 RANSAC, 게이팅한 칼만 갱신, 역계산 안티와인드업, 멀티헤드 어텐션.
4. **일주일에 두 문제를 노트 없이 다시 풀어라.** 25분이 넘게 걸리면 코드의 모양은 기억하지만 이유는 기억하지 못하는 것이니, 이론 링크를 다시 읽어라.
5. **실무에서 무엇을 쓸지 말하라.** 문제마다 라이브러리(SciPy, Open3D, Eigen, 프레임워크의 통합 교차 엔트로피)를 대고, 이제 이해하게 된 파라미터 하나를 말하라.

### 스스로 점검

1. A*가 4-연결 격자에서는 맞았는데, 대각 비용 √2인 8-연결로 바꾼 뒤 가끔 최적보다 긴 경로를 돌려준다. 가장 그럴듯한 버그는?
2. 벡터화한 최근접 탐색이 가끔 거리 제곱을 $-2 \times 10^{-13}$으로 보고하고 `np.sqrt`가 NaN을 돌려준다. 왜 그렇고, 어떻게 고치나?
3. 인라이어 30 %, $p = 0.99$로 평면을 맞출 때 RANSAC 표본은 몇 번 필요한가? 인라이어가 60 %라면?
4. 일부러 최적이 아닌 이득을 쓸 때, Joseph 형태의 공분산 갱신은 여전히 맞는데 $(I - KH)P^-$는 왜 틀리나?
5. 가중치가 $(0.25, 0.25, 0.25, 0.25)$다. 유효 표본 크기는? 체계적 재표본추출은 무엇을 돌려주나? 재표본추출해야 하나?
6. $L_1 = 1$, $L_2 = 0.5$일 때 목표 $(0.3, 0)$에 닿을 수 있나? 이유를 한 줄로.
7. 긴 포화 동안 PID의 적분기가 와인드업되었다. 오차의 부호가 바뀌면 출력이 어떻게 되는지, §7의 어느 줄이 이를 막는지 설명하라.
8. `rot_to_quat`가 $x$축에 대한 180° 회전을 변환해야 한다. 어느 가지가 실행되고, 같은 입력에서 대각합만 쓰는 공식은 어떻게 되나?
9. 교차 엔트로피 그래디언트 검사가 `eps = 1e-6`로 float64에서는 통과하는데 float32에서는 실패한다. 그래디언트가 틀린 것인가?
10. 인과 어텐션에서 가중치 행렬의 첫 행은 무엇이고, 왜 그런가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 휴리스틱이다. 맨해튼 거리는 대각 한 걸음을 과대추정하므로(√2에 대해 2) 이 이동 집합에서 허용적이지 않다. 옥타일 거리를 써라. 다른 후보는 막힌 두 칸 사이를 대각으로 가르는 것인데, 이것은 더 긴 경로가 아니라 유효하지 않은 경로를 만든다.
> 2. 전개식 $\lVert q\rVert^2 - 2q^\top p + \lVert p\rVert^2$는 $q$가 $p$에 가까우면 거의 같은 수끼리 빼므로 반올림 오차가 0 아래로 내려갈 수 있다. 제곱근 전에 `np.maximum(d2, 0.0, out=d2)`처럼 0에서 자른다.
> 3. $s = 3$이다. $w = 0.3$이면 $w^3 = 0.027$이고 $k = \lceil \log 0.01 / \log 0.973\rceil = 169$다. $w = 0.6$이면 $w^3 = 0.216$이고 $k = \lceil 4.605/0.2433\rceil = 19$다.
> 4. Joseph 형태는 실제로 쓴 $K$가 무엇이든 $x^- + K(z - Hx^-)$의 공분산을 직접 계산한 것이다. 사전 오차는 $(I - KH)$를, 측정 잡음은 $K$를 통과한다. 짧은 형태는 그 식에 최적 $K$를 대입해 얻었으므로 그 이득에서만 참 공분산과 같고, 그때조차 반올림 오차가 대칭성을 깬다.
> 5. $M_{\text{eff}} = 1/(4 \cdot 0.0625) = 4 = M$이다. $M w_i = 1$은 그 자체가 내림이자 올림이므로 체계적 재표본추출은 각 입자를 정확히 한 번씩 돌려준다. 재표본추출할 필요가 없다. ESS가 이미 최대이므로 같은 집합을 돌려줄 뿐이고, 일반적으로는 잡음만 더할 수 있다.
> 6. 아니다. 닿는 고리 영역은 $0.5 \le r \le 1.5$이고 $r = 0.3 < \lvert L_1 - L_2\rvert$다.
> 7. 오차가 뒤집힌 뒤에도 적분 항이 크게 남아, 음의 오차가 그것을 다시 적분해 끌어내릴 때까지 출력이 포화된 채로 머물고 큰 오버슈트가 생긴다. `pushing_further` 검사가, 출력이 한계에 있고 오차가 그쪽으로 더 밀 때 적분을 멈춘다.
> 8. $\operatorname{tr}R = -1$이므로 $4w^2 = 0$, $4x^2 = 1 + 2 - (-1) = 4$다. $x$ 가지가 $s = 4$로 실행되어 $q = (0, 1, 0, 0)$을 준다. 대각합만 쓰는 공식은 $w = 0$을 구한 뒤 $4w = 0$으로 나눠 inf나 NaN을 낸다.
> 9. 아마 아니다. float32에서는 약 $10^{-7}$의 반올림 오차를 $\varepsilon = 10^{-6}$으로 나눈 값이 도함수 자체와 비슷한 크기가 된다. float64에서 검사하라. 거기서 통과한 것이 증거다.
> 10. $(1, 0, \dots, 0)$이다. 위치 0은 자기 자신만 볼 수 있으므로, 마스크 뒤 softmax에 유한한 항이 하나만 남고 그 항이 모든 가중치를 받는다.

### 출처

영어 절의 Sources 목록과 같다. 원 논문은 Hart·Nilsson·Raphael (1968), Bentley (1975), Friedman·Bentley·Finkel (1977), Fischler·Bolles (1981), Torr·Zisserman (2000), Kalman (1960), Gordon·Salmond·Smith (1993), Douc·Cappé·Moulines (2005), Wampler (1986), Nakamura·Hanafusa (1986), Shoemake (1985), Vaswani 외 (2017), Dao 외 (2022)이고, 교재는 Thrun·Burgard·Fox *Probabilistic Robotics*, Lynch·Park *Modern Robotics*, Bucy·Joseph *Filtering for Stochastic Processes with Applications to Guidance*, Åström·Hägglund *Advanced PID Control*, Goodfellow·Bengio·Courville *Deep Learning*이다.
