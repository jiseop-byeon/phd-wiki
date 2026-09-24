---
title: "12.2 Git for Research Code"
tags: [foundations, tools, git, reproducibility]
study-depth: Working
wiki-support: Working
depth-goal: "On RS1's repository, say what each command does to the working tree, the index and the history; read a commit graph and name the commit that produced each results table; stamp every table with a clean commit, find a regression with git bisect in ⌈log₂ N⌉ tests, undo it without rewriting shared history, and keep bags and keys out of the repository."
mastery-when: "Raise when you maintain a lab's shared repositories — review rules, history rewrites after a leak, continuous integration, or a multi-repository robot workspace that a whole team builds from."
---

> [!note] Prerequisites · 선수 지식
> [[06-research-practice/index|6. Research Practice — RS1]] (the running study: its question, its two controllers and its frozen pilot, restated below) · [[02-foundations/algorithms/sorting-divide-conquer|11.3 §6]] (binary search on a monotone predicate, for §8) · [[02-foundations/algorithms/graph-algorithms|11.6 §3]] (a directed acyclic graph, for §1 and §3) · a terminal in which you can change directory and run a command. No Git experience is assumed.
> [[06-research-practice/index|6. 연구 실무 — RS1]](관통 연구: 질문, 두 제어기, 고정된 예비 실험. 아래에 다시 적는다) · [[02-foundations/algorithms/sorting-divide-conquer|11.3 §6]](단조 술어 위의 이진 탐색, §8에 쓴다) · [[02-foundations/algorithms/graph-algorithms|11.6 §3]](방향 비순환 그래프, §1과 §3에 쓴다) · 디렉터리를 옮기고 명령을 실행할 수 있는 터미널. Git 경험은 전제하지 않는다.

## English

*Stands on RS1, the study every page of [[06-research-practice/index|6. Research Practice]] shares, seen here as the repository that holds it: two controllers, the pilot's twenty numbers, an analysis script and a paper. First use of RS1 in the foundations track. [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility §7]] lists what a reproducible result must record; this page is how the code part of that record is kept, and how to tell afterwards which code made which number.*

> [!note] Why this matters · 왜 배우는가
> This page is part of the floor beneath the physical-AI stack of [[07-research-program/index|research program §5]]: it adds no layer, but every layer's result is only as credible as the record of the code behind it — in that section's worked instance, "Install that panel on the frame", it is the evidence for the last step, that the panel really seated, reproducibly (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without a commit on every results table, a one-character parser bug like the one §8 finds moves a mean from 10.66 N to 10.94 N and nobody can say when or why. [[06-research-practice/experimental-design-reproducibility|Research practice 2 §7]] puts the code commit first on its artifact list, [[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]] builds its pinned run on it, and the seating rates that [[05-construction-robotics/imitating-contact|10. Imitating Contact §8]] evaluates are numbers of exactly this kind — a table printed by code that a reviewer must be able to rerun; the page sits outside the seven blocks of the dissertation path ([[07-research-program/index|research program §8]]), so take it with the first code you write for the dissertation, and at the latest with block 5, where research practice 2 asks for the commit. After it you can stamp every result with the commit that made it, find the commit that broke a number in $\lceil\log_2 N\rceil$ tests, and undo it without rewriting anyone's history.

> [!note] First pass · 처음이라면
> Two sessions of 60–90 minutes each. **Session 1:** the Running object and the picture — RS1's fifteen commits, one branch, one merge, two tags — then §1 and §2: what a commit is, and how an edit travels from your files into history. End with Self-check 1 and 2. **Session 2:** §3, §7 and §8 — branches, stamping each results table with its commit, and finding and undoing a regression — then the Worked case, which sits after §9 because it uses all of them. End with Self-check 3, 5 and 6. Read §4–§6 before you first share a repository with anyone, §9 when a robot workspace spans several repositories, and do the problem set after that.

### Running object · 이 페이지의 대상

**RS1**, the running study of [[06-research-practice/index|6. Research Practice]]. *Question:* does impedance control (**B**) make the contact of plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] with a 400 N/m panel safer than position control with a force-threshold stop (**A**)? *Trial:* one approach that ends in contact; a success when the peak contact force is at most 10 N. *Pilot*, frozen, ten trials per arm — A: 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 N, so 6/10, mean 10.66 N, sample sd 2.414 N; B: 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 N, so 9/10, mean 7.50 N, sd 1.356 N. *Main study:* planned at 32 trials per arm, 64 in all.

On top of RS1 this page freezes one object of its own, specified here in full and never changed: **RS1's repository**, a real Git repository built for this page, fifteen commits dated 2 to 27 March 2026. The dates are course dates, not a record of anything. Its files:

| path | what it holds | added in |
|---|---|---|
| `README.md` | the question, the success rule and a one-line status | c13c298 |
| `.gitignore` | what Git must never track: build outputs, bags, weights, caches, `.env` (§6) | c13c298 |
| `controllers/position_stop.py` | controller A: joint gains and the stop at 6 N | 16fc8ef |
| `analysis/summarize.py` | prints the results table, stamped with the commit that ran (§7) | 2452d15 |
| `controllers/impedance.py` | controller B: stiffness $K$ and damping $D$ along the approach axis | 757338e |
| `trials/pilot.csv` | the pilot's 20 peak forces, 184 bytes | aebf24a (A), 2006419 (B) |
| `protocol.md` | the main study's plan and its pre-trial checklist | a0cd3a3, 6321a22 |
| `paper/paper.md` | the paper's methods and results sections | 041fe2f, b659311 |
| `analysis/figure.py` | prints the numbers figure 2 plots | 3568180 |

Its history, oldest first. A commit is named by the first seven of its forty hexadecimal digits (§1):

| commit | parent(s) | date (UTC) | what it does | name on it |
|---|---|---|---|---|
| c13c298 | none | 03-02 09:00 | starts the repository: README and ignore list | |
| 16fc8ef | c13c298 | 03-03 10:00 | adds controller A | |
| 2452d15 | 16fc8ef | 03-04 11:00 | adds the analysis script | |
| 757338e | 2452d15 | 03-05 14:00 | adds controller B, $K=500$ N/m, $D=30$ N·s/m | |
| aebf24a | 2452d15 | 03-05 16:00 | records A's ten pilot trials | |
| f41f0b6 | 757338e | 03-06 15:00 | tunes B on the rig to $K=300$ N/m, $D=25$ N·s/m | impedance-b |
| 882d5dd | aebf24a, f41f0b6 | 03-09 10:00 | merges B's branch, after one conflict | |
| 2006419 | 882d5dd | 03-10 16:00 | records B's ten pilot trials | pilot-v1 |
| a0cd3a3 | 2006419 | 03-16 09:00 | writes the main-study protocol: 32 per arm | |
| dda4b0f | a0cd3a3 | 03-18 13:00 | rewrites the trial parser — and drops a trial (§8) | |
| 041fe2f | dda4b0f | 03-20 10:00 | drafts the methods section | |
| 6321a22 | 041fe2f | 03-23 11:00 | adds the pre-trial checklist | study-v1 |
| b659311 | 6321a22 | 03-25 15:00 | drafts the results section | |
| 3568180 | b659311 | 03-27 10:00 | adds the figure script | |
| ea13bc4 | 3568180 | 03-27 14:00 | reverts dda4b0f | main, HEAD |

Page-local numbers, frozen with the object:

| quantity | value | kind |
|---|---|---|
| one trial bag, as rosbag2 records it | 60 MiB $=62{,}914{,}560$ bytes | course number, not a measurement |
| pilot and main study, in trials | 20 and 64 | RS1's |
| the whole history, packed | 61 objects in 10.15 KiB | measured on this page's repository |
| A's stop; B's gains | 6 N, as in F1 of [[06-research-practice/failure-analysis-system-evaluation\|3. Failure Analysis]]; $K$ and $D$ as above | the repository's own; no other page uses $K$ and $D$ |

The repository was built on macOS (arm64) with Apple Git 2.50.1, as the author `RS1 Student <student@example.com>`, with every commit's dates fixed through Git's `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` environment variables. The same files, messages and dates give the same ids on any machine; the commits you make carry your own name and clock, and so get other ids (§1 says why). Every command below was run in that repository or in scratch clones of it, and every output is as Git printed it, trimmed where marked; on the robot's Ubuntu the messages differ only where Git versions differ, mostly in the `hint:` lines.

*Scope: this page teaches the Git a robotics researcher needs to keep a study's code, small data and paper correct and recoverable — what a commit is, how files move into one, branches and merges, sharing through a remote, what must never be committed, stamping each result with the commit that made it, finding and undoing a regression, and pinning several repositories in one workspace. It does not teach history rewriting beyond one paragraph, Git LFS, hooks, signed commits or continuous integration — CI for a ROS package is [[04-robotics/ros2/debugging-data-reproducibility|25.10 §12]] — nor what a study must record besides its code, which is [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §7]]; the shell, Python environments and file formats are this track's pages [[02-foundations/tools/linux-shell|12.1]], [[02-foundations/tools/python-research-code|12.3]] and [[02-foundations/tools/config-data-formats|12.4]], and the paper's own build — what of it is committed and what is regenerated — is [[02-foundations/tools/latex-figures-references|12.6 §10]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 424" style="max-width:100%;height:auto" role="img" aria-label="RS1's commit graph: fifteen commits newest first, branch impedance-b with two commits merged by 882d5dd, tags pilot-v1 on 2006419 and study-v1 on 6321a22, the bisect range of six commits with its three tests, the first bad commit dda4b0f and the revert ea13bc4.">
  <defs><marker id="gdRev" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">RS1’s repository, newest commit at the top</text>
  <g font-size="10" fill="currentColor" fill-opacity="0.75"><text x="78" y="38">commit</text><text x="130" y="38">message</text><text x="398" y="38">refs · bisect · tables</text></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="40.0" y1="64.0" x2="40.0" y2="74.0"/>
    <line x1="40.0" y1="86.0" x2="40.0" y2="96.0"/>
    <line x1="40.0" y1="108.0" x2="40.0" y2="118.0"/>
    <line x1="40.0" y1="130.0" x2="40.0" y2="140.0"/>
    <line x1="40.0" y1="152.0" x2="40.0" y2="162.0"/>
    <line x1="40.0" y1="174.0" x2="40.0" y2="184.0"/>
    <line x1="40.0" y1="196.0" x2="40.0" y2="206.0"/>
    <line x1="40.0" y1="218.0" x2="40.0" y2="228.0"/>
    <line x1="40.0" y1="243.0" x2="40.0" y2="294.0"/>
    <line x1="46.4" y1="240.4" x2="57.8" y2="251.8"/>
    <line x1="62.0" y1="262.0" x2="62.0" y2="272.0"/>
    <line x1="59.3" y1="283.4" x2="42.7" y2="316.6"/>
    <line x1="40.0" y1="306.0" x2="40.0" y2="316.0"/>
    <line x1="40.0" y1="328.0" x2="40.0" y2="338.0"/>
    <line x1="40.0" y1="350.0" x2="40.0" y2="360.0"/>
  </g>
  <path d="M386 72 H390 V198 H386" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <path d="M34 61 C 12 80, 12 146, 33.5 164.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#gdRev)"/>
  <text x="11" y="113" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 11 113)">reverts</text>
  <circle cx="40" cy="58" r="5" fill="currentColor"/>
  <text x="78" y="62" font-size="11" font-family="monospace" fill="currentColor">ea13bc4</text>
  <text x="130" y="62" font-size="11" fill="currentColor">Revert “Parse trials without…”</text>
  <circle cx="40" cy="80" r="5" fill="currentColor"/>
  <text x="78" y="84" font-size="11" font-family="monospace" fill="currentColor">3568180</text>
  <text x="130" y="84" font-size="11" fill="currentColor">Add the figure script</text>
  <circle cx="40" cy="102" r="5" fill="currentColor"/>
  <text x="78" y="106" font-size="11" font-family="monospace" fill="currentColor">b659311</text>
  <text x="130" y="106" font-size="11" fill="currentColor">Draft the results section</text>
  <circle cx="40" cy="124" r="5" fill="currentColor"/>
  <text x="78" y="128" font-size="11" font-family="monospace" fill="currentColor">6321a22</text>
  <text x="130" y="128" font-size="11" fill="currentColor">Add the pre-trial checklist</text>
  <circle cx="40" cy="146" r="5" fill="currentColor"/>
  <rect x="32" y="138" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <text x="78" y="150" font-size="11" font-family="monospace" fill="currentColor">041fe2f</text>
  <text x="130" y="150" font-size="11" fill="currentColor">Draft the methods section</text>
  <circle cx="40" cy="168" r="5" fill="currentColor"/>
  <rect x="32" y="160" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <text x="78" y="172" font-size="11" font-family="monospace" fill="currentColor">dda4b0f</text>
  <text x="130" y="172" font-size="11" fill="currentColor">Parse trials without the csv module</text>
  <circle cx="40" cy="190" r="5" fill="currentColor"/>
  <rect x="32" y="182" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <text x="78" y="194" font-size="11" font-family="monospace" fill="currentColor">a0cd3a3</text>
  <text x="130" y="194" font-size="11" fill="currentColor">Write the main-study protocol</text>
  <circle cx="40" cy="212" r="5" fill="currentColor"/>
  <text x="78" y="216" font-size="11" font-family="monospace" fill="currentColor">2006419</text>
  <text x="130" y="216" font-size="11" fill="currentColor">Record the pilot of B: ten trials</text>
  <circle cx="40" cy="234" r="5" fill="currentColor"/>
  <circle cx="40" cy="234" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="78" y="238" font-size="11" font-family="monospace" fill="currentColor">882d5dd</text>
  <text x="130" y="238" font-size="11" fill="currentColor">Merge branch ‘impedance-b’</text>
  <circle cx="62" cy="256" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="78" y="260" font-size="11" font-family="monospace" fill="currentColor">f41f0b6</text>
  <text x="130" y="260" font-size="11" fill="currentColor">Tune B: K 500→300, D 30→25</text>
  <circle cx="62" cy="278" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="78" y="282" font-size="11" font-family="monospace" fill="currentColor">757338e</text>
  <text x="130" y="282" font-size="11" fill="currentColor">Add controller B: impedance</text>
  <circle cx="40" cy="300" r="5" fill="currentColor"/>
  <text x="78" y="304" font-size="11" font-family="monospace" fill="currentColor">aebf24a</text>
  <text x="130" y="304" font-size="11" fill="currentColor">Record the pilot of A: ten trials</text>
  <circle cx="40" cy="322" r="5" fill="currentColor"/>
  <text x="78" y="326" font-size="11" font-family="monospace" fill="currentColor">2452d15</text>
  <text x="130" y="326" font-size="11" fill="currentColor">Add the analysis script</text>
  <circle cx="40" cy="344" r="5" fill="currentColor"/>
  <text x="78" y="348" font-size="11" font-family="monospace" fill="currentColor">16fc8ef</text>
  <text x="130" y="348" font-size="11" fill="currentColor">Add controller A with a 6 N stop</text>
  <circle cx="40" cy="366" r="5" fill="currentColor"/>
  <text x="78" y="370" font-size="11" font-family="monospace" fill="currentColor">c13c298</text>
  <text x="130" y="370" font-size="11" fill="currentColor">Start RS1: question, rule, ignore list</text>
  <rect x="398" y="50" width="78" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="61.5" font-size="10" fill="currentColor">main · HEAD</text>
  <text x="482" y="61.5" font-size="10" fill="currentColor">A: 10.66 N</text>
  <text x="398" y="83.5" font-size="10" fill="currentColor">bisect: N = 6 → 3 tests</text>
  <text x="398" y="105.5" font-size="10" fill="currentColor">A: 10.94 N (9 trials)</text>
  <rect x="398" y="116" width="52" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="127.5" font-size="10" fill="currentColor">study-v1</text>
  <text x="398" y="149.5" font-size="10" fill="currentColor">test 1: bad</text>
  <text x="398" y="171.5" font-size="10" fill="currentColor" font-weight="bold">test 2: bad → first bad</text>
  <text x="398" y="193.5" font-size="10" fill="currentColor">test 3: good</text>
  <rect x="398" y="204" width="50" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="215.5" font-size="10" fill="currentColor">pilot-v1</text>
  <text x="482" y="215.5" font-size="10" fill="currentColor">A: 10.66 N</text>
  <text x="398" y="237.5" font-size="10" fill="currentColor">2 parents</text>
  <rect x="398" y="248" width="74" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="259.5" font-size="10" fill="currentColor">impedance-b</text>
  <circle cx="18" cy="388" r="5" fill="currentColor"/>
  <text x="28" y="392" font-size="10" fill="currentColor">on main</text>
  <circle cx="98" cy="388" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="108" y="392" font-size="10" fill="currentColor">on impedance-b</text>
  <circle cx="232" cy="388" r="5" fill="currentColor"/><circle cx="232" cy="388" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="245" y="392" font-size="10" fill="currentColor">merge</text>
  <text x="300" y="392" font-size="10" fill="currentColor">line: a commit and its parent below it</text>
  <text x="12" y="412" font-size="10" fill="currentColor">dashed: ea13bc4 undoes dda4b0f</text>
  <text x="300" y="412" font-size="10" fill="currentColor">A: arm A’s mean as summarize.py printed it there</text>
</svg>

RS1's fifteen commits in the order `git log --graph` prints them, newest at the top, each line joining a commit to its parent below it: branch impedance-b (757338e, f41f0b6) leaves at 2452d15 and returns in the merge 882d5dd, whose two parents are aebf24a and f41f0b6, and the tags pilot-v1 and study-v1 name the commit of the pilot's table and the code frozen before the main study's first trial. The parser rewritten in dda4b0f dropped one of A's trials, so the table printed at b659311 shows 10.94 N from 9 trials instead of 10.66 N from 10; `git bisect` searched the six commits after pilot-v1 and found dda4b0f in three tests, and ea13bc4 undoes it without removing anything, so HEAD prints 10.66 N again, stamped `study-v1-3-gea13bc4`.

### 1. What Git stores: objects, and the hash that names a commit

*In one sentence:* Git keeps every version of every file as an object named by a hash of its bytes, and a commit is one more such object — a snapshot of the whole project plus the names of its parents — so a commit's name vouches for its entire history.

A results table is only as trustworthy as your ability to name the exact code and data behind it. Git's answer, from which everything else on this page follows, is one design choice: it names each thing it stores by a fingerprint of that thing's bytes. Once that is clear, a branch, a tag, a merge and the stamp on a results table are all names for fingerprints. A repository is a database of objects, kept in the directory `.git/objects` at the top of the project, plus a few names that point into it. There are four kinds of object. A **blob** holds the bytes of one file and nothing else — not its name, not its date. A **tree** lists one directory: for each entry a mode (`100644` for an ordinary file), a type, an object id and a name. A **commit** records one tree — the whole project at that moment — together with its parent commits, its author, its committer and a message. An **annotated tag** names one object and adds a tagger and a message (§7). Nothing in the store is a difference between versions: every commit points to a complete snapshot, and the diff that `git show` prints is computed on the spot by comparing two trees (Pro Git §10.2).

`git cat-file -p` prints any object. Right after RS1's first commit:

```bash
git cat-file -p HEAD
```

```text
tree 1d9c244b46fb16231817309f95c6a2fc9940ca88
author RS1 Student <student@example.com> 1772442000 +0000
committer RS1 Student <student@example.com> 1772442000 +0000

Start RS1: question, success rule and ignore list
```

```bash
git cat-file -p HEAD^{tree}
git hash-object README.md
```

```text
100644 blob fd587a49c772738351c884e9e630b6e93f509cfa	.gitignore
100644 blob 165de4c9b8c979226499ad72f3a21cff44a33850	README.md
165de4c9b8c979226499ad72f3a21cff44a33850
```

Read it from the bottom. `git hash-object` computes the id the file's bytes would get, without storing anything, and it is the id the tree lists for `README.md`. The tree names its two blobs; the commit names the tree. The first commit has no `parent` line; the second, 16fc8ef, has one, `parent c13c29840a58…`, and the merge of §4 has two. Author and committer each carry a name, an e-mail, the time in seconds since 1 January 1970 UTC and a time zone: 1772442000 +0000 is 2 March 2026, 09:00 UTC.

> **Object id, defined.** The **object id** of a Git object is a *name computed from the object's content* — the value of a hash function, not a counter, a file path or a storage location. Four conditions define it. It is computed from **the object's type, its length and its bytes, and nothing else**: where the file sits, what it is called and when it was stored do not enter, unless they are part of the content, as a commit's dates are. The same bytes give **the same id on every machine**, so two clones agree on the name of every object without talking to each other. Different bytes give **different ids** in practice: the 160-bit output of SHA-1 has $2^{160}\approx1.46\times10^{48}$ values, and Git carries protections against the known attacks on SHA-1 (Git's BreakingChanges document). And the id is **the object's address**: Git finds every object by its id, and stores a loose object as a zlib-compressed file under `.git/objects/`, in a directory named by the id's first two hex digits (Pro Git §10.2).
>
> $$\mathrm{id}(o)=\mathrm{SHA1}\big(\,t\ \Vert\ \text{space}\ \Vert\ n\ \Vert\ \text{NUL}\ \Vert\ b\,\big)$$
>
> where $t$ is the type word (`blob`, `tree`, `commit` or `tag`), $n$ the number of content bytes written in decimal, NUL the zero byte, $b$ the content and $\Vert$ concatenation — so the id is fixed by the bytes alone, since nothing else is hashed.
>
> - **Example**: `trials/pilot.csv` at pilot-v1 is 184 bytes and has the id 3a8cd7502be7ca376de2c3d6bd0da0e294e0a7e0; the block below computes it from RS1's twenty frozen forces. Write trial A1 as 8.2 N instead of 8.1 — same length, one digit changed — and the id becomes 764faff5109a118d1006f114e601f6bf846d4497, which Git's own `hash-object` confirms.
> - **Non-example**: a file's name. Rename `README.md` and its blob keeps the id 165de4c9…; two identical files anywhere in the project share one blob. What records the name is the tree.
> - **Non-example**: `165de4c`, the seven-digit form. It is a prefix that Git expands while it is unique, with at least 7 digits and more as the repository grows (git-describe documentation); a string that is unique today can become ambiguous in a larger repository. A results table carries all forty digits (§7).
> - **Why it matters**: an id recorded beside a result names the exact bytes of every file behind it. The same idea — name data by a hash of its content — is what a checksum beside a recorded bag or dataset does (§6).

The rule can be checked without Git. This block rebuilds the pilot's file from RS1's frozen forces and hashes it, then hashes the commit that pilot-v1 names, from the 248 bytes that `git cat-file -p 2006419` prints:

```python
import hashlib

def object_id(kind, body):
    """Git's name for an object: SHA-1 of '<kind> <size>', a zero byte, then the bytes."""
    return hashlib.sha1(kind.encode() + b" " + str(len(body)).encode() + b"\0" + body).hexdigest()

A = [8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3]     # RS1's frozen pilot, N
B = [6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6]
rows = ["arm,trial,peak_N"] + [f"{arm},{i},{f}" for arm, fs in (("A", A), ("B", B))
                                for i, f in enumerate(fs, 1)]
csv_bytes = ("\n".join(rows) + "\n").encode()
print("trials/pilot.csv  ", len(csv_bytes), "bytes  blob", object_id("blob", csv_bytes))

edited = csv_bytes.replace(b"A,1,8.1\n", b"A,1,8.2\n")          # one digit of one trial
print("with A1 = 8.2 N   ", len(edited), "bytes  blob", object_id("blob", edited))

commit_2006419 = (b"tree 4710a335a55ce7dfff33469e388465ec84eba622\n"
                  b"parent 882d5dd467643461dad24896321da388cec66f86\n"
                  b"author RS1 Student <student@example.com> 1773158400 +0000\n"
                  b"committer RS1 Student <student@example.com> 1773158400 +0000\n"
                  b"\n"
                  b"Record the pilot of B: ten trials\n")
print("pilot-v1's commit ", len(commit_2006419), "bytes  commit", object_id("commit", commit_2006419))
```

```text
trials/pilot.csv   184 bytes  blob 3a8cd7502be7ca376de2c3d6bd0da0e294e0a7e0
with A1 = 8.2 N    184 bytes  blob 764faff5109a118d1006f114e601f6bf846d4497
pilot-v1's commit  248 bytes  commit 20064191fe47e9c20677136f53f58a693e5aaf05
```

The first and last ids are the ones Git gave the file and the commit in RS1's repository.

> **Commit, defined.** A **commit** is an *object that records one snapshot of the project and where it came from* — not a diff, not a file, not a branch. Four conditions. It names **exactly one tree**, the snapshot of every tracked file. It names **its parents** by id: none for the first commit, one for an ordinary commit, two or more for a merge. It carries an **author and a committer** — each a name, an e-mail, a time in seconds since 1970 and a time zone — and a **message**. And its name is **the object id of those bytes**, so it depends on the parents' ids, which depend on their parents' in turn.
>
> $$h(c)=\mathrm{id}\big(\text{commit};\ h(T_c),\ h(p_1),\dots,h(p_q),\ a_c,\ k_c,\ m_c\big)$$
>
> where $T_c$ is the commit's tree, $p_1,\dots,p_q$ its parents, $a_c$ and $k_c$ its author and committer lines and $m_c$ its message — so $h(c)$ depends on every ancestor, since each $h(p_i)$ was computed the same way from its own parents.
>
> - **Example**: 2006419, the commit pilot-v1 names: tree 4710a335…, parent 882d5dd…, author and committer RS1 Student at 1773158400 (10 March 2026, 16:00 UTC), message "Record the pilot of B: ten trials" — 248 bytes whose id the block above reproduces. Had trial A1 been written 8.2 N in aebf24a, the blob, the `trials/` tree and the root tree would differ, so aebf24a would have another id, and so would every commit that has it as an ancestor: 10 of the 15 (the Worked case counts them).
> - **Non-example**: the same content committed twice. The Draw problem replays B's branch onto main instead of merging it: the final snapshot is the same tree, e3238a51…, yet every commit after the replay has a new id, because its parent changed.
> - **Non-example**: "a commit is the change I made". `git show` prints a change, computed by comparing the commit's tree with its parent's; the commit itself stores the whole snapshot, which is why checking out an old commit writes that snapshot directly, without replaying the changes that led to it.
> - **Why it matters**: forty hex digits written in a results table fix the code, the small data and the entire history behind the number at once. Nobody can alter an ancestor and keep the id — a changed history is a different history, with different names.

**Which hash.** Git names objects with SHA-1 by default, 40 hexadecimal digits; SHA-256, with 64-digit ids, exists and is planned as the default for new repositories in Git 3.0. Nothing on this page depends on which: every rule holds with 64 digits in place of 40.

> [!note]- Deeper · 더 깊이
> A SHA-256 repository is made with `git init --object-format=sha256`, and the documentation states that SHA-256 and SHA-1 repositories cannot yet exchange objects with each other (git-init, 2.54.0). Git 3.0 is planned to make SHA-256 the default for newly created repositories and `main` the default first branch, with no release date announced (BreakingChanges, 2.55.0).

