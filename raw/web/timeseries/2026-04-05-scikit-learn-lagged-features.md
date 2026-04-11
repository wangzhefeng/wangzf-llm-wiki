---
created_at: 2026-04-05
related_concepts:
- 机器学习时间序列预测
- 预测特征工程
- 预测模型评估
source_type: web
source_url: https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html
status: inbox
topics:
- 时间序列预测
- machine-learning-forecasting
- 时间序列published_at: null
author: null
title: null
---

# scikit-learn 时间序列滞后特征示例

## 页面信息

- 标题：Lagged features for time series forecasting
- 作者/机构：The scikit-learn developers
- 页面版本：scikit-learn 1.8.0 documentation
- 来源链接：https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html
- 为什么值得收进知识库：这是一篇质量很高的官方示例，比较完整地串起了“滞后特征表格化 -> 机器学习回归 -> 时间序列正确验证 -> 分位数回归不确定性”这条实践链路。

## 页面主旨

这篇页面展示了如何把时间序列通过滞后特征转成表格监督学习问题，并用 `HistGradientBoostingRegressor` 做下一时刻预测。它的真正价值不只是“用 scikit-learn 做预测”，而是明确说明了随机切分会导致过于乐观的评估结果，时间序列任务必须使用保序的验证策略。页面最后还用分位数回归给出 5%、50%、95% 预测，补上了机器学习预测中常被忽略的不确定性表达。

## 关键知识点

### 1. 方法层

- 时间序列可以通过滞后特征、滚动统计等方式表格化，再交给通用回归模型处理。
- 页面示例使用 Polars 构造滞后特征，再用 `HistGradientBoostingRegressor` 做回归预测。
- 损失函数并不只有默认平方误差，还比较了 `squared_error`、`poisson`、`absolute_error` 和 `quantile`。

### 2. 评估层

- 页面先演示了随机 `train_test_split`，得到的 MAPE 约为 `0.389`。
- 随后改用 `TimeSeriesSplit`，并显式设置 `gap=48`、`max_train_size=10000`、`test_size=3000`，首个时间切分的 MAPE 约为 `0.443`。
- 进一步做时间序列交叉验证后，页面给出 `CV MAPE: 0.363 ± 0.068`，说明不同时间切分上的波动并不小。
- 这篇示例最重要的判断是：随机打乱切分会让时间序列机器学习评估过于乐观。

### 3. 工程层

- `gap` 的设置本质上是在控制训练集和测试集之间的时间隔离，降低泄漏风险。
- `max_train_size` 与 `test_size` 体现了时间序列回测里对训练窗口、测试窗口和计算成本的折中。
- 页面还演示了如何把多种评估指标一起纳入交叉验证，包括 `MAPE`、`RMSE`、`MAE` 和不同分位数的 pinball loss。

### 4. 不确定性层

- 页面使用 `loss="quantile"` 训练 0.05、0.5、0.95 三个分位数模型。
- 通过 5% 到 95% 分位数区间，可以看到不同时间段预测不确定性宽度不同。
- 页面指出白天区间更宽、夜间更窄，这种变化反映了需求本身的波动性。

### 5. 适用边界

- 适用于：单步预测、表格化机器学习预测、需要把时间序列接入通用 ML 工具链的场景。
- 不适用于：直接覆盖多步递归预测、复杂序列到序列建模、端到端深度时序建模。
- 页面示例主要基于单个数据集，更多是方法演示而不是完整业务方案。

## 关键图表或示例

- 图表重点：随机切分与时间切分下的误差差异、5%-95% 分位数预测区间。
- 当前处理：本轮先不复制图片到本地，先沉淀方法和评估逻辑。
- 原因：这篇页面的核心增量主要是方法链路与评估规范，暂不依赖图片才能理解。

## 待沉淀方向

- 应写入来源卡：`wiki/sources/timeseries/2026-04-05-scikit-learn-滞后特征预测示例.md`
- 应更新概念页：
  - `[[机器学习时间序列预测]]`
  - `[[预测特征工程]]`
  - `[[预测模型评估]]`
- 应更新索引页：
  - `[[时间序列预测总索引]]`
  - `[[时间序列预测来源清单]]`
  - `[[时间序列预测阅读地图]]`
- 是否值得进入 `outputs/`：值得，后续可以单独写一篇“scikit-learn 机器学习时间序列预测实践解读”。
