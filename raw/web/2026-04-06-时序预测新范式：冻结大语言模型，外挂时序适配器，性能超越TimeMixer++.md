---
source_type: web
title: "时序预测新范式：冻结大语言模型，外挂时序适配器，性能超越TimeMixer++"
author:
  - 
  - "[[时序之心]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://mp.weixin.qq.com/s/0j5fVRq27caMUm1lv-RfzA"
published: 
created: 2026-04-06
description: "ICLR 2026 | 时序预测新范式：冻结大语言模型，外挂时序适配器，性能超越TimeMixer++"
tags:
  - 
  - "clippings"
---

## ICLR 2026 | 时序预测新范式：冻结大语言模型，外挂时序适配器，性能超越TimeMixer++

原创 时序之心 *2026年2月9日 11:42*

在金融波动、电力调度和气象预警等领域， **时间序列预测（Time Series Forecasting）** 一直扮演着“水晶球”的关键角色。近年来，随着人工智能的爆发，研究人员开始尝试让通用能力极强的 **大语言模型（LLMs）** 跨界来解这一难题。然而，这里存在一个棘手的 **模态差异（Modality Gap）** ：人类语言的语法逻辑与时间序列数字中的周期、波动犹如两种截然不同的语言，强行让大模型“读”数字，往往会导致理解偏差，尤其是面对数据中的突发 **异常（Anomaly）** 时，模型容易“不知所措”。

针对这一挑战，本论文提出了一种名为 **SE-LLM** 的全新框架。该框架没有简单地把数据扔给大模型，而是通过独特的 **时序-语义互相关模块（TSCC）** 和 **时间适配器（Time-Adapter）** ，像翻译官一样将时间序列的“节奏”和“突变”转化为大模型能听懂的“语义”。这一设计不仅在不重新训练大模型参数的情况下大幅降低了计算成本，还在长短期预测、零样本预测等多个任务中取得了超越现有最先进技术的优异成绩。

另外我整理了 **时间序列即插即用相关论文** ，感兴趣的自取！

关注“时序之心”回复“C851”

免费领取 **时序即插即用相关论文合集**

## 二、 基本信息

![[Image 76.webp|图片]]

- **论文标题：** Semantic-Enhanced Time-Series Forecasting via Large Language Models
- **作者姓名：** Hao Liu, Chun Yang, Zhang Xiaoxing, Xiaobin Zhu 等
- **作者单位：** 北京科技大学（University of Science and Technology Beijing）、中国电信（China Telecom）
- **论文链接：** https://arxiv.org/abs/2508.07697

## 三、 主要贡献

1. **框架创新：** 提出了 **SE-LLM** 框架，有效弥合了时间序列数据与自然语言之间的模态鸿沟，激活了冻结状态下 LLM 的泛化能力。
2. **语义增强：** 设计了 **TSCC 模块** ，通过将时间序列的周期性和异常模式注入语义空间，显著增强了 Token 嵌入的解释性。
3. **适配器设计：** 开发了 **Time-Adapter** 插件，解决了 Transformer 架构在捕捉短期突变和长期依赖方面的不足。
4. **性能验证：** 在长短期预测、零样本学习等多种任务中击败了 TimeMixer++、AutoTimes 等 **SOTA（State-of-the-Art）** 方法。

## 四、 方法与原理

