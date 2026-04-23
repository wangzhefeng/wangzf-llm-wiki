---
title: 储能MPC建模
created: 2026-04-22
type: concept
tags: [control-algorithms, mpc, energy-storage, battery, soc, vpp, electricity-market]
topics: [control-algorithms, mpc, energy-storage]
status: summarized
sources:
  - raw/notes/control-algorithms/2026-04-22-mpc_research/2026-04-22-mpc-research.md
  - raw/notes/control-algorithms/2026-04-22-mpc_research/storage_mpc_project/README.md
related_concepts:
  - MPC
  - MPC算法家族
  - MPC数学原理
  - MPC工具库
---

# 储能MPC建模

## 概述

储能 MPC 是 MPC 在能源系统中的核心应用场景。通过滚动优化，在满足 SOC、功率、效率等约束的前提下，降低购电成本、抑制尖峰负荷、平滑并网功率。

## 核心要素

### 状态变量

$$x_k = SOC_k \quad \text{（储能荷电状态）}$$

### 控制变量

$$u_k = P_k^{batt} \quad \begin{cases} u_k > 0: & \text{放电} \\ u_k < 0: & \text{充电} \end{cases}$$

### 状态转移方程

$$SOC_{k+1} = SOC_k - \frac{\Delta t}{E} u_k$$

或含效率的完整版本：

$$SOC_{k+1} = SOC_k + \frac{\eta_c P^{ch}_k \Delta t}{E_{cap}} - \frac{P^{dis}_k \Delta t}{\eta_d E_{cap}}$$

其中：
- $\eta_c, \eta_d$：充、放电效率
- $E_{cap}$：电池额定容量
- $\Delta t$：采样时间步长

## 目标函数设计

### 基础版本（购电成本最小化）

$$\min \sum_{k=0}^{N-1} \left[ \pi_k P^{grid}_k \Delta t + \lambda_{soc}(SOC_k - SOC^{ref})^2 + \lambda_{u}u_k^2 + \lambda_{\Delta u}(u_k - u_{k-1})^2 \right] + \lambda_f(SOC_N - SOC^{ref})^2$$

其中各项意义：
- $\pi_k P^{grid}_k$：购电成本（$\pi_k$ 为电价）
- $\lambda_{soc}(SOC_k - SOC^{ref})^2$：SOC 偏差惩罚
- $\lambda_{u}u_k^2$：控制能量惩罚（防止过激动作）
- $\lambda_{\Delta u}(u_k - u_{k-1})^2$：控制平滑项（减少频繁充放切换）
- $\lambda_f(SOC_N - SOC^{ref})^2$：终端 SOC 惩罚（保证 horizon 末端行为合理）

### 经济 MPC 版本（收益最大化）

$$\max \sum_{t=k}^{k+N-1} \left( \pi_t^{sell} P_t^{sell} - \pi_t^{buy} P_t^{buy} - C_g(P_t^g) - C_{deg}(P_t^{ch}, P_t^{dis}) - C_{flex}(P_t^{flex}) \right) \Delta t$$

## 约束条件

### 必修约束

**SOC 上下界**：
$$SOC_{min} \le SOC_k \le SOC_{max}$$

**功率上下界**：
$$P_{min} \le u_k \le P_{max}$$

**并网功率**：
$$P^{grid}_k = P^{load}_k - P^{pv}_k + P^{ch}_k - P^{dis}_k$$

### 常见业务约束

**充放电互斥**（离散规则 → MILP）：
$$P^{ch}_k \cdot P^{dis}_k = 0$$

**买卖互斥**（市场规则 → MILP）：
$$P^{buy}_k \cdot P^{sell}_k = 0$$

**爬坡约束**：
$$|P^{g}_t - P^{g}_{t-1}| \le R^{ramp}$$

## 工程实现框架

**可运行的 CVXPY 储能 MPC 框架**（简化版，3 类设备：可控机组 + 储能 + 柔性负荷）：

