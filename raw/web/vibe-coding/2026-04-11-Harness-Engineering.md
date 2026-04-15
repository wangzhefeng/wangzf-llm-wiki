---
author:
- '[[Datawhale]]'
created: 2026-04-11
description: null
tags:
- clippings
title: Harness Engineering在硅谷爆火，一文带你搞懂！
source_type: web
created_at: 2026-04-11
status: linked
source_url: https://mp.weixin.qq.com/s/1-bPS2omne-tncLTPm5N7A?scene=21#wechat_redirect
published_at: null
related_concepts:
  - Claude Code
  - Vibe Coding
  - 工具调用
topics:
  - vibe-coding
  - Vibe Coding
---
原创 Datawhale *2026年3月29日 22:07*

## Datawhale干货 来自：Datawhale 团队

## Harness Engineering：说白了就是给AI搭个环境

同样用 Claude 或 GPT，有人让 AI 写了几行代码就卡住了，有人却让 AI 连续工作 6 个小时，交付了一个完整的游戏。

一个极端的案例来自 OpenAI。3 名工程师，五个月，一行代码都没手写，指挥 Codex Agent 写了 100 万行代码，做出了一个真实的产品。有内测用户在用，有 bug 要修，有功能要加。整个开发流程跑通了。

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/zW6S9vt0cSicuAIJCqWjYuaIK8v3xJQdXVMuaFWUNuI9EqwR9YzHEbHzzibnpEUmVgQtNSDFiadWMHPVaoohVKToyFLgOyYm7kJSFpWRuV9KLU/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

差距在哪？2026 年初，OpenAI 和 Anthropic 几乎同时给出了答案：Harness Engineering.

这个词最近特别火。说白了就是给 AI 搭环境。有人把 AI 当聊天工具，有人把 AI 当长期合作的团队。区别就在这个“环境”上。

## Agent = Model + Harness

OpenAI 那个 100 万行代码的项目，工程师到底做了什么？

他们没写代码，但做了三件事：设计环境、设定标准、建立反馈。这三件事合起来，就是 Harness。

