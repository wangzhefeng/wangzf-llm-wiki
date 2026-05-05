---
created_at: 2026-04-06
topics:
- deep-learning
- llm
related_concepts:
- 位置编码
- 注意力机制
status: inbox
---
# RoPE（Rotary Position Embedding）

## 定义

旋转位置编码（Rotary Position Embedding），一种用于 Transformer 的位置编码方法，已被主流 LLM 采用。

## 核心思想

RoPE 通过旋转矩阵将位置信息注入到注意力计算中，具有以下特点：

- **相对位置感知**: 自动捕获 token 间的相对位置关系
- **外推性好**: 可以处理比训练时更长的序列
- **计算高效**: 可以与 QK 矩阵乘法自然结合

## 数学表达

对于位置 $m$ 和维度 $d$，RoPE 定义为旋转操作：

$$f_q(x_m, m) = W_q x_m \cdot e^{im\theta_d}$$

其中 $\theta_d$ 是频率参数。

## 为什么主流 LLM 都用 RoPE？

### 优势

1. **更好的长度外推**: 相比绝对位置编码，RoPE 在推理时可以处理更长序列
2. **相对位置编码**: 自然捕获 token 间的相对距离
3. **与注意力兼容**: 可以高效集成到标准注意力计算中
4. **经验上稳定有效**: 在多种任务上表现优异

### 采用 RoPE 的模型

- Llama 系列
- DeepSeek 系列
- 大多数现代开源 LLM

## 实现要点

```python
# 简化示例
import torch

def apply_rotary_pos_emb(q, k, cos, sin):
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed
```

## 相关来源

- [[2026-04-06-为什么主流LLM都用RoPE？]]
- [[LLM架构训练与微调专题来源]]

## 相关概念

- [[Transformer架构]]
- [[位置编码]]
- [[注意力机制]]
- [[KV-Cache]]
