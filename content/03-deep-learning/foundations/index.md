---
title: 1. Learning Systems
tags: [deep-learning, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Trace one model from tensors and loss through an optimizer update, validation, and a defensible training claim."
mastery-when: "Raise when architecture, objective, optimization, or scaling is part of the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/neural-network-basics|0.7 Neural Networks]], [[02-foundations/calculus-backprop|2. Calculus & Backprop]], [[02-foundations/optimization|4. Optimization]], and [[02-foundations/ml-practice|9. ML Practice]].

## English

> [!note] First pass
> Read §§1–4 and do questions 1–2. Return to §5 when comparing training sections in papers.

### Running object: D1

Use **D1** from [[03-deep-learning/lab-objects|0. Lab Objects]], biases zero:

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}.$$

Forward: $W_1x=(1,2,1)$, $h=\operatorname{ReLU}(W_1x)=(1,2,1)$, $s=W_2h=(2,1)$. The prediction is $p=\operatorname{softmax}(s)$. A diagram must show shapes $2\rightarrow3\rightarrow2$. This is not **P1** ($2\to3\to1$ MSE).

### 1. A paper's model is a typed computation

Architecture prose becomes checkable only after attaching shapes. For a batch of $B$ samples, $X\in\mathbb R^{B\times2}$, $H\in\mathbb R^{B\times3}$, and $S\in\mathbb R^{B\times2}$. Parameters are learned; activations are sample-dependent; hyperparameters are chosen outside gradient descent. If these three are mixed, parameter counts and claims about efficiency become unreliable.

Those logits $s=(2,1)$ are D1's forward pass, not a second example:

$$p_1=\frac{e^2}{e^2+e^1}=0.731,\qquad p_2=0.269.$$

With class 1 as the target, cross-entropy is $-\log p_1=0.313$. Adding the same constant to both logits changes neither probability: softmax represents relative evidence.

### 2. One update is not a training result

For one-hot target $y$, softmax plus cross-entropy gives the useful derivative

$$\frac{\partial L}{\partial s}=p-y.$$

Here it is $(-0.269,0.269)$: raise the correct logit and lower the other. Backpropagating this vector computes gradients; the optimizer converts them into an update. SGD, momentum, and Adam therefore change the *update rule*, not the model's forward definition.

### 3. Training, validation, and test answer different questions

- training loss: can the parameters fit sampled training batches?
- validation metric: which checkpoint or hyperparameter should be selected?
- test metric: how did the already frozen decision perform on held-out data?

Repeated test-guided tuning leaks test information. A paper that reports its best seed without a predeclared selection rule estimates luck as well as method quality.

### 4. Regularization and scaling are claims with controls

Weight decay, augmentation, dropout, early stopping, more data, and more compute can all improve a result through different mechanisms. A scaling claim needs axes—parameters, data, compute—and a controlled comparison. “Our larger model is better” does not identify which axis caused the gain.

### 5. How to read a training recipe

Extract: data mixture and split; preprocessing; initialization; objective and coefficients; optimizer and schedule; batch size and number of updates; precision and hardware; checkpoint selection; seeds and uncertainty. Then ask which choices are essential by reading ablations. This is the operational bridge to [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]], [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]], and [[01-canonical-papers/notes/1-foundations/adam|Adam]].

### Problem set

1. **Draw.** Draw D1 with batch shapes for $B=4$ and count weights including biases.
2. **Derive.** For logits $(0,\log 3)$ and target class 1, compute probabilities, loss, and $p-y$.
3. **Interpret.** Validation improves while test performance is repeatedly inspected and used to alter augmentation. Which boundary was crossed?

> [!tip]- Solutions
> 1. $X:4\times2$, $H:4\times3$, $S:4\times2$; parameters $(2\cdot3+3)+(3\cdot2+2)=17$.
> 2. $p=(1/4,3/4)$, $L=-\log(1/4)=1.386$, $p-y=(-3/4,3/4)$.
> 3. The test set became part of model selection; the reported test result is no longer an untouched estimate.

### Exit check

Explain the difference among parameter, activation, and hyperparameter; trace one loss derivative to the logits; and list the evidence needed to attribute improvement to a training change.

## 한국어

> [!note] 처음이라면
> §1–4와 문제 1–2를 먼저 한다. 논문의 학습 절을 비교할 때 §5로 돌아온다.

### 계속 쓰는 대상: D1

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D1**을 쓴다. bias는 0이다.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}.$$

순전파: $W_1x=(1,2,1)$, $h=\operatorname{ReLU}(W_1x)=(1,2,1)$, $s=W_2h=(2,1)$, $p=\operatorname{softmax}(s)$. 그림에 $2\rightarrow3\rightarrow2$ shape를 적는다. **P1**($2\to3\to1$ MSE)과 다른 장치다.

### 1. 모델은 형식이 붙은 계산이다

배치 크기 $B$이면 $X\in\mathbb R^{B\times2}$, $H\in\mathbb R^{B\times3}$, $S\in\mathbb R^{B\times2}$. 파라미터는 학습되고, activation은 샘플마다 달라지며, 하이퍼파라미터는 경사하강 밖에서 고른다.

이 $s=(2,1)$은 D1 순전파 결과다. $p=(0.731,0.269)$이고 정답이 1번일 때 cross-entropy는 $0.313$이다. 두 logit에 같은 상수를 더해도 확률은 같다. softmax는 상대적 증거를 표현한다.

### 2. 한 번의 update는 학습 결과가 아니다

one-hot $y$에 대해 softmax와 cross-entropy를 합치면 $\partial L/\partial s=p-y$다. 여기서는 $(-0.269,0.269)$이므로 정답 logit은 올리고 다른 logit은 내린다. backprop은 gradient를 계산하고 optimizer가 update로 바꾼다.

### 3. Train·validation·test의 질문은 다르다

- train loss: 학습 배치를 맞출 수 있는가.
- validation: checkpoint와 hyperparameter 중 무엇을 고를 것인가.
- test: 이미 고정한 결정을 미사용 자료에서 평가하면 어떤가.

test를 보며 계속 조정하면 test 정보가 학습 절차로 샌다.

### 4. 정규화와 scaling은 통제가 필요한 주장이다

weight decay, augmentation, dropout, early stopping, 데이터와 compute 증가는 서로 다른 기제로 결과를 바꾼다. scaling 주장은 parameter·data·compute 축을 분리해야 한다.

### 5. 학습 recipe 읽기

데이터 혼합·split, 전처리, 초기화, 목적함수, optimizer·schedule, batch와 update 수, precision·hardware, checkpoint 선택, seed와 불확실성을 뽑는다. 그다음 ablation에서 무엇이 필수인지 확인한다.

### 과제

1. $B=4$인 D1의 shape를 그리고 bias 포함 parameter 수를 센다.
2. logit $(0,\log3)$, 정답 1번의 확률·loss·$p-y$를 구한다.
3. test를 보며 augmentation을 바꿨다면 어떤 경계를 넘었는가.

> [!tip]- 정답
> 1. $4\times2\rightarrow4\times3\rightarrow4\times2$, 총 17개.
> 2. $p=(1/4,3/4)$, $L=1.386$, $p-y=(-3/4,3/4)$.
> 3. test가 모델 선택에 들어가 더 이상 독립 평가가 아니다.

### 통과 기준

parameter·activation·hyperparameter를 구분하고, loss에서 logit까지 gradient를 추적하며, 학습 변경의 효과를 주장하는 데 필요한 증거를 말할 수 있다.

