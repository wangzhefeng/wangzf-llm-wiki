from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / ".env" / "health" / "wiki_check.py"


def load_wiki_check():
    spec = importlib.util.spec_from_file_location("wiki_check", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


wiki_check = load_wiki_check()


class WikiHealthRegressionTests(unittest.TestCase):
    def test_check_dirs_accepts_current_repo_layout(self) -> None:
        self.assertEqual(wiki_check.check_dirs(REPO_ROOT).errors, [])

    def test_health_check_entry_links_resolve(self) -> None:
        files = [
            REPO_ROOT / "wiki" / "indexes" / "shared" / "知识库工作台.md",
            REPO_ROOT / "wiki" / "indexes" / "shared" / "知识库健康检查清单.md",
            REPO_ROOT / "wiki" / "indexes" / "shared" / "知识库操作记录索引.md",
        ]
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
        missing: list[str] = []

        for path in files:
            text = path.read_text(encoding="utf-8")
            for rel in link_re.findall(text):
                target = (path.parent / rel).resolve()
                if not target.exists():
                    missing.append(f"{path.relative_to(REPO_ROOT)} -> {rel}")

        self.assertEqual(missing, [])

    def test_check_source_path_accepts_scalar_and_list_raw_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            card = root / "wiki" / "sources" / "llm-wiki" / "demo.md"
            card.parent.mkdir(parents=True, exist_ok=True)
            card.write_text(
                textwrap.dedent(
                    """\
                    ---
                    source_path:
                      - raw/web/demo/2026-01-01-a.md
                      - raw/notes/demo/index.md
                    status: summarized
                    ---
                    """
                ),
                encoding="utf-8",
            )

            result = wiki_check.check_source_path(root)
            self.assertEqual(result.errors, [])

    def test_collect_wikilinks_strips_alias_and_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            wiki_root = root / "wiki"
            concepts = wiki_root / "concepts" / "demo"
            concepts.mkdir(parents=True, exist_ok=True)

            target = concepts / "目标页.md"
            target.write_text("# 目标页\n", encoding="utf-8")

            source = concepts / "源页.md"
            source.write_text(
                textwrap.dedent(
                    """\
                    ---
                    status: linked
                    ---

                    [[目标页|自定义标题]]
                    [[目标页#某一节|带标题锚点]]
                    """
                ),
                encoding="utf-8",
            )

            pairs = wiki_check.collect_wikilinks(wiki_root)
            self.assertEqual(
                pairs,
                [
                    (source, "目标页"),
                    (source, "目标页"),
                ],
            )

    def test_collect_wikilinks_ignores_fenced_code_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            wiki_root = root / "wiki"
            concepts = wiki_root / "concepts" / "demo"
            concepts.mkdir(parents=True, exist_ok=True)

            target = concepts / "目标页.md"
            target.write_text("# 目标页\n", encoding="utf-8")

            source = concepts / "源页.md"
            source.write_text(
                textwrap.dedent(
                    """\
                    ---
                    status: linked
                    ---

                    ```python
                    df[['age']]
                    ```

                    [[目标页]]
                    """
                ),
                encoding="utf-8",
            )

            pairs = wiki_check.collect_wikilinks(wiki_root)
            self.assertEqual(pairs, [(source, "目标页")])

    def test_check_source_path_rejects_non_raw_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            card = root / "wiki" / "sources" / "llm-wiki" / "demo.md"
            card.parent.mkdir(parents=True, exist_ok=True)
            card.write_text(
                textwrap.dedent(
                    """\
                    ---
                    source_path:
                      - raw/web/demo/2026-01-01-a.md
                      - wiki/concepts/demo.md
                    status: summarized
                    ---
                    """
                ),
                encoding="utf-8",
            )

            result = wiki_check.check_source_path(root)
            self.assertTrue(any("非 raw/ 相对路径" in err for err in result.errors))

    def test_check_legacy_naming_flags_old_topic_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target = root / "wiki" / "indexes" / "shared" / "demo.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                textwrap.dedent(
                    """\
                    ---
                    topics:
                      - llm-knowledge-base
                    status: linked
                    ---

                    legacy knowledge-base marker
                    """
                ),
                encoding="utf-8",
            )

            result = wiki_check.check_legacy_naming(root)
            self.assertTrue(any("llm-knowledge-base" in err for err in result.errors))
            self.assertTrue(any("knowledge-base" in err for err in result.errors))

    def test_check_legacy_naming_allows_historical_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target = root / "wiki" / "sources" / "llm-wiki" / "demo.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                textwrap.dedent(
                    """\
                    ---
                    source_path: raw/web/knowledge-base-building/2026-04-05-demo.md
                    topics:
                      - llm-wiki
                    status: summarized
                    ---

                    - 原文：[[raw/web/knowledge-base-building/2026-04-05-demo.md]]
                    - 来源：`raw/web/knowledge-base-building/2026-04-05-demo.md`
                    """
                ),
                encoding="utf-8",
            )

            result = wiki_check.check_legacy_naming(root)
            self.assertEqual(result.errors, [])


if __name__ == "__main__":
    unittest.main()