**Why history is a graph with no loops.** A commit can only name parents that already exist, since their ids are part of its bytes. So following parent links always goes back in time and can never return to where it started: the history is a directed acyclic graph, a DAG ([[02-foundations/algorithms/graph-algorithms|11.6 §3]]), in which a merge is a node with two outgoing edges. Every picture of history on this page is that graph.

### 2. The working tree, the index and the history

*In one sentence:* a file lives in three places — the working tree you edit, the index that holds the next commit, and the history of commits — and `add`, `commit`, `status` and `diff` each move content between two of them or compare two of them.

Why a middle stage between your files and the history? Because one commit should record one intention — a gain tuned, a trial recorded — even while your directory holds several unfinished edits. Pro Git calls the three places the three trees (§7.7). The **working tree** is the ordinary directory of files, where you edit and run things. The **history** is the chain of commits; `HEAD` is the one you are on (§3). Between them sits the **index**, the proposed next commit. `git add path` copies a file's current bytes from the working tree into the index. `git commit` turns the index — only the index — into a new commit's tree. And `git status` compares the three.

RS1's commit f41f0b6 shows all of it. On branch impedance-b, both the gains in `controllers/impedance.py` and the status line in `README.md` have been edited:

```bash
git status
```

```text
On branch impedance-b
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md
	modified:   controllers/impedance.py

no changes added to commit (use "git add" and/or "git commit -a")
```

Stage the controller only, and look again:

```bash
git add controllers/impedance.py
git status
```

```text
On branch impedance-b
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   controllers/impedance.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

```

The two diffs now show different things. `git diff --staged` compares the index with `HEAD` — what the next commit will contain:

```bash
git diff --staged
```

```text
diff --git a/controllers/impedance.py b/controllers/impedance.py
index 0af9897..3884147 100644
--- a/controllers/impedance.py
+++ b/controllers/impedance.py
@@ -1,7 +1,7 @@
 """Controller B: Cartesian impedance control at the tool tip."""
 
-K_N_PER_M = 500.0     # stiffness along the approach axis
-D_NS_PER_M = 30.0     # damping along the approach axis
+K_N_PER_M = 300.0     # stiffness along the approach axis
+D_NS_PER_M = 25.0     # damping along the approach axis
 
 
 def tip_force(x, dx, x_ref):
```

and `git diff` with no argument compares the working tree with the index — what is still unstaged:

```bash
git diff
```

```text
diff --git a/README.md b/README.md
index 165de4c..ceeb665 100644
--- a/README.md
+++ b/README.md
@@ -6,4 +6,4 @@ Question: does impedance control (B) make the planar arm's contact with a
 Trial: one approach that ends in contact.
 Success: peak contact force at most 10 N.
 
-Status: repository started.
+Status: B tuned on the rig (K = 300 N/m, D = 25 N s/m).
```

The `index 165de4c..ceeb665` line is §1 again: the diff names the old and the new blob of `README.md`, and 165de4c is the blob `git hash-object` printed. Stage the README too, and commit both as one change with a message that says what changed, with numbers:

```bash
git add README.md
git commit -m "Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m"
```

```text
[impedance-b f41f0b6] Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m
 2 files changed, 3 insertions(+), 3 deletions(-)
```

> **The index, defined.** The **index** (also called the staging area, stored in the file `.git/index`) is *a table from each tracked path to one blob id and mode: the next commit's snapshot, written down before the commit exists* — a snapshot, not a list of changes, and not the working tree. Three conditions. `git add` **writes the file's current bytes** as a blob and points the path's entry at it, so an edit made after `git add` is not in the index until it is added again. `git commit` **records the index and nothing else** as the new commit's tree. And `git status` **reports two comparisons**, index against `HEAD` ("Changes to be committed") and working tree against index ("Changes not staged for commit"), plus the untracked files that neither holds.
>
> $$T_{\text{next}}=I,\qquad \text{staged}=\Delta\big(T_{\text{HEAD}},\,I\big),\qquad \text{unstaged}=\Delta\big(I,\,W\big)$$
>
> where $I$ is the index, $W$ the working tree, $T_{\text{HEAD}}$ the tree of the current commit and $\Delta$ the set of paths whose bytes differ — so a commit contains exactly what was staged, since its tree is written from $I$.
>
> - **Example**: f41f0b6. After `git add controllers/impedance.py`, $\Delta(T_{\text{HEAD}},I)$ was the controller file, with the gains, and $\Delta(I,W)$ the README, with the status line; the commit took both only because the README was added before `git commit`.
> - **Non-example**: `git diff` read as "what changed since the last commit". It compares the working tree with the index, so a staged change vanishes from it — the gains are missing from the second diff above although they differ from `HEAD`. `git diff HEAD` compares the working tree with the last commit.
> - **Why it matters**: the index lets one commit carry one intention — the tuning and the line recording it — while an experiment in another file stays out. It also means the working tree can match no commit at all, and a table computed from such a tree is a table no commit can reproduce (§7).

`git log` walks the history from `HEAD` back through parents; `git log --oneline` prints one line per commit, the short id and the message's first line, and `--graph` draws the parent links, as in §3. `git show <commit>` prints one commit with its diff against its parent.

A commit is cheap and permanent, so commit when a piece of work makes sense on its own — a controller added, a gain tuned, a pilot's numbers recorded — and write the message for the person who will read the log in a year, often you: what changed and, where there are numbers, which. "Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m" tells a reviewer what "fix" or "update" never will.

### 3. Branches and HEAD

*In one sentence:* a branch is a movable name for one commit, `HEAD` says which branch the next commit will move, and a line of work kept on its own branch leaves every other line runnable.

The problem a branch solves: you want to develop and tune controller B without breaking the analysis that already runs on main, and bring the two together later at one recorded point. On 4 March the analysis script was committed on `main` as 2452d15, and work on controller B began on its own branch:

```bash
git switch -c impedance-b
git branch
cat .git/HEAD
cat .git/refs/heads/main
cat .git/refs/heads/impedance-b
```

```text
Switched to a new branch 'impedance-b'
* impedance-b
  main
ref: refs/heads/impedance-b
2452d15b3041b365f1bd922152336d1840fc19f6
2452d15b3041b365f1bd922152336d1840fc19f6
```

That is all a branch is: a file holding one commit id, forty hex digits and a newline, 41 bytes (Pro Git §3.1). Creating impedance-b wrote one such file; nothing was copied. `HEAD` is a file too, and it names the branch, not a commit. Two commits later on impedance-b, and one on main (the pilot of A, recorded while B was being tuned), the two lines have diverged:

```bash
git log --oneline --graph --decorate --all
```

```text
* f41f0b6 (impedance-b) Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m
* 757338e Add controller B: impedance control
| * aebf24a (HEAD -> main) Record the pilot of A: ten trials
|/  
* 2452d15 Add the analysis script that prints the results table
* 16fc8ef Add controller A: position control with a 6 N stop
* c13c298 Start RS1: question, success rule and ignore list
```

`--decorate` prints the names beside the commits they point to; Git prints them by default only when the output is a terminal, so the option is written out here.

> **Branch, defined.** A **branch** is *a reference: a movable name that holds the id of one commit, its tip* — not a copy of the files, not a folder, and not a set of commits stored anywhere. Four conditions. It names **exactly one commit**. Committing while it is checked out **creates a commit whose parent is the old tip and moves the branch to it**; no other branch moves. The commits "on" a branch are its **tip and everything reachable from the tip by parent links**, so one commit can be on several branches at once. And **`HEAD` names the checked-out branch** (`ref: refs/heads/impedance-b`), which is how Git knows which branch the next commit moves; when `HEAD` holds a commit id instead, as after checking out a tag or a bare id, it is *detached*, and a commit made there belongs to no branch (Pro Git §2.6).
>
> $$b\leftarrow c',\qquad \mathrm{parents}(c')=\big(b_{\text{old}}\big),\qquad \mathrm{on}(b)=\{b\}\cup\mathrm{anc}(b)$$
>
> where $b$ is the branch `HEAD` names, $c'$ the new commit and $\mathrm{anc}(b)$ every commit reachable from $b$'s tip — so one commit moves exactly one branch, since `HEAD` names only one.
>
> - **Example**: impedance-b started as 2452d15, the same 41 bytes as main; after 757338e and f41f0b6 it holds f41f0b6, while main moved from 2452d15 to aebf24a on its own commit. `git log --oneline aebf24a..f41f0b6` — the commits on impedance-b that main does not have — prints exactly those two.
> - **Non-example**: a folder per version (`controllers_v2/`, `summarize_final.py`). It copies files, has no parent links and cannot be merged; a branch costs 41 bytes and keeps one file per path.
> - **Non-example**: a commit made on a detached `HEAD`, for instance while `git bisect` has checked out an old commit (§8). No name points to it, so it is left behind as soon as you check out anything else — give it a branch first (`git switch -c <name>`).
> - **Why it matters**: B's controller was developed and tuned on impedance-b while main kept a working analysis and A's pilot data; nothing on main could be broken by an unfinished controller, and the two lines met at one recorded point, the merge of §4.

`git switch <branch>` moves `HEAD` to another branch and makes the working tree and the index match that branch's tip; `git switch -c <name>` creates the branch at the current commit first. Git refuses to switch when an uncommitted change would be overwritten, so commit (or stash) first. In the graph above, `HEAD -> main` says that `HEAD` names main and main names aebf24a. Every figure of history on this page follows `git log --graph`: newest on top, each commit joined to its parents below it.

### 4. Merging, conflicts, and rebase in one paragraph

*In one sentence:* a merge combines two lines of work by comparing each with their best common ancestor, takes every change that only one side made, stops where both sides changed the same lines, and records the result as a commit with two parents.

Two lines of work, each of which changed the project, must become one without losing either side's changes and without guessing where they disagree. Before merging, find what the two tips have in common and what each side brought:

```bash
git merge-base aebf24a f41f0b6
git diff --stat 2452d15 aebf24a
git diff --stat 2452d15 f41f0b6
```

```text
2452d15b3041b365f1bd922152336d1840fc19f6
 README.md        |  2 +-
 trials/pilot.csv | 11 +++++++++++
 2 files changed, 12 insertions(+), 1 deletion(-)
 README.md                | 2 +-
 controllers/impedance.py | 9 +++++++++
 2 files changed, 10 insertions(+), 1 deletion(-)
```

The merge base is 2452d15, where impedance-b left main. Main brought the pilot file; the branch brought controller B; and both changed one line of `README.md`, the status line. On main:

```bash
git merge impedance-b
```

```text
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
git status
cat README.md
```

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Changes to be committed:
	new file:   controllers/impedance.py

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   README.md

# RS1: impedance against position control at a panel

Question: does impedance control (B) make the planar arm's contact with a
400 N/m panel safer than position control with a force-threshold stop (A)?

Trial: one approach that ends in contact.
Success: peak contact force at most 10 N.

<<<<<<< HEAD
Status: pilot of A recorded (10 trials).
=======
Status: B tuned on the rig (K = 300 N/m, D = 25 N s/m).
>>>>>>> impedance-b
```

Git merged what it could: controller B is already staged. Between `<<<<<<< HEAD` and `=======` stands main's version of the conflicting line, between `=======` and `>>>>>>> impedance-b` the branch's. Resolving means editing the file into what should be true — here both facts, `Status: pilot of A recorded (10 trials); B tuned on the rig (K = 300 N/m, D = 25 N s/m).` — and marking it resolved by staging it:

```bash
git add README.md
git commit -m "Merge branch 'impedance-b'"
git cat-file -p HEAD
```

```text
[main 882d5dd] Merge branch 'impedance-b'
tree 3bb71c434c8278a78079be9f95d4c3c080909c25
parent aebf24a5b39f78495d50d3ff16d098b507abaf3f
parent f41f0b663d0c48814e4c98f65690c817a01384c5
author RS1 Student <student@example.com> 1773050400 +0000
committer RS1 Student <student@example.com> 1773050400 +0000

Merge branch 'impedance-b'
```

Two `parent` lines: the first is the branch you were on, the second the branch you merged. If the merge had not conflicted, `git merge` would have written this commit by itself.

> **Three-way merge, defined.** A **three-way merge** is *an operation that builds one snapshot from two commits and their merge base, and records it as a commit with both as parents* — not a concatenation of the two histories, and not "the newer version wins". Four conditions. The **merge base** $B$ is a best common ancestor of the two tips, "ours" $O$ (the branch `HEAD` names) and "theirs" $T$; `git merge-base` prints it. The files are compared **region by region against $B$**: a side that changed a region wins over a side that left it as in $B$. Where **both sides changed the same region differently**, Git writes both versions between conflict markers and stops; you edit, `git add` and commit. And the result is a **merge commit with parents $(O, T)$** — unless $T$ already contains $O$, in which case the branch just moves forward to $T$ and no merge commit is made (a fast-forward, Pro Git §3.2).
>
> $$R_r=\begin{cases}O_r & \text{if } T_r=B_r \text{ or } O_r=T_r\\ T_r & \text{if } O_r=B_r\\ \text{conflict} & \text{otherwise}\end{cases}$$
>
> where $r$ is one region of one file and $O_r$, $T_r$, $B_r$ its three versions — so Git stops only where both sides changed the same region to different text, since every other case has an answer.
>
> - **Example**: 882d5dd. `controllers/impedance.py` exists only in $T$, so it is taken; `trials/pilot.csv` only in $O$, so it is kept; the status line of `README.md` differs from $B$ on both sides and in different ways, so it is the one conflict.
> - **Non-example**: a merge without conflicts is not a correct merge. If main had renamed the function `load` in `analysis/summarize.py` while the branch added a script calling `load`, every region would merge cleanly and the result would fail when run. Git compares text, not meaning, so run the analysis after every merge.
> - **Non-example**: a fast-forward. In the rebased history of the problem set, `git merge impedance-b` prints `Fast-forward`: $O$ was an ancestor of $T$, nothing had to be combined, and no merge commit exists.
> - **Why it matters**: the merge commit is a recorded meeting point — from 882d5dd on, the analysis, controller B and A's pilot data are known to work together — and a conflict is Git declining to guess what your lab meant.

**Rebase, in one paragraph.** Instead of merging, `git rebase main` on impedance-b replays the branch's commits one by one on top of main's tip. The replayed commits have the same changes and messages but new parents, so they are new commits with new ids, and the history becomes a straight line; the final snapshot is the same as a merge would give — in the problem set's rebased RS1 the last tree is e3238a51…, exactly as in the merged one. The rule that keeps this safe is Pro Git's (§3.6), in short: never rebase commits that already exist outside your own repository, because other people have built on the old ids. Rebasing your own unpublished branch before you share it is fine; rebasing — or amending, or squashing — commits that others have fetched rewrites their history under them, and the Interpret problem shows what that looks like from their side.

### 5. Remotes, pushes and pull requests

*In one sentence:* a remote is another repository you exchange commits with — the lab's server, GitHub — and every exchange is safe as long as a shared branch only ever moves forward.

Your commits must reach the lab's server and your collaborators, and theirs must reach you, without anyone's work being overwritten on the way. A **remote** is a named URL. `git clone` copies a whole repository — every commit, not just the latest files — and records where it came from as the remote `origin`. RS1's lab server here is a bare repository (one with no working tree, made for sharing), and the student works in a clone of it:

```bash
git clone --bare rs1 lab.git
git clone lab.git student
```

```text
Cloning into bare repository 'lab.git'...
done.
Cloning into 'student'...
done.
```

(Here the "server" is a directory beside the clones, and each clone's `origin` was set to the relative path `../lab.git`; on a team, `origin` is a URL on GitHub or the lab's server.) Inside the clone:

```bash
git remote -v
git branch -a
git status
```

```text
origin	../lab.git (fetch)
origin	../lab.git (push)
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/impedance-b
  remotes/origin/main
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`origin/main` is a **remote-tracking branch**: your repository's record of where main was on the server the last time you talked to it. You cannot commit to it; Git moves it when you exchange data (Pro Git §3.5). "Up to date" in `git status` compares main with that record, not with the server itself. Three commands do the exchanging, and tags follow a rule of their own:

- `git fetch` downloads the commits you do not have and moves the remote-tracking branches. It never touches your branches or your working tree.
- `git pull` is a fetch followed by integrating the upstream branch into yours. With no configuration it only fast-forwards; when the two have diverged it stops and asks you to choose between merging and rebasing (git-pull documentation, and the output below).
- `git push` sends your commits and asks the server to move its branch to your tip. The server accepts only a fast-forward — its current tip must be an ancestor of yours (git-push, PUSH RULES) — unless you force it.
- Tags travel only when asked: `git push origin pilot-v1`, or `--tags` for all (Pro Git §2.6).

No command on this page pushes to anything, so the pushes are shown as the documentation gives them:

```bash
# not run here: these send commits to the lab's server (git-push documentation)
git push origin main                      # accepted only as a fast-forward
git push --force-with-lease origin main   # overwrite, but only if origin/main is still what you last fetched
```

A lab-mate who squashed main's last two shared commits into one, in a clone of the same server, sees what a push would do before trying it:

```bash
git reset --soft HEAD~2
git commit -m "Add the figure script and fix the trial parser"
git status
```

```text
[main 41cea18] Add the figure script and fix the trial parser
 2 files changed, 9 insertions(+), 5 deletions(-)
 create mode 100644 analysis/figure.py
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 2 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
```

"1 and 2": the lab-mate has 41cea18, which the server lacks, and the server has 3568180 and ea13bc4, which the lab-mate's main no longer contains. A plain push is refused; `--force` would move the server's main to 41cea18 and drop the other two from everyone's future. On a clone whose main has diverged from `origin/main` in the same way — the student's, in the Interpret problem — `git pull` stops too (output trimmed to the lines that matter):

```bash
git pull
```

```text
hint: You have divergent branches and need to specify how to reconcile them.
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
fatal: Need to specify how to reconcile divergent branches.
```

The rule behind all of this has a name. A **fast-forward** is an update that moves a reference from commit $A$ to a commit $B$ that has $A$ in its history, so every commit the old tip reached is still reached and history only grows; in counts, $A\to B$ is one exactly when $|B..A|=0$, the number `git rev-list --count B..A` prints. A push to a branch is accepted only if it is a fast-forward, unless forced, because any other update "will lose history" (git-push) for everyone who builds on the new tip. A clone that is "behind 'origin/main' by 1 commit, and can be fast-forwarded" (§8 prints this) loses nothing to `git pull`. The lab-mate's ea13bc4 → 41cea18 is not one — the squash replaced ea13bc4, so $|41cea18..ea13bc4|=2$ (3568180 and ea13bc4) — and only a forced update can make it; the next person who pulls with a merge then brings the dropped commits back as duplicates (Pro Git §3.6). GitHub blocks force pushes on protected branches by default.

**Pull requests and review.** On GitHub the everyday way to put work onto a shared main is not to push to main at all. You push your branch, say impedance-b, and open a **pull request**: a proposal to merge that branch (the head) into another (the base), shown as one diff with room for discussion. Reviewers leave one of three kinds of review — comment, approve, or request changes — and a repository's administrators can protect main so that a pull request needs approving reviews before it can be merged, and so that nobody force-pushes or deletes it (GitHub Docs, "About pull request reviews" and "About protected branches"). A draft pull request shares work in progress and cannot be merged. For a study this is where a second person reads a change to the analysis before any number in the paper depends on it — and where the diff of a regression like dda4b0f's (§8) had its best chance to be caught.

### 6. What must not be committed

*In one sentence:* anything committed stays in the history of every clone for good, so large recordings, trained weights and secrets must never enter a commit, and deleting them in a later commit removes nothing.

Once something is committed and shared it is, for practical purposes, permanent: a 60 MiB bag or a password committed by accident cannot simply be deleted. The defence is to keep such files out in the first place.

**The ignore list.** A `.gitignore` file lists patterns of files Git should leave untracked; it is committed, so every clone shares it (gitignore documentation). RS1's, from its first commit:

```text
# colcon build outputs
build/
install/
log/

# trial recordings live on the lab's data server, not in Git
bags/
*.mcap
*.db3

# model weights and large arrays
*.pt
*.npz

# Python caches
__pycache__/

# credentials never enter the repository
.env
```

A trailing slash matches only a directory; `*` matches anything except a slash; a pattern with no slash other than a trailing one applies at every depth; and a line starting with `#` is a comment. The ignore list only affects **untracked** files: a file that is already tracked stays tracked until `git rm --cached` removes it from the index (gitignore documentation). The colcon directories are the ones [[04-robotics/ros2/workspaces-packages-launch|25.4 §2]] says to ignore. What the list catches, and what it misses, in a clone of RS1 with three new files:

```bash
git status --short --ignored
git check-ignore -v bags/pilot_A01/pilot_A01_0.mcap config/.env config/dashboard.env
```

```text
?? config/
!! bags/
!! config/.env
.gitignore:7:bags/	bags/pilot_A01/pilot_A01_0.mcap
.gitignore:19:.env	config/.env
```

`!!` marks ignored paths and `??` untracked ones. `git check-ignore -v` names the rule that matched — `bags/` on line 7, `.env` on line 19 — and says nothing about `config/dashboard.env`: the pattern `.env` matches a file named exactly `.env`, so a credentials file called `dashboard.env` is not ignored at all, and `git add config/` would stage it for the next commit. When a path is ignored, Git refuses to add it:

```bash
git add trials/B07.mcap
```

```text
The following paths are ignored by one of your .gitignore files:
trials/B07.mcap
hint: Use -f if you really want to add them.
hint: Disable this message with "git config set advice.addIgnoredFile false"
```

— until someone uses `-f`.

**Why deleting later does not help.** Git keeps an object as long as something leads to it. The first version of the pilot file, with A's ten rows only, is still in RS1's repository although main's file now has twenty:

```bash
git log --oneline -- trials/pilot.csv
git show aebf24a:trials/pilot.csv
```

```text
2006419 Record the pilot of B: ten trials
aebf24a Record the pilot of A: ten trials
arm,trial,peak_N
A,1,8.1
A,2,9.4
A,3,12.6
A,4,9.8
A,5,13.9
A,6,7.7
A,7,9.9
A,8,9.1
A,9,14.8
A,10,11.3
```

> **Reachable, defined.** An object is **reachable** in a repository when *some reference of that repository leads to it* — a relation between one object and one repository's references, not a property of the object alone. Four conditions. The walk **starts from a reference**: a branch, a tag, a remote-tracking branch, the index, a reflog entry, or anything else under `refs/` (git-gc documentation). It **follows every link**: a commit to its parents and its tree, a tree to its entries, a tag to its object. An object stays in the repository **as long as it is reachable** there. And **every clone has its own references**, so reachability — and with it deletion — is decided clone by clone.
>
> $$\mathrm{kept}_{\mathcal R}(o)\iff \exists\,r\in\mathcal R:\ o\in\mathrm{reach}(r)$$
>
> where $\mathcal R$ is one repository's set of references and $\mathrm{reach}(r)$ everything found from $r$ by following parents, trees, entries and tag targets — so an object disappears only when no reference in that repository leads to it, and never from a clone just because it left yours.
>
> - **Example**: the 11-line pilot file above. Main reaches 2006419, 2006419 reaches its ancestor aebf24a, and aebf24a's tree reaches that blob; `git show aebf24a:trials/pilot.csv` prints it.
> - **Non-example**: "I deleted the file in the next commit." The new commit's tree lacks it, but the old commit is still an ancestor of main, so its blob stays reachable from main — in your clone, on the server and in every clone made since.
> - **Why it matters**: a bag or a key, once committed and fetched, is in the history of every copy. Removing it means rewriting the history in which it appears, which changes the id of that commit and of every commit after it (§1), and it cannot reach the clones and forks other people already have (GitHub Docs, "Removing sensitive data"). Even locally, `git gc` keeps what the reflogs still reach — by default for 90 days, and for 30 days when the branch's current tip no longer reaches the entry (git-gc documentation).

**Recordings, datasets, weights.** A bag (a rosbag2 directory, [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]), a dataset or a checkpoint is large, binary and written once. GitHub warns when you add a file larger than 50 MiB and blocks files larger than 100 MiB, and recommends keeping a repository ideally under 1 GB and in any case under 5 GB (GitHub Docs, "About large files on GitHub") — and every clone downloads the whole history, however old. Keep recordings on the lab's data server, and commit what identifies them: the bag's name and a checksum of its bytes, which names the data the way an object id names a blob (§1). Git LFS, which stores large files outside the repository and commits a small pointer instead, and GitHub releases are the two routes GitHub itself names for large binaries; this page does not teach either. The Worked case prices RS1's 84 bags. What a bag, a Parquet table or an HDF5 file holds is [[02-foundations/tools/config-data-formats|12.4 Config and Data Formats §8]]; a rig's CAD files belong in the repository too, the native file with its exports under a revision name ([[02-foundations/tools/mechanical-design-fabrication|12.9 Mechanical Design and Fabrication §1]]).

**Secrets.** A token, a password, a private key or a cloud credential never goes into a tracked file. Code reads it from the environment (`os.environ["RS1_DASHBOARD_TOKEN"]`) or from an untracked file whose exact name the ignore list covers. GitHub's push protection blocks pushes that contain secrets it recognizes, and is on by default for pushes to public repositories — but only for the patterns it knows, and anyone with write access can bypass it with a stated reason (GitHub Docs, "About push protection"). If a key does get committed, GitHub's own order is the right one: **revoke or rotate the key first** — a revoked key is harmless wherever it lies — and only then decide whether the history is worth rewriting with a tool such as `git filter-repo`, knowing that every later commit's id changes and that forks and existing clones keep the old commits.

### 7. A tag per experiment, a commit in every table

*In one sentence:* give every experiment an annotated tag, print the commit that produced each results table on the table itself, and treat a `-dirty` stamp as a table that no commit can reproduce.

Months later a reviewer asks which code produced Table 1, and "the version from around March" is not an answer. Two habits give a better one.

**A tag per experiment.** A tag is a name for one commit that, unlike a branch, never moves. An **annotated tag** is a full object with its own id, a tagger, a date and a message; a lightweight tag is only a name (Pro Git §2.6). The Git manual means annotated tags for releases and lightweight ones for private or temporary labels, and `git describe` ignores lightweight tags unless told otherwise (git-tag, git-describe) — so an experiment gets an annotated tag. RS1 has two, each with a different meaning written into its message: pilot-v1 marks the commit whose table holds the pilot, and study-v1 the code frozen before the main study's first trial.

```bash
git tag -a pilot-v1 -m "Pilot: 10 trials per arm; tuning data, not a test"
git cat-file -p pilot-v1
git describe --long
```

```text
object 20064191fe47e9c20677136f53f58a693e5aaf05
type commit
tag pilot-v1
tagger RS1 Student <student@example.com> 1773160200 +0000

Pilot: 10 trials per arm; tuning data, not a test
pilot-v1-0-g2006419
```

