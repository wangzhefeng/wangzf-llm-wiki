---
author: null
created: 2026-04-11
description: null
tags:
- clippings
title: 9  LP Formulation and Geometry – S&DS 431/631 — Optimization and Computation
source_type: web
created_at: 2026-04-11
status: inbox
source_url: https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html
published_at: null
related_concepts: []
topics:
  - operations-research
  - 数学优化算法/运筹学
---
Why should we care about the geometry of linear programs? Because geometry reveals where the optimal solution must live. A linear objective function, when minimized over a polyhedron, always achieves its best value at a “corner” – a vertex of the feasible region. This geometric insight is the foundation of the simplex method, the most widely used LP algorithm in practice, and it reduces the search for an optimal solution from an infinite continuous region to a finite set of candidate points.

In this chapter we make the notion of “corner” precise in two complementary ways. The first is geometric: an **extreme point** is a point in a convex set that cannot be written as a proper convex combination of two other points. The second is algebraic: a **vertex** is a feasible point where $n$ linearly independent constraints are binding. We prove that these two notions coincide for polyhedra, show that every nonempty polyhedron without a line has at least one extreme point, and culminate in the **Fundamental Theorem of Linear Programming**: if an LP has an optimal solution, then it has an optimal solution that is an extreme point.

This result has profound algorithmic consequences. Instead of searching over all feasible points, it suffices to examine the vertices – and the simplex method does exactly this, moving from vertex to vertex while improving the objective at each step.

## What Will Be Covered

This chapter develops the geometric and algebraic foundations of linear programming, building toward the key algorithms:

- The four possible cases of an LP (infeasible, unbounded, multiple optima, unique optimum)
- Extreme points and vertices: geometric and algebraic characterizations of “corner” points
- Equivalence of extreme points and vertices for polyhedra
- The Fundamental Theorem of LP and its algorithmic implications
- Vertex enumeration as a naive LP algorithm
- Converting canonical form LP to equational form via slack variables
- Basic feasible solutions (BFS) and the equivalence: extreme point = vertex = BFS
- Caratheodory’s theorem as an application
- The simplex method: reduced costs, pivot selection, and the complete algorithm

## 9.1 Four Possible Cases of LP

Consider the linear program $\min c^\top x$ subject to $x \in \Omega$, where $\Omega = \{x : Ax \leq b,\; x \geq 0\}$ (see [Part 4](https://zhuoranyang.github.io/sds431-notes/lectures/05-convex-optimization.html) for LP formulation and duality). There are four possible cases:

1. **Infeasible case:** $\Omega = \emptyset$.
2. **Unbounded case:** $f^* = -\infty$. In this case, $\Omega$ is also unbounded. We can push $\{x : c^\top x = t\}$ to make the value go to $-\infty$.
3. **Infinite number of optimal solutions:** $f^*$ is finite, $x^*$ is not unique. The set $\{x : c^\top x = f^*\} \cap \Omega$ corresponds to a “face” of $\Omega$. The entire face is optimal. The vector $\vec{c}$ is normal (perpendicular) to that face.
4. **Unique optimal solution:** $f^*$ is finite, $x^*$ is unique. Then $\{x : c^\top x = f^*\} \cap \Omega = x^*$, and $x^*$ is a “corner” point of $\Omega$.

### 9.1.1 Geometric Picture: Pushing the Level Set

The key geometric insight is this: for a fixed cost vector $c$, the **level sets** $\{x : c^\top x = t\}$ form a family of parallel hyperplanes, all perpendicular to $c$. As we decrease $t$ (moving in the direction $-c$), the level-set hyperplane sweeps across the feasible region. The optimum is reached at the **last value of $t$** for which $\{x : c^\top x = t\}$ still touches $\Omega$:

- If the hyperplane can be pushed indefinitely without leaving $\Omega$, the LP is **unbounded** ($f^* = -\infty$).
- If the last contact is at a single corner point, the optimum is a **unique vertex**.
- If the last contact is along an entire edge or face (i.e., $c$ is perpendicular to that face), there are **infinitely many optimal solutions** — but the face always contains a vertex.

This “sliding hyperplane” picture is the geometric reason why the **Fundamental Theorem of LP** (proved below) holds: for a polyhedron, the last point of contact with a sweeping hyperplane is always at a vertex (or a face that contains vertices).

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/lp-four-cases.svg)

Figure 9.1: The four possible cases of a linear program, illustrated in 2D. Dashed gold lines are objective contours c ⊤ x = const c^\\top x = \\text{const}; the gold arrow shows the direction of decreasing objective.

## 9.2 Vertices and Extreme Points

We need to characterize Case 3 and Case 4. To this end, we need to answer: what does “corner points” even mean? We only have some geometric intuition. The following is a geometric definition.

### 9.2.1 Extreme Point

The informal notion of a “corner point” of a polygon is intuitive, but we need a rigorous definition that works in any dimension. The following definition captures the essential property: a corner point cannot be expressed as a mixture of two other points in the set.

**Definition 9.1 (Extreme Point)** A point $x$ is an **extreme point** of a convex set $\mathcal{C}$ if it *cannot* be written as a convex combination of any two other points in $\mathcal{C}$.

That is, if $x = \lambda y + (1-\lambda) z$ for some $y, z \in \mathcal{C}$ and $\lambda \in [0,1]$, then we have $x = y$ or $x = z$.

An extreme point is a point that cannot be “decomposed” as a mixture of two other points in the set. Geometrically, extreme points are the “corners” of a convex set. For a polygon, they are the vertices; for a disk, they are the entire boundary. This concept will be crucial for understanding where LP solutions live.

Figure 9.2: Extreme points of a polygon (green vertices) vs. non-extreme boundary points. Hover over points for details.

**Example 9.1 (Extreme Points of a Circle)** What are the extreme points of a (filled) circle? **The entire boundary** (the circle itself). Every point on the boundary cannot be written as a convex combination of two other points in the disk.

Extreme points are always on the boundary of $\mathcal{C}$. This is a *geometric* characterization. In the following, we establish an *algebraic* characterization of “corner” points.

Recall from linear algebra that vectors $a_1, a_2, \ldots, a_k$ are **linearly independent** if

$$
\sum_{i=1}^{k} \alpha_i a_i = 0 \implies \alpha_i = 0 \quad \forall\, i \in [k].
$$

### 9.2.2 Linearly Independent Constraints

To build an algebraic characterization of extreme points, we need a way to determine when a system of constraints uniquely pins down a point. Linear independence of constraint normals ensures that the intersection of the corresponding hyperplanes is a single point rather than a line or higher-dimensional subspace.

**Definition 9.2 (Linearly Independent Constraints)** $k$ linear inequalities $a_i^\top x \leq b_i$, $i = 1, 2, \ldots, k$, are called **linearly independent** if $\{a_i\}_{i \in [k]}$ are linearly independent.

Linear independence of constraints means the constraints impose genuinely different restrictions on the decision variable. When constraints are linearly dependent, their boundaries are parallel (or coincident), and they cannot “pin down” a unique point. When $n$ constraints are linearly independent, their boundaries intersect in exactly one point.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/constraints-dep-indep.svg)

