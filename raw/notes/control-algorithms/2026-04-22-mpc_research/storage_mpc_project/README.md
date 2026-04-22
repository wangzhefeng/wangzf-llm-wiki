# 储能 MPC 项目（工程版）

这是一个**可直接运行**的储能 Model Predictive Control（MPC）工程项目，面向能源/电力算法工程师设计。  
项目目标是在给定**负荷预测**与**电价预测**的情况下，对储能系统进行滚动优化调度，以降低购电成本并保持储能运行安全。

## 1. 项目特性

- 面向工程实现，而不是单一 demo
- 使用 **CVXPY + OSQP** 构建线性二次型 MPC
- 支持：
  - 负荷预测序列输入
  - 电价预测序列输入
  - 储能 SOC 约束
  - 储能功率约束
  - 功率平滑项
  - 终端 SOC 惩罚
- 提供完整的：
  - 项目结构
  - 参数配置
  - 仿真数据生成
  - MPC 控制器
  - 滚动仿真器
  - 结果可视化与结果导出

## 2. 数学模型

状态变量：

\[
x_k = SOC_k
\]

控制变量：

\[
u_k = P_k^{batt}
\]

约定：
- \( u_k > 0 \)：储能放电
- \( u_k < 0 \)：储能充电

状态转移方程：

\[
SOC_{k+1} = SOC_k - \frac{\Delta t}{E} u_k
\]

电网购电功率：

\[
P_k^{grid} = \hat{L}_k - u_k
\]

目标函数：

\[
\min \sum_{k=0}^{N-1}
\left[
\pi_k P_k^{grid} \Delta t
+ \lambda_{soc}(SOC_k - SOC^{ref})^2
+ \lambda_{u}u_k^2
+ \lambda_{\Delta u}(u_k-u_{k-1})^2
\right]
+ \lambda_f(SOC_N - SOC^{ref})^2
\]

约束：

\[
SOC_{\min} \le SOC_k \le SOC_{\max}
\]

\[
P_{\min} \le u_k \le P_{\max}
\]

\[
P_k^{grid} \ge 0
\]

## 3. 项目结构

```text
storage_mpc_project/
├── README.md
├── requirements.txt
├── configs/
│   └── default_config.json
├── data/
├── results/
├── scripts/
│   └── run_simulation.py
└── src/
    └── storage_mpc/
        ├── __init__.py
        ├── config.py
        ├── data_generator.py
        ├── forecaster.py
        ├── mpc_controller.py
        ├── simulator.py
        └── plotting.py
```

## 4. 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

或：

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 5. 运行

```bash
python scripts/run_simulation.py
```

运行后会在 `results/` 中输出：

- `simulation_results.csv`
- `soc_trajectory.png`
- `power_dispatch.png`
- `price_load_overview.png`

## 6. 可扩展方向

- 加入充放电效率 \(\eta_c, \eta_d\)
- 引入电池退化成本
- 允许售电 / 现货交易
- 接入真实负荷预测与电价预测
- 升级为 CasADi / NMPC
