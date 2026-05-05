---
created_at: 2026-04-06
topics:
- llm
related_concepts:
- 预训练
- 自注意力
- 解码
status: inbox
---
# Transformer 架构

## 定义

Transformer 是一种基于自注意力机制的序列建模架构，由 Vaswani 等人在 2017 年提出，是当前大语言模型（LLM）的核心架构。

## 核心组件

### 1. 自注意力机制（Self-Attention）

$$\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$$

- **Q (Query)**: 查询向量
- **K (Key)**: 键向量
- **V (Value)**: 值向量
- **$d_k$**: 缩放因子，防止点积过大

### 2. 多头注意力（Multi-Head Attention）

将 Q/K/V 分成多个头，分别计算注意力后拼接：

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O$$

### 3. 位置编码（Positional Encoding）

Transformer 本身不含有序信息，需添加位置编码：

- **绝对位置编码**: 原始 Transformer 使用正弦/余弦函数
- **RoPE (Rotary Position Embedding)**: 主流 LLM 采用，旋转位置编码
- **ALiBi**: 线性偏置，外推性更好

### 4. 前馈网络（FFN）

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

### 5. 残差连接与层归一化

$$\text{LayerNorm}(x + \text{Sublayer}(x))$$

## 两类 Transformer

| 类型 | 代表模型 | 注意力方式 | 任务 |
|------|----------|-----------|------|
| **Encoder-only** | BERT | 双向自注意力 | 理解任务（分类、NER） |
| **Decoder-only** | GPT 系列 | 因果自注意力（掩码） | 生成任务（文本生成） |
| **Encoder-Decoder** | T5、BART | 编码-解码交叉注意力 | 序列到序列（翻译、摘要） |

## 现代 LLM 架构演进

当前主流 LLM（GPT-4、LLaMA、DeepSeek 等）均基于 **Decoder-only** 架构，关键改进：

- **RoPE 位置编码**: 取代绝对位置编码
- **SwiGLU 激活**: 取代 ReLU
- **RMSNorm**: 取代 LayerNorm
- **Grouped-Query Attention (GQA)**: 减少 KV Cache 内存

## 相关来源

- [[大语言模型专题来源]]
- [[2026-04-06-译-Transformer-是如何工作的：600-行-Python-代码实现-self-attention-和两类-Transformer（2019）]]
- [[2026-04-06-The-Big-LLM-Architecture-Comparison]]
- [[2026-04-06-Articles-(cn-zh)]]

## 相关概念

- [[RoPE旋转位置编码]]
- [[预训练]]
- [[注意力机制]]
- [[KV-Cache]]
