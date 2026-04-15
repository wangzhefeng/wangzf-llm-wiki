---
author: null
created: 2026-04-11
description: null
tags:
- clippings
title: 7  Momentum and Adaptive Methods – S&DS 431/631 — Optimization and Computation
source_type: web
created_at: 2026-04-11
status: summarized
source_url: https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html
published_at: null
related_concepts:
  - 运筹优化
  - 深度学习优化算法
  - 数学优化
topics:
  - programming-tools
  - 编程工具
---
Gradient descent is simple and elegant, but it has a well-known weakness: on ill-conditioned problems, it converges painfully slowly. The iterates zigzag across narrow valleys, wasting most of their effort oscillating in high-curvature directions while barely making progress along the bottom of the valley. For a function with condition number $\kappa$, gradient descent requires $O(\kappa \log(1/\varepsilon))$ iterations — and in machine learning applications, $\kappa$ can easily be in the thousands or millions.

This chapter introduces techniques that dramatically accelerate first-order optimization. Momentum methods smooth out the oscillatory behavior of gradient descent by incorporating information from past gradients, reducing the iteration complexity from $O(\kappa \log(1/\varepsilon))$ to $O(\sqrt{\kappa} \log(1/\varepsilon))$ — a quadratic improvement in the dependence on the condition number. Adaptive learning rate methods (AdaGrad, RMSProp, Adam) go further by automatically adjusting the step size in each coordinate direction, effectively rescaling the problem to reduce its condition number.

These methods form the backbone of modern deep learning optimization. Nearly every large-scale neural network trained today uses some variant of Adam or SGD with momentum. Understanding why these methods work — and when they can fail — is essential for both practitioners and theorists.

TipCompanion Notebooks

Hands-on Python notebooks accompany this chapter. Click a badge to open in Google Colab.

- **Optimizer Comparison** — comparing GD, AdaGrad, RMSProp, Adam, and Heavy Ball on Beale and Rosenbrock functions
- **Tour of PyTorch Optimizers** — experimenting with PyTorch’s built-in optimizers at different learning rates
- **Learning Rate Schedules** — step, cosine, and warm-up scheduling in PyTorch

## What Will Be Covered

This chapter develops the following topics, progressing from simple acceleration techniques to adaptive optimization:

- Gradient descent recap and the role of the condition number
- Polyak’s heavy-ball momentum method and its convergence on quadratics
- Nesterov’s accelerated gradient method and its convergence on general convex functions
- Adaptive learning rate methods: AdaGrad, RMSProp, Adam — derivations, properties, and bias correction
- Weight decay vs. L2 regularization: AdamW and decoupled weight decay
- Practical PyTorch usage: training loops, learning rate schedules, and per-parameter-group configuration
- Modern matrix optimizers: Muon, Shampoo, and SOAP — exploiting the matrix structure of neural network weights

## 7.1 Gradient Descent Recap

Recall the gradient descent update with constant stepsize: (See [Part 5.1](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html) for the full derivation of gradient descent and its convergence analysis.) 
$$
x^{k+1} = x^k - \alpha \cdot \nabla f(x^k).
$$

