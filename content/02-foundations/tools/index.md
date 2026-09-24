---
title: "12. Code, Tools & File Formats"
tags: [foundations, tools, moc]
cssclasses: [curated-folder-index]
study-depth: Working
wiki-support: Working
depth-goal: "Take each tool page when its first need arrives, so that no experiment's result is decided by a robot computer, a repository, a data file, a network link, a cluster job, a paper build or a printed fixture failing silently."
mastery-when: "Raise only when the software, rig or data pipeline itself is the contribution."
---

## English

The ROS 2 track builds a robot system, and the research runs experiments on it and writes them up. Both lean on tools this wiki used and did not teach: [[04-robotics/ros2/index|25. ROS 2]] assumes a Linux shell, Git, Python and C++, every Tier A lab assumes NumPy, the dissertation's policy trains on someone else's GPUs, and every trial stands on a bracket and a fixture. This track teaches them the way the rest of the wiki teaches physics. Each page takes an object the wiki already uses — the robot computer and logs of P6, the catalog's cart on a rail ([[02-foundations/lab-plants|0.6]]); the repository and paper of RS1, the research-practice track's frozen study ([[06-research-practice/index|Research Practice]]); the pin of S1, the construction track's facade-panel task ([[05-construction-robotics/site-engineering|2.5]]) — and prices each tool's classic failure on it in bytes, milliseconds or millimetres. It is a map of pages to take when their need arrives, not a course to finish first: each page says when that is, and none of the seven blocks of the dissertation path ([[07-research-program/index|7. Research Program §8]]) waits for all nine. Every page's First-pass callout is two sessions; the pacing table of [[02-foundations/overview|0. Overview]] sizes the whole track.

### The pages, and when to take each

- [[02-foundations/tools/linux-shell|12.1 Linux and the Shell]] — paths, what the shell does to a line, processes and signals, permissions, the environment, scripts, ssh, rsync and tmux, stable device names, systemd, and time on the robot computer. *Take it* before the first robot or cluster work: before you first log in to a robot computer.
- [[02-foundations/tools/git-research-code|12.2 Git for Research Code]] — what a commit stores, the index, branches and merges, remotes, what must not be committed, a tag per experiment, bisection to the commit that broke a number, and workspaces of several repositories. *Take it* with 12.1, before the first robot or cluster work, and with the first code whose results you will keep.
- [[02-foundations/tools/python-research-code|12.3 Python for Research Code]] — interpreters and environments, names and mutability, NumPy's dtypes, strides and views, vectorization, floating point and integer wraparound, seeded randomness, script structure and tests. *Take it* before the first Tier A lab if Python is new, and at the latest before the lab of [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]].
- [[02-foundations/tools/config-data-formats|12.4 Config and Data Formats]] — text against binary, numbers printed as text, JSON, YAML, XML and CSV, binary records and `.npy`, HDF5, Parquet and MCAP, and the Markdown this wiki is written in. *Take it* when the ROS 2 track first loads a parameter file or records a bag, or before the first dataset you keep.
- [[02-foundations/tools/computer-networks|12.5 Computer Networks]] — addresses and subnets, ports and sockets, NAT, TCP and UDP, application protocols, DDS and Zenoh, fieldbuses, clocks across machines, Wi-Fi and 5G, and measuring a link. *Take it* when the ROS 2 track first puts two machines on one network, or a policy first runs off the robot.
- [[02-foundations/tools/latex-figures-references|12.6 Writing Tools: LaTeX, Figures and References]] — a LaTeX build that settles, cross-references and floats, references built from DOIs, figures drawn at their printed size with error bars that say what they are, tables printed to the digits their uncertainty supports, and the paper kept in Git. *Take it* before writing the first paper, alongside [[06-research-practice/scientific-writing-peer-review|research practice 4]].
- [[02-foundations/tools/gpu-clusters|12.7 GPU Clusters and Remote Training]] — the scheduler, storage and containers, the batch script, chains of jobs, checkpoints and how often to save them, and staging data so the GPUs stay busy. *Take it* when a training run first leaves your own machine, and at the latest in block 7.
- [[02-foundations/tools/concurrency|12.8 Concurrency: Processes, Threads and Races]] — races and interleavings, locks and deadlock, bounded queues, Amdahl's law, Python's global interpreter lock, processes and asyncio. *Take it* before the ROS 2 track reaches [[04-robotics/ros2/executors-callbacks-time|25.5.1]] on the rig, or the first time you parallelize a Python job.
- [[02-foundations/tools/mechanical-design-fabrication|12.9 Mechanical Design and Fabrication for Experiments]] — parametric CAD and its file formats, fits and tolerances, 3D printing, fasteners, a camera bracket sized by its tilt and its ringing, and a fixture that puts a part back in the same place. *Take it* before building the first rig, and at the latest before the first mock-up trial.

