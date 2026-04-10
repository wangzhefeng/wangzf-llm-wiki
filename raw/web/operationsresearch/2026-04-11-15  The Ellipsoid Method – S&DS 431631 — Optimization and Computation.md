---
author: null
created: 2026-04-11
description: null
published: null
source: https://zhuoranyang.github.io/sds431-notes/lectures/15-ellipsoid-method.html
tags:
- clippings
title: 15  The Ellipsoid Method – S&DS 431/631 — Optimization and Computation
topics:
- 运筹优化
---
The [simplex method](https://zhuoranyang.github.io/sds431-notes/lectures/10-simplex-method.html) is remarkably efficient in practice, but as we saw through the Klee–Minty construction, its worst-case complexity is exponential. This raises a fundamental question: **can linear programs be solved in polynomial time?**

The ellipsoid method, introduced by Khachiyan in 1979, provides an affirmative answer. It was the first algorithm proven to solve linear programs in polynomial time, resolving one of the most important open questions in mathematical optimization. More broadly, the ellipsoid method applies to general convex optimization: any convex problem equipped with a **separation oracle** can be solved efficiently.

The core idea is beautifully geometric. We maintain an ellipsoid that is guaranteed to contain the optimal solution. At each step, we use either a gradient or a separating hyperplane to cut the ellipsoid in half, then enclose the relevant half in a smaller ellipsoid. The volume shrinks by a constant factor at every iteration, so eventually the ellipsoid becomes too small to contain any feasible point far from optimal.

While the ellipsoid method is not practical for large-scale computation (it suffers from numerical issues and large constants), its theoretical significance is profound. It established that LP is in the complexity class P and laid the groundwork for interior point methods, which achieve both polynomial complexity and practical efficiency.

## What Will Be Covered

- Historical context: from simplex to polynomial-time algorithms
- Ellipsoids: definition, geometry, and volume
- The ellipsoid method for LP feasibility
- Reduction of LP optimization to feasibility via binary search
- The minimum volume enclosing ellipsoid (MVEE) update
- Volume shrinkage and convergence analysis
- Separation oracles and extension to general convex optimization
- The ellipsoid method for general convex programs
- Comparison with simplex and preview of interior point methods

## 15.1 Historical Context

NoteA Brief History of LP Algorithms and Convex Optimization

The quest for efficient LP algorithms spans four decades, with each breakthrough reshaping our understanding of computational complexity:

- **1947:** Dantzig introduced the simplex algorithm for LP.
- **1973:** Klee and Minty proved that the simplex algorithm is **not** a polynomial-time algorithm by constructing a family of LPs on which it visits all $2^n$ vertices.
- **1976–1977:** Shor and, independently, Nemirovski and Yudin introduced the ellipsoid method for convex programs.
- **1979:** Khachiyan proved that the ellipsoid method is a polynomial-time algorithm for LP — the first such algorithm.
- **1984:** Karmarkar introduced the polynomial-time interior point algorithm for LP.
- **1988:** Nesterov and Nemirovski extended interior point methods to general convex programs.

The ellipsoid algorithm is **not practical** — its significance is theoretical. It demonstrated for the first time that LP can be solved in polynomial time. Modern solvers (SeDuMi, SDPT3, MOSEK, Gurobi) all use variants of interior point methods.

## 15.2 Preparation: Ellipsoids

Before presenting the algorithm, we need to define the central geometric object: the ellipsoid. An ellipsoid generalizes a ball by allowing different “radii” along different directions, controlled by a positive definite matrix.

**Definition 15.1 (Definition (Ellipsoid))** Let $Q \in \mathbb{R}^{n \times n}$ be a positive definite matrix and $c \in \mathbb{R}^n$. The **ellipsoid** associated with $Q$ and centered at $c$ is defined as

$$
\mathcal{E}(c, Q) = \{c + y : y^\top Q^{-1} y \leq 1\} = \{y : (y - c)^\top Q^{-1} (y - c) \leq 1\}.
\tag{15.1}
$$

The center $c$ determines where the ellipsoid is located, and the matrix $Q$ determines its shape and orientation. The eigenvectors of $Q$ give the principal axes of the ellipsoid, and the square roots of the eigenvalues give the corresponding semi-axis lengths. A large eigenvalue corresponds to a long axis.

**Example.** The Euclidean ball of radius $R$ centered at $x_0$ is the ellipsoid $B(x_0, R) = \mathcal{E}(x_0, R^2 I)$. Here $Q = R^2 I$ is a scalar multiple of the identity, so all axes have equal length $R$.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ellipsoid-shapes.svg)

