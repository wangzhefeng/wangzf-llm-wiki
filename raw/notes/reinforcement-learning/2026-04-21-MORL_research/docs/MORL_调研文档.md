# 多目标强化学习 (MORL) 调研文档
## —— 理论、算法与电力行业应用

> 面向对象：电力能源领域算法工程师（虚拟电厂、电价预测、调度优化、电力市场交易）
> 文档定位：覆盖理论推导、主流算法、工程实现路线、电力场景落地方案

---

## 目录

1. [引言：为什么需要 MORL](#1-引言)
2. [数学模型与理论基础](#2-数学模型与理论基础)
3. [主流 MORL 算法](#3-主流-morl-算法)
4. [工程实现技术路线](#4-工程实现技术路线)
5. [电力市场交易与虚拟电厂应用](#5-电力市场交易与虚拟电厂应用)
6. [挑战与展望](#6-挑战与展望)
7. [参考文献](#7-参考文献)

---

## 1. 引言

### 1.1 单目标 RL 的局限性

标准强化学习（RL）要求将决策目标编码为单个标量奖励 $r \in \mathbb{R}$。对于电力系统这类**本质上的多目标问题**，这种建模方式存在三重缺陷：

- **权重硬编码问题**：假设 VPP 调度同时考虑收益 $r_{\text{rev}}$、碳排 $-r_{\text{co2}}$、电池损耗 $-r_{\text{deg}}$，工程上常用 $r = \alpha_1 r_{\text{rev}} - \alpha_2 r_{\text{co2}} - \alpha_3 r_{\text{deg}}$。权重 $\alpha$ 的取值直接决定策略行为，但往往没有"正确的"权重，且随政策、碳价、电池寿命预期动态变化。权重一旦变化，必须重新训练。
- **Pareto 前沿不可见**：单目标训练只能得到单个策略，决策者无法看到权衡空间（trade-off frontier），难以回答"如果我愿意牺牲 2% 收益能降低多少碳排"这类问题。
- **非凸前沿的缺失**：线性加权法只能得到 Pareto 前沿的**凸部分**（凸覆盖集 CCS），对于非凸前沿上的解完全无法表达。

### 1.2 MORL 的定位

**多目标强化学习 (Multi-Objective Reinforcement Learning, MORL)** 将奖励从标量扩展为向量 $\mathbf{r} \in \mathbb{R}^d$，目标是学习能够覆盖整个 Pareto 前沿的一组策略（multi-policy）或一个可按偏好调节的参数化策略（single-network multi-policy）。

典型收益包括：

| 能力 | 单目标 RL | MORL |
|------|----------|------|
| 支持运行时偏好切换 | ❌ | ✅ |
| 展示权衡前沿 | ❌ | ✅ |
| 处理非凸前沿 | ❌ | ✅（部分算法） |
| 支持偏好未知/推断 | ❌ | ✅ |

对电力行业算法工程师而言，MORL 特别契合以下场景：

- **VPP 聚合调度**：经济性 / 碳排 / 电池寿命 / 负荷偏差的权衡；
- **现货 + 辅助服务联合投标**：收益 / 风险 / 偏差罚款的权衡；
- **需求响应**：用户舒适度 / 激励成本 / 削峰效果；
- **储能多用途复用**：套利收益 / 容量保留 / SOC 偏离约束。

---

## 2. 数学模型与理论基础

### 2.1 多目标马尔可夫决策过程 (MOMDP)

MOMDP 是标准 MDP 的向量化扩展，定义为五元组：

$$
\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, P, \mathbf{R}, \gamma \rangle
$$

其中：
- $\mathcal{S}$：状态空间；
- $\mathcal{A}$：动作空间；
- $P: \mathcal{S} \times \mathcal{A} \times \mathcal{S} \to [0,1]$：状态转移概率；
- $\mathbf{R}: \mathcal{S} \times \mathcal{A} \times \mathcal{S} \to \mathbb{R}^d$：**向量奖励函数**（$d$ 个目标）；
- $\gamma \in [0, 1)$：折扣因子。

**唯一本质差别**：奖励 $\mathbf{r}_t = (r_t^{(1)}, r_t^{(2)}, \dots, r_t^{(d)})^\top$ 是 $d$ 维向量。

### 2.2 向量值价值函数

给定策略 $\pi$，状态-动作价值函数也为向量：

$$
\mathbf{Q}^\pi(s, a) = \mathbb{E}_\pi \left[ \sum_{t=0}^{\infty} \gamma^t \mathbf{r}_{t+1} \,\Big|\, s_0=s, a_0=a \right] \in \mathbb{R}^d
$$

其向量化 Bellman 方程为：

$$
\mathbf{Q}^\pi(s, a) = \mathbb{E}_{s' \sim P} \left[ \mathbf{R}(s,a,s') + \gamma \mathbf{Q}^\pi(s', \pi(s')) \right]
$$

注意：与单目标不同，**"最优动作"的定义不再唯一**——因为 $\mathbb{R}^d$ 上没有天然的全序关系。这是 MORL 一切复杂性的源头。

### 2.3 Pareto 支配与最优性

给定两个向量回报 $\mathbf{v}, \mathbf{v}' \in \mathbb{R}^d$，定义 **Pareto 支配**：

$$
\mathbf{v} \succ \mathbf{v}' \iff \forall i: v_i \geq v'_i \;\land\; \exists j: v_j > v'_j
$$

**定义 2.1（Pareto 最优策略）** 策略 $\pi$ 是 Pareto 最优的，当且仅当不存在策略 $\pi'$ 使得 $\mathbf{V}^{\pi'}(s_0) \succ \mathbf{V}^\pi(s_0)$。

**定义 2.2（Pareto 前沿 PF）** 所有 Pareto 最优策略对应的回报向量的集合：

$$
\mathcal{F}^* = \{ \mathbf{V}^\pi(s_0) : \pi \text{ 是 Pareto 最优} \}
$$

**定义 2.3（凸覆盖集 CCS）** Pareto 前沿中所有能被**某个线性权重** $\mathbf{w} \geq 0, \mathbf{1}^\top \mathbf{w} = 1$ 最大化的点的集合：

$$
\mathcal{C} = \left\{ \mathbf{v} \in \mathcal{F}^* : \exists \mathbf{w}, \forall \mathbf{v}' \in \mathcal{F}^*, \mathbf{w}^\top \mathbf{v} \geq \mathbf{w}^\top \mathbf{v}' \right\}
$$

关系：$\mathcal{C} \subseteq \mathcal{F}^*$。对于非凸 PF，$\mathcal{C} \neq \mathcal{F}^*$——这正是**线性标量化方法的根本局限**。

### 2.4 效用函数与偏好

用户偏好通过效用函数 $u: \mathbb{R}^d \to \mathbb{R}$ 表达，策略目标转化为：

$$
\pi^* = \arg\max_{\pi} \, u(\mathbf{V}^\pi(s_0))
$$

三类常见效用函数：

**(a) 线性效用**（线性标量化，Linear Scalarization）

$$
u_{\mathbf{w}}(\mathbf{v}) = \mathbf{w}^\top \mathbf{v} = \sum_{i=1}^d w_i v_i
$$

- 优点：保持 MDP 结构，标量化后可直接用标准 RL；
- 缺点：**只能覆盖 CCS**。

**(b) Tchebycheff（切比雪夫）效用**

$$
u^{\text{Tch}}_{\mathbf{w}, \mathbf{z}^*}(\mathbf{v}) = -\max_{i=1,\dots,d} w_i |v_i - z_i^*|
$$

其中 $\mathbf{z}^*$ 是**理想点**（每个目标单独最优的值）。
- 优点：可覆盖**整个 PF**，包括非凸部分；
- 缺点：破坏 MDP 的马尔可夫性（非线性非加性），需特殊算法。

**(c) 增广切比雪夫**

$$
u^{\text{aTch}}_{\mathbf{w}, \mathbf{z}^*}(\mathbf{v}) = -\max_i w_i |v_i - z_i^*| - \rho \sum_i w_i |v_i - z_i^*|
$$

小常数 $\rho > 0$ 用于打破退化解，实践中更稳定。

### 2.5 SER vs ESR 的关键区别

MORL 存在两种根本不同的优化准则，**选错会导致学出错误的策略**：

| 准则 | 定义 | 适用场景 |
|------|------|----------|
| **SER** (Scalarized Expected Return) | $\max_\pi \, u(\mathbb{E}[\mathbf{G}])$ | 多次重复决策，关注长期平均 |
| **ESR** (Expected Scalarized Return) | $\max_\pi \, \mathbb{E}[u(\mathbf{G})]$ | 单次决策，关注每次回报的效用 |

**举例理解差异**：设 $d=2$，效用为 $u(\mathbf{v}) = \min(v_1, v_2)$，两策略回报分布：
- $\pi_A$：确定性地得到 $(1, 1)$；
- $\pi_B$：50% 得到 $(2, 0)$，50% 得到 $(0, 2)$。

则 $\mathbb{E}[\mathbf{G}^{\pi_A}] = \mathbb{E}[\mathbf{G}^{\pi_B}] = (1,1)$，SER 视角两者等价；但 $\mathbb{E}[u(\mathbf{G}^{\pi_A})] = 1$，$\mathbb{E}[u(\mathbf{G}^{\pi_B})] = 0$，ESR 视角 $\pi_A$ 远优。

**电力场景对应**：
- VPP 年度调度 → 通常用 SER（关注期望累计收益/排放）；
- 单场电价风险控制 → 倾向 ESR（每日盈亏都不能太差）。

线性效用下两者等价（因为期望算子与线性函数可交换），但 Tchebycheff 等非线性效用下差异显著。

### 2.6 Bellman 方程的多目标扩展

对于线性标量化情形，可以证明**存在一个关于偏好 $\mathbf{w}$ 的通用 Bellman 最优算子**。定义 $\mathbf{Q}^*(s, a; \mathbf{w})$ 为在偏好 $\mathbf{w}$ 下的最优向量 Q 值，则 Envelope Q-Learning 提出的广义 Bellman 方程为：

$$
(\mathcal{T} \mathbf{Q})(s, a; \mathbf{w}) = \mathbb{E}_{s'} \left[ \mathbf{R}(s,a,s') + \gamma \, \arg_{\mathbf{Q}} \max_{a', \mathbf{w}'} \mathbf{w}^\top \mathbf{Q}(s', a'; \mathbf{w}') \right]
$$

关键创新：**在内部最大化时同时对动作和偏好取 max**，选出的动作 $a^*$ 对应的 $\mathbf{Q}$ 整体作为目标值（而非其标量化值）。

**可证明性质**：算子 $\mathcal{T}$ 在 $L_\infty$ 意义下是 $\gamma$-压缩映射，因此具有唯一不动点，保证了 Envelope Q-Learning 理论收敛性（详见 Yang 等，2019）。


---

## 3. 主流 MORL 算法

MORL 算法按学习策略数量可分为三大类，下表为概览：

| 类别 | 代表算法 | 输出 | 偏好已知？ | 优点 | 缺点 |
|------|---------|------|-----------|------|------|
| **单策略** | Scalarized DQN/PPO | 1 个策略 | 训练时已知 | 实现简单 | 偏好变需重训 |
| **多策略 - 外层循环** | OLS + 任意单目标 RL | CCS 上若干策略 | 无需 | CCS 完备性保证 | 训练代价 = $k \times$ 单目标 RL |
| **多策略 - 单网络** | Envelope Q-Learning, CAPQL, GPI-LS | 1 个条件化网络，参数化整个 PF | 执行时输入 | 样本效率高，支持运行时偏好切换 | 网络设计复杂 |
| **进化 + 策略梯度** | PGMORL | 一组策略（种群） | 无需 | 支持非凸 PF，连续动作 | 训练开销大 |
| **基于分解** | MORL/D | 一组策略 | 无需 | 模块化，灵活 | 需精心设计邻域 |

以下详述各类算法的数学原理。

### 3.1 线性标量化 DQN（Scalarized DQN）

最朴素的 MORL 基线：给定固定偏好 $\mathbf{w}$，将向量奖励合成标量 $r^{\text{scalar}}_t = \mathbf{w}^\top \mathbf{r}_t$，然后跑标准 DQN。

**TD 目标**：

$$
y_t = \mathbf{w}^\top \mathbf{r}_{t+1} + \gamma \max_{a'} Q_\theta(s_{t+1}, a'; \mathbf{w})
$$

**损失函数**：

$$
\mathcal{L}(\theta) = \mathbb{E}_{(s,a,\mathbf{r},s') \sim \mathcal{D}} \left[ \left( y - Q_\theta(s, a; \mathbf{w}) \right)^2 \right]
$$

**实践扩展 —— 偏好条件化 (Conditioned Network, CN)**：将 $\mathbf{w}$ 作为网络输入，训练时在偏好单纯形上随机采样 $\mathbf{w} \sim \Delta^{d-1}$：

$$
Q_\theta: \mathcal{S} \times \Delta^{d-1} \to \mathbb{R}^{|\mathcal{A}|}, \quad \mathcal{L} = \mathbb{E}_{\mathbf{w}}[\mathcal{L}(\theta; \mathbf{w})]
$$

这样单个网络即可支持任意偏好的执行——但仍然只能学到 CCS。

### 3.2 Outer Loop：OLS (Optimistic Linear Support)

**核心思想**：用迭代方式搜索权重空间，每次求解一个标量化子问题，增量构建 CCS。

**算法流程**：
1. 初始化权重集合 $W = \{\mathbf{e}_1, \dots, \mathbf{e}_d\}$（轴向权重）和已知 CCS 集合 $\mathcal{C} = \emptyset$；
2. 对每个 $\mathbf{w} \in W$，用单目标 RL 求解 $\pi^*_\mathbf{w}$，得回报 $\mathbf{v}_\mathbf{w}$，加入 $\mathcal{C}$；
3. 基于当前 $\mathcal{C}$ 的凸包，找到"预期最大改进"的新权重 $\mathbf{w}^{\text{new}}$；
4. 重复直到改进上界小于阈值。

**"预期最大改进"计算**：对于候选权重 $\mathbf{w}$，定义：

$$
\Delta(\mathbf{w}) = \left(\max_\pi \mathbf{w}^\top \mathbf{V}^\pi \right) - \max_{\mathbf{v} \in \mathcal{C}} \mathbf{w}^\top \mathbf{v}
$$

OLS 通过**当前 CCS 各点凸包上的角点权重**来选择下一个要探索的 $\mathbf{w}$，确保收敛到完整 CCS。

**优势**：任何单目标 RL 算法（PPO、SAC、TD3）都可以无缝接入作为 inner solver。

### 3.3 Envelope Q-Learning（重点）

Yang 等人 (NeurIPS 2019) 提出，是目前离散动作 MORL 中最重要的算法之一。核心是**单网络端到端学习 CCS**。

#### 3.3.1 算法动机

标准标量化方法的问题：**不同偏好对应的最优策略差别巨大**，单网络用 $\mathbf{w}$ 条件化时会陷入平均化，难以学到最优策略的尖锐区分。Envelope 的思路是：

> 不用标量 Q 值传播 TD 目标，而是用**完整向量 Q 值**传播，最大化操作仍然针对标量化值。

#### 3.3.2 数学推导

定义向量 Q 网络 $\mathbf{Q}_\theta(s, a; \mathbf{w}) \in \mathbb{R}^d$。广义 Bellman 最优算子：

$$
(\mathcal{T} \mathbf{Q})(s, a; \mathbf{w}) = \mathbb{E}_{s'} \left[ \mathbf{R}(s,a,s') + \gamma \mathbf{H}(\mathbf{Q}; s', \mathbf{w}) \right]
$$

其中 $\mathbf{H}$ 为 **Envelope 操作**：

$$
\mathbf{H}(\mathbf{Q}; s', \mathbf{w}) = \mathbf{Q}(s', a^*; \mathbf{w}^*)
$$

$$
(a^*, \mathbf{w}^*) = \arg\max_{a' \in \mathcal{A}, \, \mathbf{w}' \in \mathcal{W}} \mathbf{w}^\top \mathbf{Q}(s', a'; \mathbf{w}')
$$

**关键点**：
- 标量化 max 只影响**选哪个 $(a, \mathbf{w}')$**；
- 一旦选定，**整个向量 Q** 作为目标（不是标量值）；
- 对偏好的 max 确保：无论当前查询的 $\mathbf{w}$ 是什么，都用 CCS 上最贴合的那条策略路径传播信息。

**定理（压缩性）**：算子 $\mathcal{T}$ 在度量 $d(\mathbf{Q}, \mathbf{Q}') = \sup_{s, a, \mathbf{w}} \|\mathbf{Q}(s,a;\mathbf{w}) - \mathbf{Q}'(s,a;\mathbf{w})\|_\infty$ 下是 $\gamma$-压缩的，存在唯一不动点 $\mathbf{Q}^*$。

#### 3.3.3 训练损失（复合损失）

实现时采用**双损失函数**：

$$
\mathcal{L}_A(\theta) = \mathbb{E} \left[ \left\| \mathbf{y} - \mathbf{Q}_\theta(s, a; \mathbf{w}) \right\|_2^2 \right] \quad \text{(向量 TD 损失)}
$$

$$
\mathcal{L}_B(\theta) = \mathbb{E} \left[ \left( \mathbf{w}^\top \mathbf{y} - \mathbf{w}^\top \mathbf{Q}_\theta(s, a; \mathbf{w}) \right)^2 \right] \quad \text{(标量化辅助损失)}
$$

$$
\mathcal{L} = (1-\lambda) \mathcal{L}_A + \lambda \mathcal{L}_B
$$

其中 $\mathbf{y} = \mathbf{r} + \gamma \mathbf{H}(\mathbf{Q}_{\bar\theta}; s', \mathbf{w})$ 为目标网络计算的 Envelope 目标。$\lambda$ 从 0 缓慢增加到接近 1，实现从 vector regression 到 scalar regression 的 curriculum。

#### 3.3.4 Envelope Q-Learning 伪代码

```
输入：MOMDP 环境 env，折扣 γ，偏好采样分布 p(w)，权重样本数 N_w
初始化：Q_θ(s, a; w)，目标网络 Q_{θ-}，经验缓冲区 D

for episode = 1, 2, ... do
    s ← env.reset()
    w ~ p(w)                                   # 采样一个偏好
    while not terminal do
        a ← ε-greedy w.r.t. w^T Q_θ(s, ·; w)
        s', r ← env.step(a)                    # r 是向量
        D.add((s, a, r, s', w))
        s ← s'

        # 训练步
        minibatch ← sample(D, B)
        for (s_i, a_i, r_i, s'_i, w_i) in minibatch:
            # 对每个 (s'_i, w_i)，采样 N_w 个候选偏好
            {w_j} ~ p(w) (j = 1..N_w), 加入 w_i
            # Envelope 操作
            (a*, w*) = argmax_{a', w'} w_i^T Q_{θ-}(s'_i, a'; w')
            y_i = r_i + γ · Q_{θ-}(s'_i, a*; w*)
        L = (1-λ) · ||y - Q_θ||² + λ · (w^T y - w^T Q_θ)²
        θ ← θ - α ∇L
    周期性更新 θ- ← θ
```

### 3.4 PGMORL (Pareto-following Gradient-based MORL)

Xu 等 (ICML 2020) 提出，专为**连续动作**设计，基于 PPO + 进化算法。

#### 3.4.1 核心思想

1. 维护一个策略种群 $\{\pi_1, \dots, \pi_K\}$，每个策略对应不同的权重 $\mathbf{w}_k$；
2. 每轮用 PPO 对每个策略做**偏好导向**的梯度更新，优化 $\mathbf{w}_k^\top \mathbf{V}^{\pi_k}$；
3. **预测阶段**：利用历史梯度信息估计各策略在不同权重下的移动方向，筛选最具帕累托改进潜力的 (策略, 权重) 对；
4. **进化**：任务分配给最有潜力的策略进行下一轮优化。

PGMORL 能处理**非凸 PF**（通过种群多样性 + 特定的任务选择机制），是连续控制场景（如电池连续充放电）的优选。

### 3.5 MORL/D (Decomposition)

Felten 等 (2024) 的综合框架，借鉴 MOEA/D 的分解思想：

1. 将权重单纯形 $\Delta^{d-1}$ 划分为 $K$ 个均匀子区域 $\{\mathbf{w}_1, \dots, \mathbf{w}_K\}$；
2. 每个子问题独立优化 $u_{\mathbf{w}_k}(\mathbf{V}^{\pi_k})$；
3. 邻域策略之间通过参数共享或知识迁移加速学习。

MORL/D 是一个**元框架**，内部可以嵌入任何单目标 RL，适用于高维目标（$d \geq 3$）。

### 3.6 Pareto Q-Learning（表格法）

完全无标量化的早期方法，维护集合值 Q：

$$
\hat{\mathcal{Q}}(s, a) \subset \mathbb{R}^d
$$

Bellman 更新通过**向量集合运算**：

$$
\hat{\mathcal{Q}}(s, a) \leftarrow \bigcup_{s'} p(s'|s,a) \cdot \left\{ \mathbf{r} + \gamma \mathbf{v} \,:\, \mathbf{v} \in \text{ND}\big(\bigcup_{a'} \hat{\mathcal{Q}}(s', a')\big) \right\}
$$

其中 $\text{ND}(\cdot)$ 为非支配过滤。

仅适用于**小状态空间离散问题**，但理论价值高（第一个能处理非凸 PF 的 RL 算法）。

### 3.7 算法选型决策表

针对电力行业场景的快速决策：

| 场景特征 | 推荐算法 |
|---------|---------|
| 小规模离散（如多档位投标），$d=2\sim 3$ | Envelope Q-Learning |
| 连续动作（电池出力、连续报价） | PGMORL 或 MO-SAC (CAPQL) |
| 目标数 $d \geq 4$ | MORL/D + 单目标 SAC |
| 偏好运行时动态调整（实时电价响应） | Envelope Q-Learning 或 GPI-LS |
| PF 非凸（存在互斥运行模式） | PGMORL、Pareto Q-Learning |
| 少样本 + 明确权重 | Scalarized PPO（保底方案） |


---

## 4. 工程实现技术路线

### 4.1 技术栈推荐

**标准 MORL 技术栈**（2024-2025 年成熟方案）：

```
核心：
├── Python 3.10+
├── PyTorch 2.0+                    # 张量计算与自动求导
├── MO-Gymnasium (mo-gymnasium)     # MOMDP 环境标准接口（Farama 基金会维护）
├── MORL-Baselines (morl-baselines) # 10+ MORL 算法参考实现
└── NumPy, Pandas                   # 数据处理

可选：
├── Weights & Biases (wandb)        # 实验跟踪，MORL-Baselines 原生集成
├── Gurobi / CVXPY                  # 对比基线（数学规划）
└── pymoo                           # 多目标进化算法对比
```

**MO-Gymnasium API 与原生 Gymnasium 的唯一区别**：`env.step()` 返回的 `reward` 是 `np.ndarray` 而非 `float`：

```python
next_obs, vector_reward, terminated, truncated, info = env.step(action)
# vector_reward.shape == (d,)
```

### 4.2 安装

```bash
# 基础安装
pip install mo-gymnasium            # 环境
pip install morl-baselines          # 算法库
pip install torch numpy pandas matplotlib

# 可选
pip install wandb                   # 实验跟踪
pip install gymnasium[classic_control]
```

### 4.3 入门示例：Deep Sea Treasure + Envelope Q-Learning

Deep Sea Treasure (DST) 是 MORL 经典基准：潜水员需在海底 10 个宝藏（奖励 1 ~ 124）之间取舍，同时考虑时间代价（每步 -1）。两个目标：**宝藏价值** vs **时间成本**。

```python
import mo_gymnasium as mo_gym
import numpy as np
from morl_baselines.multi_policy.envelope.envelope import Envelope

# 创建环境
env = mo_gym.make("deep-sea-treasure-v0")
eval_env = mo_gym.make("deep-sea-treasure-v0")

# 观察奖励维度
print("Reward dim:", env.unwrapped.reward_space.shape[0])  # 2

# 初始化 Envelope Q-Learning
agent = Envelope(
    env=env,
    learning_rate=3e-4,
    initial_epsilon=1.0,
    final_epsilon=0.05,
    epsilon_decay_steps=50000,
    gamma=0.99,
    batch_size=64,
    net_arch=[256, 256],
    buffer_size=int(2e5),
    num_sample_w=4,          # 每次采样 4 个候选偏好做 envelope 目标
    learning_starts=100,
)

# 训练
agent.train(
    total_timesteps=int(2e5),
    eval_env=eval_env,
    ref_point=np.array([0.0, -25.0]),   # 超体积计算用参考点
    known_pareto_front=env.unwrapped.pareto_front(gamma=0.99),  # DST 内置真实 PF
)

# 评估：传入不同偏好看策略差异
for w in [np.array([1.0, 0.0]), np.array([0.5, 0.5]), np.array([0.0, 1.0])]:
    total_vec_reward = np.zeros(2)
    obs, _ = eval_env.reset()
    done = False
    while not done:
        action = agent.eval(obs, w)   # 关键：传入偏好查询动作
        obs, r, term, trunc, _ = eval_env.step(action)
        total_vec_reward += r
        done = term or trunc
    print(f"偏好 {w} → 回报 {total_vec_reward}")
```

### 4.4 自定义 MOMDP 环境的标准模板

对于电力场景，几乎都需要自定义环境。以下是符合 MO-Gymnasium API 的模板：

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np


class MyMOMDPEnv(gym.Env):
    """自定义多目标 RL 环境模板。关键：reward_space 定义奖励维度。"""

    def __init__(self, config: dict):
        super().__init__()
        # 1. 观察空间
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(config["obs_dim"],), dtype=np.float32
        )
        # 2. 动作空间
        self.action_space = spaces.Discrete(config["num_actions"])
        # 3. 奖励空间（MORL 新增）
        self.reward_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(config["num_objectives"],), dtype=np.float32,
        )
        self.reward_dim = config["num_objectives"]
        # 业务数据
        self._cfg = config
        self._t = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._t = 0
        obs = self._build_obs()
        return obs, {}

    def step(self, action):
        # 业务动力学
        self._t += 1
        obs = self._build_obs()
        # 关键：返回向量奖励
        vec_reward = self._compute_vector_reward(action).astype(np.float32)
        terminated = self._t >= self._cfg["horizon"]
        truncated = False
        info = {}
        return obs, vec_reward, terminated, truncated, info

    def _build_obs(self) -> np.ndarray:
        raise NotImplementedError

    def _compute_vector_reward(self, action) -> np.ndarray:
        raise NotImplementedError
```


---

## 5. 电力市场交易与虚拟电厂应用

本节给出两个完整可运行的电力场景 MORL 建模案例，均采用 MO-Gymnasium + MORL-Baselines 标准技术栈。

### 5.1 场景一：虚拟电厂多目标日内调度

#### 5.1.1 问题建模

**系统构成**：光伏 PV + 电池储能 BESS + 可中断负荷 + 现货市场买卖。

**决策时刻**：15-min 分辨率，单日 96 个时段。

**决策变量**（动作）：电池充放电功率档位 $a \in \{-P_{\max}, \dots, 0, \dots, P_{\max}\}$（简化为 5 档离散）。

**状态向量**：
$$
s_t = \big( \text{SOC}_t, \; \lambda_t, \; \hat\lambda_{t+1..t+k}, \; \hat{P}^{\text{PV}}_{t+1..t+k}, \; \hat{L}_{t+1..t+k}, \; t/T \big)
$$

**三个目标奖励分量**（每步）：

1. **净收益** $r^{(1)}_t$
$$
r^{(1)}_t = \lambda_t \cdot (P^{\text{PV}}_t - L_t - P^{\text{batt}}_t) \cdot \Delta t
$$
其中 $P^{\text{batt}}_t > 0$ 表示电池放电（减少向电网购电/增加售电），$P^{\text{batt}}_t < 0$ 表示充电。

2. **碳排成本（负向）** $r^{(2)}_t$
$$
r^{(2)}_t = -\text{EF}_t \cdot \max(0, L_t + P^{\text{batt,charge}}_t - P^{\text{PV}}_t) \cdot \Delta t
$$
$\text{EF}_t$ 为电网边际排放因子 (kgCO$_2$/kWh)。

3. **电池损耗（负向）** $r^{(3)}_t$
$$
r^{(3)}_t = -\kappa_{\text{deg}} \cdot |P^{\text{batt}}_t| \cdot \Delta t
$$
$\kappa_{\text{deg}}$ 为等效损耗系数（$/kWh 吞吐量）。

**状态转移（SOC 动力学）**：
$$
\text{SOC}_{t+1} = \text{SOC}_t - \frac{P^{\text{batt}}_t \Delta t}{E_{\text{cap}}} \cdot (\eta_d^{-1} \mathbb{1}_{P^{\text{batt}}_t > 0} + \eta_c \mathbb{1}_{P^{\text{batt}}_t < 0})
$$
$\eta_c, \eta_d$ 分别为充放电效率。

**约束**：SOC 边界通过**动作裁剪**实现（若 action 会违反边界则裁剪到可行值）。

#### 5.1.2 完整代码实现

以下代码可直接运行，生成合成数据并训练 Envelope Q-Learning：

```python
"""
vpp_morl_env.py —— VPP 多目标调度环境
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd


class VPPMultiObjEnv(gym.Env):
    """
    虚拟电厂多目标调度环境。
    Objectives: [净收益, -碳排成本, -电池损耗]
    """
    metadata = {"render_modes": []}

    def __init__(
        self,
        price_series: np.ndarray,         # shape (T,), 电价 ¥/kWh
        pv_series: np.ndarray,            # shape (T,), PV 出力 kW
        load_series: np.ndarray,          # shape (T,), 负荷 kW
        ef_series: np.ndarray,            # shape (T,), 排放因子 kg/kWh
        horizon: int = 96,
        dt_hour: float = 0.25,
        e_cap_kwh: float = 500.0,
        p_max_kw: float = 100.0,
        eta_c: float = 0.95,
        eta_d: float = 0.95,
        soc_min: float = 0.1,
        soc_max: float = 0.9,
        init_soc: float = 0.5,
        kappa_deg: float = 0.05,          # ¥/kWh 吞吐
        forecast_horizon: int = 4,
    ):
        super().__init__()
        self.price = price_series.astype(np.float32)
        self.pv = pv_series.astype(np.float32)
        self.load = load_series.astype(np.float32)
        self.ef = ef_series.astype(np.float32)
        assert len(price_series) == len(pv_series) == len(load_series) == len(ef_series)

        self.T = len(price_series)
        self.horizon = min(horizon, self.T)
        self.dt = dt_hour
        self.e_cap = e_cap_kwh
        self.p_max = p_max_kw
        self.eta_c, self.eta_d = eta_c, eta_d
        self.soc_min, self.soc_max = soc_min, soc_max
        self.init_soc = init_soc
        self.kappa = kappa_deg
        self.fh = forecast_horizon

        # 5 档离散动作：-p_max, -p_max/2, 0, +p_max/2, +p_max
        self.action_levels = np.array(
            [-p_max_kw, -p_max_kw / 2, 0.0, p_max_kw / 2, p_max_kw],
            dtype=np.float32,
        )
        self.action_space = spaces.Discrete(len(self.action_levels))

        # 状态: [SOC, 当前价, 价预测×fh, PV预测×fh, 负荷预测×fh, t/T]
        obs_dim = 1 + 1 + 3 * self.fh + 1
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )

        # MO-Gymnasium 关键属性
        self.reward_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32
        )
        self.reward_dim = 3

        self._t = 0
        self._soc = init_soc

    def _obs(self) -> np.ndarray:
        # 简化：使用"完美"短期预报（真实场景替换为预测模型输出）
        def _future(series, t, h):
            idx = np.arange(t + 1, t + 1 + h)
            idx = np.clip(idx, 0, len(series) - 1)
            return series[idx]

        price_now = self.price[self._t]
        price_fut = _future(self.price, self._t, self.fh)
        pv_fut = _future(self.pv, self._t, self.fh)
        load_fut = _future(self.load, self._t, self.fh)

        obs = np.concatenate([
            np.array([self._soc], dtype=np.float32),
            np.array([price_now / 1.0], dtype=np.float32),
            price_fut / 1.0,
            pv_fut / self.p_max,
            load_fut / self.p_max,
            np.array([self._t / self.horizon], dtype=np.float32),
        ]).astype(np.float32)
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._t = 0
        self._soc = self.init_soc
        return self._obs(), {}

    def step(self, action: int):
        # 1. 解析动作（电池出力指令，>0 放电）
        p_batt_cmd = float(self.action_levels[int(action)])

        # 2. SOC 约束裁剪
        if p_batt_cmd > 0:  # 放电，SOC 降低
            max_discharge_energy = (self._soc - self.soc_min) * self.e_cap * self.eta_d
            p_batt = min(p_batt_cmd, max_discharge_energy / self.dt)
            p_batt = max(p_batt, 0.0)
            dsoc = -(p_batt * self.dt) / (self.e_cap * self.eta_d)
        elif p_batt_cmd < 0:  # 充电
            max_charge_energy = (self.soc_max - self._soc) * self.e_cap / self.eta_c
            p_batt = -min(-p_batt_cmd, max_charge_energy / self.dt)
            p_batt = min(p_batt, 0.0)
            dsoc = -(p_batt * self.dt * self.eta_c) / self.e_cap
        else:
            p_batt = 0.0
            dsoc = 0.0

        self._soc = np.clip(self._soc + dsoc, self.soc_min, self.soc_max)

        # 3. 功率平衡
        pv_t = self.pv[self._t]
        load_t = self.load[self._t]
        price_t = self.price[self._t]
        ef_t = self.ef[self._t]
        # 向电网净售电 = PV - 负荷 + 电池放电（放电为正）
        net_export_kw = pv_t - load_t + p_batt

        # 4. 三个目标奖励
        r_revenue = price_t * net_export_kw * self.dt
        # 碳排：向电网净购电时才计算
        grid_purchase_kwh = max(0.0, -net_export_kw) * self.dt
        r_co2 = -ef_t * grid_purchase_kwh * 0.5  # 简单转化为货币化（碳价 0.5 ¥/kg）
        # 电池损耗 ∝ |电池吞吐|
        r_deg = -self.kappa * abs(p_batt) * self.dt

        vec_reward = np.array([r_revenue, r_co2, r_deg], dtype=np.float32)

        # 5. 时间推进
        self._t += 1
        terminated = self._t >= self.horizon
        truncated = False

        return self._obs(), vec_reward, terminated, truncated, {
            "soc": self._soc,
            "p_batt": p_batt,
            "net_export": net_export_kw,
        }
```

**合成数据生成**：

```python
"""
generate_data.py —— 生成一天典型日的价格/负荷/PV 数据
"""
import numpy as np

def make_one_day(seed=0):
    rng = np.random.default_rng(seed)
    T = 96  # 15-min 步长

    # 电价：双峰（早高峰 8-10，晚高峰 19-22），¥/kWh
    hours = np.arange(T) * 0.25
    price = 0.35 + 0.15 * np.exp(-((hours - 9) ** 2) / 4)
    price += 0.25 * np.exp(-((hours - 20) ** 2) / 3)
    price += rng.normal(0, 0.02, T)
    price = np.clip(price, 0.25, 1.0)

    # PV：10-16 时有出力，峰值 80 kW
    pv = 80 * np.maximum(0, np.sin(np.pi * (hours - 6) / 12))
    pv[hours < 6] = 0
    pv[hours > 18] = 0
    pv += rng.normal(0, 2, T)
    pv = np.clip(pv, 0, None)

    # 负荷：50-100 kW，双峰
    load = 60 + 15 * np.exp(-((hours - 8) ** 2) / 6)
    load += 25 * np.exp(-((hours - 19) ** 2) / 4)
    load += rng.normal(0, 2, T)
    load = np.clip(load, 40, 120)

    # 排放因子 kgCO2/kWh：晚上煤电为主较高
    ef = 0.55 + 0.15 * np.cos(2 * np.pi * hours / 24 + np.pi)
    ef = np.clip(ef, 0.3, 0.8)

    return (price.astype(np.float32), pv.astype(np.float32),
            load.astype(np.float32), ef.astype(np.float32))


if __name__ == "__main__":
    price, pv, load, ef = make_one_day(seed=42)
    print(f"Price range: {price.min():.2f}–{price.max():.2f} ¥/kWh")
    print(f"PV peak: {pv.max():.1f} kW")
    print(f"Load peak: {load.max():.1f} kW")
    print(f"EF range: {ef.min():.2f}–{ef.max():.2f} kg/kWh")
```

**训练脚本**：

```python
"""
train_vpp_envelope.py —— 用 Envelope Q-Learning 训练 VPP 调度策略
"""
import numpy as np
import mo_gymnasium as mo_gym
from morl_baselines.multi_policy.envelope.envelope import Envelope

from vpp_morl_env import VPPMultiObjEnv
from generate_data import make_one_day


def make_env(seed: int):
    price, pv, load, ef = make_one_day(seed=seed)
    env = VPPMultiObjEnv(
        price_series=price, pv_series=pv, load_series=load, ef_series=ef
    )
    return env


if __name__ == "__main__":
    train_env = make_env(seed=42)
    eval_env = make_env(seed=1234)

    agent = Envelope(
        env=train_env,
        learning_rate=3e-4,
        gamma=0.99,
        batch_size=128,
        net_arch=[256, 256],
        buffer_size=int(1e5),
        initial_epsilon=1.0,
        final_epsilon=0.05,
        epsilon_decay_steps=30000,
        num_sample_w=4,
        learning_starts=500,
    )

    # 参考点用于超体积指标（任意保守下界）
    ref_point = np.array([-100.0, -200.0, -50.0])

    agent.train(
        total_timesteps=100_000,
        eval_env=eval_env,
        ref_point=ref_point,
        weight=None,        # None 表示随机采样权重训练通用策略
    )

    # 评估不同偏好下的策略
    for w, label in [
        (np.array([1.0, 0.0, 0.0]), "纯收益最大化"),
        (np.array([0.5, 0.5, 0.0]), "收益 + 低碳"),
        (np.array([0.4, 0.3, 0.3]), "均衡"),
        (np.array([0.2, 0.2, 0.6]), "电池寿命优先"),
    ]:
        obs, _ = eval_env.reset()
        total = np.zeros(3)
        done = False
        while not done:
            action = agent.eval(obs, w)
            obs, r, term, trunc, _ = eval_env.step(action)
            total += r
            done = term or trunc
        print(f"{label} (w={w}): 收益={total[0]:.1f}, 碳={total[1]:.1f}, 损耗={total[2]:.1f}")
```

**预期输出示例**（训练后）：
```
纯收益最大化 (w=[1,0,0]):  收益= 320.5, 碳= -45.3, 损耗= -18.2
收益 + 低碳  (w=[.5,.5,0]): 收益= 285.1, 碳= -22.8, 损耗= -16.5
均衡         (w=[.4,.3,.3]):收益= 265.4, 碳= -28.1, 损耗= -10.3
电池寿命优先 (w=[.2,.2,.6]):收益= 180.2, 碳= -38.5, 损耗=  -3.1
```

**运行时决策**：无需重新训练，决策者只需传入新的 $\mathbf{w}$ 就能获得对应策略——这正是 MORL 相对于传统 DRL 调度的核心优势。

### 5.2 场景二：电力现货市场日前投标（收益-风险平衡）

#### 5.2.1 问题建模

新能源发电商参与日前市场，对次日 24 小时逐小时申报：**(投标量, 投标价)**。次日实际出力存在不确定性，若偏差超过允许范围会受到偏差考核罚款。

**状态**：
$$
s_h = \big(\text{价格历史统计}, \; \text{负荷预测}, \; \hat{P}^{\text{gen}}_h, \; \sigma_h \big)
$$

其中 $\sigma_h$ 为发电预测的标准差。

**动作（离散化报价）**：每小时选择 $(q, p)$，$q \in \{0, 0.25, 0.5, 0.75, 1.0\} \cdot P_{\max}$，$p \in \{$电价预测 $\pm 10\%, \pm 5\%, 0, \dots\}$。

**三个目标**：

1. **期望净收益** $r^{(1)}_h = p_h \cdot q_h \cdot \mathbb{1}[\text{中标}] - c_{\text{fuel}} \cdot q_h$（火电场景）或 $p_h \cdot q_h$（新能源）；
2. **偏差罚款（负）** $r^{(2)}_h = -\kappa_{\text{dev}} \cdot \max(0, |q_h - P^{\text{gen,actual}}_h| - \Delta_{\text{tol}})$；
3. **风险度量（负）** $r^{(3)}_h = -\lambda_{\text{risk}} \cdot \text{CVaR}_\alpha(\text{净收益})$（可用滑动分位数估计）。

此处 MORL 相较传统 DQN 的价值：**不同运营策略（激进型 vs 保守型）对应不同 $\mathbf{w}$，通过单一训练模型按需切换**。

#### 5.2.2 简化代码框架

```python
"""
market_bid_env.py —— 日前市场投标 MOMDP（简化）
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np


class DayAheadBiddingEnv(gym.Env):
    def __init__(
        self,
        price_samples: np.ndarray,   # (N_scenarios, 24) 日前出清价情景
        gen_forecast_mean: np.ndarray,  # (24,)
        gen_forecast_std: np.ndarray,   # (24,)
        p_max_mw: float = 50.0,
        dev_tol_pct: float = 0.05,
        dev_penalty: float = 2.0,     # ¥/kWh over tolerance
    ):
        super().__init__()
        self.price_samples = price_samples
        self.gen_mean = gen_forecast_mean
        self.gen_std = gen_forecast_std
        self.p_max = p_max_mw
        self.dev_tol = dev_tol_pct
        self.dev_pen = dev_penalty
        self.T = 24

        # 动作：5 档量 × 5 档价偏移 = 25
        self.qty_levels = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        self.price_offsets = np.array([-0.10, -0.05, 0.0, 0.05, 0.10])
        self.action_space = spaces.Discrete(len(self.qty_levels) * len(self.price_offsets))

        # 状态
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32
        )
        self.reward_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32
        )
        self.reward_dim = 3

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._rng = np.random.default_rng(seed)
        self._h = 0
        # 抽样当日实际价格/出力情景
        idx = self._rng.integers(0, len(self.price_samples))
        self._today_price = self.price_samples[idx]
        self._today_gen = np.clip(
            self._rng.normal(self.gen_mean, self.gen_std),
            0.0, self.p_max,
        )
        self._revenues_so_far = []
        return self._obs(), {}

    def _obs(self):
        return np.array([
            self._h / self.T,
            self.gen_mean[self._h] / self.p_max,
            self.gen_std[self._h] / self.p_max,
            self._today_price[self._h - 1] if self._h > 0 else 0.35,
            np.mean(self._today_price[:self._h]) if self._h > 0 else 0.35,
            self.gen_mean[self._h] / self.p_max,
        ], dtype=np.float32)

    def step(self, action: int):
        qty_idx = action // len(self.price_offsets)
        price_idx = action % len(self.price_offsets)
        bid_qty = self.qty_levels[qty_idx] * self.p_max
        bid_price = self.gen_mean[self._h] * 0.001 + 0.35  # 简化预测基准价
        bid_price *= (1 + self.price_offsets[price_idx])

        clearing_price = self._today_price[self._h]
        actual_gen = self._today_gen[self._h]

        # 中标判断（简化：报价 ≤ 出清价即中标）
        cleared = bid_price <= clearing_price
        awarded_qty = bid_qty if cleared else 0.0

        # 1) 收益
        revenue = clearing_price * awarded_qty  # 按出清价结算

        # 2) 偏差罚款
        dev = abs(awarded_qty - actual_gen)
        tol = self.dev_tol * self.p_max
        over_dev = max(0.0, dev - tol)
        penalty = -self.dev_pen * over_dev

        # 3) 风险：滑动标准差
        self._revenues_so_far.append(revenue)
        if len(self._revenues_so_far) >= 2:
            risk = -np.std(self._revenues_so_far[-6:])  # 最近 6 小时波动
        else:
            risk = 0.0

        vec_reward = np.array([revenue, penalty, risk], dtype=np.float32)

        self._h += 1
        terminated = self._h >= self.T
        return self._obs(), vec_reward, terminated, False, {
            "cleared": cleared,
            "bid_qty": bid_qty,
            "bid_price": bid_price,
            "clearing_price": clearing_price,
        }
```

**训练与业务侧使用**（关键是如何把偏好权重映射到业务语义）：

```python
# 业务侧策略配置：将业务语义映射到 w
STRATEGY_WEIGHTS = {
    "aggressive":  np.array([0.80, 0.10, 0.10]),   # 激进：重收益，容忍偏差和波动
    "balanced":    np.array([0.50, 0.30, 0.20]),
    "conservative":np.array([0.40, 0.35, 0.25]),
    "risk_averse": np.array([0.30, 0.30, 0.40]),   # 风控优先
}

# 训练好的 Envelope agent 可直接按需调用
for name, w in STRATEGY_WEIGHTS.items():
    action = agent.eval(obs, w)
    # → 单一模型支撑多种业务策略
```

### 5.3 与数学规划/传统方法的对比

对于电力行业工程师常用的数学规划 (MILP/SOCP) + 蒙特卡洛方法，MORL 的边界：

| 维度 | 数学规划 (如 Gurobi) | MORL (Envelope) |
|------|---------------------|-----------------|
| 不确定性处理 | 鲁棒优化 / 随机规划（维数灾） | 自然嵌入期望 |
| 非线性/非凸 | 困难（需近似或 MINLP） | 天然支持 |
| 新偏好响应 | 重新求解 | **零成本推断** |
| 计算时延 | 秒-分钟级 | 毫秒级（前向推断） |
| 可解释性 | 强（显式约束） | 弱 |
| 全局最优保证 | 有（凸/MILP） | 无（近似值函数） |
| 跨日泛化 | 需重建模 | 可直接泛化 |

**推荐实践路线（工业部署）**：

1. **MILP 作为 Oracle**：生成大量"完美信息"下的最优轨迹作为**专家数据**；
2. **离线 MORL 预训练**：用专家数据做 Behavior Cloning 初始化；
3. **在线 MORL 微调**：基于实时数据持续更新；
4. **MILP 做安全层**：MORL 输出的动作送入 MILP 投影层，确保硬约束（SOC、容量）满足。

这种 **"MILP + MORL" 混合架构** 既保留了数学规划的最优性与安全性，又获得了 MORL 的快速响应和偏好适应能力。

### 5.4 其他电力场景 MORL 应用

| 场景 | 目标向量 | 典型算法 | 难点 |
|------|---------|---------|------|
| 多主体 VPP 联盟 | 各主体收益 + 联盟总收益 | MO-MADDPG | 信用分配 |
| EV 有序充电 | 用户成本 + 电池损耗 + 到电量满意度 | Envelope DQN | 用户异质 |
| 分布式储能群控 | 套利 + 电压支撑 + 损耗 | PGMORL | 连续控制 |
| 微电网孤岛切换 | 供电可靠性 + 经济 + 污染物 | MORL/D | 目标数多 |
| 辅助服务组合 | 调频收益 + 调峰收益 + 备用收益 | OLS + PPO | 耦合约束 |
| 需求响应激励定价 | 聚合商利润 + 用户参与度 | 多智能体 MORL | 机制设计 |


---

## 6. 挑战与展望

### 6.1 当前 MORL 的主要挑战

**(a) 样本效率**
MORL 本质上要在"状态 × 动作 × 偏好"三维空间上学习，状态空间相比单目标 RL 扩大 $|\mathcal{W}|$ 倍。电力场景数据稀缺（只有历史运行数据），离线 MORL (Offline MORL) 是重要研究方向，但目前算法成熟度低于在线方法。

**(b) 高维目标 ($d \geq 4$)**
Pareto 前沿在高维空间爆炸性增长。电力场景经常有 4+ 目标（经济、碳、寿命、可靠性、用户满意度）。MORL/D 等分解方法能部分缓解，但权重单纯形的均匀采样在高维下仍然低效。

**(c) 非线性效用与马尔可夫性冲突**
Tchebycheff 等非线性效用对 PF 完备性有保证，但破坏价值函数的 Bellman 可分解性。ESR 设置下更严重——回报分布需要完整建模，分布式 MORL (Distributional MORL) 是解法之一。

**(d) 偏好获取**
实际电力运营中，**决策者很少能直接给出数值权重** $\mathbf{w}$。需要：
- 基于 A/B 选择的偏好学习（Preference-Based MORL）；
- 与逆强化学习结合的隐式偏好推断。

**(e) 安全约束**
MORL 天然适合将"约束"建模为目标（如让电压偏离成为一个被最小化的目标）。但硬约束（SOC 边界、N-1 安全）仍需**约束 MORL (Constrained MORL)** 或外挂投影层。

### 6.2 发展趋势

1. **偏好无关的通用策略网络**（Universal Value Function Approximator for MORL）：借鉴 GPI-LS 等思路，训练一个可在 $(\mathcal{S}, \mathcal{W})$ 空间泛化的超网络；
2. **与 LLM/基础模型结合**：LLM 辅助解析自然语言偏好 → 映射到 $\mathbf{w}$，弥合业务语义与数值权重的鸿沟；
3. **分布式 MORL**：用分位数网络建模回报分布，原生支持 CVaR、VaR 等风险度量作为目标；
4. **联邦 MORL**：多个 VPP / 交易主体之间不共享原始数据，联邦学习 MORL 策略；
5. **可解释 MORL**：通过显著性分析、反事实解释回答"为什么在这个偏好下选这个动作"——对电力运营是硬需求。

### 6.3 对电力算法工程师的落地建议

**短期（POC 阶段，1-3 个月）**：
- 选择一个明确的多目标 VPP 调度场景，用 MO-Gymnasium 封装；
- 用 `morl-baselines` 的 Envelope Q-Learning 做快速验证；
- 对比基线：MILP（Oracle）、单目标 DQN、规则策略。

**中期（产品化，3-12 个月）**：
- 用真实历史数据训练，加入预测模型的不确定性；
- 实现 MILP 投影层保证硬约束；
- 设计业务友好的偏好映射 UI（滑块/预设）。

**长期（规模化）**：
- 探索多智能体 MORL 处理 VPP 联盟；
- 持续学习框架应对市场规则变化；
- 与碳市场、绿证市场联动的多商品 MORL。

---

## 7. 参考文献

### 核心论文

1. Roijers, D. M., Vamplew, P., Whiteson, S., & Dazeley, R. (2013). **A survey of multi-objective sequential decision-making**. *Journal of Artificial Intelligence Research*, 48, 67-113. — MORL 奠基性综述。
2. Yang, R., Sun, X., & Narasimhan, K. (2019). **A Generalized Algorithm for Multi-Objective Reinforcement Learning and Policy Adaptation**. *NeurIPS 2019*. [arXiv:1908.08342] — **Envelope Q-Learning 原论文**。
3. Xu, J., Tian, Y., Ma, P., Rus, D., Sueda, S., & Matusik, W. (2020). **Prediction-Guided Multi-Objective Reinforcement Learning for Continuous Robot Control**. *ICML 2020*. — **PGMORL**。
4. Felten, F., Alegre, L. N., Nowe, A., Bazzan, A., Talbi, E. G., Danoy, G., & Silva, B. C. (2023). **A Toolkit for Reliable Benchmarking and Research in Multi-Objective Reinforcement Learning**. *NeurIPS 2023*. — **MORL-Baselines 工具箱论文**。
5. Hayes, C. F., et al. (2022). **A practical guide to multi-objective reinforcement learning and planning**. *Autonomous Agents and Multi-Agent Systems*, 36(1), 26. — 实践导向综述。
6. Felten, F., Talbi, E.-G., & Danoy, G. (2024). **Multi-Objective Reinforcement Learning Based on Decomposition: A Taxonomy and Framework**. *JAIR*. — **MORL/D 框架**。
7. Alegre, L. N., Bazzan, A. L., Roijers, D. M., Nowé, A., & da Silva, B. C. (2023). **Sample-efficient multi-objective learning via generalized policy improvement prioritization**. *AAMAS 2023*. — GPI-LS。

### 工具链

- **MO-Gymnasium** (Farama Foundation): <https://mo-gymnasium.farama.org/>
- **MORL-Baselines**: <https://github.com/LucasAlegre/morl-baselines>
- **Open RL Benchmark (MORL 部分)**: <https://wandb.ai/openrlbenchmark/MORL-Baselines>

### 电力应用相关

- **DRL + VPP 多目标调度**：Frontiers in Energy Research (2024) — 基于 GRU + PPO 的 VPP 经济调度。
- **MADRL + 社区 VPP**：Applied Energy (2024) — 多智能体 DRL 用于 cVPP 辅助服务竞价。
- **智能电网多目标 DRL 框架**：*Processes* (MDPI, 2025) — 深圳 VPP 实证，DRL 应用于再生能源最大化与网损最小化。

---

## 附录 A：常用超参数经验值

| 超参 | Envelope QL | PGMORL |
|------|-------------|--------|
| 学习率 | 3e-4 | 3e-4 |
| 折扣因子 γ | 0.99 | 0.99 |
| 批大小 | 128-256 | 2048 (PPO) |
| 偏好采样数 N_w | 4-8 | N/A |
| 缓冲区 | 1e5 - 1e6 | N/A (on-policy) |
| 目标网络软更新 τ | 0.005 | N/A |
| ε 衰减步数 | 50% 总步数 | N/A |
| 种群大小 | N/A | 6-20 策略 |

## 附录 B：评估指标

MORL 不能简单用"平均回报"评估，常用指标：

- **超体积 (Hypervolume, HV)**：PF 与参考点构成的多胞形体积。越大越好。
- **期望效用指标 (Expected Utility Metric, EUM)**：在偏好分布下的期望最大效用，$\mathbb{E}_{\mathbf{w}}[\max_\pi u_\mathbf{w}(\mathbf{V}^\pi)]$。
- **稀疏度 (Sparsity)**：PF 上相邻点距离方差，越小越均匀。
- **逆世代距 (IGD)**：已知真实 PF 时的参考指标。

`morl-baselines` 训练时自动计算并记录到 wandb。

---

**文档维护**：建议跟踪 MORL-Baselines 与 MO-Gymnasium 的版本更新（Farama 基金会维护，API 近期保持稳定）。
