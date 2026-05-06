#!/usr/bin/env python3
"""
兼容包装：旧 `wiki_lint.py` 入口。

标准入口已收敛为：
  python3 .env/health/wiki_check.py --checks lint
或：
  python3 .env/run_tool.py health lint
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    target = repo_root / ".env" / "health" / "wiki_check.py"
    cmd = [sys.executable, str(target), "--root", str(repo_root), "--checks", "lint", *sys.argv[1:]]
    return subprocess.run(cmd, cwd=repo_root).returncode


if __name__ == "__main__":
    raise SystemExit(main())
