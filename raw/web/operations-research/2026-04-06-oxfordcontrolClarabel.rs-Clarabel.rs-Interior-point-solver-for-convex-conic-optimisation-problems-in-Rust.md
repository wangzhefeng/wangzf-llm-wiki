---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: 'Clarabel.rs: Interior-point solver for convex conic optimisation problems
  in Rust. - oxfordcontrol/Clarabel.rs'
source_type: web
status: inbox
tags:
- null
- clippings
title: 'oxfordcontrol/Clarabel.rs: Clarabel.rs: Interior-point solver for convex conic
  optimisation problems in Rust.'
source_url: https://github.com/oxfordcontrol/Clarabel.rs
published_at: null
related_concepts: []
topics:
  - operations-research
  - 数学优化算法/运筹学
---

![[logo-banner-dark-rs.png|Clarabel.jl logo]]

## Interior Point Conic Optimization for Rust and Python

[Features](#features) • [Installation](#installation) • [License](#license-) • [Documentation](https://clarabel.org/)

**Clarabel.rs** is a Rust implementation of an interior point numerical solver for convex optimization problems using a novel homogeneous embedding. Clarabel.rs solves the following problem:

$$
minimize
      
      
        
          1
          2
        
        
          x
          T
        
        P
        x
        +
        
          q
          T
        
        x
      
    
    
      
        subject to
      
      
        A
        x
        +
        s
        =
        b
      
    
    
      
      
        s
        ∈
        
          K
$$

with decision variables $x
  ∈
  
    
      R
    
    n$ , $s
  ∈
  
    
      R
    
    m$ and data matrices $P
  =
  
    P
    ⊤
  
  ⪰
  0$ , $q
  ∈
  
    
      R
    
    n$ , $A
  ∈
  
    
      R
    
    
      m
      ×
      n$ , and $b
  ∈
  
    
      R
    
    m$ . The convex set $K$ is a composition of convex cones.

**For more information see the Clarabel Documentation ([stable](https://clarabel.org/) | [dev](https://clarabel.org/dev)).**

Clarabel is also available in a Julia implementation. See [here](https://github.com/oxfordcontrol/Clarabel.jl).

## Features

- **Versatile**: Clarabel.rs solves linear programs (LPs), quadratic programs (QPs), second-order cone programs (SOCPs) and semidefinite programs (SDPs). It also solves problems with exponential, power cone and generalized power cone constraints.
- **Quadratic objectives**: Unlike interior point solvers based on the standard homogeneous self-dual embedding (HSDE), Clarabel.rs handles quadratic objectives without requiring any epigraphical reformulation of the objective. It can therefore be significantly faster than other HSDE-based solvers for problems with quadratic objective functions.
- **Infeasibility detection**: Infeasible problems are detected using a homogeneous embedding technique.
- **Open Source**: Our code is available on [GitHub](https://github.com/oxfordcontrol/Clarabel.rs) and distributed under the Apache 2.0 License

## Installation

Clarabel can be imported to Cargo based Rust projects by adding

```
[dependencies]
clarabel = "0"
```

to the project's `Cargo.toml` file. To install from source, see the [Rust Installation Documentation](https://oxfordcontrol.github.io/ClarabelDocs/stable/rust/installation_rs/).

To use the Python interface to the solver:

```
pip install clarabel
```

To install the Python interface from source, see the [Python Installation Documentation](https://oxfordcontrol.github.io/ClarabelDocs/stable/python/installation_py/).

## Citing

```
@misc{Clarabel_2024,
      title={Clarabel: An interior-point solver for conic programs with quadratic objectives}, 
      author={Paul J. Goulart and Yuwen Chen},
      year={2024},
      eprint={2405.12762},
      archivePrefix={arXiv},
      primaryClass={math.OC}
}
```

## License 🔍

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](https://github.com/oxfordcontrol/Clarabel.rs/blob/main/LICENSE.md) file for details.