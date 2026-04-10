---
title: "S&DS 431/631 — 优化与计算 --- S&DS 431/631 — Optimization and Computation"
source: "https://zhuoranyang.github.io/sds431-notes/"
author:
  - "[[Zhuoran Yang]]"
published:
created: 2026-04-11
description:
tags:
  - "clippings"
---
## 欢迎

优化是机器学习、数据科学和现代工程背后的引擎。每当我们训练神经网络、更新推荐系统或重新配置供应链时，都在解决一个优化问题。本课程提供了对这些使其运行的理论和算法的严谨介绍。

这些交互式讲义笔记涵盖了从基础到应用的完整过程——包括凸集、凸函数、对偶性以及线性规划几何学的基础知识，通过支持工业求解器的单纯形法和内点法，驱动现代大规模计算的梯度下降、近端法、次梯度法和 Frank-Wolfe 等一阶方法，以及包括扩散模型和 Transformer 在内的现代计算模型。每章都包含正式的定义和定理，带有交叉引用，以及用于几何直观理解的交互式 Plotly 可视化，还有可以在 Jupyter 或 Google Colab 中运行的 Python 代码块。

## 课程流程

![](https://zhuoranyang.github.io/sds431-notes/lectures/figures/ch01-course-roadmap.svg)

图 1：展示 S&DS 431/631 所有五个部分之间依赖结构的课程路线图。点击放大。

## 课程概述

### 第一部分：准备

- 引言和动机——为什么优化很重要？应用巡礼——从训练神经网络到投资组合分配——以及约束条件下最小化目标函数的正式化。
- 数学基础——基本工具箱：范数和内积、特征值和谱分解、梯度、黑塞矩阵、泰勒展开以及反向传播的链式法则。

### 第二部分：凸优化基础

- 凸集——解的概念、魏尔斯特拉斯定理、凸集（半空间、多面体、锥、椭球）、保持凸性的运算、凸组合和凸包。
- 凸函数——凸函数（一阶和二阶特征），保持函数凸性的运算，次级集，以及每个局部最小值都是全局最小值这一重要推论。
- 凸优化——标准形式的凸优化，凸程序的层次结构（线性规划、二次规划、第二类锥规划、半定规划），拉格朗日对偶性、弱对偶性和强对偶性、斯莱特条件以及 KKT 条件。

### 第三部分：一阶方法

- 梯度下降——我们如何迭代地找到最小值？下降引理、平滑目标（ $O(1/k)$ ）和强凸目标（ $O(\rho^k)$ ）的收敛速度、步长选择以及条件数的作用。
- 动量、自适应方法、随机梯度下降和近端梯度 — 超越基础梯度下降：动量方法、Nesterov 加速梯度、自适应方法（AdaGrad、RMSProp、Adam）、随机梯度下降、用于复合目标的近端梯度方法以及利用神经网络权重的谱几何特性的现代矩阵优化器（Muon、Shampoo、SOAP）。
- 约束一阶方法——在约束域上优化：非光滑问题的投影子梯度下降法，以及当投影成本高但线性最小化便宜时的 Frank-Wolfe（条件梯度）方法。

### 第四部分：线性规划

- 线性规划公式与几何——线性规划看起来是什么样子？标准形式和等式形式，多面体，顶点，极点，基本可行解，以及线性规划的基本定理。
- 单纯形法——优化中最著名的算法：沿着多面体的边进行枢轴操作，每一步都改进目标。我们开发完整的表格法并分析其正确性。
- 线性规划对偶性 — 每个线性规划都有一个对偶。弱对偶性给出一个界，强对偶性给出等式，互补松弛性将原始和对偶解联系起来。
- 对偶单纯形法 — 从对偶侧入手：对偶单纯形法在保持对偶可行性的同时向原始可行性推进。对敏感性分析和热启动至关重要。
- 线性规划应用与博弈论 — 线性规划的实际应用：最大流/最小割、网络流、全整数矩阵、鲁棒优化以及两人零和博弈的最小最大定理。

### 第五部分：二阶与内点法

- 牛顿法——利用曲率：牛顿法通过黑塞矩阵实现二次收敛。我们发展了仿射不变的牛顿减量、回溯线搜索和自共轭理论，这些构成了下一章中内点法的基础。
- 椭球法——解决了线性规划多项式时间可解性的算法：保持一个包含最优解的椭球，并通过一个分离超平面在每一步收缩它。
- 内点法——约束优化的现代主力：对数障碍、中心路径和基于牛顿的路径跟踪，具有 $O(\sqrt{m}\log(1/\varepsilon))$ 迭代复杂度。

### 第六部分：现代计算模型

- 扩散模型——生成式 AI 模型如何从噪声中创建图像？正向去噪过程、得分匹配、去噪得分匹配、逆时 SDEs、DDPM 及其与最优传输的联系。
- Transformer 模型——GPT 和现代 AI 背后的架构：自注意力机制作为 softmax 加权投影、位置编码、多头注意力以及 GPT 规模模型的参数计数。

## 教科书

以下文本作为本课程的主要参考资料：

- Stephen Boyd 和 Lieven Vandenberghe 所著的《凸优化》，剑桥大学出版社，2004 年。这是关于凸集、凸函数、对偶理论和内点法的标准参考书（本课程第二、三、五部分）。在线免费提供。
- Dimitris Bertsimas 和 John Tsitsiklis 所著的《线性优化导论》，Athena Scientific 出版社，1997 年。线性规划的经典教材：单纯形法、LP 对偶理论、网络流和椭球法（本课程第四、五部分）。

## Prerequisites

This course assumes familiarity with:

- Linear algebra (vectors, matrices, eigenvalues)
- Multivariable calculus (partial derivatives, gradients)
- Basic probability and statistics
- Some exposure to programming (Python)

## Acknowledgments

Part of these lecture notes are based on previous versions of this course taught by [Anna Gilbert](https://annacgilbert.github.io/) and [Dan Spielman](http://cs-www.cs.yale.edu/homes/spielman/). I am grateful to both for their foundational contributions to the course material.