---
source_type: repo
source_url: https://github.com/wangzhefeng/tsproj_ml
created_at: 2026-04-05
topics:
  - 时间序列预测
  - machine-learning-forecasting
related_concepts:
  - 机器学习时间序列预测
  - 预测特征工程
  - 机器学习时间序列多步预测策略
status: inbox
---

# tsproj_ml 仓库入口笔记

## 仓库信息

- 仓库名：`tsproj_ml`
- 仓库地址：https://github.com/wangzhefeng/tsproj_ml
- README 入口：https://github.com/wangzhefeng/tsproj_ml/blob/main/README.md
- 主要用途：围绕机器学习模型构建时间序列预测的训练、测试、预测闭环，并系统比较多种多步预测策略。
- 当前首轮依据：主要基于 README 中已经公开整理好的方法体系、特征设计、实现 checklist 和推荐策略。

## 仓库要解决的问题

- 如何把机器学习模型系统化地用于时间序列预测，而不是只写一个零散 demo。
- 如何在单变量/多变量、直接/递归/混合多步预测之间做清晰的方法选择。
- 如何把特征工程、模型训练、测试验证和预测输出组织成可复用流程。

## 关键入口

- 仓库总入口：`README.md`
- README 中明确提到的关键模块角色：
  - `ModelConfig`
  - `FeaturePreprocessor`
  - `Model`
- README 中明确提到的关键实现点：
  - 多步预测策略对比
  - 多变量滞后特征构造
  - 训练/测试/预测完整闭环
  - 方法选择决策树
  - 实现 checklist

## 关键目录与素材

- `README.md`
  当前最重要的知识入口，已经浓缩了方法分类和工程结构。
- `docs/raw/assets/ts_stationary.png`
  README 中已引用平稳性相关示意图。

## 训练、测试、预测涉及的知识单元

- 训练前：
  - 时间特征
  - 滞后特征
  - 外生变量
  - 多变量输入组织
- 训练阶段：
  - 单步/多步目标构造
  - `MultiOutputRegressor` 风格的多输出训练
  - 不同预测策略对应的训练差异
- 测试阶段：
  - 预测精度、训练速度、预测速度、数据需求的经验对比
- 预测阶段：
  - 直接预测
  - 递归预测
  - 分块递归预测

## 建议拆分的知识单元

1. 方法策略体系
   - 7 种机器学习时间序列预测方式
   - 单变量/多变量
   - 直接/递归/混合
2. 特征工程与输入组织
   - 目标变量滞后
   - 多变量滞后
   - 外生变量
   - 时间特征
3. 训练、测试与预测闭环
   - 训练接口
   - 测试验证
   - 预测输出
   - 实现 checklist

### knowledge-unit-prediction-strategy-system

- 对应来源卡：`tsproj_ml 预测策略体系来源摘要`
- 追溯范围：README 中关于 `USMDO`、`USMD`、`USMR`、`USMDR`、`MSMD`、`MSMR`、`MSMDR` 的方法分类与决策树说明

### knowledge-unit-feature-engineering-and-input-design

- 对应来源卡：`tsproj_ml 特征工程与输入组织来源摘要`
- 追溯范围：README 中关于时间特征、目标变量滞后、多变量滞后、外生变量与输入组织的说明

### knowledge-unit-train-test-predict-loop

- 对应来源卡：`tsproj_ml 训练测试预测闭环来源摘要`
- 追溯范围：README 中关于数据加载、特征工程、模型训练、测试验证、预测输出与实现 checklist 的说明

## 首轮判断

- 这个仓库内容明显不适合只建 1 张总来源卡。
- 首轮应先按 3 个稳定知识单元落到 `wiki/sources/timeseries/`。
- 第二轮如果继续深入，再补源码级文件映射、真实训练脚本路径和更细的模块级来源卡。
