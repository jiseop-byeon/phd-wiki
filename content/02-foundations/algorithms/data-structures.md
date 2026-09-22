---
title: 11.2 Core Data Structures
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Pick the structure whose operations match a problem, state each operation's cost and where it comes from, and write heaps, hash maps, BSTs, tries, and union-find from a blank file."
mastery-when: "Raise to Mastery only if a custom index or spatial data structure becomes part of the research contribution, for example a new nearest-neighbour structure for a planner or mapper."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/complexity-recursion|11.1]] (Big-O, amortized cost, recursion) · [[02-foundations/probability|3. Probability]] (expectation, for hashing and Bloom filters)
> [[02-foundations/algorithms/complexity-recursion|11.1]](Big-O, 분할상환 비용, 재귀) · [[02-foundations/probability|3. 확률]](기댓값, 해싱과 블룸 필터에 필요)

## English

A data structure is a promise about which operations are cheap. Most interview problems are decided in the first two minutes, when you notice which operations the problem repeats: "look up by key", "take the smallest", "the next larger element", "are these two connected". This page collects the structures that research code and interviews actually use. For each one it gives the operations, the reason each costs what it does, a short implementation, and the traps.

What interviews ask: the complexity table below from memory; hash map and heap *usage* in almost every problem; implementing a heap, a trie, or union-find from scratch; BST deletion; and, in robotics labs, "why is this nearest-neighbour search slow" (§8).

> [!note] First pass · 처음이라면
> Read §1 and learn the table. §2 is review except for the monotonic stack and deque, which are worth a first read. Then read §3 and §4, because hash maps and heaps appear in most problems. §5–§7 are the structures you implement when asked, and §8 connects the page to point clouds and planners.

### 1. Choosing a structure by the operations you need

List the operations the problem repeats, then pick the **smallest** structure that supports all of them. A structure that supports more operations usually pays for them in constant factors or memory. A balanced tree can do everything a heap does, but a heap is simpler and faster if you only ever need the minimum.

**Interface, contract, invariant.** Every structure on this page has two layers, and a precise answer names both.
- The **abstract data type** is the interface and its contract: which operations exist and what each must return. A stack's `pop` must return the most recently pushed item that is still present, whatever the storage.
- The **data structure** is a representation plus an **invariant**, a condition on the stored data that every operation may assume on entry and must restore before it returns. The invariant is what makes the costs true: a heap's "parent ≤ child" rule is the reason the minimum is always at index 0.

When you implement one, write the invariant down first; when an operation misbehaves, look for the line after which the invariant stops holding.

| Structure | Lookup | Insert / delete | Good for | Python | C++ |
|---|---|---|---|---|---|
| Array (fixed size) | by index O(1); by value O(n), or O(log n) if sorted | O(n), because elements shift | dense numeric data, cache-friendly scans | `array.array`, NumPy `ndarray` | `std::array`, C array |
| Dynamic array | by index O(1) | append / pop at end O(1) amortized; middle O(n) | the default sequence | `list` | `std::vector` |
| Linked list (doubly) | by index O(n) | O(1) at a node you already hold | splicing, recency order (LRU) | none built in; `OrderedDict` for LRU | `std::list` |
| Stack | top O(1) | push / pop O(1) | LIFO: DFS, parsing, undo, monotonic stack | `list` with `append` / `pop` | `std::stack`, `std::vector` |
| Queue / deque | both ends O(1); middle O(n) | both ends O(1) | FIFO: BFS, sliding windows | `collections.deque` | `std::queue`, `std::deque` |
| Hash map / set | by key O(1) expected, O(n) worst | O(1) expected (amortized over resizes) | membership, counting, memoization, grouping | `dict`, `set`, `Counter`, `defaultdict` | `std::unordered_map`, `std::unordered_set` |
| Binary heap | min O(1); any other key O(n) | push / pop O(log n); build O(n) | repeated minimum: Dijkstra, A*, top-k, event queues | `heapq` (a min-heap on a list) | `std::priority_queue` (a max-heap) |
| Balanced BST | key, min / max, predecessor / successor O(log n) | O(log n) | ordered keys, range queries, floor / ceiling | none in stdlib; `sortedcontainers` (third party) | `std::map`, `std::set` |
| Trie | word or prefix O(L), L = key length | O(L) | prefix queries, autocomplete, longest-prefix match | nested `dict` | none; hand-rolled |
| Union-find | find O(α(n)) amortized, where α(n) ≤ 4 in practice, so effectively constant (§7) | union O(α(n)) amortized; no delete | incremental connectivity, Kruskal, clustering | none; about 20 lines | none in std (Boost `disjoint_sets`) |

A quick way to choose:

- **Only "is x present?" or "value for key x"** → hash set / hash map.
- **Only "give me the smallest (or largest) now"** → heap.
- **Order matters: "smallest key ≥ x", ranges, sorted iteration with inserts** → balanced BST (or a sorted list if inserts are rare).
- **"Do these two belong to the same group?" while groups merge** → union-find.
- **Prefixes of strings** → trie, or a sorted list plus binary search ([[02-foundations/algorithms/sorting-divide-conquer|11.3 §6]]).
- **Nearest point in low-dimensional space** → KD-tree (a binary tree that splits space one coordinate at a time) or a voxel hash (a hash map keyed by integer grid cell); both are in §8.

Two Python traps appear in almost every review: `list.pop(0)` and `list.insert(0, x)` are O(n), so use `deque`; and `x in some_list` is O(n), so convert to a `set` when you test membership inside a loop.

### 2. Arrays, linked lists, stacks, queues, deques

**Arrays** store elements in one contiguous block, so the address of element $i$ is `base + i * size`. With $s$ the bytes per element, the address is one multiplication and one addition away, so it costs the same for every $i$:
$$\text{addr}(i) = \text{base} + i \cdot s, \qquad 0 \le i < n$$
For 8-byte doubles starting at address 1000, element 5 is at $1000 + 5 \cdot 8 = 1040$. The bound $0 \le i < n$ is part of the contract: C++ `operator[]` does not check it, and reading index $n$ returns whatever memory follows. That is why indexing is O(1) and why sequential scans are fast on real hardware: the CPU cache pre-loads the next elements. Inserting in the middle shifts everything after it, which costs O(n).

**Dynamic arrays** (`list`, `std::vector`) keep spare capacity. When they are full, they allocate a larger block, usually 1.5× or 2× the old size, and copy everything. One append can cost O(n), but the total cost of n appends is O(n). With doubling, the copies cost at most $1 + 2 + 4 + \dots + n < 2n$, so each append is O(1) amortized (the accounting argument, and the invariant $0 \le \text{size} \le \text{capacity}$, are in [[02-foundations/algorithms/complexity-recursion|11.1 §4]]). The growth must be *geometric*. Growing by a fixed +100 slots makes n appends cost O(n²). C++ trap: a reallocation invalidates every pointer, reference, and iterator into the vector.

**Linked lists** store each element in its own node with a pointer to the next (and, if doubly linked, the previous) node. Once you hold a node, inserting or removing next to it is O(1), because only pointers change. The list itself holds a `head` pointer (and a `tail`, if doubly linked). A doubly linked list keeps the invariant that the two directions agree, `u.next.prev is u` for every node `u` with a successor, with `head.prev` and `tail.next` empty; a splice that updates `next` but forgets `prev` leaves forward and backward traversal seeing different lists. Reaching the $i$-th element is O(n), and every hop is likely a cache miss. In practice a linked list wins only when you splice at nodes you already hold. The standard example is an LRU cache: a hash map from key to list node, plus a doubly linked list kept in recency order, gives O(1) `get` and `put`. In Python, `OrderedDict.move_to_end` does exactly this. Interview staples are reversing a list in place (three pointers) and the fast/slow two-pointer trick for finding the middle or detecting a cycle.

**Stacks** (LIFO) and **queues** (FIFO) are access policies, not storage methods. A stack's contract is that `pop` returns the item pushed most recently among those still present (last in, first out), which in one line says that a push followed by a pop gives back the pushed item and the untouched stack:
$$\text{pop}(\text{push}(S, x)) = (S,\ x)$$
A queue's contract is that `popleft` returns the item added earliest among those still present (first in, first out). Push 1, 2, 3 and remove three times: a stack gives 3, 2, 1 and a queue gives 1, 2, 3. A deque (double-ended queue) allows adds and removals at both ends, so it can serve as either. A stack is a `list` used through `append` and `pop`. A queue should be a `collections.deque`, which is a linked list of fixed-size blocks and gives O(1) at both ends. Indexing into the middle of a deque is O(n). The stack drives DFS, expression parsing, and "undo". The queue drives BFS ([[02-foundations/algorithms/graph-algorithms|11.6]]).

**The monotonic stack / deque pattern.** Many problems ask, for each element, about the nearest larger (or smaller) element, or about the maximum of a moving window. The naive answer rescans and costs O(nk) or O(n²). The idea is to **keep only the candidates that could still be an answer, in sorted order, and throw the rest away for good.**

For the sliding-window maximum, keep a deque of indices whose values strictly decrease from front to back. When a new value $x$ arrives, pop from the back every index whose value is $\le x$. Those elements are older *and* no larger than $x$, so while $x$ is in the window they can never be the maximum, and they will leave the window before $x$ does. Then pop the front if it has slid out of the window. The front is now the maximum.

- *Invariant:* the deque holds exactly the indices in the current window that are not dominated by a later, larger-or-equal element, in decreasing value order.
- *Complexity:* O(n) total, even though there is a nested `while`, because each index is pushed once and popped at most once. This amortized argument is the part interviewers want to hear.

```python
from collections import deque

def sliding_window_max(nums, k):
    """Max of every length-k window in O(n)."""
    dq = deque()          # indices; their values strictly decrease front to back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()      # a smaller older value can never be a max again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()  # front index has slid out of the window
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

def next_greater(nums):
    """For each i, the first value to its right that is larger (or None)."""
    ans = [None] * len(nums)
    stack = []            # indices still waiting; their values decrease
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        stack.append(i)
    return ans

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
print(next_greater([2, 1, 5, 3, 4]))                     # [5, 5, None, 4, None]
```

> [!example] Worked example · 계산 예제
> `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`; the deque is shown as values.
> i=0: [1]. i=1: 3 pops 1 → [3]. i=2: [3, −1], window full → **3**. i=3: [3, −1, −3] → **3**. i=4: 5 pops all three → [5] → **5**. i=5: [5, 3] → **5**. i=6: 6 pops 3 and 5 → [6] → **6**. i=7: 7 pops 6 → [7] → **7**.
> Eight pushes and seven pops: linear work, as the amortized argument promised.

Pitfalls: storing values instead of indices (then you cannot tell when the front has left the window); using `<` where `<=` is needed, or the reverse, which changes how ties are handled; forgetting to emit output only once the first window is full. The same deque gives a rolling maximum of a force signal over the last k samples, and a rolling minimum gives the lower envelope of a noisy range reading. Both run in O(1) amortized per sample, independent of the window length.

### 3. Hash tables

**The idea in one sentence:** turn the key into an array index with a hash function, so a lookup jumps straight to where the key must be.

**Hash function.** A hash function maps a key to an integer, and the table reduces it to a bucket with `h(key) % m`, where $m$ is the number of buckets. It must be *deterministic* (equal keys give equal hashes) and should *spread* realistic keys evenly. A bad hash takes something regular in the data and keeps it. For example, bucketing memory addresses, which are multiples of 8, by `addr % 1000` never uses most buckets.

Written as one map from the universe $U$ of possible keys to bucket indices, the requirement and the hope are
$$h: U \to \{0, 1, \dots, m-1\}, \qquad x = y \implies h(x) = h(y)$$
The implication is a *requirement*, because a lookup recomputes $h$ and must land in the bucket the insert used. Spreading is a *hope*, measured by how evenly real keys fill the buckets. With $h(k) = k \bmod 10$, the keys 42 and 17 go to buckets 2 and 7, and 52 collides with 42 in bucket 2.

**Collisions are unavoidable,** because many possible keys share few buckets. Two standard fixes:

- **Separate chaining:** each bucket holds a small list, and operations scan the list in bucket `h(k)`. Deletion is easy. `std::unordered_map` works this way.
- **Open addressing:** one key per slot. On a collision, follow a *probe sequence* (linear probing tries the next slot, and so on) until an empty slot appears. This is cache-friendly with no per-node allocation. But deletion needs *tombstones*, because simply emptying a slot would break the probe chain of keys stored after it, and performance collapses as the table fills. CPython's `dict` uses open addressing with a pseudo-random probe order.

**The invariant each scheme keeps.** With chaining, every stored key $k$ is in the list of bucket $h(k)$, so a lookup that scans only that list is correct. With open addressing, key $k$ sits at some position of its probe sequence, for linear probing
$$s_i(k) = (h(k) + i) \bmod m, \qquad i = 0, 1, 2, \dots$$
and every earlier position of that sequence is occupied or holds a tombstone, so a lookup may stop at the first truly empty slot. Example with $m = 10$: insert 42, which takes slot 2, then 52, which probes slot 2, finds it taken, and lands in slot 3. Emptying slot 2 to delete 42 would make a later lookup for 52 stop at slot 2 and report "absent", which is exactly why deletion leaves a tombstone.

<svg viewBox="0 0 560 272" style="max-width:100%;height:auto" role="img" aria-label="Hash table with h(k) = k mod 10 and keys 42, 17, 52: chaining puts 42 and 52 in one list at bucket 2; linear probing moves 52 to slot 3, and deleting 42 leaves a tombstone so a lookup of 52 still reaches slot 3.">
  <defs><marker id="ad1e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="20" y="22" font-size="12" fill="currentColor" font-weight="bold">separate chaining</text>
  <text x="31" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">0</text>
  <rect x="20" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="53" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">1</text>
  <rect x="42" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="75" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">2</text>
  <rect x="64" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <circle cx="75" cy="66" r="2.6" stroke="none" fill="currentColor"/>
  <line x1="75" y1="66" x2="75" y2="99" stroke="currentColor" stroke-width="1.1" marker-end="url(#ad1e)"/>
  <rect x="59" y="100" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text x="75" y="116.5" font-size="12" fill="currentColor" text-anchor="middle">42</text>
  <line x1="75" y1="124" x2="75" y2="145" stroke="currentColor" stroke-width="1.1" marker-end="url(#ad1e)"/>
  <rect x="59" y="146" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text x="75" y="162.5" font-size="12" fill="currentColor" text-anchor="middle">52</text>
  <text x="97" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">3</text>
  <rect x="86" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="119" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">4</text>
  <rect x="108" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="141" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">5</text>
  <rect x="130" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="163" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">6</text>
  <rect x="152" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="185" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">7</text>
  <rect x="174" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <circle cx="185" cy="66" r="2.6" stroke="none" fill="currentColor"/>
  <line x1="185" y1="66" x2="185" y2="99" stroke="currentColor" stroke-width="1.1" marker-end="url(#ad1e)"/>
  <rect x="169" y="100" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text x="185" y="116.5" font-size="12" fill="currentColor" text-anchor="middle">17</text>
  <text x="207" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">8</text>
  <rect x="196" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="229" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">9</text>
  <rect x="218" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="308" y="22" font-size="12" fill="currentColor" font-weight="bold">open addressing, linear probing</text>
  <text x="319" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">0</text>
  <rect x="308" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="341" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">1</text>
  <rect x="330" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="363" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">2</text>
  <rect x="352" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="353.5" y="55.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="363" y="70.5" font-size="11" fill="currentColor" text-anchor="middle">42</text>
  <text x="385" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">3</text>
  <rect x="374" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="375.5" y="55.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="385" y="70.5" font-size="11" fill="currentColor" text-anchor="middle">52</text>
  <text x="407" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">4</text>
  <rect x="396" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="429" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">5</text>
  <rect x="418" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="451" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">6</text>
  <rect x="440" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="473" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">7</text>
  <rect x="462" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="463.5" y="55.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="473" y="70.5" font-size="11" fill="currentColor" text-anchor="middle">17</text>
  <text x="495" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">8</text>
  <rect x="484" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="517" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">9</text>
  <rect x="506" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="319" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">0</text>
  <rect x="308" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="341" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">1</text>
  <rect x="330" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="363" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">2</text>
  <rect x="352" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <line x1="357" y1="171" x2="369" y2="185" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"/>
  <line x1="369" y1="171" x2="357" y2="185" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"/>
  <text x="385" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">3</text>
  <rect x="374" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="375.5" y="167.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="385" y="182.5" font-size="11" fill="currentColor" text-anchor="middle">52</text>
  <text x="407" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">4</text>
  <rect x="396" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="429" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">5</text>
  <rect x="418" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="451" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">6</text>
  <rect x="440" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="473" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">7</text>
  <rect x="462" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="463.5" y="167.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="473" y="182.5" font-size="11" fill="currentColor" text-anchor="middle">17</text>
  <text x="495" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">8</text>
  <rect x="484" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="517" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">9</text>
  <rect x="506" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <path d="M 363.0 80 Q 374.0 94 385.0 81" stroke="currentColor" stroke-width="1.1" fill="none" marker-end="url(#ad1e)"/>
  <text x="308" y="108" font-size="11" fill="currentColor">52: slot 2 taken, go to 3</text>
  <text x="308" y="138" font-size="11" fill="currentColor" fill-opacity="0.9">after deleting 42: slot 2 holds a tombstone</text>
  <path d="M 363.0 192 Q 374.0 206 385.0 193" stroke="currentColor" stroke-width="1.1" fill="none" marker-end="url(#ad1e)"/>
  <text x="308" y="220" font-size="11" fill="currentColor">lookup 52: tombstone, go on → found at 3</text>
  <line x1="12" y1="240" x2="548" y2="240" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="280" y="260" font-size="12" fill="currentColor" text-anchor="middle">h(k) = k mod 10, keys inserted in the order 42, 17, 52</text>
</svg>

The keys 42, 17 and 52 inserted in that order with $h(k) = k \bmod 10$. With chaining, 42 and 52 share the list of bucket 2 and 17 sits alone in bucket 7. With linear probing, 52 finds slot 2 taken and lands in slot 3; after 42 is deleted, slot 2 keeps a tombstone, so a lookup for 52 passes it and still reaches slot 3 instead of stopping at an empty slot 2.

**Load factor and resizing.** The load factor is the number of stored keys per bucket,
$$\alpha = \frac{n}{m}$$
with $n$ keys and $m$ buckets, so it may exceed 1 under chaining but must stay below 1 under open addressing, since each slot holds one key. With chaining, a lookup scans a list of expected length about $\alpha$. With open addressing under an idealized uniform-probing assumption, an unsuccessful search takes about $1/(1-\alpha)$ probes: 10 at $\alpha = 0.9$. Linear probing is worse because occupied slots clump together: a key that hashes anywhere into a run of filled slots lands at the end of that run and makes it one longer, so long runs grow faster than short ones and a search must walk the whole run. Knuth's analysis gives about $\tfrac12\bigl(1 + 1/(1-\alpha)^2\bigr) \approx 50$ probes at $\alpha = 0.9$. So implementations keep $\alpha$ bounded. Java's `HashMap` resizes above 0.75, CPython's `dict` above about 2/3, and `std::unordered_map` above `max_load_factor()` (default 1.0). Resizing doubles $m$ and **re-inserts every key**, because `h(k) % m` changes when $m$ changes. You cannot just copy the old array. Because the table doubles, the resize cost averages out to O(1) per insert, by the same argument as for dynamic arrays.

**Why "expected O(1)" needs a good hash — universal hashing.** For any *fixed* hash function there is a bad input. By the pigeonhole principle, some bucket receives at least $\lvert U\rvert/m$ keys of the universe $U$, and an input drawn only from those keys puts everything in one chain, so every operation is O(n). The fix is to randomize the *function* instead of hoping the *data* are random.

> [!note] Definition · 정의
> A family $H$ of hash functions is **universal** if, for every pair of distinct keys $x \ne y$, a function drawn at random from $H$ makes them collide with probability at most $1/m$ (Carter & Wegman 1979). The probability is over the random choice of $h$, since the keys are fixed first:
> $$\Pr_{h \in H}\left[h(x) = h(y)\right] \le \frac{1}{m} \quad \text{for all } x \ne y$$

Why that is enough: fix *any* set of $n$ stored keys $k_1, \dots, k_n$ and a key $x$ that is not stored. The chain an unsuccessful lookup for $x$ scans holds exactly the stored keys that collide with $x$, so its length $L$ is a count, and a count is a sum of **indicator variables**. An indicator variable is a random variable that takes only the values 0 and 1: it is 1 when its event happens and 0 when it does not. Its expectation is therefore the probability of the event, $E[X] = 1 \cdot \Pr[\text{event}] + 0 \cdot \Pr[\text{no event}]$. Here there is one per stored key:
$$X_j = \begin{cases} 1 & h(k_j) = h(x) \\ 0 & \text{otherwise} \end{cases}, \qquad L = \sum_{j=1}^{n} X_j, \qquad E[L] = \sum_{j=1}^{n} \Pr[h(k_j) = h(x)] \le \frac{n}{m} = \alpha$$
The middle equality is linearity of expectation ([[02-foundations/probability|3. Probability §2]]), which needs no independence between the $X_j$, and the last step applies the universal bound to each pair $k_j \ne x$. With $n = 6$ stored keys and $m = 8$ buckets, each $X_j$ has expectation at most $1/8$, so the expected chain length is at most $6/8 = 0.75$. Non-example: $L$ itself is not an indicator, since it can be 2 or more; the point of the trick is that you never need $L$'s distribution, only the $n$ probabilities. The same trick counts the comparisons of randomized quicksort in [[02-foundations/algorithms/sorting-divide-conquer|11.3 §3]]. So operations run in O(1 + α) expected time, and the expectation is over the random choice of function, not over the data.

