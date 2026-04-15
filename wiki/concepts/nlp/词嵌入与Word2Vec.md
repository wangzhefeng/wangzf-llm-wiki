---
created_at: 2026-04-15
topics:
  - nlp
  - 词嵌入
  - word2vec
  - 表示学习
related_concepts:
  - 特征提取
  - 词向量
  - Embedding
  - NLP词嵌入与表示学习总索引
status: linked
---

# 词嵌入与 Word2Vec

## 一句话定义

词嵌入（Word Embedding）是将离散的词汇映射到连续的稠密向量空间中，使语义相似的词具有相近向量的方法；Word2Vec 是其代表性算法。

## 在知识体系中的位置

词嵌入是从"符号 NLP"向"向量 NLP"的关键转折点。它解决了传统独热编码（one-hot）的稀疏性和语义无关性问题，为随后的深度学习 NLP 奠定基础。现代 BERT、GPT 等预训练模型本质上是更深层的词嵌入方法，但理解 Word2Vec 的原理对掌握整个表示学习体系至关重要。

### 知识关联
- **前置概念**：[[特征提取]]（独热编码的局限性）
- **后继发展**：预训练模型（BERT）、[[自注意力机制]]
- **应用**：词相似度计算、文本分类（特征）、推荐系统

## 核心原理与方法

### Word2Vec 的两种架构

**1. Skip-gram 模型**
核心思想：**通过上下文词预测中心词**

给定中心词 $w$，预测其周围 window 大小内的词：
$$P(context|w) = \prod_{c \in context} P(c|w)$$

使用神经网络：输入词向量 $v_w$ → softmax → 预测每个上下文词的概率

**示例**：
```
句子：The quick brown fox jumps
window_size=2 for "brown":
- 输入词："brown"
- 目标词：["quick", "fox"] 
- 预测：P(quick|brown), P(fox|brown)
```

**2. CBOW（Continuous Bag of Words）模型**
核心思想：**通过中心词预测周围词**

使用上下文词向量平均来预测中心词。通常 CBOW 速度更快，Skip-gram 精度更高。

### 优化技巧

**负采样（Negative Sampling）**：
- 原始 softmax 需要对所有词计算概率（计算量大）
- 负采样：只对目标词和几个随机采样的负样本计算
- 效果：速度快 100 倍，精度相当

**分层 softmax**：
- 用二叉树结构代替平面 softmax
- 复杂度从 O(V) 降至 O(log V)，V 是词汇表大小

## 实战应用（3 个案例）

### 案例 1：用 Gensim 训练词向量

```python
from gensim.models import Word2Vec
sentences = [
    "the quick brown fox",
    "jumps over the lazy dog",
    "the dog sat on the mat"
]
model = Word2Vec(sentences=sentences, vector_size=100, window=2, min_count=1)

# 词相似度
print(model.wv.similarity('dog', 'quick'))  # 输出 相似度分数

# 找相似词
print(model.wv.most_similar('dog'))  # 输出 [('cat', 0.8), ...]

# 获取词向量
vec = model.wv['dog']  # 100 维向量
```

### 案例 2：词向量的几何性质

Word2Vec 学到的向量空间有惊人的几何性质：
$$\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}$$

应用：
```python
# 类比任务
model.wv.most_similar(positive=['king', 'woman'], negative=['man'])
# 结果：queen, princess, ...
```

### 案例 3：在文本分类中应用词向量

```python
# 传统 TF-IDF: 1000 维稀疏向量
# Word2Vec: 100 维稠密向量，包含语义信息

# 文本表示：词向量的平均
def get_sentence_vec(words, model):
    return np.mean([model.wv[w] for w in words], axis=0)

# 用作分类特征
features = [get_sentence_vec(text.split(), model) for text in texts]
clf.fit(features, labels)
```

## 常见问题

**Q: Word2Vec 的词向量是静态的，如何处理多义词？**
A: "bank"（河岸 vs 银行）在 Word2Vec 中只有一个向量。BERT 等预训练模型使用动态向量（根据上下文），解决了多义问题。

**Q: 词嵌入维度多少合适？**
A: 典型范围 50-300。更大维度捕捉更多信息但需更多数据和计算。通常 100 维在精度-速度间达到平衡。

**Q: Word2Vec 需要多大的语料库？**
A: 至少数百万词。通常用中文 10 亿+ 词、英文 Google News 100 亿词训练。小语料库可用预训练向量。

**Q: 为什么 BERT 比 Word2Vec 好？**
A: BERT 使用双向 Transformer，捕捉深层上下文和语法。Word2Vec 是浅层（只有嵌入层），信息容量有限。

**Q: OOV（未见词）如何处理？**
A: Word2Vec 无法生成新词。fastText 使用子词（char n-gram），可为 OOV 词生成近似向量。

## 代表来源

- [[2023-05-10-word2vec]]：本地笔记，原理分析、CBOW/Skip-gram、优化策略
- [[2026-04-06-nlp-word2vec-visualization]]：Word2Vec 图解教程
- [[2022-04-05-nlp-gensim]]：Gensim 工具实现
- [[2026-04-06-nlp-sense2vec]]：上下文词向量库

## 相关概念

- [[特征提取]]：Word2Vec 前的特征表示方法
- [[词嵌入]]：通用概念，Word2Vec 是一种实现
- [[Embedding]]：神经网络中的词嵌入
- [[自注意力机制]]：后继的表示学习方法

---

*最后更新：2026-04-15*