Figure 15.1: Ellipsoids in 2D with different shape matrices Q. Left: a ball ( = I Q = I ). Center: an axis-aligned ellipse. Right: a rotated ellipse. The eigenvectors of determine the principal axes.

### 15.2.1 Volume of an Ellipsoid

The volume of an ellipsoid ([Equation 15.1](https://zhuoranyang.github.io/sds431-notes/lectures/15-ellipsoid-method.html#eq-ellipsoid-def)) has a clean formula in terms of the determinant of the shape matrix.

$$
\text{vol}(\mathcal{E}(c, Q)) = \text{vol}(B_1) \cdot \det(Q)^{1/2},
$$

where $B_1$ denotes the unit ball in $\mathbb{R}^n$. Since $\det(Q) = \prod_{i=1}^n \lambda_i$ where $\lambda_1, \ldots, \lambda_n$ are the eigenvalues of $Q$, the volume is proportional to the product of the semi-axis lengths. This formula will be crucial for analyzing the convergence of the ellipsoid method: we will show that the volume shrinks by a constant factor at each iteration.

## 15.3 Ellipsoid Method for LP

Consider the linear program

$$
\min_{x} \; c^\top x \quad \text{s.t.} \quad Ax \leq b, \; x \geq 0.
$$

We write this compactly as $\min c^\top x$ subject to $x \in P$, where $P$ is the feasible polyhedron. Assume the LP has a finite optimal value $f^* > -\infty$ and that $P$ is bounded (so $P$ is a polytope).

### 15.3.2 The Feasibility Problem

To simplify notation, assume the polytope can be written as

$$
P = \{x : a_i^\top x \leq b_i, \; i \in [m]\}
$$

for some $\{a_i, b_i\}$.

**Goal:** Find a point $x \in P$. If no such $x$ exists, declare $P = \emptyset$.

TipAssumption (Bounded Feasible Region)

If $P \neq \emptyset$, there exist $x_0 \in P$ and $R, r > 0$ such that

$$
B_2(x_0, r) \subseteq P \subseteq B_2(x_0, R),
$$

where $B_2(x_0, r) = \{x : \|x - x_0\|_2 \leq r\}$. In other words, $P$ is “sandwiched” between a small ball of radius $r$ and a large ball of radius $R$. This assumption can be rigorously verified for LP; we omit the technical details.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch20-ellipsoid-method.svg)

Figure 15.2: The ellipsoid method: three progressively smaller ellipsoids E 0 \\mathcal{E}\_0, 1 \\mathcal{E}\_1 2 \\mathcal{E}\_2 each containing the feasible region P. Separating hyperplanes (dashed) cut each ellipsoid in half, and the volume shrinks by a factor of e − / ( n + ) e^{-1/(2n+2)} per step.

### 15.3.3 The Idea: Binary Search in Rn\\mathbb{R}^n

The ellipsoid method performs a kind of “binary search” in $\mathbb{R}^n$:

1. **Cover** $P$ with an ellipsoid $\mathcal{E}(c, Q)$.
2. **Check** if the center $c \in P$.
	- **Yes:** We are done — return $c$ as a feasible point.
		- **No:** The center $c$ is outside $P$. Then there exists some violated constraint $i_0 \in [m]$ such that $a_{i_0}^\top c > b_{i_0}$.

When the center is infeasible, the violated constraint gives us a **separating hyperplane** $\{x : a_{i_0}^\top x = a_{i_0}^\top c\}$. Since every $x \in P$ satisfies $a_{i_0}^\top x \leq b_{i_0} < a_{i_0}^\top c$, the entire polytope $P$ lies strictly on one side of this hyperplane:

$$
P \subseteq \{x : a_{i_0}^\top x \leq a_{i_0}^\top c\}.
$$

We can then discard the other half of the ellipsoid and construct a new, smaller ellipsoid covering the half-ellipsoid $\mathcal{E}(c, Q) \cap \{x : a_{i_0}^\top x \leq a_{i_0}^\top c\}$ that still contains $P$.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ellipsoid-cut.svg)

Figure 15.3: The ellipsoid method for feasibility. The center c is outside P, so a violated constraint provides a separating hyperplane. lies entirely in the lower half-ellipsoid. The new (green) ellipsoid covers this half and is strictly smaller.

