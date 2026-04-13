---
author: null
created: 2026-04-11
description: null
tags:
- clippings
title: 1  引言和动机 – S&DS 431/631 — 优化与计算 --- 1  Introduction and Motivation – S&DS 431/631
  — Optimization and Computation
source_type: web
created_at: 2026-04-11
status: inbox
source_url: https://zhuoranyang.github.io/sds431-notes/lectures/01-introduction.html
published_at: null
related_concepts: []
topics:
  - operations-research
  - 数学优化算法/运筹学
---
优化是几乎所有定量学科背后的数学引擎。每当统计学家拟合模型、机器学习工程师训练神经网络或金融分析师构建投资组合时，核心计算任务都是一个优化问题：从一组备选方案中找到最佳决策。区分优秀实践者和卓越实践者的关键在于理解正在解决哪个优化问题、有哪些可用算法以及如何证明解决方案的正确性。

在本章中，我们将概述来自统计学、机器学习和金融领域的一系列激励性示例。目标不是解决这些问题，而是观察它们如何自然地出现，并欣赏它们所共有的共同数学结构。到本章结束时，你将清晰地了解优化的全貌，并知道课程中的每个主题在其中的位置。

总体主题是凸优化占据了一个甜蜜点：它足够丰富，可以模拟广泛的实际问题，同时又足够结构化，可以容纳高效且易于理解的算法。

Tip配套笔记本

本章配有实践性 Python 笔记本。点击徽章可在 Google Colab 中打开。

- 通过 CVXPY 和梯度下降实现 SVM——比较支持向量机的约束和正则化形式

## 将涵盖的内容

- 来自统计学、机器学习和运筹学的激励性例子：最大似然估计、回归、支持向量机、主成分分析、投资组合优化、最优控制
- 这些问题如何作为优化问题共享共同的数学结构
- 优化的层次：凸与非凸、约束与无约束
- 课程的路线图：从凸理论到算法再到应用

## 1.1 动机实例

为什么要学习优化？因为每一个统计估计问题都涉及优化。我们从最基本的一个例子开始。

### 1.1.1 最大似然估计

**例 1.1（最大似然估计）** 假设 $X_1, X_2, \ldots, X_n \stackrel{\text{iid}}{\sim} P_{\theta^*}$ （例如 $\mathcal{N}(\theta^*, I_d)$ ）。

我们希望根据数据 $\{X_i\}_{i=1}^n$ 估计 θ∗\\theta^\*θ∗ 。

MLE 估计量定义为：

$$
\widehat{\theta}_{\text{MLE}} = \arg\min_{\theta \in \Theta} \; -\sum_{i=1}^{n} \log P_\theta(X_i). \tag{1.1}
$$

从统计学的角度来看： $\widehat{\theta}_{\text{MLE}}$ 的准确性如何？

从优化的角度来看：我们实际上如何计算 $\widehat{\theta}_{\text{MLE}}$ ？

### 1.1.2 最小二乘回归

**示例 1.2（最小二乘回归）** **Model:**

$$
y = X\beta^* + \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, I_n), \tag{1.2}
$$

在 $y \in \mathbb{R}^{n \times 1}$ ， $X \in \mathbb{R}^{n \times d}$ ， $\beta^* \in \mathbb{R}^{d}$ ， $\varepsilon \in \mathbb{R}^{n \times 1}$ 处。这里 $n$ 是样本数量， $d$ 是参数的维度。

为了估计真实参数 $\beta^*$ ，我们计算条件对数似然。由于

$$
P_\beta(y \mid X) \propto \exp\!\left(-\frac{\|y - X\beta\|_2^2}{2}\right),
$$

负对数似然为：

$$
\mathcal{L}(\beta) = -\log P_\beta(y \mid X) = \tfrac{1}{2}\|y - X\beta\|_2^2 + \text{Constant},
$$

where the constant does not involve $\beta$. Recall $\|v\|_2^2 = \sum_{i=1}^{n} v_i^2$.

因此，线性模型的 MLE 等价于最小二乘法：

$$
\min_\beta \; \|y - X\beta\|_2^2. \tag{1.3}
$$

### 1.1.3 回归的变体

普通最小二乘法有一个简洁的闭式解，但在三种常见情况下会失效：

