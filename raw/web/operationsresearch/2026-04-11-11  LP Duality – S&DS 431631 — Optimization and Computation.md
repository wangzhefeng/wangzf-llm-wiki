---
author: null
created: 2026-04-11
description: null
published: null
source: https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html
tags:
- clippings
title: 11  LP Duality – S&DS 431/631 — Optimization and Computation
topics:
- 运筹优化
---
The [simplex method](https://zhuoranyang.github.io/sds431-notes/lectures/10-simplex-method.html) finds an optimal solution by moving from vertex to vertex. But suppose the algorithm hands you a solution $x^*$ and claims it is optimal. **How do you know it is truly the best?** Simply checking feasibility is not enough — you need a *certificate* that no feasible point can do better.

Duality theory provides exactly this certificate. The core idea: for every LP (the **primal**), there is a companion LP (the **dual**) whose feasible solutions provide **upper bounds** on the primal’s optimal value. When a primal feasible value matches a dual feasible value, the gap is zero and both must be optimal. This simple idea — bounding from both sides — leads to one of the deepest and most useful frameworks in optimization.

## What Will Be Covered

- Motivation: certificates of optimality via upper bounds on the objective
- Constructing the dual LP from primal constraints
- Weak duality: dual feasible solutions bound the primal optimal value
- Strong duality: the primal and dual optimal values coincide
- Complementary slackness and its role in certifying optimality
- Economic interpretation of dual variables as shadow prices

## 11.1 Motivation for Duality

Consider a maximization LP (duality is most naturally stated in this form):

$$
\max_{x \in \mathbb{R}^n} \; c^\top x \quad \text{s.t.} \quad Ax \leq b, \quad x \geq 0.
$$

Let $\Omega = \{x \in \mathbb{R}^n \mid Ax \leq b, \; x \geq 0\}$ be the feasible set and $f^* = \max_{x \in \Omega} c^\top x$ the optimal value.

Suppose someone hands you a feasible point $x_0 \in \Omega$ and claims it is optimal. **How do you verify this?**

- **Lower bound (easy):** Since $x_0$ is feasible, $f_0 = c^\top x_0 \leq f^*$. Any feasible point gives a lower bound on $f^*$.
- **Upper bound (hard):** To prove $f_0 = f^*$, we need to show that *no* feasible point can do better, i.e., $f^* \leq f_0$. This requires an **upper bound** on $c^\top x$ that holds for *every* $x \in \Omega$.

ImportantThe Central Question

Can we systematically produce upper bounds on $c^\top x$ over all feasible $x \in \Omega$, using only the constraint data $(A, b)$? If we can find such an upper bound that equals our candidate value $f_0$, then $f_0 = f^*$ and $x_0$ is certified optimal.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/duality-gap.svg)

Figure 11.1: The duality gap between a lower bound (primal feasible value) and an upper bound (dual feasible value). When the gap closes, we have certified optimality.

## 11.2 Deriving the Dual LP

We now answer the central question by systematically constructing upper bounds on the primal objective. Starting from the primal:

$$
\text{(Primal)} \quad \max_{x \in \mathbb{R}^n} \; c^\top x \quad \text{s.t.} \quad Ax \leq b, \quad x \geq 0,
$$

where $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$, and $c \in \mathbb{R}^n$. Write the constraints row-by-row as $a_i^\top x \leq b_i$ for $i \in [m]$.

### 11.2.1 The Multiplier Idea

The derivation follows three simple steps: **multiply**, **sum**, and **dominate**.

**Step 1: Multiply.** For each constraint $a_i^\top x \leq b_i$, introduce a **multiplier** $y_i \geq 0$. Multiplying both sides by $y_i$ preserves the inequality direction (since $y_i \geq 0$):

$$
y_i \cdot a_i^\top x \leq y_i \cdot b_i \quad \forall\, i \in [m].
$$

**Step 2: Sum.** Add all $m$ weighted inequalities:

$$
\sum_{i=1}^{m} y_i \, a_i^\top x \leq \sum_{i=1}^{m} y_i \, b_i, \qquad \text{i.e.,} \quad (A^\top y)^\top x \leq b^\top y.
$$

The left side is a *new* linear function of $x$; the right side is a constant (depending only on $y$).

**Step 3: Dominate.** If the combined left side *dominates* the objective — meaning $A^\top y \geq c$ component-wise — then for any feasible $x \geq 0$:

$$
c^\top x \;\leq\; (A^\top y)^\top x \;\leq\; b^\top y.
$$

