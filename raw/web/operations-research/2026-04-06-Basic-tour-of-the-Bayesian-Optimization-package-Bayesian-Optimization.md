---
source_type: web
title: "Basic tour of the Bayesian Optimization package - Bayesian Optimization"
author: 
created_at: 2026-04-06
status: summarized
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://bayesian-optimization.github.io/BayesianOptimization/1.5.1/basic-tour.html"
published_at: null
related_concepts:
  - 运筹优化
  - 贝叶斯优化
  - 数学优化
topics:
  - operations-research
  - 数学优化算法/运筹学
---

## Basic tour of the Bayesian Optimization package

This is a constrained global optimization package built upon bayesian inference and gaussian process, that attempts to find the maximum value of an unknown function in as few iterations as possible. This technique is particularly suited for optimization of high cost functions, situations where the balance between exploration and exploitation is important.

Bayesian optimization works by constructing a posterior distribution of functions (gaussian process) that best describes the function you want to optimize. As the number of observations grows, the posterior distribution improves, and the algorithm becomes more certain of which regions in parameter space are worth exploring and which are not, as seen in the picture below.

As you iterate over and over, the algorithm balances its needs of exploration and exploitation taking into account what it knows about the target function. At each step a Gaussian Process is fitted to the known samples (points previously explored), and the posterior distribution, combined with a exploration strategy (such as UCB (Upper Confidence Bound), or EI (Expected Improvement)), are used to determine the next point that should be explored (see the gif below).

This process is designed to minimize the number of steps required to find a combination of parameters that are close to the optimal combination. To do so, this method uses a proxy optimization problem (finding the maximum of the acquisition function) that, albeit still a hard problem, is cheaper (in the computational sense) and common tools can be employed. Therefore Bayesian Optimization is most adequate for situations where sampling the function to be optimized is a very expensive endeavor. See the references for a proper discussion of this method.

## 1\. Specifying the function to be optimized

This is a function optimization package, therefore the first and most important ingredient is, of course, the function to be optimized.

**DISCLAIMER:** We know exactly how the output of the function below depends on its parameter. Obviously this is just an example, and you shouldn’t expect to know it in a real scenario. However, it should be clear that you don’t need to. All you need in order to use this package (and more generally, this technique) is a function `f` that takes a known set of parameters and outputs a real number.

```js
[1]:
```

```js
def black_box_function(x, y):
    """Function with unknown internals we wish to maximize.

    This is just serving as an example, for all intents and
    purposes think of the internals of this function, i.e.: the process
    which generates its output values, as unknown.
    """
    return -x ** 2 - (y - 1) ** 2 + 1
```

## 2\. Getting Started

All we need to get started is to instantiate a `BayesianOptimization` object specifying a function to be optimized `f`, and its parameters with their corresponding bounds, `pbounds`. This is a constrained optimization technique, so you must specify the minimum and maximum values that can be probed for each parameter in order for it to work

```js
[2]:
```

```js
from bayes_opt import BayesianOptimization
```

```js
[3]:
```

```js
# Bounded region of parameter space
pbounds = {'x': (2, 4), 'y': (-3, 3)}
```

```js
[4]:
```

```js
optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds=pbounds,
    verbose=2, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=1,
)
```

The BayesianOptimization object will work out of the box without much tuning needed. The main method you should be aware of is `maximize`, which does exactly what you think it does.

There are many parameters you can pass to maximize, nonetheless, the most important ones are: - `n_iter`: How many steps of bayesian optimization you want to perform. The more steps the more likely to find a good maximum you are. - `init_points`: How many steps of **random** exploration you want to perform. Random exploration can help by diversifying the exploration space.

```js
[5]:
```

```js
optimizer.maximize(
    init_points=2,
    n_iter=3,
)
```

```js
|   iter    |  target   |     x     |     y     |
-------------------------------------------------
| 1         | -7.135    | 2.834     | 1.322     |
| 2         | -7.78     | 2.0       | -1.186    |
| 3         | -7.11     | 2.218     | -0.7867   |
| 4         | -12.4     | 3.66      | 0.9608    |
| 5         | -6.999    | 2.23      | -0.7392   |
=================================================
```

The best combination of parameters and target value found can be accessed via the property `bo.max`.

```js
[6]:
```

```js
print(optimizer.max)
```

```js
{'target': -6.999472814518675, 'params': {'x': 2.2303920156083024, 'y': -0.7392021938893159}}
```

While the list of all parameters probed and their corresponding target values is available via the property `bo.res`.

```js
[7]:
```

```js
for i, res in enumerate(optimizer.res):
    print("Iteration {}: \n\t{}".format(i, res))
```

```js
Iteration 0:
        {'target': -7.135455292718879, 'params': {'x': 2.8340440094051482, 'y': 1.3219469606529488}}
Iteration 1:
        {'target': -7.779531005607566, 'params': {'x': 2.0002287496346898, 'y': -1.1860045642089614}}
Iteration 2:
        {'target': -7.109925819441113, 'params': {'x': 2.2175526295255183, 'y': -0.7867249801593896}}
Iteration 3:
        {'target': -12.397162416009818, 'params': {'x': 3.660003815774634, 'y': 0.9608275029525108}}
Iteration 4:
        {'target': -6.999472814518675, 'params': {'x': 2.2303920156083024, 'y': -0.7392021938893159}}
```

