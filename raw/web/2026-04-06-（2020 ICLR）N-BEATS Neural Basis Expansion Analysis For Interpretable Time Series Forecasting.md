---
source_type: web
title: "（2020 ICLR）N-BEATS: Neural Basis Expansion Analysis For Interpretable Time Series Forecasting"
author:
  - 
  - "[[的泼墨佛给克呢​​github.com/ddz16/TSFpaper]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://zhuanlan.zhihu.com/p/572850227"
published: 
created: 2026-04-06
description: "论文链接：这篇文章中了2020 ICLR https://arxiv.org/pdf/1905.10437.pdfKey PointsMain Idea在时间序列预测方面，很多经典方法如ARIMA、ETS等都还占很重要的地位。本文希望用纯DL的方法来构建一个尽可能简单有效…"
tags:
  - 
  - "clippings"
---

目录

收起

论文链接：

Key Points

Main Idea

Doubly Residual Stacking

Interpretablity

## 论文链接：

这篇文章中了2020 ICLR

## Key Points

### Main Idea

在时间序列预测方面，很多经典方法如 [ARIMA](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=ARIMA&zhida_source=entity) 、 [ETS](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=ETS&zhida_source=entity) 等都还占很重要的地位。本文希望用纯 [DL](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=DL&zhida_source=entity) 的方法来构建一个尽可能简单有效，但同时又有一定可解释性的方法。

先说定义，本文集中于解决 **单变量** （一维序列，输入和输出都是一维的）、 **多步** （一次输出多个未来时刻的预测值，而不是自回归）、 **点预测** （输出是一个预测值而不是一个预测范围）的问题。预测长度为H，过去输入的长度为nH（n是可以自己设置的常数）。

然后再说模型，模型由多个stack组成，然后每个stack又由多个block组成，如下图。下面详细介绍了两个模型架构的关键点和创新点。

![[assets/attachments/timeseries/v2-52e15dc5f23f5d6bf7591067342f029c_1440w.jpg]]

### Doubly Residual Stacking

每个block有两个输出，一个是backcast、一个是forecast，可以把它们理解为，分别是过去的信息和未来的信息。未来的信息可以理解，直接加在一起最终得到预测结果，那过去的信息怎么理解呢？实际上，这就是这篇文章用 [残差连接](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=%E6%AE%8B%E5%B7%AE%E8%BF%9E%E6%8E%A5&zhida_source=entity) 的一个技巧，我觉得有点像 [boosting](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=boosting&zhida_source=entity) 的思想。可以看模型结构Stack那一块（模型图里中间那一块），经过每个block后， **下一个block的输入** 就会是 **该block的输入** 再减去 **该block的backcast输出** 。相当于是，stack input中可能有很多不同杂糅的信息，第一个block用stack input中的一部分来预测，然后就可以把该部分（backcast）减掉，将剩下的再输入到第二个block，继续上述操作。这样就相当于，每个block只负责stack input中一部分的预测。同样利用boosting的思想是 [回归提升树](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=%E5%9B%9E%E5%BD%92%E6%8F%90%E5%8D%87%E6%A0%91&zhida_source=entity) ，上个树预测一个值，下一个树预测它离GT还差多少，预测这个残差，然后下下个树再预测剩下的残差。NBeats也利用了这种残差，即将所有block的输出加一起是最终的输出，此外，NBeats还利用了另一种残差，就是是减输入，一开始很复杂的stack input，经过一个block减去backcast，下一个block的输入就更简单，相当于逐渐把输入简化。所以，论文中提到是双残差结构（DOUBLY RESIDUAL STACKING）。

### Interpretablity

每个block中，输出backcast和forecast并不是直接输出Backcast和Forecast，而是输出系数 和 ，然后再将系数输入到函数 和中（函数可以是设定好的，也可以是可学习的） 。为什么要这样做呢，为什么不直接FC输出Backcast和Forecast呢，而非要先输出系数再将系数输入到函数中得到Backcast和Forecast呢？ **因为这样可以有一些可解释性** 。 **基（Basis）** 这个概念在机器学习中很经典，所以在很多领域的DL的方法，都会用到它的思想，有些用深度字典（Dictionary）的方法也可以将其理解为基。你可以把它理解为，将基根据系数来加权组合，就可以从系数中了解到，哪个基对当前输出更重要，也可以自己设计基。本文就是这样，预测系数 和 ，然后函数 和设计为根据系数来对基进行加权。在这里，基实际上就是一些序列，比如可以将一个正弦曲线设置为基，那这个基可以表示一些季节性的分量，再比如可以将一个线性直线或者二次曲线（多项式）设置为基，这个基可以表示一些趋势性的分量。把基加权线性相加，即可得到预测Forecast或者是Backcast。

这个基如果设定为多项式基，就对应着 **趋势：**

![[assets/attachments/timeseries/v2-5d9058c4916a0f8b0d27a31589e7cc6b_1440w.png]]

如果设定为傅里叶基，就对应着 **季节：**

![[assets/attachments/timeseries/v2-b64596010ab050fb59e41ade240fada7_1440w.png]]

如果设定为可学习的，就对应着论文中的 **Generic architecture：**

![[assets/attachments/timeseries/v2-363942d6568a32f4da9c630df9bd2a3e_1440w.png]]

其中，矩阵V是可学习的，每一列代表一个基，每一行代表一个离散的时间索引。由于没有对V施加任何约束，因此学习到的基没有固定的结构，这导致了预测的不可解释性。

如果模型中都用Generic的stack，则是 [N-BEATS](https://zhida.zhihu.com/search?content_id=215433217&content_type=Article&match_order=1&q=N-BEATS&zhida_source=entity) -G模型；如果模型中季节和趋势的stack一起用，那就是一些stack集中预测趋势，一些stack集中预测季节，就是N-BEATS-I，即可解释的NBeats。

**NBEATS模型也有一个改进版本，集成了对外生协变量的处理，可以看我另一篇文章：**

## Comments

很Solid的一篇工作，把DL和结合起来，模型结构简单有效，里面使用残差连接的这种思路（每一块负责一小部分）在时序预测里之后很多工作也借鉴过。整个模型也有一定的可解释性，用着实际效果也非常好。但实际用好像大部分都还是用N-BEATS-G而不是N-BEATS-I。

编辑于 2023-02-09 13:19・北京[时间序列预测](https://www.zhihu.com/topic/25716601)[深度学习（Deep Learning）](https://www.zhihu.com/topic/19813032)[时间序列分析](https://www.zhihu.com/topic/19712111)[数字孪生不用游戏引擎可以吗？](https://www.shanhaibi.com/?utm=v2_ad_zhihu&spu=biz%3D0%26ci%3D3673767%26si%3D0fd00e0c-47e6-466d-8c75-c862da5af141%26ts%3D1775469780%26zid%3D1629)

[

推荐一款纯自研的数字孪生引擎，是我目前能找到的产品化做的相当好的一款产品，不仅视觉效果可以媲美游戏引擎的...

](https://www.shanhaibi.com/?utm=v2_ad_zhihu&spu=biz%3D0%26ci%3D3673767%26si%3D0fd00e0c-47e6-466d-8c75-c862da5af141%26ts%3D1775469780%26zid%3D1629)