### 15.3.4 The Ellipsoid Algorithm for Feasibility

ImportantAlgorithm: Ellipsoid Method for Feasibility

**Input:** Polytope $P = \{x : a_i^\top x \leq b_i, \; i \in [m]\}$, outer radius $R$.

**Initialize:** $\mathcal{E}(c^0, Q^0) = \mathcal{E}(0, R^2 I) \supseteq P$.

**For** $k = 1, 2, \ldots$:

1. **Check** if $c^k \in P$.
2. **If $c^k \in P$:** Stop. Return $c^k \in P$ (feasible).
3. **If $c^k \notin P$:**
	- Find the constraint $a_{i_0}^\top x \leq b_{i_0}$ that $c^k$ violates.
		- **Update ellipsoid:** Let $\mathcal{E}(c^{k+1}, Q^{k+1})$ be the minimum volume ellipsoid containing $\mathcal{E}(c^k, Q^k) \cap \{x : a_{i_0}^\top x \leq a_{i_0}^\top c^k\}$.
4. **If** $\text{vol}(\mathcal{E}(c^{k+1}, Q^{k+1})) < \text{vol}(B(0, r))$: Stop. Return “infeasible.”

**Why does the stopping criterion work?** By construction, the ellipsoid always contains $P$: $\mathcal{E}(c^k, Q^k) \supseteq P$ for all $k = 1, 2, \ldots$ (this is an invariant of the algorithm). If $P$ is feasible, then $P$ contains a ball $B(x_0, r)$ of radius $r$. Therefore, if the ellipsoid volume drops below $\text{vol}(B(0, r))$, it can no longer contain such a ball, so $P$ must be infeasible.

## 15.4 Minimum Volume Enclosing Ellipsoid

The critical step of the algorithm is constructing the minimum volume ellipsoid covering a half-ellipsoid. Given the current ellipsoid $\mathcal{E}(c^k, Q^k)$ and a cutting direction $g$ (the normal vector of the separating hyperplane), we need to find the smallest ellipsoid containing the half-ellipsoid

$$
\mathcal{E}(c^k, Q^k) \cap \{y : g^\top(y - c^k) \leq 0\}.
$$

**Theorem 15.1 (Theorem (MVEE Update Formulas))** Given the half-ellipsoid $\mathcal{E}(c, Q) \cap \{y : g^\top(y - c) \leq 0\}$, the minimum volume enclosing ellipsoid $\mathcal{E}(c^+, Q^+)$ has parameters:

$$
c^+ = c - \frac{1}{n+1} \cdot \frac{Qg}{\sqrt{g^\top Q g}},
$$

$$
Q^+ = \frac{n^2}{n^2 - 1} \left[ Q - \frac{2}{n+1} \cdot \frac{Qg \, g^\top Q}{g^\top Q g} \right],
$$

where $n$ is the dimension.

The update has an elegant interpretation. The new center $c^+$ shifts from $c$ in the direction $-Qg$ (which accounts for the ellipsoid’s shape) by a step proportional to $\frac{1}{n+1}$. The new shape matrix $Q^+$ is obtained by shrinking $Q$ along the cut direction $g$ while slightly expanding in the orthogonal directions. The factor $\frac{n^2}{n^2-1}$ is a mild inflation that ensures the half-ellipsoid is fully enclosed.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/mvee-update.svg)

Figure 15.4: The MVEE update. Given a half-ellipsoid (shaded), the minimum volume enclosing ellipsoid (green dashed) is computed using the update formulas. The new center shifts away from the cut.

## 15.5 Analysis of the Ellipsoid Method

### 15.5.1 Volume Shrinkage

The following theorem is the key to the convergence analysis. It shows that each MVEE update reduces the ellipsoid volume by a fixed multiplicative factor that depends only on the dimension.

**Theorem 15.2 (Theorem (Volume Reduction))** For $k \geq 0$, we have

$$
\frac{\text{vol}(\mathcal{E}(c^{k+1}, Q^{k+1}))}{\text{vol}(\mathcal{E}(c^k, Q^k))} \leq \exp\!\left(-\frac{1}{2(n+1)}\right),
\tag{15.2}
$$

where $n$ is the dimension of $x$.

This means that after $2(n+1)$ steps, the volume of the ellipsoid shrinks by at least a factor of $\frac{1}{e} \approx 0.368$. The shrinkage is guaranteed regardless of which cutting plane is used — the geometry of the MVEE update ensures a constant-factor reduction.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/volume-shrinkage.svg)