Two rules keep tags trustworthy. A tag others have fetched is **never moved**: `git fetch` does not replace a tag someone already has, so moving it leaves two "pilot-v1"s in the world, and the manual's advice is to admit the mistake and use a new name, pilot-v1.1 (git-tag, "On Re-tagging"). And tags are **pushed explicitly**, since `git push` does not send them by default (§5). Which tag goes where, and what else a study must record beside its code — seeds, calibration, configuration, raw logs, exclusions — is [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §7]]; its vocabulary of repeatable, reproducible and replicable is its §6.

**A commit in every table.** RS1's analysis script prints the version of the code that runs it before it prints any number. The two lines that do it, from `analysis/summarize.py`:

```python
# not-run: an excerpt of analysis/summarize.py in RS1's repository; it calls git
def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def main():
    print("code:  ", git("describe", "--long", "--always", "--dirty"))
    print("commit:", git("rev-parse", "HEAD"))
```

At pilot-v1 it prints the pilot table — the one [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]] turns into the paper's Table 1:

```bash
python3 analysis/summarize.py
```

```text
code:   pilot-v1-0-g2006419
commit: 20064191fe47e9c20677136f53f58a693e5aaf05
arm   n   success   mean (N)   sd (N)
A    10    6/10      10.66     2.414
B    10    9/10       7.50     1.356
```

The first line is for people, the second for machines: forty digits never become ambiguous, as an abbreviation can (§1). `--long` keeps the id even at a tagged commit, where plain `git describe` would print only `pilot-v1`; `--always` falls back to a bare id where no tag is reachable.

> **The describe stamp, defined.** The **describe stamp** of a commit is *a human-readable name computed from the history: the nearest tag, how many commits lie beyond it, and the commit's abbreviated id* — a computed name, not a stored one, and not a version number anyone assigned. Four conditions. $t$ is the **most recent annotated tag reachable from the commit** — among several, the one with the fewest commits between. $n$ is **the number of commits reachable from the commit and not from the tag**, exactly what `git log t..c` would list. `g` plus **at least 7 hex digits** of the commit's id follow, more as the repository grows. And with `--dirty`, **`-dirty` is appended when a tracked file differs from the commit** (git-describe documentation).
>
> $$\mathrm{describe}(c)=t\text{-}n\text{-g}\,\bar h(c)\,[\text{-dirty}],\qquad n=\big|\,t\,..\,c\,\big|$$
>
> where $\bar h(c)$ is the abbreviated id and $|t..c|$ the count of commits reachable from $c$ and not from $t$ — so the stamp names $c$ exactly while saying how far it lies from the tagged experiment, since the id is in it.
>
> - **Example**: HEAD, `study-v1-3-gea13bc4`. study-v1 names 6321a22, and three commits — b659311, 3568180 and ea13bc4 — are reachable from ea13bc4 and not from 6321a22.
> - **Non-example**: an untracked file. In a clone of RS1 with a new, untracked `notes.txt`, `git describe --long --dirty` still printed `study-v1-3-gea13bc4`, with no `-dirty` (the run below): a table computed by an untracked script carries a clean stamp. `git status --porcelain` lists untracked files too, so the check before a run is that it prints nothing.
> - **Non-example**: n as a distance along main. Across a merge, n counts the merged branch's commits as well; the Derive problem works one out.
> - **Why it matters**: the stamp on a table is the address of the code that made it. A reader who sees `study-v1-1-gb659311` beside A's 9 trials knows exactly which commit to check out to see why (§8).

The run behind the first non-example — an untracked file, then an edited one:

```bash
git describe --long --dirty
echo "draft" > notes.txt
git describe --long --dirty
git status --porcelain
```

```text
study-v1-3-gea13bc4
study-v1-3-gea13bc4
?? notes.txt
```

```bash
sed -e 's/^LIMIT_N = 10.0 /LIMIT_N = 12.0 /' analysis/summarize.py > tmp && mv tmp analysis/summarize.py
git describe --long --dirty
git status --porcelain
```

```text
study-v1-3-gea13bc4-dirty
 M analysis/summarize.py
?? notes.txt
```

Changing the success limit to 12 N in the working tree makes the stamp `-dirty`: a table printed now would carry numbers from code that exists in no commit. (The edit goes to a new file that is then renamed, because in-place editing, `sed -i`, is spelled differently in Ubuntu's GNU `sed` and macOS's BSD `sed`.) The protocol's pre-trial checklist — commit 6321a22 — asks for exactly this before trial 1: write the stamp into the trial log, and refuse to start if it ends in `-dirty`. [[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]] adds the other inputs a re-run needs — the container, the bag, the parameters and the command — to make a *pinned run*; the commit is the first of them.

### 8. Finding the commit that broke a result, and undoing it

*In one sentence:* when a number changes and nobody knows why, `git bisect` finds the first commit that changed it in about $\log_2 N$ tests, and `git revert` undoes that commit by adding a new one, never by removing history.

**The symptom.** On 25 March the results section was drafted, and the table printed there did not match the pilot:

```bash
python3 analysis/summarize.py
```

```text
code:   study-v1-1-gb659311
commit: b659311c257a605d90be65f1004a5652967561cc
arm   n   success   mean (N)   sd (N)
A     9    5/9       10.94     2.377
B    10    9/10       7.50     1.356
```

A has 9 trials instead of 10. The stamp says which commit printed the table (b659311), not which commit broke it: the table at pilot-v1 was right, and by the time the search starts two days later, from the figure script's commit 3568180, six commits lie after pilot-v1.

**The test.** Bisection needs a command that says good or bad for any commit, and the same command for every commit — so it lives outside the repository, beside it, where checking out old commits cannot change it. It exits 0 when the pilot row reproduces and 1 when it does not:

```python
# not-run: pilot_check.py, run by git bisect inside RS1's repository
"""Bisect test for RS1: exit 0 if the pilot table reproduces, 1 if it does not."""
import subprocess
import sys

out = subprocess.run([sys.executable, "analysis/summarize.py"],
                     capture_output=True, text=True).stdout
row_a = next(line.split() for line in out.splitlines() if line.startswith("A "))
sys.exit(0 if row_a[1:4] == ["10", "6/10", "10.66"] else 1)
```

`git bisect run` reads the exit status: 0 means good, 1 to 127 except 125 means bad, and 125 means "cannot test this one, skip it" (git-bisect documentation). With 3568180 as `HEAD`:

```bash
git rev-list --count pilot-v1..HEAD
git bisect start HEAD pilot-v1
git bisect run python3 ../pilot_check.py
git bisect reset
```

```text
6
Bisecting: 2 revisions left to test after this (roughly 2 steps)
[041fe2fa6e2b08158d00707dd65cb94ae4a3d22b] Draft the methods section
running 'python3' '../pilot_check.py'
Bisecting: 0 revisions left to test after this (roughly 1 step)
[dda4b0fb5c300a860c8f25b0ab0379855cd581d6] Parse trials without the csv module
running 'python3' '../pilot_check.py'
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[a0cd3a3f2764283da8b096b5dabe34666ee554e6] Write the main-study protocol: 32 trials per arm
running 'python3' '../pilot_check.py'
dda4b0fb5c300a860c8f25b0ab0379855cd581d6 is the first bad commit
bisect found first bad commit
Previous HEAD position was a0cd3a3 Write the main-study protocol: 32 trials per arm
Switched to branch 'main'
```

