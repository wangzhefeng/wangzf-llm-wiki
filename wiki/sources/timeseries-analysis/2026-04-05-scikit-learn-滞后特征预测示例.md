---
source_type: web
source_url: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html
source_path: raw/web/timeseries-analysis/2026-04-05-scikit-learn-lagged-features.md
created_at: 2026-04-05
topics:
- machine-learning
- timeseries-analysis
related_concepts:
- 机器学习时间序列预测
- 预测特征工程
- 预测模型评估
status: summarized
---
# scikit-learn 滞后特征预测示例来源摘要


- 原文：[[raw/web/timeseries-analysis/2026-04-05-scikit-learn-lagged-features.md]]
## 材料定位

这是一篇官方示例页，重点不在“介绍某个单一模型”，而在演示如何把时间序列通过滞后特征转成表格监督学习问题，并用正确的时间序列验证方式评估机器学习预测模型。

## 核心结论

- 滞后特征是把时间序列接入通用机器学习回归器的关键桥梁。
- 对这类表格化时序预测，随机 `train_test_split` 会给出过于乐观的评估结果。
- `TimeSeriesSplit`、`gap`、固定训练窗口和测试窗口，是时间序列回测设计的重要控制杆。
- `HistGradientBoostingRegressor` 这类通用回归模型可以胜任单步时序预测，但前提是特征构造和验证流程正确。
- 预测任务不应只给点预测，还可以用分位数回归输出 5%、50%、95% 预测，表达不确定性区间。

## 对知识库的价值

- 它补上了当前时间序列专题里“官方工具示例”这一类来源。
- 它把 [[预测特征工程]] 与 [[预测模型评估]] 两个概念非常直接地连到了一起。
- 它也是 [[机器学习时间序列预测]] 的一个典型落地案例，说明通用 ML 框架进入时序预测时最容易犯错的地方不是模型，而是切分方式。

## 与现有概念的连接

- [[机器学习时间序列预测]]
- [[预测特征工程]]
- [[预测模型评估]]

## related_sources

- [[2022-09-13-时间序列特征工程]]
- [[2023-03-03-时间序列模型评估]]
- [[2024-09-10-机器学习预测方式]]
- [[2024-09-09-机器学习预测模型应用-DEMO]]

## 局限与注意点

- 这篇页面主要展示单步预测，不覆盖多步递归或多步直接预测的完整工程处理。
- 它使用的是官方教学示例数据，更适合作为方法规范和工作流参考，而不是业务效果上限参考。
- 页面提到 `MAPIE` 和 `sktime` 可以进一步扩展不确定性和递归预测，但没有在本例中展开。

## missing_context

- 还没有把“滞后特征 + 通用回归器”与现有库中的多步预测策略系统对齐。
- 还可以补充它与 `tsproj_ml` 这类工程化机器学习预测仓库之间的映射关系。

## related_outputs

- [[2026-04-05-scikit-learn-滞后特征预测示例]]
