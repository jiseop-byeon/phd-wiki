---
title: "Navigating to Objects in the Real World"
authors: Theophile Gervet, Soumith Chintala, Dhruv Batra, Jitendra Malik, Devendra Singh Chaplot
affiliation: Carnegie Mellon University, Meta AI
venue: Science Robotics
year: 2023
journal-ref: "Science Robotics 8(79), eadf6991"
arxiv: https://arxiv.org/abs/2212.00922
tags: [paper, navigation, objectnav, sim-to-real, evaluation]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when the thesis makes a claim about what simulation evidence is worth."
---

**Gervet, Chintala, Batra, Malik & Chaplot, *Science Robotics* 8(79), eadf6991, 2023** — [arXiv:2212.00922](https://arxiv.org/abs/2212.00922)

> [!note] Math on-ramp · 수학 준비물
> Nothing new — this is an empirical study. What you need is the ObjectNav definition and its metrics ([[04-robotics/semantic-language-navigation|19. §1–§2]]) and the sim-to-real vocabulary of [[06-research-practice/simulators-benchmarks-datasets|7. §4]].
> 새로 필요한 것은 없다 — 경험적 연구다. ObjectNav의 정의와 지표([[04-robotics/semantic-language-navigation|19. §1~§2]]), 그리고 [[06-research-practice/simulators-benchmarks-datasets|7. §4]]의 sim-to-real 어휘면 된다.

## English

**One-line summary**: Take the leading classical, modular, and end-to-end navigation methods out of the simulator and into **six real homes with no prior maps** — modular learning holds at 90% success while end-to-end collapses from 77% in simulation to 23% in reality.

### Context

Learned visual navigation policies had been evaluated almost entirely in simulation. The literature had a ranking, and nobody had checked whether the ranking survived contact with a real house. This paper checks.

### Method

> [!tip] Key intuition · 핵심 직관
> The proposed explanation is that modular interfaces can isolate visual domain shift from geometric planning and control. Comparing representative systems in real homes probes that explanation, but a family-level performance gap does not uniquely identify every causal benefit of modularity.

A large-scale empirical study across **six homes with no prior experience, maps, or instrumentation**, comparing representative methods from three families:

| Family | What it is | Real-world result |
|---|---|---|
| Classical | geometric map, plan to point goals | the baseline the others must beat |
| Modular learning | classical pipeline + learned semantic sensing and exploration | **90% success** |
| End-to-end learning | one network, sensors to actions | **23% success** (77% in simulation) |

### Results

> [!important] The number to remember
> **End-to-end learning drops from 77% in simulation to 23% in the real world.** The paper attributes this to a large image domain gap between simulation and reality. Modular learning attains **90%**. The conclusion the authors draw is architectural: **modularity and abstraction in policy design enable sim-to-real transfer** — the module interfaces are where the domain gap gets absorbed.

The paper also names two issues that stop today's simulators from being reliable evaluation benchmarks: **(A) a large sim-to-real gap in images**, and **(B) a disconnect between simulation and real-world error modes.** (B) is the subtler and more damaging one: even if you accepted a performance drop, the *kinds* of failure differ, so simulation does not tell you what to fix.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> Six homes is a real-world study, and it is still six homes — a small sample chosen by the authors. The comparison is also between *representative* methods, not exhaustive ones, so it bounds a class rather than settling it. What makes the result durable is the size of the gap, not its precision: a 54-point collapse is not a sampling artefact.

### Limitations & critique

- **Homes, not sites.** Six houses share a great deal of structure. A construction site has none of it, and the gap could be larger or differently shaped.
- **A snapshot of methods.** The end-to-end family has kept moving; [[01-canonical-papers/notes/9-navigation/navid|NaVid]] and its successors make different sim-to-real claims and deserve to be tested the same way rather than assumed to inherit the verdict.
- **Modularity has a cost the study does not price.** Module interfaces are hand-designed commitments, and the paper measures what they buy without measuring what they foreclose.

### Impact & follow-ups

This is the paper to cite whenever a navigation result exists only in simulation, and it is one of the few places in the literature where a *negative* transfer result is reported at this scale and in this venue. Its architectural conclusion — modularity as a sim-to-real mechanism — is the reason [[04-robotics/semantic-language-navigation|19]] treats the modular pipeline as the default rather than the legacy option.

**For construction**: the argument generalises. Site simulation is worse than home simulation on both axes the paper names — the images are further from reality and the failure modes are less well modelled — so a policy validated only in a site simulator should be assumed to be in the 23% regime until shown otherwise.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation]] — the concept page
- [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] — the modular architecture that holds up here
- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — the wiki's inventory of what each simulator does and does not certify
- [[01-canonical-papers/notes/4-vla/pi0|π0]] — the same pattern in manipulation: an independent evaluation far below the headline

### After reading

- [ ] Quote the three numbers — 90, 77, 23 — and say which method each belongs to.
- [ ] State the two reasons the authors give for simulators being unreliable benchmarks, and say which is worse.
- [ ] Explain the mechanism they propose for why modularity transfers.
- [ ] Name what the study's sample size does and does not let you conclude.

## 한국어

**한 줄 요약**: 대표적인 고전·모듈형·end-to-end 내비게이션 방법을 시뮬레이터 밖 **사전 지도 없는 실제 주택 여섯 곳**으로 데려간다. 모듈형 학습은 90% 성공률을 지키고, end-to-end는 시뮬레이션 77%에서 현실 23%로 무너진다.

