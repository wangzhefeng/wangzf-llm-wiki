---
title: FeatureSelector 特征选择工具
created: 2026-04-06
updated: 2026-04-15
type: source
tags:
  - feature-engineering
  - 特征工程
  - 特征选择
  - 工具
sources:
  - raw/web/feature-engineering/2026-04-06-Github项目推荐-(Python)用FeatureSelector高效特征选择工具构建机器学习工作流.md
related_sources:
  - Will Koehrsen
  - GitHub/WillKoehrsen/feature-selector
---

## 摘要

FeatureSelector 是一个 Python 库，用于自动化的特征选择和降维。该工具实现了 5 大特征选择方法，可以快速识别并移除对模型预测无贡献的特征，包含可视化工具，支持与 scikit-learn、LightGBM 等主流库的集成。

## 核心内容

### 五大特征选择方法

1. **缺失值特征过滤**
   - 识别缺失值比例超过阈值的特征
   - 移除信息不足的特征

2. **单值特征过滤**
   - 检测几乎所有样本都是同一值的特征
   - 无预测力

3. **共线特征识别**
   - 计算特征间的相关性
   - 移除高度相关的冗余特征

4. **零重要性特征**
   - 基于 LightGBM 或树模型的特征重要性
   - 移除在模型中无用的特征

5. **低重要性特征**
   - 设置重要性阈值
   - 移除低于阈值的特征

### 主要功能

- **自动化特征评估**：批量执行多种选择方法
- **可视化工具**
  - 相关性热力图
  - 特征重要性柱状图
  - 缺失值分布图
  
- **灵活的特征移除**
  - 交互式选择移除哪些特征
  - 支持自定义阈值

### 使用流程
1. 初始化 FeatureSelector 对象
2. 执行特征评估方法
3. 查看和可视化结果
4. 移除不需要的特征
5. 获取清理后的数据集

### 依赖和集成
- **主要依赖**：pandas、scikit-learn、LightGBM
- **兼容模型**：LightGBM、XGBoost、Catboost 等树模型
- **输出**：降维后的特征子集和转换后的数据

## 关键特点

- 减少模型训练时间
- 提高模型可解释性
- 自动化特征工程工作流
- 开源且持续维护

## 相关资源

- **GitHub 项目**：https://github.com/WillKoehrsen/feature-selector
- [[特征选择|特征选择概念页]]
- [[wiki/indexes/feature-engineering/特征工程总索引|特征工程总索引]]
- [[2022-09-13-特征构建|特征构建]]