(Trimmed: after "is the first bad commit" Git also printed the commit's header and its one-file diffstat.) `git bisect start HEAD pilot-v1` names the bad commit first and the good one second, and checks out a commit in the middle; "roughly 2 steps" counts the tests still to come after this one. Three tests: 041fe2f bad, dda4b0f bad, a0cd3a3 good — so the first bad commit is dda4b0f. `git bisect reset` returns to the branch you started from. What the commit did:

```bash
git show dda4b0f
```

```text
commit dda4b0fb5c300a860c8f25b0ab0379855cd581d6
Author: RS1 Student <student@example.com>
Date:   Wed Mar 18 13:00:00 2026 +0000

    Parse trials without the csv module

diff --git a/analysis/summarize.py b/analysis/summarize.py
index cdf03ec..f01152c 100644
--- a/analysis/summarize.py
+++ b/analysis/summarize.py
@@ -1,5 +1,4 @@
 """Print RS1's results table from trials/pilot.csv, stamped with the code version."""
-import csv
 import statistics
 import subprocess
 
@@ -12,9 +11,11 @@ def git(*args):
 
 def load(path):
     peaks = {}
-    with open(path, newline="") as f:
-        for row in csv.DictReader(f):
-            peaks.setdefault(row["arm"], []).append(float(row["peak_N"]))
+    with open(path) as f:
+        lines = f.read().splitlines()[2:]      # skip the header
+    for line in lines:
+        arm, trial, peak = line.split(",")
+        peaks.setdefault(arm, []).append(float(peak))
     return peaks
```

(Trimmed: two unchanged context lines at the end.) `[2:]` skips two lines, the header and trial A1; `[1:]` would have skipped the header only. One character, found in three tests.

> **Bisection, defined.** **Bisection** (`git bisect`) is *a search procedure: binary search over the commits between a known-good and a known-bad commit, for the first commit at which a test fails* — not a debugger, and not a test of its own. Four conditions. It needs a **good commit $g$ and a bad commit $b$** with $g$ in $b$'s history. It needs **one test**, the same for every commit, that decides good or bad — kept outside the repository. The property must be **monotone** along the history: once bad, bad in every later commit of the range, the monotone predicate of [[02-foundations/algorithms/sorting-divide-conquer|11.3 §6]]. And **each test roughly halves** the commits that could still be the first bad one; a commit that cannot be tested is skipped (exit 125), at the price of more tests and possibly an answer of the form "one of these".
>
> $$s=\big\lceil\log_2 N\big\rceil,\qquad N=\big|\,g\,..\,b\,\big|$$
>
> where $N$ is the number of candidates — the commits reachable from $b$ and not from $g$, $b$ included — and $s$ the number of tests in the worst case, since each test keeps at most $\lceil N/2\rceil$ candidates, so after $s$ tests at most $\lceil N/2^s\rceil$ remain, and that is one once $2^s\ge N$.
>
> - **Example**: $g=$ pilot-v1, $b=$ 3568180. $N=6$, printed by `git rev-list --count`, so $s=\lceil\log_2 6\rceil=3$, and the run above used three tests. A semester of 200 commits would need 8.
> - **Non-example**: a flaky test — one that fails on some runs of the same commit, as a timing-dependent test on a loaded computer can. The predicate is then not a property of the commit at all, and bisection returns a commit that is merely where the dice fell. So is a bug that was introduced, fixed and introduced again inside the range: the property is not monotone, and the answer is one of the two introductions, not necessarily the one you are chasing.
> - **Why it matters**: reading six diffs is possible; reading two hundred is not, and bisection turns "the number changed some time this semester" into one commit and one diff — here a single `2` that should have been a `1`.

**Undoing it: revert, not reset.** There are two ways to get rid of dda4b0f, and on a shared branch only one is safe. `git revert` records a new commit whose changes are the inverse of the named commit's (git-revert documentation); history only grows, so everyone else's next pull is a fast-forward:

```bash
git revert --no-edit dda4b0f
python3 analysis/summarize.py
```

```text
[main ea13bc4] Revert "Parse trials without the csv module"
 Date: Fri Mar 27 14:00:00 2026 +0000
 1 file changed, 4 insertions(+), 5 deletions(-)
code:   study-v1-3-gea13bc4
commit: ea13bc450f2ba5b2082b9077c3935b5ecbe330bb
arm   n   success   mean (N)   sd (N)
A    10    6/10      10.66     2.414
B    10    9/10       7.50     1.356
```

The pilot row is back, and the stamp says by which commit. `git reset` does something else: it moves the current branch to another commit, and with `--hard` also overwrites the index and the working tree, discarding uncommitted changes (git-reset). In a clone of RS1:

```bash
git reset --hard HEAD~1
git status
```

```text
HEAD is now at 3568180 Add the figure script
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

Main left ea13bc4 behind, but the server still has it; making the server agree would take a forced push, the non-fast-forward of §5. The rule: **revert what others may have; reset, amend or squash only what nobody else has fetched** — the git-reset manual's own warning on undoing commits is not to do it once you have given them to somebody else. When a reset or a rebase goes wrong locally, `git reflog` lists where `HEAD` has been, which is how a commit that "vanished" is found again; the reflog is local to your clone and expires as §6 said.

### 9. Workspaces that span several repositories

*In one sentence:* a robot's workspace combines your repository with drivers and libraries that live in others, and it is reproducible only when every one of them is pinned by commit id — as submodules in a superproject, or as hashes in a `.repos` file.

Knowing RS1's commit is not enough when the robot also runs a driver from another repository that has moved since. A ROS 2 workspace puts every package it builds under `src/` ([[04-robotics/ros2/workspaces-packages-launch|25.4 §2]]), and on a real robot those packages come from several repositories: RS1's own, the driver for P2's joint amplifiers, perhaps a vendor's force-sensor driver. There are two common ways to pin them together.

**Submodules.** The workspace itself becomes a Git repository — a *superproject* — that records each other repository as one entry: not its files, but the id of one of its commits. Here the two repositories were already in `src/`, so `git submodule add` staged them without cloning anything; the URLs are placeholders that are never contacted:

```bash
git submodule add https://example.com/lab/p2_driver.git src/p2_driver
git submodule add https://example.com/lab/rs1.git src/rs1
cat .gitmodules
```

```text
Adding existing repo at 'src/p2_driver' to the index
Adding existing repo at 'src/rs1' to the index
[submodule "src/p2_driver"]
	path = src/p2_driver
	url = https://example.com/lab/p2_driver.git
[submodule "src/rs1"]
	path = src/rs1
	url = https://example.com/lab/rs1.git
```

```bash
git commit -m "Pin the P2 driver and RS1 as submodules"
git ls-tree HEAD src/
git submodule status
```

```text
[main (root-commit) 1654d5b] Pin the P2 driver and RS1 as submodules
 3 files changed, 8 insertions(+)
 create mode 100644 .gitmodules
 create mode 160000 src/p2_driver
 create mode 160000 src/rs1
160000 commit 2e8b7cd149ac8323357065df2df88ea0958ed588	src/p2_driver
160000 commit ea13bc450f2ba5b2082b9077c3935b5ecbe330bb	src/rs1
 2e8b7cd149ac8323357065df2df88ea0958ed588 src/p2_driver (heads/main)
 ea13bc450f2ba5b2082b9077c3935b5ecbe330bb src/rs1 (study-v1-3-gea13bc4)
```

Mode `160000` is Git's mark for "a commit of another repository in place of a directory" (Pro Git §7.11). The trap is on the other side. A plain clone of the superproject records the pins but brings no files:

```bash
git clone rs1_ws ws_clone
cd ws_clone
git submodule status
```

```text
Cloning into 'ws_clone'...
done.
-2e8b7cd149ac8323357065df2df88ea0958ed588 src/p2_driver
-ea13bc450f2ba5b2082b9077c3935b5ecbe330bb src/rs1
```

The leading `-` means "not initialized": `src/rs1` and `src/p2_driver` exist and are empty. `git submodule update --init` fetches each pinned commit and checks it out on a detached `HEAD`, and `git clone --recurse-submodules` does both steps at once (git-submodule, Pro Git §7.11); neither ran here, because the placeholder URLs lead nowhere.

So a **submodule** is a pin, not a copy: the superproject's tree holds the id of one commit of the other repository, `.gitmodules` says where to fetch it, and moving the pin is a commit in the superproject — committing inside `src/rs1` changes nothing for anyone until the superproject records the new id. The workspace's commit 1654d5b pins `src/rs1` at ea13bc4 and `src/p2_driver` at 2e8b7cd, so "the robot ran workspace 1654d5b" names every repository behind a result, where "RS1 at ea13bc4" says nothing about the driver beside it. The usual trap, which Pro Git §7.11 names, is to push the superproject's commit before the submodule commits it points to: a pin must be a commit that exists on its server.

**A `.repos` file.** The ROS world more often keeps the workspace unversioned and lists its repositories in a YAML file that the `vcs` tool reads. The format is a key `repositories`, one entry per path, each with `type`, `url` and `version` — a branch, a tag or a commit id (vcstool README). RS1's workspace, pinned by hash:

```yaml
repositories:
  p2_driver:
    type: git
    url: https://example.com/lab/p2_driver.git
    version: 2e8b7cd149ac8323357065df2df88ea0958ed588
  rs1:
    type: git
    url: https://example.com/lab/rs1.git
    version: ea13bc450f2ba5b2082b9077c3935b5ecbe330bb
```

vcstool is not installed on the machine this page was built on, so its two commands are shown as its README and source give them:

```bash
# not run here: vcstool is not installed on this page's build machine
vcs import src < rs1.repos          # clone each entry into src/<path> and check out its version
vcs export --exact src > rs1.repos  # write every repository's current commit id, not its branch
```

`vcs export` writes a branch name for a repository sitting on a branch's tip, and its README warns that a later import may then fetch a newer revision; `--exact` writes the commit id instead. So a `.repos` file whose versions are branch names pins nothing: a branch moves, and the same file gives different code on different days. ROS 2's own source build uses a `.repos` file the same way — `vcs import --input` with the `ros2.repos` file of the distribution's branch — and that file lists branch names such as `jazzy`, which is right for following a distribution and wrong for freezing a study.

> [!note]- Deeper · 더 깊이
> `vcs import` clones each repository that is missing; for one that already exists with the same URL it fetches and checks out the listed version, and it stops with an error if the directory holds a different repository, unless `--force` (which deletes the directory) or `--skip-existing` is given (vcstool, `import_.py` and `clients/git.py`). The ros-infrastructure organization maintains a fork of vcstool, vcs2l, that keeps the `vcs` command and the `.repos` format and presents itself as a drop-in replacement.

**Which to use.** Submodules when the workspace itself should be a versioned object — a thesis repository whose every commit fixes all its parts. A `.repos` file with commit ids when you follow the ROS convention of a plain `src/` of many third-party repositories; commit that file into your own repository, beside the code whose results it pins. Either way, the rule of §7 extends to the whole robot: a result is reproducible only if every repository behind it is named by a commit id.

### Worked case · 대상으로 한 번 끝까지

RS1's campaign, end to end, on the frozen repository: the graph with its ids, what one corrected number would do to them, which commit produced which table, the search for the regression, and the price of committing the bags. It comes after §9 because it uses §1, §3, §6, §7 and §8 together.

**Step 1 — the graph.** At the end of 27 March:

```bash
git log --oneline --graph --decorate
```

```text
* ea13bc4 (HEAD -> main) Revert "Parse trials without the csv module"
* 3568180 Add the figure script
* b659311 Draft the results section around the pilot table
* 6321a22 (tag: study-v1) Add the pre-trial checklist to the protocol
* 041fe2f Draft the methods section
* dda4b0f Parse trials without the csv module
* a0cd3a3 Write the main-study protocol: 32 trials per arm
* 2006419 (tag: pilot-v1) Record the pilot of B: ten trials
*   882d5dd Merge branch 'impedance-b'
|\  
| * f41f0b6 (impedance-b) Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m
| * 757338e Add controller B: impedance control
* | aebf24a Record the pilot of A: ten trials
|/  
* 2452d15 Add the analysis script that prints the results table
* 16fc8ef Add controller A: position control with a 6 N stop
* c13c298 Start RS1: question, success rule and ignore list
```

Fifteen commits (`git rev-list --count HEAD` prints 15). Count the parent links: the first commit has none, the merge two, the other thirteen one each, so $0+2+13\times1=15$ links, which are the fifteen lines of the picture. Following first parents from HEAD gives main's own line of 13 commits; the other 2 were made on impedance-b. The whole history is 61 objects — 15 commits, 26 trees, 18 blobs and 2 tags — and a clone that had to transfer them (`git clone --no-local --bare`) holds them in one pack of 10.15 KiB, as `git count-objects -vH` printed it.

**Step 2 — one corrected digit.** Suppose trial A1 had been entered as 8.2 N, not 8.1, in aebf24a. By the rule of §1 the pilot file's blob changes — in aebf24a the ten-row file, 29805b11…, and from 2006419 on the twenty-row file, whose id would go from 3a8cd750… to 764faff5… (both printed by the block in §1) — so the `trials/` tree changes, so the root tree, so aebf24a's id. Every commit that has aebf24a as an ancestor names it, directly or through a parent, so their ids change too: 882d5dd, 2006419, a0cd3a3, dda4b0f, 041fe2f, 6321a22, b659311, 3568180, ea13bc4. That is 1 + 9 = 10 of the 15 ids. The other five — c13c298, 16fc8ef, 2452d15, 757338e and f41f0b6 — do not have aebf24a in their history and keep theirs. Both tags would name commits that are no longer on main. This is why the stamp on a table is evidence: had anyone quietly fixed the pilot file inside history, the stamp `pilot-v1-0-g2006419` would name a commit that no longer exists in the new history.

**Step 3 — which commit produced which table.** Three tables were printed by the same script:

| stamp | commit | A: n, successes, mean, sd | B | verdict |
|---|---|---|---|---|
| `pilot-v1-0-g2006419` | 2006419 | 10, 6/10, 10.66 N, 2.414 N | 10, 9/10, 7.50 N, 1.356 N | the pilot table |
| `study-v1-1-gb659311` | b659311 | 9, 5/9, 10.94 N, 2.377 N | unchanged | wrong: dda4b0f's parser drops trial A1 |
| `study-v1-3-gea13bc4` | ea13bc4 | 10, 6/10, 10.66 N, 2.414 N | unchanged | right again, after the revert |

The counts in the stamps follow the rule $n=|t..c|$ of §7. For b659311 the tag is study-v1 = 6321a22, and only b659311 lies beyond it: $n=1$. For ea13bc4 three do — b659311, 3568180, ea13bc4: $n=3$. The wrong row can be checked by hand, because dropping the first line after the header removes A1 = 8.1 N: A's forces then sum to $106.6-8.1=98.5$ N over 9 trials, a mean of $98.5/9=10.944$ N; the successes fall from 6 to 5, because 8.1 N was one of them; and the sample sd of the remaining nine is 2.377 N. B's row is untouched, because B's first trial is not the file's second line.

**Step 4 — the search.** The candidates for the first bad commit are the commits reachable from 3568180 and not from pilot-v1: $N=|\text{pilot-v1..3568180}|=6$ (a0cd3a3, dda4b0f, 041fe2f, 6321a22, b659311, 3568180). By §8's rule, $s=\lceil\log_2 6\rceil=3$ tests at most. The run: test 1 at 041fe2f is bad, so the first bad commit is 041fe2f or earlier — three candidates, {a0cd3a3, dda4b0f, 041fe2f}; test 2 at dda4b0f is bad — two left, {a0cd3a3, dda4b0f}; test 3 at a0cd3a3 is good, so dda4b0f is the first bad commit. Each test halved what was left, $6\to3\to2\to1$.

**Step 5 — what the bags would weigh.** One trial bag is 60 MiB (the page's course number); the pilot recorded 20 and the main study will record 64. This block prices them against GitHub's limits and against RS1's whole history, and prices the search for other $N$:

```python
import math

MiB, GiB = 2**20, 2**30
bag = 60 * MiB                    # one trial bag: a course number
packed = 10.15 * 1024             # bytes: RS1's whole history, packed (measured, see the text)
print("one bag:", bag, "bytes =", bag / MiB, "MiB =", round(bag / packed), "x the packed history")
for label, n in (("pilot", 20), ("main study", 64), ("both", 84)):
    size = n * bag
    print(f"{label:10s} {n:2d} bags  {n * 60:5d} MiB  {size / GiB:5.2f} GiB  {size / 1e9:5.2f} GB")

def tests(N):
    """Worst-case bisect tests for N candidate commits (bad one included)."""
    return math.ceil(math.log2(N)) if N > 1 else 0

for N in (6, 7, 57, 200, 1000):
    print(f"N = {N:4d}  tests = {tests(N)}")
```

```text
one bag: 62914560 bytes = 60.0 MiB = 6053 x the packed history
pilot      20 bags   1200 MiB   1.17 GiB   1.26 GB
main study 64 bags   3840 MiB   3.75 GiB   4.03 GB
both       84 bags   5040 MiB   4.92 GiB   5.28 GB
N =    6  tests = 3
N =    7  tests = 3
N =   57  tests = 6
N =  200  tests = 8
N = 1000  tests = 10
```

Read it against §6. Each bag is $60/50=1.2$ times the size at which GitHub warns, and under the 100 MiB at which it blocks, so every push of a bag would succeed, with a warning. The pilot's 20 bags alone, 1.26 GB, are past the "ideally less than 1 GB" GitHub recommends for a whole repository; with the main study's 64 the repository would hold 5.28 GB (4.92 GiB), five times that and at the 5 GB GitHub strongly recommends staying under. One bag weighs as much as 6,053 copies of RS1's entire packed history, and each would stay reachable — and be downloaded by every clone — after any later deletion. The same 84 bags as checksums in a text file cost a line each.

### 10. What this page does not cover

Rewriting history on purpose — interactive rebase, `git filter-repo` — beyond the rule of §4 and the leak procedure of §6; Git LFS and its quotas; hooks, signed commits and tags; `git stash` and `git worktree` beyond their names; branching models for large teams; continuous integration, which for a ROS package is [[04-robotics/ros2/debugging-data-reproducibility|25.10 §12]]; and GitHub's administration — organizations, permissions, Actions. The shell itself ([[02-foundations/tools/linux-shell|12.1]]), Python environments and packaging ([[02-foundations/tools/python-research-code|12.3]]) and file formats such as MCAP and CSV ([[02-foundations/tools/config-data-formats|12.4]]) have their own pages in this track; C++ is [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]].

### After reading

- [ ] Say what a blob, a tree, a commit and an annotated tag contain, and compute an object id from bytes.
- [ ] Explain why changing one byte in an old commit changes the id of every commit after it, and count which ones.
- [ ] Say what `git add`, `git commit`, `git status`, `git diff` and `git diff --staged` do in terms of the working tree, the index and `HEAD`.
- [ ] Say what a branch and `HEAD` are as files, and what moves when you commit.
- [ ] Find a merge base, predict where a merge will conflict, resolve the conflict, and say what a merge commit records.
- [ ] Tell a fast-forward from a forced update, and say why rebasing or squashing published commits hurts collaborators.
- [ ] Write an ignore list for a robot repository, and say why a deleted bag or key is still in every clone.
- [ ] Tag an experiment, stamp a results table with the commit, and read a `describe` stamp, including `-dirty`.
- [ ] Find a regression with `git bisect` in $\lceil\log_2 N\rceil$ tests, and undo a shared commit with `git revert`, not `git reset`.
- [ ] Pin a multi-repository workspace by commit id, with submodules or a `.repos` file.

### Self-check

1. Two lab-mates, on two machines, each commit a byte-identical copy of `trials/pilot.csv` in a new repository. Do their blobs have the same id? Their commits?
2. You `git add` a file, edit it again, and commit. Which version is in the commit, and what does `git status` show afterwards?
3. What is in `.git/refs/heads/main`, and what changes in it when you commit on main? When you commit on impedance-b?
4. Why did the merge 882d5dd stop at `README.md` but not at `controllers/impedance.py` or `trials/pilot.csv`?
5. A table says `study-v1-3-gea13bc4-dirty`. What does each part say, and can the table be reproduced?
6. How many tests does `git bisect` need for 1,000 candidate commits, and what must be true of the test for its answer to mean anything?
7. A token was committed in one commit and deleted in the next, and both were pushed. What do you do first, and why did the deletion not remove it?

> [!tip]- Answers
> 1. The blobs, yes: a blob's id depends only on its bytes, so both are 3a8cd750…. The commits, almost certainly not: a commit's bytes include the author's and committer's names, e-mails and times, and a parent line — different people at different moments produce different commits even for one identical tree.
> 2. The version you added. `git add` wrote those bytes into the index, and `git commit` records the index. Afterwards `git status` shows the file under "Changes not staged for commit", because the working tree still holds the later edit.
> 3. One commit id — 40 hex digits and a newline, 41 bytes. A commit on main writes the new commit's id into that file, and the new commit has the old id as its parent. A commit on impedance-b changes `.git/refs/heads/impedance-b` and leaves main's file as it was, because `HEAD` named impedance-b.
> 4. Compared with the merge base 2452d15, `controllers/impedance.py` was changed only on impedance-b and `trials/pilot.csv` only on main, so each was taken from the one side that changed it. The status line of `README.md` was changed on both sides, to different text, and that is the only case in which a three-way merge stops.
> 5. study-v1: the nearest annotated tag, the code frozen for the main study. 3: three commits lie beyond it. gea13bc4: the commit, ea13bc4. -dirty: a tracked file differed from ea13bc4 when the table was printed. So the table came from code that is in no commit, and nobody, including you tomorrow, can check it out and rerun it — unless the change is committed and the table printed again.
> 6. $\lceil\log_2 1000\rceil=10$, since $2^{10}=1024\ge1000>2^9$. The test must be deterministic for a given commit — not flaky — and the property monotone over the range: once bad, bad in every later commit. And it must be the same test for every commit, so keep it outside the repository.
> 7. Revoke or rotate the token at the service that issued it; that makes every copy of it harmless. The deletion added a commit whose tree lacks the file, but the earlier commit is still an ancestor of the branch, so its blob is reachable in your repository, on the server and in every clone that fetched — `git show <commit>:<path>` prints it. Rewriting history is a separate decision, made after the rotation, that changes every later commit's id and cannot reach existing clones or forks.

### Problem set · 과제

Tier B. By hand, using only this page, its prerequisites and RS1. The variants: B's branch is rebased instead of merged, one of B's commits is rewritten, the regression hides among more commits, the rig records a second camera, and a lab-mate's week goes wrong in four ways.

1. **Draw.** RS1's history as it would be had impedance-b been rebased onto main instead of merged, with the same files, messages, dates and tags, and the same bug and revert: the commits and their parent links, which ids stay and which are new, where pilot-v1, study-v1 and main point, the bisect range at the time of the search with $N$, and what `git describe --long` prints at `HEAD`. Say what the rebase did to the final snapshot.
2. **Derive.** (a) Someone rewrites 757338e, the first commit of B's branch, to add a missing unit to its message. How many of the fifteen ids change, which keep theirs, and what must happen to the two tags? (b) After the main study a figure stops matching its table; the last good commit is 57 commits behind `HEAD`. How many tests does `git bisect` need in the worst case? Two of the 57 cannot be built and are skipped with exit 125: what can that cost? (c) A second camera doubles each trial bag to 120 MiB. What happens when a bag is pushed to GitHub, and how large would the 84 bags make the repository, in MiB, GiB and GB? (d) After study-v1, main receives 5 commits while a branch fix-filter receives 3, starting at study-v1; the branch is then merged into main with a merge commit. What is $n$ in `git describe` at the merge commit, and what does `git describe --first-parent` print for $n$?
3. **Interpret.** A lab-mate spent 30 March in their own clone of the lab server. Their terminal at the end of the day:

    ```text
    $ git log --oneline --graph --decorate -6
    * 328d473 (HEAD -> main, origin/main, origin/HEAD) Remove the token from the upload script
    * 1866f39 Add the upload script for the lab dashboard
    * 4257fa3 Add the bag of trial B07 for figure 2
    * 41cea18 Add the figure script and fix the trial parser
    * b659311 Draft the results section around the pilot table
    * 6321a22 (tag: study-v1) Add the pre-trial checklist to the protocol
    $ git status
    On branch main
    Your branch is up to date with 'origin/main'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git restore <file>..." to discard changes in working directory)
    	modified:   analysis/summarize.py

    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    	results/

    no changes added to commit (use "git add" and/or "git commit -a")
    $ cat results/table_12N.txt
    code:   study-v1-5-g328d473-dirty
    commit: 328d473b53f1df56735c60d606807cac98510f9e
    arm   n   success   mean (N)   sd (N)
    A    10    7/10      10.66     2.414
    B    10   10/10       7.50     1.356
    $ git show --stat --format="%h %s" HEAD~2
    4257fa3 Add the bag of trial B07 for figure 2

     trials/B07.mcap | Bin 0 -> 62914560 bytes
     1 file changed, 0 insertions(+), 0 deletions(-)
    ```

    and the student's, in their own clone, the next morning:

    ```text
    $ git fetch
    From ../lab
     + ea13bc4...328d473 main       -> origin/main  (forced update)
    $ git status
    On branch main
    Your branch and 'origin/main' have diverged,
    and have 2 and 4 different commits each, respectively.
      (use "git pull" if you want to integrate the remote branch with yours)

    nothing to commit, working tree clean
    ```

    (Both screens are real output from scratch clones of RS1's repository, each command run at the state shown. The lab server was rewritten the way a force-push rewrites it, and the token is an obvious placeholder.) (a) Name every problem the two screens show, the line that shows it, and what it costs the study. (b) For each, the repair now and the habit that would have prevented it. (c) The student is about to run `git pull --no-rebase` "to get the lab-mate's work". What would the history look like afterwards, and what should happen instead?

> [!note]- How to draw it · 그리는 법
> - **Newest on top, one row per commit**, as `git log --graph` prints it, so that your drawing can be checked against the terminal line by line.
> - **Lines join a commit to its parents**, which lie below it; a merge has two lines going down, an ordinary commit one, the first commit none. A rebased history has no merge and so no second line anywhere.
> - **Write at least seven hex digits on every commit**, and mark which ids are new. A commit keeps its id only if its whole history is unchanged; one changed ancestor anywhere below gives it a new id.
> - **Branches and tags are labels beside commits**, not lanes of commits: draw `main`, `HEAD`, `impedance-b`, `pilot-v1` and `study-v1` as boxes pointing at one commit each.
> - **The bisect range is a bracket over commits**: from the one after the good commit up to and including the bad one, with $N$ and $\lceil\log_2 N\rceil$ written beside it.
> - **Write the describe stamp at HEAD** and check its $n$ by counting the commits above the tag that `HEAD` reaches.
> - **Say what happened to the snapshot**: compare the final tree's id with the original's, not the commits'.

> [!tip]- Solutions
> 1. Fourteen commits on one straight line, no merge. c13c298, 16fc8ef, 2452d15 and aebf24a keep their ids: nothing in their history changed. B's two commits are replayed on top of aebf24a and get new ids — 757338e becomes 83db14a and f41f0b6 becomes 04bbc92 — because their parent is now aebf24a instead of 2452d15, and the rebase stops once, at the tuning commit, on the same status line of `README.md` that the merge stopped at. Every commit after them changes too, since its parent chain did: 2006419 → 0d96d14 (pilot-v1), a0cd3a3 → 302b9af, dda4b0f → 9b68b59, 041fe2f → fab61c5, 6321a22 → 2b60c62 (study-v1), b659311 → 3a1ccef, 3568180 → 6a2bd00, ea13bc4 → 1ad0242 (main, HEAD). 882d5dd has no counterpart. `git merge impedance-b` after the rebase prints `Fast-forward`. The bisect range before the revert is still six commits, 302b9af to 6a2bd00, so three tests, and `git describe --long` at HEAD prints `study-v1-3-g1ad0242`. The snapshot did not change: the final tree is e3238a51…, the pilot's 4710a335… and study-v1's bcefb113…, as in the merged history. (These ids come from rebuilding the variant in a scratch clone with the original dates, the rebased commits' committer date set to 9 March, 10:00.)
> 2. (a) 757338e and every commit that has it in its history: f41f0b6, 882d5dd, 2006419, a0cd3a3, dda4b0f, 041fe2f, 6321a22, b659311, 3568180, ea13bc4 — 11 of the 15. c13c298, 16fc8ef, 2452d15 and aebf24a keep theirs. Both tags still name the old 2006419 and 6321a22, which are no longer on main; since the tags have been published, they are not moved but replaced by new names, pilot-v1.1 and study-v1.1, and every table stamped with the old ids names commits the new history lacks. (b) $\lceil\log_2 57\rceil=6$ tests, since $2^5=32<57\le64=2^6$. Skipped commits cost extra tests, and if a skipped commit sits right next to the first bad one, bisect cannot tell which of them it was and reports the candidates instead (git-bisect documentation). (c) 120 MiB is more than the 100 MiB at which GitHub blocks a file, so every push that carries a bag is refused outright. The 84 bags would be $84\times120=10{,}080$ MiB $=9.84$ GiB $=10.57$ GB — twice the 5 GB GitHub strongly recommends, before a single one could be pushed. (d) $n=|\text{study-v1..merge}|$ counts every commit reachable from the merge and not from study-v1: 5 on main, 3 on fix-filter and the merge itself, $n=9$. With `--first-parent` the walk follows only main's line — the 5 commits and the merge — and prints $n=6$. Both numbers were checked in a scratch clone of RS1 built with exactly this shape: `study-v1-9-g…` and `study-v1-6-g…`.
> 3. (a) Four problems. *A table from uncommitted code:* `modified: analysis/summarize.py` and the stamp `study-v1-5-g328d473-dirty`. The file's limit is 12 N, so A shows 7/10 and B 10/10 — the 12 N variant that [[06-research-practice/research-questions-claims|1. Research Questions & Claims]] asks about, a fair question — but the code that printed it exists in no commit, and `results/` is not tracked either, so nobody can reproduce or review it. *A force-push over shared history:* the student's `+ ea13bc4...328d473 … (forced update)` and "diverged … 2 and 4". The lab-mate squashed 3568180 and ea13bc4 into one new commit, 41cea18, and forced the server's main onto it. The snapshot survived — 41cea18's tree is e3238a51…, the same as ea13bc4's — but the history did not: the revert of dda4b0f is no longer recorded as a revert, the commit now carries the lab-mate's name, and every table the student stamped `study-v1-3-gea13bc4` names a commit the server no longer has. *A committed bag:* 4257fa3 adds `trials/B07.mcap`, `Bin 0 -> 62914560 bytes` — 60 MiB, against RS1's whole history of 10.15 KiB packed. The bag matches the `*.mcap` rule of `.gitignore`, so it was forced in with `git add -f`; at 60 MiB it is over GitHub's 50 MiB warning, and it now sits in every clone that fetched, the student's included. *A token in history:* 1866f39 added the upload script and 328d473 "removed the token", but 1866f39 is still reachable from main, so `git show 1866f39:analysis/upload.py` prints the token in every clone that has fetched main since — the student's too; `git log -S` finds both commits. (b) *Table:* commit the 12 N change on its own branch with a message that says so, rerun, and the stamp is clean; the habit is `git status --porcelain` printing nothing before any table is made. *Force-push:* stop, and agree as a group which history is main — the student still has ea13bc4, the lab-mate has 41cea18, and they hold the same tree, so no work is lost either way. Then protect main on the server so that a force-push is refused, and review changes by pull request; the habit is never to rewrite commits others have fetched (§4). *Bag:* the bag belongs on the data server with its checksum in the repository; removing it from history is a rewrite that changes 4257fa3, 1866f39 and 328d473, needs everyone's agreement, and cannot reach clones that already have it — so decide deliberately, and never `add -f` a bag. *Token:* revoke or rotate the token at the dashboard first; then decide on a rewrite as for the bag; keep the token in an environment variable, as 328d473 now does, and turn on push protection. (c) A merge of ea13bc4 and 328d473: the student's 3568180 and ea13bc4 come back beside 41cea18, which carries the same changes, and the next push would republish exactly the commits the lab-mate removed — the duplicate history Pro Git §3.6 describes. Instead: talk first, pick one history, and then either reset main to `origin/main` (safe here, since ea13bc4's tree equals 41cea18's and nothing else is only in the student's clone) or put the old commits back on the server with `--force-with-lease`. Afterwards the tables are printed again from a commit everyone has.

### Sources

- Chacon, S. & Straub, B. *Pro Git*, 2nd ed. ([git-scm.com/book](https://git-scm.com/book/en/v2)) — §2.6 tags, §3.1 branches, §3.2 merging, §3.5 remote branches, §3.6 rebasing and its rule, §7.7 the three trees, §7.11 submodules, §10.2 Git objects.
- Git reference manual ([git-scm.com/docs](https://git-scm.com/docs)), versions 2.52–2.55 — git-init and BreakingChanges (SHA-256, Git 3.0), git-describe, git-bisect (exit codes), git-revert, git-reset, git-push (push rules), git-pull, git-log, git-diff, gitignore, git-gc (reachability, reflog expiry), git-reflog, git-tag (on re-tagging), git-switch, git-submodule, gitdiffcore (`-S`).
- GitHub Docs ([docs.github.com](https://docs.github.com/en)) — "About large files on GitHub" (50 MiB, 100 MiB, 1 GB, 5 GB), "Removing sensitive data from a repository", "About push protection", "About pull requests", "About pull request reviews", "About protected branches".
- vcstool ([github.com/dirk-thomas/vcstool](https://github.com/dirk-thomas/vcstool)) — the `.repos` format, `vcs export --exact`, `vcs import` on existing directories (`import_.py`, `clients/git.py`); vcs2l ([github.com/ros-infrastructure/vcs2l](https://github.com/ros-infrastructure/vcs2l)) — its fork and drop-in replacement.
- ROS 2 on GitHub, jazzy — [Ubuntu-Development-Setup.rst](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Alternatives/Ubuntu-Development-Setup.rst) (`vcs import --input` of `ros2.repos`) and [ros2.repos](https://github.com/ros2/ros2/blob/jazzy/ros2.repos) (branch names as versions).
- GNU `sed(1)` on man7.org and the BSD `sed(1)` of macOS — the two spellings of `-i` that §7 avoids.

## 한국어

*[[06-research-practice/index|6. 연구 실무]]의 모든 페이지가 함께 쓰는 연구 RS1 위에 선다. 여기서는 그 연구를 담은 저장소로 본다. 제어기 둘, 예비 실험의 숫자 스무 개, 분석 스크립트 하나, 논문 하나다. 기초 트랙에서 RS1을 처음 쓰는 페이지다. [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성 §7]]은 재현 가능한 결과가 무엇을 기록해야 하는지 나열한다. 이 페이지는 그 기록 가운데 코드 부분을 어떻게 남기는지, 그리고 나중에 어느 코드가 어느 숫자를 만들었는지 어떻게 가려내는지를 다룬다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]의 물리 AI 스택 아래 바닥의 일부다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 층을 하나 더하지는 않지만 모든 층의 결과는 그 뒤에 있는 코드의 기록만큼만 믿을 만하고, 그 절의 예 "저 패널을 프레임에 설치해"에서 이 페이지가 맡는 것은 마지막 단계, 곧 패널이 정말로, 재현 가능하게 안착했다는 증거다. 결과 표마다 커밋이 없으면, §8이 찾아내는 문자 하나짜리 파서 버그가 평균을 10.66 N에서 10.94 N으로 옮겨도 언제 왜 그랬는지 아무도 말하지 못한다. [[06-research-practice/experimental-design-reproducibility|연구 실무 2 §7]]은 산출물 목록 맨 앞에 코드 커밋을 두고, [[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]은 그 위에 고정된 실행을 세우며, [[05-construction-robotics/imitating-contact|10. 접촉 모방 §8]]이 평가하는 안착률도 바로 이런 숫자 — 리뷰어가 다시 돌릴 수 있어야 하는, 코드가 출력한 표 — 다. 이 페이지는 [[07-research-program/index|학위논문 경로(연구 프로그램 §8)]]의 일곱 블록 밖에 있으므로 학위논문을 위한 첫 코드를 쓸 때, 늦어도 연구 실무 2가 커밋을 묻는 블록 5에서 읽고, 다 읽으면 모든 결과에 그것을 만든 커밋을 찍고, 숫자를 망가뜨린 커밋을 $\lceil\log_2 N\rceil$번의 시험으로 찾고, 누구의 히스토리도 다시 쓰지 않고 되돌릴 수 있다.

> [!note] 처음이라면 · First pass
> 60–90분짜리 두 회차로 읽는다. **1회차:** 이 페이지의 대상과 그림 — RS1의 커밋 열다섯 개, 브랜치 하나, 병합 하나, 태그 둘 — 그다음 §1과 §2. 커밋이 무엇인지, 편집한 내용이 파일에서 히스토리까지 어떻게 가는지다. 스스로 점검 1과 2로 마친다. **2회차:** §3, §7, §8 — 브랜치, 결과 표마다 그것을 낸 커밋을 찍는 일, 회귀를 찾아 되돌리는 일 — 그다음 대상으로 한 번 끝까지. 그 계산은 이 절들을 모두 쓰므로 §9 뒤에 있다. 스스로 점검 3, 5, 6으로 마친다. §4–§6은 저장소를 처음 남과 나누기 전에, §9는 로봇 워크스페이스가 저장소 여러 개에 걸칠 때 읽고, 과제는 그 뒤에 푼다.

### 이 페이지의 대상 · Running object

[[06-research-practice/index|6. 연구 실무]]의 관통 연구 **RS1**. *질문:* 임피던스 제어(**B**)가 힘 문턱 정지를 단 위치 제어(**A**)보다 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**와 400 N/m 패널의 접촉을 더 안전하게 만드는가? *시행:* 접촉으로 끝나는 접근 한 번이고, 최대 접촉력이 10 N 이하면 성공이다. *예비 실험*(고정), 팔마다 10회 — A: 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 N이므로 6/10, 평균 10.66 N, 표본 표준편차 2.414 N. B: 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 N이므로 9/10, 평균 7.50 N, 표준편차 1.356 N. *본 실험:* 팔마다 32회, 모두 64회로 계획되어 있다.

이 페이지는 RS1 위에 자기 대상 하나를 고정한다. 여기서 전부 명세하고 다시는 바꾸지 않는다. **RS1의 저장소**, 이 페이지를 위해 실제로 만든 Git 저장소로, 2026년 3월 2일부터 27일까지 날짜가 붙은 커밋 열다섯 개다. 날짜는 교과용 날짜이고 무엇의 기록도 아니다. 파일은 다음과 같다.

| 경로 | 담긴 것 | 추가된 커밋 |
|---|---|---|
| `README.md` | 질문, 성공 규칙, 한 줄짜리 상태 | c13c298 |
| `.gitignore` | Git이 절대 추적하면 안 되는 것: 빌드 산출물, bag, 가중치, 캐시, `.env`(§6) | c13c298 |
| `controllers/position_stop.py` | 제어기 A: 관절 이득과 6 N 정지 | 16fc8ef |
| `analysis/summarize.py` | 결과 표를 출력하고, 실행한 커밋을 표에 찍는다(§7) | 2452d15 |
| `controllers/impedance.py` | 제어기 B: 접근 축 방향 강성 $K$와 감쇠 $D$ | 757338e |
| `trials/pilot.csv` | 예비 실험의 최대 접촉력 20개, 184바이트 | aebf24a(A), 2006419(B) |
| `protocol.md` | 본 실험 계획과 시행 전 점검표 | a0cd3a3, 6321a22 |
| `paper/paper.md` | 논문의 방법 절과 결과 절 | 041fe2f, b659311 |
| `analysis/figure.py` | 그림 2가 그리는 숫자를 출력한다 | 3568180 |

히스토리는 오래된 것부터 적는다. 커밋은 16진수 마흔 자리 가운데 앞 일곱 자리로 부른다(§1).

| 커밋 | 부모 | 날짜(UTC) | 하는 일 | 붙은 이름 |
|---|---|---|---|---|
| c13c298 | 없음 | 03-02 09:00 | 저장소 시작: README와 무시 목록 | |
| 16fc8ef | c13c298 | 03-03 10:00 | 제어기 A 추가 | |
| 2452d15 | 16fc8ef | 03-04 11:00 | 분석 스크립트 추가 | |
| 757338e | 2452d15 | 03-05 14:00 | 제어기 B 추가, $K=500$ N/m, $D=30$ N·s/m | |
| aebf24a | 2452d15 | 03-05 16:00 | A의 예비 시행 10회 기록 | |
| f41f0b6 | 757338e | 03-06 15:00 | 장치에서 B를 $K=300$ N/m, $D=25$ N·s/m로 조율 | impedance-b |
| 882d5dd | aebf24a, f41f0b6 | 03-09 10:00 | B의 브랜치를 병합, 충돌 한 번 뒤 | |
| 2006419 | 882d5dd | 03-10 16:00 | B의 예비 시행 10회 기록 | pilot-v1 |
| a0cd3a3 | 2006419 | 03-16 09:00 | 본 실험 프로토콜 작성: 팔마다 32회 | |
| dda4b0f | a0cd3a3 | 03-18 13:00 | 시행 파서를 다시 짬 — 그리고 시행 하나를 떨어뜨림(§8) | |
| 041fe2f | dda4b0f | 03-20 10:00 | 방법 절 초안 | |
| 6321a22 | 041fe2f | 03-23 11:00 | 시행 전 점검표 추가 | study-v1 |
| b659311 | 6321a22 | 03-25 15:00 | 결과 절 초안 | |
| 3568180 | b659311 | 03-27 10:00 | 그림 스크립트 추가 | |
| ea13bc4 | 3568180 | 03-27 14:00 | dda4b0f를 되돌림 | main, HEAD |

대상과 함께 고정하는 이 페이지의 숫자:

| 양 | 값 | 종류 |
|---|---|---|
| rosbag2가 기록하는 시행 bag 하나 | 60 MiB $=62{,}914{,}560$바이트 | 교과용 숫자, 측정값이 아님 |
| 예비 실험과 본 실험의 시행 수 | 20과 64 | RS1의 것 |
| 히스토리 전체, 팩으로 묶었을 때 | 객체 61개, 10.15 KiB | 이 페이지의 저장소에서 잰 값 |
| A의 정지, B의 이득 | 6 N, [[06-research-practice/failure-analysis-system-evaluation\|3. 실패 분석]]의 F1과 같다. $K$와 $D$는 위와 같다 | 저장소의 것. $K$와 $D$는 다른 페이지가 쓰지 않는다 |

저장소는 macOS(arm64)에서 Apple Git 2.50.1로, 작성자 `RS1 Student <student@example.com>`으로 만들었고, 모든 커밋의 작성 날짜와 커밋 날짜를 Git의 환경 변수 `GIT_AUTHOR_DATE`와 `GIT_COMMITTER_DATE`로 고정했다. 같은 파일, 같은 메시지, 같은 날짜는 어느 기계에서나 같은 마흔 자리 id를 준다. 여러분이 만드는 커밋에는 여러분의 이름과 시계가 들어가므로 다른 id를 받는다. 그 이유는 §1에 있다. 아래의 모든 명령은 그 저장소나 그것을 복제한 임시 저장소에서 실행했고, 모든 출력은 Git이 출력한 그대로이며, 줄인 곳은 표시했다. 로봇의 Ubuntu에서는 Git 버전이 다른 곳에서만, 주로 `hint:` 줄에서만 메시지가 다르다.

*범위: 이 페이지는 로보틱스 연구자가 연구의 코드, 작은 데이터, 논문을 올바르고 되살릴 수 있게 지키는 데 필요한 Git을 가르친다 — 커밋이 무엇인지, 파일이 커밋에 어떻게 들어가는지, 브랜치와 병합, 원격 저장소를 통한 공유, 절대 커밋하면 안 되는 것, 모든 결과에 그것을 만든 커밋을 찍는 일, 회귀를 찾아 되돌리는 일, 워크스페이스 하나에 저장소 여러 개를 고정하는 일이다. 한 문단을 넘는 히스토리 재작성, Git LFS, hook, 서명된 커밋, 지속적 통합은 가르치지 않는다 — ROS 패키지의 CI는 [[04-robotics/ros2/debugging-data-reproducibility|25.10 §12]]다. 연구가 코드 말고 무엇을 기록해야 하는지도 가르치지 않는다. 그것은 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §7]]이다. 셸, Python 환경, 파일 형식은 이 트랙의 [[02-foundations/tools/linux-shell|12.1]], [[02-foundations/tools/python-research-code|12.3]], [[02-foundations/tools/config-data-formats|12.4]]이고, 논문 자체의 빌드 — 무엇을 커밋하고 무엇을 다시 만드는지 — 는 [[02-foundations/tools/latex-figures-references|12.6 §10]]이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 424" style="max-width:100%;height:auto" role="img" aria-label="RS1의 커밋 그래프: 최신 순으로 커밋 열다섯 개, 커밋 둘인 브랜치 impedance-b와 그것을 합친 882d5dd, 2006419의 태그 pilot-v1과 6321a22의 태그 study-v1, 커밋 여섯 개의 bisect 범위와 시험 세 번, 첫 bad 커밋 dda4b0f, 그리고 그것을 되돌린 ea13bc4.">
  <defs><marker id="gdRevk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">RS1의 저장소, 최신 커밋이 위</text>
  <g font-size="10" fill="currentColor" fill-opacity="0.75"><text x="78" y="38">커밋</text><text x="130" y="38">메시지</text><text x="398" y="38">참조 · bisect · 표</text></g>
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="40.0" y1="64.0" x2="40.0" y2="74.0"/>
    <line x1="40.0" y1="86.0" x2="40.0" y2="96.0"/>
    <line x1="40.0" y1="108.0" x2="40.0" y2="118.0"/>
    <line x1="40.0" y1="130.0" x2="40.0" y2="140.0"/>
    <line x1="40.0" y1="152.0" x2="40.0" y2="162.0"/>
    <line x1="40.0" y1="174.0" x2="40.0" y2="184.0"/>
    <line x1="40.0" y1="196.0" x2="40.0" y2="206.0"/>
    <line x1="40.0" y1="218.0" x2="40.0" y2="228.0"/>
    <line x1="40.0" y1="243.0" x2="40.0" y2="294.0"/>
    <line x1="46.4" y1="240.4" x2="57.8" y2="251.8"/>
    <line x1="62.0" y1="262.0" x2="62.0" y2="272.0"/>
    <line x1="59.3" y1="283.4" x2="42.7" y2="316.6"/>
    <line x1="40.0" y1="306.0" x2="40.0" y2="316.0"/>
    <line x1="40.0" y1="328.0" x2="40.0" y2="338.0"/>
    <line x1="40.0" y1="350.0" x2="40.0" y2="360.0"/>
  </g>
  <path d="M386 72 H390 V198 H386" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <path d="M34 61 C 12 80, 12 146, 33.5 164.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#gdRevk)"/>
  <text x="11" y="113" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 11 113)">되돌림</text>
  <circle cx="40" cy="58" r="5" fill="currentColor"/>
  <text x="78" y="62" font-size="11" font-family="monospace" fill="currentColor">ea13bc4</text>
  <text x="130" y="62" font-size="11" fill="currentColor">Revert “Parse trials without…”</text>
  <circle cx="40" cy="80" r="5" fill="currentColor"/>
  <text x="78" y="84" font-size="11" font-family="monospace" fill="currentColor">3568180</text>
  <text x="130" y="84" font-size="11" fill="currentColor">Add the figure script</text>
  <circle cx="40" cy="102" r="5" fill="currentColor"/>
  <text x="78" y="106" font-size="11" font-family="monospace" fill="currentColor">b659311</text>
  <text x="130" y="106" font-size="11" fill="currentColor">Draft the results section</text>
  <circle cx="40" cy="124" r="5" fill="currentColor"/>
  <text x="78" y="128" font-size="11" font-family="monospace" fill="currentColor">6321a22</text>
  <text x="130" y="128" font-size="11" fill="currentColor">Add the pre-trial checklist</text>
  <circle cx="40" cy="146" r="5" fill="currentColor"/>
  <rect x="32" y="138" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <text x="78" y="150" font-size="11" font-family="monospace" fill="currentColor">041fe2f</text>
  <text x="130" y="150" font-size="11" fill="currentColor">Draft the methods section</text>
  <circle cx="40" cy="168" r="5" fill="currentColor"/>
  <rect x="32" y="160" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <text x="78" y="172" font-size="11" font-family="monospace" fill="currentColor">dda4b0f</text>
  <text x="130" y="172" font-size="11" fill="currentColor">Parse trials without the csv module</text>
  <circle cx="40" cy="190" r="5" fill="currentColor"/>
  <rect x="32" y="182" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 2"/>
  <text x="78" y="194" font-size="11" font-family="monospace" fill="currentColor">a0cd3a3</text>
  <text x="130" y="194" font-size="11" fill="currentColor">Write the main-study protocol</text>
  <circle cx="40" cy="212" r="5" fill="currentColor"/>
  <text x="78" y="216" font-size="11" font-family="monospace" fill="currentColor">2006419</text>
  <text x="130" y="216" font-size="11" fill="currentColor">Record the pilot of B: ten trials</text>
  <circle cx="40" cy="234" r="5" fill="currentColor"/>
  <circle cx="40" cy="234" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="78" y="238" font-size="11" font-family="monospace" fill="currentColor">882d5dd</text>
  <text x="130" y="238" font-size="11" fill="currentColor">Merge branch ‘impedance-b’</text>
  <circle cx="62" cy="256" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="78" y="260" font-size="11" font-family="monospace" fill="currentColor">f41f0b6</text>
  <text x="130" y="260" font-size="11" fill="currentColor">Tune B: K 500→300, D 30→25</text>
  <circle cx="62" cy="278" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="78" y="282" font-size="11" font-family="monospace" fill="currentColor">757338e</text>
  <text x="130" y="282" font-size="11" fill="currentColor">Add controller B: impedance</text>
  <circle cx="40" cy="300" r="5" fill="currentColor"/>
  <text x="78" y="304" font-size="11" font-family="monospace" fill="currentColor">aebf24a</text>
  <text x="130" y="304" font-size="11" fill="currentColor">Record the pilot of A: ten trials</text>
  <circle cx="40" cy="322" r="5" fill="currentColor"/>
  <text x="78" y="326" font-size="11" font-family="monospace" fill="currentColor">2452d15</text>
  <text x="130" y="326" font-size="11" fill="currentColor">Add the analysis script</text>
  <circle cx="40" cy="344" r="5" fill="currentColor"/>
  <text x="78" y="348" font-size="11" font-family="monospace" fill="currentColor">16fc8ef</text>
  <text x="130" y="348" font-size="11" fill="currentColor">Add controller A with a 6 N stop</text>
  <circle cx="40" cy="366" r="5" fill="currentColor"/>
  <text x="78" y="370" font-size="11" font-family="monospace" fill="currentColor">c13c298</text>
  <text x="130" y="370" font-size="11" fill="currentColor">Start RS1: question, rule, ignore list</text>
  <rect x="398" y="50" width="78" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="61.5" font-size="10" fill="currentColor">main · HEAD</text>
  <text x="482" y="61.5" font-size="10" fill="currentColor">A: 10.66 N</text>
  <text x="398" y="83.5" font-size="10" fill="currentColor">bisect: N = 6 → 시험 3번</text>
  <text x="398" y="105.5" font-size="10" fill="currentColor">A: 10.94 N (9회)</text>
  <rect x="398" y="116" width="52" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="127.5" font-size="10" fill="currentColor">study-v1</text>
  <text x="398" y="149.5" font-size="10" fill="currentColor">시험 1: bad</text>
  <text x="398" y="171.5" font-size="10" fill="currentColor" font-weight="bold">시험 2: bad → 첫 bad</text>
  <text x="398" y="193.5" font-size="10" fill="currentColor">시험 3: good</text>
  <rect x="398" y="204" width="50" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="215.5" font-size="10" fill="currentColor">pilot-v1</text>
  <text x="482" y="215.5" font-size="10" fill="currentColor">A: 10.66 N</text>
  <text x="398" y="237.5" font-size="10" fill="currentColor">부모 2개</text>
  <rect x="398" y="248" width="74" height="15" rx="3" fill="none" stroke="currentColor" stroke-width="1"/><text x="403" y="259.5" font-size="10" fill="currentColor">impedance-b</text>
  <circle cx="18" cy="388" r="5" fill="currentColor"/>
  <text x="28" y="392" font-size="10" fill="currentColor">main의 커밋</text>
  <circle cx="98" cy="388" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="108" y="392" font-size="10" fill="currentColor">impedance-b의 커밋</text>
  <circle cx="232" cy="388" r="5" fill="currentColor"/><circle cx="232" cy="388" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="245" y="392" font-size="10" fill="currentColor">merge</text>
  <text x="300" y="392" font-size="10" fill="currentColor">선: 커밋과 그 아래의 부모</text>
  <text x="12" y="412" font-size="10" fill="currentColor">점선: ea13bc4가 dda4b0f를 되돌린다</text>
  <text x="300" y="412" font-size="10" fill="currentColor">A: 그 커밋에서 summarize.py가 출력한 A의 평균</text>
</svg>

`git log --graph`가 출력하는 순서대로 최신 커밋을 위에 둔 RS1의 커밋 열다섯 개이고, 선은 각 커밋을 그 아래의 부모와 잇는다. 브랜치 impedance-b(757338e, f41f0b6)는 2452d15에서 갈라져 병합 커밋 882d5dd로 돌아오고, 그 병합의 두 부모는 aebf24a와 f41f0b6이며, 태그 pilot-v1과 study-v1은 예비 실험 표를 낸 커밋과 본 실험 첫 시행 전에 고정한 코드를 가리킨다. dda4b0f에서 다시 짠 파서가 A의 시행 하나를 떨어뜨려 b659311에서 출력한 표는 10회의 10.66 N 대신 9회의 10.94 N을 보이고, `git bisect`는 pilot-v1 뒤의 커밋 여섯 개를 뒤져 시험 세 번 만에 dda4b0f를 찾으며, ea13bc4가 아무것도 지우지 않고 그것을 되돌려 HEAD는 `study-v1-3-gea13bc4`라는 도장과 함께 다시 10.66 N을 출력한다.

### 1. Git이 저장하는 것: 객체, 그리고 커밋에 이름을 붙이는 해시

*한 문장으로:* Git은 모든 파일의 모든 판을 그 바이트의 해시로 이름 붙인 객체로 보관하고, 커밋도 그런 객체 하나 — 프로젝트 전체의 스냅샷에 부모의 이름을 더한 것 — 이므로, 커밋의 이름은 그 히스토리 전체를 보증한다.

결과 표는 그 뒤의 코드와 데이터를 정확히 댈 수 있는 만큼만 믿을 만하다. Git의 답은 설계상의 선택 하나이고, 이 페이지의 나머지는 모두 거기서 나온다. 저장하는 모든 것에 그 바이트의 지문으로 이름을 붙인다는 것이다. 이것만 분명하면 브랜치, 태그, 병합, 결과 표의 도장은 모두 지문에 붙인 이름이다. 저장소는 객체들의 데이터베이스다. 프로젝트 맨 위의 `.git/objects` 디렉터리에 있고, 그 안을 가리키는 이름 몇 개가 곁에 있다. 객체는 네 종류다. **blob**은 파일 하나의 바이트만 담는다. 이름도 날짜도 담지 않는다. **tree**는 디렉터리 하나를 나열한다. 항목마다 모드(보통 파일은 `100644`), 종류, 객체 id, 이름이다. **commit**은 tree 하나 — 그 순간 프로젝트 전체 — 를 부모 커밋, 작성자, 커미터, 메시지와 함께 기록한다. **annotated tag**는 객체 하나에 이름을 붙이고 태그한 사람과 메시지를 더한다(§7). 저장소 안의 어떤 것도 판과 판 사이의 차이가 아니다. 모든 커밋은 완전한 스냅샷을 가리키고, `git show`가 출력하는 diff는 두 tree를 비교해 그 자리에서 계산한 것이다(Pro Git §10.2).

`git cat-file -p`는 어떤 객체든 출력한다. RS1의 첫 커밋 직후 영어 절의 세 명령을 실행하면, 커밋은 `tree 1d9c244b…` 한 줄, 작성자 줄과 커미터 줄(`RS1 Student <student@example.com> 1772442000 +0000`), 빈 줄, 메시지로 되어 있고, 그 tree는 blob 둘 — `.gitignore`의 fd587a49…와 `README.md`의 165de4c9… — 을 나열하며, `git hash-object README.md`는 165de4c9…를 출력한다.

아래에서부터 읽는다. `git hash-object`는 아무것도 저장하지 않고 파일의 바이트가 받을 id를 계산하는데, 그것이 tree가 `README.md`에 대해 적은 id다. tree는 blob 둘을 가리키고, 커밋은 tree를 가리킨다. 첫 커밋에는 `parent` 줄이 없다. 둘째 커밋 16fc8ef에는 `parent c13c29840a58…` 한 줄이 있고, §4의 병합 커밋에는 두 줄이 있다. 작성자와 커미터는 각각 이름, 이메일, 1970년 1월 1일 UTC부터 센 초, 시간대를 싣는다. 1772442000 +0000은 2026년 3월 2일 09:00 UTC다.

> **객체 id의 정의.** Git 객체의 **객체 id**(object id)는 *객체의 내용으로 계산한 이름*이다. 해시 함수의 값이지, 번호나 파일 경로나 저장 위치가 아니다. 정의 조건 넷. **객체의 종류, 길이, 바이트만으로** 계산한다. 파일이 어디 있는지, 이름이 무엇인지, 언제 저장했는지는 들어가지 않는다 — 커밋의 날짜처럼 내용의 일부일 때만 들어간다. 같은 바이트는 **어느 기계에서나 같은 id**를 주므로, 두 클론은 서로 연락하지 않고도 모든 객체의 이름에 합의한다. 다른 바이트는 실제로 **다른 id**를 준다. SHA-1의 160비트 출력은 $2^{160}\approx1.46\times10^{48}$가지 값을 가지며, Git은 SHA-1에 대해 알려진 공격을 막는 장치를 갖고 있다(Git의 BreakingChanges 문서). 그리고 id는 **객체의 주소**다. Git은 모든 객체를 id로 찾고, 느슨한(loose) 객체는 `.git/objects/` 아래 id의 앞 두 자리를 이름으로 한 디렉터리에 zlib으로 압축한 파일로 저장한다(Pro Git §10.2).
>
> $$\mathrm{id}(o)=\mathrm{SHA1}\big(\,t\ \Vert\ \text{space}\ \Vert\ n\ \Vert\ \text{NUL}\ \Vert\ b\,\big)$$
>
> $t$는 종류를 나타내는 단어(`blob`, `tree`, `commit`, `tag`), $n$은 내용의 바이트 수를 십진수로 쓴 것, NUL은 0 바이트, $b$는 내용, $\Vert$는 이어 붙이기다. 해시되는 것이 이것뿐이므로 id는 바이트만으로 정해진다.
>
> - **예**: pilot-v1의 `trials/pilot.csv`는 184바이트이고 id는 3a8cd7502be7ca376de2c3d6bd0da0e294e0a7e0이다. 영어 절의 Python 블록이 RS1의 고정된 힘 스무 개에서 이것을 계산한다. 시행 A1을 8.1 N 대신 8.2 N으로 적으면 — 길이는 같고 숫자 하나만 다르다 — id는 764faff5109a118d1006f114e601f6bf846d4497이 되며, Git의 `hash-object`도 같은 값을 낸다.
> - **비예**: 파일의 이름. `README.md`의 이름을 바꿔도 그 blob은 id 165de4c9…를 유지하고, 프로젝트 어디에 있든 똑같은 파일 둘은 blob 하나를 나눠 쓴다. 이름을 기록하는 것은 tree다.
> - **비예**: 일곱 자리 형태 `165de4c`. 그것은 Git이 유일한 동안 펼쳐 주는 접두사다. 최소 7자리이고 저장소가 커지면 더 길어진다(git-describe 문서). 오늘 유일한 문자열도 더 큰 저장소에서는 모호해질 수 있다. 결과 표에는 마흔 자리를 다 적는다(§7).
> - **왜 중요한가**: 결과 옆에 적은 id는 그 뒤의 모든 파일의 바이트를 정확히 가리킨다. 기록한 bag이나 데이터셋 옆에 두는 체크섬도 같은 생각 — 데이터를 내용의 해시로 이름 붙이기 — 이다(§6).

이 규칙은 Git 없이도 확인할 수 있다. 영어 절의 Python 블록은 RS1의 고정된 힘으로 예비 실험 파일을 다시 만들어 해시하고, 이어서 pilot-v1이 가리키는 커밋을 `git cat-file -p 2006419`가 출력하는 248바이트로 해시한다. 출력은 세 줄이다. `trials/pilot.csv`는 184바이트, blob 3a8cd7502be7ca376de2c3d6bd0da0e294e0a7e0. A1 = 8.2 N이면 184바이트, blob 764faff5109a118d1006f114e601f6bf846d4497. pilot-v1의 커밋은 248바이트, commit 20064191fe47e9c20677136f53f58a693e5aaf05.

첫째와 셋째 id는 RS1 저장소에서 Git이 그 파일과 그 커밋에 준 id다.

> **커밋의 정의.** **커밋**(commit)은 *프로젝트의 스냅샷 하나와 그것이 어디서 왔는지를 기록하는 객체*다. diff도 파일도 브랜치도 아니다. 정의 조건 넷. **tree를 정확히 하나** 가리키는데, 추적하는 모든 파일의 스냅샷이다. **부모를** id로 가리킨다. 첫 커밋은 없고, 보통 커밋은 하나, 병합 커밋은 둘 이상이다. **작성자와 커미터** — 각각 이름, 이메일, 1970년부터 센 초, 시간대 — 와 **메시지**를 싣는다. 그리고 그 이름은 **이 바이트들의 객체 id**이므로 부모의 id에 의존하고, 부모의 id는 다시 그 부모의 id에 의존한다.
>
> $$h(c)=\mathrm{id}\big(\text{commit};\ h(T_c),\ h(p_1),\dots,h(p_q),\ a_c,\ k_c,\ m_c\big)$$
>
> $T_c$는 커밋의 tree, $p_1,\dots,p_q$는 부모, $a_c$와 $k_c$는 작성자 줄과 커미터 줄, $m_c$는 메시지다. 각 $h(p_i)$도 자기 부모로부터 같은 방식으로 계산되므로 $h(c)$는 모든 조상에 의존한다.
>
> - **예**: pilot-v1이 가리키는 2006419. tree 4710a335…, 부모 882d5dd…, 작성자와 커미터 RS1 Student, 1773158400(2026년 3월 10일 16:00 UTC), 메시지 "Record the pilot of B: ten trials" — 영어 절의 블록이 id를 재현하는 248바이트다. aebf24a에 시행 A1이 8.2 N으로 적혔다면 blob, `trials/` tree, 루트 tree가 달라지므로 aebf24a의 id가 달라지고, 그것을 조상으로 가진 모든 커밋의 id도 달라진다. 15개 가운데 10개다(대상으로 한 번 끝까지가 센다).
> - **비예**: 같은 내용을 두 번 커밋한 것. 그리기 과제는 B의 브랜치를 병합하지 않고 main 위에 다시 쌓는다. 최종 스냅샷은 같은 tree e3238a51…이지만, 다시 쌓은 뒤의 모든 커밋은 부모가 바뀌었으므로 새 id를 받는다.
> - **비예**: "커밋은 내가 한 변경이다." `git show`가 출력하는 변경은 커밋의 tree를 부모의 tree와 비교해 계산한 것이다. 커밋 자체는 스냅샷 전체를 저장한다. 그래서 옛 커밋을 checkout하면 그 스냅샷을 곧바로 쓰고, 거기에 이른 변경들을 다시 적용하지 않는다.
> - **왜 중요한가**: 결과 표에 적은 16진수 마흔 자리는 그 숫자 뒤의 코드, 작은 데이터, 히스토리 전체를 한꺼번에 고정한다. 누구도 조상을 고치고 id를 유지할 수 없다. 바뀐 히스토리는 다른 이름을 가진 다른 히스토리다.

**어떤 해시인가.** Git은 기본으로 객체에 SHA-1로, 16진수 40자리로 이름을 붙인다. 64자리 id의 SHA-256도 있고, Git 3.0에서 새 저장소의 기본값이 될 계획이다. 이 페이지의 어떤 것도 어느 쪽인지에 좌우되지 않는다. 40자리 대신 64자리여도 모든 규칙이 그대로 성립한다.

> [!note]- 더 깊이 · Deeper
> SHA-256 저장소는 `git init --object-format=sha256`으로 만들고, 문서는 SHA-256 저장소와 SHA-1 저장소가 아직 서로 객체를 주고받을 수 없다고 적는다(git-init, 2.54.0). Git 3.0은 새로 만드는 저장소의 기본값을 SHA-256으로, 첫 브랜치의 기본 이름을 `main`으로 바꿀 계획이며, 출시일은 발표되지 않았다(BreakingChanges, 2.55.0).

**히스토리가 고리 없는 그래프인 이유.** 부모의 id가 커밋의 바이트 일부이므로, 커밋은 이미 존재하는 부모만 가리킬 수 있다. 그래서 부모 링크를 따라가면 늘 과거로 가고 출발한 곳으로 돌아올 수 없다. 히스토리는 방향 비순환 그래프, DAG다([[02-foundations/algorithms/graph-algorithms|11.6 §3]]). 병합 커밋은 나가는 간선이 둘인 노드다. 이 페이지의 모든 히스토리 그림이 이 그래프다.

### 2. 작업 트리, 인덱스, 히스토리

*한 문장으로:* 파일은 세 곳에 산다 — 편집하는 작업 트리, 다음 커밋을 담는 인덱스, 커밋들의 히스토리 — 그리고 `add`, `commit`, `status`, `diff`는 저마다 그중 두 곳 사이에서 내용을 옮기거나 두 곳을 비교한다.

파일과 히스토리 사이에 왜 중간 단계가 있을까? 작업 디렉터리에 끝나지 않은 편집이 여럿 있어도 커밋 하나는 의도 하나 — 조율한 이득, 기록한 시행 — 만 담아야 하기 때문이다. Pro Git은 이 세 곳을 세 트리라 부른다(§7.7). **작업 트리**(working tree)는 파일이 있는 보통 디렉터리로, 편집하고 실행하는 곳이다. **히스토리**는 커밋의 사슬이고, `HEAD`는 지금 있는 커밋이다(§3). 그 사이에 **인덱스**, 곧 제안된 다음 커밋이 있다. `git add path`는 작업 트리에 있는 파일의 지금 바이트를 인덱스로 복사한다. `git commit`은 인덱스를 — 인덱스만을 — 새 커밋의 tree로 만든다. `git status`는 셋을 비교한다.

RS1의 커밋 f41f0b6에 모든 것이 다 나온다. 브랜치 impedance-b에서 `controllers/impedance.py`의 이득과 `README.md`의 상태 줄을 둘 다 고쳤다. 영어 절의 첫 `git status`는 두 파일을 모두 "Changes not staged for commit"에 적는다. 제어기만 스테이지하고 다시 보면, `controllers/impedance.py`는 "Changes to be committed"로 옮겨 가고 `README.md`는 "Changes not staged for commit"에 남는다.

이제 두 diff가 서로 다른 것을 보인다. `git diff --staged`는 인덱스를 `HEAD`와 비교하므로 다음 커밋이 담을 것 — `K_N_PER_M`이 500.0에서 300.0으로, `D_NS_PER_M`이 30.0에서 25.0으로 — 을 보인다. 인자 없는 `git diff`는 작업 트리를 인덱스와 비교하므로 아직 스테이지하지 않은 것 — 상태 줄이 `Status: repository started.`에서 `Status: B tuned on the rig (K = 300 N/m, D = 25 N s/m).`로 — 만 보인다.

`index 165de4c..ceeb665` 줄은 다시 §1이다. diff는 `README.md`의 옛 blob과 새 blob의 이름을 대고, 165de4c는 `git hash-object`가 출력한 그 blob이다. README까지 스테이지한 뒤, 무엇이 바뀌었는지 숫자와 함께 말하는 메시지로 둘을 한 변경으로 커밋한다. Git은 `[impedance-b f41f0b6] Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m`와 `2 files changed, 3 insertions(+), 3 deletions(-)`를 출력한다.

> **인덱스의 정의.** **인덱스**(index, 스테이징 영역이라고도 하며 파일 `.git/index`에 있다)는 *추적하는 경로마다 blob id 하나와 모드를 적은 표, 곧 커밋이 생기기 전에 미리 적어 둔 다음 커밋의 스냅샷*이다. 스냅샷이지 변경 목록이 아니고, 작업 트리도 아니다. 정의 조건 셋. `git add`는 **파일의 지금 바이트를** blob으로 쓰고 그 경로의 항목이 그것을 가리키게 한다. 그래서 `git add` 뒤에 한 편집은 다시 add할 때까지 인덱스에 없다. `git commit`은 **인덱스를, 인덱스만을** 새 커밋의 tree로 기록한다. 그리고 `git status`는 **두 비교를 보고한다**. 인덱스 대 `HEAD`("Changes to be committed")와 작업 트리 대 인덱스("Changes not staged for commit"), 그리고 어느 쪽에도 없는 추적되지 않는 파일이다.
>
> $$T_{\text{next}}=I,\qquad \text{staged}=\Delta\big(T_{\text{HEAD}},\,I\big),\qquad \text{unstaged}=\Delta\big(I,\,W\big)$$
>
> $I$는 인덱스, $W$는 작업 트리, $T_{\text{HEAD}}$는 지금 커밋의 tree, $\Delta$는 바이트가 다른 경로의 집합이다. 커밋의 tree가 $I$로부터 쓰이므로 커밋은 스테이지한 것을 정확히 담는다.
>
> - **예**: f41f0b6. `git add controllers/impedance.py` 뒤에 $\Delta(T_{\text{HEAD}},I)$는 이득이 든 제어기 파일이었고, $\Delta(I,W)$는 상태 줄이 든 README였다. 커밋이 둘 다 담은 것은 `git commit` 전에 README도 add했기 때문일 뿐이다.
> - **비예**: `git diff`를 "마지막 커밋 뒤로 바뀐 것"으로 읽기. 그것은 작업 트리를 인덱스와 비교하므로 스테이지한 변경은 거기서 사라진다. 영어 절의 둘째 diff에 이득이 없는 것은 `HEAD`와 같아서가 아니다. 작업 트리를 마지막 커밋과 비교하는 것은 `git diff HEAD`다.
> - **왜 중요한가**: 인덱스 덕분에 커밋 하나가 의도 하나 — 조율과 그것을 기록한 줄 — 를 담고, 다른 파일의 실험은 빠질 수 있다. 동시에 작업 트리가 어떤 커밋과도 일치하지 않을 수 있다는 뜻이고, 그런 트리에서 계산한 표는 어떤 커밋도 재현할 수 없는 표다(§7).

`git log`는 `HEAD`에서 부모를 따라 히스토리를 거슬러 간다. `git log --oneline`은 커밋마다 짧은 id와 메시지 첫 줄을 한 줄로 출력하고, `--graph`는 §3에서처럼 부모 링크를 그린다. `git show <커밋>`은 커밋 하나를 부모와의 diff와 함께 출력한다.

커밋은 싸고 영구적이다. 그러니 일 한 덩이가 그 자체로 뜻을 가질 때 — 제어기를 더했을 때, 이득을 조율했을 때, 예비 실험의 숫자를 기록했을 때 — 커밋하고, 메시지는 일 년 뒤 로그를 읽을 사람, 흔히 자기 자신을 위해 쓴다. 무엇이 바뀌었고, 숫자가 있으면 어떤 숫자인지다. "Tune B on the rig: K 500 -> 300 N/m, D 30 -> 25 N s/m"는 "fix"나 "update"가 결코 말해 주지 않는 것을 리뷰어에게 말해 준다.

### 3. 브랜치와 HEAD

*한 문장으로:* 브랜치는 커밋 하나를 가리키는 움직이는 이름이고, `HEAD`는 다음 커밋이 어느 브랜치를 움직일지 말하며, 자기 브랜치에 둔 작업 줄기는 다른 모든 줄기를 돌아가는 상태로 남겨 둔다.

브랜치가 푸는 문제는 이것이다. main에서 이미 돌아가는 분석을 망가뜨리지 않고 제어기 B를 개발하고 조율한 뒤, 나중에 기록된 한 점에서 둘을 합치고 싶다. 3월 4일 분석 스크립트가 `main`에 2452d15로 커밋되었고, 제어기 B 작업은 자기 브랜치에서 시작했다. 영어 절의 명령들은 `git switch -c impedance-b`로 브랜치를 만들어 옮겨 가고(`Switched to a new branch 'impedance-b'`), `git branch`는 두 브랜치를 나열하며 지금 브랜치에 `*`를 붙이고, `cat .git/HEAD`는 `ref: refs/heads/impedance-b`를, 두 브랜치 파일은 똑같이 2452d15b3041b365f1bd922152336d1840fc19f6을 출력한다.

브랜치는 이것이 전부다. 커밋 id 하나 — 16진수 마흔 자리와 줄바꿈, 41바이트 — 를 담은 파일이다(Pro Git §3.1). impedance-b를 만든 일은 그런 파일 하나를 쓴 것이고, 아무것도 복사되지 않았다. `HEAD`도 파일이며, 커밋이 아니라 브랜치의 이름을 담는다. impedance-b에서 커밋 둘, main에서 커밋 하나(B를 조율하는 동안 기록한 A의 예비 실험) 뒤에 두 줄기는 갈라져 있다. 영어 절의 `git log --oneline --graph --decorate --all`은 impedance-b 쪽에 f41f0b6과 757338e를, main 쪽에 `(HEAD -> main)`이 붙은 aebf24a를, 그 아래 공통 부분에 2452d15, 16fc8ef, c13c298을 그린다.

`--decorate`는 커밋 옆에 그것을 가리키는 이름을 출력한다. Git은 출력이 터미널일 때만 기본으로 그렇게 하므로 여기서는 옵션을 적어 두었다.

> **브랜치의 정의.** **브랜치**(branch)는 *참조, 곧 커밋 하나 — 그 끝(tip) — 의 id를 담는 움직이는 이름*이다. 파일의 사본도, 폴더도, 어딘가에 저장된 커밋 집합도 아니다. 정의 조건 넷. **정확히 커밋 하나**를 가리킨다. 그 브랜치를 checkout한 채로 커밋하면 **옛 끝을 부모로 가진 커밋을 만들고 브랜치를 그리로 옮긴다**. 다른 브랜치는 움직이지 않는다. 브랜치 "위의" 커밋은 **끝과, 끝에서 부모 링크로 닿는 모든 것**이므로 커밋 하나가 여러 브랜치 위에 동시에 있을 수 있다. 그리고 **`HEAD`는 checkout한 브랜치의 이름을 담는다**(`ref: refs/heads/impedance-b`). Git은 그것으로 다음 커밋이 어느 브랜치를 옮길지 안다. 태그나 맨 id를 checkout한 뒤처럼 `HEAD`가 커밋 id를 직접 담으면 *분리된*(detached) 상태이고, 거기서 만든 커밋은 어느 브랜치에도 속하지 않는다(Pro Git §2.6).
>
> $$b\leftarrow c',\qquad \mathrm{parents}(c')=\big(b_{\text{old}}\big),\qquad \mathrm{on}(b)=\{b\}\cup\mathrm{anc}(b)$$
>
> $b$는 `HEAD`가 가리키는 브랜치, $c'$은 새 커밋, $\mathrm{anc}(b)$는 $b$의 끝에서 닿는 모든 커밋이다. `HEAD`는 브랜치를 하나만 가리키므로 커밋 하나는 정확히 브랜치 하나를 옮긴다.
>
> - **예**: impedance-b는 main과 똑같은 41바이트, 2452d15로 시작했다. 757338e와 f41f0b6 뒤에는 f41f0b6을 담고, main은 자기 커밋으로 2452d15에서 aebf24a로 옮겨 갔다. `git log --oneline aebf24a..f41f0b6` — impedance-b에 있고 main에 없는 커밋 — 은 정확히 그 둘을 출력한다.
> - **비예**: 판마다 폴더 하나(`controllers_v2/`, `summarize_final.py`). 파일을 복사하고, 부모 링크가 없고, 병합할 수 없다. 브랜치는 41바이트이고 경로마다 파일을 하나만 둔다.
> - **비예**: 분리된 `HEAD`에서 만든 커밋. 예를 들어 `git bisect`가 옛 커밋을 checkout해 둔 동안(§8). 그것을 가리키는 이름이 없으므로 다른 무엇을 checkout하는 순간 뒤에 남는다. 먼저 브랜치를 준다(`git switch -c <이름>`).
> - **왜 중요한가**: B의 제어기는 impedance-b에서 개발되고 조율되는 동안 main은 돌아가는 분석과 A의 예비 데이터를 지켰다. 끝나지 않은 제어기가 main의 어떤 것도 망가뜨릴 수 없었고, 두 줄기는 기록된 한 점, §4의 병합에서 만났다.

`git switch <브랜치>`는 `HEAD`를 다른 브랜치로 옮기고 작업 트리와 인덱스를 그 브랜치의 끝에 맞춘다. `git switch -c <이름>`은 먼저 지금 커밋에 브랜치를 만든다. 커밋하지 않은 변경을 덮어쓰게 되면 Git은 전환을 거부하므로 먼저 커밋한다(또는 stash한다). 영어 절 그래프의 `HEAD -> main`은 `HEAD`가 main을 가리키고 main이 aebf24a를 가리킨다는 뜻이다. 이 페이지의 모든 히스토리 그림은 `git log --graph`를 따른다. 최신이 위, 각 커밋은 그 아래의 부모와 이어진다.

### 4. 병합과 충돌, 그리고 한 문단의 rebase

*한 문장으로:* 병합은 두 작업 줄기를 각각 가장 좋은 공통 조상과 비교해 합치고, 한쪽만 한 변경은 모두 받아들이며, 양쪽이 같은 줄을 바꾼 곳에서 멈추고, 결과를 부모가 둘인 커밋으로 기록한다.

각각 프로젝트를 바꾼 두 작업 줄기를, 어느 쪽의 변경도 잃지 않고 서로 어긋나는 곳을 짐작하지도 않으면서 하나로 만들어야 한다. 병합하기 전에 두 끝의 공통 부분과 각 쪽이 가져온 것을 본다. 영어 절의 `git merge-base aebf24a f41f0b6`은 2452d15b…를 출력하고, 2452d15에서 aebf24a까지의 `git diff --stat`은 `README.md` 한 줄과 `trials/pilot.csv`(11줄 추가)를, 2452d15에서 f41f0b6까지는 `README.md` 한 줄과 `controllers/impedance.py`(9줄 추가)를 보인다.

병합 기준(merge base)은 impedance-b가 main을 떠난 2452d15다. main은 예비 실험 파일을, 브랜치는 제어기 B를 가져왔고, 양쪽 모두 `README.md`의 한 줄, 상태 줄을 바꾸었다. main에서 `git merge impedance-b`를 실행하면 Git은 `Auto-merging README.md`, `CONFLICT (content): Merge conflict in README.md`, `Automatic merge failed; fix conflicts and then commit the result.`를 출력하고 멈춘다.

그 뒤의 `git status`는 "You have unmerged paths"라고 말하며, `controllers/impedance.py`는 이미 "Changes to be committed"에, `README.md`는 "Unmerged paths"의 "both modified"에 적는다. `cat README.md`는 상태 줄 자리에 충돌 표지를 보인다. `<<<<<<< HEAD`와 `=======` 사이에 main의 `Status: pilot of A recorded (10 trials).`가, `=======`와 `>>>>>>> impedance-b` 사이에 브랜치의 `Status: B tuned on the rig (K = 300 N/m, D = 25 N s/m).`가 있다.

Git은 할 수 있는 것은 병합했다. 제어기 B는 이미 스테이지되어 있다. 해결이란 파일을 참이어야 하는 내용으로 고치는 것 — 여기서는 두 사실을 다 적은 `Status: pilot of A recorded (10 trials); B tuned on the rig (K = 300 N/m, D = 25 N s/m).` — 이고, 스테이지해서 해결했다고 표시하는 것이다. 이어서 `git commit -m "Merge branch 'impedance-b'"`는 `[main 882d5dd] Merge branch 'impedance-b'`를 출력하고, `git cat-file -p HEAD`는 tree 3bb71c43… 아래에 `parent` 줄 둘 — aebf24a5…와 f41f0b66… — 을 보인다.

`parent` 줄이 둘이다. 첫째는 있던 브랜치, 둘째는 병합해 들여온 브랜치다. 충돌이 없었다면 `git merge`가 이 커밋을 스스로 썼을 것이다.

> **삼방향 병합의 정의.** **삼방향 병합**(three-way merge)은 *두 커밋과 그 병합 기준으로 스냅샷 하나를 만들고, 그것을 두 커밋을 부모로 가진 커밋으로 기록하는 연산*이다. 두 히스토리를 이어 붙이는 것도, "새 판이 이긴다"도 아니다. 정의 조건 넷. **병합 기준** $B$는 두 끝, "우리 쪽" $O$(`HEAD`가 가리키는 브랜치)와 "저쪽" $T$의 가장 좋은 공통 조상이다. `git merge-base`가 출력한다. 파일은 **$B$에 대해 영역별로** 비교한다. 한 영역을 바꾼 쪽이 $B$ 그대로 둔 쪽을 이긴다. **양쪽이 같은 영역을 서로 다르게 바꾼** 곳에서는 Git이 두 판을 충돌 표지 사이에 써 두고 멈춘다. 고치고, `git add`하고, 커밋한다. 그리고 결과는 **부모가 $(O, T)$인 병합 커밋**이다 — 다만 $T$가 이미 $O$를 품고 있으면 브랜치는 $T$로 앞으로 옮겨 가기만 하고 병합 커밋은 생기지 않는다(fast-forward, Pro Git §3.2).
>
> $$R_r=\begin{cases}O_r & \text{if } T_r=B_r \text{ or } O_r=T_r\\ T_r & \text{if } O_r=B_r\\ \text{conflict} & \text{otherwise}\end{cases}$$
>
> $r$은 파일 하나의 영역 하나, $O_r$, $T_r$, $B_r$은 그 세 판이다. 다른 모든 경우에는 답이 있으므로, Git은 양쪽이 같은 영역을 서로 다른 글로 바꾼 곳에서만 멈춘다.
>
> - **예**: 882d5dd. `controllers/impedance.py`는 $T$에만 있으므로 받아들이고, `trials/pilot.csv`는 $O$에만 있으므로 유지하며, `README.md`의 상태 줄은 양쪽에서 $B$와 다르고 서로도 다르므로 유일한 충돌이다.
> - **비예**: 충돌 없는 병합이 옳은 병합은 아니다. main이 `analysis/summarize.py`의 함수 `load`의 이름을 바꾸는 동안 브랜치가 `load`를 부르는 스크립트를 더했다면, 모든 영역이 깨끗이 병합되고 결과는 실행할 때 실패한다. Git은 뜻이 아니라 글을 비교하므로, 병합할 때마다 분석을 돌린다.
> - **비예**: fast-forward. 과제의 rebase한 히스토리에서 `git merge impedance-b`는 `Fast-forward`를 출력한다. $O$가 $T$의 조상이었으므로 합칠 것이 없었고, 병합 커밋도 없다.
> - **왜 중요한가**: 병합 커밋은 기록된 만남의 점이다 — 882d5dd부터는 분석, 제어기 B, A의 예비 데이터가 함께 돌아간다고 알려져 있다 — 그리고 충돌은 연구실이 무엇을 뜻했는지 Git이 추측하기를 사양하는 것이다.

**한 문단의 rebase.** 병합하는 대신 impedance-b에서 `git rebase main`을 실행하면 브랜치의 커밋을 하나씩 main의 끝 위에 다시 쌓는다. 다시 쌓은 커밋은 변경과 메시지는 같지만 부모가 새롭고, 그래서 id가 새로운 새 커밋이며, 히스토리는 한 줄이 된다. 최종 스냅샷은 병합이 주었을 것과 같다 — 과제의 rebase한 RS1에서 마지막 tree는 병합한 쪽과 똑같이 e3238a51…이다. 이것을 안전하게 지키는 규칙은 Pro Git의 것(§3.6)이고, 줄여 말하면 이렇다. 이미 자기 저장소 밖에 있는 커밋은 절대 rebase하지 않는다. 다른 사람들이 옛 id 위에 쌓았기 때문이다. 아직 공유하지 않은 자기 브랜치를 나누기 전에 rebase하는 것은 괜찮다. 남이 이미 fetch한 커밋을 rebase하거나 — 또는 amend하거나 squash하면 — 그들의 발밑에서 히스토리를 다시 쓰는 것이고, 해석 과제가 그것이 그들 쪽에서 어떻게 보이는지 보여 준다.

### 5. 원격 저장소, push, pull request

*한 문장으로:* 원격 저장소는 커밋을 주고받는 다른 저장소 — 연구실 서버, GitHub — 이고, 공유 브랜치가 앞으로만 움직이는 한 모든 주고받기는 안전하다.

내 커밋은 연구실 서버와 동료에게, 그들의 커밋은 나에게 가야 하고, 그 길에서 누구의 작업도 덮어쓰이면 안 된다. **원격 저장소**(remote)는 이름 붙은 URL이다. `git clone`은 최신 파일만이 아니라 모든 커밋까지 저장소 전체를 복사하고, 어디서 왔는지를 원격 `origin`으로 기록한다. 여기서 RS1의 연구실 서버는 bare 저장소(작업 트리 없이 공유용으로 만든 저장소)이고, 학생은 그것을 복제한 곳에서 일한다. 영어 절의 `git clone --bare rs1 lab.git`과 `git clone lab.git student`는 각각 `Cloning into bare repository 'lab.git'...`, `Cloning into 'student'...`와 `done.`을 출력한다.

(여기서 "서버"는 클론들 옆의 디렉터리이고, 각 클론의 `origin`은 상대 경로 `../lab.git`으로 바꿔 두었다. 팀에서는 `origin`이 GitHub나 연구실 서버의 URL이다.) 클론 안에서 `git remote -v`는 `origin ../lab.git`을 fetch용과 push용으로 한 줄씩, `git branch -a`는 `main`과 `remotes/origin/HEAD -> origin/main`, `remotes/origin/impedance-b`, `remotes/origin/main`을, `git status`는 `Your branch is up to date with 'origin/main'.`을 출력한다.

`origin/main`은 **원격 추적 브랜치**(remote-tracking branch)다. 마지막으로 서버와 이야기했을 때 main이 서버에서 어디 있었는지에 대한, 자기 저장소의 기록이다. 거기에 커밋할 수는 없고, 데이터를 주고받을 때 Git이 옮긴다(Pro Git §3.5). `git status`의 "up to date"는 main을 서버 자체가 아니라 그 기록과 비교한 것이다. 주고받기는 명령 셋이 하고, 태그에는 따로 규칙이 있다.

- `git fetch`는 없는 커밋을 내려받고 원격 추적 브랜치를 옮긴다. 자기 브랜치나 작업 트리는 절대 건드리지 않는다.
- `git pull`은 fetch 뒤에 upstream 브랜치를 자기 브랜치에 통합한다. 설정이 없으면 fast-forward만 한다. 둘이 갈라졌으면 멈추고 병합과 rebase 가운데 고르라고 한다(git-pull 문서, 그리고 이 절 뒤쪽에서 보는 출력).
- `git push`는 자기 커밋을 보내고 서버에 그 브랜치를 자기 끝으로 옮겨 달라고 한다. 서버는 fast-forward만 받아들인다 — 서버의 지금 끝이 자기 끝의 조상이어야 한다(git-push, PUSH RULES) — 강제하지 않는 한.
- 태그는 요청할 때만 간다. `git push origin pilot-v1`, 또는 전부는 `--tags`(Pro Git §2.6).

이 페이지의 어떤 명령도 어디로 push하지 않으므로, 영어 절은 push를 문서가 주는 그대로 "여기서 실행하지 않음"으로 표시해 보인다. `git push origin main`은 fast-forward일 때만 받아들여지고, `git push --force-with-lease origin main`은 `origin/main`이 마지막으로 fetch한 그대로일 때만 덮어쓴다.

같은 서버를 복제한 연구실 동료가 main의 마지막 공유 커밋 둘을 하나로 squash하면, push해 보기 전에 push가 무엇을 할지 본다. 영어 절의 `git reset --soft HEAD~2`와 `git commit -m "Add the figure script and fix the trial parser"`는 새 커밋 `[main 41cea18]`을 만들고, `git status`는 `Your branch and 'origin/main' have diverged, and have 1 and 2 different commits each, respectively.`를 출력한다.

"1과 2": 동료에게는 서버에 없는 41cea18이 있고, 서버에는 동료의 main에 더는 없는 3568180과 ea13bc4가 있다. 보통의 push는 거부된다. `--force`는 서버의 main을 41cea18로 옮기고 나머지 둘을 모든 사람의 미래에서 떨어뜨릴 것이다. main이 `origin/main`에서 같은 식으로 갈라진 클론 — 해석 과제의 학생 클론 — 에서는 `git pull`도 멈춘다. 영어 절의 출력(가르치는 줄만 남겼다)은 `hint:` 줄로 병합(`pull.rebase false`), rebase(`pull.rebase true`), fast-forward만(`pull.ff only`) 가운데 고르는 설정을 안내하고, `fatal: Need to specify how to reconcile divergent branches.`로 끝난다.

이 모두의 뒤에 있는 규칙에는 이름이 있다. **fast-forward**는 참조를 커밋 $A$에서, $A$를 히스토리에 가진 커밋 $B$로 옮기는 갱신이다. 옛 끝이 닿던 모든 커밋에 여전히 닿으므로 히스토리는 자라기만 한다. 수로 말하면 $A\to B$가 fast-forward인 것은 정확히 $|B..A|=0$일 때이고, 그것은 `git rev-list --count B..A`가 출력하는 수다. 브랜치로의 push는 강제하지 않는 한 fast-forward일 때만 받아들여진다. 그 밖의 갱신은 새 끝 위에 쌓는 모든 사람에게 "히스토리를 잃게" 하기 때문이다(git-push). "behind 'origin/main' by 1 commit, and can be fast-forwarded"인 클론(§8이 이것을 출력한다)은 `git pull`로 아무것도 잃지 않는다. 동료의 ea13bc4 → 41cea18은 fast-forward가 아니다 — squash가 ea13bc4를 대체했으므로 $|41cea18..ea13bc4|=2$(3568180과 ea13bc4)다 — 그래서 강제한 갱신만이 그것을 할 수 있고, 그 뒤 병합으로 pull하는 다음 사람이 떨어진 커밋들을 중복으로 되살린다(Pro Git §3.6). GitHub는 보호된 브랜치의 force push를 기본으로 막는다.

**pull request와 리뷰.** GitHub에서 공유 main에 작업을 올리는 일상적인 방법은 main에 push하지 않는 것이다. 자기 브랜치, 예컨대 impedance-b를 push하고 **pull request**를 연다. 그 브랜치(head)를 다른 브랜치(base)에 병합하자는 제안으로, 토론할 자리가 붙은 diff 하나로 보인다. 리뷰어는 세 종류의 리뷰 — 의견(comment), 승인(approve), 변경 요청(request changes) — 가운데 하나를 남기고, 저장소 관리자는 main을 보호해 pull request가 승인 리뷰를 받아야만 병합되게 하고 누구도 force push하거나 지우지 못하게 할 수 있다(GitHub Docs, "About pull request reviews"와 "About protected branches"). draft pull request는 진행 중인 작업을 나누며 병합할 수 없다. 연구에서는 논문의 어떤 숫자가 분석의 변경에 기대기 전에 두 번째 사람이 그 변경을 읽는 곳이 여기이고 — dda4b0f 같은 회귀(§8)의 diff가 잡힐 가장 좋은 기회였던 곳이다.

### 6. 커밋하면 안 되는 것

*한 문장으로:* 커밋한 것은 모든 클론의 히스토리에 영원히 남으므로, 큰 기록, 학습된 가중치, 비밀은 절대 커밋에 들어가면 안 되고, 나중 커밋에서 지워도 아무것도 없어지지 않는다.

무언가를 한 번 커밋해 나누고 나면 사실상 영구적이다. 실수로 커밋한 60 MiB짜리 bag이나 비밀번호는 그냥 지울 수 없다. 방어는 처음부터 그런 파일을 들이지 않는 것이다.

**무시 목록.** `.gitignore` 파일은 Git이 추적하지 않고 둘 파일의 패턴을 나열한다. 이 파일도 커밋되므로 모든 클론이 나눠 쓴다(gitignore 문서). 영어 절에 RS1의 첫 커밋의 목록이 있다. colcon의 `build/`, `install/`, `log/`, 시행 기록인 `bags/`, `*.mcap`, `*.db3`, 모델 가중치와 큰 배열인 `*.pt`, `*.npz`, Python 캐시 `__pycache__/`, 그리고 자격 증명 `.env`다.

끝의 슬래시는 디렉터리에만 맞는다. `*`는 슬래시를 뺀 무엇에든 맞는다. 끝 말고는 슬래시가 없는 패턴은 모든 깊이에 적용된다. `#`로 시작하는 줄은 주석이다. 무시 목록은 **추적되지 않는** 파일에만 작용한다. 이미 추적하는 파일은 `git rm --cached`가 인덱스에서 빼기 전까지 계속 추적된다(gitignore 문서). colcon 디렉터리들은 [[04-robotics/ros2/workspaces-packages-launch|25.4 §2]]가 무시하라고 하는 그것이다. 새 파일 셋을 둔 RS1 클론에서 목록이 무엇을 잡고 무엇을 놓치는지: 영어 절의 `git status --short --ignored`는 `?? config/`, `!! bags/`, `!! config/.env`를, `git check-ignore -v`는 `.gitignore:7:bags/`(bag 파일)과 `.gitignore:19:.env`(`config/.env`)를 출력하고 `config/dashboard.env`에 대해서는 아무것도 출력하지 않는다.

`!!`는 무시된 경로, `??`는 추적되지 않는 경로다. `git check-ignore -v`는 맞은 규칙 — 7번 줄의 `bags/`, 19번 줄의 `.env` — 을 대고, `config/dashboard.env`에 대해서는 아무 말도 하지 않는다. 패턴 `.env`는 이름이 정확히 `.env`인 파일에만 맞으므로, `dashboard.env`라는 자격 증명 파일은 전혀 무시되지 않고, `git add config/`는 그것을 다음 커밋에 스테이지할 것이다. 경로가 무시되어 있으면 Git은 add를 거부한다. 영어 절의 `git add trials/B07.mcap`은 `The following paths are ignored by one of your .gitignore files:`와 `hint: Use -f if you really want to add them.`을 출력한다 — 누군가 `-f`를 쓰기 전까지는.

**나중에 지워도 소용없는 이유.** Git은 무언가가 객체로 이어지는 한 그 객체를 보관한다. A의 열 줄만 담은 예비 실험 파일의 첫 판은, main의 파일이 이제 스무 줄인데도 RS1 저장소에 그대로 있다. 영어 절의 `git log --oneline -- trials/pilot.csv`는 그 파일을 건드린 커밋 둘, 2006419와 aebf24a를 나열하고, `git show aebf24a:trials/pilot.csv`는 헤더와 A의 열 줄을 그대로 출력한다.

> **닿을 수 있음의 정의.** 객체가 저장소에서 **닿을 수 있다**(reachable)는 것은 *그 저장소의 어떤 참조가 그 객체로 이어진다*는 뜻이다. 객체 하나와 한 저장소의 참조들 사이의 관계이지, 객체 혼자의 성질이 아니다. 정의 조건 넷. 걸음은 **참조에서 시작한다**. 브랜치, 태그, 원격 추적 브랜치, 인덱스, reflog 항목, 그 밖의 `refs/` 아래 무엇이든이다(git-gc 문서). **모든 링크를 따른다**. 커밋에서 부모와 tree로, tree에서 항목으로, 태그에서 그 객체로. 객체는 그 저장소에서 **닿을 수 있는 동안** 남는다. 그리고 **클론마다 자기 참조가 있으므로** 닿을 수 있음 — 그리고 그와 함께 삭제 — 은 클론마다 따로 정해진다.
>
> $$\mathrm{kept}_{\mathcal R}(o)\iff \exists\,r\in\mathcal R:\ o\in\mathrm{reach}(r)$$
>
> $\mathcal R$은 한 저장소의 참조 집합, $\mathrm{reach}(r)$은 $r$에서 부모, tree, 항목, 태그 대상을 따라 찾을 수 있는 모든 것이다. 그러므로 객체는 그 저장소의 어떤 참조도 그리로 이어지지 않을 때에만 사라지고, 내 저장소에서 떠났다고 남의 클론에서 사라지지는 않는다.
>
> - **예**: 영어 절이 출력한 11줄짜리 예비 실험 파일. main은 2006419에 닿고, 2006419는 조상 aebf24a에 닿고, aebf24a의 tree는 그 blob에 닿는다. `git show aebf24a:trials/pilot.csv`가 그것을 출력한다.
> - **비예**: "다음 커밋에서 파일을 지웠다." 새 커밋의 tree에는 그 파일이 없지만 옛 커밋은 여전히 main의 조상이므로, 그 blob은 main에서 계속 닿는다 — 내 클론에서도, 서버에서도, 그 뒤에 만든 모든 클론에서도.
> - **왜 중요한가**: bag이나 키는 한 번 커밋되어 fetch되면 모든 사본의 히스토리에 있다. 그것을 없애려면 그것이 들어 있는 히스토리를 다시 써야 하고, 그러면 그 커밋과 그 뒤 모든 커밋의 id가 바뀌며(§1), 남들이 이미 가진 클론과 fork에는 닿지 못한다(GitHub Docs, "Removing sensitive data"). 내 컴퓨터 안에서도 `git gc`는 reflog가 아직 닿는 것을 보관한다 — 기본으로 90일, 브랜치의 지금 끝이 더는 그 항목에 닿지 않으면 30일(git-gc 문서).

**기록, 데이터셋, 가중치.** bag(rosbag2의 디렉터리, [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]), 데이터셋, 체크포인트는 크고, 바이너리이고, 한 번 쓰고 끝이다. GitHub는 50 MiB보다 큰 파일을 더하면 경고하고 100 MiB보다 큰 파일은 막으며, 저장소를 이상적으로는 1 GB 아래, 어떤 경우에도 5 GB 아래로 두라고 권한다(GitHub Docs, "About large files on GitHub"). 그리고 모든 클론은 아무리 오래된 것이든 히스토리 전체를 내려받는다. 기록은 연구실 데이터 서버에 두고, 그것을 식별하는 것 — bag의 이름과 그 바이트의 체크섬 — 을 커밋한다. 체크섬은 객체 id가 blob에 이름을 붙이듯 데이터에 이름을 붙인다(§1). Git LFS — 큰 파일을 저장소 밖에 두고 작은 포인터를 대신 커밋한다 — 와 GitHub release가 GitHub 스스로 큰 바이너리에 권하는 두 길이다. 이 페이지는 둘 다 가르치지 않는다. 대상으로 한 번 끝까지가 RS1의 bag 84개에 값을 매긴다. bag, Parquet 표, HDF5 파일이 무엇을 담는지는 [[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식 §8]]이고, 리그의 CAD 파일도 저장소에 들어간다. 원본 파일과 내보낸 파일을 리비전 이름과 함께 둔다([[02-foundations/tools/mechanical-design-fabrication|12.9 실험을 위한 기계 설계와 제작 §1]]).

**비밀.** 토큰, 비밀번호, 개인 키, 클라우드 자격 증명은 절대 추적되는 파일에 들어가지 않는다. 코드는 그것을 환경 변수(`os.environ["RS1_DASHBOARD_TOKEN"]`)나, 무시 목록이 정확한 이름으로 덮는 추적되지 않는 파일에서 읽는다. GitHub의 push protection은 알아보는 비밀이 든 push를 막고, 공개 저장소로의 push에 대해 기본으로 켜져 있다 — 다만 아는 패턴에 대해서만이고, 쓰기 권한이 있는 사람은 이유를 밝히고 우회할 수 있다(GitHub Docs, "About push protection"). 키가 커밋되고 말았다면 GitHub 자신의 순서가 옳다. **먼저 키를 폐기하거나 교체한다** — 폐기한 키는 어디에 있든 해가 없다 — 그리고 그다음에야 `git filter-repo` 같은 도구로 히스토리를 다시 쓸 가치가 있는지 정한다. 그 뒤 모든 커밋의 id가 바뀌고, fork와 이미 있는 클론은 옛 커밋을 가진다는 것을 알고서다.

### 7. 실험마다 태그 하나, 표마다 커밋 하나

*한 문장으로:* 실험마다 annotated tag를 붙이고, 결과 표마다 그 표를 만든 커밋을 표 자체에 찍고, `-dirty` 도장이 찍힌 표는 어떤 커밋도 재현할 수 없는 표로 다룬다.

몇 달 뒤 리뷰어가 표 1을 낸 코드가 무엇이냐고 묻는다. "3월쯤의 판"은 답이 아니다. 두 습관이 더 나은 답을 준다.

**실험마다 태그 하나.** 태그는 커밋 하나의 이름이고, 브랜치와 달리 움직이지 않는다. **annotated tag**는 자기 id, 태그한 사람, 날짜, 메시지를 가진 온전한 객체이고, lightweight tag는 이름일 뿐이다(Pro Git §2.6). Git 매뉴얼은 annotated tag를 릴리스용으로, lightweight tag를 개인적이거나 임시적인 표지용으로 여기며, `git describe`는 따로 말하지 않으면 lightweight tag를 무시한다(git-tag, git-describe). 그래서 실험에는 annotated tag를 붙인다. RS1에는 둘이 있고, 메시지에 서로 다른 뜻이 적혀 있다. pilot-v1은 예비 실험 표를 낸 커밋을, study-v1은 본 실험 첫 시행 전에 고정한 코드를 가리킨다. 영어 절에서 `git tag -a pilot-v1 -m "…"` 뒤의 `git cat-file -p pilot-v1`은 태그 객체 — `object 20064191…`, `type commit`, `tag pilot-v1`, `tagger RS1 Student <student@example.com> 1773160200 +0000`, 빈 줄, 메시지 — 를 출력하고, `git describe --long`은 `pilot-v1-0-g2006419`를 출력한다.

두 규칙이 태그를 믿을 만하게 지킨다. 남이 fetch한 태그는 **절대 옮기지 않는다**. `git fetch`는 누군가 이미 가진 태그를 바꾸지 않으므로, 태그를 옮기면 세상에 "pilot-v1"이 둘 생긴다. 매뉴얼의 조언은 실수를 인정하고 새 이름, pilot-v1.1을 쓰라는 것이다(git-tag, "On Re-tagging"). 그리고 태그는 **따로 push한다**. `git push`는 기본으로 태그를 보내지 않는다(§5). 어느 태그를 어디에 붙이는지, 연구가 코드 말고 무엇을 기록해야 하는지 — 시드, 보정, 설정, 원시 로그, 제외 — 는 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §7]]이고, 반복 가능·재현 가능·재연 가능의 어휘는 그 페이지의 §6이다.

