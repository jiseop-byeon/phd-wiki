---
title: "Human-Robot Collaboration in Construction: Classification and Research Trends (Liang et al., 2021)"
authors: Ci-Jyun Liang, Xi Wang, Vineet R. Kamat, Carol C. Menassa
affiliation: University of Michigan
venue: Journal of Construction Engineering and Management, 147(10)
year: 2021
doi: https://doi.org/10.1061/%28ASCE%29CO.1943-7862.0002154
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Liang et al., JCEM 2021** — [DOI](https://doi.org/10.1061/%28ASCE%29CO.1943-7862.0002154) (paywalled, ASCE)

> [!note] Math on-ramp · 수학 준비물
> [[04-robotics/hri-safety|11. HRI & Safety §1–§2]] — a taxonomy paper is only useful if you can place papers into it, so read it holding the autonomy-spectrum and in/on/out-of-the-loop distinctions.
> [[04-robotics/hri-safety|11. HRI·안전 §1~§2]] — 분류 논문은 다른 논문을 그 안에 놓을 수 있어야 쓸모가 있으므로, 자율성 스펙트럼과 in/on/out-of-the-loop 구분을 손에 들고 읽어라.

## English

**One-line summary**: THE orientation taxonomy for construction HRC — a systematic review that classifies how humans and robots divide work in construction research and maps where the field's effort concentrates, widely cited as the field's shared vocabulary — indices disagree on how widely (Crossref 209, Semantic Scholar 145), so quote a count only with the index it came from.

**Lineage position**: the Kamat/Menassa (UMich) group writing the map of the territory their own lab then populates — read it as the entry gate to the [[05-construction-robotics/hrc-worker-centered|HRC and worker-centered stream]]. It pairs with [[01-canonical-papers/notes/8-construction/davila-delgado-2019|Davila Delgado 2019]] as the two orientation surveys: Davila Delgado answers *why adoption fails* (demand side), Liang answers *how the research space is organized* (supply side).

> [!tip] Key intuition · 핵심 직관
> For a review, the key is a comparison axis: who senses, decides, and executes in human–robot work. Grouping studies by work division exposes differences that a list of robot types would hide; a sparsely populated category is a reading lead, not proof of technical impossibility.

**Method** (literacy level): a review of construction automation and robotics articles published after 2000, found through Google Scholar and Scopus with the keywords "construction robotics", "construction automation" and "building robotics", then screened by hand. It sorts them into **five levels** by robot autonomy and the human effort left in sensing, planning and acting: Preprogramming, Adaptive Manipulation, Imitation Learning, Improvisatory Control and Full Autonomy. Of the 259 articles, 135 fall under Preprogramming, 72 Adaptive Manipulation, 3 Imitation Learning, 18 Improvisatory Control and 31 Full Autonomy (Table 2). No level is empty, but Imitation Learning is nearly so. The authors cite their own group's 2020 imitation-learning work as an example of it. Evidence: the corpus review itself and the citation record — for a survey, uptake as shared vocabulary *is* the evidence. Do not quote a bare number: Crossref and Semantic Scholar returned 209 and 145 on the same day.

**Limitations**: a 2021 snapshot — pre-foundation-model, so language-conditioned and learned generalist robots barely register; classification is by published research, not by deployed practice, so the map can overweight what academics find publishable; taxonomy boundaries will strain as learning-based systems blur the operated/collaborative/autonomous lines. No testbed or site result of its own — it is a survey, and should be judged as one.

> [!question] Reading the claim · 핵심 주장 읽는 법
> The taxonomy organizes published research on human–robot work division. It does not measure deployment prevalence or prove the best allocation of authority. Check corpus boundaries and date before interpreting an empty category as an open technical problem.

## 한국어

**한 줄 요약**: 건설 HRC의 방향 잡기용 분류 체계, 그 자체 — 건설 연구에서 인간과 로봇이 일을 어떻게 나누는지를 분류하고 분야의 연구가 어디에 몰리는지 지도로 그린 체계적 리뷰로, 널리 인용되며 분야의 공용 어휘가 되었다 — 다만 색인마다 수치가 달라(Crossref 209, Semantic Scholar 145) 인용 횟수는 출처 색인과 함께만 적어야 한다.

**계보에서의 위치**: Kamat/Menassa(미시간) 그룹이 자기 연구실이 채워 갈 영토의 지도를 직접 그린 것 — [[05-construction-robotics/hrc-worker-centered|HRC·작업자 중심 스트림]]의 입구로 읽어야 한다. [[01-canonical-papers/notes/8-construction/davila-delgado-2019|Davila Delgado 2019]]와 함께 두 편의 방향 잡기 서베이를 이룬다: Davila Delgado는 *왜 도입이 실패하는가*(수요 측)에 답하고, Liang은 *연구 공간이 어떻게 조직되는가*(공급 측)에 답한다.

> [!tip] 핵심 직관 · Key intuition
> 리뷰의 핵심은 인간–로봇 작업에서 누가 감지·결정·실행하는가라는 비교축이다. 분업으로 연구를 묶으면 로봇 종류 목록이 숨기는 차이가 드러난다. 연구가 적은 분류는 읽을 단서이지 기술적 불가능성의 증거는 아니다.

**방법** (리터러시 수준): 2000년 이후 출판된 건설 자동화·로봇 논문을 Google Scholar와 Scopus에서 "construction robotics", "construction automation", "building robotics"라는 키워드로 모은 뒤 손으로 걸러낸 리뷰다. 로봇의 자율성과 감지·계획·실행에 사람에게 남는 노력에 따라 **다섯 수준**으로 분류한다: Preprogramming, Adaptive Manipulation, Imitation Learning, Improvisatory Control, Full Autonomy. 259편 가운데 Preprogramming이 135편, Adaptive Manipulation 72편, Imitation Learning 3편, Improvisatory Control 18편, Full Autonomy 31편이다(표 2). 빈 수준은 없지만 Imitation Learning은 거의 비어 있다. 저자들은 그 예로 자기 그룹의 2020년 모방학습 연구를 든다. 증거: 코퍼스 리뷰 자체와 인용 기록 — 서베이에서는 공용 어휘로의 채택이 곧 증거다. 맨숫자로 인용하지 마라. 같은 날 Crossref는 209, Semantic Scholar는 145를 돌려주었다.

**한계**: 2021년의 스냅숏 — 파운데이션 모델 이전이라 언어 조건화·학습된 범용 로봇은 거의 등장하지 않는다; 분류는 배치된 실무가 아니라 출판된 연구 기준이라, 지도가 학계가 출판하기 좋은 것에 과중될 수 있다; 학습 기반 시스템이 조작/협업/자율의 경계를 흐리면 분류 경계가 압박받을 것이다. 자체 테스트베드·현장 결과는 없다 — 서베이이고, 서베이로 평가해야 한다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 분류는 인간–로봇 분업의 발표 연구를 정리한다. 배포 보급률을 측정하거나 최적 권한 배분을 증명하지 않는다. 빈 분류를 미해결 기술 문제로 읽기 전에 자료 범위와 시점을 확인한다.

### 연결

- 스트림: [[05-construction-robotics/hrc-worker-centered|6. HRC·작업자 중심 스트림]]의 입구
- 짝: [[01-canonical-papers/notes/8-construction/davila-delgado-2019|Davila Delgado 2019]] (수요 측 서베이) · [[05-construction-robotics/lineage|건설로봇 계보]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading (○)

- [ ] State this survey's organizing principle: classification by the form of human–robot work division · 인간-로봇 작업 분담 형태에 따른 분류라는 이 서베이의 조직 원리를 말할 수 있다
- [ ] Explain the division of labor between Davila Delgado (demand side) and Liang (supply side) as a pair of orienting surveys · Davila Delgado(수요 측)와 Liang(공급 측)의 분업, 즉 방향을 잡아 주는 두 서베이가 짝을 이루는 방식을 설명할 수 있다
- [ ] Point out the pressure that the 2021 snapshot's blind spots (foundation models, learned general-purpose robots) place on the taxonomy · 2021년 스냅숏의 공백(파운데이션 모델, 학습된 범용 로봇)이 분류 체계에 줄 압박을 지적할 수 있다
