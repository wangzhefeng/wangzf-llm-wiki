---
author:
- null
- '[[时序之心]]'
created: 2026-04-06
created_at: 2026-04-06
description: AAAI 2026 | 刷新9大榜单！哈工大提出interPDN：干翻iTransformer，时序预测新霸主诞生！
published: null
source: https://mp.weixin.qq.com/s/Cu7PP9UkSDpUb068hLtOKg
source_type: web
status: inbox
tags:
- null
- clippings
title: 刷新9大榜单！哈工大提出interPDN：干翻iTransformer，时序预测新霸主诞生！
topics:
- 大语言模型
- 时间序列
---

## AAAI 2026 | 刷新9大榜单！哈工大提出interPDN：干翻iTransformer，时序预测新霸主诞生！

原创 时序之心 *2026年1月28日 10:39*

在金融市场波动、电力负荷调度以及气象灾害预警等领域，准确预测未来的数据走势至关重要。这就是所谓的 **时间序列预测（TSF）** 。然而，现有的深度学习模型大多面临一个难题：它们通常只能给出一个具体的预测数值，却无法告诉我们这个预测有多大的把握，忽略了数据中内在的不确定性。虽然有一些概率预测模型尝试解决这个问题，但它们往往需要假设数据符合某种特定的分布形状（如高斯分布），或者在将连续数值转化为离散类别时产生误差。

为了彻底解决这些痛点，本论文提出了一种名为 **interPDN** 的创新模型框架。该框架不直接预测数值，而是让模型去预测每个时间步上数值出现的 **概率分布** ，并通过计算期望值来获得最终结果。为了防止预测偏差，它巧妙地设计了双分支结构，像两把尺子交错测量一样互相校正误差，并引入了长周期的粗粒度分支进行自我监督。这一设计在多个权威数据集上均取得了超越现有最强模型的优异效果，不仅预测更准，还能捕捉长期的变化趋势。

另外我整理了 **时间序列+小样本数据增强** 相关论文合集，感兴趣的自取！（科研人专属物资见文末！）

关注“时序之心”回复“C799”

免费领取 **时间序列+小样本数据增强论文合集**

## 一、论文基本信息

![[Image 79.webp|图片]]

**论文标题：** Time Series Forecasting via Direct Per-Step Probability Distribution Modeling

**作者姓名：** Linghao Kong, Xiaopeng Hong

**作者单位/机构：** 哈尔滨工业大学计算学部 (The Faculty of Computing, Harbin Institute of Technology)

**论文链接：** https://arxiv.org/pdf/2511.23260

**论文代码：** https://github.com/leonardokong486/interPDN

## 二、主要贡献与创新

1. 摒弃了标量回归的传统范式，将时间序列预测重构为直接的离散 **概率密度分布** 建模问题，无需对数据分布做任何先验假设。
2. 独创了交错式双分支架构，利用两组相互交错的 **支撑集（Support Set）** 来量化输出，有效解决了离散化过程中的边界误判和量化误差问题。
3. 引入了粗细双尺度的自监督学习机制，利用粗粒度分支作为辅助信号，强制模型关注长期趋势，抑制了参数增加带来的过拟合风险。
4. 在九个真实世界数据集的对比实验中，该模型在多数任务上刷新了历史最佳成绩，证明了直接概率建模在确定性预测任务中的巨大潜力。

## 三、研究方法与原理

该论文提出的 **interPDN** 模型的核心思路是：不要让神经网络直接猜数字，而是让它输出一个概率分布直方图，通过统计学方法计算出预测值，并用“两套标准”相互印证来消除误差。