1. 多重共线性。当特征高度相关时， $X^\top X$ 几乎是奇异的，并且 OLS 估计变得极其不稳定——数据中的微小扰动会导致 $\widehat{\beta}$ 产生大幅波动。
2. 高维性。当特征数量 $d$ 超过样本数量 $n$ 时，普通最小二乘法 (OLS) 是欠定的：无限多个 $\beta$ 可以实现零训练损失，并且 OLS 无法区分信号与噪声。
3. 可解释性。一个拥有 500 个特征的从业者想知道哪些特征是重要的。OLS 对每个特征都给出非零系数，无法提供任何指导。

以下每种回归变体通过修改优化问题来解决其中一种或多种这些缺陷。关键在于，每种修改都导致一类不同的优化问题，预览了本课程中的算法图景。

**定义 1.1（最小二乘法 (MLE)）** 
$$
\arg\min_{\beta \in \mathbb{R}^d} \; \|y - X\beta\|_2^2
$$

最小化 $\ell_2$ 误差。这是一个凸优化问题。

最小二乘法是我们的基准：只要 $X^\top X$ 可逆，它就有闭式解 $\widehat{\beta} = (X^\top X)^{-1} X^\top y$ =(X⊤X)−1X⊤y 。但当特征相关或 ddd 较大时，我们需要进一步深入。

**定义 1.2（岭回归）** 
$$
\arg\min_{\beta \in \mathbb{R}^d} \; \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2
$$

这是一个正则化最小二乘问题。它是强凸的。

岭回归直接解决多重共线性问题： $\ell_2$ -惩罚 $\lambda \|\beta\|_2^2$ 将 $\lambda I$ 添加到 $X^\top X$ ，使系统始终可逆，解始终唯一。从几何上看，岭回归将所有系数收缩到零，以较小的偏差增加换取较大的方差减少。从优化的角度来看， $\ell_2$ -惩罚使目标函数强凸——这一特性保证了迭代算法（如梯度下降）具有更快的收敛速度，正如我们将在梯度下降中看到的那样。

**Definition 1.3 (Lasso ($\ell_1$ -Regularized Least-Squares))** 
$$
\arg\min_{\beta \in \mathbb{R}^d} \; \|y - X\beta\|_2^2 + \lambda \|\beta\|_1, \qquad \|\beta\|_1 = \sum_{j=1}^{d} |\beta_j|.
$$

This is a **convex** problem, specifically a **cone program**.

The Lasso addresses the high-dimensionality and interpretability problems simultaneously. By replacing the $\ell_2$ -penalty with an $\ell_1$ -penalty, it encourages **sparsity**: many coefficients are driven to *exactly* zero, performing automatic feature selection. Why does $\ell_1$ produce zeros but $\ell_2$ does not? The geometry is the key: the $\ell_1$ -ball is a diamond with corners on the coordinate axes, and the level sets of the loss function are far more likely to first touch the constraint boundary at a corner (where some coordinates are zero) than along a smooth face. The Lasso is convex but **non-smooth** — the $|\beta_j|$ terms are not differentiable at zero — which means gradient descent does not directly apply. Solving the Lasso efficiently requires **proximal gradient methods**, a topic we develop in detail later in the course.

Comparison of regression coefficients for OLS, Ridge, and Lasso on a problem with a sparse true parameter vector β\* = (3, −1.5, 0, 0, 2). Lasso produces exact zeros for the irrelevant features, performing automatic feature selection.

### 1.1.4 Linear Programming (ℓ1\\ell\_1/ℓ∞\\ell\_\\infty-Minimization)

**Example 1.3 ($\ell_\infty$ -Regression)** Given data points $(x_i, y_i)$ for $i \in [n] = \{1, 2, \ldots, n\}$, with $y = \begin{pmatrix} y_1 \\ \vdots \\ y_n \end{pmatrix}$ and $X = \begin{pmatrix} x_1^\top \\ x_2^\top \\ \vdots \\ x_n^\top \end{pmatrix}$, the $\ell_\infty$ -norm is $\|v\|_\infty = \max_i |v_i|$. Then:

$$
\|y - X\beta\|_\infty = \max_i |y_i - x_i^\top \beta|.
$$

The $\ell_\infty$ -regression problem becomes:

$$
\arg\min_\beta \; \left\{\max_i |y_i - x_i^\top \beta|\right\}. \tag{1.4}
$$

