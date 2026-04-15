# Conformal Prediction（保形预测）

## 概述

Conformal Prediction 是一种**无分布假设（distribution-free）的不确定性量化框架**，能够为任意机器学习模型的预测结果附上**统计上有保证的置信区间或预测集合**。其核心优势在于：无需对数据分布做任何假设，且置信保证是严格有效的（valid）。

---

## 核心思想

传统机器学习模型输出的是点预测（point prediction），例如"这张图片是猫"或"明天气温为 22°C"。然而在实际应用中，我们更想知道：

> *这个预测有多可靠？我们能以多大的把握相信它？*

Conformal Prediction 通过构造**预测集合（Prediction Set）** 来回答这个问题：

- **回归任务**：输出一个区间，例如 `[18°C, 26°C]`，保证真实值以 90% 的概率落在其中。
- **分类任务**：输出一个标签集合，例如 `{猫, 狗}`，保证真实标签以 90% 的概率在集合中。

---

## 理论基础

### 可交换性假设（Exchangeability）

Conformal Prediction 的唯一核心假设是：**训练数据与测试数据是可交换的（exchangeable）**。这比 i.i.d.（独立同分布）假设更弱，更贴近实际。

### 非一致性分数（Nonconformity Score）

每个样本的"异常程度"由一个**非一致性分数函数** $s(x, y)$ 衡量，分数越高说明该样本与训练分布越不一致。常见定义：

- **回归**：$s_i = |y_i - \hat{y}_i|$（残差的绝对值）
- **分类**：$s_i = 1 - \hat{p}(y_i | x_i)$（真实类别的预测概率的补）

### 预测集合的构造

给定用户指定的错误率 $\alpha$（例如 $\alpha = 0.1$ 表示 90% 置信度）：

1. 在**校准集（Calibration Set）**上计算每个样本的非一致性分数 $s_1, s_2, \ldots, s_n$。
2. 计算第 $\lceil (1-\alpha)(1 + 1/n) \rceil$ 个分位数，记为 $\hat{q}$。
3. 对于新样本 $x_{\text{test}}$，预测集合为：

$$C(x_{\text{test}}) = \{ y : s(x_{\text{test}}, y) \leq \hat{q} \}$$

### 边际覆盖保证（Marginal Coverage Guarantee）

**定理**：对于任意模型和数据分布，只要可交换性成立，以下保证严格成立：

$$P(Y_{\text{test}} \in C(X_{\text{test}})) \geq 1 - \alpha$$

这是一个**有限样本**（finite-sample）保证，无需任何渐近近似。

---

## 主要变体

| 变体 | 特点 |
|---|---|
| **Split Conformal** | 将数据分为训练集和校准集，简单高效，最常用 |
| **Full Conformal** | 利用所有数据，计算成本高，理论最优 |
| **Cross-Conformal** | 类似交叉验证，平衡效率与数据利用率 |
| **Mondrian Conformal** | 按类别条件化，实现类别级别的覆盖保证 |
| **Conformalized Quantile Regression (CQR)** | 结合分位数回归，生成自适应区间宽度 |
| **RAPS / APS** | 改进分类任务的预测集合效率 |

---

## 效率（Efficiency）vs. 有效性（Validity）

Conformal Prediction 在**有效性**上是理论保证的，但**效率**（即预测集合的大小）取决于底层模型的质量：

- 底层模型越强，非一致性分数越集中，预测集合越小越精确。
- 差的模型仍能保证覆盖率，但预测集合可能很大（例如包含所有类别）。

> 这体现了 Conformal Prediction 的一个重要性质：**它不会让坏模型变好，但会诚实地告诉你模型有多不确定。**

---

## 与贝叶斯方法的对比

| 维度 | Conformal Prediction | 贝叶斯方法 |
|---|---|---|
| 分布假设 | 无（仅需可交换性） | 需要先验分布 |
| 覆盖保证 | 严格有效（finite-sample） | 依赖模型假设正确性 |
| 计算复杂度 | 低（Split CP） | 通常较高（MCMC等） |
| 灵活性 | 可包装任意模型 | 需要概率模型 |
| 条件覆盖 | 仅边际保证（默认） | 可实现条件保证 |

---

## 典型应用场景

- 🏥 **医疗诊断**：分类模型输出可信的候选疾病集合，辅助医生决策。
- 💊 **药物发现**：为分子属性预测提供置信区间。
- 🤖 **大语言模型**：为 LLM 生成的答案提供不确定性估计。
- 🚗 **自动驾驶**：目标检测中的置信集合，提升安全性。
- 📈 **金融预测**：时间序列预测区间，用于风险管理。

---

## 简单示例（Python）

使用 [`MAPIE`](https://github.com/scikit-learn-contrib/MAPIE) 库实现回归任务的 Conformal Prediction：

```python
from mapie.regression import MapieRegressor
from sklearn.linear_model import Ridge
import numpy as np

# 训练数据
X_train, y_train = ...
X_test = ...

# 用 MAPIE 包装任意 sklearn 模型
mapie = MapieRegressor(estimator=Ridge(), method="base", cv="split")
mapie.fit(X_train, y_train)

# 预测，alpha=0.1 表示 90% 置信度
y_pred, y_pis = mapie.predict(X_test, alpha=0.1)

# y_pis[:, 0, 0] 为下界，y_pis[:, 1, 0] 为上界
print(f"预测区间: [{y_pis[0, 0, 0]:.2f}, {y_pis[0, 1, 0]:.2f}]")
```

---

## 关键参考文献

1. Vovk, V., Gammerman, A., & Shafer, G. (2005). *Algorithmic Learning in a Random World*. Springer.
2. Angelopoulos, A. N., & Bates, S. (2023). [Conformal Prediction: A Gentle Introduction](https://arxiv.org/abs/2107.07511). *Foundations and Trends in Machine Learning*.
3. Romano, Y., Patterson, E., & Candès, E. (2019). Conformalized Quantile Regression. *NeurIPS*.
4. Tibshirani, R. J., et al. (2019). Conformal Prediction Under Covariate Shift. *NeurIPS*.
