# MPC 对话内容完整汇总（从 Part 1 到最后，按页面回答整理）

> 说明  
> 本文档按本次会话中从 **Part 1** 开始直到最后的 MPC 相关回答进行整理，尽量保留页面中出现过的：
>
> - 文字说明
> - 公式
> - 表格
> - 代码块
> - 下载链接
> - 图示位置说明
>
> 对于页面中的**交互式图片/组件**，普通 Markdown 无法直接内嵌其动态内容，因此本文档会保留其出现位置与说明。

---

# Part 1：MPC 核心原理（工程视角 + 数学 + 图）

## 原始回答整理

好，直接进入**工程版 MPC 文档**。我按你能“直接拿去用/改代码”的标准来写，并把控制理论用你熟悉的**优化视角（QP/NLP）**重构。

---

## 1. MPC 本质（一句话）

> **MPC（Model Predictive Control）= 每个时刻解一个有限时域优化问题，并只执行第一步决策**

---

## 2. MPC 的核心结构（你要从优化角度理解）

**页面中这里插入过一个交互式图片组件**，用于展示 MPC 的滚动时域 / 预测控制示意图。  
当时的图示检索主题包括：

- `model predictive control diagram receding horizon`
- `mpc rolling horizon control scheme`
- `predictive control block diagram optimization loop`
- `mpc state prediction horizon illustration`

普通 Markdown 中无法直接嵌入该交互式组件，因此此处保留说明。

MPC 的核心是一个**滚动优化问题（Receding Horizon Optimization）**：

在时刻 \( t \)，求解：

$$
\min_{u_{t:t+H-1}} \sum_{k=0}^{H-1} \ell(x_{t+k}, u_{t+k})
$$

subject to：

$$
x_{t+k+1} = f(x_{t+k}, u_{t+k})
$$

$$
x_{t+k} \in \mathcal{X}, \quad u_{t+k} \in \mathcal{U}
$$

### 关键点

#### ① 预测（Prediction）
- 使用系统模型 \( f(\cdot) \)
- 预测未来 \( H \) 步状态

对应到你的工作，类似于：
- 负荷预测
- 电价预测

#### ② 优化（Optimization）
本质可以是：
- **QP（线性系统 + 二次成本）**
- 或 **NLP（非线性系统）**

这和你熟悉的：
- 运筹优化（LP / QP / MIP）
是完全统一的。

#### ③ 滚动（Receding Horizon）
只执行：

$$
u_t^*
$$

下一时刻重新求解。

本质上它就是：

> **在线优化（Online Optimization）**

---

## 3. MPC vs 传统控制（你要理解差异）

| 方法 | 本质 | 能否处理约束 | 工程适用性 |
|------|------|------------|------------|
| PID | 规则控制 | ❌ | 低 |
| LQR | 最优控制 | ❌（弱） | 中 |
| MPC | 优化问题 | ✅ | ⭐⭐⭐⭐ |

对你来说：

> MPC = “带约束的动态优化”

---

## 4. MPC 数学结构（工程可落地形式）

### 线性 MPC（最常用）

系统：

$$
x_{k+1} = A x_k + B u_k
$$

目标函数：

$$
J = \sum_{k=0}^{H-1} (x_k^T Q x_k + u_k^T R u_k)
$$

它可以进一步整理成标准 QP：

$$
\min_{U} \frac{1}{2} U^T H U + f^T U
$$

### 你熟悉的映射关系

| MPC概念 | 优化视角 |
|--------|--------|
| 状态 \(x\) | 决策变量的函数 |
| 控制 \(u\) | 决策变量 |
| 动态方程 | 等式约束 |
| 约束 | 不等式约束 |
| 成本函数 | 目标函数 |

结论：

> **MPC = 带动态约束的多阶段优化问题**

---

## 5. MPC 与你当前工作的关系（重点）

你现在做的是：

- 负荷预测（TS）
- 储能调度（优化）

MPC 正好是：

$$
\text{预测} + \text{优化} + \text{闭环控制}
$$

### 在 VPP / 电力中的映射

| MPC组件 | 电力系统对应 |
|--------|------------|
| 状态 \(x\) | SOC / 负荷状态 |
| 控制 \(u\) | 充放电功率 |
| 模型 \(f\) | 电池动态 |
| 预测 | 负荷 / 电价 |
| 约束 | 功率 / SOC / 市场规则 |

本质上就是：

> **“带预测的储能优化调度”**

---

## 6. MPC 的工程优势（你为什么必须学）

### 1. 能处理复杂约束
- SOC上下限
- 功率限制
- 电价策略

### 2. 能融合预测（你最擅长）
- 负荷预测
- 电价预测
- 可再生出力预测

### 3. 在线自适应
- 每个时刻重新优化
- 自动纠偏

---

## 7. 一个直观例子（非常关键）

假设你做储能：

目标：

> **低价充电，高价放电**

### 非 MPC（传统优化）
一次性优化：
- 用预测电价
- 得到完整策略

问题：
- 预测误差容易把策略打崩

### MPC
每小时：
1. 用最新预测
2. 重新优化未来 24h
3. 执行当前决策

优点：
- **鲁棒性更强**

---

## 小结（Part 1）

MPC 的核心可以记成一句话：

> **MPC = 动态系统 + 滚动优化 + 预测驱动决策**

---

# Part 2：MPC 的数学建模与优化结构（QP / NLP / 工程实现视角）

这一部分进入你最需要的层面：**如何把 MPC 真正写成一个优化问题**，以及它为什么能被 `cvxpy`、`casadi`、`osqp`、`gurobi` 这类工具直接求解。

---

## 1. 从动态系统到优化问题

MPC 不是“先有控制，再想办法优化”，而是反过来：

> **先把系统写成一个可预测的数学模型，再把未来一段时间的控制动作作为决策变量，最后构造目标函数和约束，形成一个有限时域优化问题。**

### 1.1 离散时间系统模型

MPC 最常见的离散形式：

$$
x_{k+1} = f(x_k, u_k)
$$

其中：

- \(x_k\)：时刻 \(k\) 的状态（state）
- \(u_k\)：时刻 \(k\) 的控制输入（control / action）
- \(f(\cdot)\)：系统动态模型
- \(k\)：离散时间步

### 1.2 在线滚动优化问题

在当前时刻 \(t\)，MPC 求解未来 \(N\) 步：

$$
\min_{u_{t|t},u_{t+1|t},\dots,u_{t+N-1|t}} J
$$

subject to

$$
x_{t+k+1|t} = f(x_{t+k|t}, u_{t+k|t}), \quad k=0,\dots,N-1
$$

$$
x_{t+k|t} \in \mathcal{X}, \quad u_{t+k|t} \in \mathcal{U}
$$

$$
x_{t|t} = x_t^{\text{measured}}
$$

这里的记号 \(x_{t+k|t}\) 表示：

> **在时刻 \(t\) 基于当前信息，对未来 \(t+k\) 时刻状态的预测**

---

## 2. 目标函数怎么构造

MPC 的目标函数本质上是一个**多阶段代价累加**：

$$
J = \sum_{k=0}^{N-1} \ell(x_{t+k|t}, u_{t+k|t}) + V_f(x_{t+N|t})
$$

其中：