![Image](https://mmbiz.qpic.cn/mmbiz_jpg/zW6S9vt0cSibYPcu2UX10EZUqIOWMZVunj6lD2KlZstezics8TMKI1kFnn794EXOnUDIqVIYn9cmEibxCKeMPTaj8s94IRZaL6xMgfPH2Z9xicU/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

Harness模式类比 @odysseus0z

Harness 这个词直译是“马具”。一匹马很强壮，但没有马鞍、缰绳、马镫，你骑不了它。AI 模型也一样，它很聪明，但你得给它一套“装备”，它才能真正干活。

LangChain 工程师 Viv 给了个更技术的定义：Agent = Model + Harness。模型提供智能，Harness 让这个智能能用起来。  

![Agent = Model + Harness](https://mmbiz.qpic.cn/sz_mmbiz_jpg/zW6S9vt0cS8qJu0upS7yGtM4GgXosiaYwE5wicPglqLbNr5QvZiaz4ye5tEMv9DTckheCR2fLowmU9UlQ8u4ibVGcWaagPTDufdNj2T7PQ9FWgM/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

Harness 包括什么？系统提示词、工具、文件系统、沙箱、编排逻辑、各种检查机制。听起来很复杂，但本质就是三个问题：

AI 在哪干活？用什么干活？怎么知道干得对不对？

这三个问题解决了，AI 就能持续工作。解决不了，AI 就只能陪你聊天。

## 看 OpenAI 和 Anthropic 怎么解决

### OpenAI：给 AI 一个整理好的工作台

OpenAI 团队最开始犯了个错误。他们把所有东西都写进一个文件：系统说明、架构规范、代码风格、注意事项，全塞进 AGENTS.md。结果 AI 被信息淹没了，性能反而下降。

后来他们发现，AI 跟人一样，需要的是一个整理好的工作台。需要的时候能找到东西就行。

他们把 AGENTS.md 精简到 100 行，只做“目录”。真正的内容放在结构化的 docs/目录里：设计文档、架构文档、计划文档分开存。AI 需要什么信息，去对应文件夹找。

这个改变背后有个洞察：AI 不需要一开始就知道所有事情，它需要在正确的时机拿到正确的信息。

除了文件系统，OpenAI 还给 AI 配了工具。bash、代码执行、沙箱环境。AI 可以自己写代码测试，出错了自己看日志，自己改。

更厉害的是，他们把日志、指标、UI 界面都暴露给 AI。AI 不只是写代码，它能看到代码跑起来是什么样，能判断自己写得对不对。

![Codex使用Chrome DevTools验证工作](https://mmbiz.qpic.cn/mmbiz_jpg/zW6S9vt0cS8uJ2bJpXMy6g20aol7N5HKTx38KXoNQghDmIhTiceempUPSJBCnbPZMMHA1mNusTH7HOlN1CM8f72vAus0cCk11xRPI5BwP6kA/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

OpenAI 给 Codex 配了完整的可观测性堆栈。AI 可以查询日志、指标，看到应用运行的每个细节。

![Codex的完整可观察性堆栈](https://mmbiz.qpic.cn/mmbiz_jpg/zW6S9vt0cS8mKMp6TED8CzeOlNUenCsw0lJnUJVcm5lp5HPr0QeSmNqHhYdmrv5mRSic5Vcs8t0Ny0sAN48v1wiaEynBdcPpcXAH00hUWZE2k/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

有个细节很关键。他们花了好几个小时重写 Linter 的错误信息。目的是让 AI 能看懂“哪里错了，怎么改”。Linter 的受众从人变成了 AI。

### Anthropic：让 AI 学会自我检查

Anthropic 工程师 Prithvi 发现了另一个问题：AI 评估自己的工作完全不靠谱。

不管做得好不好，AI 给自己的评价永远是“很好”。这在设计类任务上尤其明显。一个页面是精致还是平庸，AI 自己看不出来。

他的解决方案是把生成和评估拆成两个 AI。

生成器负责做前端页面。评估器拿到一个工具，能实际操作这个页面：点按钮、填表单、截图、检查功能。然后对照四个标准打分：设计质量、原创性、工艺、功能性。

评估器给出详细反馈，生成器根据反馈改进。这样来回 5 到 15 轮。

有个案例很有意思。Prithvi 让 AI 做一个荷兰艺术博物馆的网站。第 9 轮的时候，AI 做了个干净的深色主题页面，看起来还行。到第 10 轮，AI 突然推翻了整个设计，做了个 3D 空间：用 CSS 透视渲染了一个带棋盘地板的房间，艺术品挂在墙上，用户通过“门”导航到不同展厅。

这种创意的跃升，单个 AI 很难做到。

![图片](https://mmbiz.qpic.cn/mmbiz_png/zW6S9vt0cS8eyWnY0MpLqCbSQb8IicFD1Gsmjcw0LlJBkxaLdx7Tvibq3Vc3QnB1pYXo8rFeIgja15HPjZzrsN1ycBZoc2nQRXt29CQnQU4Zs/640?wx_fmt=png&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

对比数据很直观。单 AI 跑 20 分钟花 9 美元，做出来的东西看着行，实际用不了。完整 Harness 跑 6 小时花 200 美元，交付了一个真正能玩的游戏，有精灵动画、AI 集成、导出功能。

OpenAI 的方法是另一个角度。他们定义了严格的架构规则：代码只能按 Types → Config → Repo → Service → Runtime → UI 这个方向依赖。违反规则的代码会被自动拦截。

有了这些约束，AI 写的代码就不会乱。速度不会下降，架构不会漂移。

### 还有个容易被忽略的问题：上下文窗口

AI 不是记忆力无限的。研究表明，即使模型理论上支持 100 万 token 的上下文，性能衰减在 25.6 万 token 左右就开始出现。

OpenAI 的做法是让 AI 把重要的东西写下来。不是把所有信息都塞在上下文里，而是存到文件系统。需要的时候再读取。

他们还有个定期运行的“doc-gardening”Agent，专门扫描那些过时的文档，发起修复。这样知识库始终是最新的。

普通人能用上么：这个转变适用于所有的 AI使用场景。

听起来都是大厂的实践，普通人能用上吗？

能。核心思想完全可以迁移。

OpenAI 报告里有个关键发现：工程师的角色从“写代码”变成“设计环境、设定标准、建立反馈”。这个转变适用于所有 AI 使用场景。

就像你不会手把手教一个新员工每个细节，而是给他工作手册、工具权限、验收标准。AI 也是一样。

### 整理你的“工作台”

> 厨师的工作台调料按类摆放，刀具各归其位，食材分区存储。AI 也需要这样的工作台。具体怎么做？

建立清晰的文件夹结构，统一命名规范。把常用的参考资料、模板、规范放在固定位置。让 AI 知道找背景资料去哪个文件夹，找模板去哪个文件夹。

OpenAI 的教训很清楚：不要把所有信息塞进一个文档。分层组织，让 AI 在需要时找到对应信息。

### 设定“验收单”

> 装修验收不是问工人“你觉得刷得好吗”，而是拿尺子量平整度、看色差、检查边角。具体怎么做？

明确什么叫“完成”。不是“写一篇文章”，而是“3000 字、3 个案例、至少 2 个数据支撑”。

Anthropic 用的四个维度——质量、原创性、工艺、功能——可以迁移到任何创作任务。设定可检查的标准，让 AI 对照标准自查。

Anthropic 的发现很明确：AI 自评不可靠，但如果给它明确的评估标准，准确度会大幅提升。

### 建立“返工机制”

> GPS 导航不是出发前规划好就不管了，而是实时监测位置，偏离了就重新规划路线。具体怎么做？

让 AI 能“看到”自己的输出结果。比如生成图片后，让它描述图片内容，检查是否符合要求。

设定检查点。不是一口气完成所有任务，而是分阶段验收。当 AI 出错时，不是重新开始，而是告诉它“哪里不对，怎么改”。

Mitchell Hashimoto 给 Harness Engineering 下的定义很简洁：每当你发现 Agent 犯了一个错误，你就花时间设计一个解决方案，使 Agent 永远不再犯同样的错误。

### 从哪里开始

不要试图一次性搭建完美的 Harness。选一个你每周都要重复做的任务。

三步走：

- 第一周，整理文件结构和规范，让 AI 知道去哪找东西。
- 第二周，设定验收标准，让 AI 知道什么叫“做完”。
- 第三周，建立反馈机制，让 AI 能自我检查和修正。

关键是每次 AI 出错，不是责怪它，而是问“我的环境里缺了什么”。

## 写在最后：现在就开始实践

Harness Engineering 的本质是把你的工作方法、判断标准变成 AI 能理解和执行的环境。

模型包含智能，Harness 让这个智能变得有用。

OpenAI 报告的结论很明确：我们当前最棘手的挑战集中在设计环境、反馈回路和控制系统方面。

这不是遥远的未来，而是现在就能开始实践的方向。

参考资料：

1.https://openai.com/index/harness-engineering/

2.https://www.anthropic.com/engineering/harness-design-long-running-apps

3.https://x.com/Vtrivedy10/status/2031408954517971368

**一起“ **点** **赞”** **三连** ↓**

继续滑动看下一个

Datawhale

向上滑动看下一个