As we will show in later lectures, if $f$ is twice-differentiable and $\nabla^2 f$ is bounded (as defined in [Part 3](https://zhuoranyang.github.io/sds431-notes/lectures/04-convex-functions.html)): 
$$
m \cdot \mathbf{I}_n \preceq \nabla^2 f(x) \preceq M \cdot \mathbf{I}_n,
$$

let $\kappa = \frac{M}{m} \geq 1$ be defined as the **condition number** of $f$. Then setting $\alpha = \frac{1}{M}$, we have:

$$
\begin{aligned}
f(x^{k+1}) - f(x^*) &\leq \exp(-k/\kappa) \cdot \bigl[f(x^1) - f(x^*)\bigr], \\
\|x^{k+1} - x^*\|_2 &\leq \exp(-k/\kappa) \cdot \|x^k - x^*\|_2.
\end{aligned}
$$

Thus, to achieve an $\varepsilon$ -approximate minimizer, the number of GD updates (queries to the gradient oracle) is:

$$
\text{Iteration complexity} = O\!\bigl(\kappa \cdot \log(1/\varepsilon)\bigr). \tag{7.1}
$$

### 7.1.1 Quadratic Example

**Example 7.1 (Gradient Descent on a Quadratic)** Consider $f(x) = \frac{1}{2} x^\top A x - b^\top x$, where $A$ is PSD with $m \mathbf{I} \preceq A \preceq M \mathbf{I}$. Then $x^* = A^{-1}b$ and $\kappa = M/m$.

The GD update becomes: 
$$
x^{k+1} = x^k - \alpha \cdot (Ax^k - b) = x^k - \alpha \cdot (Ax^k - Ax^*) = (\mathbf{I} - \alpha A)\, x^k + \alpha A\, x^*.
$$

Taking the difference with $x^*$: 
$$
\begin{aligned}
\|x^{k+1} - x^*\|_2 &= \|(\mathbf{I} - \alpha A)(x^k - x^*)\|_2 = \|(\mathbf{I} - \alpha A)^k (x^1 - x^*)\|_2 \\
&\leq \|(\mathbf{I} - \alpha A)^k\|_2 \cdot \|x^1 - x^*\|_2 \\
&\leq \bigl(\rho(\mathbf{I} - \alpha A) + o(1)\bigr)^k \cdot \|x^1 - x^*\|_2.
\end{aligned}
$$

*Proof*. *Deriving the Rate.* The eigenvalues of $(\mathbf{I} - \alpha A)$ with $\alpha = 1/M$ are bounded in: 
$$
\bigl[1 - \alpha M, \; 1 - \alpha m\bigr] = \bigl[0, \; 1 - 1/\kappa\bigr].
$$

Thus $\rho(\mathbf{I} - \alpha A) \leq 1 - 1/\kappa$. Substituting into the spectral radius bound above, and using the standard inequality $1 - t \leq \exp(-t)$ for $t \geq 0$, we obtain: 
$$
\|x^{k+1} - x^*\|_2 \leq \Bigl(1 - \frac{1}{\kappa}\Bigr)^k \|x^1 - x^*\| \leq \exp(-k/\kappa) \cdot \|x^1 - x^*\|_2.
$$

To achieve $\varepsilon$ -error $\|x^k - x^*\|_2 \leq \varepsilon$, we need: 
$$
k = O\!\Bigl(\kappa \cdot \log\!\bigl(\tfrac{\|x^1 - x^*\|_2}{\varepsilon}\bigr)\Bigr) = O\!\bigl(\kappa \cdot \log(1/\varepsilon)\bigr),
$$
 when $\|x^1 - x^*\|_2$ is of constant order. Hence we conclude that the iteration complexity of gradient descent on this quadratic is $O(\kappa \cdot \log(1/\varepsilon))$. $\blacksquare$

### 7.1.2 Remarks on GD

TipRemarks

1. **Condition number dependence:** For the quadratic case, iteration complexity is linear in $\kappa$. If $A$ is ill-conditioned, then GD needs more iterations.
2. **Descent property:** We can show the objective value decays at each step. Why? Because $\nabla f(x^k)$ is a descent direction.
3. **Optimal stepsize choice:** $\alpha^* = \frac{2}{m + M}$, which gives a slightly better rate: 
	$$
	\|x^{k+1} - x^*\|_2 \leq \Bigl(1 - \frac{2}{\kappa+1}\Bigr) \cdot \|x^k - x^*\|_2.
	$$
	 Note that $\frac{2}{m+M} \geq \frac{2}{2M} = \frac{1}{M}$, the stepsize we used in the previous bound.

## 7.2 Momentum Methods

The $O(\kappa \cdot \log(1/\varepsilon))$ complexity of gradient descent ([Equation 7.1](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-gd-complexity)) becomes prohibitively large when the condition number $\kappa$ is high. The key idea of momentum methods is to break this bottleneck by incorporating information from previous iterates. The previous methods are of the form $x^{k+1} = x^k + \alpha^k \cdot d^k$, where the descent direction $d^k$ is computed based on the *current gradient* $\nabla f(x^k)$.

Momentum methods propose to also incorporate **“past gradients”** $\{\nabla f(x^\ell),\, \ell < k\}$ when updating $x^k$.

TipWhy Momentum?

The trajectory of GD bounces back and forth in the **high curvature directions**, and makes slow progress in **low curvature directions**.

By adding past gradients, we smooth out the trajectory. Momentum methods are first-order (gradient-based) methods.

GD oscillates on an ill-conditioned quadratic. Momentum methods smooth out the trajectory, accelerating convergence.

### 7.2.1 Polyak’s Heavy-Ball Method

ImportantAlgorithm: Polyak’s Momentum (Heavy-Ball Method)

**Update rule:** 
$$
x^{k+1} = x^k - \alpha \cdot \nabla f(x^k) + \beta \cdot (x^k - x^{k-1}). \tag{7.2}
$$

Parameters:

- $\alpha$: stepsize
- $\beta \in [0, 1)$: momentum parameter

The term $\beta(x^k - x^{k-1})$ is the **momentum** term.

**Another way to view the momentum update.** Define $z^k = \frac{1}{\alpha}(x^{k-1} - x^k)$. Then: 
$$
\begin{cases} z^{k+1} = \beta \cdot z^k + \nabla f(x^k) \\ x^{k+1} = x^k - \alpha \cdot z^{k+1} \end{cases}
$$

Expanding the recursion: 
$$
z^{k+1} = \nabla f(x^k) + \beta \cdot \nabla f(x^{k-1}) + \beta^2 \cdot \nabla f(x^{k-2}) + \cdots + \beta^{k-1} \nabla f(x^1).
$$

This contains all **past gradient evaluations**, with exponential damping.

- $\beta = 0$ reduces to standard GD.
- $\beta < 1$ ensures the past gradients are damped (if $\beta = 1$, $\nabla f(x^1)$ would be added in each step without decay).

TipRemark: Alternative Form

The momentum method is sometimes written as: 
$$
\begin{cases} m^{k+1} = \beta \cdot m^k + (1 - \beta)\,\nabla f(x^k) \\ x^{k+1} = x^k - \alpha \cdot m^{k+1} \end{cases}
$$

This is equivalent to the previous form with $\widetilde{\alpha} = \alpha(1-\beta)$.

### 7.2.2 Intuition of Momentum

In practice, $\beta$ is set to a constant that is **close to 1** (e.g., 0.9 or 0.999).

**Intuition of momentum:**

- In **high curvature directions**, the gradients cancel each other out, so momentum damps oscillations.
- In **low curvature directions**, the gradients point in the same direction, so momentum effectively increases the stepsize.

TipRemarks on Heavy-Ball

- The stepsize $\alpha$ usually needs to be tuned (e.g., grid search). Practically, $\alpha$ is often between 0.001 and 0.1.
- $\alpha$ too small — slow progress; $\alpha$ too large — oscillations; $\alpha$ much too large — instability.
- As the update direction is perturbed by momentum, generally the objectives $\{f(x^k)\}$ generated by the heavy-ball method are **not monotonically decreasing**.
- We can only prove its convergence in the quadratic case. In this case, momentum is better than GD.
- In practice, overall momentum is better than GD and almost never hurts.

### 7.2.3 Improved Convergence of Heavy-Ball Method

We now formalize the convergence advantage of momentum. The key insight is to lift the iteration into a higher-dimensional space by tracking both the current and previous iterates, which turns the heavy-ball recursion into a linear dynamical system governed by a companion matrix $T$. The convergence rate is then determined by the spectral radius of $T$, and by choosing $\alpha$ and $\beta$ optimally we can minimize this spectral radius.

**Theorem 7.1 (Heavy-Ball Convergence on Quadratics)** Consider the quadratic $f(x) = \frac{1}{2} x^\top A x - b^\top x$ with $m \mathbf{I}_n \preceq A \preceq M \cdot \mathbf{I}_n$. Then $\nabla f(x) = Ax - b = A(x - x^*)$ with $x^* = A^{-1}b$.

The heavy-ball updates satisfy: 
$$
x^{k+1} - x^* = \bigl[(1+\beta)\mathbf{I} - \alpha A\bigr](x^k - x^*) - \beta(x^{k-1} - x^*).
$$

Define $w^k = x^k - x^*$. In matrix form: 
$$
\begin{pmatrix} w^{k+1} \\ w^k \end{pmatrix} = \underbrace{\begin{pmatrix} (1+\beta)\mathbf{I} - \alpha A & -\beta \mathbf{I} \\ \mathbf{I} & \mathbf{0} \end{pmatrix}}_{T} \begin{pmatrix} w^k \\ w^{k-1} \end{pmatrix}.
$$

Using recursion: $\displaystyle\left\|\binom{w^{k+2}}{w^{k+1}}\right\|_2 \leq \|T^k\|_2 \cdot \left\|\binom{w^2}{w^1}\right\|_2 \leq \bigl(\rho(T) + o(1)\bigr)^k \cdot \left\|\binom{w^2}{w^1}\right\|_2,$

where $\rho(T) = \max\{|\lambda_i(T)|\}$ is the **spectral radius** of $T$.

This result shows that the convergence rate of the heavy-ball method **on quadratics** is governed by the spectral radius of a $2n \times 2n$ companion matrix $T$. The goal is now to choose $\alpha$ and $\beta$ to **minimize** $\rho(T)$.

**Corollary 7.1 (Optimal Parameters for Heavy-Ball (Quadratics))** For the quadratic $f(x) = \frac{1}{2}x^\top A x - b^\top x$ with $m\mathbf{I} \preceq A \preceq M\mathbf{I}$, the optimal heavy-ball parameters are: 
$$
\alpha^* = \Bigl(\frac{2}{\sqrt{m} + \sqrt{M}}\Bigr)^2, \qquad \beta^* = \Bigl(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\Bigr)^2.
$$

The resulting spectral radius and convergence rate are: 
$$
\rho(T) = \frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}, \qquad \|x^{k+1} - x^*\|_2 \leq \Bigl(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\Bigr)^k \|x^1 - x^*\|_2.
$$

Iteration complexity: 
$$
\text{Iteration complexity (Heavy-Ball, quadratics)} = O\!\bigl(\sqrt{\kappa} \cdot \log(1/\varepsilon)\bigr). \tag{7.3}
$$

*Proof*. *Derivation of the optimal parameters.* Since $A$ is symmetric, it suffices to analyze each eigenvalue $\lambda \in [m, M]$ of $A$ independently. For each $\lambda$, the companion matrix $T$ reduces to a $2 \times 2$ block: 
$$
T_\lambda = \begin{pmatrix} 1 + \beta - \alpha\lambda & -\beta \\ 1 & 0 \end{pmatrix}.
$$

**Step 1: Characteristic polynomial.** The eigenvalues $\mu$ of $T_\lambda$ satisfy: 
$$
\mu^2 - (1+\beta - \alpha\lambda)\,\mu + \beta = 0.
$$
 Note that $\mu_1 \cdot \mu_2 = \beta$ (the product of eigenvalues equals the determinant).

**Step 2: Complex eigenvalues give modulus $\sqrt{\beta}$.** When the discriminant $(1+\beta-\alpha\lambda)^2 - 4\beta < 0$, the eigenvalues are complex conjugates with $|\mu_1| = |\mu_2| = \sqrt{\beta}$. When the eigenvalues are real, $|\mu_{\max}| \geq \sqrt{\beta}$. Therefore, $\rho(T_\lambda) \geq \sqrt{\beta}$ always, with equality when the eigenvalues are complex.

**Step 3: Ensure complex eigenvalues for all $\lambda \in [m, M]$.** We need $|1 + \beta - \alpha\lambda| \leq 2\sqrt{\beta}$ for all $\lambda \in [m, M]$. The tightest constraints are at the endpoints. Setting both to equality: 
$$
\begin{aligned}
1 + \beta - \alpha m &= 2\sqrt{\beta}, \\
\alpha M - 1 - \beta &= 2\sqrt{\beta}.
\end{aligned}
$$

**Step 4: Solve for $\alpha$ and $\beta$.** Adding the two equations gives $\alpha = \frac{4\sqrt{\beta}}{M - m}$. Let $u = \sqrt{\beta}$. Substituting into the first equation and simplifying: 
$$
\frac{1+u}{1-u} = \sqrt{\kappa} \qquad \Longrightarrow \qquad u = \frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}.
$$

Therefore $\beta = u^2 = \bigl(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\bigr)^2$ and $\rho(T) = \sqrt{\beta} = \frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}$. Substituting back: 
$$
\alpha = \frac{(1+u)^2}{M} = \frac{4\kappa}{M(\sqrt{\kappa}+1)^2} = \Bigl(\frac{2}{\sqrt{m}+\sqrt{M}}\Bigr)^2.
$$

**Step 5: Iteration complexity.** Using $1 - t \leq e^{-t}$: 
$$
\rho(T) = 1 - \frac{2}{\sqrt{\kappa}+1} \leq \exp\!\Bigl(-\frac{2}{\sqrt{\kappa}+1}\Bigr).
$$
 To reach $\varepsilon$ -accuracy, we need $\rho(T)^k \leq \varepsilon$, i.e., $k = O(\sqrt{\kappa}\log(1/\varepsilon))$. $\blacksquare$

WarningLimitation

The heavy-ball convergence result above is **only proven for quadratic objectives**. For a general (non-quadratic) smooth strongly convex function, the heavy-ball method with these parameters may fail to converge at the $O(\sqrt{\kappa})$ rate, or may even diverge. Nesterov’s accelerated gradient, presented next, overcomes this limitation.

In other words, by tuning the stepsize and momentum parameter optimally, the heavy-ball method replaces the $\kappa$ dependence in the GD complexity ([Equation 7.1](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-gd-complexity)) with $\sqrt{\kappa}$. This is a substantial speedup, especially for ill-conditioned problems where $\kappa$ is large.

