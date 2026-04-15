---
source_type:
source: "https://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144874&idx=1&sn=16ca24b3e6b510394067b074831c4ab6&chksm=be859a7989f2136f73d29aebd0f80dd4fe8586cd61c537c0bbec3a7231589e162b74ee862428&scene=178&cur_album_id=2515660787328253953&search_click_id=#rd"
title: "因果推断简介之五：因果图 (Causal Diagram)"
author:
published_at:
created_at: "2026-04-15T16:35:48+08:00"
topics: "这部分介绍 Judea Pearl 于 1995 年发表在 Biometrika 上的工作 “Causal diagrams for empirical research”."
tags:
  - "clippings"
related_concepts:
status: "inbox"
---
*2020年3月5日 20:58*

编辑部于2019年10月在微信端开启《朝花夕拾》栏目，目的是推送2013年（含）之前主站发表的优秀文章，微信端与主站的同步始于2013年年初，然而初期用户量有限，故优质文章可能被埋没。  

![[Image 8.webp|图片]]

这部分介绍 Judea Pearl 于 1995 年发表在 Biometrika 上的工作 “Causal diagrams for empirical research”，这篇文章是 Biometrika 创刊一百多年来少有的讨论文章，Sir David Cox，Guido Imbens, Donald Rubin 和 James Robins 等人都对文章作了讨论。由于 Judea Pearl 最近刚获得了图灵奖，我想他的工作会引起更多的关注（事实上计算机界早就已经过度的关注了）。  

## 一 有向无环图和 do 算子

为了避免过多图论的术语，这里仅仅需要知道有向图中“父亲”和“后代”的概念：有向箭头上游的变量是“父亲”，下游的变量是“后代”。在一个有向无环图（Directed Acyclic Graph；DAG）中，记所有的节点集合为 。这里用 表示连续变量的密度函数和离散变量的概率函数。有两种观点看待一个 DAG：一是将其看成表示条件独立性的模型；二是将其看成一个数据生成机制。当然，本质上这两种观点是一样的。在第一种观点下，给定 DAG 中某个节点的“父亲”节点，它与其所有的非“后代”都独立。根据全概公式和条件独立性，DAG 中变量的联合分布可以有如下的递归分解：

其中表示的“父亲”集合，即所有指向的节点集合。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 1: An Example of Causal Diagram

**例子：** 在 Figure 1 中，联合分布可以分解成为

如果将 DAG 看成一个数据生成机制，那么它和下面的非参数结构方程模型是等价的：

注意，这个联立方程组是“三角的”（triangular）或者“递归的”（recursive），因为 DAG 中没有环，方程组中也就没有反馈。计量经济学中的联立方程组模型 （simultaneous equation model: SEM），并不在这个讨论的框架下。DAG 用于描述数据的生成机制，而不常用于描述系统均衡时的状态；后者主要是 SEM 的目的。这样描述变量联合分布或者数据生成机制的模型，被称为“图模型”或者“贝叶斯网络”（Bayesian network）。

显然，一个有向无环图唯一地决定了一个联合分布；反过来，一个联合分布不能唯一地决定有向无环图。反过来的结论不成立，对我们的实践有很重要的意义，比如 Figure 2 中的两个有向无环图，原因和结果不同，图的结构也不同；但是，我们观测到的联合分布可以有两种分解和因此，我们从观测变量的联合分布，很难确定“原因”和“结果”。在下一节图模型结构的学习中，我们会看到，只有在一些假定和特殊情形下，我们可以从观测数据确定“原因”和“结果”。

用一个 DAG 连表示变量之间的关系，并不是最近才有的。图模型也并不是 Judea Pearl 发明的。但是，早期将图模型作为因果推断的工具，成果并不深刻，大家也不太清楚仅仅凭一个图，怎么能讲清楚因果关系。教育、心理和社会学中常用的结构方程模型（structural equation model: SEM），就是早期的尝试；甚至可以说 SEM 是因果图的先驱。（注意，这里出现的两个 SEM 表示不同的模型！）

DAG 中的箭头，似乎表示了某种“因果关系”。但是，要在 DAG 上引入“因果”的概念，则需要引进 **do 算子** ，do 的意思可以理解成“干预” （intervention）。没有“干预”的概念，很多时候没有办法谈因果关系。在 DAG 中 （也可以记做 ），表示如下的操作：将 中指向 的有向边全部切断，且将 的取值固定为常数 . 如此操作，得到的新 的联合分布可以记做 可以证明，干预后的联合分布为

请注意， 和 在绝大多数情况下是不同的。

