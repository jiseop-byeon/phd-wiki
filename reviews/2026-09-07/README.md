# 위키 학습성 전수 감사

감사일: 2026-09-07  
기준 커밋: `1824821`에서 시작해 현재 트리에 후속 수정 적용

공업수학을 수강한 공대생이 Physical AI를 처음부터 독학할 때, 용어·수식·주장·실험을
정확히 읽고 필요한 분야를 Working/Mastery로 올릴 수 있는지를 점검했다.

## 검토 범위

- `content/`의 공개 Markdown **210개 전수 정독**
- Foundations, 논문 노트 115편, Deep Learning maps, Robotics, Construction,
  Research Practice/Program, Radar, Glossary, Study Log, 템플릿
- 형식 검사와 영·한 링크 대응 검사
- 분야별 내부 일관성과 교육 경로 검토

이는 원 논문 115편의 모든 수치와 최신 외부 사실을 다시 peer review한 감사는 아니다.
외부 원문 재검증이 필요한 항목은 별도로 표시했다.

## 문서 안내

- [FINAL-REVIEW.md](FINAL-REVIEW.md) — 전체 판정과 통합 우선순위
- [IMPLEMENTATION.md](IMPLEMENTATION.md) — 실제 반영 내용, 보류 이유, 검증 결과
- [foundations.md](foundations.md) — Foundations·Research Practice·Program
- [papers-dl.md](papers-dl.md) — DL·CV·VLM 논문
- [papers-policy.md](papers-policy.md) — VLA·world models·diffusion·navigation 논문
- [robotics.md](robotics.md) — Robotics와 Modern Robotics
- [construction.md](construction.md) — Construction Robotics
- [learning-path.md](learning-path.md) — 진입 경로·깊이·용어집·템플릿
- [radar-and-rendering.md](radar-and-rendering.md) — Research Radar와 렌더링
- [inventory.md](inventory.md) — 파일 인벤토리

## 현재 상태

감사와 후속 편집은 완료됐다. 내부 QA는 210개 문서에서 0건이며, 로컬 Node 26의 Quartz
전체 빌드는 지원 버전 밖 V8 heap OOM으로 실패했다. 저장소가 지원하는 Node 24를 사용하는
GitHub Pages workflow의 빌드·배포 결과를 최종 기준으로 삼는다.