**Comparison with standard GD:**

- GD with $\alpha = \frac{2}{m+M}$: iteration complexity $K = O(\kappa \cdot \log(1/\varepsilon))$.
- Heavy-ball (momentum): iteration complexity $K = O(\sqrt{\kappa} \cdot \log(1/\varepsilon))$.
- Momentum improves from $\kappa \cdot \log(1/\varepsilon)$ to $\sqrt{\kappa} \cdot \log(1/\varepsilon)$.
- $\alpha_{\text{momentum}} = \bigl(\frac{2}{\sqrt{m}+\sqrt{M}}\bigr)^2 \approx \frac{4}{M} \approx 2 \cdot \alpha_{\text{GD}}$ (when $\kappa$ is large).
- $\beta_{\text{momentum}} \approx 1$.

## 7.3 Nesterov’s Accelerated Gradient (NAG)

The heavy-ball method achieves the optimal $O(\sqrt{\kappa}\log(1/\varepsilon))$ rate on quadratics, but its convergence guarantee does not extend to general smooth convex functions. A natural question arises:

> *Can we achieve the $O(\sqrt{\kappa}\log(1/\varepsilon))$ rate for **all** smooth strongly convex functions, not just quadratics?*

Nesterov’s accelerated gradient (NAG) answers this affirmatively. The key idea is a seemingly minor modification to the heavy-ball update: instead of evaluating the gradient at the current iterate $x^k$, NAG first extrapolates along the momentum direction to a “lookahead” point, and then evaluates the gradient there. This reordering — momentum first, gradient second — is what upgrades the convergence theory from quadratics to the full class of smooth strongly convex objectives.

Recall the heavy-ball update ([Equation 7.2](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-heavy-ball-update)): 
$$
\underbrace{x^{k+1} = x^k - \alpha \nabla f(x^k)}_{\text{gradient step}} + \underbrace{\beta(x^k - x^{k-1})}_{\text{momentum}}.
$$

The heavy-ball method first computes the gradient at the current point $x^k$, then adds the momentum term. Nesterov’s method **reverses this order**:

ImportantAlgorithm: Nesterov’s Accelerated Gradient

**Step 1 (Momentum/Extrapolation).** Compute the lookahead point: 
$$
y^{k+1} = x^k + \beta(x^k - x^{k-1}).
$$

**Step 2 (Gradient).** Take a gradient step from the lookahead point: 
$$
x^{k+1} = y^{k+1} - \alpha \nabla f(y^{k+1}).
$$

Combining both steps into a single update: 
$$
x^{k+1} = x^k + \beta(x^k - x^{k-1}) - \alpha \cdot \nabla f\!\bigl(x^k + \beta(x^k - x^{k-1})\bigr). \tag{7.4}
$$

To highlight the structural difference, we can write both methods in two-step form:

$$
\boxed{\textbf{Heavy-ball:}} \quad \begin{cases} y^{k+1} = x^k - \alpha \nabla f(x^k) & \text{(gradient at } x^k\text{)} \\ x^{k+1} = y^{k+1} + \beta(x^k - x^{k-1}) & \text{(then add momentum)} \end{cases}
$$

$$
\boxed{\textbf{Nesterov:}} \quad \begin{cases} y^{k+1} = x^k + \beta(x^k - x^{k-1}) & \text{(first extrapolate)} \\ x^{k+1} = y^{k+1} - \alpha \nabla f(y^{k+1}) & \text{(gradient at } y^{k+1}\text{)} \end{cases}
$$

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch07-nesterov-momentum.svg)

Figure 7.2: Nesterov’s accelerated gradient vs. heavy-ball momentum. Heavy-ball evaluates the gradient at the current point x k x^k and then adds momentum. Nesterov first extrapolates to an intermediate “lookahead” point y + 1 = β ( − ) y^{k+1} = x^k + \\beta(x^k - x^{k-1}) and then evaluates the gradient there. This seemingly small change in evaluation point is what upgrades the convergence guarantee from quadratics-only (heavy-ball) to all smooth convex functions.

**Key difference:** Heavy-ball ([Equation 7.2](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-heavy-ball-update)) computes the gradient at $x^k$, then adds momentum. Nesterov ([Equation 7.4](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-nag-update)) first adds momentum, then computes the gradient at the “look-ahead” point.

NAG is a modified version of the heavy-ball method with **faster convergence** than GD. Crucially, the convergence theory applies to **general convex functions**, not just quadratics.

**Detailed comparison: Heavy-Ball vs. Nesterov AGD**

| **Step 1** | Compute gradient at current point $x^k$ | Extrapolate: $y^{k+1} = x^k + \beta(x^k - x^{k-1})$ |
| --- | --- | --- |
| **Step 2** | Add momentum: $x^{k+1} = x^k - \alpha \nabla f(x^k) + \beta(x^k - x^{k-1})$ | Compute gradient at lookahead: $x^{k+1} = y^{k+1} - \alpha \nabla f(y^{k+1})$ |
| **Order** | Gradient first, then momentum | Momentum first, then gradient |
| **Gradient evaluated at** | Current iterate $x^k$ | Lookahead point $y^{k+1} = x^k + \beta(x^k - x^{k-1})$ |
| **Optimal $\alpha$** | $\bigl(\frac{2}{\sqrt{m}+\sqrt{M}}\bigr)^2 \approx \frac{4}{M}$ | $\frac{1}{M}$ |
| **Optimal $\beta$** | $\bigl(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\bigr)^2$ | $\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}$ |
| **Rate** | $O(\sqrt{\kappa} \log(1/\varepsilon))$ | $O(\sqrt{\kappa} \log(1/\varepsilon))$ |
| **Convergence guarantee** | Quadratics only | All $M$ -smooth, $m$ -strongly convex functions |

The seemingly small change — evaluating the gradient at a “lookahead” point instead of the current iterate — is what allows Nesterov’s method to achieve provable acceleration on the full class of smooth strongly convex functions. Heavy-ball uses a larger stepsize ($\approx 4/M$) with a squared momentum coefficient, while Nesterov uses a more conservative stepsize ($1/M$) with an unsquared momentum coefficient. This pairing makes NAG more stable: the lookahead gradient provides a corrective signal that prevents the overshoot issues that can cause heavy-ball to diverge on non-quadratic objectives.

### 7.3.1 NAG Convergence

The key question is whether the accelerated $O(\sqrt{\kappa})$ rate — which for the heavy-ball method was only proven for quadratics — can be achieved for **all** smooth strongly convex functions. The answer is yes: by evaluating the gradient at the lookahead point, NAG achieves this rate universally.

We first derive the optimal parameters on quadratics (where the analysis is transparent), then state the general result.

**Derivation on quadratics.** For $f(x) = \frac{1}{2}x^\top A x - b^\top x$ with $m\mathbf{I} \preceq A \preceq M\mathbf{I}$, the NAG update becomes: 
$$
w^{k+1} = (1+\beta)(\mathbf{I} - \alpha A)\,w^k - \beta(\mathbf{I} - \alpha A)\,w^{k-1},
$$
 where $w^k = x^k - x^*$. For each eigenvalue $\lambda \in [m, M]$ of $A$, let $\gamma = 1 - \alpha\lambda$. The $2\times 2$ companion block is: 
$$
T_{\lambda}^{\text{NAG}} = \begin{pmatrix} (1+\beta)\gamma & -\beta\gamma \\ 1 & 0 \end{pmatrix},
$$
 with characteristic polynomial $\mu^2 - (1+\beta)\gamma\,\mu + \beta\gamma = 0$ and eigenvalue product $\mu_1 \mu_2 = \beta\gamma = \beta(1 - \alpha\lambda)$.

Unlike the heavy-ball case where $\mu_1\mu_2 = \beta$ is constant, here the product $\beta(1-\alpha\lambda)$ varies with $\lambda$. Choosing $\alpha = 1/M$ ensures $\gamma \in [0, 1-1/\kappa]$ for all $\lambda \in [m, M]$, and setting $\beta = \frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}$ (unsquared, unlike HB) minimizes the worst-case spectral radius over all eigenvalues. The resulting spectral radius is: 
$$
\rho(T^{\text{NAG}}) = \frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1} = 1 - \frac{2}{\sqrt{\kappa}+1}.
$$

Crucially, this same rate holds **beyond quadratics**. Nesterov proved (using an *estimate sequence* technique) that the lookahead gradient evaluation makes the convergence analysis robust to the nonlinear terms that arise in general smooth strongly convex objectives:

**Corollary 7.2 (NAG Convergence (General Smooth Strongly Convex))** Let $f$ be $M$ -smooth and $m$ -strongly convex (not necessarily quadratic). With parameters: 
$$
\alpha_{\text{NAG}} = \frac{1}{M}, \qquad \beta_{\text{NAG}} = \frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1},
$$

