---
created_at: 2026-04-06
topics:
  - 计算机视觉
related_concepts:
  - 卷积
  - 池化
  - 特征图
status: inbox
---

# 卷积神经网络 (CNN)

## 定义

卷积神经网络（Convolutional Neural Network, CNN）是一类专门处理网格状数据（如图像）的深度学习架构。

## 核心组件

### 1. 卷积层（Convolution）
- 使用卷积核在图像上滑动提取特征
- **局部连接**: 每个神经元只连接局部区域
- **权重共享**: 同一卷积核在不同位置使用相同权重
- **平移等变性**: 目标移动时特征图相应移动

### 2. 池化层（Pooling）
- **最大池化**: 取区域最大值，保留显著特征
- **平均池化**: 取区域平均值，平滑特征
- 作用：降维、减少参数、增强鲁棒性

### 3. 激活函数
- **ReLU**: $f(x) = \max(0, x)$，最常用
- **Leaky ReLU**: 解决 Dying ReLU 问题
- **GELU**: Transformer 中常用

### 4. 全连接层
- 整合全局特征，输出分类或其他任务结果

## 经典架构

| 架构 | 年份 | 关键创新 |
|------|------|----------|
| LeNet | 1998 | 第一个 CNN，手写数字识别 |
| AlexNet | 2012 | ReLU、Dropout、数据增强，ImageNet 突破 |
| VGG | 2014 | 小卷积核（3×3）、深网络 |
| GoogLeNet/Inception | 2014 | Inception 模块，多尺度卷积 |
| ResNet | 2015 | 残差连接，解决退化问题 |
| EfficientNet | 2019 | 复合缩放，效率优化 |
| MobileNet | 2017 | 深度可分离卷积，移动端友好 |

## 与 Vision Transformer 的对比

| 特性 | CNN | ViT |
|------|-----|-----|
| 感受野 | 局部 → 全局（逐层） | 全局（单层） |
| 归纳偏置 | 强（平移等变、局部性） | 弱 |
| 数据效率 | 高 | 低（需大量预训练） |
| 计算复杂度 | $O(N)$ | $O(N^2)$ |
| 部署友好性 | 高 | 中等 |

## 应用场景

- **图像分类**: ResNet、EfficientNet
- **目标检测**: YOLO、Faster R-CNN
- **图像分割**: U-Net、DeepLab
- **图像生成**: DCGAN、StyleGAN

## 可视化工具

- [[2026-04-06-cbovarConvNetDraw Draw multi-layer neural network in your browser]] — ConvNetDraw 浏览器可视化
- [[2026-04-06-Articles (cn-zh)]] — CNN 直观解释

## 相关来源

- [[计算机视觉专题来源]]
- [[2026-04-06-jimgoocaffe-oxford102 Caffe CNNs for the Oxford 102 flower dataset]]
- [[2026-04-06-Articles (cn-zh)]]
- [[2026-04-06-cbovarConvNetDraw Draw multi-layer neural network in your browser]]
- [[2026-04-06-nn4nlp-conceptsconcepts.md at master]]

## 相关概念

- [[YOLO目标检测]]
- [[VisionTransformerViT]]
- [[图像分割]]
- [[ResNet]]
