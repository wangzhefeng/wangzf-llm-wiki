---
created_at: 2026-04-17
updated_at: 2026-05-02
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

## 检查结果（2026-05-02）

| 检查 | 结果 |
|---|---|
| lint | 0 errors / 0 warnings ✅ |
| health | 0 errors / 311 warnings |

## 本轮完成事项

### 结构层修复
- **raw frontmatter**: 11 → 0 ✅
- **raw naming**: 10 → 0 ✅
- **missing attachments**: 2 → 0 ✅
- **wikilink 断链**: 62 → 0 ✅（指向不存在文件的死链 → 纯文本）

### 规则与流程
- **schema.md**: wikilink 适用范围明确 + ingest 入库前检查
- **知识库健康检查清单.md**: 三层频率标签（🔵快速/🟢常规/🟠深度）
- **时间序列预测来源清单.md**: 完整索引 239 张来源卡，16 个分类维度, timeseries warning 138→1
- **wiki_check.py**: raw/outputs 跨层 wikilink 保持静默跳过（Obsidian 可正常解析）

### 语义层修复
- **power-market-trading**: 16 个名称不匹配 wikilink 修正（`-v1` 后缀 → 实际文件名）
- **DPO/ORPO**: 2 个概念页 wikilink 修正（指向 `DPO直接偏好优化`）
- **Word2Vec**: 2 个死链 → 纯文本

## 重要规则修正

`[[raw/...]]` 和 `[[outputs/...]]` 跨层 wikilink **允许使用**——在 Obsidian 中可正常解析为页面链接。`wiki_check.py` 对此类链接不做错误检查（保持静默跳过），不强制转换为 Markdown 链接。

## 当前 warning 边界

311 warnings 全部为低入口来源卡（无入链），按主题分布：
- deep-learning: 134 | llm: 79 | machine-learning: 56 | operations-research: 37
- 其余 < 5 各

**策略**：按需激活——仅操作活跃主题时才收敛对应 warning。

## 语义层深度检查

### 调研缺口
活跃主题 raw→sources 覆盖率良好，无明显断层。

### 概念-来源平衡
timeseries(33/242) 和 operations-research(19/81) 源头过剩但概念稀薄。建议等同一概念被 3+ 来源引用时再建概念页。

### 过时声明
所有概念页和索引页均在 90 天内更新，无过时内容。

## 整体健康评分：B+

- 结构层：A（0 errors 全覆盖）
- 输入覆盖：A（raw→sources 良好）
- 概念提炼：C（source-heavy 主题概念不足）
- 交叉引用：B（概念间互链稀疏，但无矛盾）

## 下一步

1. 给活跃主题补充概念间互链
2. 3+ 来源 → 1 概念页的提炼节奏
3. 每次 ingest 后跑 `wiki_check.py --checks lint`
4. 每个专题完成后跑 `--checks health`
5. 深度语义检查每 2 周一次（`prompts/lint/llm-wiki-health-check.md`）