The first “ $\leq$ ” uses $A^\top y \geq c$ and $x \geq 0$; the second uses the summed constraint from Step 2. We have produced an **upper bound** $b^\top y$ on $c^\top x$ that holds for *every* feasible $x$.

### 11.2.2 The Dual LP

To find the **tightest upper bound**, we minimize $b^\top y$ over all valid multipliers:

$$
\text{(Dual)} \quad \min_{y \in \mathbb{R}^m} \; b^\top y \quad \text{s.t.} \quad A^\top y \geq c, \quad y \geq 0.
$$

Side by side:

| $\max \; c^\top x$ | $\min \; b^\top y$ |
| --- | --- |
| s.t. $Ax \leq b$ | s.t. $A^\top y \geq c$ |
| $x \geq 0$ | $y \geq 0$ |

Notice the elegant symmetry: the primal has $n$ variables and $m$ constraints; the dual has $m$ variables and $n$ constraints. The data $(A, b, c)$ is shared — only the roles are swapped. The constraint matrix $A$ becomes $A^\top$, the objective $c$ becomes the right-hand side, and the right-hand side $b$ becomes the objective.

The derivation above assumed the primal has only “ $\leq$ ” constraints and nonnegative variables. In practice, LPs may contain equality constraints, “ $\geq$ ” constraints, or free variables. The next section extends the correspondence to handle all cases.

## 11.3 General Primal-Dual Correspondence

The dual we derived assumed the primal has only “ $\leq$ ” constraints and nonneg variables. Real LPs may have equality constraints, “ $\geq$ ” constraints, or free variables. The same multiply-sum-dominate logic extends to all cases — the key is tracking how each constraint and variable type affects the signs.

### 11.3.1 General Primal Form

Consider a general primal LP (maximization) with:

- $n$ decision variables $x_1, x_2, \ldots, x_n$
- Sign constraints on each $x_j$: either $x_j \geq 0$, $x_j \leq 0$, or $x_j \in \mathbb{R}$ (free)
- $m$ linear constraints $a_i^\top x \; \square \; b_i$ where $\square$ is $\leq$, $=$, or $\geq$
- Objective: $\max \; c^\top x$

### 11.3.2 Deriving the Dual

We apply the same recipe, but must handle each case:

**Multiplier signs (from constraint types).** For each constraint $i$, the multiplier $y_i$ must have the right sign so that multiplying preserves a valid upper bound:

- $a_i^\top x \leq b_i$: need $y_i \geq 0$ (multiplying by a nonneg number preserves “ $\leq$ ”)
- $a_i^\top x \geq b_i$: need $y_i \leq 0$ (multiplying by a nonpositive number flips “ $\geq$ ” to “ $\leq$ ”)
- $a_i^\top x = b_i$: $y_i$ is **free** (both sides are equal, so any sign works)

After summing all weighted constraints, we get $(A^\top y)^\top x \leq b^\top y$ for all feasible $x$.

**Dual constraint types (from variable signs).** We need the combined left side to dominate the objective: $(A^\top y)_j x_j \geq c_j x_j$ for all feasible $x_j$. The sign constraint on $x_j$ determines what this requires:

- $x_j \geq 0$ (can be positive): need $(A^\top y)_j \geq c_j$, so that $(A^\top y)_j x_j \geq c_j x_j$
- $x_j \leq 0$ (can be negative): need $(A^\top y)_j \leq c_j$, so the inequality flips correctly
- $x_j$ free (can be anything): need $(A^\top y)_j = c_j$ exactly (otherwise we could violate domination by choosing $x_j$ with the wrong sign)

The dual LP is: $\min\, b^\top y$ subject to these $n$ constraints and the sign constraints on $y_i$.

### 11.3.3 Correspondence Table

Table 11.1: Primal-dual correspondence rules. Each row shows how a primal element maps to a dual element.

| Constraint $a_i^\top x \leq b_i$ | Variable $y_i \geq 0$ |
| --- | --- |
| Constraint $a_i^\top x \geq b_i$ | Variable $y_i \leq 0$ |
| Constraint $a_i^\top x = b_i$ | Variable $y_i$ free |
| Variable $x_j \geq 0$ | Constraint $\sum_i y_i a_{ij} \geq c_j$ |
| Variable $x_j \leq 0$ | Constraint $\sum_i y_i a_{ij} \leq c_j$ |
| Variable $x_j$ free | Constraint $\sum_i y_i a_{ij} = c_j$ |

TipMnemonic

