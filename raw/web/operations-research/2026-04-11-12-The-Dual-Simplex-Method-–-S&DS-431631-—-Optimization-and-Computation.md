---
author: null
created: 2026-04-11
description: null
tags:
- clippings
title: 12  The Dual Simplex Method – S&DS 431/631 — Optimization and Computation
source_type: web
created_at: 2026-04-11
status: summarized
source_url: https://zhuoranyang.github.io/sds431-notes/lectures/12-dual-simplex.html
published_at: null
related_concepts:
  - 运筹优化
  - 线性规划
  - 数学优化
topics:
  - operations-research
  - 数学优化算法/运筹学
---
**This chapter is optional.** The dual simplex method is a powerful algorithmic tool used in modern LP solvers, but it is not required for the remainder of the course. It is included for students who want a deeper understanding of the primal-dual interplay and how solvers re-optimize after adding constraints.

The [simplex method](https://zhuoranyang.github.io/sds431-notes/lectures/10-simplex-method.html) solves a linear program by walking along the vertices of the primal feasible region, improving the objective at each step. At every iteration it maintains **primal feasibility** ($\widetilde{b} \geq 0$) and works toward **dual feasibility** ($\widetilde{c} \leq 0$ for maximization, equivalently all reduced costs non-positive). But what if we turned things around? What if we instead maintained dual feasibility and worked toward primal feasibility?

This reversal leads to the **dual simplex method** – an algorithm that implicitly runs the simplex method on the [dual LP](https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html), but does so entirely through the primal dictionary. The key insight is the **negative transpose property**: the dual dictionary is always the negative transpose of the primal dictionary. This elegant algebraic relationship means that every primal pivot corresponds to a dual pivot, and we never need to explicitly form the dual problem.

The dual simplex method is not merely a theoretical curiosity. It is the workhorse algorithm behind modern LP solvers when constraints are added to an already-optimal tableau, when sensitivity analysis modifies the right-hand side, or when branch-and-bound algorithms need to re-optimize after adding cutting planes. Understanding the primal-dual interplay through the dictionary is essential for mastering computational optimization.

## What Will Be Covered

- Recap of the primal simplex method and optimality conditions
- The negative transpose property: the dual dictionary is the negative transpose of the primal
- The dual simplex algorithm: maintaining dual feasibility while restoring primal feasibility
- Pivoting rules for the dual simplex method
- Applications: sensitivity analysis, adding constraints, and warm-starting after cuts

## 12.1 Recap of the Primal Simplex Method

Consider the standard-form LP and its dual:

$$
\text{(P):} \quad \max \; c^\top x \quad \text{s.t.} \quad Ax \leq b, \; x \geq 0, \quad x \in \mathbb{R}^n,
$$

$$
\text{(D):} \quad \min \; b^\top y \quad \text{s.t.} \quad A^\top y \geq c, \; y \geq 0.
$$

We introduce $m$ slack variables $w_i = x_{n+i} \geq 0$ so that (P) becomes:

$$
\max \; \bar{c}^\top x \quad \text{s.t.} \quad \bar{A} x = b, \; x \geq 0, \quad x \in \mathbb{R}^{n+m},
$$

where $\bar{A} = (A \mid I_m)$ and $\bar{c} = \begin{pmatrix} c \\ 0 \end{pmatrix}$.

The simplex method partitions the variable indices $[n+m]$ into a **basis** $B$ of size $m$ and **nonbasic** set $N = [n+m] \setminus B$. Given a basis $B$, we compute:

- **Current BFS:** $x_B^* = \bar{A}_B^{-1} b$, $x_N^* = 0$.
- **Reduced costs:** $\widetilde{c} = \bar{c}_N - \widetilde{A}^\top \bar{c}_B$ where $\widetilde{A} = \bar{A}_B^{-1} \bar{A}_N$.
- **Transformed RHS:** $\widetilde{b} = \bar{A}_B^{-1} b = x_B^*$.
- **Objective value:** $\widetilde{\zeta} = \bar{c}_B^\top x_B^*$.

The **primal dictionary** (tableau) is then:

$$
\begin{array}{c|c}
\widetilde{\zeta} & \widetilde{c}^\top \\
\hline
\widetilde{b} & -\widetilde{A}
\end{array}
$$

The primal simplex method maintains $\widetilde{b} \geq 0$ (primal feasibility) and works toward $\widetilde{c} \leq 0$ (dual feasibility / optimality). At each step it chooses an entering variable $q \in N$ with $\widetilde{c}_q > 0$ and a leaving variable $p \in B$ via the minimum ratio test, then pivots $(p, q)$.

The key question is: what happens if we write down the dual dictionary alongside the primal? A remarkably clean algebraic relationship – the negative transpose property – connects the two, and understanding it is the gateway to the dual simplex method.

## 12.2 The Primal-Dual Dictionary Relationship

Having reviewed the primal simplex method, we now uncover the algebraic structure that connects the primal and dual dictionaries. The relationship between the primal and dual dictionaries is one of the most elegant facts in linear programming. We demonstrate this through a concrete example and then state the general result.

### 12.2.1 A Detailed Example

Consider the primal-dual pair:

$$
\text{(P):} \quad \max \; 4x_1 + x_2 + 3x_3 \quad \text{s.t.} \quad x_1 + 4x_2 \leq 1, \;\; 3x_1 - x_2 + x_3 \leq 3,
$$

$$
\text{(D):} \quad \min \; y_1 + 3y_2 \quad \text{s.t.} \quad y_1 + 3y_2 \geq 4, \;\; 4y_1 - y_2 \geq 1, \;\; y_2 \geq 3.
$$

Introduce slack variables $w_1, w_2$ for the primal constraints. The initial basis is $B = \{w_1, w_2\}$, giving $x_1 = x_2 = x_3 = 0$, $w_1 = 1$, $w_2 = 3$. The primal dictionary is:

$$
\text{(P):} \quad \zeta = 4x_1 + x_2 + 3x_3,
$$

$$
w_1 = 1 - x_1 - 4x_2, \qquad w_2 = 3 - 3x_1 + x_2 - x_3.
$$

Now write the dual dictionary. The dual has decision variables $y_1, y_2$ and slack variables $z_1, z_2, z_3$. The initial dual dictionary is:

$$
\text{(D):} \quad -\xi = -y_1 - 3y_2,
$$

$$
z_1 = -4 + y_1 + 3y_2, \qquad z_2 = -1 + 4y_1 - y_2, \qquad z_3 = -3 + y_2.
$$

Write the primal tableau as a matrix:

$$
\text{(P):} \quad \begin{pmatrix} 0 & 4 & 1 & 3 \\ 1 & -1 & -4 & 0 \\ 3 & -3 & 1 & -1 \end{pmatrix}
$$

and the dual tableau:

$$
\text{(D):} \quad \begin{pmatrix} 0 & -1 & -3 \\ -4 & 1 & 3 \\ -1 & 4 & -1 \\ -3 & 0 & 1 \end{pmatrix}.
$$

ImportantThe Negative Transpose Property

The dual dictionary is the **negative transpose** of the primal dictionary. That is, if the primal tableau is a matrix $T$, then the dual tableau is $-T^\top$.

This is not a coincidence for this particular example – it holds in general and is preserved under pivoting.

### Primal–Dual Dictionary Explorer

Step through the pivots and hover any cell to verify: T\[i,j\] + (−T <sup>⊤</sup>)\[j,i\] = 0

Primal Dictionary **T**

|  |  | x₁ | x₂ | x₃ |
| --- | --- | --- | --- | --- |
| ζ | 0 | 4 | 1 | 3 |
| w₁ | 1 | −1 | −4 | 0 |
| w₂ | 3 | −3 | 1 | −1 |

\= − **T** <sup>⊤</sup>

Dual Dictionary **−T <sup>⊤</sup>**

|  |  | y₁ | y₂ |
| --- | --- | --- | --- |
| −ξ | 0 | −1 | −3 |
| z₁ | −4 | 1 | 3 |
| z₂ | −1 | 4 | −1 |
| z₃ | −3 | 0 | 1 |

Hover a cell to verify

Basic ↔ nonbasic swap: primal basis {w₁, w₂} corresponds to dual nonbasic {y₁, y₂}. Primal nonbasic {x₁, x₂, x₃} correspond to dual basic {z₁, z₂, z₃}. Hover any matching cells to verify the negative transpose!

### 12.2.2 Variable Correspondence

The negative transpose property reveals a deep symmetry between primal and dual variables:

| Decision variable $x_j$ | Slack variable $z_j$ |
| --- | --- |
| Slack variable $w_i$ ($= x_{n+i}$) | Decision variable $y_i$ ($= z_{n+i}$) |
| Basic variable | Nonbasic variable |
| Nonbasic variable | Basic variable |

In the example above, the initial primal basis is $B = \{w_1, w_2\}$ (slack variables basic), so $x_1, x_2, x_3$ are nonbasic. In the dual, this means $y_1, y_2$ are nonbasic (set to zero) and $z_1, z_2, z_3$ are basic.

### 12.2.3 Pivoting Preserves the Negative Transpose

Continuing the example, suppose we pivot in the primal dictionary with entering variable $x_3$ and leaving variable $w_2$. After the pivot:

$$
\text{(P):} \quad \zeta = 9 - 5x_1 + 4x_2 - 3w_2,
$$

$$
w_1 = 1 - x_1 - 4x_2, \qquad x_3 = 3 - 3x_1 + x_2 - w_2.
$$

The new basis is $B = \{w_1, x_3\}$ with $w_1 = 1$, $x_3 = 3$, and $x_1 = x_2 = w_2 = 0$.

The corresponding dual dictionary (after $y_2$ enters and $z_3$ leaves the dual basis) becomes:

$$
\text{(D):} \quad -\xi = -9 - y_1 - 3z_3,
$$

$$
z_1 = 5 + y_1 + 3z_3, \qquad z_2 = -4 + 4y_1 - z_3, \qquad y_2 = 3 + z_3.
$$

Write these as matrices:

$$
\text{(P):} \quad \begin{pmatrix} 9 & -5 & 4 & -3 \\ 1 & -1 & -4 & 0 \\ 3 & -3 & 1 & -1 \end{pmatrix}, \qquad
\text{(D):} \quad \begin{pmatrix} -9 & -1 & -3 \\ 5 & 1 & 3 \\ -4 & 4 & -1 \\ 3 & 0 & 1 \end{pmatrix}.
$$

The **negative transpose property still holds** after pivoting. This is a general fact: since the primal pivot and the dual pivot are the same algebraic operation (expressed in transposed form), the structural relationship is preserved at every iteration.

After a second pivot with entering $x_2$ and leaving $w_1$ in the primal:

$$
\text{(P):} \quad \zeta = 10 - 6x_1 - w_1 - 3w_2, \qquad \text{(primal optimal)}
$$

$$
x_2 = 0.25 - 0.25x_1 - 0.25w_1, \qquad x_3 = 3.25 - 3.25x_1 - 0.25w_1 - w_2.
$$

$$
\text{(D):} \quad -\xi = -10 - 0.25z_2 - 3.25z_3, \qquad \text{(dual optimal)}
$$

$$
z_1 = 6 + 0.25z_2 + 3.25z_3, \qquad y_1 = 1 + 0.25z_2 + 0.25z_3, \qquad y_2 = 3 + z_3.
$$

Both are now optimal: the primal has $\widetilde{c} \leq 0$ and $\widetilde{b} \geq 0$; the dual has $\widetilde{b}_{\text{dual}} \geq 0$ and $\widetilde{c}_{\text{dual}} \leq 0$. The optimal value is $\zeta^* = 10$ for the primal (max) and $\xi^* = 10$ for the dual (min), confirming strong duality.

The example reveals several structural patterns about how primal and dual dictionaries evolve in tandem. We now distill these into five general observations that underpin the dual simplex method.

## 12.3 Five Key Observations

The example above illustrates several fundamental facts about the primal-dual relationship through dictionaries. These observations hold in general and provide the foundation for the dual simplex method. Understanding them is essential before we derive the dual simplex pivot rules in the next section.

**Proposition 12.1 (Key Observations about Primal-Dual Pivoting)** Let (P) and (D) be a primal-dual LP pair, and consider the simplex method applied to (P). The following five properties describe how the primal and dual dictionaries evolve in lockstep:

1. **Negative transpose is preserved.** The dual dictionary is always the negative transpose of the primal dictionary, at every iteration.
2. **Basic/nonbasic sets swap.** If $x_j$ is in the primal basis $B$ (resp. nonbasic set $N$), then the corresponding dual variable $z_j$ is in the dual nonbasic set $N_D$ (resp. basis $B_D$). Similarly, if $w_i$ is in $B$ (resp. $N$), then $y_i$ is in $N_D$ (resp. $B_D$).
3. **Pivots correspond.** If $w_i / x_j$ enters/leaves the primal basis $B$, then $y_i / z_j$ leaves/enters the dual basis $B_D$. Complementary slackness is preserved.
4. **Feasibility vs. optimality swap.** During our pivots, the first two dictionaries were infeasible for the dual (some $\widetilde{b}_{\text{dual}} < 0$). But the final dictionary gives the optimal BFS for the dual.
5. **Simplex implicitly solves the dual.** We can solve (D) entirely by running simplex on (P). The simplex method for the primal LP **implicitly solves the dual LP**.

TipPrimal Feasibility $\leftrightarrow$ Dual Optimality

Observation 4 reveals a striking symmetry between the primal and dual dictionaries:

- **Primal feasible** ($\widetilde{b} \geq 0$) $\longleftrightarrow$ **Dual optimal** (all dual reduced costs $\leq 0$)
- **Primal optimal** ($\widetilde{c} \leq 0$) $\longleftrightarrow$ **Dual feasible** ($\widetilde{b}_{\text{dual}} \geq 0$)

This is precisely the content of complementary slackness and strong duality, but observed through the lens of the dictionary.

## 12.4 Derivation of the Dual Simplex Method

The five observations above suggest a powerful idea: instead of running simplex on the dual LP directly (which would require explicitly forming the dual), we can run it using the **primal dictionary**. We now make this precise by deriving the pivot rules from the negative transpose property.

### 12.4.1 The Idea

Recall the primal tableau structure for a general basis $B$:

$$
\begin{array}{c|c}
\widetilde{\zeta} & \widetilde{c}^\top \\
\hline
\widetilde{b} & -\widetilde{A}
\end{array}
\qquad \longleftrightarrow \qquad
\begin{array}{c|c}
\widetilde{\zeta} & -z_N^{*\top} \\
\hline
x_B^* & -\widetilde{A}
\end{array}
$$

where we have used the correspondence $\widetilde{c} = -z_N^*$ (the reduced costs are the negatives of the dual nonbasic variable values) and $\widetilde{b} = x_B^*$ (the transformed RHS is the primal basic variable values).

The dual dictionary, by the negative transpose property, is:

$$
\begin{array}{c|c}
-\widetilde{\zeta} & -\widetilde{b}^\top \\
\hline
-\widetilde{c} & \widetilde{A}
\end{array}
$$

Running standard simplex on the dual means:

- **Dual feasibility** requires $-\widetilde{c} \geq 0$, i.e., $\widetilde{c} \leq 0$ in the primal. This means all primal reduced costs are non-positive.
- **Dual optimality** requires $-\widetilde{b} \leq 0$, i.e., $\widetilde{b} \geq 0$ in the primal. This means the primal BFS is feasible.

So from the primal dictionary’s perspective:

- **Maintain** $\widetilde{c} \leq 0$ (dual feasibility, equivalently primal optimality condition on reduced costs).
- **Work toward** $\widetilde{b} \geq 0$ (dual optimality, equivalently primal feasibility).

### 12.4.2 Deriving the Pivot Rules

In the dual simplex method, we work directly with the primal dictionary but follow the dual’s logic.

**Choosing the leaving variable** (entering in the dual): We look for a basic variable $x_p$ with $\widetilde{b}_p < 0$. In the dual dictionary, this corresponds to a positive reduced cost ($-\widetilde{b}_p > 0$), so it is the entering variable for the dual simplex. We select:

$$
p \in \{i \in B : \widetilde{b}_i < 0\}.
$$

**Choosing the entering variable** (leaving in the dual): We need a ratio test. The row for $x_p$ in the primal dictionary is:

$$
x_p = \widetilde{b}_p - \sum_{j \in N} \widetilde{A}_{pj} \, x_j.
$$

When we increase $x_p$ away from its current value (which is $\widetilde{b}_p < 0$), we need to maintain dual feasibility. The new reduced costs after pivoting must remain non-positive. For the dual to remain feasible, we need:

$$
\widetilde{c}_j - t \cdot \widetilde{A}_{pj} \leq 0 \quad \text{for all } j \in N,
$$

where $t$ is the step size. When $\widetilde{A}_{pj} < 0$, this becomes $t \leq \frac{\widetilde{c}_j}{\widetilde{A}_{pj}}$. Since $\widetilde{c}_j \leq 0$ and $\widetilde{A}_{pj} < 0$, the ratio $\frac{\widetilde{c}_j}{\widetilde{A}_{pj}} \geq 0$. We choose the tightest bound:

$$
q = \operatorname*{argmin}_{j \in N} \left\{ \frac{-\widetilde{c}_j}{\widetilde{A}_{pj}} \;\Big|\; \widetilde{A}_{pj} < 0 \right\} = \operatorname*{argmin}_{j \in N} \left\{ \frac{|\widetilde{c}_j|}{|\widetilde{A}_{pj}|} \;\Big|\; \widetilde{A}_{pj} < 0 \right\}.
\tag{12.1}
$$

If no $\widetilde{A}_{pj} < 0$ exists, then the dual is unbounded, which means the **primal is infeasible**.

TipWorking with Dictionary Coefficients

In practice, it is easier to work directly with the **dictionary coefficients** $a_{pj}$ (the numbers appearing in the dictionary row $x_p = \widetilde{b}_p + \sum_j a_{pj}\,x_j$) rather than the $\widetilde{A}$ entries. Since $\widetilde{A}_{pj} = -a_{pj}$, the condition “ $\widetilde{A}_{pj} < 0$ ” is the same as “ $a_{pj} > 0$ ” (positive dictionary coefficient). The ratio test becomes:

$$
q = \operatorname*{argmin}_{j \in N} \left\{ \frac{|\widetilde{c}_j|}{a_{pj}} \;\Big|\; a_{pj} > 0 \right\}.
$$

**Rule of thumb:** in the leaving row, look for **positive** dictionary coefficients; compute the ratio of the corresponding **absolute reduced cost** to the coefficient; choose the smallest ratio.

## 12.5 The Dual Simplex Algorithm

We now state the primal and dual simplex algorithms side by side. Both operate on the same primal dictionary – the difference is which condition they maintain and which they achieve.

### 12.5.1 Side-by-Side Comparison

ImportantPrimal Simplex Algorithm

**Step 0 (Feasibility).** Start with a basis $B$ such that $\widetilde{b} = x_B^* \geq 0$ (primal feasible BFS).

**Step 1 (Optimality check).** If $\widetilde{c} \leq 0$, **STOP** – current BFS is optimal.

**Step 2 (Select entering variable).** Choose $q \in N$ such that $\widetilde{c}_q > 0$. (Bland’s rule: choose smallest index.)

**Step 3 (Select leaving variable).** If $\widetilde{A}_{iq} \leq 0$ for all $i \in B$, **STOP** – problem is unbounded. Otherwise:

$$
p = \operatorname*{argmin}_{i \in B} \left\{ \frac{\widetilde{b}_i}{\widetilde{A}_{iq}} \;\Big|\; \widetilde{A}_{iq} > 0 \right\}.
$$

**Step 4 (Pivot).** Pivot on $(p, q)$: $p$ leaves $B$, $q$ enters $B$. Go to Step 1.

ImportantDual Simplex Algorithm

**Step 0 (Feasibility).** Start with a basis $B$ such that $\widetilde{c} \leq 0$ (dual feasible, i.e., $z_N^* \geq 0$).

**Step 1 (Optimality check).** If $\widetilde{b} \geq 0$, **STOP** – current basis is both primal and dual feasible, hence optimal.

**Step 2 (Select leaving variable).** Choose $p \in B$ such that $\widetilde{b}_p < 0$. (Choose most negative, or smallest index for Bland’s rule.)

**Step 3 (Select entering variable).** If $\widetilde{A}_{pj} \geq 0$ for all $j \in N$, **STOP** – dual is unbounded, **primal is infeasible**. Otherwise:

$$
q = \operatorname*{argmin}_{j \in N} \left\{ \frac{-\widetilde{c}_j}{\widetilde{A}_{pj}} \;\Big|\; \widetilde{A}_{pj} < 0 \right\}.
$$

**Step 4 (Pivot).** Pivot on $(p, q)$: $p$ leaves $B$, $q$ enters $B$. Go to Step 1.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/primal-vs-dual-simplex.svg)