**Example 1.4 ($\ell_1$ -Regression)** The $\ell_1$ -norm is $\|v\|_1 = \sum_{i=1}^{n} |v_i|$. The $\ell_1$ -regression problem is:

$$
\arg\min_{\beta \in \mathbb{R}^d} \; \|y - X\beta\|_1 = \arg\min_{\beta \in \mathbb{R}^d} \; \sum_{i=1}^{n} |y_i - x_i^\top \beta|. \tag{1.5}
$$

Both $\ell_1$ - and $\ell_\infty$ -regression can be reformulated as **linear programs**.

The ℓ <sub>1</sub>, ℓ <sub>2</sub>, and ℓ <sub>∞</sub> unit balls in 2D. The diamond shape of the ℓ <sub>1</sub> -ball explains why Lasso produces sparse solutions: its corners lie on the coordinate axes, making it likely that the optimal point has zero entries.

### 1.1.5 Sparse Regression (ℓ0\\ell\_0-Regularization)

**Example 1.5 ($\ell_0$ -Regularized Least-Squares / Sparse Regression)** The $\ell_0$ -“norm” counts nonzero entries: $\|v\|_0 = \#\{i : v_i \neq 0\}$.

The $\ell_0$ -regularized least-squares problem is:

$$
\arg\min_{\beta \in \mathbb{R}^d} \; \|y - X\beta\|_2^2 + \lambda \|\beta\|_0. \tag{1.6}
$$

This problem is **NP-hard**. We need to relax or approximate it. Two common relaxations are:

- **Constrained form:** $\displaystyle\arg\min_{\beta \in \mathbb{R}^d} \|y - X\beta\|_2 \quad \text{s.t.} \quad \|\beta\|_0 \leq k$, where $k$ is an integer.
- **Inverse form:** $\displaystyle\arg\min_{\beta \in \mathbb{R}^d} \|\beta\|_0 \quad \text{s.t.} \quad \|y - X\beta\|_2 \leq \varepsilon$.

### 1.1.6 Empirical Risk Minimization

All of the regression variants above share a common pattern: choose a loss function, optionally add a regularizer, and minimize the resulting objective over the data. The Empirical Risk Minimization (ERM) framework captures this pattern in full generality, providing a single template that encompasses least-squares, ridge, Lasso, and many other estimators.

**Definition 1.4 (Empirical Risk Minimization Framework)** Given data points $\{(x_i, y_i)\}_{i \in [n]}$, define:

- $h_\theta : \mathbb{R}^d \to \mathbb{R}$ — hypothesis parameterized by $\theta \in \Theta$ (e.g., $h_\theta(x) = x^\top \theta$).
- $\ell : \mathbb{R} \times \mathbb{R} \to \mathbb{R}$ — loss function (e.g., $\ell(u, v) = (u - v)^2$).
- $R : \Theta \to \mathbb{R}$ — regularizer.

**Regularized ERM:**

$$
\min_{\theta \in \Theta} \; \left\{\sum_{i=1}^{n} \ell\!\left(h_\theta(x_i),\, y_i\right) + \lambda \cdot R(\theta)\right\}. \tag{1.7}
$$

**Constrained ERM:**

$$
\min_{\theta} \; \sum_{i=1}^{n} \ell\!\left(h_\theta(x_i),\, y_i\right) \quad \text{s.t.} \quad R(\theta) \leq \lambda. \tag{1.8}
$$

TipRemark

All the regression variants above — least-squares, ridge, Lasso, $\ell_1$ / $\ell_\infty$ -regression — are special cases of the ERM framework with particular choices of loss and regularizer.

### 1.1.7 LLM Pretraining as MLE

**Example 1.6 (Maximum Likelihood Estimation for Language Models)** Let $\mathbf{x}$ be a document corpus, $\mathbf{x} = (x_1, x_2, x_3, \ldots, x_T)$. An **autoregressive language model** predicts $x_t$ given $x_1, \ldots, x_{t-1}$ using a neural network $f_\theta(\,\cdot \mid x_{1:t-1})$.

The MLE objective is:

$$
\min_\theta \; -\sum_{t=1}^{T} \log f_\theta(x_t \mid x_{1:t-1}).
$$

When $f_\theta$ is a **transformer**, this is exactly the **pretraining of LLMs** (Large Language Models).