Nesterov’s accelerated gradient satisfies: 
$$
\|x^{k+1} - x^*\|_2 \leq \Bigl(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\Bigr)^k \cdot \|x^1 - x^*\|_2 \leq \exp\!\Bigl(-\frac{2k}{\sqrt{\kappa} + 1}\Bigr) \cdot \|x^1 - x^*\|_2.
$$

Iteration complexity: 
$$
\text{Iteration complexity (NAG)} = O\!\bigl(\sqrt{\kappa} \cdot \log(1/\varepsilon)\bigr). \tag{7.5}
$$

Nesterov’s accelerated gradient achieves the same $O(\sqrt{\kappa} \cdot \log(1/\varepsilon))$ rate as the heavy-ball method on quadratics (compare [Equation 7.5](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-nag-complexity) with [Equation 7.3](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-hb-complexity)), but with the crucial advantage that this rate is **provably achieved for all smooth strongly convex functions**. This makes NAG a foundational algorithm in convex optimization theory.

The following figure shows the three methods on the ill-conditioned quadratic $f(x) = \frac{1}{2}(x_1^2 + \kappa\, x_2^2)$. Drag the slider to increase the condition number and observe how GD develops increasingly severe oscillations, while Nesterov’s method maintains a smooth path to the optimum.

### GD vs. Heavy Ball vs. Nesterov

Quadratic: f(x) = ½(x <sub>1</sub> ² + κ x <sub>2</sub> ²)  |  Starting point: (4, 1)  |  60 iterations

15

After 60 iterations  |  GD: f = 1.70e-6   HB: f = 2.18e-23   NAG: f = 5.92e-13

## 7.4 Adaptive Learning Rates (Stepsizes)

While momentum methods reduce the dependence on the condition number from $\kappa$ to $\sqrt{\kappa}$, they still use the **same stepsize in each direction** of $x$. This is undesirable because it does not utilize the curvature — actually we want to move slower along high curvature directions, and move faster along low curvature directions.

This motivates **adaptive methods**, which use the “variance of gradient” to weight the gradient updates. We will introduce **AdaGrad**, **RMSProp**, and **Adam**. These methods are popular in training neural networks. Convergence theory for these methods is out of the scope of this course.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch07-uniform-vs-adaptive-stepsize.svg)

Figure 7.3: Uniform stepsize treats all directions equally, while adaptive stepsize adjusts to local curvature.