Figure 9.2: Left — Linearly dependent constraints (parallel boundary lines). Right — Linearly independent constraints (crossing boundary lines) with unique intersection at ( 1, ) (1,1).

In $\mathbb{R}^2$: the constraints $3x_1 - 3x_2 \leq 3$ and $x_1 - x_2 \leq 0$ are **linearly dependent** because their normal vectors are parallel. Halfspaces with parallel boundary lines are linearly dependent. Halfspaces whose boundary lines cross are linearly independent.

### 9.2.3 Binding / Tight Constraints

How do we characterize a “corner” point algebraically? Geometrically, it is an extreme point. Algebraically, it is the intersection of constraint boundaries – the hyperplanes where inequality constraints hold with equality. A constraint that holds with equality at a point is said to be **binding** at that point.

**Definition 9.3 (Binding / Tight Constraint)** We say a constraint $a_i^\top x \leq b_i$ (where $a_i \in \mathbb{R}^n$, $b_i \in \mathbb{R}$) is **binding** (or **tight**) at a point $\bar{x}$ if $a_i^\top \bar{x} = b_i$.

In other words, $\bar{x}$ is on the boundary of the halfspace $\{x : a_i^\top x \leq b_i\}$.

A binding constraint is one that is satisfied with equality at a given point – the point lies exactly on the boundary of that constraint’s halfspace. The more constraints that are binding at a point, the more “pinned down” that point is. As we will see, a vertex requires exactly $n$ linearly independent binding constraints.

**Example 9.2 (Binding Constraints in 2D and 3D)** **2-dimensional:** An extreme point $A$ is the intersection of two lines $\Rightarrow$ two linearly independent constraints are binding at $A$.

**3-dimensional:** An extreme point $A$ of a tetrahedron is the intersection of 3 planes (e.g., Face ABC, Face ACD, Face ABD) $\Rightarrow$ 3 linearly independent constraints are binding at $A$.

In general, in $\mathbb{R}^n$, an extreme point is determined by $n$ linearly independent binding constraints.

Figure 9.4: A tetrahedron in 3D. Each vertex is the intersection of 3 face-planes. Hover over vertices to see binding constraints.

### 9.2.4 Vertex

We are now ready to give the algebraic definition of a “corner” point. A vertex is a feasible point where enough linearly independent constraints are tight to uniquely determine it – exactly $n$ constraints in $\mathbb{R}^n$.

**Definition 9.4 (Vertex)** A point $\bar{x} \in \mathbb{R}^n$ is a **vertex** of a polyhedron $P = \{x : Ax \leq b\}$ if:

1. $\bar{x}$ is **feasible**, i.e., $A\bar{x} \leq b$.
2. There exist $n$ **linearly independent** constraints that are **tight** at $\bar{x}$.

The vertex definition provides an algebraic, computable criterion for identifying corners of a polyhedron: find $n$ linearly independent constraints that are simultaneously tight, then solve the resulting linear system. This is the basis for the vertex enumeration algorithm we develop later.

TipRemark

**Extreme point** is a *geometric* characterization of “corner” points.

**Vertex** is an *algebraic* characterization: if we can find $n$ linearly independent constraints $a_{j_1}^\top x = b_{j_1}, \ldots, a_{j_n}^\top x = b_{j_n}$ out of the $m$ constraints, then solving

$$
\begin{pmatrix} a_{j_1}^\top \\ \vdots \\ a_{j_n}^\top \end{pmatrix} x = \begin{pmatrix} b_{j_1} \\ \vdots \\ b_{j_n} \end{pmatrix}
$$

yields an extreme point.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/lp-geometry.svg)

Figure 9.3: Geometry of a linear program: the feasible polytope (shaded), its vertices, the objective function direction, and the optimal vertex where the isoprofit line is tangent.

### 9.2.5 Vertex = Extreme Point

For polyhedra, **vertex = extreme point**.

The geometric and algebraic characterizations of “corner” points turn out to be equivalent for polyhedra. This is a key result: it means we can use whichever characterization is more convenient – the geometric one for intuition and proofs by contradiction, the algebraic one for computation and enumeration.

**Theorem 9.1 (Equivalence of Extreme Point and Vertex)** Let $P = \{x \in \mathbb{R}^n \mid Ax \leq b\}$ be a nonempty polyhedron with $A \in \mathbb{R}^{m \times n}$. Let $\bar{x} \in P$. Then

$$
\bar{x} \text{ is an extreme point} \iff \bar{x} \text{ is a vertex.}
$$

This equivalence bridges geometry and algebra: the geometric notion of “cannot be decomposed as a convex combination” is exactly the same as the algebraic notion of “has $n$ linearly independent tight constraints.” This means we can use either characterization depending on which is more convenient for a given argument.

*Proof*. We prove both directions. Write the polyhedron as $P = \{x : a_i^\top x \leq b_i, \; i = 1, \ldots, m\}$ and let $I(\bar{x}) = \{i : a_i^\top \bar{x} = b_i\}$ denote the set of binding constraints at $\bar{x}$.

**($\Leftarrow$) Vertex $\Rightarrow$ Extreme point.** Suppose $\bar{x}$ is a vertex, so $\{a_i : i \in I(\bar{x})\}$ contains $n$ linearly independent vectors. Assume for contradiction that $\bar{x}$ is not an extreme point: there exist $y, z \in P$ with $y \neq z$ and $\lambda \in (0,1)$ such that $\bar{x} = \lambda y + (1-\lambda) z$.

For each binding constraint $i \in I(\bar{x})$:

$$
b_i = a_i^\top \bar{x} = \lambda \, a_i^\top y + (1-\lambda) \, a_i^\top z.
$$

Since $y, z \in P$, both $a_i^\top y \leq b_i$ and $a_i^\top z \leq b_i$. A convex combination of two quantities each at most $b_i$ can equal $b_i$ only if both equal $b_i$. Therefore $a_i^\top y = a_i^\top z = b_i$ for every $i \in I(\bar{x})$, which gives $a_i^\top (y - z) = 0$ for all $i \in I(\bar{x})$.

Since $\{a_i : i \in I(\bar{x})\}$ contains $n$ linearly independent vectors in $\mathbb{R}^n$, the only solution is $y - z = 0$, contradicting $y \neq z$. Hence $\bar{x}$ is an extreme point.

**($\Rightarrow$) Extreme point $\Rightarrow$ Vertex.** Suppose $\bar{x}$ is an extreme point. Assume for contradiction that the vectors $\{a_i : i \in I(\bar{x})\}$ do **not** span $\mathbb{R}^n$, i.e., their rank is less than $n$. Then there exists a nonzero direction $d \in \mathbb{R}^n$ with $a_i^\top d = 0$ for all $i \in I(\bar{x})$.

For each non-binding constraint $i \notin I(\bar{x})$, we have $a_i^\top \bar{x} < b_i$ (strict inequality). By continuity, there exists $\epsilon > 0$ small enough that $a_i^\top (\bar{x} \pm \epsilon d) < b_i$ for all $i \notin I(\bar{x})$.

