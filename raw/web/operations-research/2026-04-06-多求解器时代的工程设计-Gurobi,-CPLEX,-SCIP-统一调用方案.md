---
source_type: web
title: "多求解器时代的工程设计 Gurobi, CPLEX, SCIP 统一调用方案"
author:
  - 
  - "[[王源]]"
created_at: 2026-04-06
status: summarized
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://mp.weixin.qq.com/s/9z1TfR0XB58CCRAf-ccPxw"
published_at: null
related_concepts:
  - 运筹优化
  - 整数规划
  - 数学优化
topics:
  - operations-research
  - 数学优化算法/运筹学
---

原创 王源 *2026年2月27日 12:04*

在运筹优化算法工程里，我们经常会遇到一个很现实的问题：

- 数学模型是通用的（变量、约束、目标）
- 但不同的求解器 API 完全不同（Gurobi / CPLEX / SCIP 各有各的调用方式）
- 一旦业务代码里直接写死某个求解器，后续如果要切换、对比和扩展求解器都会很痛苦

如果不对求解器的行为进行抽象，想要支持多种不同求解器切换，对比和扩展，那么业务代码很容易写成这样（伪代码）：

```
if solver_name == "gurobi":
    # Gurobi API 建模 + 求解
elif solver_name == "cplex":
    # CPLEX API 建模 + 求解
elif solver_name == "scip":
    # SCIP API 建模 + 求解
```

上述代码采用了三个if-else逻辑来实现三种不同求解器的切换，对比和扩展。这么做短期是没有问题的，但是从工程化的角度来看长期会出现几个典型痛点：

1. 业务代码和求解器 API 强耦合：业务逻辑里混杂了大量 `Gurobi/CPLEX/SCIP` 求解器API实现的细节，后续维护成本高。
2. 切换求解器代价高：想做 solver A/B 测试（比如对比 Gurobi 和 SCIP 的求解效果），往往需要增加或者修改很多代码，无法做到优雅地无缝切换不同求解器。
3. 扩展新的求解器比较困难：后续如果新增 HiGHS、CBC、Xpress等新的求解器时，if-else/switch 会越来越长。
4. 测试困难：如果想测试“业务逻辑在 infeasible/time-limit 下怎么处理”，没有统一接口就很难做 mock。

针对以上痛点，这篇文章用一个简化的 Python 示例，讲清楚如何用 **策略模式（Strategy）+ 工厂模式（Factory）** 来抽象求解器行为，让你的求解器调用层变得“可插拔、可维护、可扩展”，从而达到可以优雅的无缝切换，对比和扩展多种不同的求解器。

##### 1 策略模式+工厂模式简介

策略模式和工厂模式属于常见的设计模式。如果学习过设计模式的同学应该对这两个概念不陌生，我们这里就简单回顾一下这两个经典的设计模式，并且初步展示如何采用这两个设计模式来对求解器的行为进行抽象。

策略模式的核心思想：把一组可互换的算法/行为封装成独立对象，并通过统一接口对外提供能力。

如果对应到本文所关心的求解器场景里：

- GurobiStrategy类：封装Gurobi的API调用细节
- CplexStrategy类：封装CPLEX的API调用细节
- ScipStrategy类：封装SCIP的API调用细节

以上三个具体的类都实现一个相同的接口函数，比如：

```
solve(model, config) -> result
```

这样业务层只需调用solve函数接口，在业务层就不需要感知底层具体是在调用哪家求解器。

工厂模式的核心思想是：把对象创建逻辑集中管理，调用方不直接 new 具体类，而是向工厂“要”对象。

如果对应到本文所关心的求解器场景里：

- 输入 Gurobi 工厂类可以返回 GurobiStrategy类
- 输入 Cplex 工厂类可以返回 CplexStrategy类
- 输入 SCIP 工厂类可以返回 ScipStrategy类

这样业务层就不需要写大量 `if-else` 来创建不同求解器的对象。

将上述策略模式和工厂模式结合在一起使用，不同求解器的行为依靠策略模式进行抽象，创建具体的求解器对象依靠工厂模式。两者组合起来就形成了一个清晰的架构：策略模式负责“怎么做”，工厂模式负责“创建谁来做”。

##### 2 用策略模式抽象不同求解器行为

下面用一个简化 Python 示例说明思想。代码刻意简化，不依赖真实 Gurobi/CPLEX/SCIP 包，重点看结构帮助理解思想为主。

##### 2.1 定义通用数据结构（模型 / 配置 / 结果）

第一步不是写求解器，而是先定义一个“和具体 solver 无关”的统一接口层。

