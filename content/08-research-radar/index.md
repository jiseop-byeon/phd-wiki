---
title: 8. Research Radar
tags: [research, trends, dashboard]
study-depth: Literacy
depth-goal: "Use the radar to locate momentum and volume; depth decisions belong to the study-depth guide."
mastery-when: "Not applicable — this is a decision-support dashboard, not study material."
---

## English

The Research Radar is a decision-support layer for the point **after foundational
literacy and before choosing a research problem**. It separates established volume from
momentum and small-but-rising signals, then exposes the evidence behind every label.

<iframe
  class="research-radar-frame"
  src="../static/research-radar/index.html"
  title="Interactive Research Radar"
  loading="eager"
></iframe>

### How to use it

1. Start broad with **Deep Learning** or **Physical AI** to see the field-level landscape.
2. Filter to Robot Learning, Computer Vision, or Construction Physical AI as the question
   becomes technical.
3. Use the quadrant for orientation, not as an automatic thesis selector.
4. Open the evidence panel: inspect five-year counts, venue breadth, aliases, and papers.

The scope controls are **overlapping research lenses**, not mutually exclusive folders.
A topic can appear under Deep Learning, Physical AI, and Robot Learning at the same time;
the visible topic count therefore need not shrink monotonically between scopes.

Research depth belongs to the pages themselves, not to this dashboard. Use the
[[00-study-depth-guide|Study Depth Guide]] after the Radar identifies a candidate area.

> [!warning] Known limitations (read before trusting a trend)
> - **Venue coverage**: IROS, RSS, RA-L, and T-RO — a large share of robotics output — are
>   now indexed as of the 2026-08-21 rebuild, which took robotics coverage from 7,846 to
>   23,604 papers (a factor of 3.0) and the whole corpus from 58,439 to 76,701. Robotics trends before that rebuild
>   undercounted the field badly, so do not compare a reading taken now against one taken
>   earlier. **CoRL 2025 and RSS 2025 are missing** from the current dataset (DBLP had not
>   indexed them at build time; see the audit panel).
> - **Single denominator**: shares normalize by each year's total across all indexed
>   venues, so changes in venue mix or indexing completeness can masquerade as topic
>   trends. Treat cross-year momentum as a lead to investigate, not a measurement.
> - **Ontology mixing**: in the current dataset the Transformer topic also matched
>   state-space/Mamba terms (separated in the taxonomy going forward), and broad topics
>   like Foundation Models absorb general LLM vocabulary — a "rise" can be a naming shift.
> - Use the Radar to *generate* questions and find representative papers — not as the
>   final basis for choosing a research topic.

> [!warning] Conservative by design
> The first release excludes arXiv and workshops. A topic can therefore appear later than
> it does on social media. That lag is intentional: this page tracks published research,
> not attention.

### Methodology

- Data compiler: `scripts/compile_research_radar.py`
- Source cache builder: `scripts/build_research_radar.py`
- Output: versioned static JSON; no personal API credentials or user tracking
- Topic ontology is multi-scope and auditable; confidence is reduced for small samples
- Construction signals use domain/task × robotics/AI intersections and two dedicated journals
- Technical-debate labels will be published only after human review

## 한국어

Research Radar는 **기초 문해력을 얻은 뒤, 연구 문제를 고르기 전**에 쓰는 의사결정 층이다.
현재 논문량과 상승 속도, 작지만 떠오르는 신호를 분리하고 모든 판정의 근거를 공개한다.

### 사용법

1. Deep Learning 또는 Physical AI에서 전체 지형을 본다.
2. 질문이 구체화되면 Robot Learning·Computer Vision·Construction Physical AI로 좁힌다.
3. 사분면은 방향을 잡는 도구이지 논문 주제를 자동으로 정하는 순위가 아니다.
4. 근거 패널에서 5년 논문 수, venue 확산, 동의어와 대표 논문을 확인한다.

범위 컨트롤은 서로 배타적인 폴더가 아니라 **겹치는 연구 관점**이다. 따라서 하나의 주제가
Deep Learning·Physical AI·Robot Learning에 동시에 나타날 수 있으며, 범위를 바꿀 때 보이는
주제 수가 반드시 단조롭게 줄어들지는 않는다.

학습 깊이는 이 대시보드가 아니라 각 학습 페이지에서 정한다. Radar로 후보 분야를 찾은
뒤 [[00-study-depth-guide|Study Depth Guide]]를 사용한다.

> [!warning] 알려진 한계 (추세를 믿기 전에 읽을 것)
> - **학회 커버리지**: IROS, RSS, RA-L, T-RO — 로보틱스 출판의 큰 몫 — 이
>   2026-08-21 재빌드에서 색인됐다. 로보틱스 커버리지가 7,846편에서 23,604편으로
>   (3.0배), 전체 코퍼스가 58,439편에서 76,701편으로 늘었다. 그 재빌드 이전의 로보틱스 추세는 분야를 크게
>   과소집계했으므로, 지금 읽은 값을 그 이전에 읽은 값과 비교하지 마라. **CoRL 2025와
>   RSS 2025는 현재 데이터셋에 없다** (빌드 시점에 DBLP 미색인; 감사 패널 참고).
> - **단일 분모**: 점유율이 그해 색인된 전체 학회 합계로 정규화되므로, 학회 구성이나 수집
>   완전성의 변화가 주제 추세처럼 보일 수 있다. 연도 간 momentum은 측정값이 아니라 조사할
>   단서로 취급하라.
> - **온톨로지 혼합**: 현 데이터셋에서 Transformer 토픽이 state-space/Mamba 용어와도
>   매칭됐고(향후 분리), Foundation Models 같은 넓은 토픽은 일반 LLM 어휘를 흡수한다 —
>   "상승"이 명명 변화일 수 있다.
> - Radar는 질문을 *생성*하고 대표 논문을 찾는 용도로 쓰라 — 연구 주제 선정의 최종 근거가
>   아니다.

> [!warning] 의도적으로 보수적
> 초기판은 arXiv와 워크숍을 제외한다. 소셜미디어보다 신호가 늦게 보일 수 있지만, 이는 관심이
> 아니라 출판된 연구를 추적하기 위한 의도적인 지연이다.

### 방법론

- 데이터 컴파일러: `scripts/compile_research_radar.py`
- 소스 캐시 빌더: `scripts/build_research_radar.py`
- 출력: 버전이 매겨진 정적 JSON; 개인 API 자격 증명이나 사용자 추적 없음
- 토픽 온톨로지는 다중 범위이며 감사 가능; 표본이 작으면 신뢰도를 낮춘다
- 건설 신호는 도메인/작업 × 로보틱스/AI 교차와 전용 저널 두 곳을 사용
- 기술적 논쟁 라벨은 사람의 검토를 거친 뒤에만 공개한다