For each binding constraint $i \in I(\bar{x})$: $a_i^\top (\bar{x} \pm \epsilon d) = b_i \pm \epsilon \cdot 0 = b_i \leq b_i$.

Therefore both $y = \bar{x} + \epsilon d$ and $z = \bar{x} - \epsilon d$ lie in $P$, with $y \neq z$ and $\bar{x} = \tfrac{1}{2} y + \tfrac{1}{2} z$. This contradicts $\bar{x}$ being an extreme point. Hence $\{a_i : i \in I(\bar{x})\}$ must contain $n$ linearly independent vectors, so $\bar{x}$ is a vertex. $\blacksquare$

#### 9.2.5.1 Finite Number of Extreme Points

**Corollary 9.1** Given a finite set of linear inequalities, there can only be a **finite number** of extreme points.

This is a reassuring finiteness result: although a polyhedron is a continuous set with infinitely many points, it has only finitely many “corners.” This makes the strategy of searching over extreme points (which the Simplex method exploits) at least conceivable.

*Proof*. Since extreme points $\Leftrightarrow$ vertices, we show that the number of vertices is finite.

Suppose there are $m$ linear inequalities. We need to pick $n$ linearly independent constraints. How many choices?

Since choosing $n$ (not necessarily linearly independent) constraints out of $m$ constraints has $\binom{m}{n}$ ways, there are at most $\binom{m}{n}$ ways of choosing $n$ linearly independent constraints.

Each such set of $n$ constraints yields at most one candidate vertex by solving $Ax = b \implies x = A^{-1}b$ (when the matrix is invertible), since the solution to a system of $n$ linearly independent equations in $n$ unknowns is unique.

Therefore, the number of vertices is at most $\binom{m}{n}$, which is finite. This completes the proof. $\blacksquare$

#### 9.2.5.2 Vertices of the LP Feasible Set

**Corollary 9.2 (Number of Vertices of the Feasible Set of LP)** Consider an LP in the canonical form:

$$
\min \; c^\top x \quad \text{s.t.} \quad Ax \leq b, \; x \geq 0.
$$

The feasible set $\{x \in \mathbb{R}^n : Ax \leq b, \; x \geq 0\}$ has at most $\binom{m+n}{n}$ vertices.

*Proof*. By the previous corollary, $\{x \in \mathbb{R}^n : \widetilde{A}x \leq \widetilde{b}\}$ has at most $\binom{d}{n}$ vertices, where $\widetilde{A} \in \mathbb{R}^{d \times n}$ and $\widetilde{b} \in \mathbb{R}^d$.

We need to write $\Omega = \{x : Ax \leq b,\; x \geq 0\}$ in this form. Let

$$
\widetilde{A} = \begin{pmatrix} -I_n \\ A \end{pmatrix} \in \mathbb{R}^{(m+n) \times n}, \quad \widetilde{b} = \begin{pmatrix} 0 \\ b \end{pmatrix},
$$

where $-I_n$ is the negative identity matrix (encoding $x \geq 0$). Then $\Omega = \{x : \widetilde{A}x \leq \widetilde{b}\}$.

Thus, the number of vertices of $\Omega$ is at most $\binom{m+n}{n}$. This completes the proof. $\blacksquare$

**Question:** Can you identify one extreme point of $\Omega$? The zero vector $\vec{0}$ is an extreme point (it is the solution to $-I \cdot x \leq 0$ with $n$ linearly independent binding constraints).

We know that the number of extreme points is finite, but do they always exist? The answer depends on the geometry of the polyhedron — specifically, on whether it contains an entire line.

### 9.2.6 Existence of Extreme Points

#### 9.2.6.1 Containing a Line

Before we can state when extreme points exist, we need to identify the one situation where they fail to exist: when the polyhedron extends infinitely in some direction and its “reverse” – that is, when it contains an entire line.

**Definition 9.5 (Contain a Line)** A polyhedron $P$ **contains a line** if there exist $x \in P$ and $d \in \mathbb{R}^n$, $d \neq 0$, such that

$$
x + \lambda d \in P \quad \forall\, \lambda \in \mathbb{R}.
$$

A polyhedron contains a line when it extends infinitely in both directions along some direction $d$. For example, a half-plane in $\mathbb{R}^2$ contains lines parallel to its boundary. This condition is the obstruction to having extreme points: if the polyhedron contains a line, no point on that line can be an extreme point.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/polyhedron-line.svg)

Figure 9.4: Left — An unbounded polyhedron that contains a line (the dotted red line extends infinitely in both directions). Right — Bounded polyhedra that do not contain a line.

#### 9.2.6.2 Existence Theorem

We have seen that extreme points and vertices are equivalent for polyhedra ([Theorem 9.1](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#thm-equivalence-extreme-vertex)), and that their number is finite ([Corollary 9.1](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#cor-finite-extreme-points)). But do they always exist? The following theorem precisely characterizes when a polyhedron has extreme points. It tells us that extreme points exist unless the polyhedron contains an entire line – a condition that is automatically satisfied when the polyhedron is bounded or when nonnegativity constraints are present (as in LP canonical form).

**Theorem 9.2 (Existence of Extreme Points)** Consider a nonempty polyhedron $P$.

$$
P \text{ has at least one extreme point} \iff P \text{ does not contain a line.}
$$

This theorem gives a clean necessary and sufficient condition for the existence of extreme points. In practice, most polyhedra arising in LP do not contain lines (e.g., nonnegativity constraints $x \geq 0$ prevent any line from lying in the feasible set), so extreme points almost always exist.

*Proof*. Write $P = \{x : a_i^\top x \leq b_i, \; i = 1, \ldots, m\}$ with $A$ the matrix of rows $a_i^\top$.

**($\Rightarrow$) Has extreme point $\Rightarrow$ contains no line.** We prove the contrapositive. If $P$ contains a line, there exist $x_0 \in P$ and $d \neq 0$ with $x_0 + \lambda d \in P$ for all $\lambda \in \mathbb{R}$. This forces $Ad = 0$ (otherwise, sending $\lambda \to \pm\infty$ violates some constraint). But then for **any** $\bar{x} \in P$ and any $\lambda$, we have $A(\bar{x} + \lambda d) = A\bar{x} + \lambda Ad = A\bar{x} \leq b$, so $\bar{x} + \lambda d \in P$. Writing $\bar{x} = \tfrac{1}{2}(\bar{x} + \epsilon d) + \tfrac{1}{2}(\bar{x} - \epsilon d)$ with both summands in $P$ and distinct, we see $\bar{x}$ is not an extreme point. Since $\bar{x}$ was arbitrary, $P$ has no extreme points.

**($\Leftarrow$) Contains no line $\Rightarrow$ has extreme point.** Since $P$ contains no line, $\ker(A) = \{0\}$, i.e., $A$ has full column rank $n$. We construct a vertex by an iterative procedure.

Pick any $\bar{x} \in P$ and let $I(\bar{x}) = \{i : a_i^\top \bar{x} = b_i\}$. If the binding constraints $\{a_i : i \in I(\bar{x})\}$ have rank $n$, then $\bar{x}$ is already a vertex and we are done. Otherwise, their rank is some $k < n$.

Since $k < n$, there exists $d \neq 0$ with $a_i^\top d = 0$ for all $i \in I(\bar{x})$. Since $\operatorname{rank}(A) = n$, we know $Ad \neq 0$, so some constraint $j \notin I(\bar{x})$ has $a_j^\top d \neq 0$. Replacing $d$ by $-d$ if necessary, assume there exists such a $j$ with $a_j^\top d > 0$. Define

$$
\lambda^* = \min_{\substack{i \notin I(\bar{x}) \\ a_i^\top d > 0}} \frac{b_i - a_i^\top \bar{x}}{a_i^\top d} > 0
$$

and set $\bar{x}' = \bar{x} + \lambda^* d$. The point $\bar{x}'$ is feasible: for $i \in I(\bar{x})$, we have $a_i^\top \bar{x}' = b_i$; for $i \notin I(\bar{x})$ with $a_i^\top d \leq 0$, the constraint only gets more slack; and for $i \notin I(\bar{x})$ with $a_i^\top d > 0$, the ratio test ensures $a_i^\top \bar{x}' \leq b_i$.

Crucially, $\bar{x}'$ has at least one **new** binding constraint $j^*$ (the minimizer). Since $a_{j^*}^\top d > 0$ while $a_i^\top d = 0$ for all $i \in I(\bar{x})$, the vector $a_{j^*}$ is linearly independent of $\{a_i : i \in I(\bar{x})\}$. So $\operatorname{rank}\{a_i : i \in I(\bar{x}')\} \geq k + 1$.

