---
title: "Making Sense of Vision and Touch: Self-Supervised Learning of Multimodal Representations for Contact-Rich Tasks"
authors: Michelle A. Lee, Yuke Zhu, Krishnan Srinivasan, et al.
affiliation: Stanford University
venue: ICRA
year: 2019
arxiv: https://arxiv.org/abs/1810.10191
pdf: https://arxiv.org/pdf/1810.10191
code: https://github.com/stanford-iprl-lab/multimodal_representation
project: https://sites.google.com/view/visionandtouch
tags: [paper, manipulation, tactile, representation-learning]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when visuotactile fusion or a touch-conditioned policy is part of the thesis contribution."
---

**Lee et al., ICRA 2019, pp. 8943–8950** — [arXiv](https://arxiv.org/abs/1810.10191) · [PDF](https://arxiv.org/pdf/1810.10191) · [Code](https://github.com/stanford-iprl-lab/multimodal_representation) · [Official](https://sites.google.com/view/visionandtouch)

> [!note] Math on-ramp · 수학 준비물
> Two ideas carry this paper. **Self-supervision**: a training signal built from the data's own structure instead of labels — here one modality predicting another ([[02-foundations/ml-practice|9. ML Practice]] for why that matters when labels are expensive). And **representation learning**: policy learning happens in a learned latent space rather than on raw pixels and newtons, which is the sample-efficiency argument of [[02-foundations/rl-basics|7. RL Basics]].
> 두 발상이 이 논문을 진다. **자기지도**: 라벨 대신 데이터 자신의 구조에서 만든 학습 신호 — 여기서는 한 모달리티가 다른 모달리티를 예측한다(라벨이 비쌀 때 왜 중요한지는 [[02-foundations/ml-practice|9. ML 실무]]). 그리고 **표현 학습**: 정책 학습이 원 픽셀과 뉴턴이 아니라 학습된 잠재 공간에서 일어난다 — [[02-foundations/rl-basics|7. RL 기초]]의 샘플 효율 논증.

## English

**One-line summary**: Fuse RGB, force/torque and proprioception into one compact latent using self-supervised objectives the modalities generate for each other, then learn contact-rich insertion in that latent space instead of on raw inputs.

### Context

Contact-rich manipulation needs both vision (where things are) and touch (what is happening
at the contact), and the reasons vision alone is not enough are the ones in
[[04-robotics/tactile-visuotactile|14. §1]]. But naively concatenating an image, a
six-axis wrench, and joint states gives a high-dimensional, badly-conditioned input, and
reinforcement learning on a real robot cannot afford to learn a representation and a policy
at the same time from scratch.

The obvious fix — supervise the representation — runs into the usual wall: nobody has
labels for "what a good multimodal representation of contact looks like".

### Method

> [!tip] Key intuition
> The modalities can supervise each other. If you can see the scene and feel the contact,
> then each one carries information about the other — so predicting one from the other is a
> free training signal, available in unlimited quantity, with no human labelling at all.

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="three input streams fused into one latent that feeds two self-supervised heads and a policy">
  <g fill="currentColor">
    <rect x="24" y="40" width="104" height="30" rx="3" fill-opacity="0.12"/>
    <rect x="24" y="80" width="104" height="30" rx="3" fill-opacity="0.12"/>
    <rect x="24" y="120" width="104" height="30" rx="3" fill-opacity="0.12"/>
    <rect x="188" y="70" width="94" height="50" rx="3" fill-opacity="0.30"/>
    <rect x="352" y="26" width="184" height="30" rx="3" fill-opacity="0.18"/>
    <rect x="352" y="66" width="184" height="30" rx="3" fill-opacity="0.18"/>
    <rect x="352" y="112" width="184" height="30" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="40" width="104" height="30" rx="3"/><rect x="24" y="80" width="104" height="30" rx="3"/><rect x="24" y="120" width="104" height="30" rx="3"/>
    <rect x="188" y="70" width="94" height="50" rx="3"/>
    <rect x="352" y="26" width="184" height="30" rx="3"/><rect x="352" y="66" width="184" height="30" rx="3"/><rect x="352" y="112" width="184" height="30" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.75" marker-end="url(#arV)">
    <path d="M 132 55 L 160 55 L 160 88 L 184 88"/>
    <line x1="132" y1="95" x2="184" y2="95"/>
    <path d="M 132 135 L 160 135 L 160 102 L 184 102"/>
    <path d="M 286 88 L 318 88 L 318 41 L 348 41"/>
    <line x1="286" y1="95" x2="348" y2="81"/>
    <path d="M 286 102 L 318 102 L 318 127 L 348 127"/>
  </g>
  <defs><marker id="arV" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="76" y="59">RGB image</text>
    <text x="76" y="99">force / torque</text>
    <text x="76" y="139">proprioception</text>
    <text x="235" y="91" font-size="10.5">fused</text><text x="235" y="105" font-size="10.5">latent</text>
    <text x="444" y="45">predict optical flow</text>
    <text x="444" y="85">predict: does contact occur?</text>
    <text x="444" y="131">policy, learned by RL</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="176">The top two heads are the trick. Neither needs a human label &#8212; the image supplies the flow</text>
    <text x="20" y="192">target and the wrench supplies the contact target, so training needs no annotation at all.</text>
    <text x="20" y="216">Only the third head is the task. Learning it in the latent space rather than on raw pixels and</text>
    <text x="20" y="232">newtons is what makes reinforcement learning affordable on a real arm.</text>
  </g>
</svg>

- **Inputs**: RGB image, six-axis force/torque, and end-effector proprioception, each
  through its own encoder.
- **Self-supervised objectives**: predict **optical flow** (the image's own next-frame
  motion) and predict **whether contact occurs**. Both targets are computable from the data
  itself, so the representation can be trained without any human annotation.
- **Then policy learning**: reinforcement learning runs on the compact fused latent, not on
  the raw streams — which is the step that makes real-robot training tractable.
- **Task**: peg insertion, the canonical contact-rich problem
  ([[04-robotics/force-compliance-control|13. §5]] for why insertion is the hard case).

### Results

> [!warning] Reading the claims · 주장 읽는 법
> **This paper's abstract states no numbers** — not a success rate, not a sample-efficiency
> multiplier, not a vision-only comparison. Its strongest abstract-level claim is verbatim
> "generalizing over different geometry, configurations, and clearances, while being robust
> to external perturbations" — note the exact wording, which is routinely misquoted as
> "varying geometries". The insertion success rates commonly quoted for it are body-only. Check them there before citing.
> **이 논문의 초록에는 숫자가 없다** — 성공률도, 샘플 효율 배수도, 비전만과의 비교도. 초록
> 수준의 가장 강한 주장은 원문 그대로 "generalizing over different geometry, configurations,
> and clearances, while being robust to external perturbations"이다 — "varying geometries"로
> 잘못 인용되는 일이 잦으니 표현을 정확히 옮겨라. 흔히 인용되는 삽입 성공률은 본문에만 있다. 인용 전에 거기서 확인하라.

The claim that matters is the generalisation one: the same learned representation transfers
across geometries, configurations and clearances rather than being fitted to one peg.

### Limitations & critique

- **What fusion buys is sample efficiency, not a new capability.** The honest reading from
  [[04-robotics/tactile-visuotactile|14. §4]]: this makes learning affordable on a real
  robot, which is a large win where data is the binding constraint — but it is a different
  claim from "the task is impossible without touch".
- **The tactile channel is a wrist wrench**, not a dense contact image, so the fine contact
  geometry an optical tactile sensor would supply is not in this representation at all.
- Peg insertion is a well-posed, well-instrumented task; how the approach fares on
  deformable or dimensionally uncertain parts is not answered here.
- The self-supervised objectives were *chosen*; the paper's journal version ablates them,
  which is where to look before assuming these two are the right pair for another task.

### Impact & follow-ups

This is the reference architecture for visuotactile representation learning, and its claim
structure — raw multimodal input is badly conditioned, self-supervision supplies free
signal, the compact latent makes real-robot learning tractable — recurs across the area.

**Cite it carefully.** The extended journal version is *"Making Sense of Vision and Touch:
Learning Multimodal Representations for Contact-Rich Tasks"* (T-RO, vol. 36, no. 3,
pp. 582–596, 2020) — note that **"Self-Supervised" is dropped from the title and the author
list differs**. They are two entries, not one.

### Connections

- [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing]] — the concept page this is the anchor for
- [[04-robotics/force-compliance-control|13. Force & Compliance Control]] — why insertion is the hard contact case
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — the policy-class alternative to learning a representation first

