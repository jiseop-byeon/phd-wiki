---
title: 8. Research Radar
tags: [research, trends, dashboard]
---

The Research Radar is a decision-support layer for the point **after foundational
literacy and before choosing a research problem**. It separates established volume from
momentum and small-but-rising signals, then exposes the evidence behind every label.

<iframe
  class="research-radar-frame"
  src="../static/research-radar/index.html"
  title="Interactive Research Radar"
  loading="eager"
></iframe>

## How to use it

1. Start broad with **Deep Learning** or **Physical AI** to see the field-level landscape.
2. Filter to Robot Learning, Computer Vision, or Construction Physical AI as the question
   becomes technical.
3. Use the quadrant for orientation, not as an automatic thesis selector.
4. Open the evidence panel: inspect five-year counts, venue breadth, aliases, and papers.
5. Study every adjacent topic to **Literacy**, daily-use methods to **Working**, and only
   the intended contribution area to **Mastery**.

> [!warning] Conservative by design
> The first release excludes arXiv and workshops. A topic can therefore appear later than
> it does on social media. That lag is intentional: this page tracks published research,
> not attention.

## 한국어

Research Radar는 **기초 문해력을 얻은 뒤, 연구 문제를 고르기 전**에 쓰는 의사결정 층이다.
현재 논문량과 상승 속도, 작지만 떠오르는 신호를 분리하고 모든 판정의 근거를 공개한다.

1. Deep Learning 또는 Physical AI에서 전체 지형을 본다.
2. 질문이 구체화되면 Robot Learning·Computer Vision·Construction Physical AI로 좁힌다.
3. 사분면은 방향을 잡는 도구이지 논문 주제를 자동으로 정하는 순위가 아니다.
4. 근거 패널에서 5년 논문 수, venue 확산, 동의어와 대표 논문을 확인한다.
5. 인접 분야는 Literacy, 매일 쓰는 방법은 Working, 기여 영역만 Mastery까지 공부한다.

> [!warning] 의도적으로 보수적
> 초기판은 arXiv와 워크숍을 제외한다. 소셜미디어보다 신호가 늦게 보일 수 있지만, 이는 관심이
> 아니라 출판된 연구를 추적하기 위한 의도적인 지연이다.

## Methodology

- Data compiler: `scripts/compile_research_radar.py`
- Source cache builder: `scripts/build_research_radar.py`
- Output: versioned static JSON; no personal API credentials or user tracking
- Topic labels are multi-label and auditable; confidence is reduced for small samples
- Technical-debate labels will be published only after human review
