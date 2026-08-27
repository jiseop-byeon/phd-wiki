---
title: Home
---

## English

Welcome. This wiki is my long-term knowledge base for PhD research at the intersection of
**deep learning** and **construction robotics**.

**What this wiki is for**: research *literacy*, not uniform technical mastery — making the
vocabulary, equations, claims, and experimental language of physical-AI papers readable on
first contact. Derivations, implementation, and reproduction are pursued selectively, in
one's own research area.

### Start here — pick the path that matches you

1. **Choose the required depth first**: [[00-study-depth-guide|0. Study Depth Guide]] — Literacy for every adjacent field, Working for methods you use, Mastery only for the contribution area.
2. **Systematic self-study** (recommended): [[02-foundations/overview|Foundations 0. Overview]] → foundation pages 0.5–9 in order → the [[02-foundations/overview|gate check]] at the end of the Overview → then path 3. If you have engineering mathematics but no machine learning, [[02-foundations/neural-network-basics|0.7 What a Neural Network Is]] is the twenty minutes that makes the rest readable.
3. **Reading the papers**: [[01-canonical-papers/how-to-read|0. How to Read Papers]] first, then the [[01-canonical-papers/canonical-list|Canonical Paper List]] in order — ★ papers in full, ◐ note + skim, ○ note only — with the [[03-deep-learning/lineage|Paper Lineage]] open alongside.
4. **Quick overview only**: [[03-deep-learning/lineage|Paper Lineage]] + [[03-deep-learning/physical-ai-ecosystem|Physical AI Ecosystem]].
5. **Manipulation-first path** (specialization — take it *after* path 2, not instead of it): read [[07-research-program/index|7. Research Program]] for why this order exists, then kinematics ([[04-robotics/modern-robotics/index|MR ch.2–6]]) → dynamics and the task-space bridge ([[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]]) → planning ([[04-robotics/planning-decision-making|4. Planning & Decision-Making]]) → control ([[04-robotics/modern-robotics/ch11-robot-control|MR ch.11]], [[04-robotics/control-theory-ce397|5. Control Theory]]) → contact and compliance ([[04-robotics/contact-force-tactile|9. Contact, Force & Tactile]], [[04-robotics/force-compliance-control|13. Force & Compliance Control]]) → demonstration data ([[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection]]) → touch and grasp ([[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing]], [[04-robotics/grasping|15. Grasping]]) → policies ([[01-canonical-papers/notes/4-vla/act|ACT]] and [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — read [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] and [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]] from path 3 first, since each policy declares one of them as a prerequisite) → the construction assembly lineage ([[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]]) → the construction task layer ([[05-construction-robotics/construction-manipulation|Construction Manipulation]]).

### Maps of Content

- [[03-deep-learning/index|Deep Learning]] — foundations, computer vision, VLM, VLA, world models, diffusion
- [[04-robotics/index|Robotics & Physical Systems]] — geometry, estimation, planning, control, contact, embodiment, deployment, HRI and safety (sections A–G), then three optional specialization layers: manipulation, unstructured-environment navigation, and human perception (H–J)
- [[05-construction-robotics/index|Construction Robotics]] — construction & manufacturing robotics literature

### Reference

- [[02-foundations/index|Foundations]] — course-level math & systems basics, with priority map
- [[00-study-depth-guide|Study Depth Guide]] — topic-by-topic Literacy / Working / Mastery profile
- [[01-canonical-papers/how-to-read|How to Read Papers]] — paper vocabulary, equations, claims and evidence
- [[06-research-practice/index|Research Practice]] — questions, experiments, failure analysis, writing and peer review
- [[07-research-program/index|Research Program]] — the research identity, the three pillars, and the paper arc they become
- [[08-research-radar/index|Research Radar]] — published-venue trend map, for after foundational literacy
- [[glossary|Glossary]] — quick term lookup
- [[study-log|Study Log]] — what I read and when