### After reading

- [ ] Name the two self-supervised objectives and say why neither needs a label.
- [ ] Explain why policy learning happens in the latent space rather than on raw inputs.
- [ ] State what fusion usually buys and what it does not.
- [ ] Give both versions' titles and say why they are separate citations.

## 한국어

**한 줄 요약**: RGB·힘/토크·고유수용감각을, 모달리티끼리 서로 만들어 주는 자기지도 목적함수로 하나의 압축된 잠재 표현에 융합하고, 원 입력이 아니라 그 잠재 공간에서 접촉 다량 삽입을 학습한다.

### 배경

접촉 다량 조작에는 비전(무엇이 어디 있는가)과 촉각(접촉에서 무슨 일이 일어나는가)이 둘 다
필요하고, 비전만으로 부족한 이유는 [[04-robotics/tactile-visuotactile|14. §1]]의 그것들이다.
그런데 이미지와 6축 렌치와 관절 상태를 소박하게 이어 붙이면 고차원이고 조건이 나쁜 입력이
되며, 실기계 강화학습은 표현과 정책을 동시에 처음부터 배울 여유가 없다.

명백한 처방 — 표현을 지도학습하기 — 은 늘 같은 벽에 부딪힌다: "접촉의 좋은 멀티모달 표현이
어떻게 생겼는가"에 대한 라벨은 아무도 갖고 있지 않다.

