---
title: "Learning Robust Perceptive Locomotion for Quadrupedal Robots in the Wild"
authors: Takahiro Miki, Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, Marco Hutter
affiliation: ETH Zürich, KAIST, Intel Labs
venue: Science Robotics
year: 2022
journal-ref: "Science Robotics 7(62), eabk2822"
arxiv: https://arxiv.org/abs/2201.08117
tags: [paper, locomotion, legged, perception, sim-to-real]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if fusing unreliable exteroception with proprioception becomes part of the contribution."
---

**Miki, Lee, Hwangbo, Wellhausen, Koltun & Hutter, *Science Robotics* 7(62), eabk2822, 2022** — [arXiv:2201.08117](https://arxiv.org/abs/2201.08117)

> [!note] Math on-ramp · 수학 준비물
> The teacher–student setup of [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]], plus recurrent encoders and attention as a *gating* mechanism rather than a sequence model ([[04-robotics/legged-locomotion|18. §3]]).
> [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]의 teacher–student 구조, 그리고 시퀀스 모델이 아니라 *게이팅* 기구로서의 순환 인코더와 어텐션([[04-robotics/legged-locomotion|18. §3]]).

## English

**One-line summary**: Put exteroception back in, but never trust it — an attention-based recurrent encoder learns *when* the terrain map is believable and falls back on proprioception when it is not, giving a controller that is both fast and robust.

### Context

[[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] showed that a blind controller is extraordinarily robust, and paid for it in speed: the robot must physically feel out the terrain before adapting its gait. The abstract of this paper states the trade-off directly — perceiving terrain *before* contact is what allows gait planning ahead of time, which is where speed and energy efficiency come from.

The obstacle is that outdoor exteroception is not merely noisy, it is **systematically wrong**: snow, vegetation and water appear as obstacles the robot cannot step on, or are missing altogether because of high reflectance. On top of that, depth degrades under difficult lighting, dust, fog, reflective or transparent surfaces, and occlusion.

### Method

> [!tip] Key intuition
> Do not ask "what does the map say". Ask "**should I believe the map right now**". The encoder is trained end-to-end so that this judgement is learned rather than hand-tuned, which is precisely what a heuristic confidence threshold cannot do.

An **attention-based recurrent encoder** integrates proprioceptive and exteroceptive input, trained end-to-end, and learns to combine the modalities **without resorting to heuristics**. The recurrence carries the belief over time; the attention decides how much weight the exteroceptive channel gets.

### Results

The evidence is deployment breadth plus one memorable demonstration: testing across **a variety of challenging natural and urban environments over multiple seasons**, and completion of an **hour-long hike in the Alps in the time recommended for human hikers**.

> [!warning] Reading the claims · 주장 읽는 법
> The Alpine hike is a *time-budget* result, not a success rate: on the full 2.2 km route the controller took **78 minutes against a 76-minute** hiking-guide time — two minutes *over*, which the paper words as "virtually the same time". It was faster only on the summit leg: 31 min against the 35 min on the signage. That is a genuinely good metric — it is externally defined and not chosen by the authors — but it is a single route, and it is not a distribution over routes. As with [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]], **the abstract contains no success rates and no comparison numbers.**
> 알프스 등반은 성공률이 아니라 *시간 예산* 결과다: 2.2 km 전체 경로에서 제어기는 **76분짜리 등산 안내 시간에 대해 78분**이 걸렸다 — 2분 *초과*이고, 논문은 이를 "사실상 같은 시간"이라 표현한다. 더 빨랐던 것은 정상 구간뿐이다: 표지판의 35분에 대해 31분. 외부에서 정의되었고 저자가 고르지 않았다는 점에서 정말 좋은 지표지만, 경로 하나이지 경로의 분포가 아니다. [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]과 마찬가지로 **초록에 성공률도 비교 수치도 없다.**

### Limitations & critique

- **Learned trust is still trust.** The gating is trained on the failure modes present in simulation and in the training deployments. A novel way for perception to be wrong — a mirrored curtain wall, a laser-scanned dust cloud — is outside what the encoder learned to distrust.
- **Falling back is not free.** When exteroception is discarded the controller degrades toward the blind regime, which means the speed advantage disappears exactly in the conditions where speed was hardest to get.
- **Still locomotion, not navigation.** Where to go remains someone else's problem — see [[04-robotics/semantic-language-navigation|19]].
- The method presumes a terrain map exists to be judged; it does not build one.

### Impact & follow-ups

Together with [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] this pair defines the modern legged-control recipe, and the "learn when to trust a sensor" pattern generalises well past locomotion — it is the same problem a construction robot has with a dusty depth camera, and the same problem a manipulation policy has with an occluded wrist view.

**For construction**: this is the paper to cite for why a site robot should not be given a perception stack it must trust unconditionally. Dust, glare off glazing, wet concrete and standing water are the paper's own listed failure conditions, restated in site vocabulary.

### Connections

- [[04-robotics/legged-locomotion|18. Legged Locomotion]] — the concept page
- [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee et al. 2020]] — the blind controller this extends
- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — where the terrain signal comes from
- [[04-robotics/robot-systems-deployment|10. Robot Systems, Embodiment & Deployment]] — sensor failure as a systems property

### After reading

- [ ] State the specific reason exteroception is dangerous outdoors, in the paper's own terms.
- [ ] Explain what the attention mechanism decides, and why a fixed confidence threshold is not equivalent.
- [ ] Say what the Alpine hike measures, and what it does not.
- [ ] Name the condition under which this controller's advantage over a blind one disappears.

## 한국어