A classic universal family is $h_{a,b}(x) = ((ax+b) \bmod p) \bmod m$ with $p$ a prime larger than every key and $a \ne 0$, $b$ chosen at random. Checked exhaustively for $p = 7$, $m = 3$ and keys $0$ to $6$ (all $6 \times 7 = 42$ choices of $a$ and $b$), the worst pair of distinct keys collides under 10 of the 42 functions, probability $0.238 \le 1/3$. Non-example: the single function $h(x) = x \bmod 3$ is a family of one, and the keys 0, 3, 6, 9 collide under it with probability 1. The same principle is the reason Python randomizes string hashing per process (SipHash, `PYTHONHASHSEED`).

**Adversarial worst case.** Crosby & Wallach (2003) showed that real servers could be stalled by sending keys crafted to collide under a known, fixed hash function. The defences are a keyed or randomized hash, or a structure with a worst-case guarantee (Java's `HashMap` turns a long chain into a balanced tree). In CPython, `int` hashes are *not* randomized (`hash(n) == n` for small `n`), so a hostile set of integer keys can still degrade a `dict`. This almost never matters in robotics code, but it is the complete answer to "is a dict lookup always O(1)?": expected O(1), worst case O(n).

**Hashability in Python.** A key must be *hashable*: its `__hash__` never changes during its lifetime, and equal objects have equal hashes. The second condition is the hash-function requirement above, written for Python objects:
$$a == b \implies \text{hash}(a) == \text{hash}(b)$$
The first matters because the table chose the key's bucket from its hash at insert time, so a key whose hash later changed would be looked for in the wrong bucket. Mutable containers (`list`, `dict`, `set`) are not hashable. `tuple` is hashable when its contents are, and `frozenset` is the hashable set. A `@dataclass(frozen=True)` gets a field-based hash. Two traps catch people. First, `1`, `1.0` and `True` are equal and hash equally, so they are *the same key*. Second, floating-point coordinates make terrible keys, because `0.1 + 0.2 != 0.3`. In grid maps and voxel filters, quantize coordinates to integer cell indices first. NumPy arrays are not hashable; use `tuple(a)` or `a.tobytes()`.

```python
from dataclasses import dataclass

seen = {}
try:
    key = [1, 2]
    seen[key] = "x"                    # lists are mutable -> unhashable
except TypeError as e:
    print("TypeError:", e)
seen[(1, 2)] = "tuple ok"              # tuples of hashables are hashable
seen[frozenset({"a", "b"})] = "frozenset ok"

d = {1: "int"}
d[True] = "bool"                       # True == 1 and hash(True) == hash(1)
print(d)                               # {1: 'bool'}  -- one key, not two

@dataclass(frozen=True)                # frozen dataclass gets __hash__ from its fields
class Cell:
    ix: int
    iy: int

def voxel_key(x, y, res=0.25):         # key on integer cells, not raw floats
    return Cell(int(x // res), int(y // res))   # // floors, so negatives bin correctly

print((0.1 + 0.2) in {0.3})                         # False: 0.30000000000000004
grid = {voxel_key(0.1 + 0.2, 1.0): "hit"}
print(voxel_key(0.3, 1.0) in grid, voxel_key(-0.1, 0.0))  # True Cell(ix=-1, iy=0)
```

A point that lies almost exactly on a cell boundary can fall into either neighbouring cell, so a radius query over a voxel hash must also check the adjacent cells.

A minimal chaining table shows where the costs come from:

```python
class ChainedHashMap:
    """Separate chaining; doubles the bucket array when load factor > 0.75."""
    def __init__(self, capacity=8):
        self.buckets = [list() for _ in range(capacity)]
        self.size = 0

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)       # overwrite, do not duplicate
                return
        b.append((key, value))
        self.size += 1
        if self.size > 0.75 * len(self.buckets):
            old = self.buckets             # every key must be re-bucketed,
            self.buckets = [list() for _ in range(2 * len(old))]  # since % changed
            for pair in (p for bucket in old for p in bucket):
                self._bucket(pair[0]).append(pair)

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

m = ChainedHashMap()
for i in range(100):
    m.put(f"cell{i}", i)
print(m.get("cell42"), m.size, len(m.buckets))  # 42 100 256
```

Interview patterns built on a hash map: two-sum (store what you have seen, look up `target - x`), counting with `Counter`, grouping with `defaultdict(list)` (anagrams keyed by `tuple(sorted(word))`), a visited set in graph search, and memoization ([[02-foundations/algorithms/dynamic-programming|11.5]]). C++ trap: `m[key]` *inserts* a default value when the key is missing, so use `find` or `contains` (C++20) to test membership.

#### Bloom filter

A Bloom filter (Bloom 1970) answers "have I seen x?" in a small, fixed number of bits. It may answer *yes* wrongly (a false positive), but it never answers *no* wrongly. Use an array of $m$ bits and $k$ hash functions. To insert, set the $k$ bits $h_1(x),\dots,h_k(x)$. To query, report "present" only if all $k$ bits are set. An inserted item always has its bits set, so there are no false negatives. It stores no keys and cannot delete (clearing a bit could erase other items). After $n$ insertions, a given bit is still 0 with probability $(1-1/m)^{kn} \approx e^{-kn/m}$, so a query for an absent item finds all $k$ of its bits set with probability

$$p \approx \left(1 - e^{-kn/m}\right)^{k}$$

This treats the hashes as independent and uniform, which is a heuristic. For a fixed budget of $m/n$ bits per item, $p$ is minimized at $k^* = (m/n)\ln 2$. The trade-off: more hash functions give an absent item more bits that must all be set, but they also fill the array faster. To see where the balance falls, let $q = e^{-kn/m}$ be the fraction of bits still 0, so $k = -(m/n)\ln q$ and $\ln p = k\ln(1-q) = -(m/n)\ln q\,\ln(1-q)$. That expression is unchanged when $q$ and $1-q$ swap, and it is smallest at $q = 1/2$. So at the optimum half the bits are set and $p^* \approx 2^{-k^*} \approx 0.6185^{\,m/n}$. The error falls exponentially in the bits per item, so each extra 4.8 bits per item cuts the false-positive rate by 10×.

> [!example] Worked example · 계산 예제
> **8 bits per item:** $k^* = 8 \ln 2 = 5.55$. Using $k = 5$ or $6$ gives $p \approx 2.17\%$ or $2.16\%$.
> **10 bits per item:** $k^* = 6.93 \to 7$, so $p = (1 - e^{-0.7})^7 \approx 0.82\%$.
> **Sizing for 1 % on $10^6$ items:** $m/n = \log_2(100)/\ln 2 \approx 9.6$ bits, which is about 1.2 MB, with $k = 7$. A Python `set` of a million strings takes tens of megabytes.
> A simulation with random bit positions ($n = 1000$, $m = 10\,000$, $k = 7$) measured 0.81 %, matching the formula. The double-hashing filter below measures about 0.9 %, slightly worse, because its $k$ positions are not fully independent.

```python
import hashlib, math

class BloomFilter:
    def __init__(self, m_bits, k):
        self.m, self.k = m_bits, k
        self.bits = bytearray(m_bits)

    def _indices(self, item):
        d = hashlib.sha256(repr(item).encode()).digest()
        h1 = int.from_bytes(d[:8], "little")
        h2 = int.from_bytes(d[8:16], "little") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]  # double hashing

    def add(self, item):
        for j in self._indices(item):
            self.bits[j] = 1

    def __contains__(self, item):
        return all(self.bits[j] for j in self._indices(item))

n, m = 1000, 10_000                      # 10 bits per stored item
k = round(m / n * math.log(2))           # 7
bf = BloomFilter(m, k)
for x in range(n):
    bf.add(x)
assert all(x in bf for x in range(n))    # never a false negative
fp = sum(("q", x) in bf for x in range(100_000)) / 100_000
print(k, round((1 - math.exp(-k * n / m)) ** k, 4), fp)  # 7 0.0082, measured close to that
```

Use a Bloom filter as a cheap pre-check in front of an expensive exact lookup, such as a disk read, a network call, or a large visited set in an enormous search. A "no" answer skips the expensive lookup, and a "yes" answer is then confirmed with the exact lookup.

### 4. Binary heaps

**The idea in one sentence:** a complete binary tree in which every parent is ≤ its children, so the minimum sits at the root, and the tree is stored in a plain array with no pointers.

**Array layout (0-indexed).** The node at index $i$ has children at $2i+1$ and $2i+2$ and parent at $(i-1)//2$. Because the tree is complete (every level full except the last, which fills left to right), there are no gaps in the array and the height is $\lfloor \log_2 n \rfloor$. Heap order is *vertical only*: siblings are unordered, so a heap is **not** sorted, and searching it for an arbitrary key is O(n). Some textbooks use 1-indexing (children $2i, 2i+1$, parent $i//2$). Say which one you use.

**The two invariants.** A binary min-heap is an array $A[0], \dots, A[n-1]$ with the **shape property**, that the implicit tree is complete, which a gap-free array under this indexing satisfies automatically, and the **heap property**:
$$A[\lfloor (i-1)/2 \rfloor] \le A[i] \quad \text{for every } 1 \le i < n$$
So every parent is at most its children, and following the path up from any node shows that $A[0]$ is the minimum. A max-heap reverses the inequality. Non-example: `[2, 3, 1]` is not a heap, because index 2 holds 1, below its parent 2. A heap is the usual implementation of a **priority queue**, the abstract type whose operations are "insert with a priority" and "remove the item with the smallest priority".

> [!example] Worked example · 계산 예제
> The array `[1, 3, 2, 7, 4, 5]` is a min-heap. Index 1 (value 3) has children at indices 3 and 4 (values 7 and 4), both ≥ 3. Index 5 (value 5) has parent $(5-1)//2 = 2$ (value 2). Index 2's children are indices 5 and 6, and index 6 does not exist. The array is not sorted, since 7 comes before 4, yet it is a valid heap.

**Sift-up (push).** Append the new key at the end, the next free leaf, then swap it with its parent while it is smaller. Only the path to the root can be out of order, so this costs at most one swap per level: O(log n).

**Sift-down (pop).** Remove the root, move the *last* leaf into the root, then swap it with its **smaller** child while it is larger than that child. Swapping with the smaller child makes the new parent ≤ both children. Swapping with the larger child would break heap order at once. One swap per level: O(log n).

<svg viewBox="0 0 560 276" style="max-width:100%;height:auto" role="img" aria-label="Binary min-heap [1, 3, 2, 7, 4, 5] as a tree and an array; popping 1 moves the last leaf 5 to the root, which swaps once with its smaller child 2, giving [2, 3, 5, 7, 4].">
  <defs><marker id="ad2e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="swd2e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="96" y="22" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">(a) the heap</text>
  <line x1="87" y1="65.4" x2="63" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="105" y1="65.4" x2="129" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="48.2" y1="111.6" x2="37.8" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="59.8" y1="111.6" x2="70.2" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="132.6" y1="111.8" x2="123.4" y2="132.2" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <circle cx="96" cy="56" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="96" y="60.5" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <circle cx="54" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="54" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="138" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="138" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="32" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="32" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <circle cx="76" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="76" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <circle cx="118" cy="144" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="118" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <rect x="18" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="31" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <text x="31" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <rect x="44" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="57" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <text x="57" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">1</text>
  <rect x="70" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="83" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <text x="83" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">2</text>
  <rect x="96" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="109" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <text x="109" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">3</text>
  <rect x="122" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="135" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <text x="135" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">4</text>
  <rect x="148" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="161" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <text x="161" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <text x="280" y="22" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">(b) pop 1: last leaf 5 → root</text>
  <line x1="271" y1="65.4" x2="247" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="289" y1="65.4" x2="313" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="232.2" y1="111.6" x2="221.8" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="243.8" y1="111.6" x2="254.2" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <circle cx="280" cy="56" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="280" y="60.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <circle cx="238" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="238" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="322" cy="100" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="322" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="216" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="216" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <circle cx="260" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="260" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <rect x="202" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="215" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <text x="215" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <rect x="228" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="241" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <text x="241" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">1</text>
  <rect x="254" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="267" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <text x="267" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">2</text>
  <rect x="280" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="293" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <text x="293" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">3</text>
  <rect x="306" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="319" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <text x="319" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">4</text>
  <rect x="332" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0" stroke-opacity="0.35" stroke-dasharray="3 3"/>
  <text x="345" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <text x="464" y="22" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">(c) after one swap</text>
  <line x1="455" y1="65.4" x2="431" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="473" y1="65.4" x2="497" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="416.2" y1="111.6" x2="405.8" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="427.8" y1="111.6" x2="438.2" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <circle cx="464" cy="56" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="464" y="60.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="422" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="422" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="506" cy="100" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="506" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <circle cx="400" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="400" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <circle cx="444" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="444" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <rect x="386" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="399" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <text x="399" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <rect x="412" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="425" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <text x="425" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">1</text>
  <rect x="438" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="451" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <text x="451" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">2</text>
  <rect x="464" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="477" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <text x="477" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">3</text>
  <rect x="490" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="503" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <text x="503" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">4</text>
  <rect x="516" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0" stroke-opacity="0.35" stroke-dasharray="3 3"/>
  <text x="529" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <path d="M 57.0 189 Q 83.0 170 109.0 188" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8" fill="none" marker-end="url(#ad2e)"/>
  <path d="M 57.0 189 Q 96.0 166 135.0 188" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8" fill="none" marker-end="url(#ad2e)"/>
  <path d="M 130 137 C 178 104 158 46 111 52" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3" fill="none" marker-end="url(#ad2e)"/>
  <path d="M 294 54 Q 330 50 328 86" stroke="currentColor" stroke-width="1.2" fill="none" marker-end="url(#swd2e)" marker-start="url(#swd2e)"/>
  <text x="96" y="248" font-size="11" fill="currentColor" text-anchor="middle">children of index i:</text>
  <text x="96" y="263" font-size="11" fill="currentColor" text-anchor="middle">2i+1 and 2i+2 (i = 1: 3, 4)</text>
  <text x="280" y="248" font-size="11" fill="currentColor" text-anchor="middle">5 &gt; 2, the smaller child:</text>
  <text x="280" y="263" font-size="11" fill="currentColor" text-anchor="middle">swap indices 0 and 2</text>
  <text x="464" y="248" font-size="11" fill="currentColor" text-anchor="middle">index 2 has no child:</text>
  <text x="464" y="263" font-size="11" fill="currentColor" text-anchor="middle">2·2+1 = 5 ≥ n = 5, stop</text>
</svg>

The worked-example heap `[1, 3, 2, 7, 4, 5]` as a tree and as the array that stores it; the arcs mark the children of index 1, at $2i+1 = 3$ and $2i+2 = 4$. `heap_pop` removes 1 and moves the last leaf, 5, to the root. 5 is larger than its smaller child, 2, so they swap; at index 2 the first child would be at $2 \cdot 2 + 1 = 5$, past the end of the five-element array, so the sift-down stops with `[2, 3, 5, 7, 4]`.

**Heapify in O(n).** Building a heap by n pushes costs O(n log n). Sifting *down* from the last parent back to the root costs only O(n). The reason is that most nodes are near the bottom: about $n/2^{h+1}$ nodes have height $h$, and sifting a node down costs O(its height), not O(log n). So the total is

$$\sum_{h=0}^{\lfloor \log_2 n\rfloor} \frac{n}{2^{h+1}}\, O(h) \;=\; O\!\left(n \sum_{h \ge 0} \frac{h}{2^{h+1}}\right) \;=\; O(n)$$

since the series $\sum_{h \ge 0} h/2^{h+1}$ sums to exactly 1. To see why, write each $h$ as a sum of $h$ ones, $h = \sum_{j=1}^{h} 1$, and swap the order of summation, which is allowed because every term is non-negative. The inner sum is then the tail of a geometric series ([[02-foundations/engineering-math|0.5 §5]]), $\sum_{h \ge j} 1/2^{h+1} = (1/2^{j+1}) \cdot 2 = 1/2^{j}$, so
$$\sum_{h \ge 0} \frac{h}{2^{h+1}} = \sum_{j \ge 1} \sum_{h \ge j} \frac{1}{2^{h+1}} = \sum_{j \ge 1} \frac{1}{2^{j}} = 1$$
The first five terms, $0 + 1/4 + 2/8 + 3/16 + 4/32 = 0.8125$, already show the approach to 1. Half the nodes are leaves and do no work at all. Sifting *up* from the top does not have this property, because the many deep nodes would each travel a long way.

```python
def heap_push(h, x):
    h.append(x)
    i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] > h[i]:          # sift up
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]
        i = (i - 1) // 2

def sift_down(h, i):
    n = len(h)
    while True:
        smallest, l, r = i, 2 * i + 1, 2 * i + 2
        if l < n and h[l] < h[smallest]:
            smallest = l
        if r < n and h[r] < h[smallest]:
            smallest = r
        if smallest == i:
            return
        h[i], h[smallest] = h[smallest], h[i]
        i = smallest

def heap_pop(h):
    top, last = h[0], h.pop()          # IndexError on empty, like heapq
    if h:
        h[0] = last                    # move the last leaf to the root
        sift_down(h, 0)
    return top

def heapify(h):                        # O(n): sift down from the last parent
    for i in range(len(h) // 2 - 1, -1, -1):
        sift_down(h, i)

h = [9, 4, 7, 1, 8, 2]
heapify(h)
print([heap_pop(h) for _ in range(6)])   # [1, 2, 4, 7, 8, 9]
```

**`heapq` in practice.** `heapq` is a set of functions that act on an ordinary list as a **min-heap**: `heappush`, `heappop`, `heapify` (O(n)), `heapreplace`/`heappushpop`, and `nsmallest`/`nlargest` for top-k. Three idioms come up constantly:

- **Tuples as (priority, tiebreak, item).** Tuples compare element by element, so when two priorities are equal Python compares the items. For dicts or custom objects that raises `TypeError`, and for NumPy arrays it raises `ValueError`. A monotonically increasing counter as the second field breaks ties first-in-first-out and never reaches the item.
- **Max-heap:** push `-priority`. Python 3.14 added public max-heap functions (`heappush_max`, `heappop_max`, `heapify_max`), but interview environments often run older versions, where the negation trick is the portable answer. Do not reach for the private `_heapify_max`.
- **Decrease-key by lazy deletion.** `heapq` cannot find an entry and lower its key. Push a *new* entry with the better key instead, and when an entry is popped whose key is worse than the best known value, skip it as stale. The heap can hold up to one entry per edge relaxation, O(m) entries, so Dijkstra costs O(m log m). Since $m \le n^2$, $\log m \le 2\log n$, and that is the same as O(m log n). This is how nearly all Python Dijkstra and A* code is written ([[02-foundations/algorithms/graph-algorithms|11.6]]).

```python
import heapq, itertools

# 1. Priority first, a counter to break ties, then the payload.
#    Without the counter, equal priorities compare the payloads (dicts -> TypeError).
tie = itertools.count()
pq = []
heapq.heappush(pq, (2.5, next(tie), {"task": "replan"}))
heapq.heappush(pq, (2.5, next(tie), {"task": "log"}))
heapq.heappush(pq, (-1.0, next(tie), {"task": "e-stop"}))   # max-heap: push -priority
print(heapq.heappop(pq)[2])                                   # {'task': 'e-stop'}

# 2. "Decrease-key" by lazy deletion: push a new entry, skip stale ones on pop.
def dijkstra(graph, src):
    dist = {src: 0.0}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                    # stale entry: u was already improved
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))   # the old (d_v, v) stays, now stale
    return dist

g = {"a": [("b", 4), ("c", 1)], "c": [("b", 2)], "b": []}
print(dijkstra(g, "a"))                 # {'a': 0.0, 'b': 3.0, 'c': 1.0}
print(heapq.nsmallest(2, [5, 1, 4, 2])) # [1, 2]
```

**Running median with two heaps.** Keep the smaller half in a max-heap `low` (negated) and the larger half in a min-heap `high`. The invariant is that every element of `low` ≤ every element of `high`, and `len(low)` equals `len(high)` or `len(high) + 1`. Then the median is `-low[0]`, or the average of the two tops when the sizes are equal. Each insertion does a constant number of heap operations, so it costs O(log n), and reading the median is O(1). The same pattern tracks any quantile: size the halves by the quantile instead of equally. A rolling median over a sensor window also needs deletions, so it uses two heaps with lazy deletion or an ordered container.

```python
import heapq

class RunningMedian:
    """Invariant: every item in low <= every item in high,
    and len(low) is len(high) or len(high) + 1."""
    def __init__(self):
        self.low = []   # max-heap of the smaller half, stored negated
        self.high = []  # min-heap of the larger half

    def add(self, x):
        heapq.heappush(self.low, -x)
        heapq.heappush(self.high, -heapq.heappop(self.low))  # fixes the order
        if len(self.high) > len(self.low):                    # fixes the sizes
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2

rm = RunningMedian()
out = []
for x in [5, 15, 1, 3, 8]:
    rm.add(x)
    out.append(rm.median())
print(out)   # [5, 10.0, 5, 4.0, 5]
```

**Top-k of a stream:** keep a *min*-heap of size k holding the k largest items seen so far. A new item replaces the root only if it is larger. This costs O(n log k) time and O(k) memory, and it works on a stream too large to sort.

**C++ note.** `std::priority_queue<T>` is a **max-heap**. Get a min-heap with `std::priority_queue<T, std::vector<T>, std::greater<T>>`. It has no decrease-key either, so use lazy deletion as in Python, or a `std::set<std::pair<dist, node>>` whose entries you erase and re-insert. Heaps are the frontier of every best-first planner. The open list of A* in [[04-robotics/planning-decision-making|Planning & Decision-Making]] is a heap keyed by $f = g + h$.

### 5. Binary search trees

**The idea in one sentence:** a binary tree ordered so that you can discard half of the remaining tree at each step, like binary search, while still allowing inserts and deletes.

**Invariant.** At *every* node, *all* keys in the left subtree are smaller than the node's key, and *all* keys in the right subtree are larger:
$$\text{key}(u) < \text{key}(v) < \text{key}(w) \quad \text{for every node } v, \text{ every } u \text{ in its left subtree}, \text{ every } w \text{ in its right subtree}$$
So one comparison at $v$ rules out a whole subtree, which is what makes search follow a single path. The tree the code below builds from 50, 30, 70, 20, 40, 60, 80 satisfies it: 20, 30 and 40 sit left of 50, and 60, 70 and 80 sit right. Checking only the immediate children is the classic bug in "validate a BST". The tree 5 → left 3 → right 8 passes every parent-child check but is invalid, because 8 sits in 5's left subtree. The correct check passes down an allowed `(low, high)` range.

**Search and insert** walk down one root-to-leaf path, going left if the key is smaller and right if it is larger. Insert attaches a new leaf where the search fell off the tree. Both cost O(h), where $h$ is the height: the number of edges on the longest root-to-leaf path, 0 for a single node.

**Delete** has three cases:

1. **Leaf:** remove it.
2. **One child:** splice the child into the node's place.
3. **Two children:** find the **in-order successor**, the smallest key in the right subtree (go right once, then left as far as possible). Copy its key into the node, then delete the successor from the right subtree. The successor has no left child, since otherwise that child would be smaller, so its deletion is case 1 or 2. Using the successor keeps the order: its key is larger than everything in the left subtree and no larger than anything left in the right subtree. The in-order predecessor works symmetrically.

```python
class Node:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def insert(root, key):                   # returns the (possibly new) subtree root
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:                 # equal keys are ignored
        root.right = insert(root.right, key)
    return root

def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    elif root.left is None or root.right is None:   # cases 1-2: 0 or 1 child
        return root.left or root.right
    else:                                            # case 3: two children
        succ = root.right
        while succ.left:                 # successor = leftmost node of right subtree
            succ = succ.left
        root.key = succ.key
        root.right = delete(root.right, succ.key)    # succ has no left child
    return root

def inorder(node):                       # left, node, right -> sorted keys
    return inorder(node.left) + [node.key] + inorder(node.right) if node else []

root = None
for k in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, k)
root = delete(root, 50)
print(root.key, inorder(root))           # 60 [20, 30, 40, 60, 70, 80]
```

**Traversals,** each O(n) because every node is visited once:

- **In-order** (left, node, right) visits keys in sorted order, which follows directly from the invariant by induction. It answers "k-th smallest" and "is this a valid BST" (the sequence must be strictly increasing).
- **Pre-order** (node, left, right) visits a parent before its subtrees. Re-inserting keys in pre-order rebuilds the same tree, so it is used for serialization and copying. For the tree above after the deletion: `[60, 30, 20, 40, 70, 80]`.
- **Post-order** (left, right, node) finishes both children before their parent. Use it to free memory in C++, or to compute a subtree quantity (height, size, sum) from the children's results. Above: `[20, 40, 30, 80, 70, 60]`.

**Why balance matters.** Every operation costs O(h), and $h$ ranges from $\lfloor\log_2 n\rfloor$ (perfectly balanced) to $n-1$ (a chain). Inserting keys *already in sorted order*, such as timestamps or sequential IDs, produces the chain, and the "tree" becomes a slow linked list. For $n = 10^6$, that is about 20 steps versus a million. Random insertion order gives an average depth near $2\ln n \approx 1.39\log_2 n$, but real data are rarely random. Recursive code on a degenerate tree also exceeds Python's default recursion limit of 1000, so write iterative versions for large or untrusted trees.

**Balanced trees: what they guarantee.** Self-balancing BSTs restore balance with local *rotations* after each insert or delete, and keep the height O(log n) *in the worst case*, so every operation stays O(log n). A red-black tree needs at most three rotations per update (plus recolourings along the path); an AVL deletion may rotate at every level of the path. A **red-black tree** (Guibas & Sedgewick 1978) guarantees height ≤ $2\log_2(n+1)$. An **AVL tree** (Adelson-Velsky & Landis 1962) keeps subtree heights within 1 of each other and guarantees height about ≤ $1.44\log_2 n$. AVL trees are more tightly balanced and faster to search; red-black trees do less restructuring per update. Interviews rarely ask for the rotation cases. They ask what the guarantee is and which library gives it. If you store the subtree size in each node, *select* (the k-th smallest) and *rank* also run in O(log n).

The invariants behind those height bounds:
- **AVL:** at every node $v$ the two subtree heights differ by at most one, with an empty subtree counted as height $-1$:
$$\lvert \text{height}(v.\text{left}) - \text{height}(v.\text{right}) \rvert \le 1$$
  So the fewest nodes an AVL tree of height $h$ can have obeys $N(h) = N(h-1) + N(h-2) + 1$, which gives 1, 2, 4, 7, 12, 20 for $h = 0, \dots, 5$ and grows like the Fibonacci numbers; that exponential growth is where $1.44\log_2 n$ comes from. Non-example: inserting 1, 2, 3 in order gives a chain whose root has subtree heights $-1$ and $1$, a difference of 2.
- **Red-black:** every node is red or black; the root is black; the empty child positions (NIL) count as black; a red node has no red child; and every path from a node down to a NIL passes the same number of black nodes. The last two rules make the longest root-to-NIL path, alternating red and black, at most twice the shortest, all black, so the height is at most $2\log_2(n+1)$, about 40 for $n = 10^6$.
- **Rotation**, the repair both use: lift one child of a node $x$ above $x$ and re-hang that child's inner subtree under $x$. Three pointers change and the in-order sequence does not, so the BST invariant survives. One left rotation at the root turns the chain 1 → 2 → 3 into 2 with children 1 and 3.

**Libraries.** C++ `std::map` / `std::set` are balanced BSTs (red-black in all major implementations), with `lower_bound` / `upper_bound` for floor and ceiling queries and O(log n) insert and erase. Python's standard library has no balanced BST. `bisect` on a sorted `list` gives O(log n) search but O(n) insert. The third-party `sortedcontainers` package (`SortedList`, `SortedDict`) is the usual answer. Internally it is a list of sorted sublists, not a tree, but it provides the same ordered interface with roughly logarithmic cost and fast constants. If an interview environment lacks it, say so and fall back to `bisect` or a heap with lazy deletion.

### 6. Tries for prefix queries

**The idea in one sentence:** store strings as paths from a root, one character per edge, so all strings with a common prefix share one path.

Each node maps a character to a child and marks whether a word ends there. Because a node's children are keyed by distinct characters, each string has at most one path, and membership of a word $w$ in the stored set $S$ is decided by that path together with the end marker:
$$w \in S \iff \text{walk}(\text{root}, w) \text{ exists and carries the end marker}$$
In the code below, after inserting `arm` and `arm_left`, the walk for `arm_` exists but has no marker, so `arm_` is a prefix and not a word. Insert, exact lookup, and "is there a word with this prefix" each cost O(L) for a key of length L, **independent of how many words are stored**. Collecting every word under a prefix costs O(L + size of the output subtree). A hash set also looks up a whole word in O(L) time, because hashing the string reads all of it, but it cannot answer prefix questions without scanning every key.

The cost is memory. Every node is a dict (or a 26-slot array in C++), so a trie of many short words can be several times larger than a set of the same words. Compressed tries (radix trees) merge chains of single-child nodes. Often a **sorted list plus binary search** is enough: all words starting with `p` occupy one contiguous block, found with two `bisect` calls.

Where tries are the right answer: autocomplete; word search on a letter grid, where backtracking abandons a path as soon as its prefix is not in the trie; **longest-prefix matching**, which is how IP routing tables choose a route; and greedy longest-match tokenizers, which match the longest vocabulary entry at each position.

```python
class Trie:
    END = "$"                      # marks "a word ends here"

    def __init__(self):
        self.root = {}             # nested dicts: char -> child node

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node[self.END] = True

    def _walk(self, s):            # node reached by spelling s, or None
        node = self.root
        for ch in s:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def contains(self, word):
        node = self._walk(word)
        return node is not None and self.END in node

    def with_prefix(self, prefix):
        out, start = [], self._walk(prefix)
        stack = [] if start is None else [(start, prefix)]
        while stack:
            node, s = stack.pop()
            for ch, child in node.items():
                if ch == self.END:
                    out.append(s)
                else:
                    stack.append((child, s + ch))
        return sorted(out)

t = Trie()
for w in ["arm", "arm_left", "arm_right", "base", "base_link"]:
    t.insert(w)
print(t.contains("arm_"), t.with_prefix("arm_"))  # False ['arm_left', 'arm_right']
print(t.with_prefix("ba"), t.with_prefix("x"))    # ['base', 'base_link'] []
```

Pitfalls: confusing "prefix exists" with "word exists", since `arm_` is a path but not a word (hence the end marker); using a sentinel key such as `"$"` that can also occur as a real character (use a key that cannot, or a separate node class); and building `s + ch` strings repeatedly on very deep tries, which costs O(L²). For long keys, pass a list of characters and join once.

### 7. Union-find (disjoint-set union)

**The idea in one sentence:** keep each group as a tree of parent pointers whose root names the group. Two items are in the same group exactly when they reach the same root.

- **`find(x)`** follows parent pointers to the root.
- **`union(a, b)`** finds both roots and, if they differ, makes one root the child of the other.

The contract the two operations keep is that `find` returns one canonical representative per set, so after any sequence of unions
$$\text{find}(x) = \text{find}(y) \iff x \text{ and } y \text{ are connected by some chain of unions}$$
The representation invariant behind it: `parent[r] == r` exactly when $r$ is a root, and following `parent` from any element reaches a root, because the pointers form a forest with no cycles. Example with the `DSU` class below: on 4 elements, `union(0, 1)` and `union(2, 3)` make `find(0) == find(1)` and `find(1) != find(2)`; after `union(1, 3)` all four `find` calls return 0.

Deleting an item or splitting a group is not supported. If you must remove edges, process the operations offline in reverse order, so removals become unions, or use a different structure.

**Two optimizations make it fast:**

- **Union by size (or rank):** always hang the *smaller* tree under the larger one. A node's depth increases only when its tree is merged under a tree at least as large, so each such step at least doubles the size of the tree the node belongs to. That can happen at most $\log_2 n$ times, so the height stays ≤ $\log_2 n$ and every operation is O(log n) even without the next trick. Union by *rank* uses an upper bound on height instead of size and gives the same guarantee.
- **Path compression:** during `find`, point every node on the path directly at the root. Later finds on those nodes take one step. *Path halving* (`parent[x] = parent[parent[x]]` while walking up) is a one-pass variant with the same asymptotic benefit.

With both optimizations, any sequence of $m$ operations on $n$ elements takes $O(m\,\alpha(n))$ time (Tarjan 1975). Here $\alpha$ is the inverse Ackermann function, which is at most 4 for any $n$ that could exist in a computer. Precisely, in the form Cormen et al. use: let $A_0(j) = j + 1$, and let $A_k(j)$ apply $A_{k-1}$ to $j$, $j + 1$ times in a row. Then
$$\alpha(n) = \min\{k : A_k(1) \ge n\}$$
Since $A_1(1) = 3$, $A_2(1) = 7$, $A_3(1) = 2047$ and $A_4(1)$ exceeds $2^{2048}$, a 617-digit number, $\alpha(n) \le 4$ for every $n$ below that. So in practice each operation costs a constant amortized amount. Interviews want the statement, not the proof. Pitfall: without union by size or rank, and without path compression, repeatedly linking in a bad order builds a chain, and `find` becomes O(n).

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:          # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                        # already in the same set
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                    # union by size: small under large
        self.size[ra] += self.size[rb]
        return True

def kruskal(n, edges):
    """edges: (weight, u, v). Total weight of a minimum spanning forest."""
    dsu = DSU(n)
    return sum(w for w, u, v in sorted(edges) if dsu.union(u, v))

print(kruskal(4, [(1, 0, 1), (3, 1, 2), (2, 0, 2), (4, 2, 3), (5, 1, 3)]))  # 7
```

**Uses.**

- **Connected components.** For a fixed graph, BFS or DFS also takes O(V + E). Union-find wins when edges *arrive over time* and you must answer "connected yet?" between arrivals, and when you want the answer without building adjacency lists.
- **Cycle detection in an undirected graph:** `union` returning `False` means the edge closes a cycle.
- **Kruskal's minimum spanning tree** (Kruskal 1956): sort the edges by weight and keep an edge exactly when its endpoints lie in different components. That check is the `union` call above. Sorting dominates, so the total is O(E log E). The proof is in [[02-foundations/algorithms/greedy-mst|11.4]].

**Robotics note.** Union-find is how you label *blobs* in an occupancy grid or a segmentation mask: union each occupied cell with its occupied right and down neighbours, then each root is one obstacle. Classic two-pass connected-component labeling in image processing uses the same structure to merge label equivalences. For **point-cloud segmentation**, Euclidean clustering unions every point with each neighbour within a radius $r$, where the neighbours come from a KD-tree or a voxel hash (§8). The sets that result are the clusters, the same answer as region-growing BFS, and you can add points incrementally as scans arrive. Keying the parent map on cell tuples keeps a sparse map cheap:

```python
def cluster_cells(occupied):
    """occupied: set of (row, col). Returns 4-connected clusters as lists."""
    parent = {cell: cell for cell in occupied}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path halving
            x = parent[x]
        return x

    for r, c in occupied:
        for nb in ((r + 1, c), (r, c + 1)):  # each adjacent pair seen once
            if nb in occupied:
                parent[find(nb)] = find((r, c))
    clusters = {}
    for cell in occupied:
        clusters.setdefault(find(cell), []).append(cell)
    return sorted(sorted(c) for c in clusters.values())

cells = {(0, 0), (0, 1), (1, 1), (1, 3), (2, 3), (3, 3), (3, 2), (3, 0)}
for cluster in cluster_cells(cells):
    print(cluster)
# [(0, 0), (0, 1), (1, 1)]
# [(1, 3), (2, 3), (3, 2), (3, 3)]
# [(3, 0)]
```

This short version uses path halving without union by size. That is fine for grid blobs; add the size array if the input could be adversarial.

### 8. Robotics bridge: KD-trees for nearest neighbours

The data-structure question a robotics lab most often asks is not about any of the structures above. It is: "your ICP, normal estimation, or RRT spends all its time in nearest-neighbour search. What would you use?" The standard answer is a **KD-tree** (Bentley 1975): a binary search tree over points in $\mathbb{R}^d$. Each internal node splits space by one coordinate, usually cycling through the axes or picking the widest spread, at the median. That makes the tree balanced, and building it takes O(n log n).

**Invariant.** Each internal node stores a point, a split axis $s$, and a split value $t$ equal to that point's $s$-th coordinate. Every point $p$ below it satisfies
$$p_s < t \text{ for } p \text{ in the left subtree}, \qquad p_s \ge t \text{ for } p \text{ in the right subtree}$$
so the plane $x_s = t$ separates the regions of the two subtrees, which is what lets a query skip one side.

**What a query does.** Descend to the leaf region that contains the query and keep the closest point found so far, at distance $r$. Then backtrack, and visit the *other* side of a split only if the splitting plane is closer to the query than $r$, because otherwise no point there can beat the current best. In low dimensions most subtrees are pruned, and for well-behaved data the *expected* query cost is O(log n) (Friedman, Bentley & Finkel 1977). The worst case is still O(n). Radius search and k-nearest search use the same pruning. Written as a test, the far side of a node is visited only when
$$\lvert q_s - t \rvert < r$$
because every point $p$ on the far side has $\lVert q - p \rVert \ge \lvert q_s - p_s \rvert \ge \lvert q_s - t \rvert$, so if that plane distance is already at least $r$ nothing there can be closer.

> [!example] Worked example · 계산 예제
> Points $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)$, split at the median on $x$ at the root and on $y$ one level down: root $(7,2)$; left child $(5,4)$ with children $(2,3)$ and $(4,7)$; right child $(9,6)$ with left child $(8,1)$. Query $q = (9,1)$.
> The root is at distance $\sqrt{5} = 2.236$, so $r = 2.236$; $q_x = 9 \ge 7$, go right. $(9,6)$ is at distance 5; $q_y = 1 < 6$, go left. $(8,1)$ is at distance 1, so $r = 1$. Back at $(9,6)$ the far side is empty. Back at the root, $\lvert 9 - 7 \rvert = 2 \ge r = 1$, so the whole left subtree is pruned and $(5,4)$, $(2,3)$, $(4,7)$ are never measured.
> Three distance computations instead of six, and the answer $(8,1)$ matches brute force. The usual libraries are `scipy.spatial.cKDTree`/`KDTree`, `nanoflann` in C++, and the KD-trees inside PCL and Open3D.

<svg viewBox="0 0 560 280" style="max-width:100%;height:auto" role="img" aria-label="KD-tree on six points, split at x = 7, then y = 4 on the left and y = 6 on the right. The query q = (9, 1) measures (7,2), (9,6), (8,1); since |9 − 7| = 2 ≥ r = 1, the left half is never searched.">
  <rect x="34" y="44" width="168" height="192" stroke="none" fill="currentColor" fill-opacity="0.07"/>
  <rect x="34" y="44" width="240" height="192" stroke="currentColor" stroke-width="1.0" fill="none" stroke-opacity="0.5"/>
  <text x="34" y="251" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <text x="154" y="251" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <text x="274" y="251" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">10</text>
  <text x="28" y="240" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">0</text>
  <text x="28" y="144" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">4</text>
  <text x="28" y="48" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">8</text>
  <line x1="202" y1="236" x2="202" y2="44" stroke="currentColor" stroke-width="2.0"/>
  <line x1="34" y1="140" x2="202" y2="140" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <line x1="202" y1="92" x2="274" y2="92" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <text x="207" y="58" font-size="11" fill="currentColor" font-weight="bold">x = 7</text>
  <text x="38.8" y="135" font-size="11" fill="currentColor">y = 4</text>
  <text x="207" y="87" font-size="11" fill="currentColor">y = 6</text>
  <circle cx="82" cy="164" r="3.6" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>
  <text x="89" y="168" font-size="11" fill="currentColor" fill-opacity="0.6">(2,3)</text>
  <circle cx="154" cy="140" r="3.6" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>
  <text x="160" y="134" font-size="11" fill="currentColor" fill-opacity="0.6">(5,4)</text>
  <circle cx="250" cy="92" r="3.6" stroke="none" fill="currentColor"/>
  <text x="244" y="106" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="1.0">(9,6)</text>
  <circle cx="130" cy="68" r="3.6" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>
  <text x="137" y="72" font-size="11" fill="currentColor" fill-opacity="0.6">(4,7)</text>
  <circle cx="226" cy="212" r="3.6" stroke="none" fill="currentColor"/>
  <text x="226" y="203" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1.0">(8,1)</text>
  <circle cx="202" cy="188" r="3.6" stroke="none" fill="currentColor"/>
  <text x="196" y="183" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="1.0">(7,2)</text>
  <line x1="245" y1="207" x2="255" y2="217" stroke="currentColor" stroke-width="1.8"/>
  <line x1="245" y1="217" x2="255" y2="207" stroke="currentColor" stroke-width="1.8"/>
  <text x="258" y="207" font-size="12" fill="currentColor" font-weight="bold">q</text>
  <line x1="230" y1="212" x2="244" y2="212" stroke="currentColor" stroke-width="1.0" stroke-dasharray="3 2"/>
  <text x="238" y="228" font-size="11" fill="currentColor" text-anchor="middle">r = 1</text>
  <line x1="202" y1="246" x2="250" y2="246" stroke="currentColor" stroke-width="1.1"/>
  <line x1="202" y1="242" x2="202" y2="250" stroke="currentColor" stroke-width="1.1"/>
  <line x1="250" y1="242" x2="250" y2="250" stroke="currentColor" stroke-width="1.1"/>
  <text x="226" y="263" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">|9 − 7| = 2 ≥ r = 1</text>
  <text x="118" y="204.8" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">pruned: never measured</text>
  <text x="434" y="22" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">the tree; d = distance to q</text>
  <line x1="434" y1="80" x2="366" y2="125" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="434" y1="80" x2="502" y2="118" stroke="currentColor" stroke-width="1.8" stroke-opacity="1.0"/>
  <line x1="366" y1="147" x2="338" y2="199" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="366" y1="147" x2="400" y2="199" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="502" y1="154" x2="468" y2="192" stroke="currentColor" stroke-width="1.8" stroke-opacity="1.0"/>
  <rect x="401" y="44" width="66" height="36" rx="4" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1" stroke-opacity="1.0"/>
  <text x="434" y="60" font-size="11" fill="currentColor" text-anchor="middle">(7,2)</text>
  <text x="434" y="74" font-size="11" fill="currentColor" text-anchor="middle">d = 2.236</text>
  <text x="471" y="52" font-size="11" fill="currentColor" fill-opacity="0.7">x</text>
  <rect x="343" y="125" width="46" height="22" rx="4" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="366" y="140" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.55">(5,4)</text>
  <text x="393" y="133" font-size="11" fill="currentColor" fill-opacity="0.7">y</text>
  <rect x="469" y="118" width="66" height="36" rx="4" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1" stroke-opacity="1.0"/>
  <text x="502" y="134" font-size="11" fill="currentColor" text-anchor="middle">(9,6)</text>
  <text x="502" y="148" font-size="11" fill="currentColor" text-anchor="middle">d = 5</text>
  <text x="539" y="126" font-size="11" fill="currentColor" fill-opacity="0.7">y</text>
  <rect x="315" y="199" width="46" height="22" rx="4" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="338" y="214" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.55">(2,3)</text>
  <rect x="377" y="199" width="46" height="22" rx="4" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="400" y="214" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.55">(4,7)</text>
  <rect x="435" y="192" width="66" height="36" rx="4" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1" stroke-opacity="1.0"/>
  <text x="468" y="208" font-size="11" fill="currentColor" text-anchor="middle">(8,1)</text>
  <text x="468" y="222" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">d = 1</text>
  <text x="384" y="102" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">x &lt; 7</text>
  <text x="484" y="102" font-size="11" fill="currentColor" fill-opacity="0.9">x ≥ 7</text>
  <text x="473" y="176" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.9">y &lt; 6</text>
  <text x="320" y="254" font-size="11" fill="currentColor" fill-opacity="0.6">pruned: never measured</text>
</svg>

The worked example drawn: the root splits at $x = 7$, its children at $y = 4$ (left) and $y = 6$ (right). The query $q = (9, 1)$ measures only the filled points, at distances 2.236, 5 and 1, along the solid path in the tree. Once the best distance is $r = 1$, the plane $x = 7$ lies $\lvert 9 - 7 \rvert = 2 \ge r$ away, so the shaded half holding $(5,4)$, $(2,3)$ and $(4,7)$ is never measured.

**Curse of dimensionality.** Pruning relies on the query ball crossing few splitting planes. As $d$ grows, the ball crosses planes along almost every axis, and the search visits most leaves, approaching a linear scan. A common rule of thumb is that a KD-tree helps only when $n \gg 2^d$. For 3-D point clouds that holds easily. For 50-D or 512-D learned descriptors it fails, so use approximate nearest-neighbour methods (randomized KD-forests, graph-based indexes such as HNSW) and accept a small chance of missing the true nearest point.

**In RRT.** Every iteration asks for the tree node nearest the random sample ([[04-robotics/modern-robotics/ch10-motion-planning|MR Ch. 10]]). With a linear scan, N iterations cost O(N²) in total, and nearest-neighbour search becomes the bottleneck well before collision checking does on simple scenes. A KD-tree reduces this to roughly O(log N) per query. Three caveats a good answer mentions: the planner's tree grows one node at a time, so the KD-tree must support incremental insertion and occasional rebuilds to stay balanced; configuration spaces with angles *wrap around* ($\theta = \pi$ is next to $-\pi$), so a plain Euclidean KD-tree needs a topology-aware metric; and for 7-DoF or higher arms the dimensionality penalty returns, so planners commonly accept approximate neighbours.

**When a hash grid beats a tree.** For fixed-radius queries at a known scale, such as clustering with radius $r$ or voxel downsampling, a voxel hash map with cells of size $r$ answers a query by checking the 27 cells around the query (in 3-D). With bounded point density that takes expected O(1) time, using the hashing of §3. Many mapping pipelines use exactly this structure. See also [[04-robotics/state-estimation-slam|State Estimation & SLAM]] for where these queries sit in a pipeline.

### Self-check

1. A logger stores `(timestamp, message)` pairs that arrive out of order, and it must answer "the first message at or after time t" while inserts continue. Which structure do you use, and why not a heap or a hash map?
2. The sliding-window-maximum code has a `while` loop inside a `for` loop. Why is it O(n) and not O(nk)?
3. You need a Bloom filter for $10^6$ items with a 1 % false-positive rate. How many bits and how many hash functions do you need, and what does the filter answer for an item that was inserted?
4. In Dijkstra with `heapq` and lazy deletion, the heap can hold more entries than there are vertices. Bound its size and show that the running time is still O(m log n).
5. In BST deletion with two children, why does the in-order successor never have a left child, and why does copying its key into the node preserve the BST invariant?
6. With union by size alone, what is the worst-case cost of `find`, and why? What does path compression add? Why can't union-find handle "remove this edge"?
7. A KD-tree nearest-neighbour search over 512-D image embeddings is barely faster than brute force. Explain why and propose a fix.

> [!tip]- Answers
> 1. A balanced BST keyed by timestamp: C++ `std::map::lower_bound`, or `SortedList.bisect_left` from `sortedcontainers` in Python. Both give O(log n) inserts and "smallest key ≥ t". A heap only exposes the minimum, so finding the successor of an arbitrary t costs O(n). A hash map has no order at all. If the messages arrived in order, a plain list with `bisect` would do, because appends at the end are O(1).
> 2. Each index is appended to the deque exactly once and removed at most once, whether from the back by a larger arrival or from the front by aging out. So the inner `while` pops at most n times over the whole run, and total work is O(n) amortized. No single step is O(1) in the worst case, but the sum is.
> 3. $m/n = \log_2(1/p)/\ln 2 = \log_2 100/\ln 2 \approx 9.6$ bits per item, so about 9.6 million bits (1.2 MB), and $k = (m/n)\ln 2 \approx 6.6 \to 7$ hash functions (check: $(1-e^{-7/9.6})^7 \approx 1.0\%$). An inserted item always answers "present", because a Bloom filter has no false negatives.
> 4. Each successful relaxation pushes one entry, and there is at most one per directed edge, plus the source. So the heap holds O(m) entries, and each push or pop costs O(log m). Since $m \le n^2$, $\log m \le 2\log n$, so O(m log m) = O(m log n). Stale entries are popped once each and skipped in O(1).
> 5. The successor is the minimum of the right subtree. If it had a left child, that child would be in the right subtree and smaller, a contradiction. Its key is larger than every key in the node's left subtree, since it came from the right subtree, and smaller than every other key in the right subtree, since it was the minimum. So placing it at the node satisfies the invariant on both sides, and removing it from the right subtree is the easy leaf or one-child case.
> 6. O(log n): a node gets deeper only when its tree merges under one at least as large, which at least doubles its tree's size, so this can happen at most $\log_2 n$ times. Path compression flattens paths as they are used, bringing $m$ operations down to $O(m\,\alpha(n))$, effectively constant per operation. Removing an edge would require splitting a set, but the parent-pointer forest does not record which union connected which elements, so there is nothing to undo. Handle deletions offline in reverse order, or use a dynamic-connectivity structure.
> 7. In 512 dimensions the query ball crosses the splitting planes of nearly every node, so pruning almost never happens and the search visits most leaves. The rule of thumb $n \gg 2^d$ is hopeless at d = 512. Use approximate nearest neighbours (HNSW, IVF-PQ, randomized KD-forests), reduce dimension first (PCA), or, if exact answers are required and n is moderate, a vectorized brute force on a GPU.

### Sources

- Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — hash tables and universal hashing, heaps, binary search trees, red-black trees, disjoint sets.
- Roughgarden, *Algorithms Illuminated*, Part 2 (*Graph Algorithms and Data Structures*, 2018) and Part 3 (*Greedy Algorithms and Dynamic Programming*, 2019), Soundlikeyourself Publishing — heaps, search trees, hashing, Bloom filters, union-find.
- Kulikov & Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018.
- Bloom, B. H. "Space/time trade-offs in hash coding with allowable errors." *Communications of the ACM* 13(7), 1970. doi:10.1145/362686.362692
- Carter, J. L. & Wegman, M. N. "Universal classes of hash functions." *Journal of Computer and System Sciences* 18(2), 1979. doi:10.1016/0022-0000(79)90044-8
- Crosby, S. A. & Wallach, D. S. "Denial of service via algorithmic complexity attacks." *USENIX Security Symposium*, 2003.
- Williams, J. W. J. "Algorithm 232: Heapsort." *Communications of the ACM* 7(6), 1964; Floyd, R. W. "Algorithm 245: Treesort 3." *Communications of the ACM* 7(12), 1964 (linear-time heap construction).
- Adelson-Velsky, G. M. & Landis, E. M. "An algorithm for the organization of information." *Soviet Mathematics Doklady* 3, 1962.
- Guibas, L. J. & Sedgewick, R. "A dichromatic framework for balanced trees." *IEEE Symposium on Foundations of Computer Science (FOCS)*, 1978.
- Fredkin, E. "Trie memory." *Communications of the ACM* 3(9), 1960.
- Tarjan, R. E. "Efficiency of a good but not linear set union algorithm." *Journal of the ACM* 22(2), 1975. doi:10.1145/321879.321884
- Kruskal, J. B. "On the shortest spanning subtree of a graph and the traveling salesman problem." *Proceedings of the American Mathematical Society* 7(1), 1956.
- Bentley, J. L. "Multidimensional binary search trees used for associative searching." *Communications of the ACM* 18(9), 1975. doi:10.1145/361002.361007
- Friedman, J. H., Bentley, J. L. & Finkel, R. A. "An algorithm for finding best matches in logarithmic expected time." *ACM Transactions on Mathematical Software* 3(3), 1977.
- LaValle, S. M. *Planning Algorithms*, Cambridge University Press, 2006 — nearest-neighbour queries in sampling-based planning.

## 한국어

자료구조는 어떤 연산이 싼지에 대한 약속이다. 인터뷰 문제 대부분은 처음 2분 안에 갈린다. 문제가 반복해서 요구하는 연산이 무엇인지 알아채는 순간이다: "키로 찾기", "가장 작은 것 꺼내기", "다음으로 큰 원소", "이 둘이 연결되어 있는가". 이 페이지는 연구 코드와 인터뷰가 실제로 쓰는 자료구조를 모은다. 각각에 대해 연산과 그 비용이 나오는 이유, 짧은 구현, 함정을 정리한다.

인터뷰가 묻는 것: 아래 복잡도 표를 외워서 말하기, 거의 모든 문제에서의 해시 맵·힙 *사용법*, 힙·트라이·union-find의 백지 구현, BST 삭제, 그리고 로봇 연구실이라면 "이 최근접점 탐색은 왜 느린가"(§8).

> [!note] 처음이라면 · First pass
> §1을 읽고 표를 익혀라. §2는 복습이지만 단조 스택과 덱은 처음부터 읽어 둘 만하다. 대부분의 문제에 해시 맵과 힙이 나오므로 그다음 §3, §4를 읽는다. §5–§7은 구현하라고 할 때 쓰는 구조이고, §8은 이 페이지를 포인트 클라우드와 플래너에 연결한다.

### 1. 필요한 연산으로 자료구조 고르기

문제가 반복하는 연산을 적고, 그 모두를 지원하는 **가장 작은** 구조를 고른다. 더 많은 연산을 지원하는 구조는 보통 상수 배나 메모리로 그 값을 치른다. 균형 트리는 힙이 하는 일을 전부 할 수 있지만, 최솟값만 필요하다면 힙이 더 단순하고 빠르다.

**인터페이스, 계약, 불변식.** 이 페이지의 모든 구조에는 두 층이 있고, 정확한 답은 둘 다 말한다.
- 추상 자료형(**abstract data type**)은 인터페이스와 그 계약이다. 어떤 연산이 있고 각 연산이 무엇을 돌려줘야 하는가. 스택의 `pop`은 저장 방식과 상관없이 아직 남아 있는 것 중 가장 최근에 넣은 항목을 돌려줘야 한다.
- 자료구조(**data structure**)는 표현과 불변식(**invariant**)의 쌍이다. 불변식은 저장된 데이터에 대한 조건으로, 모든 연산이 들어올 때 가정해도 되고 돌아가기 전에 반드시 회복시켜야 한다. 비용을 참으로 만드는 것이 불변식이다. 힙의 "부모 ≤ 자식" 규칙이 최솟값이 언제나 인덱스 0에 있는 이유다.

구현할 때는 불변식부터 적어라. 연산이 이상하게 동작하면 불변식이 깨지기 시작하는 줄을 찾아라.

| 구조 | 조회 | 삽입 / 삭제 | 쓰임 | Python | C++ |
|---|---|---|---|---|---|
| 배열(고정 크기) | 인덱스 O(1); 값으로 O(n), 정렬돼 있으면 O(log n) | 원소를 밀어야 하므로 O(n) | 촘촘한 수치 데이터, 캐시 친화적 순회 | `array.array`, NumPy `ndarray` | `std::array`, C 배열 |
| 동적 배열 | 인덱스 O(1) | 끝에서 append / pop 분할상환 O(1); 중간 O(n) | 기본 시퀀스 | `list` | `std::vector` |
| 연결 리스트(이중) | 인덱스 O(n) | 이미 쥔 노드에서 O(1) | 이어 붙이기, 최근 사용 순서(LRU) | 내장 없음; LRU는 `OrderedDict` | `std::list` |
| 스택 | top O(1) | push / pop O(1) | LIFO: DFS, 파싱, 되돌리기, 단조 스택 | `list`의 `append` / `pop` | `std::stack`, `std::vector` |
| 큐 / 덱 | 양 끝 O(1); 중간 O(n) | 양 끝 O(1) | FIFO: BFS, 슬라이딩 윈도 | `collections.deque` | `std::queue`, `std::deque` |
| 해시 맵 / 셋 | 키로 기대 O(1), 최악 O(n) | 기대 O(1)(리사이즈 포함 분할상환) | 소속 검사, 세기, 메모이제이션, 묶기 | `dict`, `set`, `Counter`, `defaultdict` | `std::unordered_map`, `std::unordered_set` |
| 이진 힙 | 최솟값 O(1); 다른 키 O(n) | push / pop O(log n); 구축 O(n) | 반복되는 최솟값: Dijkstra, A*, top-k, 이벤트 큐 | `heapq`(리스트 위의 최소 힙) | `std::priority_queue`(최대 힙) |
| 균형 BST | 키, 최소 / 최대, 선행자 / 후속자 O(log n) | O(log n) | 순서 있는 키, 범위 질의, floor / ceiling | 표준 라이브러리에 없음; `sortedcontainers`(서드파티) | `std::map`, `std::set` |
| 트라이 | 단어나 접두사 O(L), L = 키 길이 | O(L) | 접두사 질의, 자동완성, 최장 접두사 일치 | 중첩 `dict` | 없음; 직접 구현 |
| Union-find | find 분할상환 O(α(n)), 실제로 α(n) ≤ 4라서 사실상 상수(§7) | union 분할상환 O(α(n)); 삭제 없음 | 점진적 연결성, Kruskal, 군집화 | 없음; 약 20줄 | 표준에 없음(Boost `disjoint_sets`) |

빨리 고르는 법:

- **"x가 있는가?"나 "키 x의 값"만** 필요하면 해시 셋 / 해시 맵.
- **"지금 가장 작은(큰) 것"만** 필요하면 힙.
- **순서가 중요하면**("x 이상인 가장 작은 키", 범위, 삽입하면서 정렬 순회) 균형 BST. 삽입이 드물면 정렬 리스트.
- **그룹이 합쳐지는 동안 "이 둘이 같은 그룹인가?"를** 물으면 union-find.
- **문자열 접두사는** 트라이, 또는 정렬 리스트와 이진 탐색([[02-foundations/algorithms/sorting-divide-conquer|11.3 §6]]).
- **저차원 공간의 최근접점은** KD-tree(좌표 하나씩 공간을 나누는 이진 트리)나 복셀 해시(정수 격자 셀을 키로 쓰는 해시 맵). 둘 다 §8에 있다.

거의 모든 코드 리뷰에서 나오는 Python 함정 두 가지가 있다. `list.pop(0)`과 `list.insert(0, x)`는 O(n)이므로 `deque`를 쓴다. `x in some_list`는 O(n)이므로 루프 안에서 소속을 검사할 때는 `set`으로 바꾼다.

### 2. 배열, 연결 리스트, 스택, 큐, 덱

**배열은** 원소를 연속된 한 블록에 저장하므로, 원소 $i$의 주소가 `base + i * size`다. 원소당 바이트 수를 $s$라 하면 주소는 곱셈 한 번과 덧셈 한 번이면 나오므로 모든 $i$에서 비용이 같다:
$$\text{addr}(i) = \text{base} + i \cdot s, \qquad 0 \le i < n$$
주소 1000에서 시작하는 8바이트 double이라면 원소 5는 $1000 + 5 \cdot 8 = 1040$에 있다. 범위 $0 \le i < n$도 계약의 일부다. C++ `operator[]`는 이를 검사하지 않으므로 인덱스 $n$을 읽으면 그 뒤에 있는 아무 메모리나 돌려준다. 인덱싱이 O(1)인 이유이고, 실제 하드웨어에서 순차 순회가 빠른 이유이기도 하다. CPU 캐시가 다음 원소들을 미리 올려 두기 때문이다. 중간에 삽입하면 뒤의 원소를 모두 밀어야 하므로 O(n)이 든다.

**동적 배열**(`list`, `std::vector`)은 여유 용량을 둔다. 꽉 차면 보통 기존의 1.5배나 2배 크기로 새로 할당하고 전부 복사한다. append 한 번이 O(n)일 수는 있지만, n번의 append 전체 비용은 O(n)이다. 두 배로 늘리면 복사 비용이 합쳐서 $1 + 2 + 4 + \dots + n < 2n$이므로 append 한 번은 분할상환 O(1)이다(회계 논증과 불변식 $0 \le \text{size} \le \text{capacity}$는 [[02-foundations/algorithms/complexity-recursion|11.1 §4]]). 성장은 반드시 *기하급수적*이어야 한다. 고정된 +100칸씩 늘리면 n번 append가 O(n²)이 된다. C++ 함정: 재할당이 일어나면 벡터를 가리키던 포인터·참조·반복자가 전부 무효가 된다.

**연결 리스트는** 원소마다 노드를 따로 두고 다음(이중이면 이전도) 노드를 가리킨다. 노드를 쥐고 있으면 그 옆에 넣고 빼는 것은 포인터만 바꾸므로 O(1)이다. 리스트 자체는 `head` 포인터(이중이면 `tail`도)를 든다. 이중 연결 리스트는 두 방향이 일치한다는 불변식을 지킨다. 후속 노드가 있는 모든 노드 `u`에 대해 `u.next.prev is u`이고, `head.prev`와 `tail.next`는 비어 있다. `next`만 고치고 `prev`를 잊은 이어 붙이기는 앞으로 순회할 때와 뒤로 순회할 때 서로 다른 리스트가 보이게 만든다. 하지만 $i$번째 원소까지 가는 데 O(n)이 들고, 한 칸 건널 때마다 캐시 미스가 나기 쉽다. 실무에서 연결 리스트가 이기는 경우는 이미 쥔 노드에서 이어 붙일 때뿐이다. 대표 예가 LRU 캐시다. 키에서 리스트 노드로 가는 해시 맵과 최근 사용 순서로 유지되는 이중 연결 리스트를 함께 쓰면 `get`과 `put`이 O(1)이다. Python에서는 `OrderedDict.move_to_end`가 정확히 이 일을 한다. 인터뷰 단골은 포인터 세 개로 리스트를 제자리에서 뒤집기, 그리고 중간 찾기나 사이클 검출에 쓰는 fast/slow 두 포인터 기법이다.

**스택**(LIFO)과 **큐**(FIFO)는 저장 방식이 아니라 접근 규칙이다. 스택의 계약은 `pop`이 남아 있는 것 중 가장 최근에 넣은 항목을 돌려준다는 것이다(후입선출). 한 줄로 쓰면, 넣고 바로 꺼내면 넣은 항목과 손대지 않은 스택이 돌아온다는 뜻이다:
$$\text{pop}(\text{push}(S, x)) = (S,\ x)$$
큐의 계약은 `popleft`가 남아 있는 것 중 가장 먼저 넣은 항목을 돌려준다는 것이다(선입선출). 1, 2, 3을 넣고 세 번 꺼내면 스택은 3, 2, 1을, 큐는 1, 2, 3을 준다. 덱(double-ended queue)은 양 끝 모두에서 넣고 뺄 수 있으므로 어느 쪽으로도 쓸 수 있다. 스택은 `append`와 `pop`으로만 쓰는 `list`다. 큐는 `collections.deque`를 써야 한다. 고정 크기 블록의 연결 리스트로 되어 있어 양 끝이 O(1)이다. 덱의 중간 인덱싱은 O(n)이다. 스택은 DFS, 수식 파싱, "되돌리기"를 움직이고, 큐는 BFS([[02-foundations/algorithms/graph-algorithms|11.6]])를 움직인다.

**단조 스택 / 덱 패턴.** 많은 문제가 원소마다 가장 가까운 더 큰(작은) 원소를 묻거나 움직이는 윈도의 최댓값을 묻는다. 순진한 답은 매번 다시 훑어서 O(nk)나 O(n²)이 든다. 핵심은 **아직 답이 될 수 있는 후보만 정렬된 상태로 남기고, 나머지는 영원히 버리는 것이다.**

슬라이딩 윈도 최댓값에서는 앞에서 뒤로 값이 엄격히 감소하는 인덱스 덱을 유지한다. 새 값 $x$가 오면 값이 $x$ 이하인 인덱스를 뒤에서 모두 꺼낸다. 그 원소들은 $x$보다 오래되었고 크지도 않다. 그러니 $x$가 윈도에 있는 동안 최댓값이 될 수 없고, $x$보다 먼저 윈도를 떠난다. 그다음 맨 앞 인덱스가 윈도 밖으로 밀려났으면 꺼낸다. 이제 맨 앞이 최댓값이다.

- *불변식:* 덱에는 현재 윈도의 인덱스 중 뒤에 오는 같거나 큰 원소에 가려지지 않은 것만, 값의 내림차순으로 들어 있다.
- *복잡도:* 안쪽에 `while`이 있어도 전체 O(n)이다. 각 인덱스가 한 번 들어가고 많아야 한 번 나오기 때문이다. 면접관이 듣고 싶어 하는 것이 바로 이 분할상환 논증이다.

```python
from collections import deque

def sliding_window_max(nums, k):
    """Max of every length-k window in O(n)."""
    dq = deque()          # indices; their values strictly decrease front to back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()      # a smaller older value can never be a max again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()  # front index has slid out of the window
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

def next_greater(nums):
    """For each i, the first value to its right that is larger (or None)."""
    ans = [None] * len(nums)
    stack = []            # indices still waiting; their values decrease
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        stack.append(i)
    return ans

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]
print(next_greater([2, 1, 5, 3, 4]))                     # [5, 5, None, 4, None]
```

> [!example] 계산 예제 · Worked example
> `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`. 덱은 값으로 적는다.
> i=0: [1]. i=1: 3이 1을 꺼냄 → [3]. i=2: [3, −1], 윈도가 참 → 3. i=3: [3, −1, −3] → 3. i=4: 5가 셋을 모두 꺼냄 → [5] → 5. i=5: [5, 3] → 5. i=6: 6이 3과 5를 꺼냄 → [6] → 6. i=7: 7이 6을 꺼냄 → [7] → 7.
> 여덟 번 넣고 일곱 번 꺼냈다. 분할상환 논증이 약속한 대로 선형 작업이다.

함정: 인덱스 대신 값을 저장하는 것(그러면 맨 앞이 윈도를 떠났는지 알 수 없다), `<=`가 필요한 곳에 `<`를 쓰거나 그 반대로 써서 동점 처리가 달라지는 것, 첫 윈도가 찬 뒤에만 출력해야 한다는 것을 잊는 것. 같은 덱으로 최근 k개 샘플에 대한 힘 신호의 이동 최댓값을 구할 수 있고, 이동 최솟값은 잡음 낀 거리 측정의 하한 포락선이 된다. 둘 다 윈도 길이와 무관하게 샘플당 분할상환 O(1)이다.

### 3. 해시 테이블

**한 문장 요지:** 해시 함수로 키를 배열 인덱스로 바꿔서, 조회가 키가 있어야 할 자리로 바로 뛰어가게 한다.

**해시 함수.** 해시 함수는 키를 정수로 바꾸고, 테이블은 버킷 수 $m$에 대해 `h(key) % m`으로 버킷을 정한다. *결정적*이어야 하고(같은 키는 같은 해시), 현실의 키를 고르게 *퍼뜨려야* 한다. 나쁜 해시는 데이터의 규칙성을 그대로 남긴다. 예를 들어 8의 배수인 메모리 주소를 `addr % 1000`으로 나누면 버킷 대부분이 쓰이지 않는다.

가능한 키 전체의 집합 $U$에서 버킷 인덱스로 가는 사상 하나로 쓰면, 요구 조건과 바람은 다음과 같다:
$$h: U \to \{0, 1, \dots, m-1\}, \qquad x = y \implies h(x) = h(y)$$
함의는 *요구 조건*이다. 조회는 $h$를 다시 계산하므로 삽입이 쓴 버킷에 도착해야 하기 때문이다. 퍼뜨리기는 *바람*이고, 실제 키가 버킷을 얼마나 고르게 채우는지로 잰다. $h(k) = k \bmod 10$이면 키 42와 17은 버킷 2와 7로 가고, 52는 버킷 2에서 42와 충돌한다.

**충돌은 피할 수 없다.** 가능한 키는 많고 버킷은 적기 때문이다. 표준 해법은 두 가지다:

- **분리 체이닝:** 버킷마다 작은 리스트를 두고, 연산은 버킷 `h(k)`의 리스트를 훑는다. 삭제가 쉽다. `std::unordered_map`이 이 방식이다.
- **개방 주소법:** 칸마다 키 하나. 충돌하면 빈칸이 나올 때까지 *탐사 순서*를 따른다(선형 탐사는 다음 칸, 그다음 칸…). 캐시에 유리하고 노드 할당이 없다. 대신 삭제에는 *묘비(tombstone)* 표시가 필요하다. 칸을 그냥 비우면 그 뒤에 저장된 키의 탐사 사슬이 끊기기 때문이다. 또 테이블이 찰수록 성능이 급격히 무너진다. CPython `dict`는 의사난수 탐사 순서를 쓰는 개방 주소법이다.

**각 방식이 지키는 불변식.** 체이닝에서는 저장된 모든 키 $k$가 버킷 $h(k)$의 리스트에 있으므로, 그 리스트만 훑는 조회가 옳다. 개방 주소법에서는 키 $k$가 자기 탐사 순서의 어느 위치에 있고(선형 탐사라면 아래 식), 그 순서의 앞선 위치는 모두 차 있거나 묘비가 있다. 그래서 조회는 처음 만나는 진짜 빈칸에서 멈춰도 된다:
$$s_i(k) = (h(k) + i) \bmod m, \qquad i = 0, 1, 2, \dots$$
$m = 10$인 예: 42를 넣으면 칸 2에 들어가고, 52는 칸 2를 탐사해 차 있음을 보고 칸 3에 들어간다. 42를 지우려고 칸 2를 비우면 이후 52의 조회가 칸 2에서 멈춰 "없음"이라고 답한다. 삭제가 묘비를 남기는 이유가 정확히 이것이다.

<svg viewBox="0 0 560 272" style="max-width:100%;height:auto" role="img" aria-label="h(k) = k mod 10, 키 42, 17, 52인 해시 테이블. 체이닝은 42와 52를 버킷 2의 한 리스트에 두고, 선형 탐사는 52를 칸 3으로 보낸다. 42를 지우면 묘비가 남아 52의 조회가 여전히 칸 3에 닿는다.">
  <defs><marker id="ad1k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="20" y="22" font-size="12" fill="currentColor" font-weight="bold">분리 체이닝</text>
  <text x="31" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">0</text>
  <rect x="20" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="53" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">1</text>
  <rect x="42" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="75" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">2</text>
  <rect x="64" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <circle cx="75" cy="66" r="2.6" stroke="none" fill="currentColor"/>
  <line x1="75" y1="66" x2="75" y2="99" stroke="currentColor" stroke-width="1.1" marker-end="url(#ad1k)"/>
  <rect x="59" y="100" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text x="75" y="116.5" font-size="12" fill="currentColor" text-anchor="middle">42</text>
  <line x1="75" y1="124" x2="75" y2="145" stroke="currentColor" stroke-width="1.1" marker-end="url(#ad1k)"/>
  <rect x="59" y="146" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text x="75" y="162.5" font-size="12" fill="currentColor" text-anchor="middle">52</text>
  <text x="97" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">3</text>
  <rect x="86" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="119" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">4</text>
  <rect x="108" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="141" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">5</text>
  <rect x="130" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="163" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">6</text>
  <rect x="152" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="185" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">7</text>
  <rect x="174" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <circle cx="185" cy="66" r="2.6" stroke="none" fill="currentColor"/>
  <line x1="185" y1="66" x2="185" y2="99" stroke="currentColor" stroke-width="1.1" marker-end="url(#ad1k)"/>
  <rect x="169" y="100" width="32" height="24" rx="3" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text x="185" y="116.5" font-size="12" fill="currentColor" text-anchor="middle">17</text>
  <text x="207" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">8</text>
  <rect x="196" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="229" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">9</text>
  <rect x="218" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="308" y="22" font-size="12" fill="currentColor" font-weight="bold">개방 주소법, 선형 탐사</text>
  <text x="319" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">0</text>
  <rect x="308" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="341" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">1</text>
  <rect x="330" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="363" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">2</text>
  <rect x="352" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="353.5" y="55.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="363" y="70.5" font-size="11" fill="currentColor" text-anchor="middle">42</text>
  <text x="385" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">3</text>
  <rect x="374" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="375.5" y="55.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="385" y="70.5" font-size="11" fill="currentColor" text-anchor="middle">52</text>
  <text x="407" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">4</text>
  <rect x="396" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="429" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">5</text>
  <rect x="418" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="451" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">6</text>
  <rect x="440" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="473" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">7</text>
  <rect x="462" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="463.5" y="55.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="473" y="70.5" font-size="11" fill="currentColor" text-anchor="middle">17</text>
  <text x="495" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">8</text>
  <rect x="484" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="517" y="48" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">9</text>
  <rect x="506" y="54" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="319" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">0</text>
  <rect x="308" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="341" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">1</text>
  <rect x="330" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="363" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">2</text>
  <rect x="352" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <line x1="357" y1="171" x2="369" y2="185" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"/>
  <line x1="369" y1="171" x2="357" y2="185" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"/>
  <text x="385" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">3</text>
  <rect x="374" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="375.5" y="167.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="385" y="182.5" font-size="11" fill="currentColor" text-anchor="middle">52</text>
  <text x="407" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">4</text>
  <rect x="396" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="429" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">5</text>
  <rect x="418" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="451" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">6</text>
  <rect x="440" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="473" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">7</text>
  <rect x="462" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <rect x="463.5" y="167.5" width="19" height="21" stroke="none" fill="currentColor" fill-opacity="0.12"/>
  <text x="473" y="182.5" font-size="11" fill="currentColor" text-anchor="middle">17</text>
  <text x="495" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">8</text>
  <rect x="484" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <text x="517" y="160" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.65">9</text>
  <rect x="506" y="166" width="22" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04"/>
  <path d="M 363.0 80 Q 374.0 94 385.0 81" stroke="currentColor" stroke-width="1.1" fill="none" marker-end="url(#ad1k)"/>
  <text x="308" y="108" font-size="11" fill="currentColor">52: 칸 2가 차 있어 칸 3으로</text>
  <text x="308" y="138" font-size="11" fill="currentColor" fill-opacity="0.9">42를 지운 뒤: 칸 2에 묘비</text>
  <path d="M 363.0 192 Q 374.0 206 385.0 193" stroke="currentColor" stroke-width="1.1" fill="none" marker-end="url(#ad1k)"/>
  <text x="308" y="220" font-size="11" fill="currentColor">52 조회: 묘비면 계속 → 칸 3에서 찾음</text>
  <line x1="12" y1="240" x2="548" y2="240" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
  <text x="280" y="260" font-size="12" fill="currentColor" text-anchor="middle">h(k) = k mod 10, 키를 넣은 순서는 42, 17, 52</text>
</svg>

키 42, 17, 52를 이 순서로 $h(k) = k \bmod 10$에 넣은 그림이다. 체이닝에서는 42와 52가 버킷 2의 리스트를 함께 쓰고 17은 버킷 7에 혼자 있다. 선형 탐사에서는 52가 칸 2가 차 있음을 보고 칸 3에 들어간다. 42를 지운 뒤에도 칸 2에는 묘비가 남으므로, 52의 조회는 빈 칸 2에서 멈추지 않고 그곳을 지나 칸 3에 닿는다.

**적재율과 리사이즈.** 적재율은 버킷당 저장된 키 수다.
$$\alpha = \frac{n}{m}$$
$n$은 키 수, $m$은 버킷 수다. 그래서 체이닝에서는 1을 넘을 수 있지만, 개방 주소법에서는 칸마다 키가 하나이므로 1 미만이어야 한다. 체이닝에서 조회는 기대 길이 약 $\alpha$인 리스트를 훑는다. 개방 주소법에서는 이상화된 균일 탐사 가정 아래 실패하는 탐색이 약 $1/(1-\alpha)$번 탐사한다. $\alpha = 0.9$면 10번이다. 선형 탐사는 차 있는 칸이 뭉치므로 더 나쁘다. 차 있는 칸들의 연속 구간 어디에 해시되든 키는 그 구간 끝에 놓여 구간을 한 칸 늘리므로, 긴 구간일수록 더 빨리 자라고 탐색은 구간 전체를 걸어야 한다. Knuth의 분석으로는 $\alpha = 0.9$에서 약 $\tfrac12\bigl(1 + 1/(1-\alpha)^2\bigr) \approx 50$번이다. 그래서 구현들은 $\alpha$를 묶어 둔다. Java `HashMap`은 0.75, CPython `dict`는 약 2/3, `std::unordered_map`은 `max_load_factor()`(기본 1.0)를 넘으면 리사이즈한다. 리사이즈는 $m$을 두 배로 하고 **모든 키를 다시 넣는다.** $m$이 바뀌면 `h(k) % m`이 바뀌므로 옛 배열을 그냥 복사할 수 없다. 테이블이 두 배씩 커지므로 동적 배열과 같은 논리로 리사이즈 비용은 삽입당 O(1)로 평균된다.

**"기대 O(1)"에 좋은 해시가 필요한 이유 — 범용 해싱.** *고정된* 해시 함수에는 반드시 나쁜 입력이 있다. 비둘기집 원리에 따라 어떤 버킷에는 전체 키 공간 $U$의 키가 적어도 $\lvert U\rvert/m$개 몰린다. 입력을 그 키들로만 고르면 모두 한 사슬에 들어가 모든 연산이 O(n)이 된다. 해법은 *데이터*가 무작위이기를 바라는 대신 *함수*를 무작위로 고르는 것이다.

> [!note] 정의 · Definition
> 해시 함수족 $H$가 **범용(universal)이라는** 것은, 서로 다른 모든 키 쌍 $x \ne y$에 대해 $H$에서 무작위로 뽑은 함수로 두 키가 충돌할 확률이 $1/m$ 이하라는 뜻이다(Carter & Wegman 1979). 키가 먼저 고정되므로 확률은 $h$를 무작위로 고르는 것에 대한 것이다:
> $$\Pr_{h \in H}\left[h(x) = h(y)\right] \le \frac{1}{m} \quad \text{for all } x \ne y$$

이것으로 충분한 이유: 저장된 키 $k_1, \dots, k_n$의 집합을 *아무것이나* 고정하고, 저장되지 않은 키 $x$를 하나 잡자. $x$를 찾다 실패하는 조회가 훑는 사슬에는 $x$와 충돌하는 저장 키가 정확히 들어 있으므로, 그 길이 $L$은 개수이고, 개수는 지시 변수(**indicator variable**)의 합이다. 지시 변수는 0과 1만 값으로 갖는 확률변수로, 그 사건이 일어나면 1, 일어나지 않으면 0이다. 그래서 기댓값은 그 사건의 확률이다: $E[X] = 1 \cdot \Pr[\text{사건}] + 0 \cdot \Pr[\text{사건 아님}]$. 여기서는 저장된 키마다 하나씩 둔다:
$$X_j = \begin{cases} 1 & h(k_j) = h(x) \\ 0 & \text{otherwise} \end{cases}, \qquad L = \sum_{j=1}^{n} X_j, \qquad E[L] = \sum_{j=1}^{n} \Pr[h(k_j) = h(x)] \le \frac{n}{m} = \alpha$$
가운데 등호는 기댓값의 선형성([[02-foundations/probability|3. 확률 §2]])이고, $X_j$들 사이의 독립은 필요 없다. 마지막 단계는 각 쌍 $k_j \ne x$에 범용 상한을 적용한 것이다. 저장된 키가 $n = 6$개, 버킷이 $m = 8$개이면 각 $X_j$의 기댓값은 $1/8$ 이하이므로 사슬의 기대 길이는 $6/8 = 0.75$ 이하다. 반례: $L$ 자체는 2 이상이 될 수 있으므로 지시 변수가 아니다. 이 기법의 요점은 $L$의 분포를 몰라도 되고 확률 $n$개만 알면 된다는 것이다. 같은 기법이 [[02-foundations/algorithms/sorting-divide-conquer|11.3 §3]]에서 무작위 퀵정렬의 비교 횟수를 센다. 따라서 연산은 기대 O(1 + α)이고, 기댓값은 데이터가 아니라 함수를 고르는 무작위성에 대한 것이다.

고전적인 범용 함수족은 $h_{a,b}(x) = ((ax+b) \bmod p) \bmod m$이다. 여기서 $p$는 모든 키보다 큰 소수이고, $a \ne 0$과 $b$를 무작위로 고른다. $p = 7$, $m = 3$, 키 $0$~$6$에 대해 전수로 확인하면($a$와 $b$의 선택 $6 \times 7 = 42$가지 전부), 가장 나쁜 서로 다른 키 쌍도 42개 함수 중 10개에서만 충돌하므로 확률 $0.238 \le 1/3$이다. 반례: 함수 하나 $h(x) = x \bmod 3$은 원소가 하나뿐인 함수족이고, 키 0, 3, 6, 9는 여기서 확률 1로 충돌한다. Python이 문자열 해시를 프로세스마다 무작위화하는 것(SipHash, `PYTHONHASHSEED`)도 같은 원리다.

**적대적 최악의 경우.** Crosby & Wallach(2003)는 알려진 고정 해시에서 충돌하도록 만든 키를 보내 실제 서버를 멈출 수 있음을 보였다. 방어법은 키가 있거나 무작위화된 해시, 또는 최악의 경우를 보장하는 구조다(Java `HashMap`은 긴 사슬을 균형 트리로 바꾼다). CPython에서 `int` 해시는 무작위화되지 *않으므로*(작은 `n`에서 `hash(n) == n`), 악의적인 정수 키 집합은 여전히 `dict`를 느리게 만들 수 있다. 로봇 코드에서는 거의 문제가 되지 않지만, "dict 조회는 언제나 O(1)인가?"에 대한 완전한 답은 이렇다: 기대 O(1), 최악 O(n).

**Python의 해시 가능성.** 키는 *해시 가능*해야 한다. 살아 있는 동안 `__hash__`가 바뀌지 않고, 같은 객체는 같은 해시를 가져야 한다. 둘째 조건은 위의 해시 함수 요구 조건을 Python 객체에 대해 쓴 것이다:
$$a == b \implies \text{hash}(a) == \text{hash}(b)$$
첫째 조건이 중요한 이유는 테이블이 삽입 시점의 해시로 키의 버킷을 골랐기 때문이다. 그래서 나중에 해시가 바뀐 키는 엉뚱한 버킷에서 찾게 된다. 가변 컨테이너(`list`, `dict`, `set`)는 해시 불가능하다. `tuple`은 내용물이 해시 가능하면 해시 가능하고, `frozenset`이 해시 가능한 집합이다. `@dataclass(frozen=True)`는 필드 기반 해시를 얻는다. 사람들이 걸리는 함정이 두 가지 있다. 첫째, `1`, `1.0`, `True`는 서로 같고 해시도 같으므로 *같은 키*다. 둘째, `0.1 + 0.2 != 0.3`이므로 부동소수점 좌표는 최악의 키다. 격자 지도와 복셀 필터에서는 좌표를 먼저 정수 셀 인덱스로 양자화한다. NumPy 배열은 해시 불가능하므로 `tuple(a)`나 `a.tobytes()`를 쓴다.

```python
from dataclasses import dataclass

seen = {}
try:
    key = [1, 2]
    seen[key] = "x"                    # lists are mutable -> unhashable
except TypeError as e:
    print("TypeError:", e)
seen[(1, 2)] = "tuple ok"              # tuples of hashables are hashable
seen[frozenset({"a", "b"})] = "frozenset ok"

d = {1: "int"}
d[True] = "bool"                       # True == 1 and hash(True) == hash(1)
print(d)                               # {1: 'bool'}  -- one key, not two

@dataclass(frozen=True)                # frozen dataclass gets __hash__ from its fields
class Cell:
    ix: int
    iy: int

def voxel_key(x, y, res=0.25):         # key on integer cells, not raw floats
    return Cell(int(x // res), int(y // res))   # // floors, so negatives bin correctly

print((0.1 + 0.2) in {0.3})                         # False: 0.30000000000000004
grid = {voxel_key(0.1 + 0.2, 1.0): "hit"}
print(voxel_key(0.3, 1.0) in grid, voxel_key(-0.1, 0.0))  # True Cell(ix=-1, iy=0)
```

셀 경계에 거의 정확히 걸친 점은 이웃한 두 셀 중 어느 쪽에나 들어갈 수 있다. 그래서 복셀 해시로 반경 질의를 할 때는 인접 셀도 확인해야 한다.

최소한의 체이닝 테이블을 보면 비용이 어디서 오는지 알 수 있다:

```python
class ChainedHashMap:
    """Separate chaining; doubles the bucket array when load factor > 0.75."""
    def __init__(self, capacity=8):
        self.buckets = [list() for _ in range(capacity)]
        self.size = 0

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)       # overwrite, do not duplicate
                return
        b.append((key, value))
        self.size += 1
        if self.size > 0.75 * len(self.buckets):
            old = self.buckets             # every key must be re-bucketed,
            self.buckets = [list() for _ in range(2 * len(old))]  # since % changed
            for pair in (p for bucket in old for p in bucket):
                self._bucket(pair[0]).append(pair)

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

m = ChainedHashMap()
for i in range(100):
    m.put(f"cell{i}", i)
print(m.get("cell42"), m.size, len(m.buckets))  # 42 100 256
```

해시 맵 위에 선 인터뷰 패턴: two-sum(본 값을 저장하고 `target - x`를 조회), `Counter`로 세기, `defaultdict(list)`로 묶기(애너그램은 `tuple(sorted(word))`를 키로), 그래프 탐색의 방문 집합, 메모이제이션([[02-foundations/algorithms/dynamic-programming|11.5]]). C++ 함정: `m[key]`는 키가 없으면 기본값을 *삽입한다*. 소속 검사에는 `find`나 `contains`(C++20)를 쓴다.

#### 블룸 필터

블룸 필터(Bloom 1970)는 "x를 본 적이 있는가?"에 작은 고정 비트 수로 답한다. 틀리게 *예*라고 할 수는 있지만(거짓 양성), 틀리게 *아니오*라고 하지는 않는다. $m$비트 배열과 해시 함수 $k$개를 쓴다. 삽입할 때는 비트 $h_1(x),\dots,h_k(x)$를 켠다. 질의할 때는 $k$개가 모두 켜져 있을 때만 "있음"이라고 답한다. 삽입한 원소의 비트는 항상 켜져 있으므로 거짓 음성이 없다. 키를 저장하지 않고 삭제도 할 수 없다(비트를 끄면 다른 원소가 지워질 수 있다). $n$개를 넣은 뒤 특정 비트가 여전히 0일 확률은 $(1-1/m)^{kn} \approx e^{-kn/m}$이므로, 없는 원소의 $k$개 비트가 모두 켜져 있을 확률은 다음과 같다.

$$p \approx \left(1 - e^{-kn/m}\right)^{k}$$

해시들이 독립이고 균일하다고 보는 휴리스틱 계산이다. 원소당 비트 수 $m/n$이 고정되어 있을 때 $p$는 $k^* = (m/n)\ln 2$에서 최소가 된다. 줄다리기는 이렇다. 해시 함수가 많을수록 없는 원소가 통과하려면 켜져 있어야 할 비트가 늘지만, 배열도 더 빨리 찬다. 균형점을 보려면 아직 0인 비트의 비율을 $q = e^{-kn/m}$라 두자. 그러면 $k = -(m/n)\ln q$이고 $\ln p = k\ln(1-q) = -(m/n)\ln q\,\ln(1-q)$이다. 이 식은 $q$와 $1-q$를 바꿔도 그대로이고 $q = 1/2$에서 가장 작다. 그래서 최적점에서는 비트의 절반이 켜져 있고 $p^* \approx 2^{-k^*} \approx 0.6185^{\,m/n}$이다. 오류는 원소당 비트 수에 대해 지수적으로 줄어서, 원소당 4.8비트를 더할 때마다 거짓 양성률이 10분의 1이 된다.

> [!example] 계산 예제 · Worked example
> **원소당 8비트:** $k^* = 8 \ln 2 = 5.55$. $k = 5$나 $6$이면 $p \approx 2.17\%$ 또는 $2.16\%$.
> **원소당 10비트:** $k^* = 6.93 \to 7$이므로 $p = (1 - e^{-0.7})^7 \approx 0.82\%$.
> **$10^6$개 원소에 1 %로 맞추기:** $m/n = \log_2(100)/\ln 2 \approx 9.6$비트, 약 1.2 MB이고 $k = 7$. 문자열 백만 개를 담은 Python `set`은 수십 MB를 차지한다.
> 비트 위치를 무작위로 뽑은 시뮬레이션($n = 1000$, $m = 10\,000$, $k = 7$)은 0.81 %로 공식과 맞았다. 아래의 이중 해싱 필터는 약 0.9 %로 조금 나쁜데, $k$개 위치가 완전히 독립이 아니기 때문이다.

```python
import hashlib, math

class BloomFilter:
    def __init__(self, m_bits, k):
        self.m, self.k = m_bits, k
        self.bits = bytearray(m_bits)

    def _indices(self, item):
        d = hashlib.sha256(repr(item).encode()).digest()
        h1 = int.from_bytes(d[:8], "little")
        h2 = int.from_bytes(d[8:16], "little") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]  # double hashing

    def add(self, item):
        for j in self._indices(item):
            self.bits[j] = 1

    def __contains__(self, item):
        return all(self.bits[j] for j in self._indices(item))

n, m = 1000, 10_000                      # 10 bits per stored item
k = round(m / n * math.log(2))           # 7
bf = BloomFilter(m, k)
for x in range(n):
    bf.add(x)
assert all(x in bf for x in range(n))    # never a false negative
fp = sum(("q", x) in bf for x in range(100_000)) / 100_000
print(k, round((1 - math.exp(-k * n / m)) ** k, 4), fp)  # 7 0.0082, measured close to that
```

블룸 필터는 비싼 정확 조회 앞에 두는 싼 사전 검사로 쓴다. 디스크 읽기, 네트워크 호출, 거대한 탐색의 큰 방문 집합 같은 것이다. "아니오"면 비싼 조회를 건너뛰고, "예"면 정확 조회로 확인한다.

### 4. 이진 힙

**한 문장 요지:** 모든 부모가 자식 이하인 완전 이진 트리다. 그래서 최솟값은 루트에 있고, 트리는 포인터 없이 평범한 배열에 저장된다.

**배열 배치(0부터 시작).** 인덱스 $i$ 노드의 자식은 $2i+1$, $2i+2$이고 부모는 $(i-1)//2$다. 트리가 완전하므로(마지막 층을 뺀 모든 층이 차 있고, 마지막 층은 왼쪽부터 찬다) 배열에 빈칸이 없고 높이는 $\lfloor \log_2 n \rfloor$이다. 힙 순서는 *세로 방향뿐이다.* 형제끼리는 순서가 없으므로 힙은 정렬되어 있지 **않고**, 임의의 키를 찾으려면 O(n)이 든다. 교재에 따라 1부터 세기도 한다(자식 $2i, 2i+1$, 부모 $i//2$). 어느 쪽을 쓰는지 밝혀라.

**두 불변식.** 이진 최소 힙은 배열 $A[0], \dots, A[n-1]$로서, 암묵적 트리가 완전하다는 모양 성질(**shape property**)과 — 이 인덱스 규칙에서 빈칸 없는 배열은 자동으로 만족한다 — 다음 힙 성질(**heap property**)을 갖는다:
$$A[\lfloor (i-1)/2 \rfloor] \le A[i] \quad \text{for every } 1 \le i < n$$
그래서 모든 부모는 자식 이하이고, 어느 노드에서든 경로를 따라 올라가 보면 $A[0]$이 최솟값임을 알 수 있다. 최대 힙은 부등식을 뒤집는다. 반례: `[2, 3, 1]`은 힙이 아니다. 인덱스 2의 값 1이 부모 2보다 작기 때문이다. 힙은 우선순위 큐(**priority queue**)의 통상적인 구현이다. 우선순위 큐는 "우선순위와 함께 넣기"와 "우선순위가 가장 작은 항목 꺼내기"를 연산으로 갖는 추상 자료형이다.

> [!example] 계산 예제 · Worked example
> 배열 `[1, 3, 2, 7, 4, 5]`는 최소 힙이다. 인덱스 1(값 3)의 자식은 인덱스 3과 4(값 7, 4)로 둘 다 3 이상이다. 인덱스 5(값 5)의 부모는 $(5-1)//2 = 2$(값 2)다. 인덱스 2의 자식은 인덱스 5와 6인데 6은 없다. 7이 4보다 앞에 있으니 정렬은 아니지만 올바른 힙이다.

**Sift-up(push).** 새 키를 끝, 즉 다음 빈 잎에 붙이고, 부모보다 작은 동안 부모와 바꾼다. 순서가 어긋날 수 있는 곳은 루트까지의 경로뿐이므로 층마다 많아야 한 번 바꾼다: O(log n).

**Sift-down(pop).** 루트를 꺼내고 *마지막* 잎을 루트로 옮긴 뒤, **더 작은** 자식보다 큰 동안 그 자식과 바꾼다. 더 작은 자식과 바꿔야 새 부모가 두 자식 이하가 된다. 더 큰 자식과 바꾸면 곧바로 힙 순서가 깨진다. 층마다 한 번: O(log n).

<svg viewBox="0 0 560 276" style="max-width:100%;height:auto" role="img" aria-label="이진 최소 힙 [1, 3, 2, 7, 4, 5]를 트리와 배열로 그렸다. 1을 꺼내면 마지막 잎 5가 루트로 오고, 더 작은 자식 2와 한 번 바꿔 [2, 3, 5, 7, 4]가 된다.">
  <defs><marker id="ad2k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="swd2k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="96" y="22" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">(a) 힙</text>
  <line x1="87" y1="65.4" x2="63" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="105" y1="65.4" x2="129" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="48.2" y1="111.6" x2="37.8" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="59.8" y1="111.6" x2="70.2" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="132.6" y1="111.8" x2="123.4" y2="132.2" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <circle cx="96" cy="56" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="96" y="60.5" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <circle cx="54" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="54" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="138" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="138" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="32" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="32" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <circle cx="76" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="76" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <circle cx="118" cy="144" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="118" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <rect x="18" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="31" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">1</text>
  <text x="31" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <rect x="44" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="57" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <text x="57" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">1</text>
  <rect x="70" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="83" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <text x="83" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">2</text>
  <rect x="96" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="109" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <text x="109" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">3</text>
  <rect x="122" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="135" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <text x="135" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">4</text>
  <rect x="148" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="161" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <text x="161" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <text x="280" y="22" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">(b) 1 꺼냄: 마지막 잎 5 → 루트</text>
  <line x1="271" y1="65.4" x2="247" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="289" y1="65.4" x2="313" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="232.2" y1="111.6" x2="221.8" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="243.8" y1="111.6" x2="254.2" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <circle cx="280" cy="56" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="280" y="60.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <circle cx="238" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="238" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="322" cy="100" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="322" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="216" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="216" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <circle cx="260" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="260" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <rect x="202" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="215" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <text x="215" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <rect x="228" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="241" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <text x="241" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">1</text>
  <rect x="254" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="267" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <text x="267" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">2</text>
  <rect x="280" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="293" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <text x="293" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">3</text>
  <rect x="306" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="319" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <text x="319" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">4</text>
  <rect x="332" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0" stroke-opacity="0.35" stroke-dasharray="3 3"/>
  <text x="345" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <text x="464" y="22" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">(c) 한 번 바꾼 뒤</text>
  <line x1="455" y1="65.4" x2="431" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="473" y1="65.4" x2="497" y2="90.6" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="416.2" y1="111.6" x2="405.8" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="427.8" y1="111.6" x2="438.2" y2="132.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <circle cx="464" cy="56" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="464" y="60.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="422" cy="100" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="422" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="506" cy="100" r="13" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.14"/>
  <text x="506" y="104.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <circle cx="400" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="400" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <circle cx="444" cy="144" r="13" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.04"/>
  <text x="444" y="148.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <rect x="386" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="399" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">2</text>
  <text x="399" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <rect x="412" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="425" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">3</text>
  <text x="425" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">1</text>
  <rect x="438" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="451" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">5</text>
  <text x="451" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">2</text>
  <rect x="464" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="477" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">7</text>
  <text x="477" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">3</text>
  <rect x="490" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.04" stroke-opacity="1.0"/>
  <text x="503" y="205.5" font-size="12" fill="currentColor" text-anchor="middle">4</text>
  <text x="503" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">4</text>
  <rect x="516" y="190" width="26" height="22" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0" stroke-opacity="0.35" stroke-dasharray="3 3"/>
  <text x="529" y="226" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <path d="M 57.0 189 Q 83.0 170 109.0 188" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8" fill="none" marker-end="url(#ad2k)"/>
  <path d="M 57.0 189 Q 96.0 166 135.0 188" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8" fill="none" marker-end="url(#ad2k)"/>
  <path d="M 130 137 C 178 104 158 46 111 52" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3" fill="none" marker-end="url(#ad2k)"/>
  <path d="M 294 54 Q 330 50 328 86" stroke="currentColor" stroke-width="1.2" fill="none" marker-end="url(#swd2k)" marker-start="url(#swd2k)"/>
  <text x="96" y="248" font-size="11" fill="currentColor" text-anchor="middle">인덱스 i의 자식:</text>
  <text x="96" y="263" font-size="11" fill="currentColor" text-anchor="middle">2i+1과 2i+2 (i = 1이면 3, 4)</text>
  <text x="280" y="248" font-size="11" fill="currentColor" text-anchor="middle">5 &gt; 2(더 작은 자식):</text>
  <text x="280" y="263" font-size="11" fill="currentColor" text-anchor="middle">인덱스 0과 2를 바꿈</text>
  <text x="464" y="248" font-size="11" fill="currentColor" text-anchor="middle">인덱스 2는 자식이 없다:</text>
  <text x="464" y="263" font-size="11" fill="currentColor" text-anchor="middle">2·2+1 = 5 ≥ n = 5, 멈춤</text>
</svg>

계산 예제의 힙 `[1, 3, 2, 7, 4, 5]`를 트리와, 그것을 저장하는 배열로 그렸다. 호는 인덱스 1의 자식 $2i+1 = 3$과 $2i+2 = 4$를 가리킨다. `heap_pop`은 1을 꺼내고 마지막 잎 5를 루트로 옮긴다. 5가 더 작은 자식 2보다 크므로 둘을 바꾸고, 인덱스 2에서는 첫 자식 자리 $2 \cdot 2 + 1 = 5$가 원소 다섯 개짜리 배열의 끝을 넘으므로 `[2, 3, 5, 7, 4]`에서 sift-down이 멈춘다.

**O(n) heapify.** push를 n번 해서 힙을 만들면 O(n log n)이다. 마지막 부모부터 루트까지 거꾸로 *sift-down*하면 O(n)이면 된다. 대부분의 노드가 바닥 근처에 있기 때문이다. 높이 $h$인 노드는 약 $n/2^{h+1}$개이고, 노드 하나를 내리는 비용은 O(log n)이 아니라 O(그 노드의 높이)다. 그래서 합은

$$\sum_{h=0}^{\lfloor \log_2 n\rfloor} \frac{n}{2^{h+1}}\, O(h) \;=\; O\!\left(n \sum_{h \ge 0} \frac{h}{2^{h+1}}\right) \;=\; O(n)$$

이 되는데, 급수 $\sum_{h \ge 0} h/2^{h+1}$의 합이 정확히 1이기 때문이다. 이유를 보려면 각 $h$를 1을 $h$번 더한 것 $h = \sum_{j=1}^{h} 1$로 쓰고 합의 순서를 바꾼다. 모든 항이 음이 아니므로 순서를 바꿔도 된다. 그러면 안쪽 합은 기하급수의 꼬리가 되어([[02-foundations/engineering-math|0.5 §5]]) $\sum_{h \ge j} 1/2^{h+1} = (1/2^{j+1}) \cdot 2 = 1/2^{j}$이고, 따라서
$$\sum_{h \ge 0} \frac{h}{2^{h+1}} = \sum_{j \ge 1} \sum_{h \ge j} \frac{1}{2^{h+1}} = \sum_{j \ge 1} \frac{1}{2^{j}} = 1$$
처음 다섯 항 $0 + 1/4 + 2/8 + 3/16 + 4/32 = 0.8125$만 더해도 1에 다가가는 것이 보인다. 노드의 절반은 잎이라 아무 일도 하지 않는다. 위에서부터 *sift-up*하는 방식에는 이런 성질이 없다. 수많은 깊은 노드가 각각 먼 길을 올라가야 하기 때문이다.

```python
def heap_push(h, x):
    h.append(x)
    i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] > h[i]:          # sift up
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]
        i = (i - 1) // 2

def sift_down(h, i):
    n = len(h)
    while True:
        smallest, l, r = i, 2 * i + 1, 2 * i + 2
        if l < n and h[l] < h[smallest]:
            smallest = l
        if r < n and h[r] < h[smallest]:
            smallest = r
        if smallest == i:
            return
        h[i], h[smallest] = h[smallest], h[i]
        i = smallest

def heap_pop(h):
    top, last = h[0], h.pop()          # IndexError on empty, like heapq
    if h:
        h[0] = last                    # move the last leaf to the root
        sift_down(h, 0)
    return top

def heapify(h):                        # O(n): sift down from the last parent
    for i in range(len(h) // 2 - 1, -1, -1):
        sift_down(h, i)

h = [9, 4, 7, 1, 8, 2]
heapify(h)
print([heap_pop(h) for _ in range(6)])   # [1, 2, 4, 7, 8, 9]
```

**실전 `heapq`.** `heapq`는 평범한 리스트를 **최소 힙으로** 다루는 함수 모음이다: `heappush`, `heappop`, `heapify`(O(n)), `heapreplace`/`heappushpop`, 그리고 top-k용 `nsmallest`/`nlargest`. 늘 나오는 관용구가 세 가지 있다:

- **(우선순위, 동점 처리, 항목) 튜플.** 튜플은 원소별로 비교하므로, 우선순위가 같으면 Python이 항목을 비교한다. dict나 사용자 객체면 `TypeError`, NumPy 배열이면 `ValueError`가 난다. 두 번째 필드에 단조 증가 카운터를 넣으면 동점이 선입선출로 풀리고 항목까지 비교가 가지 않는다.
- **최대 힙:** `-priority`를 넣는다. Python 3.14에서 공개 최대 힙 함수(`heappush_max`, `heappop_max`, `heapify_max`)가 추가되었지만, 인터뷰 환경은 더 오래된 버전인 경우가 많으므로 부호 뒤집기가 어디서나 통하는 답이다. 비공개 `_heapify_max`에는 손대지 마라.
- **지연 삭제로 decrease-key.** `heapq`는 항목을 찾아 키를 낮출 수 없다. 대신 더 좋은 키로 *새* 항목을 넣고, 꺼낸 항목의 키가 알려진 최선값보다 나쁘면 낡은 것으로 보고 건너뛴다. 힙에는 간선 완화마다 항목이 하나씩, 즉 O(m)개가 쌓일 수 있으므로 Dijkstra는 O(m log m)이다. $m \le n^2$이면 $\log m \le 2\log n$이므로 O(m log n)과 같다. Python의 Dijkstra와 A* 코드는 거의 전부 이렇게 쓴다([[02-foundations/algorithms/graph-algorithms|11.6]]).

```python
import heapq, itertools

# 1. Priority first, a counter to break ties, then the payload.
#    Without the counter, equal priorities compare the payloads (dicts -> TypeError).
tie = itertools.count()
pq = []
heapq.heappush(pq, (2.5, next(tie), {"task": "replan"}))
heapq.heappush(pq, (2.5, next(tie), {"task": "log"}))
heapq.heappush(pq, (-1.0, next(tie), {"task": "e-stop"}))   # max-heap: push -priority
print(heapq.heappop(pq)[2])                                   # {'task': 'e-stop'}

# 2. "Decrease-key" by lazy deletion: push a new entry, skip stale ones on pop.
def dijkstra(graph, src):
    dist = {src: 0.0}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                    # stale entry: u was already improved
        for v, w in graph[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))   # the old (d_v, v) stays, now stale
    return dist

g = {"a": [("b", 4), ("c", 1)], "c": [("b", 2)], "b": []}
print(dijkstra(g, "a"))                 # {'a': 0.0, 'b': 3.0, 'c': 1.0}
print(heapq.nsmallest(2, [5, 1, 4, 2])) # [1, 2]
```

**힙 두 개로 이동 중앙값.** 작은 절반은 최대 힙 `low`(부호를 뒤집어 저장)에, 큰 절반은 최소 힙 `high`에 둔다. 불변식은 `low`의 모든 원소가 `high`의 모든 원소 이하이고, `len(low)`가 `len(high)` 또는 `len(high) + 1`이라는 것이다. 그러면 중앙값은 `-low[0]`이고, 크기가 같으면 두 꼭대기의 평균이다. 삽입마다 힙 연산을 상수 번 하므로 O(log n)이고, 중앙값 읽기는 O(1)이다. 같은 패턴으로 임의의 분위수를 추적할 수 있다. 절반씩 나누는 대신 분위수 비율로 크기를 맞추면 된다. 센서 윈도에 대한 이동 중앙값은 삭제도 필요하므로 지연 삭제를 쓰는 힙 두 개나 순서 있는 컨테이너를 쓴다.

```python
import heapq

class RunningMedian:
    """Invariant: every item in low <= every item in high,
    and len(low) is len(high) or len(high) + 1."""
    def __init__(self):
        self.low = []   # max-heap of the smaller half, stored negated
        self.high = []  # min-heap of the larger half

    def add(self, x):
        heapq.heappush(self.low, -x)
        heapq.heappush(self.high, -heapq.heappop(self.low))  # fixes the order
        if len(self.high) > len(self.low):                    # fixes the sizes
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2

rm = RunningMedian()
out = []
for x in [5, 15, 1, 3, 8]:
    rm.add(x)
    out.append(rm.median())
print(out)   # [5, 10.0, 5, 4.0, 5]
```

**스트림의 top-k:** 지금까지 본 가장 큰 k개를 크기 k인 *최소* 힙에 담는다. 새 항목이 루트보다 클 때만 루트를 대체한다. 시간 O(n log k), 메모리 O(k)이고, 정렬하기엔 너무 큰 스트림에서도 동작한다.

**C++ 메모.** `std::priority_queue<T>`는 **최대 힙이다.** 최소 힙은 `std::priority_queue<T, std::vector<T>, std::greater<T>>`로 만든다. 여기에도 decrease-key가 없으므로 Python처럼 지연 삭제를 쓰거나, 항목을 지웠다가 다시 넣는 `std::set<std::pair<dist, node>>`를 쓴다. 힙은 모든 최선 우선 플래너의 경계(frontier)다. [[04-robotics/planning-decision-making|계획과 의사결정]]의 A* open list는 $f = g + h$를 키로 하는 힙이다.

### 5. 이진 탐색 트리

**한 문장 요지:** 이진 탐색처럼 단계마다 남은 트리의 절반을 버릴 수 있게 순서를 매긴 이진 트리이면서, 삽입과 삭제도 허용한다.

**불변식.** *모든* 노드에서 왼쪽 서브트리의 *모든* 키는 노드의 키보다 작고, 오른쪽 서브트리의 *모든* 키는 크다:
$$\text{key}(u) < \text{key}(v) < \text{key}(w) \quad \text{for every node } v, \text{ every } u \text{ in its left subtree}, \text{ every } w \text{ in its right subtree}$$
그래서 $v$에서의 비교 한 번이 서브트리 하나를 통째로 배제하고, 탐색이 경로 하나만 따라가게 된다. 아래 코드가 50, 30, 70, 20, 40, 60, 80으로 만드는 트리는 이를 만족한다. 20, 30, 40은 50의 왼쪽에, 60, 70, 80은 오른쪽에 있다. 바로 아래 자식만 확인하는 것이 "BST 검증" 문제의 고전적인 버그다. 5 → 왼쪽 3 → 오른쪽 8인 트리는 모든 부모-자식 검사를 통과하지만, 8이 5의 왼쪽 서브트리에 있으므로 틀린 트리다. 올바른 검사는 허용 범위 `(low, high)`를 아래로 넘긴다.

**탐색과 삽입은** 루트에서 잎까지 경로 하나를 따라 내려간다. 키가 작으면 왼쪽, 크면 오른쪽이다. 삽입은 탐색이 트리 밖으로 떨어진 자리에 새 잎을 단다. 둘 다 높이 $h$에 대해 O(h)다. 높이는 루트에서 잎까지 가장 긴 경로의 간선 수이고, 노드 하나뿐이면 0이다.

**삭제는** 세 경우가 있다:

1. **잎:** 그냥 지운다.
2. **자식 하나:** 그 자식을 노드 자리에 끼워 넣는다.
3. **자식 둘:** **중위 후속자**, 즉 오른쪽 서브트리의 최소 키를 찾는다(오른쪽으로 한 번, 그다음 왼쪽으로 끝까지). 그 키를 노드에 복사하고, 오른쪽 서브트리에서 후속자를 삭제한다. 후속자는 왼쪽 자식이 없으므로(있다면 그 자식이 더 작을 것이다) 그 삭제는 경우 1이나 2가 된다. 후속자를 쓰면 순서가 유지된다. 그 키는 왼쪽 서브트리의 모든 키보다 크고, 오른쪽 서브트리에 남은 어떤 키보다도 크지 않다. 중위 선행자를 써도 대칭적으로 된다.

```python
class Node:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def insert(root, key):                   # returns the (possibly new) subtree root
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:                 # equal keys are ignored
        root.right = insert(root.right, key)
    return root

def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    elif root.left is None or root.right is None:   # cases 1-2: 0 or 1 child
        return root.left or root.right
    else:                                            # case 3: two children
        succ = root.right
        while succ.left:                 # successor = leftmost node of right subtree
            succ = succ.left
        root.key = succ.key
        root.right = delete(root.right, succ.key)    # succ has no left child
    return root

def inorder(node):                       # left, node, right -> sorted keys
    return inorder(node.left) + [node.key] + inorder(node.right) if node else []

root = None
for k in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, k)
root = delete(root, 50)
print(root.key, inorder(root))           # 60 [20, 30, 40, 60, 70, 80]
```

**순회.** 모든 노드를 한 번씩 방문하므로 각각 O(n)이다:

- **중위**(왼쪽, 노드, 오른쪽)는 키를 정렬 순서로 방문한다. 불변식에서 귀납법으로 바로 나온다. "k번째로 작은 원소"와 "올바른 BST인가"(수열이 엄격히 증가해야 한다)에 답한다.
- **전위**(노드, 왼쪽, 오른쪽)는 부모를 서브트리보다 먼저 방문한다. 전위 순서로 키를 다시 넣으면 같은 트리가 만들어지므로 직렬화와 복사에 쓴다. 위 코드에서 삭제 후 트리는 `[60, 30, 20, 40, 70, 80]`.
- **후위**(왼쪽, 오른쪽, 노드)는 두 자식을 부모보다 먼저 끝낸다. C++에서 메모리를 해제하거나, 자식들의 결과로 서브트리 값(높이, 크기, 합)을 계산할 때 쓴다. 위 트리는 `[20, 40, 30, 80, 70, 60]`.

**균형이 중요한 이유.** 모든 연산이 O(h)인데, $h$는 $\lfloor\log_2 n\rfloor$(완전 균형)부터 $n-1$(사슬)까지 될 수 있다. 타임스탬프나 순차 ID처럼 *이미 정렬된 순서로* 키를 넣으면 사슬이 되어 "트리"가 느린 연결 리스트로 전락한다. $n = 10^6$이면 약 20걸음 대 백만 걸음이다. 무작위 순서로 넣으면 평균 깊이가 $2\ln n \approx 1.39\log_2 n$ 근처지만, 실제 데이터는 좀처럼 무작위가 아니다. 한쪽으로 쏠린 트리에서 재귀 코드를 돌리면 Python 기본 재귀 한도 1000도 넘는다. 크거나 신뢰할 수 없는 트리에는 반복문 버전을 써라.

**균형 트리가 보장하는 것.** 자가 균형 BST는 삽입·삭제 뒤 국소적인 *회전*으로 균형을 되찾고, 높이를 *최악의 경우에도* O(log n)으로 유지하므로 모든 연산이 O(log n)에 머문다. 레드-블랙 트리는 갱신당 회전이 많아야 세 번이고(경로를 따라 색 바꾸기는 더 있다), AVL 삭제는 경로의 모든 층에서 회전할 수도 있다. **레드-블랙 트리**(Guibas & Sedgewick 1978)는 높이 ≤ $2\log_2(n+1)$을 보장한다. **AVL 트리**(Adelson-Velsky & Landis 1962)는 서브트리 높이 차를 1 이내로 유지하고 높이가 대략 $1.44\log_2 n$ 이하임을 보장한다. AVL은 더 촘촘히 균형을 맞춰 탐색이 빠르고, 레드-블랙은 갱신당 재구성이 적다. 인터뷰는 회전의 경우 나누기를 거의 묻지 않는다. 보장이 무엇이고 어느 라이브러리가 그것을 주는지를 묻는다. 노드마다 서브트리 크기를 저장하면 *select*(k번째로 작은 원소)와 *rank*도 O(log n)이 된다.

그 높이 보장 뒤에 있는 불변식:
- **AVL:** 모든 노드 $v$에서 두 서브트리의 높이 차가 1 이하다. 빈 서브트리의 높이는 $-1$로 센다:
$$\lvert \text{height}(v.\text{left}) - \text{height}(v.\text{right}) \rvert \le 1$$
  그래서 높이 $h$인 AVL 트리가 가질 수 있는 최소 노드 수는 $N(h) = N(h-1) + N(h-2) + 1$을 따르고, $h = 0, \dots, 5$에서 1, 2, 4, 7, 12, 20으로 피보나치 수처럼 자란다. 이 지수적 증가가 $1.44\log_2 n$의 출처다. 반례: 1, 2, 3을 순서대로 넣으면 사슬이 되고, 루트의 서브트리 높이는 $-1$과 $1$로 차이가 2다.
- **레드-블랙:** 모든 노드는 빨강 아니면 검정이고, 루트는 검정이며, 빈 자식 자리(NIL)는 검정으로 세고, 빨간 노드는 빨간 자식을 갖지 않으며, 어느 노드에서 NIL까지 내려가는 모든 경로는 같은 수의 검정 노드를 지난다. 마지막 두 규칙 때문에 빨강과 검정이 번갈아 나오는 가장 긴 루트-NIL 경로가 전부 검정인 가장 짧은 경로의 두 배를 넘지 못하므로 높이는 $2\log_2(n+1)$ 이하, $n = 10^6$이면 약 40이다.
- **회전**(rotation), 둘 다 쓰는 수리 연산: 노드 $x$의 자식 하나를 $x$ 위로 올리고, 그 자식의 안쪽 서브트리를 $x$ 밑에 다시 단다. 포인터 세 개가 바뀌고 중위 순서는 바뀌지 않으므로 BST 불변식이 유지된다. 루트에서 왼쪽 회전 한 번이면 사슬 1 → 2 → 3이 자식 1과 3을 가진 2가 된다.

**라이브러리.** C++ `std::map` / `std::set`은 균형 BST이고(주요 구현은 모두 레드-블랙), floor·ceiling 질의용 `lower_bound` / `upper_bound`와 O(log n) 삽입·삭제를 제공한다. Python 표준 라이브러리에는 균형 BST가 없다. 정렬된 `list`에 `bisect`를 쓰면 탐색은 O(log n)이지만 삽입은 O(n)이다. 보통의 답은 서드파티 `sortedcontainers` 패키지(`SortedList`, `SortedDict`)다. 내부는 트리가 아니라 정렬된 부분 리스트들의 리스트지만, 같은 순서 인터페이스를 대략 로그 비용과 빠른 상수로 제공한다. 인터뷰 환경에 없다면 그렇게 말하고 `bisect`나 지연 삭제 힙으로 대신하라.

### 6. 접두사 질의를 위한 트라이

**한 문장 요지:** 문자열을 루트에서 시작하는 경로로 저장하고 간선마다 문자 하나를 두어, 공통 접두사를 가진 문자열들이 경로 하나를 공유하게 한다.

각 노드는 문자에서 자식으로 가는 사상을 갖고, 거기서 끝나는 단어가 있는지 표시한다. 한 노드의 자식들은 서로 다른 문자를 키로 가지므로 문자열마다 경로는 많아야 하나이고, 단어 $w$가 저장된 집합 $S$에 속하는지는 그 경로와 끝 표시가 함께 정한다:
$$w \in S \iff \text{walk}(\text{root}, w) \text{ exists and carries the end marker}$$
아래 코드에서 `arm`과 `arm_left`를 넣은 뒤 `arm_`의 경로는 있지만 표시가 없으므로, `arm_`은 접두사이지 단어가 아니다. 길이 L인 키의 삽입, 정확 조회, "이 접두사로 시작하는 단어가 있는가"는 각각 O(L)이고, **저장된 단어 수와 무관하다.** 접두사 아래 모든 단어를 모으는 데는 O(L + 출력 서브트리 크기)가 든다. 해시 셋도 단어 하나를 O(L)에 조회한다(문자열을 해시하려면 전부 읽어야 하므로). 하지만 모든 키를 훑지 않고는 접두사 질문에 답할 수 없다.

대가는 메모리다. 노드마다 dict(C++에서는 26칸 배열)이므로, 짧은 단어가 많으면 트라이가 같은 단어의 집합보다 몇 배 클 수 있다. 압축 트라이(radix tree)는 자식이 하나뿐인 노드 사슬을 합친다. **정렬 리스트와 이진 탐색으로** 충분한 경우도 많다. `p`로 시작하는 모든 단어는 연속된 한 구간에 있고, `bisect` 두 번으로 찾을 수 있다.

트라이가 정답인 곳: 자동완성, 글자 격자에서 단어 찾기(백트래킹이 접두사가 트라이에 없으면 곧바로 그 경로를 버린다), **최장 접두사 일치**(IP 라우팅 테이블이 경로를 고르는 방식), 그리고 위치마다 가장 긴 어휘 항목을 맞추는 탐욕적 최장 일치 토크나이저.

```python
class Trie:
    END = "$"                      # marks "a word ends here"

    def __init__(self):
        self.root = {}             # nested dicts: char -> child node

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node[self.END] = True

    def _walk(self, s):            # node reached by spelling s, or None
        node = self.root
        for ch in s:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def contains(self, word):
        node = self._walk(word)
        return node is not None and self.END in node

    def with_prefix(self, prefix):
        out, start = [], self._walk(prefix)
        stack = [] if start is None else [(start, prefix)]
        while stack:
            node, s = stack.pop()
            for ch, child in node.items():
                if ch == self.END:
                    out.append(s)
                else:
                    stack.append((child, s + ch))
        return sorted(out)