![Figure 2.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 2.

- **核心思路：** 模型的核心在于“翻译”与“增强”。它不通过微调大模型本身来适应数字，而是先通过 **时序-语义互相关** 机制，把时间序列里的“异常噪点”和“正常周期”分离并转化成大模型熟悉的语义特征；再给大模型装上一个专门的“眼镜”（适配器），让习惯看长文的大模型也能敏锐捕捉数据的长短时变化。
- **架构解析：**
	SE-LLM 的整体工作流程可以分为三个关键阶段，如图2所示。其核心在于如何在保持 LLM 参数冻结（Frozen）的情况下，注入时间序列特征。
- **模块结构：** 作者在 LLM 的自注意力层中嵌入了 Time-Adapter（对应原论文图4）。该模块包含两条并行的 LSTM 路径：一条用于捕捉 **长期依赖** ，通过低秩投影压缩维度后输入 LSTM；另一条用于捕捉 **短期异常** 。
	- **注入方式：** 处理后的时序信息被注入到注意力机制的 Key () 和 Value () 矩阵中：这使得 LLM在推理时，既能利用其强大的通用推理能力，又能兼顾时间序列特有的长短期动态特性。
- **互相关计算：** 首先计算时序特征 与语义特征 之间的标准化互相关矩阵 ，用于衡量哪些语义与当前的时间模式最相关：其中， 和 分别代表均值和标准差。
	- **异常建模：** 为了处理时间序列中的噪声和突变，模块引入了一个 **异常建模变分自编码器（AM-VAE）** 。它在联合空间中重构均值和方差，将语义分解为“异常语义”（）和“去异常语义”（）。
	- **特征融合：** 通过 Top-K 筛选机制，将最相关的时序模式加权注入到上述语义中，最终生成带有丰富时间规律的语义嵌入，供 LLM 理解。
1. **时序嵌入与语义对齐：** 输入的时间序列首先经过滑动窗口处理，通过一个线性层投影为高维的 **TS Embeddings** （）。同时，利用预训练 LLM 的词嵌入（Word Embedding）生成通用的 **语义空间（Semantic Space, ）** 。为了让两者“对话”，模型使用交叉注意力机制（Cross-Attention）将时序特征对齐到语义空间。
	2. **时序-语义互相关模块（TSCC）：** 这是本论文的核心创新点（对应原论文图3）。为了让语义向量包含时间的动态变化，作者设计了 TSCC。
	3. **时间适配器（Time-Adapter）：** 即便有了增强的语义，LLM 原生的 Transformer 结构更擅长处理文本的长依赖，而对数值的短期波动不敏感。

## 五、 实验与结果

![Table 1.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Table 1.

![Figure 6.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 6.

为了验证 SE-LLM 的有效性，研究团队在 ETTh1、Weather、Traffic、ECL 等 8 个主流数据集上进行了广泛测试，涵盖了长短期预测、零样本预测等场景。

- **对比实验：** 在长时预测任务中，SE-LLM 展现了压倒性的优势。
	如表1所示，在 **ETTh1** 和 **Traffic** 等数据集上，SE-LLM 的 **均方误差（MSE）** 显著低于 TimeMixer++ 和 AutoTimes 等现有顶尖模型。特别是在 Traffic 数据集上，MSE 相比 SOTA 方法降低了 **4.4%** 。这意味着模型在处理具有复杂交通流特征的数据时，能够更精准地捕捉波动趋势。
	在短时预测任务（M4数据集）中，SE-LLM 同样表现出色，其 SMAPE 指标比第二名降低了 0.26%，证明了其在不同时间跨度下的鲁棒性。
- **可视化与消融实验：**
	为了探究这种提升究竟来自哪里，作者进行了详细的消融实验和可视化分析。
	如图6所示，未经处理的语义空间特征分布较为混乱，而在引入 **TSCC 模块** 后，通过 t-SNE 可视化可以看到，原本混杂的异常模式（Anomaly Patterns）呈现出了清晰的聚类特征。这直观地证明了模型成功地将时间序列中的异常信息“剥离”并嵌入到了语义空间中，使得 LLM 能够区分正常波动与突发异常。 此外，针对 Time-Adapter 的消融实验显示，相较于通用的 LoRA 微调技术，Time-Adapter 能更好地适应时间序列任务，验证了专门针对时序设计的 LSTM 旁路结构的必要性。

## 六、 结论与评价

- **总结：** 本论文提出了一种极具启发性的时间序列预测新范式 SE-LLM。它并没有试图完全重新训练一个时间大模型，而是聪明地构建了一座桥梁——利用 TSCC 将冰冷的数字规律转化为大模型可理解的语义，并利用 Time-Adapter 弥补了大模型在微观数值变化感知上的短板。实验结论表明，这种“冻结大模型 + 外挂时序组件”的策略，不仅大幅提升了预测精度，也为未来利用通用大模型解决特定领域（如金融、气象）的数值分析问题提供了极为重要的技术启示。
- **优点：**
1. **解释性强：** 与传统“黑盒”模型不同，通过将异常和周期模式映射到语义空间，增强了模型对数据内在逻辑的可解释性。
	2. **高效低耗：** 采用冻结 LLM 参数的策略，仅训练轻量级的适配器和投影层，极大地降低了训练资源消耗，且推理速度优于 AutoTimes 和 Time-LLM。
	3. **泛化能力：** VAE 的引入使得模型能够模拟噪声分布，从而在零样本（Zero-shot）预测场景下表现出极强的适应性，面对未见过的数据集也能从容应对。
- **缺点：**
1. **架构复杂性：** 引入 AM-VAE、互相关计算以及双路 LSTM 适配器，使得整体模型架构相对复杂，超参数调整（如 Top-K 的选择）可能对模型性能有较大影响。
	2. **数据兼容性：** 论文在实验部分提到，由于算法设计原因，部分数据集（如 Table 1 中 Traffic 的部分基线结果缺失）无法兼容测试，这暗示了该方法在处理极端特殊结构的时间序列数据时可能存在一定的局限性或工程适配难度。

扫码添加小助手回复“C851”

免费获取全部论文资料

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

相关推荐

[2026时序新思路-时间序列+多模态LLM](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488925&idx=1&sn=73736357182b7611da6479cce3d2298d&scene=21#wechat_redirect)

[ICLR 2026 | 终于不用改模型架构了！TaTS仅用轻量MLP层就让现有时序模型效果飞升](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488905&idx=1&sn=a0e7a5af5bbb513ce41d83c71a8efdf1&scene=21#wechat_redirect)

[ICLR 2026 | 时序可解释性大提升！TimeSliver在26个数据集上性能逼近SOTA!](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488896&idx=1&sn=28ab1b7e00d3c847bf09d17637363a97&scene=21#wechat_redirect)

[ACM 2026 | 精度暴涨66%！即插即用的轻量级时序分类增强模块DualCD！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488870&idx=1&sn=193e17e2fef7ae6ebb26c7565af8442c&scene=21#wechat_redirect)

[ICLR 2026 | 都在吹大模型，实测下来还得看架构设计！TimeOmni 在 SciTS 上的跑分说明了一切](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488860&idx=1&sn=ec374978ec6cdce9f1b6dff4e8980355&scene=21#wechat_redirect)

[师弟用Claude Code肝了48页时序综述+理论到实践全覆盖+质量够硬，可冲SCI](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488849&idx=1&sn=6744e801d56a35184e9dde325711f1f2&scene=21#wechat_redirect)

[ICLR 2026 震撼放榜！1.9万投稿激战，28%接收率，时间序列方向最全盘点来喽！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488824&idx=1&sn=43171736ef708a941ba85ed17d4f0510&scene=21#wechat_redirect)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) ![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

注：本公众号发布的内容仅用于信息传递与知识分享，不保证绝对准确，也不构成专业建议。因使用内容造成的任何损失，我们概不负责。 若公众号含外部链接，链接内容及运营不受我们控制，由此产生的风险和损失，读者自行承担。此外，原创内容版权归本号所有，未经授权禁止商用。因不可抗力、技术故障等致内容异常，本号同样免责。阅读即视为同意本声明，如有疑问，欢迎联系。

ICLR · 目录

作者提示: 个人观点，仅供参考

阅读原文

继续滑动看下一个

时序之心

向上滑动看下一个