**표마다 커밋 하나.** RS1의 분석 스크립트는 숫자를 하나라도 출력하기 전에 자기를 돌린 코드의 판을 출력한다. 영어 절에 실린 `analysis/summarize.py`의 두 줄이 그 일을 한다. `git describe --long --always --dirty`의 결과를 `code:` 줄에, `git rev-parse HEAD`의 결과를 `commit:` 줄에 찍는다. pilot-v1에서 이 스크립트는 예비 실험 표 — [[06-research-practice/scientific-writing-peer-review|4. 과학적 글쓰기와 peer review]]가 논문의 표 1로 만드는 바로 그 표 — 를 출력한다. `code:   pilot-v1-0-g2006419`, `commit: 20064191fe47e9c20677136f53f58a693e5aaf05`, 그리고 A: 10회, 6/10, 10.66, 2.414와 B: 10회, 9/10, 7.50, 1.356이다.

첫 줄은 사람을 위한 것이고 둘째 줄은 기계를 위한 것이다. 마흔 자리는 줄인 형태와 달리 결코 모호해지지 않는다(§1). `--long`은 태그가 붙은 커밋에서도 id를 남긴다. 그냥 `git describe`는 거기서 `pilot-v1`만 출력했을 것이다. `--always`는 닿는 태그가 없는 곳에서 맨 id로 물러선다.