Figure 15.5: Volume shrinkage of the ellipsoid over iterations for different dimensions n. The volume decreases exponentially, with a per-step shrinkage factor of exp ⁡ ( − 1 / 2 + ) \\exp(-1/(2(n+1))). Higher dimensions lead to slower per-step shrinkage.

### 15.5.2 Iteration Complexity

**Theorem 15.3 (Theorem (Iteration Complexity of the Ellipsoid Method))** The ellipsoid method solves the feasibility problem after $O(n^2 \log(R/r))$ iterations.

The proof is a direct calculation: the volume shrinkage bound ([Equation 15.2](https://zhuoranyang.github.io/sds431-notes/lectures/15-ellipsoid-method.html#eq-volume-shrinkage)) limits how many halvings are needed before the ellipsoid becomes smaller than the inscribed ball.

*Proof*. Since $\frac{\text{vol}(\mathcal{E}(c^{k+1}, Q^{k+1}))}{\text{vol}(\mathcal{E}(c^k, Q^k))} \leq \exp\!\left(-\frac{1}{2(n+1)}\right)$, the number of iterations needed is at most

$$
\frac{\log\!\left(\frac{\text{vol}(B(0, R))}{\text{vol}(B(0, r))}\right)}{\log\!\left(\exp\!\left(\frac{1}{2(n+1)}\right)\right)}.
$$

The numerator is $\log\!\left(\frac{R^n}{r^n}\right) = n \log(R/r)$, which is $O(n \log(R/r))$.

The denominator is $\frac{1}{2(n+1)}$.

Therefore, the number of iterations is at most

$$
O\!\left(n \log(R/r) \cdot 2(n+1)\right) = O(n^2 \log(R/r)). \qquad \blacksquare
$$

NoteKey Observation

The number of iterations depends only on $n$ (the number of variables) and $\log(R/r)$, and is **independent of the number of constraints** $m$. This is a remarkable feature: the ellipsoid method does not slow down when the polyhedron is described by many constraints.

**Complexity for LP.** Each iteration requires $O(n^2)$ arithmetic operations (for the matrix update $Q^{k+1}$), so the total arithmetic complexity is $O(n^4 \log(R/r))$. For linear programs, Khachiyan showed that $\log(R/r)$ is polynomial in the input size (the bit lengths of $A$, $b$, and $c$), yielding an overall **polynomial-time** algorithm.

The polynomial iteration bound $O(n^2 \log(R/r))$ was a landmark result: it proved for the first time that LP lies in the complexity class P. Equally remarkable, the bound is independent of the number of constraints $m$. We next show that this framework extends well beyond polyhedra to any convex set equipped with a suitable oracle.

## 15.6 Separation Oracles and General Convex Sets

The ellipsoid method for LP feasibility relied on a simple observation: when $c^k \notin P$, a violated linear constraint provides a separating hyperplane. This idea generalizes far beyond LP to **any convex set** through the concept of a separation oracle, making the ellipsoid method a universal tool for convex optimization.

### 15.6.1 Separating Hyperplane Theorem

Recall the separating hyperplane theorem from convex analysis:

**Theorem 15.4 (Theorem (Separating Hyperplane Theorem))** Let $\mathcal{C}, \mathcal{D}$ be two disjoint closed convex sets, with $\mathcal{C}$ bounded. Then there exists $a \in \mathbb{R}^n$, $a \neq 0$, and $b \in \mathbb{R}$ such that

$$
a^\top x + b < 0 \quad \forall\, x \in \mathcal{C}, \qquad a^\top x + b \geq 0 \quad \forall\, x \in \mathcal{D}.
$$

**Corollary 15.1 (Corollary (Separating a Point from a Compact Convex Set))** If $x_0 \notin \mathcal{C}$ and $\mathcal{C}$ is compact and convex, then there exists $a \in \mathbb{R}^n$, $a \neq 0$, such that

$$
x^\top a < x_0^\top a \quad \forall\, x \in \mathcal{C}.
$$

That is, $\mathcal{C} \subseteq \{x : a^\top(x - x_0) < 0\}$.

### 15.6.2 Separation Oracle

**Definition 15.2 (Definition (Separation Oracle))** A **separation oracle** for a convex set $\mathcal{C}$ is a procedure that, given a query point $x_0$:

- Returns **“Yes”** if $x_0 \in \mathcal{C}$.
- Otherwise, returns **“No”** together with a **separating hyperplane** $\{x : a^\top x = a^\top x_0\}$ such that $\mathcal{C} \subseteq \{x : a^\top x < a^\top x_0\}$.

**For LP,** implementing a separation oracle is straightforward: to check if $c^k \in P = \{x : a_i^\top x \leq b_i\}$, simply evaluate each constraint. If $a_{i_0}^\top c^k > b_{i_0}$ for some $i_0$, use $a_{i_0}$ as the separating direction.

**For general convex sets,** the separating hyperplane theorem guarantees that a separation oracle exists (in principle), though it may be nontrivial to implement. The power of the ellipsoid method is that it works for **any** convex set equipped with a separation oracle.

### 15.6.3 Ellipsoid Method for General Convex Feasibility

With the separation oracle, we can derive the ellipsoid method for a general convex set $\mathcal{C}$. The invariant is: $\mathcal{E}(c^k, Q^k) \supseteq \mathcal{C}$ for all $k$.

1. Given $\mathcal{E}(c^k, Q^k) \supseteq \mathcal{C}$, call the separation oracle to check if $c^k \in \mathcal{C}$.
2. **If Yes:** We are done.
3. **If No:** The separation oracle gives us a hyperplane that cuts $\mathcal{E}(c^k, Q^k)$ in half, with $\mathcal{C}$ on one side. Then let $\mathcal{E}(c^{k+1}, Q^{k+1})$ be the smallest ellipsoid containing the half-ellipsoid that contains $\mathcal{C}$.

The same volume reduction theorem applies, so the convergence guarantee is identical: $O(n^2 \log(R/r))$ iterations.

## 15.7 Ellipsoid Method for Convex Optimization

With the separation oracle framework in hand, we now extend the ellipsoid method from feasibility to **general convex optimization**. The key idea is that the gradient of the objective provides a natural cutting plane even when the current point is feasible.

$$
\min_{x} \; f(x) \quad \text{s.t.} \quad x \in \Omega,
$$

where $f$ is convex and $\Omega$ is a convex feasible set.

### 15.7.1 Two Scenarios

Recall the first-order optimality condition for convex optimization: $x^*$ is optimal if and only if

$$
\langle x - x^*, \nabla f(x^*) \rangle \geq 0 \quad \forall\, x \in \Omega.
$$

This means the gradient $\nabla f(x^*)$ at the optimum provides a separating hyperplane between $x^*$ and the sublevel set $\Omega$. Moreover, if $x$ is **not** optimal, then there exists $y$ such that $y^\top \nabla f(x) < x^\top \nabla f(x)$ — that is, moving along $-\nabla f(x)$ decreases the objective.

At each iteration, the center $c^k$ of the current ellipsoid falls into one of two scenarios:

**Scenario 1: $c^k \in \Omega$ (feasible) but not optimal.** The gradient $\nabla f(c^k)$ defines a cutting hyperplane. The optimal $x^*$ lies in the halfspace $\{y : (y - c^k)^\top \nabla f(c^k) \leq 0\}$, because moving along $-\nabla f(c^k)$ decreases the objective. We restrict to

$$
\Omega \cap \{y : (y - c^k)^\top \nabla f(c^k) \leq 0\}.
$$

**Scenario 2: $c^k \notin \Omega$ (infeasible).** Query the separation oracle for $\Omega$: it returns a hyperplane through $c^k$ such that $\Omega$ lies in one halfspace. We restrict to the half-ellipsoid containing $\Omega$.

In both cases, we have a cutting plane through $c^k$, and the next ellipsoid $\mathcal{E}(c^{k+1}, Q^{k+1})$ is the MVEE of the relevant half. We also track the **best feasible point seen so far** as our candidate solution.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ellipsoid-scenarios.svg)

Figure 15.6: The two scenarios of the ellipsoid method for convex optimization. Left (Scenario 1): the center is feasible but not optimal — the gradient provides the cutting plane. Right (Scenario 2): the center is infeasible — the separation oracle provides the cutting plane.

### 15.7.2 The Full Algorithm

ImportantAlgorithm: Ellipsoid Method for Convex Optimization

**Input:** Convex function $f$, convex feasible set $\Omega$ (with separation oracle), initial ellipsoid $\mathcal{E}(c^0, Q^0) \supseteq \{x^*\}$.

**Initialize:** $x_{\text{best}} \leftarrow \text{None}$, $f_{\text{best}} \leftarrow +\infty$.

**For** $k = 1, 2, \ldots$:

1. **Check** if $c^k \in \Omega$.
2. **(a) If $c^k \notin \Omega$ (infeasible):**
	- Query the separation oracle $\to$ get separating direction $a$.
		- Construct half-ellipsoid: $\mathcal{E}(c^k, Q^k) \cap \{y : a^\top y \leq a^\top c^k\}$.
		- Set $g \leftarrow a$ and update: $\mathcal{E}(c^{k+1}, Q^{k+1}) \supseteq$ half-ellipsoid.
3. **(b) If $c^k \in \Omega$ (feasible):**
	- Update best: if $f(c^k) < f_{\text{best}}$, set $x_{\text{best}} \leftarrow c^k$, $f_{\text{best}} \leftarrow f(c^k)$.
		- Query gradient oracle $\to$ get $\nabla f(c^k)$.
		- Construct half-ellipsoid: $\mathcal{E}(c^k, Q^k) \cap \{y : (y - c^k)^\top \nabla f(c^k) \leq 0\}$.
		- Set $g \leftarrow \nabla f(c^k)$ and update: $\mathcal{E}(c^{k+1}, Q^{k+1}) \supseteq$ half-ellipsoid.
4. **Ellipsoid update** (same formulas in both cases):

$$
c^{k+1} = c^k - \frac{1}{n+1} \cdot \frac{Q^k g}{\sqrt{g^\top Q^k g}}, \qquad Q^{k+1} = \frac{n^2}{n^2 - 1}\left[Q^k - \frac{2}{n+1} \cdot \frac{Q^k g \, g^\top Q^k}{g^\top Q^k g}\right].
$$

**Return:** $x_{\text{best}}$, $f_{\text{best}}$.

Having developed the full ellipsoid method for convex optimization, we now compare it with the other major approaches to LP and convex programming.

## 15.8 Comparison: Simplex vs. Ellipsoid vs. Interior Point

| **Worst-case complexity** | Exponential | **Polynomial** | **Polynomial** |
| --- | --- | --- | --- |
| **Practical performance** | **Excellent** | Poor | **Excellent** |
| **Applies to** | LP only | General convex | General convex |
| **Year introduced** | 1947 (Dantzig) | 1979 (Khachiyan) | 1984 (Karmarkar) |
| **Key idea** | Vertex hopping | Volume shrinking | Path following |

TipThe Bottom Line

- The **simplex method** has exponential worst-case complexity (Klee–Minty) but is the fastest in practice for LP.
- The **ellipsoid method** was the first polynomial-time algorithm for LP and works for any convex problem with a separation oracle, but it is not practical due to numerical issues and large constants.
- **Interior point methods** (which we will study next) achieve the best of both worlds: polynomial worst-case complexity *and* excellent practical performance. They are the algorithms behind modern solvers like MOSEK, Gurobi, and SeDuMi.

NoteLooking Ahead

The ellipsoid method bridges LP theory and general convex optimization. Having established that LP (and convex optimization more broadly) can be solved in polynomial time, we next turn to **interior point methods**, which achieve polynomial complexity with practical efficiency. These methods follow a smooth central path through the interior of the feasible region, combining the theoretical guarantees of the ellipsoid method with the practical speed of the simplex method.

## Summary

- **First polynomial-time LP algorithm.** Khachiyan’s ellipsoid method (1979) resolved a major open question by proving that linear programs can be solved in polynomial time, running in $O(n^2 \log(V/\varepsilon))$ iterations where each iteration shrinks the enclosing ellipsoid’s volume by a constant factor.
- **Geometric core idea.** Maintain an ellipsoid $\mathcal{E}(c, Q)$ guaranteed to contain the optimum; at each step, use a separating hyperplane to cut the ellipsoid in half, then compute the minimum-volume ellipsoid enclosing the relevant half-ellipsoid.
- **Separation oracle framework.** The ellipsoid method applies to any convex optimization problem equipped with a separation oracle—given a point $x$, either certify $x \in C$ or return a hyperplane separating $x$ from $C$ —making it far more general than simplex.
- **Theoretical vs. practical significance.** Despite its polynomial worst-case guarantee, the ellipsoid method is not used in practice due to numerical sensitivity and large constants; its legacy is establishing LP $\in$ P and motivating the development of interior point methods.