### 2.1 Changing bounds

During the optimization process you may realize the bounds chosen for some parameters are not adequate. For these situations you can invoke the method `set_bounds` to alter them. You can pass any combination of **existing** parameters and their associated new bounds.

```js
[8]:
```

```js
optimizer.set_bounds(new_bounds={"x": (-2, 3)})
```

```js
[9]:
```

```js
optimizer.maximize(
    init_points=0,
    n_iter=5,
)
```

```js
|   iter    |  target   |     x     |     y     |
-------------------------------------------------
| 6         | -2.942    | 1.98      | 0.8567    |
| 7         | -0.4597   | 1.096     | 1.508     |
| 8         | 0.5304    | -0.6807   | 1.079     |
| 9         | -5.33     | -1.526    | 3.0       |
| 10        | -5.419    | -2.0      | -0.5552   |
=================================================
```

## 3\. Guiding the optimization

It is often the case that we have an idea of regions of the parameter space where the maximum of our function might lie. For these situations the `BayesianOptimization` object allows the user to specify specific points to be probed. By default these will be explored lazily (`lazy=True`), meaning these points will be evaluated only the next time you call `maximize`. This probing process happens before the gaussian process takes over.

Parameters can be passed as dictionaries such as below:

```js
[10]:
```

```js
optimizer.probe(
    params={"x": 0.5, "y": 0.7},
    lazy=True,
)
```

Or as an iterable. Beware that the order has to be alphabetical. You can usee `optimizer.space.keys` for guidance

```js
[11]:
```

```js
print(optimizer.space.keys)
```

```js
['x', 'y']
```

```js
[12]:
```

```js
optimizer.probe(
    params=[-0.3, 0.1],
    lazy=True,
)
```

```js
[13]:
```

```js
optimizer.maximize(init_points=0, n_iter=0)
```

```js
|   iter    |  target   |     x     |     y     |
-------------------------------------------------
| 11        | 0.66      | 0.5       | 0.7       |
| 12        | 0.1       | -0.3      | 0.1       |
=================================================
```

By default you can follow the progress of your optimization by setting `verbose>0` when instantiating the `BayesianOptimization` object. If you need more control over logging/alerting you will need to use an observer. For more information about observers checkout the advanced tour notebook. Here we will only see how to use the native `JSONLogger` object to save to and load progress from files.

### 4.1 Saving progress

```js
[14]:
```

```js
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
```

The observer paradigm works by: 1. Instantiating an observer object. 2. Tying the observer object to a particular event fired by an optimizer.

The `BayesianOptimization` object fires a number of internal events during optimization, in particular, every time it probes the function and obtains a new parameter-target combination it will fire an `Events.OPTIMIZATION_STEP` event, which our logger will listen to.

**Caveat:** The logger will not look back at previously probed points.

```js
[15]:
```

```js
logger = JSONLogger(path="./logs.log")
optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
```

```js
[16]:
```

```js
optimizer.maximize(
    init_points=2,
    n_iter=3,
)
```

```js
|   iter    |  target   |     x     |     y     |
-------------------------------------------------
| 13        | -12.48    | -1.266    | -2.446    |
| 14        | -3.854    | -1.069    | -0.9266   |
| 15        | -3.594    | 0.7709    | 3.0       |
| 16        | 0.8238    | 0.03434   | 1.418     |
| 17        | 0.9721    | -0.1051   | 0.87      |
=================================================
```

Naturally, if you stored progress you will be able to load that onto a new instance of `BayesianOptimization`. The easiest way to do it is by invoking the `load_logs` function, from the `util` submodule.

```js
[17]:
```

```js
from bayes_opt.util import load_logs
```

```js
[18]:
```

```js
new_optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds={"x": (-2, 2), "y": (-2, 2)},
    verbose=2,
    random_state=7,
)
print(len(new_optimizer.space))
```

```js
0
```

```js
[19]:
```

```js
load_logs(new_optimizer, logs=["./logs.log"]);
```

```js
[20]:
```

```js
print("New optimizer is now aware of {} points.".format(len(new_optimizer.space)))
```

```js
New optimizer is now aware of 5 points.
```

```js
[21]:
```

```js
new_optimizer.maximize(
    init_points=0,
    n_iter=10,
)
```

```js
|   iter    |  target   |     x     |     y     |
-------------------------------------------------
| 1         | -3.548    | -2.0      | 1.74      |
| 2         | -3.041    | 1.914     | 0.3844    |
| 3         | -12.0     | 2.0       | -2.0      |
| 4         | -3.969    | 2.0       | 1.984     |
| 5         | -0.7794   | -1.238    | 0.5022    |
| 6         | 0.529     | 0.685     | 0.9576    |
| 7         | 0.2987    | 0.1242    | 0.1718    |
| 8         | 0.9544    | 0.2123    | 0.9766    |
| 9         | 0.7157    | -0.437    | 1.305     |
| 10        | 0.983     | -0.06785  | 1.111     |
=================================================
```

This tour should be enough to cover most usage scenarios of this package. If, however, you feel like you need to know more, please checkout the `advanced-tour` notebook. There you will be able to find other, more advanced features of this package that could be what you’re looking for. Also, browse the examples folder for implementation tips and ideas.