### 방법

> [!tip] 핵심 직관
> 모달리티끼리 서로를 지도할 수 있다. 장면을 볼 수 있고 접촉을 느낄 수 있다면 각각이 다른
> 쪽에 대한 정보를 담고 있으므로, 하나에서 다른 하나를 예측하는 것이 공짜 학습 신호가 된다 —
> 무제한으로 있고, 사람의 라벨링은 하나도 필요 없다.

<svg viewBox="0 0 560 250" style="max-width:100%;height:auto" role="img" aria-label="세 입력 스트림이 하나의 잠재 표현으로 융합되어 자기지도 헤드 둘과 정책에 들어간다">
  <g fill="currentColor">
    <rect x="24" y="40" width="104" height="30" rx="3" fill-opacity="0.12"/>
    <rect x="24" y="80" width="104" height="30" rx="3" fill-opacity="0.12"/>
    <rect x="24" y="120" width="104" height="30" rx="3" fill-opacity="0.12"/>
    <rect x="188" y="70" width="94" height="50" rx="3" fill-opacity="0.30"/>
    <rect x="352" y="26" width="184" height="30" rx="3" fill-opacity="0.18"/>
    <rect x="352" y="66" width="184" height="30" rx="3" fill-opacity="0.18"/>
    <rect x="352" y="112" width="184" height="30" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="40" width="104" height="30" rx="3"/><rect x="24" y="80" width="104" height="30" rx="3"/><rect x="24" y="120" width="104" height="30" rx="3"/>
    <rect x="188" y="70" width="94" height="50" rx="3"/>
    <rect x="352" y="26" width="184" height="30" rx="3"/><rect x="352" y="66" width="184" height="30" rx="3"/><rect x="352" y="112" width="184" height="30" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.75" marker-end="url(#arVk)">
    <path d="M 132 55 L 160 55 L 160 88 L 184 88"/>
    <line x1="132" y1="95" x2="184" y2="95"/>
    <path d="M 132 135 L 160 135 L 160 102 L 184 102"/>
    <path d="M 286 88 L 318 88 L 318 41 L 348 41"/>
    <line x1="286" y1="95" x2="348" y2="81"/>
    <path d="M 286 102 L 318 102 L 318 127 L 348 127"/>
  </g>
  <defs><marker id="arVk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="76" y="59">RGB 이미지</text>
    <text x="76" y="99">힘 / 토크</text>
    <text x="76" y="139">고유수용감각</text>
    <text x="235" y="91" font-size="10.5">융합된</text><text x="235" y="105" font-size="10.5">잠재 표현</text>
    <text x="444" y="45">광학 흐름 예측</text>
    <text x="444" y="85">접촉이 일어나는가 예측</text>
    <text x="444" y="131">RL로 학습하는 정책</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="176">위의 두 헤드가 요령이다. 둘 다 사람의 라벨이 필요 없다 &#8212; 이미지가 흐름의 정답을, 렌치가 접촉의</text>
    <text x="20" y="192">정답을 공급하므로, 표현이 로봇이 어차피 만들어내는 데이터로 학습된다.</text>
    <text x="20" y="216">과제는 세 번째 헤드뿐이다. 원 픽셀과 뉴턴이 아니라 잠재 공간에서 그것을 학습하는 것이,</text>
    <text x="20" y="232">실제 팔에서 강화학습을 감당 가능하게 만든다.</text>
  </g>
</svg>

- **입력**: RGB 이미지, 6축 힘/토크, 말단 고유수용감각. 각각 자기 인코더를 통과한다.
- **자기지도 목적함수**: **광학 흐름** 예측(이미지 자신의 다음 프레임 운동)과 **접촉 발생
  여부** 예측. 두 정답 모두 데이터 자체에서 계산되므로 사람의 주석 없이 표현을 학습할 수 있다.
- **그다음 정책 학습**: 강화학습이 원 스트림이 아니라 압축된 융합 잠재 표현 위에서 돈다 —
  실기계 학습을 감당 가능하게 만드는 단계가 이것이다.
- **과제**: peg 삽입. 정본 접촉 다량 문제이며, 삽입이 왜 어려운 경우인지는
  [[04-robotics/force-compliance-control|13. §5]].

### 결과

> [!warning] 주장 읽는 법 · Reading the claim
> **이 논문의 초록에는 숫자가 없다** — 성공률도, 샘플 효율 배수도, 비전만과의 비교도. 초록
> 수준의 가장 강한 주장은 표현이 "다양한 기하·구성·공차에 걸쳐 일반화하며 외부 교란에
> 견고하다"는 것이다. 흔히 인용되는 삽입 성공률은 본문에만 있다.
> **The abstract states no numbers**; the commonly quoted insertion success rates are
> body-only. Check them there before citing.

중요한 주장은 일반화 쪽이다: 같은 학습된 표현이 하나의 peg에 맞춰진 것이 아니라 여러 기하·
구성·공차를 가로질러 이전된다는 것.

### 한계와 비판

- **융합이 사는 것은 샘플 효율이지 새 능력이 아니다.** [[04-robotics/tactile-visuotactile|14. §4]]의
  정직한 독법: 데이터가 제약인 실기계에서 학습을 감당 가능하게 만드는 큰 승리이지만,
  "촉각 없이는 그 과제가 불가능하다"와는 다른 주장이다.
- **촉각 채널이 손목 렌치**이지 조밀한 접촉 이미지가 아니므로, 광학 촉각 센서가 줄 미세한
  접촉 기하는 이 표현에 아예 없다.
- Peg 삽입은 잘 정의되고 계측이 잘 된 과제다. 변형되거나 치수가 불확실한 부재에서 이 접근이
  어떨지는 여기서 답하지 않는다.
- 자기지도 목적함수는 *선택된* 것이다. 저널판이 이를 ablation하므로, 다른 과제에 이 둘이
  옳은 짝이라고 가정하기 전에 거기를 보라.

### 영향과 후속 연구

시촉각 표현 학습의 기준 아키텍처이며, 그 주장 구조 — 원 멀티모달 입력은 조건이 나쁘다, 자기
지도가 공짜 신호를 준다, 압축된 잠재 표현이 실기계 학습을 감당 가능하게 한다 — 가 이 영역
전반에서 반복된다.

**인용에 주의.** 확장된 저널판은 *"Making Sense of Vision and Touch: Learning Multimodal
Representations for Contact-Rich Tasks"*(T-RO, vol. 36, no. 3, pp. 582–596, 2020)이며,
**제목에서 "Self-Supervised"가 빠지고 저자 목록도 다르다.** 하나가 아니라 두 항목이다.

### 연결

- [[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱]] — 이 논문이 앵커인 개념 페이지
- [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]] — 삽입이 왜 어려운 접촉 경우인가
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — 표현을 먼저 배우는 대신 정책 계열로 푸는 대안

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 두 자기지도 목적함수를 대고 왜 둘 다 라벨이 필요 없는지 말한다.
- [ ] 정책 학습이 왜 원 입력이 아니라 잠재 공간에서 일어나는지 설명한다.
- [ ] 융합이 보통 사는 것과 사지 못하는 것을 말한다.
- [ ] 두 판본의 제목을 대고 왜 별개의 인용인지 말한다.
