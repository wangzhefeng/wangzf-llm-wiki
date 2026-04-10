---
source_type: web
title: "Chebyshev polynomials - Wikipedia"
author:
  - 
  - "[[Contributors to Wikimedia projects]]"
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://en.wikipedia.org/wiki/Chebyshev_polynomials"
published: 2003-02-18
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

![[250px-Chebyshev_Polynomials_of_the_First_Kind.svg.png]]

Plot of the first five T n Chebyshev polynomials (first kind)

![[250px-Chebyshev_Polynomials_of_the_Second_Kind.svg.png]]

Plot of the first five U n Chebyshev polynomials (second kind)

The **Chebyshev polynomials** are two sequences of [orthogonal polynomials](https://en.wikipedia.org/wiki/Orthogonal_polynomials "Orthogonal polynomials") related to the [cosine and sine functions](https://en.wikipedia.org/wiki/Trigonometric_functions "Trigonometric functions"), notated as ${\displaystyle T_{n}(x)}$ and ${\displaystyle U_{n}(x)}$. They can be defined in several equivalent ways, one of which starts with [trigonometric functions](https://en.wikipedia.org/wiki/Trigonometric_functions "Trigonometric functions"):

The **Chebyshev polynomials of the first kind** ${\displaystyle T_{n}}$ are defined by

$$
{\displaystyle T_{n}(\cos \theta )=\cos(n\theta ).}
$$

Similarly, the **Chebyshev polynomials of the second kind** ${\displaystyle U_{n}}$ are defined by

$$
{\displaystyle U_{n}(\cos \theta )\sin \theta ={\sin }{\big (}(n+1)\theta {\big )}.}
$$

That these expressions define polynomials in ${\displaystyle \cos \theta }$ is not obvious at first sight but can be shown using [de Moivre's formula](https://en.wikipedia.org/wiki/De_Moivre%27s_formula "De Moivre's formula") (see [below](#Trigonometric_definition)).

The Chebyshev polynomials *T <sub>n</sub>* are polynomials with the largest possible leading coefficient whose [absolute value](https://en.wikipedia.org/wiki/Absolute_value "Absolute value") on the [interval](https://en.wikipedia.org/wiki/Interval_\(mathematics\) "Interval (mathematics)") \[−1, 1\] is bounded by 1. They are also the "extremal" polynomials for many other properties.[^1]

In 1952, [Cornelius Lanczos](https://en.wikipedia.org/wiki/Cornelius_Lanczos "Cornelius Lanczos") showed that the Chebyshev polynomials are important in [approximation theory](https://en.wikipedia.org/wiki/Approximation_theory "Approximation theory") for the solution of linear systems;[^2] the [roots](https://en.wikipedia.org/wiki/Root_of_a_polynomial "Root of a polynomial") of *T <sub>n</sub>* (*x*), which are also called *[Chebyshev nodes](https://en.wikipedia.org/wiki/Chebyshev_nodes "Chebyshev nodes")*, are used as matching points for optimizing [polynomial interpolation](https://en.wikipedia.org/wiki/Polynomial_interpolation "Polynomial interpolation"). The resulting interpolation polynomial minimizes the problem of [Runge's phenomenon](https://en.wikipedia.org/wiki/Runge%27s_phenomenon "Runge's phenomenon") and provides an approximation that is close to the best polynomial approximation to a [continuous function](https://en.wikipedia.org/wiki/Continuous_function "Continuous function") under the [maximum norm](https://en.wikipedia.org/wiki/Maximum_norm "Maximum norm"), also called the " [minimax](https://en.wikipedia.org/wiki/Minimax "Minimax") " criterion. This approximation leads directly to the method of [Clenshaw–Curtis quadrature](https://en.wikipedia.org/wiki/Clenshaw%E2%80%93Curtis_quadrature "Clenshaw–Curtis quadrature").

These polynomials were named after [Pafnuty Chebyshev](https://en.wikipedia.org/wiki/Pafnuty_Chebyshev "Pafnuty Chebyshev").[^3] The letter T is used because of the alternative [transliterations](https://en.wikipedia.org/wiki/Transliteration "Transliteration") of the name *Chebyshev* as *Tchebycheff*, *Tchebyshev* (French) or *Tschebyschow* (German).

## Definitions

### Recurrence definition

The *Chebyshev polynomials of the first kind* can be defined by the recurrence relation

$$
{\displaystyle {\begin{aligned}T_{0}(x)&=1,\\T_{1}(x)&=x,\\T_{n+1}(x)&=2x\,T_{n}(x)-T_{n-1}(x).\end{aligned}}}
$$

The *Chebyshev polynomials of the second kind* can be defined by the recurrence relation

$$
{\displaystyle {\begin{aligned}U_{0}(x)&=1,\\U_{1}(x)&=2x,\\U_{n+1}(x)&=2x\,U_{n}(x)-U_{n-1}(x),\end{aligned}}}
$$
 which differs from the above only by the rule for *n=1*.

### Trigonometric definition

The Chebyshev polynomials of the first and second kind can be defined as the unique polynomials satisfying 
$$
{\displaystyle T_{n}(\cos \theta )=\cos(n\theta )\quad }
$$
 and 
$$
{\displaystyle U_{n}(\cos \theta )={\frac {{\sin }{\big (}(n+1)\theta {\big )}}{\sin \theta }},}
$$
 for *n* = 0, 1, 2, 3, ….

An equivalent way to state this is via exponentiation of a [complex number](https://en.wikipedia.org/wiki/Complex_number "Complex number"): given a complex number *z* = *a* + *bi* with absolute value of one, 
$$
{\displaystyle z^{n}=T_{n}(a)+ib\,U_{n-1}(a).}
$$

Chebyshev polynomials can also be defined in this form when studying [trigonometric polynomials](https://en.wikipedia.org/wiki/Trigonometric_polynomials "Trigonometric polynomials").[^4]

That ${\displaystyle \cos(nx)}$ is an ${\displaystyle n}$ th- [degree](https://en.wikipedia.org/wiki/Degree_of_a_polynomial "Degree of a polynomial") polynomial in ${\displaystyle \cos(x)}$ can be seen by observing that ${\displaystyle \cos(nx)}$ is the [real part](https://en.wikipedia.org/wiki/Complex_number "Complex number") of one side of [de Moivre's formula](https://en.wikipedia.org/wiki/De_Moivre%27s_formula "De Moivre's formula"): 
$$
{\displaystyle \cos n\theta +i\sin n\theta =(\cos \theta +i\sin \theta )^{n}.}
$$

The real part of the other side is a polynomial in ${\displaystyle \cos x}$ and ${\displaystyle \sin x}$, in which all powers of ${\displaystyle \sin x}$ are [even](https://en.wikipedia.org/wiki/Parity_\(mathematics\) "Parity (mathematics)") and thus replaceable through the identity ${\displaystyle \cos ^{2}x+\sin ^{2}x=1}$. By the same reasoning, ${\displaystyle \sin nx}$ is the [imaginary part](https://en.wikipedia.org/wiki/Complex_number "Complex number") of the polynomial, in which all powers of ${\displaystyle \sin x}$ are [odd](https://en.wikipedia.org/wiki/Parity_\(mathematics\) "Parity (mathematics)") and thus, if one factor of ${\displaystyle \sin x}$ is factored out, the remaining factors can be replaced to create a polynomial of degree ${\displaystyle n-1}$ in ${\displaystyle \cos x}$.

For ${\displaystyle x}$ outside the interval \[-1,1\], the above definition implies 
$$
{\displaystyle T_{n}(x)={\begin{cases}\cos(n\arccos x)&{\text{ if }}|x|\leq 1,\\\cosh(n\operatorname {arccosh} x)&{\text{ if }}x\geq 1,\\{(-1)^{n}\cosh }(n\operatorname {arccosh} (-x))&{\text{ if }}x\leq -1.\end{cases}}}
$$

### Commuting polynomials definition

Chebyshev polynomials can also be characterized by the following theorem:[^5]

If ${\displaystyle F_{n}(x)}$ is a family of monic polynomials with coefficients in a field of characteristic ${\displaystyle 0}$ such that ${\displaystyle \deg F_{n}(x)=n}$ and ${\displaystyle F_{m}{\bigl (}F_{n}(x){\bigr )}=F_{n}{\bigl (}F_{m}(x){\bigr )}}$ for all ${\displaystyle m}$ and ${\displaystyle n}$, then, up to a simple change of variables, either ${\displaystyle F_{n}(x)=x^{n}}$ for all ${\displaystyle n}$ or ${\displaystyle F_{n}(x)=2\cdot T_{n}{\bigl (}{\tfrac {1}{2}}x{\bigr )}}$ for all ${\displaystyle n}$.

### Pell equation definition

The Chebyshev polynomials can also be defined as the solutions to the [Pell equation](https://en.wikipedia.org/wiki/Pell_equation "Pell equation"): 
$$
{\displaystyle T_{n}(x)^{2}-(x^{2}-1)\,U_{n-1}(x)^{2}=1}
$$

in a [ring](https://en.wikipedia.org/wiki/Ring_\(mathematics\) "Ring (mathematics)") ⁠ ${\displaystyle R[x]}$ ⁠.[^6] Thus, they can be generated by the standard technique for Pell equations of taking powers of a fundamental solution: 
$$
{\displaystyle T_{n}(x)+U_{n-1}(x){\textstyle {\sqrt {x^{2}-1}}}={\bigl (}{\textstyle x+{\sqrt {x^{2}-1}}~\!}{\bigr )}^{n}.}
$$

### Generating functions

The [ordinary generating function](https://en.wikipedia.org/wiki/Generating_function "Generating function") for ${\displaystyle T_{n}}$ is 
$$
{\displaystyle \sum _{n=0}^{\infty }T_{n}(x)\,t^{n}={\frac {1-tx}{1-2tx+t^{2}}}.}
$$

There are several other [generating functions](https://en.wikipedia.org/wiki/Generating_function "Generating function") for the Chebyshev polynomials; the [exponential generating function](https://en.wikipedia.org/wiki/Exponential_generating_function "Exponential generating function") is 
$$
{\displaystyle {\begin{aligned}\sum _{n=0}^{\infty }T_{n}(x){\frac {t^{n}}{n!}}&={\tfrac {1}{2}}{\Bigl (}{\exp }{\Bigl (}t{\bigl (}{\textstyle x-{\sqrt {x^{2}-1}}~\!}{\bigr )}{\Bigr )}+{\exp }{\Bigl (}t{\bigl (}{\textstyle x+{\sqrt {x^{2}-1}}~\!}{\bigr )}{\Bigr )}{\Bigr )}\\&={e^{tx}\cosh }{\bigl (}{\textstyle t{\sqrt {x^{2}-1}}}~\!{\bigr )}.\end{aligned}}}
$$

The generating function relevant for 2-dimensional [potential theory](https://en.wikipedia.org/wiki/Potential_theory "Potential theory") and [multipole expansion](https://en.wikipedia.org/wiki/Cylindrical_multipole_moments "Cylindrical multipole moments") is 
$$
{\displaystyle \sum \limits _{n=1}^{\infty }T_{n}(x){\frac {t^{n}}{n}}=\ln \left({\frac {1}{\sqrt {1-2tx+t^{2}}}}\right).}
$$

The ordinary generating function for U <sub>n</sub> is 
$$
{\displaystyle \sum _{n=0}^{\infty }U_{n}(x)\,t^{n}={\frac {1}{1-2tx+t^{2}}},}
$$
 and the exponential generating function is 
$$
{\displaystyle \sum _{n=0}^{\infty }U_{n}(x){\frac {t^{n}}{n!}}=e^{tx}{\biggl (}{\cosh }{\bigl (}{\textstyle t{\sqrt {x^{2}-1}}~\!}{\bigr )}+{{\frac {x}{\sqrt {x^{2}-1}}}\sinh }{\bigl (}{\textstyle t{\sqrt {x^{2}-1}}~\!}{\bigr )}{\biggr )}.}
$$

## Relations between the two kinds of Chebyshev polynomials

The Chebyshev polynomials of the first and second kinds correspond to a complementary pair of [Lucas sequences](https://en.wikipedia.org/wiki/Lucas_sequence "Lucas sequence") ${\displaystyle {\tilde {V}}_{n}(P,Q)}$ and ${\displaystyle {\tilde {U}}_{n}(P,Q)}$ with parameters ${\displaystyle P=2x}$ and ${\displaystyle Q=1}$:

$$
{\displaystyle {\begin{aligned}{\tilde {U}}_{n}(2x,1)&=U_{n-1}(x),\\{\tilde {V}}_{n}(2x,1)&=2\,T_{n}(x).\end{aligned}}}
$$

It follows that they also satisfy a pair of mutual recurrence equations:[^7]

$$
{\displaystyle {\begin{aligned}T_{n+1}(x)&=x\,T_{n}(x)-(1-x^{2})\,U_{n-1}(x),\\U_{n+1}(x)&=x\,U_{n}(x)+T_{n+1}(x).\end{aligned}}}
$$

The second of these may be rearranged using the [recurrence definition](#Recurrence_definition) for the Chebyshev polynomials of the second kind to give: 
$$
{\displaystyle T_{n}(x)={\tfrac {1}{2}}{\big (}U_{n}(x)-U_{n-2}(x){\big )}.}
$$

Using this formula iteratively gives the sum formula: 
$$
{\displaystyle U_{n}(x)={\begin{cases}2\sum _{{\text{ odd }}j>0}^{n}T_{j}(x)&{\text{ for odd }}n.\\2\sum _{{\text{ even }}j\geq 0}^{n}T_{j}(x)-1&{\text{ for even }}n,\end{cases}}}
$$

while replacing ${\displaystyle U_{n}(x)}$ and ${\displaystyle U_{n-2}(x)}$ using the [derivative formula](#Differentiation_and_integration) for ${\displaystyle T_{n}(x)}$ gives the recurrence relationship for the derivative of ${\displaystyle T_{n}}$: 
$$
{\displaystyle 2T_{n}(x)={\frac {1}{n+1}},{\frac {\mathrm {d} }{\mathrm {d} x}}\,T_{n+1}(x)-{\frac {1}{n-1}}\,{\frac {\mathrm {d} }{\mathrm {d} x}}\,T_{n-1}(x),}
$$
 for ${\displaystyle n=2,3,\ldots }$.

This relationship is used in the [Chebyshev spectral method](https://en.wikipedia.org/wiki/Chebyshev_spectral_method "Chebyshev spectral method") of solving differential equations.

[Turán's inequalities](https://en.wikipedia.org/wiki/Tur%C3%A1n%27s_inequalities "Turán's inequalities") for the Chebyshev polynomials are:[^8] 
$$
{\displaystyle {\begin{aligned}T_{n}(x)^{2}-T_{n-1}(x)\,T_{n+1}(x)&=1-x^{2}>0&&{\text{ for }}-1<x<1&&{\text{ and }}\\U_{n}(x)^{2}-U_{n-1}(x)\,U_{n+1}(x)&=1>0.\end{aligned}}}
$$

The [integral](https://en.wikipedia.org/wiki/Integral "Integral") relations are [^9] [^10] 
$$
{\displaystyle {\begin{aligned}\int _{-1}^{1}{\frac {T_{n}(y)}{y-x}}\,{\frac {\mathrm {d} y}{\sqrt {1-y^{2}}}}&=\pi \,U_{n-1}(x),\\[3mu]\int _{-1}^{1}{\frac {U_{n-1}(y)}{y-x}}\,{\textstyle {\sqrt {1-y^{2}}}}\,\mathrm {d} y&=-\pi \,T_{n}(x)\end{aligned}}}
$$

where integrals are considered as principal value.

## Explicit expressions

Using the complex number exponentiation definition of the Chebyshev polynomial, one can derive the following expressions, valid for any real ⁠ ${\displaystyle x}$ ⁠: 
$$
{\displaystyle {\begin{aligned}T_{n}(x)&={\tfrac {1}{2}}{\Bigl (}{\bigl (}{\textstyle x-{\sqrt {x^{2}-1}}\!~}{\bigr )}^{n}+{\bigl (}{\textstyle x+{\sqrt {x^{2}-1}}\!~}{\bigr )}^{n}{\Bigr )}\\[5mu]&={\tfrac {1}{2}}{\Bigl (}{\bigl (}{\textstyle x-{\sqrt {x^{2}-1}}\!~}{\bigr )}^{n}+{\bigl (}{\textstyle x-{\sqrt {x^{2}-1}}\!~}{\bigr )}^{-n}{\Bigr )}.\end{aligned}}}
$$
 The two are equivalent because ${\displaystyle \textstyle {\bigl (}x+{\sqrt {x^{2}-1}}\!~{\bigr )}^{\pm 1}={\bigl (}x-{\sqrt {x^{2}-1}}\!~{\bigr )}^{\mp 1}.}$

An explicit form of the Chebyshev polynomial in terms of monomials ${\displaystyle \textstyle x^{k}}$ can be obtained as follows. Letting ${\displaystyle {\mathfrak {R}}}$ denote the [real part](https://en.wikipedia.org/wiki/Complex_number#Notation "Complex number") of a complex number, the following equalities, in order, follow by the definition of ${\displaystyle T_{n}}$, the definition of **${\displaystyle {\mathfrak {R}}}$**, [de Moivre's formula](https://en.wikipedia.org/wiki/De_Moivre%27s_formula "De Moivre's formula"), and the [binomial theorem](https://en.wikipedia.org/wiki/Binomial_theorem "Binomial theorem"):
$$
{\displaystyle {\begin{aligned}T_{n}{\bigl (}\cos(\theta ){\bigr )}&=\cos(n\theta )\\&={\mathfrak {R}}{\bigl (}\cos(n\theta )+i\sin(n\theta ){\bigr )}\\&={\mathfrak {R}}{\bigl (}(\cos(\theta )+i\sin(\theta ))^{n}{\bigr )}\\&={\mathfrak {R}}\left(\sum _{j=0}^{n}{\binom {n}{j}}\,i^{j}\sin ^{j}(\theta )\,\cos ^{n-j}(\theta )\right).\end{aligned}}}
$$
 Because of the factor of ${\displaystyle i^{j}}$, the even-indexed terms are purely real, while the odd-indexed terms are purely imaginary; furthermore, ${\displaystyle \sin ^{2j}\theta =\left(1-\cos ^{2}\theta \right)^{j},}$ so 
$$
{\displaystyle T_{n}{\bigl (}\cos(\theta ){\bigr )}=\sum _{j=0}^{\lfloor n/2\rfloor }{\binom {n}{2j}}\,(-1)^{j}(1-\cos ^{2}(\theta ))^{j}\cos ^{n-2j}(\theta ).}
$$
 Finally, substituting ${\displaystyle x=\cos(\theta )}$ yields 
$$
{\displaystyle T_{n}(x)=\sum \limits _{j=0}^{\lfloor n/2\rfloor }{\binom {n}{2j}}\left(x^{2}-1\right)^{j}x^{n-2j}.}
$$
 This can be written as a ⁠ ${\displaystyle {}_{2}F_{1}}$ ⁠ [hypergeometric function](https://en.wikipedia.org/wiki/Hypergeometric_function "Hypergeometric function"): 
$$
{\displaystyle {\begin{aligned}T_{n}(x)&=\sum _{k=0}^{\lfloor n/2\rfloor }{\binom {n}{2k}}(x^{2}-1)^{k}x^{n-2k}\\&=x^{n}\sum _{k=0}^{\lfloor n/2\rfloor }{\binom {n}{2k}}(1-x^{-2})^{k}\\&={\tfrac {1}{2}}n\sum _{k=0}^{\lfloor n/2\rfloor }(-1)^{k}{\frac {(n-k-1)!}{k!(n-2k)!}}(2x)^{n-2k}\qquad {\text{ for }}n>0\\&=n\sum _{k=0}^{n}(-2)^{k}{\frac {(n+k-1)!}{(n-k)!(2k)!}}(1-x)^{k}\qquad {\text{ for }}n>0\\&={}_{2}F_{1}{\bigl (}{-n},n;{\tfrac {1}{2}};{\tfrac {1}{2}}(1-x){\bigr )}\\\end{aligned}}}
$$
 with inverse [^11] [^12] 
$$
{\displaystyle x^{n}={\frac {1}{2^{n-1}}}\mathop {{\sum }'} _{{j=0} \atop {j\equiv n{\pmod {2}}}}^{n}{\binom {n}{\tfrac {n-j}{2}}}T_{j}(x),}
$$
 where the prime on the summation symbol indicates that the contribution of ${\displaystyle j=0}$ needs to be halved if it appears.

A related expression for ${\displaystyle T_{n}}$ as a sum of monomials with binomial coefficients and powers of two is 
$$
{\displaystyle T_{n}(x)=\sum \limits _{m=0}^{\lfloor n/2\rfloor }(-1)^{m}{\Biggl (}{\binom {n-m}{m}}+{\binom {n-m-1}{n-2m}}{\Biggr )}\cdot 2^{n-2m-1}\cdot x^{n-2m}.}
$$
 Similarly, ${\displaystyle U_{n}}$ can be expressed in terms of hypergeometric functions:
$$
{\displaystyle {\begin{aligned}U_{n}(x)&={\frac {{\bigl (}x+{\sqrt {x^{2}-1}}~\!{\bigr )}^{n+1}-{\bigl (}x-{\sqrt {x^{2}-1}}~\!{\bigr )}^{n+1}}{2{\sqrt {x^{2}-1}}}}\\&=\sum _{k=0}^{\lfloor n/2\rfloor }{\binom {n+1}{2k+1}}{\bigl (}x^{2}-1{\bigr )}^{k}x^{n-2k}\\&=x^{n}\sum _{k=0}^{\lfloor n/2\rfloor }{\binom {n+1}{2k+1}}{\bigl (}1-x^{-2}{\bigr )}^{k}\\&=\sum _{k=0}^{\lfloor n/2\rfloor }{\binom {2k-(n+1)}{k}}(2x)^{n-2k}&{\text{ for }}n>0\\&=\sum _{k=0}^{\lfloor n/2\rfloor }(-1)^{k}{\binom {n-k}{k}}(2x)^{n-2k}&{\text{ for }}n>0\\&=\sum _{k=0}^{n}(-2)^{k}{\frac {(n+k+1)!}{(n-k)!(2k+1)!}}(1-x)^{k}&{\text{ for }}n>0\\&=(n+1)\cdot {}_{2}F_{1}{\bigl (}{-n},n+2;{\tfrac {3}{2}};{\tfrac {1}{2}}(1-x){\bigr )}.\end{aligned}}}
$$

## Properties

### Symmetry

$$
{\displaystyle {\begin{aligned}T_{n}(-x)&=(-1)^{n}T_{n}(x),\\[1ex]U_{n}(-x)&=(-1)^{n}U_{n}(x).\end{aligned}}}
$$
 That is, Chebyshev polynomials of even order have [even symmetry](https://en.wikipedia.org/wiki/Even_and_odd_functions "Even and odd functions") and therefore contain only even powers of ${\displaystyle x}$. Chebyshev polynomials of odd order have [odd symmetry](https://en.wikipedia.org/wiki/Even_and_odd_functions "Even and odd functions") and therefore contain only odd powers of ${\displaystyle x}$.

### Roots and extrema

A Chebyshev polynomial of either kind with degree n has n different [simple roots](https://en.wikipedia.org/wiki/Simple_root "Simple root"), called **Chebyshev roots**, in the interval \[−1, 1\]. The roots of the Chebyshev polynomial of the first kind are sometimes called [Chebyshev nodes](https://en.wikipedia.org/wiki/Chebyshev_nodes "Chebyshev nodes") because they are used as *nodes* in polynomial interpolation. Using the trigonometric definition and the fact that 
$$
{\displaystyle \cos \left((2k+1){\frac {\pi }{2}}\right)=0,}
$$
 one can show that the roots of ${\displaystyle T_{n}}$ are 
$$
{\displaystyle x_{k}=\cos \left({\frac {2k+1}{2n}}\pi \right),\quad k=0,\ldots ,n-1.}
$$
 Similarly, the roots of ${\displaystyle U_{n}}$ are:
$$
{\displaystyle x_{k}=\cos \left({\frac {k}{n+1}}\pi \right),\quad k=1,\ldots ,n.}
$$
 The [extrema](https://en.wikipedia.org/wiki/Maxima_and_minima "Maxima and minima") of ${\displaystyle T_{n}}$ on the interval ${\displaystyle -1\leq x\leq 1}$ are located at:
$$
{\displaystyle x_{k}=\cos \left({\frac {k}{n}}\pi \right),\quad k=0,\ldots ,n.}
$$
 One unique property of the Chebyshev polynomials of the first kind is that on the interval ${\displaystyle -1\leq x\leq 1}$ all of the [extrema](https://en.wikipedia.org/wiki/Maxima_and_minima "Maxima and minima") have values that are either −1 or 1. Thus these polynomials have only two finite [critical values](https://en.wikipedia.org/wiki/Critical_value_\(critical_point\) "Critical value (critical point)"), the defining property of [Shabat polynomials](https://en.wikipedia.org/wiki/Shabat_polynomial "Shabat polynomial"). Both the first and second kinds of Chebyshev polynomial have extrema at the endpoints, given by:
$$
{\displaystyle {\begin{aligned}T_{n}(1)&=1\\T_{n}(-1)&=(-1)^{n}\\U_{n}(1)&=n+1\\U_{n}(-1)&=(-1)^{n}(n+1).\end{aligned}}}
$$
 The [extrema](https://en.wikipedia.org/wiki/Maxima_and_minima "Maxima and minima") of ${\displaystyle T_{n}(x)}$ on the interval ${\displaystyle -1\leq x\leq 1}$ where ${\displaystyle n>0}$ are located at ${\displaystyle n+1}$ values of ${\displaystyle x}$. They are ${\displaystyle \pm 1}$, or ${\displaystyle \cos(2\pi k/d)}$ where ${\displaystyle d>2}$, ${\displaystyle d\mid 2n}$, ${\displaystyle 0<k<{\tfrac {1}{2}}d}$ and ${\displaystyle (k,d)=1}$, i.e., ${\displaystyle k}$ and ${\displaystyle d}$ are [relatively prime](https://en.wikipedia.org/wiki/Relatively_prime "Relatively prime").

Specifically ([Minimal polynomial of 2cos(2pi/n)](https://en.wikipedia.org/wiki/Minimal_polynomial_of_2cos\(2pi/n\) "Minimal polynomial of 2cos(2pi/n)") [^13] [^14]) when ${\displaystyle n}$ is even:

- ${\displaystyle T_{n}(x)=1}$ if ${\displaystyle x=\pm 1}$, or ${\displaystyle d>2}$ and ${\displaystyle 2n/d}$ is even. There are ${\displaystyle {\tfrac {1}{2}}n+1}$ such values of ${\displaystyle x}$.
- ${\displaystyle T_{n}(x)=-1}$ if ${\displaystyle d>2}$ and ${\displaystyle 2n/d}$ is odd. There are ${\displaystyle {\tfrac {1}{2}}n}$ such values of ${\displaystyle x}$.

When ${\displaystyle n}$ is odd:

- ${\displaystyle T_{n}(x)=1}$ if ${\displaystyle x=1}$, or ${\displaystyle d>2}$ and ${\displaystyle 2n/d}$ is even. There are ${\displaystyle {\tfrac {1}{2}}(n+1)}$ such values of ${\displaystyle x}$.
- ${\displaystyle T_{n}(x)=-1}$ if ${\displaystyle x=-1}$, or ${\displaystyle d>2}$ and ${\displaystyle 2n/d}$ is odd. There are ${\displaystyle {\tfrac {1}{2}}(n+1)}$ such values of ${\displaystyle x}$.

### Differentiation and integration

The derivatives of the polynomials can be less than straightforward. By differentiating the polynomials in their trigonometric forms, it can be shown that: 
$$
{\displaystyle {\begin{aligned}{\frac {\mathrm {d} T_{n}}{\mathrm {d} x}}&=nU_{n-1}\\{\frac {\mathrm {d} U_{n}}{\mathrm {d} x}}&={\frac {(n+1)T_{n+1}-xU_{n}}{x^{2}-1}}\\{\frac {\mathrm {d} ^{2}T_{n}}{\mathrm {d} x^{2}}}&=n{\frac {nT_{n}-xU_{n-1}}{x^{2}-1}}=n{\frac {(n+1)T_{n}-U_{n}}{x^{2}-1}}.\end{aligned}}}
$$
 The last two formulas can be numerically troublesome due to the [division by zero](https://en.wikipedia.org/wiki/Division_by_zero "Division by zero") (⁠00⁠ [indeterminate form](https://en.wikipedia.org/wiki/Indeterminate_form "Indeterminate form"), specifically) at ${\displaystyle x=1}$ and ${\displaystyle x=-1}$. By [L'Hôpital's rule](https://en.wikipedia.org/wiki/L%27H%C3%B4pital%27s_rule "L'Hôpital's rule"): 
$$
{\displaystyle {\begin{aligned}\left.{\frac {\mathrm {d} ^{2}T_{n}}{\mathrm {d} x^{2}}}\right|_{x=1}\!\!&={\frac {n^{4}-n^{2}}{3}},\\\left.{\frac {\mathrm {d} ^{2}T_{n}}{\mathrm {d} x^{2}}}\right|_{x=-1}\!\!&=(-1)^{n}{\frac {n^{4}-n^{2}}{3}}.\end{aligned}}}
$$
 More generally,
$$
{\displaystyle \left.{\frac {\mathrm {d} ^{p}T_{n}}{\mathrm {d} x^{p}}}\right|_{x=\pm 1}\!\!=(\pm 1)^{n+p}\prod _{k=0}^{p-1}{\frac {n^{2}-k^{2}}{2k+1}},}
$$
 which is of great use in the numerical solution of [eigenvalue](https://en.wikipedia.org/wiki/Eigenvalue "Eigenvalue") problems.

Also, we have:
$$
{\displaystyle {\frac {\mathrm {d} ^{p}}{\mathrm {d} x^{p}}}T_{n}(x)=2^{p}n\mathop {{\sum }'} _{0\leq k\leq n-p \atop k\equiv n-p{\pmod {2}}}{\binom {{\frac {n+p-k}{2}}-1}{\frac {n-p-k}{2}}}{\frac {\left({\frac {n+p+k}{2}}-1\right)!}{\left({\frac {n-p+k}{2}}\right)!}}T_{k}(x),\qquad p\geq 1,}
$$
 where the prime at the summation symbols means that the term contributed by *k* = 0 is to be halved, if it appears.

Concerning integration, the first derivative of the T <sub>n</sub> implies that:
$$
{\displaystyle \int U_{n}\,\mathrm {d} x={\frac {T_{n+1}}{n+1}}}
$$
 and the recurrence relation for the first kind polynomials involving derivatives establishes that for ${\displaystyle n\geq 2}$:
$$
{\displaystyle \int T_{n}\,\mathrm {d} x={\frac {1}{2}}\left({\frac {T_{n+1}}{n+1}}-{\frac {T_{n-1}}{n-1}}\right)={\frac {n\,T_{n+1}}{n^{2}-1}}-{\frac {xT_{n}}{n-1}}.}
$$
 The last formula can be further manipulated to express the integral of ${\displaystyle T_{n}}$ as a function of Chebyshev polynomials of the first kind only:
$$
{\displaystyle {\begin{aligned}\int T_{n}\,\mathrm {d} x&={\frac {n}{n^{2}-1}}T_{n+1}-{\frac {1}{n-1}}T_{1}T_{n}\\&={\frac {n}{n^{2}-1}}T_{n+1}-{\frac {1}{2(n-1)}}(T_{n+1}+T_{n-1})\\&={\frac {1}{2(n+1)}}T_{n+1}-{\frac {1}{2(n-1)}}T_{n-1}.\end{aligned}}}
$$
 Furthermore, we have:
$$
{\displaystyle \int _{-1}^{1}T_{n}(x)\,\mathrm {d} x={\begin{cases}{\dfrac {(-1)^{n}+1}{1-n^{2}}}&{\text{ if }}n\neq 1\\[3mu]0&{\text{ if }}n=1.\end{cases}}}
$$

### Products of Chebyshev polynomials

The Chebyshev polynomials of the first kind satisfy the relation 
$$
{\displaystyle T_{m}(x)\,T_{n}(x)={\tfrac {1}{2}}{\left(T_{m+n}(x)+T_{|m-n|}(x)\right)},}
$$
 for all non-negative values of ⁠ ${\displaystyle m}$ ⁠ and ⁠ ${\displaystyle n}$ ⁠, which is easily proved from the [product-to-sum formula](https://en.wikipedia.org/wiki/List_of_trigonometric_identities#Product-to-sum_and_sum-to-product_identities "List of trigonometric identities") for the cosine:
$$
{\displaystyle 2\cos \alpha \,\cos \beta =\cos(\alpha +\beta )+\cos(\alpha -\beta ).}
$$
 For ${\displaystyle n=1}$ this results in the already-known recurrence formula, just arranged differently, and with ${\displaystyle n=2}$ it forms the recurrence relation for all even or all odd indexed Chebyshev polynomials (depending on the parity of the lowest m) which implies the evenness or oddness of these polynomials. Three more useful formulas for evaluating Chebyshev polynomials can be concluded from this product expansion:
$$
{\displaystyle {\begin{aligned}T_{2n}(x)&=2T_{n}^{2}(x)-T_{0}(x)&&=2T_{n}^{2}(x)-1,\\[3mu]T_{2n+1}(x)&=2T_{n+1}(x)\,T_{n}(x)-T_{1}(x)&&=2T_{n+1}(x)\,T_{n}(x)-x,\\[3mu]T_{2n-1}(x)&=2T_{n-1}(x)\,T_{n}(x)-T_{1}(x)&&=2T_{n-1}(x)\,T_{n}(x)-x.\end{aligned}}}
$$
 The polynomials of the second kind satisfy the similar relation:
$$
{\displaystyle T_{m}(x)U_{n}(x)={\begin{cases}{\frac {1}{2}}{\bigl (}U_{m+n}(x)+U_{n-m}(x){\bigr )},&{\text{ if }}n\geq m-1,\\[5mu]{\frac {1}{2}}{\bigl (}U_{m+n}(x)-U_{m-n-2}(x){\bigr )},&{\text{ if }}n\leq m-2.\end{cases}}}
$$
 (with the definition ${\displaystyle U_{-1}\equiv 0}$ by convention ). They also satisfy:
$$
{\displaystyle U_{m}(x)\,U_{n}(x)=\sum _{k=0}^{n}U_{m-n+2k}(x)=\sum _{\underset {\text{ step 2 }}{p=m-n}}^{m+n}U_{p}(x).}
$$
 for ${\displaystyle m\geq n}$. For ${\displaystyle n=2}$ this recurrence reduces to:
$$
{\displaystyle {\begin{aligned}U_{m+2}(x)&=U_{2}(x)\,U_{m}(x)-U_{m}(x)-U_{m-2}(x)\\&=U_{m}(x){\big (}U_{2}(x)-1{\big )}-U_{m-2}(x),\end{aligned}}}
$$
 which establishes the evenness or oddness of the even or odd indexed Chebyshev polynomials of the second kind depending on whether ${\displaystyle m}$ starts with 2 or 3.

### Composition and divisibility properties

The trigonometric definitions of ${\displaystyle T_{n}}$ and ${\displaystyle U_{n}}$ imply the composition or nesting properties:[^15] 
$$
{\displaystyle {\begin{aligned}T_{mn}(x)&=T_{m}{\bigl (}T_{n}(x){\bigr )},\\[3mu]U_{mn-1}(x)&=U_{m-1}{\bigl (}T_{n}(x){\bigr )}\,U_{n-1}(x).\end{aligned}}}
$$
 For ${\displaystyle T_{mn}}$ the order of composition may be reversed, making the family of polynomial functions ${\displaystyle T_{n}}$ a [commutative](https://en.wikipedia.org/wiki/Commutative "Commutative") [semigroup](https://en.wikipedia.org/wiki/Semigroup "Semigroup") under composition.

Since ${\displaystyle T_{m}(x)}$ is divisible by ${\displaystyle x}$ if ${\displaystyle m}$ is odd, it follows that ${\displaystyle T_{mn}(x)}$ is divisible by ${\displaystyle T_{n}(x)}$ if ${\displaystyle m}$ is odd. Furthermore, ${\displaystyle U_{mn-1}(x)}$ is divisible by ${\displaystyle U_{n-1}(x)}$, and in the case that ${\displaystyle m}$ is even, divisible by ${\displaystyle T_{n}(x)\,U_{n-1}(x)}$.

### Orthogonality

Both ${\displaystyle T_{n}}$ and ${\displaystyle U_{n}}$ form a sequence of [orthogonal polynomials](https://en.wikipedia.org/wiki/Orthogonal_polynomials "Orthogonal polynomials"). The polynomials of the first kind ${\displaystyle T_{n}}$ are orthogonal with respect to the weight:
$$
{\displaystyle {\frac {1}{\sqrt {1-x^{2}}}},}
$$
 on the interval \[−1, 1\], i.e. we have 
$$
{\displaystyle \int _{-1}^{1}T_{n}(x)\,T_{m}(x){\frac {\mathrm {d} x}{\sqrt {1-x^{2}}}}={\begin{cases}0&{\text{ if }}n\neq m,\\[5mu]\pi &{\text{ if }}n=m=0,\\[5mu]{\frac {\pi }{2}}&{\text{ if }}n=m\neq 0.\end{cases}}}
$$
 This can be proven by letting ${\displaystyle x=\cos(\theta )}$ and using the defining identity ${\displaystyle T_{n}(\cos(\theta ))=\cos(n\theta )}$.

Similarly, the polynomials of the second kind U <sub>n</sub> are orthogonal with respect to the weight 
$$
{\displaystyle {\sqrt {1-x^{2}}}}
$$
 on the interval \[−1, 1\], i.e. we have 
$$
{\displaystyle \int _{-1}^{1}U_{n}(x)\,U_{m}(x){\sqrt {1-x^{2}}}\,\mathrm {d} x={\begin{cases}0&{\text{ if }}n\neq m,\\[5mu]{\frac {\pi }{2}}&{\text{ if }}n=m.\end{cases}}}
$$
 (The measure ${\displaystyle {\sqrt {1-x^{2}}}\,\mathrm {d} x}$ is, to within a normalizing constant, the [Wigner semicircle distribution](https://en.wikipedia.org/wiki/Wigner_semicircle_distribution "Wigner semicircle distribution").)

These orthogonality properties follow from the fact that the Chebyshev polynomials solve the [Chebyshev differential equations](https://en.wikipedia.org/wiki/Chebyshev_equation "Chebyshev equation") 
$$
{\displaystyle {\begin{aligned}(1-x^{2})T_{n}''-xT_{n}'+n^{2}T_{n}&=0,\\[1ex](1-x^{2})U_{n}''-3xU_{n}'+n(n+2)U_{n}&=0,\end{aligned}}}
$$
 which are [Sturm–Liouville differential equations](https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_problem "Sturm–Liouville problem"). It is a general feature of such [differential equations](https://en.wikipedia.org/wiki/Differential_equation "Differential equation") that there is a distinguished orthonormal set of solutions. (Another way to define the Chebyshev polynomials is as the solutions to [those equations](https://en.wikipedia.org/wiki/Sturm%E2%80%93Liouville_problem "Sturm–Liouville problem").)

The ${\displaystyle T_{n}}$ also satisfy a discrete orthogonality condition:
$$
{\displaystyle \sum _{k=0}^{N-1}{T_{i}(x_{k})\,T_{j}(x_{k})}={\begin{cases}0&{\text{ if }}i\neq j,\\[5mu]N&{\text{ if }}i=j=0,\\[5mu]{\frac {N}{2}}&{\text{ if }}i=j\neq 0,\end{cases}}}
$$
 where ${\displaystyle N}$ is any integer greater than ${\displaystyle \max(i,j)}$,[^10] and the ${\displaystyle x_{k}}$ are the ${\displaystyle N}$ [Chebyshev nodes](https://en.wikipedia.org/wiki/Chebyshev_nodes "Chebyshev nodes") (see above) of ${\displaystyle T_{N}(x)}$:
$$
{\displaystyle x_{k}=\cos \left(\pi {\frac {2k+1}{2N}}\right)\quad {\text{ for }}k=0,1,\dots ,N-1.}
$$
 For the polynomials of the second kind and any integer ${\displaystyle N>i+j}$ with the same Chebyshev nodes ${\displaystyle x_{k}}$, there are similar sums:
$$
{\displaystyle \sum _{k=0}^{N-1}{U_{i}(x_{k})\,U_{j}(x_{k})\left(1-x_{k}^{2}\right)}={\begin{cases}0&{\text{ if }}i\neq j,\\[5mu]{\frac {N}{2}}&{\text{ if }}i=j,\end{cases}}}
$$
 and without the [weight function](https://en.wikipedia.org/wiki/Weight_function "Weight function"):
$$
{\displaystyle \sum _{k=0}^{N-1}{U_{i}(x_{k})\,U_{j}(x_{k})}={\begin{cases}0&{\text{ if }}i\not \equiv j{\pmod {2}},\\[5mu]N\cdot (1+\min\{i,j\})&{\text{ if }}i\equiv j{\pmod {2}}.\end{cases}}}
$$
 For any integer ${\displaystyle N>i+j}$, based on the ${\displaystyle N}$ } zeros of ${\displaystyle U_{N}(x)}$:
$$
{\displaystyle y_{k}=\cos \left(\pi {\frac {k+1}{N+1}}\right)\quad {\text{ for }}k=0,1,\dots ,N-1,}
$$
 one can get the sum:
$$
{\displaystyle \sum _{k=0}^{N-1}{U_{i}(y_{k})\,U_{j}(y_{k})(1-y_{k}^{2})}={\begin{cases}0&{\text{ if }}i\neq j,\\[5mu]{\frac {N+1}{2}}&{\text{ if }}i=j,\end{cases}}}
$$
 and again without the weight function:
$$
{\displaystyle \sum _{k=0}^{N-1}{U_{i}(y_{k})\,U_{j}(y_{k})}={\begin{cases}0&{\text{ if }}i\not \equiv j{\pmod {2}},\\[5mu]{\bigl (}\min\{i,j\}+1{\bigr )}{\bigl (}N-\max\{i,j\}{\bigr )}&{\text{ if }}i\equiv j{\pmod {2}}.\end{cases}}}
$$

### Minimal ∞-norm

For any given ${\displaystyle n\geq 1}$, among the polynomials of degree ${\displaystyle n}$ with leading coefficient 1 ([monic](https://en.wikipedia.org/wiki/Monic_polynomial "Monic polynomial") polynomials): 
$$
{\displaystyle f(x)={\frac {1}{2^{n-1}}}T_{n}(x)}
$$
 is the one of which the maximal absolute value on the interval \[−1, 1\] is minimal.

This maximal absolute value is: 
$$
{\displaystyle {\frac {1}{2^{n-1}}}}
$$
 and ${\displaystyle |f(x)|}$ reaches this maximum exactly ${\displaystyle n+1}$ times at: 
$$
{\displaystyle x=\cos {\frac {k\pi }{n}}\quad {\text{for }}0\leq k\leq n.}
$$

**Proof**

Let's assume that ${\displaystyle w_{n}(x)}$ is a polynomial of degree ${\displaystyle n}$ with leading coefficient 1 with maximal absolute value on the interval \[−1, 1\] less than 1 / 2 <sup><i>n</i> − 1</sup>.

Define 
$$
{\displaystyle f_{n}(x)={\frac {1}{2^{n-1}}}T_{n}(x)-w_{n}(x)}
$$

Because at extreme points of T <sub>n</sub> we have 
$$
{\displaystyle {\begin{aligned}|w_{n}(x)|&<\left|{\frac {1}{2^{n-1}}}T_{n}(x)\right|\\f_{n}(x)&>0\qquad {\text{ for }}x=\cos {\frac {2k\pi }{n}}&&{\text{ where }}0\leq 2k\leq n\\f_{n}(x)&<0\qquad {\text{ for }}x=\cos {\frac {(2k+1)\pi }{n}}&&{\text{ where }}0\leq 2k+1\leq n\end{aligned}}}
$$

From the [intermediate value theorem](https://en.wikipedia.org/wiki/Intermediate_value_theorem "Intermediate value theorem"), *f <sub>n</sub>* (*x*) has at least n roots. However, this is impossible, as *f <sub>n</sub>* (*x*) is a polynomial of degree *n* − 1, so the [fundamental theorem of algebra](https://en.wikipedia.org/wiki/Fundamental_theorem_of_algebra "Fundamental theorem of algebra") implies it has at most *n* − 1 roots.

#### Remark

By the [equioscillation theorem](https://en.wikipedia.org/wiki/Equioscillation_theorem "Equioscillation theorem"), among all the polynomials of degree ≤  *n*, the polynomial f minimizes ‖  *f*  ‖ <sub>∞</sub> on \[−1, 1\] [if and only if](https://en.wikipedia.org/wiki/If_and_only_if "If and only if") there are *n* + 2 points −1 ≤ *x* <sub>0</sub> < *x* <sub>1</sub> < ⋯ < *x* <sub><i>n</i> + 1</sub> ≤ 1 such that |  *f* (*x <sub>i</sub>*)| = ‖  *f*  ‖ <sub>∞</sub>.

Of course, the null polynomial on the interval \[−1, 1\] can be approximated by itself and minimizes the ∞-norm.

Above, however, |  *f*  | reaches its maximum only *n* + 1 times because we are searching for the best polynomial of degree *n* ≥ 1 (therefore the theorem evoked previously cannot be used).

### Chebyshev polynomials as special cases of more general polynomial families

The Chebyshev polynomials are a special case of the ultraspherical or [Gegenbauer polynomials](https://en.wikipedia.org/wiki/Gegenbauer_polynomials "Gegenbauer polynomials") ${\displaystyle C_{n}^{(\lambda )}(x)}$, which themselves are a special case of the [Jacobi polynomials](https://en.wikipedia.org/wiki/Jacobi_polynomials "Jacobi polynomials") ${\displaystyle P_{n}^{(\alpha ,\beta )}(x)}$: 
$$
{\displaystyle {\begin{aligned}T_{n}(x)&={\frac {n}{2}}\lim _{q\to 0}{\frac {1}{q}}C_{n}^{(q)}(x)\qquad {\text{ if }}n\geq 1,\\&={\frac {1}{\binom {n-{\frac {1}{2}}}{n}}}P_{n}^{\left(-{\frac {1}{2}},-{\frac {1}{2}}\right)}(x)={\frac {2^{2n}}{\binom {2n}{n}}}P_{n}^{\left(-{\frac {1}{2}},-{\frac {1}{2}}\right)}(x),\\[2ex]U_{n}(x)&=C_{n}^{(1)}(x)\\&={\frac {n+1}{\binom {n+{\frac {1}{2}}}{n}}}P_{n}^{\left({\frac {1}{2}},{\frac {1}{2}}\right)}(x)={\frac {2^{2n+1}}{\binom {2n+2}{n+1}}}P_{n}^{\left({\frac {1}{2}},{\frac {1}{2}}\right)}(x).\end{aligned}}}
$$

Chebyshev polynomials are also a special case of [Dickson polynomials](https://en.wikipedia.org/wiki/Dickson_polynomial "Dickson polynomial"): 
$$
{\displaystyle {\begin{aligned}D_{n}(2x\alpha ,\alpha ^{2})&=2\alpha ^{n}T_{n}(x),\\E_{n}(2x\alpha ,\alpha ^{2})&=\alpha ^{n}U_{n}(x).\end{aligned}}}
$$
 In particular, when ${\displaystyle \alpha ={\tfrac {1}{2}}}$, they are related by ${\displaystyle D_{n}{\bigl (}x,{\tfrac {1}{4}}{\bigr )}=2^{1-n}T_{n}(x)}$ and ${\displaystyle E_{n}{\bigl (}x,{\tfrac {1}{4}}{\bigr )}=2^{-n}U_{n}(x)}$.

### Other properties

The curves given by *y* = *T* <sub><i>n</i></sub> (*x*), or equivalently, by the parametric equations *y* = *T* <sub><i>n</i></sub> (cos *θ*) = cos *nθ*, *x* = cos *θ*, are a special case of [Lissajous curves](https://en.wikipedia.org/wiki/Lissajous_curve "Lissajous curve") with frequency ratio equal to n.

Similar to the formula: 
$$
{\displaystyle T_{n}(\cos \theta )=\cos(n\theta ),}
$$
 we have the analogous formula: 
$$
{\displaystyle T_{2n+1}(\sin \theta )={(-1)^{n}\sin }{\bigl (}(2n+1)\theta {\bigr )}.}
$$

For *x* ≠ 0: 
$$
{\displaystyle T_{n}\!\left({\frac {x+x^{-1}}{2}}\right)={\frac {x^{n}+x^{-n}}{2}}}
$$
 and: 
$$
{\displaystyle x^{n}=T_{n}\left({\frac {x+x^{-1}}{2}}\right)+{\frac {x-x^{-1}}{2}}U_{n-1}\left({\frac {x+x^{-1}}{2}}\right),}
$$
 which follows from the fact that this holds by definition for *x* = *e <sup>iθ</sup>*.

There are relations between [Legendre polynomials](https://en.wikipedia.org/wiki/Legendre_polynomial "Legendre polynomial") and Chebyshev polynomials 
$$
{\displaystyle {\begin{aligned}\sum _{k=0}^{n}P_{k}(x)\,T_{n-k}(x)&=\left(n+1\right)P_{n}(x),\\\sum _{k=0}^{n}P_{k}(x)\,P_{n-k}(x)&=U_{n}(x).\end{aligned}}}
$$
 These identities can be proven using generating functions and discrete convolution.

#### Chebyshev polynomials as determinants

From their definition by recurrence it follows that the Chebyshev polynomials can be obtained as [determinants](https://en.wikipedia.org/wiki/Determinant "Determinant") of special [tridiagonal matrices](https://en.wikipedia.org/wiki/Tridiagonal_matrix "Tridiagonal matrix") of size ${\displaystyle k\times k}$:

$$
{\displaystyle T_{k}(x)=\det {\begin{bmatrix}x&1&0&\cdots &0\\1&2x&1&\ddots &\vdots \\0&1&2x&\ddots &0\\\vdots &\ddots &\ddots &\ddots &1\\0&\cdots &0&1&2x\end{bmatrix}},}
$$
 and similarly for ${\displaystyle U_{k}}$.

## Examples

### First kind

![[330px-Chebyshev_Polynomials_of_the_1st_Kind_%28n%3D0-5%2C_x%3D%28-1%2C1%29%29.svg.png]]

The first few Chebyshev polynomials of the first kind in the domain −1 < x < 1: The flat T 0, 1 2 3 4 and 5.

The first few Chebyshev polynomials of the first kind are [OEIS](https://en.wikipedia.org/wiki/On-Line_Encyclopedia_of_Integer_Sequences "On-Line Encyclopedia of Integer Sequences"): [A028297](https://oeis.org/A028297 "oeis:A028297") 
$$
{\displaystyle {\begin{aligned}T_{0}(x)&=1\\T_{1}(x)&=x\\T_{2}(x)&=2x^{2}-1\\T_{3}(x)&=4x^{3}-3x\\T_{4}(x)&=8x^{4}-8x^{2}+1\\T_{5}(x)&=16x^{5}-20x^{3}+5x\\T_{6}(x)&=32x^{6}-48x^{4}+18x^{2}-1\\T_{7}(x)&=64x^{7}-112x^{5}+56x^{3}-7x\\T_{8}(x)&=128x^{8}-256x^{6}+160x^{4}-32x^{2}+1\\T_{9}(x)&=256x^{9}-576x^{7}+432x^{5}-120x^{3}+9x\\T_{10}(x)&=512x^{10}-1280x^{8}+1120x^{6}-400x^{4}+50x^{2}-1\end{aligned}}}
$$

### Second kind

![[330px-Chebyshev_Polynomials_of_the_2nd_Kind_%28n%3D0-5%2C_x%3D%28-1%2C1%29%29.svg.png]]

The first few Chebyshev polynomials of the second kind in the domain −1 < x < 1: The flat U 0, 1 2 3 4 and 5. Although not visible in the image, n (1) = + 1 (−1) = ( + 1)(−1).

The first few Chebyshev polynomials of the second kind are [OEIS](https://en.wikipedia.org/wiki/On-Line_Encyclopedia_of_Integer_Sequences "On-Line Encyclopedia of Integer Sequences"): [A053117](https://oeis.org/A053117 "oeis:A053117") 
$$
{\displaystyle {\begin{aligned}U_{0}(x)&=1\\U_{1}(x)&=2x\\U_{2}(x)&=4x^{2}-1\\U_{3}(x)&=8x^{3}-4x\\U_{4}(x)&=16x^{4}-12x^{2}+1\\U_{5}(x)&=32x^{5}-32x^{3}+6x\\U_{6}(x)&=64x^{6}-80x^{4}+24x^{2}-1\\U_{7}(x)&=128x^{7}-192x^{5}+80x^{3}-8x\\U_{8}(x)&=256x^{8}-448x^{6}+240x^{4}-40x^{2}+1\\U_{9}(x)&=512x^{9}-1024x^{7}+672x^{5}-160x^{3}+10x\\U_{10}(x)&=1024x^{10}-2304x^{8}+1792x^{6}-560x^{4}+60x^{2}-1\end{aligned}}}
$$

## As a basis set

![[250px-ChebyshevExpansion.png]]

The non-smooth function (top) y = − x 3 H (− ), where is the Heaviside step function, and (bottom) the 5th partial sum of its Chebyshev expansion. The 7th sum is indistinguishable from the original function at the resolution of the graph.

In the appropriate [Sobolev space](https://en.wikipedia.org/wiki/Sobolev_space "Sobolev space"), the set of Chebyshev polynomials form an [orthonormal basis](https://en.wikipedia.org/wiki/Hilbert_space#Orthonormal_bases "Hilbert space"), so that a function in the same space can, on −1 ≤ *x* ≤ 1, be expressed via the expansion:[^16] 
$$
{\displaystyle f(x)=\sum _{n=0}^{\infty }a_{n}T_{n}(x).}
$$
 Furthermore, as mentioned previously, the Chebyshev polynomials form an [orthogonal](https://en.wikipedia.org/wiki/Orthogonal "Orthogonal") basis which (among other things) implies that the coefficients *a* <sub><i>n</i></sub> can be determined easily through the application of an [inner product](https://en.wikipedia.org/wiki/Inner_product "Inner product"). This sum is called a **Chebyshev series** or a **Chebyshev expansion**.

Since a Chebyshev series is related to a [Fourier cosine series](https://en.wikipedia.org/wiki/Fourier_cosine_series "Fourier cosine series") through a change of variables, all of the theorems, identities, etc. that apply to [Fourier series](https://en.wikipedia.org/wiki/Fourier_series "Fourier series") have a Chebyshev counterpart.[^16] These attributes include:

- The Chebyshev polynomials form a [complete](https://en.wikipedia.org/wiki/Complete_metric_space "Complete metric space") orthogonal system.
- The Chebyshev series converges to *f* (*x*) if the function is [piecewise](https://en.wikipedia.org/wiki/Piecewise "Piecewise") [smooth](https://en.wikipedia.org/wiki/Smooth_function "Smooth function") and [continuous](https://en.wikipedia.org/wiki/Continuous_function "Continuous function"). The smoothness requirement can be relaxed in most cases – as long as there are a finite number of discontinuities in *f* (*x*) and its derivatives.
- At a discontinuity, the series will converge to the average of the right and left limits.

The abundance of the theorems and identities inherited from [Fourier series](https://en.wikipedia.org/wiki/Fourier_series "Fourier series") make the Chebyshev polynomials important tools in [numeric analysis](https://en.wikipedia.org/wiki/Numeric_analysis "Numeric analysis"); for example they are the most popular general purpose basis functions used in the [spectral method](https://en.wikipedia.org/wiki/Spectral_method "Spectral method"),[^16] often in favor of trigonometric series due to generally faster convergence for continuous functions ([Gibbs' phenomenon](https://en.wikipedia.org/wiki/Gibbs%27_phenomenon "Gibbs' phenomenon") is still a problem).

The [Chebfun](https://en.wikipedia.org/wiki/Chebfun "Chebfun") software package supports function manipulation based on their expansion in the Chebyshev basis.

### Example 1

Consider the Chebyshev expansion of log(1 + *x*). One can express: 
$$
{\displaystyle \log(1+x)=\sum _{n=0}^{\infty }a_{n}T_{n}(x).}
$$

One can find the coefficients *a <sub>n</sub>* either through the application of an inner product or by the discrete orthogonality condition. For the inner product: 
$$
{\displaystyle \int _{-1}^{+1}{\frac {T_{m}(x)\log(1+x)}{\sqrt {1-x^{2}}}}\,\mathrm {d} x=\sum _{n=0}^{\infty }a_{n}\int _{-1}^{+1}{\frac {T_{m}(x)T_{n}(x)}{\sqrt {1-x^{2}}}}\,\mathrm {d} x,}
$$
 which gives: 
$$
{\displaystyle a_{n}={\begin{cases}-\log 2&{\text{ for }}n=0,\\[3mu]{\dfrac {-2(-1)^{n}}{n}}&{\text{ for }}n>0.\end{cases}}}
$$

Alternatively, when the inner product of the function being approximated cannot be evaluated, the discrete orthogonality condition gives an often useful result for *approximate* coefficients: 
$$
{\displaystyle a_{n}\approx {\frac {2-\delta _{0n}}{N}}\sum _{k=0}^{N-1}T_{n}(x_{k})\log(1+x_{k}),}
$$

where δ <sub>ij</sub> is the [Kronecker delta](https://en.wikipedia.org/wiki/Kronecker_delta "Kronecker delta") function and the x <sub>k</sub> are the N Gauss–Chebyshev zeros of *T* <sub><i>N</i> </sub> (*x*): 
$$
{\displaystyle x_{k}=\cos \left({\frac {\pi {\bigl (}k+{\tfrac {1}{2}}{\bigr )}}{N}}\right).}
$$

For any N, these approximate coefficients provide an exact approximation to the function at x <sub>k</sub> with a controlled error between those points. The exact coefficients are obtained with *N* = ∞, thus representing the function exactly at all points in \[−1,1\]. The [rate of convergence](https://en.wikipedia.org/wiki/Rate_of_convergence "Rate of convergence") depends on the function and its smoothness.

This allows us to compute the approximate coefficients a <sub>n</sub> very efficiently through the [discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform "Discrete cosine transform"):

$$
{\displaystyle a_{n}\approx {\frac {2-\delta _{0n}}{N}}\sum _{k=0}^{N-1}\cos \left({\frac {n\pi {\bigl (}k+{\tfrac {1}{2}}{\bigr )}}{N}}\right)\log(1+x_{k}).}
$$

### Example 2

To provide another example:

$$
{\displaystyle {\begin{aligned}\left(1-x^{2}\right)^{\alpha }&=-{\frac {1}{\sqrt {\pi }}}\,{\frac {\Gamma \left({\tfrac {1}{2}}+\alpha \right)}{\Gamma (\alpha +1)}}+2^{1-2\alpha }\,\sum _{n=0}\left(-1\right)^{n}\,{2\alpha  \choose \alpha -n}\,T_{2n}(x)\\[1ex]&=2^{-2\alpha }\,\sum _{n=0}\left(-1\right)^{n}\,{2\alpha +1 \choose \alpha -n}\,U_{2n}(x).\end{aligned}}}
$$

### Partial sums

The partial sums of: 
$$
{\displaystyle f(x)=\sum _{n=0}^{\infty }a_{n}T_{n}(x)}
$$
 are very useful in the [approximation](https://en.wikipedia.org/wiki/Approximation_theory "Approximation theory") of various functions and in the solution of [differential equations](https://en.wikipedia.org/wiki/Differential_equation "Differential equation") (see [spectral method](https://en.wikipedia.org/wiki/Spectral_method "Spectral method")). Two common methods for determining the coefficients a <sub>n</sub> are through the use of the [inner product](https://en.wikipedia.org/wiki/Inner_product "Inner product") as in [Galerkin's method](https://en.wikipedia.org/wiki/Galerkin%27s_method "Galerkin's method") and through the use of [collocation](https://en.wikipedia.org/wiki/Collocation_method "Collocation method") which is related to [interpolation](https://en.wikipedia.org/wiki/Interpolation "Interpolation").

As an interpolant, the N coefficients of the (*N* − 1)st partial sum are usually obtained on the Chebyshev–Gauss–Lobatto [^17] points (or Lobatto grid), which results in minimum error and avoids [Runge's phenomenon](https://en.wikipedia.org/wiki/Runge%27s_phenomenon "Runge's phenomenon") associated with a uniform grid. This collection of points corresponds to the extrema of the highest order polynomial in the sum, plus the endpoints and is given by: 
$$
{\displaystyle x_{k}=-\cos \left({\frac {k\pi }{N-1}}\right);\qquad k=0,1,\dots ,N-1.}
$$

### Polynomial in Chebyshev form

An arbitrary polynomial of degree N can be written in terms of the Chebyshev polynomials of the first kind.[^10] Such a polynomial *p* (*x*) is of the form: 
$$
{\displaystyle p(x)=\sum _{n=0}^{N}a_{n}T_{n}(x).}
$$

Polynomials in Chebyshev form can be evaluated using the [Clenshaw algorithm](https://en.wikipedia.org/wiki/Clenshaw_algorithm "Clenshaw algorithm").

Polynomials denoted ${\displaystyle C_{n}(x)}$ and ${\displaystyle S_{n}(x)}$ closely related to Chebyshev polynomials are sometimes used. They are defined by:[^18]

$$
{\displaystyle C_{n}(x)=2T_{n}\left({\frac {x}{2}}\right),\qquad S_{n}(x)=U_{n}\left({\frac {x}{2}}\right)}
$$

and satisfy:

$$
{\displaystyle C_{n}(x)=S_{n}(x)-S_{n-2}(x).}
$$

A. F. Horadam called the polynomials ${\displaystyle C_{n}(x)}$ **Vieta–Lucas polynomials** and denoted them ${\displaystyle v_{n}(x)}$. He called the polynomials ${\displaystyle S_{n}(x)}$ **Vieta–Fibonacci polynomials** and denoted them ${\displaystyle V_{n}(x)}$.[^19] All of these polynomials have 1 as their leading coefficient. Lists of both sets of polynomials are given in [Viète's](https://en.wikipedia.org/wiki/Fran%C3%A7ois_Vi%C3%A8te "François Viète") *Opera Mathematica*, Chapter IX, Theorems VI and VII.[^20] The Vieta–Lucas and Vieta–Fibonacci polynomials of real argument are, up to a power of ${\displaystyle i}$ and a shift of index in the case of the latter, equal to [Lucas and Fibonacci polynomials](https://en.wikipedia.org/wiki/Fibonacci_polynomials "Fibonacci polynomials") *L* <sub><i>n</i></sub> and *F* <sub><i>n</i></sub> of imaginary argument.

**Shifted Chebyshev polynomials** of the first and second kinds are related to the Chebyshev polynomials by:[^18]

$$
{\displaystyle {T}_{n}^{*}(x)=T_{n}(2x-1),\qquad {U}_{n}^{*}(x)=U_{n}(2x-1).}
$$

When the argument of the Chebyshev polynomial satisfies 2 *x* − 1 ∈ \[−1, 1\] the argument of the shifted Chebyshev polynomial satisfies *x* ∈ \[0, 1\]. Similarly, one can define shifted polynomials for generic intervals \[*a*, *b*\].

Around 1990 the terms "third-kind" and "fourth-kind" came into use in connection with Chebyshev polynomials, although the polynomials denoted by these terms had an earlier development under the name **airfoil polynomials**. According to J. C. Mason and G. H. Elliott, the terminology "third-kind" and "fourth-kind" is due to [Walter Gautschi](https://en.wikipedia.org/wiki/Walter_Gautschi "Walter Gautschi"), "in consultation with colleagues in the field of orthogonal polynomials." [^21] The **Chebyshev polynomials of the third kind** are defined as:

$$
{\displaystyle V_{n}(x)={\frac {\cos \left(\left(n+{\frac {1}{2}}\right)\theta \right)}{\cos \left({\frac {\theta }{2}}\right)}}={\sqrt {\frac {2}{1+x}}}T_{2n+1}\left({\sqrt {\frac {x+1}{2}}}\right)}
$$
 and the **Chebyshev polynomials of the fourth kind** are defined as: 
$$
{\displaystyle W_{n}(x)={\frac {\sin \left(\left(n+{\frac {1}{2}}\right)\theta \right)}{{\sin }{\bigl (}{\tfrac {1}{2}}\theta {\bigr )}}}=U_{2n}\left({\sqrt {\frac {x+1}{2}}}\right),}
$$

where ${\displaystyle \theta =\arccos x}$.[^21] [^22] They coincide with the [Dirichlet kernel](https://en.wikipedia.org/wiki/Dirichlet_kernel "Dirichlet kernel").

In the airfoil literature ${\displaystyle V_{n}(x)}$ and ${\displaystyle W_{n}(x)}$ are denoted ${\displaystyle t_{n}(x)}$ and ${\displaystyle u_{n}(x)}$. The polynomial families ${\displaystyle T_{n}(x)}$, ${\displaystyle U_{n}(x)}$, ${\displaystyle V_{n}(x)}$, and ${\displaystyle W_{n}(x)}$ are orthogonal with respect to the weights: 
$$
{\displaystyle \left(1-x^{2}\right)^{-1/2},\quad \left(1-x^{2}\right)^{1/2},\quad (1-x)^{-1/2}(1+x)^{1/2},\quad (1+x)^{-1/2}(1-x)^{1/2}}
$$

and are proportional to Jacobi polynomials ${\displaystyle P_{n}^{(\alpha ,\beta )}(x)}$ with:[^22] 
$$
{\displaystyle (\alpha ,\beta )={\bigl (}{-{\tfrac {1}{2}}},{-{\tfrac {1}{2}}}{\bigr )},\quad (\alpha ,\beta )={\bigl (}{\tfrac {1}{2}},{\tfrac {1}{2}}{\bigr )},\quad (\alpha ,\beta )={\bigl (}{-{\tfrac {1}{2}}},{\tfrac {1}{2}}{\bigr )},\quad (\alpha ,\beta )={\bigl (}{\tfrac {1}{2}},{-{\tfrac {1}{2}}}{\bigr )}.}
$$

All four families satisfy the recurrence ${\displaystyle p_{n}(x)=2xp_{n-1}(x)-p_{n-2}(x)}$ with ${\displaystyle p_{0}(x)=1}$, where ${\displaystyle p_{n}=T_{n}}$, ${\displaystyle U_{n}}$, ${\displaystyle V_{n}}$, or ${\displaystyle W_{n}}$, but they differ according to whether ${\displaystyle p_{1}(x)}$ equals ${\displaystyle x}$, ${\displaystyle 2x}$, ${\displaystyle 2x-1}$, or ${\displaystyle 2x+1}$.[^21]

### Irreducible Factorization of Chebyshev Polynomials

It is easier to discuss this detail by first examining the factorization of the Vieta-Lucas and Vieta-Fibonacci polynomials.

Given the roots of the Chebyshev polynomials, it is easy to see—by comparing their root sets—that 
$$
{\displaystyle x^{n}C_{n}\left(x+{\frac {1}{x}}\right)=x^{2n}+1}
$$
 and 
$$
{\displaystyle x^{n}S_{n}\left(x+{\frac {1}{x}}\right)=\sum _{k=0}^{n}x^{2k}.}
$$

By expressing the right-hand side expressions in form 
$$
{\displaystyle x^{2n}+1={\frac {x^{4n}-1}{x^{2n}-1}},}
$$
 and 
$$
{\displaystyle \sum _{k=0}^{n}x^{2k}={\frac {x^{2n+2}-1}{x^{2}-1}},}
$$
 the numerators and denominators of these fractions—and consequently the fractions themselves—can be written as products of expressions like ${\displaystyle x-g_{i}}$ where each ${\displaystyle g_{i}}$ is a primitive [root of unity](https://en.wikipedia.org/wiki/Root_of_unity "Root of unity"). Thus, we obtain: 
$$
{\displaystyle x^{n}C_{n}{\left(x+{\frac {1}{x}}\right)}=\prod _{d\geq 3,\;d\mid 4n,\;d\nmid 2n}\Phi _{d}(x)}
$$
 and 
$$
{\displaystyle x^{n}S_{n}{\left(x+{\frac {1}{x}}\right)}=\prod _{d\geq 3,\;d\mid 2n+2}\Phi _{d}(x),}
$$
 where ${\displaystyle \Phi _{d}(x)}$ is the ⁠ ${\displaystyle d}$ ⁠th [cyclotomic polynomial](https://en.wikipedia.org/wiki/Cyclotomic_polynomial "Cyclotomic polynomial").

It can be shown that, for every ${\displaystyle n\geq 3}$, corresponding to the [cyclotomic polynomial](https://en.wikipedia.org/wiki/Cyclotomic_polynomial "Cyclotomic polynomial") ${\displaystyle \Phi _{n}(x)}$ of degree ${\displaystyle \varphi (n)}$ there exists a unique polynomial ${\displaystyle \Psi _{n}(x)}$ of degree ${\displaystyle \varphi (n)/2}$ such that 
$$
{\displaystyle x^{\varphi (n)/2}\Psi _{n}{\left(x+{\frac {1}{x}}\right)}=\Phi _{n}(x),}
$$
 where ${\displaystyle \varphi (n)}$ is the well known [Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function "Euler's totient function").

The polynomials ${\displaystyle \Psi _{n}(x)}$ may be referred to as cyclotomic pre-polynomials, since the [cyclotomic polynomials](https://en.wikipedia.org/wiki/Cyclotomic_polynomials "Cyclotomic polynomials") can be obtained from them via a well-defined mapping.

An obvious property of the mapping 
$$
{\displaystyle P_{n}(x)\rightarrow x^{n}P_{n}{\left(x+{\frac {1}{x}}\right)}}
$$
 applicable to any polynomial ${\displaystyle P_{n}(x)}$ of degree ${\displaystyle n}$ is that it maps the product of two or more polynomials to the product of the images of the individual polynomials.

From all of the above, it follows that 
$$
{\displaystyle C_{n}(x)=\prod _{d\geq 3,\;d\mid 4n,\;d\nmid 2n}\Psi _{d}(x)}
$$
 and 
$$
{\displaystyle S_{n}(x)=\prod _{d\geq 3,\;d\mid 2n+2}\Psi _{d}(x).}
$$

Now, it follows directly that the Chebyshev polynomials ${\displaystyle T_{n}(x)}$ and ${\displaystyle U_{n}(x)}$ can be factorized as follows: 
$$
{\displaystyle T_{n}(x)={\tfrac {1}{2}}\prod _{d\geq 3,\;d\mid 4n,\;d\nmid 2n}\Psi _{d}(2x)}
$$
 and 
$$
{\displaystyle U_{n}(x)=\prod _{d\geq 3,\;d\mid 2n+2}\Psi _{d}(2x).}
$$

From the irreducibility of the polynomials ${\displaystyle \Phi _{n}(x)}$ it follows that the polynomials ${\displaystyle \Psi _{n}(x)}$ are also irreducible.

For more details, see.[^23]

### Even order modified Chebyshev polynomials

Some applications rely on Chebyshev polynomials but may be unable to accommodate the lack of a root at zero, which rules out the use of standard Chebyshev polynomials for these kinds of applications. Even order [Chebyshev filter](https://en.wikipedia.org/wiki/Chebyshev_filter "Chebyshev filter") designs using equally terminated passive networks are an example of this.[^24] However, even order Chebyshev polynomials may be modified to move the lowest roots down to zero while still maintaining the desirable Chebyshev equi-ripple effect. Such modified polynomials contain two roots at zero, and may be referred to as even order modified Chebyshev polynomials. Even order modified Chebyshev polynomials may be created from the [Chebyshev nodes](https://en.wikipedia.org/wiki/Chebyshev_nodes "Chebyshev nodes") in the same manner as standard Chebyshev polynomials.

$$
{\displaystyle P_{N}=\prod _{i=1}^{N}(x-C_{i})}
$$
 where

- ${\displaystyle P_{N}}$ is an *N* -th order Chebyshev polynomial
- ${\displaystyle C_{i}}$ is the *i* -th Chebyshev node

In the case of even order modified Chebyshev polynomials, the [even order modified Chebyshev nodes](https://en.wikipedia.org/wiki/Chebyshev_nodes#Even_order_modified_Chebyshev_nodes "Chebyshev nodes") are used to construct the even order modified Chebyshev polynomials.

$$
{\displaystyle Pe_{N}=\prod _{i=1}^{N}(x-Ce_{i})}
$$
 where

- ${\displaystyle Pe_{N}}$ is an *N* -th order even order modified Chebyshev polynomial
- ${\displaystyle Ce_{i}}$ is the *i* -th even order modified Chebyshev node

For example, the 4th order Chebyshev polynomial from the [example above](#Examples) is ${\displaystyle X^{4}-X^{2}+.125}$, which by inspection contains no roots of zero. Creating the polynomial from the even order modified Chebyshev nodes creates a 4th order even order modified Chebyshev polynomial of ${\displaystyle X^{4}-.828427X^{2}}$, which by inspection contains two roots at zero, and may be used in applications requiring roots at zero.

[^1]: [Rivlin, Theodore J.](https://en.wikipedia.org/wiki/Theodore_J._Rivlin "Theodore J. Rivlin") (1974). "Chapter 2, Extremal properties". *The Chebyshev Polynomials*. Pure and Applied Mathematics (1st ed.). New York-London-Sydney: Wiley-Interscience \[John Wiley & Sons\]. pp. 56–123. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-047172470-4](https://en.wikipedia.org/wiki/Special:BookSources/978-047172470-4 "Special:BookSources/978-047172470-4").

[^2]: Lanczos, C. (1952). ["Solution of systems of linear equations by minimized iterations"](https://doi.org/10.6028%2Fjres.049.006). *Journal of Research of the National Bureau of Standards*. **49** (1): 33. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.6028/jres.049.006](https://doi.org/10.6028%2Fjres.049.006).

[^3]: Chebyshev first presented his eponymous polynomials in a paper read before the St. Petersburg Academy in 1853: Chebyshev, P. L. (1854). ["Théorie des mécanismes connus sous le nom de parallélogrammes"](https://archive.org/details/mmoiresprsentsla07impe/page/537/). *Mémoires des Savants étrangers présentés à l'Académie de Saint-Pétersbourg* (in French). **7**: 539–586. Also published separately as Chebyshev, P. L. (1853). *Théorie des mécanismes connus sous le nom de parallélogrammes*. St. Petersburg: Imprimerie de l'Académie Impériale des Sciences. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.3931/E-RARA-120037](https://doi.org/10.3931%2FE-RARA-120037).

[^4]: Schaeffer, A. C. (1941). ["Inequalities of A. Markoff and S. Bernstein for polynomials and related functions"](https://projecteuclid.org/journals/bulletin-of-the-american-mathematical-society/volume-47/issue-8/Inequalities-of-A-Markoff-and-S-Bernstein-for-polynomials-and/bams/1183503783.full). *Bulletin of the American Mathematical Society*. **47** (8): 565–579. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1090/S0002-9904-1941-07510-5](https://doi.org/10.1090%2FS0002-9904-1941-07510-5). [ISSN](https://en.wikipedia.org/wiki/ISSN_\(identifier\) "ISSN (identifier)") [0002-9904](https://search.worldcat.org/issn/0002-9904).

[^5]: [Ritt, J. F.](https://en.wikipedia.org/wiki/Joseph_Ritt "Joseph Ritt") (1922). ["Prime and Composite Polynomials"](https://www.ams.org/journals/tran/1922-023-01/S0002-9947-1922-1501189-9). *Trans. Amer. Math. Soc*. **23**: 51–66. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1090/S0002-9947-1922-1501189-9](https://doi.org/10.1090%2FS0002-9947-1922-1501189-9).

[^6]: Demeyer, Jeroen (2007). [*Diophantine sets over polynomial rings and Hilbert's tenth problem for function fields*](https://web.archive.org/web/20070702185523/https://cage.ugent.be/~jdemeyer/phd.pdf) (PDF) (Ph.D. thesis). p. 70. Archived from [the original](http://cage.ugent.be/~jdemeyer/phd.pdf) (PDF) on 2 July 2007.

[^7]: [Bateman & Bateman Manuscript Project 1953](#CITEREFBatemanBateman_Manuscript_Project1953), [p. 184, eqs. 3–4](https://archive.org/details/highertranscende02bate/page/184/).

[^8]: Beckenbach, E. F.; Seidel, W.; Szász, Otto (1951), "Recurrent determinants of Legendre and of ultraspherical polynomials", *Duke Math. J.*, **18**: 1–10, [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1215/S0012-7094-51-01801-7](https://doi.org/10.1215%2FS0012-7094-51-01801-7), [MR](https://en.wikipedia.org/wiki/MR_\(identifier\) "MR (identifier)") [0040487](https://mathscinet.ams.org/mathscinet-getitem?mr=0040487)

[^9]: [Bateman & Bateman Manuscript Project 1953](#CITEREFBatemanBateman_Manuscript_Project1953), [p. 187, eqs. 47–48](https://archive.org/details/highertranscende02bate/page/187/).

[^10]: [Mason & Handscomb 2002](#CITEREFMasonHandscomb2002).

[^11]: Cody, W.J. (1970). "A survey of practical rational and polynomial approximation of functions". *[SIAM Review](https://en.wikipedia.org/wiki/SIAM_Review "SIAM Review")*. **12** (3): 400–423. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1137/1012082](https://doi.org/10.1137%2F1012082).

[^12]: Mathar, Richard J. (2006). ["Chebyshev series expansion of inverse polynomials"](https://doi.org/10.1016%2Fj.cam.2005.10.013). *Journal of Computational and Applied Mathematics*. **196** (2): 596–607. [arXiv](https://en.wikipedia.org/wiki/ArXiv_\(identifier\) "ArXiv (identifier)"):[math/0403344](https://arxiv.org/abs/math/0403344). [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1016/j.cam.2005.10.013](https://doi.org/10.1016%2Fj.cam.2005.10.013).

[^13]: Gürtaş, Y. Z. (2017). "Chebyshev Polynomials and the minimal polynomial of ${\displaystyle \cos(2\pi /n)}$ ". *American Mathematical Monthly*. **124** (1): 74–78. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.4169/amer.math.monthly.124.1.74](https://doi.org/10.4169%2Famer.math.monthly.124.1.74). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [125797961](https://api.semanticscholar.org/CorpusID:125797961).

[^14]: Wolfram, D. A. (2022). "Factoring Chebyshev polynomials of the first and second kinds with minimal polynomials of ${\displaystyle \cos(2\pi /d)}$ ". *American Mathematical Monthly*. **129** (2): 172–176. [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1080/00029890.2022.2005391](https://doi.org/10.1080%2F00029890.2022.2005391). [S2CID](https://en.wikipedia.org/wiki/S2CID_\(identifier\) "S2CID (identifier)") [245808448](https://api.semanticscholar.org/CorpusID:245808448).

[^15]: Rayes, M. O.; Trevisan, V.; Wang, P. S. (2005), "Factorization properties of chebyshev polynomials", *Computers & Mathematics with Applications*, **50** (8–9): 1231–1240, [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1016/j.camwa.2005.07.003](https://doi.org/10.1016%2Fj.camwa.2005.07.003)

[^16]: Boyd, John P. (2001). [*Chebyshev and Fourier Spectral Methods*](https://web.archive.org/web/20100331183829/http://www-personal.umich.edu/~jpboyd/aaabook_9500may00.pdf) (PDF) (second ed.). Dover. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [0-486-41183-4](https://en.wikipedia.org/wiki/Special:BookSources/0-486-41183-4 "Special:BookSources/0-486-41183-4"). Archived from [the original](http://www-personal.umich.edu/~jpboyd/aaabook_9500may00.pdf) (PDF) on 31 March 2010. Retrieved 19 March 2009.

[^17]: ["Chebyshev Interpolation: An Interactive Tour"](https://web.archive.org/web/20170318214311/http://www.scottsarra.org/chebyApprox/chebyshevApprox.html). Archived from [the original](http://www.scottsarra.org/chebyApprox/chebyshevApprox.html) on 18 March 2017. Retrieved 2 June 2016.

[^18]: [Hochstrasser 1972](#CITEREFHochstrasser1972), p. 778.

[^19]: Horadam, A. F. (2002), ["Vieta polynomials"](https://www.fq.math.ca/Scanned/40-3/horadam2.pdf) (PDF), *Fibonacci Quarterly*, **40** (3): 223–232

[^20]: Viète, François (1646). [*Francisci Vietae Opera mathematica: in unum volumen congesta ac recognita / opera atque studio Francisci a Schooten*](https://gallica.bnf.fr/ark:/12148/bpt6k107597d.pdf) (PDF). Bibliothèque nationale de France.

[^21]: Mason, J. C.; Elliott, G. H. (1993), "Near-minimax complex approximation by four kinds of Chebyshev polynomial expansion", *J. Comput. Appl. Math.*, **46** (1–2): 291–300, [doi](https://en.wikipedia.org/wiki/Doi_\(identifier\) "Doi (identifier)"):[10.1016/0377-0427(93)90303-S](https://doi.org/10.1016%2F0377-0427%2893%2990303-S)

[^22]: Desmarais, Robert N.; Bland, Samuel R. (1995), ["Tables of properties of airfoil polynomials"](https://ntrs.nasa.gov/citations/19960001864), *NASA Reference Publication 1343*, National Aeronautics and Space Administration

[^23]: Kéri, Gerzson (2021): Compressed Chebyshev Polynomials and Multiple-Angle Formulas, Omniscriptum Publishing Company, ISBN 978-620-0-62498-7.

[^24]: Saal, Rudolf (January 1979). [*Handbook of Filter Design*](https://archive.org/details/handbuchzumfilte0000saal) (in English and German) (1st ed.). Munich, Germany: Allgemeine Elektricitais-Gesellschaft. pp. 25, 26, 56–61, 116, 117. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [3-87087-070-2](https://en.wikipedia.org/wiki/Special:BookSources/3-87087-070-2 "Special:BookSources/3-87087-070-2").