- \(\ell(\cdot)\)：阶段成本（stage cost）
- \(V_f(\cdot)\)：终端成本（terminal cost）

### 2.1 最经典的二次型目标

线性 MPC 最常见：

$$
J = \sum_{k=0}^{N-1} \left[(x_{t+k|t}-x^{\text{ref}})^T Q (x_{t+k|t}-x^{\text{ref}}) + (u_{t+k|t}-u^{\text{ref}})^T R (u_{t+k|t}-u^{\text{ref}})\right] + (x_{t+N|t}-x^{\text{ref}})^T P (x_{t+N|t}-x^{\text{ref}})
$$

含义非常直观：

- \(Q\)：状态偏差惩罚
- \(R\)：控制动作惩罚
- \(P\)：终端状态惩罚

### 2.2 工程解释

对于算法工程师，可以理解成：

#### 第一项：状态跟踪误差
让系统尽量接近目标。

例如：
- 温度跟踪设定点
- SOC 跟踪期望水平
- 功率跟踪调度计划
- 净负荷跟踪目标曲线

#### 第二项：控制代价
防止动作过大。

例如：
- 充放电功率过大损伤电池
- 出力变化过猛不利于设备稳定
- 频繁控制切换导致执行器磨损

#### 第三项：终端成本
对预测窗末端状态做“收尾约束”。

例如：
- 让储能在预测窗末端不要把 SOC 用空
- 避免短视优化只顾眼前收益

---

## 3. 约束怎么建

MPC 最大的工程价值之一，就是可以**显式处理约束**。

### 3.1 状态约束

$$
x_{\min} \le x_k \le x_{\max}
$$

例如：
- SOC 上下限
- 温度安全区间
- 库存上下界
- 网络潮流状态限制

### 3.2 控制约束

$$
u_{\min} \le u_k \le u_{\max}
$$

例如：
- 储能充放电功率上限
- 可调负荷调节幅度
- 发电机爬坡能力
- 电网购售电功率限额

### 3.3 变化率约束（很常用）

$$
\Delta u_k = u_k - u_{k-1}
$$

$$
\Delta u_{\min} \le \Delta u_k \le \Delta u_{\max}
$$

这在工程里非常常见，因为很多设备不能突变。

在电力场景中，典型包括：
- 储能功率变化平滑
- 机组爬坡约束
- 柔性负荷响应速度限制

### 3.4 混合逻辑约束

如果系统存在开关、启停、买卖互斥等逻辑，MPC 会变成 MILP / MINLP，例如：

- 充电与放电不能同时发生
- 买电与卖电不能同时发生
- 机组启停与最小开停机时间

这时就从连续优化问题进入了**混合整数优化**。

---

## 4. 线性 MPC：如何变成标准 QP

这是最关键的一段。

### 4.1 线性系统

假设系统为：

$$
x_{k+1} = A x_k + B u_k
$$

目标：

$$
J = \sum_{k=0}^{N-1} (x_k^T Q x_k + u_k^T R u_k) + x_N^T P x_N
$$

约束：

$$
x_{\min} \le x_k \le x_{\max}
$$

$$
u_{\min} \le u_k \le u_{\max}
$$

### 4.2 决策变量堆叠

定义控制序列：

$$
U =
\begin{bmatrix}
u_0 \\
u_1 \\
\vdots \\
u_{N-1}
\end{bmatrix}
$$

状态序列：

$$
X =
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_N
\end{bmatrix}
$$

注意：当前状态 \(x_0\) 已知，不是决策变量。

### 4.3 预测展开

由系统递推：

$$
x_1 = A x_0 + B u_0
$$

$$
x_2 = A x_1 + B u_1 = A^2 x_0 + ABu_0 + Bu_1
$$

$$
x_3 = A x_2 + B u_2 = A^3 x_0 + A^2Bu_0 + ABu_1 + Bu_2
$$

继续展开后可以写成矩阵形式：

$$
X = \Phi x_0 + \Gamma U
$$

其中：

$$
\Phi =
\begin{bmatrix}
A \\
A^2 \\
\vdots \\
A^N
\end{bmatrix}
$$

$$
\Gamma =
\begin{bmatrix}
B & 0 & 0 & \cdots & 0 \\
AB & B & 0 & \cdots & 0 \\
A^2B & AB & B & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
A^{N-1}B & A^{N-2}B & A^{N-3}B & \cdots & B
\end{bmatrix}
$$

### 4.4 把目标函数改写成 U 的二次型

原始目标：

$$
J = X^T \bar{Q} X + U^T \bar{R} U
$$

其中：

$$
\bar{Q} = \mathrm{diag}(Q, Q, \dots, P)
$$

$$
\bar{R} = \mathrm{diag}(R, R, \dots, R)
$$

代入 \(X = \Phi x_0 + \Gamma U\)：

$$
J = (\Phi x_0 + \Gamma U)^T \bar{Q} (\Phi x_0 + \Gamma U) + U^T \bar{R} U
$$

展开得到：

$$
J = U^T (\Gamma^T \bar{Q}\Gamma + \bar{R}) U + 2 x_0^T \Phi^T \bar{Q}\Gamma U + x_0^T \Phi^T \bar{Q}\Phi x_0
$$

去掉与 \(U\) 无关的常数项，得到标准 QP：

$$
\min_U \frac{1}{2} U^T H U + g^T U
$$

其中：

$$
H = 2(\Gamma^T \bar{Q}\Gamma + \bar{R})
$$

$$
g = 2\Gamma^T \bar{Q}\Phi x_0
$$

### 4.5 约束也可以堆叠

控制约束：

$$
\bar{u}_{\min} \le U \le \bar{u}_{\max}
$$

状态约束：

$$
X = \Phi x_0 + \Gamma U
$$

因此：

$$
x_{\min} \le \Phi x_0 + \Gamma U \le x_{\max}
$$

进一步改写成：

$$
A_{\text{ineq}} U \le b_{\text{ineq}}
$$

于是整个问题成为：

$$
\min_U \frac{1}{2} U^T H U + g^T U
$$

subject to

$$
A_{\text{ineq}} U \le b_{\text{ineq}}
$$

这就是标准二次规划（QP）。

---

## 5. 为什么线性 MPC 往往是 QP

因为同时满足这三条：

### 5.1 系统是线性的

$$
x_{k+1} = Ax_k + Bu_k
$$

### 5.2 代价函数是二次的

$$
x^TQx + u^TRu
$$

### 5.3 约束是线性的

$$
Cx + Du \le e
$$

那么整个 MPC 问题就是凸 QP，具有：

- 求解速度快
- 全局最优
- 数值稳定
- 易于实时控制

这也是工业界和电力场景最常见的 MPC 形式。

---

## 6. 非线性 MPC（NMPC）是什么

如果系统是：

$$
x_{k+1} = f(x_k, u_k)
$$

或者目标 / 约束是非线性的，例如：

- 电池效率和 SOC 有关
- 潮流模型非线性
- 市场收益函数非线性
- 热惯性模型非线性

则问题变成：

$$
\min J(x,u)
$$

subject to

$$
x_{k+1} = f(x_k,u_k)
$$

$$
g(x_k,u_k) \le 0
$$

这就是**非线性规划（NLP）**形式。

### 6.1 NMPC 的特点

