# LLM Wiki 维护系统

此目录包含用于维护和管理 LLM Wiki 知识库的工具脚本系统。所有脚本都针对 `/Users/wangzf/wangzf-llm-wiki` 仓库设计。

## 目录结构

```
.env/
├── README.md                     # 本文档
├── .venv/                        # Python 虚拟环境 (Python 3.11)
├── .python-version               # Python 版本指定 (3.11)
├── pyproject.toml                # 项目元数据 (uv 依赖管理)
├── uv.lock                       # 依赖锁定文件 (uv)
├── archive/                      # 历史一次性任务脚本 (已归档)
├── health/                       # 健康检查与 Lint 工具
├── fix/                          # 修复工具
├── backfill/                     # 回填与补充工具
├── classify/                     # 文件分类工具
├── assets/                       # 资产管理工具
└── create/                       # 创建与生成工具
```

## 虚拟环境

本目录包含专用的 Python 虚拟环境（Python 3.11），用于运行所有维护脚本。

**激活虚拟环境：**
```bash
cd /Users/wangzf/wangzf-llm-wiki/.env
source .venv/bin/activate
```

**退出虚拟环境：**
```bash
deactivate
```

**更新依赖：**
```bash
cd /Users/wangzf/wangzf-llm-wiki/.env
source .venv/bin/activate
uv sync
```

## 统一入口工具

提供了一个统一的入口脚本 `run_tool.py`，方便调用各类维护工具：

**列出所有可用工具：**
```bash
cd /Users/wangzf/wangzf-llm-wiki/.env
python run_tool.py list
```

**运行健康检查：**
```bash
cd /Users/wangzf/wangzf-llm-wiki/.env
python run_tool.py health check         # 统一入口：运行标准检查
python run_tool.py health lint          # 只运行 lint 检查
python run_tool.py health health_check  # 只运行 health 检查
```

**运行修复工具：**
```bash
cd /Users/wangzf/wangzf-llm-wiki/.env
python run_tool.py fix links --dry-run
python run_tool.py fix raw_frontmatter
```

**查看工具帮助：**
```bash
cd /Users/wangzf/wangzf-llm-wiki/.env
python run_tool.py health lint --help
```

**直接运行脚本：**
```bash
cd /Users/wangzf/wangzf-llm-wiki
python3 .env/health/wiki_check.py --checks lint
python3 .env/health/wiki_check.py --checks health
python3 .env/health/wiki_check.py --checks all
```

## 工具分类说明

### 1. 健康检查工具 (`health/`)

| 脚本 | 功能 | 使用频率 |
|------|------|----------|
| `wiki_check.py` | **统一检查工具** - 当前唯一可信入口，整合 lint 与 health 检查，支持选择性检查，并检查旧命名残留 | 推荐使用 |
| `test_wiki_health_regressions.py` | 单元测试，确保健康检查逻辑不会退化 | CI/CD 或开发时 |

**推荐用法（使用统一检查工具）：**
```bash
# 推荐：先分开看 lint 与 health
cd /Users/wangzf/wangzf-llm-wiki
python3 .env/health/wiki_check.py --checks lint
python3 .env/health/wiki_check.py --checks health

# 或使用统一入口
cd /Users/wangzf/wangzf-llm-wiki/.env
python run_tool.py health check

# 详细输出
python health/wiki_check.py --output detailed --max-errors 100
```

**兼容性说明：**
旧命令名 `wiki_lint.py` / `wiki_health_check.py` 仅保留为兼容包装；标准入口统一收敛到 `wiki_check.py` 或 `run_tool.py`：
```bash
# 使用原 lint 命令名（实际调用 wiki_check.py --checks lint）
cd /Users/wangzf/wangzf-llm-wiki/.env
python3 run_tool.py health lint

# 使用原 health_check 命令名（实际调用 wiki_check.py --checks health）
python3 run_tool.py health health_check
```

**统一检查工具功能：**
- **Lint 检查**：目录结构、source_path 字段、status 字段、相对链接、旧命名残留
- **Health 检查**：wikilink 断链、孤页、raw frontmatter 缺失、raw 命名规范、缺失附件
- **灵活选择**：支持单独运行 lint 或 health 检查
- **统一输出**：清晰的汇总报告和详细信息

## 当前执行口径

- 正式重编译输入范围：`raw/web/**`、`raw/repos/repo-*.md`、`raw/notes/**`
- `raw/repos/**` 中镜像仓库文档默认只作背景证据，不逐文件编译
- 标准顺序：`基线盘点 -> 修断链 -> 重编译 sources -> 刷新 indexes/concepts -> 更新流程文档 -> 复验与日志收尾`