Figure 12.1: Comparison of primal and dual simplex: the primal simplex (left) moves through primal feasible bases toward dual feasibility, while the dual simplex (right) moves through dual feasible bases toward primal feasibility. Both converge to the same optimal solution.

### 12.5.2 Structural Comparison

The following table summarizes the structural differences between primal and dual simplex.

NotePrimal vs. Dual Simplex at a Glance

| **Maintains** | Primal feasibility: $\widetilde{b} \geq 0$ | Dual feasibility: $\widetilde{c} \leq 0$ |
| --- | --- | --- |
| **Achieves** | Dual feasibility: $\widetilde{c} \leq 0$ | Primal feasibility: $\widetilde{b} \geq 0$ |
| **Optimality** | $\widetilde{c} \leq 0$ | $\widetilde{b} \geq 0$ |
| **Choose first** | Entering $q$ (positive reduced cost) | Leaving $p$ (negative $\widetilde{b}_p$) |
| **Choose second** | Leaving $p$ (min ratio on $\widetilde{b}/\widetilde{A}$) | Entering $q$ (min ratio on $\widetilde{c}/\widetilde{A}$) |
| **Unbounded detection** | No positive $\widetilde{A}_{iq}$ in column | No negative $\widetilde{A}_{pj}$ in row |
| **Unbounded means** | Primal unbounded | Dual unbounded (primal infeasible) |
| **Objective movement** | Increases (for max) | Decreases (for max) |