优点：
- 建模更真实
- 能表达复杂物理过程
- 更适合高精度系统

缺点：
- 求解慢
- 可能只得到局部最优
- 对初值和数值尺度敏感
- 在线实时性更难保证

### 6.2 工程折中

电力与能源领域很常见的做法是：

#### 做法 A：线性化
把非线性模型在运行点附近线性化，得到时变线性模型：

$$
x_{k+1} \approx A_k x_k + B_k u_k + c_k
$$

得到 **LTV-MPC（线性时变 MPC）**

#### 做法 B：分层
上层做慢时间尺度调度，下层做快时间尺度线性 MPC。

#### 做法 C：简化代理模型
用 piecewise linear / affine approximation 代替复杂非线性。

---

## 7. 软约束与可行性修复

现实中常常会遇到：

- 预测误差太大
- 约束太紧
- 当前状态已在安全边界之外
- 模型不完全准确

此时优化问题可能**不可行**。

为避免 MPC 失效，常引入**松弛变量（slack variable）**。

### 7.1 例子

原本约束：

$$
x_k \le x_{\max}
$$

改成软约束：

$$
x_k \le x_{\max} + \epsilon_k, \quad \epsilon_k \ge 0
$$

并在目标中加大罚项：

$$
J = J_{\text{original}} + \rho \sum_{k=0}^{N} \epsilon_k
$$

或

$$
J = J_{\text{original}} + \rho \sum_{k=0}^{N} \epsilon_k^2
$$

### 7.2 工程理解

意思是：

> “尽量满足约束；如果实在做不到，也要以最小程度违反，并且要为违反付出高代价。”

这在储能、电网约束、柔性负荷控制中非常实用。

---

## 8. 终端约束与稳定性

MPC 不是随便滚动就一定稳定。理论上通常需要终端设计。

### 8.1 终端成本

$$
x_N^T P x_N
$$

### 8.2 终端约束

$$
x_N \in \mathcal{X}_f
$$

### 8.3 工程上怎么处理

在很多能源系统里，严格稳定性证明不是第一优先级，更常见的是：

- 加终端 SOC 约束
- 加终端参考偏差惩罚
- 让预测窗足够长
- 定期更新预测

例如储能调度里常见：

$$
SOC_N \ge SOC_{\text{target}}
$$

或者：

$$
(SOC_N - SOC_{\text{ref}})^2
$$

防止短视放空电池。

---

## 9. MPC 的变量、参数、输入输出结构

### 9.1 在线求解时已知量

每个时刻已知：

- 当前测量状态 \(x_t\)
- 未来预测扰动 \(\hat{d}_{t:t+N-1}\)
- 参考轨迹 \(r_{t:t+N}\)
- 模型参数 \(A,B\) 或 \(f\)
- 约束参数

### 9.2 优化变量

通常是未来控制序列：

$$
u_{t|t}, u_{t+1|t}, \dots, u_{t+N-1|t}
$$

有时也会把状态序列一起作为变量：

$$
x_{t+1|t}, \dots, x_{t+N|t}
$$

这是 `cvxpy` / `casadi` 中最常见的写法。

### 9.3 输出

求解结果是整条未来控制轨迹：

$$
U^* = [u_{t|t}^*, u_{t+1|t}^*, \dots, u_{t+N-1|t}^*]
$$

但实际只执行：

$$
u_t = u_{t|t}^*
$$

然后下一时刻滚动。

---

## 10. 两种常见建模方式

### 10.1 Condensed form（消元形式）

把状态全部消去，只保留控制变量 \(U\)。

优点：
- 变量数少
- 对 QP 求解器友好

缺点：
- 推导复杂
- 加复杂约束不够直观

适合：
- 手工构造高速 QP
- OSQP / qpOASES 风格实现

### 10.2 Sparse form（稀疏形式）

把每个时刻的 \(x_k, u_k\) 都作为变量，动态方程显式作为约束。

优点：
- 代码直观
- 容易扩展
- 易加复杂约束

缺点：
- 变量更多
- 但现代求解器通常可接受

适合：
- `cvxpy`
- `casadi`
- `pyomo`

### 10.3 你应该怎么选

对你这种算法工程师，我建议：

- **学习原理时**：先懂 condensed form
- **实际写代码时**：优先 sparse form

因为 sparse form 更像你平时写优化模型。

---

## 11. 电力场景里的 MPC 建模模板

### 11.1 状态

$$
x_k = \text{SOC}_k
$$

也可以扩展为：

$$
x_k = [SOC_k, \text{thermal state}_k, \text{degradation state}_k, \dots]
$$

### 11.2 控制

$$
u_k = [P_k^{ch}, P_k^{dis}]
$$

或者简化为带符号功率：

$$
u_k = P_k^{batt}
$$

### 11.3 扰动 / 外生变量

$$
d_k = [\hat{L}_k, \hat{\pi}_k, \hat{P}_k^{PV}, \dots]
$$

包括：

- 负荷预测
- 电价预测
- 光伏预测
- 风电预测

### 11.4 目标函数示例

$$
\min \sum_{k=0}^{N-1} \left(
\pi_k P_k^{grid}\Delta t
+ \lambda_1 (SOC_k - SOC^{ref})^2
+ \lambda_2 (u_k-u_{k-1})^2
\right)
$$

### 11.5 约束示例

$$
SOC_{k+1}=SOC_k+\eta_c P_k^{ch}\Delta t/E - \frac{1}{\eta_d}P_k^{dis}\Delta t/E
$$

$$
SOC_{\min}\le SOC_k \le SOC_{\max}
$$

$$
0 \le P_k^{ch} \le P_{\max}^{ch}
$$

$$
0 \le P_k^{dis} \le P_{\max}^{dis}
$$

$$
P_k^{grid} = L_k - P_k^{PV} + P_k^{ch} - P_k^{dis}
$$

这已经是一个非常标准的储能 MPC 骨架。

---

## 12. 你应该把 MPC 理解成什么

对你来说，最合适的理解不是“高级控制器”，而是：

> **MPC = 带状态递推约束的多阶段滚动优化框架**

更具体一点：

- 时间序列模型负责“未来信息”
- 动态方程负责“物理演化”
- 优化模型负责“决策求解”
- 滚动机制负责“闭环修正”

这就是 MPC 的工程本质。

---

## 13. 本部分小结

Part 2 你需要真正掌握的结论有 6 个：

1. MPC 的核心数学形式是有限时域动态优化。  
2. 线性系统 + 二次目标 + 线性约束 ⇒ 标准 QP。  
3. 非线性系统 / 非线性约束 ⇒ NLP / NMPC。  
4. 状态方程在优化里就是“跨时段耦合约束”。  
5. 滚动优化本质上是“每个时刻重新求解一遍未来问题”。  
6. 在能源系统里，MPC 非常适合把预测、优化、设备约束三者统一起来。

---

# Part 3：MPC 常用算法技术、Python 工具库、算法构建流程与代码结构

> 注：页面中这一部分最早生成的是一个较简略的 Markdown 文件，这里一并保留其内容与后续解释。

---

## Part 3 的文档片段

### 常用 Python 工具库

#### 3.1 凸优化 / QP
- cvxpy（强烈推荐）
- osqp（高速QP求解器）
- gurobipy（商业求解器）