**例子** ：考虑如下的两个 DAG：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在 Figure 2 (1) 中，有。由于是的“原因”，“条件”和“干预”，对应的的分布相同。但是在 Figure 2 (2) 中，有. 由于是的“结果”，“条件”（或者“给定”）“结果”，“原因”的分布不再等于他的边缘分布，但是人为的“干预”“结果”，并不影响“原因”的分布。

根据 do 算子，便可以定义因果作用。比如二值的变量 对于 的平均因果作用定义为

上面 do 算子下的期望，分别对应 do 算子下的分布。这样在 do 算子下定义的因果模型，被已故计量经济学家 Halbert White 称为 Pearl Causal Model (PCM; White and Chalak 2009)。Pearl 在其书中写到：

> “I must take the opportunity to acknowledge four colleagues who saw clarity shining through the do(x) operator before it gained popularity: Steffen Lauritzen, David Freedman, James Robins and Philip David. Phil showed special courage in pringting my paper in Biometrika, the journal founded by causality’s worst adversary – Karl Pearson.” (Pearl, 2000)

在书中 Pearl 论述了 RCM 和 PCM 的等价性，即

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

其中，表示潜在结果。要想说明两个模型的等价性，可以将潜在结果嵌套在 DAG 所对应的数据生成机制之中，所有的潜在结果都由这个非参数结构方程模型产生：

其中，表示除去的父亲节点。上面的方程表示：将的值强制在时，DAG 系统所产生的值。这个意义下，do 算子导出的结果，就是“潜在结果”。

## 二 d分离，前门准则和后门准则

在上面的叙述中，如果整个 DAG 的结构已知且所有的变量都可观测，那么我们可以根据上面 do 算子的公式算出任意变量之间的因果作用。但是，在绝大多数的实际问题中，我们既不知道整个 DAG 的结构，也不能将所有的变量观测到。因此，仅仅有上面的公式是不够的。

下面，我将介绍 Judea Pearl 提出的“后门准则”（backdoor criterion）和“前门准则”（frontdoor criterion）。这两个准则的意义在于：（1）某些研究中，即使 DAG 中的某些变量不可观测，我们依然可以从观测数据中估计出某些因果作用；（2）这两个准则有助于我们鉴别“混杂变量”和设计观察性研究。

下面的讨论中，“ **可识别性** ”这个概念将被频繁的使用。因果推断中的识别性，和传统统计中的识别性定义是一致的。统计中，如果两个不同的模型参数，对应不同的观测数据的分布，那么我们称模型的参数可以识别。这里，如果因果作用可以用观测数据的分布唯一的表示，那么我们称因果作用是 **可以识别** 的。

前门准则和后门准则，都涉及了 d 分离（d-seperation）的概念。

定义（ **d 分离** ）: 设 ，， 是 DAG 中不相交的节点集合， 为一条连接 中某节点到 中某节点的路径 （不管方向）。如果路径 上某节点满足如下的条件：

1. 在路径 上， 点处为 结构 （或称冲撞点，collider），且 及其后代不在 中；
2. 在路径 上， 点处不是 结构，且 在 中,

那么称 阻断 (block) 了路径 。进一步，如果 阻断了 到 的所有路径，那么称 d 分离 和 ，记为 。

下面介绍 Pearl (1995) 的主要工作： **后门准则和前门准则** 。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**后门准则：** 在 DAG 中，如果如下条件满足：

1. 中节点不能是 的后代；
2. 阻断了之间所有指向 的路径（这样的路径可以称为后门路径）；

则称变量的集合相对于变量的有序对满足后门准则。进一步，若相对于变量的有序对满足后门准则，其中 和 是和中的任意节点；那么称变量的集合相对于节点集合的有序对满足后门准则。

Pearl (1995) 证明，若存在一个变量集合相对于满足后门准则，那么到的因果作用是可以识别的，且

为了理解因果图的概念，下面的简短证明是很有必要的。

**证明：** 在 Figure 3 (a) 中，

从上面可以看出，上面的后门准则和可忽略性假定下 ACE 的识别公式一样：都是用 做调整 (adjustment)，先分层再加权求和。这条结论在 Rosenbaum and Rubin (1983) 之后提出，且流行病学家也都用这样的调整方法控制混杂因素，因此对很多统计学家和流行病学家来说并不新奇。比较新颖的结论是下面的前门准则。

**前门准则：** 在 DAG 中，称节点的集合 相对于有序对 满足前门准则，如果

1. 切断了所有 到 的直接路径；
2. 到 没有后门路径；
3. 所有 到 的后门路径都被 阻断。

此时，如果，则到的因果作用可识别，为

**证明：** Figure 3 (b) 中蕴含了条件独立性，将在推导中用到：。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这个前门路径看似很难理解，证明似乎很不直观，恰似变魔术。但是它其实是很显然的，在前门路径的 DAG 中，我们有：（1）XY的因果作用可识别——这样看来，这个结论就不奇怪了！

