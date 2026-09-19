---
title: 3. Vision–Language Models
tags: [deep-learning, vlm, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Distinguish contrastive alignment, fusion, and generation; compute a contrastive batch; and bound what language-grounded evidence proves."
mastery-when: "Raise when multimodal grounding, representation, or language-conditioned perception is modified in the thesis."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/computer-vision/index|2. Computer Vision]], [[02-foundations/information-theory|5. Information Theory]], and [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|the Transformer note]].

## English

> [!note] First pass
> Read D3, §2, and questions 1–2. Return to §3 when a caption or VQA number is treated as grounding.

### Running object: D3

**D3** from [[03-deep-learning/lab-objects|0. Lab Objects]] is three matched image–caption pairs with frozen unit embeddings and $\tau=1/2$:

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix}.$$

Similarity logits are $\ell_{ij}=v_i^\top t_j/\tau$. Rows ask “which text matches this image?”; columns ask the reverse.

### 1. Three VLM families

- **dual encoder:** image and text encoded separately; fast retrieval and zero-shot classification through similarity.
- **fusion model:** tokens interact through cross-attention; stronger pair reasoning, more expensive all-pairs use.
- **generative model:** predicts language tokens conditioned on visual representations; fluent output is not proof of grounded perception.

### 2. Contrastive learning, by hand

Image 1 dots are $v_1^\top t_j=(1,1/2,0)$. Dividing by $\tau=1/2$ gives logits $(2,1,0)$. Its correct-pair probability is

$$p_{11}=\frac{e^2}{e^2+e+1}=0.665,\qquad L_{i\to t}=-\log p_{11}=0.408.$$

The full CLIP-style objective averages image-to-text and text-to-image cross-entropies over the batch. The other batch members are not generic “wrong language”; they are sampled negatives. False negatives and batch composition therefore affect what is learned.

### 3. Conditioning is not grounding

A model is *conditioned on* an image when the image changes its output distribution. Grounding additionally asks whether a claim or token is supported by localized visual evidence. Caption likelihood, retrieval accuracy, VQA accuracy, hallucination rate, and spatial grounding measure different abilities.

### 4. From VLM to robot use

VLM representations can supply semantic labels, language-conditioned goals, reward signals, or a backbone for a VLA. None of these alone supplies control frequency, action feasibility, or recovery. Read [[01-canonical-papers/notes/3-vlm/clip|CLIP]] first, then fusion/generative entries and the [[03-deep-learning/vla/index|VLA course]].

### Problem set

1. **Draw.** Draw D3's $3\times3$ similarity matrix and mark positives on the diagonal.
2. **Derive.** On D3 image 1, recompute logits and row loss at $\tau=1/4$. Explain the effect of the lower temperature.
3. **Interpret.** A model answers “red valve” correctly but no localization or intervention is tested. What claim remains open?

> [!tip]- Solutions
> 1. Rows are images, columns captions; $(i,i)$ are matched pairs.
> 2. Dots unchanged, so logits $(4,2,0)$. $p=e^4/(e^4+e^2+1)=0.867$, loss $0.143$. Sharper logits improve confidence here but also sharpen mistakes.
> 3. Whether the answer is grounded in the valve pixels rather than language priors.

### Exit check

Identify a VLM's encoder/fusion/generation pattern, objective, negatives, output, and the experiment needed to separate semantic fluency from visual grounding.

## 한국어

> [!note] 처음이라면
> D3, §2, 문제 1–2를 먼저 한다. caption이나 VQA 숫자를 grounding으로 읽을 때 §3으로 돌아온다.

### 계속 쓰는 대상: D3

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D3**는 이미지–캡션 3쌍이다. 고정 임베딩과 $\tau=1/2$는

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix}.$$

logit은 $\ell_{ij}=v_i^\top t_j/\tau$다. 행은 이미지에 맞는 텍스트, 열은 텍스트에 맞는 이미지를 묻는다.

### 1. 세 VLM 계열

- dual encoder: 따로 encoding해 similarity로 retrieval·zero-shot 분류.
- fusion model: cross-attention으로 token을 섞어 pair reasoning.
- generative model: 시각 표현을 조건으로 language token 생성. 유창함은 grounding 증거가 아니다.

### 2. 대조학습 계산

이미지 1의 내적은 $v_1^\top t_j=(1,1/2,0)$이고 $\tau=1/2$로 나누면 logit $(2,1,0)$이다. 정답 확률은 $0.665$, loss는 $0.408$이다. 전체 목적함수는 image→text와 text→image cross-entropy를 평균한다. batch의 다른 항목은 sampled negative라서 false negative와 batch 구성이 학습을 바꾼다.

### 3. Conditioning은 grounding이 아니다

이미지가 출력 분포를 바꾸면 conditioning이다. grounding은 주장이나 token이 국소 시각 증거에 지지되는지 추가로 묻는다. caption likelihood·retrieval·VQA·hallucination·spatial grounding은 서로 다른 능력이다.

### 4. 로봇으로의 연결

VLM은 의미 label, 언어 목표, reward, VLA backbone을 줄 수 있지만 제어 주기·행동 가능성·recovery를 자동으로 주지 않는다.

### 과제

1. D3의 $3\times3$ similarity matrix와 diagonal positive를 그린다.
2. D3 이미지 1에서 $\tau=1/4$일 때 logit과 row loss, 낮은 temperature의 효과를 계산한다.
3. “red valve” 정답만으로 남는 grounding 질문을 말한다.

> [!tip]- 정답
> 1. 행=image, 열=caption, $(i,i)$가 positive.
> 2. 내적은 같고 logit은 $(4,2,0)$. 확률 $0.867$, loss $0.143$; 맞을 때 더 자신 있지만 오류도 날카로워진다.
> 3. valve pixel을 실제 사용했는지 language prior를 사용했는지 미확인이다.

### 통과 기준

VLM의 encoder/fusion/generation 구조, 목적함수, negative, 출력과 fluency–grounding을 가르는 실험을 설명할 수 있다.