![Figure 2.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 2.

### 1\. 基础骨干网络：提取时序特征

为了处理多变量时间序列中的不同特征，模型首先采用了通道独立的策略，将多维数据拆解为单维序列。对于每一个输入序列，模型利用线性层提取 **趋势项** ，剩下的部分作为 **季节项** 。

在各分支内部，季节项的处理借鉴了 ResNet 的残差结构。模型通过卷积层捕获局部特征，结合线性变换层提取全局信息，最终将季节项和趋势项的输出拼接，得到该分支的基础特征输出 。这里 代表预测的时间步长。其公式表达为：

这种设计保证了模型既能抓住数据的周期性波动，也能把握整体的上升或下降趋势。

### 2\. 概率生成模块：从数值到分布

这是本论文最核心的理论部分。传统的模型会通过一个输出层直接把特征压缩成预测值 ，这忽略了不确定性。 **interPDN** 则引入了一个概率生成模块。

首先，模型通过全连接层将特征维度扩展到 ，其中 是预定义的 **支撑集** 的大小。支撑集可以理解为一系列可能的数值锚点。为了让预测更精准，论文并没有简单地均分数值区间，而是利用正态分布的累积分布函数（CDF）将区间划分为不等长的子区间，使得数据落在每个锚点附近的概率尽可能相等。

模型输出的不再是数值，而是分布 。通过 Softmax 函数，我们可以得到每个时间步上，数值落在各个锚点上的概率。最终的预测值是通过计算这个离散概率分布的 **期望（Expectation）** 得到的：

其中， 是支撑集向量， 表示向量点积。这种计算期望的方式，使得模型即使在面对极不确定的未来时，也能给出一个统计学上最稳健的估计。

### 3\. 交错式双分支架构：消除边界误差

在将连续数值离散化的过程中，如果真实值恰好落在两个锚点的中间边界上，模型很容易产生误判，这被称为量化误差。为了解决这个问题，论文提出了 **交错支撑集** 的概念。

模型构建了两个平行的分支，分别使用两套不同的支撑集 和 。 的锚点位置恰好处于 锚点的中间，两者形成了交错互补的关系。这样，当一个分支在边界处“犹豫不决”导致预测置信度低时，另一个分支往往处于高置信度区域。

为了融合这两个分支的结果，论文设计了一种基于 **最大预测置信度** 的加权融合算法。首先计算每个分支在每个时间步上的最大概率值 和 ：

然后根据置信度计算权重 ：

最终的精细尺度预测结果 由加权和决定：

这种机制确保了模型总是倾向于信任那个“更有把握”的分支，从而极大地平滑了预测结果。

### 4\. 跨尺度约束与损失函数

为了让模型不但在细节上准，在长趋势上也不跑偏，论文不仅在正常时间尺度上部署了上述双分支，还在 **粗粒度时间尺度** （即对时间序列进行降采样）上复制了一套同样的双分支结构。

这就构成了总共四个分支。粗粒度分支的输出并不直接用于最终预测，而是作为一种 **自监督信号** 。论文设计了复杂的综合损失函数 来训练这个庞大的网络：

这里包含了四部分：

1. ：预测值与真实值之间的加权误差，距离当前时刻越近的误差权重越大。
2. 和 ：分别是精细尺度和粗粒度尺度下，两个交错分支之间的 **一致性损失** （使用 **均方误差 (MSE)** ），强制两个分支的输出趋同，防止分裂。
3. ：跨尺度一致性损失，强制精细尺度的预测结果在降采样后，与粗粒度分支的预测结果保持一致。

正是这种层层递进的约束机制，使得 **interPDN** 能够在参数量翻倍的情况下依然保持极好的泛化能力，没有陷入过拟合的泥潭。

## 四、实验设计与结果分析

为了验证模型的有效性，论文在九个主流的真实世界数据集上进行了广泛的实验，涵盖了电力、天气、交通、疾病等多个领域。实验采用了两个核心评测指标： **均方误差（MSE）** 和 **平均绝对误差（MAE）** ，数值越低代表预测越准确。

### 对比实验

论文将 **interPDN** 与当前最先进的9个模型进行了全方位的对比，包括 PatchTST、iTransformer、TimesNet 等知名模型。

![Table 1.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Table 1.

从表1的详细数据可以看出，在总共45项预测任务中， **interPDN** 在32项任务上取得了MSE的第一名，在38项任务上取得了MAE的第一名。例如，在涵盖电力变压器数据的 ETTh1 数据集上，相比于基于 Transformer 的 iTransformer 模型， **interPDN** 的 MSE 平均降低了约 35%。即使在所有的对比模型中（包括最新的 AMD 和 RAFT），本模型在绝大多数情况下都保持了显著的领先优势，证明了其架构的优越性。

### 可视化对比

为了直观展示模型在捕捉长期趋势方面的能力，论文选取了 ETTh1 和 Weather 数据集的部分测试样本进行了可视化。

![Figure 6.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 6.

在图中，我们可以清晰地看到，当预测窗口较长时，传统的 TimesNet 模型在后期往往丢失了波动的幅度，预测曲线变得平缓；而 iTransformer 有时甚至会出现趋势反向的错误。相比之下， **interPDN** 的预测曲线（通常用红色或醒目颜色表示）与真实值（黑色线条）的贴合度极高，不仅准确预测了整体的上升或下降趋势，甚至连波峰波谷的转折点都拟合得非常精准。这主要归功于粗粒度分支提供的宏观趋势约束。

另外，论文还专门展示了双分支如何修正误差。

![Figure 5.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Figure 5.

如图展示了在某个具体时间步上，分支1因为真实值落在两个锚点中间而产生了“双峰”分布，置信度较低，预测偏差较大；而分支2由于使用了交错的锚点，呈现出尖锐的单峰分布，置信度高且预测极准。融合后的结果成功修正了分支1的量化误差。

### 消融实验

为了证明模型中每个组件都不是多余的，论文进行了详细的消融实验。

![Table 2.](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Table 2.

表2的结果显示：

1. 如果只用单分支且直接预测标量（SBSP），效果最差。
2. 仅引入概率分布预测（SBPDP），效果有提升，证明概率建模有效。
3. 引入交错双分支（IBBPDP），效果显著提升，证明了交错设计解决了边界误差。
4. 引入双尺度约束（BSPDP），效果进一步提升。
5. 最终的完整模型 **interPDN** 结合了所有优势，表现最佳。 有趣的是，如果仅仅简单堆叠4个分支取平均，效果反而不如单分支，这有力地证明了论文设计的交错互补和跨尺度约束机制才是性能提升的关键，而非仅仅靠增加参数量。

## 五、论文结论与评价

### 总结

这篇论文在大规模时间序列预测领域迈出了重要一步。它通过 **interPDN** 模型，成功证明了直接对每个时间步进行 **概率密度分布** 建模比传统的直接预测数值更具优势。理论上，它巧妙地结合了概率论中的期望计算与深度学习的特征提取能力；结构上，交错式双分支和粗细双尺度设计完美解决了离散化带来的精度损失和长序列预测中的趋势丢失问题。实验结果表明，该方法在电力、交通、医疗等多个实际场景中都能提供比现有最先进技术更精准、更稳健的预测，为未来的高可靠性时序分析提供了新的技术路径。

### 优点

1. **理论视角新颖且扎实：** 跳出了“预测一个数”的思维定势，转向预测“数值的分布”，这种方法更能反映现实世界的不确定性，且计算期望值的方式在数学上保证了结果的无偏性。
2. **精巧的工程设计：** 交错双分支的设计非常聪明，用极其直观的方式（类似游标卡尺的原理）消除了离散化建模中常见的量化误差，这是一个非常具有建设性的工程创新。
3. **泛化能力强：** 实验覆盖了9个不同领域的数据集，无论是短周期还是长周期任务，模型都表现出色，说明其核心算法具有很强的普适性，不依赖于特定数据的统计特性。

### 缺点

1. **模型复杂度与资源消耗：** 为了实现交错验证和多尺度约束，模型实际上构建了四个并行的主干网络。虽然论文辩解称主干网络本身较轻量，但这无疑增加了训练时的显存占用和推理时的计算开销，可能不利于在资源受限的边缘设备上部署。
2. **支撑集的预定义依赖：** 模型的性能在很大程度上依赖于预定义的支撑集（Support Set）范围。虽然使用了统计方法划分区间，但如果未来数据的分布范围发生了剧烈的 **概念漂移（Concept Drift）** ，超出了预设的上下界，模型的预测能力可能会大打折扣，这一点在论文中讨论得相对较少。
3. **超参数敏感性：** 损失函数中引入了三个平衡系数（），实验部分显示模型对这些参数虽有一定鲁棒性，但在实际应用中，针对不同数据集寻找最优的参数组合可能需要耗费大量的时间和算力进行调优。

扫码添加小助手回复“C799”

免费获取全部论文资料

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

---

**🎁 科研人专属物资 · 免费补给**

为了帮大家理清全年的投稿时间线，我们特别制作了 **“2026科研日历鼠标垫”** 和 **“学术通勤帆布袋”** 。不做虚的，只送实用的工具。

- **选品一：全功能鼠标垫** 印有全年CCF会议时间轴，抬头就能看DDL，治愈拖延症。扫码还能直通内部学术交流群，获取大佬经验。
- **选品二：大容量帆布袋** 尺寸40\*34cm，不仅能装下电脑和论文，简约设计也让通勤更轻松。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**🚀 领取指南（请仔细阅读）**

本活动真实有效，限量500份，手慢无。

- **第一步：** 扫描下方二维码。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)
- **第二步：** 后台回复关键词 **【鼠标垫】** 获取参与链接。
- **注意事项：**
- **仅限学术地址：** 我们只发往高校、研究院或医院。非学术机构地址无法发货，感谢理解。
	- **截止时间：** 2026年2月2日 17:00。
	- **发货时间：** 2月2日首批，3月2日第二批。

新的一年，愿这份小礼物能陪伴你的Paper之路。预祝各位2026年Paper High Accept，毕业求职一路绿灯！

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

  

---

相关推荐

[2026 | 时序分割新思路：引入逻辑回归，让模型自己决定在哪里“切一刀”！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488793&idx=1&sn=ad10191a29de65032dda04e1271f7cec&scene=21#wechat_redirect)

[百度/中科大等联合发布：TimeFound-超越谷歌TimesFM的时序基础模型，零样本泛化能力惊人！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488781&idx=1&sn=97dbff8a7d97ba7e5cd940628a643084&scene=21#wechat_redirect)

[AAAI 2026 炸场！华人团队“鲨疯了”，5 篇杰出论文狂揽 3 席，港科大、同济等立大功！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488770&idx=1&sn=f7b255a467c8cdf2f083a89f0c56725c&scene=21#wechat_redirect)

[AAAI 2026 | Transformer不再被MLP吊打！EMAformer穿上“嵌入装甲”杀回来了，重夺时序预测SOTA！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488735&idx=1&sn=7b24c54ab163d6923adf00c87c8ae5a4&scene=21#wechat_redirect)

[炼狱级开局！AAAI 2026 录用率暴跌至 17% ，快手斩获 3 篇 Oral](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488713&idx=1&sn=53cdf9c110b2431a376122da25ce3dab&scene=21#wechat_redirect)

[2025时序分析风向标：左手TimeCAP语义增强，右手TIMEMIXER++全能SOTA，这波你站谁？](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488701&idx=1&sn=429e6eb7aaf5e12be077f3733cf01d47&scene=21#wechat_redirect)

[VLDB 2025 | 时间序列相关论文篇盘点（附原文源码）！](https://mp.weixin.qq.com/s?__biz=Mzk2NDIyMjI0Mg==&mid=2247488580&idx=1&sn=2a926758f17aa935e408e64206ce23fa&scene=21#wechat_redirect)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

作者提示: 个人观点，仅供参考

阅读原文

继续滑动看下一个

时序之心

向上滑动看下一个