## 한국어

박사 과정에서 공부하는 딥러닝과 건설로봇 지식을 정리해 두는 공간이다.

**이 위키의 목표**: 모든 분야의 균일한 기술적 숙달이 아니라 연구 *문해력* — physical AI
논문의 용어·수식·주장·실험 표현을 처음 보더라도 읽을 수 있게 만드는 것. 유도·구현·재현은
자신의 연구 분야를 중심으로 선택적으로 깊게 한다.

### 처음이라면 여기서부터 — 자신에게 맞는 경로 하나를 고르라

1. **먼저 필요한 깊이를 정한다**: [[00-study-depth-guide|0. Study Depth Guide]] — 모든 인접 분야는 Literacy, 직접 쓰는 방법은 Working, 기여 영역만 Mastery.
2. **체계적 독학** (권장): [[02-foundations/overview|기초 0. Overview]] → 기초 0.5~9를 순서대로 → Overview 끝의 [[02-foundations/overview|통과 점검]] → 그다음 3번 경로로. 공업수학은 했지만 기계학습이 처음이라면 [[02-foundations/neural-network-basics|0.7 신경망이란 무엇인가]]가 나머지를 읽히게 만드는 20분이다.
3. **논문 읽기**: [[01-canonical-papers/how-to-read|0. How to Read Papers]]를 먼저 읽고, [[01-canonical-papers/canonical-list|핵심 논문 리스트]]를 순서대로 — ★는 원문 정독, ◐는 노트 후 훑기, ○는 노트로 충분 — [[03-deep-learning/lineage|계보도]]를 옆에 열어두고.
4. **빠른 조감만**: [[03-deep-learning/lineage|논문 계보도]] + [[03-deep-learning/physical-ai-ecosystem|Physical AI Ecosystem]].
5. **매니퓰레이션 우선 경로** (전문화 — 2번을 *대신하는* 것이 아니라 2번 *다음에* 타는 경로): 왜 이 순서인지는 [[07-research-program/index|7. 연구 프로그램]]에서 읽고, 그다음 기구학([[04-robotics/modern-robotics/index|MR 2~6장]]) → 동역학과 작업 공간 다리([[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]]) → 계획([[04-robotics/planning-decision-making|4. 계획과 의사결정]]) → 제어([[04-robotics/modern-robotics/ch11-robot-control|MR 11장]], [[04-robotics/control-theory-ce397|5. 제어 이론]]) → 접촉과 컴플라이언스([[04-robotics/contact-force-tactile|9. 접촉·힘·촉각]], [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]) → 시연 데이터([[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]]) → 촉각과 파지([[04-robotics/tactile-visuotactile|14. 촉각·시각촉각 센싱]], [[04-robotics/grasping|15. 파지]]) → 정책([[01-canonical-papers/notes/4-vla/act|ACT]], [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — 각 정책이 선행으로 지목하는 [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]]와 [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]]을 경로 3에서 먼저 읽어라) → 건설 조립 계보([[05-construction-robotics/assembly-fabrication|조립과 제작]]) → 건설 작업 층([[05-construction-robotics/construction-manipulation|건설 매니퓰레이션]]).

### 콘텐츠 지도

- [[03-deep-learning/index|딥러닝]] — 기초 이론, 컴퓨터비전, VLM, VLA, 월드모델, 디퓨전
- [[04-robotics/index|로보틱스 & Physical Systems]] — 기하, 추정, 계획, 제어, 접촉, embodiment, 배포, HRI와 안전(A~G절), 그다음 선택 전문화 층 셋: 매니퓰레이션, 비정형 환경 내비게이션, 사람 인지(H~J절)
- [[05-construction-robotics/index|건설로봇]] — 건설·제조 분야 로봇 연구 논문 정리

### 참고 자료