> **describe 도장의 정의.** 커밋의 **describe 도장**(describe stamp)은 *히스토리로부터 계산한, 사람이 읽을 수 있는 이름: 가장 가까운 태그, 그 너머 커밋 수, 커밋의 줄인 id*다. 계산한 이름이지 저장된 이름이 아니고, 누가 정한 버전 번호도 아니다. 정의 조건 넷. $t$는 **그 커밋에서 닿는 가장 최근의 annotated tag**다 — 여럿이면 사이의 커밋이 가장 적은 것이다. $n$은 **그 커밋에서는 닿고 태그에서는 닿지 않는 커밋의 수**로, `git log t..c`가 나열할 바로 그것이다. 이어서 `g`와 **최소 7자리**의 커밋 id가 오고, 저장소가 커지면 더 길어진다. 그리고 `--dirty`를 주면 **추적하는 파일이 커밋과 다를 때 `-dirty`가 붙는다**(git-describe 문서).
>
> $$\mathrm{describe}(c)=t\text{-}n\text{-g}\,\bar h(c)\,[\text{-dirty}],\qquad n=\big|\,t\,..\,c\,\big|$$
>
> $\bar h(c)$는 줄인 id, $|t..c|$는 $c$에서는 닿고 $t$에서는 닿지 않는 커밋의 수다. id가 들어 있으므로, 도장은 $c$를 정확히 가리키면서 태그 붙은 실험에서 얼마나 떨어졌는지도 말한다.
>
> - **예**: HEAD, `study-v1-3-gea13bc4`. study-v1은 6321a22를 가리키고, ea13bc4에서 닿지만 6321a22에서는 닿지 않는 커밋이 셋 — b659311, 3568180, ea13bc4 — 이다.
> - **비예**: 추적되지 않는 파일. 추적되지 않는 새 `notes.txt`가 있는 RS1 클론에서 `git describe --long --dirty`는 여전히 `study-v1-3-gea13bc4`를, `-dirty` 없이 출력했다(이 정의 뒤의 실행). 추적되지 않는 스크립트가 계산한 표는 깨끗한 도장을 단다. `git status --porcelain`은 추적되지 않는 파일까지 나열하므로, 실행 전 점검은 그것이 아무것도 출력하지 않는 것이다.
> - **비예**: $n$을 main을 따라 잰 거리로 읽기. 병합을 건너면 $n$은 병합해 들인 브랜치의 커밋까지 센다. 유도 과제가 하나를 푼다.
> - **왜 중요한가**: 표에 찍힌 도장은 그 표를 만든 코드의 주소다. A의 9회 옆에서 `study-v1-1-gb659311`을 본 독자는 이유를 보려면 어느 커밋을 checkout해야 하는지 정확히 안다(§8).

