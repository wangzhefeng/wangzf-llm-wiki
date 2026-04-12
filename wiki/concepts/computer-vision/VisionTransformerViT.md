---
created_at: 2026-04-06
topics:
- computer-vision
related_concepts:
- Transformer
- 自注意力
- 图像分类
status: inbox
---
# Vision Transformer (ViT)

## 定义

Vision Transformer（ViT）是将 Transformer 架构应用于图像分类任务的方法，由 Dosovitskiy 等人于 2020 年提出。

## 核心思想

将图像切分为固定大小的图像块（patches），将其视为序列输入，使用标准 Transformer 编码器进行处理。

## 架构流程

1. **图像切分**: 将图像 $x \in \mathbb{R}^{H \times W \times C}$ 切分为 $N$ 个固定大小的 patches
2. **线性嵌入**: 每个 patch 展平并投影到 $D$ 维向量
3. **位置编码**: 添加可学习的位置嵌入
4. **Class Token**: 添加特殊的分类 token
5. **Transformer 编码器**: 多层自注意力 + MLP
6. **分类头**: 提取 class token 输出，通过 MLP 分类

## 与 CNN 的对比

| 特性 | CNN | ViT |
|------|-----|-----|
| 感受野 | 局部（卷积核） | 全局（自注意力） |
| 归纳偏置 | 强（平移等变性） | 弱 |
| 数据需求 | 中等 | 大量（预训练） |
| 长距离依赖 | 需要深层堆叠 | 直接建模 |
| 推理速度 | 快 | 较慢（注意力复杂度 $O(N^2)$） |

## 关键优势

- **全局建模**: 自注意力机制直接捕获全局长距离依赖
- **可扩展性**: 在大数据集上性能持续扩展
- **统一架构**: 与 NLP Transformer 统一，便于多模态融合

## 变体

- **Swin Transformer**: 滑动窗口，层次特征
- **DeiT**: 数据高效训练
- **InternViT**: 内部视觉 Transformer
- **SigLIP**: Sigmoid Loss for Image-Text Pre-training

## 在多模态 LLM 中的应用

ViT 作为图像编码器广泛应用于多模态 LLM：
- **CLIP**: 图像-文本对比学习
- **InternViT/ SigLIP**: 多模态 LLM 的视觉编码器
- **VLMEvalKit**: 多模态评测基准

## 相关来源

- [[计算机视觉专题来源]]
- [[2026-04-06-Vision Transformers (ViTs) Computer Vision with Transformer Models]]
- [[2026-04-06-Understanding Multimodal LLMs]]
- [[2026-04-06-open-compassVLMEvalKit Open-source evaluation toolkit of large multi-modality models (LMMs), support 220+ LMMs, 80+ benchmarks]]

## 相关概念

- [[Transformer架构]]
- [[注意力机制]]
- [[卷积神经网络CNN]]
- [[视觉语言模型VLM]]
- [[CLIP]]
