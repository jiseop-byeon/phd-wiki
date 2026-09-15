---
title: 11.6 Graph Algorithms & Search
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Implement BFS, DFS, topological sort, Dijkstra, Bellman–Ford and grid A* from a blank file, and state for each the invariant that makes it correct and the input that breaks it."
mastery-when: "Raise to Mastery if you build or modify a search-based planner, where heuristic design, incremental replanning and memory layout become the contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/data-structures|11.2 Core Data Structures]] (queue, stack, binary heap, hash map) · Bellman–Ford is dynamic programming, so [[02-foundations/algorithms/dynamic-programming|11.5]] helps but is not required
> [[02-foundations/algorithms/data-structures|11.2 핵심 자료구조]](큐, 스택, 이진 힙, 해시 맵) · Bellman–Ford는 동적 계획법이므로 [[02-foundations/algorithms/dynamic-programming|11.5]]가 도움이 되지만 필수는 아니다

## English

*The graph page of the algorithms track. It owns the mechanics and the code; the planning
pages own what a planner is for. Read [[04-robotics/planning-decision-making|4. Planning & Decision-Making]] for costmaps, inflation and the global/local split, and [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]] for why grids stop scaling.*

Graph questions are the most common single topic in both kinds of interview. A coding
interview hides the graph: a word ladder, a course schedule, islands in a matrix. A robotics
lab names it: "write A* on this occupancy grid", "why can't Dijkstra handle negative costs",
"what does a consistent heuristic buy you". Both reward the same three habits: pick the
representation first, know the invariant that makes the algorithm correct, and know the one
input that breaks the naive version.

> [!note] First pass · 처음이라면
> Read §1, §2 and §4, then write the grid A* in §6 from memory. §3 and §5 are the interview variants; §7 is the idea that makes all of them one algorithm.

### 1. Representations

A graph is a set of vertices $V$ and edges $E$; write $n = \lvert V\rvert$ and $m = \lvert E\rvert$. The
representation decides the cost of the two operations every search repeats: *list the
neighbours of $u$* and *is $(u, v)$ an edge?*

**The vocabulary, each term defined.** A **graph** is a pair $G = (V, E)$, a finite vertex set and an edge set, with these parts:

- **Directed or undirected.** In a directed graph an edge is an *ordered* pair $(u, v)$, written $u \to v$, and can be followed only from $u$ to $v$. In an undirected graph an edge is an *unordered* pair $\{u, v\}$ and can be followed both ways.
- **Weights.** A weighted graph adds a function $w : E \to \mathbb{R}$ giving each edge a cost; an unweighted graph is the case $w \equiv 1$.
- **Degree.** In a directed graph the out-degree and in-degree of $v$ count the edges leaving and entering it, $\deg^+(v) = \lvert\{u : (v, u) \in E\}\rvert$ and $\deg^-(v) = \lvert\{u : (u, v) \in E\}\rvert$; in an undirected graph $\deg v$ counts the edges touching $v$.
- **Path, simple path, cycle.** A path is a vertex sequence $v_0, v_1, \dots, v_k$ with every $(v_{i-1}, v_i) \in E$; it is simple if no vertex repeats, and it is a cycle if $k \ge 1$ and $v_k = v_0$ (in an undirected graph a cycle also needs $k \ge 3$ with no edge reused). Its weight is the sum of its edge weights, as the formula below says.
$$w(P) = \sum_{i=1}^{k} w(v_{i-1}, v_i)$$
- **Sparse and dense.** Since a simple directed graph has at most $n(n-1)$ edges, $m$ lies between $0$ and about $n^2$; a graph is called sparse when $m = O(n)$ and dense when $m = \Theta(n^2)$.

*Example.* The directed edges in the code below, $a \to b$ (4), $a \to c$ (1), $c \to b$ (2), $b \to d$ (5), give $n = m = 4$, $\deg^+(a) = 2$ and $\deg^-(b) = 2$. The path $a, c, b, d$ has weight $1 + 2 + 5 = 8$ and $a, b, d$ has weight $4 + 5 = 9$. *Non-example:* $d, b$ is not a path, because the edge is $b \to d$ and a directed edge cannot be walked backwards.

| | Adjacency list | Adjacency matrix | Implicit (grid, lattice) |
|---|---|---|---|
| Memory | $O(n + m)$ | $O(n^2)$ | occupancy only; edges are never stored |
| Neighbours of $u$ | $O(\deg u)$ | $O(n)$ | $O(k)$, $k$ = 4 or 8 on a grid |
| Edge test $(u, v)$ | $O(\deg u)$; $O(1)$ expected with a set | $O(1)$ | $O(1)$ |
| One BFS/DFS | $O(n + m)$ | $O(n^2)$ | $O(n)$, since $m \le kn$ |
| Use when | sparse graphs, which is nearly all real ones | dense graphs, a few thousand vertices, Floyd–Warshall | occupancy grids, state lattices, puzzles whose states are generated |

The matrix loses on memory long before it loses on speed: $10^4$ vertices need $10^8$
entries, which is 800 MB as `float64`. A road network or a roadmap with average degree 4 needs
about $4 \times 10^4$ list entries for the same vertex count. A grid is the extreme case: an
$H \times W$ map *is* the graph, and neighbours are computed from the cell index when asked.

```python
from collections import defaultdict

edges = [("a", "b", 4), ("a", "c", 1), ("c", "b", 2), ("b", "d", 5)]

adj = defaultdict(list)                  # adjacency list: O(n + m) memory
for u, v, w in edges:
    adj[u].append((v, w))                # directed; also append (u, w) to adj[v] if undirected

names = sorted({x for u, v, _ in edges for x in (u, v)})
index = {name: i for i, name in enumerate(names)}
INF = float("inf")
mat = [ [INF] * len(names) for _ in names ]  # adjacency matrix: O(n^2) memory
for u, v, w in edges:
    mat[index[u]][index[v]] = w

def grid_neighbors(grid, r, c):          # implicit graph: edges computed, never stored
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0:
            yield nr, nc

tiny = [
    [0, 1],
    [0, 0],
]
print(adj["a"], mat[index["a"]][index["c"]], list(grid_neighbors(tiny, 0, 0)))
```

**Pitfalls.** A `defaultdict` creates a key when you *read* a missing vertex, so
`for u in adj: ... adj[v] ...` can raise "dictionary changed size during iteration"; and a
vertex with no outgoing edge never appears as a key unless you add it. Build the vertex set
explicitly when an algorithm needs every vertex (topological sort, SCC). For undirected graphs,
store each edge in both lists and remember that $m$ then counts twice.

### 2. BFS and DFS

**Breadth-first search** explores in rings: every vertex one edge away, then every vertex two
edges away. So the first time BFS reaches a vertex, it has reached it by a path with the fewest
edges. Stated precisely, BFS from a source $s$ is a graph traversal that computes, for every vertex, the **unweighted distance** (hop count), where the minimum over an empty set is $\infty$ so unreachable vertices get $\infty$:

$$\text{dist}(v) = \min\{\,k : \text{there is a path } s = v_0, v_1, \dots, v_k = v\,\}$$

*Why that is true.* The queue always holds vertices whose distances are non-decreasing from
front to back and differ by at most one. A vertex $v$ is discovered from the first dequeued
neighbour $u$, and $u$ is dequeued no later than any other neighbour of $v$, so
`dist[v] = dist[u] + 1` is the minimum. *Cost:* each vertex is enqueued once, each adjacency
list is scanned once, so $O(n + m)$. A parent map recorded at discovery time turns distances
into paths: walk the parents back from the target and reverse.

```python
from collections import deque

def bfs_path(adj, s, t):
    parent = {s: None}                   # doubles as the visited set
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return path[::-1]
        for v in adj.get(u, ()):
            if v not in parent:          # mark on ENQUEUE, not on dequeue
                parent[v] = u
                q.append(v)
    return None

adj = {"s": ["a", "b"], "a": ["c"], "b": ["c"], "c": ["t"]}
print(bfs_path(adj, "s", "t"))           # ['s', 'a', 'c', 't']
```

**BFS pitfalls.** Marking a vertex visited when it is *dequeued* keeps distances correct (if later copies are
skipped) but lets the same vertex sit in the queue once per incoming edge. `list.pop(0)` is $O(n)$, which
turns BFS into $O(n^2)$; use `collections.deque`. BFS is wrong on weighted edges, with one cheap
exception: if every weight is 0 or 1, push 0-edges to the *front* of the deque and 1-edges to the
back (0-1 BFS), still $O(n + m)$. Seeding the queue with many sources at distance 0 gives
**multi-source BFS**, which on an occupancy grid is the *brushfire* distance transform: the
distance from every free cell to its nearest obstacle in one pass. It computes the distance to the *nearest* member of the source set $S$, which is correct because a single BFS from an imaginary super-source joined to every $s \in S$ by a free edge would enqueue exactly the same vertices in the same order:

$$\text{dist}_S(v) = \min_{s \in S} \text{dist}_s(v)$$

*Example.* A one-row map with obstacles at both ends, cells $[1, 0, 0, 0, 1]$, gives distances $[0, 1, 2, 1, 0]$: the middle cell is two steps from either wall.

**Depth-first search** follows one branch as far as it goes, then backs up. Its value is not the
order it visits vertices but the *timestamps* it leaves: a vertex is **discovered** when first
entered and **finished** when every edge out of it has been explored. For any two vertices the
discovery–finish intervals are either nested or disjoint, like parentheses. With one clock that ticks at every discovery and every finish, write $d(u)$ and $f(u)$ for the two times; the **parenthesis theorem** says that for any two vertices $u \ne v$ exactly one of these holds, since a vertex discovered while $u$ is open must finish before $u$ does:

$$[d(u), f(u)] \cap [d(v), f(v)] = \varnothing \quad\text{or}\quad [d(v), f(v)] \subset [d(u), f(u)] \quad\text{or}\quad [d(u), f(u)] \subset [d(v), f(v)]$$

The times classify every directed edge $u \to v$ at the moment DFS examines it, by the colour of $v$:

- **Tree edge:** $v$ is white, so DFS enters $v$ through this edge.
- **Back edge:** $v$ is gray, meaning $v$ is an ancestor of $u$ still on the stack.
- **Forward edge:** $v$ is black and $d(u) < d(v)$, so $v$ is a finished descendant reached earlier by another route.
- **Cross edge:** $v$ is black and $d(v) < d(u)$, so $v$ lies in a subtree that was already finished.

*Example.* Edges $a \to b$, $b \to c$, $a \to c$, $d \to c$, visited in that order. DFS gives $a$: 1/6, $b$: 2/5, $c$: 3/4, $d$: 7/8 (discovery/finish). So $a \to b$ and $b \to c$ are tree edges, $a \to c$ is a forward edge ($c$ black, $1 < 3$), and $d \to c$ is a cross edge ($c$ black, $3 < 7$). $[3, 4] \subset [2, 5] \subset [1, 6]$ are nested and $[7, 8]$ is disjoint from all of them. There is no back edge, so no cycle.

That structure is what detects cycles. Colour a vertex gray while it is on the recursion stack
and black once finished. In a directed graph, meeting a *gray* neighbour means an edge back to an
ancestor still being explored, which is a cycle; a directed graph has a cycle exactly when DFS
finds such a back edge. *Non-example:* forward and cross edges do not signal a cycle, which is why a "visited" flag alone (black or gray lumped together) reports false cycles on the graph above. In an undirected graph every edge is stored both ways, so ignore the
edge to the vertex you just came from, and any other visited neighbour closes a cycle (with
parallel edges, compare edge ids rather than parent vertices). DFS is also $O(n + m)$.

```python
def dfs_recursive(adj):
    """adj must list every vertex as a key. Returns (finish order, has_cycle)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in adj}
    finish, has_cycle = [], False

    def visit(u):
        nonlocal has_cycle
        color[u] = GRAY                  # discovered, still on the stack
        for v in adj[u]:
            if color[v] == GRAY:
                has_cycle = True         # back edge: directed cycle
            elif color[v] == WHITE:
                visit(v)
        color[u] = BLACK                 # finished
        finish.append(u)

    for u in adj:
        if color[u] == WHITE:
            visit(u)
    return finish, has_cycle

print(dfs_recursive({"a": ["b"], "b": ["c"], "c": []}))   # (['c', 'b', 'a'], False)
```

Python's default recursion limit is 1000 frames, so a DFS down a long corridor of a
$100 \times 100$ grid crashes with `RecursionError`. Raising the limit helps only up to a point: deep
recursion is slow and can still crash the process on some Python versions. The robust version keeps an explicit stack of *(vertex, iterator over its neighbours)*,
which reproduces the recursive discovery and finish order exactly:

```python
def dfs_iterative(adj):
    """Same finish order and cycle test as dfs_recursive, with no recursion."""
    color, finish, has_cycle = {u: 0 for u in adj}, [], False
    for root in adj:
        if color[root]:
            continue
        color[root] = 1
        stack = [(root, iter(adj[root]))]
        while stack:
            u, it = stack[-1]
            v = next(it, None)
            if v is None:                # every neighbour done: u finishes
                color[u] = 2
                finish.append(u)
                stack.pop()
            elif color[v] == 1:
                has_cycle = True
            elif color[v] == 0:
                color[v] = 1
                stack.append((v, iter(adj[v])))
    return finish, has_cycle

print(dfs_iterative({"a": ["b"], "b": ["c"], "c": ["a"]}))  # (['c', 'b', 'a'], True)
```

The common shortcut, "BFS with a stack" (push all neighbours, mark on pop), does visit vertices
depth-first, but it never knows when a vertex finishes, so it cannot give a topological order or
use the gray test.

### 3. Topological sort and strongly connected components

A **topological order** of a directed graph lists the vertices so that every edge points
forward. It exists exactly when the graph is a DAG (directed acyclic graph). Both terms, precisely:

- A **DAG** is a directed graph that contains no directed cycle, that is, no path $v_0 \to v_1 \to \dots \to v_k$ with $k \ge 1$ and $v_k = v_0$ (§1).
- A **topological order** is a numbering of the vertices, a bijection $\pi : V \to \{1, \dots, n\}$, such that every edge goes from a smaller number to a larger one, so that for every edge $(u, v)$, $u$ precedes $v$:
$$\pi(u) < \pi(v) \quad \text{for every edge } (u, v) \in E$$
- **Why "exactly when DAG".** If a cycle $v_0 \to \dots \to v_k = v_0$ existed, the condition would give $\pi(v_0) < \pi(v_1) < \dots < \pi(v_k) = \pi(v_0)$, which is impossible; conversely, Kahn's algorithm below builds an order for every DAG.

*Example.* For the build graph in the code below (`msgs` → `driver`, `msgs` → `planner`, `driver` → `bringup`, `planner` → `bringup`), both `msgs, driver, planner, bringup` and `msgs, planner, driver, bringup` are topological orders, so the order is generally not unique. *Non-example:* `msgs, bringup, driver, planner` fails, because the edge `driver` → `bringup` points backwards. Interviews dress it
as course prerequisites or build order; robotics uses it for the same thing: `colcon` builds ROS 2
packages in dependency order, an assembly sequence installs columns before beams, and a task
graph cannot execute a step before its inputs exist.

