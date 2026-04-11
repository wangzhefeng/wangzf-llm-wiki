---
created_at: 2026-04-06
topics:
  - 自然语言处理
related_concepts:
  - 词表示
  - 语义空间
status: inbox
---

# Word2Vec

## 定义

Word2Vec 是一组将词转换为向量表示的模型，由 Google 的 Tomas Mikolov 团队提出。

## 核心思想

通过词的上下文来学习词的分布式表示，使得语义相近的词在向量空间中距离更近。

## 两种架构

### CBOW (Continuous Bag of Words)
- 根据上下文预测目标词
- 适合小数据集

### Skip-gram
- 根据目标词预测上下文
- 适合大数据集
- 对稀有词效果更好

## 关键特性

- **类比推理**: king - man + woman ≈ queen
- **语义相似度**: 余弦相似度度量
- **降维**: 比 one-hot 更高效

## 数学表达

Skip-gram 目标函数：

$$\max \sum_{t} \sum_{-c \leq j \leq c, j \neq 0} \log P(w_{t+j} | w_t)$$

其中 $c$ 是上下文窗口大小。

## 局限

- 一词多义问题（静态表示）
- 不考虑词序
- 被 Transformer/Embeddings 取代

## 相关来源

- [[NLP与词嵌入专题来源]]
- [[2026-04-06-2.图解Word2vec]]
- [[2026-04-06-What are embeddings]]

## 相关概念

- [[Embedding]]
- [[Self-Attention]]
- [[Transformer架构]]