t = Trie()
for w in ["arm", "arm_left", "arm_right", "base", "base_link"]:
    t.insert(w)
print(t.contains("arm_"), t.with_prefix("arm_"))  # False ['arm_left', 'arm_right']
print(t.with_prefix("ba"), t.with_prefix("x"))    # ['base', 'base_link'] []
```

함정: "접두사가 있다"와 "단어가 있다"를 헷갈리는 것(`arm_`은 경로이지만 단어가 아니다. 그래서 끝 표시가 필요하다), 실제 문자로도 나올 수 있는 `"$"` 같은 표식 키를 쓰는 것(나올 수 없는 키나 별도 노드 클래스를 써라), 아주 깊은 트라이에서 `s + ch` 문자열을 반복해서 만들어 O(L²)을 치르는 것. 긴 키는 문자 리스트를 넘기고 마지막에 한 번 join하라.

### 7. Union-find(서로소 집합)

**한 문장 요지:** 그룹마다 부모 포인터로 된 트리를 두고 그 루트가 그룹의 이름이 된다. 두 항목은 같은 루트에 닿을 때, 오직 그때만 같은 그룹이다.

- **`find(x)`는** 부모 포인터를 따라 루트까지 간다.
- **`union(a, b)`는** 두 루트를 찾고, 다르면 한 루트를 다른 루트의 자식으로 만든다.

두 연산이 지키는 계약은 `find`가 집합마다 대표 원소 하나를 돌려준다는 것이다. 그래서 어떤 합치기 순서 뒤에도
$$\text{find}(x) = \text{find}(y) \iff x \text{ and } y \text{ are connected by some chain of unions}$$
그 뒤의 표현 불변식: `parent[r] == r`인 것은 정확히 $r$이 루트일 때이고, 포인터들이 사이클 없는 숲을 이루므로 어느 원소에서든 `parent`를 따라가면 루트에 닿는다. 아래 `DSU` 클래스로 예를 들면, 원소 4개에서 `union(0, 1)`과 `union(2, 3)` 뒤에는 `find(0) == find(1)`이고 `find(1) != find(2)`다. `union(1, 3)` 뒤에는 네 `find` 호출이 모두 0을 돌려준다.

항목 삭제나 그룹 분할은 지원하지 않는다. 간선을 지워야 한다면 연산을 오프라인으로 역순 처리해 삭제를 합치기로 바꾸거나, 다른 구조를 써라.

**두 가지 최적화가 빠르게 만든다:**

- **크기(또는 랭크) 기준 합치기:** 항상 *작은* 트리를 큰 트리 밑에 단다. 노드의 깊이는 그 트리가 적어도 같은 크기의 트리 밑으로 들어갈 때만 늘어나므로, 그때마다 노드가 속한 트리의 크기가 적어도 두 배가 된다. 이것은 많아야 $\log_2 n$번 일어나므로 높이는 $\log_2 n$ 이하이고, 다음 기법 없이도 모든 연산이 O(log n)이다. *랭크* 기준은 크기 대신 높이의 상한을 쓰며 같은 보장을 준다.
- **경로 압축:** `find` 중에 경로 위 모든 노드가 루트를 직접 가리키게 한다. 그 노드들의 다음 find는 한 걸음이다. *경로 반감*(올라가며 `parent[x] = parent[parent[x]]`)은 같은 점근 효과를 내는 한 번짜리 변형이다.

둘을 함께 쓰면 원소 $n$개에 대한 연산 $m$번이 $O(m\,\alpha(n))$ 시간에 끝난다(Tarjan 1975). 여기서 $\alpha$는 역 아커만 함수로, 컴퓨터에 존재할 수 있는 어떤 $n$에 대해서도 4 이하다. 정확히는 Cormen 등의 형태로, $A_0(j) = j + 1$이라 두고 $A_k(j)$를 $j$에 $A_{k-1}$을 $j + 1$번 연달아 적용한 값이라 하자. 그러면
$$\alpha(n) = \min\{k : A_k(1) \ge n\}$$
이다. $A_1(1) = 3$, $A_2(1) = 7$, $A_3(1) = 2047$이고 $A_4(1)$은 617자리 수인 $2^{2048}$보다 크므로, 그보다 작은 모든 $n$에서 $\alpha(n) \le 4$다. 그러니 실제로는 연산당 분할상환 상수다. 인터뷰는 증명이 아니라 이 명제를 원한다. 함정: 크기·랭크 기준 합치기도 경로 압축도 없이 나쁜 순서로 계속 연결하면 사슬이 생겨 `find`가 O(n)이 된다.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:          # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                        # already in the same set
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                    # union by size: small under large
        self.size[ra] += self.size[rb]
        return True

def kruskal(n, edges):
    """edges: (weight, u, v). Total weight of a minimum spanning forest."""
    dsu = DSU(n)
    return sum(w for w, u, v in sorted(edges) if dsu.union(u, v))

print(kruskal(4, [(1, 0, 1), (3, 1, 2), (2, 0, 2), (4, 2, 3), (5, 1, 3)]))  # 7
```