Pearl 在书中讲了一个非常有趣的例子，来说明前门准则的用处。

**例子：** 我们关心吸烟和肺癌之间的因果关系。由于一个潜在的不可观测的基因 的存在，吸烟和肺癌之间有一条“活”的后门路径，因此不借助其他的条件，我们无法识别吸烟与肺癌的因果关系。如果我们有这样的知识“吸烟 仅仅通过肺部烟焦油的含量 来影响肺癌 ”，那么吸烟对肺癌的因果作用就可以估计出来了。不过，这里需要两个条件，也就是在证明中使用的两个条件独立性，他们表明：（1）吸烟 和肺部烟焦油的含量 之间没有“活”的后门路径（或者没有混杂因素）；（2）吸烟 对肺癌 的作用仅仅来源于吸烟 对肺部烟焦油 的作用，或者说，吸烟 对肺癌 没有“直接作用”。

**例子：** 在 Figure 1 的 DAG 中， 之间的后门路径被 或者 阻断，而前门路径被 阻断。上面的两个准则表明， **要识别从 到 的因果作用，我们不需要观测到所有的变量，只需要观测到切断后门路径或者前门路径的变量即可。**

## 三 回到 Yule-Simpson’s Paradox

在第一节中，我们看到了经典的 Yule-Simpson’s Paradox。记 为处理（吃药与否）； 为结果（存活与否）， 是用于分层的变量（在最开始的例子中， 是性别；在这里我们先将 简单地看成某个用于分层的变量）。悖论存在，是因为 和 正相关；但是按照 的值分层后， 和 负相关。分，还是不分？—–这是一个问题！这在实际应用是非常重要的问题。

不过，仅仅从“相关”（association）的角度讨论这个问题，是没有答案的。从“因果”（causation）的角度来看，才能有确切的回答。解释 Yule-Simpson’s Paradox，算是因果图的第一个重要应用。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

下面，我将以上面的 Figure 4 中的四个图为例说明，三个变量之间的关系的复杂性。

图（a）：根据后门准则， 阻断了 到 的后门路径，因此，根据 做调整可以得到 对 的因果作用。如果实际问题符合图（a），那么我们需要用调整后的估计量。

图（b）： 是 的“后代”且是 的“父亲”。很多地方称，此时 处于 到 的因果路径上。直观的看，如果忽略 ，那么 和 之间的相关性就是 对 的因果作用，因为 和 之间的后门路径被空集阻断，我们无须调整。如果此时我们用 进行调整，那么得到的是 到 的“直接作用”。不过，什么是“直接作用”，我们将会在后面讨论；这里只是给一个形象的名字。

图（c）：和图（b）相同， 和 之间的相关性就是因果作用。但是，复杂性在于 和 之间有一个共同的但是不可观测的原因 。此时，不调整的相关性，是一个因果关系的度量。但是，如果我们用 进行调整，那么给定 后， 和 相关， 和 之间的后门路径被打通，我们得到的估计量不再具有因果的含义。这种现象发生的原因是， 之间形成了一个 结构：虽然 和 之间是独立的，但是给定 之后， 和 不再独立。

图（d）：这个图常常被 Judea Pearl 用来批评 Donald Rubin，因为它存在一个有趣的 结构。在这个图中，由于 结构的存在， 和 之间的后门路径被空集阻断，因此 和 之间的相关性就是因果性。但是由于 结构的存在，当我们用 进行调整的时候， 和 之间打开了一条“通路”（它们不再独立），因此 和 之间的后门路径被打通，此时 和 之间的相关性不再具有因果的含义。

我个人认为，因果图是揭开 Yule-Simpson’s Paradox 神秘面纱的有力工具。正如 Judea Pearl 在他的书中写到，不用因果的语言来描述这个问题，我们是讲不清楚这个悖论的。当然，因果的语言不止因果图，Judea Pearl 的解释始终不能得到 Donald Rubin 的认可。

## 四 讨论

用一个图来描述变量之间的因果关系，是很自然和直观的事情。但是，这并不意味着 Pearl 的理论是老妪能解的。事实上，这套基于 DAG 的因果推断的语言，比传统的 Neyman-Rubin 模型要晦涩很多。DAG 在描述因果关系的时候，常常基于很多暗含的假定而并不明说，这也是 DAG 并没有被大家完全接受的原因。传统的因果推断的语言，开始于 Jerzy Neyman 的博士论文；Donald Rubin 发展这套“潜在结果”的语言，并将它和缺失数据的理论联系在一起，成为统计界更多使用的语言。

在实际中，人们对于图模型的批评从未中断。主要的问题集中在如下的方面：

