---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
source_type: web
status: inbox
tags:
- null
- clippings
title: minimize — SciPy v1.17.0 Manual
source_url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize
published_at: null
related_concepts: []
topics:
  - operations-research
  - 数学优化算法/运筹学
---

scipy.optimize.

## minimize

scipy.optimize.minimize(*fun*, *x0*, *args=()*, *method=None*, *jac=None*, *hess=None*, *hessp=None*, *bounds=None*, *constraints=()*, *tol=None*, *callback=None*, *options=None*) [\[source\]](https://github.com/scipy/scipy/blob/v1.17.0/scipy/optimize/_minimize.py#L54-L828) [#](#scipy.optimize.minimize "Link to this definition")

Minimization of scalar function of one or more variables.

Parameters:

**fun** callable

The objective function to be minimized:

```
fun(x, *args) -> float
```

where `x` is a 1-D array with shape (n,) and `args` is a tuple of the fixed parameters needed to completely specify the function.

Suppose the callable has signature `f0(x, *my_args, **my_kwargs)`, where `my_args` and `my_kwargs` are required positional and keyword arguments. Rather than passing `f0` as the callable, wrap it to accept only `x`; e.g., pass `fun=lambda x: f0(x, *my_args, **my_kwargs)` as the callable, where `my_args` (tuple) and `my_kwargs` (dict) have been gathered before invoking this function.

**x0** ndarray, shape (n,)

Initial guess. Array of real elements of size (n,), where `n` is the number of independent variables.

**args** tuple, optional

Extra arguments passed to the objective function and its derivatives (*fun*, *jac* and *hess* functions).

**method** str or callable, optional

Type of solver. Should be one of

- ‘Nelder-Mead’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html#optimize-minimize-neldermead)
- ‘Powell’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-powell.html#optimize-minimize-powell)
- ‘CG’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cg.html#optimize-minimize-cg)
- ‘BFGS’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-bfgs.html#optimize-minimize-bfgs)
- ‘Newton-CG’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-newtoncg.html#optimize-minimize-newtoncg)
- ‘L-BFGS-B’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb)
- ‘TNC’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-tnc.html#optimize-minimize-tnc)
- ‘COBYLA’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html#optimize-minimize-cobyla)
- ‘COBYQA’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyqa.html#optimize-minimize-cobyqa)
- ‘SLSQP’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp)
- ‘trust-constr’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html#optimize-minimize-trustconstr)
- ‘dogleg’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-dogleg.html#optimize-minimize-dogleg)
- ‘trust-ncg’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustncg.html#optimize-minimize-trustncg)
- ‘trust-exact’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustexact.html#optimize-minimize-trustexact)
- ‘trust-krylov’ [(see here)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustkrylov.html#optimize-minimize-trustkrylov)
- custom - a callable object, see below for description.

If not given, chosen to be one of `BFGS`, `L-BFGS-B`, `SLSQP`, depending on whether or not the problem has constraints or bounds.

**jac** {callable, ‘2-point’, ‘3-point’, ‘cs’, bool}, optional

Method for computing the gradient vector. Only for CG, BFGS, Newton-CG, L-BFGS-B, TNC, SLSQP, dogleg, trust-ncg, trust-krylov, trust-exact and trust-constr. If it is a callable, it should be a function that returns the gradient vector:

```
jac(x, *args) -> array_like, shape (n,)
```

where `x` is an array with shape (n,) and `args` is a tuple with the fixed parameters. If *jac* is a Boolean and is True, *fun* is assumed to return a tuple `(f, g)` containing the objective function and the gradient. Methods ‘Newton-CG’, ‘trust-ncg’, ‘dogleg’, ‘trust-exact’, and ‘trust-krylov’ require that either a callable be supplied, or that *fun* return the objective and gradient. If None or False, the gradient will be estimated using 2-point finite difference estimation with an absolute step size. Alternatively, the keywords {‘2-point’, ‘3-point’, ‘cs’} can be used to select a finite difference scheme for numerical estimation of the gradient with a relative step size. These finite difference schemes obey any specified *bounds*.

**hess** {callable, ‘2-point’, ‘3-point’, ‘cs’, HessianUpdateStrategy}, optional

Method for computing the Hessian matrix. Only for Newton-CG, dogleg, trust-ncg, trust-krylov, trust-exact and trust-constr. If it is callable, it should return the Hessian matrix:

```
hess(x, *args) -> {LinearOperator, spmatrix, array}, (n, n)
```

where `x` is a (n,) ndarray and `args` is a tuple with the fixed parameters. The keywords {‘2-point’, ‘3-point’, ‘cs’} can also be used to select a finite difference scheme for numerical estimation of the hessian. Alternatively, objects implementing the [`HessianUpdateStrategy`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.HessianUpdateStrategy.html#scipy.optimize.HessianUpdateStrategy "scipy.optimize.HessianUpdateStrategy") interface can be used to approximate the Hessian. Available quasi-Newton methods implementing this interface are:

- [`BFGS`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.BFGS.html#scipy.optimize.BFGS "scipy.optimize.BFGS")
- [`SR1`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.SR1.html#scipy.optimize.SR1 "scipy.optimize.SR1")

Not all of the options are available for each of the methods; for availability refer to the notes.

**hessp** callable, optional

Hessian of objective function times an arbitrary vector p. Only for Newton-CG, trust-ncg, trust-krylov, trust-constr. Only one of *hessp* or *hess* needs to be given. If *hess* is provided, then *hessp* will be ignored. *hessp* must compute the Hessian times an arbitrary vector:

```
hessp(x, p, *args) ->  ndarray shape (n,)
```

where `x` is a (n,) ndarray, `p` is an arbitrary vector with dimension (n,) and `args` is a tuple with the fixed parameters.

**bounds** sequence or [`Bounds`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.Bounds.html#scipy.optimize.Bounds "scipy.optimize.Bounds"), optional

Bounds on variables for Nelder-Mead, L-BFGS-B, TNC, SLSQP, Powell, trust-constr, COBYLA, and COBYQA methods. There are two ways to specify the bounds:

1. Instance of [`Bounds`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.Bounds.html#scipy.optimize.Bounds "scipy.optimize.Bounds") class.
2. Sequence of `(min, max)` pairs for each element in *x*. None is used to specify no bound.

**constraints** {Constraint, dict} or List of {Constraint, dict}, optional

Constraints definition. Only for COBYLA, COBYQA, SLSQP and trust-constr.

Constraints for ‘trust-constr’, ‘cobyqa’, and ‘cobyla’ are defined as a single object or a list of objects specifying constraints to the optimization problem. Available constraints are:

- [`LinearConstraint`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.LinearConstraint.html#scipy.optimize.LinearConstraint "scipy.optimize.LinearConstraint")
- [`NonlinearConstraint`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.NonlinearConstraint.html#scipy.optimize.NonlinearConstraint "scipy.optimize.NonlinearConstraint")

Constraints for COBYLA, SLSQP are defined as a list of dictionaries. Each dictionary with fields:

typestr

Constraint type: ‘eq’ for equality, ‘ineq’ for inequality.

funcallable

The function defining the constraint.

jaccallable, optional

The Jacobian of *fun* (only for SLSQP).

argssequence, optional

Extra arguments to be passed to the function and Jacobian.

Equality constraint means that the constraint function result is to be zero whereas inequality means that it is to be non-negative.

**tol** float, optional

Tolerance for termination. When *tol* is specified, the selected minimization algorithm sets some relevant solver-specific tolerance(s) equal to *tol*. For detailed control, use solver-specific options.

**options** dict, optional

A dictionary of solver options. All methods except *TNC* accept the following generic options:

maxiterint

Maximum number of iterations to perform. Depending on the method each iteration may use several function evaluations.

For *TNC* use *maxfun* instead of *maxiter*.

dispbool

Set to True to print convergence messages.

For method-specific options, see [`show_options`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.show_options.html#scipy.optimize.show_options "scipy.optimize.show_options").

**callback** callable, optional

A callable called after each iteration.

All methods except TNC support a callable with the signature:

```
callback(intermediate_result: OptimizeResult)
```

where `intermediate_result` is a keyword parameter containing an [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") with attributes `x` and `fun`, the present values of the parameter vector and objective function. Not all attributes of [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") may be present. The name of the parameter must be `intermediate_result` for the callback to be passed an [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult"). These methods will also terminate if the callback raises `StopIteration`.

All methods except trust-constr (also) support a signature like:

```
callback(xk)
```

where `xk` is the current parameter vector.

Introspection is used to determine which of the signatures above to invoke.

Returns:

**res** OptimizeResult

The optimization result represented as a `OptimizeResult` object. Important attributes are: `x` the solution array, `success` a Boolean flag indicating if the optimizer exited successfully and `message` which describes the cause of the termination. See [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") for a description of other attributes.

See also

[`minimize_scalar`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html#scipy.optimize.minimize_scalar "scipy.optimize.minimize_scalar")

Interface to minimization algorithms for scalar univariate functions

[`show_options`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.show_options.html#scipy.optimize.show_options "scipy.optimize.show_options")

Additional options accepted by the solvers

Notes

This section describes the available solvers that can be selected by the ‘method’ parameter. The default method is *BFGS*.

**Unconstrained minimization**

Method [CG](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cg.html#optimize-minimize-cg) uses a nonlinear conjugate gradient algorithm by Polak and Ribiere, a variant of the Fletcher-Reeves method described in [^20] pp.120-122. Only the first derivatives are used.

Method [BFGS](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-bfgs.html#optimize-minimize-bfgs) uses the quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shanno (BFGS) [^20] pp. 136. It uses the first derivatives only. BFGS has proven good performance even for non-smooth optimizations. This method also returns an approximation of the Hessian inverse, stored as *hess\_inv* in the OptimizeResult object.

Method [Newton-CG](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-newtoncg.html#optimize-minimize-newtoncg) uses a Newton-CG algorithm [^20] pp. 168 (also known as the truncated Newton method). It uses a CG method to the compute the search direction. See also *TNC* method for a box-constrained minimization with a similar algorithm. Suitable for large-scale problems.

Method [dogleg](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-dogleg.html#optimize-minimize-dogleg) uses the dog-leg trust-region algorithm [^20] for unconstrained minimization. This algorithm requires the gradient and Hessian; furthermore the Hessian is required to be positive definite.

Method [trust-ncg](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustncg.html#optimize-minimize-trustncg) uses the Newton conjugate gradient trust-region algorithm [^20] for unconstrained minimization. This algorithm requires the gradient and either the Hessian or a function that computes the product of the Hessian with a given vector. Suitable for large-scale problems.

Method [trust-krylov](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustkrylov.html#optimize-minimize-trustkrylov) uses the Newton GLTR trust-region algorithm [^29], [^30] for unconstrained minimization. This algorithm requires the gradient and either the Hessian or a function that computes the product of the Hessian with a given vector. Suitable for large-scale problems. On indefinite problems it requires usually less iterations than the *trust-ncg* method and is recommended for medium and large-scale problems.

Method [trust-exact](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustexact.html#optimize-minimize-trustexact) is a trust-region method for unconstrained minimization in which quadratic subproblems are solved almost exactly [^28]. This algorithm requires the gradient and the Hessian (which is *not* required to be positive definite). It is, in many situations, the Newton method to converge in fewer iterations and the most recommended for small and medium-size problems.

**Bound-Constrained minimization**

Method [Nelder-Mead](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html#optimize-minimize-neldermead) uses the Simplex algorithm [^16], [^17]. This algorithm is robust in many applications. However, if numerical computation of derivative can be trusted, other algorithms using the first and/or second derivatives information might be preferred for their better performance in general.

Method [L-BFGS-B](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb) uses the L-BFGS-B algorithm [^21], [^22] for bound constrained minimization.

Method [Powell](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-powell.html#optimize-minimize-powell) is a modification of Powell’s method [^18], [^19] which is a conjugate direction method. It performs sequential one-dimensional minimizations along each vector of the directions set (*direc* field in *options* and *info*), which is updated at each iteration of the main minimization loop. The function need not be differentiable, and no derivatives are taken. If bounds are not provided, then an unbounded line search will be used. If bounds are provided and the initial guess is within the bounds, then every function evaluation throughout the minimization procedure will be within the bounds. If bounds are provided, the initial guess is outside the bounds, and *direc* is full rank (default has full rank), then some function evaluations during the first iteration may be outside the bounds, but every function evaluation after the first iteration will be within the bounds. If *direc* is not full rank, then some parameters may not be optimized and the solution is not guaranteed to be within the bounds.

Method [TNC](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-tnc.html#optimize-minimize-tnc) uses a truncated Newton algorithm [^20], [^23] to minimize a function with variables subject to bounds. This algorithm uses gradient information; it is also called Newton Conjugate-Gradient. It differs from the *Newton-CG* method described above as it wraps a C implementation and allows each variable to be given upper and lower bounds.

**Constrained Minimization**

Method [COBYLA](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html#optimize-minimize-cobyla) uses the PRIMA implementation [^34] of the Constrained Optimization BY Linear Approximation (COBYLA) method [^24], [^25], [^26]. The algorithm is based on linear approximations to the objective function and each constraint.

Method [COBYQA](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyqa.html#optimize-minimize-cobyqa) uses the Constrained Optimization BY Quadratic Approximations (COBYQA) method [^33]. The algorithm is a derivative-free trust-region SQP method based on quadratic approximations to the objective function and each nonlinear constraint. The bounds are treated as unrelaxable constraints, in the sense that the algorithm always respects them throughout the optimization process.

Method [SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp) uses Sequential Least SQuares Programming to minimize a function of several variables with any combination of bounds, equality and inequality constraints. The method wraps the SLSQP Optimization subroutine originally implemented by Dieter Kraft [^27]. Note that the wrapper handles infinite values in bounds by converting them into large floating values.

Method [trust-constr](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html#optimize-minimize-trustconstr) is a trust-region algorithm for constrained optimization. It switches between two implementations depending on the problem definition. It is the most versatile constrained minimization algorithm implemented in SciPy and the most appropriate for large-scale problems. For equality constrained problems it is an implementation of Byrd-Omojokun Trust-Region SQP method described in [^32] and in [^20], p. 549. When inequality constraints are imposed as well, it switches to the trust-region interior point method described in [^31]. This interior point algorithm, in turn, solves inequality constraints by introducing slack variables and solving a sequence of equality-constrained barrier problems for progressively smaller values of the barrier parameter. The previously described equality constrained SQP method is used to solve the subproblems with increasing levels of accuracy as the iterate gets closer to a solution.

**Finite-Difference Options**

For Method [trust-constr](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html#optimize-minimize-trustconstr) the gradient and the Hessian may be approximated using three finite-difference schemes: {‘2-point’, ‘3-point’, ‘cs’}. The scheme ‘cs’ is, potentially, the most accurate but it requires the function to correctly handle complex inputs and to be differentiable in the complex plane. The scheme ‘3-point’ is more accurate than ‘2-point’ but requires twice as many operations. If the gradient is estimated via finite-differences the Hessian must be estimated using one of the quasi-Newton strategies.

**Method specific options for the** *hess* **keyword**

| method/Hess | None | callable | ‘2-point/’3-point’/’cs’ | HUS |
| --- | --- | --- | --- | --- |
| Newton-CG | x | (n, n) LO | x | x |
| dogleg |  | (n, n) |  |  |
| trust-ncg |  | (n, n) | x | x |
| trust-krylov |  | (n, n) | x | x |
| trust-exact |  | (n, n) |  |  |
| trust-constr | x | (n, n) LO sp | x | x |

where LO=LinearOperator, sp=Sparse matrix, HUS=HessianUpdateStrategy

**Custom minimizers**

It may be useful to pass a custom minimization method, for example when using a frontend to this method such as [`scipy.optimize.basinhopping`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html#scipy.optimize.basinhopping "scipy.optimize.basinhopping") or a different library. You can simply pass a callable as the `method` parameter.

The callable is called as `method(fun, x0, args, **kwargs, **options)` where `kwargs` corresponds to any other parameters passed to (such as *callback*, *hess*, etc.), except the *options* dict, which has its contents also passed as *method* parameters pair by pair. Also, if *jac* has been passed as a bool type, *jac* and *fun* are mangled so that *fun* returns just the function values and *jac* is converted to a function returning the Jacobian. The method shall return an [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") object.

The provided *method* callable must be able to accept (and possibly ignore) arbitrary parameters; the set of parameters accepted by may expand in future versions and then these parameters will be passed to the method. You can find an example in the scipy.optimize tutorial.

References

Examples

Let us consider the problem of minimizing the Rosenbrock function. This function (and its respective derivatives) is implemented in [`rosen`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.rosen.html#scipy.optimize.rosen "scipy.optimize.rosen") (resp. [`rosen_der`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.rosen_der.html#scipy.optimize.rosen_der "scipy.optimize.rosen_der"), [`rosen_hess`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.rosen_hess.html#scipy.optimize.rosen_hess "scipy.optimize.rosen_hess")) in the [`scipy.optimize`](https://docs.scipy.org/doc/scipy/reference/optimize.html#module-scipy.optimize "scipy.optimize").

```
>>> from scipy.optimize import minimize, rosen, rosen_der
```

A simple application of the *Nelder-Mead* method is:

```
>>> x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
>>> res = minimize(rosen, x0, method='Nelder-Mead', tol=1e-6)
>>> res.x
array([ 1.,  1.,  1.,  1.,  1.])
```

Now using the *BFGS* algorithm, using the first derivative and a few options:

```
>>> res = minimize(rosen, x0, method='BFGS', jac=rosen_der,
...                options={'gtol': 1e-6, 'disp': True})
Optimization terminated successfully.
         Current function value: 0.000000
         Iterations: 26
         Function evaluations: 31
         Gradient evaluations: 31
>>> res.x
array([ 1.,  1.,  1.,  1.,  1.])
>>> print(res.message)
Optimization terminated successfully.
>>> res.hess_inv
array([
    [ 0.00749589,  0.01255155,  0.02396251,  0.04750988,  0.09495377],  # may vary
    [ 0.01255155,  0.02510441,  0.04794055,  0.09502834,  0.18996269],
    [ 0.02396251,  0.04794055,  0.09631614,  0.19092151,  0.38165151],
    [ 0.04750988,  0.09502834,  0.19092151,  0.38341252,  0.7664427 ],
    [ 0.09495377,  0.18996269,  0.38165151,  0.7664427,   1.53713523]
])
```

Next, consider a minimization problem with several constraints (namely Example 16.4 from [^20]). The objective function is:

```
>>> fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2
```

There are three constraints defined as:

```
>>> cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
...         {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
...         {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})
```

And variables must be positive, hence the following bounds:

```
>>> bnds = ((0, None), (0, None))
```

The optimization problem is solved using the SLSQP method as:

```
>>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)
```

It should converge to the theoretical solution `[1.4 ,1.7]`. *SLSQP* also returns the multipliers that are used in the solution of the problem. These multipliers, when the problem constraints are linear, can be thought of as the Karush-Kuhn-Tucker (KKT) multipliers, which are a generalization of Lagrange multipliers to inequality-constrained optimization problems ([^35]).

Notice that at the solution, the first constraint is active. Let’s evaluate the function at solution:

```
>>> cons[0]['fun'](res.x)
np.float64(1.4901224698604665e-09)
```

Also, notice that at optimality there is a non-zero multiplier:

```
>>> res.multipliers
array([0.8, 0. , 0. ])
```

This can be understood as the local sensitivity of the optimal value of the objective function with respect to changes in the first constraint. If we tighten the constraint by a small amount `eps`:

```
>>> eps = 0.01
>>> cons[0]['fun'] = lambda x: x[0] - 2 * x[1] + 2 - eps
```

we expect the optimal value of the objective function to increase by approximately `eps * res.multipliers[0]`:

```
>>> eps * res.multipliers[0]  # Expected change in f0
np.float64(0.008000000027153205)
>>> f0 = res.fun  # Keep track of the previous optimal value
>>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)
>>> f1 = res.fun  # New optimal value
>>> f1 - f0
np.float64(0.008019998807885509)
```

[^1]: Method [CG](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cg.html#optimize-minimize-cg) uses a nonlinear conjugate gradient algorithm by Polak and Ribiere, a variant of the Fletcher-Reeves method described in pp.120-122. Only the first derivatives are used.

[^2]: Method [BFGS](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-bfgs.html#optimize-minimize-bfgs) uses the quasi-Newton method of Broyden, Fletcher, Goldfarb, and Shanno (BFGS) pp. 136. It uses the first derivatives only. BFGS has proven good performance even for non-smooth optimizations. This method also returns an approximation of the Hessian inverse, stored as *hess\_inv* in the OptimizeResult object.

[^3]: Method [Newton-CG](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-newtoncg.html#optimize-minimize-newtoncg) uses a Newton-CG algorithm pp. 168 (also known as the truncated Newton method). It uses a CG method to the compute the search direction. See also *TNC* method for a box-constrained minimization with a similar algorithm. Suitable for large-scale problems.

[^4]: Method [dogleg](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-dogleg.html#optimize-minimize-dogleg) uses the dog-leg trust-region algorithm for unconstrained minimization. This algorithm requires the gradient and Hessian; furthermore the Hessian is required to be positive definite.

[^5]: Method [trust-ncg](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustncg.html#optimize-minimize-trustncg) uses the Newton conjugate gradient trust-region algorithm for unconstrained minimization. This algorithm requires the gradient and either the Hessian or a function that computes the product of the Hessian with a given vector. Suitable for large-scale problems.

[^6]: Method [trust-krylov](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustkrylov.html#optimize-minimize-trustkrylov) uses the Newton GLTR trust-region algorithm, for unconstrained minimization. This algorithm requires the gradient and either the Hessian or a function that computes the product of the Hessian with a given vector. Suitable for large-scale problems. On indefinite problems it requires usually less iterations than the *trust-ncg* method and is recommended for medium and large-scale problems.

[^7]: Method [trust-exact](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustexact.html#optimize-minimize-trustexact) is a trust-region method for unconstrained minimization in which quadratic subproblems are solved almost exactly. This algorithm requires the gradient and the Hessian (which is *not* required to be positive definite). It is, in many situations, the Newton method to converge in fewer iterations and the most recommended for small and medium-size problems.

**Bound-Constrained minimization**

[^8]: Method [Nelder-Mead](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html#optimize-minimize-neldermead) uses the Simplex algorithm,. This algorithm is robust in many applications. However, if numerical computation of derivative can be trusted, other algorithms using the first and/or second derivatives information might be preferred for their better performance in general.

[^9]: Method [L-BFGS-B](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html#optimize-minimize-lbfgsb) uses the L-BFGS-B algorithm, for bound constrained minimization.

[^10]: Method [Powell](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-powell.html#optimize-minimize-powell) is a modification of Powell’s method, which is a conjugate direction method. It performs sequential one-dimensional minimizations along each vector of the directions set (*direc* field in *options* and *info*), which is updated at each iteration of the main minimization loop. The function need not be differentiable, and no derivatives are taken. If bounds are not provided, then an unbounded line search will be used. If bounds are provided and the initial guess is within the bounds, then every function evaluation throughout the minimization procedure will be within the bounds. If bounds are provided, the initial guess is outside the bounds, and *direc* is full rank (default has full rank), then some function evaluations during the first iteration may be outside the bounds, but every function evaluation after the first iteration will be within the bounds. If *direc* is not full rank, then some parameters may not be optimized and the solution is not guaranteed to be within the bounds.

[^11]: Method [TNC](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-tnc.html#optimize-minimize-tnc) uses a truncated Newton algorithm, to minimize a function with variables subject to bounds. This algorithm uses gradient information; it is also called Newton Conjugate-Gradient. It differs from the *Newton-CG* method described above as it wraps a C implementation and allows each variable to be given upper and lower bounds.

**Constrained Minimization**

[^12]: Method [COBYLA](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html#optimize-minimize-cobyla) uses the PRIMA implementation of the Constrained Optimization BY Linear Approximation (COBYLA) method,,. The algorithm is based on linear approximations to the objective function and each constraint.

[^13]: Method [COBYQA](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyqa.html#optimize-minimize-cobyqa) uses the Constrained Optimization BY Quadratic Approximations (COBYQA) method. The algorithm is a derivative-free trust-region SQP method based on quadratic approximations to the objective function and each nonlinear constraint. The bounds are treated as unrelaxable constraints, in the sense that the algorithm always respects them throughout the optimization process.

[^14]: Method [SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp) uses Sequential Least SQuares Programming to minimize a function of several variables with any combination of bounds, equality and inequality constraints. The method wraps the SLSQP Optimization subroutine originally implemented by Dieter Kraft. Note that the wrapper handles infinite values in bounds by converting them into large floating values.

[^15]: Method [trust-constr](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html#optimize-minimize-trustconstr) is a trust-region algorithm for constrained optimization. It switches between two implementations depending on the problem definition. It is the most versatile constrained minimization algorithm implemented in SciPy and the most appropriate for large-scale problems. For equality constrained problems it is an implementation of Byrd-Omojokun Trust-Region SQP method described in and in, p. 549. When inequality constraints are imposed as well, it switches to the trust-region interior point method described in. This interior point algorithm, in turn, solves inequality constraints by introducing slack variables and solving a sequence of equality-constrained barrier problems for progressively smaller values of the barrier parameter. The previously described equality constrained SQP method is used to solve the subproblems with increasing levels of accuracy as the iterate gets closer to a solution.

**Finite-Difference Options**

For Method [trust-constr](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-trustconstr.html#optimize-minimize-trustconstr) the gradient and the Hessian may be approximated using three finite-difference schemes: {‘2-point’, ‘3-point’, ‘cs’}. The scheme ‘cs’ is, potentially, the most accurate but it requires the function to correctly handle complex inputs and to be differentiable in the complex plane. The scheme ‘3-point’ is more accurate than ‘2-point’ but requires twice as many operations. If the gradient is estimated via finite-differences the Hessian must be estimated using one of the quasi-Newton strategies.

**Method specific options for the** *hess* **keyword**

| method/Hess | None | callable | ‘2-point/’3-point’/’cs’ | HUS |
| --- | --- | --- | --- | --- |
| Newton-CG | x | (n, n) LO | x | x |
| dogleg |  | (n, n) |  |  |
| trust-ncg |  | (n, n) | x | x |
| trust-krylov |  | (n, n) | x | x |
| trust-exact |  | (n, n) |  |  |
| trust-constr | x | (n, n) LO sp | x | x |

where LO=LinearOperator, sp=Sparse matrix, HUS=HessianUpdateStrategy

**Custom minimizers**

It may be useful to pass a custom minimization method, for example when using a frontend to this method such as [`scipy.optimize.basinhopping`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html#scipy.optimize.basinhopping "scipy.optimize.basinhopping") or a different library. You can simply pass a callable as the `method` parameter.

The callable is called as `method(fun, x0, args, **kwargs, **options)` where `kwargs` corresponds to any other parameters passed to (such as *callback*, *hess*, etc.), except the *options* dict, which has its contents also passed as *method* parameters pair by pair. Also, if *jac* has been passed as a bool type, *jac* and *fun* are mangled so that *fun* returns just the function values and *jac* is converted to a function returning the Jacobian. The method shall return an [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") object.

The provided *method* callable must be able to accept (and possibly ignore) arbitrary parameters; the set of parameters accepted by may expand in future versions and then these parameters will be passed to the method. You can find an example in the scipy.optimize tutorial.

References

Examples

[^16]: \[[1](#id9)\]

Nelder, J A, and R Mead. 1965. A Simplex Method for Function Minimization. The Computer Journal 7: 308-13.

[^17]: \[[2](#id10)\]

Wright M H. 1996. Direct search methods: Once scorned, now respectable, in Numerical Analysis 1995: Proceedings of the 1995 Dundee Biennial Conference in Numerical Analysis (Eds. D F Griffiths and G A Watson). Addison Wesley Longman, Harlow, UK. 191-208.

[^18]: \[[3](#id13)\]

Powell, M J D. 1964. An efficient method for finding the minimum of a function of several variables without calculating derivatives. The Computer Journal 7: 155-162.

[^19]: \[[4](#id14)\]

Press W, S A Teukolsky, W T Vetterling and B P Flannery. Numerical Recipes (any edition), Cambridge University Press.

[^20]: \[5\] ([1](#id1),[2](#id2),[3](#id3),[4](#id4),[5](#id5),[6](#id15),[7](#id24),[8](#id46))

Nocedal, J, and S J Wright. 2006. Numerical Optimization. Springer New York.

[^21]: \[[6](#id11)\]

Byrd, R H and P Lu and J. Nocedal. 1995. A Limited Memory Algorithm for Bound Constrained Optimization. SIAM Journal on Scientific and Statistical Computing 16 (5): 1190-1208.

[^22]: \[[7](#id12)\]

Zhu, C and R H Byrd and J Nocedal. 1997. L-BFGS-B: Algorithm 778: L-BFGS-B, FORTRAN routines for large scale bound constrained optimization. ACM Transactions on Mathematical Software 23 (4): 550-560.

[^23]: \[[8](#id16)\]

Nash, S G. Newton-Type Minimization Via the Lanczos Method. 1984. SIAM Journal of Numerical Analysis 21: 770-778.

[^24]: \[[9](#id18)\]

Powell, M J D. A direct search optimization method that models the objective and constraint functions by linear interpolation. 1994. Advances in Optimization and Numerical Analysis, eds. S. Gomez and J-P Hennart, Kluwer Academic (Dordrecht), 51-67.

[^25]: \[[10](#id19)\]

Powell M J D. Direct search algorithms for optimization calculations. 1998. Acta Numerica 7: 287-336.

[^26]: \[[11](#id20)\]

Powell M J D. A view of algorithms for optimization without derivatives. 2007.Cambridge University Technical Report DAMTP 2007/NA03

[^27]: \[[12](#id22)\]

Kraft, D. A software package for sequential quadratic programming. 1988. Tech. Rep. DFVLR-FB 88-28, DLR German Aerospace Center – Institute for Flight Mechanics, Koln, Germany.

[^28]: \[[13](#id8)\]

Conn, A. R., Gould, N. I., and Toint, P. L. Trust region methods. 2000. Siam. pp. 169-200.

[^29]: \[[14](#id6)\]

F. Lenders, C. Kirches, A. Potschka: “trlib: A vector-free implementation of the GLTR method for iterative solution of the trust region problem”, [arXiv:1611.04718](https://arxiv.org/abs/1611.04718)

[^30]: \[[15](#id7)\]

N. Gould, S. Lucidi, M. Roma, P. Toint: “Solving the Trust-Region Subproblem using the Lanczos Method”, SIAM J. Optim., 9(2), 504–525, (1999).

[^31]: \[[16](#id25)\]

Byrd, Richard H., Mary E. Hribar, and Jorge Nocedal. 1999. An interior point algorithm for large-scale nonlinear programming. SIAM Journal on Optimization 9.4: 877-900.

[^32]: \[[17](#id23)\]

Lalee, Marucha, Jorge Nocedal, and Todd Plantenga. 1998. On the implementation of an algorithm for large-scale equality constrained optimization. SIAM Journal on Optimization 8.3: 682-706.

[^33]: \[[18](#id21)\]

Ragonneau, T. M. *Model-Based Derivative-Free Optimization Methods and Software*. PhD thesis, Department of Applied Mathematics, The Hong Kong Polytechnic University, Hong Kong, China, 2022. URL: [https://theses.lib.polyu.edu.hk/handle/200/12294](https://theses.lib.polyu.edu.hk/handle/200/12294).

[^34]: \[[19](#id17)\]

Zhang, Z. “PRIMA: Reference Implementation for Powell’s Methods with Modernization and Amelioration”, [https://www.libprima.net](https://www.libprima.net/), [DOI:10.5281/zenodo.8052654](https://doi.org/10.5281/zenodo.8052654)

[^35]: \[[20](#id47)\]

Karush-Kuhn-Tucker conditions, [https://en.wikipedia.org/wiki/Karush%E2%80%93Kuhn%E2%80%93Tucker\_conditions](https://en.wikipedia.org/wiki/Karush%E2%80%93Kuhn%E2%80%93Tucker_conditions)

[^36]: Let us consider the problem of minimizing the Rosenbrock function. This function (and its respective derivatives) is implemented in [`rosen`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.rosen.html#scipy.optimize.rosen "scipy.optimize.rosen") (resp. [`rosen_der`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.rosen_der.html#scipy.optimize.rosen_der "scipy.optimize.rosen_der"), [`rosen_hess`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.rosen_hess.html#scipy.optimize.rosen_hess "scipy.optimize.rosen_hess")) in the [`scipy.optimize`](https://docs.scipy.org/doc/scipy/reference/optimize.html#module-scipy.optimize "scipy.optimize").

```
>>> from scipy.optimize import minimize, rosen, rosen_der
```

A simple application of the *Nelder-Mead* method is:

```
>>> x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
>>> res = minimize(rosen, x0, method='Nelder-Mead', tol=1e-6)
>>> res.x
array([ 1.,  1.,  1.,  1.,  1.])
```

Now using the *BFGS* algorithm, using the first derivative and a few options:

```
>>> res = minimize(rosen, x0, method='BFGS', jac=rosen_der,
...                options={'gtol': 1e-6, 'disp': True})
Optimization terminated successfully.
         Current function value: 0.000000
         Iterations: 26
         Function evaluations: 31
         Gradient evaluations: 31
>>> res.x
array([ 1.,  1.,  1.,  1.,  1.])
>>> print(res.message)
Optimization terminated successfully.
>>> res.hess_inv
array([
    [ 0.00749589,  0.01255155,  0.02396251,  0.04750988,  0.09495377],  # may vary
    [ 0.01255155,  0.02510441,  0.04794055,  0.09502834,  0.18996269],
    [ 0.02396251,  0.04794055,  0.09631614,  0.19092151,  0.38165151],
    [ 0.04750988,  0.09502834,  0.19092151,  0.38341252,  0.7664427 ],
    [ 0.09495377,  0.18996269,  0.38165151,  0.7664427,   1.53713523]
])
```

Next, consider a minimization problem with several constraints (namely Example 16.4 from ). The objective function is:

```
>>> fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2
```

There are three constraints defined as:

```
>>> cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
...         {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
...         {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})
```

And variables must be positive, hence the following bounds:

```
>>> bnds = ((0, None), (0, None))
```

The optimization problem is solved using the SLSQP method as:

```
>>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)
```

It should converge to the theoretical solution `[1.4 ,1.7]`. *SLSQP* also returns the multipliers that are used in the solution of the problem. These multipliers, when the problem constraints are linear, can be thought of as the Karush-Kuhn-Tucker (KKT) multipliers, which are a generalization of Lagrange multipliers to inequality-constrained optimization problems ().

Notice that at the solution, the first constraint is active. Let’s evaluate the function at solution:

```
>>> cons[0]['fun'](res.x)
np.float64(1.4901224698604665e-09)
```

Also, notice that at optimality there is a non-zero multiplier:

```
>>> res.multipliers
array([0.8, 0. , 0. ])
```

This can be understood as the local sensitivity of the optimal value of the objective function with respect to changes in the first constraint. If we tighten the constraint by a small amount `eps`:

```
>>> eps = 0.01
>>> cons[0]['fun'] = lambda x: x[0] - 2 * x[1] + 2 - eps
```

we expect the optimal value of the objective function to increase by approximately `eps * res.multipliers[0]`:

```
>>> eps * res.multipliers[0]  # Expected change in f0
np.float64(0.008000000027153205)
>>> f0 = res.fun  # Keep track of the previous optimal value
>>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)
>>> f1 = res.fun  # New optimal value
>>> f1 - f0
np.float64(0.008019998807885509)
```

[^37]: It should converge to the theoretical solution `[1.4 ,1.7]`. *SLSQP* also returns the multipliers that are used in the solution of the problem. These multipliers, when the problem constraints are linear, can be thought of as the Karush-Kuhn-Tucker (KKT) multipliers, which are a generalization of Lagrange multipliers to inequality-constrained optimization problems ().

Notice that at the solution, the first constraint is active. Let’s evaluate the function at solution:

```
>>> cons[0]['fun'](res.x)
np.float64(1.4901224698604665e-09)
```

Also, notice that at optimality there is a non-zero multiplier:

```
>>> res.multipliers
array([0.8, 0. , 0. ])
```

This can be understood as the local sensitivity of the optimal value of the objective function with respect to changes in the first constraint. If we tighten the constraint by a small amount `eps`:

```
>>> eps = 0.01
>>> cons[0]['fun'] = lambda x: x[0] - 2 * x[1] + 2 - eps
```

we expect the optimal value of the objective function to increase by approximately `eps * res.multipliers[0]`:

```
>>> eps * res.multipliers[0]  # Expected change in f0
np.float64(0.008000000027153205)
>>> f0 = res.fun  # Keep track of the previous optimal value
>>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)
>>> f1 = res.fun  # New optimal value
>>> f1 - f0
np.float64(0.008019998807885509)
```