**쓰임.**

- **연결 성분.** 고정된 그래프라면 BFS나 DFS도 O(V + E)다. Union-find가 이기는 것은 간선이 *시간에 따라 도착하고* 도착 사이사이 "벌써 연결됐나?"에 답해야 할 때, 그리고 인접 리스트를 만들지 않고 답을 원할 때다.
- **무방향 그래프의 사이클 검출:** `union`이 `False`를 돌려주면 그 간선이 사이클을 닫는다.
- **Kruskal 최소 신장 트리**(Kruskal 1956): 간선을 가중치로 정렬하고, 두 끝점이 다른 성분에 있을 때만 간선을 채택한다. 그 검사가 위의 `union` 호출이다. 정렬이 지배하므로 전체 O(E log E)다. 증명은 [[02-foundations/algorithms/greedy-mst|11.4]].

**로보틱스 메모.** 점유 격자나 분할 마스크에서 *덩어리(blob)에* 라벨을 붙이는 방법이 union-find다. 점유된 셀마다 점유된 오른쪽·아래 이웃과 합치면 루트 하나가 장애물 하나다. 영상 처리의 고전적인 두 번 훑기 연결 성분 라벨링도 같은 구조로 라벨 동치를 합친다. **포인트 클라우드 분할에서는** 유클리드 군집화가 반경 $r$ 안의 이웃과 모든 점을 합친다. 이웃은 KD-tree나 복셀 해시(§8)에서 얻는다. 결과로 나오는 집합이 군집이고, 영역 확장 BFS와 같은 답을 준다. 스캔이 도착하는 대로 점을 점진적으로 추가할 수도 있다. 부모 사상을 셀 튜플로 키잉하면 희소한 지도에서도 싸다:

```python
def cluster_cells(occupied):
    """occupied: set of (row, col). Returns 4-connected clusters as lists."""
    parent = {cell: cell for cell in occupied}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path halving
            x = parent[x]
        return x

    for r, c in occupied:
        for nb in ((r + 1, c), (r, c + 1)):  # each adjacent pair seen once
            if nb in occupied:
                parent[find(nb)] = find((r, c))
    clusters = {}
    for cell in occupied:
        clusters.setdefault(find(cell), []).append(cell)
    return sorted(sorted(c) for c in clusters.values())

cells = {(0, 0), (0, 1), (1, 1), (1, 3), (2, 3), (3, 3), (3, 2), (3, 0)}
for cluster in cluster_cells(cells):
    print(cluster)
# [(0, 0), (0, 1), (1, 1)]
# [(1, 3), (2, 3), (3, 2), (3, 3)]
# [(3, 0)]
```

이 짧은 버전은 크기 기준 합치기 없이 경로 반감만 쓴다. 격자 덩어리에는 충분하다. 입력이 적대적일 수 있으면 크기 배열을 추가하라.

### 8. 로보틱스 다리: 최근접점을 위한 KD-tree

로봇 연구실이 가장 자주 묻는 자료구조 질문은 위의 어느 구조에 관한 것도 아니다. "ICP, 법선 추정, RRT가 시간을 전부 최근접점 탐색에 쓴다. 무엇을 쓰겠는가?"이다. 표준 답은 **KD-tree**(Bentley 1975)다. $\mathbb{R}^d$의 점들에 대한 이진 탐색 트리로, 내부 노드마다 좌표 하나를 골라(보통 축을 돌아가며, 또는 퍼짐이 가장 큰 축) 중앙값에서 공간을 나눈다. 그래서 트리가 균형을 이루고, 구축에는 O(n log n)이 든다.