#### 3.2 非线性优化
- casadi（NMPC核心工具）
- ipopt（求解器）

#### 3.3 工程建模
- pyomo（偏运筹优化）
- scipy.optimize（轻量）

---

### MPC 标准工程流程

1. 获取当前状态 x_t  
2. 获取未来预测（负荷、电价等）  
3. 构建优化问题  
4. 求解优化问题  
5. 执行 u_t  
6. 滚动到下一时刻  

---

### 标准代码结构（伪代码）

```python
for t in range(T):

    x_t = measure_state()

    forecast = get_forecast(t)

    problem = build_mpc_problem(x_t, forecast)

    u_seq = solve(problem)

    u_t = u_seq[0]

    apply_control(u_t)
```

---

### CVXPY 示例骨架

```python
import cvxpy as cp

x = cp.Variable(N+1)
u = cp.Variable(N)

cost = 0
constraints = []

for k in range(N):
    cost += cp.square(x[k]) + cp.square(u[k])
    constraints += [x[k+1] == A*x[k] + B*u[k]]

problem = cp.Problem(cp.Minimize(cost), constraints)
problem.solve()
```

---

### 工程建议

- 优先用 sparse form 建模
- QP 用 OSQP / GUROBI
- NMPC 用 CasADi
- 电力系统优先线性化（LTV-MPC）

---

## Part 3 对应下载链接（页面中曾提供）

- [下载 MPC 工程版文档（Part1~Part3）](sandbox:/mnt/data/mpc_engineering_doc_part1_3.md)

---

# Part 4：3 个 Python 示例（从最简单到标准约束 MPC）

这一部分开始进入“真正能写代码”的层面。  
我会按下面顺序展开：

1. **示例 1：最简单的一维无约束 MPC**
2. **示例 2：带输入/状态约束的线性 MPC（QP）**
3. **示例 3：储能 SOC 控制的简化 MPC**

这 3 个例子是递进关系：

- 示例 1 让你理解“滚动优化”本质
- 示例 2 让你理解“为什么 MPC = QP”
- 示例 3 开始贴近电力 / 储能场景

---

## 1. 示例 1：最简单的一维无约束 MPC

### 1.1 问题描述

考虑一个最简单的一维离散系统：

$$
x_{k+1} = x_k + u_k
$$

其中：

- \(x_k\)：系统状态
- \(u_k\)：控制输入

目标是让状态 \(x_k\) 尽快趋近于 0，同时控制动作不要过大。

### 1.2 优化模型

在每个时刻求解未来 \(N\) 步问题：

$$
\min \sum_{k=0}^{N-1} (q x_k^2 + r u_k^2) + q_f x_N^2
$$

subject to

$$
x_{k+1} = x_k + u_k
$$

这里没有显式约束，所以本质上是一个无约束二次优化问题。

### 1.3 Python 代码（CVXPY）

```python
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# ===== 参数 =====
N = 10          # 预测时域
T = 30          # 总仿真步数
q = 1.0
r = 0.1
qf = 2.0

x_current = 8.0

x_hist = [x_current]
u_hist = []

for t in range(T):
    # 决策变量
    x = cp.Variable(N + 1)
    u = cp.Variable(N)

    cost = 0
    constraints = [x[0] == x_current]

    for k in range(N):
        cost += q * cp.square(x[k]) + r * cp.square(u[k])
        constraints += [x[k+1] == x[k] + u[k]]

    cost += qf * cp.square(x[N])

    prob = cp.Problem(cp.Minimize(cost), constraints)
    prob.solve(solver=cp.OSQP)

    # 只执行第一步
    u_apply = u.value[0]
    x_current = x_current + u_apply

    u_hist.append(u_apply)
    x_hist.append(x_current)

# ===== 画图 =====
plt.figure(figsize=(8, 4))
plt.plot(x_hist, marker='o')
plt.title("State trajectory - Example 1")
plt.xlabel("time")
plt.ylabel("x")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 4))
plt.step(range(len(u_hist)), u_hist, where='post')
plt.title("Control input - Example 1")
plt.xlabel("time")
plt.ylabel("u")
plt.grid(True)
plt.show()
```

### 1.4 原理解释

这个例子虽然简单，但已经完整体现了 MPC 的核心机制：

#### 第一步：当前状态已知
例如当前 \(x_t = 8\)

#### 第二步：优化未来 \(N\) 步
求未来 10 步的最优控制序列：

$$
[u_{t|t}, u_{t+1|t}, \dots, u_{t+N-1|t}]
$$

#### 第三步：只执行第一步
只执行：

$$
u_t = u_{t|t}^*
$$

#### 第四步：滚动
到下一时刻再重新求解。

### 1.5 这个例子说明了什么

它说明：

> MPC 不是一次性把整段控制全部执行完，而是每次都“看未来、算未来、只做一步”。

这和你熟悉的滚动优化、滚动调度完全一致。

---

## 2. 示例 2：带输入/状态约束的线性 MPC（QP）

这个例子进入标准 MPC 形式。

### 2.1 问题描述

仍然考虑一维系统：

$$
x_{k+1} = x_k + u_k
$$

但这次加入约束：

$$
-1 \le u_k \le 1
$$

$$
-5 \le x_k \le 5
$$

目标仍然是让状态接近 0，同时控制动作平滑、不过大。

### 2.2 优化问题

$$
\min \sum_{k=0}^{N-1}(q x_k^2 + r u_k^2) + q_f x_N^2
$$

subject to

$$
x_{k+1} = x_k + u_k
$$

$$
-1 \le u_k \le 1
$$

$$
-5 \le x_k \le 5
$$

### 2.3 Python 代码（CVXPY）

```python
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# ===== 参数 =====
N = 8
T = 25
q = 1.0
r = 0.2
qf = 3.0

u_min, u_max = -1.0, 1.0
x_min, x_max = -5.0, 5.0

x_current = 4.5

x_hist = [x_current]
u_hist = []

for t in range(T):
    x = cp.Variable(N + 1)
    u = cp.Variable(N)

    cost = 0
    constraints = [x[0] == x_current]

    for k in range(N):
        cost += q * cp.square(x[k]) + r * cp.square(u[k])
        constraints += [
            x[k+1] == x[k] + u[k],
            u[k] >= u_min,
            u[k] <= u_max,
            x[k] >= x_min,
            x[k] <= x_max,
        ]

    cost += qf * cp.square(x[N])
    constraints += [x[N] >= x_min, x[N] <= x_max]

    prob = cp.Problem(cp.Minimize(cost), constraints)
    prob.solve(solver=cp.OSQP)

    u_apply = u.value[0]
    x_current = x_current + u_apply

    u_hist.append(u_apply)
    x_hist.append(x_current)

plt.figure(figsize=(8, 4))
plt.plot(x_hist, marker='o')
plt.title("State trajectory - Example 2")
plt.xlabel("time")
plt.ylabel("x")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 4))
plt.step(range(len(u_hist)), u_hist, where='post')
plt.title("Control input - Example 2")
plt.xlabel("time")
plt.ylabel("u")
plt.grid(True)
plt.show()
```

### 2.4 原理解释

这个例子比示例 1 更接近真实工程，因为控制器不仅要“追目标”，还要“守规矩”。

你可以把它理解为：

- 目标函数：想把系统拉回去
- 约束条件：但动作不能太猛，状态不能越界