첫 비예 뒤의 실행 — 추적되지 않는 파일, 그다음 고친 파일 — 은 영어 절에 있다. 처음 `git describe --long --dirty`는 `study-v1-3-gea13bc4`, `notes.txt`를 만든 뒤에도 `study-v1-3-gea13bc4`이고, 그때 `git status --porcelain`은 `?? notes.txt`를 출력한다. 이어서 성공 한계를 `sed`로 12 N으로 바꾸면 도장은 `study-v1-3-gea13bc4-dirty`가 되고, `git status --porcelain`은 ` M analysis/summarize.py`와 `?? notes.txt`를 출력한다.

작업 트리에서 성공 한계를 12 N으로 바꾸자 도장이 `-dirty`가 되었다. 지금 출력하는 표는 어떤 커밋에도 없는 코드에서 나온 숫자를 싣게 된다. (고친 내용은 새 파일에 쓴 뒤 이름을 바꾼다. 제자리 편집 `sed -i`의 철자가 Ubuntu의 GNU `sed`와 macOS의 BSD `sed`에서 다르기 때문이다.) 프로토콜의 시행 전 점검표 — 커밋 6321a22 — 가 첫 시행 전에 요구하는 것이 정확히 이것이다. 도장을 시행 로그에 적고, `-dirty`로 끝나면 시작하지 않는다. [[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]은 다시 돌리는 데 필요한 나머지 입력 — 컨테이너, bag, 파라미터, 명령 — 을 더해 *고정된 실행*(pinned run)을 만든다. 커밋은 그 첫째다.

### 8. 결과를 망가뜨린 커밋 찾기와 되돌리기

*한 문장으로:* 숫자가 바뀌었는데 아무도 이유를 모를 때, `git bisect`는 그것을 바꾼 첫 커밋을 약 $\log_2 N$번의 시험으로 찾고, `git revert`는 그 커밋을 히스토리를 지우지 않고 새 커밋을 더해 되돌린다.

**증상.** 3월 25일 결과 절 초안을 쓰면서 출력한 표가 예비 실험과 맞지 않았다. 영어 절의 출력은 `code:   study-v1-1-gb659311` 아래 A: 9회, 5/9, 10.94, 2.377과, 그대로인 B: 10회, 9/10, 7.50, 1.356이다.

A가 10회가 아니라 9회다. 도장은 어느 커밋이 표를 출력했는지(b659311)는 말하지만 어느 커밋이 망가뜨렸는지는 말하지 않는다. pilot-v1의 표는 옳았고, 이틀 뒤 그림 스크립트의 커밋 3568180에서 탐색을 시작할 때에는 pilot-v1 뒤에 커밋이 여섯 개 있다.

**시험.** 이분 탐색에는 어느 커밋에 대해서든 good인지 bad인지 말해 주는 명령, 그리고 모든 커밋에 대해 같은 명령이 필요하다. 그래서 그 명령은 옛 커밋을 checkout해도 바뀌지 않는 저장소 밖, 곁에 산다. 영어 절의 `pilot_check.py`는 `analysis/summarize.py`를 돌려 A의 줄이 10회, 6/10, 10.66이면 0으로, 아니면 1로 끝난다.

`git bisect run`은 종료 코드를 읽는다. 0은 good, 125를 뺀 1–127은 bad, 125는 "이 커밋은 시험할 수 없으니 건너뛰라"다(git-bisect 문서). `HEAD`가 3568180일 때 영어 절의 실행(끝부분을 줄였다)을 따라가 보자. `git rev-list --count pilot-v1..HEAD`는 6을 출력한다. `git bisect start HEAD pilot-v1`은 bad 커밋을 먼저, good 커밋을 다음에 대고, 가운데 커밋 041fe2f를 checkout하며 `Bisecting: 2 revisions left to test after this (roughly 2 steps)`를 출력한다. "roughly 2 steps"는 이번 시험 뒤에 남은 시험을 센다. `git bisect run python3 ../pilot_check.py`는 041fe2f(bad), dda4b0f(bad), a0cd3a3(good)을 차례로 시험하고 `dda4b0f… is the first bad commit`으로 끝낸다. 시험 세 번이다. `git bisect reset`은 시작한 브랜치로 돌아간다.

그 커밋이 한 일은 영어 절의 `git show dda4b0f`(끝의 바뀌지 않은 문맥 줄 둘을 줄였다)가 보인다. `import csv`를 지우고, `csv.DictReader` 대신 `f.read().splitlines()[2:]`로 줄을 읽는다. `[2:]`는 두 줄, 헤더와 시행 A1을 건너뛴다. `[1:]`이었다면 헤더만 건너뛰었을 것이다. 문자 하나를, 시험 세 번으로 찾았다.

> **이분 탐색의 정의.** **이분 탐색**(bisection, `git bisect`)은 *good으로 알려진 커밋과 bad로 알려진 커밋 사이의 커밋들 위에서, 시험이 처음 실패하는 커밋을 찾는 이진 탐색 절차*다. 디버거도 아니고 그 자체로 시험도 아니다. 정의 조건 넷. **good 커밋** $g$와 **bad 커밋** $b$가 필요하고, $g$는 $b$의 히스토리에 있어야 한다. 모든 커밋에 대해 같은, good인지 bad인지 정하는 **시험 하나**가 필요하다 — 저장소 밖에 둔다. 그 성질은 히스토리를 따라 **단조**여야 한다. 범위 안에서 한 번 bad면 뒤의 모든 커밋에서 bad다. [[02-foundations/algorithms/sorting-divide-conquer|11.3 §6]]의 단조 술어다. 그리고 **시험마다 첫 bad 커밋일 수 있는 커밋을 대략 반으로 줄인다**. 시험할 수 없는 커밋은 건너뛰는데(종료 코드 125), 시험이 늘고 "이것들 가운데 하나"라는 답이 나올 수 있다.
>
> $$s=\big\lceil\log_2 N\big\rceil,\qquad N=\big|\,g\,..\,b\,\big|$$
>
> $N$은 후보의 수 — $b$에서는 닿고 $g$에서는 닿지 않는 커밋, $b$ 포함 — 이고, $s$는 최악의 경우 시험 수다. 시험 하나가 후보를 많아야 $\lceil N/2\rceil$개 남기므로 $s$번 뒤에는 많아야 $\lceil N/2^s\rceil$개가 남고, $2^s\ge N$이면 그것이 하나이기 때문이다.
>
> - **예**: $g=$ pilot-v1, $b=$ 3568180. `git rev-list --count`가 출력한 $N=6$이므로 $s=\lceil\log_2 6\rceil=3$이고, 위에서 따라간 실행은 시험 세 번을 썼다. 한 학기 200 커밋이면 8번이다.
> - **비예**: 들쭉날쭉한 시험 — 같은 커밋을 돌려도 어떤 때는 실패하는 시험, 예컨대 바쁜 컴퓨터에서 타이밍에 기대는 시험. 그러면 술어가 커밋의 성질이 아니게 되고, 이분 탐색은 주사위가 떨어진 곳일 뿐인 커밋을 돌려준다. 범위 안에서 생겼다가 고쳐졌다가 다시 생긴 버그도 마찬가지다. 성질이 단조가 아니므로 답은 두 번의 도입 가운데 하나이고, 쫓는 그것이라는 보장이 없다.
> - **왜 중요한가**: diff 여섯 개는 읽을 수 있지만 이백 개는 읽을 수 없다. 이분 탐색은 "이번 학기 언젠가 숫자가 바뀌었다"를 커밋 하나와 diff 하나로 바꾼다 — 여기서는 `1`이어야 했던 `2` 하나다.

**되돌리기: reset이 아니라 revert.** dda4b0f를 없애는 길은 둘이고, 공유 브랜치에서 안전한 것은 하나뿐이다. `git revert`는 지정한 커밋의 변경을 거꾸로 한 새 커밋을 기록한다(git-revert 문서). 히스토리는 자라기만 하므로, 다른 모든 사람의 다음 pull은 fast-forward다. 영어 절에서 `git revert --no-edit dda4b0f`는 `[main ea13bc4] Revert "Parse trials without the csv module"`를 출력하고, 그 뒤 분석 스크립트는 `code:   study-v1-3-gea13bc4` 아래 A: 10회, 6/10, 10.66, 2.414를 다시 출력한다.

예비 실험의 줄이 돌아왔고, 도장은 어느 커밋이 되돌렸는지 말한다. `git reset`은 다른 일을 한다. 지금 브랜치를 다른 커밋으로 옮기고, `--hard`면 인덱스와 작업 트리까지 덮어써 커밋하지 않은 변경을 버린다(git-reset). RS1 클론에서 영어 절의 `git reset --hard HEAD~1`은 `HEAD is now at 3568180 Add the figure script`를 출력하고, 이어 `git status`는 `Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.`를 출력한다.

main은 ea13bc4를 뒤에 두고 왔지만 서버에는 아직 그것이 있다. 서버를 맞추려면 강제 push, §5의 fast-forward가 아닌 갱신이 필요하다. 규칙: **남이 가졌을 수 있는 것은 revert하고, reset·amend·squash는 아무도 fetch하지 않은 것에만 한다** — git-reset 매뉴얼의 커밋 되돌리기 경고도, 커밋을 이미 남에게 주었다면 하지 말라는 것이다. 로컬에서 reset이나 rebase가 잘못되면 `git reflog`가 `HEAD`가 거쳐 온 곳을 나열하고, "사라진" 커밋은 그렇게 다시 찾는다. reflog는 자기 클론에만 있고 §6이 말한 대로 만료된다.

### 9. 여러 저장소에 걸친 워크스페이스

*한 문장으로:* 로봇의 워크스페이스는 자기 저장소와 다른 저장소에 사는 드라이버·라이브러리를 합친 것이고, 그 하나하나가 커밋 id로 고정될 때에만 재현 가능하다 — superproject 안의 submodule로든, `.repos` 파일 안의 해시로든.

로봇이 그사이 움직인 다른 저장소의 드라이버도 함께 돌린다면, RS1의 커밋을 아는 것만으로는 모자라다. ROS 2 워크스페이스는 빌드하는 모든 패키지를 `src/` 아래에 둔다([[04-robotics/ros2/workspaces-packages-launch|25.4 §2]]). 실제 로봇에서는 그 패키지들이 여러 저장소에서 온다. RS1 자신의 것, P2의 관절 증폭기 드라이버, 어쩌면 제조사의 힘 센서 드라이버. 이것들을 함께 고정하는 흔한 방법이 둘 있다.

**submodule.** 워크스페이스 자체가 Git 저장소 — *superproject* — 가 되어, 다른 저장소를 항목 하나로 기록한다. 그 파일이 아니라 그 커밋 하나의 id다. 여기서는 두 저장소가 이미 `src/`에 있었으므로 `git submodule add`가 아무것도 복제하지 않고 그것들을 스테이지했다. URL은 한 번도 연결하지 않는 자리표시자다. 영어 절의 두 `git submodule add`는 각각 `Adding existing repo at 'src/p2_driver' to the index`와 `… 'src/rs1' …`을 출력하고, `.gitmodules`에는 submodule마다 `path`와 `url`이 적힌다. 커밋 뒤 `git ls-tree HEAD src/`는 `160000 commit 2e8b7cd1… src/p2_driver`와 `160000 commit ea13bc45… src/rs1`을, `git submodule status`는 두 id와 함께 각각의 describe 결과 `(heads/main)`과 `(study-v1-3-gea13bc4)`를 출력한다.

모드 `160000`은 "디렉터리 자리에 다른 저장소의 커밋"을 뜻하는 Git의 표지다(Pro Git §7.11). 함정은 반대편에 있다. superproject를 그냥 복제하면 고정은 기록되지만 파일은 오지 않는다. 영어 절에서 `git clone rs1_ws ws_clone` 뒤의 `git submodule status`는 두 id 앞에 `-`를 붙여 출력한다.

앞의 `-`는 "초기화되지 않음"이다. `src/rs1`과 `src/p2_driver`는 있지만 비어 있다. `git submodule update --init`이 고정된 커밋을 저마다 가져와 분리된 `HEAD`로 checkout하고, `git clone --recurse-submodules`는 두 단계를 한 번에 한다(git-submodule, Pro Git §7.11). 자리표시자 URL은 아무 데로도 이어지지 않으므로 둘 다 여기서는 실행하지 않았다.

그러니 **submodule**은 사본이 아니라 고정이다. superproject의 tree는 다른 저장소의 커밋 하나의 id를 담고, `.gitmodules`는 그것을 어디서 가져올지 말하며, 고정을 옮기는 것은 superproject의 커밋이다 — `src/rs1` 안에서 커밋해도 superproject가 새 id를 기록하기 전까지는 누구에게도 아무것도 바뀌지 않는다. 워크스페이스의 커밋 1654d5b는 `src/rs1`을 ea13bc4에, `src/p2_driver`를 2e8b7cd에 고정한다. 그래서 "로봇은 워크스페이스 1654d5b를 돌렸다"는 결과 뒤의 모든 저장소를 가리키고, "RS1 ea13bc4"는 그 옆의 드라이버에 대해 아무것도 말하지 않는다. Pro Git §7.11이 꼽는 흔한 함정은 superproject의 커밋을 그것이 가리키는 submodule 커밋보다 먼저 push하는 것이다. 고정은 그 서버에 실제로 있는 커밋이어야 한다.

**`.repos` 파일.** ROS 세계는 워크스페이스를 버전 관리하지 않고, 그 저장소들을 `vcs` 도구가 읽는 YAML 파일에 나열하는 쪽이 더 흔하다. 형식은 `repositories` 키 아래 경로마다 항목 하나이고, 항목마다 `type`, `url`, `version` — 브랜치, 태그, 또는 커밋 id — 이 있다(vcstool README). 영어 절의 파일은 RS1의 워크스페이스를 해시로 고정한다. `p2_driver`는 2e8b7cd149ac8323357065df2df88ea0958ed588에, `rs1`은 ea13bc450f2ba5b2082b9077c3935b5ecbe330bb에.

이 페이지를 만든 기계에는 vcstool이 설치되어 있지 않으므로, 영어 절은 두 명령을 README와 소스가 주는 그대로 "여기서 실행하지 않음"으로 표시해 보인다. `vcs import src < rs1.repos`는 항목마다 `src/<경로>`에 복제하고 그 버전을 checkout하며, `vcs export --exact src > rs1.repos`는 저장소마다 브랜치가 아니라 지금 커밋의 id를 쓴다.

`vcs export`는 브랜치의 끝에 있는 저장소에 대해 브랜치 이름을 쓰고, README는 그러면 나중의 import가 더 새로운 판을 가져올 수 있다고 경고한다. `--exact`는 대신 커밋 id를 쓴다. 그러니 버전이 브랜치 이름인 `.repos` 파일은 아무것도 고정하지 않는다. 브랜치는 움직이므로 같은 파일이 날마다 다른 코드를 준다. ROS 2 자신의 소스 빌드도 `.repos` 파일을 같은 식으로 쓴다 — 배포판 브랜치의 `ros2.repos` 파일을 `vcs import --input`으로 — 그리고 그 파일은 `jazzy` 같은 브랜치 이름을 나열한다. 배포판을 따라가기에는 옳고 연구를 얼리기에는 틀리다.

> [!note]- 더 깊이 · Deeper
> `vcs import`는 없는 저장소를 복제한다. 같은 URL로 이미 있는 저장소는 fetch한 뒤 적힌 버전을 checkout하고, 디렉터리에 다른 저장소가 있으면 오류로 멈춘다 — `--force`(디렉터리를 지운다)나 `--skip-existing`을 주지 않는 한(vcstool, `import_.py`와 `clients/git.py`). ros-infrastructure 조직은 `vcs` 명령과 `.repos` 형식을 그대로 둔 vcstool의 fork, vcs2l을 유지하며, 그대로 갈아 끼울 수 있는 대체품으로 소개한다.

**무엇을 쓸까.** 워크스페이스 자체가 버전 관리되는 대상이어야 할 때 — 커밋마다 모든 부분을 고정하는 학위논문 저장소 — 는 submodule. 제3자 저장소 여럿이 든 평범한 `src/`라는 ROS 관례를 따를 때는 커밋 id를 적은 `.repos` 파일이다. 그 파일은 그것이 고정하는 결과를 낸 코드 곁, 자기 저장소에 커밋한다. 어느 쪽이든 §7의 규칙이 로봇 전체로 넓어진다. 결과 뒤의 모든 저장소가 커밋 id로 불릴 때에만 그 결과는 재현 가능하다.

### 대상으로 한 번 끝까지 · Worked case

고정된 저장소 위에서 RS1의 캠페인을 처음부터 끝까지 따라간다. id가 붙은 그래프, 고친 숫자 하나가 id에 하는 일, 어느 커밋이 어느 표를 냈는지, 회귀 탐색, bag을 커밋했을 때의 값이다. §1, §3, §6, §7, §8을 함께 쓰므로 §9 뒤에 둔다.

**1단계 — 그래프.** 3월 27일이 끝날 때 영어 절의 `git log --oneline --graph --decorate`는 그림과 같은 그래프를 출력한다. 맨 위 `ea13bc4 (HEAD -> main)`부터 `6321a22 (tag: study-v1)`, `2006419 (tag: pilot-v1)`, 병합 `882d5dd`와 그 오른쪽 가지의 `f41f0b6 (impedance-b)`, `757338e`를 지나 맨 아래 `c13c298`까지다.

커밋은 열다섯 개다(`git rev-list --count HEAD`가 15를 출력한다). 부모 링크를 세면 첫 커밋은 없고, 병합은 둘, 나머지 열셋은 하나씩이므로 $0+2+13\times1=15$개이고, 그것이 그림의 선 열다섯 개다. HEAD에서 첫째 부모만 따라가면 main 자신의 줄기, 커밋 13개가 나오고, 나머지 2개는 impedance-b에서 만들었다. 히스토리 전체는 객체 61개 — 커밋 15, tree 26, blob 18, 태그 2 — 이고, 그것을 실제로 전송해야 했던 클론(`git clone --no-local --bare`)은 `git count-objects -vH`가 출력한 대로 10.15 KiB짜리 팩 하나에 담는다.

**2단계 — 고친 숫자 하나.** aebf24a에서 시행 A1이 8.1이 아니라 8.2 N으로 입력되었다고 하자. §1의 규칙에 따라 예비 실험 파일의 blob이 바뀐다 — aebf24a에서는 열 줄짜리 파일 29805b11…이, 2006419부터는 스무 줄짜리 파일이 바뀌어 그 id가 3a8cd750…에서 764faff5…가 된다(둘 다 §1의 블록이 출력한다). 그러면 `trials/` tree가, 그러면 루트 tree가, 그러면 aebf24a의 id가 바뀐다. aebf24a를 조상으로 가진 모든 커밋은 직접이든 부모를 거쳐서든 그것을 가리키므로 그 id도 바뀐다. 882d5dd, 2006419, a0cd3a3, dda4b0f, 041fe2f, 6321a22, b659311, 3568180, ea13bc4다. 15개 가운데 1 + 9 = 10개다. 나머지 다섯 — c13c298, 16fc8ef, 2452d15, 757338e, f41f0b6 — 은 히스토리에 aebf24a가 없으므로 id를 유지한다. 두 태그는 더는 main 위에 없는 커밋을 가리키게 된다. 표의 도장이 증거인 이유가 이것이다. 누군가 히스토리 안에서 조용히 예비 실험 파일을 고쳤다면, 도장 `pilot-v1-0-g2006419`는 새 히스토리에 더는 없는 커밋을 가리킨다.

**3단계 — 어느 커밋이 어느 표를 냈나.** 같은 스크립트가 표 셋을 출력했다.

| 도장 | 커밋 | A: 횟수, 성공, 평균, 표준편차 | B | 판정 |
|---|---|---|---|---|
| `pilot-v1-0-g2006419` | 2006419 | 10, 6/10, 10.66 N, 2.414 N | 10, 9/10, 7.50 N, 1.356 N | 예비 실험 표 |
| `study-v1-1-gb659311` | b659311 | 9, 5/9, 10.94 N, 2.377 N | 그대로 | 틀림: dda4b0f의 파서가 시행 A1을 떨어뜨린다 |
| `study-v1-3-gea13bc4` | ea13bc4 | 10, 6/10, 10.66 N, 2.414 N | 그대로 | 되돌린 뒤 다시 옳음 |

도장의 수는 §7의 규칙 $n=|t..c|$를 따른다. b659311의 태그는 study-v1 = 6321a22이고, 그 너머에는 b659311만 있다. $n=1$. ea13bc4에는 셋 — b659311, 3568180, ea13bc4 — 이 있다. $n=3$. 틀린 줄은 손으로 확인할 수 있다. 헤더 다음 첫 줄을 떨어뜨리면 A1 = 8.1 N이 빠지므로, A의 힘의 합은 $106.6-8.1=98.5$ N이고 시행은 9회, 평균은 $98.5/9=10.944$ N이다. 8.1 N은 성공이었으므로 성공은 6에서 5로 준다. 남은 아홉의 표본 표준편차는 2.377 N이다. B의 첫 시행은 파일의 둘째 줄이 아니므로 B의 줄은 그대로다.

**4단계 — 탐색.** 첫 bad 커밋의 후보는 3568180에서는 닿고 pilot-v1에서는 닿지 않는 커밋이다. $N=|\text{pilot-v1..3568180}|=6$(a0cd3a3, dda4b0f, 041fe2f, 6321a22, b659311, 3568180). §8의 규칙으로 시험은 많아야 $s=\lceil\log_2 6\rceil=3$번이다. 실행에서는 시험 1, 041fe2f가 bad이므로 첫 bad 커밋은 041fe2f이거나 그보다 앞이다 — 후보 셋, {a0cd3a3, dda4b0f, 041fe2f}. 시험 2, dda4b0f가 bad — 둘 남음, {a0cd3a3, dda4b0f}. 시험 3, a0cd3a3이 good이므로 dda4b0f가 첫 bad 커밋이다. 시험마다 남은 것이 반으로 줄었다. $6\to3\to2\to1$.

**5단계 — bag의 무게.** 시행 bag 하나는 60 MiB(이 페이지의 교과용 숫자)이고, 예비 실험은 20개를 기록했으며 본 실험은 64개를 기록할 것이다. 영어 절의 Python 블록은 그것을 GitHub의 한계와 RS1의 히스토리 전체에 견주어 값을 매기고, 다른 $N$에 대한 탐색의 값도 매긴다. 출력은 이렇다. bag 하나는 62,914,560바이트 = 60.0 MiB = 팩으로 묶은 히스토리의 6,053배. 예비 실험 20개는 1,200 MiB, 1.17 GiB, 1.26 GB. 본 실험 64개는 3,840 MiB, 3.75 GiB, 4.03 GB. 모두 84개는 5,040 MiB, 4.92 GiB, 5.28 GB. 그리고 $N=6, 7, 57, 200, 1000$에 대해 시험은 3, 3, 6, 8, 10번이다.

§6에 대어 읽는다. bag 하나는 GitHub가 경고하는 크기의 $60/50=1.2$배이고, 막는 100 MiB 아래이므로 bag을 push할 때마다 경고와 함께 성공할 것이다. 예비 실험의 bag 20개만으로 1.26 GB여서, GitHub가 저장소 전체에 권하는 "이상적으로 1 GB 아래"를 넘는다. 본 실험의 64개까지 더하면 저장소는 5.28 GB(4.92 GiB), 그 다섯 배이고 GitHub가 그 아래로 두라고 강하게 권하는 5 GB에 걸린다. bag 하나는 RS1의 팩으로 묶은 히스토리 전체 6,053개와 무게가 같고, 나중에 지워도 계속 닿으며 모든 클론이 내려받는다. 같은 bag 84개를 텍스트 파일 속 체크섬으로 두면 한 줄씩이면 된다.

### 10. 이 페이지가 다루지 않는 것

일부러 히스토리를 다시 쓰는 일 — 대화형 rebase, `git filter-repo` — 은 §4의 규칙과 §6의 유출 절차를 넘어서는 다루지 않는다. Git LFS와 그 할당량, hook, 서명된 커밋과 태그, 이름 이상의 `git stash`와 `git worktree`, 큰 팀을 위한 브랜치 모델, 지속적 통합 — ROS 패키지라면 [[04-robotics/ros2/debugging-data-reproducibility|25.10 §12]] — 그리고 GitHub의 관리(조직, 권한, Actions)도 다루지 않는다. 셸 자체([[02-foundations/tools/linux-shell|12.1]]), Python 환경과 패키징([[02-foundations/tools/python-research-code|12.3]]), MCAP이나 CSV 같은 파일 형식([[02-foundations/tools/config-data-formats|12.4]])은 이 트랙에 각자의 페이지가 있고, C++은 [[04-robotics/ros2/cpp-for-robot-code|25.0 로봇 코드를 위한 C++]]이다.

### 읽고 나면

- [ ] blob, tree, commit, annotated tag가 무엇을 담는지 말하고, 바이트로부터 객체 id를 계산한다.
- [ ] 옛 커밋의 바이트 하나를 바꾸면 그 뒤 모든 커밋의 id가 바뀌는 이유를 설명하고, 어느 것인지 센다.
- [ ] `git add`, `git commit`, `git status`, `git diff`, `git diff --staged`가 작업 트리, 인덱스, `HEAD`에 대해 무엇을 하는지 말한다.
- [ ] 브랜치와 `HEAD`가 파일로서 무엇인지, 커밋할 때 무엇이 움직이는지 말한다.
- [ ] 병합 기준을 찾고, 병합이 어디서 충돌할지 예측하고, 충돌을 해결하고, 병합 커밋이 무엇을 기록하는지 말한다.
- [ ] fast-forward와 강제 갱신을 구별하고, 공개된 커밋을 rebase하거나 squash하는 것이 왜 동료를 해치는지 말한다.
- [ ] 로봇 저장소의 무시 목록을 쓰고, 지운 bag이나 키가 왜 여전히 모든 클론에 있는지 말한다.
- [ ] 실험에 태그를 붙이고, 결과 표에 커밋을 찍고, `-dirty`까지 포함해 describe 도장을 읽는다.
- [ ] `git bisect`로 $\lceil\log_2 N\rceil$번의 시험 안에 회귀를 찾고, 공유된 커밋을 `git reset`이 아니라 `git revert`로 되돌린다.
- [ ] 여러 저장소로 된 워크스페이스를 submodule이나 `.repos` 파일로, 커밋 id로 고정한다.

### 스스로 점검

1. 두 연구실 동료가 두 기계에서 각자 새 저장소에 바이트까지 똑같은 `trials/pilot.csv`를 커밋한다. blob의 id는 같은가? 커밋은?
2. 파일을 `git add`하고, 다시 고치고, 커밋한다. 커밋에는 어느 판이 들어가고, 그 뒤 `git status`는 무엇을 보이는가?
3. `.git/refs/heads/main`에는 무엇이 있고, main에서 커밋하면 그 안의 무엇이 바뀌는가? impedance-b에서 커밋하면?
4. 병합 882d5dd는 왜 `README.md`에서 멈추고 `controllers/impedance.py`나 `trials/pilot.csv`에서는 멈추지 않았는가?
5. 표에 `study-v1-3-gea13bc4-dirty`라고 적혀 있다. 각 부분은 무엇을 말하고, 그 표는 재현할 수 있는가?
6. 후보 커밋이 1,000개면 `git bisect`는 시험이 몇 번 필요하고, 그 답이 뜻을 가지려면 시험에 대해 무엇이 참이어야 하는가?
7. 한 커밋에서 토큰이 커밋되고 다음 커밋에서 지워졌으며, 둘 다 push되었다. 무엇을 먼저 하고, 왜 지운 것으로 없어지지 않았는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. blob은 같다. blob의 id는 바이트에만 의존하므로 둘 다 3a8cd750…이다. 커밋은 거의 확실히 다르다. 커밋의 바이트에는 작성자와 커미터의 이름, 이메일, 시각, 그리고 부모 줄이 들어가므로, 다른 사람이 다른 순간에 만들면 tree가 똑같아도 커밋은 다르다.
> 2. add한 판이다. `git add`가 그 바이트를 인덱스에 썼고, `git commit`은 인덱스를 기록한다. 그 뒤 `git status`는 그 파일을 "Changes not staged for commit"에 보인다. 작업 트리에 나중 편집이 아직 있기 때문이다.
> 3. 커밋 id 하나 — 16진수 마흔 자리와 줄바꿈, 41바이트 — 가 있다. main에서 커밋하면 새 커밋의 id가 그 파일에 쓰이고, 새 커밋은 옛 id를 부모로 갖는다. impedance-b에서 커밋하면 `HEAD`가 impedance-b를 가리키므로 `.git/refs/heads/impedance-b`가 바뀌고 main의 파일은 그대로다.
> 4. 병합 기준 2452d15와 비교하면 `controllers/impedance.py`는 impedance-b에서만, `trials/pilot.csv`는 main에서만 바뀌었으므로 각각 바꾼 쪽에서 가져왔다. `README.md`의 상태 줄은 양쪽에서 서로 다른 글로 바뀌었고, 삼방향 병합이 멈추는 경우는 그것뿐이다.
> 5. study-v1: 가장 가까운 annotated tag, 본 실험을 위해 고정한 코드. 3: 그 너머 커밋 셋. gea13bc4: 커밋 ea13bc4. -dirty: 표를 출력할 때 추적하는 파일이 ea13bc4와 달랐다. 그러므로 그 표는 어떤 커밋에도 없는 코드에서 나왔고, 변경을 커밋하고 표를 다시 출력하지 않는 한 누구도 — 내일의 자신도 — 그것을 checkout해 다시 돌릴 수 없다.
> 6. $2^{10}=1024\ge1000>2^9$이므로 $\lceil\log_2 1000\rceil=10$번이다. 시험은 주어진 커밋에 대해 결정적이어야 하고 — 들쭉날쭉하지 않아야 하고 — 성질은 범위 위에서 단조여야 한다. 한 번 bad면 뒤의 모든 커밋에서 bad다. 그리고 모든 커밋에 같은 시험이어야 하므로 저장소 밖에 둔다.
> 7. 토큰을 발급한 서비스에서 폐기하거나 교체한다. 그러면 모든 사본이 해가 없어진다. 지운 일은 그 파일이 없는 tree를 가진 커밋을 더했을 뿐이고, 앞의 커밋은 여전히 브랜치의 조상이므로 그 blob은 내 저장소에서도, 서버에서도, fetch한 모든 클론에서도 닿는다 — `git show <커밋>:<경로>`가 그것을 출력한다. 히스토리 재작성은 교체 뒤에 따로 내리는 결정이고, 그 뒤 모든 커밋의 id를 바꾸며 이미 있는 클론이나 fork에는 닿지 못한다.

### 과제 · Problem set

Tier B. 이 페이지, 선수 지식, RS1만 써서 손으로 푼다. 변형은 이렇다. B의 브랜치를 병합하지 않고 rebase한다, B의 커밋 하나를 다시 쓴다, 회귀가 더 많은 커밋 사이에 숨는다, 장치가 카메라를 하나 더 기록한다, 그리고 연구실 동료의 하루가 네 가지로 어긋난다.

1. **그리기.** impedance-b를 병합하지 않고 main 위로 rebase했다면 RS1의 히스토리가 어떻게 되었을지 그린다. 파일, 메시지, 날짜, 태그가 같고 버그와 되돌림도 같다. 커밋과 부모 링크, 어느 id가 남고 어느 것이 새것인지, pilot-v1, study-v1, main이 가리키는 곳, 탐색 당시의 bisect 범위와 $N$, 그리고 `HEAD`에서 `git describe --long`이 출력하는 것을 적는다. rebase가 최종 스냅샷에 무엇을 했는지 말한다.
2. **유도.** (a) 누군가 B의 브랜치의 첫 커밋 757338e를, 메시지에 빠진 단위를 넣으려고 다시 쓴다. 열다섯 id 가운데 몇 개가 바뀌고, 어느 것이 유지되며, 두 태그에는 무슨 일이 있어야 하는가? (b) 본 실험 뒤 그림 하나가 표와 맞지 않게 되었다. 마지막 good 커밋은 `HEAD`보다 57 커밋 뒤에 있다. 최악의 경우 `git bisect`는 시험이 몇 번 필요한가? 57개 가운데 두 개는 빌드할 수 없어 종료 코드 125로 건너뛴다. 그것은 무엇을 치르게 할 수 있는가? (c) 두 번째 카메라가 시행 bag을 120 MiB로 두 배 늘린다. bag을 GitHub에 push하면 무슨 일이 일어나고, bag 84개는 저장소를 MiB, GiB, GB로 얼마나 크게 만드는가? (d) study-v1 뒤 main이 커밋 5개를 받는 동안, study-v1에서 시작한 브랜치 fix-filter가 커밋 3개를 받는다. 그 브랜치를 병합 커밋으로 main에 병합한다. 병합 커밋에서 `git describe`의 $n$은 얼마이고, `git describe --first-parent`는 $n$으로 무엇을 출력하는가?
3. **해석.** 한 연구실 동료가 3월 30일을 연구실 서버의 자기 클론에서 보냈다. 영어 절에 두 화면이 있다. 하루가 끝날 때 동료의 터미널은 `git log --oneline --graph --decorate -6`(맨 위부터 328d473 "Remove the token from the upload script", 1866f39 "Add the upload script for the lab dashboard", 4257fa3 "Add the bag of trial B07 for figure 2", 41cea18 "Add the figure script and fix the trial parser", b659311, study-v1의 6321a22), `analysis/summarize.py`가 수정되었고 `results/`가 추적되지 않았다는 `git status`, 도장 `study-v1-5-g328d473-dirty` 아래 A 7/10, B 10/10을 담은 `results/table_12N.txt`, 그리고 4257fa3이 `trials/B07.mcap`을 `Bin 0 -> 62914560 bytes`로 더했다는 `git show --stat`을 보인다. 이튿날 아침 학생의 터미널은 `+ ea13bc4...328d473 main -> origin/main (forced update)`라는 `git fetch`와, "diverged … 2 and 4"라는 `git status`를 보인다. (두 화면 모두 RS1 저장소를 복제한 임시 저장소에서, 보이는 그 상태로 실행한 명령의 실제 출력이다. 연구실 서버는 force push가 다시 쓰는 방식 그대로 다시 쓰였고, 토큰은 누가 봐도 자리표시자다.) (a) 두 화면이 보이는 문제를 모두, 그것을 보여 주는 줄과 함께 대고, 연구에 무슨 값을 치르게 하는지 말한다. (b) 문제마다 지금의 수리와, 그것을 막았을 습관을 말한다. (c) 학생이 "동료의 작업을 받으려고" `git pull --no-rebase`를 실행하려 한다. 그 뒤 히스토리는 어떻게 보이고, 대신 무엇을 해야 하는가?

> [!note]- 그리는 법 · How to draw it
> - **최신이 위, 커밋마다 한 줄**, `git log --graph`가 출력하는 대로. 그래야 그림을 터미널과 한 줄씩 대조할 수 있다.
> - **선은 커밋을 그 아래의 부모와 잇는다.** 병합 커밋에서는 선이 둘 내려가고, 보통 커밋은 하나, 첫 커밋은 없다. rebase한 히스토리에는 병합이 없으므로 둘째 선이 어디에도 없다.
> - **모든 커밋에 16진수를 최소 일곱 자리 적고**, 어느 id가 새것인지 표시한다. 커밋은 히스토리 전체가 그대로일 때에만 id를 유지한다. 아래 어디서든 조상 하나가 바뀌면 새 id를 받는다.
> - **브랜치와 태그는 커밋 옆의 꼬리표다.** 커밋의 줄이 아니다. `main`, `HEAD`, `impedance-b`, `pilot-v1`, `study-v1`을 각각 커밋 하나를 가리키는 상자로 그린다.
> - **bisect 범위는 커밋들 위의 괄호다.** good 커밋 다음부터 bad 커밋까지 포함하고, 옆에 $N$과 $\lceil\log_2 N\rceil$을 적는다.
> - **HEAD에 describe 도장을 적고**, 태그 위에서 `HEAD`가 닿는 커밋을 세어 그 $n$을 확인한다.
> - **스냅샷에 일어난 일을 말한다.** 커밋이 아니라 최종 tree의 id를 원래 것과 비교한다.

> [!tip]- 정답 · Solutions
> 1. 병합 없이 한 줄로 선 커밋 열네 개다. c13c298, 16fc8ef, 2452d15, aebf24a는 히스토리가 바뀌지 않았으므로 id를 유지한다. B의 두 커밋은 aebf24a 위에 다시 쌓여 새 id를 받는다 — 757338e는 83db14a, f41f0b6은 04bbc92 — 부모가 2452d15에서 aebf24a로 바뀌었기 때문이다. rebase는 조율 커밋에서 한 번, 병합이 멈췄던 바로 그 `README.md` 상태 줄에서 멈춘다. 그 뒤의 모든 커밋도 부모 사슬이 바뀌었으므로 바뀐다. 2006419 → 0d96d14(pilot-v1), a0cd3a3 → 302b9af, dda4b0f → 9b68b59, 041fe2f → fab61c5, 6321a22 → 2b60c62(study-v1), b659311 → 3a1ccef, 3568180 → 6a2bd00, ea13bc4 → 1ad0242(main, HEAD). 882d5dd에 해당하는 것은 없다. rebase 뒤의 `git merge impedance-b`는 `Fast-forward`를 출력한다. 되돌리기 전의 bisect 범위는 여전히 커밋 여섯 개, 302b9af부터 6a2bd00까지이므로 시험 세 번이고, HEAD에서 `git describe --long`은 `study-v1-3-g1ad0242`를 출력한다. 스냅샷은 바뀌지 않았다. 최종 tree는 e3238a51…, 예비 실험의 것은 4710a335…, study-v1의 것은 bcefb113…로 병합한 히스토리와 같다. (이 id들은 원래 날짜로, rebase한 커밋의 커미터 날짜는 3월 9일 10:00으로 두고 임시 클론에서 변형을 다시 만들어 얻었다.)
> 2. (a) 757338e와 그것을 히스토리에 가진 모든 커밋 — f41f0b6, 882d5dd, 2006419, a0cd3a3, dda4b0f, 041fe2f, 6321a22, b659311, 3568180, ea13bc4 — 15개 가운데 11개가 바뀐다. c13c298, 16fc8ef, 2452d15, aebf24a는 유지된다. 두 태그는 여전히 옛 2006419와 6321a22를 가리키는데, 그것들은 더는 main 위에 없다. 태그는 이미 공개되었으므로 옮기지 않고 새 이름 pilot-v1.1과 study-v1.1로 대신하며, 옛 id로 도장을 찍은 모든 표는 새 히스토리에 없는 커밋을 가리킨다. (b) $2^5=32<57\le64=2^6$이므로 시험은 $\lceil\log_2 57\rceil=6$번이다. 건너뛴 커밋은 시험을 더 들게 하고, 건너뛴 커밋이 첫 bad 커밋 바로 옆에 있으면 bisect는 그 가운데 어느 것인지 가리지 못하고 후보들을 보고한다(git-bisect 문서). (c) 120 MiB는 GitHub가 파일을 막는 100 MiB보다 크므로, bag을 담은 push는 모두 곧바로 거부된다. bag 84개는 $84\times120=10{,}080$ MiB $=9.84$ GiB $=10.57$ GB로, 하나라도 push하기 전에 이미 GitHub가 강하게 권하는 5 GB의 두 배다. (d) $n=|\text{study-v1..merge}|$는 병합 커밋에서는 닿고 study-v1에서는 닿지 않는 모든 커밋을 센다. main의 5개, fix-filter의 3개, 병합 커밋 자신으로 $n=9$다. `--first-parent`면 걸음은 main의 줄기 — 커밋 5개와 병합 커밋 — 만 따라가 $n=6$을 출력한다. 두 수 모두 정확히 이 모양으로 만든 RS1의 임시 클론에서 확인했다. `study-v1-9-g…`와 `study-v1-6-g…`다.
> 3. (a) 문제는 넷이다. *커밋하지 않은 코드로 만든 표:* `modified: analysis/summarize.py`와 도장 `study-v1-5-g328d473-dirty`. 파일의 한계가 12 N이어서 A는 7/10, B는 10/10을 보인다. [[06-research-practice/research-questions-claims|1. 연구 질문과 주장]]이 묻는 12 N 변형으로, 정당한 질문이다 — 그러나 그것을 출력한 코드는 어떤 커밋에도 없고, `results/`도 추적되지 않으므로 누구도 재현하거나 리뷰할 수 없다. *공유 히스토리 위의 force push:* 학생 쪽의 `+ ea13bc4...328d473 … (forced update)`와 "diverged … 2 and 4". 동료는 3568180과 ea13bc4를 새 커밋 하나, 41cea18로 squash하고 서버의 main을 강제로 그리로 옮겼다. 스냅샷은 살아남았다 — 41cea18의 tree는 ea13bc4와 같은 e3238a51…이다 — 그러나 히스토리는 아니다. dda4b0f의 되돌림은 더는 되돌림으로 기록되어 있지 않고, 그 커밋은 이제 동료의 이름을 달고 있으며, 학생이 `study-v1-3-gea13bc4`로 도장을 찍은 모든 표는 서버에 더는 없는 커밋을 가리킨다. *커밋된 bag:* 4257fa3이 `trials/B07.mcap`을 더한다. `Bin 0 -> 62914560 bytes` — 60 MiB로, 팩으로 묶은 RS1의 히스토리 전체 10.15 KiB와 견준다. 이 bag은 `.gitignore`의 `*.mcap` 규칙에 맞으므로 `git add -f`로 밀어 넣은 것이다. 60 MiB면 GitHub의 50 MiB 경고를 넘고, 이제 fetch한 모든 클론, 학생의 클론에까지 들어 있다. *히스토리 속 토큰:* 1866f39가 업로드 스크립트를 더했고 328d473이 "토큰을 지웠지만", 1866f39는 여전히 main에서 닿으므로 `git show 1866f39:analysis/upload.py`는 그 뒤 main을 fetch한 모든 클론 — 학생의 것도 — 에서 토큰을 출력한다. `git log -S`는 두 커밋을 다 찾는다. (b) *표:* 12 N 변경을 자기 브랜치에, 그렇다고 말하는 메시지와 함께 커밋하고 다시 돌리면 도장이 깨끗해진다. 습관은 표를 만들기 전에 `git status --porcelain`이 아무것도 출력하지 않는 것이다. *force push:* 멈추고, 무엇이 main인지 모두 함께 정한다. 학생에게는 ea13bc4가, 동료에게는 41cea18이 있고 둘은 같은 tree를 가지므로 어느 쪽이든 잃는 작업은 없다. 그다음 서버에서 main을 보호해 force push가 거부되게 하고, 변경은 pull request로 리뷰한다. 습관은 남이 fetch한 커밋은 절대 다시 쓰지 않는 것이다(§4). *bag:* bag은 체크섬을 저장소에 두고 데이터 서버에 있어야 한다. 히스토리에서 없애는 것은 4257fa3, 1866f39, 328d473을 바꾸는 재작성이고, 모두의 동의가 필요하며, 이미 가진 클론에는 닿지 못한다 — 그러니 신중하게 정하고, bag을 `add -f`하지 않는다. *토큰:* 먼저 대시보드에서 토큰을 폐기하거나 교체한다. 그다음 bag처럼 재작성 여부를 정한다. 토큰은 328d473이 이제 하듯 환경 변수에 두고, push protection을 켠다. (c) ea13bc4와 328d473의 병합이다. 학생의 3568180과 ea13bc4가 같은 변경을 담은 41cea18 곁으로 돌아오고, 다음 push는 동료가 지운 바로 그 커밋들을 다시 공개한다 — Pro Git §3.6이 말하는 중복 히스토리다. 대신 먼저 이야기하고, 히스토리 하나를 고르고, 그다음 main을 `origin/main`으로 reset하거나(ea13bc4의 tree가 41cea18과 같고 학생 클론에만 있는 다른 것이 없으므로 여기서는 안전하다) `--force-with-lease`로 옛 커밋을 서버에 되돌려 놓는다. 그 뒤 표는 모두가 가진 커밋에서 다시 출력한다.

### 출처

- Chacon, S. & Straub, B. *Pro Git*, 2판 ([git-scm.com/book](https://git-scm.com/book/en/v2)) — §2.6 태그, §3.1 브랜치, §3.2 병합, §3.5 원격 브랜치, §3.6 rebase와 그 규칙, §7.7 세 트리, §7.11 submodule, §10.2 Git 객체.
- Git 참조 매뉴얼 ([git-scm.com/docs](https://git-scm.com/docs)), 2.52–2.55판 — git-init과 BreakingChanges(SHA-256, Git 3.0), git-describe, git-bisect(종료 코드), git-revert, git-reset, git-push(push 규칙), git-pull, git-log, git-diff, gitignore, git-gc(닿을 수 있음, reflog 만료), git-reflog, git-tag(태그 다시 달기), git-switch, git-submodule, gitdiffcore(`-S`).
- GitHub Docs ([docs.github.com](https://docs.github.com/en)) — "About large files on GitHub"(50 MiB, 100 MiB, 1 GB, 5 GB), "Removing sensitive data from a repository", "About push protection", "About pull requests", "About pull request reviews", "About protected branches".
- vcstool ([github.com/dirk-thomas/vcstool](https://github.com/dirk-thomas/vcstool)) — `.repos` 형식, `vcs export --exact`, 이미 있는 디렉터리에 대한 `vcs import`(`import_.py`, `clients/git.py`). vcs2l ([github.com/ros-infrastructure/vcs2l](https://github.com/ros-infrastructure/vcs2l)) — 그 fork이자 그대로 갈아 끼우는 대체품.
- GitHub의 ROS 2, jazzy — [Ubuntu-Development-Setup.rst](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Alternatives/Ubuntu-Development-Setup.rst)(`ros2.repos`의 `vcs import --input`)와 [ros2.repos](https://github.com/ros2/ros2/blob/jazzy/ros2.repos)(버전으로 적힌 브랜치 이름).
- man7.org의 GNU `sed(1)`과 macOS의 BSD `sed(1)` — §7이 피해 가는 `-i`의 두 철자.