```
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

# =========================
# 通用抽象（不依赖具体求解器）
# =========================

@dataclass
class Variable:
    name: str
    lb: float = 0.0
    ub: float = float("inf")
    vtype: str = "C"   # C: continuous, I: integer, B: binary

@dataclass
class Constraint:
    name: str
    expr: Dict[str, float]   # 简化：线性表达式 dict[var_name] = coeff
    sense: str               # "<=", "==", ">="
    rhs: float

@dataclass
class Objective:
    sense: str               # "min" / "max"
    expr: Dict[str, float]
    constant: float = 0.0

@dataclass
class OptimizationModel:
    name: str
    variables: List[Variable] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    objective: Optional[Objective] = None

@dataclass
class SolverConfig:
    time_limit_sec: float = 60.0
    mip_gap: float = 1e-4
    threads: int = 1
    output_log: bool = True
    # 预留：求解器特有参数（如 Gurobi 的 MIPFocus，SCIP 的某些参数）
    backend_params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SolveResult:
    status: str
    objective_value: Optional[float] = None
    variable_values: Dict[str, float] = field(default_factory=dict)
    message: str = ""
    solver_name: str = ""
```

很多人一上来就直接写 `GurobiStrategy` ，结果很容易把业务层和 solver API 又绑在一起。这里先定义 `OptimizationModel / SolverConfig / SolveResult` 的意义是：

1. 业务层和求解器层之间有了清晰边界
2. 上层只依赖统一抽象；下层负责把统一抽象“翻译”成具体求解器 API

这一步其实是整个设计能否长期维护的关键。

##### 2.2 定义策略接口：统一 solve() 行为

有了统一的数据结构，下一步定义策略接口。

```
# =========================
# 策略模式：统一接口
# =========================

class SolverStrategy(ABC):
    @abstractmethod
    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
```

这段代码的意义很直接：不管是 Gurobi、CPLEX 还是 SCIP，对外都必须提供 `solve(model, config)` 接口，并且返回统一的 `SolveResult` ，这样业务层只要拿到一个 `SolverStrategy` 对象，就能调用求解器实现求解，而不需要知道它具体是哪种 solver。

##### 2.3 具体策略实现：把差异封装进各自类中

下面是三个简化版策略类，分别对应三个不同的求解器的具体实现的策略类。注意：这里不实现真实 API，只展示“结构与职责”，大家体会这个思想即可。

```
# =========================
# 具体策略：不同求解器实现
# =========================

class GurobiStrategy(SolverStrategy):
    @property
    def name(self) -> str:
        return"Gurobi"

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 真实实现中应包含：
        # 1) 创建 Gurobi env/model
        # 2) 参数映射（time_limit, mip_gap, threads...）
        # 3) 添加变量/约束/目标
        # 4) optimize()
        # 5) 读取状态与解，并映射成 SolveResult

        print(f"[{self.name}] build model: {model.name}")
        print(f"[{self.name}] set params: time_limit={config.time_limit_sec}, gap={config.mip_gap}")

        return SolveResult(
            status="OPTIMAL",
            objective_value=123.45,
            variable_values={"x": 2, "y": 6},
            message="Solved by Gurobi (demo)",
            solver_name=self.name,
        )

class CplexStrategy(SolverStrategy):
    @property
    def name(self) -> str:
        return"CPLEX"

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        print(f"[{self.name}] build model: {model.name}")
        print(f"[{self.name}] set params: threads={config.threads}")

        return SolveResult(
            status="OPTIMAL",
            objective_value=124.00,
            variable_values={"x": 2, "y": 6},
            message="Solved by CPLEX (demo)",
            solver_name=self.name,
        )

class ScipStrategy(SolverStrategy):
    @property
    def name(self) -> str:
        return"SCIP"

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        print(f"[{self.name}] build model: {model.name}")
        print(f"[{self.name}] backend params: {config.backend_params}")

        return SolveResult(
            status="FEASIBLE",
            objective_value=126.80,
            variable_values={"x": 1, "y": 7},
            message="Solved by SCIP (demo)",
            solver_name=self.name,
        )
```

关键点不是“类名”，而是职责划分： `GurobiStrategy` 的职责是 把通用模型翻译成 Gurobi API 调用，把通用参数映射成 Gurobi 参数和把 Gurobi 状态码映射成统一结果结构。 `CplexStrategy` 和 `ScipStrategy` 的职责和 `GurobiStrategy` 是完全相似的。

我们使用策略模式并不是为了使用设计模式去装逼，而是为了把变化点（在这个场景中就是各个求解器的差异）集中封装。这一步完成后，业务层就可以真正做到“只面向接口编程”，用户就可以真正做到调用求解器，但是不需要感知具体是什么求解器。

#### 3 用工厂模式创建不同的求解器对象

有了多个策略类之后，接下来要解决另一个问题：业务层如何根据配置选择并创建对应的策略对象？