### 배경

학습 기반 시각 내비게이션 정책은 거의 전적으로 시뮬레이션에서만 평가되어 왔다. 문헌에는 순위가 있었고, 그 순위가 실제 집과의 접촉에서 살아남는지는 아무도 확인하지 않았다. 이 논문이 확인한다.

### 방법

> [!tip] 핵심 직관 · Key intuition
> 제안한 설명은 모듈 인터페이스가 시각 도메인 이동을 기하 계획·제어와 분리할 수 있다는 것이다. 실제 주택의 대표 시스템 비교가 이 설명을 살핀다. 계열별 성능 차이만으로 모듈성의 모든 인과적 이점을 유일하게 식별하지는 못한다.

**사전 경험도, 지도도, 계측 설비도 없는 주택 여섯 곳**에서의 대규모 경험 연구로, 세 계열의 대표 방법을 비교한다:

| 계열 | 무엇인가 | 실제 환경 결과 |
|---|---|---|
| 고전 | 기하 지도, 점 목표까지 계획 | 나머지가 넘어야 할 기준선 |
| 모듈형 학습 | 고전 파이프라인 + 학습된 의미 감지·탐색 | **성공률 90%** |
| end-to-end 학습 | 센서에서 행동까지 네트워크 하나 | **성공률 23%** (시뮬레이션에서는 77%) |

### 결과

> [!important] 기억할 숫자
> **end-to-end 학습이 시뮬레이션 77%에서 현실 23%로 떨어진다.** 논문은 이를 시뮬레이션과 현실 사이의 큰 이미지 도메인 격차로 돌린다. 모듈형 학습의 성공률은 **90%** 다. 저자들이 끌어내는 결론은 구조적이다: **정책 설계에서의 모듈성과 추상화가 sim-to-real 전이를 가능하게 한다** — 도메인 격차가 흡수되는 자리가 모듈 인터페이스다.

논문은 오늘날의 시뮬레이터가 신뢰할 만한 평가 벤치마크가 되지 못하는 두 가지 이유도 지목한다: **(A) 이미지에서의 큰 sim-to-real 격차**, 그리고 **(B) 시뮬레이션과 현실의 실패 양상 사이의 단절.** (B)가 더 미묘하고 더 해롭다: 성능 하락을 받아들인다 해도 실패의 *종류*가 다르므로, 시뮬레이션은 무엇을 고쳐야 하는지를 알려주지 못한다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 여섯 집은 실제 환경 연구이고, 그래도 여섯 집이다 — 저자가 고른 작은 표본이다. 비교 대상도 망라가 아니라 *대표* 방법들이므로, 한 계열을 한정할 뿐 결판내지는 않는다. 이 결과를 오래가게 만드는 것은 정밀도가 아니라 격차의 크기다: 54포인트의 붕괴는 표집의 우연이 아니다.

### 한계와 비판

- **현장이 아니라 주택이다.** 집 여섯 채는 구조를 아주 많이 공유한다. 건설 현장에는 그것이 없고, 격차는 더 크거나 다른 모양일 수 있다.
- **방법들의 스냅숏이다.** end-to-end 계열은 계속 움직였다. [[01-canonical-papers/notes/9-navigation/navid|NaVid]]와 그 후속들은 다른 sim-to-real 주장을 내놓고 있고, 이 판결을 물려받는다고 가정할 것이 아니라 같은 방식으로 시험받아야 한다.
- **모듈성에는 이 연구가 값을 매기지 않은 비용이 있다.** 모듈 인터페이스는 손으로 설계한 약속이고, 논문은 그것이 사주는 것을 측정하되 그것이 막아버리는 것은 측정하지 않는다.

### 영향과 후속 연구

내비게이션 결과가 시뮬레이션에만 존재할 때 인용할 논문이고, 이 규모와 이 게재지에서 *부정적* 전이 결과가 보고된 드문 사례다. 모듈성이 sim-to-real 기구라는 구조적 결론이, [[04-robotics/semantic-language-navigation|19]]가 모듈형 파이프라인을 유산이 아니라 기본값으로 다루는 이유다.

**건설의 경우**: 논증이 그대로 일반화된다. 현장 시뮬레이션은 논문이 지목한 두 축 모두에서 주택 시뮬레이션보다 나쁘다 — 이미지가 현실에서 더 멀고, 실패 양상이 더 부실하게 모형화된다. 그러니 현장 시뮬레이터에서만 검증된 정책은 반증되기 전까지 23% 영역에 있다고 가정해야 한다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] — 여기서 살아남는 모듈형 구조
- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — 각 시뮬레이터가 무엇을 보증하고 못 하는지에 대한 위키의 목록
- [[01-canonical-papers/notes/4-vla/pi0|π0]] — 매니퓰레이션에서의 같은 패턴: 헤드라인보다 한참 낮은 독립 평가

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 세 숫자 — 90, 77, 23 — 를 말하고 각각이 어느 방법의 것인지 댄다.
- [ ] 시뮬레이터가 신뢰할 수 없는 벤치마크인 두 이유를 말하고 어느 쪽이 더 나쁜지 말한다.
- [ ] 모듈성이 전이되는 이유로 저자들이 제시한 기구를 설명한다.
- [ ] 이 연구의 표본 크기가 무엇을 결론짓게 하고 무엇을 못 하게 하는지 댄다.