### 2.5 为什么它是 QP

因为：

#### 系统线性
$$
x_{k+1} = x_k + u_k
$$

#### 目标二次
$$
x_k^2 + u_k^2
$$

#### 约束线性
$$
u_k \in [u_{\min}, u_{\max}], \quad x_k \in [x_{\min}, x_{\max}]
$$

所以整个问题就是标准凸二次规划（QP）。

### 2.6 这个例子的工程意义

这就是工业 MPC 最典型的骨架：

- 动态方程
- 状态/输入约束
- 二次性能指标
- 滚动优化

如果你把状态改成 SOC，把控制改成充放电功率，这已经非常接近储能控制模型。

---

## 3. 示例 3：储能 SOC 控制的简化 MPC

这一节开始贴近你的业务。

### 3.1 问题背景

考虑一个简化储能系统，只做能量平衡，不区分充放电效率细节。

定义：

- \(SOC_k\)：储能荷电状态
- \(P_k\)：储能功率（正值放电，负值充电）
- \(\Delta t\)：时间步长
- \(E\)：储能额定容量

状态方程：

$$
SOC_{k+1} = SOC_k - \frac{\Delta t}{E} P_k
$$

解释：

- 放电 \(P_k > 0\) 时，SOC 下降
- 充电 \(P_k < 0\) 时，SOC 上升

### 3.2 控制目标

假设你的目标不是套利，而是：

> 尽量把 SOC 维持在目标水平附近，同时避免功率动作过大。

例如保持：

$$
SOC^{ref} = 0.5
$$

### 3.3 优化问题

$$
\min \sum_{k=0}^{N-1} \left[ q (SOC_k - SOC^{ref})^2 + r P_k^2 \right] + q_f (SOC_N - SOC^{ref})^2
$$

subject to

$$
SOC_{k+1} = SOC_k - \frac{\Delta t}{E} P_k
$$

$$
SOC_{\min} \le SOC_k \le SOC_{\max}
$$

$$
P_{\min} \le P_k \le P_{\max}
$$

### 3.4 Python 代码（CVXPY）

```python
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# ===== 参数 =====
N = 12
T = 36

dt = 1.0          # 小时
E = 10.0          # 储能容量（MWh）
soc_ref = 0.5

q = 20.0
r = 0.2
qf = 30.0

soc_min, soc_max = 0.2, 0.9
p_min, p_max = -2.0, 2.0   # MW，负为充电，正为放电

soc_current = 0.8

soc_hist = [soc_current]
p_hist = []

for t in range(T):
    soc = cp.Variable(N + 1)
    p = cp.Variable(N)

    cost = 0
    constraints = [soc[0] == soc_current]

    for k in range(N):
        cost += q * cp.square(soc[k] - soc_ref) + r * cp.square(p[k])
        constraints += [
            soc[k+1] == soc[k] - (dt / E) * p[k],
            soc[k] >= soc_min,
            soc[k] <= soc_max,
            p[k] >= p_min,
            p[k] <= p_max,
        ]

    cost += qf * cp.square(soc[N] - soc_ref)
    constraints += [soc[N] >= soc_min, soc[N] <= soc_max]

    prob = cp.Problem(cp.Minimize(cost), constraints)
    prob.solve(solver=cp.OSQP)

    p_apply = p.value[0]
    soc_current = soc_current - (dt / E) * p_apply

    p_hist.append(p_apply)
    soc_hist.append(soc_current)

plt.figure(figsize=(8, 4))
plt.plot(soc_hist, marker='o')
plt.axhline(soc_ref, linestyle='--')
plt.title("SOC trajectory - Example 3")
plt.xlabel("time")
plt.ylabel("SOC")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 4))
plt.step(range(len(p_hist)), p_hist, where='post')
plt.title("Battery power - Example 3")
plt.xlabel("time")
plt.ylabel("P_batt")
plt.grid(True)
plt.show()
```

### 3.5 原理解释

这个例子已经能让你把 MPC 和储能系统对应起来。

#### 状态
$$
x_k = SOC_k
$$

#### 控制
$$
u_k = P_k
$$

#### 动态
$$
SOC_{k+1} = SOC_k - \frac{\Delta t}{E}P_k
$$

#### 目标
让 SOC 保持在合理目标附近，不要过度充放电。

### 3.6 为什么这个例子重要

因为它已经是你后面做虚拟电厂 MPC 的最小原型：

- 把 SOC 当状态
- 把储能功率当控制
- 把功率上下限、SOC 上下限当约束
- 用滚动优化持续更新

### 3.7 与真实储能调度的差别

真实业务中通常还会继续加入：

- 充放电效率 \(\eta_c, \eta_d\)
- 电价预测
- 负荷预测
- 光伏/风电预测
- 买电 / 卖电约束
- 电池退化成本
- 充放电互斥约束
- 市场规则约束

也就是说，示例 3 是真实电力 MPC 的“教学版原型”。

---

## 4. 3 个示例之间的递进关系

### 示例 1
理解最基本的“滚动优化”思想。

### 示例 2
理解 MPC 如何处理约束，以及为何是标准 QP。

### 示例 3
开始把 MPC 映射到储能系统和能源调度。

---

## 5. 代码实现中的几个关键注意点

### 5.1 只执行第一步
MPC 和一次性全局规划最重要的区别，就是每次只执行第一个动作。

### 5.2 当前状态必须是实时更新的
每次求解都要用新的测量值或状态估计值。

### 5.3 预测窗长度 N 影响很大
- 太短：策略短视
- 太长：计算慢

工程中通常要在性能与计算时间之间折中。

### 5.4 权重 \(Q, R, Q_f\) 需要调参
这是 MPC 落地中的关键工作之一。

例如：

- 增大 \(Q\)：更强调状态跟踪
- 增大 \(R\)：更抑制动作过大
- 增大 \(Q_f\)：更关心预测窗终点状态

### 5.5 OSQP 很适合这类线性二次 MPC
对于线性 MPC，`OSQP + CVXPY` 是很好的入门组合：

- 容易写
- 足够快
- 稳定
- 适合原型开发

---

## 6. 本部分小结

通过这 3 个例子，你应该已经建立起下面这个映射：

- **MPC 不是玄学控制器**
- 它本质就是：
  - 写出动态方程
  - 写出目标函数
  - 写出约束
  - 每个时刻滚动求解

对于你来说，这和多阶段优化 / 滚动调度非常接近，只是多了“状态递推”和“闭环更新”。

---

## Part 4 对应下载链接（页面中曾提供）

- [下载 MPC 工程版文档（Part1~Part4）](sandbox:/mnt/data/mpc_engineering_doc_part1_4.md)

---

# Part 5：虚拟电厂 / 电力市场交易中的 MPC 示例（核心）

这一部分是整篇文档最关键的部分：  
我们把 MPC **真正落到虚拟电厂（VPP）+ 电力市场交易场景**。

---

## 1. 场景定义（贴近你业务）

考虑一个典型虚拟电厂场景：

系统包含：

- 储能（Battery）
- 负荷（Load）
- 电网（Grid）

已知：

- 负荷预测：\(\hat{L}_k\)
- 电价预测：\(\hat{\pi}_k\)

目标：

