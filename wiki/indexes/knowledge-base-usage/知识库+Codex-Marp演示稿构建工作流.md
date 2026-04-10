---
created_at: 2026-04-05
topics:
  - 知识库维护
  - Marp
  - 演示稿
related_concepts:
  - 知识库+Codex-Marp汇报型演示稿工作流
  - 知识库+Codex-Marp研究型演示稿工作流
  - 知识库+Codex-时间序列模型开发工作流
status: linked
---

# 知识库 + Codex Marp 演示稿构建工作流

这页只负责回答一个问题：**你现在要做的 slide，属于哪一种。**

真正的操作细节拆到两页：

- [[知识库+Codex-Marp汇报型演示稿工作流]]
- [[知识库+Codex-Marp研究型演示稿工作流]]

## 先做哪种，不要混着写

### 1. 汇报型演示稿

适合这些场景：

- 5 到 10 分钟口头汇报
- 给同事、老板、合作方快速说明
- 希望结论先行，信息密度受控

这类 slide 的特点：

- 页数少，通常 6 到 8 页
- 每页一个判断
- 少解释过程，多强调结论、风险、动作

入口页：

- [[知识库+Codex-Marp汇报型演示稿工作流]]

### 2. 研究型演示稿

适合这些场景：

- 自己回顾一个专题
- 需要保留方法链路、对照关系和推理过程
- 不是为了正式汇报，而是为了后续继续研究

这类 slide 的特点：

- 页数可以更多，通常 8 到 15 页
- 允许保留方法分层、来源映射和待研究问题
- 结论之外，还保留“为什么这样判断”

入口页：

- [[知识库+Codex-Marp研究型演示稿工作流]]

## 两类 slide 共用的底层分工

- `outputs/answers/`
  提供内容底稿。
- `outputs/figures/`
  提供本地图片、示意图、流程图。
- `outputs/slides/`
  存放 Marp Markdown 与导出文件。

推荐保持一组对应关系：

- 一篇答案页
- 一组本地图片目录
- 一份演示稿 Markdown

例如：

- `outputs/answers/2026-04-05-scikit-learn-机器学习时间序列预测实践解读.md`
- `outputs/figures/2026-04-05-scikit-learn-机器学习时间序列预测实践解读/`
- `outputs/slides/2026-04-05-scikit-learn-机器学习时间序列预测实践解读-演示稿.md`

## 共用的 Marp 约束

最小 front matter：

```yaml
---
marp: true
theme: default
paginate: true
size: 16:9
---
```

共用实践：

- 演示稿优先从 `outputs/answers/` 压缩，不从零编
- 图片优先本地化，不依赖外链
- 导出 PDF 时使用 `--allow-local-files`
- 需要浏览器导出时，优先显式指定 `--browser chrome`

命令示例：

```bash
brew install marp-cli
marp --version
```

```bash
marp --pdf --allow-local-files --browser chrome \
  outputs/slides/xxx-演示稿.md \
  -o outputs/slides/xxx-演示稿.pdf
```

## 怎么选

如果你现在更关心：

- “别人能不能 5 分钟听懂”
  走 [[知识库+Codex-Marp汇报型演示稿工作流]]
- “我之后还能不能拿它继续研究”
  走 [[知识库+Codex-Marp研究型演示稿工作流]]

如果拿不准，默认先做 **汇报型**，因为它更能暴露你的核心论点是否真的清楚。

## 已跑通的样例

- [[2026-04-05-scikit-learn-机器学习时间序列预测实践解读]]
- [[2026-04-05-scikit-learn-机器学习时间序列预测实践解读-演示稿]]

这个样例当前更接近“汇报型”，后续如果要扩展更多方法链路和来源映射，可以按研究型再派生一版。

如果需要回到 shared 工作台层重新选任务入口，先看：[[知识库任务与输出工作流索引]]
