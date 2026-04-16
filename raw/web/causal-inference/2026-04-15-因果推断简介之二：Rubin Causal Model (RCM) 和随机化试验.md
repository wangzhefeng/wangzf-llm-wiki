---
source_type: web
source: "https://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144668&idx=1&sn=570baaf9b7e2dff3fc8c8eeee16df39d&chksm=be86658f89f1ec99a118be4c5bb687789500a60069a96612f84cde36d5b281173fc35e49bd72&scene=178&cur_album_id=2515660787328253953&search_click_id=#rd"
title: "因果推断简介之二：Rubin Causal Model (RCM) 和随机化试验"
author:
  - "[[丁鹏]]"
published_at:
created_at: 2026-04-15
topics:
  - causal-inference
tags:
  - "clippings"
related_concepts:
status: "inbox"
---
原创 丁鹏 *2019年12月11日 19:33*

编辑部于2019年10月在微信端开启《朝花夕拾》栏目，目的是推送2013年（含）之前主站发表的优秀文章，微信端与主站的同步始于2013年年初，然而初期用户量有限，故优质文章可能被埋没。

![[Image 5.webp|图片]]

因果推断用的最多的模型是 Rubin Causal Model (RCM; Rubin 1978) 和 Causal Diagram (Pearl 1995)。Pearl (2000) 中介绍了这两个模型的等价性，但是就应用来看，RCM 更加精确，而 Causal Diagram 更加直观，后者深受计算机专家们的推崇。这部分主要讲 RCM。

设表示个体 i接受处理与否，处理取1，对照取0 (这部分的处理变量都讨论二值的，多值的可以做相应的推广)；表示个体 i的结果变量。另外记 表示个体 i接受处理或者对照的潜在结果 (potential outcome)，那么 表示个体 i 接受治疗的个体因果作用。不幸的是，每个个体要么接受处理，要么接受对照， 中必然缺失一半，个体的因果作用是不可识别的。观测的结果是 。但是，在Z做随机化的前提下，我们可以识别总体的平均因果作用 (Average Causal Effect; ACE):

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这是因为

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

最后一个等式表明 ![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 可以由观测的数据估计出来。其中第一个等式用到了期望算子的线性性(非线性的算子导出的因果度量很难被识别！)；第二个式子用到了随机化，即

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 其中，表示独立性。由此可见，随机化试验对于平均因果作用的识别起着至关重要的作用。

当Y是二值的时候，平均因果作用是流行病学中常用的“风险差”（risk difference; RD）：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

当然，流行病学还常用“风险比”（risk ratio; RR）：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

和“优势比”（odds ratio; OR）：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

上面的记号都带着“C”，是为了强调“causal”。细心的读者会发现，定义 CRR 和 COR 的出发点和 ACE 不太一样。ACE 是通过对个体因果作用求期望得到的，但是 CRR 和 COR 是直接在总体上定义的。这点微妙的区别还引起了不少人的研究兴趣。比如，经济学中的某些问题，受到经济理论的启示，处理的作用可能是非常数的，仅仅研究平均因果作用不能满足实际问题的需要。这时候，计量经济学家提出了“分位数处理作用”（quantile treatment effect: QTE）：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

在随机化下，这个量也是可以识别的。但是，其实这个量并不能回答处理作用异质性（heterogenous treatment effects）的问题，因为处理作用非常数，最好用如下的量刻画：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

这个量刻画的是处理作用的分布。不幸的是，估计 需要非常强的假定，通常不具有可行性。

作为结束，留下如下的问题：

1. “可识别性”（identifiability）在统计中是怎么定义的？
2. 医学研究者通常认为，随机对照试验（randomized controlled experiment）是研究处理有效性的黄金标准，原因是什么呢？随机化试验为什么能够消除 Yule-Simpson 悖论？
3. ![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) 在随机化下是可识别的。另外一个和它“对偶”的量是 Ju and Geng (2010) 提出的分布因果作用（distributional causal effect: DCE）： ![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E) ，在随机化下也可以识别。
4. 即使完全随机化， 也不可识别。也就是说，经济学家提出的具有“经济学意义”的量，很难用观测数据来估计。这种现象在实际中常常发生：关心实际问题的人向统计学家索取的太多，而他们提供的数据又很有限。

关于 RCM 的版权，需要做一些说明。目前可以看到的文献，最早的是 Jerzy Neyman 于 1923 年用波兰语写的博士论文，第一个在试验设计中提出了“潜在结果”（potential outcome）的概念。后来 Donald Rubin 在观察性研究中重新（独立地）提出了这个概念，并进行了广泛的研究。Donald Rubin 早期的文章并没有引用 Jerzy Neyman 的文章，Jerzy Neyman 的文章也不为人所知。一直到 1990 年，D. M. Dabrowska 和 T. P. Speed 将 Jerzy Neyman 的文章翻译成英文发表在 Statistical Science 上，大家才知道 Jerzy Neyman 早期的重要贡献。今天的文献中，有人称 Neyman-Rubin Model，其实就是潜在结果模型。计量经济学家，如 James Heckman 称，经济学中的 Roy Model 是潜在结果模型的更早提出者。在 Donald Rubin 2004 年的 Fisher Lecture 中，他非常不满地批评计量经济学家，因为 Roy 最早的论文中，全文没有一个数学符号，确实没有明确的提出这个模型。详情请见，Donald Rubin 的 Fisher Lecture，发表在 2005 年的 Journal of the American Statistical Association 上。研究 Causal Diagram 的学者，大多比较认可 Donald Rubin 的贡献。但是 Donald Rubin 却是 Causal Diagram 的坚定反对者，他认为 Causal Diagram 具有误导性，且没有他的模型清楚。他与James Heckman （诺贝尔经济学奖）， Judea Pearl （图灵奖） 和 James Robins 之间的激烈争论，成为了广为流传的趣闻。

参考文献：

1. Neyman, J. (1923) On the application of probability theory to agricultural experiments. Essay on principles. Section 9. reprint in Statistical Science. 5, 465-472.
2. Pearl, J. (1995) Causal diagrams for empirical research. Biometrika, 82, 669-688.
3. Pearl, J. (2000) Causality: models, reasoning, and inference. Cambridge University Press。
4. Rubin, D.B. (1978) Bayesian inference for causal effects: The role of randomization. The Annals of Statistics, 6, 34-58.

关于作者

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

丁鹏，2004-2011 年在北京大学概率统计系学习，获得学士和硕士学位；2011-2015 年在哈佛大学统计系学习，获得博士学位；2015 年在哈佛大学流行病学系做博士后；2016 年加入伯克利统计系任教。研究方向是因果推断。

***往期回顾***

[*因果推断之一：* *从Yule-Simpson's Paradoc讲起*](https://mp.weixin.qq.com/s?__biz=MjM5NDQ3NTkwMA==&mid=2650144615&idx=1&sn=ecf6b8e67af3b7cf615c867e187b797d&scene=21#wechat_redirect)

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