**Kahn's algorithm** repeatedly outputs a vertex with no remaining incoming edges, that is, a vertex whose in-degree $\deg^-(v)$ (§1) among the vertices not yet output is 0. *Why it
works:* every DAG has such a vertex, since otherwise you could walk backwards along incoming
edges forever and would have to repeat a vertex, which is a cycle; deleting it leaves a DAG. If
the queue empties while vertices remain, each remaining vertex still has an incoming edge from
another remaining vertex, so a cycle exists, and the length check reports it.

**The DFS version** outputs vertices in *reverse finish order*. *Why:* for an edge $u \to v$, when
DFS explores it $v$ is either white (so $v$ finishes inside $u$'s interval, before $u$), black
(already finished), or gray, which would be a cycle. In a DAG, $v$ always finishes first, so
reversing the finish list puts $u$ before $v$. Both versions are $O(n + m)$.

```python
from collections import deque

def topo_kahn(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(u for u in adj if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == len(adj) else None    # None: a cycle remains

def topo_dfs(adj):
    state, order = {}, []
    def visit(u):
        state[u] = "active"
        for v in adj[u]:
            if state.get(v) == "active":
                raise ValueError("cycle")
            if v not in state:
                visit(v)
        state[u] = "done"
        order.append(u)
    for u in adj:
        if u not in state:
            visit(u)
    return order[::-1]                   # reverse finish order

deps = {"msgs": ["driver", "planner"], "driver": ["bringup"], "planner": ["bringup"], "bringup": []}
print(topo_kahn(deps), topo_dfs(deps))
```

Variants worth knowing: replace Kahn's queue by a min-heap to get the lexicographically smallest
order; relax edges (relaxation is defined in §4) in topological order to get **shortest or longest paths in a DAG** in
$O(n + m)$, even with negative weights, because when a vertex's outgoing edges are relaxed every edge into it has already been relaxed. The longest-path version is the critical-path method of
project scheduling, and Viterbi decoding of a hidden Markov model is the same relaxation over a
trellis ([[02-foundations/probability|3. Probability §7]]).

**Strongly connected components** (SCCs) are the maximal sets of vertices in which every vertex
can reach every other. Contracting each SCC to a single node always leaves a DAG, the
*condensation*. The definition has three parts:

- **Reachability.** Write $u \rightsquigarrow v$ when there is a directed path from $u$ to $v$ (a path of length 0 counts, so $u \rightsquigarrow u$).
- **Mutual reachability** is an equivalence relation: it is reflexive ($u \leftrightarrow u$), symmetric by its definition, and transitive, since paths can be concatenated.
$$u \leftrightarrow v \iff u \rightsquigarrow v \ \text{and}\ v \rightsquigarrow u$$
- **SCCs are its equivalence classes.** So they partition $V$, every vertex lies in exactly one SCC, and "maximal" means no vertex outside a class can be added while keeping mutual reachability.
- **Condensation.** Its vertices are the SCCs, with an edge $C \to C'$ whenever some $u \in C$, $v \in C'$, $C \ne C'$ have $(u, v) \in E$. It is always a DAG, because a cycle $C \to C' \to C$ would make every vertex of $C$ and $C'$ mutually reachable, merging them into one class.

*Non-example:* in the worked example below, $2 \rightsquigarrow 3$ but not $3 \rightsquigarrow 2$, so vertices 2 and 3 are in different SCCs even though the whole graph is connected when edge directions are ignored (it is one *weakly* connected component). Two classic algorithms compute them in $O(n + m)$. **Kosaraju's** runs DFS twice:
once to get finish times, then again on the reversed graph in decreasing finish time, where each
new DFS tree is exactly one SCC. **Tarjan's** does it in one DFS by tracking, for each vertex, the
earliest discovery time its subtree can reach among vertices still on the stack (its *low-link*). Written out, with $T_u$ the DFS subtree rooted at $u$, the low-link is the smaller of $u$'s own discovery time and the discovery time of any still-stacked vertex that one edge out of $T_u$ reaches:
$$\text{low}(u) = \min\big(d(u),\ \min\{\, d(x) : (y, x) \in E,\ y \in T_u,\ x \text{ on the stack} \,\}\big)$$
When $u$ finishes with $\text{low}(u) = d(u)$, nothing in its subtree can climb above $u$, so $u$ is the first-discovered vertex of its SCC and Tarjan pops the stack down to $u$ as one component. In a directed state lattice
or a roadmap with one-way edges, a state outside the goal's SCC can reach the goal but cannot
come back, which is how dead-end regions are found before a planner walks into them.

> [!example] Worked example · 계산 예제
> Edges $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 4$, $4 \to 3$. The cycle $0 \to 1 \to 2 \to 0$ makes $\{0, 1, 2\}$ one SCC and $3 \leftrightarrow 4$ makes $\{3, 4\}$ another; the condensation is the single edge $\{0,1,2\} \to \{3,4\}$. Kosaraju: a DFS from 0 finishes vertices in the order $4, 3, 2, 1, 0$. On the reversed graph, the DFS from 0 (latest finish) reaches $2$ and $1$ but not $3$, because $2 \to 3$ now points into $\{0,1,2\}$, so the first tree is $\{0, 1, 2\}$; the next unvisited vertex, 3, gives $\{3, 4\}$. If 4 is the goal, states 0, 1, 2 can reach it, but once a planner is in $\{3, 4\}$ it can never return to them.

### 4. Dijkstra's algorithm

**Two definitions every shortest-path algorithm shares.**

- **Shortest-path distance.** For a source $s$, $\delta(v)$ is the least weight of any path from $s$ to $v$ (path weight as in §1), with $\delta(v) = \infty$ when no path exists. It is well defined only when no cycle of negative total weight is reachable from $s$ (§5), since otherwise going round that cycle again always lowers the cost.
$$\delta(v) = \min\{\, w(P) : P \text{ a path from } s \text{ to } v \,\}$$
- **Relaxation** of an edge $(u, v)$ is the update that tests whether going through $u$ improves $v$'s label $d[v]$, the best path weight found so far, and if so lowers it and records $u$ as the parent:
$$\text{if } d[u] + w(u, v) < d[v]: \quad d[v] \leftarrow d[u] + w(u, v),\ \ \text{parent}[v] \leftarrow u$$
- **What it preserves.** Every label stays the weight of a real path, so $d[v] \ge \delta(v)$ at all times; and true distances satisfy the triangle inequality $\delta(v) \le \delta(u) + w(u, v)$, so once every edge passes the relaxation test with no change, the labels are exact. BFS, Dijkstra, Bellman–Ford and A* differ only in *which* edges they relax and in what order.

*Example.* In the graph of the code below, after $s$ is expanded $d[a] = 2$ and $d[b] = 5$. Relaxing $a \to b$ (weight 1) finds $2 + 1 = 3 < 5$, so $d[b]$ drops to 3 with parent $a$.

**Idea.** With non-negative edge weights, grow the set of vertices whose shortest distance is
final, always adding the unfinished vertex with the smallest tentative distance.

**Invariant and correctness sketch.** Write $\delta(u)$ for the true shortest distance and $d[u]$
for the label. Every label is the length of a real path, so $d[u] \ge \delta(u)$ always. Claim:
when $u$ is popped, $d[u] = \delta(u)$. Take a true shortest path to $u$ and let $y$ be the first
vertex on it that is not yet final; its predecessor $x$ is final, and relaxing $x \to y$ set
$d[y] \le \delta(y)$. Since $u$ was popped with the smallest label, and since the rest of the
path from $y$ to $u$ has non-negative length,

$$d[u] \le d[y] \le \delta(y) \le \delta(u) \le d[u]$$

so every inequality is an equality, which means that $d[u] = \delta(u)$ because the chain starts and ends at $d[u]$. The step $\delta(y) \le \delta(u)$ is the only place the
non-negative weights are used, and it is exactly the step a negative edge breaks.

**Implementation.** Python's `heapq` has no decrease-key, so push a new entry whenever a label
improves and skip stale entries when they are popped (*lazy deletion*).

```python
import heapq

def dijkstra(adj, s):
    """adj[u] = [(v, w), ...] with every w >= 0. Returns (dist, parent)."""
    INF = float("inf")
    dist, parent, done = {s: 0}, {s: None}, set()
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue                     # stale entry: u was finalized cheaper
        done.add(u)
        for v, w in adj.get(u, ()):
            if v not in done and d + w < dist.get(v, INF):
                dist[v], parent[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    return dist, parent

adj = {"s": [("a", 2), ("b", 5)], "a": [("b", 1), ("t", 6)], "b": [("t", 2)]}
print(dijkstra(adj, "s")[0]["t"])        # 5, via s-a-b-t
```

**Complexity.** Each successful relaxation pushes one entry, so the heap holds at most $m + 1$
entries and each push or pop costs $O(\log m) = O(\log n)$ (since $m \le n^2$). With $n$ pops and
at most $m$ pushes the total is $O((n + m)\log n)$. A Fibonacci heap gives $O(m + n \log n)$ in
theory; on a dense graph ($m \approx n^2$) a plain array scan, $O(n^2)$, beats both.

**Pitfalls.** Stop when the *target is popped*, not when it is first pushed; a cheaper path may
still be on the way. If two entries tie on distance, `heapq` compares the vertices next, which
raises `TypeError` for objects without an ordering; push `(d, counter, v)`. For a single target
on a map, run A* (§6) instead. **C++:** `std::priority_queue` is a *max*-heap, so declare
`std::priority_queue<std::pair<long long,int>, std::vector<std::pair<long long,int>>, std::greater<>>`,
and it has no decrease-key either, so the same lazy-deletion check applies.

> [!example] Worked example · 계산 예제
> **Why a negative edge breaks it.** Three vertices: $s \to a$ with weight 2, $s \to b$ with weight 1, $a \to b$ with weight $-2$.
> - Pop $s$ (0). Relax: $d[a] = 2$, $d[b] = 1$.
> - Pop $b$ (1). It is now *final* at 1.
> - Pop $a$ (2). The edge $a \to b$ offers $2 - 2 = 0 < 1$, but $b$ is already final and is not reopened.
>
> Dijkstra reports $d[b] = 1$; the truth is 0 via $s \to a \to b$. The failed step is $\delta(y) \le \delta(u)$: a path can get *cheaper* after leaving the frontier. Deleting the `v not in done` guard does not rescue it in general: $b$'s label would drop to 0, but anything already relaxed from $b$'s old label would keep the stale value, and if you also re-expand $b$ you have built a label-correcting method (§7), correct without negative cycles but exponential in the worst case.
>
> **And why adding a constant does not fix it.** Add 2 to every weight to make them non-negative: $s \to b$ becomes 3, while $s \to a \to b$ becomes $4 + 0 = 4$. The shortest path changes, because the shift penalizes paths by their number of edges.

### 5. Bellman–Ford and Floyd–Warshall

**Bellman–Ford idea.** Dynamic programming over the number of edges. Let $d_k(v)$ be the length of
the shortest path to $v$ that uses at most $k$ edges. A best path with at most $k$ edges either
uses at most $k-1$ edges or ends with some last edge $(u, v)$ preceded by a best path to $u$ with
at most $k-1$ edges, which gives the recurrence

$$d_k(v) = \min\Big(d_{k-1}(v),\ \min_{(u, v) \in E}\big(d_{k-1}(u) + w(u, v)\big)\Big)$$

If there is no negative cycle, some shortest path is simple, so it has at most $n-1$ edges, and
$d_{n-1}$ is final. Each round scans all $m$ edges, so the time is $O(nm)$ and the space $O(n)$.

**Negative cycle, defined.** A negative cycle is a directed cycle $v_0 \to \dots \to v_k = v_0$ whose total weight is below zero:
$$w(C) = \sum_{i=1}^{k} w(v_{i-1}, v_i) < 0$$
If one is reachable from $s$ and can reach $v$, then $\delta(v)$ does not exist (it is $-\infty$), because each extra lap lowers the path weight by the same amount. Negative *edges* alone are harmless to Bellman–Ford; only negative *cycles* are. *Example:* edges $0 \to 1$ (1), $1 \to 2$ ($-2$), $2 \to 1$ (1) contain the cycle $1 \to 2 \to 1$ of weight $-2 + 1 = -1$, and `bellman_ford(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)], 0)` returns `None`. *Non-example:* the graph in the code below has the negative edge $1 \to 2$ but no cycle, and the answer `[0, 2, 0]` is exact.

**Negative-cycle detection.** Run one more round. If nothing improves, every edge satisfies
$d(v) \le d(u) + w(u, v)$; adding that inequality around any cycle cancels the $d$ terms and shows
the cycle weight is $\ge 0$. So an improvement in round $n$ means a negative cycle reachable from
the source.

```python
def bellman_ford(n, edges, s):
    """Vertices 0..n-1, edges = [(u, v, w)]. None if a negative cycle is reachable."""
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):               # a simple path has at most n-1 edges
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                        # labels stable: stop early
    for u, v, w in edges:                # round n still improves => negative cycle
        if dist[u] + w < dist[v]:
            return None
    return dist

print(bellman_ford(3, [(0, 1, 2), (0, 2, 1), (1, 2, -2)], 0))   # [0, 2, 0]
```

**Pitfalls.** Updating `dist` in place is fine for plain shortest paths (it only converges
faster), but it is *wrong* for hop-limited questions such as "cheapest route with at most $K$
edges": within one round a label can chain through several edges. Copy `prev = dist[:]` at the
start of each round and relax from `prev`. In C++, guard `dist[u] != INF` before adding, or
`INF + w` overflows. The queue-based variant (re-scan only vertices whose label changed) is often
much faster in practice with the same $O(nm)$ worst case. The same recursion, run over stages of
a decision process, is value iteration in [[02-foundations/rl-basics|7. RL Basics]].

**Floyd–Warshall** answers all pairs at once. Number the vertices and let $D^{(k)}_{ij}$ be the
shortest $i \to j$ length using only vertices $0..k$ as intermediate stops. A shortest such path
either avoids $k$ or passes through it once, so

$$D^{(k)}_{ij} = \min\big(D^{(k-1)}_{ij},\ D^{(k-1)}_{ik} + D^{(k-1)}_{kj}\big)$$

Three nested loops give $O(n^3)$ time and $O(n^2)$ space. Updating one 2-D table in place is safe
because row $k$ and column $k$ do not change during round $k$. The loop over $k$ **must be the
outer loop**: the subproblem is indexed by $k$, and putting it inside computes something else.
A negative diagonal entry $D_{ii} < 0$ at the end marks a vertex on a negative cycle.

```python
def floyd_warshall(n, edges):
    INF = float("inf")
    d = [ [0 if i == j else INF for j in range(n)] for i in range(n) ]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)        # keep the cheapest parallel edge
    for k in range(n):                   # k MUST be outermost
        for i in range(n):
            dik = d[i][k]
            for j in range(n):
                if dik + d[k][j] < d[i][j]:
                    d[i][j] = dik + d[k][j]
    return d                             # d[i][i] < 0  <=>  i lies on a negative cycle

print(floyd_warshall(3, [(0, 1, 4), (1, 2, 1), (0, 2, 7)])[0][2])   # 5
```

**Which one to use.**

| Situation | Algorithm | Time |
|---|---|---|
| Unweighted, one source | BFS | $O(n + m)$ |
| Weights 0 or 1 | 0-1 BFS with a deque | $O(n + m)$ |
| DAG, any weights | relax in topological order | $O(n + m)$ |
| Non-negative weights, one source | Dijkstra (binary heap) | $O((n + m)\log n)$ |
| Non-negative weights, one target, good heuristic | A* | same worst case, far fewer expansions |
| Negative weights, or you must detect a negative cycle | Bellman–Ford | $O(nm)$ |
| All pairs, dense or $n$ up to a few hundred | Floyd–Warshall | $O(n^3)$ |
| All pairs, sparse, negative weights | Johnson: one Bellman–Ford to reweight, then $n$ Dijkstras | $O(nm \log n)$ |

### 6. A* search

**Idea.** Dijkstra expands in a circle around the start. A* orders the open list by
$f(n) = g(n) + h(n)$, cost so far plus an estimate of the cost remaining, so the circle is
stretched toward the goal. The planning page explains what $g$, $h$ and $f$ mean for a planner;
this section is about why the algorithm is correct and how to write it.

**The three quantities.** $g(n)$ is the cost of the cheapest path from the start $s$ to $n$ found so far (Dijkstra's label); $h(n)$ is the heuristic, any function of the vertex alone that estimates the remaining cost; and $h^*(n)$ is the true remaining cost, the shortest-path distance (§4) from $n$ to the goal, $\infty$ if the goal is unreachable. The open list is the priority queue of generated but unexpanded vertices, and the closed set holds the vertices already expanded.

**Admissible** means $h(n) \le h^*(n)$, never overestimating the true remaining cost.
**Consistent** means $h(n) \le c(n, n') + h(n')$ for every edge, with $h(\text{goal}) = 0$.
Consistency implies admissibility: apply the inequality along an optimal path from $n$ to the
goal and the $h$ terms telescope to $h(n) \le h^*(n)$. As formulas, with every condition named:

- **Admissible:** the estimate is non-negative and never exceeds the truth at any vertex, so it is a lower bound on the cost to go.
$$0 \le h(v) \le h^*(v) \quad \text{for all } v \in V$$
- **Consistent** (also called monotone): two conditions, the triangle inequality on every edge, and zero at the goal. The first says $h$ never drops by more than the edge just paid for, so $f = g + h$ never decreases along a path, since $f(v) = g(u) + c(u, v) + h(v) \ge g(u) + h(u) = f(u)$.
$$h(u) \le c(u, v) + h(v) \ \text{ for every edge } (u, v) \in E, \qquad h(\text{goal}) = 0$$

*Non-example (inadmissible).* Edges $s \to t$ (6), $s \to m$ (1), $m \to t$ (3), so the optimum is $s \to m \to t$ with cost 4 and $h^*(m) = 3$. Set $h(m) = 10$, $h(s) = h(t) = 0$. A* pushes $t$ with $f = 6$ and $m$ with $f = 1 + 10 = 11$, pops $t$ first and returns 6. With the admissible $h(m) = 3$, $m$ has $f = 4 < 6$, and A* returns 4.

**Why consistency means no re-expansion.** Define reduced edge costs

$$c'(u, v) = c(u, v) - h(u) + h(v) \ge 0$$

The inequality is the consistency condition, rearranged. Along any path from $s$ to $n$ the $h$
terms telescope, so the reduced cost of the path is its real cost $g$ minus $h(s)$ plus $h(n)$,
that is, $f(n) - h(s)$. Dijkstra on $c'$ therefore pops vertices in exactly A*'s order, and since
$c' \ge 0$, Dijkstra's invariant holds: *the first time a vertex is popped its $g$ is optimal*. A
closed set is then safe, and each vertex is expanded at most once. With a heuristic that is only
admissible, a vertex can be popped with a too-large $g$ and later reached more cheaply; A* then
stays optimal only if it reopens closed vertices.

> [!example] Worked example · 계산 예제
> **Admissible but inconsistent.** Edges $s \to a$ (1), $a \to m$ (1), $s \to m$ (3), $m \to t$ (3); the optimum is $s \to a \to m \to t$ with cost 5. Take $h(s) = 0$, $h(a) = 4$, $h(m) = 0$, $h(t) = 0$. Each is admissible ($h^*(a) = 4$, $h^*(m) = 3$), but $h(a) = 4 > c(a, m) + h(m) = 1$, so $h$ is inconsistent.
> - Pop $s$. Push $a$ with $f = 1 + 4 = 5$ and $m$ with $f = 3 + 0 = 3$.
> - Pop $m$ with $g = 3$ and close it. Push $t$ with $f = 6$.
> - Pop $a$ ($f = 5$). It offers $m$ a cost of 2, but $m$ is closed.
> - Without reopening, pop $t$ with cost 6, which is not optimal. With reopening, $m$ returns with $g = 2$, then $t$ with $g = 5$.
>
> **Consistent, same graph.** Take $h(s) = 2$, $h(a) = 2$, $h(m) = 1$, $h(t) = 0$; every edge passes $h(u) \le c(u,v) + h(v)$. The reduced costs are $c'(s,a) = 1$, $c'(a,m) = 0$, $c'(s,m) = 2$, $c'(m,t) = 2$, all $\ge 0$, whereas the inconsistent $h$ above gave $c'(a,m) = 1 - 4 + 0 = -3$. The optimal path's reduced cost is $1 + 0 + 2 = 3 = 5 - h(s)$, as the telescoping predicts. A* pops $s$ ($f = 2$), $a$ ($f = 3$), $m$ with $g = 2$ ($f = 3$), then $t$ with $g = 5$: each vertex once, and each first pop already optimal.

**Grid heuristics.** On a grid, the right heuristic is the exact cost of the move set with the
obstacles removed:

| Moves and costs | Heuristic, with $\Delta x, \Delta y$ the absolute offsets | Notes |
|---|---|---|
| 4-connected, cost 1 | Manhattan $\Delta x + \Delta y$ | consistent and exact on an empty grid |
| 8-connected, straight 1, diagonal $\sqrt 2$ | octile $\max(\Delta x, \Delta y) + (\sqrt 2 - 1)\min(\Delta x, \Delta y)$ | consistent; Manhattan would overestimate here |
| 8-connected, all moves cost 1 | Chebyshev $\max(\Delta x, \Delta y)$ | consistent |
| any of the above, or free-space motion | Euclidean $\sqrt{\Delta x^2 + \Delta y^2}$ | admissible and consistent, but weaker, so more expansions |

If cells carry traversal costs, multiply the heuristic by the *smallest* possible per-step cost,
and keep the units the same: a cost in seconds needs a heuristic of distance divided by the top
speed.

```python
import math

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def octile(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

print(manhattan((0, 0), (3, 4)), euclidean((0, 0), (3, 4)), round(octile((0, 0), (3, 4)), 3))
```

**Grid A\*, 4-connected, with obstacles.** This is the version a lab interview asks for.

```python
import heapq

def astar_grid(grid, start, goal):
    """grid[r][c] == 1 is an obstacle. 4-connected, unit cost. Returns (path, cost)."""
    rows, cols = len(grid), len(grid[0])
    if grid[start[0]][start[1]] or grid[goal[0]][goal[1]]:
        return None, float("inf")
    def h(cell):                         # Manhattan: consistent on a 4-grid
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
    g, parent, closed = {start: 0}, {start: None}, set()
    open_heap = [(h(start), h(start), start)]    # (f, h, cell): equal f prefers smaller h
    while open_heap:
        _, _, cell = heapq.heappop(open_heap)
        if cell in closed:
            continue                     # stale entry (lazy deletion)
        if cell == goal:                 # goal test on POP, not on push
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            return path[::-1], g[goal]
        closed.add(cell)
        r, c = cell
        for nxt in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nxt[0] < rows and 0 <= nxt[1] < cols and not grid[nxt[0]][nxt[1]] \
                    and nxt not in closed and g[cell] + 1 < g.get(nxt, float("inf")):
                g[nxt], parent[nxt] = g[cell] + 1, cell
                heapq.heappush(open_heap, (g[nxt] + h(nxt), h(nxt), nxt))
    return None, float("inf")

grid = [
    [0, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
]
print(astar_grid(grid, (2, 0), (0, 0)))  # cost 8: around the wall on the right
```

**Tie-breaking.** On an open grid with Manhattan distance, *every* cell in the rectangle between
start and goal has the same $f$, equal to the optimal cost, so an arbitrary tie order can expand
most of that rectangle. Breaking ties toward smaller $h$ (equivalently larger $g$) makes A* run
almost straight at the goal. It changes only the order among equal $f$, so optimality is
untouched. Scaling $h$ up by a tiny factor to break ties does something different: it can make $h$
slightly inadmissible.

**Weighted A\*.** Order by $g + \varepsilon h$ with $\varepsilon > 1$. The search becomes greedier
and expands far fewer vertices, and with a consistent $h$ (or an admissible one plus reopening)
the returned cost is at most $\varepsilon$ times the optimum $C^*$, so the priority and the guarantee are
$$f_\varepsilon(n) = g(n) + \varepsilon\, h(n), \qquad C_{\text{returned}} \le \varepsilon\, C^*$$
That bound is why the trade is acceptable: you choose how much
optimality to give up. Anytime planners (ARA\*) start with a large $\varepsilon$ to get a path
quickly and lower it while time remains.

**Pitfalls.** Testing for the goal when it is pushed; a heuristic in different units from the edge
costs; 8-connected moves that cut the corner between two diagonal obstacles (disallow a diagonal
step if either adjacent straight cell is blocked); and forgetting that on a grid the path is only
optimal *for the grid*, a staircase that still needs smoothing.

### 7. One algorithm: label-correcting search

Every algorithm above is the same loop with a different rule for which open vertex to take
next. LaValle's *Planning Algorithms* (ch. 2) presents BFS, DFS, Dijkstra, best-first and A* as
one forward-search template whose only real difference is how the open list $Q$ is sorted, and
then generalizes it to the **label-correcting** algorithm (the same family appears in Bertsekas's
*Dynamic Programming and Optimal Control*, Vol. I, ch. 2). In plain words the loop keeps a to-do
list of vertices, starting with just the start vertex: take any vertex off the list, check whether
going through it gives a neighbour a cheaper cost than that neighbour already has, and if so lower
the neighbour's cost and put the neighbour on the list (a goal neighbour instead just updates the best
answer so far); stop when the list is empty. With symbols:

1. Every vertex has a label $C(x)$, the best cost-to-come found so far; $C(s) = 0$, all others $\infty$. Keep $U$, the best cost to the goal found so far.
2. Remove some $x$ from $Q$. For each edge $x \to x'$: if $C(x) + c(x, x') + h(x') < \min(C(x'), U)$ (with $h$ admissible, or $h = 0$), lower $C(x')$ and record the parent. If $x'$ is the goal, update $U$; otherwise put $x'$ back in $Q$ if it is not there.
3. Stop when $Q$ is empty.

The key word is *correcting*: a vertex may re-enter $Q$ whenever its label improves. Because of
that, on a finite graph without negative cycles the loop ends with the optimal cost **for any
ordering of $Q$**. The ordering changes how much work is wasted, not the answer:

| Take from $Q$ | You get | Can a label change after its vertex is removed? |
|---|---|---|
| oldest (FIFO) | BFS; on weighted graphs, queue-based Bellman–Ford | yes, on weighted graphs |
| newest (LIFO) | DFS | yes, often many times |
| smallest $C(x)$ | Dijkstra | never, if weights are $\ge 0$ |
| smallest $h(x)$ | greedy best-first | yes |
| smallest $C(x) + h(x)$ | A* | never, if $h$ is consistent |

This is the cleanest way to see what Dijkstra and A* *add*: an ordering for which the first
removal is final, which is what lets them drop reopening and use a closed set. The textbook
forward search that never reopens is optimal only under those orderings, which is why greedy
best-first, run without reopening, is fast but not optimal.

```python
def label_correcting(adj, s, t, rule, h=lambda v: 0):
    """rule: 'fifo' | 'lifo' | 'dijkstra' | 'astar'. Returns (optimal cost, removals)."""
    INF = float("inf")
    C, Q, upper, removals = {s: 0}, [s], INF, 0
    while Q:
        if rule == "fifo":
            x = Q.pop(0)
        elif rule == "lifo":
            x = Q.pop()
        else:                            # linear scans for clarity; real code uses a heap
            key = (lambda v: C[v]) if rule == "dijkstra" else (lambda v: C[v] + h(v))
            x = min(Q, key=key)
            Q.remove(x)
        removals += 1
        for y, w in adj.get(x, ()):
            new = C[x] + w
            if new < C.get(y, INF) and new + h(y) < upper:
                C[y] = new
                if y == t:
                    upper = new
                elif y not in Q:
                    Q.append(y)
    return upper, removals

adj = {"s": [("b", 1), ("d", 5)], "a": [("d", 6)], "b": [("c", 2), ("d", 4), ("t", 6)],
       "c": [("d", 1), ("t", 3)], "d": [("a", 1), ("b", 2)]}
hh = {"s": 6, "a": 13, "b": 5, "c": 3, "d": 7, "t": 0}    # exact cost-to-go: consistent
for rule in ("fifo", "lifo", "dijkstra", "astar"):
    print(rule, label_correcting(adj, "s", "t", rule, hh.get if rule == "astar" else (lambda v: 0)))
# fifo (6, 7)   lifo (6, 7)   dijkstra (6, 5)   astar (6, 4)
```

All four rules return cost 6, via $s \to b \to c \to t$ ($1 + 2 + 3 = 6$); only the work differs.
FIFO and LIFO remove $d$ and $a$ twice each, because a cheaper route to them turns up after they
were expanded. Dijkstra removes each vertex once. A*, given the exact cost-to-go as $h$, never
expands $a$ at all, since its $C + h$ already exceeds the cost found.

### 8. Spanning trees, and the bridge to robot planning

**Minimum spanning tree, in one paragraph.** A shortest-path tree minimizes each vertex's distance
from a source; a minimum spanning tree minimizes the *total* edge weight connecting all vertices,
and the two trees are generally different. In a connected undirected weighted graph, a **spanning tree** is a subset of edges $T \subseteq E$ that (1) touches every vertex, (2) is connected and (3) has no cycle, which together force exactly $n - 1$ edges; a **minimum spanning tree** is one whose total weight is smallest, so it solves
$$\min_{T \text{ spanning tree}} \ \sum_{e \in T} w(e)$$
*Example:* the triangle $a - b$ (2), $b - c$ (2), $a - c$ (3) has MST $\{ab, bc\}$ of weight 4. The shortest-path tree from $a$ is $\{ab, ac\}$ instead, because $c$ is 3 away directly but 4 via $b$, and that tree weighs 5. *Non-example:* $\{ab, bc, ac\}$ connects everything but contains a cycle, so it is not a tree. Prim's algorithm is Dijkstra's loop with the key
"weight of the cheapest edge into the tree" instead of "distance from the source"; Kruskal's sorts
edges and adds each one that joins two different components, using union-find. Proofs and code
are in [[02-foundations/algorithms/greedy-mst|11.4 Greedy Algorithms & Spanning Trees]].

**Occupancy-grid planning.** The global planner in a 2-D navigation stack is §6 run on the
costmap the planning page describes. What changes in real code is mechanics, not theory:

- **Index cells, don't hash them.** Use a flat index $r \cdot W + c$ and store $g$, the parent and
  the closed flag in arrays of $H \cdot W$ entries. A $2000 \times 2000$ map has $4 \times 10^6$
  cells; a `float32` array for $g$ is 16 MB, while a Python dict keyed by tuples costs many times
  that and is slower to probe.
- **Edge cost is the cost of entering a cell**: step length times a factor derived from the cell's
  cost value, with lethal cells skipped as obstacles. Scale the heuristic by the cheapest possible
  step, or it stops being admissible.
- **Replanning.** When the costmap changes, many stacks simply rerun A* at a few hertz, because a
  2-D search is cheap. Incremental algorithms (LPA\*, D\* Lite) reuse the previous search and pay
  off when replanning is frequent and changes are local.
- **Grid artefacts.** A 4-connected path is a staircase and 8-connected paths snap to 45°. Either
  smooth the result or search *any-angle* (Theta\* lets a vertex's parent be any visible ancestor).

**Lattice planners.** A car cannot turn in place, so a grid over $(x, y)$ hides infeasible paths.
A **state lattice** discretizes $(x, y, \theta)$, sometimes with velocity, and its edges are
precomputed **motion primitives**: short feasible arcs from each heading. The graph is directed
and implicit, and the search is still A*. The usual heuristic is the maximum of two estimates, each of which
ignores one constraint: an obstacle-aware 2-D distance that ignores heading, computed once by a
backward Dijkstra from the goal over the grid, and an obstacle-free distance that respects the
turning radius. The maximum of lower bounds is still a lower bound (and the maximum of consistent
heuristics is consistent), and it is much tighter than either alone. Hybrid A\* keeps a continuous pose inside each discrete cell
for the same purpose. Nav2, for example, ships 2-D A\*, Hybrid-A\* and state-lattice planners.

**Where sampling takes over.** Search cost grows with the number of grid cells, which grows
exponentially with dimension. Three or four dimensions ($x, y, \theta$, perhaps speed) are fine;
a 6- or 7-joint arm is not, and [[04-robotics/modern-robotics/ch10-motion-planning|MR ch.10]]
works the numbers. There the planner stops enumerating states and starts sampling them (PRM, RRT).
Search survives in pieces: a sampling-based roadmap is still queried with Dijkstra or A*, and
search over a small set of arm motion primitives works when the task is structured. The
[[04-robotics/planning-decision-making|planning page]] places these families side by side.

### Self-check

1. Your BFS marks a vertex visited when it is dequeued instead of when it is enqueued. Are the distances still correct? What goes wrong?
2. Why does Kahn's algorithm output fewer than $n$ vertices exactly when the graph has a cycle?
3. Give a three-vertex graph on which Dijkstra returns a wrong distance, and name the step of the correctness proof that fails.
4. "Cheapest flight from A to B with at most $K$ stops." Why does in-place Bellman–Ford give wrong answers, and what is the fix?
5. Why must the $k$ loop be outermost in Floyd–Warshall?
6. On an 8-connected grid with diagonal cost $\sqrt 2$, is Manhattan distance admissible? What should you use?
7. A teammate multiplies the Manhattan heuristic by 10 "to make the planner faster". What did they buy, and what did they give up?
8. In label-correcting search, what changes when you switch the open list from FIFO to "smallest $C(x)$": the answer, or the work?

> [!tip]- Answers
> 1. Yes, provided a vertex's distance is fixed by the first copy dequeued and later copies are skipped: copies sit in the queue in non-decreasing distance order, so the first one carries the minimum. But a vertex can be enqueued once per incoming edge before it is marked, so the queue can hold $O(m)$ entries and the same vertex is processed repeatedly unless you skip duplicates on dequeue.
> 2. Every DAG has a vertex with in-degree 0, and removing it leaves a DAG, so on a DAG the queue never empties early. If vertices remain when it empties, each of them has an incoming edge from another remaining vertex; walking those edges backwards must repeat a vertex, which is a cycle.
> 3. $s \to a$ (2), $s \to b$ (1), $a \to b$ ($-2$). Dijkstra finalizes $b$ at 1 before expanding $a$, but $s \to a \to b$ costs 0. The failing step is $\delta(y) \le \delta(u)$, which assumes the rest of a path cannot have negative length.
> 4. In place, a label updated early in a round can be used later in the same round, so one round can extend a path by several edges and the "at most $k$ edges after round $k$" meaning is lost. Relax every edge from a copy `prev` of the previous round's labels, for exactly $K + 1$ rounds (stops are edges minus one).
> 5. The subproblem "intermediate vertices only from $0..k$" is indexed by $k$; round $k$ needs every $D^{(k-1)}$ entry to be complete. With $k$ inside, $D_{ij}$ is finalized before paths through later intermediates have been built.
> 6. No. From $(0,0)$ to $(1,1)$ Manhattan says 2, but one diagonal step costs $\sqrt 2 \approx 1.414$. Use octile distance.
> 7. That is weighted A* with $\varepsilon = 10$: far fewer expansions, but the path can cost up to 10 times the optimum, and in practice it hugs obstacles and takes greedy detours. Choose $\varepsilon$ deliberately (for example 1.5 to 3) or use an anytime planner that lowers it.
> 8. Only the work. For any ordering the loop ends with the optimal cost on a finite graph without negative cycles; with non-negative weights, "smallest $C$" is the ordering for which each vertex's first removal is final, so nothing is ever re-expanded.

### Sources

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — elementary graph algorithms, single-source and all-pairs shortest paths.
- T. Roughgarden, *Algorithms Illuminated, Part 2: Graph Algorithms and Data Structures*, Soundlikeyourself Publishing, 2018; *Part 3: Greedy Algorithms and Dynamic Programming*, 2019 (Bellman–Ford, Floyd–Warshall).
- S. M. LaValle, *Planning Algorithms*, Cambridge University Press, 2006 — ch. 2, forward search template and label-correcting algorithms. [Free online](http://lavalle.pl/planning/).
- D. P. Bertsekas, *Dynamic Programming and Optimal Control*, Vol. I, Athena Scientific — ch. 2, label-correcting shortest-path methods.
- E. W. Dijkstra, "A note on two problems in connexion with graphs," *Numerische Mathematik* 1, 269–271, 1959. doi:10.1007/BF01386390
- R. Bellman, "On a routing problem," *Quarterly of Applied Mathematics* 16(1), 87–90, 1958. doi:10.1090/qam/102435
- R. W. Floyd, "Algorithm 97: Shortest path," *Communications of the ACM* 5(6), 345, 1962. doi:10.1145/367766.368168
- S. Warshall, "A theorem on Boolean matrices," *Journal of the ACM* 9(1), 11–12, 1962. doi:10.1145/321105.321107
- A. B. Kahn, "Topological sorting of large networks," *Communications of the ACM* 5(11), 558–562, 1962. doi:10.1145/368996.369025
- R. E. Tarjan, "Depth-first search and linear graph algorithms," *SIAM Journal on Computing* 1(2), 146–160, 1972. doi:10.1137/0201010
- M. Sharir, "A strong-connectivity algorithm and its applications in data flow analysis," *Computers & Mathematics with Applications* 7(1), 67–72, 1981 (the two-pass algorithm usually credited to Kosaraju).
- P. E. Hart, N. J. Nilsson, B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Transactions on Systems Science and Cybernetics* 4(2), 100–107, 1968. doi:10.1109/TSSC.1968.300136
- I. Pohl, "Heuristic search viewed as path finding in a graph," *Artificial Intelligence* 1(3–4), 193–204, 1970 (weighted A*).
- M. Likhachev, G. Gordon, S. Thrun, "ARA\*: Anytime A\* with provable bounds on sub-optimality," *NeurIPS (NIPS)* 16, 2003.
- S. Koenig, M. Likhachev, "D\* Lite," *AAAI*, 2002.
- M. Pivtoraiko, R. A. Knepper, A. Kelly, "Differentially constrained mobile robot motion planning in state lattices," *Journal of Field Robotics* 26(3), 308–333, 2009.
- D. Dolgov, S. Thrun, M. Montemerlo, J. Diebel, "Path planning for autonomous vehicles in unknown semi-structured environments," *International Journal of Robotics Research* 29(5), 485–501, 2010 (Hybrid A\*).

## 한국어

*알고리즘 트랙의 그래프 페이지다. 이 페이지는 동작 원리와 코드를 맡고, 플래너가 무엇을 위한
것인지는 계획 페이지들이 맡는다. 코스트맵, 인플레이션, 전역/지역 분리는 [[04-robotics/planning-decision-making|4. 계획과 의사결정]]을, 격자가 왜 확장되지 않는지는 [[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]을 읽어라.*

그래프 문제는 두 종류의 인터뷰 모두에서 단일 주제로 가장 자주 나온다. 코딩 인터뷰는
그래프를 숨긴다: 단어 사다리, 수강 순서, 행렬 속 섬 개수. 로봇 연구실은 이름을 댄다: "이
점유 격자에서 A*를 짜 보라", "Dijkstra는 왜 음수 비용을 못 다루나", "일관된 휴리스틱은 무엇을
사 주나". 둘 다 같은 세 가지 습관에 점수를 준다. 표현을 먼저 고르고, 알고리즘을 옳게 만드는
불변식을 알고, 순진한 구현을 깨뜨리는 입력 하나를 아는 것이다.

> [!note] 처음이라면 · First pass
> §1, §2, §4를 읽고 §6의 격자 A*를 외워서 써 보라. §3과 §5는 인터뷰 변형 문제이고, §7은 이 모두를 하나의 알고리즘으로 보게 하는 관점이다.

### 1. 표현

그래프는 정점 집합 $V$와 간선 집합 $E$다. $n = \lvert V\rvert$, $m = \lvert E\rvert$로 쓴다. 표현이
탐색이 매번 반복하는 두 연산의 비용을 정한다: *$u$의 이웃 나열*과 *$(u, v)$가 간선인가?*

**용어, 하나씩 정의.** 그래프(**graph**)는 쌍 $G = (V, E)$, 즉 유한한 정점 집합과 간선 집합이며, 다음 요소를 가진다.

- **방향 또는 무방향.** 방향 그래프에서 간선은 *순서쌍* $(u, v)$이고 $u \to v$로 쓰며, $u$에서 $v$ 쪽으로만 따라갈 수 있다. 무방향 그래프에서 간선은 *순서 없는 쌍* $\{u, v\}$이고 양쪽으로 따라갈 수 있다.
- **가중치.** 가중 그래프는 각 간선에 비용을 주는 함수 $w : E \to \mathbb{R}$을 더한다. 가중치 없는 그래프는 $w \equiv 1$인 경우다.
- **차수.** 방향 그래프에서 $v$의 진출 차수와 진입 차수는 $v$에서 나가는 간선과 들어오는 간선의 수로, $\deg^+(v) = \lvert\{u : (v, u) \in E\}\rvert$, $\deg^-(v) = \lvert\{u : (u, v) \in E\}\rvert$다. 무방향 그래프에서 $\deg v$는 $v$에 닿는 간선의 수다.
- **경로, 단순 경로, 사이클.** 경로는 모든 $(v_{i-1}, v_i) \in E$인 정점 열 $v_0, v_1, \dots, v_k$다. 정점이 반복되지 않으면 단순 경로이고, $k \ge 1$이고 $v_k = v_0$이면 사이클이다(무방향 그래프의 사이클은 간선을 재사용하지 않고 $k \ge 3$이어야 한다). 경로의 가중치는 아래 식처럼 간선 가중치의 합이다.
$$w(P) = \sum_{i=1}^{k} w(v_{i-1}, v_i)$$
- **희소와 조밀.** 단순 방향 그래프의 간선은 많아야 $n(n-1)$개이므로 $m$은 $0$부터 약 $n^2$ 사이에 있다. $m = O(n)$이면 희소, $m = \Theta(n^2)$이면 조밀하다고 한다.

*예.* 아래 코드의 방향 간선 $a \to b$ (4), $a \to c$ (1), $c \to b$ (2), $b \to d$ (5)는 $n = m = 4$, $\deg^+(a) = 2$, $\deg^-(b) = 2$를 준다. 경로 $a, c, b, d$의 가중치는 $1 + 2 + 5 = 8$이고 $a, b, d$는 $4 + 5 = 9$다. *반례:* $d, b$는 경로가 아니다. 간선은 $b \to d$이고 방향 간선은 거꾸로 걸을 수 없기 때문이다.

| | 인접 리스트 | 인접 행렬 | 암묵적(격자, 래티스) |
|---|---|---|---|
| 메모리 | $O(n + m)$ | $O(n^2)$ | 점유 정보뿐, 간선은 저장하지 않음 |
| $u$의 이웃 | $O(\deg u)$ | $O(n)$ | $O(k)$, 격자에서 $k$ = 4 또는 8 |
| 간선 검사 $(u, v)$ | $O(\deg u)$, set이면 기대 $O(1)$ | $O(1)$ | $O(1)$ |
| BFS/DFS 한 번 | $O(n + m)$ | $O(n^2)$ | $m \le kn$이므로 $O(n)$ |
| 쓸 때 | 희소 그래프, 즉 거의 모든 실제 그래프 | 조밀 그래프, 정점 수천 개, Floyd–Warshall | 점유 격자, 상태 래티스, 상태를 생성하는 퍼즐 |

행렬은 속도보다 메모리에서 훨씬 먼저 진다. 정점 $10^4$개면 원소 $10^8$개가 필요하고,
`float64`로 800 MB다. 평균 차수 4인 도로망이나 로드맵은 같은 정점 수에 리스트 원소 약
$4 \times 10^4$개면 된다. 격자는 극단적인 경우다. $H \times W$ 지도 자체가 그래프이고, 이웃은
요청받을 때 셀 인덱스로 계산한다.

```python
from collections import defaultdict

edges = [("a", "b", 4), ("a", "c", 1), ("c", "b", 2), ("b", "d", 5)]

adj = defaultdict(list)                  # adjacency list: O(n + m) memory
for u, v, w in edges:
    adj[u].append((v, w))                # directed; also append (u, w) to adj[v] if undirected

names = sorted({x for u, v, _ in edges for x in (u, v)})
index = {name: i for i, name in enumerate(names)}
INF = float("inf")
mat = [ [INF] * len(names) for _ in names ]  # adjacency matrix: O(n^2) memory
for u, v, w in edges:
    mat[index[u]][index[v]] = w

def grid_neighbors(grid, r, c):          # implicit graph: edges computed, never stored
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0:
            yield nr, nc

tiny = [
    [0, 1],
    [0, 0],
]
print(adj["a"], mat[index["a"]][index["c"]], list(grid_neighbors(tiny, 0, 0)))
```

**함정.** `defaultdict`는 없는 정점을 *읽기만* 해도 키를 만든다. 그래서
`for u in adj: ... adj[v] ...`가 "dictionary changed size during iteration"을 낼 수 있고,
나가는 간선이 없는 정점은 따로 넣지 않으면 키로 나타나지 않는다. 모든 정점이 필요한
알고리즘(위상 정렬, SCC)에서는 정점 집합을 명시적으로 만들어라. 무방향 그래프는 간선을
양쪽 리스트에 넣고, 그러면 $m$이 두 번 세어진다는 점을 기억하라.

### 2. BFS와 DFS

**너비 우선 탐색**(BFS)은 고리 모양으로 퍼진다. 간선 하나 거리의 모든 정점, 그다음 두 개
거리의 모든 정점. 그래서 BFS가 어떤 정점에 처음 도달했을 때는 간선 수가 가장 적은 경로로
도달한 것이다. 정확히 말하면, 출발점 $s$에서의 BFS는 모든 정점에 대해 가중치 없는 거리(**unweighted distance**), 즉 홉 수를 계산하는 그래프 순회다. 공집합의 최솟값은 $\infty$로 두므로 도달할 수 없는 정점은 $\infty$를 받는다.

$$\text{dist}(v) = \min\{\,k : \text{there is a path } s = v_0, v_1, \dots, v_k = v\,\}$$

*왜 그런가.* 큐에 든 정점들의 거리는 앞에서 뒤로 감소하지 않고, 차이는 많아야 1이다. 정점
$v$는 가장 먼저 꺼내진 이웃 $u$에게 발견되고, $u$는 $v$의 다른 어느 이웃보다 늦게 꺼내지지
않으므로 `dist[v] = dist[u] + 1`이 최솟값이다. *비용:* 각 정점은 한 번 큐에 들어가고 각 인접
리스트는 한 번 훑으므로 $O(n + m)$. 발견 시점에 기록한 부모 맵이 거리를 경로로 바꾼다. 목표에서
부모를 따라 거슬러 올라간 뒤 뒤집으면 된다.

```python
from collections import deque

def bfs_path(adj, s, t):
    parent = {s: None}                   # doubles as the visited set
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return path[::-1]
        for v in adj.get(u, ()):
            if v not in parent:          # mark on ENQUEUE, not on dequeue
                parent[v] = u
                q.append(v)
    return None

adj = {"s": ["a", "b"], "a": ["c"], "b": ["c"], "c": ["t"]}
print(bfs_path(adj, "s", "t"))           # ['s', 'a', 'c', 't']
```

**BFS 함정.** 정점을 *꺼낼 때* 방문 표시하면 (나중 사본을 건너뛴다면) 거리는 맞지만, 같은 정점이 들어오는 간선 수만큼
큐에 쌓인다. `list.pop(0)`은 $O(n)$이라 BFS가 $O(n^2)$이 된다. `collections.deque`를 써라.
가중치가 있으면 BFS는 틀린다. 싼 예외가 하나 있다. 가중치가 모두 0 또는 1이면 0 간선은 덱의
*앞*에, 1 간선은 뒤에 넣는다(0-1 BFS). 여전히 $O(n + m)$이다. 여러 출발점을 거리 0으로 큐에
미리 넣으면 다중 출발 BFS(**multi-source BFS**)가 되고, 점유 격자에서는 이것이 *brushfire* 거리 변환이다. 한 번의
훑기로 모든 빈 셀에서 가장 가까운 장애물까지의 거리를 얻는다. 이것은 출발점 집합 $S$의 *가장 가까운* 원소까지의 거리를 계산한다. 모든 $s \in S$에 비용 없는 간선으로 이어진 가상의 초출발점에서 BFS를 한 번 돌리면 정확히 같은 정점을 같은 순서로 큐에 넣기 때문에 옳다.

$$\text{dist}_S(v) = \min_{s \in S} \text{dist}_s(v)$$

*예.* 양 끝에 장애물이 있는 한 줄 지도 $[1, 0, 0, 0, 1]$은 거리 $[0, 1, 2, 1, 0]$을 준다. 가운데 셀은 어느 벽에서나 두 걸음이다.

**깊이 우선 탐색**(DFS)은 한 가지를 끝까지 따라가고 나서 되돌아온다. 가치는 방문 순서가 아니라
남기는 *타임스탬프*에 있다. 정점은 처음 들어갈 때 **발견**(discovered)되고, 나가는 모든 간선을
탐색하고 나면 **종료**(finished)된다. 두 정점의 발견–종료 구간은 괄호처럼 포개지거나 서로소다. 발견과 종료 때마다 한 칸씩 가는 시계 하나로 두 시각을 $d(u)$, $f(u)$라 쓰자. 괄호 정리(**parenthesis theorem**)는 서로 다른 두 정점 $u \ne v$에 대해 다음 중 정확히 하나가 성립한다고 말한다. $u$가 열려 있는 동안 발견된 정점은 $u$보다 먼저 종료해야 하기 때문이다.

$$[d(u), f(u)] \cap [d(v), f(v)] = \varnothing \quad\text{or}\quad [d(v), f(v)] \subset [d(u), f(u)] \quad\text{or}\quad [d(u), f(u)] \subset [d(v), f(v)]$$

이 시각들은 DFS가 방향 간선 $u \to v$를 살펴보는 순간 $v$의 색으로 모든 간선을 분류한다.

- **트리 간선:** $v$가 흰색이라 DFS가 이 간선으로 $v$에 들어간다.
- **역방향 간선:** $v$가 회색, 즉 아직 스택에 있는 $u$의 조상이다.
- **순방향 간선:** $v$가 검은색이고 $d(u) < d(v)$다. 다른 길로 먼저 도달해 종료된 자손이다.
- **교차 간선:** $v$가 검은색이고 $d(v) < d(u)$다. 이미 종료된 서브트리에 있다.

*예.* 간선 $a \to b$, $b \to c$, $a \to c$, $d \to c$를 이 순서로 방문한다. DFS는 $a$: 1/6, $b$: 2/5, $c$: 3/4, $d$: 7/8(발견/종료)을 준다. 그래서 $a \to b$와 $b \to c$는 트리 간선, $a \to c$는 순방향 간선($c$ 검은색, $1 < 3$), $d \to c$는 교차 간선($c$ 검은색, $3 < 7$)이다. $[3, 4] \subset [2, 5] \subset [1, 6]$은 포개지고 $[7, 8]$은 모두와 서로소다. 역방향 간선이 없으므로 사이클도 없다.

사이클을 잡는 것이 이 구조다. 재귀 스택 위에 있는 동안은 회색, 종료되면 검은색으로 칠한다.
방향 그래프에서 *회색* 이웃을 만나면 아직 탐색 중인 조상으로 돌아가는 간선이므로 사이클이다.
방향 그래프에 사이클이 있는 것과 DFS가 이런 역방향 간선을 찾는 것은 정확히 동치다. *반례:* 순방향 간선과 교차 간선은 사이클의 신호가 아니다. 그래서 (검은색과 회색을 뭉뚱그린) "방문함" 표시만 쓰면 위 그래프에서 없는 사이클을 보고한다. 무방향
그래프는 모든 간선이 양방향으로 저장되므로 방금 온 정점으로의 간선은 무시하고, 그 밖의 방문한
이웃은 사이클을 닫는다(평행 간선이 있으면 부모 정점이 아니라 간선 id를 비교하라). DFS도
$O(n + m)$이다.

```python
def dfs_recursive(adj):
    """adj must list every vertex as a key. Returns (finish order, has_cycle)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in adj}
    finish, has_cycle = [], False

    def visit(u):
        nonlocal has_cycle
        color[u] = GRAY                  # discovered, still on the stack
        for v in adj[u]:
            if color[v] == GRAY:
                has_cycle = True         # back edge: directed cycle
            elif color[v] == WHITE:
                visit(v)
        color[u] = BLACK                 # finished
        finish.append(u)

    for u in adj:
        if color[u] == WHITE:
            visit(u)
    return finish, has_cycle

print(dfs_recursive({"a": ["b"], "b": ["c"], "c": []}))   # (['c', 'b', 'a'], False)
```

Python의 기본 재귀 한도는 1000 프레임이라, $100 \times 100$ 격자의 긴 복도를 따라가는 DFS는
`RecursionError`로 죽는다. 한도를 올리는 것은 어느 정도까지만 통한다. 깊은 재귀는 느리고, 일부 Python 버전에서는 여전히 프로세스를 죽일 수 있다. 견고한 버전은
*(정점, 그 이웃에 대한 반복자)* 의 명시적 스택을 두며, 재귀 버전의 발견·종료 순서를 그대로
재현한다.

```python
def dfs_iterative(adj):
    """Same finish order and cycle test as dfs_recursive, with no recursion."""
    color, finish, has_cycle = {u: 0 for u in adj}, [], False
    for root in adj:
        if color[root]:
            continue
        color[root] = 1
        stack = [(root, iter(adj[root]))]
        while stack:
            u, it = stack[-1]
            v = next(it, None)
            if v is None:                # every neighbour done: u finishes
                color[u] = 2
                finish.append(u)
                stack.pop()
            elif color[v] == 1:
                has_cycle = True
            elif color[v] == 0:
                color[v] = 1
                stack.append((v, iter(adj[v])))
    return finish, has_cycle

print(dfs_iterative({"a": ["b"], "b": ["c"], "c": ["a"]}))  # (['c', 'b', 'a'], True)
```

흔한 지름길인 "스택으로 하는 BFS"(이웃을 모두 넣고 꺼낼 때 표시)는 정점을 깊이 우선으로
방문하긴 하지만 언제 정점이 종료되는지 모르므로, 위상 순서를 줄 수도 회색 검사를 쓸 수도 없다.

### 3. 위상 정렬과 강연결 요소

방향 그래프의 위상 순서(**topological order**)는 모든 간선이 앞에서 뒤로 향하도록 정점을 나열한 것이다. 그래프가
DAG(방향 비순환 그래프)일 때에만 존재한다. 두 용어를 정확히 쓰면 이렇다.

- **DAG**(directed acyclic graph)는 방향 사이클이 없는 방향 그래프다. 즉 $k \ge 1$이고 $v_k = v_0$인 경로 $v_0 \to v_1 \to \dots \to v_k$가 없다(§1).
- 위상 순서(**topological order**)는 정점에 번호를 매기는 전단사 $\pi : V \to \{1, \dots, n\}$로서, 모든 간선이 작은 번호에서 큰 번호로 간다. 곧 모든 간선 $(u, v)$에서 $u$가 $v$보다 앞선다.
$$\pi(u) < \pi(v) \quad \text{for every edge } (u, v) \in E$$
- **왜 "DAG일 때에만"인가.** 사이클 $v_0 \to \dots \to v_k = v_0$가 있다면 조건이 $\pi(v_0) < \pi(v_1) < \dots < \pi(v_k) = \pi(v_0)$를 요구하므로 불가능하다. 거꾸로, 아래의 Kahn 알고리즘은 모든 DAG에 대해 순서를 만든다.

*예.* 아래 코드의 빌드 그래프(`msgs` → `driver`, `msgs` → `planner`, `driver` → `bringup`, `planner` → `bringup`)에서는 `msgs, driver, planner, bringup`과 `msgs, planner, driver, bringup`이 모두 위상 순서이므로, 순서는 일반적으로 유일하지 않다. *반례:* `msgs, bringup, driver, planner`는 간선 `driver` → `bringup`이 뒤로 향하므로 위상 순서가 아니다. 인터뷰는 이것을 수강 선수과목이나 빌드 순서로
포장하고, 로보틱스도 같은 일에 쓴다. `colcon`은 ROS 2 패키지를 의존성 순서로 빌드하고, 조립
순서는 보보다 기둥을 먼저 세우며, 작업 그래프는 입력이 생기기 전의 단계를 실행할 수 없다.

Kahn 알고리즘(**Kahn's algorithm**)은 남은 진입 간선이 없는 정점, 즉 아직 출력하지 않은 정점들 사이에서 진입 차수 $\deg^-(v)$(§1)가 0인 정점을 반복해서 출력한다. *왜 되는가:* 모든 DAG에는
그런 정점이 있다. 없다면 진입 간선을 따라 끝없이 거슬러 갈 수 있고, 결국 정점이 반복되니
사이클이다. 그 정점을 지워도 DAG가 남는다. 정점이 남았는데 큐가 비면, 남은 정점마다 다른 남은
정점에서 오는 진입 간선이 있으므로 사이클이 존재하고, 길이 검사가 이를 알려 준다.

DFS 버전(**DFS version**)은 *종료 순서의 역순*으로 출력한다. *왜:* 간선 $u \to v$를 DFS가 탐색할 때 $v$는
흰색(그러면 $v$는 $u$의 구간 안에서, $u$보다 먼저 종료), 검은색(이미 종료), 또는 회색(사이클)
중 하나다. DAG에서는 항상 $v$가 먼저 종료되므로, 종료 목록을 뒤집으면 $u$가 $v$ 앞에 온다. 두
버전 모두 $O(n + m)$이다.

```python
from collections import deque

def topo_kahn(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(u for u in adj if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == len(adj) else None    # None: a cycle remains

def topo_dfs(adj):
    state, order = {}, []
    def visit(u):
        state[u] = "active"
        for v in adj[u]:
            if state.get(v) == "active":
                raise ValueError("cycle")
            if v not in state:
                visit(v)
        state[u] = "done"
        order.append(u)
    for u in adj:
        if u not in state:
            visit(u)
    return order[::-1]                   # reverse finish order

deps = {"msgs": ["driver", "planner"], "driver": ["bringup"], "planner": ["bringup"], "bringup": []}
print(topo_kahn(deps), topo_dfs(deps))
```

알아 둘 변형: Kahn의 큐를 최소 힙으로 바꾸면 사전순으로 가장 앞선 순서가 나온다. 위상 순서로
간선을 완화하면(완화의 정의는 §4) DAG의 최단·최장 경로(**DAG shortest/longest path**)를 음수 가중치가 있어도 $O(n + m)$에 구한다. 어떤 정점의 나가는 간선을 완화할 때는 그 정점으로 들어오는 간선이 이미 모두 완화되었기 때문이다. 최장 경로
버전이 공정 관리의 주공정법(critical path method)이고, 은닉 마르코프 모델의 Viterbi 복호도
트렐리스 위에서의 같은 완화다([[02-foundations/probability|3. 확률 §7]]).

**강연결 요소**(SCC)는 모든 정점이 서로에게 도달할 수 있는 극대 정점 집합이다. 각 SCC를 한
노드로 축약하면 항상 DAG, 즉 *응축 그래프*가 남는다. 정의는 세 부분으로 되어 있다.

- **도달 가능성.** $u$에서 $v$로 가는 방향 경로가 있으면 $u \rightsquigarrow v$로 쓴다(길이 0인 경로도 치므로 $u \rightsquigarrow u$).
- **상호 도달 가능성**은 동치 관계다. 반사적이고($u \leftrightarrow u$), 정의상 대칭이며, 경로를 이어 붙일 수 있으므로 추이적이다.
$$u \leftrightarrow v \iff u \rightsquigarrow v \ \text{and}\ v \rightsquigarrow u$$
- **SCC는 그 동치류다.** 그래서 SCC들은 $V$를 분할하고, 모든 정점은 정확히 하나의 SCC에 속한다. "극대"란 상호 도달 가능성을 유지하면서 동치류 밖의 정점을 더할 수 없다는 뜻이다.
- **응축 그래프.** 정점은 SCC들이고, 어떤 $u \in C$, $v \in C'$, $C \ne C'$에 대해 $(u, v) \in E$이면 간선 $C \to C'$을 둔다. 사이클 $C \to C' \to C$가 있다면 $C$와 $C'$의 모든 정점이 서로 도달 가능해져 한 동치류로 합쳐지므로, 응축 그래프는 항상 DAG다.

*반례:* 아래 계산 예제에서 $2 \rightsquigarrow 3$이지만 $3 \rightsquigarrow 2$는 아니므로, 간선 방향을 무시하면 그래프 전체가 연결되어 있는데도(약연결 요소 하나) 정점 2와 3은 서로 다른 SCC에 있다. 두 고전 알고리즘이 $O(n + m)$에 구한다.
Kosaraju(**Kosaraju's**)는 DFS를 두 번 돈다. 한 번은 종료 시각을 얻고, 다시 역방향 그래프에서 종료 시각이
큰 순서로 돌면 새 DFS 트리 하나가 정확히 SCC 하나다. Tarjan(**Tarjan's**)은 각 정점에서 그 서브트리가
아직 스택에 있는 정점 중에서 닿을 수 있는 가장 이른 발견 시각(*low-link*)을 추적해 DFS 한 번으로 해낸다. 풀어 쓰면, $u$를 뿌리로 하는 DFS 서브트리를 $T_u$라 할 때 low-link는 $u$ 자신의 발견 시각과, $T_u$에서 간선 하나로 닿는 아직 스택에 있는 정점의 발견 시각 중 작은 값이다.
$$\text{low}(u) = \min\big(d(u),\ \min\{\, d(x) : (y, x) \in E,\ y \in T_u,\ x \text{ on the stack} \,\}\big)$$
$u$가 $\text{low}(u) = d(u)$로 종료하면 서브트리의 어떤 정점도 $u$ 위로 올라갈 수 없으므로 $u$는 자기 SCC에서 가장 먼저 발견된 정점이고, Tarjan은 스택을 $u$까지 꺼내 요소 하나로 만든다. 방향이 있는 상태
래티스나 일방통행 간선이 있는 로드맵에서, 목표의 SCC 밖에 있는 상태는 목표에 갈 수는 있어도
돌아올 수 없다. 플래너가 막다른 영역에 들어가기 전에 그런 영역을 찾는 방법이 이것이다.

> [!example] 계산 예제 · Worked example
> 간선 $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 4$, $4 \to 3$. 사이클 $0 \to 1 \to 2 \to 0$ 때문에 $\{0, 1, 2\}$가 SCC 하나, $3 \leftrightarrow 4$ 때문에 $\{3, 4\}$가 또 하나이고, 응축 그래프는 간선 하나 $\{0,1,2\} \to \{3,4\}$다. Kosaraju: 0에서 시작한 DFS는 정점을 $4, 3, 2, 1, 0$ 순서로 종료한다. 역방향 그래프에서 (가장 늦게 종료한) 0부터 DFS를 돌면 $2$와 $1$에는 닿지만 $3$에는 닿지 않는다. $2 \to 3$이 이제 $\{0,1,2\}$ 쪽을 가리키기 때문이다. 그래서 첫 트리는 $\{0, 1, 2\}$이고, 방문하지 않은 다음 정점 3이 $\{3, 4\}$를 준다. 4가 목표라면 상태 0, 1, 2는 목표에 갈 수 있지만, 플래너가 일단 $\{3, 4\}$에 들어가면 다시는 돌아올 수 없다.

### 4. Dijkstra 알고리즘

**모든 최단 경로 알고리즘이 공유하는 두 정의.**

- **최단 경로 거리.** 출발점 $s$에 대해 $\delta(v)$는 $s$에서 $v$로 가는 경로의 가중치(§1) 중 가장 작은 값이고, 경로가 없으면 $\delta(v) = \infty$다. 출발점에서 도달 가능한 음수 총합 사이클이 없을 때에만 잘 정의된다(§5). 그런 사이클이 있으면 한 바퀴 더 돌 때마다 비용이 내려가기 때문이다.
$$\delta(v) = \min\{\, w(P) : P \text{ a path from } s \text{ to } v \,\}$$
- 간선 $(u, v)$의 완화(**relaxation**)는 $u$를 거치면 $v$의 레이블 $d[v]$(지금까지 찾은 최선의 경로 가중치)가 좋아지는지 검사하고, 그렇다면 레이블을 낮추고 $u$를 부모로 기록하는 갱신이다.
$$\text{if } d[u] + w(u, v) < d[v]: \quad d[v] \leftarrow d[u] + w(u, v),\ \ \text{parent}[v] \leftarrow u$$
- **무엇을 보존하는가.** 모든 레이블은 실제 경로의 가중치로 남으므로 늘 $d[v] \ge \delta(v)$다. 그리고 참 거리는 삼각 부등식 $\delta(v) \le \delta(u) + w(u, v)$를 만족하므로, 모든 간선이 완화 검사에서 아무것도 바꾸지 않으면 레이블이 정확하다. BFS, Dijkstra, Bellman–Ford, A*는 *어떤* 간선을 어떤 순서로 완화하느냐만 다르다.

*예.* 아래 코드의 그래프에서 $s$를 확장하면 $d[a] = 2$, $d[b] = 5$다. $a \to b$(가중치 1)를 완화하면 $2 + 1 = 3 < 5$이므로 $d[b]$가 3으로 내려가고 부모는 $a$가 된다.

**아이디어.** 간선 가중치가 음수가 아니면, 최단 거리가 확정된 정점 집합을 키워 나가되 항상
미확정 정점 중 임시 거리가 가장 작은 것을 더한다.

**불변식과 정당성 스케치.** 참 최단 거리를 $\delta(u)$, 레이블을 $d[u]$로 쓴다. 모든 레이블은
실제 경로의 길이이므로 늘 $d[u] \ge \delta(u)$다. 주장: $u$가 꺼내질 때 $d[u] = \delta(u)$다. $u$로
가는 참 최단 경로를 잡고, 그 위에서 아직 확정되지 않은 첫 정점을 $y$라 하자. 그 직전 정점 $x$는
확정되어 있고, $x \to y$를 완화할 때 $d[y] \le \delta(y)$가 되었다. $u$가 가장 작은 레이블로
꺼내졌고, $y$에서 $u$까지 남은 경로의 길이가 음수가 아니므로

$$d[u] \le d[y] \le \delta(y) \le \delta(u) \le d[u]$$

사슬이 $d[u]$에서 시작해 $d[u]$로 끝나므로 모든 부등호가 등호이고, 곧 $d[u] = \delta(u)$다. 음이 아닌 가중치를 쓰는 곳은 $\delta(y) \le \delta(u)$ 한 단계뿐이고, 음수
간선이 깨뜨리는 것이 바로 그 단계다.

**구현.** Python의 `heapq`에는 decrease-key가 없으므로, 레이블이 좋아질 때마다 새 항목을 넣고
꺼낼 때 낡은 항목을 건너뛴다(*지연 삭제*).

```python
import heapq

def dijkstra(adj, s):
    """adj[u] = [(v, w), ...] with every w >= 0. Returns (dist, parent)."""
    INF = float("inf")
    dist, parent, done = {s: 0}, {s: None}, set()
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue                     # stale entry: u was finalized cheaper
        done.add(u)
        for v, w in adj.get(u, ()):
            if v not in done and d + w < dist.get(v, INF):
                dist[v], parent[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    return dist, parent

adj = {"s": [("a", 2), ("b", 5)], "a": [("b", 1), ("t", 6)], "b": [("t", 2)]}
print(dijkstra(adj, "s")[0]["t"])        # 5, via s-a-b-t
```

**복잡도.** 성공한 완화마다 항목 하나를 넣으므로 힙에는 많아야 $m + 1$개가 있고, 넣기·꺼내기는
$O(\log m) = O(\log n)$이다($m \le n^2$이므로). 꺼내기 $n$번과 넣기 최대 $m$번이면 합계
$O((n + m)\log n)$. 피보나치 힙은 이론상 $O(m + n \log n)$이지만, 조밀 그래프($m \approx n^2$)에서는
단순 배열 훑기 $O(n^2)$가 둘 다 이긴다.

**함정.** 목표가 처음 *넣어질 때*가 아니라 *꺼내질 때* 멈춰라. 더 싼 경로가 아직 오는 중일 수
있다. 거리가 같은 항목이 둘이면 `heapq`는 다음으로 정점을 비교하는데, 순서가 없는 객체면
`TypeError`가 난다. `(d, counter, v)`를 넣어라. 지도 위의 목표 하나라면 A*(§6)를 대신 써라.
**C++:** `std::priority_queue`는 *최대* 힙이므로
`std::priority_queue<std::pair<long long,int>, std::vector<std::pair<long long,int>>, std::greater<>>`로
선언하고, 역시 decrease-key가 없으니 같은 지연 삭제 검사를 쓴다.

> [!example] 계산 예제 · Worked example
> **음수 간선이 왜 깨뜨리는가.** 정점 셋: $s \to a$ 가중치 2, $s \to b$ 가중치 1, $a \to b$ 가중치 $-2$.
> - $s$(0)를 꺼낸다. 완화: $d[a] = 2$, $d[b] = 1$.
> - $b$(1)를 꺼낸다. 이제 1로 *확정*이다.
> - $a$(2)를 꺼낸다. 간선 $a \to b$가 $2 - 2 = 0 < 1$을 제시하지만, $b$는 이미 확정이라 다시 열리지 않는다.
>
> Dijkstra는 $d[b] = 1$을 보고하지만 참값은 $s \to a \to b$로 0이다. 실패한 단계는 $\delta(y) \le \delta(u)$다. 경로가 경계를 떠난 뒤에 *더 싸질* 수 있다. `v not in done` 검사를 지워도 일반적으로 구제되지 않는다. $b$의 레이블은 0으로 내려가지만 $b$의 옛 레이블로 이미 완화한 정점들은 낡은 값을 유지하고, $b$를 다시 확장까지 하면 레이블 수정 방법(§7)을 만든 것이다. 음수 사이클이 없으면 옳지만 최악의 경우 지수 시간이다.
>
> **상수를 더해도 안 고쳐지는 이유.** 모든 가중치에 2를 더해 음수를 없애 보자. $s \to b$는 3이 되고 $s \to a \to b$는 $4 + 0 = 4$가 된다. 상수를 더하면 간선 수가 많은 경로일수록 벌점이 커지므로 최단 경로가 바뀐다.

### 5. Bellman–Ford와 Floyd–Warshall

**Bellman–Ford 아이디어.** 간선 수에 대한 동적 계획법이다. $d_k(v)$를 간선을 많아야 $k$개 쓰는
$v$까지의 최단 경로 길이라 하자. 간선이 $k$개 이하인 최선의 경로는 $k-1$개 이하를 쓰거나, 간선
$k-1$개 이하로 $u$까지 가는 최선의 경로 뒤에 마지막 간선 $(u, v)$를 붙인 것이므로 점화식은

$$d_k(v) = \min\Big(d_{k-1}(v),\ \min_{(u, v) \in E}\big(d_{k-1}(u) + w(u, v)\big)\Big)$$

음수 사이클이 없으면 단순 경로인 최단 경로가 있고, 그 간선은 많아야 $n-1$개이므로 $d_{n-1}$이
최종값이다. 한 라운드가 간선 $m$개를 모두 훑으니 시간 $O(nm)$, 공간 $O(n)$이다.

**음수 사이클의 정의.** 음수 사이클은 총 가중치가 0보다 작은 방향 사이클 $v_0 \to \dots \to v_k = v_0$이다.
$$w(C) = \sum_{i=1}^{k} w(v_{i-1}, v_i) < 0$$
그런 사이클이 $s$에서 도달 가능하고 $v$에 닿을 수 있으면 $\delta(v)$는 존재하지 않는다($-\infty$). 한 바퀴 더 돌 때마다 경로 가중치가 같은 양만큼 내려가기 때문이다. 음수 *간선*만으로는 Bellman–Ford에 해가 없고, 문제는 음수 *사이클*뿐이다. *예:* 간선 $0 \to 1$ (1), $1 \to 2$ ($-2$), $2 \to 1$ (1)에는 가중치 $-2 + 1 = -1$인 사이클 $1 \to 2 \to 1$이 있고, `bellman_ford(3, [(0, 1, 1), (1, 2, -2), (2, 1, 1)], 0)`은 `None`을 반환한다. *반례:* 아래 코드의 그래프에는 음수 간선 $1 \to 2$가 있지만 사이클이 없고, 답 `[0, 2, 0]`은 정확하다.

**음수 사이클 검출.** 한 라운드를 더 돈다. 아무것도 좋아지지 않으면 모든 간선이
$d(v) \le d(u) + w(u, v)$를 만족한다. 이 부등식을 어떤 사이클을 따라 더하면 $d$ 항이 상쇄되어
사이클 가중치가 $\ge 0$임이 나온다. 그러니 $n$번째 라운드에서 개선이 있다면 출발점에서 도달 가능한
음수 사이클이 있다.

```python
def bellman_ford(n, edges, s):
    """Vertices 0..n-1, edges = [(u, v, w)]. None if a negative cycle is reachable."""
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):               # a simple path has at most n-1 edges
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                        # labels stable: stop early
    for u, v, w in edges:                # round n still improves => negative cycle
        if dist[u] + w < dist[v]:
            return None
    return dist

print(bellman_ford(3, [(0, 1, 2), (0, 2, 1), (1, 2, -2)], 0))   # [0, 2, 0]
```

**함정.** 제자리에서 `dist`를 갱신하는 것은 보통의 최단 경로에는 괜찮지만(수렴이 빨라질 뿐),
"간선 $K$개 이하의 가장 싼 경로" 같은 홉 제한 문제에는 *틀린다*. 한 라운드 안에서 레이블이 여러
간선을 연쇄로 타고 갈 수 있기 때문이다. 라운드마다 처음에 `prev = dist[:]`로 복사하고 `prev`에서
완화하라. C++에서는 더하기 전에 `dist[u] != INF`를 검사하지 않으면 `INF + w`가 오버플로한다. 큐
기반 변형(레이블이 바뀐 정점만 다시 훑기)은 최악은 같은 $O(nm)$이지만 실제로는 훨씬 빠른 경우가
많다. 같은 점화식을 결정 과정의 단계에 걸쳐 돌리면 [[02-foundations/rl-basics|7. 강화학습 기초]]의
가치 반복이다.

Floyd–Warshall(**Floyd–Warshall**)은 모든 쌍을 한꺼번에 답한다. 정점에 번호를 매기고 $D^{(k)}_{ij}$를 중간 경유지로
정점 $0..k$만 쓰는 $i \to j$ 최단 길이라 하자. 그런 최단 경로는 $k$를 피하거나 한 번 지나므로

$$D^{(k)}_{ij} = \min\big(D^{(k-1)}_{ij},\ D^{(k-1)}_{ik} + D^{(k-1)}_{kj}\big)$$

삼중 루프로 시간 $O(n^3)$, 공간 $O(n^2)$이다. 라운드 $k$ 동안 $k$행과 $k$열은 바뀌지 않으므로
2차원 표 하나를 제자리 갱신해도 안전하다. $k$ 루프는 반드시 가장 바깥(**must be outermost**)이어야 한다. 부분 문제가
$k$로 색인되기 때문이고, 안쪽에 두면 다른 것을 계산하게 된다. 끝에서 대각 원소가 $D_{ii} < 0$이면
그 정점이 음수 사이클 위에 있다.

```python
def floyd_warshall(n, edges):
    INF = float("inf")
    d = [ [0 if i == j else INF for j in range(n)] for i in range(n) ]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)        # keep the cheapest parallel edge
    for k in range(n):                   # k MUST be outermost
        for i in range(n):
            dik = d[i][k]
            for j in range(n):
                if dik + d[k][j] < d[i][j]:
                    d[i][j] = dik + d[k][j]
    return d                             # d[i][i] < 0  <=>  i lies on a negative cycle

print(floyd_warshall(3, [(0, 1, 4), (1, 2, 1), (0, 2, 7)])[0][2])   # 5
```

**무엇을 쓸까.**

| 상황 | 알고리즘 | 시간 |
|---|---|---|
| 가중치 없음, 출발점 하나 | BFS | $O(n + m)$ |
| 가중치 0 또는 1 | 덱을 쓰는 0-1 BFS | $O(n + m)$ |
| DAG, 임의 가중치 | 위상 순서로 완화 | $O(n + m)$ |
| 음이 아닌 가중치, 출발점 하나 | Dijkstra(이진 힙) | $O((n + m)\log n)$ |
| 음이 아닌 가중치, 목표 하나, 좋은 휴리스틱 | A* | 최악은 같고 확장은 훨씬 적음 |
| 음수 가중치, 또는 음수 사이클을 검출해야 함 | Bellman–Ford | $O(nm)$ |
| 모든 쌍, 조밀하거나 $n$이 수백 이하 | Floyd–Warshall | $O(n^3)$ |
| 모든 쌍, 희소, 음수 가중치 | Johnson: Bellman–Ford 한 번으로 재가중 후 Dijkstra $n$번 | $O(nm \log n)$ |

### 6. A* 탐색

**아이디어.** Dijkstra는 출발점 둘레로 원을 그리며 확장한다. A*는 열린 목록을
$f(n) = g(n) + h(n)$, 즉 지금까지의 비용과 남은 비용의 추정치의 합으로 정렬해서 그 원을 목표 쪽으로
늘인다. $g$, $h$, $f$가 플래너에게 무엇을 뜻하는지는 계획 페이지가 설명한다. 이 절은 알고리즘이 왜
옳은지와 어떻게 짜는지를 다룬다.

**세 가지 양.** $g(n)$은 시작점 $s$에서 $n$까지 지금까지 찾은 가장 싼 경로의 비용(Dijkstra의 레이블)이다. $h(n)$은 휴리스틱으로, 정점만의 함수로 남은 비용을 추정한다. $h^*(n)$은 참 잔여 비용, 즉 $n$에서 목표까지의 최단 경로 거리(§4)이며 목표에 도달할 수 없으면 $\infty$다. 열린 목록은 생성되었지만 아직 확장하지 않은 정점의 우선순위 큐이고, 닫힌 집합은 이미 확장한 정점들이다.

**허용적**(admissible)이란 $h(n) \le h^*(n)$, 즉 참 잔여 비용을 절대 과대추정하지 않는다는 뜻이다.
**일관적**(consistent)이란 모든 간선에서 $h(n) \le c(n, n') + h(n')$이고 $h(\text{goal}) = 0$이라는
뜻이다. 일관성은 허용성을 함의한다. $n$에서 목표까지의 최적 경로를 따라 부등식을 적용하면 $h$ 항이
소거되어 $h(n) \le h^*(n)$이 된다. 모든 조건을 이름 붙여 식으로 쓰면 이렇다.

- **허용적:** 추정값은 음수가 아니고 어느 정점에서도 참값을 넘지 않는다. 따라서 남은 비용의 하한이다.
$$0 \le h(v) \le h^*(v) \quad \text{for all } v \in V$$
- **일관적**(단조적이라고도 한다): 조건은 둘이다. 모든 간선에서의 삼각 부등식, 그리고 목표에서 0. 첫 조건은 $h$가 방금 치른 간선 비용보다 더 많이 떨어지지 않는다는 뜻이므로, $f(v) = g(u) + c(u, v) + h(v) \ge g(u) + h(u) = f(u)$가 되어 $f = g + h$는 경로를 따라 감소하지 않는다.
$$h(u) \le c(u, v) + h(v) \ \text{ for every edge } (u, v) \in E, \qquad h(\text{goal}) = 0$$

*반례(비허용적).* 간선 $s \to t$ (6), $s \to m$ (1), $m \to t$ (3). 최적은 비용 4인 $s \to m \to t$이고 $h^*(m) = 3$이다. $h(m) = 10$, $h(s) = h(t) = 0$으로 잡는다. A*는 $t$를 $f = 6$으로, $m$을 $f = 1 + 10 = 11$로 넣고, $t$를 먼저 꺼내 6을 반환한다. 허용적인 $h(m) = 3$이면 $m$의 $f = 4 < 6$이므로 A*는 4를 반환한다.

**일관성이 재확장 없음을 뜻하는 이유.** 축소 간선 비용을 정의한다.

$$c'(u, v) = c(u, v) - h(u) + h(v) \ge 0$$

이 부등식은 일관성 조건을 옮겨 쓴 것이다. $s$에서 $n$까지의 어떤 경로에서도 $h$ 항이 소거되므로,
경로의 축소 비용은 실제 비용 $g$에서 $h(s)$를 빼고 $h(n)$을 더한 값, 즉 $f(n) - h(s)$다. 따라서
$c'$ 위의 Dijkstra는 A*와 정확히 같은 순서로 정점을 꺼내고, $c' \ge 0$이므로 Dijkstra의 불변식이
성립한다. *정점이 처음 꺼내질 때 그 $g$는 최적이다.* 그러면 닫힌 집합이 안전하고 각 정점은 많아야
한 번 확장된다. 허용적이기만 한 휴리스틱에서는 정점이 너무 큰 $g$로 꺼내진 뒤 나중에 더 싸게 도달될
수 있고, 이때 A*는 닫힌 정점을 다시 열어야만 최적을 유지한다.

> [!example] 계산 예제 · Worked example
> **허용적이지만 비일관적.** 간선 $s \to a$ (1), $a \to m$ (1), $s \to m$ (3), $m \to t$ (3). 최적은 비용 5인 $s \to a \to m \to t$다. $h(s) = 0$, $h(a) = 4$, $h(m) = 0$, $h(t) = 0$으로 잡는다. 모두 허용적이지만($h^*(a) = 4$, $h^*(m) = 3$), $h(a) = 4 > c(a, m) + h(m) = 1$이므로 비일관적이다.
> - $s$를 꺼낸다. $a$를 $f = 1 + 4 = 5$로, $m$을 $f = 3 + 0 = 3$으로 넣는다.
> - $m$을 $g = 3$으로 꺼내 닫는다. $t$를 $f = 6$으로 넣는다.
> - $a$($f = 5$)를 꺼낸다. $m$에 비용 2를 제시하지만 $m$은 닫혀 있다.
> - 다시 열지 않으면 $t$를 비용 6으로 꺼내며, 최적이 아니다. 다시 열면 $m$이 $g = 2$로 돌아오고, 이어서 $t$가 $g = 5$로 나온다.
>
> **같은 그래프, 일관적.** $h(s) = 2$, $h(a) = 2$, $h(m) = 1$, $h(t) = 0$으로 잡으면 모든 간선이 $h(u) \le c(u,v) + h(v)$를 만족한다. 축소 비용은 $c'(s,a) = 1$, $c'(a,m) = 0$, $c'(s,m) = 2$, $c'(m,t) = 2$로 모두 $\ge 0$이다. 위의 비일관적 $h$에서는 $c'(a,m) = 1 - 4 + 0 = -3$이었다. 최적 경로의 축소 비용은 $1 + 0 + 2 = 3 = 5 - h(s)$로, 소거(telescoping)가 예측한 대로다. A*는 $s$($f = 2$), $a$($f = 3$), $g = 2$인 $m$($f = 3$), 그리고 $g = 5$인 $t$ 순서로 꺼낸다. 정점마다 한 번씩이며, 처음 꺼낼 때 이미 최적이다.

**격자 휴리스틱.** 격자에서 올바른 휴리스틱은 장애물을 없앤 상태에서 이동 집합의 정확한 비용이다.

| 이동과 비용 | 휴리스틱, $\Delta x, \Delta y$는 절대 차이 | 비고 |
|---|---|---|
| 4-연결, 비용 1 | 맨해튼 $\Delta x + \Delta y$ | 일관적이고 빈 격자에서 정확 |
| 8-연결, 직선 1, 대각 $\sqrt 2$ | 옥타일 $\max(\Delta x, \Delta y) + (\sqrt 2 - 1)\min(\Delta x, \Delta y)$ | 일관적; 여기서 맨해튼은 과대추정 |
| 8-연결, 모든 이동 비용 1 | 체비쇼프 $\max(\Delta x, \Delta y)$ | 일관적 |
| 위의 모든 경우, 또는 자유 공간 이동 | 유클리드 $\sqrt{\Delta x^2 + \Delta y^2}$ | 허용적·일관적이지만 약해서 확장이 더 많음 |

셀에 통과 비용이 있으면 휴리스틱에 가능한 *가장 싼* 한 걸음 비용을 곱하고, 단위를 맞춰라. 비용이
초 단위면 휴리스틱은 거리를 최고 속도로 나눈 값이어야 한다.

```python
import math

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def octile(a, b):
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

print(manhattan((0, 0), (3, 4)), euclidean((0, 0), (3, 4)), round(octile((0, 0), (3, 4)), 3))
```

**격자 A\*, 4-연결, 장애물 포함.** 연구실 인터뷰가 요구하는 버전이다.

```python
import heapq

def astar_grid(grid, start, goal):
    """grid[r][c] == 1 is an obstacle. 4-connected, unit cost. Returns (path, cost)."""
    rows, cols = len(grid), len(grid[0])
    if grid[start[0]][start[1]] or grid[goal[0]][goal[1]]:
        return None, float("inf")
    def h(cell):                         # Manhattan: consistent on a 4-grid
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
    g, parent, closed = {start: 0}, {start: None}, set()
    open_heap = [(h(start), h(start), start)]    # (f, h, cell): equal f prefers smaller h
    while open_heap:
        _, _, cell = heapq.heappop(open_heap)
        if cell in closed:
            continue                     # stale entry (lazy deletion)
        if cell == goal:                 # goal test on POP, not on push
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            return path[::-1], g[goal]
        closed.add(cell)
        r, c = cell
        for nxt in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nxt[0] < rows and 0 <= nxt[1] < cols and not grid[nxt[0]][nxt[1]] \
                    and nxt not in closed and g[cell] + 1 < g.get(nxt, float("inf")):
                g[nxt], parent[nxt] = g[cell] + 1, cell
                heapq.heappush(open_heap, (g[nxt] + h(nxt), h(nxt), nxt))
    return None, float("inf")

grid = [
    [0, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
]
print(astar_grid(grid, (2, 0), (0, 0)))  # cost 8: around the wall on the right
```

**동점 처리.** 맨해튼 거리를 쓰는 빈 격자에서는 출발점과 목표 사이 직사각형의 *모든* 셀이 최적
비용과 같은 $f$를 가지므로, 동점 순서가 임의이면 그 직사각형의 대부분을 확장할 수 있다. 동점을
더 작은 $h$(같은 말로 더 큰 $g$) 쪽으로 깨면 A*가 거의 곧장 목표로 달린다. $f$가 같은 것들 사이의
순서만 바꾸므로 최적성은 그대로다. 동점을 깨려고 $h$를 아주 조금 키우는 것은 다른 일이다. $h$를
살짝 비허용적으로 만들 수 있다.

**가중 A\*.** $g + \varepsilon h$($\varepsilon > 1$)로 정렬한다. 탐색이 더 탐욕적이 되어 확장이 훨씬
줄고, $h$가 일관적이면(또는 허용적이고 다시 열기를 하면) 반환 비용은 최적 $C^*$의 $\varepsilon$배 이하다. 우선순위와 보장을 식으로 쓰면
$$f_\varepsilon(n) = g(n) + \varepsilon\, h(n), \qquad C_{\text{returned}} \le \varepsilon\, C^*$$
이 상한 덕분에 거래가 받아들일 만하다.
최적성을 얼마나 포기할지 내가 고른다. 애니타임 플래너(ARA\*)는 큰 $\varepsilon$으로 경로를 빨리 얻고
시간이 남는 동안 값을 낮춘다.

**함정.** 목표를 넣을 때 검사하기, 간선 비용과 단위가 다른 휴리스틱, 대각 장애물 두 개 사이의
모서리를 가로지르는 8-연결 이동(인접한 직선 셀 중 하나라도 막혔으면 대각 이동을 금지하라), 그리고
격자 위 경로는 *격자에 대해서만* 최적인 계단 모양이라 여전히 평활화가 필요하다는 점을 잊는 것.

### 7. 하나의 알고리즘: 레이블 수정 탐색

위의 모든 알고리즘은 다음에 어떤 열린 정점을 꺼낼지의 규칙만 다른 같은 루프다. LaValle의
*Planning Algorithms*(2장)는 BFS, DFS, Dijkstra, best-first, A*를 열린 목록 $Q$를 어떻게 정렬하느냐만
실질적으로 다른 하나의 전방 탐색 틀로 제시하고, 이를 **레이블 수정**(label-correcting) 알고리즘으로
일반화한다(같은 계열이 Bertsekas의 *Dynamic Programming and Optimal Control* 1권 2장에도 나온다). 말로 하면 이 루프는 시작 정점 하나로
시작하는 할 일 목록을 유지한다. 목록에서 아무 정점이나 꺼내, 그 정점을 거치면 이웃에게 지금보다 싼
비용이 생기는지 확인하고, 그렇다면 이웃의 비용을 낮춘 뒤 이웃을 목록에 넣는다(이웃이 목표라면 대신 지금까지의 최선 답만 갱신한다). 목록이 비면 멈춘다.
기호로 쓰면 다음과 같다.

1. 모든 정점은 지금까지 찾은 최선의 도달 비용인 레이블 $C(x)$를 가진다. $C(s) = 0$, 나머지는 $\infty$. 지금까지 찾은 목표까지의 최선 비용 $U$를 유지한다.
2. $Q$에서 어떤 $x$를 꺼낸다. 각 간선 $x \to x'$에 대해 $C(x) + c(x, x') + h(x') < \min(C(x'), U)$이면($h$는 허용적이거나 $h = 0$) $C(x')$을 낮추고 부모를 기록한다. $x'$이 목표면 $U$를 갱신하고, 아니면 $Q$에 없을 때 $x'$을 다시 넣는다.
3. $Q$가 비면 멈춘다.

핵심 단어는 *수정*이다. 레이블이 좋아질 때마다 정점이 $Q$에 다시 들어갈 수 있다. 그 덕분에 음수
사이클이 없는 유한 그래프에서는 **$Q$의 정렬이 무엇이든** 루프가 최적 비용으로 끝난다. 정렬이 바꾸는
것은 답이 아니라 낭비되는 일의 양이다.

| $Q$에서 꺼내는 것 | 얻는 알고리즘 | 꺼낸 뒤에도 레이블이 바뀔 수 있나? |
|---|---|---|
| 가장 오래된 것(FIFO) | BFS; 가중 그래프에서는 큐 기반 Bellman–Ford | 가중 그래프에서는 그렇다 |
| 가장 최근 것(LIFO) | DFS | 그렇다, 흔히 여러 번 |
| 가장 작은 $C(x)$ | Dijkstra | 가중치가 $\ge 0$이면 절대 없음 |
| 가장 작은 $h(x)$ | 탐욕적 best-first | 그렇다 |
| 가장 작은 $C(x) + h(x)$ | A* | $h$가 일관적이면 절대 없음 |

Dijkstra와 A*가 *더하는* 것이 무엇인지 가장 깔끔하게 보는 방법이 이것이다. 처음 꺼내는 순간이
최종인 정렬이고, 그래서 다시 열기를 버리고 닫힌 집합을 쓸 수 있다. 다시 열지 않는 교과서식 전방
탐색은 그 정렬에서만 최적이며, 그래서 다시 열기 없이 돌린 탐욕적 best-first는 빠르지만 최적이 아니다.

```python
def label_correcting(adj, s, t, rule, h=lambda v: 0):
    """rule: 'fifo' | 'lifo' | 'dijkstra' | 'astar'. Returns (optimal cost, removals)."""
    INF = float("inf")
    C, Q, upper, removals = {s: 0}, [s], INF, 0
    while Q:
        if rule == "fifo":
            x = Q.pop(0)
        elif rule == "lifo":
            x = Q.pop()
        else:                            # linear scans for clarity; real code uses a heap
            key = (lambda v: C[v]) if rule == "dijkstra" else (lambda v: C[v] + h(v))
            x = min(Q, key=key)
            Q.remove(x)
        removals += 1
        for y, w in adj.get(x, ()):
            new = C[x] + w
            if new < C.get(y, INF) and new + h(y) < upper:
                C[y] = new
                if y == t:
                    upper = new
                elif y not in Q:
                    Q.append(y)
    return upper, removals

adj = {"s": [("b", 1), ("d", 5)], "a": [("d", 6)], "b": [("c", 2), ("d", 4), ("t", 6)],
       "c": [("d", 1), ("t", 3)], "d": [("a", 1), ("b", 2)]}
hh = {"s": 6, "a": 13, "b": 5, "c": 3, "d": 7, "t": 0}    # exact cost-to-go: consistent
for rule in ("fifo", "lifo", "dijkstra", "astar"):
    print(rule, label_correcting(adj, "s", "t", rule, hh.get if rule == "astar" else (lambda v: 0)))
# fifo (6, 7)   lifo (6, 7)   dijkstra (6, 5)   astar (6, 4)
```

네 규칙 모두 $s \to b \to c \to t$($1 + 2 + 3 = 6$)로 비용 6을 돌려준다. 다른 것은 일의 양뿐이다.
FIFO와 LIFO는 $d$와 $a$를 각각 두 번 꺼낸다. 확장한 뒤에 더 싼 경로가 나타나기 때문이다. Dijkstra는
각 정점을 한 번씩 꺼낸다. 정확한 잔여 비용을 $h$로 받은 A*는 $a$를 아예 확장하지 않는다. $C + h$가 이미
찾은 비용을 넘기 때문이다.

### 8. 신장 트리, 그리고 로봇 계획으로 가는 다리

**최소 신장 트리, 한 문단으로.** 최단 경로 트리는 출발점에서 각 정점까지의 거리를 최소화하고,
최소 신장 트리는 모든 정점을 잇는 간선 가중치의 *합*을 최소화한다. 두 트리는 일반적으로 다르다. 연결된 무방향 가중 그래프에서 신장 트리(**spanning tree**)는 (1) 모든 정점에 닿고 (2) 연결되어 있고 (3) 사이클이 없는 간선 부분집합 $T \subseteq E$이며, 세 조건이 합쳐져 간선 수는 정확히 $n - 1$개가 된다. 최소 신장 트리(**minimum spanning tree**)는 총 가중치가 가장 작은 신장 트리이므로 다음 문제를 푼다.
$$\min_{T \text{ spanning tree}} \ \sum_{e \in T} w(e)$$
*예:* 삼각형 $a - b$ (2), $b - c$ (2), $a - c$ (3)의 MST는 가중치 4인 $\{ab, bc\}$다. $a$에서의 최단 경로 트리는 $\{ab, ac\}$다. $c$까지 직접 가면 3, $b$를 거치면 4이기 때문이고, 그 트리의 가중치는 5다. *반례:* $\{ab, bc, ac\}$는 모두를 잇지만 사이클이 있으므로 트리가 아니다.
Prim 알고리즘은 키를 "출발점에서의 거리" 대신 "트리로 들어오는 가장 싼 간선의 가중치"로 바꾼
Dijkstra 루프다. Kruskal은 간선을 정렬하고 서로 다른 두 요소를 잇는 간선을 union-find로 확인하며
더한다. 증명과 코드는 [[02-foundations/algorithms/greedy-mst|11.4 그리디 알고리즘과 신장 트리]]에 있다.

**점유 격자 계획.** 2차원 내비게이션 스택의 전역 플래너는 계획 페이지가 설명하는 코스트맵 위에서
돌리는 §6이다. 실제 코드에서 바뀌는 것은 이론이 아니라 구현 방식이다.

- **셀은 해시하지 말고 인덱스로.** 평탄 인덱스 $r \cdot W + c$를 쓰고 $g$, 부모, 닫힘 표시를 원소
  $H \cdot W$개짜리 배열에 저장한다. $2000 \times 2000$ 지도는 셀이 $4 \times 10^6$개다. $g$를 담는
  `float32` 배열은 16 MB인 반면, 튜플 키 Python dict는 그 몇 배가 들고 조회도 느리다.
- **간선 비용은 셀에 들어가는 비용이다.** 걸음 길이에 셀 비용 값에서 나온 계수를 곱하고, 치명
  셀은 장애물로 건너뛴다. 휴리스틱에는 가능한 가장 싼 걸음 비용을 곱해라. 그러지 않으면 허용성이
  깨진다.
- **재계획.** 코스트맵이 바뀌면 많은 스택은 그냥 A*를 몇 Hz로 다시 돌린다. 2차원 탐색은 싸기
  때문이다. 증분 알고리즘(LPA\*, D\* Lite)은 이전 탐색을 재사용하며, 재계획이 잦고 변화가 국소적일
  때 이득이다.
- **격자 인공물.** 4-연결 경로는 계단 모양이고 8-연결 경로는 45°에 달라붙는다. 결과를 평활화하거나
  *any-angle* 탐색을 하라(Theta\*는 정점의 부모를 보이는 어떤 조상으로도 둘 수 있게 한다).

**래티스 플래너.** 자동차는 제자리에서 돌 수 없으므로 $(x, y)$ 격자는 실행 불가능한 경로를 가린다.
상태 래티스(**state lattice**)는 $(x, y, \theta)$를, 때로는 속도까지 이산화하고, 간선은 미리 계산한 **모션
프리미티브**, 즉 각 방향에서 출발하는 짧은 실행 가능 호다. 그래프는 방향이 있고 암묵적이며,
탐색은 여전히 A*다. 흔한 휴리스틱은 각각 제약 하나를 무시하는 두 추정의 최댓값이다. 하나는 방향을 무시하고
목표에서 격자 위로 거꾸로 Dijkstra를 한 번 돌려 얻는 장애물 인지 2차원 거리, 다른 하나는 회전 반경을
지키는 장애물 없는 거리다. 하한들의 최댓값은 여전히 하한이고(일관적 휴리스틱들의 최댓값은 일관적이다),
어느 하나보다 훨씬 빡빡하다. Hybrid A\*는 같은 목적으로 각 이산 셀 안에 연속
자세를 유지한다. 예를 들어 Nav2는 2차원 A\*, Hybrid-A\*, 상태 래티스 플래너를 제공한다.

**샘플링이 넘겨받는 곳.** 탐색 비용은 격자 셀 수에 따라 늘고, 셀 수는 차원에 지수적으로 는다. 3–4
차원($x, y, \theta$, 경우에 따라 속도)은 괜찮지만 관절 6–7개의 팔은 아니다.
[[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]이 그 숫자를 계산해 보인다. 거기서
플래너는 상태를 열거하기를 멈추고 샘플링하기 시작한다(PRM, RRT). 탐색은 조각으로 살아남는다. 샘플링
기반 로드맵도 결국 Dijkstra나 A*로 질의하고, 작업이 구조화되어 있으면 작은 팔 모션 프리미티브 집합
위의 탐색도 통한다. [[04-robotics/planning-decision-making|계획 페이지]]가 이 계열들을 나란히 놓는다.

### 스스로 점검

1. 내 BFS가 정점을 큐에 넣을 때가 아니라 꺼낼 때 방문 표시한다. 거리는 여전히 맞는가? 무엇이 잘못되는가?
2. Kahn 알고리즘이 정점을 $n$개보다 적게 출력하는 것이 왜 정확히 그래프에 사이클이 있을 때인가?
3. Dijkstra가 틀린 거리를 내는 정점 세 개짜리 그래프를 들고, 정당성 증명의 어느 단계가 실패하는지 말하라.
4. "A에서 B까지 경유 $K$회 이하의 가장 싼 항공편." 제자리 Bellman–Ford가 왜 틀린 답을 내며, 어떻게 고치는가?
5. Floyd–Warshall에서 $k$ 루프가 왜 가장 바깥이어야 하는가?
6. 대각 비용이 $\sqrt 2$인 8-연결 격자에서 맨해튼 거리는 허용적인가? 무엇을 써야 하나?
7. 동료가 "플래너를 빠르게 하려고" 맨해튼 휴리스틱에 10을 곱했다. 무엇을 얻고 무엇을 포기했나?
8. 레이블 수정 탐색에서 열린 목록을 FIFO에서 "가장 작은 $C(x)$"로 바꾸면 무엇이 바뀌는가: 답인가, 일의 양인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 그렇다. 처음 꺼낸 사본으로 거리를 확정하고 나중 사본을 건너뛴다면 맞다. 사본들은 거리가 감소하지 않는 순서로 큐에 있으므로 첫 사본이 최솟값을 가진다. 하지만 표시되기 전까지 정점이 들어오는 간선마다 한 번씩 큐에 들어갈 수 있어 큐가 $O(m)$개를 담고, 꺼낼 때 중복을 건너뛰지 않으면 같은 정점을 반복 처리한다.
> 2. 모든 DAG에는 진입 차수 0인 정점이 있고 이를 지워도 DAG가 남으므로, DAG에서는 큐가 일찍 비지 않는다. 큐가 비었는데 정점이 남았다면 각각 다른 남은 정점에서 오는 진입 간선이 있고, 그 간선을 거꾸로 따라가면 정점이 반복되어야 하니 사이클이다.
> 3. $s \to a$ (2), $s \to b$ (1), $a \to b$ ($-2$). Dijkstra는 $a$를 확장하기 전에 $b$를 1로 확정하지만 $s \to a \to b$는 비용 0이다. 실패하는 단계는 경로의 나머지가 음수 길이일 수 없다고 가정하는 $\delta(y) \le \delta(u)$다.
> 4. 제자리 갱신에서는 한 라운드 초반에 갱신된 레이블을 같은 라운드 후반에 쓸 수 있어, 한 라운드가 경로를 여러 간선만큼 늘릴 수 있고 "라운드 $k$ 후 간선 $k$개 이하"라는 의미가 사라진다. 이전 라운드 레이블의 복사본 `prev`에서 모든 간선을 완화하고, 정확히 $K + 1$ 라운드 돌린다(경유 횟수는 간선 수보다 하나 적다).
> 5. "중간 정점은 $0..k$만"이라는 부분 문제는 $k$로 색인되고, 라운드 $k$는 모든 $D^{(k-1)}$ 원소가 완성되어 있어야 한다. $k$가 안쪽에 있으면 뒤쪽 중간 정점을 거치는 경로가 만들어지기 전에 $D_{ij}$가 확정된다.
> 6. 아니다. $(0,0)$에서 $(1,1)$까지 맨해튼은 2라고 하지만 대각 한 걸음은 $\sqrt 2 \approx 1.414$다. 옥타일 거리를 써라.
> 7. $\varepsilon = 10$인 가중 A*다. 확장은 훨씬 줄지만 경로 비용이 최적의 10배까지 될 수 있고, 실제로는 장애물에 붙어 탐욕적으로 우회한다. $\varepsilon$을 의도적으로 고르거나(예: 1.5–3) 값을 낮춰 가는 애니타임 플래너를 써라.
> 8. 일의 양만 바뀐다. 음수 사이클이 없는 유한 그래프에서는 어떤 정렬이든 루프가 최적 비용으로 끝난다. 가중치가 음이 아니면 "가장 작은 $C$"가 각 정점을 처음 꺼내는 순간이 최종이 되는 정렬이라 아무것도 다시 확장되지 않는다.

### 출처

영어 절의 Sources 목록과 같다. 교재는 Cormen 외 *Introduction to Algorithms*, Roughgarden *Algorithms Illuminated* 2·3부, LaValle *Planning Algorithms* 2장, Bertsekas *Dynamic Programming and Optimal Control* 1권 2장이고, 원 논문은 Dijkstra (1959), Bellman (1958), Floyd (1962), Warshall (1962), Kahn (1962), Tarjan (1972), Sharir (1981), Hart·Nilsson·Raphael (1968), Pohl (1970), Likhachev 외 (2003), Koenig·Likhachev (2002), Pivtoraiko 외 (2009), Dolgov 외 (2010)다.