TipIntuition

**Primal simplex** moves through primal feasible vertices, improving the objective until dual feasibility is achieved.

**Dual simplex** moves through dual feasible bases (which may correspond to primal infeasible points), **decreasing** the objective until primal feasibility is achieved. The objective starts too good (super-optimal) and comes down to the true optimum.

With the algorithm stated precisely, we now trace through a complete numerical example to see each step in action.

## 12.6 Worked Example

Having derived the dual simplex pivot rules, including the ratio test ([Equation 12.1](https://zhuoranyang.github.io/sds431-notes/lectures/12-dual-simplex.html#eq-dual-simplex-ratio)), we now demonstrate the method on a complete example.

### 12.6.1 Problem Setup

Consider the LP:

$$
\min \; x_1 + 3x_2 \quad \text{s.t.} \quad x_1 + 3x_2 \geq 4, \;\; 4x_1 - x_2 \geq 1, \;\; x_2 \geq 3.
$$

To apply the simplex framework, convert to maximization and $\leq$ constraints:

$$
\max \; -x_1 - 3x_2 \quad \text{s.t.} \quad -x_1 - 3x_2 \leq -4, \;\; -4x_1 + x_2 \leq -1, \;\; -x_2 \leq -3.
$$

Introduce slack variables $x_3, x_4, x_5 \geq 0$:

$$
x_3 = x_1 + 3x_2 - 4, \qquad x_4 = 4x_1 - x_2 - 1, \qquad x_5 = x_2 - 3.
$$

The initial dictionary is:

$$
\zeta = -x_1 - 3x_2,
$$

$$
x_3 = -4 + x_1 + 3x_2, \qquad x_4 = -1 + 4x_1 - x_2, \qquad x_5 = -3 + x_2.
$$

The initial tableau is:

$$
\begin{array}{c|rr}
& x_1 & x_2 \\
\hline
\zeta = 0 & -1 & -3 \\
x_3 = -4 & 1 & 3 \\
x_4 = -1 & 4 & -1 \\
x_5 = -3 & 0 & 1
\end{array}
$$

### 12.6.2 Checking Initial Conditions

- **Reduced costs:** $\widetilde{c}_1 = -1 \leq 0$ and $\widetilde{c}_2 = -3 \leq 0$. So $\widetilde{c} \leq 0$: **dual feasibility holds**.
- **RHS values:** $\widetilde{b}_3 = -4 < 0$, $\widetilde{b}_4 = -1 < 0$, $\widetilde{b}_5 = -3 < 0$. So $\widetilde{b} \not\geq 0$: **primal feasibility fails**.

This is exactly the setup for dual simplex: we have dual feasibility but not primal feasibility.

### 12.6.3 Iteration 1

**Step 1:** $\widetilde{b} \not\geq 0$, so we are not optimal. Continue.

**Step 2 (Choose leaving $p$):** We need a basic variable with $\widetilde{b}_p < 0$. All three are negative: $\widetilde{b}_3 = -4$, $\widetilde{b}_4 = -1$, $\widetilde{b}_5 = -3$. We choose $p = x_5$.

TipSign Convention for the Ratio Test

Before applying the ratio test, let us clarify the sign convention. The dictionary row for a basic variable $x_p$ is written as:

$$
x_p = \widetilde{b}_p + a_{p1}\,x_1 + a_{p2}\,x_2 + \cdots
$$

where $a_{pj}$ are the **dictionary coefficients** (the numbers that appear directly in the equation). In the tableau notation, the $-\widetilde{A}$ block stores these same coefficients with a sign flip: $(-\widetilde{A})_{pj} = a_{pj}$, so $\widetilde{A}_{pj} = -a_{pj}$.

The dual simplex ratio test ([Equation 12.1](https://zhuoranyang.github.io/sds431-notes/lectures/12-dual-simplex.html#eq-dual-simplex-ratio)) requires $\widetilde{A}_{pj} < 0$, which means we look for dictionary coefficients $a_{pj} > 0$ (positive entries in the dictionary row). The ratio is then:

$$
q = \operatorname*{argmin}_{j:\, a_{pj} > 0} \frac{|\widetilde{c}_j|}{a_{pj}}.
$$

**Step 3 (Choose entering $q$):** The dictionary row for $x_5$ is:

$$
x_5 = -3 + 0 \cdot x_1 + 1 \cdot x_2.
$$

The dictionary coefficient of $x_1$ is $0$ (does not qualify) and the dictionary coefficient of $x_2$ is $+1$ (positive, so it qualifies). Since only $x_2$ qualifies:

$$
q = x_2, \qquad \text{ratio} = \frac{|\widetilde{c}_2|}{a_{5,2}} = \frac{|-3|}{1} = 3.
$$

**Step 4: Pivot $(x_5, x_2)$.** Solve for $x_2$ from the $x_5$ row:

$$
x_5 = -3 + x_2 \implies x_2 = 3 + x_5.
$$

Substitute into all other rows:

$$
\zeta = -(x_1) - 3(3 + x_5) = -9 - x_1 - 3x_5,
$$

$$
x_3 = -4 + x_1 + 3(3 + x_5) = 5 + x_1 + 3x_5,
$$

$$
x_4 = -1 + 4x_1 - (3 + x_5) = -4 + 4x_1 - x_5.
$$

The new dictionary after Iteration 1:

$$
\zeta = -9 - x_1 - 3x_5,
$$

$$
x_3 = 5 + x_1 + 3x_5, \qquad x_4 = -4 + 4x_1 - x_5, \qquad x_2 = 3 + x_5.
$$

New tableau:

$$
\begin{array}{c|rr}
& x_1 & x_5 \\
\hline
-9 & -1 & -3 \\
5 & 1 & 3 \\
-4 & 4 & -1 \\
3 & 0 & 1
\end{array}
$$

**Check:** $\widetilde{c}_1 = -1 \leq 0$, $\widetilde{c}_5 = -3 \leq 0$: dual feasibility is maintained. But $\widetilde{b}_4 = -4 < 0$: not yet primal feasible.

### 12.6.4 Iteration 2

**Step 1:** $\widetilde{b} \not\geq 0$ (since $\widetilde{b}_4 = -4$). Continue.

**Step 2 (Choose leaving $p$):** The only negative $\widetilde{b}$ is $\widetilde{b}_4 = -4$, so $p = x_4$.

**Step 3 (Choose entering $q$):** The dictionary row for $x_4$ is:

$$
x_4 = -4 + 4x_1 - 1 \cdot x_5.
$$

The dictionary coefficient of $x_1$ is $+4 > 0$ (qualifies) and the dictionary coefficient of $x_5$ is $-1 < 0$ (does not qualify). Only $x_1$ qualifies:

$$
q = x_1, \qquad \text{ratio} = \frac{|\widetilde{c}_1|}{a_{4,1}} = \frac{|-1|}{4} = 0.25.
$$

**Step 4: Pivot $(x_4, x_1)$.** Solve for $x_1$ from the $x_4$ row:

$$
x_4 = -4 + 4x_1 - x_5 \implies x_1 = 1 + 0.25 x_4 + 0.25 x_5.
$$

Substitute:

$$
\zeta = -9 - (1 + 0.25x_4 + 0.25x_5) - 3x_5 = -10 - 0.25x_4 - 3.25x_5,
$$

$$
x_3 = 5 + (1 + 0.25x_4 + 0.25x_5) + 3x_5 = 6 + 0.25x_4 + 3.25x_5,
$$

$$
x_2 = 3 + x_5.
$$

Final dictionary:

$$
\zeta = -10 - 0.25 x_4 - 3.25 x_5,
$$

$$
x_3 = 6 + 0.25 x_4 + 3.25 x_5, \qquad x_1 = 1 + 0.25 x_4 + 0.25 x_5, \qquad x_2 = 3 + x_5.
$$

Final tableau:

$$
\begin{array}{c|rr}
& x_4 & x_5 \\
\hline
-10 & -0.25 & -3.25 \\
6 & 0.25 & 3.25 \\
1 & 0.25 & 0.25 \\
3 & 0 & 1
\end{array}
$$

### 12.6.5 Verifying Optimality

- **Reduced costs:** $\widetilde{c}_4 = -0.25 \leq 0$, $\widetilde{c}_5 = -3.25 \leq 0$. Dual feasibility maintained.
- **RHS values:** $\widetilde{b}_3 = 6 \geq 0$, $\widetilde{b}_1 = 1 \geq 0$, $\widetilde{b}_2 = 3 \geq 0$. **Primal feasibility achieved!**

Both conditions hold, so we have reached optimality. The optimal solution is:

$$
x_1^* = 1, \quad x_2^* = 3, \quad \zeta^* = -10.
$$

Since the original problem was $\min \, x_1 + 3x_2$, the minimum value is $\boxed{10}$, achieved at $(x_1, x_2) = (1, 3)$. The dual simplex method reached optimality in just two pivots, maintaining dual feasibility throughout and restoring primal feasibility at termination.

### Dual Simplex Iteration Visualizer

The dual simplex starts at a super-optimal (infeasible) point and pivots toward the feasible region

Iteration 0

Terracotta = infeasible  |  Green = feasible  |  Dashed gold = optimal contour x₁+3x₂ = 10

**Point:** (x₁, x₂) = (0, 0)  →  **Objective:** x₁ + 3x₂ = 0 (super-optimal)

**Basis:** B = {x₃, x₄, x₅}

**RHS values:** b̃ = \[−4, −1, −3\] — all negative

**Reduced costs:** c̃ = \[−1, −3\] ≤ 0 ✓ (dual feasible)

✗ Primal infeasible — all b̃ᵢ < 0

**Action:** Choose leaving: p = x₅ (b̃₅ = −3 < 0). Row of x₅: coefficients \[0, 1\]. Only x₂ has positive coefficient → q = x₂ enters.

## 12.7 When to Use the Dual Simplex Method

The dual simplex method is not just a theoretical mirror of the primal simplex. It arises naturally in several important practical situations.

### 12.7.1 Adding a New Constraint

Suppose you have already solved an LP to optimality and now need to add a new constraint. The current optimal basis satisfies $\widetilde{c} \leq 0$ (optimality / dual feasibility), but the new constraint may violate primal feasibility ($\widetilde{b} \not\geq 0$ for the new row). This is exactly the setting for dual simplex: maintain dual feasibility, pivot to restore primal feasibility.

This situation arises constantly in:

- **Branch-and-bound** for integer programming: each node adds a branching constraint ($x_i \leq k$ or $x_i \geq k+1$) to the parent LP.
- **Cutting-plane methods**: violated inequalities are added iteratively, and the LP must be re-optimized after each cut.
- **Sensitivity analysis**: when the right-hand side $b$ changes, the current basis may lose primal feasibility but retain dual feasibility.

### 12.7.2 Natural Dual Feasibility

Some LPs arise with a natural initial basis that is dual feasible but not primal feasible. The worked example above is typical: when all constraints are of the $\geq$ type (converted to $\leq$ by multiplying by $-1$), the initial slack basis often has $\widetilde{c} \leq 0$ but $\widetilde{b} < 0$.

### 12.7.3 Warm-Starting After Constraint Changes

When solving a sequence of related LPs (as in column generation or Benders decomposition), the dual simplex method allows efficient **warm-starting**: the previous optimal basis provides dual feasibility, and only a few pivots may be needed to restore primal feasibility after the problem is modified.

NoteSummary

| Natural starting BFS available | Yes | – |
| --- | --- | --- |
| $\widetilde{c} \leq 0$ but $\widetilde{b} \not\geq 0$ | – | Yes |
| Adding constraints to optimal LP | – | Yes |
| Branch-and-bound / cutting planes | – | Yes |
| RHS perturbation / sensitivity | – | Yes |
| Objective change | Yes | – |

## 12.8 Summary of the Primal-Dual Framework

TipThe Big Picture

The two simplex variants are mirror images of each other, differing only in which feasibility condition is maintained as an invariant and which is achieved through pivoting:

**Primal simplex** maintains primal feasibility and drives toward dual feasibility:

- $x_B^*$ is primal feasible ($\widetilde{b} \geq 0$) at every iteration
- $z_N^*$ eventually becomes dual feasible ($\widetilde{c} \leq 0$) through pivots
- Complementary slackness is preserved at every step

**Dual simplex** maintains dual feasibility and drives toward primal feasibility:

- $z_N^*$ is dual feasible ($\widetilde{c} \leq 0$) at every iteration
- $x_B^*$ eventually becomes primal feasible ($\widetilde{b} \geq 0$) through pivots
- Complementary slackness is preserved at every step

Both methods terminate at the same optimal solution, where **both** primal and dual feasibility hold simultaneously. This is the algebraic expression of [strong duality](https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html). The complementary slackness conditions are maintained as an invariant throughout both algorithms.

TipLooking Ahead

The dual simplex method, combined with the primal simplex, gives us a complete toolkit for solving linear programs and re-optimizing after modifications. These tools are the backbone of modern LP solvers and form the computational engine behind integer programming, robust optimization, and large-scale decomposition methods.