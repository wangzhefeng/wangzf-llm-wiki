---
marp: true
theme: default
paginate: true
size: 16:9
footer: "wangzf-llm-wiki · 2026-04-05"
style: |
  section {
    background: linear-gradient(180deg, #fffdf8 0%, #f8fafc 100%);
    color: #0f172a;
    font-family: "Helvetica Neue", Arial, sans-serif;
    padding: 52px 64px;
    font-size: 28px;
  }
  h1 {
    color: #0f172a;
    font-size: 1.65em;
    margin-bottom: 0.3em;
  }
  h2 {
    color: #0f172a;
    font-size: 1.2em;
    margin-bottom: 0.35em;
  }
  p, li {
    line-height: 1.45;
  }
  strong {
    color: #b45309;
  }
  code {
    background: #eff6ff;
    color: #1d4ed8;
    padding: 0.1em 0.28em;
    border-radius: 0.2em;
  }
  .lead {
    background: radial-gradient(circle at top right, #dbeafe 0%, #fffdf8 42%, #f8fafc 100%);
  }
  .compact {
    font-size: 24px;
  }
---

<!-- _class: lead -->

# scikit-learn 机器学习时间序列预测实践解读

把官方示例读成一条可复用的机器学习时序工作流

- 基于 [`2026-04-05-scikit-learn-机器学习时间序列预测实践解读.md`](../answers/2026-04-05-scikit-learn-机器学习时间序列预测实践解读.md)
- 目标：提炼方法，而不是复述 API

---

## 这篇示例真正讲了什么

![bg right:42% contain](../figures/2026-04-05-scikit-learn-机器学习时间序列预测实践解读/workflow.svg)

- **序列先被转成监督学习表格**
- **再用通用回归模型训练预测器**
- **评估必须保留时间顺序**
- **最后用分位数回归表达不确定性**

一句话总结：

**机器学习能做时间序列预测，但前提是你必须主动编码时间结构。**

---

## 启示 1：滞后特征是桥，不是细节

![bg right:42% contain](../figures/2026-04-05-scikit-learn-机器学习时间序列预测实践解读/workflow.svg)

- 不做 lag feature，模型几乎看不到时间依赖
- 把“序列问题”改写成“过去预测未来”的监督学习问题
- 实际上决定上限的，常常是：
  - 滞后项
  - 滚动统计
  - 日历特征
  - 协变量设计

---

## 启示 2：随机切分会高估效果

![bg right:44% contain](../figures/2026-04-05-scikit-learn-机器学习时间序列预测实践解读/split-comparison.svg)

- 随机 `train_test_split` 会让结果偏乐观
- 原因不是 API 问题，而是 **时间泄漏**
- 示例里随机切分的 `MAPE ≈ 0.389`
- 改为 `TimeSeriesSplit` 后，首个时间切分 `MAPE ≈ 0.443`

结论：

**一旦你把时序问题表格化，验证阶段就必须重新尊重时间顺序。**

---

## 启示 3：评估设计本身就是模型设计

<!-- _class: compact -->

- `gap=48`：减少潜在泄漏
- `max_train_size=10000`：定义历史记忆范围
- `test_size=3000`：控制稳定性与计算成本

这不是“换一个 split API”而已，而是在定义更接近真实部署条件的回测实验。

可以把它理解成 3 个问题：

1. 模型能看到多长历史？
2. 训练与测试之间要不要留缓冲区？
3. 你想用多长的未来窗口来评价它？

---

## 启示 4：点预测不够，最好给区间

![bg right:44% contain](../figures/2026-04-05-scikit-learn-机器学习时间序列预测实践解读/uncertainty-band.svg)

- 用 `loss="quantile"` 训练 5%、50%、95% 分位数模型
- 预测从“一个值”升级成“一个区间”
- 高波动时段区间更宽，低波动时段区间更窄

对业务更有价值的是：

- 容量规划
- 库存配置
- 风险预留

---

## 这篇示例在知识库里的位置

- 连接 [[机器学习时间序列预测]]
- 连接 [[预测特征工程]]
- 连接 [[预测模型评估]]

它的价值不在于“最强模型”，而在于：

**把特征工程、时间切分和不确定性表达串成一条完整工作流。**

---

## 对后续建模的直接检查项

1. 是否明确包含滞后项、窗口统计和时间索引特征
2. 训练/验证切分是否仍混入随机打乱
3. 是否需要显式设置 `gap`
4. 报告是否只有点预测，没有区间预测
5. 是否同时报告 `MAPE`、`MAE`、`RMSE` 与 pinball loss

如果这 5 项里还有 2-3 项没做，流程通常还不算真正规范。

---

## 结论

- 这篇示例最值得复用的不是某个具体模型
- 而是一条 **规范的机器学习时间序列预测工作流**
- 真正的重点依次是：
  - 特征构造
  - 时间保序评估
  - 不确定性表达

下一步可以继续补：

- 单步监督学习预测 vs 多步预测策略
- 时间切分设计的专项方法笔记
