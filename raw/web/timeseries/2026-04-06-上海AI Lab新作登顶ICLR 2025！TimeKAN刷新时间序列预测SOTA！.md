---
source_type: web
title: "上海AI Lab新作登顶ICLR 2025！TimeKAN刷新时间序列预测SOTA！"
author:
  - 
  - "[[时序之心]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "现实世界中的时间序列数据往往是非平稳的，且包含多种频率成分，这些成分相互交织，使得时间序列内部的关系复杂化，难"
tags:
  - 
  - "clippings"
source_url: "https://mp.weixin.qq.com/s/3Kk-WK5cD_wocIEN6RgRGg"
published_at: null
related_concepts: []
---

原创 时序之心 *2025年8月11日 11:39*

现实世界中的时间序列数据往往是非平稳的，且包含多种频率成分，这些成分相互交织，使得时间序列内部的关系复杂化，难以捕捉历史观测与未来目标之间的联系。低频成分通常代表长期周期性变化，而高频成分则捕捉短期波动或突发事件。不同频率成分的信息密度不同，采用统一的建模方法可能会导致对不同频率成分的特征描述不准确，从而影响预测效果。

为了解决这个问题，来自上海人工智能实验室，兰州大学等研究团队提出了TimeKAN，将时间序列中的不同频率成分分离出来，分别对它们进行建模。该文章已中稿ICLR 2025。

另外，我整理了 **ICLR 2025时间序列** 相关论文合集，感兴趣的自取~

关注“时序之心”回复“C276”

免费领取ICLR 2025时间序列论文+源码

## 相关论文

![[Image 67.webp|标题]]

标题

论文标题：TimeKAN: KAN-based Frequency Decomposition Learning Architecture for Long-term Time Series Forecasting

论文链接：https://arxiv.org/pdf/2502.06910

代码链接：https://github.com/huangst21/TimeKAN

## 背景

时间序列数据通常包含多种频率成分，例如： 低频成分代表长期趋势或周期性变化，如季节性变化（每年的季节性波动）或长期趋势（如经济的长期增长）。而高频成分捕捉短期波动或突发事件，如每日的交通流量变化或突发的天气变化。这些不同频率成分的信息密度不同，且它们在时间序列中的相互作用使得预测变得极为复杂。例如，在金融市场中，长期趋势可能受到宏观经济因素的影响，而短期波动可能受到突发事件（如新闻报道或政策变化）的影响。

现有的方法核心思想是通过分解简化时间序列，从而为预测提供更有价值的信息。然而，这些方法主要集中在趋势和季节性成分的分解，而对于频率成分的分解和建模仍然不够完善。它们采用统一的建模方法来处理这些不同频率成分，可能会导致对某些成分的特征描述不准确，从而影响预测效果。

## TimeKAN

为了解决上述问题，研究者们提出了TimeKAN。TimeKAN 的核心思想是将时间序列中的不同频率成分分离出来，分别对它们进行建模，然后再将它们重新组合，从而实现更准确的预测。这一过程被称为“分解 - 学习 - 混合”架构。其整体框架如图1所示。