### 2. 修复工具 (`fix/`)

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `fix_links.py` | 修复单个文件中的错误链接 | 发现断链时 |
| `fix_missing_attachments_refs.py` | 检查并修复缺失的附件引用 | 附件管理时 |
| `fix_raw_frontmatter.py` | 修复 raw 文件的 frontmatter | 新 raw 文件摄入后 |
| `fix_raw_links.py` | 修复 raw 链接 | raw 文件链接错误时 |
| `fix_raw_web_links.py` | 修复 raw/web 链接 | web 来源链接错误时 |
| `fix_remaining_links.py` | 修复剩余链接 | 综合链接修复 |
| `fix_wikilink_network.py` | 修复 wikilink 网络一致性 | wikilink 网络维护 |
| `normalize_raw_web_frontmatter.py` | 规范化 raw/web frontmatter 格式 | 前端数据标准化 |

### 3. 回填工具 (`backfill/`)

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `backfill_raw_frontmatter.py` | 为 raw 目录下所有文件补全 frontmatter | 批量处理历史 raw 文件 |
| `backfill_raw_wikilinks_in_source_cards.py` | 在 source cards 中回填 wikilink 到概念页 | 来源卡与概念页链接维护 |
| `backfill_sources_dir_indexes.py` | 为每个 source 子目录生成/更新 index.md | 目录索引自动生成 |
| `backfill_unreferenced_attachments_entrypoints.py` | 为未引用的附件创建入口页 | 附件管理 |

### 4. 分类工具 (`classify/`)

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `classify_files.py` | 多维度加权分类算法（内容关键词、文件名、目录位置、主题优先级） | 大批量 raw/web 文件自动分类 |
| `classify_simple.py` | 简化版分类，基于文件名前缀匹配 | 快速分类少量文件 |

### 5. 资产管理工具 (`assets/`)

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `migrate_uncategorized_attachments.py` | 将未分类的附件迁移到规范目录 | 附件整理 |
| `normalize_attachment_dir_names.py` | 规范化附件目录命名 | 保持命名一致性 |
| `organize_assets_leftovers.py` | 整理 assets 遗留文件 | 资产清理 |

### 6. 创建工具 (`create/`)

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `create_missing_source_cards_for_raw.py` | 为 raw 中尚未生成来源卡的文件自动创建 source card | 自动化摄取流程 |

### 7. 配置文件（根目录）

遵循 uv Python 虚拟环境规则，配置文件直接位于 `.env/` 根目录：

| 文件 | 功能 |
|------|------|
| `.python-version` | Python 版本指定 (3.11) |
| `pyproject.toml` | 项目元数据 (uv 依赖管理) |
| `uv.lock` | 依赖锁定文件 (uv) |

### 8. 归档脚本 (`archive/`)

包含已完成的一次性历史任务脚本，仅供参考：
- `cleanup_autofix.py`, `cleanup_autofix_batch.py`, `cleanup_remaining_autofix.py` - autofix 占位页清理
- `find_autofix_mappings.py` - autofix 映射查找
- `fix_broken_links.py`, `fix_broken_source_path_by_filename.py` - 特定断链修复
- `backfill_raw_local_notes_index_links.py`, `backfill_wikilinks_from_md_list.py` - 特定回填任务

## 维护工作流建议

### 日常检查
```bash
cd /Users/wangzf/wangzf-llm-wiki
# 快速 lint 检查
python3 .env/health/wiki_check.py --checks lint

# 全面健康检查
python3 .env/health/wiki_check.py --checks all

# 推荐：使用统一入口工具
cd .env
python3 run_tool.py health check
```

### 新内容摄入后
1. 运行分类工具将新文件归类
2. 运行 frontmatter 修复工具
3. 创建缺失的来源卡
4. 运行健康检查确认无问题

### 定期维护（每月）
1. 运行所有健康检查
2. 检查并修复断链
3. 整理附件和资产
4. 更新目录索引

## 注意事项

1. **虚拟环境**：所有脚本应在激活的虚拟环境中运行，以确保依赖一致性。
2. **备份**：运行任何修改脚本前，建议先提交 git 或备份重要文件。
3. **测试**：大多数脚本支持 `--dry-run` 或 `--check` 参数，先测试再执行。
4. **日志**：重要操作应在 `outputs/logs/` 中记录。

## 扩展开发

如需添加新维护工具：
1. 将脚本放入合适的分类目录
2. 在虚拟环境中安装所需依赖
3. 更新本文档说明
4. 考虑添加相应的测试到 `health/test_wiki_health_regressions.py`

---

*最后更新：2026-04-17*
*维护系统版本：1.0.0*
