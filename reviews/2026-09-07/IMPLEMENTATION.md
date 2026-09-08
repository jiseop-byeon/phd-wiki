# 2026-09-07 전수 감사 후속 적용 기록

## 범위

`content/`의 공개 Markdown 210개를 전수 정독한 감사 결과를 기준으로 수정했다. 상세한
발견·근거·우선순위는 같은 폴더의 `FINAL-REVIEW.md`와 분야별 보고서에 보존한다. 이 문서는
무엇을 실제로 반영했고 무엇을 의도적으로 보류했는지를 기록한다.

## 반영한 핵심 수정

- Foundations: 선수지식 범위와 게이트 수를 실제 페이지에 맞추고, DDPM 조건부 분포,
  LM/최소제곱, deadly triad, PPO, convex MPC, 신호처리, SE(3), 동역학·컴플라이언스의
  강한 단정을 조건부 설명으로 교정했다.
- Deep learning papers: Adam의 두 번째 모멘트, BERT 생성 표현, Depth Anything의 상대/미터
  깊이, NeRF의 spectral bias, LoRA의 저랭크 매개변수화, ViT의 데이터 의존성, U-Net skip,
  scaling-law evidence, PPO/GAE, Faster R-CNN의 end-to-end 범위를 교정했다.
- VLA·world models·diffusion: ACT 실행 의미, CFG scale convention, Flow Matching의 경로와
  step 수, Dreamer RSSM, π0 claim, world-model/diffusion index의 길찾기를 보강했다.
- Robotics: 제어 안정성의 적용 조건, 파지 접촉 모델과 wrench normalization, extrinsic,
  환경 접촉, PFL 번역, disparity, AUC와 conformal coverage, LQR 가중치, 원격조작 지연,
  VLA–저수준 제어 인터페이스를 교정했다.
- Construction: AES 단위, sim-to-real의 오차 원인, 현장 사례 수, worker-centered 범위,
  디지털 트윈 단계, as-built 번역, labs/lineage의 최상급 표현을 정리했다. Han–Lee 용접
  논문은 기관 기록으로 DOI `10.1016/j.autcon.2024.105782`와 article number `105782`를
  확인해 원문 링크를 복구했다.
- Learning UX: canonical 체크박스는 노트 존재 표시임을 명시하고, ◐인데 전용 노트가 없는
  경우의 대체 읽기 절차, 읽기 깊이 정책 기준일, 영문 Paper Notes 안내, Study Log의 역사
  기록 경고를 추가했다. 논문·개념 템플릿에는 판본/검증일, I/O, 주장–근거, 한계와 퇴장
  기준을 넣었다.
- Research Radar: 그래프와 표시값의 단위를 topic–paper match share로 통일하고, 중복 매칭,
  근거량, 대표 논문의 선정 의미, 빈 필터 상태, 온톨로지 한계를 UI에 드러냈다.

## 의도적으로 자동 교정하지 않은 항목

다음은 문장만 고치면 오히려 가짜 확실성을 만들 수 있어 감사 보고서에 남겼다.

- “관련 연구가 없다/몇 편뿐이다” 같은 부재·희소성 주장은 검색식, 데이터베이스, 기간,
  포함·제외 기준을 함께 재실행한 뒤에만 갱신한다.
- JND와 일부 HRI/안전 수치는 과제·자극·표준 판본별 정의를 원 출처에서 다시 확인한 뒤
  변경한다.
- 최신 프리프린트의 세부 구현과 분야 전체의 수렴 방향은 출판판 또는 공식 구현이 없는
  한 관찰·가설로만 유지한다.

## 검증 결과

- `python3 scripts/verify_content.py`: **210 files, 0 problems**
- `python3 scripts/audit_parity.py`: **0 mismatched bilingual destinations**
- `npx tsc --noEmit`: 통과
- `node --check quartz/static/research-radar/radar.js`: 통과
- `git diff --check`: 통과
- 로컬 `npm run site`: 로컬 Node 26.5.0에서 V8 8 GB heap OOM. 저장소 지원 범위는
  Node `>=22 <25`이며 GitHub Pages workflow는 Node 24를 사용하므로, 배포 빌드 결과는
  GitHub Actions에서 최종 판정한다.

