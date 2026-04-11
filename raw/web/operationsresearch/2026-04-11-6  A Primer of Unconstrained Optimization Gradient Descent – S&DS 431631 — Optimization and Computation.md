---
author: null
created: 2026-04-11
description: null
published: null
source: https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html
tags:
- clippings
title: '6  A Primer of Unconstrained Optimization: Gradient Descent – S&DS 431/631
  — Optimization and Computation'
topics:
- 运筹优化
source_type: local_note
created_at: 2026-04-11
---
In the previous chapters we developed a rich theory of convex optimization – convex sets, convex functions, and problem formulations – that tells us *what* an optimal solution looks like (for instance, a point where the gradient vanishes). But how do we actually *find* one? For most problems of practical interest, closed-form solutions do not exist, and we must turn to iterative algorithms that start from an initial guess and progressively improve it.

The most natural idea is to use the gradient. The gradient of a function at a point tells us the direction of steepest ascent; moving in the opposite direction decreases the function value. This simple principle – “follow the negative gradient” – is the basis of **gradient descent**, one of the most fundamental algorithms in all of computational mathematics. It is the workhorse of modern machine learning (training neural networks), statistics (fitting models), and scientific computing.

But gradient descent is just one member of a larger family. By choosing different descent directions (coordinate descent, Newton’s method) and different step size strategies (constant, diminishing, line search), we obtain a rich design space of first-order and second-order methods with different tradeoffs between computational cost per iteration and convergence speed. Understanding this design space is essential for choosing the right algorithm in practice.

TipCompanion Notebooks

Hands-on Python notebooks accompany this chapter. Click a badge to open in Google Colab.

- **Steepest Descent** — steepest descent on quadratics with varying condition numbers
- **Learning Rate Analysis** — how learning rate and curvature interact in gradient descent convergence
- **GD Visualization** — animated gradient descent trajectories on various objective landscapes

## What Will Be Covered

- Unconstrained optimization setup: stationary points and optimality conditions
- The general iterative framework: descent directions and step sizes
- Steepest descent under different norms: $\ell_2$ (gradient descent), $\ell_1$ (coordinate descent), $\ell_\infty$ (sign gradient descent), spectral norm (Muon optimizer)
- Newton’s method and diagonally scaled descent (preview)
- Step size strategies: constant, diminishing, and backtracking line search
- Convergence analysis: smoothness, strong convexity, the condition number, and the descent lemma
- Three convergence cases: nonconvex + smooth, convex + smooth, strongly convex + smooth
- The Polyak–Łojasiewicz condition and linear convergence without convexity

## 6.1 Unconstrained Optimization Setup

We consider the unconstrained optimization problem:

$$
\min_{x \in \mathbb{R}^n} f(x),
$$

where $f$ is continuously differentiable ($f \in C^1$).

TipRemark: Convexity and Local Minima

When $f$ is **convex**, global minimum = local minimum.

In the unconstrained case, $x^*$ is a local minimum    $\iff$ $\nabla f(x^*) = 0$.

### 6.1.1 Stationary Points

The key insight that connects calculus to optimization is that, for convex functions, the familiar condition “derivative equals zero” is both necessary and sufficient for optimality. This means that finding the minimum of a convex function reduces to finding a point where the gradient vanishes.

**Theorem 6.1 (Optimality Condition for Convex Functions)** Let $f$ be convex and differentiable. Then $x_0$ is a local minimum of $f$ if and only if $\nabla f(x_0) = 0$.

*Proof*. **($\Rightarrow$):** Define a univariate function $g(t) = f(x_0 - t \cdot \nabla f(x_0))$. Since $x_0$ is a local minimum of $f$, $t = 0$ is a local minimum of $g$. Therefore:

$$
0 = g'(t)\big|_{t=0} = -\|\nabla f(x_0)\|^2 \implies \nabla f(x_0) = 0.
$$

**($\Leftarrow$):** On the other hand, if $\nabla f(x_0) = 0$, then by the first-order characterization of convexity:

$$
f(x) \geq f(x_0) + \langle \nabla f(x_0),\, x - x_0 \rangle = f(x_0) + 0 = f(x_0) \quad \forall\, x \in \mathbb{R}^n,
$$

where the second equality uses $\nabla f(x_0) = 0$. This shows $x_0$ is a global minimizer. Hence we conclude the proof. $\blacksquare$

For nonconvex functions, the condition $\nabla f(x) = 0$ does not guarantee a global minimum – it could also be a local minimum, a local maximum, or a saddle point. Nevertheless, finding stationary points is still the primary goal of first-order algorithms, since it is the best we can guarantee without convexity.

**Definition 6.1 (Stationary Point)** For any differentiable $f$ (possibly nonconvex), $x$ is called a **stationary point** of $f$ if $\nabla f(x) = 0$.

ImportantOptimality    $\iff$ Stationarity (Unconstrained Convex Case)

For **unconstrained minimization of a convex, differentiable** $f$, [Theorem 6.1](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#thm-optimality-convex) shows that the following are equivalent:

$$
x^* \text{ is a global minimizer of } f \quad \iff \quad \nabla f(x^*) = 0.
$$

This is the key reduction that makes convex optimization tractable: instead of searching over all of $\mathbb{R}^n$ for a global minimum, we only need to **find a stationary point**. The entire algorithmic program of this chapter — gradient descent, coordinate descent, Newton’s method — is built on this equivalence. Each method is simply a different strategy for solving the nonlinear equation $\nabla f(x) = 0$.

### 6.1.2 Motivation for Iterative Methods

To minimize a convex and differentiable $f$, it suffices to find a **stationary point**. Finding a stationary point is equivalent to solving the equation $\nabla f(x) = 0$.

This can be done by **“local” algorithms** — iterative algorithms that update using “local information” at each iterate. The three levels of local information, in order of increasing richness, are:

- **Function value** — zeroth-order information (the cheapest to evaluate).
- **Gradient** — first-order information (the workhorse of most practical methods).
- **Hessian** — second-order information (the most expensive, but captures curvature).

### 6.1.3 General Iterative Framework

With the goal of finding a stationary point established, we now introduce the general iterative framework that all descent methods share. Every method we study in this chapter—gradient descent, coordinate descent, Newton’s method—is a special case of this template.

The general form of the iterative algorithm is:

$$
x^{k+1} = x^k + \alpha^k \cdot d^k \tag{6.1}
$$

where we write $k$ as the superscript (iteration index):

- $k \in \{1, 2, \ldots\}$: index of the iteration number.
- $x^k \in \mathbb{R}^n$: current point (current iterate).
- $x^{k+1} \in \mathbb{R}^n$: next point.
- $d^k \in \mathbb{R}^n$: direction to move along at iteration $k$ (**descent direction**).
- $d^k$ uses the local information at $x^k$.
- $\alpha^k > 0$: step size at iteration $k$.

The two design choices—the descent direction $d^k$ and the step size $\alpha^k$ —determine the algorithm’s behavior. The next several sections address these choices in turn: first, which directions guarantee descent; then, specific algorithmic instantiations; and finally, how to pick the step size.

## 6.2 Descent Directions and the Gradient

The descent direction $d^k$ is based on the gradient $\nabla f(x^k)$ (and maybe other information such as the Hessian $\nabla^2 f(x^k)$, previous gradients $\{\nabla f(x^j)\}_{j < k}$, etc.).

The simplest and most natural choice is $d^k = -\nabla f(x^k)$. Why?

### 6.2.1 Why the Negative Gradient?

The idea comes from **linearization**. Near the current point $x$, Taylor expansion gives

$$
f(x + \alpha\, d) \approx f(x) + \alpha \cdot \langle \nabla f(x),\, d \rangle.
$$

If we want to decrease $f$ as fast as possible, we should choose $d$ to minimize the linear term $\langle \nabla f(x), d \rangle$. Of course, without a constraint on $\|d\|$, we could make this arbitrarily negative. So the natural question is: **among all unit-norm directions, which one decreases $f$ at the fastest rate?**

**Theorem 6.2 (Steepest Descent Direction)** Assuming $d \in B_2(1) = \{v \in \mathbb{R}^n \mid \|v\|_2 \leq 1\}$, the direction that decreases $f$ at the **fastest rate** within $B_2(1)$ is given by

$$
d^* = -\frac{\nabla f(x)}{\|\nabla f(x)\|_2}. \tag{6.2}
$$

This is why gradient descent is also called the “method of **steepest descent**.”

*Proof*. We want to maximize the instantaneous rate of decrease $-\langle \nabla f(x), d \rangle$ over unit-norm directions, i.e., solve

$$
\min_{d \in B_2(1)} \; d^\top \nabla f(x).
$$

By the Cauchy–Schwarz inequality, $d^\top \nabla f(x) \geq -\|d\|_2 \cdot \|\nabla f(x)\|_2$, with equality when $d$ is a negative scalar multiple of $\nabla f(x)$. Since $\|d\|_2 \leq 1$, the minimizer is $d^* = -\nabla f(x) / \|\nabla f(x)\|_2$. $\blacksquare$

TipRemark: Magnitude of the Direction

When we talk about the search direction $d$, its magnitude does not matter. $5\,\nabla f(x)$, $0.01\,\nabla f(x)$, $\frac{\nabla f(x)}{\|f(x)\|}$ are all in the same direction. We use the step size $\alpha$ to adjust the magnitude.

### 6.2.2 General Descent Directions

The negative gradient is the steepest descent direction, but it is not the only direction that decreases the function. Any direction that makes an acute angle with the negative gradient – equivalently, an obtuse angle with the gradient – will also decrease the objective for a sufficiently small step. This flexibility is important because alternative descent directions (such as Newton’s direction) can converge much faster in practice.

**Definition 6.2 (Descent Direction)** For a given point $x \in \mathbb{R}^n$, a direction $d \in \mathbb{R}^n$ is called a **descent direction** if there exists $\bar{\alpha} > 0$ such that

$$
f(x + \alpha \cdot d) < f(x) \qquad \forall\, \alpha \in (0, \bar{\alpha}).
$$

Intuitively, $d$ is a descent direction means we can move at least a small step along $d$ and decrease the objective function.

### 6.2.3 Descent Condition

The definition above is existential — it says *some* small step works, but doesn’t tell us how to check. The following lemma gives a **simple, checkable condition**: its inner product with the gradient must be negative.

**Theorem 6.3 (Descent Condition)** Consider a point $x \in \mathbb{R}^n$. Any direction $d$ satisfying

$$
\langle d, \nabla f(x) \rangle < 0 \tag{6.3}
$$

is a descent direction. Geometrically, $d$ and $\nabla f(x)$ form an **obtuse angle**.

Why does this work? The gradient $\nabla f(x)$ points in the direction of steepest *increase*. Any direction $d$ that makes an obtuse angle with $\nabla f(x)$ has a negative projection onto the gradient — so the linear approximation $f(x) + \langle \nabla f(x), d \rangle$ decreases. The proof below makes this precise by showing the linear term dominates the higher-order remainder for small steps.

This condition is much more permissive than steepest descent: the negative gradient is the *best* descent direction, but the entire **half-space** of directions opposite to $\nabla f(x)$ also works. This flexibility is what allows us to use alternative descent directions (such as Newton’s direction or coordinate descent directions) that may converge faster.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch06-descent-direction.svg)