**불변식.** 내부 노드마다 점 하나, 분할 축 $s$, 그 점의 $s$번째 좌표와 같은 분할값 $t$를 저장한다. 그 아래의 모든 점 $p$는 다음을 만족한다:
$$p_s < t \text{ for } p \text{ in the left subtree}, \qquad p_s \ge t \text{ for } p \text{ in the right subtree}$$
그래서 평면 $x_s = t$가 두 서브트리의 영역을 가르고, 질의가 한쪽을 건너뛸 수 있게 된다.

**질의가 하는 일.** 질의점을 포함하는 잎 영역까지 내려가며 지금까지 가장 가까운 점(거리 $r$)을 기억한다. 그런 다음 되돌아오면서, 분할 평면이 질의점에서 $r$보다 가까울 때만 분할의 *반대편을* 방문한다. 그렇지 않으면 그쪽의 어떤 점도 현재 최선을 이길 수 없기 때문이다. 저차원에서는 대부분의 서브트리가 가지치기되고, 잘 분포된 데이터에서 *기대* 질의 비용은 O(log n)이다(Friedman, Bentley & Finkel 1977). 최악은 여전히 O(n)이다. 반경 탐색과 k-최근접 탐색도 같은 가지치기를 쓴다. 검사로 쓰면, 노드의 반대편은 다음일 때만 방문한다:
$$\lvert q_s - t \rvert < r$$
반대편의 모든 점 $p$는 $\lVert q - p \rVert \ge \lvert q_s - p_s \rvert \ge \lvert q_s - t \rvert$를 만족하므로, 평면까지의 거리가 이미 $r$ 이상이면 그쪽에 더 가까운 점이 있을 수 없기 때문이다.

