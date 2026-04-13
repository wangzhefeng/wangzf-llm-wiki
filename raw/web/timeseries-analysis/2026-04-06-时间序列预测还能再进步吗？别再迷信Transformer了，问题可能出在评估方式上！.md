---
author:
- null
- '[[时序之心]]'
created: 2026-04-06
created_at: 2026-04-06
description: 时间序列预测还能再进步吗？你有没有过这种感觉：明明用了很“高级”的模型，比如Transformer，跑时间序列预测，结果表现还不如一个简单的线性模型？
source_type: web
status: inbox
tags:
- null
- clippings
title: 时间序列预测还能再进步吗？别再迷信Transformer了，问题可能出在评估方式上！
source_url: https://mp.weixin.qq.com/s/6DGiRXxrI872KUAIooP9Fg
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

原创 时序之心 *2025年11月13日 12:21*

#### 时间序列预测还能再进步吗？

你有没有过这种感觉：明明用了很“高级”的模型，比如Transformer，跑时间序列预测，结果表现还不如一个简单的线性模型？别怀疑自己，可能不是你不行，而是整个评估方式本身就有点“拧巴”。

最近有位搞时间序列研究两年多的朋友分享了一些挺扎心但很真实的观察，我觉得特别值得聊聊。总结下来，主要有这么几点：

### 1.任务设定“贪心”反而拖后腿

现在主流的长期时间序列预测（LTSF）方法，动不动就号称能预测天气、汇率、心电、交通……看起来很牛，但问题来了：这些数据本质完全不同！天气和心电属于确定性系统，有规律可循；而汇率更像是随机游走，连专家都说不准。一个模型既要对付混沌，又要应对纯随机，还要扛住分布突变——这不是“全能”，这是“为难”。

### 2.评估指标暗藏“陷阱”

大家习惯用MSE（均方误差）来评判模型好坏，但这其实隐含了一个假设：未来是可以被“平均”猜对的。可现实中，很多时间序列充满突发冲击和不可知变量。灵活的模型（比如Transformer）反而容易被MSE“带偏”，只学会画出一团“平均正确”的模糊曲线，而不是真正抓住动态规律。

### 3.别死磕公开benchmark了

很多人花大量时间调参，就为了在ETT、Weather这些数据集上“打榜”。但这些数据集本身可能藏雷（比如Weather里藏着-9999的异常值），而且你根本不知道真实世界背后的生成机制。与其在“模拟器比赛”里卷，不如回归本质。

### 4.试试从“玩具系统”开始

建议先用经典的混沌系统（比如Lorenz系统）做测试。这类系统虽然短期可预测、长期不可测，但好处是：你知道“标准答案”！能清晰判断模型到底有没有学到东西。而且别一上来就做归一化——那可能会掩盖模型的真实缺陷。

**总之，时间序列预测远没到天花板，但突破点或许不在堆模型，而在于换种思路：少点“通吃天下”的幻想，多点“先搞懂再拓展”的踏实。**

---

在能源、气象和金融等领域，准确预测未来数据（如未来几天的用电量或股价）至关重要。然而，评估现有预测模型的优劣是一个难题，因为现实世界的数据总是混杂着各种未知类型的噪声和复杂的信号模式。这使得我们很难判断一个模型到底是学到了真实的数据规律，还是仅仅记住了噪声。

为了解决这一难题，本论文提出了一个 **可参数化合成数据集的评估框架** 。该框架能像搭积木一样，通过精确控制信号的频率、形状和噪声的类型、强度，生成各种各样的人工时间序列数据。通过在这个“靶场”上测试不同的模型，论文发现了很多现有方法在特定场景下的优势与短板，例如在何种信号模式下表现更佳，以及对哪种类型的噪声更为敏感，为实践中的模型选择提供了清晰的指导。

另外我整理了 **时间序列预测相关论文（多变量时间序列预测、扩散模型+时间序列预测等）** ，感兴趣的自取，希望能帮到你！

关注“时序之心”回复“C348”

免费领取 **时间序列预测** 相关论文+源码

## 一、论文基本信息

**论文标题：** Benchmarking M-LTSF: Frequency and Noise-Based Evaluation of Multivariate Long Time Series Forecasting Models

**作者姓名：** Nick Janßen, Melanie Schaller, Bodo Rosenhahn