1. 现实的问题，是否能用一个有向无环图表示？大多数生物学家看到 DAG 的反应是“能不能用图表示反馈？”的确，DAG 作为一种简化的模型，在复杂系统中可能不完全适用。要想将 DAG 推广到动态的系统，或者时间序列中，还有待研究。
2. Pearl 引入的 do 算子，是他在因果推断领域最主要的贡献。所谓 “do”，就是“干预”，Pearl 认为干预就是从系统之外人为的控制某些变量。但是，这依赖于一个假定：干预某些变量并不会引起 DAG 中其他结构的变化。这个假定常常会受到质疑，但是质疑归质疑，Pearl 的这个假定虽然看似很强，但根据观测数据却不可检验。这种质疑并不是 Pearl 的理论独有的缺陷，这事实上是一切研究的缺陷。比如，我们用完全随机化试验来研究处理的作用，我们要想将实验推广到观察性的数据或者更大的人群中去，也必须用到一些不可验证的假定。
3. 很多人看了 Pearl 的理论后就嘲笑他：难道我们可以在 DAG 中干预“性别”？确实，离开了实际的背景，干预性别似乎是不太合理的。那这个时候，根据 Pearl 的 do算子得到的因果作用意味着什么呢？可以从几个方面回答这个问题。
- 很多问题，我们不能谈论“干预性别”，也不能谈论“性别”的“因果作用”。“性别”的特性是“协变量”（covariate），对于这类变量（如身高、肤色等），谈论因果作用不合适，因为我们不能想象出一个可能的“实验”，干预这些变量。
	- 上面的回答基于“实验学派”（experimentalists’）的观点，认为不可干预，就没有“因果”。但是，如果认为只要有数据的生成机制，就有因果关系，那么算出性别的因果作用也不奇怪。（计量经就学一直有争议，以 Joshua Angrist、Guido Imbens 等为首的“实验派”，和以 James Heckman 为首的“结构方程模型”派，有过很激烈的讨论。）
	- 有些问题中性别的因果作用是良好定义的。比如，我们可以人工的修改应聘者简历上的名字（随机的使用男性和女性名字），便可以研究性别对于求职的影响，是否存在性别歧视等等（已有研究使用过这种实验设计）。
5. 一个更为严重的问题是，实际工作中，我们很难得到一个完整的 DAG，用于阐述变量之间的因果关系或者数据生成机制，使得 DAG 的应用受到的巨大的阻碍。不过，从观测数据学习 DAG 的结构，确实是一个很有趣且重要的问题，这留待下回分解。

在结束时，留些一些思考的问题：

- 在何种意义下，后门准则的条件，等价于可忽略性，即 ？
- 在第一节的 Yule-Simpson’s Paradox 中，我们最终选择调整的估计量，还是不调整的估计量？

关于作者

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

丁鹏，2004-2011 年在北京大学概率统计系学习，获得学士和硕士学位；2011-2015 年在哈佛大学统计系学习，获得博士学位；2015 年在哈佛大学流行病学系做博士后；2016 年加入伯克利统计系任教。研究方向是因果推断。

***往期回顾***

[*因果推断之一：* *从Yule-Simpson's Paradoc讲起*](https://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144615&idx=1&sn=ecf6b8e67af3b7cf615c867e187b797d&scene=21#wechat_redirect)

[*因果推断之二：* *Rubin Causal Model (RCM) 和随机化试验*](http://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144668&idx=1&sn=570baaf9b7e2dff3fc8c8eeee16df39d&chksm=be86658f89f1ec99a118be4c5bb687789500a60069a96612f84cde36d5b281173fc35e49bd72&scene=21#wechat_redirect)

[*因果推断之三：* *R. A. Fisher 和 J. Neyman 的分歧*](http://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144760&idx=1&sn=34d3ba1e49c64496937949280005d934&chksm=be8665eb89f1ecfd84cdf731416b4fc45ee887d7e7f74b75c0deacaa9232f5f888dc906b44b3&scene=21#wechat_redirect)

[*因果推断简介之四：观察性研究，可忽略性和倾向得分*](http://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144844&idx=1&sn=0a0de37da5a5843e04c7f860785ad26f&chksm=be859a5f89f21349054e669c4e5d4b848032cbb6a2a5943bbf9e1718ec528fc4e828a444e11e&scene=21#wechat_redirect)  

作者：丁鹏

编辑：向悦

统计之都：专业、人本、正直的中国统计学社区。

关注方式：扫描下图二维码。或查找公众号，搜索 统计之都 或 CapStat 即可。

往期推送：进入统计之都会话窗口，点击右上角小人图标，查看历史消息即可。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

阅读原文

继续滑动看下一个

统计之都

向上滑动看下一个