[Figure 7.3](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#fig-uniform-vs-adaptive) contrasts the two strategies on an elongated quadratic (elliptic contours indicate very different curvature along the two axes). With a uniform stepsize (left), the iterates zig-zag: the step is too large in the high-curvature (short-axis) direction and too small in the low-curvature (long-axis) direction. An adaptive method (right) rescales each coordinate by the inverse of its accumulated gradient magnitude, taking larger steps along the flat direction and smaller steps along the steep direction, producing a much more direct path to the optimum.

### 7.4.1 AdaGrad (Adaptive Gradient)

**Motivation.** Gradient descent uses the same step size $\alpha$ for every coordinate. But in many problems — especially with sparse features (NLP, recommender systems) — some coordinates receive frequent gradient updates while others are updated rarely. A coordinate that is rarely updated has accumulated less information, so we should be willing to take *larger* steps in that direction. Conversely, a frequently updated coordinate has been refined more, so smaller steps are appropriate.

AdaGrad formalizes this idea: it maintains a **per-coordinate accumulation of past squared gradients** and uses their inverse square root to scale the learning rate. Coordinates with large accumulated gradients (frequently or sharply updated) get smaller effective step sizes; coordinates with small accumulated gradients get larger ones.

ImportantAlgorithm: AdaGrad

At iteration $k$, let $g^k = \nabla f(x^k)$ denote the gradient. Maintain a running sum of squared gradients for each coordinate:

$$
v_j^k = \sum_{\ell=1}^{k} \bigl[g_j^\ell\bigr]^2 = v_j^{k-1} + \bigl[g_j^k\bigr]^2, \qquad j = 1, \ldots, n.
$$

**Update:** 
$$
x_j^{k+1} = x_j^k - \frac{\alpha}{\sqrt{v_j^k} + \varepsilon} \cdot g_j^k, \qquad \forall\, j \in [n],
$$

where $\alpha > 0$ is the base learning rate and $\varepsilon > 0$ (e.g., $10^{-8}$) prevents division by zero.

**Derivation.** The full-matrix version of AdaGrad sets $G^k = \sum_{\ell=1}^k g^\ell (g^\ell)^\top$ and updates $x^{k+1} = x^k - \alpha (G^k + \varepsilon I)^{-1/2} g^k$. The matrix $(G^k)^{-1/2}$ acts as an approximate inverse Hessian, adapting the geometry to the curvature revealed by past gradients. Since computing $(G^k)^{-1/2}$ costs $O(n^3)$, the **diagonal approximation** $v_j^k = [G^k]_{jj}$ is used in practice, reducing the cost to $O(n)$ per step.

**Properties of AdaGrad:**

- **Adaptive per-coordinate learning rates.** The effective step size for coordinate $j$ at step $k$ is $\alpha / (\sqrt{v_j^k} + \varepsilon)$. Coordinates with large accumulated gradients (high curvature or frequent updates) receive smaller steps; coordinates with small accumulated gradients receive larger steps.
- **Well-suited for sparse problems.** In NLP and recommendation, most features are zero in any given example. AdaGrad automatically gives larger updates to rare features and smaller updates to common ones, which is exactly the right behavior for learning sparse representations.
- **Monotonically decreasing step sizes.** Since $v_j^k$ only increases, the effective learning rate $\alpha / \sqrt{v_j^k}$ decreases monotonically. For convex problems, this is desirable (it mirrors a diminishing step size schedule). For nonconvex problems like neural network training, this can be **too aggressive** — the learning rate may shrink to near zero before the model has converged, causing training to stall. This motivates RMSProp.

**In PyTorch:**

```python
optimizer = torch.optim.Adagrad(model.parameters(), lr=0.01)
```

### 7.4.2 RMSProp (Root Mean-Square Propagation)

**Motivation.** AdaGrad’s monotonically increasing denominator $v_j^k = \sum_{\ell=1}^k [g_j^\ell]^2$ is both a strength and a weakness. For convex optimization with a fixed objective, the diminishing step size guarantees convergence. But for neural network training, the loss landscape is nonstationary — the relevant curvature changes as the network learns — so we want the step size to *adapt* to recent curvature, not be permanently shrunk by gradients from early training.

RMSProp (proposed by Hinton in a lecture, never published as a paper) fixes this by replacing the cumulative sum with an **exponential moving average (EMA)** of squared gradients. This forgets old gradient information at a controlled rate, so the effective learning rate can increase again when recent gradients are small.

ImportantAlgorithm: RMSProp

Maintain an exponential moving average of squared gradients:

$$
v_j^k = \beta \cdot v_j^{k-1} + (1-\beta)\,\bigl[g_j^k\bigr]^2, \qquad \beta \in (0, 1).
$$

**Update:** 
$$
x_j^{k+1} = x_j^k - \frac{\alpha}{\sqrt{v_j^k} + \varepsilon} \cdot g_j^k, \qquad \forall\, j \in [n].
$$

Typical hyperparameter: $\beta = 0.9$ (or $0.99$).

**What the EMA computes.** Expanding the recursion:

$$
v_j^k = (1-\beta) \sum_{\ell=1}^{k} \beta^{k-\ell} \bigl[g_j^\ell\bigr]^2.
$$

This is a *weighted* average of past squared gradients, with weights that decay exponentially. The effective window length is approximately $1/(1-\beta)$: with $\beta = 0.9$, the algorithm “remembers” roughly the last 10 gradients; with $\beta = 0.99$, roughly the last 100.

**Properties of RMSProp:**

- **Non-monotonic learning rate.** Unlike AdaGrad, the effective step size $\alpha / \sqrt{v_j^k}$ can increase when recent gradients are smaller than the historical average. This makes RMSProp better suited for the nonstationary objectives encountered in deep learning.
- **Implicit curvature estimation.** Since $v_j^k \approx \mathbb{E}[(g_j^k)^2]$, dividing by $\sqrt{v_j^k}$ approximately normalizes each coordinate by its root-mean-square gradient magnitude. If coordinate $j$ has typical gradient magnitude $\sigma_j$, the effective update is $\alpha \cdot g_j^k / \sigma_j$, which has unit scale regardless of $\sigma_j$.
- **No bias correction.** RMSProp does not correct for the initialization bias when $v_j^0 = 0$ (see Adam below for the fix).

**In PyTorch:**

```python
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.001, alpha=0.9)
# Note: PyTorch uses \`alpha\` for what we call β (the EMA decay)
```

### 7.4.3 Adam (Adaptive Moment Estimation)

**Motivation.** RMSProp adapts the learning rate per coordinate using second-moment information (the magnitude of recent gradients), but uses the raw gradient $g_j^k$ for the update direction. The heavy-ball method uses momentum to smooth the update direction, but with a uniform step size. **Adam** combines the best of both: it uses a first-moment EMA (momentum) for the direction and a second-moment EMA (RMSProp) for per-coordinate step size scaling.

ImportantAlgorithm: Adam

Initialize $m^0 = 0$, $v^0 = 0$. At each step $k = 1, 2, \ldots$:

**First moment (momentum):** 
$$
m_j^k = \beta_1 \cdot m_j^{k-1} + (1-\beta_1)\,g_j^k
$$

**Second moment (RMSProp):** 
$$
v_j^k = \beta_2 \cdot v_j^{k-1} + (1-\beta_2)\,\bigl[g_j^k\bigr]^2
$$

**Bias correction:** 
$$
\widehat{m}_j^k = \frac{m_j^k}{1 - \beta_1^k}, \qquad \widehat{v}_j^k = \frac{v_j^k}{1 - \beta_2^k}
$$

**Parameter update:** 
$$
x_j^{k+1} = x_j^k - \alpha \cdot \frac{\widehat{m}_j^k}{\sqrt{\widehat{v}_j^k} + \varepsilon} \tag{7.6}
$$

Typical hyperparameters: $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\varepsilon = 10^{-8}$, $\alpha = 10^{-3}$.

**Why bias correction?** Both $m^k$ and $v^k$ are initialized at zero, so early iterates are biased toward zero. To see why, expand the first-moment EMA:

$$
m_j^k = (1-\beta_1)\sum_{\ell=1}^{k} \beta_1^{k-\ell}\, g_j^\ell.
$$

Taking expectations (assuming $\mathbb{E}[g_j^\ell] \approx \mu_j$ is roughly constant):

$$
\mathbb{E}[m_j^k] = \mu_j \cdot (1-\beta_1) \sum_{\ell=1}^{k} \beta_1^{k-\ell} = \mu_j \cdot (1 - \beta_1^k).
$$

This is biased: $\mathbb{E}[m_j^k] = \mu_j(1-\beta_1^k) \neq \mu_j$. Dividing by $(1-\beta_1^k)$ corrects this:

$$
\mathbb{E}[\widehat{m}_j^k] = \frac{\mathbb{E}[m_j^k]}{1-\beta_1^k} = \mu_j.
$$

The same argument applies to $v_j^k$ with $\beta_2$. The bias is most significant in the first few iterations (when $\beta_1^k$ and $\beta_2^k$ are not yet negligible) and vanishes as $k \to \infty$.

**Example 7.2 (Example: Bias Correction in Practice)** With $\beta_2 = 0.999$, at step $k=1$: $v_j^1 = 0.001 \cdot [g_j^1]^2$, which underestimates the true second moment by a factor of 1000. The corrected $\widehat{v}_j^1 = v_j^1 / (1 - 0.999) = [g_j^1]^2$ recovers the unbiased estimate. By $k = 1000$: $1 - \beta_2^{1000} \approx 0.632$, so the correction is about $1.58\times$. By $k = 5000$: the correction is negligible ($\approx 1.007\times$).

**Properties of Adam:**

- **Bounded effective step size.** The update $\widehat{m}_j^k / (\sqrt{\widehat{v}_j^k} + \varepsilon)$ has a natural scale. By the Cauchy–Schwarz inequality, $|\widehat{m}_j^k| \leq \sqrt{\widehat{v}_j^k}$ (since the absolute mean is at most the root-mean-square), so $|\widehat{m}_j^k / \sqrt{\widehat{v}_j^k}| \leq 1$. This means each coordinate update is bounded by $\alpha$, providing a form of **implicit gradient clipping**.
- **Scale invariance.** Multiplying all gradients by a constant $c > 0$ does not change the Adam update direction, since $\widehat{m}_j \to c\,\widehat{m}_j$ and $\sqrt{\widehat{v}_j} \to |c|\sqrt{\widehat{v}_j}$. This makes Adam robust to the scale of the loss function.
- **Default for deep learning.** Adam (and its variant AdamW) is the most widely used optimizer for training neural networks, particularly transformers. It converges well out-of-the-box with default hyperparameters.

WarningKnown Issue: Non-convergence of Adam

Adam can fail to converge even on simple convex problems. The issue is that the second-moment estimate $v_j^k$ is a *moving* average, so the effective step size can increase at inopportune times. **AMSGrad** fixes this by maintaining the running maximum of $v_j^k$: $\widehat{v}_j^k = \max(\widehat{v}_j^{k-1}, v_j^k)$, ensuring the effective learning rate is non-increasing.

**In PyTorch:**

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999))
```

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch07-adam-components.svg)

Figure 7.4: Adam combines momentum (first moment) with RMSProp (second moment) for adaptive optimization.

[Figure 7.4](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#fig-adam-components) traces the data flow inside Adam. Each gradient $g_t$ feeds into two parallel streams: the **first-moment** estimate $m_t$ (an exponential moving average of $g_t$, the momentum branch in blue) and the **second-moment** estimate $v_t$ (an exponential moving average of $g_t^2$, the RMSProp branch in red). The update divides the bias-corrected first moment $\widehat{m}_t$ by $\sqrt{\widehat{v}_t} + \varepsilon$, so each coordinate is scaled by the inverse of its typical gradient magnitude — combining directional smoothing from momentum with per-coordinate adaptivity from RMSProp.

### 7.4.4 Weight Decay vs. L2 Regularization

The Adam update rule ([Equation 7.6](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-adam-update)) divides each gradient component by the square root of its accumulated second moment. While this adaptive scaling is powerful for optimization, it introduces a subtle interaction with regularization that must be handled carefully. A common technique to prevent overfitting in machine learning is **L2 regularization** (also called **ridge regularization**), which adds a penalty $\frac{\lambda}{2}\|\theta\|_2^2$ to the loss:

$$
\min_\theta \; \mathcal{L}(\theta) + \frac{\lambda}{2}\|\theta\|_2^2.
$$

For standard SGD, L2 regularization and **weight decay** are mathematically equivalent. However, for Adam, they are *not* — and confusing the two leads to subtle but significant training issues.

#### 7.4.4.1 SGD: L2 Regularization = Weight Decay

With L2 regularization, the gradient becomes $\nabla \mathcal{L}(\theta) + \lambda\theta$. The SGD update is:

$$
\theta \leftarrow \theta - \alpha\bigl(\nabla \mathcal{L}(\theta) + \lambda\theta\bigr) = (1 - \alpha\lambda)\,\theta - \alpha\,\nabla \mathcal{L}(\theta).
$$

With weight decay (shrinking parameters directly by a factor at each step):

$$
\theta \leftarrow \theta - \alpha\,\nabla \mathcal{L}(\theta) - \alpha\lambda\,\theta = (1 - \alpha\lambda)\,\theta - \alpha\,\nabla \mathcal{L}(\theta).
$$

These are identical. For SGD, “L2 regularization” and “weight decay” are two names for the same operation.

#### 7.4.4.2 Adam: L2 Regularization ≠\\neq Weight Decay

Now apply Adam to the L2-regularized objective. The gradient is $g = \nabla \mathcal{L}(\theta) + \lambda\theta$. Adam computes:

$$
m \leftarrow \beta_1 m + (1-\beta_1)\,g, \qquad v \leftarrow \beta_2 v + (1-\beta_2)\,g^2,
$$
 
$$
\theta_j \leftarrow \theta_j - \alpha \cdot \frac{\widehat{m}_j}{\sqrt{\widehat{v}_j} + \varepsilon}.
$$

The weight decay term $\lambda\theta_j$ is included in $g$, so it gets divided by $\sqrt{\widehat{v}_j}$. This means:

- For parameters with **large accumulated gradients** (large $\widehat{v}_j$): the effective decay $\frac{\lambda\theta_j}{\sqrt{\widehat{v}_j}}$ is **small**.
- For parameters with **small accumulated gradients** (small $\widehat{v}_j$): the effective decay is **large**.

This is the **opposite** of what we want — weight decay should shrink all parameters uniformly, but Adam’s adaptive scaling distorts it.

WarningThe Core Problem

Adam’s per-coordinate adaptive learning rate interferes with L2 regularization. The regularization penalty, which should apply uniformly to all parameters, gets non-uniformly scaled by the second moment estimate $\widehat{v}$. Frequently updated parameters receive less decay than they should, while rarely updated parameters receive more.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch07-adam-l2-vs-adamw.svg)

Figure 7.5: Adam with L2 regularization distorts the weight decay non-uniformly across parameters. AdamW decouples weight decay from the adaptive gradient, applying it uniformly.

### 7.4.5 AdamW (Adam with Decoupled Weight Decay)

ImportantAlgorithm: AdamW

The fix is simple: **decouple** weight decay from the gradient computation. Instead of adding $\lambda\theta$ to the gradient before Adam processes it, apply weight decay directly to the parameters *after* the Adam update.

**Updates:** 
$$
\begin{aligned}
g^k &= \nabla \mathcal{L}(\theta^k) & &\text{(gradient of loss only, no L2 term)} \\
m^{k+1} &= \beta_1 \cdot m^k + (1-\beta_1)\,g^k, \\
v^{k+1} &= \beta_2 \cdot v^k + (1-\beta_2)\,(g^k)^2, \\
\theta^{k+1}_j &= \theta^k_j - \alpha\,\frac{\widehat{m}^{k+1}_j}{\sqrt{\widehat{v}^{k+1}_j} + \varepsilon} - \alpha\lambda\,\theta^k_j. & &\text{(weight decay applied directly)}
\end{aligned}
$$

Equivalently: $\theta^{k+1} = (1 - \alpha\lambda)\,\theta^k - \alpha\,\frac{\widehat{m}^{k+1}}{\sqrt{\widehat{v}^{k+1}} + \varepsilon}.$

The key difference: in AdamW, the decay $\alpha\lambda\,\theta^k_j$ is **not** divided by $\sqrt{\widehat{v}_j}$, so all parameters are decayed at the same rate regardless of their gradient history. This recovers the intended behavior of weight decay.

**Side-by-side comparison:**

| Gradient | $g = \nabla\mathcal{L}(\theta) + \lambda\theta$ | $g = \nabla\mathcal{L}(\theta)$ |
| --- | --- | --- |
| Decay mechanism | $\lambda\theta$ scaled by $1/\sqrt{\widehat{v}}$ | $\lambda\theta$ applied directly |
| Effective decay | Non-uniform across parameters | Uniform across parameters |
| Equivalent to SGD+WD? | No | Yes (in the limit $\beta_1, \beta_2 \to 0$) |

In practice, AdamW with weight decay $\lambda \approx 0.01$ is the default optimizer for training Transformers (GPT, BERT, etc.).

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch07-optimizer-timeline.svg)

Figure 7.6: Evolution of first-order optimizers: from vanilla gradient descent to AdamW.

### Interactive: Adaptive Methods on the Beale Function

f(x,y) = (1.5 − x + xy)² + (2.25 − x + xy²)² + (2.625 − x + xy³)²  |  Minimum at (3, 0.5)  |  Start: (1, 1)

**Left:** Trajectories on the Beale function contour. **Right:** Objective value vs. iteration (log scale). **Try:** Give AdaGrad a much larger α (e.g. 1.0) — its self-regulating denominator keeps it stable. Heavy-Ball with momentum converges fastest at these default settings.

### Interactive: Gradient Descent Oscillation on Quadratics

f(x) = ½ x <sup>T</sup> Ax,   A = diag(1, λ <sub>max</sub>)  |  Start: (−5, 5)  |  60 iterations

GD oscillates along the high-curvature direction (x <sub>2</sub>) while making slow progress along x <sub>1</sub>. Increasing κ = λ <sub>max</sub> makes oscillation worse. The optimal step size α = 2/(λ <sub>min</sub> + λ <sub>max</sub>) minimizes this zigzag. **Try:** set α near 2/λ <sub>max</sub> to see the oscillation vanish — but convergence along x <sub>1</sub> slows dramatically.

Figure 7.1: Convergence rates of GD vs. Heavy-Ball momentum. The *O* (√κ log 1/ε) complexity of momentum is a significant improvement over *O* (κ log 1/ε) for GD.

**Summary of iteration complexities** (strongly convex quadratics):

- **Gradient Descent:** $O\!\bigl(\kappa \cdot \log(1/\varepsilon)\bigr)$
- **Heavy-Ball Momentum:** $O\!\bigl(\sqrt{\kappa} \cdot \log(1/\varepsilon)\bigr)$
- **Nesterov’s Accelerated Gradient:** $O\!\bigl(\sqrt{\kappa} \cdot \log(1/\varepsilon)\bigr)$
- **AdaGrad / RMSProp / Adam:** Widely used in practice; convergence theory is more nuanced.

## 7.5 Using Adam and AdamW in PyTorch

The optimizers described in this chapter are implemented in PyTorch’s `torch.optim` module. Here we show the standard training pattern using Adam and AdamW — the two most widely used optimizers for modern deep learning.

### 7.5.1 Basic Training Loop

The PyTorch training loop follows a three-step pattern: (1) compute the loss, (2) backpropagate gradients, (3) update parameters.

```python
import torch
import torch.nn as nn