Figure 6.1: Any direction forming an obtuse angle with the gradient is a descent direction. The half-space { d: ⟨, ∇ f ( x ) ⟩ < 0 } \\{d: \\langle d, \\nabla f(x) \\rangle < 0\\} contains all descent directions, including the steepest descent − -\\nabla f(x).

*Proof*. Define $g(\alpha) = f(x + \alpha \cdot d)$. By Taylor expansion at $\alpha = 0$:

$$
g(\alpha) = g(0) + g'(0) \cdot \alpha + o(\alpha) \qquad \text{where } \lim_{\alpha \to 0} \frac{|o(\alpha)|}{\alpha} = 0.
$$

Therefore:

$$
f(x + \alpha \cdot d) - f(x) = \alpha \cdot \langle d,\, \nabla f(x) \rangle + o(\alpha),
$$

where the leading term $\alpha \cdot \langle d, \nabla f(x) \rangle$ is negative by assumption. Since $\frac{|o(\alpha)|}{\alpha} \to 0$, the higher-order remainder becomes negligible for small $\alpha$. Specifically, there exists $\bar{\alpha} > 0$ such that

$$
\frac{|o(\alpha)|}{\alpha} < |\langle d,\, \nabla f(x) \rangle| \qquad \forall\, \alpha \in (0, \bar{\alpha}).
$$

Therefore, for all $\alpha \in (0, \bar{\alpha})$:

$$
f(x + \alpha \cdot d) - f(x) = \alpha \cdot \langle d,\, \nabla f(x) \rangle + o(\alpha) < 0,
$$

which shows that $d$ is a descent direction. This completes the proof. $\blacksquare$

### 6.2.4 Positive Definite Scaling

We now know that *any* direction satisfying $\langle d, \nabla f(x) \rangle < 0$ works. A natural and powerful way to produce such directions is to premultiply the gradient by a **positive definite matrix** $B$: setting $d = -B\nabla f(x)$ automatically satisfies the descent condition. Different choices of $B$ give different algorithms — this single idea unifies gradient descent, Newton’s method, and quasi-Newton methods.

**Theorem 6.4 (Positive Definite Descent)** Let $B \in \mathbb{R}^{n \times n}$ be a positive definite matrix. For any point $x$ with $\nabla f(x) \neq 0$, $d = -B\,\nabla f(x)$ is a descent direction.

*Proof*. With $d = -B\,\nabla f(x)$:

$$
d^\top \nabla f(x) = -\nabla f(x)^\top B\,\nabla f(x) < 0,
$$

where the strict inequality follows from positive definiteness ($v^\top B v > 0$ for all $v \neq 0$) and $\nabla f(x) \neq 0$. By the descent condition ([Equation 6.3](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-descent-condition)), $d$ is a descent direction. $\blacksquare$

By choosing different positive definite matrices $B^k$ at each iteration, we recover a family of algorithms under the general update rule:

$$
x^{k+1} = x^k - \alpha^k \cdot B^k\, \nabla f(x^k). \tag{6.4}
$$

## 6.3 Common Choices of Descent Directions

Having established the general framework, we now explore specific choices. The unifying idea is **steepest descent under different norms**: given a norm $\|\cdot\|$ on $\mathbb{R}^n$, find the direction that decreases the linear approximation the fastest within the unit ball:

$$
d^* = \operatorname{argmin}_{d:\,\|d\| \leq 1} \langle \nabla f(x),\, d \rangle.
$$

Different norms yield different unit balls, which yield different optimal directions. The $\ell_2$ -ball is a sphere (giving gradient descent), the $\ell_1$ -ball is a diamond (giving coordinate descent), and the $\ell_\infty$ -ball is a cube (giving sign gradient descent). Each can also be viewed as a different choice of $B^k$ in the general update [Equation 6.4](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-general-update).

### 6.3.1 Steepest Descent with ℓ2\\ell\_2-norm (Gradient Descent)

With the $\ell_2$ -norm:

$$
\operatorname{argmin}_{d:\,\|d\|_2 \leq 1} \langle \nabla f(x),\, d \rangle = -\frac{\nabla f(x)}{\|\nabla f(x)\|_2}.
$$

This corresponds to $B^k = I$, giving the standard **gradient descent** update:

$$
x^{k+1} = x^k - \alpha^k \cdot \nabla f(x^k). \tag{6.5}
$$

TipRemark: Sensitivity to Condition Number

This is the simplest direction but **not always the fastest**. It has poor performance when the **condition number** $\frac{\lambda_{\max}(\nabla^2 f)}{\lambda_{\min}(\nabla^2 f)}$ is large. The iterates oscillate in the dimension with the large eigenvalue and make fast progress in the dimension with the small eigenvalue.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch05-condition-number.svg)

Figure 6.2: Effect of the condition number κ = L / μ \\kappa = L/\\mu on gradient descent convergence. When \\kappa is close to 1 (left), the contours are nearly circular and GD converges quickly along a direct path. When is large (right), the contours are elongated ellipses and GD zig-zags across the narrow valley, making slow progress toward the optimum.

Figure 6.1: Gradient descent on an ill-conditioned quadratic. The iterates oscillate perpendicular to the valley and make slow progress along it.

### 6.3.2 Oscillation Analysis

**Example 6.1 (Example: 1D Quadratic)** Consider the 1D case: $f(x) = \tfrac{1}{2}a\,x^2$, so $f'(x) = a\,x$ and $f''(x) = a$.

Solution: $x^* = 0$. Gradient descent gives:

$$
x' = x - \alpha \cdot f'(x) = (1 - a \cdot \alpha) \cdot x.
$$

Therefore $|x'| = |1 - a \cdot \alpha| \cdot |x|$, and after $k$ steps:

$$
|x^k| = |1 - a \cdot \alpha|^k \cdot |x^0|. \tag{6.6}
$$

- If $\alpha$ is large such that $|1 - a \cdot \alpha| \geq 1$: **Non-convergence**.
- If $|1 - a \cdot \alpha| < 1$: **Exponential (linear rate) convergence**. To get $|x^k| \leq \varepsilon$, need $k = O(\log(1/\varepsilon))$.

So we need $0 < \alpha < 2/a$:

- If $\alpha \in (0, 1/a)$: $1 - a\alpha \in (0,1)$, and $\{x^k\}$ **monotonically converges** to 0.
- If $\alpha \in (1/a, 2/a)$: $1 - a\alpha \in (-1,0)$, and $\{x^k\}$ **oscillates** to 0.

The convergence rate is controlled by the **contraction factor** $|1 - a\alpha|$: it depends on both the curvature $a$ and the step size $\alpha$. The optimal choice $\alpha^* = 1/a$ gives $|1-a\alpha^*| = 0$, so GD solves the 1D problem in **one step**. But in higher dimensions, we cannot simultaneously zero out the contraction factor for all eigenvalues.

**Example 6.2 (Example: 2D Quadratic — Zig-Zag Behavior)** Consider the 2D case: $f(x, y) = \tfrac{1}{2}(a\,x^2 + b\,y^2)$ with $a < b$. GD gives:

$$
\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} (1 - a \cdot \alpha)\, x \\ (1 - b \cdot \alpha)\, y \end{pmatrix}.
$$

To get convergence, we need $|1 - a\alpha| < 1$ and $|1 - b\alpha| < 1$, which gives $\alpha \in (0, 2/b)$.

If $\alpha \in (1/b, 2/b)$: $\{x^k\}$ monotonically converges to 0 (since $1-a\alpha > 0$), while $\{y^k\}$ oscillates to 0 (since $1-b\alpha < 0$). This produces a **zig-zag trajectory**.

**What is the best step size?** The overall convergence rate is controlled by the *worst* contraction factor:

$$
\rho(\alpha) = \max\{|1 - a\alpha|,\; |1 - b\alpha|\}.
$$

We want to choose $\alpha$ to minimize $\rho(\alpha)$. As $\alpha$ increases from $0$, $|1-a\alpha|$ decreases while $|1-b\alpha|$ decreases faster then increases. The optimal $\alpha$ balances the two:

$$
1 - a\alpha = -(1 - b\alpha) \;\implies\; \alpha^* = \frac{2}{a + b}.
$$

At this step size, the contraction factor is:

$$
\rho^* = 1 - a \cdot \frac{2}{a+b} = \frac{b - a}{b + a} = \frac{\kappa - 1}{\kappa + 1}, \qquad \text{where } \kappa = b/a
$$

is the **condition number** of the Hessian. When $\kappa \approx 1$ (nearly equal curvatures), $\rho^* \approx 0$ and GD converges quickly. When $\kappa \gg 1$ (very different curvatures), $\rho^* \approx 1$ and convergence is slow. This quadratic warm-up foreshadows the general theory: **the condition number $\kappa$ governs the convergence speed of gradient descent**.

Figure 6.2: Zig-zag trajectory of gradient descent on a 2D quadratic with different eigenvalues. The iterate oscillates in the y-direction while progressing monotonically in x.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/gradient-descent-convergence.svg)

Figure 6.3: Gradient descent trajectories: smooth convex objective with O ( 1 / k ) O(1/k) convergence (left) versus strongly convex objective with linear ρ O(\\rho^k) convergence (right). The condition number κ = L μ \\kappa = L/\\mu controls the eccentricity of the contours.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/convergence-rates-comparison.svg)

Figure 6.4: Comparison of convergence rates encountered in first-order optimization. From slowest to fastest: O ( 1 / k ) O(1/\\sqrt{k}) for subgradient methods on nonsmooth problems, O(1/k) for GD on smooth convex functions, 2 O(1/k^2) for accelerated methods, and linear ρ O(\\rho^k) convergence for strongly convex objectives. The gap between these rates motivates the momentum and adaptive methods studied in subsequent chapters.

### 6.3.3 GD as Quadratic Upper Bound Minimization

There is a deeper way to understand the GD update that will be the key to all convergence proofs. Two observations:

1. **The GD update minimizes a simple surrogate.** Define

$$
g_{\alpha}(x) = f(x^k) + \langle \nabla f(x^k),\, x - x^k \rangle + \frac{1}{2\alpha} \|x - x^k\|_2^2.
$$

This is the first-order Taylor expansion of $f$ at $x^k$, plus a **proximity penalty** that prevents us from moving too far. Setting the gradient to zero: $\nabla f(x^k) + \frac{1}{\alpha}(x - x^k) = 0$, which gives $x = x^k - \alpha \nabla f(x^k)$. This is exactly the GD update! So:

$$
x^{k+1} = \operatorname{argmin}_{x \in \mathbb{R}^n}\; g_{\alpha^k}(x).
$$

1. **When $\alpha$ is small enough, the surrogate upper-bounds $f$.** When $\alpha \leq 1/\lambda_{\max}(\nabla^2 f(x^k))$, the quadratic penalty $\frac{1}{2\alpha}\|x - x^k\|_2^2$ dominates the true curvature, so $g_\alpha(x) \geq f(x)$ for all $x$.

Combining these two observations: **GD minimizes a quadratic upper bound of $f$**. Since $f(x^{k+1}) \leq g_\alpha(x^{k+1}) \leq g_\alpha(x^k) = f(x^k)$, each step is guaranteed to decrease the objective. This is the intuition behind the descent lemma that we will prove formally in [Theorem 6.5](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#thm-descent-lemma).

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch05-quadratic-upper-bound.svg)

Figure 6.5: Gradient descent as quadratic upper bound minimization. At the current iterate x k x^k, the quadratic surrogate g α ( ) g\_\\alpha(x) (dashed) upper-bounds the true objective f f(x) (solid). The GD step moves to the minimizer of the surrogate. With a smaller stepsize \\alpha, the surrogate is tighter (steeper parabola) and the step is more conservative.

### 6.3.4 Steepest Descent with ℓ1\\ell\_1-norm (Coordinate Descent)

With the $\ell_1$ -norm, the unit ball $\{d : \|d\|_1 \leq 1\}$ is a diamond (cross-polytope). Its extreme points are the standard basis vectors $\pm e_j$. Since the linear objective $\langle \nabla f(x), d \rangle$ is minimized at an extreme point, the solution picks a single coordinate:

$$
\operatorname{argmin}_{d:\,\|d\|_1 \leq 1} \langle d,\, \nabla f(x) \rangle.
$$

**Solution:** $d^* \in \mathbb{R}^n$ has only **one nonzero entry**:

$$
d^*_j = \begin{cases} -\operatorname{sign}\!\bigl(\frac{\partial f}{\partial x_j}(x)\bigr) & \text{if } j = \operatorname{argmax}_j \bigl|\frac{\partial f}{\partial x_j}(x)\bigr| \\[4pt] 0 & \text{otherwise.} \end{cases}
$$

Note that the magnitude does not matter. We can choose $d^*$ with magnitude:

$$
d^*_j = -\bigl|\tfrac{\partial f}{\partial x_j}(x)\bigr| \cdot \operatorname{sign}\!\bigl(\tfrac{\partial f}{\partial x_j}(x)\bigr) = -\tfrac{\partial f}{\partial x_j}(x).
$$

This gives the **coordinate descent** update: pick $i = \operatorname{argmax}_j \bigl|\frac{\partial f}{\partial x_j}(x^k)\bigr|$, then

$$
(x^{k+1})_i = (x^k)_i - \alpha^k \cdot \frac{\partial f}{\partial x_i}(x^k), \qquad (x^{k+1})_\ell = (x^k)_\ell \quad \forall\, \ell \neq i.
$$

TipRemark: Coordinate Descent

This algorithm is called **coordinate descent** because we update only one coordinate of $x$ at each iteration. In general, at the $k$ -th iteration:

- Pick a coordinate $i \in [n]$ according to some rule.
- Update: $(x^{k+1})_i = (x^k)_i - \alpha^k \cdot \frac{\partial f}{\partial x_i}(x^k)$ (only update coordinate $x_i$).

This corresponds to $B^k$ being a diagonal matrix with a single nonzero entry.

### 6.3.5 Steepest Descent with ℓ∞\\ell\_\\infty-norm (Sign Gradient Descent)

The $\ell_\infty$ -ball $\{d : \|d\|_\infty \leq 1\}$ is a cube. Its extreme points are the corners $\{\pm 1\}^n$. The linear objective is minimized by choosing each coordinate independently: $d_j^* = -\operatorname{sign}(\partial f / \partial x_j)$.

With the $\ell_\infty$ -norm:

$$
\operatorname{argmin}_{d:\,\|d\|_\infty \leq 1} \langle d,\, \nabla f(x) \rangle = -\operatorname{sign}(\nabla f(x)) = -\begin{pmatrix} \operatorname{sign}\!\bigl(\frac{\partial f}{\partial x_1}(x)\bigr) \\ \operatorname{sign}\!\bigl(\frac{\partial f}{\partial x_2}(x)\bigr) \\ \vdots \\ \operatorname{sign}\!\bigl(\frac{\partial f}{\partial x_n}(x)\bigr) \end{pmatrix} \in \{\pm 1\}^n.
$$

The update is:

$$
x^{k+1} = x^k - \alpha^k \cdot \operatorname{sign}(\nabla f(x^k)).
$$

TipRemark: Sign Gradient Descent and Adam

This algorithm is called **sign gradient descent**. It only uses the sign of each partial derivative, ignoring magnitudes. It is related to the Adam optimizer commonly used in deep learning.

### 6.3.6 Steepest Descent with Spectral Norm (Matrix Optimization)

When the optimization variable is a **matrix** $W \in \mathbb{R}^{m \times n}$ — for example, a weight matrix in a neural network — we can choose the **spectral norm** (operator norm) $\|D\|_{\mathrm{op}} = \sigma_{\max}(D)$ as the geometry:

$$
d^* = \operatorname{argmin}_{D:\,\|D\|_{\mathrm{op}} \leq 1} \langle \nabla f(W),\, D \rangle_F,
$$

where $\langle A, B \rangle_F = \operatorname{tr}(A^\top B)$ is the Frobenius inner product. This is the natural norm for the matrix viewed as a linear operator, treating all singular-value directions on an equal footing.

**Solution.** Let $\nabla f(W) = U \Sigma V^\top$ be the (compact) singular value decomposition. By the duality between the spectral norm and the nuclear norm $\|G\|_* = \sum_i \sigma_i(G)$, the minimizer is

$$
d^* = -U V^\top.
$$

The steepest descent update becomes:

$$
W^{k+1} = W^k - \alpha^k \cdot U^k (V^k)^\top,
$$

where $\nabla f(W^k) = U^k \Sigma^k (V^k)^\top$. The update direction $UV^\top$ is a partial isometry (orthogonal matrix when $m = n$): it retains only the *directional* information of the gradient, discarding all singular value magnitudes. Contrast this with standard gradient descent on matrices, which uses the Frobenius norm $\|D\|_F$ (equivalent to $\ell_2$ on the vectorized matrix) and simply sets $d^* = -\nabla f(W) / \|\nabla f(W)\|_F$ — preserving the (often skewed) singular value profile.

TipRemark: The Muon Optimizer

The **Muon** (Momentum + Orthogonalization) optimizer combines spectral steepest descent with [Nesterov momentum](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html):

1. Update momentum buffer: $M \leftarrow \beta M + \nabla f(W)$.
2. **Orthogonalize:** compute the SVD $M = U\Sigma V^\top$ and set the update direction to $UV^\top$.
3. Update: $W \leftarrow W - \alpha \cdot UV^\top$.