> [!example] 계산 예제 · Worked example
> 점 $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)$를 루트에서는 $x$의 중앙값으로, 한 층 아래에서는 $y$로 나눈다: 루트 $(7,2)$, 왼쪽 자식 $(5,4)$와 그 자식 $(2,3)$, $(4,7)$, 오른쪽 자식 $(9,6)$과 그 왼쪽 자식 $(8,1)$. 질의 $q = (9,1)$.
> 루트까지 거리는 $\sqrt{5} = 2.236$이므로 $r = 2.236$. $q_x = 9 \ge 7$이니 오른쪽으로. $(9,6)$까지 거리 5, $q_y = 1 < 6$이니 왼쪽으로. $(8,1)$까지 거리 1이므로 $r = 1$. $(9,6)$로 돌아오면 반대편은 비어 있다. 루트로 돌아오면 $\lvert 9 - 7 \rvert = 2 \ge r = 1$이므로 왼쪽 서브트리 전체가 가지치기되어 $(5,4)$, $(2,3)$, $(4,7)$은 거리를 재지도 않는다.
> 거리 계산 여섯 번 대신 세 번이고, 답 $(8,1)$은 전수 조사와 같다. 흔히 쓰는 라이브러리는 `scipy.spatial.cKDTree`/`KDTree`, C++의 `nanoflann`, 그리고 PCL과 Open3D 안의 KD-tree다.