There is a beautiful symmetry: **constraint type** in the primal maps to **variable sign** in the dual, and **variable sign** in the primal maps to **constraint type** in the dual. The direction of the inequality always “matches” the sign constraint in a consistent way.

### 11.3.4 Common Special Cases (Vector Formulations)

| $\max \; c^\top x$ s.t. $Ax \leq b$, $x \geq 0$ | $\min \; b^\top y$ s.t. $A^\top y \geq c$, $y \geq 0$ |
| --- | --- |
| $\max \; c^\top x$ s.t. $Ax \leq b$, $x \in \mathbb{R}^n$ | $\min \; b^\top y$ s.t. $A^\top y = c$, $y \geq 0$ |
| $\max \; c^\top x$ s.t. $Ax = b$, $x \geq 0$ | $\min \; b^\top y$ s.t. $A^\top y \geq c$, $y \in \mathbb{R}^m$ |

### 11.3.5 Dual of the Dual = Primal

A natural question: if we take the dual of the dual, do we recover the original primal? The answer is yes, confirming that duality is a **symmetric** relationship.

**Theorem 11.1 (Dual of the Dual is the Primal)** The dual of the dual LP is the primal LP.

*Proof*. The strategy is to rewrite the dual as a maximization problem, apply the primal-to-dual recipe, and simplify to recover the original primal.

Consider the dual problem:

$$
\min \; b^\top y \quad \text{s.t.} \quad A^\top y \geq c, \quad y \geq 0.
$$

This is equivalent to:

$$
-\max \; (-b^\top y) \quad \text{s.t.} \quad -A^\top y \leq -c, \quad y \geq 0.
$$

Now we can take its dual using the primal form with data:

$$
c \leftarrow -b, \quad A \leftarrow -A^\top, \quad b \leftarrow -c.
$$

The dual of this maximization problem is:

$$
\min \; (-c)^\top z \quad \text{s.t.} \quad (-A^\top)^\top z \geq -b, \quad z \geq 0,
$$

which simplifies to:

$$
-\min \; (-c^\top z) \quad \text{s.t.} \quad -Az \geq -b, \quad z \geq 0,
$$

i.e.,

$$
\max \; c^\top z \quad \text{s.t.} \quad Az \leq b, \quad z \geq 0.
$$

This is exactly the primal! $\blacksquare$

Since the dual of the dual is the primal, there is no preferred “direction” — we can always choose which LP to call primal and which to call dual.

With the dual LP defined and duality shown to be symmetric, we turn to the fundamental question: **what is the quantitative relationship between the primal and dual optimal values?** The answer comes in two stages — weak duality (an inequality that always holds) and strong duality (equality at optimality).

## 11.4 Weak Duality

We now formalize the bounding relationship between the primal and dual. Let $\Omega_P = \{x : Ax \leq b, \; x \geq 0\}$ denote the primal feasible set and $\Omega_D = \{y : A^\top y \geq c, \; y \geq 0\}$ denote the dual feasible set.

**Theorem 11.2 (Weak Duality)** If $x$ is feasible for the primal and $y$ is feasible for the dual, then

$$
c^\top x \leq b^\top y.
\tag{11.1}
$$

In other words,

$$
\max_{x \in \Omega_P} c^\top x \;\leq\; \min_{y \in \Omega_D} b^\top y.
$$

*Proof*. The strategy is to chain two inequalities: first use primal feasibility ($Ax \leq b$) to bound $b^\top y$ from below by $x^\top A^\top y$, then use dual feasibility ($A^\top y \geq c$) to bound $x^\top A^\top y$ from below by $c^\top x$.

Since $x, y$ are feasible for the primal and dual respectively, we have:

$$
b^\top y = (b - Ax)^\top y + (Ax)^\top y.
$$

Now:

- $b - Ax \geq 0$ (since $Ax \leq b$) and $y \geq 0$, so $(b - Ax)^\top y \geq 0$.
- Therefore $b^\top y \geq (Ax)^\top y = x^\top A^\top y$.

Next:

- $A^\top y \geq c$ (dual feasibility) and $x \geq 0$, so $x^\top A^\top y \geq x^\top c = c^\top x$.

Chaining together:

$$
b^\top y \geq x^\top A^\top y \geq c^\top x. \qquad \blacksquare
$$

### 11.4.1 The Duality Gap

**Definition 11.1 (Duality Gap)** For any primal feasible $x$ and dual feasible $y$, the **duality gap** is

$$
\text{Gap}(x, y) = b^\top y - c^\top x.
\tag{11.2}
$$