TipRemark: How Language Models Work

A language model takes previous words (context) as input and outputs a probability distribution over the next word/token. For example:

- Input context: “The boy went to the”
- Output probabilities: Cafe (0.1), Hospital (0.05), **Playground (0.4)**, Park (0.15), School (0.3)

The probability $P(\text{Playground} \mid \text{The boy went to the}) = 0.4$.

### 1.1.8 Markowitz Portfolio Selection

**Example 1.7 (Markowitz’s Portfolio Selection Model)** Suppose we have 3 assets. Their returns are random variables $X = (X_1, X_2, X_3)^\top$ with:

$$
\mathbb{E}[X] = \mu = \begin{pmatrix} \mu_1 \\ \mu_2 \\ \mu_3 \end{pmatrix}, \quad \text{Cov}(X) = \Sigma = \begin{pmatrix} \Sigma_{11} & \Sigma_{12} & \Sigma_{13} \\ - & - & - \\ - & \cdots & \Sigma_{33}\end{pmatrix}.
$$

Let $w \in \mathbb{R}^3$ be a weight vector specifying how we invest in these three assets, with $\sum_{i=1}^{3} w_i = 1$ and $w_i \geq 0$. Our portfolio return is:

$$
Y_w = \sum_{i=1}^{3} w_i \cdot X_i, \quad \mathbb{E}[Y_w] = w^\top \mu, \quad \text{Var}(Y_w) = w^\top \Sigma\, w.
$$

**Goal:** Choose the best $w$ that minimizes $\text{Var}(Y_w)$ while achieving a desired return $R$:

$$
\begin{aligned}
\min_{w} \quad & w^\top \Sigma\, w \\
\text{s.t.} \quad & w^\top \mu \geq R \\
& \textstyle\sum w_i = 1 \\
& w_i \geq 0, \quad i = 1, 2, 3.
\end{aligned}
$$

This is a **constrained quadratic optimization** problem.

Markowitz efficient frontier. Each grey dot represents a feasible portfolio; the frontier curve traces the minimum variance achievable for each level of expected return. Diversification allows portfolios that are less risky than any individual asset.

## 1.2 General Form of Optimization

We have seen that statistical estimation, machine learning, and finance all lead to optimization problems with shared mathematical structure. The general form of an optimization problem is:

$$
\begin{aligned}
\min_{x} \quad & f(x) & & \text{(objective function)} \\
\text{s.t.} \quad & g_i(x) \leq b_i, & & i = 1, 2, \ldots, m \\
& h_j(x) = 0, & & j = 1, 2, \ldots, \ell \\
& x \in \mathcal{X}
\end{aligned}
$$

In a more abstract form: $\min_x \; f(x) \quad \text{s.t.} \quad x \in \text{Constraint}.$

But optimization in general is NP-hard — there is no hope of efficiently solving arbitrary problems. The key insight is that a large and practically important class of problems, called **convex optimization** problems, can always be solved efficiently.

## 1.3 Convex Optimization

**Definition 1.5 (General Form of Convex Optimization)** A convex optimization problem takes the general form:

$$
\begin{aligned}
\min_{x} \quad & f(x) && \text{(convex objective function)} \\
\text{s.t.} \quad & g_i(x) \leq b_i, && i = 1, 2, \ldots, m \\
& h_j(x) = 0, && j = 1, 2, \ldots, \ell \\
& x \in \mathcal{X}
\end{aligned} \tag{1.9}
$$

where $f$ is a **convex objective function** and the constraints $g_i(x) \leq b_i$, $h_j(x) = 0$ define a **convex feasible set**.

A convex optimization problem is one where both the objective function and the feasible region are convex. This structure is powerful because it guarantees that any local minimum is automatically a global minimum, which makes the problem tractable for efficient algorithms.

TipRemark: Why Convexity Matters

A key geometric property of convex sets: for any two points $x, y$ in a convex set, the line segment connecting them lies entirely within the set. That is, $\lambda x + (1-\lambda)y$ is in the set for all $\lambda \in [0,1]$.

For convex functions: **every local minimum is a global minimum**. This makes convex optimization problems tractable (solvable in polynomial time), while general optimization is typically NP-hard.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/optimization-landscape.svg)

