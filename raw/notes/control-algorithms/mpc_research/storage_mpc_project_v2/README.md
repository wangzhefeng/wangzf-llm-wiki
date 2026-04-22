# 储能 MPC 项目（工程版 V2）

这是一个更贴近业务落地的储能 MPC 工程项目。相比 V1，本版本新增了：

- 充电功率 / 放电功率分离建模
- 充放电效率
- 电网买电 / 卖电分离
- 光伏出力输入接口
- 电池退化近似成本
- 更清晰的功率平衡约束
- 更接近虚拟电厂 / 工商业储能 / 电力交易场景

---

## 1. 场景定义

系统包含：

- 用户负荷 `load`
- 光伏出力 `pv`
- 储能 `battery`
- 电网买电 `p_grid_buy`
- 电网卖电 `p_grid_sell`

在每个时刻，控制器基于未来 `N` 步预测信息滚动求解最优储能策略。

---

## 2. 数学模型

### 2.1 状态变量

\[
x_k = SOC_k
\]

### 2.2 控制变量

\[
u_k = [P_k^{ch}, P_k^{dis}, P_k^{buy}, P_k^{sell}]
\]

其中：

- \(P_k^{ch} \ge 0\)：充电功率
- \(P_k^{dis} \ge 0\)：放电功率
- \(P_k^{buy} \ge 0\)：向电网购电
- \(P_k^{sell} \ge 0\)：向电网售电

### 2.3 状态转移方程

\[
SOC_{k+1} = SOC_k + \frac{\eta_c \Delta t}{E} P_k^{ch} - \frac{\Delta t}{\eta_d E} P_k^{dis}
\]

### 2.4 功率平衡

\[
P_k^{buy} - P_k^{sell} + P_k^{dis} - P_k^{ch} + P_k^{pv} = P_k^{load}
\]

等价理解：

> 电网净购电 + 储能净放电 + 光伏 = 负荷需求

### 2.5 目标函数

\[
\min \sum_{k=0}^{N-1}
\left[
\pi_k^{buy} P_k^{buy} \Delta t
- \pi_k^{sell} P_k^{sell} \Delta t
+ \lambda_{soc}(SOC_k - SOC^{ref})^2
+ \lambda_{deg}(P_k^{ch}+P_k^{dis})\Delta t
+ \lambda_{\Delta u}((P_k^{ch}-P_{k-1}^{ch})^2 + (P_k^{dis}-P_{k-1}^{dis})^2)
\right]
+ \lambda_f(SOC_N - SOC^{ref})^2
\]

解释：

- 买电成本
- 售电收益
- SOC 安全惩罚
- 电池退化近似成本
- 控制平滑项
- 终端 SOC 惩罚

---

## 3. 运行

```bash
python scripts/run_simulation.py
```

运行后输出：

- `data/synthetic_inputs.csv`
- `results/simulation_results.csv`
- `results/soc_trajectory.png`
- `results/power_stack.png`
- `results/price_overview.png`

---

## 4. V2 相比 V1 的关键升级

### 4.1 为什么要拆分充放电功率

V1 用单个带符号功率变量表示储能功率，适合教学，但业务上常常更适合：

- 单独统计充电量 / 放电量
- 分别加入效率
- 方便后续加入互斥逻辑与退化成本

### 4.2 为什么要拆分买电/卖电

真实市场交易里，买电与卖电价格通常不同，而且业务结算通常也是分开的。

### 4.3 为什么要加入退化成本

如果只优化套利收益，模型容易频繁充放电。加入简单退化项后，策略更接近真实业务。

---

## 5. 后续可扩展方向

- 加入充放电互斥二进制变量（MILP）
- 加入需量电费 / 容量电费
- 加入偏差考核成本
- 加入多储能聚合
- 加入真实预测模型接口
- 扩展为日前 + 日内 + 实时分层调度