通过 `if-else` 肯定是可以实现这个逻辑的。如果就是让业务层自己写 `if-else` 来决定创建哪个对象，这个创建的逻辑会散落在代码的各个地方。工厂模式就是来收敛这部分逻辑的，让这部分创建的逻辑可以被集中管理。

```
# =========================
# 工厂模式：根据配置创建策略
# =========================

class SolverFactory:
    _registry = {
        "gurobi": GurobiStrategy,
        "cplex": CplexStrategy,
        "scip": ScipStrategy,
    }

    @classmethod
    def create(cls, solver_name: str) -> SolverStrategy:
        key = solver_name.strip().lower()
        if key notin cls._registry:
            raise ValueError(f"Unsupported solver: {solver_name}")
        return cls._registry[key]()
```

工厂模式实现：集中创建策略对象。这样业务层就统一创建入口，业务层不需要知道具体类名和构造逻辑，只需要：

```
strategy = SolverFactory.create("gurobi")
```

就可以完成对指定的gurobi求解器对象的创建。确实做到了优雅并且丝滑的调用不同的求解器。同时所有可用求解器在 `_registry` 中一目了然，便于后续维护。例如要新增一种求解器的时候，只需要新增一个策略类，同时将这个新增的策略类注册到工厂类就可以了。这么做的好处是就不需要对每一处涉及创建求解器的业务逻辑代码进行修改了。

#### 4 完整调用代码实例展示

最后看一个完整调用的代码示例，来真正展示业务层是如何使用策略模式+工厂模式：真正做到“切换求解器不改业务逻辑”。

```
# =========================
# 统一入口：业务层调用
# =========================

class SolverEngine:
    def __init__(self, strategy: SolverStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SolverStrategy):
        self.strategy = strategy

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 可在这里加：
        # - 模型合法性检查
        # - 统一日志
        # - 统计耗时
        # - 异常包装
        print(f"[Engine] use solver = {self.strategy.name}")
        result = self.strategy.solve(model, config)
        print(f"[Engine] status = {result.status}, obj = {result.objective_value}")
        return result
```
```
# =========================
# 统一入口：业务层调用
# =========================

class SolverEngine:
    def __init__(self, strategy: SolverStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SolverStrategy):
        self.strategy = strategy

    def solve(self, model: OptimizationModel, config: SolverConfig) -> SolveResult:
        # 可在这里加：
        # - 模型合法性检查
        # - 统一日志
        # - 统计耗时
        # - 异常包装
        print(f"[Engine] use solver = {self.strategy.name}")
        result = self.strategy.solve(model, config)
        print(f"[Engine] status = {result.status}, obj = {result.objective_value}")
        return result
def build_toy_model() -> OptimizationModel:
    model = OptimizationModel(name="toy_mip")

    model.variables.extend([
        Variable("x", lb=0, ub=100, vtype="I"),
        Variable("y", lb=0, ub=100, vtype="I"),
    ])

    # x + 2y <= 14
    model.constraints.append(
        Constraint(name="c1", expr={"x": 1, "y": 2}, sense="<=", rhs=14)
    )

    # 3x - y >= 0
    model.constraints.append(
        Constraint(name="c2", expr={"x": 3, "y": -1}, sense=">=", rhs=0)
    )

    # max 5x + 4y
    model.objective = Objective(sense="max", expr={"x": 5, "y": 4})

    return model

if __name__ == "__main__":
    model = build_toy_model()

    config = SolverConfig(
        time_limit_sec=30,
        mip_gap=1e-4,
        threads=4,
        output_log=True,
        backend_params={"scip/separating/maxrounds": 5}
    )

    # 关键点：只改这里就能切换求解器
    solver_name = "gurobi"   # 改成 "cplex" 或 "scip"
    strategy = SolverFactory.create(solver_name)

    engine = SolverEngine(strategy)
    result = engine.solve(model, config)

    print("\n=== Final Result ===")
    print("solver :", result.solver_name)
    print("status :", result.status)
```

这段示例代码最想表达的不是“跑出什么结果”，而是这件事：业务层构造模型和读取结果的代码完全不变，只通过工厂切换策略对象，就能切换底层求解器。这就是“策略模式 + 工厂模式”组合在运筹优化求解器调用中的核心价值。

#### 5 总结

本篇将两种非常常见的设计模式：策略模式和工厂模式，应用在实际的运筹优化工程项目中思路，并且结合实际代码讲解了具体实现逻辑。这个技巧对于实际落地应用的运筹优化项目开发非常有意义。对于运筹优化算法工程来说，真正难的往往不只是“把模型写出来”，也不是“设计高效的算法”，而是如何把建模、求解、工程维护这三件事长期协调好。

策略模式 + 工厂模式并不复杂，但用在“通用求解器调用层”上，能很好地帮助我们把 **稳定的业务建模逻辑** 和 **多变的求解器实现细节** 分开，这是一个非常值得在团队里推广的工程实践。