**한 줄 요약**: 외수용 감각을 되돌려 넣되 결코 무조건 믿지 않는다 — 어텐션 기반 순환 인코더가 지형 지도를 *언제* 믿을 수 있는지 학습하고, 믿을 수 없을 때는 고유수용 감각으로 물러난다. 그 결과가 빠르면서 동시에 강건한 제어기다.

### 배경

[[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]은 맹목 제어기가 대단히 강건함을 보였고 그 대가를 속도로 치렀다: 로봇이 보행을 조정하기 전에 지형을 물리적으로 더듬어야 한다. 이 논문의 초록은 그 교환을 직접 진술한다 — 접촉 *이전에* 지형을 인지하는 것이 보행을 미리 계획하게 해주고, 속도와 에너지 효율이 거기서 나온다.

장애물은 야외 외수용 감각이 단지 노이즈가 많은 것이 아니라 **체계적으로 틀린다**는 점이다: 눈·식생·물은 로봇이 디딜 수 없는 장애물로 보이거나, 반사율이 높아 아예 사라진다. 그 위에 어려운 조명, 먼지, 안개, 반사면·투명면, 가림이 깊이를 더 망가뜨린다.

### 방법

> [!tip] 핵심 직관
> "지도가 뭐라고 하는가"를 묻지 마라. "**지금 이 지도를 믿어야 하는가**"를 물어라. 인코더를 end-to-end로 학습해 그 판단 자체를 배우게 하는 것이, 손으로 맞춘 신뢰도 임계값이 결코 할 수 없는 일이다.

**어텐션 기반 순환 인코더**가 고유수용 입력과 외수용 입력을 통합하고, end-to-end로 학습되며, **휴리스틱에 의존하지 않고** 모달리티를 결합하는 법을 배운다. 순환이 믿음을 시간에 걸쳐 나르고, 어텐션이 외수용 채널에 얼마의 가중치를 줄지 정한다.

### 결과

증거는 배포의 폭에 기억할 만한 실증 하나가 더해진 형태다: **여러 계절에 걸쳐 다양한 험한 자연·도시 환경**에서의 시험, 그리고 **알프스에서 사람 등산객에게 권장되는 시간 안에 한 시간짜리 산행 완주**.

> [!warning] 주장 읽는 법 · Reading the claim
> 알프스 산행은 성공률이 아니라 *시간 예산* 결과다: 2.2 km 전체 경로에서 제어기는 **76분짜리 등산 안내 시간에 대해 78분**이 걸렸다 — 2분 *초과*이고, 논문은 이를 "사실상 같은 시간"이라 표현한다. 더 빨랐던 것은 정상 구간뿐이다: 표지판의 35분에 대해 31분. 외부에서 정의되었고 저자가 고르지 않았다는 점에서 정말 좋은 지표지만, 경로 하나이지 경로의 분포가 아니다. [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]과 마찬가지로 **초록에 성공률도 비교 수치도 없다.**
> The Alpine hike is a time-budget result against an externally published human recommendation — one route, not a distribution.

### 한계와 비판

- **학습된 신뢰도 여전히 신뢰다.** 게이팅은 시뮬레이션과 학습 배포에 존재했던 실패 양상 위에서 학습된다. 인지가 틀리는 새로운 방식 — 거울 커튼월, 레이저에 잡힌 먼지 구름 — 은 인코더가 불신하도록 배운 범위 밖이다.
- **물러서는 것이 공짜가 아니다.** 외수용 감각을 버리면 제어기는 맹목 영역 쪽으로 성능이 내려가고, 그것은 속도를 얻기 가장 어려웠던 바로 그 조건에서 속도 이점이 사라진다는 뜻이다.
- **여전히 로코모션이지 내비게이션이 아니다.** 어디로 갈지는 남의 문제다 — [[04-robotics/semantic-language-navigation|19]]를 보라.
- 이 방법은 판단할 지형 지도가 이미 있다고 전제한다. 지도를 만들지는 않는다.

### 영향과 후속 연구

[[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]]과 함께 이 둘이 현대 레그드 제어의 표준 레시피를 정의한다. 그리고 "센서를 언제 믿을지 학습한다"는 패턴은 로코모션을 훨씬 넘어 일반화된다 — 먼지 낀 깊이 카메라를 든 건설 로봇의 문제도, 손목 시야가 가려진 조작 정책의 문제도 같은 문제다.

**건설의 경우**: 현장 로봇에게 무조건 믿어야 하는 인지 스택을 쥐여주면 안 되는 이유로 인용할 논문이다. 먼지, 유리에서 되쏘는 반사광, 젖은 콘크리트, 고인 물은 이 논문이 스스로 나열한 실패 조건을 현장 어휘로 옮긴 것에 지나지 않는다.

### 연결

- [[04-robotics/legged-locomotion|18. 레그드 로코모션]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/lee-quadruped-terrain|Lee 등 2020]] — 이것이 확장하는 맹목 제어기
- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율주행]] — 지형 신호가 오는 곳
- [[04-robotics/robot-systems-deployment|10. 로봇 시스템·구현·배포]] — 시스템 성질로서의 센서 실패

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 야외에서 외수용 감각이 위험한 구체적 이유를 논문의 표현으로 말한다.
- [ ] 어텐션이 무엇을 결정하며, 고정 신뢰도 임계값이 왜 같지 않은지 설명한다.
- [ ] 알프스 산행이 무엇을 재고 무엇을 재지 않는지 말한다.
- [ ] 이 제어기의 맹목 제어기 대비 이점이 사라지는 조건을 댄다.