```python
import numpy as np
import cvxpy as cp

def solve_vpp_mpc(
    load_hat, pv_hat, price_buy, price_sell,
    soc0,
    dt=1.0, eta_c=0.95, eta_d=0.95,
    g_max=3.0, g_ramp=1.0,
    ch_max=2.0, dis_max=2.0,
    soc_min=0.5, soc_max=8.0, soc_target=4.0,
    flex_max=1.0,
    c_gen_quad=0.05, c_gen_lin=0.40,
    c_deg=0.02, c_flex=0.10, c_soc_terminal=5.0
):
    H = len(load_hat)

    # 决策变量
    pg   = cp.Variable(H)      # 机组出力
    pch  = cp.Variable(H)      # 储能充电功率
    pdis = cp.Variable(H)      # 储能放电功率
    soc  = cp.Variable(H + 1)   # SOC 序列
    pflex = cp.Variable(H)     # 柔性负荷调整
    pbuy = cp.Variable(H)      # 向市场买电
    psell = cp.Variable(H)     # 向市场卖电

    cons = [soc[0] == soc0]
    for t in range(H):
        # 储能动态
        cons += [soc[t+1] == soc[t] + eta_c*pch[t]*dt - (pdis[t]/eta_d)*dt]
        # 功率平衡
        cons += [pg[t] + pv_hat[t] + pdis[t] + pbuy[t] + pflex[t]
                  == load_hat[t] + pch[t] + psell[t]]
        # 边界约束
        cons += [0 <= pg[t], pg[t] <= g_max,
                 0 <= pch[t], pch[t] <= ch_max,
                 0 <= pdis[t], pdis[t] <= dis_max,
                 -flex_max <= pflex[t], pflex[t] <= flex_max,
                 0 <= pbuy[t], 0 <= psell[t],
                 soc_min <= soc[t], soc[t] <= soc_max]
        # 爬坡约束
        if t >= 1:
            cons += [pg[t] - pg[t-1] <= g_ramp,
                     pg[t-1] - pg[t] <= g_ramp]

    # 目标函数
    obj = cp.sum(
        price_buy * pbuy - price_sell * psell
        + c_gen_quad * cp.square(pg) + c_gen_lin * pg
        + c_deg * (pch + pdis)
        + c_flex * cp.abs(pflex)
    ) + c_soc_terminal * cp.square(soc[H] - soc_target)

    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=cp.OSQP, warm_start=True, verbose=False)
    return {"pg": pg.value, "pch": pch.value, "pdis": pdis.value,
            "soc": soc.value, "pflex": pflex.value,
            "pbuy": pbuy.value, "psell": psell.value}
```

## 滚动优化执行循环

```python
soc_now = soc_measurement()
for k in range(current_time, end_time):
    # 1) 更新预测（接入时间序列预测模块）
    load_hat   = load_forecaster.predict(k, horizon=H)
    pv_hat     = pv_forecaster.predict(k, horizon=H)
    price_buy  = price_model.predict_buy(k, horizon=H)
    price_sell = price_model.predict_sell(k, horizon=H)

    # 2) 求解 MPC
    sol = solve_vpp_mpc(load_hat, pv_hat, price_buy, price_sell, soc_now)

    # 3) 仅执行第一步
    dispatch_to_assets(pg=sol["pg"][0], pch=sol["pch"][0],
                       pdis=sol["pdis"][0], pflex=sol["pflex"][0])

    # 4) 读取新状态
    soc_now = soc_measurement()
```

## 关键工程参数建议

| 参数 | 建议初值 | 作用 | 调参建议 |
|------|---------|------|---------|
| 采样周期 $\Delta t$ | 5-15 分钟（交易层） | 在线求解频率 | 与数据刷新、执行机构能力一致 |
| 预测时域 $H$ | 8-24 步 | 前瞻性 | 太短"近视"，太长放大预测误差 |
| 终端 SOC 目标 | 日内中性或次日目标值 | 避免 horizon 末端透支 | 有跨日交易时必须加终端项 |
| 退化成本系数 | 从 throughput 近似开始 | 抑制无意义频繁充放 | 先粗后细 |
| 软约束罚系数 | 经济项 1-2 个数量级 | 保证"宁可贵，别不可行" | 先让系统总能解，再收紧 |
| warm-start | 默认开启 | 缩短重复求解时间 | 线性 QP 几乎必开 |

## 与虚拟电厂的结合

储能 MPC 是虚拟电厂（VPP）的核心调度组件。VPP MPC 模型通常包含：

**四类资产**：
- 可控发电机组 $P^g$
- 储能系统 $P^{ch}/P^{dis}$
- 柔性负荷 $P^{flex}$
- 市场交易接口 $P^{buy}/P^{sell}$

**不确定性处理三路径**：
1. **确定性滚动优化**：用最新点预测直接求解，靠每轮重优化消化误差
2. **场景化随机 MPC**：生成若干联合场景，最小化期望成本或 CVaR
3. **鲁棒 MPC**：用区间预测 + reserve margin 做约束收缩

## 多时间尺度设计

推荐**两层时间尺度**：

| 层级 | 周期 | 内容 | MPC 类型 |
|------|------|------|---------|
| 交易/经济调度层 | 15 分钟 - 1 小时 | 日内滚动、4-24h 前瞻 | 线性/经济 MPC |
| 站内功率跟踪层 | 秒级 - 分钟级 | 频率响应、逆变器限额 | 线性 MPC 或规则控制 |

> **核心原则**：交易层不要背全部设备高速控制，设备层也不要直接承接市场级场景树。

## 工程迭代（storage_mpc_project）

项目经历了 v1 ~ v4 版本迭代，覆盖从简化单设备到完整 VPP 多资产的建模演进：

- **v1**：单储能 + 固定价格，验证 MPC 框架可运行性
- **v2**：引入可控机组 + 爬坡约束，验证调度层可行性
- **v3**：引入储能退化成本 + 柔性负荷，价格信号接入
- **v4**：多时间尺度 + 市场交易接口（买/卖互斥、偏差惩罚）

## 相关概念

- [[MPC]] — MPC 核心概念
- [[MPC算法家族]] — 线性/经济/随机 MPC
- [[MPC数学原理]] — 数学 formulation
- [[MPC工具库]] — CVXPY/OSQP 实现

## 来源

- [[2026-04-22-mpc-research]] — 储能 MPC 建模与 VPP 集成
- [[2026-04-22-storage-mpc-project-v1]] 至 v4 — 工程模板迭代
