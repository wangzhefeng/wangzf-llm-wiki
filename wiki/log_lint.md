---
created_at: 2026-04-17
topics:
  - 知识库维护
  - 健康检查
  - llm-wiki
related_concepts:
  - 知识库维护检查索引
  - 知识库健康检查清单
  - 输出回流
status: linked
---

# LLM Wiki 审查报告

> 本文件是最新 lint / health 审查主报告唯一出口。过程日志统一追加到 [[log]]。

## 本次检查结果（2026-04-17）

本轮按“全主题审计、限定原始资料重编译、统一流程文档收口”的口径复验，正式输入范围收敛为：

- `raw/web/**`
- `raw/repos/repo-*.md`
- `raw/notes/**`

`raw/repos/**` 下镜像仓库目录中的 `README.md`、`AGENTS.md`、`CONTRIBUTING.md` 等文件默认只作为仓库入口卡的背景证据，不逐文件编译。

## 实测结果

| 检查 | 命令 | 结果 |
|---|---|---|
| lint | `python3 .env/health/wiki_check.py --checks lint --output summary` | `0 errors / 0 warnings` |
| health | `python3 .env/health/wiki_check.py --checks health --output summary` | `0 errors / 50 warnings` |
| 回归测试 | `python3 .env/health/test_wiki_health_regressions.py` | `OK` |

## 本轮已完成修复

### 1. 健康检查器与规则口径收敛

- `.env/health/wiki_check.py` 已进一步修正别名解析、代码块误报和跨层路径误报。
- `wiki/log.md`、`raw/...`、`outputs/...` 与常见媒体文件引用已从 wikilink 断链检查中排除。
- 回归测试继续通过，说明本轮规则调整没有引入新的明显退化。

### 2. 剩余真实 wikilink 错误清零

- `machine-learning` 旧索引页中的占位链接、历史英文别名和 non-canonical 入口已回收。
- `nlp` 主题旧任务索引中的 `nlp-tasks`、`nlp-kg`、`nlp-libs` 等占位链接已收敛为现有稳定页或普通文本。
- 若干 `operations-research`、`reinforcement-learning`、`statistics-theory`、`timeseries-analysis`、`vibe-coding` 长尾坏链也已同步处理。

### 3. 来源层与 notes 口径增强

- 本轮继续按 `raw/web/**`、`raw/repos/repo-*.md`、`raw/notes/**` 重审来源层。
- `raw/notes/**` 已明确写入正式编译范围，不再只作为历史材料存在。
- `raw/notes/2026-04-17-电力市场交易调研文档.md` 已补齐最小 frontmatter，纳入标准编译链。

### 4. 控制文件与 shared 工作流页更新

- `README.md`、`wiki/index.md`、`schema.md` 已同步到当前执行顺序与输入边界。
- `知识库工作台`、`知识库来源与专题摄取索引`、`知识库问答与研究工作流`、`知识库输出回流工作流`、`知识库维护检查索引` 已统一到当前唯一可信工具链：
  - `python3 .env/health/wiki_check.py`
  - `python3 .env/run_tool.py health check`

## 当前 warning 边界

当前 `health` 剩余 `50 warnings`，但已无真实 wikilink 错误。warning 主要集中在两类：

### A. 低入口来源卡

- 以 `wiki/sources/deep-learning/*.md` 为主。
- 这些页面多数不是坏链，而是尚未被足够多索引或阅读地图吸收，属于“可达性偏弱”而非“结构损坏”。

### B. 少量长尾孤页

- 目前已确认的代表页包括：
  - `wiki/concepts/deep-learning/RoPE.md`
  - `wiki/sources/control-algorithms/2026-04-06-API reference - simple-pid 2.0.0.md`
  - `wiki/sources/control-algorithms/2026-04-06-掌握Shell编程，一篇就够了.md`
- 这类页面后续优先通过“补索引入口”解决，而不是再造平行概念页。

## 当前判断

- `lint` 已恢复到稳定通过状态。
- `health` 中的真实 wikilink 错误已清零。
- 当前主要工作已从“修红链”切换到“收敛 warning、增强入口和摘要质量”。

## 下一步优先级

1. 优先给 `deep-learning` 的长尾来源卡补主题索引入口，压缩 warning。
2. 为 `RoPE` 和少量高频孤页补更稳定的阅读路径，而不是继续增设桥接页。
3. 继续抽样复核 `raw/notes/**` 在主要主题下的“原始笔记 -> 来源卡 -> 索引入口”闭环。
4. 对 `raw/repos/repo-*.md` 仓库入口卡继续统一“仓库定位 / 模块边界 / 概念连接”写法。

## 备注

- 三份 `outputs/syntheses/2026-04-08-llm-wiki-*.md` 仍可从 `[[LLM-Wiki总索引]]` 到达。
- 本轮主报告不再沿用 `2026-04-16` 的旧问题清单；以当前实测结果为唯一基线。