Computing the full SVD at every step would be prohibitively expensive for large weight matrices. In practice, the orthogonalization $M \mapsto UV^\top$ is approximated efficiently using a **Newton–Schulz iteration** — a simple matrix recurrence that converges to $UV^\top$ without explicitly computing singular values. We discuss such numerical methods in the [second-order methods](https://zhuoranyang.github.io/sds431-notes/lectures/14-newton-method.html) part of this book.

The related **SOAP** optimizer combines spectral preconditioning with adaptive learning rates in a similar spirit. These spectral methods have shown strong empirical performance for training large-scale neural networks, where the weight matrices are naturally high-dimensional linear operators.

### 6.3.7 Newton’s Method

The previous methods used only first-order (gradient) information. **Newton’s method** incorporates second-order information — the Hessian matrix — to adapt the search direction to the local curvature. Set $B^k = (\nabla^2 f(x^k))^{-1}$:

ImportantAlgorithm: Newton’s Method

$$
x^{k+1} = x^k - \bigl(\nabla^2 f(x^k)\bigr)^{-1} \nabla f(x^k). \tag{6.7}
$$

The intuition: recall from [Section 6.3.3](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#sec-gd-surrogate) that GD minimizes a quadratic surrogate with an isotropic proximity penalty $\frac{1}{2\alpha}\|x - x^k\|^2$. Newton’s method replaces this with the **exact local curvature** by minimizing the second-order Taylor expansion

$$
g_{x^k}(x) = f(x^k) + \langle \nabla f(x^k),\, x - x^k \rangle + \tfrac{1}{2}(x - x^k)^\top \nabla^2 f(x^k)\, (x - x^k).
$$

Setting $\nabla g_{x^k}(x) = 0$ recovers the Newton update. Since the surrogate matches $f$ up to second order, Newton’s method achieves **quadratic convergence** near the solution (the number of correct digits doubles per step), at the cost of computing and inverting the $n \times n$ Hessian ($O(n^3)$ per iteration). If $f$ is quadratic, the second-order Taylor expansion is exact, so Newton’s method converges in **one step**.

We develop the full theory of Newton’s method — convergence analysis, damped Newton steps, and the connection to interior-point methods — in [Chapter 14](https://zhuoranyang.github.io/sds431-notes/lectures/14-newton-method.html).

### 6.3.8 Diagonally Scaled Steepest Descent

Set $B^k = \operatorname{diag}(b_1, b_2, \ldots, b_n)$, for example:

$$
b_j = \Bigl(\frac{\partial^2 f(x^k)}{\partial x_j^2}\Bigr)^{-1},
$$

i.e.,

$$
d^k = \bigl[\operatorname{diag}\bigl(\nabla^2 f(x^k)\bigr)\bigr]^{-1} \nabla f(x^k).
$$

TipRemark: Diagonal Hessian Approximation

This approximates $\nabla^2 f(x^k)$ using only its **diagonal part**, avoiding the cost of a full matrix inversion. It captures per-coordinate curvature information and is related to adaptive methods like AdaGrad.

We have now assembled a toolbox of descent directions—from the simple negative gradient to the curvature-aware Newton direction. But choosing the direction is only half of the update rule [Equation 6.1](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-iterative-update); the other half is the step size $\alpha^k$. A good direction paired with a poor step size can lead to slow convergence or even divergence, as the oscillation analysis in [Example 6.2](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#exm-2d-quadratic-zigzag) illustrated. We turn to step size strategies next.

## 6.4 Choice of Step Sizes

The step size $\alpha^k$ controls how far we move along the descent direction at each iteration. A good step size must balance two competing goals: making enough progress toward the optimum (large $\alpha$) without overshooting and increasing the objective (small $\alpha$).

To see why this balance matters, recall the 1D quadratic example ([Example 6.1](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#exm-1d-quadratic)): on $f(x) = \frac{1}{2}ax^2$, the update $x' = (1 - a\alpha)x$ converges only when $\alpha < 2/a$, and converges fastest at $\alpha^* = 1/a$. In higher dimensions, the curvature varies across directions, so no single step size is optimal everywhere — but the principle remains: **the step size must be calibrated to the curvature of $f$**. A step that is safe for the flattest direction may be far too aggressive for the steepest one.

The three strategies below represent fundamentally different approaches to this calibration problem: ignore curvature entirely (constant), adapt conservatively over time (diminishing), or estimate the right scale at each step (line search).

### 6.4.1 Constant Step Size

The simplest strategy: fix $\alpha^k = \alpha$ for all $k \geq 1$.

- **Simple to implement** — no per-iteration computation of step sizes, no function evaluations beyond the gradient.
- **Requires knowledge of the problem.** The convergence theory (see [Theorem 6.5](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#thm-descent-lemma) below) will show that the step size $\alpha = 1/L$ — the reciprocal of the smoothness constant — guarantees descent. But $L$ may not be known in advance. If $\alpha$ is too large, the iterates overshoot and diverge; if too small, each step makes negligible progress.
- **Most common in practice for neural network training**, where $\alpha$ (the “learning rate”) is treated as a hyperparameter tuned via grid search or heuristics.

**Example 6.3 (Example: Constant Step Size on a Quadratic)** For $f(x) = \frac{1}{2}x^\top Q\,x$ with eigenvalues $\mu \leq \lambda_1 \leq \cdots \leq \lambda_n \leq L$, the GD update is $x^{k+1} = (I - \alpha Q)x^k$. Convergence requires all eigenvalues of $I - \alpha Q$ to have magnitude less than 1, i.e., $\alpha < 2/L$. The optimal constant step size $\alpha^* = 2/(\mu + L)$ gives contraction factor $\frac{\kappa - 1}{\kappa + 1}$ (as derived in [Example 6.2](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#exm-2d-quadratic-zigzag)), where $\kappa = L/\mu$.

### 6.4.2 Diminishing Step Size

When the smoothness constant $L$ is unknown and line search is too expensive, a **diminishing step size** provides a safe default: the step sizes shrink to zero, so the algorithm eventually takes steps small enough to avoid overshooting any curvature. Formally, the step sizes satisfy two conditions:

$$
\alpha^k \to 0 \qquad \text{and} \qquad \sum_{k=1}^{\infty} \alpha^k = +\infty.
$$

For example, $\alpha^k = c/k$ for some constant $c > 0$, or $\alpha^k = c/\sqrt{k}$.

**Why both conditions?** They serve complementary roles:

- **$\sum \alpha^k = +\infty$ (sufficient travel).** The total distance the algorithm can travel is $\sum_k \alpha^k \|\nabla f(x^k)\|$. If $\sum \alpha^k < \infty$, the iterates could converge to a non-stationary point simply because they run out of “fuel” before reaching the optimum. The divergence condition ensures the algorithm can always travel far enough.
- **$\alpha^k \to 0$ (eventual caution).** As the iterates approach the optimum, the gradient becomes small and the linear approximation is valid only in a shrinking neighborhood. Decaying step sizes ensure the algorithm does not overshoot in this delicate regime.

TipRemark: Diminishing vs. Constant Step Sizes

Diminishing step sizes are most important for **stochastic** gradient descent (SGD), where the gradient estimate is noisy. The noise does not vanish as $x^k \to x^*$, so a constant step size causes the iterates to oscillate around the optimum rather than converging. Diminishing steps average out the noise. For deterministic GD with a known smoothness constant, the constant step size $\alpha = 1/L$ is typically preferred.

## 6.5 Convergence Analysis of Gradient Descent

We have developed the gradient descent algorithm and its variants, along with step size strategies. The central question remains: **how fast does gradient descent converge?**

The quadratic warm-up in [Example 6.2](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#exm-2d-quadratic-zigzag) already gave us the answer for one special case: on the quadratic $f(x,y) = \frac{1}{2}(ax^2 + by^2)$, the convergence rate is $\frac{\kappa-1}{\kappa+1}$ where $\kappa = b/a$ is the ratio of curvatures. We now develop the general theory, which shows that this is no coincidence — the convergence rate of GD is always governed by two numbers that bound the **curvature** of $f$:

- **Smoothness parameter $L$:** an upper bound on how fast the gradient changes (curvature from above).
- **Strong convexity parameter $\mu$:** a lower bound on how much the function curves upward (curvature from below).

Their ratio $\kappa = L/\mu$ is the **condition number**, and it controls how many iterations gradient descent needs.

### 6.5.1 Smoothness: Bounding Curvature from Above

The first structural property we need is **smoothness**, which says that the gradient of $f$ does not change too rapidly. Informally, a smooth function has no “sharp bends” in its gradient.

**Definition 6.3 ($L$ -Smoothness)** A differentiable function $f$ is **$L$ -smooth** if its gradient is $L$ -Lipschitz continuous:

$$
\|\nabla f(x) - \nabla f(y)\|_2 \leq L \cdot \|x - y\|_2 \qquad \forall\, x, y.
$$

**What does this mean?** If you move from $x$ to $y$, the gradient cannot change by more than $L$ times the distance you moved. A small $L$ means the gradient changes slowly (the function is “gently curved”), while a large $L$ means the gradient can change rapidly.

**Why do we need this for convergence?** Recall the linearization idea behind GD: we approximate $f(x + \alpha d) \approx f(x) + \alpha \langle \nabla f(x), d \rangle$ and move in the direction that decreases this linear approximation. But this approximation is only valid locally — if the gradient can change wildly (large $L$), a step that looks good based on the current gradient may actually increase $f$. Smoothness quantifies exactly how far we can trust the linear approximation.

The most important consequence of $L$ -smoothness is the **quadratic upper bound**: for all $x, y$,

$$
f(y) \leq f(x) + \nabla f(x)^\top (y - x) + \frac{L}{2}\|y - x\|_2^2. \tag{6.9}
$$

This says that $f$ is bounded above by a quadratic that “hugs” it from above. The linear part $f(x) + \nabla f(x)^\top(y-x)$ is the tangent-line approximation, and the quadratic term $\frac{L}{2}\|y-x\|_2^2$ controls how far $f$ can deviate from this tangent. See [Figure 6.5](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#fig-quadratic-upper-bound) for an illustration.

For twice-differentiable functions, $L$ -smoothness is equivalent to requiring that all eigenvalues of the Hessian are at most $L$:

$$
\nabla^2 f(x) \preceq L \cdot I \qquad \forall\, x.
$$

**Example 6.4 (Example: Quadratic Function)** For $f(x) = \frac{1}{2}x^\top Q\, x$ with $Q \succ 0$, we have $\nabla^2 f(x) = Q$, so $f$ is $L$ -smooth with $L = \lambda_{\max}(Q)$.

### 6.5.2 Strong Convexity: Bounding Curvature from Below

While smoothness bounds curvature from above, **strong convexity** bounds it from below. It says that $f$ curves upward at least as fast as a quadratic.

**Definition 6.4 ($\mu$ -Strong Convexity)** A differentiable function $f$ is **$\mu$ -strongly convex** (with $\mu > 0$) if for all $x, y$:

$$
f(y) \geq f(x) + \nabla f(x)^\top (y - x) + \frac{\mu}{2}\|y - x\|_2^2.
$$

**What does this mean?** Ordinary convexity says that $f$ lies above all of its tangent lines. Strong convexity says something stronger: $f$ lies above all of its tangent lines **plus a quadratic bowl** of curvature $\mu$. The bigger $\mu$ is, the more strongly $f$ curves upward.

TipIntuition: Curvature Sandwich

When $f$ is both $\mu$ -strongly convex and $L$ -smooth, the curvature of $f$ is **sandwiched** between two quadratics:

$$
\underbrace{f(x) + \nabla f(x)^\top(y-x) + \frac{\mu}{2}\|y-x\|_2^2}_{\text{quadratic lower bound}} \;\leq\; f(y) \;\leq\; \underbrace{f(x) + \nabla f(x)^\top(y-x) + \frac{L}{2}\|y-x\|_2^2}_{\text{quadratic upper bound}}.
$$

The left side is a “tight-fitting bowl” from strong convexity, and the right side is a “loose-fitting bowl” from smoothness. The function $f$ is trapped between them.

For twice-differentiable functions, $\mu$ -strong convexity is equivalent to $\nabla^2 f(x) \succeq \mu \cdot I$ for all $x$. Together with smoothness, this means all Hessian eigenvalues are sandwiched:

$$
\mu \cdot I \preceq \nabla^2 f(x) \preceq L \cdot I \qquad \forall\, x.
$$

Strong convexity guarantees two important properties:

1. **Unique minimizer.** A $\mu$ -strongly convex function has exactly one minimizer $x^*$. (If there were two minimizers $x_1^* \neq x_2^*$, applying the definition with $x = x_1^*$ and $y = x_2^*$ would give $f(x_2^*) > f(x_1^*)$, contradicting optimality of $x_2^*$.)
2. **Gradient domination.** For all $x$:

$$
f(x) - f(x^*) \leq \frac{1}{2\mu}\|\nabla f(x)\|_2^2. \tag{6.10}
$$

This says: **when the gradient is small, the function value must be close to optimal**. To see why, minimize the strong convexity lower bound over $y$: $f(y) \geq f(x) + \langle \nabla f(x), y - x \rangle + \frac{\mu}{2}\|y-x\|_2^2$. The right side is minimized at $y = x - \frac{1}{\mu}\nabla f(x)$, giving $f(x^*) \geq f(x) - \frac{1}{2\mu}\|\nabla f(x)\|_2^2$. Rearranging yields [Equation 6.10](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-gradient-domination). This property is so useful that it has its own name — the **Polyak–Łojasiewicz condition** — which we revisit in [Definition 6.6](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#def-pl).

### 6.5.3 The Condition Number

When $f$ is both $\mu$ -strongly convex and $L$ -smooth, the ratio of these two parameters plays a central role.

**Definition 6.5 (Condition Number)** The **condition number** of a $\mu$ -strongly convex and $L$ -smooth function is

$$
\kappa = \frac{L}{\mu} \geq 1.
$$

The condition number measures how “elongated” the contours of $f$ are. When $\kappa \approx 1$, the contours are nearly circular and gradient descent converges quickly in a direct path ([Figure 14.1](https://zhuoranyang.github.io/sds431-notes/lectures/14-newton-method.html#fig-condition-number), left panel). When $\kappa \gg 1$, the contours are elongated ellipses and gradient descent zig-zags slowly toward the optimum ([Figure 14.1](https://zhuoranyang.github.io/sds431-notes/lectures/14-newton-method.html#fig-condition-number), right panel).

Recall from [Example 6.2](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#exm-2d-quadratic-zigzag): on the quadratic $f(x,y) = \frac{1}{2}(ax^2 + by^2)$ with $a < b$, the contraction factors are $|1-a\alpha|$ and $|1-b\alpha|$. With the optimal step size $\alpha = 2/(a+b)$, both factors equal $\frac{b-a}{b+a} = \frac{\kappa-1}{\kappa+1}$, where $\kappa = b/a$. This **contraction factor** $\frac{\kappa-1}{\kappa+1}$ governs the convergence speed of gradient descent.

### 6.5.4 The Descent Lemma

The descent lemma is the **engine behind all gradient descent convergence proofs**. It makes precise the surrogate-minimization intuition from [Section 6.3.3](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#sec-gd-surrogate): every GD step makes guaranteed progress, provided the step size is small enough.

**Theorem 6.5 (Descent Lemma)** If $f$ is $L$ -smooth and $x^+ = x - \alpha\,\nabla f(x)$ with $\alpha \leq 1/L$, then

$$
f(x^+) \leq f(x) - \frac{\alpha}{2}\|\nabla f(x)\|_2^2. \tag{6.11}
$$

Note two things about this result:

- It is **quantitative**: each step decreases $f$ by at least $\frac{\alpha}{2}\|\nabla f(x)\|_2^2$, which is large when the gradient is large (far from optimality) and small when the gradient is small (close to optimality).
- It requires **no convexity** — it works for any $L$ -smooth function, even nonconvex ones. Convexity will enter only when we translate “gradient gets small” into “function value gets close to optimal.”

*Proof*. The proof is a direct calculation using the quadratic upper bound ([Equation 6.9](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-quadratic-upper)). Start from:

$$
f(x^+) \leq f(x) + \nabla f(x)^\top(x^+ - x) + \frac{L}{2}\|x^+ - x\|_2^2.
$$

Substitute the GD update $x^+ - x = -\alpha\,\nabla f(x)$:

$$
f(x^+) \leq f(x) - \alpha\|\nabla f(x)\|_2^2 + \frac{L\alpha^2}{2}\|\nabla f(x)\|_2^2 = f(x) - \alpha\!\left(1 - \frac{L\alpha}{2}\right)\|\nabla f(x)\|_2^2.
$$

The coefficient $(1 - L\alpha/2)$ measures the tradeoff: the first term $-\alpha\|\nabla f\|^2$ comes from the linear decrease along the gradient, and the second term $+\frac{L\alpha^2}{2}\|\nabla f\|^2$ is the penalty for curvature. When $\alpha \leq 1/L$, the curvature penalty is at most half the linear gain, giving $(1 - L\alpha/2) \geq 1/2$:

$$
f(x^+) \leq f(x) - \frac{\alpha}{2}\|\nabla f(x)\|_2^2. \qquad \blacksquare
$$

### 6.5.5 Three Convergence Cases

With the descent lemma in hand, we can analyze gradient descent under three settings of increasing structure. Each added assumption yields a strictly faster convergence rate.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch05-three-cases.svg)

Figure 6.6: Convergence rates of gradient descent under three structural assumptions: nonconvex + smooth (finding approximate stationary points), convex + smooth (sublinear O ( 1 / K ) O(1/K) convergence to the global minimum), and strongly convex + smooth (linear convergence governed by the condition number κ \\kappa ).

#### 6.5.5.1 Case 1: Nonconvex + Smooth

When $f$ is only smooth (possibly nonconvex), we cannot hope to find a global minimum—the function may have many local minima and saddle points. The best we can guarantee is finding an **approximate stationary point** where $\|\nabla f(x)\| \leq \varepsilon$.

**Theorem 6.6 (GD: Nonconvex + Smooth)** If $f$ is $L$ -smooth and $\alpha = 1/L$, then after $K$ iterations:

$$
\min_{0 \leq k < K} \|\nabla f(x^k)\|_2^2 \leq \frac{2L\bigl(f(x^0) - f(x^*)\bigr)}{K}.
$$

To find an $\varepsilon$ -approximate stationary point ($\|\nabla f(x)\|_2 \leq \varepsilon$), we need $K = O(L/\varepsilon^2)$ iterations.

*Proof*. By the descent lemma ([Equation 6.11](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-descent-lemma)), each step satisfies $f(x^{k+1}) \leq f(x^k) - \frac{1}{2L}\|\nabla f(x^k)\|_2^2$. Rearranging:

$$
\frac{1}{2L}\|\nabla f(x^k)\|_2^2 \leq f(x^k) - f(x^{k+1}).
$$

Now sum from $k = 0$ to $K-1$. The right-hand side **telescopes**:

$$
\frac{1}{2L}\sum_{k=0}^{K-1}\|\nabla f(x^k)\|_2^2 \leq \bigl(f(x^0) - f(x^1)\bigr) + \bigl(f(x^1) - f(x^2)\bigr) + \cdots + \bigl(f(x^{K-1}) - f(x^K)\bigr) = f(x^0) - f(x^K) \leq f(x^0) - f(x^*).
$$

Since the minimum is at most the average: $\min_{k} \|\nabla f(x^k)\|_2^2 \leq \frac{1}{K}\sum_k \|\nabla f(x^k)\|_2^2$. Dividing by $K$ gives the result. $\blacksquare$

TipIntuition

The descent lemma says each step “uses up” at least $\frac{1}{2L}\|\nabla f(x^k)\|_2^2$ of the initial gap $f(x^0) - f(x^*)$. Since this gap is finite, the gradients must eventually become small. After $K$ steps, at least one iterate has gradient norm at most $O(1/\sqrt{K})$.

#### 6.5.5.2 Case 2: Convex + Smooth

When $f$ is convex, every stationary point is a global minimum, so we can track the **function value gap** $f(x^k) - f(x^*)$ directly. Convexity upgrades the guarantee from “finding a stationary point” to “finding an approximate global minimizer.” But convexity also gives us a new proof tool: the first-order characterization $f(y) \geq f(x) + \langle \nabla f(x), y - x \rangle$, which provides a **lower bound** to complement the smoothness upper bound.

**Theorem 6.7 (GD: Convex + Smooth)** If $f$ is convex and $L$ -smooth, with $\alpha = 1/L$, then:

$$
f(x^K) - f(x^*) \leq \frac{L\|x^0 - x^*\|_2^2}{2K}.
$$

To achieve $f(x^K) - f(x^*) \leq \varepsilon$, we need $K = O(L/\varepsilon)$ iterations.

The proof strategy is: combine the smoothness **upper bound** with the convexity **lower bound** to show that each GD step makes progress measured by the **distance to the optimum** $\|x^k - x^*\|_2^2$. A useful algebraic identity (the “three-point identity”) then converts inner products into squared distances, enabling a clean telescoping argument.

NoteThree-Point Identity

For any three points $a, b, c \in \mathbb{R}^n$:

$$
\langle a - b,\, a - c \rangle = \frac{1}{2}\|a - b\|_2^2 + \frac{1}{2}\|a - c\|_2^2 - \frac{1}{2}\|b - c\|_2^2.
$$

This follows by expanding $\|b - c\|^2 = \|(a-c) - (a-b)\|^2$ and rearranging. It converts an inner product (hard to telescope) into a difference of squared distances (easy to telescope). This identity appears repeatedly in optimization proofs — in projected gradient descent, proximal methods, and mirror descent.

*Proof*. **Step 1 (Smoothness — upper bound).** The quadratic upper bound ([Equation 6.9](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-quadratic-upper)) at the GD update gives:

$$
f(x^{k+1}) \leq f(x^k) + \nabla f(x^k)^\top(x^{k+1} - x^k) + \frac{L}{2}\|x^{k+1} - x^k\|_2^2.
$$

**Step 2 (Convexity — lower bound).** The first-order characterization of convexity, applied at $x^k$ with target $x^*$, gives:

$$
f(x^*) \geq f(x^k) + \nabla f(x^k)^\top(x^* - x^k).
$$

**Step 3 (Subtract to eliminate $f(x^k)$).** Subtracting the lower bound from the upper bound cancels $f(x^k)$:

$$
f(x^{k+1}) - f(x^*) \leq \nabla f(x^k)^\top\bigl[(x^{k+1} - x^k) - (x^* - x^k)\bigr] + \frac{L}{2}\|x^{k+1} - x^k\|_2^2 = \nabla f(x^k)^\top(x^{k+1} - x^*) + \frac{L}{2}\|x^{k+1} - x^k\|_2^2.
$$

**Step 4 (Use GD update to replace gradient).** Since $x^{k+1} = x^k - \alpha\nabla f(x^k)$, we have $\nabla f(x^k) = \frac{1}{\alpha}(x^k - x^{k+1})$. Substituting:

$$
f(x^{k+1}) - f(x^*) \leq \frac{1}{\alpha}\langle x^k - x^{k+1},\, x^{k+1} - x^* \rangle + \frac{L}{2}\|x^{k+1} - x^k\|_2^2.
$$

**Step 5 (Apply three-point identity).** Expanding $\|x^k - x^*\|^2 = \|(x^k - x^{k+1}) + (x^{k+1} - x^*)\|^2$ gives the identity:

$$
\langle x^k - x^{k+1},\, x^{k+1} - x^*\rangle = \tfrac{1}{2}\bigl[\|x^k - x^*\|^2 - \|x^{k+1} - x^*\|^2 - \|x^k - x^{k+1}\|^2\bigr].
$$

Substituting:

$$
f(x^{k+1}) - f(x^*) \leq \frac{1}{2\alpha}\bigl[\|x^k - x^*\|_2^2 - \|x^{k+1} - x^*\|_2^2\bigr] - \frac{1}{2\alpha}\|x^k - x^{k+1}\|_2^2 + \frac{L}{2}\|x^{k+1} - x^k\|_2^2.
$$

With $\alpha = 1/L$, the last two terms cancel exactly, leaving:

$$
f(x^{k+1}) - f(x^*) \leq \frac{L}{2}\bigl[\|x^k - x^*\|_2^2 - \|x^{k+1} - x^*\|_2^2\bigr]. \tag{6.12}
$$

**Step 6 (Telescope).** Summing [Equation 6.12](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-convex-telescope) over $k = 0, \ldots, K-1$, the right side telescopes:

$$
\sum_{k=0}^{K-1}\bigl(f(x^{k+1}) - f(x^*)\bigr) \leq \frac{L}{2}\bigl[\|x^0 - x^*\|_2^2 - \|x^K - x^*\|_2^2\bigr] \leq \frac{L}{2}\|x^0 - x^*\|_2^2.
$$

Since $f(x^k)$ is monotonically decreasing (by the descent lemma), $f(x^K) \leq f(x^{k+1})$ for all $k < K$:

$$
K \cdot \bigl(f(x^K) - f(x^*)\bigr) \leq \sum_{k=0}^{K-1}\bigl(f(x^{k+1}) - f(x^*)\bigr) \leq \frac{L}{2}\|x^0 - x^*\|_2^2.
$$

Dividing by $K$ gives the result. $\blacksquare$

TipIntuition

The proof reveals a clean picture: each GD step reduces the squared distance $\|x^k - x^*\|_2^2$ to the optimum, and the total “budget” of distance reduction is $\|x^0 - x^*\|_2^2$. Spreading this budget over $K$ steps gives each step an average reduction of $\|x^0 - x^*\|_2^2 / K$, which translates to a $1/K$ rate for the function value gap.

Note the crucial role of **convexity**: it provided the lower bound in Step 2 that let us relate the function value gap $f(x^{k+1}) - f(x^*)$ to geometric quantities (distances to $x^*$). Without convexity, we could only bound the gradient norm (Case 1).

#### 6.5.5.3 Case 3: Strongly Convex + Smooth

The strongest setting gives the best result: **linear convergence** (also called geometric or exponential convergence), where the error contracts by a fixed factor at each step. The key insight is that the proof reduces to the same eigenvalue analysis as the 2D quadratic warm-up ([Example 6.2](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#exm-2d-quadratic-zigzag)), but now applied to the Hessian of a general function via the mean value theorem.

**Theorem 6.8 (GD: Strongly Convex + Smooth)** If $f$ is $\mu$ -strongly convex and $L$ -smooth, with step size $\alpha = \frac{2}{\mu + L}$ and condition number $\kappa = L/\mu$, then:

$$
\|x^k - x^*\|_2 \leq \left(\frac{\kappa - 1}{\kappa + 1}\right)^k \|x^0 - x^*\|_2, \tag{6.13}
$$

$$
f(x^k) - f(x^*) \leq \frac{L}{2}\left(\frac{\kappa - 1}{\kappa + 1}\right)^{2k} \|x^0 - x^*\|_2^2. \tag{6.14}
$$

To achieve $f(x^k) - f(x^*) \leq \varepsilon$, we need $K = O(\kappa \log(1/\varepsilon))$ iterations.

*Proof*. **Step 1 (Linearize the gradient via the mean value theorem).** The key idea is to express the gradient $\nabla f(x^k)$ in terms of the error $e^k = x^k - x^*$. By the mean value theorem (for vector-valued functions), there exists a point $\xi$ on the segment between $x^k$ and $x^*$ such that:

$$
\nabla f(x^k) = \nabla f(x^k) - \underbrace{\nabla f(x^*)}_{= 0} = \nabla^2 f(\xi)\,(x^k - x^*) = \nabla^2 f(\xi)\, e^k.
$$

This is the crucial step: it turns the nonlinear gradient into a **linear operator** applied to the error.

**Step 2 (Write the error recursion).** Substituting into the GD update:

$$
e^{k+1} = x^{k+1} - x^* = e^k - \alpha\,\nabla f(x^k) = \bigl(I - \alpha\,\nabla^2 f(\xi)\bigr)\, e^k.
$$

This is the same form as the 2D quadratic example! The matrix $M = I - \alpha\,\nabla^2 f(\xi)$ is the **contraction matrix**.

**Step 3 (Bound the spectral radius).** By strong convexity and smoothness, the eigenvalues of $\nabla^2 f(\xi)$ lie in $[\mu, L]$, so the eigenvalues of $M$ lie in $[1 - \alpha L,\, 1 - \alpha\mu]$. The spectral norm $\|M\|_{\mathrm{op}} = \max\{|1 - \alpha\mu|,\, |1 - \alpha L|\}$. Just as in the 2D warm-up, the optimal step size balances these two extremes:

$$
\alpha^* = \frac{2}{\mu + L} \quad\implies\quad \|M\|_{\mathrm{op}} = \frac{L - \mu}{L + \mu} = \frac{\kappa - 1}{\kappa + 1}.
$$

**Step 4 (Unroll).** Therefore $\|e^{k+1}\|_2 \leq \frac{\kappa - 1}{\kappa + 1}\|e^k\|_2$, and unrolling gives [Equation 6.13](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-sc-rate-iterates). The function value bound [Equation 6.14](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-sc-rate-function) follows from the smoothness inequality $f(x) - f(x^*) \leq \frac{L}{2}\|x - x^*\|_2^2$. $\blacksquare$

TipIntuition: Why Logarithmic Iterations

Linear convergence means the error decreases **geometrically**: after $k$ steps, the error is multiplied by $\rho^k$ where $\rho = \frac{\kappa-1}{\kappa+1} < 1$. To reduce the error from $\Delta_0$ to $\varepsilon$, we need $\rho^k \cdot \Delta_0 \leq \varepsilon$, i.e., $k \geq \frac{\log(\Delta_0/\varepsilon)}{\log(1/\rho)}$. Since $\log(1/\rho) \approx 2/\kappa$ for large $\kappa$, this gives $k = O(\kappa \log(1/\varepsilon))$.

**Concrete comparison:** Convex + smooth needs $O(1/\varepsilon)$ iterations (e.g., 1,000,000 for $\varepsilon = 10^{-6}$), while strongly convex + smooth needs only $O(\kappa \cdot \log(1/\varepsilon)) \approx 14\kappa$ iterations for the same accuracy.

#### 6.5.5.4 Convergence Summary

| Nonconvex + Smooth | $1/L$ | $\min_k\\|\nabla f(x^k)\\|_2^2$ | $O(1/K)$ | $O(1/\varepsilon^2)$ for $\\|\nabla f\\| \leq \varepsilon$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Convex + Smooth | $1/L$ | $f(x^K) - f(x^*)$ | $O(1/K)$ | $O(1/\varepsilon)$ |
| Strongly Convex + Smooth | $2/(\mu+L)$ | $\\|x^k - x^*\\|_2$ | $\left(\frac{\kappa-1}{\kappa+1}\right)^k$ | $O(\kappa\log(1/\varepsilon))$ |

Each row adds a structural assumption and gains a faster rate. The jump from $O(1/K)$ to linear convergence is the most dramatic: it is the difference between polynomial and logarithmic dependence on the target accuracy $\varepsilon$. See [Figure 6.4](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#fig-convergence-rates) for a visual comparison across different method classes.

### 6.5.6 The Polyak–Łojasiewicz Condition

A remarkable fact is that we do not need strong convexity—or even convexity at all—to achieve linear convergence. The **Polyak–Łojasiewicz (PL) condition** is a weaker assumption that still guarantees the same rate.

**Definition 6.6 (Polyak–Łojasiewicz Condition)** A function $f$ satisfies the **PL condition** with parameter $\mu > 0$ if

$$
\|\nabla f(x)\|_2^2 \geq 2\mu \cdot \bigl(f(x) - f(x^*)\bigr) \qquad \forall\, x.
$$

The PL condition says: *whenever the gradient is small, the function value must be close to optimal*. This is automatically satisfied by $\mu$ -strongly convex functions (it is their gradient domination property [Equation 6.10](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html#eq-gradient-domination)), but it can also hold for some **nonconvex** functions.

**Example 6.5 (Example: A Nonconvex PL Function)** Consider $f(x) = x^2 + 3\sin^2(x)$. This function is **nonconvex** (it has inflection points where $f''(x) < 0$), yet it satisfies the PL condition. Intuitively, the $x^2$ term ensures the function always grows away from the origin, so the gradient cannot be small far from the minimizer $x^* = 0$, even though the $\sin^2$ term creates wiggles. Every stationary point of $f$ is the global minimizer — there are no spurious local minima.

**PL + smoothness gives linear convergence.** The proof is remarkably simple — just combine the descent lemma with the PL condition. Using step size $\alpha = 1/L$:

$$
f(x^{k+1}) - f(x^*) \leq f(x^k) - f(x^*) - \frac{1}{2L}\|\nabla f(x^k)\|_2^2 \stackrel{\text{PL}}{\leq} \left(1 - \frac{\mu}{L}\right)\bigl(f(x^k) - f(x^*)\bigr).
$$

Unrolling: $f(x^k) - f(x^*) \leq (1 - \mu/L)^k \cdot (f(x^0) - f(x^*))$ — linear convergence, without assuming convexity. The PL condition arises naturally in many practical settings, including over-parameterized least squares and certain neural network training problems, which helps explain why GD works well even on nonconvex objectives.

## 6.6 Stopping Criteria

The convergence theorems above guarantee that gradient descent *eventually* finds a good solution, but they do not tell the algorithm when to stop. In practice, we need a computable criterion to decide that the current iterate is “close enough” to optimal. The choice of stopping criterion should reflect the convergence guarantee: for nonconvex problems, monitor the gradient norm; for convex problems, the function value gap or iterate distance may be more appropriate.

Set $\varepsilon$ to be a small number. Common stopping criteria:

1. **Gradient norm:** $\|\nabla f(x)\| \leq \varepsilon$.
	- We find an $\varepsilon$ -approximate stationary point. If $f$ is convex, stationary point    $\iff$ optimal solution.
2. **Objective change:** $|f(x_{k+1}) - f(x_k)| \leq \varepsilon$ (or $|f(x_{k+\ell}) - f(x_k)| \leq \varepsilon$ for some fixed $\ell$).
	- The objective does not change much.
3. **Iterate change:** $\|x_{k+1} - x_k\| \leq \varepsilon$.
	- The iterates do not change much.
4. **Relative objective change:** $\displaystyle\frac{|f(x_{k+1}) - f(x_k)|}{\max\{1,\, |f(x_k)|\}} < \varepsilon$.
	- Removes the effect of the magnitude of $f$.
5. **Relative iterate change:** $\displaystyle\frac{\|x_{k+1} - x_k\|}{\max\{1,\, \|x_k\|\}} < \varepsilon$.

## Summary

- **Iterative descent framework.** All first-order methods share the update $x^{k+1} = x^k + \alpha^k d^k$; convergence requires $d^k$ to be a descent direction ($\langle d^k, \nabla f(x^k) \rangle < 0$) and an appropriate step size $\alpha^k$.
- **Steepest descent and its variants.** Choosing different norms in the steepest descent problem yields gradient descent ($\ell_2$), coordinate descent ($\ell_1$), sign gradient descent ($\ell_\infty$), and spectral steepest descent (operator norm on matrices, giving the Muon optimizer); choosing $B^k = [\nabla^2 f(x^k)]^{-1}$ gives Newton’s direction.
- **Step size strategies.** Constant step sizes are simple but require tuning; diminishing step sizes ($\alpha^k \to 0$, $\sum \alpha^k = \infty$) guarantee convergence; backtracking line search adaptively finds a step size ensuring sufficient decrease.
- **GD as surrogate minimization.** Each GD step minimizes a quadratic upper bound $g_\alpha(x) = f(x^k) + \langle \nabla f(x^k), x-x^k\rangle + \frac{1}{2\alpha}\|x-x^k\|^2$. Newton’s method replaces the isotropic penalty with the true Hessian.
- **Smoothness and strong convexity.** $L$ -smoothness ($\|\nabla f(x) - \nabla f(y)\| \leq L\|x-y\|$) bounds curvature from above; $\mu$ -strong convexity bounds it from below and gives gradient domination: $f(x) - f^* \leq \frac{1}{2\mu}\|\nabla f(x)\|^2$. Their ratio $\kappa = L/\mu$ is the condition number.
- **Descent lemma.** If $f$ is $L$ -smooth and $\alpha \leq 1/L$, then $f(x^+) \leq f(x) - \frac{\alpha}{2}\|\nabla f(x)\|^2$: every GD step makes guaranteed progress.
- **Three convergence cases.** Nonconvex + smooth: $\min_k \|\nabla f(x^k)\|^2 = O(1/K)$. Convex + smooth: $f(x^K) - f^* = O(1/K)$. Strongly convex + smooth: linear convergence $O((\frac{\kappa-1}{\kappa+1})^k)$, needing $O(\kappa\log(1/\varepsilon))$ iterations.
- **PL condition.** The Polyak–Łojasiewicz condition $\|\nabla f(x)\|^2 \geq 2\mu(f(x) - f^*)$ yields linear convergence without convexity.

TipLooking Ahead

The convergence rates in this chapter— $O(1/K)$ for convex functions and $O(\rho^k)$ for strongly convex functions—are fundamental baselines, but they can be improved. In the next chapter, we study advanced first-order methods: momentum techniques (Heavy-Ball, Nesterov acceleration) that achieve the optimal $O(1/K^2)$ rate for smooth convex functions, and adaptive learning rate methods (AdaGrad, RMSProp, Adam) that automatically tune per-coordinate step sizes.