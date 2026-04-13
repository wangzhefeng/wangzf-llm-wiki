---
source_type: web
title: "GenAI/GPT/AIGC/LLM/NLP/ChatGPT 学习 - 飞书云文档"
author: 
created_at: 2026-04-06
status: inbox
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://gofurther.feishu.cn/docx/Enofdl25BotoVrxth8ec4rNBn5c"
published_at: null
related_concepts: []
topics:
  - llm-theory
  - 大语言模型理论
---

- [🧭GenAI/GPT/AIGC/LLM/NLP/ChatGPT 学习](#Enofdl25BotoVrxth8ec4rNBn5c)
- [1\. 资料汇总](#R8OqdCoKcoWMawxyk3OcD0wZnjh)
- [1.1 GPT & LLM 总览（Transformer）](#DquydaIoYo6caUxO0mFc2Dn8n5V)
- [1.1.1 论文](#EKwGdqKewoCSGoxlECNckIQLnyO)
- [1.1.2 报告](#UO6WdosKSoGis8xCUeacJ3Dknng)
- [1.2 AIGC（LDM & Diffusion & NeRF）总览](#PAmmdgyMcoACE4xY7cPcIsQ4nAb)
- [1.2.1 论文](#SOSIdoYEKoeOkcxszsfcECOHn3e)
- [1.2.2 资料](#UGWud222aoUYwmx6xRmcx4x8nnc)
- [1.3 公司和项目](#RgUcdweqWoYSU4xisblcvAcEnNd)
- [2\. GPT & LLM 路线](#Gwa6dk8suomGYex6S0ecjo5Ynz8)
- [2.1 GPT 提供的基础设施](#PNLJdeQZqoX88gxjy3ec5F4mnLh)
- [2.2 GPT 原理](#LWTwdrVzWoVSixx2F7fcc8TXnse)
- [2.2.1 组成部分](#MJnTd1JBbowzWnx1TQAcn4DCnle)
- [2.2.2 GPT-4 原理](#LNbkdGQYMouyvdxBfyZcIvZSnUd)
- [2.2.2.1 总结](#MYSmdFlgloOSv5xDQT4c4I4rnFc)
- [2.2.2.2 消息源](#UY1cdAwfSoaQ3IxmkfGccu5CnTg)
- [2.3 ⭐️ 未来怎么发展](#KCxUdvovqo8CUZxHvYLclZQUnXc)
- [3\. 真实落地效果 | 可落地的场景](#R6gAde4SiouaOux4gFGcssnOnEd)
- [3.1 ⭐️ 大类分类](#AgOCd6q0Ao8cA2x8NSDcSGG1nme)
- [3.2 GPT/AIGC+ 的产品/服务列表](#TAg8daqgQomYOQxuP1GcWjFwn2F)
- [3.2.1 Miro AI+ 支持表](#H0ScdSysmoGq0UxcvS2ccFcjnFh)
- [3.2.2 Gamma App 支持表](#DUYyd8eY8oiYOaxsZ3jcCUu8nih)
- [3.2.2.1 官网的展示视频：](#YCqGdOkA8oMqEMxkpm7cbzaznqc)
- [3.2.2.2 对外开放的功能](#FI0kdAQQ4oK0Gsx27WlcqgGAnvc)
- [3.2.2.3 Credit 增长邀请策略](#YgOsd2UcAoYW0ixmoyUcAeSUnDg)
- [3.3 AIGC](#TYmedsw2YoSEMqxCe9EcDBc4nBd)
- [3.3.1 Midjourney](#UEcGdWGyIoMEagxKGR6ckmcsnId)
- [3.3.1.1 相关数据](#EiQ8dUIW4ouA4exY9KNcf3cMnqg)
- [3.3.1.2 迭代方向](#BQoudSUuKowQKixKqjqcQqfGnLd)
- [3.3.1.3 V5 效果](#EckGdsQkMo42MKxCAUecrGnwnPe)
- [3.3.2 图片模态](#DrNldtgHvo27Mtx5QPhcFglcnxd)
- [3.3.2.1 设计常用视图 #领域知识](#THu9dIEQsouNrnxcS4Ic1imZnNd)
- [3.3.3 视频模态](#RPLOdLMqVoUFbtxQEcdcQak6nkb)
- [3.3.3.1 Runway Gen-2 模型的功能](#YmTbdhYzaoRCOBxFLU9cn7tNnFb)
- [4\. ⭐️ 点子/商业化](#DimidcUQQoMA0MxG0kwcoHYanZg)
- [5\. 如何让 GPT 发挥更强的能力](#NW8Kdy4OMoI0Iyxg9ZFcZypon3d)
- [5.1 GPT-3 应对不同任务的收敛方式](#C64Ydmwi6o6u8IxaGsHc3UoKnje)
- [5.2 如何给 GPT 添加更多上下文 | 常用训练方式](#McEudY42CooW0qxGgBncSEVunil)
- [5.2.1 综述](#XD3ad4bgEoqinjx01p8cUJrfnBe)
- [5.2.2 常见思路](#UMFYdQIDIo535sxLr3Jcz3A6nrf)
- [5.2.2.1 Prompt Engineering/Few-shot learning](#M08Kdaw0Io8O2axCqd7cLiJmn8w)
- [5.2.2.2 Fine-tuning](#IWQWdsko2oSQ2wxgDJFct1fKnTh)
- [5.2.2.3 RAG - Retrival Augmented Generation/检索增强生成](#HTD2d5JSNoBQzgxPGiMcbLr0nYc)
- [5.2.3 补充：结合 Embedding 加长上下文](#ZwQWduAE4oMAu6x47zxc51yknxY)
- [6\. LLM 大语言的模型的 Evaluation/评估 & Benchmark/基准](#BcSMdSKeGoYCiWxiiYXc6IxZn9y)
- [6.1 评估框架](#F0Med8M8uoL7Vnx5epvc5dSDnkc)
- [6.1.1 Chain-of-Thought Hub](#SoMWdUOFUoLXU3xIKqGcKpJjnAd)
- [6.2 评估数据集/方法](#J2AydVpskoFboJxfWg0cD3m5n7b)
- [6.3 GPT3.5 和 GPT4 在同样问题序列下的不同表现](#AioEd0wyco82iCxyPAAcDlAunZa)
- [6.4 GPT-4 解决不了但人可以的问题](#C82qdugCOoawYYx8jsfcRV5Cnk9)
- [6.5 ⭐️ 不同模型明确场景 Benchmark](#T5Pjdf7Z9ojnEAx51wScOLaKnSb)
- [6.5.1 目的和场景：对『VC维』『乔姆斯基语言层级』等公域信息少的专业概念做解读](#RalBdQ5Tnol0ugxkkLVchL5Qnfd)
- [6.5.1.1 具体对比表](#NYTPdUJ6lo6fwbxQanQc9040nIe)
- [6.5.2 目的和场景：调研『视觉频率极限』](#XwcbdryZZoPka7xLDYdcqhMwnUf)
- [6.5.2.1 具体对比表](#U6aOdP4UvoHxwMxc32bcbVC2nNh)
- [6.5.3 目的和场景：横向对比编程语言的内存管理方式（功能分析）](#OFUjdLWS4oesTBxZJbscAYWknLd)
- [6.5.3.1 具体对比表](#XDwKd4kjRoN0MuxoDm2c0V5PnSf)
- [7\. Prompt 工程](#LG4kd4oSkoUOmoxuMkscUluPn4f)
- [7.1 相关资料](#PeoEdq2mQoyqQaxcpnjcDjPpnTf)
- [7.2 工程化使用 GPT | Prompt 高阶使用](#BeEEdUw4so6YeCx2OmNctntnnqq)
- [7.3 方法论](#WMEedMqwwoES44xC2nvcgeSAnFb)
- [7.3.1 结构化 Prompt](#Nys3dlYOYo18TzxIxgbcQD3unb3)
- [7.3.2 从 Langchain 内学习 Prompt 书写](#BrfPddgVmo9HWbxssiNcbetinTF)
- [7.3.3 用“BORE”分析法设计 ChatGPT Prompt](#GWkkd6C44o6mgqxstDccemLunnh)
- [7.3.4 10 个小技巧](#QuCQdC4QyoGos6xkzoCcfcpjnGd)
- [7.3.5 不使用太长的对话序列](#JMI1dPuJFomPujxJmBKcG079nPd)
- [8\. 成本/花多少钱&时间](#CW6MdWcEGoK8cOxKM7qc7hyanhb)
- [8.1 模型训练和运行推理](#H6OgdSwiIo0OO2x0u8wcRsRbnKc)
- [8.1.1 服务器花费拆解](#Q4OodiA0moC6CoxoFKGcwDqInJf)
- [8.1.2 计算卡参数](#Q0bad9tMVonoibxtHfAcLa4onGe)
- [8.2 调用 OpenAI API](#HEs8dCQEsowUqcx1YwFcxugVnyY)
- [8.3 实例 / Foundry](#SyA8dOiOmo2uuoxm2mPcGFJpngc)
- [9\. 领域知识](#Oyu8dyUMGoukIYx0ccWc0qBwnWd)
- [9.1 BERT 预训练模型的任务类型](#YSYMdCESuokyoIx484ucTdpqnRe)
- [9.2 GPT-3 和 BERT 的比较](#BAggdAcUSoGIuYxgTpIcUaLInSd)
- [10\. OpenAI API Playground 详解](#TGmydwWCOoUW2sxElG4cQi8mnVd)
- [10.1 概述和模式](#Eq6QdekmsoaMwOx6BV7cVKognZd)
- [10.2 Mode = Complete 的 Preset 🚧](#RgGcduMEioOwEYxcXI1cUdkbnTg)
- [10.3 可调参数](#NK2GdWG2soSQQMxcjemc9I0cnFf)
- [11\. 碎片事实](#TywWdoM0UoGGUUxrd7GcmC2ynlt)
- [12\. 灵感收集](#QSSqdgKg6oM2YKxqs18cxEZnnkf)
- [13\. 问题列表](#MKa2dsCkAoAagyxSOfQcBguknNh)

💡

New SaaS: Semantic as a Service / 语义即服务 | This is the iPhone moment of AI —— Jensen Huang（Stakeholder | Nvidia）

<table><colgroup><col width="83"> <col width="113"> <col width="170"> <col width="647"></colgroup><tbody><tr><td rowspan="1" colspan="1"><p>公司</p></td><td rowspan="1" colspan="1"><p>Apple</p></td><td rowspan="1" colspan="1"><p>OpenAI</p></td><td rowspan="4" colspan="1"><p>可怕的是，当年做个 App Store 上的 App，门槛高，得会编程。未来，只需会清晰的描述你的需求。所以描述问题和需求的能力暂时不过时。</p><p>5.4 亿年前，寒武纪生命形态大爆发，只是海水的氧气水平略微增加到某个阈值以上，涌现在一瞬之间（和 <a href="https://www.mubucm.com/doc/NRsKWQsYB">复杂科学</a> 里涌现不是一个含义）</p><p><a href="https://gofurther.feishu.cn/docx/Enofdl25BotoVrxth8ec4rNBn5c#KCxUdvovqo8CUZxHvYLclZQUnXc">体验问题</a> 拆解：体验(可控|延迟) 商业(成本) 扩展(内存|行动|多模态|自动代理)</p>82%<div><p></p><p>附件不支持打印</p><img src="https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/EwhibfFDboai20xmQs8cnWQMnXd/?fallback_source=1&height=1280&mount_node_token=V65Vdd4NGoomd5xLRkYcJ0mynzd&mount_point=docx_image&policy=equal&width=1280" width="1300" height="721"><p></p><p></p><p>附件不支持打印</p><img src="https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/R2S7b595goMAY7x5BYAciqtKnxg/?fallback_source=1&height=1280&mount_node_token=S8iidY5etoARTrxbGCXcrxONnub&mount_point=docx_image&policy=equal&width=1280" width="2388" height="1316"><p></p>18%</div></td></tr><tr><td rowspan="1" colspan="1"><p>产品-萌芽</p></td><td rowspan="1" colspan="1"><p>iPhone 1-2007</p></td><td rowspan="1" colspan="1"><p>GPT-4(<a href="https://mathstodon.xyz/@tao/110534826121112802">满血版</a>)-2023</p></td></tr><tr><td rowspan="1" colspan="1"><p>产品-流行</p></td><td rowspan="1" colspan="1"><p>iPhone 4-2012</p></td><td rowspan="1" colspan="1"><p>解决体验问题的 X-202?</p></td></tr><tr><td rowspan="1" colspan="1"><p>操作系统</p></td><td rowspan="1" colspan="1"><p>iOS</p></td><td rowspan="1" colspan="1"><p>ChatGPT</p></td></tr><tr><td rowspan="1" colspan="1"><p>平台</p></td><td rowspan="1" colspan="1"><p>App Store</p></td><td rowspan="1" colspan="1"><p>Plugin</p></td><td rowspan="1" colspan="1"><p>截止 2023年6月1日，根据对 Plugin 商店的观察和 <a href="https://mp.weixin.qq.com/s/Qir5v3uJFT75wydPGHAlTQ">最新访谈</a> （原文被删了，但 <a href="https://web.archive.org/web/20230531203946/https://humanloop.com/blog/openai-plans">有人存档</a> ，真实性自查），受限于算力、体验（例如延迟和准确性），平台化/Plugin PMF 不成立。需提高上下文窗口、响应速度、交互准确度、降低操作路径冗余。</p></td></tr></tbody></table>

这篇是个人学习零碎笔记（CC BY-NC 协议），由于飞书文档的编辑限制和卡顿暂停更新，适合作为了解大模型第一性原理的硬核入门，建议从业者至少标红的论文烂熟于心（ [我](https://charlesliuyx.github.io/) 是 One2X Cofounder，前 [https://dora.run](https://dora.run/) 产品合伙人，前 [幕布](https://mubu.com/) 产品负责，创立 [🔄『信息流转学』](https://gofurther.feishu.cn/docx/OqQ2dgVUzoZeB3xuXM0cZjnbnqc) ）但希望有更多人了解 GPT 背后的原理且认识到它的变革性，如果能帮到大家是我的荣幸，与众君共勉 🙌

左侧目录中有 ⭐️ 的章节可考虑先读

1.

资料汇总

已经阅读并觉得靠谱的参考资料（ 强烈推荐 推荐 普通推荐/总览/数据库）

1.1

GPT & LLM 总览（Transformer）

评论（15）

跳转至首条评论

用户86442023年3月28日

寓意无敌

用户6479,用户4877,

+1 人

用户61762023年4月24日

针对OpenAI，这部分的操作系统是不是应该是GPT-4，产品是ChatGPT，是不是写反了？

用户6316

用户49022023年8月17日 （编辑过）

这个类比本身其实不是很准确，但 iPhone 是一个破圈时刻（体验达标，或者用PM说法，留存率达标）。个人观点：满血版 GPT-4 才是真正首个破圈时刻。

且在架构上满足 Semantic as a Service 的逻辑，ChatGPT 是一个服务名称，结合 Plugin 的设计，更像系统。

用户6479

用户64502024年12月5日

笑死🤣

用户71782024年12月5日

@飞书运营团队 FYI

用户25582023年8月10日

除了NB没有别的词可以形容

0 字

- 帮助中心

- 效率指南