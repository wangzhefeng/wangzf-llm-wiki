#!/usr/bin/env python3
"""LLM Wiki 维护工具统一入口

用法:
  uv run scripts/run.py list                      # 列出所有工具
  uv run scripts/run.py <tool> [args...]          # 运行指定工具
  uv run scripts/run.py check                     # → wiki_check.py --checks all
  uv run scripts/run.py lint                      # → wiki_check.py --checks lint

特殊别名:
  check, lint, health  → wiki_lint.py (结构健康检查)
"""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TOOLS_DIR = SCRIPT_DIR / "tools"
ROOT_DIR = SCRIPT_DIR.parent

# 别名映射：简短命令 → (实际脚本, 追加参数)
ALIASES = {
    "check":  ("wiki_lint.py", ["--checks", "all"]),
    "lint":   ("wiki_lint.py", ["--checks", "lint"]),
    "health": ("wiki_lint.py", ["--checks", "health"]),
}


def _docstring_of(path: Path) -> str:
    """从脚本文件提取第一行 docstring 作为描述"""
    try:
        with open(path, encoding="utf-8") as f:
            f.readline()  # shebang
            line = f.readline().strip()
            if line.startswith('"""'):
                desc = line[3:].rstrip('"').strip()
                if not desc:
                    desc = f.readline().strip().rstrip('"').strip()
                return desc[:60]
    except Exception:
        pass
    return "-"


def list_tools():
    print("LLM Wiki 维护工具\n" + "=" * 50)
    py_files = sorted(TOOLS_DIR.glob("*.py"))
    for pf in py_files:
        desc = _docstring_of(pf)
        print(f"  {pf.stem:28} {desc}")
    print("\n别名:")
    for alias, (script, args) in ALIASES.items():
        print(f"  {alias:28} → {script} {' '.join(args)}")


def run_tool(script_name: str, args: list[str]) -> int:
    # 处理别名
    extra_args = []
    if script_name in ALIASES:
        actual, extra_args = ALIASES[script_name]
        script_path = TOOLS_DIR / actual
    else:
        script_path = TOOLS_DIR / f"{script_name}.py"

    if not script_path.exists():
        # 模糊匹配
        matches = list(TOOLS_DIR.glob(f"*{script_name}*.py"))
        if not matches:
            print(f"未知工具: {script_name}")
            print(f"可用: {', '.join(p.stem for p in sorted(TOOLS_DIR.glob('*.py')))}")
            print(f"别名: {', '.join(ALIASES.keys())}")
            return 1
        if len(matches) > 1:
            print(f"多个匹配: {', '.join(p.stem for p in matches)}")
            return 1
        script_path = matches[0]

    cmd = [sys.executable, str(script_path)] + extra_args + args

    # 自动注入 --root
    if "--root" not in cmd:
        try:
            with open(script_path, encoding="utf-8") as f:
                if "--root" in f.read() or "argparse" in f.read():
                    cmd.insert(2, "--root")
                    cmd.insert(3, str(ROOT_DIR))
        except Exception:
            pass

    env = os.environ.copy()
    env["WIKI_ROOT"] = str(ROOT_DIR)

    print(f"▶ {' '.join(cmd)}\n")
    try:
        return subprocess.run(cmd, cwd=ROOT_DIR, env=env).returncode
    except KeyboardInterrupt:
        print("\n中断")
        return 130


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    if sys.argv[1] == "list":
        list_tools()
        return 0
    return run_tool(sys.argv[1], sys.argv[2:])


if __name__ == "__main__":
    raise SystemExit(main())