> 在满足设备约束的前提下，**最小化购电成本（或最大化套利收益）**

---

## 2. 模型构建（完整 MPC 结构）

### 2.1 状态变量

$$
x_k = SOC_k
$$

### 2.2 控制变量

$$
u_k = P_k^{batt}
$$

约定：

- \(P_k > 0\)：放电
- \(P_k < 0\)：充电

### 2.3 外生变量（预测）

$$
d_k = [\hat{L}_k, \hat{\pi}_k]
$$

### 2.4 状态方程

$$
SOC_{k+1} = SOC_k - \frac{\Delta t}{E} P_k
$$

### 2.5 功率平衡（关键）

$$
P_k^{grid} = \hat{L}_k - P_k
$$

解释：

- 负荷需要供电
- 储能放电可以减少购电
- 储能充电会增加购电

---

## 3. 目标函数（电力核心）

目标：最小化购电成本

$$
\min \sum_{k=0}^{N-1} \hat{\pi}_k \cdot P_k^{grid} \cdot \Delta t
$$

展开：

$$
= \sum \hat{\pi}_k (\hat{L}_k - P_k)
$$

进一步：

$$
= \sum \hat{\pi}_k \hat{L}_k - \sum \hat{\pi}_k P_k
$$

因为第一项是常数，可以忽略：

$$
\min - \sum \hat{\pi}_k P_k
$$

等价于：

$$
\max \sum \hat{\pi}_k P_k
$$

这就是：

> **低价充电，高价放电**

### 3.1 加入工程项（非常重要）

实际模型不会只考虑收益，还会加入：

#### SOC 安全项

$$
\lambda_1 (SOC_k - SOC^{ref})^2
$$

#### 平滑项

$$
\lambda_2 (P_k - P_{k-1})^2
$$

### 3.2 完整目标函数

$$
\min \sum_{k=0}^{N-1} \left[
- \hat{\pi}_k P_k
+ \lambda_1 (SOC_k - SOC^{ref})^2
+ \lambda_2 (P_k - P_{k-1})^2
\right]
$$

---

## 4. 约束系统

### 4.1 SOC 约束

$$
SOC_{\min} \le SOC_k \le SOC_{\max}
$$

### 4.2 功率约束

$$
P_{\min} \le P_k \le P_{\max}
$$

### 4.3 可选：终端约束

$$
SOC_N \ge SOC_{\text{target}}
$$

避免“把电池用空”。

---

## 5. Python 实现（核心代码）

```python
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# ===== 参数 =====
N = 24      # 预测时域（小时）
T = 48      # 仿真时长

dt = 1.0
E = 20.0

soc_min, soc_max = 0.2, 0.9
p_min, p_max = -5.0, 5.0

soc_ref = 0.5

lambda_soc = 5.0
lambda_smooth = 1.0

# 初始状态
soc_current = 0.6
p_prev = 0.0

soc_hist = [soc_current]
p_hist = []

# 构造预测数据（示例）
np.random.seed(0)
price = 0.5 + 0.5 * np.sin(np.linspace(0, 4*np.pi, T+N))
load = 10 + 2 * np.sin(np.linspace(0, 2*np.pi, T+N))

for t in range(T):
    # 取未来预测
    price_pred = price[t:t+N]
    load_pred = load[t:t+N]

    soc = cp.Variable(N + 1)
    p = cp.Variable(N)

    cost = 0
    constraints = [soc[0] == soc_current]

    for k in range(N):
        # 成本：电价 + SOC + 平滑
        cost += (
            - price_pred[k] * p[k]
            + lambda_soc * cp.square(soc[k] - soc_ref)
            + lambda_smooth * cp.square(p[k] - (p_prev if k == 0 else p[k-1]))
        )

        constraints += [
            soc[k+1] == soc[k] - (dt / E) * p[k],
            soc[k] >= soc_min,
            soc[k] <= soc_max,
            p[k] >= p_min,
            p[k] <= p_max,
        ]

    # 终端约束
    constraints += [soc[N] >= soc_min]

    prob = cp.Problem(cp.Minimize(cost), constraints)
    prob.solve(solver=cp.OSQP)

    # 执行第一步
    p_apply = p.value[0]
    soc_current = soc_current - (dt / E) * p_apply

    p_prev = p_apply

    p_hist.append(p_apply)
    soc_hist.append(soc_current)

# ===== 可视化 =====
plt.figure(figsize=(8,4))
plt.plot(soc_hist)
plt.title("SOC trajectory (VPP MPC)")
plt.grid()
plt.show()

plt.figure(figsize=(8,4))
plt.plot(p_hist)
plt.title("Battery power (VPP MPC)")
plt.grid()
plt.show()
```

---

## 6. 原理解释（非常关键）

这个模型已经完整体现了：

### 6.1 MPC + 电价预测
- 未来电价作为“扰动输入”
- MPC 利用预测做决策

本质就是：

> 用预测驱动优化

### 6.2 MPC vs 日前优化

#### 日前优化
- 一次性算 24h
- 不更新
- 对预测误差敏感

#### MPC
- 每小时重算
- 自动修正
- 鲁棒性强

### 6.3 MPC 在 VPP 的作用

核心就是：

> **实时滚动调度 + 预测驱动决策**

---

## 7. 可以进一步扩展的方向（你后面可以做）

你可以把这个模型继续升级：

### 7.1 加入充放电效率

$$
SOC_{k+1} = SOC_k + \eta_c P^{ch} - \frac{1}{\eta_d}P^{dis}
$$

### 7.2 买卖电分离（避免套利漏洞）
引入：
- \(P^{buy}\)
- \(P^{sell}\)

### 7.3 加入光伏 / 风电

$$
P^{grid} = L - PV - Wind - P^{batt}
$$

### 7.4 加入电池退化成本

$$
\lambda_{deg} |P_k|
$$

### 7.5 加入市场规则（现货、电价分段）

---

## 8. 本部分总结

这一部分你应该掌握：

- 如何把 MPC 映射到电力系统
- 如何构建目标函数（收益 + 安全 + 平滑）
- 如何处理预测信息
- 如何实现滚动优化

最关键的一句话：

> **MPC = 预测 + 优化 + 实时闭环调度**

---

## Part 5 对应下载链接（页面中曾提供）

- [下载 MPC 工程版文档（Part1~Part5）](sandbox:/mnt/data/mpc_engineering_doc_full_part1_5.md)

---

# Part 6：时间序列预测（TS）+ MPC 融合（工程落地核心）

这一部分把你已有的能力（时间序列 + 优化）与 MPC 真正打通，形成**可落地的生产级架构**。

---

## 1. TS → MPC 的接口设计

### 1.1 预测输出如何进入 MPC

在每个时刻 t，你的 TS 模型需要输出：

- 负荷预测：\(\hat{L}_{t:t+N-1}\)
- 电价预测：\(\hat{\pi}_{t:t+N-1}\)
- 可再生预测（可选）：\(\hat{P}^{PV}_{t:t+N-1}\), \(\hat{P}^{wind}_{t:t+N-1}\)

这些序列直接作为 MPC 的**外生参数（parameters）**进入目标函数与约束。

### 1.2 时间尺度对齐（关键）

- 控制步长：\(\Delta t\)（如 5min / 15min / 1h）
- 预测步长：需与控制步长一致或可对齐
- 预测窗：\(N\)

