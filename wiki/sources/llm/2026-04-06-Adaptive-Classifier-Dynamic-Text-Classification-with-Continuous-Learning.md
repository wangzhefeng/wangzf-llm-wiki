---
title: 'Adaptive Classifier: Dynamic Text Classification with Continuous Learning'
created: 2026-04-15
updated: 2026-04-15
type: source
tags:
  - llm
sources:
  - raw/web/llm/2026-04-06-Adaptive-Classifier-Dynamic-Text-Classification-with-Continuous-Learning.md
status: summarized
---
## 内容摘要
We introduce **Adaptive Classifier**, a novel text classification system that enables dynamic class addition and continuous learning without catastrophic forgetting. Our approach combines prototype-ba

## 关键要点
- **Selective Example Retention**: We maintain up to k representative examples per class, selected through k-means clustering to preserve diversity
- **Incremental Index Updates**: FAISS indices are rebuilt only when accumulated updates exceed a threshold, balancing accuracy with computational efficiency
- **Normalized Embeddings**: All embeddings are L2-normalized to enable meaningful cosine similarity comparisons

## 来源信息
- 原始文件：2026-04-06-Adaptive-Classifier-Dynamic-Text-Classification-with-Continuous-Learning.md
- 来源类型：web