**作者单位/机构：** 莱布尼兹汉诺威大学信息处理研究所 (Institute for Information Processing, Leibniz University Hannover)

**论文来源：** IEEE 2025

**论文地址：** https://arxiv.org/abs/2510.04900

## 二、主要贡献与创新

1. 提出可控的合成数据集框架，能系统性地评估模型在特定信号与噪声下的性能。
2. 为模型选择提供明确指导，揭示不同架构在效率和准确性上的具体权衡。
3. 深入刻画了模型行为，指出了不同架构对特定季节性模式和噪声类型的偏好。
4. 开源了完整的基准测试框架，促进了研究的可复现性和后续工作的开展。

## 三、研究方法与原理

该论文的核心思路是： **通过分层组合、精确控制的信号和噪声模块，来构建一个可定制的、用于评估预测模型的人造多维时间序列数据集。**

这个数据集的构建过程遵循一种基于组件的层次化方法，整体流程如下图所示。

![Figure 4.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 4.

首先，框架为每个数据维度（variate）的生成引入了一种 **带惩罚的概率分配机制** 。这个机制确保了信号和噪声组件能被相对均匀地分配到不同的数据维度上，避免某个维度过于复杂而其他维度过于简单。具体来说，为一个数据维度 分配新组件的概率 由以下公式决定：

其中， 是已经分配给维度 的组件数量，而指数 是一个可配置的惩罚强度。这个设计巧妙地在模拟数据维度间的关联性和保持组件分布的均衡性之间取得了平衡。接下来，我们详细解析构成最终时间序列的各个模块。

### 信号组件 (Signal Components)

信号组件是模拟真实世界数据潜在规律的基础，分为趋势（Trend）和季节性（Seasonal）两类。

![Figure 2.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 2.

1. **趋势组件** ：用于模拟数据中的长期变化，例如传感器漂移或全局气温上升。它由一个单项式函数定义：
	这里， 代表时间步，参数 控制趋势的方向（增长或下降）， 控制趋势的形态（线性或非线性）。这种设计可以灵活地模拟各种长期变化模式。
2. **季节性组件** ：用于模拟数据中呈现周期性波动的规律，如每日的温度变化。论文设计了三种不同波形：
	这三种波形覆盖了从平滑到剧烈变化的多种周期性模式，为测试模型对不同 **自相关 (autocorrelation)** 模式的捕捉能力提供了基础。
- **正弦波 (Sinusoidal)** ：模拟平滑的周期性振荡，其公式为 ，代表了自然界中常见的平滑周期变化。
	- **平滑锯齿波 (Smooth Sawtooth)** ：模拟缓慢增长后突变的模式，例如电池的充放电循环。其公式较为复杂，通过反正弦和双曲正切函数构造：
	其中 。
	- **平滑方波 (Smooth Square)** ：模拟在达到物理极限时信号被“削平”的现象，如流量控制系统中的饱和状态。公式为：

### 噪声组件 (Noise Components)

为了模拟真实数据中的不确定性，框架集成了多种噪声类型，分为信号无关和信号相关两类。

![Figure 3.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 3.

1. **信号无关噪声** ：这类噪声的产生与信号本身无关，模拟外部随机干扰。
- **白噪声 (White Noise)** ：从标准正态分布 中采样，模拟完全随机、没有时间关联性的误差。
	- **布朗噪声 (Brownian Noise)** ：通过累加白噪声得到， ，模拟具有强时间依赖性的随机游走过程。
	- **脉冲噪声 (Impulse Noise)** ：在随机时间点上叠加若干高斯脉冲，模拟硬件故障或数据传输错误等瞬时异常。
3. **信号相关噪声** ：这类噪声的强度与信号的特性直接相关，模拟测量误差随信号变化的情况。
- **趋势噪声 (Trend Noise)** ：其幅度与趋势组件的大小成正比， ，其中 。这反映了信号长期漂移越大，测量不确定性也越大的情况。
	- **季节性噪声 (Seasonal Noise)** ：其幅度与季节性组件的大小成正比， ，模拟了在周期性高峰期噪声也更强的现象。

### 多变量时间序列生成

最后，框架将上述信号和噪声组件合成为最终的 **多变量长时序预测 (M-LTSF)** 数据。这一过程分两步：首先，将所有信号组件和噪声组件分别加权求和，得到一个纯净的信号序列 和一个纯净的噪声序列 。然后，根据预设的\*\*信噪比 (signal-to-noise ratio, SNR)\*\*，用特定的权重将两者混合。为了确保混合后的序列方差为1且满足设定的信噪比，权重 和 的计算考虑了信号与噪声之间的相关性 ：

最终的输出序列为 。通过这种方式，研究者可以系统地调整预测任务的难度，从而精细地评估模型的鲁棒性。

## 四、实验设计与结果分析

实验旨在全面评估四种代表性的 **多变量长时序预测** 模型：S-Mamba (基于 **状态空间模型 (state-space model, SSM)**)、iTransformer (基于 **Transformer**)、R-Linear (基于 **线性模型 (Linear Models)**) 和 Autoformer (基于分解)。所有实验均在论文提出的合成数据集上进行，数据总量为35,040个时间点，包含800个维度。模型使用过去96个点（ `lookback horizon` ）来预测未来96个点（ `forecast horizon` ）。评估指标为 **均方误差 (Mean Squared Error, MSE) **，一个关键的实验设计是：** 模型在带噪声的数据上训练，但在对应的无噪声纯净信号上进行评估** ，以此检验模型去伪存真的能力。

### 频率和信号类型的基础评估

在无噪声和无趋势的理想条件下，实验首先探究了模型对不同频率和季节性模式的响应。

![Figure 7.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 7.

分析图7可以发现，所有模型都存在一个共性短板：当信号的周期过长，以至于模型的输入窗口（ `lookback window` ，长度96）无法容纳一个完整的周期时， **所有模型的性能都急剧下降** 。这是因为模型无法观察到完整的周期性模式，容易将其误判为趋势，从而导致预测失败。

此外，不同模型对信号形状表现出明显的偏好。 **S-Mamba 和 Autoformer 在处理锯齿波时表现最好** ，这可能是因为 Autoformer 的分解机制和 S-Mamba 的时变状态空间结构更擅长捕捉这种包含线性斜坡和突变的信号。相比之下， **R-Linear 和 iTransformer 则在处理平滑的正弦波时性能更优** ，这或许与 iTransformer 的 **注意力机制 (attention mechanisms)** 更容易捕捉平滑信号中渐变的相位关系有关。

### 噪声鲁棒性分析

本部分通过引入五种不同类型的噪声（白噪声、布朗噪声、脉冲噪声、趋势噪声和季节性噪声），并在不同 **信噪比** 下进行测试，深入分析了模型的抗干扰能力。

![Figure 10.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 10.

![Figure 11.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 11.

![Figure 12.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 12.

实验结果（如图10和图11所示）揭示了几个关键现象：

1. 在所有噪声类型中， **布朗噪声在低信噪比（SNR=1）时对所有模型的性能破坏最为严重** ，凸显了模型在处理具有强时间相关性的非平稳噪声时面临的巨大挑战。
2. 正如预期，随着 **信噪比** 的提高，所有模型在白噪声下的性能都稳步提升，S-Mamba和iTransformer在此场景下表现出众。
3. 模型表现出特定的“软肋”。如图12所示， **iTransformer 对季节性噪声更敏感，而 S-Mamba 对趋势噪声的抵抗力更弱** 。这直接反映了它们内部架构的差异：基于注意力的 iTransformer 可能在季节性模式被噪声干扰时难以建立正确的关联，而 S-Mamba 的状态空间在信号长期趋势被噪声污染时更容易发生漂移。
4. Autoformer 的性能表现出较大的不稳定性，但在处理带有噪声的锯齿波信号时却相当稳健，表明其分解机制与这类信号的特性非常契合。

### 谱分析 (Spectral Analysis)

为了从频域视角补充 **均方误差** 分析，论文对模型的预测结果进行了谱分析，旨在检验模型对原始信号频率成分的还原能力。

![Figure 13.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 13.

![Figure 14.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 14.

![Figure 15.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 15.

![Figure 16.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 16.

谱分析的结果令人深思： **即使在完全没有噪声的理想情况下，没有一个模型能够完美地重构出干净的原始信号频谱** 。这揭示了当前深度学习方法在时序预测任务中一个普遍的优化难题，即模型倾向于收敛到引入了额外杂散频率的局部最优解。

尽管如此，模型之间仍有优劣之分。 **S-Mamba 和 iTransformer 展现了最强的频谱学习能力** （如图13和图14所示），它们在信噪比较高时能较好地还原主频率成分，其频谱上的误差大小与它们在 **均方误差** 上的表现高度相关。相比之下，Autoformer 和 R-Linear 的频谱还原能力较差，且对噪声水平的变化不甚敏感，这与它们在时间域上性能饱和或不稳定的表现相符，进一步暴露了其模型表达能力的局限性。

## 五、论文结论与评价

### 总结

这篇论文的核心贡献在于创建了一个精细可控的合成数据生成框架，从而能够系统地、深入地剖析各种 **多变量长时序预测** 模型的真实能力和短板。实验结论非常明确：模型的性能不仅取决于其自身架构，还严重受到数据信号的频率、形状以及噪声类型的影响。例如，所有模型在输入窗口无法覆盖完整信号周期时都会失效；不同模型对锯齿波和正弦波有不同的偏好；并且，特定类型的噪声会精准打击特定架构的弱点。这项研究为实际应用中如何根据数据特点选择合适的模型提供了宝贵的经验性指导，也为未来模型的设计指明了需要改进的方向，例如提升模型对非平稳噪声的鲁棒性和频谱还原能力。

### 优点

该论文最大的优点在于其 **创新的评估范式** 。它摆脱了传统基准测试中“知其然，不知其所以然”的困境，通过可控实验，将模型的性能表现与具体的数据特征（频率、波形、噪声类型）直接关联起来，使得结论更加深刻和具有指导意义。此外，研究方法系统严谨，对多种模型架构的弱点进行了有力的揭示，并且开源其框架，极大地促进了社区的后续研究。

### 缺点

论文的主要局限性在于其 **结论完全基于合成数据** 。尽管合成数据能够实现完美的控制变量，但它毕竟简化了真实世界数据的复杂性，例如多种未知噪声的叠加、突发事件的不可预测性等。因此，从合成数据中得出的模型偏好和弱点是否能完全推广到所有真实场景，还需要进一步的验证。此外，虽然论文揭示了所有模型在频谱还原上的普遍失败，但未能从深度学习优化理论的层面深入探讨导致这一问题的根本原因。

扫码添加小助手回复“C348”

免费获取全部论文资料

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

相关推荐

[NeurIPS 2025 | 中科大等提出PIR：实例感知后处理修正框架，显著提升时序预测可靠性！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488092&idx=1&sn=2151a83b9135ce8b8b96a179c3c38223&scene=21#wechat_redirect)

[时序论文速递：覆盖多场景时间序列预测、时间序列异常检测、特定领域与时序交叉分析等方向（11.03-11.07）](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488076&idx=1&sn=77941cd7b33bf358388f21349e86cdc3&scene=21#wechat_redirect)

[EMNLP 2025 | 时间序列相关论文盘点(附原文源码)！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488062&idx=1&sn=8e2d2b4bafe7108fa3c3c9c1e2cfb2b4&scene=21#wechat_redirect)

[CIKM 2025 | 中国科技大学&华盛顿大学提出：通过文本增强提升多模态时序预测！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488045&idx=1&sn=ac17bd407fdb8e7225ca8814a4a827e0&scene=21#wechat_redirect)

[小样本也能精准预测！时间序列小样本学习突破技术瓶颈！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488030&idx=1&sn=a8b3214bc12148dfedb3acc2c78f7410&scene=21#wechat_redirect)

[2025 | 时序预测新范式：多智能体AI系统实现全流程自动化！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488020&idx=1&sn=2c03d9eadab6ffd06ee4c48b7719d809&scene=21#wechat_redirect)

[时序论文速递：覆盖时间序列预测、时间序列异常检测、时间序列因果关系发现等方向！（10.27-10.31）](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247487934&idx=1&sn=c745de56ae9cdb1a5f46ad66b79b01cd&scene=21#wechat_redirect)

注：本公众号发布的内容仅用于信息传递与知识分享，不保证绝对准确，也不构成专业建议。因使用内容造成的任何损失，我们概不负责。 若公众号含外部链接，链接内容及运营不受我们控制，由此产生的风险和损失，读者自行承担。此外，原创内容版权归本号所有，未经授权禁止商用。因不可抗力、技术故障等致内容异常，本号同样免责。阅读即视为同意本声明，如有疑问，欢迎联系。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

作者提示: 个人观点，仅供参考

阅读原文

继续滑动看下一个

时序之心

向上滑动看下一个