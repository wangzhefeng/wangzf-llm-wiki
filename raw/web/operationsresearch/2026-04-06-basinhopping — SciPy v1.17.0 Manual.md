---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
published: null
source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html
source_type: web
status: inbox
tags:
- null
- clippings
title: basinhopping — SciPy v1.17.0 Manual
topics:
- 运筹优化
---

scipy.optimize.

## basinhopping

scipy.optimize.basinhopping(*func*, *x0*, *niter=100*, *T=1.0*, *stepsize=0.5*, *minimizer\_kwargs=None*, *take\_step=None*, *accept\_test=None*, *callback=None*, *interval=50*, *disp=False*, *niter\_success=None*, *rng=None*, *\**, *target\_accept\_rate=0.5*, *stepwise\_factor=0.9*, *seed=None*) [\[source\]](https://github.com/scipy/scipy/blob/v1.17.0/scipy/optimize/_basinhopping.py#L350-L742) [#](#scipy.optimize.basinhopping "Link to this definition")

Find the global minimum of a function using the basin-hopping algorithm.

Basin-hopping is a two-phase method that combines a global stepping algorithm with local minimization at each step. Designed to mimic the natural process of energy minimization of clusters of atoms, it works well for similar problems with “funnel-like, but rugged” energy landscapes [^8].

As the step-taking, step acceptance, and minimization methods are all customizable, this function can also be used to implement other two-phase methods.

Parameters:

**func** callable `f(x, *args)`

Function to be optimized. `args` can be passed as an optional item in the dict *minimizer\_kwargs*

**x0** array\_like

Initial guess.

**niter** integer, optional

The number of basin-hopping iterations. There will be a total of `niter + 1` runs of the local minimizer.

**T** float, optional

The “temperature” parameter for the acceptance or rejection criterion. Higher “temperatures” mean that larger jumps in function value will be accepted. For best results *T* should be comparable to the separation (in function value) between local minima.

**stepsize** float, optional

Maximum step size for use in the random displacement.

**minimizer\_kwargs** dict, optional

Extra keyword arguments to be passed to the local minimizer [`scipy.optimize.minimize`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize "scipy.optimize.minimize") Some important options could be:

methodstr

The minimization method (e.g. `"L-BFGS-B"`)

argstuple

Extra arguments passed to the objective function (*func*) and its derivatives (Jacobian, Hessian).

**take\_step** callable `take_step(x)`, optional

Replace the default step-taking routine with this routine. The default step-taking routine is a random displacement of the coordinates, but other step-taking algorithms may be better for some systems. *take\_step* can optionally have the attribute `take_step.stepsize`. If this attribute exists, then will adjust `take_step.stepsize` in order to try to optimize the global minimum search.

**accept\_test** callable, `accept_test(f_new=f_new, x_new=x_new, f_old=fold, x_old=x_old)`, optional

Define a test which will be used to judge whether to accept the step. This will be used in addition to the Metropolis test based on “temperature” *T*. The acceptable return values are True, False, or `"force accept"`. If any of the tests return False then the step is rejected. If the latter, then this will override any other tests in order to accept the step. This can be used, for example, to forcefully escape from a local minimum that is trapped in.

**callback** callable, `callback(x, f, accept)`, optional

A callback function which will be called for all minima found. `x` and `f` are the coordinates and function value of the trial minimum, and `accept` is whether that minimum was accepted. This can be used, for example, to save the lowest N minima found. Also, *callback* can be used to specify a user defined stop criterion by optionally returning True to stop the routine.

**interval** integer, optional

interval for how often to update the *stepsize*

**disp** bool, optional

Set to True to print status messages

**niter\_success** integer, optional

Stop the run if the global minimum candidate remains the same for this number of iterations.

**rng** {None, int, [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator "(in NumPy v2.4)") }, optional

If *rng* is passed by keyword, types other than [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator "(in NumPy v2.4)") are passed to [`numpy.random.default_rng`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng "(in NumPy v2.4)") to instantiate a `Generator`. If *rng* is already a `Generator` instance, then the provided instance is used. Specify *rng* for repeatable function behavior.

If this argument is passed by position or *seed* is passed by keyword, legacy behavior for the argument *seed* applies:

- If *seed* is None (or [`numpy.random`](https://numpy.org/doc/stable/reference/random/index.html#module-numpy.random "(in NumPy v2.4)")), the [`numpy.random.RandomState`](https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState "(in NumPy v2.4)") singleton is used.
- If *seed* is an int, a new `RandomState` instance is used, seeded with *seed*.
- If *seed* is already a `Generator` or `RandomState` instance then that instance is used.

Changed in version 1.15.0: As part of the [SPEC-007](https://scientific-python.org/specs/spec-0007/) transition from use of [`numpy.random.RandomState`](https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState "(in NumPy v2.4)") to [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator "(in NumPy v2.4)"), this keyword was changed from *seed* to *rng*. For an interim period, both keywords will continue to work, although only one may be specified at a time. After the interim period, function calls using the *seed* keyword will emit warnings. The behavior of both *seed* and *rng* are outlined above, but only the *rng* keyword should be used in new code.

The random numbers generated only affect the default Metropolis *accept\_test* and the default *take\_step*. If you supply your own *take\_step* and *accept\_test*, and these functions use random number generation, then those functions are responsible for the state of their random number generator.

**target\_accept\_rate** float, optional

The target acceptance rate that is used to adjust the *stepsize*. If the current acceptance rate is greater than the target, then the *stepsize* is increased. Otherwise, it is decreased. Range is (0, 1). Default is 0.5.

Added in version 1.8.0.

**stepwise\_factor** float, optional

The *stepsize* is multiplied or divided by this stepwise factor upon each update. Range is (0, 1). Default is 0.9.

Added in version 1.8.0.

Returns:

**res** OptimizeResult

The optimization result represented as a [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") object. Important attributes are: `x` the solution array, `fun` the value of the function at the solution, and `message` which describes the cause of the termination. The `OptimizeResult` object returned by the selected minimizer at the lowest minimum is also contained within this object and can be accessed through the `lowest_optimization_result` attribute. `lowest_optimization_result` will only be updated if a local minimization was successful. See [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") for a description of other attributes.

See also

[`minimize`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize "scipy.optimize.minimize")

The local minimization function called once for each basinhopping step. *minimizer\_kwargs* is passed to this routine.

Notes

Basin-hopping is a stochastic algorithm which attempts to find the global minimum of a smooth scalar function of one or more variables [^4] [^5] [^6] [^7]. The algorithm in its current form was described by David Wales and Jonathan Doye [^5] [http://www-wales.ch.cam.ac.uk/](http://www-wales.ch.cam.ac.uk/).

The algorithm is iterative with each cycle composed of the following features

1. random perturbation of the coordinates
2. local minimization
3. accept or reject the new coordinates based on the minimized function value

The acceptance test used here is the Metropolis criterion of standard Monte Carlo algorithms, although there are many other possibilities [^6].

This global minimization method has been shown to be extremely efficient for a wide variety of problems in physics and chemistry. It is particularly useful when the function has many minima separated by large barriers. See the [Cambridge Cluster Database](https://www-wales.ch.cam.ac.uk/CCD.html) for databases of molecular systems that have been optimized primarily using basin-hopping. This database includes minimization problems exceeding 300 degrees of freedom.

See the free software program [GMIN](https://www-wales.ch.cam.ac.uk/GMIN) for a Fortran implementation of basin-hopping. This implementation has many variations of the procedure described above, including more advanced step taking algorithms and alternate acceptance criterion.

For stochastic global optimization there is no way to determine if the true global minimum has actually been found. Instead, as a consistency check, the algorithm can be run from a number of different random starting points to ensure the lowest minimum found in each example has converged to the global minimum. For this reason, will by default simply run for the number of iterations *niter* and return the lowest minimum found. It is left to the user to ensure that this is in fact the global minimum.

Choosing *stepsize*: This is a crucial parameter in and depends on the problem being solved. The step is chosen uniformly in the region from x0-stepsize to x0+stepsize, in each dimension. Ideally, it should be comparable to the typical separation (in argument values) between local minima of the function being optimized. will, by default, adjust *stepsize* to find an optimal value, but this may take many iterations. You will get quicker results if you set a sensible initial value for `stepsize`.

Choosing *T*: The parameter *T* is the “temperature” used in the Metropolis criterion. Basinhopping steps are always accepted if `func(xnew) < func(xold)`. Otherwise, they are accepted with probability:

```
exp( -(func(xnew) - func(xold)) / T )
```

So, for best results, *T* should to be comparable to the typical difference (in function values) between local minima. (The height of “walls” between local minima is irrelevant.)

If *T* is 0, the algorithm becomes Monotonic Basin-Hopping, in which all steps that increase energy are rejected.

Added in version 0.12.0.

References

Examples

The following example is a 1-D minimization problem, with many local minima superimposed on a parabola.

```
>>> import numpy as np
>>> from scipy.optimize import basinhopping
>>> func = lambda x: np.cos(14.5 * x - 0.3) + (x + 0.2) * x
>>> x0 = [1.]
```

Basinhopping, internally, uses a local minimization algorithm. We will use the parameter *minimizer\_kwargs* to tell basinhopping which algorithm to use and how to set up that minimizer. This parameter will be passed to [`scipy.optimize.minimize`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize "scipy.optimize.minimize").

```
>>> minimizer_kwargs = {"method": "BFGS"}
>>> ret = basinhopping(func, x0, minimizer_kwargs=minimizer_kwargs,
...                    niter=200)
>>> # the global minimum is:
>>> ret.x, ret.fun
-0.1951, -1.0009
```

Next consider a 2-D minimization problem. Also, this time, we will use gradient information to significantly speed up the search.

```
>>> def func2d(x):
...     f = np.cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] +
...                                                            0.2) * x[0]
...     df = np.zeros(2)
...     df[0] = -14.5 * np.sin(14.5 * x[0] - 0.3) + 2. * x[0] + 0.2
...     df[1] = 2. * x[1] + 0.2
...     return f, df
```

We’ll also use a different local minimization algorithm. Also, we must tell the minimizer that our function returns both energy and gradient (Jacobian).

```
>>> minimizer_kwargs = {"method":"L-BFGS-B", "jac":True}
>>> x0 = [1.0, 1.0]
>>> ret = basinhopping(func2d, x0, minimizer_kwargs=minimizer_kwargs,
...                    niter=200)
>>> print("global minimum: x = [%.4f, %.4f], f(x) = %.4f" % (ret.x[0],
...                                                           ret.x[1],
...                                                           ret.fun))
global minimum: x = [-0.1951, -0.1000], f(x) = -1.0109
```

Here is an example using a custom step-taking routine. Imagine you want the first coordinate to take larger steps than the rest of the coordinates. This can be implemented like so:

```
>>> class MyTakeStep:
...    def __init__(self, stepsize=0.5):
...        self.stepsize = stepsize
...        self.rng = np.random.default_rng()
...    def __call__(self, x):
...        s = self.stepsize
...        x[0] += self.rng.uniform(-2.*s, 2.*s)
...        x[1:] += self.rng.uniform(-s, s, x[1:].shape)
...        return x
```

Since `MyTakeStep.stepsize` exists basinhopping will adjust the magnitude of *stepsize* to optimize the search. We’ll use the same 2-D function as before

```
>>> mytakestep = MyTakeStep()
>>> ret = basinhopping(func2d, x0, minimizer_kwargs=minimizer_kwargs,
...                    niter=200, take_step=mytakestep)
>>> print("global minimum: x = [%.4f, %.4f], f(x) = %.4f" % (ret.x[0],
...                                                           ret.x[1],
...                                                           ret.fun))
global minimum: x = [-0.1951, -0.1000], f(x) = -1.0109
```

Now, let’s do an example using a custom callback function which prints the value of every minimum found

```
>>> def print_fun(x, f, accepted):
...         print("at minimum %.4f accepted %d" % (f, int(accepted)))
```

We’ll run it for only 10 basinhopping steps this time.

```
>>> rng = np.random.default_rng()
>>> ret = basinhopping(func2d, x0, minimizer_kwargs=minimizer_kwargs,
...                    niter=10, callback=print_fun, rng=rng)
at minimum 0.4159 accepted 1
at minimum -0.4317 accepted 1
at minimum -1.0109 accepted 1
at minimum -0.9073 accepted 1
at minimum -0.4317 accepted 0
at minimum -0.1021 accepted 1
at minimum -0.7425 accepted 1
at minimum -0.9073 accepted 1
at minimum -0.4317 accepted 0
at minimum -0.7425 accepted 1
at minimum -0.9073 accepted 1
```

The minimum at -1.0109 is actually the global minimum, found already on the 8th iteration.

[^1]: Basin-hopping is a two-phase method that combines a global stepping algorithm with local minimization at each step. Designed to mimic the natural process of energy minimization of clusters of atoms, it works well for similar problems with “funnel-like, but rugged” energy landscapes

As the step-taking, step acceptance, and minimization methods are all customizable, this function can also be used to implement other two-phase methods.

Parameters:

**func** callable `f(x, *args)`

Function to be optimized. `args` can be passed as an optional item in the dict *minimizer\_kwargs*

**x0** array\_like

Initial guess.

**niter** integer, optional

The number of basin-hopping iterations. There will be a total of `niter + 1` runs of the local minimizer.

**T** float, optional

The “temperature” parameter for the acceptance or rejection criterion. Higher “temperatures” mean that larger jumps in function value will be accepted. For best results *T* should be comparable to the separation (in function value) between local minima.

**stepsize** float, optional

Maximum step size for use in the random displacement.

**minimizer\_kwargs** dict, optional

Extra keyword arguments to be passed to the local minimizer [`scipy.optimize.minimize`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize "scipy.optimize.minimize") Some important options could be:

methodstr

The minimization method (e.g. `"L-BFGS-B"`)

argstuple

Extra arguments passed to the objective function (*func*) and its derivatives (Jacobian, Hessian).

**take\_step** callable `take_step(x)`, optional

Replace the default step-taking routine with this routine. The default step-taking routine is a random displacement of the coordinates, but other step-taking algorithms may be better for some systems. *take\_step* can optionally have the attribute `take_step.stepsize`. If this attribute exists, then will adjust `take_step.stepsize` in order to try to optimize the global minimum search.

**accept\_test** callable, `accept_test(f_new=f_new, x_new=x_new, f_old=fold, x_old=x_old)`, optional

Define a test which will be used to judge whether to accept the step. This will be used in addition to the Metropolis test based on “temperature” *T*. The acceptable return values are True, False, or `"force accept"`. If any of the tests return False then the step is rejected. If the latter, then this will override any other tests in order to accept the step. This can be used, for example, to forcefully escape from a local minimum that is trapped in.

**callback** callable, `callback(x, f, accept)`, optional

A callback function which will be called for all minima found. `x` and `f` are the coordinates and function value of the trial minimum, and `accept` is whether that minimum was accepted. This can be used, for example, to save the lowest N minima found. Also, *callback* can be used to specify a user defined stop criterion by optionally returning True to stop the routine.

**interval** integer, optional

interval for how often to update the *stepsize*

**disp** bool, optional

Set to True to print status messages

**niter\_success** integer, optional

Stop the run if the global minimum candidate remains the same for this number of iterations.

**rng** {None, int, [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator "(in NumPy v2.4)") }, optional

If *rng* is passed by keyword, types other than [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator "(in NumPy v2.4)") are passed to [`numpy.random.default_rng`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng "(in NumPy v2.4)") to instantiate a `Generator`. If *rng* is already a `Generator` instance, then the provided instance is used. Specify *rng* for repeatable function behavior.

If this argument is passed by position or *seed* is passed by keyword, legacy behavior for the argument *seed* applies:

- If *seed* is None (or [`numpy.random`](https://numpy.org/doc/stable/reference/random/index.html#module-numpy.random "(in NumPy v2.4)")), the [`numpy.random.RandomState`](https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState "(in NumPy v2.4)") singleton is used.
- If *seed* is an int, a new `RandomState` instance is used, seeded with *seed*.
- If *seed* is already a `Generator` or `RandomState` instance then that instance is used.

Changed in version 1.15.0: As part of the [SPEC-007](https://scientific-python.org/specs/spec-0007/) transition from use of [`numpy.random.RandomState`](https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState "(in NumPy v2.4)") to [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.Generator "(in NumPy v2.4)"), this keyword was changed from *seed* to *rng*. For an interim period, both keywords will continue to work, although only one may be specified at a time. After the interim period, function calls using the *seed* keyword will emit warnings. The behavior of both *seed* and *rng* are outlined above, but only the *rng* keyword should be used in new code.

The random numbers generated only affect the default Metropolis *accept\_test* and the default *take\_step*. If you supply your own *take\_step* and *accept\_test*, and these functions use random number generation, then those functions are responsible for the state of their random number generator.

**target\_accept\_rate** float, optional

The target acceptance rate that is used to adjust the *stepsize*. If the current acceptance rate is greater than the target, then the *stepsize* is increased. Otherwise, it is decreased. Range is (0, 1). Default is 0.5.

Added in version 1.8.0.

**stepwise\_factor** float, optional

The *stepsize* is multiplied or divided by this stepwise factor upon each update. Range is (0, 1). Default is 0.9.

Added in version 1.8.0.

Returns:

**res** OptimizeResult

The optimization result represented as a [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") object. Important attributes are: `x` the solution array, `fun` the value of the function at the solution, and `message` which describes the cause of the termination. The `OptimizeResult` object returned by the selected minimizer at the lowest minimum is also contained within this object and can be accessed through the `lowest_optimization_result` attribute. `lowest_optimization_result` will only be updated if a local minimization was successful. See [`OptimizeResult`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html#scipy.optimize.OptimizeResult "scipy.optimize.OptimizeResult") for a description of other attributes.

See also

[`minimize`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize "scipy.optimize.minimize")

The local minimization function called once for each basinhopping step. *minimizer\_kwargs* is passed to this routine.

Notes

[^2]: Basin-hopping is a stochastic algorithm which attempts to find the global minimum of a smooth scalar function of one or more variables. The algorithm in its current form was described by David Wales and Jonathan Doye [http://www-wales.ch.cam.ac.uk/](http://www-wales.ch.cam.ac.uk/)

The algorithm is iterative with each cycle composed of the following features

1. random perturbation of the coordinates
2. local minimization
3. accept or reject the new coordinates based on the minimized function value

[^3]: The acceptance test used here is the Metropolis criterion of standard Monte Carlo algorithms, although there are many other possibilities

This global minimization method has been shown to be extremely efficient for a wide variety of problems in physics and chemistry. It is particularly useful when the function has many minima separated by large barriers. See the [Cambridge Cluster Database](https://www-wales.ch.cam.ac.uk/CCD.html) for databases of molecular systems that have been optimized primarily using basin-hopping. This database includes minimization problems exceeding 300 degrees of freedom.

See the free software program [GMIN](https://www-wales.ch.cam.ac.uk/GMIN) for a Fortran implementation of basin-hopping. This implementation has many variations of the procedure described above, including more advanced step taking algorithms and alternate acceptance criterion.

For stochastic global optimization there is no way to determine if the true global minimum has actually been found. Instead, as a consistency check, the algorithm can be run from a number of different random starting points to ensure the lowest minimum found in each example has converged to the global minimum. For this reason, will by default simply run for the number of iterations *niter* and return the lowest minimum found. It is left to the user to ensure that this is in fact the global minimum.

Choosing *stepsize*: This is a crucial parameter in and depends on the problem being solved. The step is chosen uniformly in the region from x0-stepsize to x0+stepsize, in each dimension. Ideally, it should be comparable to the typical separation (in argument values) between local minima of the function being optimized. will, by default, adjust *stepsize* to find an optimal value, but this may take many iterations. You will get quicker results if you set a sensible initial value for `stepsize`

Choosing *T*: The parameter *T* is the “temperature” used in the Metropolis criterion. Basinhopping steps are always accepted if `func(xnew) < func(xold)`. Otherwise, they are accepted with probability:

```
exp( -(func(xnew) - func(xold)) / T )
```

So, for best results, *T* should to be comparable to the typical difference (in function values) between local minima. (The height of “walls” between local minima is irrelevant.)

If *T* is 0, the algorithm becomes Monotonic Basin-Hopping, in which all steps that increase energy are rejected.

Added in version 0.12.0.

References

Examples

[^4]: \[[1](#id2)\]

Wales, David J. 2003, Energy Landscapes, Cambridge University Press, Cambridge, UK.

[^5]: \[2\] ([1](#id3),[2](#id6))

Wales, D J, and Doye J P K, Global Optimization by Basin-Hopping and the Lowest Energy Structures of Lennard-Jones Clusters Containing up to 110 Atoms. Journal of Physical Chemistry A, 1997, 101, 5111.

[^6]: \[3\] ([1](#id4),[2](#id7))

Li, Z. and Scheraga, H. A., Monte Carlo-minimization approach to the multiple-minima problem in protein folding, Proc. Natl. Acad. Sci. USA, 1987, 84, 6611.

[^7]: \[[4](#id5)\]

Wales, D. J. and Scheraga, H. A., Global optimization of clusters, crystals, and biomolecules, Science, 1999, 285, 1368.

[^8]: \[[5](#id1)\]

Olson, B., Hashmi, I., Molloy, K., and Shehu1, A., Basin Hopping as a General and Versatile Optimization Framework for the Characterization of Biological Macromolecules, Advances in Artificial Intelligence, Volume 2012 (2012), Article ID 674832, [DOI:10.1155/2012/674832](https://doi.org/10.1155/2012/674832)