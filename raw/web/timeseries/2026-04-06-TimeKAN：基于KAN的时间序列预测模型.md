---
source_type: web
title: "TimeKAN：基于KAN的时间序列预测模型"
author:
  - 
  - "[[QuantML致力于机器学习量化模型最深度研究]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://zhuanlan.zhihu.com/p/27937723158"
published: 
created: 2026-04-06
description: "1. 引言时间序列预测（TSF）在金融、能源管理、交通流量规划和天气预报等多个领域具有重要应用。近年来，深度学习技术，特别是基于卷积神经网络（CNN）、Transformer和多层感知器（MLP）的方法，极大地推动了TSF的…"
tags:
  - 
  - "clippings"
---

![[raw/assets/attachments/timeseries/v2-d6d99355b514bb7fe34d7ecfc5c9e35e_1440w.jpg]]

### 1\. 引言

时间序列预测（TSF）在金融、能源管理、交通流量规划和天气预报等多个领域具有重要应用。近年来，深度学习技术，特别是基于 [卷积神经网络](https://zhida.zhihu.com/search?content_id=254610134&content_type=Article&match_order=1&q=%E5%8D%B7%E7%A7%AF%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C&zhida_source=entity) （CNN）、Transformer和 [多层感知器](https://zhida.zhihu.com/search?content_id=254610134&content_type=Article&match_order=1&q=%E5%A4%9A%E5%B1%82%E6%84%9F%E7%9F%A5%E5%99%A8&zhida_source=entity) （MLP）的方法，极大地推动了TSF的发展。然而，现实世界中的时间序列往往具有非平稳性和复杂的模式，这使得准确捕捉历史数据与未来目标之间的联系变得极具挑战性。

为了应对时间序列中复杂的时序模式，越来越多的研究开始关注利用先验知识将时间序列分解为更简单的组成部分，为预测提供基础。例如，Autoformer将时间序列分解为季节性和趋势性成分，DLinear和FEDFormer也采用了类似的方法。TimeMixer则进一步引入了多尺度季节-趋势分解，强调不同尺度之间的相互作用。 [TimesNet](https://zhida.zhihu.com/search?content_id=254610134&content_type=Article&match_order=1&q=TimesNet&zhida_source=entity) 、PDF和SparseTSF等模型则强调时间序列中固有的周期性，并根据周期长度将长序列分解为多个短序列，从而能够分别对周期内和周期间的依赖关系进行建模。

值得注意的是，时间序列通常由多个频率成分组成，低频成分代表长期周期性变化，高频成分则捕捉某些突发事件。不同频率成分的混合使得准确预测变得尤为困难。上述分解方法启发我们设计一种频率分解框架，将时间序列中的不同频率成分解耦，并独立学习与每个频率相关的时序模式。然而，这又引入了另一个挑战：不同频率下的模式信息密度不同，采用统一的建模方法对不同频率成分进行建模可能导致表征不准确，从而导致结果欠佳。

幸运的是，一种名为 [Kolmogorov-Arnold网络](https://zhida.zhihu.com/search?content_id=254610134&content_type=Article&match_order=1&q=Kolmogorov-Arnold%E7%BD%91%E7%BB%9C&zhida_source=entity) （KAN）的新型神经网络架构最近在深度学习社区引起了广泛关注。KAN因其卓越的数据拟合能力和灵活性，被认为是传统MLP的有力替代品。与使用固定激活函数的MLP不同，KAN在边缘引入可学习的激活函数。此外，KAN还提供可选的内核，并允许调整内核阶数以控制其拟合能力。这些特性促使我们探索使用多阶KAN来表示不同频率下的时序模式，从而为预测提供更准确的信息。

### 2\. 相关工作

### 2.1 Kolmogorov-Arnold网络（KAN）

Kolmogorov-Arnold表示定理指出，任何多变量连续函数都可以表示为单变量函数和加法操作的组合。KAN利用这一理论，提出了一种创新的传统MLP替代方案。与MLP在节点处使用固定激活函数不同，KAN在边缘引入可学习的激活函数。由于其灵活性和适应性，KAN被认为是MLP的有前途的替代品。

最初的KAN使用样条函数进行参数化，但由于样条函数的固有复杂性，其速度和可扩展性不尽如人意。因此，后续研究探索使用更简单的基函数来替代样条函数，从而实现更高的效率。例如， [ChebyshevKAN](https://zhida.zhihu.com/search?content_id=254610134&content_type=Article&match_order=1&q=ChebyshevKAN&zhida_source=entity) 采用切比雪夫多项式对可学习函数进行参数化，FastKAN使用更快的Gaussian径向基函数来近似三阶B样条函数。

此外，KAN已被应用于替代MLP的各种领域。例如，卷积KAN用可学习的样条函数矩阵替换传统卷积网络中的线性权重矩阵， [U-KAN](https://zhida.zhihu.com/search?content_id=254610134&content_type=Article&match_order=1&q=U-KAN&zhida_source=entity) 将KAN层集成到U-Net架构中，在多个医学图像分割任务中表现出色。KAN还被用于弥合AI与科学之间的差距，例如PIKAN和PINN利用KAN构建物理信息机器学习模型。本文旨在将KAN引入TSF，并展示KAN在表示时间序列数据方面的强大潜力。

### 2.2 时间序列预测

传统的TSF方法，如ARIMA，虽然可以为预测结果提供足够的可解释性，但往往无法实现令人满意的准确性。近年来，深度学习方法在TSF领域占据主导地位，主要包括基于CNN、Transformer和MLP的方法。基于CNN的模型主要沿时间维度应用卷积操作以提取时序模式。例如，MICN和TimesNet通过调整感受野来捕捉序列中的短期和长期视图，从而提高序列建模的精度。ModernTCN主张沿时间维度使用大型卷积核，并捕捉跨时间和跨变量的依赖关系。

与感受野有限的CNN方法相比，Transformer方法具有全局建模能力，使其更适合处理长而复杂的序列数据。它们已成为现代时间序列预测的基石。例如，Informer是Transformer模型在TSF中的早期实现之一，通过仔细修改内部Transformer架构，实现了高效预测。PatchTST沿时间维度将序列划分为多个补丁，然后将其输入Transformer，使其成为时间序列领域的重要基准。相比之下，iTransformer将每个变量视为一个独立的token，以捕捉多变量时间序列中的跨变量依赖关系。然而，Transformer方法由于参数数量庞大和内存消耗高而面临挑战。

最近对MLP方法的研究表明，通过适当设计的架构利用先验知识，简单的MLP可以胜过复杂的Transformer方法。例如，DLinear使用趋势-季节分解策略对序列进行预处理，FITS在频域中进行线性变换，而TimeMixer使用MLP促进不同尺度上的信息交互。这些基于MLP的方法在预测准确性和效率方面都表现出强大的性能。与上述方法不同，本文将新颖的KAN引入TSF，以更准确地表示时间序列数据，并提出了一种精心设计的分解-学习-混合架构，以充分释放KAN在时间序列预测中的潜力。

### 2.3 时间序列分解

现实世界中的时间序列通常包含各种潜在模式。为了利用不同模式的特征，最近的方法倾向于将序列分解为多个子成分，包括趋势-季节分解、多尺度分解和多周期分解。例如，DLinear使用移动平均来解耦季节性和趋势性成分，SCINet使用分层下采样树来迭代提取和交换多个时间分辨率的信息，TimeMixer遵循从细到粗的原则，将序列分解为不同时间跨度的多个尺度，并进一步将每个尺度分解为季节性和周期性成分。TimesNet和PDF利用傅里叶周期分析，根据计算出的周期将序列解耦为多个子周期序列。受这些工作的启发，本文提出了一种新颖的分解-学习-混合架构，从多频率角度审视时间序列，以准确建模时间序列中的复杂模式。

![[raw/assets/attachments/timeseries/v2-e4c1ad79e2610a706ac027eaa7a0e21e_1440w.jpg]]

### 3\. TimeKAN

### 3.1 整体架构

给定历史多变量时间序列输入 ，时间序列预测的目标是预测未来输出序列 ，其中 是回溯窗口长度和未来窗口长度， 代表变量的数量。本文提出 TimeKAN 来应对时间序列中多频率成分复杂混合带来的挑战。TimeKAN 的整体架构如图 1 所示。我们采用变量独立的方式独立预测每个单变量序列。每个单变量输入时间序列表示为 ，在以下计算中我们将单变量时间序列视为实例。在我们的 TimeKAN 中，第一步是使用移动平均逐步去除相对高频成分，并生成多级序列，然后将这些序列投影到高维空间中。接下来，遵循分解-学习-混合架构设计原则，我们首先设计级联频率分解 (CFD) 块以采用自下而上的级联方法获取每个频率带的序列表示。然后，我们提出多阶 KAN 表示学习 (M-KAN) 块以学习并表示每个频率带内的特定时序模式。最后，频率混合块将频率带重新组合成原始格式，确保分解-学习-混合过程可重复。以下是 TimeKAN 的更多详细信息。

### 3.2 分层序列预处理

假设我们将原始时间序列 的频率范围划分为预定义的 个频率带。我们首先使用移动平均逐步去除相对高频成分，并生成多级序列 ，其中 。 等于输入序列 ， 表示移动平均窗口的长度。生成多级序列的过程如下：

在获得多级序列后，每个序列都通过线性层独立嵌入到更高维度：

其中 且 是嵌入维度。我们将 定义为最高级别的序列，将 定义为最低级别的序列。值得注意的是，每个较低级别的序列都是通过从比其高一级的序列中去除一部分高频信息而获得的。上述过程是预处理过程，在 TimeKAN 中只发生一次。

### 3.3 级联频率分解

现实世界中的时间序列通常由多个频率成分组成，低频成分代表时间序列的长期变化，高频成分代表短期波动或突发事件。这些不同的频率成分相辅相成，为准确建模时间序列提供了全面的视角。因此，我们设计了级联频率分解 (CFD) 块以级联方式准确分解每个频率成分，从而为准确建模不同频率成分奠定基础。

CFD 块的目标是获得每个频率成分的表示。这里，我们以获得第 个频率带的表示为例。为了实现这一点，我们首先使用快速傅里叶变换 (FFT) 获得 在频域中的表示。然后，使用零填充来扩展频域序列的长度，使其在转换回时域后可以与上序列 保持相同的长度。接下来，我们使用逆快速傅里叶变换 (IFFT) 将其转换回时域。我们将这种上采样过程称为频率上采样，它确保了上采样前后频率信息保持不变。频率上采样的过程可以描述为：

$${\\hat{x}}\_{i}={\\mathrm{IFFT}({\\mathrm{Padding}}({\\mathrm{FFT}}(x\_{i+1}))) $$

这里， 和 具有相同的序列长度。值得注意的是，与 相比， 缺少第 个频率成分。原因是 原本是通过在分层序列预处理中从 中去除第 个频率成分而形成的，而 现在通过无损频率转换过程转换为 ，从而在时域中与 对齐长度。因此，要获得时域中第 个频率成分 的序列表示，我们只需要获得 和 之间的残差：

### 3.4 多阶 KAN 表示学习

鉴于 CFD 块生成的多级频率成分表示 ，我们提出多阶 KAN 表示学习 (M-KAN) 块来学习每个频率下的特定表示和时序依赖性。M-KAN 采用双分支并行架构，以频率特定的方式分别对时序表示学习和时序依赖学习进行建模，使用多阶 KAN 来学习每个频率成分的表示，并采用深度卷积来捕捉时序依赖性。以下将详细介绍深度卷积和多阶 KAN。

深度卷积为了将时序依赖性的建模与学习序列表示分离开来，我们采用了一种特殊的群卷积，即深度卷积，其中群的数量与嵌入维度相匹配。深度卷积使用 组卷积核对每个通道的序列进行独立的卷积操作。这使得模型能够专注于捕捉时序模式，而不会受到通道间关系干扰。深度卷积的过程为：

多阶 KAN 与传统的 MLP 相比，KAN 用可学习的单变量函数替换线性权重，使得可以用更少的参数和更高的可解释性对复杂的非线性关系进行建模（ 等人，2024a）。假设 KAN 由 层神经元组成，第 层神经元的数量为 。第 层的第 个神经元与第 层的所有神经元之间的传输关系可以表示为 i=l1 l,j,i(zl,i)，其中 是第 层的第 个神经元， 是第 层的第 个神经元。我们可以简单地理解为每个神经元都通过一个可学习的单变量函数 与前一层的其他神经元相连。原始 KAN（Liu 等人，2024c）使用样条函数作为可学习的单变量基本函数 ，但由于样条函数的复杂递归计算过程，KAN 的效率受到影响。在这里，我们采用 ChebyshevKAN（SS，2024）来学习每个频率成分的表示，即通道学习。ChebyshevKAN 是由切比雪夫多项式的线性组合构建的。也就是说，使用不同阶数的切比雪夫多项式的线性组合来生成可学习的单变量函数 。切比雪夫多项式定义为：

其中 是切比雪夫多项式的最高阶数，切比雪夫多项式的复杂性随着阶数的增加而增加。应用于通道维度的 1 层 ChebyshevKAN 可以表示为：

其中 是输出神经元的索引， 是用于线性组合切比雪夫多项式的可学习系数。值得注意的是，时间序列中的频率成分随着频率的增加表现出越来越复杂的时序动态，这需要具有更强表示能力的网络来学习这些特征。ChebyshevKAN 允许调整切比雪夫多项式的最高阶数 以增强其表示能力。因此，从低频到高频成分，我们采用递增的切比雪夫多项式阶数以使频率成分与 KAN 的复杂性保持一致，从而准确学习不同频率成分的表示。我们将这一组具有不同最高切比雪夫多项式阶数的 KAN 称为多阶 KAN。我们设置一个较低的阶数下限 ， 的表示学习过程可以表示为：

M-KAN 块的最终输出是多阶 KAN 和深度卷积输出的总和。

### 3.5 频率混合

在专门学习每个频率成分的表示之后，我们需要将频率表示重新转换为多级序列的形式，然后进入下一个 CFD 块，确保分解-学习-混合过程可重复。因此，我们设计了频率混合块，将第 级的频率成分 转换为多级序列 ，使其能够作为下一个 CFD 块的输入。要将第 级的频率成分 转换为多级序列 ，我们只需将第 级到第 级的频率信息补充回第 级。因此，我们再次采用频率上采样来逐步将信息重新整合到更高频率成分中：

对于最后一个频率混合块，我们提取最高级别的序列 并使用简单的线性层生成预测结果 。

由于采用变量独立策略，我们还需要将所有变量的预测结果堆叠在一起，以获得最终的多变量预测 。

![[raw/assets/attachments/timeseries/v2-3c79c0fe47b3708be31eba33609c8762_1440w.jpg]]

### 4\. 实验

### 4.1 主要结果

实验结果表明，TimeKAN 在所有数据集中均表现出卓越的预测性能，除了 Electricity 数据集，其中 iTransformer 取得了最佳结果。这是由于 iTransformer 使用了通道级自注意力机制来对变量间依赖关系进行建模，这对于像 Electricity 这样高维的数据集特别有效。此外，TimeKAN 和 TimeMixer 在长期预测任务中均表现一致良好，这展示了精心设计的时序分解架构在准确预测方面的通用性。与其他最先进的方法相比，TimeKAN 引入了新颖的分解-学习-混合框架，将多阶 KAN 的特性与这种分层架构紧密集成，使其在广泛的长期预测任务中表现出色。

![[raw/assets/attachments/timeseries/v2-2794b10c3bdc6e79f75d0c44196a5b37_1440w.jpg]]

### 4.2 消融研究

消融研究主要探讨了 TimeKAN 的几个关键组成部分，包括频率上采样、深度卷积和多阶 KAN。

频率上采样为了研究频率上采样的有效性，我们将其与三种可能无法在转换前后保留频率信息的上采样方法进行了比较：(1) 线性映射；(2) 线性插值；(3) 转置卷积。如表 2 所示，用这三种方法中的任何一种替换频率上采样都会导致性能下降。这表明这些上采样技术在转换后无法保持频率信息的完整性，导致分解-学习-混合框架失效。这有力地证明了所选的频率上采样作为一种非参数方法，是 TimeKAN 框架中不可替代的组成部分。

多阶 KAN我们设计了以下模块来研究多阶 KAN 的有效性：(1) MLPs，这意味着使用 MLP 替换每个 KAN；(2) 固定低阶 KAN，这意味着在每个频率级别使用阶数为 2 的 KAN；(3) 固定高阶 KAN，这意味着在每个频率级别使用阶数为 5 的 KAN。比较结果如表 3 所示。总体而言，多阶 KAN 取得了最佳性能。与 MLPs 相比，多阶 KAN 的表现明显更好，这表明精心设计的 KAN 比 MLPs 具有更强的表示能力，是 MLPs 的有力替代品。低阶 KAN 和高阶 KAN 的表现均不如多阶 KAN，这表明我们逐步增加 KAN 阶数的选择是有效的，以适应不同频率成分的表示。因此，KAN 的可学习函数确实是一把双刃剑；要获得满意的结果，需要为特定任务选择适当的功能复杂性水平。

![[raw/assets/attachments/timeseries/v2-8807587eb466b15712b6bb7c759c50ba_1440w.jpg]]

深度卷积为了评估深度卷积的有效性，我们用以下选择替换它：(1) 无深度卷积；(2) 标准卷积；(3) 多头自注意力。结果如表 4 所示。总体而言，深度卷积是最佳选择。我们清楚地观察到，移除深度卷积或将其替换为多头自注意力会导致性能显著下降，这突出了使用卷积来学习时序依赖性的有效性。当深度卷积被标准卷积替换时，大多数指标都有所下降，这意味着关注单独提取时序依赖性而不受通道间关系干扰是合理的。

![[raw/assets/attachments/timeseries/v2-1dcc6919c3b845488ea18290465d77b3_1440w.jpg]]

### 5\. 结论

我们提出了一种高效的基于 KAN 的频率分解学习架构 (TimeKAN) 用于长期时间序列预测。基于分解-学习-混合架构，TimeKAN 使用级联频率分解块获取每个频率带的序列表示。此外，多阶 KAN 表示学习块进一步利用 KAN 高度的灵活性来学习并表示每个频率带内的特定时序模式。最后，频率混合块将频率带重新组合成原始格式。对现实世界数据集的广泛实验表明，TimeKAN 实现了最先进的预测性能和极轻量级的计算消耗。

完整代码见星球，加入QuantML星球，与750+专业人士一起交流学习：

![[raw/assets/attachments/timeseries/v2-c54040ac633768c401cdd8395d270532_1440w.jpg]]

往期回顾

QuantML-Qlib开发版：

- [QuantML-Qlib重磅更新：DeepSeek核心模型结构用于选股](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489025%26idx%3D1%26sn%3D35941156783794d719e6ff891ce720c3%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Factor | 融合TA-Lib100+技术指标，自定义构建AlphaZoo](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488425%26idx%3D1%26sn%3Da071798fdcc183b3d630e8bc0d637adf%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 还在使用MSE？试试这些更加适合金融预测的损失函数](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247487997%26idx%3D1%26sn%3De05e8e0dafa605615d425ff1f0702c4b%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 如何运行日内中高频模型](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247487722%26idx%3D1%26sn%3D4597316f8066c31d4bbf34226d888ef4%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 超越GRU，液态神经网络LNN用于股票预测](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247487291%26idx%3D1%26sn%3Dba0c7cb11cbe247900fa326a50dd5dd9%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 华泰SAM：提升AI量化模型的泛化性能 研报复现](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247487238%26idx%3D1%26sn%3D41cbb5b3bb3e5a277c9175ba64642259%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 华泰AlphaNet模型复现](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485666%26idx%3D1%26sn%3Dd9a7ec92f3f93d44d4620bb56ab0d620%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 清华大学&华泰证券 在高胜率时交易](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485500%26idx%3D1%26sn%3Db29e1d2efe2482165245ab6add4af051%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Factor | 高效优雅的因子构建方法：以开源金工切割动量因子为例](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485016%26idx%3D1%26sn%3D17598e7dbdfcb7e908b2a393c5dd28ad%26chksm%3Dce7e6146f909e85067dd7de6ca5f02c12afb9f195f92871c87b0daed0153b1ea04f3057d9683%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | 滚动模型训练](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485371%26idx%3D1%26sn%3D37b9d5c40f9b08244fd68ee73991218f%26chksm%3Dce7e60a5f909e9b373b4b850300768fd2dbe0250e1237e11132f3af9d54f9bde97ba84c47766%26scene%3D21%23wechat_redirect)
- [QuantML-QlibModel | KAN + GRU 时序模型用于股票预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484511%26idx%3D1%26sn%3Dbb9168cb75b1b31fea0b8a5c3ce61d84%26chksm%3Dce7e6341f909ea5755b03dec3d0407d15ac38b60a573cd5517a8a51ba047b1d630c7a15972cb%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 蚂蚁&清华 TimeMixer：可分解多尺度融合的时间序列模型用于金融市场预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484961%26idx%3D1%26sn%3Dc5acb48d3c063c0a69d6566817875aee%26chksm%3Dce7e613ff909e8290602d7d0c32fd7d764fb25660956fbfc3238a7df3d41d5f7e0ffaa2cb6a8%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib Model | Kansformer：KAN+Transformer时序模型用于股票收益率预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484779%26idx%3D1%26sn%3Df417e4ef37562e22fa592ca280fe5a43%26chksm%3Dce7e6275f909eb63cf3410377b0c40a033fb2788b342665c3b266ecbfb426465dcf241bb847d%26scene%3D21%23wechat_redirect)
- [QuantML-QlibModel | 使用OPTUNA优化模型超参](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484466%26idx%3D1%26sn%3D8c6a69a98e64eeba373b1042d276fb81%26chksm%3Dce7e632cf909ea3ae70af5b1acee4163c7b85cb8170a0ef6a999130d05bdb5a54b89a895a0d8%26scene%3D21%23wechat_redirect)
- [QuantML-QlibDB | Clickhouse 行情存储与读取方案](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484391%26idx%3D1%26sn%3Db56d54740da5d77bef608d787033e321%26chksm%3Dce7e64f9f909edef46da039efbeaf07b636ef08477a3f4ba2b49dea329d2c29b71635a809aca%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib LLM | GPT-4o复现因子计算代码](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484355%26idx%3D1%26sn%3D0e2e068277314d93d0373ad5e1b0da82%26chksm%3Dce7e64ddf909edcb0f2894f353b26825800a7862dfb6a53b692b212ae5e93e43c0d7b1ee71cf%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 最新xLSTM用于股票市场预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484305%26idx%3D1%26sn%3Ddeac6944b376b2e7d7cdb552b2bcc0b4%26chksm%3Dce7e648ff909ed99d80c0a73506003b9afbb1e414e748bb91e5b36e7ecb737ded8745d183518%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 强化学习因子挖掘](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484272%26idx%3D1%26sn%3D0b9b53150500d4c77f6afc3267b1313f%26chksm%3Dce7e646ef909ed78bb3216dd647872ffc47fafc116021b34caef842d6b78c1cbf98c343e3fd2%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 清华大学时序SOTA模型iTransformer用于股票市场预测QuantML-Qlib开发版 | 最新神经网络结构KAN用于因子挖掘](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484235%26idx%3D1%26sn%3D5f8f21ad605eee4a9152954164b9b441%26chksm%3Dce7e6455f909ed43d8e4c8d964b5d2d02ed448e8530f6bed0bce00fc8c5d823a82184af1e5c7%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 直接读取pg/mysql/mongodb数据库](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484180%26idx%3D2%26sn%3D69ca761ab7d152740a3058b86ed02e6c%26chksm%3Dce7e640af909ed1cc246be0a4e683a9b45e8bf256cc034cba0a6d316f6e62f9858d4e75e4efb%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | MoE混合专家系统用于提升Transformer表现](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484124%26idx%3D1%26sn%3D735f6f9488e202679ad96b3d19329673%26chksm%3Dce7e65c2f909ecd438e908babf20726acc73162f9a5198c445f5bf3b1bc8ed6ed16474cbecfd%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 一键数据更新](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484065%26idx%3D2%26sn%3Db2ad5cf74fcc452e49f7e4c4ec07439b%26chksm%3Dce7e65bff909eca9c28072649b39e7ad08b9db4a71e5d5d492bfca04ac6b720ca368a665257a%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | AAAI最佳论文Informer用于金融市场预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484065%26idx%3D1%26sn%3Dd666c3cd759ceffbdb304c1097a4ebb8%26chksm%3Dce7e65bff909eca9a4fedaef3b9edabf3d4d65c11f38d6edc80e973a9cc6d4c9944944666071%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 取代Transformer的下一代神经网络结构Mamba用于金融市场预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483988%26idx%3D1%26sn%3D214bf5cd0739cb26c4af3a56252a99eb%26chksm%3Dce7e654af909ec5cba364d5fea1cb170d9a5a7181b5ed063b97e2dbdff3a7a1fdfd587aafffd%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 时序SOTA模型PatchTST用于金融市场预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483873%26idx%3D1%26sn%3Dc2376b203dc69fc2b8df1db00c5246a0%26chksm%3Dce7e66fff909efe99c0f61c17f6226e7e310c8c0fbe900bb7bdad4aafece8aa85e98348297f7%26scene%3D21%23wechat_redirect)
- [QuantML-Qlib开发版 | 一行代码运行DLinear模型用于股票预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483796%26idx%3D1%26sn%3Dc10f4d766eb52e8dee53ffb954beeafc%26chksm%3Dce7e668af909ef9c5a1a8c6ebc29566475af184ffdf503a0fda308f896eaf42272c6dd591fd2%26scene%3D21%23wechat_redirect)  
	研报复现：
- [重磅更新！80+量化策略复现（持续更新中）](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488528%26idx%3D1%26sn%3Df9c98f60baca2b690956ff6b56a2553f%26scene%3D21%23wechat_redirect)
- [BARRA CNE6模型复现](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484419%26idx%3D1%26sn%3Dec71d0938e90e65145742754ddc4e6d9%26chksm%3Dce7e631df909ea0b60b8a41c67f03e193aff17c556ef30f83528d354e3256402a12205f40b91%26scene%3D21%23wechat_redirect)
- [研报复现 | QRS择时信号及改进](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247487334%26idx%3D1%26sn%3D110ef4c3ae5dce77260eab213d6163ac%26scene%3D21%23wechat_redirect)
- [研报复现 | 跳跃因子系列-下](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247486787%26idx%3D1%26sn%3Dbfe98c0b8d331027191761df3b85ea8c%26scene%3D21%23wechat_redirect)
- [研报复现 | 跳跃因子系列-上](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247486761%26idx%3D1%26sn%3D84a2de96dd3bc7a7fb38386684b3eec4%26scene%3D21%23wechat_redirect)
- [研报复现 | 锚定反转因子](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247486379%26idx%3D1%26sn%3Dd6763bb198d0706c101f2544aa752b4f%26scene%3D21%23wechat_redirect)
- [研报复现 | 另类ETF交易策略：日内动量](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485900%26idx%3D1%26sn%3Dc7facdbd47ebc0161839fbea1def4ecc%26scene%3D21%23wechat_redirect)
- [研报复现 | 国盛金工：如何将隔夜涨跌变为有效的选股因子？——基于对知情交易者信息优势的刻画](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485766%26idx%3D1%26sn%3D89d4060fb135105b969c0ef2f145a7e0%26scene%3D21%23wechat_redirect)
- [研报复现 | 招商证券：基于鳄鱼线的指数择时及轮动策略](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485702%26idx%3D1%26sn%3D2b0ed284177a66ee9d0e8623cd9cb1b4%26scene%3D21%23wechat_redirect)
- [研报复现 | 华西金工-股票网络与网络中心度因子研究](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484829%26idx%3D1%26sn%3D3da8197374301bab9610f7ed5d4b715b%26chksm%3Dce7e6283f909eb9509b3ebc9989fe9d140d5ee663ac8749aeb608833ff37544421d0dcd0fa9c%26scene%3D21%23wechat_redirect)
- [研报复现 | 基于筹码分布的选股策略](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485327%26idx%3D1%26sn%3D260ff24d4fde6fa394f989b23488780f%26chksm%3Dce7e6091f909e987086ba01ad8df6f3dd8ef0fa63fe41930e784f2648066e44bad6c24b02a91%26scene%3D21%23wechat_redirect)
- [研报复现 | 开源金工-高频追涨杀跌因子复现](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484915%26idx%3D1%26sn%3Da7279f3516c0998cd6c3e6fddec017a9%26chksm%3Dce7e62edf909ebfb211722e6bb19b4a43243c4751dd6e4143249b04afe3bed980ffb0ce68ff3%26scene%3D21%23wechat_redirect)
- [研报复现 | 开源证券 ：形态识别，均线的](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484616%26idx%3D1%26sn%3Dcbf8bf6df9906603258516c808e45b94%26chksm%3Dce7e63d6f909eac044db7ca34624d21c241c485bce4450e1ea23ccf4463414638c52cae5cbea%26scene%3D21%23wechat_redirect)
- [券商研报因子复现及表现研究](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484329%26idx%3D1%26sn%3D24f18ad20fc0a44ba09a19d43becf651%26scene%3D21%23wechat_redirect)  
	前沿论文代码：
- [DeepSeek-TS+: MLA-Mamba及GRPO用于多序列预测统一框架](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489198%26idx%3D1%26sn%3D4ea3856dcf099493c2ba6db7cf0e23a2%26scene%3D21%23wechat_redirect)
- [Hummingbot：开源加密货币做市机器人框架](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489153%26idx%3D1%26sn%3D98198f6cca4aa5bc5646e926c358f01d%26scene%3D21%23wechat_redirect)
- [FinRLlama：基于强化学习和市场反馈的金融情感分析LLM优化方案](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489127%26idx%3D1%26sn%3Dfaad16c8ac3ca02dcb982837d03b21ab%26scene%3D21%23wechat_redirect)
- [端到端基于LLM的增强型交易系统](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489113%26idx%3D1%26sn%3Db145d87e23cfa5c9e780099fc7c1136c%26scene%3D21%23wechat_redirect)
- [基于分层强化学习的日内风险因子挖掘](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489104%26idx%3D1%26sn%3Dc0b6938ebcf0cbd8244f87abe609798e%26scene%3D21%23wechat_redirect)
- [DeepScalper：深度强化学习捕捉日内交易的短暂机会](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247489018%26idx%3D1%26sn%3D1ea12b6de5e28e2700b4947081a32b7b%26scene%3D21%23wechat_redirect)
- [TradingAgents：基于多智能体LLM的金融交易框架](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488712%26idx%3D1%26sn%3Ddaa7fb4a9d49a621f9f54579dda4a184%26scene%3D21%23wechat_redirect)
- [Kaggle - Optiver trading at the close第一名解决方案及部分代码](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484474%26idx%3D1%26sn%3Dd7cb587cd3604299930006e2f0dd54cf%26chksm%3Dce7e6324f909ea320e815af314efc2f2eb4dd944ca56e0fccaf0990e099b001610461a1e798d%26scene%3D21%23wechat_redirect)
- [量化交易全攻略：从入门到精通的终极指南](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247485434%26idx%3D1%26sn%3D9ea5dd98ac51fa0eb0381d97fa2d2b78%26scene%3D21%23wechat_redirect)
- [普林斯顿&牛津大学 | 大模型在金融领域的应用、前景和挑战](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484935%26idx%3D1%26sn%3Dc04614316ebaaf46fe0ef35b88aba330%26chksm%3Dce7e6119f909e80fcc08f835d91cdddeb1e3dacf3bd924fcd5958381f13eaace114139af909b%26scene%3D21%23wechat_redirect)
- [Style Miner：基于强化学习算法的风格因子构造](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488487%26idx%3D1%26sn%3D82c708030492662f4bd958c09cd6ad35%26scene%3D21%23wechat_redirect)
- [AQR创始人Cliff Asness：市场效率下降假说](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488456%26idx%3D1%26sn%3D7014a441007cd69045f69cfada3f64fd%26scene%3D21%23wechat_redirect)
- [增强动量策略：动量Transformer模型](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488434%26idx%3D1%26sn%3De8431bb689e27562a620cdb6cf3c6d31%26scene%3D21%23wechat_redirect)
- [XGBoost 2.0 ：提升时间序列预测能力](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488387%26idx%3D1%26sn%3Dd123dcfc4c74e13b7bfd10a707eab81f%26scene%3D21%23wechat_redirect)
- [NIPS 24 | FinCon: 基于LLM的多智能体交易及组合管理框架](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488353%26idx%3D1%26sn%3Df6684d1c9788e0f9dcd09b781cbd619a%26scene%3D21%23wechat_redirect)
- [NIPS 24 | CausalStock: 基于端到端因果发现的新闻驱动股价预测模型](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488342%26idx%3D1%26sn%3D4793d31201295e14a5978556f449adca%26scene%3D21%23wechat_redirect)
- [JFE | 高效估计买卖价差的模型、实证与应用](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488303%26idx%3D1%26sn%3D60ab39ed1be0a71185396aadfa33aeee%26scene%3D21%23wechat_redirect)
- [超越传统网格交易：新型网格交易系统](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488269%26idx%3D1%26sn%3D7b9a60116d5c65278e6894ded1ce79aa%26scene%3D21%23wechat_redirect)
- [JFE | ETF日内套利研究](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488257%26idx%3D1%26sn%3D9eb00eade68c4f6816916330b859adb0%26scene%3D21%23wechat_redirect)
- [NIPS 24 | 超越CVXPY,新型端到端优化器](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247488193%26idx%3D1%26sn%3Da91d10d06dca7a988dda550ccaaa9941%26scene%3D21%23wechat_redirect)
- [揭秘Jane Street低延迟系统的优化技巧——减少系统抖动](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247487942%26idx%3D1%26sn%3D834867f33667a640961b34756c730ca9%26scene%3D21%23wechat_redirect)
- [南京大学LAMDA-强化学习DRL挖掘逻辑公式型Alpha因子](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484882%26idx%3D1%26sn%3De4fee58dd1ca85b6469e3803be5e97a5%26chksm%3Dce7e62ccf909ebdaa93ae29cef9c59c7f889d784b1c774014b339dc55a375d03443d61b48037%26scene%3D21%23wechat_redirect)
- [3万个因子，数据挖掘能超越同行审议的因子吗？](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484872%26idx%3D1%26sn%3D2f420bd9522473ad83dc6f825c421e5c%26chksm%3Dce7e62d6f909ebc05b45a79d8d6e96cac7910b7509ef168a2a7349f29a4c63dbbf7bb9b3ba11%26scene%3D21%23wechat_redirect)
- [KDD 24 | 基于增强记忆的上下文感知强化学习的高频交易框架](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484852%26idx%3D1%26sn%3D612490637ac96cfa86d829e9ed665c2b%26chksm%3Dce7e62aaf909ebbc864a29a4af3cc6db60eb2930f7dade6882515a61d46222e8877e8018fd07%26scene%3D21%23wechat_redirect)
- [FinRobot：用于金融领域的大模型AI平台](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484560%26idx%3D1%26sn%3D689e9b1ec3bf370e7332b538f3060ca1%26chksm%3Dce7e638ef909ea989847e2b1501d17f9524808ad0544ccceaba918b8fda7c13556522b740647%26scene%3D21%23wechat_redirect)
- [KDD 23 | DoubleAdapt: 显著提升各类模型表现的元学习模型](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484726%26idx%3D1%26sn%3D68a12011fce4197b96d2f67b92f7b5c2%26chksm%3Dce7e6228f909eb3e3ca1504f4b29adc1986cdb1bd451f73049077b864be1999d3b3fdcb860ad%26scene%3D21%23wechat_redirect)
- [市场微观结构教程：深度订单簿预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484660%26idx%3D1%26sn%3Dfc191107da65068ab9a5cd01135a5f1d%26chksm%3Dce7e63eaf909eafcc529fa1a5b07985b5b1e3a548c363134f0cc0ee57a5463ceaf91a2946af0%26scene%3D21%23wechat_redirect)
- [基于高频和日频因子的端到端直接排序组合构建模型](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484549%26idx%3D1%26sn%3D347c69bb297aef162bb364a1e68e9e72%26chksm%3Dce7e639bf909ea8d632046f8f9acac70209067aa1f4c142f3a26733262d298b097041744f92d%26scene%3D21%23wechat_redirect)
- [BOA 312页报告：Everything you wanted to know about quant](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484528%26idx%3D1%26sn%3D01c2c5c1be9c62ee11936badd36aca81%26chksm%3Dce7e636ef909ea7896cac5c96c66a9ec1c2626d68e67fcd52632aea20683643d2191d043f0a8%26scene%3D21%23wechat_redirect)
- [深度学习模型DeepLOB用于订单簿价格预测](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484318%26idx%3D1%26sn%3Dce53c0720707138434d539bf1fd265cc%26chksm%3Dce7e6480f909ed96c06a8a6caae8a38d312b9539364cca2570524f184f68d54783cf35a18b37%26scene%3D21%23wechat_redirect)
- [What KAN I say？KAN代码全解析](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484285%26idx%3D1%26sn%3D14a024ba53e87188e7f4eb5a6658744c%26chksm%3Dce7e6463f909ed75d6c00d19f0e5468b58fa19c8ac5e067bbd84111d4df8213a01b8d2cde5b0%26scene%3D21%23wechat_redirect)
- [取代MLP？MIT全新神经网络结构KAN,3天1.4k star](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484180%26idx%3D1%26sn%3D97c579083e1c9fa93e5c6b0310ddc306%26chksm%3Dce7e640af909ed1cf2718c8db750f10afbca50ab7d93cd4537547d8958db0c305b255a1f7e6d%26scene%3D21%23wechat_redirect)
- [WWW'24 | FinReport: 结合新闻语义信息的多因子模型显著提升预测准确性](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484046%26idx%3D1%26sn%3Dbcb0fff3bdf5f7b44f11200a6618ac01%26chksm%3Dce7e6590f909ec86a6c81cde08dd6cc7f45f40bda780014f9e19fa498b7b1e5f7111c2b28e0b%26scene%3D21%23wechat_redirect)
- [WWW'24 | UniTime: 融合文本信息的时间序列预测模型](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484032%26idx%3D1%26sn%3D604d6ba7bcd2fa070bc73909484b621d%26chksm%3Dce7e659ef909ec880ec0c0c1c9fb685b992e1ac84367e89d736578c665022d0bcf7bc14c7cd8%26scene%3D21%23wechat_redirect)
- [WWW'24 | EarnMore: 如何利用强化学习来处理可定制股票池中的投资组合管理问题](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483897%26idx%3D1%26sn%3D00d406b6b8475c6e453e8cef837a5733%26chksm%3Dce7e66e7f909eff1a4b6347d4e21f8263962ec99207a3514f5f76f3747a533a2360b4fb7aa0d%26scene%3D21%23wechat_redirect)
- [KDD'23 | AlphaMix: 高效专家混合框架（MoE）显著提高上证50选股表现](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483915%26idx%3D1%26sn%3D2dc8f2ceffdd225bd3b8ed70385a4a3a%26chksm%3Dce7e6515f909ec03ecdbf9258f1e73972e98229da395c79c7dd533d56455612ab248fc879ff6%26scene%3D21%23wechat_redirect)
- [IJCAI'23 | StockFormer: RL+Self-Attention优化摆动交易提高股票预测精度](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484098%26idx%3D1%26sn%3D40d40326f9a703296115e9720d776f48%26chksm%3Dce7e65dcf909ecca166614ff70d12bdcfb0265b99e8dddfeec75e579a1d3c6e62e5ae9446924%26scene%3D21%23wechat_redirect)
- [AAAI-24 | EarnHFT:针对高频交易的分层强化学习（RL）框架](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483884%26idx%3D1%26sn%3Db6cde76f0cecd07f19179fce94b67922%26chksm%3Dce7e66f2f909efe4a8e9dcae71358111132135ba8f36bbe40faa5e0a2f42c2291f6ebbe9e4c6%26scene%3D21%23wechat_redirect)
- [AAAI-24 | MASTER 结合市场信息的自动特征选择的股票预测模型，25%年化收益](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247483818%26idx%3D1%26sn%3D8f17951f57c801a612c7d47f3e1c3a77%26chksm%3Dce7e66b4f909efa2a462cb0640427342a98fe733beeb3e275b1625b9e6f72dcd29a5adb196f6%26scene%3D21%23wechat_redirect)
- [COLING 2024 | AlphaFin: 结合深度学习及大模型用于股票预测和金融问答，击败现有预测模型](https://link.zhihu.com/?target=http%3A//mp.weixin.qq.com/s%3F__biz%3DMzg2MzAwNzM0NQ%3D%3D%26mid%3D2247484079%26idx%3D1%26sn%3D8459f251f43c453415a615c353c427d2%26chksm%3Dce7e65b1f909eca7fa00766474ddc207110b158528b6da2f6ec96a91a7fbb66727ea5e2a77f2%26scene%3D21%23wechat_redirect)

还没有人送礼物，鼓励一下作者吧

发布于 2025-03-04 18:40・上海[时间序列分析](https://www.zhihu.com/topic/19712111)[2025年最新版DAMA数据治理工程师CDGA通关指南！（附赠资料包）](https://zhuanlan.zhihu.com/p/1969441920406263085)

[

作为一名在一线城市从事数据分析工作6年的职场人，去年5月，我决定通过考取CDGA认证来系统提升自己在数据治理领域的...

](https://zhuanlan.zhihu.com/p/1969441920406263085)