### Two tool pages that live in other tracks

- [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]] heads the ROS 2 track because its object is P6's controller: values and lifetime, RAII and ownership, templates and interfaces, the build, and the rules of a real-time tick. Take it before the first C++ node of [[04-robotics/ros2/nodes-topics-messages|25.2]].
- [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing for Robot Learning]] sits in the deep-learning track: what a GPU does with a batch, and why one robot's forward pass is nearly all overhead. 12.7 gets a training run onto a cluster's GPUs; 1.4 says what those GPUs do with it.

## 한국어

ROS 2 트랙은 로봇 시스템을 만들고, 연구는 그 위에서 실험을 돌려 글로 쓴다. 둘 다 이 위키가 쓰기만 하고 가르치지는 않은 도구에 기댄다. [[04-robotics/ros2/index|25. ROS 2]]는 리눅스 셸, Git, Python, C++를 안다고 가정하고, Tier A 실습은 모두 NumPy를 가정하며, 학위논문의 정책은 남의 GPU에서 학습하고, 모든 시행은 브래킷과 고정구 위에 선다. 이 트랙은 그 도구들을 위키의 나머지가 물리를 가르치는 방식으로 가르친다. 페이지마다 위키가 이미 쓰는 대상 하나 — P6(레일 위 카트와 그 시계들, [[02-foundations/lab-plants|0.6]])의 로봇 컴퓨터와 그 로그, RS1(연구 실무 트랙의 고정 연구, [[06-research-practice/index|연구 실무]])의 저장소와 논문, S1(건설 트랙의 외장 패널 과제, [[05-construction-robotics/site-engineering|2.5]])의 핀 — 를 잡고, 도구마다 전형적인 실패를 그 위에서 바이트·밀리초·밀리미터로 값을 매긴다. 먼저 끝내야 하는 과목이 아니라, 필요가 생길 때 꺼내 드는 페이지들의 지도다. 페이지마다 그때가 언제인지 적혀 있고, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])의 일곱 블록 가운데 아홉 페이지를 모두 기다리는 블록은 없다. 페이지마다 처음이라면 콜아웃은 2회이고, 트랙 전체의 분량은 [[02-foundations/overview|0. Overview]]의 페이스 표가 정한다.

### 페이지와, 각각을 할 때

