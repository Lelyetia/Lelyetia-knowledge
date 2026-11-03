from pathlib import Path
from types import SimpleNamespace
import sys
import unittest

import markdown
from mkdocs.exceptions import PluginError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
import note_versions


def note(rows="| v0.1.0 | 2026-11-03 | 建立版本记录。 |", body="# 笔记\n\n原有正文。"):
    return body + "\n\n## 版本记录 {#version-history}\n\n| 版本号 | 更新日期 | 更新概述 |\n| --- | --- | --- |\n" + rows + "\n"


def render(source):
    page = SimpleNamespace(meta={}, file=SimpleNamespace(src_uri="example.md"))
    processed = note_versions.on_page_markdown(source, page)
    html = markdown.markdown(processed, extensions=["attr_list", "tables", "footnotes"])
    return note_versions.on_page_content(html, page), page


class NoteVersionTests(unittest.TestCase):
    def test_current_version_comes_from_history_not_row_position(self):
        source = note("| v0.9.0 | 2026-11-01 | 原有版本。 |\n| v0.10.0 | 2026-11-03 | 新版本。 |")
        html, page = render(source)
        self.assertEqual(page.meta["note_version"], {"version": "v0.10.0", "date": "2026-11-03"})
        self.assertIn("当前版本 <strong>v0.10.0</strong>", html)
        self.assertLess(html.index("</h1>"), html.index('class="note-version"'))
        self.assertLess(html.index('class="note-version"'), html.index("原有正文"))

    def test_new_history_record_updates_both_header_fields(self):
        html, _ = render(note("| v0.2.0 | 2026-11-04 | 补充示例。 |\n| v0.1.0 | 2026-11-03 | 初始记录。 |"))
        self.assertIn("当前版本 <strong>v0.2.0</strong>", html)
        self.assertIn('<time datetime="2026-11-04">2026-11-04</time>', html)

    def test_history_panel_preserves_versions_dates_and_formatted_summaries(self):
        html, _ = render(note(
            "| v0.1.0 | 2026-11-01 | 初始记录。 |\n"
            "| v0.2.0 | 2026-11-03 | 补充 **示例** 与 [来源](https://example.com)。 |"
        ))
        panel = html[html.index('<section class="note-history"'):]
        self.assertIn("2 个版本", panel)
        self.assertIn('<strong>示例</strong>', panel)
        self.assertIn('href="https://example.com"', panel)
        self.assertIn('datetime="2026-11-01"', panel)
        self.assertIn('datetime="2026-11-03"', panel)
        self.assertEqual(panel.count('class="note-history-current"'), 1)
        self.assertLess(panel.index('>v0.2.0</span>'), panel.index('>v0.1.0</span>'))

    def test_fenced_history_example_is_not_used_as_real_metadata(self):
        body = "# 笔记\n\n````markdown\n## 版本记录\n```python\npass\n```\n````\n\n原有正文。"
        html, _ = render(note(body=body))
        self.assertEqual(html.count('class="note-version"'), 1)
        self.assertIn("原有正文", html)

    def test_footnotes_stay_above_final_history_and_keep_return_links(self):
        body = "# 笔记\n\n正文[^source]。再次引用[^source]。\n\n## 参考资料\n\n[^source]: 课程来源。"
        html, _ = render(note(body=body))
        self.assertLess(html.index('class="footnote"'), html.index('<h2 id="version-history">'))
        self.assertIn('href="#fnref2:source"', html)
        self.assertIn('href="#version-history"', html)

    def test_notes_without_h1_can_use_material_navigation_title(self):
        html, _ = render(note(body=""))
        self.assertTrue(html.startswith('<div class="note-version"'))

    def test_escaped_pipe_can_be_used_in_summary(self):
        _, latest = note_versions.read_history(note(r"| v0.1.0 | 2026-11-03 | 解释 A \| B。 |"))
        self.assertEqual(latest["summary"], "解释 A | B。")

    def test_invalid_or_incomplete_history_fails_with_file_name(self):
        invalid_rows = [
            "| v0.1.0 | 2026-02-30 | 日期错误。 |",
            "| v0.1.0 | 2026-11-03 | |",
            "| v0.1.0 | 2026-11-03 | 首次。 |\n| 0.1.0 | 2026-11-03 | 重复。 |",
            "| v0.2.0 | 2026-11-01 | 新版。 |\n| v0.1.0 | 2026-11-03 | 旧版。 |",
            "| v0.1.0 | 2026-11-03 | 没有转义 | 竖线。 |",
        ]
        for rows in invalid_rows:
            with self.subTest(rows=rows), self.assertRaisesRegex(PluginError, "example.md"):
                note_versions.read_history(note(rows), "example.md")

    def test_missing_history_and_nonfinal_history_are_rejected(self):
        for source in ["# 新笔记", note() + "\n## 后续正文\n内容。", note() + "\n```python\npass\n```"]:
            with self.subTest(source=source), self.assertRaises(PluginError):
                note_versions.read_history(source)


if __name__ == "__main__":
    unittest.main()
