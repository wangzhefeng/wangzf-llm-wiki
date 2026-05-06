import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools" / "wiki_health_check.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wiki_health_check", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WikiHealthCheckTest(unittest.TestCase):
    def test_scan_repo_reports_core_health_dimensions(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "raw" / "web" / "demo").mkdir(parents=True)
            (root / "raw" / "repos" / "demo-repo").mkdir(parents=True)
            (root / "wiki" / "sources" / "demo").mkdir(parents=True)
            (root / "wiki" / "indexes").mkdir(parents=True)
            (root / "outputs" / "answers").mkdir(parents=True)
            (root / "outputs" / "logs").mkdir(parents=True)
            (root / "raw" / "assets" / "attachments" / "demo").mkdir(parents=True)

            (root / "wiki" / "log.md").write_text("# log\n", encoding="utf-8")
            (root / "raw" / "web" / "demo" / "2026-01-01-demo-source.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    source_type: web
                    created_at: 2026-01-01
                    topics:
                      - demo
                    status: inbox
                    ---

                    ![missing](raw/assets/attachments/demo/missing.png)
                    """
                ),
                encoding="utf-8",
            )
            (root / "raw" / "repos" / "demo-repo" / "README.md").write_text(
                "# demo repo\n", encoding="utf-8"
            )
            (root / "wiki" / "indexes" / "index.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    created_at: 2026-01-01
                    topics:
                      - demo
                    status: linked
                    ---

                    [[wiki/missing/index]]
                    """
                ),
                encoding="utf-8",
            )
            (root / "wiki" / "sources" / "demo" / "2026-01-01-demo-source.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    created_at: 2026-01-01
                    topics:
                      - demo
                    status: summarized
                    source_path: raw/web/demo/2026-01-01-demo-source.md
                    ---
                    """
                ),
                encoding="utf-8",
            )
            (root / "wiki" / "sources" / "demo" / "2026-01-01-demo source.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    created_at: 2026-01-01
                    topics:
                      - demo
                    status: summarized
                    source_path: raw/web/demo/2026-01-01-demo-source.md
                    ---
                    """
                ),
                encoding="utf-8",
            )
            (root / "outputs" / "answers" / "report.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    created_at: 2026-01-01
                    topics:
                      - demo
                    status: active
                    ---
                    """
                ),
                encoding="utf-8",
            )

            summary = module.scan_repo(root)

            self.assertEqual(summary["counts"]["wiki_broken_links_a"], 1)
            self.assertEqual(summary["frontmatter"]["raw_missing_frontmatter"], 1)
            self.assertEqual(summary["frontmatter"]["raw_missing_source_type"], 1)
            self.assertEqual(summary["frontmatter"]["nonstandard_output_status"], 1)
            self.assertEqual(summary["duplicate_source_cards"]["group_count"], 1)
            self.assertEqual(summary["missing_assets"]["missing_reference_count"], 1)
            self.assertEqual(summary["coverage"]["raw_without_source_card"], 1)


if __name__ == "__main__":
    unittest.main()