![图1 TimeKAN 框架图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图1 TimeKAN 框架图

### 级联频率分解（CFD）模块

CFD 模块采用自底向上的级联方法，逐步从时间序列中提取不同频率成分的表示。具体来说，CFD 模块首先使用移动平均法逐步去除时间序列中的高频成分，生成多级序列。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

然后，通过快速傅里叶变换（FFT）将这些序列转换到频率域，并通过零填充扩展频率域序列的长度，使其在转换回时间域后与上一级序列长度相同。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这一过程称为频率上采样。通过计算上一级序列与频率上采样后的序列之间的残差，可以得到特定频率成分的时间序列表示。

### 多阶 KAN 表示学习（M-KAN）模块

M-KAN 模块是 TimeKAN 的核心部分，它利用 KAN 的高灵活性来学习和表示每个频率成分中的特定时间模式。KAN（Kolmogorov-Arnold Network）是一种基于 Kolmogorov-Arnold 表示定理的神经网络架构，能够通过可学习的激活函数来建模复杂的非线性关系。与传统的 MLP 相比，KAN 提供了更高的灵活性和适应性。

在 M-KAN 模块中，研究者们采用了双分支并行架构，分别用于建模时间依赖性和学习序列表示。具体来说，M-KAN 模块包括深度卷积（Depthwise Convolution）和多阶 KAN 两个部分。深度卷积通过分组卷积操作独立地对每个通道的序列进行卷积，从而捕捉时间模式，而不受通道间关系的干扰。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

多阶 KAN 则通过调整 Chebyshev 多项式的最高阶数来控制其表示能力，从而更好地学习不同频率成分的复杂性。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

最终输出为

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### 频率混合模块

在分别学习了每个频率成分的表示之后，需要将这些频率成分重新组合为原始格式。频率混合模块通过频率上采样将每个频率成分逐步补充回更高频率成分中，从而生成多级序列。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

最终，通过一个简单的线性层将最高级序列映射为预测输出。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

## 实验分析

### 主实验

TimeKAN 在多个真实世界的时间序列数据集上进行了广泛的实验，包括 Weather、ETTh1、ETTh2、ETTm1、ETTm2 和 Electricity 等数据集。实验结果表明，TimeKAN 在长期时间序列预测任务中取得了最先进的性能。

![图2 预测结果，输入长度96](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图2 预测结果，输入长度96

### 参数量

TimeKAN的参数数量显著低于现有的时间序列预测模型。TimeKAN 的参数数量仅为 23.34K，而 PatchTST 的参数数量则高达 6.90M，是 TimeKAN 的 295 倍。此外，TimeKAN 的乘累加运算（MACs）也远低于其他模型，显示出其高效的计算性能。

![图3 参数量对比](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图3 参数量对比

### 不同预测长度的性能对比

为了进一步评估 TimeKAN 在不同预测长度下的性能，我们对 ETTm2 和 Weather 数据集进行了实验，预测长度分别为 96、192、336 和 720 个时间步。随着预测长度的增加，TimeKAN 的 MSE 值逐渐降低，表明其在处理更长时间序列时具有更强的预测能力

![图4 更长输入长度](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

图4 更长输入长度

## 结论

TimeKAN 作为一种新型的时间序列预测模型，通过其独特的频率分解 - 学习 - 混合架构，为长期时间序列预测提供了一种高效且准确的解决方案。它不仅在多个真实世界的数据集上取得了优异的性能，还展示了其轻量级和高效计算的优势。TimeKAN 的成功为时间序列预测领域带来了新的思路和方法，也为未来的研究提供了新的方向。

扫码添加小助手回复“C276”

免费获取全部论文资料

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

相关推荐

[ICML 2025 | LangTime 语言引导的时序基础模型实现跨领域精准预测！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486582&idx=1&sn=51d6b2e49614c76f697e88fa1a546119&scene=21#wechat_redirect)

[2025 | 重构已死，相异性当立！SimAD重新定义时间序列异常检测新范式!](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486563&idx=1&sn=c9e7dee6604ab7b7cccd7cd6aff74fea&scene=21#wechat_redirect)

[25|中科大TimeReasoner：LLM慢思考解锁TSF新境界!](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486539&idx=1&sn=ff084374f33b8d87a28e30de0d9c94fa&scene=21#wechat_redirect)

[ICLR 2025 | TIMEMIXER++：通用时序预测新SOTA，全面超越Transformer！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486524&idx=1&sn=ba81479a7b9b52af1e80cf8f2e5e853c&scene=21#wechat_redirect)

[ACL 2025精选：时间序列论文精华速览！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486516&idx=1&sn=e2596c7b20965db60c67be9ac6031dc8&scene=21#wechat_redirect)

[ICML 2025 | A2P模型精准预测时间序列未来异常点！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247486516&idx=2&sn=47ca77273f1994090df08f34106feee1&scene=21#wechat_redirect)

注：本公众号发布的内容仅用于信息传递与知识分享，不保证绝对准确，也不构成专业建议。因使用内容造成的任何损失，我们概不负责。 若公众号含外部链接，链接内容及运营不受我们控制，由此产生的风险和损失，读者自行承担。此外，原创内容版权归本号所有，未经授权禁止商用。因不可抗力、技术故障等致内容异常，本号同样免责。阅读即视为同意本声明，如有疑问，欢迎联系。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

作者提示: 个人观点，仅供参考

阅读原文

继续滑动看下一个

时序之心

向上滑动看下一个