Repeat, increasing the rank by at least 1 each step. After at most $n - k$ steps we obtain a point with $n$ linearly independent binding constraints – a vertex. $\blacksquare$

**Corollary 9.3** Every **polytope** (bounded polyhedron) contains at least one extreme point.

Since a polytope is bounded, it cannot contain a line, so the theorem above immediately applies. This corollary guarantees that bounded LP feasible regions always have vertices to search over.

## 9.3 Fundamental Theorem of LP

The equivalence of extreme points and vertices ([Theorem 9.1](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#thm-equivalence-extreme-vertex)), combined with the existence theorem ([Theorem 9.2](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#thm-existence-extreme-points)), sets the stage for the most important structural result in linear programming. We now arrive at the central result of LP geometry. The Fundamental Theorem tells us that the search for an optimal solution can be restricted to the extreme points of the feasible polyhedron – a finite set. This is the theoretical justification for the simplex method and explains why linear programs, despite having infinitely many feasible points, can be solved by examining a finite number of candidates.

**Theorem 9.3 (Fundamental Theorem of LP (Geometric Version))** Suppose the polyhedron $P = \{x : \widetilde{A}x \leq \widetilde{b}\}$ has an extreme point. Consider the LP:

$$
\min_x \; c^\top x \quad \text{s.t.} \quad x \in P.
$$

If there exists an optimal solution, there also exists an **optimal solution which is an extreme point**.

This is the most important structural result about linear programs. It says that we never need to look at interior points of the feasible region — the optimum is always attained at a corner. Geometrically, a linear objective “tilts” the feasible polyhedron, and the lowest point under this tilt is always a vertex (or a face containing a vertex).

**Implication:** It suffices to only search among the extreme points of the feasible polyhedron $\{x : Ax \leq b,\; x \geq 0\}$. This is the core idea behind the **Simplex method**!

We call this the **geometric version** because it is stated in terms of extreme points of a polyhedron in inequality form. Later in this chapter ([Section 9.5.6](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#sec-algebraic-ftlp)), after introducing the equational form and basic feasible solutions (BFS), we will restate this result as the **Algebraic Fundamental Theorem of LP**: if the LP has an optimal solution, it has an optimal *BFS*. The algebraic version is more directly useful for algorithm design, since BFS have a concrete computational representation (a basis $B$ and a solution $x_B = \bar{A}_B^{-1}b$), which is exactly what the simplex method manipulates.

### 9.3.1 Proof

The proof strategy is to show that the set of optimal solutions $Q$ is itself a polyhedron with at least one extreme point, and that any extreme point of $Q$ must also be an extreme point of $P$.

*Proof*. **Proof of the Fundamental Theorem.**

Assume there exists at least an optimal solution. The set of all optimal solutions is

$$
Q = \{x : c^\top x = f^*\} \cap \{x : \widetilde{A}x \leq \widetilde{b}\} \neq \emptyset,
$$

where $f^*$ is the optimal value.

In addition, $Q = \{x : c^\top x = f^*\} \cap P$ is a sub-polyhedron of $P$ (since $Q$ is a polyhedron and $Q \subseteq P$).

We have the following reasoning chain:

1. $P$ has an extreme point.
2. $\Rightarrow$ (by the Existence Theorem) $P$ does not contain a line.
3. $\Rightarrow$ (since $Q \subseteq P$) $Q$ does not contain a line.
4. $\Rightarrow$ (by the Existence Theorem) $Q$ has an extreme point, denoted by $x^*$.

***Idea of the proof:*** Since $x^* \in Q$, we have $x^* \in P$ and $(x^*)^\top c = f^*$. If we can show that $x^*$ is also an extreme point of $P$, then we conclude the proof.

To see this, suppose $x^*$ is *not* an extreme point of $P$. Then there exist $y \neq x^*$ and $z \neq x^*$, and $\lambda \in [0,1]$ such that

$$
x^* = \lambda y + (1-\lambda) z.
$$

Then

$$
f^* = c^\top x^* = \lambda \cdot c^\top y + (1-\lambda) \cdot c^\top z.
$$

Since $f^*$ is the optimal value and $y, z \in P$ are feasible, we have $f^* \leq c^\top y$ and $f^* \leq c^\top z$. Substituting these lower bounds gives

$$
f^* = \lambda \cdot c^\top y + (1-\lambda) \cdot c^\top z \geq \lambda f^* + (1-\lambda) f^* = f^*.
$$

Since we have $f^*$ on both sides, the inequality must hold with equality, which forces $c^\top y = f^*$ and $c^\top z = f^*$.

This means that $y$ and $z$ are both optimal solutions of the LP as well. Thus $y, z \in Q$.

What did we show? We showed that $x^* \in Q$ can be written as $x^* = \lambda y + (1-\lambda) z$ for $y, z \neq x^*$ and $y, z \in Q$.

$\Rightarrow$ $x^*$ is **not** an extreme point of $Q$. **Contradiction** (since $x^*$ was chosen as an extreme point of $Q$).

Therefore, $x^*$ is an extreme point of $P$ and we are done. $\blacksquare$

### 9.3.2 Main Message

When solving an LP, there are **three cases only**:

1. **LP is infeasible**: $\Omega = \emptyset$.
2. **LP is unbounded** ($-\infty$): $\Omega$ is unbounded, $\{x : c^\top x = t\} \cap \Omega \neq \emptyset$ for any sufficiently small $t$ (as $t \to -\infty$).
3. **LP has an optimal value** $f^*$ and at least one optimal solution $x^*$ which is a **vertex (extreme point)**.

Thus, when looking for an optimal solution, it suffices to examine **only the extreme points (vertices)**.

The following interactive figure brings this result to life. Drag the slider to rotate the objective direction $c$: the parallel level-set lines ($c^\top x = \text{const}$) sweep across the polytope, and the **optimal is always at a vertex** — no matter where $c$ points. As the direction rotates, the optimal vertex jumps from corner to corner.

### Fundamental Theorem of LP Explorer

Polytope: x <sub>1</sub> +x <sub>2</sub> ≤ 4,   x <sub>1</sub> −x <sub>2</sub> ≤ 2,   −x <sub>1</sub> +x <sub>2</sub> ≤ 2,   x ≥ 0.   Maximize c <sup>T</sup> x over the polytope.

30°

**Objective:** max c <sup>T</sup> x   with c = (0.87, 0.50)  
**Vertex values:**  (0,0): 0.00   (2,0): 1.73   **(3,1): 3.10 ← optimal**   (1,3): 2.37   (0,2): 1.00    
**f\* = 3.10** at vertex **(3,1)**  —  The optimal is always at a vertex.

This leads to an algorithm for LP: **enumerate all extreme points and find the best one**. But how?

### 9.3.3 Algorithm: Enumerating Extreme Points

The Fundamental Theorem ([Theorem 9.3](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#thm-fundamental-lp)) tells us that we only need to search among extreme points. The simplest approach is brute-force enumeration: check every possible vertex. We want to check all extreme points of $\Omega = \{x : Ax \leq b,\; x \geq 0\}$.

We first rewrite $\Omega$ as $\Omega = \{x : \widetilde{A}x \leq \widetilde{b}\}$, where

$$
\widetilde{A} = \begin{pmatrix} -I_n \\ A \end{pmatrix} \in \mathbb{R}^{(m+n) \times n}, \quad \widetilde{b} = \begin{pmatrix} 0 \\ b \end{pmatrix} \in \mathbb{R}^{m+n}.
$$

This gives us $(m+n)$ inequalities.

An extreme point of $\Omega$ corresponds to $n$ linear inequalities among $\widetilde{A}x \leq \widetilde{b}$ that are **binding** and **linearly independent**.

So the algorithm enumerates all subsets of $n$ linear inequalities and checks if there is a corresponding extreme point.

Let $I \subseteq [m+n]$ with $|I| = n$. We write $\widetilde{A}_I = (\widetilde{a}_i^\top)_{i \in I}$ and $\widetilde{b}_I = (\widetilde{b}_j)_{j \in I}$ as the submatrix of $\widetilde{A}$ and subvector of $\widetilde{b}$ with row index in $I$.

ImportantAlgorithm: Check All Extreme Points

**For** each subset $I \subseteq [m+n]$ with $|I| = n$:

1. **Check independence.** If $\widetilde{A}_I$ is invertible (i.e., the rows of $\widetilde{A}_I$ are linearly independent):
	1. **Solve.** Compute the candidate extreme point: 
		$$
		x^{(I)} = \widetilde{A}_I^{-1}\,\widetilde{b}_I.
		$$
		2. **Check feasibility.** If $x^{(I)} \in \Omega$ (i.e., $\widetilde{A}\,x^{(I)} \leq \widetilde{b}$), set $f^{(I)} = c^\top x^{(I)}$. Otherwise, set $f^{(I)} = +\infty$.
2. If $\widetilde{A}_I$ is not invertible, set $f^{(I)} = +\infty$.

**Return:** $I^* = \arg\min_{I} f^{(I)}$,    $\;x^* = x^{(I^*)}$,    $\;f^* = f^{(I^*)}$.

TipRemark: Complexity

Unfortunately, $\binom{m+n}{n}$ is **exponential** in $n$. In particular, $\binom{m+n}{n} \geq n^n$.

For example, the number of extreme points of $\{x : 0 \leq x \leq \mathbf{1}\}$ (the unit hypercube) is $2^n$.

The idea of **smartly searching over vertices** (rather than enumerating all of them) leads to the **Simplex method**.

The vertex enumeration algorithm makes the Fundamental Theorem concrete, but its exponential complexity ($\binom{m+n}{n}$ subsets to check) makes it impractical for all but the smallest LPs. This motivates a smarter approach: rather than examining every vertex, we want an algorithm that navigates from vertex to vertex while improving the objective at each step. The simplex method does exactly this — and to develop it, we need to reformulate the LP in a way that makes vertex-to-vertex moves algebraically transparent.

## 9.4 From Canonical Form to Equational Form

### 9.4.1 Recap: Canonical Form

The **canonical form** of a linear program is

$$
\min_{x \in \mathbb{R}^n} \; c^\top x \quad \text{s.t.} \quad Ax \leq b, \; x \geq 0,
$$

where $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$, and $c \in \mathbb{R}^n$. The feasible polyhedron is $P = \{x \in \mathbb{R}^n : Ax \leq b, \; x \geq 0\}$. This form is convenient for geometric visualization: the constraints $Ax \leq b$ and $x \geq 0$ carve out a polyhedron in $\mathbb{R}^n$.

However, for algebraic manipulation – and in particular for the simplex method – it is much more convenient to work with **equalities** rather than inequalities. We achieve this by introducing slack variables.

### 9.4.2 Slack Variables

Each inequality constraint $a_i^\top x \leq b_i$ can be converted to an equality by introducing a **slack variable** $s_i \geq 0$ that measures the gap between the right-hand side and the left-hand side:

$$
s_i = b_i - a_i^\top x = b_i - \sum_{j=1}^{n} a_{ij} x_j, \quad i = 1, 2, \ldots, m.
$$

In vector form, this is simply

$$
s = b - Ax.
$$

The constraint $a_i^\top x \leq b_i$ holds if and only if $s_i \geq 0$. When $s_i = 0$, the $i$ -th constraint is **binding** (tight); when $s_i > 0$, there is “slack” in the constraint.

### 9.4.3 The Augmented System

We now define the **augmented decision variable**, **augmented cost vector**, and **augmented constraint matrix**:

$$
\bar{x} = \begin{pmatrix} x \\ s \end{pmatrix} = \begin{pmatrix} x_1 \\ \vdots \\ x_n \\ s_1 \\ \vdots \\ s_m \end{pmatrix} \in \mathbb{R}^{n+m}, \qquad \bar{c} = \begin{pmatrix} c \\ 0 \end{pmatrix} \in \mathbb{R}^{n+m}, \qquad \bar{A} = \begin{pmatrix} A & I_m \end{pmatrix} \in \mathbb{R}^{m \times (n+m)}.
$$

The $i$ -th component of $\bar{x}$ is

$$
\bar{x}_i = \begin{cases} x_i & \text{if } i \in [n], \\ s_{i-n} & \text{if } i > n. \end{cases}
$$

**Definition 9.6 (Definition (Equational Form of LP))** The **equational form** of the linear program $\min c^\top x$ subject to $Ax \leq b$, $x \geq 0$ is

$$
\min_{\bar{x} \in \mathbb{R}^{n+m}} \; \bar{c}^\top \bar{x} \quad \text{s.t.} \quad \bar{A}\bar{x} = b, \; \bar{x} \geq 0, \tag{9.1}
$$

where $\bar{A} = (A \mid I_m) \in \mathbb{R}^{m \times (n+m)}$, $\bar{c} = (c^\top, 0^\top)^\top \in \mathbb{R}^{n+m}$, and $\bar{x} = (x^\top, s^\top)^\top \in \mathbb{R}^{n+m}$.

**Why does this work?** Since $s = b - Ax$, we have $Ax + Is = b$, which is $\bar{A}\bar{x} = b$. The nonnegativity $\bar{x} \geq 0$ encodes both $x \geq 0$ and $s \geq 0$ (i.e., $Ax \leq b$). The objective $\bar{c}^\top \bar{x} = c^\top x + 0^\top s = c^\top x$ is unchanged.

The equational form polyhedron is

$$
P_{\text{eq}} = \{\bar{x} \in \mathbb{R}^{n+m} : \bar{A}\bar{x} = b, \; \bar{x} \geq 0\}.
$$

TipCanonical vs. Equational Form

| **Constraints** | $Ax \leq b$, $x \geq 0$ | $\bar{A}\bar{x} = b$, $\bar{x} \geq 0$ |
| --- | --- | --- |
| **Variables** | $x \in \mathbb{R}^n$ | $\bar{x} \in \mathbb{R}^{n+m}$ |
| **Advantage** | Easy to visualize the polyhedron | Easy to manipulate the linear equations |
| **Use case** | Geometric arguments | Simplex method and algebraic proofs |

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/slack-variables.svg)

Figure 9.5: A 2D LP in canonical form (left) and its equational form interpretation (right). Slack variables measure the distance from each constraint boundary. At a vertex, the binding constraints ( s i = 0 s\_i = 0 ) identify which constraints hold with equality.

### 9.4.4 Why Equational Form?

Why go through the trouble of introducing slack variables? The key insight from the [LP geometry discussion above](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#four-cases) is:

> $x_0 \in \mathbb{R}^n$ is an extreme point of $P = \{x : \widetilde{A}x \leq \widetilde{b}\}$ if and only if $n$ linearly independent inequality constraints are binding at $x_0$.

Recall that $\widetilde{A} = \binom{-I_n}{A}$ and $\widetilde{b} = \binom{0}{b}$, so the rows $\widetilde{a}_j = -e_j$ for $j = 1, \ldots, n$ and $\widetilde{a}_{n+i} = a_i$ for $i = 1, \ldots, m$. When an inequality $\widetilde{a}_i^\top x \leq \widetilde{b}_i$ is binding at $x_0$, the corresponding component of $\bar{x}$ is zero:

- If $i \in \{1, \ldots, n\}$: binding means $-e_i^\top x = 0$, i.e., $x_i = 0 = \bar{x}_i$.
- If $i \in \{n+1, \ldots, n+m\}$: binding means $a_{i-n}^\top x = b_{i-n}$, i.e., $s_{i-n} = b_{i-n} - a_{i-n}^\top x = 0 = \bar{x}_i$.

**Conclusion:** In the equational form, binding constraints correspond to components of $\bar{x}$ that are zero. This simple observation is the gateway to the concept of basic feasible solutions.

## 9.5 Basic Solutions and Basic Feasible Solutions

### 9.5.1 Block Matrix Computation

Before defining basic solutions, we review a useful fact from linear algebra. Let $A \in \mathbb{R}^{m \times n}$ (with $m \leq n$) and $b \in \mathbb{R}^m$. Let $\mathcal{I} \subseteq [n]$ with $|\mathcal{I}| = \ell$ be an index set. Write $A_\mathcal{I} \in \mathbb{R}^{m \times \ell}$ for the submatrix of $A$ consisting of columns indexed by $\mathcal{I}$, and $x_\mathcal{I} \in \mathbb{R}^\ell$ for the subvector of $x$ with entries in $\mathcal{I}$. Let $\mathcal{I}^c = [n] \setminus \mathcal{I}$ be the complement. Then

$$
Ax = A_\mathcal{I} \, x_\mathcal{I} + A_{\mathcal{I}^c} \, x_{\mathcal{I}^c}.
$$

If $|\mathcal{I}| = m$ and $A_\mathcal{I}$ is invertible, and if we set $x_{\mathcal{I}^c} = 0$, then $Ax = b$ reduces to $A_\mathcal{I} x_\mathcal{I} = b$, giving $x_\mathcal{I} = A_\mathcal{I}^{-1} b$. This is the core computation behind basic solutions.

### 9.5.2 Basic Solution

Consider the equational form system $\bar{A}\bar{x} = b$ with $\bar{A} \in \mathbb{R}^{m \times (n+m)}$, $\bar{x} \in \mathbb{R}^{n+m}$, $b \in \mathbb{R}^m$, and $\operatorname{rank}(\bar{A}) = m$.

**Definition 9.7 (Definition (Basic Solution))** Let $B = \{i_1, i_2, \ldots, i_m\} \subseteq [n+m]$ be an index set such that the columns $\bar{a}_{i_1}, \bar{a}_{i_2}, \ldots, \bar{a}_{i_m}$ of $\bar{A}$ are linearly independent (i.e., $\bar{A}_B \in \mathbb{R}^{m \times m}$ is invertible). Define

$$
x_B = \bar{A}_B^{-1} b, \qquad \bar{x}^* = \begin{pmatrix} x_B \\ 0 \end{pmatrix}, \tag{9.2}
$$

where the entries of $\bar{x}^*$ corresponding to indices in $B$ are set to $x_B$, and all other entries are zero. Then $\bar{x}^*$ is called a **basic solution** to $\bar{A}\bar{x} = b$ with **basic variables** $x_B = \{x_{i_1}, \ldots, x_{i_m}\}$.

The set $B$ is called the **basis**, and $N = [n+m] \setminus B$ is the **non-basic** index set. The variables $x_N$ are called **non-basic variables**.

The idea is simple: we select $m$ linearly independent columns of $\bar{A}$, set all other variables to zero, and solve the resulting $m \times m$ system.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/basic-solutions-block.svg)

Figure 9.6: Block structure of a basic solution. We select m columns of the augmented matrix (the basis), set the remaining variables to zero, and solve the square system.

### 9.5.3 Basic Feasible Solution

A basic solution need not be feasible for the LP – the values $x_B = \bar{A}_B^{-1}b$ might contain negative entries. When the basic solution is also feasible, we get a BFS.

**Definition 9.8 (Definition (Basic Feasible Solution))** A basic solution ([Equation 9.2](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#eq-basic-solution)) $\bar{x}^*$ is called a **basic feasible solution (BFS)** if $\bar{x}^* \geq 0$, i.e., if $x_B = \bar{A}_B^{-1} b \geq 0$.

That is, a BFS is a basic solution that is feasible for the equational form LP:

$$
\min_{\bar{x}} \; \bar{c}^\top \bar{x} \quad \text{s.t.} \quad \bar{A}\bar{x} = b, \; \bar{x} \geq 0.
$$

When we talk about BFS, we **always** work in the equational form.

### 9.5.4 Worked Example

Consider the LP (in canonical form):

$$
\min \; -x_2 \quad \text{s.t.} \quad -x_1 + x_2 \leq 1, \quad x_1 + x_2 \leq 2, \quad x_1 \geq 0, \quad x_2 \geq 0.
$$

Here $n = 2$, $m = 2$. The equational form has

$$
\bar{c} = \begin{pmatrix} 0 \\ -1 \\ 0 \\ 0 \end{pmatrix}, \quad b = \begin{pmatrix} 1 \\ 2 \end{pmatrix}, \quad \bar{A} = \begin{pmatrix} -1 & 1 & 1 & 0 \\ 1 & 1 & 0 & 1 \end{pmatrix}.
$$

We enumerate all possible bases $B \subseteq \{1,2,3,4\}$ with $|B| = 2$:

| $\{1,2\}$ | $\bigl(\begin{smallmatrix} -1 & 1 \\ 1 & 1 \end{smallmatrix}\bigr)$ | $\bigl(\begin{smallmatrix} 0.5 \\ 1.5 \end{smallmatrix}\bigr)$ | $(0.5,\, 1.5,\, 0,\, 0)$ | Yes — BFS (*a*) |
| --- | --- | --- | --- | --- |
| $\{1,3\}$ | $\bigl(\begin{smallmatrix} -1 & 1 \\ 1 & 0 \end{smallmatrix}\bigr)$ | $\bigl(\begin{smallmatrix} 2 \\ 3 \end{smallmatrix}\bigr)$ | $(2,\, 0,\, 3,\, 0)$ | Yes — BFS (*b*) |
| $\{1,4\}$ | $\bigl(\begin{smallmatrix} -1 & 0 \\ 1 & 1 \end{smallmatrix}\bigr)$ | $\bigl(\begin{smallmatrix} -1 \\ 3 \end{smallmatrix}\bigr)$ | $(-1,\, 0,\, 0,\, 3)$ | **No** ($x_1 < 0$, point *c*) |
| $\{2,3\}$ | $\bigl(\begin{smallmatrix} 1 & 1 \\ 1 & 0 \end{smallmatrix}\bigr)$ | $\bigl(\begin{smallmatrix} 2 \\ -1 \end{smallmatrix}\bigr)$ | $(0,\, 2,\, -1,\, 0)$ | **No** ($s_1 < 0$) |
| $\{2,4\}$ | $\bigl(\begin{smallmatrix} 1 & 0 \\ 1 & 1 \end{smallmatrix}\bigr)$ | $\bigl(\begin{smallmatrix} 1 \\ 1 \end{smallmatrix}\bigr)$ | $(0,\, 1,\, 0,\, 1)$ | Yes — BFS (*d*) |
| $\{3,4\}$ | $\bigl(\begin{smallmatrix} 1 & 0 \\ 0 & 1 \end{smallmatrix}\bigr)$ | $\bigl(\begin{smallmatrix} 1 \\ 2 \end{smallmatrix}\bigr)$ | $(0,\, 0,\, 1,\, 2)$ | Yes — BFS (*e*) |

The BFS are exactly the extreme points (vertices) of the feasible polytope.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/bfs-example.svg)

Figure 9.7: BFS enumeration for the example LP. Green points are BFS (feasible basic solutions = extreme points). The red point is a basic solution that is infeasible.

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch14-vertex-bfs.svg)

Figure 9.8: The vertex–BFS correspondence. Each vertex v i v\_i of the polytope (left, geometric view) corresponds to a basic feasible solution with a specific set of basic and nonbasic variables (right, algebraic view).

### 9.5.5 Extreme Point = Vertex = BFS

We have now defined basic feasible solutions algebraically through the equational form ([Equation 9.1](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#eq-equational-form)). The central question is: how do BFS relate to the geometric notions of extreme points and vertices established [earlier in this chapter](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#four-cases)? We proved there that extreme points and vertices are equivalent for polyhedra in inequality form. We now extend this equivalence to include BFS in the equational form.

**Theorem 9.4 (Theorem (Equivalence of Extreme Point, Vertex, and BFS))** Consider the equational form polyhedron

$$
P_{\text{eq}} = \{\bar{x} \in \mathbb{R}^{n+m} : \bar{A}\bar{x} = b, \; \bar{x} \geq 0\},
$$

where $\bar{A} \in \mathbb{R}^{m \times (n+m)}$ with $\operatorname{rank}(\bar{A}) = m$. For any $\bar{x}^* \in P_{\text{eq}}$, the following are equivalent:

1. $\bar{x}^*$ is an **extreme point** of $P_{\text{eq}}$.
2. $\bar{x}^*$ is a **vertex** of $P_{\text{eq}}$.
3. $\bar{x}^*$ is a **basic feasible solution** of the system $\bar{A}\bar{x} = b$, $\bar{x} \geq 0$.

$$
\text{Extreme point} \iff \text{Vertex} \iff \text{BFS}
$$

The equivalence (1) $\Leftrightarrow$ (2) was established [above](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#equivalence). The key new piece is the equivalence with BFS. The argument proceeds as follows.

**Vertex $\Rightarrow$ BFS.** We showed that $x_0$ is a vertex if and only if $n$ linearly independent constraints from $\widetilde{A}x \leq \widetilde{b}$ are binding at $x_0$. Let $\mathcal{I}$ be the index set of these binding constraints. In the equational form, binding means $\bar{x}_i = 0$ for $i \in \mathcal{I}$, with $|\mathcal{I}| = n$. Since $\bar{x} \in \mathbb{R}^{n+m}$ has $n+m$ components and $n$ of them are zero, at most $m$ components are nonzero. Let $\bar{\mathcal{I}} = [n+m] \setminus \mathcal{I}$ be the complement (the indices of potentially nonzero entries), so $|\bar{\mathcal{I}}| = m$. Since the binding constraints are linearly independent, the columns $\bar{A}_{\bar{\mathcal{I}}}$ are linearly independent (this follows from the relationship between the row space of $\widetilde{A}_\mathcal{I}$ and the column space of $\bar{A}_{\bar{\mathcal{I}}}$). Setting $B = \bar{\mathcal{I}}$ gives $\bar{A}_B$ invertible, $x_N = 0$, and $x_B = \bar{A}_B^{-1}b$ – exactly a basic solution. Feasibility ($\bar{x} \geq 0$) is inherited from $\bar{x}^* \in P_{\text{eq}}$.

**BFS $\Rightarrow$ Vertex.** Conversely, if $\bar{x}^*$ is a BFS with basis $B$, then $x_N = 0$ means $n$ components of $\bar{x}$ are zero. These correspond to $n$ binding inequality constraints (from the nonnegativity constraints $\bar{x} \geq 0$). The linear independence of the columns of $\bar{A}_B$ translates to the linear independence of these binding constraint normals, so $\bar{x}^*$ is a vertex.

### 9.5.6 Algebraic Fundamental Theorem of LP

The Fundamental Theorem of LP can now be restated in purely algebraic terms, using the language of BFS.

**Theorem 9.5 (Theorem (Algebraic Fundamental Theorem of LP))** Consider an LP in equational form:

$$
\min_{\bar{x} \in \mathbb{R}^{n+m}} \; \bar{c}^\top \bar{x} \quad \text{s.t.} \quad \bar{A}\bar{x} = b, \; \bar{x} \geq 0,
$$

where $\bar{A} \in \mathbb{R}^{m \times (n+m)}$ has full row rank ($\operatorname{rank}(\bar{A}) = m$) and the LP is feasible.

Then if the LP has an optimal solution, it has an **optimal BFS**.

*Proof*. By the geometric Fundamental Theorem ([Theorem 9.3](https://zhuoranyang.github.io/sds431-notes/lectures/09-lp-formulation-geometry.html#thm-fundamental-lp)), if $P_{\text{eq}}$ has an extreme point and the LP has an optimal solution, then it has an optimal extreme point. The equational form polyhedron $P_{\text{eq}} = \{\bar{x} : \bar{A}\bar{x} = b, \bar{x} \geq 0\}$ does not contain a line (the nonnegativity constraints $\bar{x} \geq 0$ prevent this), so $P_{\text{eq}}$ has at least one extreme point (by the Existence Theorem). By the equivalence theorem above, extreme points of $P_{\text{eq}}$ are exactly the BFS. Therefore, the LP has an optimal BFS. $\blacksquare$

**Corollary 9.4 (Corollary (Finite Number of BFS))** The number of basic feasible solutions is at most

$$
\binom{n+m}{m},
$$

which is finite (though potentially exponential in $m$).

*Proof*. A BFS corresponds to choosing a basis $B \subseteq [n+m]$ with $|B| = m$. The number of such choices is $\binom{n+m}{m}$, and each choice yields at most one basic solution (since $\bar{A}_B$ being invertible gives a unique solution $x_B = \bar{A}_B^{-1}b$). $\blacksquare$

### 9.5.7 Why Is the Algebraic Characterization Powerful?

The Algebraic Fundamental Theorem and the finiteness corollary together reveal a profound structural insight: **they transform a continuous optimization problem into a combinatorial one.**

Without this result, solving an LP would mean searching over an infinite, continuous feasible region – a daunting task. The Algebraic Fundamental Theorem tells us that we can instead restrict attention to the basic feasible solutions, which are completely characterized by algebraic data: a BFS is determined by choosing $m$ linearly independent columns of $A$ (a basis $B$) and solving the system $x_B = A_B^{-1}b$. The Corollary further guarantees that the number of such candidates is finite – at most $\binom{n+m}{m}$.

This suggests a naïve algorithm: enumerate all $\binom{n+m}{m}$ bases, check which ones give feasible solutions ($x_B = A_B^{-1}b \geq 0$), and return the one with the smallest objective value. While correct, this brute-force approach is hopelessly inefficient – the number of candidates is exponential in $m$. For instance, the unit hypercube $\{x \in \mathbb{R}^n : 0 \leq x \leq \mathbf{1}\}$ has $2^n$ vertices.

The key question becomes: **can we search over BFS intelligently, without examining all of them?** The answer is the **simplex method**, which we develop in the [next chapter](https://zhuoranyang.github.io/sds431-notes/lectures/10-simplex-method.html). Instead of enumerating all BFS, the simplex method starts at one BFS and moves to an **adjacent** BFS (one that differs by exactly one basic variable) that has a strictly lower objective value. Each such move is called a **pivot**. Since the objective strictly decreases at each step (in the nondegenerate case) and there are finitely many BFS, the algorithm must terminate at an optimal BFS.

TipThe Road to Simplex

$$
\text{Vertices} = \text{BFS} \quad \xrightarrow{\text{finitely many}} \quad \text{combinatorial search} \quad \xrightarrow{\text{smart pivoting}} \quad \text{simplex method}
$$

The Algebraic Fundamental Theorem provides the foundation; the simplex method provides the efficient search strategy.

### 9.5.8 Caratheodory’s Theorem

As a beautiful application of the Fundamental Theorem, we can prove Caratheodory’s theorem – a classical result in convex geometry.

**Theorem 9.6 (Theorem (Caratheodory’s Theorem))** Let $x_1, x_2, \ldots, x_n$ be $n$ points in $\mathbb{R}^m$. Let $x_0 \in \operatorname{conv}(x_1, \ldots, x_n)$. Then there exist indices $i_1, \ldots, i_{m+1} \in [n]$ such that

$$
x_0 \in \operatorname{conv}(x_{i_1}, \ldots, x_{i_{m+1}}).
$$

That is, $x_0$ can be written as a convex combination of at most $m+1$ of the points.

*Proof*. Since $x_0 \in \operatorname{conv}(x_1, \ldots, x_n)$, we can write $x_0 = \sum_{i=1}^n t_i x_i$ with $\sum_{i=1}^n t_i = 1$ and $t_i \geq 0$. Let $t = (t_1, \ldots, t_n)^\top$ and $A = (x_1 \mid x_2 \mid \cdots \mid x_n) \in \mathbb{R}^{m \times n}$. Then the conditions become:

$$
At = x_0, \quad \mathbf{1}^\top t = 1, \quad t \geq 0.
$$

Consider the LP:

$$
\min_{t} \; 0 \quad \text{s.t.} \quad At = x_0, \; \mathbf{1}^\top t = 1, \; t \geq 0.
$$

This LP is feasible (by assumption) and bounded (the objective is constant). By the Algebraic Fundamental Theorem, it has an optimal BFS $t^*$. This BFS has at most $m + 1$ nonzero entries (since the constraint matrix $\binom{A}{\mathbf{1}^\top}$ has $m+1$ rows). Therefore, $x_0 = \sum_{i=1}^n t_i^* x_i$ is a convex combination using at most $m+1$ of the points. $\blacksquare$

## Summary

- **Equational form.** Any LP can be converted to equational (standard) form $\min c^\top x$ subject to $Ax = b$, $x \geq 0$ by introducing slack variables; this canonical form is the starting point for the simplex method.
- **Basic feasible solutions (BFS).** A BFS corresponds to selecting $m$ linearly independent columns of $A$ (a basis $B$) and setting $x_B = A_B^{-1}b \geq 0$, $x_N = 0$; geometrically, each BFS is a vertex of the feasible polyhedron.
- **Vertex–BFS equivalence.** The Algebraic Fundamental Theorem of LP establishes that vertices, extreme points, and basic feasible solutions are equivalent characterizations of the “corners” of the feasible polyhedron; if an LP has an optimal solution, it has one at a BFS.
- **From continuous to combinatorial.** The algebraic characterization reduces LP from searching over an infinite feasible region to searching over finitely many (at most $\binom{n+m}{m}$) basic feasible solutions – setting the stage for the simplex method in the [next chapter](https://zhuoranyang.github.io/sds431-notes/lectures/10-simplex-method.html).