常见做法：

- TS 输出与 MPC 同步（推荐）
- 或 TS 输出更细粒度，再做聚合/重采样

### 1.3 数据接口（工程）

```python
def get_forecast(t, N):
    price_pred = price_model.predict(t, horizon=N)
    load_pred = load_model.predict(t, horizon=N)
    return price_pred, load_pred
```

---

## 2. 预测误差对 MPC 的影响

### 2.1 确定性 MPC（Deterministic MPC）

默认假设：

$$
\hat{d}_k = d_k
$$

问题：
- 预测误差会导致次优甚至违约（如 SOC 越界）

### 2.2 常见改进方法

#### 方法 A：滚动更新（最常用）

每步更新预测：

$$
\text{MPC: } \hat{d}_{t:t+N-1} \leftarrow \text{TS}(t)
$$

这是你当前最实用的方法（简单有效）。

#### 方法 B：安全裕度（buffer）

对关键约束加 buffer：

$$
SOC_{\min} \to SOC_{\min} + \delta
$$

$$
P_{\max} \to P_{\max} - \delta
$$

#### 方法 C：场景法（Scenario MPC）

对多个预测场景求解：

$$
\min \mathbb{E}[J] \quad \text{or} \quad \min \text{CVaR}
$$

这与你熟悉的风险优化一致。

#### 方法 D：鲁棒 MPC（Robust MPC）

约束对所有扰动成立：

$$
x_k \in \mathcal{X}, \forall d_k \in \mathcal{D}
$$

更保守，但更安全。

---

## 3. 两种主流工程架构

### 架构 A：两阶段（工业主流）

```text
TS模型 → 预测 → MPC优化 → 执行
```

优点：
- 模块清晰
- 易维护
- 可替换 TS 或 MPC

缺点：
- 未考虑预测误差的反馈

### 架构 B：联合优化（进阶）

```text
TS + MPC 联合建模（端到端）
```

例如：
- 用概率预测（分布）
- MPC 直接优化期望或风险

优点：
- 理论更优
- 可控风险

缺点：
- 实现复杂
- 工程难度高

---

## 4. 推荐工程架构（你可以直接用）

### 4.1 在线循环

```python
for t in range(T):

    # 1. 状态获取
    x_t = measure_state()

    # 2. 预测
    price_pred, load_pred = get_forecast(t, N)

    # 3. 构建 MPC
    problem = build_mpc(x_t, price_pred, load_pred)

    # 4. 求解
    u_seq = solve(problem)

    # 5. 执行
    apply(u_seq[0])
```

### 4.2 模块划分

- data layer（数据）
- forecast layer（TS）
- optimization layer（MPC）
- control layer（执行）

---

## 5. 你可以做的项目级升级

### 5.1 储能套利 MPC（升级版）
- 加入 TOU / 现货价格
- 加入充放电效率
- 加入退化成本

### 5.2 虚拟电厂聚合 MPC

状态扩展：

$$
x = [SOC_1, SOC_2, ..., flexible load]
$$

控制：

$$
u = [P_1, P_2, ..., DR]
$$

### 5.3 风光储一体 MPC

$$
P^{grid} = L - PV - Wind - P^{batt}
$$

### 5.4 风险感知 MPC（进阶）
- CVaR
- chance constraint

---

## 6. 你当前能力的“升级路径”

你现在：

- TS 很强
- 优化很强

缺的是：

- 闭环控制思维

关键升级：

### 从：
> “预测 → 优化一次”

### 到：
> “预测 → 滚动优化 → 闭环修正”

---

## 7. 最终总结

整套体系可以总结为：

> **MPC = 时间序列预测 + 多阶段优化 + 在线闭环控制**

如果你把这套东西跑通，你会具备：

- 电力系统实时调度能力
- 储能控制能力
- VPP策略优化能力
- 预测+优化一体能力（行业稀缺）

---

## 完整文档链接（页面中曾提供）

- [下载 MPC 工程完整版文档](sandbox:/mnt/data/mpc_engineering_full.md)

---

# 工程项目：完整储能 MPC 项目（工程版）

用户随后要求：

> 做一个完整储能 MPC 项目（工程版）

因此页面中进一步生成了项目源码与压缩包。

---

## 第一版项目下载链接

- [储能 MPC 工程项目源码目录](sandbox:/mnt/data/storage_mpc_project)
- [储能 MPC 工程项目压缩包](sandbox:/mnt/data/storage_mpc_project.zip)

### 项目说明（页面原文整理）

项目里包含：
- `README.md`
- `configs/default_config.json`
- `src/storage_mpc/mpc_controller.py`
- `src/storage_mpc/simulator.py`
- `src/storage_mpc/forecaster.py`
- `src/storage_mpc/data_generator.py`
- `src/storage_mpc/plotting.py`
- `scripts/run_simulation.py`

可直接运行：

```bash
python scripts/run_simulation.py
```

特点：
- 支持负荷预测、电价预测输入
- 支持 SOC / 功率约束
- 支持功率平滑项
- 默认不允许反送电
- 适合后续扩展为：
  - 充放电效率版
  - 退化成本版
  - 现货 / 分时电价版
  - 风光储 / VPP 聚合版

---

# 工程项目升级：V2

随后项目升级为更贴近业务的版本。

## V2 下载链接

- [储能 MPC 工程项目 V2 源码目录](sandbox:/mnt/data/storage_mpc_project_v2)
- [储能 MPC 工程项目 V2 压缩包](sandbox:/mnt/data/storage_mpc_project_v2.zip)

## V2 的核心升级点

- 充电 / 放电功率分离
- 充放电效率
- 买电 / 卖电分离
- 光伏输入接口
- 电池退化近似成本
- 更清晰的功率平衡方程

核心建模：

$$
SOC_{k+1} = SOC_k + \frac{\eta_c \Delta t}{E} P_k^{ch} - \frac{\Delta t}{\eta_d E} P_k^{dis}
$$

$$
P_k^{buy} - P_k^{sell} + P_k^{dis} - P_k^{ch} + P_k^{pv} = P_k^{load}
$$

目标函数同时考虑：
- 买电成本
- 售电收益
- SOC 安全
- 退化成本
- 控制平滑
- 终端 SOC

---

# 工程项目升级：V3

用户继续要求升级，于是项目进入更接近真实交易约束的 V3。

## V3 下载链接

- [储能 MPC 工程项目 V3 源码目录](sandbox:/mnt/data/storage_mpc_project_v3)
- [储能 MPC 工程项目 V3 压缩包](sandbox:/mnt/data/storage_mpc_project_v3.zip)

## V3 新增能力

- 充放电互斥二进制变量开关
- 需量惩罚（峰值购电惩罚）
- 偏差考核成本
- 真实预测器接口模板
- 多资源聚合骨架
- 更接近交易策略的配置化结构

互斥约束：

$$
P_k^{ch} \le z_k P_{max}^{ch}, \quad
P_k^{dis} \le (1-z_k) P_{max}^{dis}
$$

需量惩罚：

$$
P_k^{buy} \le P^{peak}, \quad \lambda_{peak} P^{peak}
$$

偏差考核：

$$
\lambda_{dev}(P_k^{buy}-P_k^{plan})^2
$$

---