# Define model and data
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)
loss_fn = nn.CrossEntropyLoss()

# Create optimizer — AdamW is the recommended default
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-3,            # base learning rate α
    betas=(0.9, 0.999), # (β₁, β₂): momentum and RMSProp decay
    weight_decay=0.01   # decoupled weight decay λ
)

# Training loop
for epoch in range(num_epochs):
    for X_batch, y_batch in dataloader:
        loss = loss_fn(model(X_batch), y_batch)  # forward pass
        optimizer.zero_grad()   # clear old gradients
        loss.backward()         # compute ∇L(θ) via backpropagation
        optimizer.step()        # θ ← θ - α · m̂/(√v̂ + ε) - αλθ
```

### 7.5.2 Combining with Learning Rate Schedules

In practice, Adam/AdamW is almost always combined with a learning rate schedule (see [Chapter 6](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html) for the theory). PyTorch provides schedulers that adjust $\alpha$ over training:

```python
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

# Warmup for 1000 steps, then cosine decay
warmup = LinearLR(optimizer, start_factor=0.01, total_iters=1000)
cosine = CosineAnnealingLR(optimizer, T_max=50000)
scheduler = SequentialLR(optimizer, [warmup, cosine], milestones=[1000])

for step, (X, y) in enumerate(dataloader):
    loss = loss_fn(model(X), y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    scheduler.step()  # update learning rate after each step
```

### 7.5.3 Per-Parameter-Group Configuration

For large models, different parts of the network often benefit from different hyperparameters. A common pattern is to **exclude bias and normalization parameters from weight decay** (since shrinking biases toward zero is rarely desirable):

```python
# Separate parameters into two groups
decay_params = [p for name, p in model.named_parameters()
                if p.ndim >= 2]              # weight matrices
no_decay_params = [p for name, p in model.named_parameters()
                   if p.ndim < 2]             # biases, LayerNorm

optimizer = torch.optim.AdamW([
    {"params": decay_params, "weight_decay": 0.01},
    {"params": no_decay_params, "weight_decay": 0.0}
], lr=1e-3, betas=(0.9, 0.999))
```

This configuration is standard for training transformers (GPT, BERT, ViT) and is used by virtually all large language model training codebases.

TipPractical Guidelines for Choosing an Optimizer

| **Transformers / LLMs** | AdamW + cosine schedule + warmup | $\alpha = 10^{-4}$ – $10^{-3}$, $\beta_1 = 0.9$, $\beta_2 = 0.95$, WD $= 0.1$ |
| --- | --- | --- |
| **CNNs (ResNet, etc.)** | SGD + momentum + StepLR | $\alpha = 0.1$, $\beta = 0.9$, WD $= 10^{-4}$ |
| **Fine-tuning pretrained models** | AdamW + small LR | $\alpha = 10^{-5}$ – $10^{-4}$, WD $= 0.01$ |
| **Sparse / NLP (classical)** | AdaGrad | $\alpha = 0.01$ – $0.1$ |
| **General-purpose default** | AdamW | $\alpha = 10^{-3}$, default $\beta$ s, WD $= 0.01$ |

---

## 7.6 Modern Matrix Optimizers

The adaptive methods above — AdaGrad, RMSProp, Adam — adjust the learning rate *per coordinate*, using diagonal approximations to the gradient’s second-moment matrix. This works well when the important curvature information is captured by per-coordinate variance. But training deep neural networks involves optimizing over **matrix-shaped parameters** — the weight matrices $W \in \mathbb{R}^{m \times n}$ in every linear layer. Standard optimizers treat these matrices as flat vectors of $mn$ numbers, ignoring their rich structure. Recent advances have shown that exploiting the matrix geometry of parameters — through spectral norms, SVD-based updates, and Kronecker-factored preconditioners — can dramatically accelerate training while remaining firmly first-order methods (no Hessian computation required). This section develops the theory behind these modern optimizers and connects them to the steepest descent framework from [Chapter 6](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html).

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch23-optimizer-branches.svg)

Figure 7.7: Three approaches to matrix gradient updates: GD flattens the gradient, Muon orthogonalizes via SVD, and Shampoo preconditions with Kronecker factors.

### 7.6.1 The Steepest Descent Framework for Matrices

Recall from [Chapter 6](https://zhuoranyang.github.io/sds431-notes/lectures/06-gradient-descent.html) the steepest descent framework: given a norm $\|\cdot\|$, the steepest descent direction solves

$$
\min_{d:\,\|d\| \leq 1} \;\langle \nabla f(x),\, d \rangle. \tag{7.7}
$$

Different norms yield different algorithms. For **vector** parameters, we established:

| $\ell_2$ | $-\nabla f / \\|\nabla f\\|_2$ | Gradient descent |
| --- | --- | --- | --- | --- |
| $\ell_1$ | $-e_j \cdot \text{sign}(\partial_j f)$ | Coordinate descent |
| $\ell_\infty$ | $-\text{sign}(\nabla f)$ | Sign gradient descent |
| Hessian ($\\|\cdot\\|_{\nabla^2 f}$) | $-[\nabla^2 f]^{-1} \nabla f$ | Newton’s method |

For **matrix** parameters $W \in \mathbb{R}^{m \times n}$, the gradient $G = \nabla_W \mathcal{L}$ is also a matrix, and we can choose among several matrix norms:

| Frobenius $\\|D\\|_F$ | $\sqrt{\sum_{ij} D_{ij}^2}$ | $-G / \\|G\\|_F$ | Gradient descent |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Spectral $\\|D\\|_{\text{op}}$ | $\sigma_{\max}(D)$ | $-UV^\top$ (from SVD of $G$) | **Muon** |

The Frobenius norm treats the matrix as a flat vector — it is simply the $\ell_2$ norm of $\text{vec}(W)$. The spectral norm is sensitive to the singular value structure, leading to qualitatively different update directions.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch14-frobenius-vs-spectral.svg)

Figure 7.8: Singular values of the gradient G vs. the Muon update U V ⊤ UV^\\top. Gradient descent preserves the (often skewed) singular value distribution; Muon equalizes all singular values to 1.

### 7.6.2 Muon: Steepest Descent under the Spectral Norm

The steepest descent framework ([Equation 7.7](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-steepest-descent-general)) tells us that the choice of norm determines the update direction. We now work out what happens when we choose the spectral (operator) norm for matrix parameters — this leads to the Muon optimizer. Given a matrix parameter $W$ with gradient $G = \nabla_W \mathcal{L}$, the **spectral-norm steepest descent** problem is:

$$
\min_{D:\,\|D\|_{\text{op}} \leq 1} \;\langle G,\, D \rangle_F = \min_{D:\,\|D\|_{\text{op}} \leq 1} \;\text{tr}(G^\top D).
$$

**Theorem 7.2 (Spectral-Norm Steepest Descent)** Let $G = U \Sigma V^\top$ be the (compact) SVD of the gradient $G \in \mathbb{R}^{m \times n}$. Then the solution to $\min_{\|D\|_{\text{op}} \leq 1} \text{tr}(G^\top D)$ is:

$$
D^* = -U V^\top.
$$

The minimum value is $-\|G\|_* = -\sum_i \sigma_i(G)$ (the negative nuclear norm of $G$).

*Proof*. The proof uses von Neumann’s trace inequality to lower-bound the objective and then verifies that $D^* = -UV^\top$ attains that bound.

**Proof.** By von Neumann’s trace inequality, for any matrices $A, B \in \mathbb{R}^{m \times n}$:

$$
\text{tr}(A^\top B) \leq \sum_i \sigma_i(A)\,\sigma_i(B).
$$

Applying this with $A = G$ and $B = D$, and using $\|D\|_{\text{op}} \leq 1$ (so $\sigma_i(D) \leq 1$ for all $i$):

$$
\text{tr}(G^\top D) \geq -\sum_i \sigma_i(G) \cdot \sigma_i(D) \geq -\sum_i \sigma_i(G) = -\|G\|_*.
$$

Equality holds when $D = -UV^\top$, since $\sigma_i(-UV^\top) = 1$ for all $i$ and the singular vectors align with those of $G$. $\blacksquare$

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch23-muon-svd.svg)

Figure 7.9: Muon replaces the singular values Σ \\boldsymbol{\\Sigma} of the gradient SVD with the identity I \\mathbf{I}, producing the orthogonal update U V ⊤ \\mathbf{U}\\mathbf{V}^\\top.

The **Muon optimizer** (Momentum + Orthogonalization) applies this idea:

ImportantAlgorithm: Muon

For matrix parameter $W \in \mathbb{R}^{m \times n}$ with gradient $G = \nabla_W \mathcal{L}$:

1. **Momentum:** $M \leftarrow \beta \cdot M + (1-\beta)\,G$ (exponential moving average)
2. **Orthogonalize:** Compute SVD $M = U\Sigma V^\top$, set $\widetilde{M} = UV^\top$
3. **Update:** $W \leftarrow W - \alpha\,\widetilde{M}$

The orthogonalization step replaces all singular values of the momentum buffer with 1, producing a direction with unit spectral norm.

TipWhy Spectral-Norm Steepest Descent?

The key insight is that **all directions in the update receive equal “energy”** in terms of the spectral norm. Standard gradient descent can have singular values spanning orders of magnitude — the update is dominated by a few large singular values. The orthogonalization in Muon eliminates this imbalance, analogous to how adaptive methods like Adam equalize per-coordinate scales.

In practice, Muon is applied only to the **matrix-shaped** parameters (weight matrices in linear layers), while scalar parameters (biases, layer norms) use standard Adam or AdamW.

#### 7.6.2.1 Practical Considerations

Computing the full SVD of $M \in \mathbb{R}^{m \times n}$ costs $O(\min(m,n) \cdot mn)$, which is comparable to a matrix multiplication. In practice, Muon often uses a cheaper approximation:

- **Newton-Schulz iteration**: Approximate $UV^\top$ (the polar factor of $M$) by iterating $X \leftarrow \frac{3}{2}X - \frac{1}{2}X X^\top X$, starting from $X_0 = M / \|M\|_F$. This converges cubically and typically needs only 5–10 iterations of matrix multiplications — which are highly optimized on GPUs.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch14-muon-vs-gd.svg)

Figure 7.10: Singular value distributions of gradient vs. Muon update across training. GD updates have highly non-uniform spectra (dominated by top singular values), while Muon equalizes the spectrum to all ones.

### 7.6.3 Shampoo: Full-Matrix Adaptive Preconditioning

Muon exploits the spectral structure of the gradient through orthogonalization, but it does not accumulate historical gradient information the way adaptive methods like AdaGrad and Adam do. Shampoo takes a complementary approach: it builds a full-matrix preconditioner from gradient history, but uses Kronecker factorization to keep the cost manageable.

Recall that AdaGrad adapts the learning rate per coordinate using accumulated squared gradients. The **full-matrix** version maintains $\mathbf{G} = \sum_\ell g^\ell (g^\ell)^\top \in \mathbb{R}^{d \times d}$ and updates $\theta \leftarrow \theta - \alpha\,\mathbf{G}^{-1/2} g$. This is a much better preconditioner because it captures **correlations between coordinates**, not just per-coordinate variance. The diagonal AdaGrad is a special case that ignores all off-diagonal entries.

#### 7.6.3.1 The Scalability Problem

For a matrix parameter $W \in \mathbb{R}^{m \times n}$, we could vectorize it as $\text{vec}(W) \in \mathbb{R}^{mn}$, but then the full-matrix AdaGrad preconditioner would be an $mn \times mn$ matrix — storing and inverting it costs $O(m^2 n^2)$ and $O(m^3 n^3)$ respectively. For a typical Transformer layer with $m = n = 4096$, this would require storing a $16\text{M} \times 16\text{M}$ matrix. Clearly impossible.

**Shampoo** solves this by exploiting the **Kronecker structure** of the gradient outer products.

**Definition 7.1 (Shampoo Preconditioner)** For matrix parameter $W \in \mathbb{R}^{m \times n}$ with gradient $G^k = \nabla_W \mathcal{L}$ at step $k$, Shampoo maintains two smaller matrices:

$$
L^k = \sum_{\ell=1}^{k} G^\ell (G^\ell)^\top \in \mathbb{R}^{m \times m}, \qquad R^k = \sum_{\ell=1}^{k} (G^\ell)^\top G^\ell \in \mathbb{R}^{n \times n}.
$$

The **Shampoo update** is:

$$
W \leftarrow W - \alpha\,(L^k)^{-1/4}\,G^k\,(R^k)^{-1/4}. \tag{7.8}
$$

#### 7.6.3.2 Why Kronecker Factorization Works

The Shampoo update ([Equation 7.8](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-shampoo-update)) applies separate left and right preconditioners rather than a single $mn \times mn$ matrix. The following theorem justifies this factorization by showing that the full preconditioner is well-approximated by a Kronecker product of the two smaller matrices.

**Theorem 7.3 (Kronecker Approximation)** The full-matrix AdaGrad preconditioner for $\text{vec}(W)$ is $\mathbf{G} = \sum_\ell \text{vec}(G^\ell)\,\text{vec}(G^\ell)^\top \in \mathbb{R}^{mn \times mn}$. Using the identity $\text{vec}(ABC) = (C^\top \otimes A)\,\text{vec}(B)$, this admits the approximation:

$$
\mathbf{G} \approx R \otimes L, \tag{7.9}
$$

where $\otimes$ denotes the Kronecker product. Therefore:

$$
\mathbf{G}^{-1/2} \approx R^{-1/2} \otimes L^{-1/2},
$$

which acts on $\text{vec}(G)$ as $L^{-1/2}\, G\, R^{-1/2}$.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch23-kronecker-factorization.svg)

Figure 7.11: Shampoo approximates the intractable m n × mn \\times mn preconditioner G \\mathbf{G} with a Kronecker product L ⊗ R \\mathbf{L} \\otimes \\mathbf{R}, reducing storage from O ( 2 ) O(m^2 n^2) to + O(m^2 + n^2).

The fourth-root version $(L^{-1/4}, R^{-1/4})$ is used in practice for numerical stability.

**Computational savings:**

| Full-matrix AdaGrad | $O(m^2 n^2)$ | $O(m^3 n^3)$ |
| --- | --- | --- |
| Shampoo | $O(m^2 + n^2)$ | $O(m^3 + n^3)$ |
| Diagonal AdaGrad | $O(mn)$ | $O(mn)$ |

Shampoo captures cross-coordinate correlations at a fraction of the cost of the full preconditioner. For $m = n = 4096$: full AdaGrad needs $\sim 10^{14}$ entries; Shampoo needs $\sim 3 \times 10^7$.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch14-preconditioner-comparison.svg)

Figure 7.12: The preconditioner structures. Diagonal AdaGrad uses only the diagonal; Shampoo captures left and right correlations via Kronecker factorization L ⊗ R \\mathbf{L} \\otimes \\mathbf{R}; full-matrix AdaGrad captures everything but is intractable for large dimensions.

### 7.6.4 SOAP: Combining Shampoo with Adam

Shampoo captures cross-coordinate correlations via the Kronecker-factored preconditioner ([Equation 7.9](https://zhuoranyang.github.io/sds431-notes/lectures/07-momentum-adaptive.html#eq-kronecker-approx)), but it does not include the per-coordinate adaptivity that makes Adam so effective in practice. SOAP bridges this gap by running Adam in the coordinate system defined by Shampoo’s eigenbasis, combining the strengths of both methods.

**SOAP** (Shampoo Orthogonalized Adam Preconditioning) combines the best of Shampoo and Adam by running Adam in a coordinate system defined by Shampoo’s preconditioner:

1. **Compute eigenbases:** Eigendecompose $L = Q_L \Lambda_L Q_L^\top$ and $R = Q_R \Lambda_R Q_R^\top$.
2. **Rotate gradient:** $\widetilde{G} = Q_L^\top G\, Q_R$ (project into the Shampoo eigenbasis).
3. **Apply Adam** to $\widetilde{G}$ (maintain momentum and second-moment estimates in the rotated basis).
4. **Rotate back:** Apply the Shampoo fourth-root scaling and rotate the update back to the original coordinates.

TipWhy Rotate?

The eigenvectors of $L$ and $R$ identify the “natural” coordinate system for the optimization landscape — the directions along which gradient variance is highest or lowest. Running Adam in this rotated basis means the per-coordinate adaptive learning rates align with the true principal axes of curvature, rather than the arbitrary axes of the parameter matrix.

This is the same principle behind second-order methods: adapt the coordinate system to the local geometry. SOAP does this using gradient statistics (like Adam/Shampoo) rather than the Hessian, making it practical for the large-scale non-convex problems of deep learning.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch23-soap-pipeline.svg)

Figure 7.13: SOAP pipeline: compute Shampoo eigenbases, rotate the gradient, apply Adam in the rotated basis, then rotate back.

#### 7.6.4.1 Computational Cost

SOAP’s overhead compared to Adam comes from:

- **Eigendecompositions** of $L \in \mathbb{R}^{m \times m}$ and $R \in \mathbb{R}^{n \times n}$: $O(m^3 + n^3)$, but these need not be recomputed every step (e.g., every 100 steps suffices).
- **Rotation**: Two matrix multiplications per step: $O(m^2 n + mn^2)$.
- **Adam in rotated basis**: Same as standard Adam, $O(mn)$.

In practice, the amortized cost per step is modest, and the convergence speedup often compensates for the overhead.

### 7.6.5 The Unified View

Having developed three matrix-aware optimizers — Muon (spectral norm), Shampoo (Kronecker preconditioning), and SOAP (rotated Adam) — we now step back and place them in a single framework that also includes the classical methods from this chapter.

All the optimizers we have studied fit the general framework:

$$
x^{k+1} = x^k - \alpha^k \cdot B^k\,\nabla f(x^k),
$$

differing only in the choice of the **preconditioning matrix** $B^k$:

| GD | $I$ | Nothing | $O(n)$ |
| --- | --- | --- | --- |
| Sign GD | $\text{diag}(1/\|g_j\|)$ | Gradient sign only | $O(n)$ |
| AdaGrad/Adam | $\text{diag}(1/\sqrt{\widehat{v}_j})$ | Per-coord gradient variance | $O(n)$ |
| Muon | SVD orthogonalization | Matrix spectral structure | $O(mn \cdot \min(m,n))$ |
| Shampoo | $(L^{-1/4} \cdot R^{-1/4})$ | Cross-coord correlations | $O(m^3 + n^3)$ |
| SOAP | Shampoo eigenbasis + Adam | Correlations + variance | $O(m^3 + n^3)$ amortized |

The progression tells a clear story:

1. **GD**: Ignore all structure — same step in every direction.
2. **Adam**: Adapt per-coordinate, using gradient variance as a proxy for curvature.
3. **Muon**: Exploit matrix structure via spectral norm — equalize singular values.
4. **Shampoo/SOAP**: Approximate full-matrix preconditioning via Kronecker structure — capture cross-coordinate correlations without the cost of full second-order methods.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch14-optimizer-landscape.svg)

Figure 7.14: The optimizer design space. Moving right adds more structural information about the optimization landscape; moving up increases computational cost. The sweet spot for deep learning lies in the upper-middle region (Muon, Shampoo, SOAP).

## Summary

- **Momentum methods.** Heavy-ball momentum adds a fraction of the previous step ($\beta(x^k - x^{k-1})$) to the gradient update, damping oscillations; Nesterov’s accelerated gradient evaluates the gradient at a “lookahead” point, achieving the optimal $O(\sqrt{\kappa}\log(1/\varepsilon))$ rate for smooth convex optimization.
- **Adaptive learning rates.** AdaGrad accumulates squared gradients to give infrequent features larger updates; RMSProp uses an exponential moving average to prevent the learning rate from vanishing; Adam combines momentum with RMSProp and includes bias correction. AdamW (Adam with decoupled weight decay) is the default optimizer for training large-scale deep learning models.
- **Iteration complexity.** On strongly convex quadratics, GD needs $O(\kappa \log(1/\varepsilon))$ iterations while momentum methods (Heavy-Ball, Nesterov) need only $O(\sqrt{\kappa}\log(1/\varepsilon))$ —a significant improvement when $\kappa$ is large.
- **Modern matrix optimizers.** Muon (spectral-norm steepest descent via SVD), Shampoo (Kronecker-factored preconditioning), and SOAP (Adam in Shampoo’s rotated eigenbasis) exploit the matrix structure of neural network weights, capturing cross-coordinate correlations that diagonal methods like Adam miss.
- **PyTorch usage.** AdamW with cosine learning rate schedule and warmup is the standard recipe for training transformers. Per-parameter-group configuration (excluding biases from weight decay) is essential for large models.

### First-Order Methods Comparison

| **GD** | $x^{k+1} = x^k - \alpha \nabla f(x^k)$ | $O(\kappa \log \tfrac{1}{\varepsilon})$ | Simple, reliable |
| --- | --- | --- | --- |
| **Heavy-Ball** | adds $\beta(x^k - x^{k-1})$ | $O(\sqrt{\kappa} \log \tfrac{1}{\varepsilon})$ | Damps oscillations |
| **Nesterov AGD** | gradient at lookahead point | $O(\sqrt{\kappa} \log \tfrac{1}{\varepsilon})$ | Optimal for smooth convex |
| **AdaGrad** | per-coordinate adaptive $\alpha$ | problem-dependent | Sparse / NLP tasks |
| **Adam** | momentum + RMSProp + bias correction | problem-dependent | Default for deep learning |
| **AdamW** | Adam + decoupled weight decay | problem-dependent | Default for transformers |
| **Muon** | SVD orthogonalization of gradient | problem-dependent | Equalizes singular values |
| **Shampoo** | Kronecker-factored preconditioner | problem-dependent | Cross-coord correlations |
| **SOAP** | Adam in Shampoo eigenbasis | problem-dependent | Best of Shampoo + Adam |

TipLooking Ahead

The momentum and adaptive methods in this chapter assume we can compute the full gradient $\nabla f(x)$ at each iteration and that the objective is smooth. The next chapter addresses three practical challenges: what if the dataset is too large for full gradient computation (SGD), what if the objective is nonsmooth (proximal gradient), and what if there are constraints (Frank-Wolfe)?