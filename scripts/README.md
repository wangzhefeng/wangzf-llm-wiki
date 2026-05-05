# LLM Wiki 维护工具库

## 结构

```
scripts/
├── run.py                    # 统一入口
├── verify.py                 # 环境验证
├── qmd-wrapper.sh            # qmd 代理兼容包装
└── tools/                    # 所有功能工具
    ├── wiki_lint.py          # 核心：结构健康检查 (lint + health)
    ├── test_lint.py          # 回归测试
    ├── backfill_frontmatter.py
    ├── backfill_wikilinks.py
    ├── backfill_sources.py
    ├── backfill_attachments.py
    ├── create_sources.py
    ├── fix_attachments.py
    ├── fix_frontmatter.py
    └── migrate_attachments.py
```

## 常用命令

```bash
# 工具列表
uv run scripts/run.py list

# 结构健康检查
uv run scripts/run.py check      # lint + health
uv run scripts/run.py lint       # 仅 lint
uv run scripts/run.py health     # 仅 health

# 直接运行
uv run scripts/tools/wiki_lint.py --checks all

# 环境验证
uv run scripts/verify.py
```

## 工具速查

| 工具 | 功能 | 常用参数 |
|------|------|----------|
| `wiki_lint` | 结构健康检查 | `--checks lint\|health\|all` |
| `backfill_frontmatter` | 补全 raw 文件 frontmatter | `--apply` |
| `backfill_wikilinks` | 补全来源卡中 raw wikilink | `--apply` |
| `backfill_sources` | 更新 sources 目录索引 | — |
| `backfill_attachments` | 补全附件引用入口 | `--apply` |
| `create_sources` | 为 raw 文件创建来源卡 | — |
| `fix_attachments` | 修复附件引用断链 | `--apply` |
| `fix_frontmatter` | 规范化 raw/web frontmatter | `--apply` |
| `migrate_attachments` | 迁移未分类附件 | `--apply` |
