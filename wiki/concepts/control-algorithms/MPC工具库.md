---
title: MPC工具库
created: 2026-04-22
type: concept
tags: [control-algorithms, mpc, python-tools, cvxpy, casadi, pyomo, do-mpc, gekko]
topics: [control-algorithms, mpc]
status: summarized
sources:
  - raw/notes/control-algorithms/2026-04-22-mpc_research/2026-04-22-mpc-research.md
related_concepts:
  - MPC
  - MPC算法家族
  - 储能MPC建模
---

# MPC工具库

## Python MPC 工具链三层架构

```
Layer 1: 建模语言
  ├── CVXPY       — 凸优化，DCP 规则
  └── Pyomo       — 代数建模，MILP/stochastic programming

Layer 2: 最优控制 / 自动微分框架
  ├── CasADi      — 自动微分 + OCP/NLP + 代码生成
  ├── do-mpc      — CasADi 上层框架，MPC/MHE 封装
  └── GEKKO       — 动态优化一体化，DAE 支持

Layer 3: 领域工作流平台
  └── MPCPy       — 楼宇/FMU/Modelica 工作流
```

## 工具对比表

| 工具库 | 最适合的问题 | 优点 | 局限 | 求解器接口 |
|--------|------------|------|------|-----------|
| **CVXPY** | 凸 LMPC、经济调度、QP/SOCP | DCP 语义清晰、prototype 快、warm-start 友好 | 仅凸问题、NMPC 不适合 | OSQP（内置）；Gurobi/CPLEX |
| **CasADi** | NMPC、最优控制、自动微分 | 自动微分强、multiple shooting 友好、可生成 C 代码 | 建模层偏底层 | IPOPT（默认）；OSQP/Gurobi/CPLEX |
| **Pyomo** | MILP、调度、随机规划 | 代数建模成熟、电力/运筹习惯一致 | 动态系统体验不如 CasADi | IPOPT；Gurobi/CPLEX |
| **do-mpc** | 研究型 NMPC/robust multi-stage | CasADi 上层封装、带 robust multi-stage、MHE | 生产级性能不如手写 CasADi | CasADi + IPOPT（内置）|
| **GEKKO** | 动态优化、NMPC、实时优化 | 一体化程度高、支持 DAE | 大规模稀疏 NMPC 可控性不如 CasADi | APOPT/BPOPT/IPOPT（内置）|
| **MPCPy** | 楼宇/FMU/Modelica 工作流 | 预测-估计-控制工作流清晰 | 项目老、偏楼宇 | JModelica/FMUs |

## 选型经验

> **CVXPY/OSQP 用来快速试错与做凸主干；Pyomo/Gurobi 或 CPLEX 用来承接 MILP 级的市场约束；CasADi/IPOPT 用来处理 NMPC 与高保真设备模型。**

## CVXPY — 凸 MPC 原型

**适用场景**：线性 MPC、凸经济 MPC、QP/SOCP

**核心特性**：DCP 规则、Parameter 支持（warm-start 友好）、内置 OSQP

```python
import cvxpy as cp

x = cp.Variable((nx, N+1))
u = cp.Variable((nu, N))
x0 = cp.Parameter(nx)

cost = cp.sum([cp.quad_form(x[:,k], Q) + cp.quad_form(u[:,k], R) for k in range(N)])
cons = [x[:,0] == x0]
for k in range(N):
    cons += [x[:,k+1] == A @ x[:,k] + B @ u[:,k], cp.abs(u[:,k]) <= umax]

prob = cp.Problem(cp.Minimize(cost), cons)
prob.solve(solver=cp.OSQP, warm_start=True)
```

## CasADi — NMPC 与自动微分

**适用场景**：非线性 MPC、代码生成、复杂约束

**核心特性**：符号数学 + 自动微分、多种求解器后端、支持 C code 生成（嵌入式部署）

```python
import casadi as ca

opti = ca.Opti()
X = opti.variable(nx, N+1)
U = opti.variable(nu, N)
x0 = opti.parameter(nx)

opti.subject_to(X[:,0] == x0)
for k in range(N):
    opti.subject_to(X[:,k+1] == f(X[:,k], U[:,k]))
opti.minimize(sum1(sum2(X[:,:N]**2)) + 0.1 * sum1(sum2(U**2)))
opti.solver("ipopt")
```

## Pyomo — MILP 与调度

**适用场景**：市场出清、机组组合、随机规划

```python
import pyomo.environ as pyo

m = pyo.ConcreteModel()
m.T = pyo.RangeSet(0, N-1)
m.u = pyo.Var(m.T, bounds=(-umax, umax))
m.obj = pyo.Objective(expr=sum(m.u[t]**2 for t in m.T))
solver = pyo.SolverFactory("gurobi")
solver.solve(m)
```

## do-mpc — 研究型 NMPC

**适用场景**：鲁棒 NMPC、多阶段 MPC、MHE

```python
import do_mpc

model = do_mpc.model.Model("discrete")
x = model.set_variable("_x", "x")
u = model.set_variable("_u", "u")
model.set_rhs("x", x + u)
model.setup()

mpc = do_mpc.controller.MPC(model)
mpc.set_param(n_horizon=20, t_step=1.0)
mpc.set_objective(mterm=x**2, lterm=x**2 + 0.1*u**2)
mpc.bounds["lower", "_u", "u"] = -1
mpc.bounds["upper", "_u", "u"] = 1
mpc.setup()
```

## GEKKO — 动态优化

**适用场景**：动态优化、NMPC、实时优化

```python
from gekko import GEKKO
import numpy as np

m = GEKKO(remote=False)
m.time = np.linspace(0, 10, 21)
u = m.MV(lb=-1, ub=1); u.STATUS = 1
x = m.CV(value=2.0); x.STATUS = 1
m.Equation(x.dt() == -x + u)
m.options.IMODE = 6  # MPC
m.solve(disp=False)
```

## 求解器生态

| 求解器 | 问题类型 | 特点 |
|--------|---------|------|
| **OSQP** | 凸 QP | factorization caching、warm-start |
| **ECOS** | 凸 QP/SOCP | 轻量级嵌入式 |
| **SCS** | 凸 QP/SOCP/SDP | 原始对偶算法 |
| **IPOPT** | 非凸 NLP | 内点法、工业标准 |
| **Gurobi** | MILP/凸 QP | 商业级、性能最强 |
| **CPLEX** | MILP/凸 QP | 商业级、工业广泛使用 |
| **Bonmin** | MINLP | 非线性 MINLP |

## 工程选型流程图

```
问题类型判断
    │
    ├── 连续凸 QP/SOCP
    │   └── CVXPY + OSQP（原研）/ Gurobi（生产）
    │
    ├── 包含离散变量（启停、互斥）
    │   └── Pyomo + Gurobi/CPLEX（MILP）
    │
    ├── 非线性动力学 + 实时性要求高
    │   └── CasADi + IPOPT（原型）/ CasADi + 嵌入式求解器（生产）
    │
    └── 研究型鲁棒/NMPC
        └── do-mpc（快速原型）
```

## 相关概念

- [[MPC]] — MPC 核心概念
- [[MPC算法家族]] — 不同 MPC 类型
- [[储能MPC建模]] — 能源场景具体建模

## 来源

- [[2026-04-22-mpc-research]] — Python 工具链详解
