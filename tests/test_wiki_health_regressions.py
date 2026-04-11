from __future__ import annotations

import re
import unittest
from pathlib import Path

from tools import wiki_lint


ROOT = Path(__file__).resolve().parents[1]


class WikiHealthRegressionTests(unittest.TestCase):
    def test_check_dirs_accepts_current_repo_layout(self) -> None:
        self.assertEqual(wiki_lint.check_dirs(ROOT), [])

    def test_health_check_entry_links_resolve(self) -> None:
        files = [
            ROOT / "wiki" / "indexes" / "knowledge-base-operations" / "知识库工作台.md",
            ROOT / "wiki" / "indexes" / "knowledge-base-operations" / "知识库健康检查清单.md",
            ROOT / "wiki" / "indexes" / "knowledge-base-operations" / "知识库操作记录索引.md",
        ]
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
        missing: list[str] = []

        for path in files:
            text = path.read_text(encoding="utf-8")
            for rel in link_re.findall(text):
                target = (path.parent / rel).resolve()
                if not target.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {rel}")

        self.assertEqual(missing, [])

    def test_all_source_paths_point_to_existing_raw_files(self) -> None:
        missing: list[str] = []

        for path in sorted((ROOT / "wiki" / "sources").rglob("*.md")):
            for line_no, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if not line.startswith("source_path:"):
                    continue
                rel = line.split(":", 1)[1].strip()
                if not rel.startswith("raw/"):
                    continue
                base = rel.split("#", 1)[0]
                if not (ROOT / base).exists():
                    missing.append(f"{path.relative_to(ROOT)}:{line_no} -> {rel}")

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