Figure 1.1: Optimization landscape showing local minimum, local maximum, global minimum, and constrained optimum within a feasible region. In high-dimensional non-convex optimization, most stationary points that appear as local minima or local maxima in 1D are in fact saddle points — critical points where the Hessian has both positive and negative eigenvalues.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch01-convex-vs-nonconvex.svg)

Figure 1.2: Left — A convex function with a unique global minimum. Right — A non-convex function with multiple local minima. In convex optimization, any local minimum is a global minimum.

Figure 1.3: A saddle point of f(x,y) = x² − y² at the origin. Along the x-direction (blue curve), the surface curves upward — the origin is a local minimum. Along the y-direction (red curve), the surface curves downward — the origin is a local maximum. The Hessian at the origin has one positive and one negative eigenvalue.

TipRemark: Saddle Points in High Dimensions

In high-dimensional non-convex optimization (e.g., training deep neural networks), most critical points are **saddle points**, not true local minima or maxima. A saddle point is a critical point where the Hessian has both positive and negative eigenvalues — the function curves upward in some directions and downward in others, as shown in the 3D figure above. In $d$ dimensions, a random critical point is exponentially more likely to be a saddle point than a local minimum, since each eigenvalue of the Hessian is independently likely to be positive or negative.

## 1.4 Course Overview

**Focus:** We will mainly focus on **convex optimization**.

- Optimization is generally **hard** (NP-hard).
- But we can always **solve** convex optimization (in polynomial time).

What do we mean by “hard” or “solve”? This is formalized through run-time complexity and oracle computation models. The course is organized around three main questions:

**Three main questions:**

1. **What optimization problems?**
2. **What algorithms?**
3. **How do we know we have solved the problem?**

### 1.4.1 1. What Optimization Problems?

- We will cover **theory & algorithms of convex optimization**.
	- Why? This is a class of **tractable** problems that can be solved in a principled fashion.
- We will also cover some **nonconvex optimization** problems:
	- With important applications in **deep learning & AI**
		- Interesting phenomena not present in the convex world

### 1.4.2 2. What Algorithms?

1. **Unconstrained optimization**
	- **First-order methods** (gradient descent, stochastic gradient descent, projected gradient descent)
		- Second-order methods
2. **Constrained optimization**
	- Linear programming $\rightarrow$ Simplex method, Ellipsoid method
		- General constrained problems $\rightarrow$ Interior point methods

### 1.4.3 3. How Do We Know We Have Solved the Problem?

- **Duality**, **Lagrange multipliers**, **KKT conditions**

Figure 1.4: The landscape of optimization problems covered in this course, from linear programs to general convex optimization and beyond.

## Summary

- **Optimization as a unifying framework.** Many statistical and machine learning problems — maximum likelihood estimation, OLS, Ridge, Lasso regression, LLM pretraining, and portfolio optimization — reduce to minimizing an objective $\min_{x} f(x)$ subject to constraints, placing them under the umbrella of mathematical optimization.
- **Empirical risk minimization (ERM).** Supervised learning seeks parameters $\theta$ that minimize the empirical risk $\frac{1}{n}\sum_{i=1}^{n}\ell(h_\theta(x_i), y_i)$; the choice of loss $\ell$ and hypothesis class $h_\theta$ determines the optimization landscape.
- **Key problem classes.** Linear programs (LP), quadratic programs (QP), and general convex programs each carry different structural guarantees; recognizing the class determines which algorithms and solvers apply.
- **Convex vs. nonconvex problems.** Convex problems (e.g., OLS, Ridge, Lasso) admit global solutions efficiently because every local minimum is a global minimum. Nonconvex problems (e.g., neural network training) lack this guarantee and require careful algorithm design.
- **Role of regularization.** Adding a penalty term — $\|\theta\|_2^2$ for Ridge or $\|\theta\|_1$ for Lasso — controls model complexity and induces desirable structure such as sparsity.
- **Course roadmap.** The course progresses from convex analysis and duality theory, through first- and second-order algorithms, to LP-specific methods (simplex, interior point) and modern applications (diffusion models, transformers).

TipLooking Ahead

In the next chapter, we establish the **mathematical foundations** — norms for measuring distance, matrix decompositions for revealing structure, gradients and Hessians for guiding descent, and automatic differentiation for computing gradients efficiently. These tools form the vocabulary that every optimization algorithm in this course builds upon.