By weak duality ([Equation 11.1](https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html#eq-weak-duality)), $\text{Gap}(x, y) \geq 0$ for all $(x, y) \in \Omega_P \times \Omega_D$.

NoteConsequences of Weak Duality

Weak duality immediately yields four important structural consequences for the primal-dual pair:

1. If we find primal feasible $x$ and dual feasible $y$ with $c^\top x = b^\top y$, then $x$ is primal optimal and $y$ is dual optimal.
2. If the primal is unbounded (objective $\to +\infty$), the dual must be **infeasible** (otherwise weak duality would give a finite upper bound).
3. If the dual is unbounded (objective $\to -\infty$), the primal must be **infeasible**.
4. The primal and dual **cannot both be unbounded** (this would violate weak duality).

Together, these consequences show that feasible dual solutions serve as certificates of optimality, and that unboundedness in one problem forces infeasibility in the other.

The following interactive figure lets you explore weak duality concretely on the LP from [Section 12.6](https://zhuoranyang.github.io/sds431-notes/lectures/12-dual-simplex.html#sec-worked-example).

**Setup.** The primal is $\max\, 3x_1 + 5x_2$ subject to $x_1 \leq 4$, $x_2 \leq 6$, $3x_1 + 2x_2 \leq 18$, $x_1, x_2 \geq 0$, with optimal value $f^* = 36$. Its dual is $\min\, 4y_1 + 6y_2 + 18y_3$ subject to $y_1 + 3y_3 \geq 3$, $y_2 + 2y_3 \geq 5$, $y \geq 0$.

**How it works.** Drag the slider to choose $y_3$. The figure automatically sets $y_1$ and $y_2$ to the tightest dual-feasible values (i.e., $y_1 = \max(0, 3 - 3y_3)$ and $y_2 = \max(0, 5 - 2y_3)$), then computes the dual bound $g(y) = 4y_1 + 6y_2 + 18y_3$.

**What to observe:**

- **Left panel:** The green region is the primal feasible set. The dashed gold line is the optimal contour $3x_1 + 5x_2 = 36$. The solid blue line is the contour at the current dual bound $g(y)$. By weak duality, this blue line must lie *above* the gold line (a higher contour value). When $y_3 = 1$, the two lines merge — the dual bound exactly matches $f^* = 36$.
- **Right panel:** The dual bound $g(y)$ as a function of $y_3$. It is piecewise-linear and achieves its minimum at $y_3^* = 1$, where $g^* = 36 = f^*$. For any other $y_3$, the bound is strictly larger — confirming that the gap is positive away from the dual optimum.

### LP Duality Explorer

Primal: max 3x <sub>1</sub> + 5x <sub>2</sub>   s.t.   x <sub>1</sub> ≤ 4,   x <sub>2</sub> ≤ 6,   3x <sub>1</sub> +2x <sub>2</sub> ≤ 18  |  Dual: min 4y <sub>1</sub> + 6y <sub>2</sub> + 18y <sub>3</sub>   s.t.   y <sub>1</sub> +3y <sub>3</sub> ≥ 3,   y <sub>2</sub> +2y <sub>3</sub> ≥ 5,   y ≥ 0

1.00

**Strong duality!**   f\* = g\* = 36   (zero duality gap)  
y = (0.00, 3.00, 1.00)   (tightest dual feasible for this y <sub>3</sub>)

### 11.4.2 Primal-Dual Possibilities

The Fundamental Theorem of LP says every LP is either infeasible, unbounded, or has a finite optimum. For a primal-dual pair, weak duality further constrains the combinations. Since “both unbounded” would violate [Equation 11.1](https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html#eq-weak-duality) (consequence 4 above), exactly **four possibilities** remain:

| 1. | Infeasible | Infeasible |
| --- | --- | --- |
| 2. | Infeasible | Unbounded ($\inf = -\infty$) |
| 3. | Unbounded ($\sup = +\infty$) | Infeasible |
| 4. | **Finite optimum $f^*$** | **Finite optimum $g^* = f^*$** |

Case 4 asserts something stronger than weak duality alone: not just that a bound exists, but that the bound is **tight**. This is the content of strong duality, which we prove next.

## 11.5 Strong Duality

Weak duality ([Equation 11.1](https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html#eq-weak-duality)) gives an inequality. The remarkable **strong duality theorem** says that at optimality, the gap vanishes.

**Theorem 11.3 (Strong Duality)** If one of (P) and (D) has a finite optimal value (and hence an optimal solution), so does the other. Moreover,

$$
\max_{x \in \Omega_P} c^\top x \;=\; \min_{y \in \Omega_D} b^\top y.
\tag{11.3}
$$

That is, the duality gap is zero at optimality.

### 11.5.1 Proof via the Simplex Method

The proof is constructive: we run the simplex method on the primal and extract a dual feasible solution directly from the final tableau, then show it achieves the same objective value.

*Proof*. **Proof of Strong Duality.**

Suppose the primal $\max\, c^\top x$ s.t. $Ax \leq b$, $x \geq 0$ has a finite optimal value $f^*$. Adding slack variables $w = b - Ax \geq 0$, the equational form is

$$
\max \; c^\top x \quad \text{s.t.} \quad \begin{pmatrix} A & I \end{pmatrix} \begin{pmatrix} x \\ w \end{pmatrix} = b, \quad x \geq 0, \quad w \geq 0.
$$

This LP has $n + m$ variables and $m$ equality constraints. The augmented cost vector is $(c^\top, 0^\top)^\top$ (original variables carry cost $c_j$; slack variables carry cost $0$).

Run the [simplex method](https://zhuoranyang.github.io/sds431-notes/lectures/10-simplex-method.html) on this LP to obtain an optimal BFS with basis $B$. Let $\mathbf{A}_B$ denote the $m \times m$ submatrix of $(A \mid I)$ formed by the basic columns, and let $c_B$ denote the corresponding cost coefficients.

**Step 1: Define the candidate dual solution.**

$$
y^* \;=\; (\mathbf{A}_B^{-1})^\top c_B \;\in\; \mathbb{R}^m.
$$

This is the **simplex multiplier** vector — the same object that appears implicitly in the reduced cost formulas of the simplex method.

**Step 2: Show $y^*$ is dual feasible.**

At the optimal BFS of a maximization LP, every nonbasic variable has a **nonpositive** reduced cost (otherwise we could improve the objective by bringing it into the basis). We check two types of variables:

- *Original variable $x_j$:* Its column in $(A \mid I)$ is $a_j$ (the $j$ -th column of $A$). Its reduced cost is

$$
\bar{c}_j = c_j - c_B^\top \mathbf{A}_B^{-1} a_j = c_j - (y^*)^\top a_j \;\leq\; 0,
$$

which gives $(A^\top y^*)_j \geq c_j$. Since this holds for every $j \in [n]$, we have $A^\top y^* \geq c$. (If $x_j$ is basic, its reduced cost is zero by definition, so the inequality still holds.)

- *Slack variable $w_i$:* Its column in $(A \mid I)$ is $e_i$ (the $i$ -th standard basis vector). Its reduced cost is

$$
\bar{c}_{n+i} = 0 - c_B^\top \mathbf{A}_B^{-1} e_i = -y_i^* \;\leq\; 0,
$$

which gives $y_i^* \geq 0$. Therefore $y^* \geq 0$.

Combining: $y^*$ satisfies $A^\top y^* \geq c$ and $y^* \geq 0$, so it is **dual feasible**.

**Step 3: Show the objectives match.**

At the optimal BFS, all nonbasic variables are zero, so

$$
f^* = c^\top x^* = c_B^\top x_B^* = c_B^\top \mathbf{A}_B^{-1} b = (y^*)^\top b = b^\top y^*.
$$

**Conclusion.** We have constructed $y^*$ that is dual feasible with $b^\top y^* = f^*$. By weak duality, $b^\top y^* \geq \min_{y \in \Omega_D} b^\top y \geq f^*$. Since $b^\top y^* = f^*$, all inequalities are equalities: $y^*$ is dual optimal and the duality gap is zero. $\blacksquare$

NoteKey Insight

The simplex method simultaneously solves both the primal and the dual! The optimal dual variables are the **simplex multipliers** $y^* = (\mathbf{A}_B^{-1})^\top c_B$, and each $y_i^*$ equals the **negative of the reduced cost** of the $i$ -th slack variable $w_i$. You never need to solve the dual LP separately — it comes for free from the primal simplex tableau.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/lp-duality-relationships.svg)

Figure 11.2: Relationships between primal and dual linear programs: weak duality provides a bound, strong duality gives equality at optimality, and complementary slackness links the solutions.

[Figure 11.2](https://zhuoranyang.github.io/sds431-notes/lectures/11-lp-duality.html#fig-lp-duality-relationships) summarizes the three pillars of LP duality: **weak duality** (the dual always bounds the primal), **strong duality** (the bounds meet at optimality), and **complementary slackness** (which links the structure of optimal solutions). The number line at the bottom illustrates the duality gap shrinking to zero at the optimal pair $(x^*, y^*)$.

The algebraic proof is constructive: the simplex method produces dual variables for free. But is there a more intuitive, geometric understanding of *why* duality works?

## 11.6 Geometric Interpretation

The algebraic derivation tells us *what* the dual is. A geometric picture reveals *why* it works.

### 11.6.1 Shooting a Ray Through the Polytope

Consider the feasible polytope $P = \{x \in \mathbb{R}^n : Ax \leq b, \; x \geq 0\}$ with the origin inside (which holds whenever $b \geq 0$). Imagine standing at the origin and firing a ray in the direction of an objective vector $c$:

$$
x(\alpha) = \alpha \cdot c, \qquad \alpha \geq 0.
$$

**How far can the ray travel before exiting the polytope?** Each constraint $a_i^\top x \leq b_i$ acts as a wall. Along the ray:

$$
a_i^\top (\alpha c) = \alpha \, (a_i^\top c) \leq b_i \quad \Longleftrightarrow \quad \alpha \leq \frac{b_i}{a_i^\top c},
$$

provided $a_i^\top c > 0$ (if $a_i^\top c \leq 0$, the ray runs parallel to or away from wall $i$, which never blocks it). The ray exits through the **most restrictive wall**:

$$
\alpha^* = \min_{i \,:\, a_i^\top c > 0} \frac{b_i}{a_i^\top c}.
$$

### 11.6.2 Combining Walls: The Dual Perspective

Each wall provides an individual bound on $\alpha$. But the dual does something cleverer: it **combines walls** with nonnegative weights $y_1, \ldots, y_m \geq 0$. Adding up $y_i \cdot (a_i^\top x \leq b_i)$ yields:

$$
\left(\sum_{i=1}^m y_i \, a_i\right)^\top x \;\leq\; \sum_{i=1}^m y_i \, b_i = b^\top y.
$$

If the combined normal dominates $c$ (meaning $A^\top y \geq c$), then for *every* feasible $x \geq 0$:

$$
c^\top x \;\leq\; (A^\top y)^\top x \;\leq\; b^\top y.
$$

The first “ $\leq$ ” uses $A^\top y \geq c$ and $x \geq 0$; the second uses $Ax \leq b$ and $y \geq 0$. The quantity $b^\top y$ bounds the objective over the *entire* polytope — not just along the ray. The dual LP $\min\, b^\top y$ subject to $A^\top y \geq c$, $y \geq 0$ finds the **tightest such combined barrier**.

NoteThe Geometric Essence of LP Duality

The primal-dual pair captures a push-versus-block contest between the objective and the constraints:

- **Primal** = push the objective forward as far as the polytope allows
- **Dual** = combine constraint walls to form the tightest barrier against forward progress
- **Weak duality** = the barrier always lies ahead of the farthest reachable point
- **Strong duality** = at optimality, the barrier *exactly touches* the farthest reachable point

In short, duality theory tells us that the tightest combined barrier exactly meets the farthest reachable point — there is never a gap between what the polytope permits and what the constraints can certify.

**Connection to duality.** The ray picture illustrates the *primal* side: how far can we push in direction $c$ before a wall stops us? Each wall $a_i^\top x \leq b_i$ gives an individual bound $\alpha \leq b_i / (a_i^\top c)$. The tightest wall determines the exit point. The *dual* side does something more powerful: instead of using one wall at a time, it **combines walls** with weights $y_1, \ldots, y_m \geq 0$ to create a synthetic barrier that bounds the objective over the *entire* polytope, not just along a single ray. The dual LP finds the tightest such combination.

Drag the slider below to rotate the ray direction $\theta$. As the angle changes, different constraint walls become the binding barrier. The colored dots mark where each wall would block the ray; the **star** marks the ray’s exit point. The **diamond** marks the LP-optimal vertex, and the dashed line shows the dual barrier $c^\top x = b^\top y^*$. The stacked bar decomposes the dual bound into each wall’s contribution.

### Ray Through Polytope

Polytope: x <sub>1</sub> ≤ 4,   x <sub>2</sub> ≤ 6,   3x <sub>1</sub> +2x <sub>2</sub> ≤ 18,   x ≥ 0.   The ray exits through the tightest wall; the dual combines walls to certify the LP optimum.

59°

**Direction:** c = (0.515, 0.857)  
**Wall bounds on α:**  ● 3x₁+2x₂ ≤ 18: α ≤ 5.52 **← exit**   ● x₂ ≤ 6: α ≤ 7.00   ● x₁ ≤ 4: α ≤ 7.77    
**Ray exit:** α\* = 5.52   **LP optimum:** c <sup>T</sup> x\* = 6.17 at (2, 6)  
**Dual certificate:** y\* = (0.000, 0.514, 0.172)

b <sup>T</sup> y\* =

6y₂ = 3.08

18y₃ = 3.09

\= 6.17

Strong duality: c <sup>T</sup> x\* = b <sup>T</sup> y\* = 6.17 — the combined barrier touches the optimum exactly.

The geometric picture – pushing forward against combined barriers – gives powerful intuition for why weak duality holds (the barrier is always ahead) and why strong duality is remarkable (the barrier touches the farthest reachable point). We now move from geometry to economics, asking what the dual variables tell us about the sensitivity of the optimal value to changes in the problem data.

## 11.7 Sensitivity Analysis and Shadow Prices

So far, duality has told us about the *value* of the optimal solution. But in practice, we also want to know: **if we change the problem slightly, how does the optimal value respond?** For instance, if a factory has 100 units of a resource and could acquire 1 more, how much additional profit would that yield? The dual variables answer exactly this question.

### 11.7.1 Perturbed Primal

Consider a **perturbed primal** LP where we change $b$ to $b + \Delta$:

$$
\text{(P')} \quad \max \; c^\top x \quad \text{s.t.} \quad Ax \leq b + \Delta, \quad x \geq 0.
$$

The corresponding perturbed dual is:

$$
\text{(D')} \quad \min \; (b + \Delta)^\top y \quad \text{s.t.} \quad A^\top y \geq c, \quad y \geq 0.
$$

**Key observations:**

1. The dual feasible set $\Omega_D = \{y : A^\top y \geq c, \; y \geq 0\}$ does **not change** when we perturb $b$. Only the dual objective changes from $b^\top y$ to $(b + \Delta)^\top y$.
2. If $\Delta$ is sufficiently small, the dual problems (D) and (D’) have the **same optimal solution** $y^*$ (because the set of BFS vertices is discrete and does not change for small perturbations of the objective).
3. By strong duality: 
	$$
	\text{OptVal}(\text{P'}) - \text{OptVal}(\text{P}) = (b + \Delta)^\top y^* - b^\top y^* = \Delta^\top y^*.
	$$

### 11.7.2 Shadow Price Interpretation

**Definition 11.2 (Shadow Price)** The optimal dual variable $y_i^*$ is called the **shadow price** of the $i$ -th constraint. It measures the rate of change of the optimal value with respect to the $i$ -th constraint’s right-hand side:

$$
y_i^* = \frac{\partial}{\partial b_i} \text{OptVal}(\text{LP}(A, b, c)).
$$

Intuitively, $y^* = (y_1^*, \ldots, y_m^*)$ reflects how much the objective changes when we change each constraint by one unit. In economics, $y_i^*$ represents the **marginal value** of relaxing the $i$ -th constraint – if the constraint $a_i^\top x \leq b_i$ represents a resource limit, then $y_i^*$ is the price one should be willing to pay for one additional unit of that resource.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/sensitivity.svg)

Figure 11.3: Sensitivity analysis. Perturbing the resource constraint bound b 3 b\_3 ( x 1 + 2 ≤ 3x\_1+2x\_2 \\leq b\_3 ) changes the optimal value. The slope of the tangent line at the default point 18, 36 ) (18, 36) equals the shadow price y ∗ = y\_3^\* = 1.

TipEconomic Interpretation

Consider a production planning LP where the decision variables and parameters have the following economic meaning:

- $x_j$ = amount of product $j$ to produce
- $c_j$ = profit per unit of product $j$
- $b_i$ = available amount of resource $i$
- $a_{ij}$ = amount of resource $i$ needed per unit of product $j$

Under this interpretation, the optimal dual variable $y_i^*$ is the **marginal value of resource $i$**: how much additional profit we could earn if we had one more unit of resource $i$. A resource with $y_i^* = 0$ is not a bottleneck (the constraint is not tight at optimality); a resource with $y_i^* > 0$ is scarce and limits our profit.

Shadow prices tell us how the optimal value changes with perturbations to the right-hand side, but they do not directly characterize the structure of optimal solutions. For that, we need a pointwise condition linking primal and dual optima: complementary slackness.

## 11.9 Worked Example

Let us trace through a complete example to see all the duality results in action.

**Example 11.1 (Complete Duality Example)** Consider the primal LP:

$$
\max \; 3x_1 + 5x_2 \quad \text{s.t.} \quad x_1 \leq 4, \quad x_2 \leq 6, \quad 3x_1 + 2x_2 \leq 18, \quad x_1, x_2 \geq 0.
$$

**Step 1: Write the dual.** With $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 3 & 2 \end{pmatrix}$, $b = \begin{pmatrix} 4 \\ 6 \\ 18 \end{pmatrix}$, $c = \begin{pmatrix} 3 \\ 5 \end{pmatrix}$:

$$
\min \; 4y_1 + 6y_2 + 18y_3 \quad \text{s.t.} \quad y_1 + 3y_3 \geq 3, \quad y_2 + 2y_3 \geq 5, \quad y_1, y_2, y_3 \geq 0.
$$

**Step 2: Solve the primal.** By vertex enumeration or the simplex method, the optimal solution is $x^* = (2, 6)$ with $f^* = 3(2) + 5(6) = 36$.

**Step 3: Check complementary slackness.** The primal slack variables are: 
$$
w_1 = 4 - 2 = 2, \quad w_2 = 6 - 6 = 0, \quad w_3 = 18 - 3(2) - 2(6) = 0.
$$

By complementary slackness, $w_i y_i = 0$ for all $i$:

- $w_1 = 2 > 0 \implies y_1^* = 0$
- $w_2 = 0$ and $w_3 = 0$: $y_2^*, y_3^*$ can be nonzero

Also, $x_1^* = 2 > 0 \implies z_1 = 0$, i.e., $y_1^* + 3y_3^* = 3$, and $x_2^* = 6 > 0 \implies z_2 = 0$, i.e., $y_2^* + 2y_3^* = 5$.

From $y_1^* = 0$: $3y_3^* = 3 \implies y_3^* = 1$. Then $y_2^* + 2(1) = 5 \implies y_2^* = 3$.

**Step 4: Verify strong duality.** $b^\top y^* = 4(0) + 6(3) + 18(1) = 36 = f^*$. The duality gap is zero!

**Step 5: Shadow prices.** $y_1^* = 0$ means the constraint $x_1 \leq 4$ is not binding (we have slack $w_1 = 2$), so relaxing it has no effect on the optimum. $y_2^* = 3$ means that increasing the bound on $x_2$ by one unit (from 6 to 7) would increase the optimal profit by approximately 3. $y_3^* = 1$ means relaxing the combined resource constraint by one unit increases profit by approximately 1.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/duality-worked-example.svg)

Figure 11.4: Worked example: primal feasible region with objective contours at f = 10, 20 30 36 f = 10, 20, 30, 36. Each vertex is labeled with its objective value. The optimal vertex ( 2 6 ) (2,6) achieves ∗ f^\* = 36, which equals the dual optimal value.

## 11.10 Summary

NoteKey Takeaways

1. **Every LP has a dual LP** obtained by the multiply-sum-dominate recipe: weight constraints by multipliers $y \geq 0$, sum to get a combined inequality, require the left side to dominate $c$. The dual minimizes the resulting upper bound.
2. **Weak duality** always holds: $c^\top x \leq b^\top y$ for every primal feasible $x$ and dual feasible $y$. If the gap is zero, both solutions are optimal.
3. **Strong duality** holds at optimality: $c^\top x^* = b^\top y^*$. The simplex multipliers $y^* = (\mathbf{A}_B^{-1})^\top c_B$ are automatically dual optimal.
4. **Shadow prices** ($y_i^*$) measure the sensitivity of the optimal value to changes in the right-hand side: $y_i^* = \partial f^* / \partial b_i$.
5. **Complementary slackness** characterizes optimality pointwise: at an optimal pair, if a variable is positive, the corresponding constraint is tight, and vice versa.
6. The **four possibilities** for a primal-dual pair are: both infeasible, primal infeasible & dual unbounded, primal unbounded & dual infeasible, or both finite optimal (with zero duality gap).

TipLooking Ahead

Duality theory is not just a theoretical curiosity – it is the engine behind some of the most important LP algorithms. In the [next chapter](https://zhuoranyang.github.io/sds431-notes/lectures/12-dual-simplex.html), we will see how the **dual simplex method** maintains dual feasibility and works toward primal feasibility, essentially solving the dual LP while recovering a primal solution. We will also explore how duality underpins important [LP applications](https://zhuoranyang.github.io/sds431-notes/lectures/13-lp-applications.html) including two-person zero-sum games and robust optimization.