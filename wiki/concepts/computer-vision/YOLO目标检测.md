---
created_at: 2026-04-06
topics:
- computer-vision
related_concepts:
- 目标检测
- 实时检测
- 单阶段检测
status: inbox
---
# YOLO 目标检测

## 定义

YOLO（You Only Look Once）是一系列实时目标检测算法，以速度快、精度高著称。由 Joseph Redmon 于 2016 年首次提出。

## 核心思想

将目标检测任务转化为单次前向传播的回归问题，不需要区域提议（region proposal）阶段。

## 版本演进

| 版本 | 年份 | 作者 | 关键创新 |
|------|------|------|----------|
| YOLOv1 | 2016 | Joseph Redmon | 首次提出单阶段检测框架，45 FPS 实时检测 |
| YOLOv2/YOLO9000 | 2017 | Joseph Redmon | 多尺度预测、锚框机制、联合训练 |
| YOLOv3 | 2018 | Joseph Redmon | 多尺度特征融合（FPN 思想） |
| YOLOv4 | 2020 | Alexey Bochkovskiy | Bag of Freebies / Bag of Specials |
| YOLOv5 | 2020 | Ultralytics | 易用性、部署友好 |
| YOLOv9 | 2024 | Chien-Yao Wang 等 | PGI 可编程梯度信息、辅助反向传播 |

## 关键机制

### 锚框（Anchor Boxes）
预定义的边界框形状，用于预测目标位置和大小。

### 非极大值抑制（NMS）
去除重复检测框，保留最优结果。

### 多尺度预测
在不同特征层预测不同大小的目标，提升小目标检测能力。

### 单阶段 vs 两阶段

| 特性 | 单阶段（YOLO/SSD） | 两阶段（Faster R-CNN） |
|------|-------------------|----------------------|
| 速度 | 快 | 慢 |
| 精度 | 中高 | 高 |
| 适用场景 | 实时检测 | 高精度检测 |

## 相关来源

- [[计算机视觉专题来源]]
- [[2026-04-06-YOLOv9 终于来了！]]
- [[2026-04-06-YOLOv4：使用 Darknet 和 OpenCV 进行对象检测的综合指南]]
- [[raw/web/computer-vision/2026-04-06-使用YOLOv5模型进行目标检测！]]
- [[2026-04-06-Joseph Redmon - Survival Strategies for the Robot Rebellion]]
- [[2026-04-06-Welcome to MMDetection’s documentation! — MMDetection 3.3.0 documentation]]

## 相关概念

- [[目标检测]]
- [[VisionTransformerViT]]
- [[卷积神经网络CNN]]
- [[多目标跟踪 (MOT)]]
- [[MMDetection]]
