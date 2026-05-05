# LLM Wiki 维护系统

> **迁移说明**：2026-05-05 从 `.env/` 目录迁移而来。UV Python 虚拟环境已升至项目根目录。

## 目录结构

```
scripts/
├── README.md                 # 本文档
├── run_tool.py               # 统一入口工具
├── verify_setup.py           # 环境验证
├── qmd-wrapper.sh            # qmd 代理兼容包装
├── health/                   # 健康检查与 Lint
│   ├── wiki_check.py         # 统一检查工具（主入口）
│   └── test_wiki_health_regressions.py
├── fix/                      # 修复工具
├── backfill/                 # 回填与补充
├── classify/                 # 文件分类
├── assets/                   # 资产管理
├── create/                   # 创建与生成
├── compat/                   # 旧命令名兼容包装
│   ├── wiki_health_check.py  # → health/wiki_check.py --checks health
│   └── wiki_lint.py          # → health/wiki_check.py --checks lint
├── archive/                  # 历史一次性任务脚本
├── repair_logs/              # 历史修复日志与JSON数据
└── tests/                    # 单元测试
```

## 虚拟环境

项目根目录 `.venv/`，由 `uv` 管理。python 3.11。

```bash
# 根目录
cd /Users/wangzf/wangzf-llm-wiki
source .venv/bin/activate   # 或: uv sync
```

## 常用命令

```bash
# 快速检查
uv run scripts/health/wiki_check.py --checks lint

# 全面检查
uv run scripts/health/wiki_check.py --checks all

# 统一入口（cd scripts/ 后）
python run_tool.py health check
python run_tool.py list
```

## 迁移历史

- **2026-05-05**：`.env/` 目录解散，内容移至 `scripts/`，虚拟环境升至根目录
- 原始 `.env/README.md` 保留了原始说明，本文档替代之
