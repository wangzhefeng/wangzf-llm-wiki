---
created_at: 2026-04-06
topics:
  - 计算机视觉
  - 多模态
related_concepts:
  - 视觉语言模型
  - 图像文本对齐
  - CLIP
status: inbox
---

# 视觉语言模型 (VLM)

## 定义

视觉语言模型（Vision-Language Model, VLM）是同时处理视觉和文本模态的多模态模型，能够理解和生成跨模态的内容。

## 核心架构

### 典型 VLM 结构

```
图像 → ViT/图像编码器 → 视觉特征
                              ↓
文本 → 文本编码器 → 文本特征 → 跨模态融合 → 输出
```

### 图像编码器
- **ViT/Vision Transformer**: 标准视觉 Transformer
- **CLIP**: 对比语言-图像预训练
- **InternViT**: 内部视觉 Transformer
- **SigLIP**: Sigmoid Loss for Image-Text Pre-training

### 跨模态融合
- **早期融合**: 直接拼接视觉和文本特征
- **晚期融合**: 分别处理后融合
- **交叉注意力**: 使用交叉注意力机制实现模态交互

## 关键方法

### CLIP（Contrastive Language-Image Pre-training）
- **目标**: 学习图像-文本联合表示
- **方法**: 对比学习，拉近匹配的图像-文本对，推开不匹配的
- **应用**: 零样本分类、图像检索、文本生成图像

### VLM 训练流程
1. **图像编码**: ViT 提取视觉特征
2. **文本编码**: Transformer 编码文本
3. **跨模态对齐**: 拉近匹配的图像-文本表示
4. **任务微调**: 下游任务适配

## 应用方向

- **视觉问答（VQA）**: 回答关于图像的问题
- **图像描述**: 生成图像的自然语言描述
- **视觉推理**: 基于图像进行逻辑推理
- **图像检索**: 根据文本查询搜索图像
- **零样本分类**: 无需训练即可分类新类别

## 评测基准

- **CVBench**: 视觉能力评测
- **VLMEvalKit**: 220+ LMM，80+ 基准

## 小型 VLM

- **SmolVLM**: 小型但强大的视觉语言模型，适合资源受限场景

## 学习路径

- **[[2026-04-06-SkalskiPvlms-zero-to-hero This series will take you on a journey from the fundamentals of NLP and Computer Vision to the cutting edge of Vision-Language Models]]** — 从零到英雄系列（NLP + CV 基础到前沿 VLM）

## 相关来源

- [[计算机视觉专题来源]]
- [[2026-04-06-SmolVLM - small yet mighty Vision Language Model]]
- [[2026-04-06-Understanding Multimodal LLMs]]
- [[2026-04-06-open-compassVLMEvalKit Open-source evaluation toolkit of large multi-modality models (LMMs), support 220+ LMMs, 80+ benchmarks]]
- [[2026-04-06-SkalskiPvlms-zero-to-hero This series will take you on a journey from the fundamentals of NLP and Computer Vision to the cutting edge of Vision-Language Models]]

## 相关概念

- [[VisionTransformerViT]]
- [[CLIP]]
- [[多模态 LLM]]
- [[图像分类]]