- [[02-foundations/tools/linux-shell|12.1 리눅스와 셸]] — 경로, 셸이 한 줄에 하는 일, 프로세스와 시그널, 권한, 환경, 스크립트, ssh·rsync·tmux, 바뀌지 않는 장치 이름, systemd, 그리고 로봇 컴퓨터의 시간. *할 때:* 로봇이나 클러스터 작업을 처음 하기 전, 곧 로봇 컴퓨터에 처음 로그인하기 전.
- [[02-foundations/tools/git-research-code|12.2 연구 코드를 위한 Git]] — 커밋이 저장하는 것, 인덱스, 브랜치와 병합, 원격, 커밋하면 안 되는 것, 실험마다 태그, 숫자를 망가뜨린 커밋까지 가는 이분 탐색, 저장소 여럿으로 된 워크스페이스. *할 때:* 12.1과 함께, 로봇이나 클러스터 작업을 처음 하기 전, 그리고 결과를 남길 첫 코드와 함께.
- [[02-foundations/tools/python-research-code|12.3 연구 코드를 위한 Python]] — 인터프리터와 환경, 이름과 가변성, NumPy의 dtype·스트라이드·뷰, 벡터화, 부동소수점과 정수 되감김, 재현되는 난수, 스크립트 구조와 테스트. *할 때:* Python이 처음이면 첫 Tier A 실습 전에, 늦어도 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]]의 실습 전에.
- [[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식]] — 텍스트 대 바이너리, 텍스트로 찍은 숫자, JSON·YAML·XML·CSV, 바이너리 레코드와 `.npy`, HDF5·Parquet·MCAP, 그리고 이 위키를 쓰는 Markdown. *할 때:* ROS 2 트랙이 처음으로 파라미터 파일을 읽거나 bag을 기록할 때, 또는 남길 첫 데이터셋 전에.
- [[02-foundations/tools/computer-networks|12.5 컴퓨터 네트워크]] — 주소와 서브넷, 포트와 소켓, NAT, TCP와 UDP, 응용 프로토콜, DDS와 Zenoh, 필드버스, 기계 사이의 시계, Wi-Fi와 5G, 링크 측정. *할 때:* ROS 2 트랙이 처음으로 기계 두 대를 한 네트워크에 올릴 때, 또는 정책이 처음으로 로봇 밖에서 돌 때.
- [[02-foundations/tools/latex-figures-references|12.6 글쓰기 도구: LaTeX, 그림, 참고문헌]] — 수렴하는 LaTeX 빌드, 상호 참조와 플로트, DOI에서 만든 참고문헌, 인쇄 크기로 그리고 오차 막대가 무엇인지 말하는 그림, 불확실성이 받쳐 주는 자릿수로 찍은 표, 그리고 Git에 둔 논문. *할 때:* 첫 논문을 쓰기 전, [[06-research-practice/scientific-writing-peer-review|연구 실무 4]]와 함께.
- [[02-foundations/tools/gpu-clusters|12.7 GPU 클러스터와 원격 학습]] — 스케줄러, 저장소와 컨테이너, 배치 스크립트, 작업 사슬, 체크포인트와 그 저장 간격, 그리고 GPU가 놀지 않게 데이터를 옮겨 두는 법. *할 때:* 학습이 처음으로 자기 기계를 떠날 때, 늦어도 7 블록에서.
- [[02-foundations/tools/concurrency|12.8 동시성: 프로세스, 스레드, 경쟁]] — 경쟁과 인터리빙, 락과 교착, 유한 버퍼 큐, 암달의 법칙, Python의 전역 인터프리터 락, 프로세스와 asyncio. *할 때:* ROS 2 트랙이 리그에서 [[04-robotics/ros2/executors-callbacks-time|25.5.1]]에 닿기 전, 또는 Python 작업을 처음 병렬로 돌릴 때.
- [[02-foundations/tools/mechanical-design-fabrication|12.9 실험을 위한 기계 설계와 제작]] — 파라메트릭 CAD와 그 파일 형식, 끼워맞춤과 공차, 3D 프린팅, 체결구, 목표에서의 기울기와 떨림으로 크기를 정하는 카메라 브래킷, 부품을 매번 같은 자리에 돌려놓는 고정구. *할 때:* 첫 리그를 만들기 전, 늦어도 첫 목업 시행 전.

### 다른 트랙에 사는 도구 페이지 둘

- [[04-robotics/ros2/cpp-for-robot-code|25.0 로봇 코드를 위한 C++]]는 대상이 P6의 제어기이므로 ROS 2 트랙의 맨 앞에 있다. 값과 수명, RAII와 소유권, 템플릿과 인터페이스, 빌드, 그리고 실시간 틱의 규칙. [[04-robotics/ros2/nodes-topics-messages|25.2]]의 첫 C++ 노드 전에 한다.
- [[03-deep-learning/foundations/gpu-computing|1.4 로봇 학습을 위한 GPU 계산]]은 딥러닝 트랙에 있다. GPU가 배치로 무엇을 하는지, 로봇 한 대의 순전파가 왜 거의 전부 오버헤드인지. 12.7은 학습을 클러스터의 GPU에 올리고, 1.4는 그 GPU가 그것으로 무엇을 하는지 말한다.
