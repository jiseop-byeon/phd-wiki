---
title: "BERT — Pre-training of Deep Bidirectional Transformers"
authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
affiliation: Google AI Language
venue: NAACL
year: 2019
arxiv: https://arxiv.org/abs/1810.04805
pdf: https://arxiv.org/pdf/1810.04805
code: https://github.com/google-research/bert
tags: [paper, foundations, nlp]
status: to-read
---

**Devlin et al., NAACL 2019** — [arXiv](https://arxiv.org/abs/1810.04805) · [PDF](https://arxiv.org/pdf/1810.04805) · [Code](https://github.com/google-research/bert)

## English

**One-line summary**: Pre-train a bidirectional Transformer encoder with masked language modeling, then fine-tune it — one recipe swept every NLP benchmark and established the pretrain-finetune paradigm.

### Context

After the [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]], language model pre-training was emerging (ELMo's contextual embeddings, GPT-1's left-to-right Transformer). But left-to-right models can't let a word see its *right* context, and shallow bidirectional features (ELMo) only concatenate two one-directional views. The question: how to pre-train *deeply bidirectional* representations without the model trivially seeing itself?

### Method

> [!tip] Key intuition
> You can't train a bidirectional LM by predicting the next word (the answer leaks). So hide 15% of the words and make the model fill in the blanks — a cloze task — forcing every representation to integrate context from both sides.

- **Masked LM (MLM)**: randomly mask 15% of tokens; predict them from full bidirectional context (with the 80/10/10 mask/random/keep trick to reduce pretrain-finetune mismatch).
- **Next Sentence Prediction (NSP)**: classify whether sentence B follows A — intended to teach inter-sentence relations (later shown mostly unnecessary by RoBERTa).
- Architecture: Transformer *encoder* only. BERT-base 110M / BERT-large 340M parameters, trained on BooksCorpus + Wikipedia (3.3B words).
- Downstream use: add a small task head and **fine-tune everything** — same pretrained weights for classification, QA, NER, etc.

### Results

- New state of the art on **11 NLP tasks** at once: GLUE +7.7%p absolute, SQuAD v1.1 F1 93.2 (surpassing human performance), etc.
- Large gains even for small downstream datasets — pre-training is doing most of the work.

### Limitations & critique

- Encoder-only: cannot generate text — the paradigm that scaled (GPT) eventually dominated for that reason.
- MLM wastes computation (predicts only 15% of positions per pass); NSP proved nearly useless (RoBERTa dropped it and improved).
- Fixed 512-token context; fine-tuning per task means one specialized model per task, unlike the in-context learning of [[01-canonical-papers/notes/gpt-3|GPT-3]].

### Impact & follow-ups

Made "download pretrained weights, fine-tune on your data" the default workflow of applied NLP — the same paradigm later inherited by vision ([[01-canonical-papers/notes/mae|MAE]]) and robotics (VLA fine-tuning). Descendants: RoBERTa, ALBERT, ELECTRA, DistilBERT; MLM itself reappears as masked-patch pretraining in [[01-canonical-papers/notes/mae|MAE]].

### Connections

- Previous: [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]] · Contrast: [[01-canonical-papers/notes/gpt-3|GPT-3]] (decoder, in-context learning)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 양방향 Transformer 인코더를 masked LM으로 사전학습한 뒤 파인튜닝 — 하나의 레시피로 NLP 벤치마크 전체를 석권하며 사전학습-파인튜닝 패러다임을 확립했다.

### 배경

[[01-canonical-papers/notes/attention-is-all-you-need|Transformer]] 이후 언어모델 사전학습이 떠오르고 있었다(ELMo의 문맥 임베딩, GPT-1의 좌→우 Transformer). 하지만 좌→우 모델은 단어가 자신의 *오른쪽* 문맥을 볼 수 없고, ELMo의 얕은 양방향은 한 방향짜리 표현 둘을 이어붙인 것에 불과했다. 질문: 모델이 답을 미리 보는 문제 없이 *깊게 양방향인* 표현을 어떻게 사전학습할까?

### 방법

> [!tip] 핵심 직관
> 다음 단어 예측으로는 양방향 LM을 학습할 수 없다(답이 새어 나온다). 그러니 단어의 15%를 가리고 빈칸 채우기를 시키자 — 모든 표현이 양쪽 문맥을 통합하도록 강제된다.

- **Masked LM (MLM)**: 토큰의 15%를 무작위로 가리고 완전한 양방향 문맥에서 예측 (사전학습-파인튜닝 불일치를 줄이는 80/10/10 트릭 포함).
- **Next Sentence Prediction (NSP)**: 문장 B가 A 뒤에 오는지 분류 — 문장 간 관계 학습이 목적이었지만 이후 RoBERTa가 거의 불필요함을 보임.
- 구조: Transformer *인코더*만 사용. BERT-base 1.1억 / BERT-large 3.4억 파라미터, BooksCorpus + Wikipedia(33억 단어)로 학습.
- 다운스트림: 작은 태스크 헤드를 얹고 **전체를 파인튜닝** — 분류·QA·NER 모두 같은 사전학습 가중치에서 출발.

### 결과

- **11개 NLP 과제**에서 동시에 신기록: GLUE +7.7%p, SQuAD v1.1 F1 93.2(인간 성능 상회) 등.
- 다운스트림 데이터가 작아도 큰 이득 — 일의 대부분을 사전학습이 하고 있다는 뜻.

### 한계와 비판

- 인코더 전용이라 텍스트 생성 불가 — 결국 생성이 되는 GPT 계열이 스케일 경쟁에서 승리한 이유.
- MLM은 연산 낭비가 있다(한 번에 15% 위치만 예측); NSP는 거의 무용지물로 판명(RoBERTa는 빼고 더 좋아짐).
- 512 토큰 고정 문맥; 과제마다 파인튜닝 = 과제마다 전용 모델 — [[01-canonical-papers/notes/gpt-3|GPT-3]]의 in-context learning과 대비된다.

### 영향과 후속 연구

"사전학습 가중치를 받아 내 데이터로 파인튜닝"을 응용 NLP의 기본 워크플로로 만들었다 — 이 패러다임은 비전([[01-canonical-papers/notes/mae|MAE]])과 로보틱스(VLA 파인튜닝)로 그대로 계승된다. 후손: RoBERTa, ALBERT, ELECTRA, DistilBERT; MLM 아이디어는 [[01-canonical-papers/notes/mae|MAE]]의 마스크된 패치 사전학습으로 재등장한다.

### 연결

- 이전: [[01-canonical-papers/notes/attention-is-all-you-need|Transformer]] · 대비: [[01-canonical-papers/notes/gpt-3|GPT-3]] (디코더, in-context learning)
- 계보: [[03-deep-learning/lineage|논문 계보도]]