- [[02-foundations/index|기초 과목]] — 수학·시스템 기초, 우선순위 지도 포함
- [[00-study-depth-guide|Study Depth Guide]] — 주제별 Literacy / Working / Mastery 기준
- [[01-canonical-papers/how-to-read|How to Read Papers]] — 논문의 용어·수식·주장·증거 읽기
- [[06-research-practice/index|Research Practice]] — 연구 질문, 실험, 실패 분석, 글쓰기와 peer review
- [[07-research-program/index|Research Program]] — 연구 정체성, 세 기둥, 그리고 그것이 되는 논문 arc
- [[glossary|용어집]] — 용어 빠르게 찾아보기
- [[08-research-radar/index|Research Radar]] — 문해력 이후 연구 주제 선택을 위한 규모·상승속도·근거 지도
- [[study-log|학습 일지]] — 언제 무엇을 읽었는지 기록

---

> [!info]- Sources · 이 위키가 참고한 출처들
> **Primary sources (1차 자료)** — 모든 논문 노트는 해당 논문의 arXiv/공식 PDF·프로젝트 페이지·공식 코드 저장소를 직접 참조하며, 각 노트 첫 줄에 링크되어 있다.
> - [DBLP Computer Science Bibliography](https://dblp.org/) — Research Radar의 venue별 출판 논문 메타데이터. arXiv·워크숍을 섞지 않고 연도별 논문량과 토픽 신호를 재현 가능하게 집계한다.
> - [Crossref](https://www.crossref.org/) — Automation in Construction·Construction Robotics의 출판 메타데이터와 DOI 근거 링크를 보완한다.
>
> **Curricula & study-note exemplars (커리큘럼·정리 방식 참고)**
> - [Stanford CS231n](https://cs231n.stanford.edu/schedule.html) — 딥러닝 파트의 흐름·정확성 교차 검증
> - [sudoremove](https://sudoremove.com/) — physical AI 최신 동향 큐레이션 벤치마크; 생태계 페이지의 착안점
> - [Lil'Log (Lilian Weng)](https://lilianweng.github.io/) — 주제 서베이형 글쓰기의 모범; RL 개관
> - [Sutton & Barto, *Reinforcement Learning: An Introduction*](http://incompleteideas.net/book/the-book.html) — RL 기초의 표준 교과서 (무료 공개)
> - [Holderrieth & Erives, *An Introduction to Flow Matching and Diffusion Models*](https://arxiv.org/abs/2506.02070) — 디퓨전/flow matching 수학의 참고 튜토리얼
> - [Modern Robotics (Lynch & Park)](http://modernrobotics.org) — 로보틱스 트랙의 교과서 (공식 무료 PDF)
> - [Matthew Bartos, *Control Theory for Smart Infrastructure* (UT Austin CE397)](https://future-water.org/teaching/) · [공개 course packet PDF](https://future-water-website.s3.amazonaws.com/docs/teaching/ce397/ce397_course_packet.pdf) — 상태공간·안정성·가제어성/가관측성과 피드백 제어 트랙의 주교재
> - [Underactuated Robotics (Tedrake)](https://underactuated.csail.mit.edu/) · [Stanford EE363](https://web.stanford.edu/class/ee363/) — 제어 학습 자료
>
> **Wiki structure (위키 구조 참고)**
> - [Quartz](https://quartz.jzhao.xyz/) — 이 사이트를 만드는 정적 사이트 생성기
> - [Maggie Appleton — digital gardeners](https://github.com/MaggieAppleton/digital-gardeners) · [Andy Matuschak — evergreen notes](https://notes.andymatuschak.org/) — digital garden/노트 설계 패턴
>
> **공식 발표 자료** — Google DeepMind·Meta AI·NVIDIA·OpenAI·Physical Intelligence의 공식 블로그와 기술 보고서 (해당 노트에 개별 링크). 입문 보조로는 [3Blue1Brown](https://www.3blue1brown.com/)과 Khan Academy를 권장한다.