<svg viewBox="0 0 560 280" style="max-width:100%;height:auto" role="img" aria-label="점 여섯 개의 KD-tree. x = 7에서 나누고, 왼쪽은 y = 4, 오른쪽은 y = 6에서 다시 나눈다. 질의 q = (9, 1)은 (7,2), (9,6), (8,1)만 재고, |9 − 7| = 2 ≥ r = 1이므로 왼쪽 절반은 탐색하지 않는다.">
  <rect x="34" y="44" width="168" height="192" stroke="none" fill="currentColor" fill-opacity="0.07"/>
  <rect x="34" y="44" width="240" height="192" stroke="currentColor" stroke-width="1.0" fill="none" stroke-opacity="0.5"/>
  <text x="34" y="251" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">0</text>
  <text x="154" y="251" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">5</text>
  <text x="274" y="251" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">10</text>
  <text x="28" y="240" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">0</text>
  <text x="28" y="144" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">4</text>
  <text x="28" y="48" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">8</text>
  <line x1="202" y1="236" x2="202" y2="44" stroke="currentColor" stroke-width="2.0"/>
  <line x1="34" y1="140" x2="202" y2="140" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <line x1="202" y1="92" x2="274" y2="92" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3"/>
  <text x="207" y="58" font-size="11" fill="currentColor" font-weight="bold">x = 7</text>
  <text x="38.8" y="135" font-size="11" fill="currentColor">y = 4</text>
  <text x="207" y="87" font-size="11" fill="currentColor">y = 6</text>
  <circle cx="82" cy="164" r="3.6" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>
  <text x="89" y="168" font-size="11" fill="currentColor" fill-opacity="0.6">(2,3)</text>
  <circle cx="154" cy="140" r="3.6" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>
  <text x="160" y="134" font-size="11" fill="currentColor" fill-opacity="0.6">(5,4)</text>
  <circle cx="250" cy="92" r="3.6" stroke="none" fill="currentColor"/>
  <text x="244" y="106" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="1.0">(9,6)</text>
  <circle cx="130" cy="68" r="3.6" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.6"/>
  <text x="137" y="72" font-size="11" fill="currentColor" fill-opacity="0.6">(4,7)</text>
  <circle cx="226" cy="212" r="3.6" stroke="none" fill="currentColor"/>
  <text x="226" y="203" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1.0">(8,1)</text>
  <circle cx="202" cy="188" r="3.6" stroke="none" fill="currentColor"/>
  <text x="196" y="183" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="1.0">(7,2)</text>
  <line x1="245" y1="207" x2="255" y2="217" stroke="currentColor" stroke-width="1.8"/>
  <line x1="245" y1="217" x2="255" y2="207" stroke="currentColor" stroke-width="1.8"/>
  <text x="258" y="207" font-size="12" fill="currentColor" font-weight="bold">q</text>
  <line x1="230" y1="212" x2="244" y2="212" stroke="currentColor" stroke-width="1.0" stroke-dasharray="3 2"/>
  <text x="238" y="228" font-size="11" fill="currentColor" text-anchor="middle">r = 1</text>
  <line x1="202" y1="246" x2="250" y2="246" stroke="currentColor" stroke-width="1.1"/>
  <line x1="202" y1="242" x2="202" y2="250" stroke="currentColor" stroke-width="1.1"/>
  <line x1="250" y1="242" x2="250" y2="250" stroke="currentColor" stroke-width="1.1"/>
  <text x="226" y="263" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">|9 − 7| = 2 ≥ r = 1</text>
  <text x="118" y="204.8" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">가지치기: 재지 않음</text>
  <text x="434" y="22" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">트리. d = q까지의 거리</text>
  <line x1="434" y1="80" x2="366" y2="125" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="434" y1="80" x2="502" y2="118" stroke="currentColor" stroke-width="1.8" stroke-opacity="1.0"/>
  <line x1="366" y1="147" x2="338" y2="199" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="366" y1="147" x2="400" y2="199" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <line x1="502" y1="154" x2="468" y2="192" stroke="currentColor" stroke-width="1.8" stroke-opacity="1.0"/>
  <rect x="401" y="44" width="66" height="36" rx="4" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1" stroke-opacity="1.0"/>
  <text x="434" y="60" font-size="11" fill="currentColor" text-anchor="middle">(7,2)</text>
  <text x="434" y="74" font-size="11" fill="currentColor" text-anchor="middle">d = 2.236</text>
  <text x="471" y="52" font-size="11" fill="currentColor" fill-opacity="0.7">x</text>
  <rect x="343" y="125" width="46" height="22" rx="4" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="366" y="140" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.55">(5,4)</text>
  <text x="393" y="133" font-size="11" fill="currentColor" fill-opacity="0.7">y</text>
  <rect x="469" y="118" width="66" height="36" rx="4" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1" stroke-opacity="1.0"/>
  <text x="502" y="134" font-size="11" fill="currentColor" text-anchor="middle">(9,6)</text>
  <text x="502" y="148" font-size="11" fill="currentColor" text-anchor="middle">d = 5</text>
  <text x="539" y="126" font-size="11" fill="currentColor" fill-opacity="0.7">y</text>
  <rect x="315" y="199" width="46" height="22" rx="4" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="338" y="214" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.55">(2,3)</text>
  <rect x="377" y="199" width="46" height="22" rx="4" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.45" stroke-dasharray="4 3"/>
  <text x="400" y="214" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.55">(4,7)</text>
  <rect x="435" y="192" width="66" height="36" rx="4" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1" stroke-opacity="1.0"/>
  <text x="468" y="208" font-size="11" fill="currentColor" text-anchor="middle">(8,1)</text>
  <text x="468" y="222" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">d = 1</text>
  <text x="384" y="102" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.6">x &lt; 7</text>
  <text x="484" y="102" font-size="11" fill="currentColor" fill-opacity="0.9">x ≥ 7</text>
  <text x="473" y="176" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.9">y &lt; 6</text>
  <text x="320" y="254" font-size="11" fill="currentColor" fill-opacity="0.6">가지치기: 재지 않음</text>
</svg>

계산 예제를 그린 것이다. 루트는 $x = 7$에서, 그 자식들은 $y = 4$(왼쪽)와 $y = 6$(오른쪽)에서 나눈다. 질의 $q = (9, 1)$은 트리의 실선 경로를 따라 채운 점들만 거리 2.236, 5, 1로 잰다. 최선 거리가 $r = 1$이 되고 나면 평면 $x = 7$이 $\lvert 9 - 7 \rvert = 2 \ge r$만큼 떨어져 있으므로, $(5,4)$, $(2,3)$, $(4,7)$이 있는 음영 절반은 한 번도 재지 않는다.

**차원의 저주.** 가지치기는 질의 공이 분할 평면을 몇 개만 가로지른다는 데 기댄다. $d$가 커지면 공이 거의 모든 축의 평면을 가로질러 탐색이 대부분의 잎을 방문하게 되고, 선형 탐색에 가까워진다. 흔한 경험칙은 $n \gg 2^d$일 때만 KD-tree가 도움이 된다는 것이다. 3차원 포인트 클라우드에서는 쉽게 성립한다. 50차원이나 512차원 학습 기술자에서는 성립하지 않으므로 근사 최근접점 방법(무작위 KD-forest, HNSW 같은 그래프 기반 인덱스)을 쓰고, 진짜 최근접점을 놓칠 작은 확률을 받아들인다.

**RRT에서.** 반복마다 무작위 샘플에 가장 가까운 트리 노드를 묻는다([[04-robotics/modern-robotics/ch10-motion-planning|MR 10장]]). 선형 탐색이면 N번 반복에 전체 O(N²)이 들고, 단순한 장면에서는 충돌 검사보다 훨씬 먼저 최근접점 탐색이 병목이 된다. KD-tree는 이를 질의당 대략 O(log N)으로 줄인다. 좋은 답이 언급하는 주의점이 세 가지 있다. 플래너의 트리는 노드가 하나씩 자라므로 KD-tree가 점진적 삽입과 가끔의 재구축으로 균형을 유지해야 한다. 각도가 있는 형상 공간은 *한 바퀴 돌아 이어지므로*($\theta = \pi$ 옆이 $-\pi$) 평범한 유클리드 KD-tree에는 위상을 아는 거리 함수가 필요하다. 7자유도 이상의 팔에서는 차원 페널티가 돌아오므로 플래너들이 흔히 근사 이웃을 받아들인다.

**해시 격자가 트리를 이길 때.** 군집화 반경 $r$이나 복셀 다운샘플링처럼 크기가 정해진 고정 반경 질의라면, 셀 크기가 $r$인 복셀 해시 맵이 질의점 주변 27개 셀(3차원)만 보고 답한다. 점 밀도가 유한하면 §3의 해싱으로 기대 O(1)이다. 많은 매핑 파이프라인이 바로 이 구조를 쓴다. 이런 질의가 파이프라인의 어디에 놓이는지는 [[04-robotics/state-estimation-slam|상태 추정과 SLAM]]을 보라.

### 스스로 점검

1. 로거가 순서 없이 도착하는 `(timestamp, message)` 쌍을 저장하고, 삽입이 계속되는 동안 "시각 t 이후의 첫 메시지"에 답해야 한다. 어떤 구조를 쓰고, 왜 힙이나 해시 맵은 안 되는가?
2. 슬라이딩 윈도 최댓값 코드는 `for` 안에 `while`이 있다. 왜 O(nk)가 아니라 O(n)인가?
3. 원소 $10^6$개, 거짓 양성률 1 %인 블룸 필터가 필요하다. 비트 수와 해시 함수 수는? 삽입했던 원소를 질의하면 무엇이라고 답하는가?
4. `heapq`와 지연 삭제를 쓰는 Dijkstra에서 힙에는 정점 수보다 많은 항목이 들어갈 수 있다. 크기의 상한을 구하고, 실행 시간이 여전히 O(m log n)임을 보여라.
5. 자식이 둘인 BST 삭제에서 중위 후속자에게 왜 왼쪽 자식이 없는가? 그 키를 노드에 복사해도 BST 불변식이 유지되는 이유는?
6. 크기 기준 합치기만 쓸 때 `find`의 최악 비용과 그 이유는? 경로 압축은 무엇을 더하는가? union-find가 "이 간선을 지워라"를 처리할 수 없는 이유는?
7. 512차원 이미지 임베딩에 대한 KD-tree 최근접점 탐색이 전수 탐색보다 거의 빠르지 않다. 이유를 설명하고 해결책을 제안하라.

> [!tip]- 스스로 점검 정답 · Answers
> 1. 타임스탬프를 키로 하는 균형 BST다. C++ `std::map::lower_bound`나 Python `sortedcontainers`의 `SortedList.bisect_left`가 O(log n) 삽입과 "t 이상인 최소 키"를 준다. 힙은 최솟값만 보여 주므로 임의의 t의 후속자를 찾는 데 O(n)이 들고, 해시 맵에는 순서가 아예 없다. 메시지가 순서대로 온다면 끝 append가 O(1)이므로 평범한 리스트와 `bisect`로 충분하다.
> 2. 각 인덱스는 덱에 정확히 한 번 들어가고, 뒤에서(더 큰 값이 와서) 또는 앞에서(윈도를 벗어나서) 많아야 한 번 나온다. 그러니 안쪽 `while`의 pop은 전체 실행에서 많아야 n번이고, 총 작업은 분할상환 O(n)이다. 한 단계가 최악에서 O(1)인 것은 아니지만 합은 O(n)이다.
> 3. $m/n = \log_2(1/p)/\ln 2 = \log_2 100/\ln 2 \approx 9.6$비트이므로 약 960만 비트(1.2 MB), 해시 함수는 $k = (m/n)\ln 2 \approx 6.6 \to 7$개다(검산: $(1-e^{-7/9.6})^7 \approx 1.0\%$). 블룸 필터에는 거짓 음성이 없으므로 삽입한 원소는 항상 "있음"이다.
> 4. 완화에 성공할 때마다 항목이 하나 들어가고, 이는 방향 간선마다 많아야 한 번(출발점 하나 추가)이다. 그래서 힙 크기는 O(m)이고 push·pop은 각각 O(log m)이다. $m \le n^2$이므로 $\log m \le 2\log n$이고, O(m log m) = O(m log n)이다. 낡은 항목은 한 번씩 꺼내져 O(1)에 건너뛰어진다.
> 5. 후속자는 오른쪽 서브트리의 최솟값이다. 왼쪽 자식이 있다면 그 자식도 오른쪽 서브트리에 있으면서 더 작을 테니 모순이다. 그 키는 오른쪽 서브트리에서 왔으므로 노드의 왼쪽 서브트리 모든 키보다 크고, 최솟값이었으므로 오른쪽 서브트리의 다른 모든 키보다 작다. 따라서 노드 자리에 두면 양쪽 불변식이 모두 성립하고, 오른쪽 서브트리에서 그것을 지우는 일은 쉬운 잎 또는 자식 하나 경우다.
> 6. O(log n)이다. 노드는 자기 트리가 적어도 같은 크기의 트리 밑으로 들어갈 때만 깊어지고, 그때마다 트리 크기가 적어도 두 배가 되므로 많아야 $\log_2 n$번 일어난다. 경로 압축은 쓰이는 경로를 평평하게 만들어 연산 $m$번을 $O(m\,\alpha(n))$, 사실상 연산당 상수로 낮춘다. 간선을 지우려면 집합을 쪼개야 하는데, 부모 포인터 숲은 어느 union이 어떤 원소들을 이었는지 기록하지 않으므로 되돌릴 정보가 없다. 삭제는 오프라인 역순으로 처리하거나 동적 연결성 구조를 써라.
> 7. 512차원에서는 질의 공이 거의 모든 노드의 분할 평면을 가로지르므로 가지치기가 거의 일어나지 않고, 탐색이 대부분의 잎을 방문한다. d = 512에서 경험칙 $n \gg 2^d$는 가망이 없다. 근사 최근접점(HNSW, IVF-PQ, 무작위 KD-forest)을 쓰거나, 먼저 차원을 줄이거나(PCA), 정확한 답이 필요하고 n이 적당하면 GPU에서 벡터화한 전수 탐색을 쓴다.

### 출처

- Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — 해시 테이블과 범용 해싱, 힙, 이진 탐색 트리, 레드-블랙 트리, 서로소 집합.
- Roughgarden, *Algorithms Illuminated*, Part 2 (*Graph Algorithms and Data Structures*, 2018)와 Part 3 (*Greedy Algorithms and Dynamic Programming*, 2019), Soundlikeyourself Publishing — 힙, 탐색 트리, 해싱, 블룸 필터, union-find.
- Kulikov & Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018.
- Bloom, B. H. "Space/time trade-offs in hash coding with allowable errors." *Communications of the ACM* 13(7), 1970. doi:10.1145/362686.362692
- Carter, J. L. & Wegman, M. N. "Universal classes of hash functions." *Journal of Computer and System Sciences* 18(2), 1979. doi:10.1016/0022-0000(79)90044-8
- Crosby, S. A. & Wallach, D. S. "Denial of service via algorithmic complexity attacks." *USENIX Security Symposium*, 2003.
- Williams, J. W. J. "Algorithm 232: Heapsort." *Communications of the ACM* 7(6), 1964; Floyd, R. W. "Algorithm 245: Treesort 3." *Communications of the ACM* 7(12), 1964 (선형 시간 힙 만들기).
- Adelson-Velsky, G. M. & Landis, E. M. "An algorithm for the organization of information." *Soviet Mathematics Doklady* 3, 1962.
- Guibas, L. J. & Sedgewick, R. "A dichromatic framework for balanced trees." *IEEE Symposium on Foundations of Computer Science (FOCS)*, 1978.
- Fredkin, E. "Trie memory." *Communications of the ACM* 3(9), 1960.
- Tarjan, R. E. "Efficiency of a good but not linear set union algorithm." *Journal of the ACM* 22(2), 1975. doi:10.1145/321879.321884
- Kruskal, J. B. "On the shortest spanning subtree of a graph and the traveling salesman problem." *Proceedings of the American Mathematical Society* 7(1), 1956.
- Bentley, J. L. "Multidimensional binary search trees used for associative searching." *Communications of the ACM* 18(9), 1975. doi:10.1145/361002.361007
- Friedman, J. H., Bentley, J. L. & Finkel, R. A. "An algorithm for finding best matches in logarithmic expected time." *ACM Transactions on Mathematical Software* 3(3), 1977.
- LaValle, S. M. *Planning Algorithms*, Cambridge University Press, 2006 — 샘플링 기반 계획의 최근접점 질의.