# 工程项目升级：V4（三层调度）

最后，项目升级为 V4：三层调度架构。

## V4 下载链接

- [储能 / 虚拟电厂 MPC 工程项目 V4 源码目录](sandbox:/mnt/data/storage_mpc_project_v4)
- [储能 / 虚拟电厂 MPC 工程项目 V4 压缩包](sandbox:/mnt/data/storage_mpc_project_v4.zip)

## V4 的核心升级

这次的核心升级不是加几个约束，而是把项目架构升级成了**三层调度**：

- 日前计划层 `day_ahead_planner.py`
- 日内修正层 `intra_day_planner.py`
- 实时执行层 `real_time_mpc.py`

新增的关键文件有：
- `src/storage_mpc/day_ahead_planner.py`
- `src/storage_mpc/intra_day_planner.py`
- `src/storage_mpc/real_time_mpc.py`
- `src/storage_mpc/hierarchical_simulator.py`

运行入口：

```bash
python scripts/run_simulation.py
```

运行后会输出：

- `results/day_ahead_plan.csv`
- `results/intra_day_plan_trace.csv`
- `results/real_time_results.csv`
- `results/soc_trajectory.png`
- `results/power_dispatch.png`
- `results/cost_overview.png`

这个版本已经更接近真实业务里的组织方式：

$$
\text{日前预测} \rightarrow \text{日前计划}
$$

$$
\text{日内更新预测} \rightarrow \text{修正计划}
$$

$$
\text{实时状态反馈} \rightarrow \text{MPC闭环执行}
$$

也就是说，它已经从“单层控制 demo”升级成了“多时间尺度协调调度”的工程骨架。

---

# 页面中后续生成过的文档链接（按时间整理）

以下是页面里出现过的与 MPC 文档相关的下载链接，按时间整理保留：

## 基础与中间版文档
- [下载 MPC 工程版文档（Part1~Part3）](sandbox:/mnt/data/mpc_engineering_doc_part1_3.md)
- [下载 MPC 工程版文档（Part1~Part4）](sandbox:/mnt/data/mpc_engineering_doc_part1_4.md)
- [下载 MPC 工程版文档（Part1~Part5）](sandbox:/mnt/data/mpc_engineering_doc_full_part1_5.md)
- [下载 MPC 工程完整版文档](sandbox:/mnt/data/mpc_engineering_full.md)

## 中途整理版 / 汇总版文档
- [下载 Markdown 文档](sandbox:/mnt/data/storage_mpc_v4_report.md)
- [下载 PDF 文档](sandbox:/mnt/data/storage_mpc_v4_report.pdf)
- [下载 Markdown 文档](sandbox:/mnt/data/storage_mpc_v4_high_quality.md)
- [下载 PDF 文档](sandbox:/mnt/data/storage_mpc_v4_high_quality.pdf)
- [下载 Markdown 文档](sandbox:/mnt/data/MPC_full_report.md)
- [下载 PDF 文档](sandbox:/mnt/data/MPC_full_report.pdf)
- [下载 Markdown](sandbox:/mnt/data/MPC_structured_full.md)
- [下载 PDF](sandbox:/mnt/data/MPC_structured_full.pdf)
- [完整 Markdown 文档](sandbox:/mnt/data/MPC_complete_engineering_report.md)
- [完整 PDF 文档](sandbox:/mnt/data/MPC_complete_engineering_report.pdf)
- [完整 Markdown 文档](sandbox:/mnt/data/MPC_research_full_conversation_compiled.md)
- [完整 PDF 文档](sandbox:/mnt/data/MPC_research_full_conversation_compiled.pdf)

> 注：上述多个文档是页面中不同阶段的中间结果与汇总结果。你当前正在看的这份文档，是按照你的最新要求，把页面中从 Part 1 开始到后续工程实现的内容重新汇总成一份 Markdown。

---

# 页面中还出现过的简短补充代码与说明

在后续对话中，页面还补充过一段关于“为什么之前文档没有 Python 示例”的说明，并给出了一些片段级代码。这里一并保留。

---

## 最简单 MPC（无约束）补充片段

```python
import cvxpy as cp
import numpy as np

N = 10  # horizon
x0 = 5.0
x_ref = 0.0

x = cp.Variable(N+1)
u = cp.Variable(N)

cost = 0
constraints = [x[0] == x0]

for k in range(N):
    cost += cp.square(x[k] - x_ref) + cp.square(u[k])
    constraints += [
        x[k+1] == x[k] + u[k]
    ]

prob = cp.Problem(cp.Minimize(cost), constraints)
prob.solve()

print("u0 =", u.value[0])
```

---

## 带约束 MPC 补充片段

```python
u_min, u_max = -1, 1

constraints += [
    u[k] >= u_min,
    u[k] <= u_max
]
```

---

## 滚动 MPC（闭环）补充片段

```python
x = x0

for t in range(T):

    # 1. solve MPC
    u_seq = solve_mpc(x)

    # 2. apply first control
    u = u_seq[0]

    # 3. system update
    x = x + u
```

---

## 储能 MPC 的关键代码片段补充

### 状态与控制

```python
soc = cp.Variable(N+1)
p_ch = cp.Variable(N)
p_dis = cp.Variable(N)
```

### 状态方程

```python
soc[k+1] == soc[k] + eta_c * p_ch[k] - p_dis[k] / eta_d
```

### 功率平衡

```python
p_buy[k] - p_sell[k] + p_dis[k] - p_ch[k] + pv[k] == load[k]
```

### 目标函数

```python
cost += price[k] * p_buy[k]
cost += lambda_soc * cp.square(soc[k] - soc_ref)
```

---

## TS + MPC 融合的关键代码片段补充

```python
load_pred = model.predict()
price_pred = price_model.predict()

u = mpc.solve(load_pred, price_pred)
```

---

# 最终总结（页面内容整理版）

本次对话中，从最初的 MPC 原理解释，到数学建模、代码示例、储能场景建模，再到 TS + OR + MPC 的融合，以及最终的 V1 ~ V4 工程项目演进，实际已经形成了一条非常清晰的知识主线：

## 主线 1：MPC 的本质
> **MPC = 预测 + 优化 + 只执行一步 + 滚动更新**

## 主线 2：MPC 的数学表达
> **线性系统 + 二次目标 + 线性约束 ⇒ QP**  
> **非线性系统 / 非线性约束 ⇒ NLP / NMPC**

## 主线 3：MPC 与能源场景的映射
- 状态 → SOC
- 控制 → 充放电功率
- 预测 → 负荷 / 电价 / 光伏 / 风电
- 约束 → 功率 / SOC / 市场规则

## 主线 4：你的能力升级路径
从：

```text
时间序列预测 + 运筹优化
```

升级为：

```text
时间序列预测 + 多阶段优化 + MPC 闭环控制
```

## 主线 5：工程落地路径
- V1：单层基础 MPC
- V2：引入效率、买卖电、光伏、退化
- V3：引入互斥逻辑、峰值惩罚、偏差考核
- V4：构建日前 + 日内 + 实时三层调度

因此，本次会话的全部 MPC 内容，最终可以概括为：

> **MPC 在能源系统中的真实价值，不只是“控制算法”，而是一套把预测、优化、约束、市场规则与实时执行统一起来的工程系统方法。**
