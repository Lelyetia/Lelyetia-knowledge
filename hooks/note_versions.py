"""Render each note's current version and a styled history from its Markdown table."""

from datetime import date
from html import escape
import re

from mkdocs.exceptions import PluginError


HISTORY_HEADING = re.compile(r"^ {0,3}##\s+版本记录(?:\s+\{#version-history\})?\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
VERSION = re.compile(r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
HEADERS = ["版本号", "更新日期", "更新概述"]
HISTORY_ROW = re.compile(
    r"<tr>\s*<td>(v?\d+\.\d+\.\d+)</td>\s*"
    r"<td>(\d{4}-\d{2}-\d{2})</td>\s*<td>(.*?)</td>\s*</tr>",
    re.DOTALL,
)


def _visible_lines(markdown):
    """Keep line numbers while hiding fenced examples and HTML comment blocks."""
    fence = None
    comment = False
    for line in markdown.splitlines():
        match = FENCE.match(line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            yield ""
        elif comment:
            comment = "-->" not in line
            yield ""
        elif match:
            fence = (match[1][0], len(match[1]))
            yield ""
        elif line.lstrip().startswith("<!--"):
            comment = "-->" not in line
            yield ""
        else:
            yield line


def _error(path, message, line=None):
    location = f"{path}:{line}" if line else path
    raise PluginError(f"{location}：{message}")


def _cells(line, path, number):
    text = line.strip()
    if not text.startswith("|"):
        _error(path, "版本记录需使用三列表格：版本号、更新日期、更新概述。", number)
    text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    cells = [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", text)]
    if len(cells) != 3:
        _error(path, "每条版本记录必须恰好包含三列；概述中的竖线请写成 \\|。", number)
    return cells


def read_history(markdown, path="note.md"):
    visible = list(_visible_lines(markdown))
    headings = [index for index, line in enumerate(visible) if HISTORY_HEADING.fullmatch(line)]
    if len(headings) != 1:
        _error(path, "请在文末保留且仅保留一个“## 版本记录”板块，可复制 templates/note.md。")
    start = headings[0]
    lines = [(index + 1, line) for index, line in enumerate(visible) if index > start and line.strip()]
    # Code examples after the footer would otherwise disappear from validation.
    if any(line.strip() and not masked.strip() and not line.lstrip().startswith("<!--")
           for line, masked in zip(markdown.splitlines()[start + 1:], visible[start + 1:])):
        _error(path, "版本记录应放在文末，表格后不要再放正文或代码块。")
    if len(lines) < 3:
        _error(path, "版本记录需包含表头、分隔行和至少一条记录。", start + 1)
    if _cells(lines[0][1], path, lines[0][0]) != HEADERS:
        _error(path, "版本记录表头应为：版本号 | 更新日期 | 更新概述。", lines[0][0])
    if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in _cells(lines[1][1], path, lines[1][0])):
        _error(path, "版本记录表格的第二行应使用 --- 分隔各列。", lines[1][0])

    records = []
    versions = set()
    for number, line in lines[2:]:
        version, updated, summary = _cells(line, path, number)
        match = VERSION.fullmatch(version)
        if not match:
            _error(path, "版本号请使用 v0.1.0 这样的三段数字格式。", number)
        key = tuple(int(value) for value in match.groups())
        if key in versions:
            _error(path, f"版本号 {version} 重复，请为每次更新填写不同版本号。", number)
        versions.add(key)
        try:
            if not ISO_DATE.fullmatch(updated):
                raise ValueError
            date.fromisoformat(updated)
        except ValueError:
            _error(path, "更新日期请填写真实有效的 YYYY-MM-DD 日期。", number)
        if not summary:
            _error(path, "每条版本记录都需要填写更新概述。", number)
        records.append({"version": version, "date": updated, "summary": summary, "key": key})

    ordered = sorted(records, key=lambda record: record["key"])
    if any(previous["date"] > current["date"] for previous, current in zip(ordered, ordered[1:])):
        _error(path, "新版本的更新日期不能早于旧版本。")
    return start, ordered[-1]


def on_page_markdown(markdown, page, **kwargs):
    start, latest = read_history(markdown, page.file.src_uri)
    page.meta["note_version"] = {"version": latest["version"], "date": latest["date"]}
    # A stable anchor lets the header link work regardless of translated TOC slugs.
    lines = markdown.splitlines(keepends=True)
    ending = "\n" if lines[start].endswith("\n") else ""
    lines[start] = "## 版本记录 {#version-history}" + ending
    return "".join(lines)


def _history_panel(history_html, metadata, path):
    heading_end = re.search(r"</h2\s*>", history_html)
    rows = list(HISTORY_ROW.finditer(history_html))
    if heading_end is None or not rows:
        _error(path, "版本记录表格未正确渲染，请确认 tables 扩展已启用。")
    rows.sort(key=lambda row: tuple(int(value) for value in VERSION.fullmatch(row[1]).groups()), reverse=True)
    entries = []
    for row in rows:
        version, updated, summary_html = row.groups()
        current = version == metadata["version"]
        current_class = " is-current" if current else ""
        current_badge = '<span class="note-history-current">当前版本</span>' if current else ""
        entries.append(
            f'<li class="note-history-entry{current_class}">'
            '<div class="note-history-entry-heading">'
            f'<span class="note-history-version" aria-label="版本 {escape(version)}">{escape(version)}</span>'
            f'{current_badge}'
            f'<time class="note-history-date" datetime="{updated}" aria-label="更新日期 {updated}">{updated}</time>'
            '</div>'
            f'<div class="note-history-summary">{summary_html}</div>'
            '</li>'
        )
    icon = (
        '<span class="note-history-icon" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 10a9 9 0 1 1 2.6 8.4"/><path d="M3 4v6h6"/>'
        '<path d="M12 7v5l3 2"/></svg></span>'
    )
    return (
        '<section class="note-history" aria-labelledby="version-history">'
        f'<div class="note-history-heading">{icon}{history_html[:heading_end.end()]}'
        f'<span class="note-history-count">{len(rows)} 个版本</span></div>'
        f'<ol class="note-history-list" role="list">{"".join(entries)}</ol>'
        '</section>'
    )


def on_page_content(html, page, **kwargs):
    metadata = page.meta["note_version"]
    version = escape(metadata["version"])
    updated = escape(metadata["date"])
    banner = (
        '<div class="note-version" role="note" aria-label="笔记版本信息">'
        f'<span class="note-version-current">当前版本 <strong>{version}</strong></span>'
        f'<span class="note-version-updated">最后更新 <time datetime="{updated}">{updated}</time></span>'
        '<a class="note-version-link" href="#version-history">查看版本记录 <span aria-hidden="true">↓</span></a>'
        '</div>'
    )
    heading = re.search(r'<h2\b[^>]*\bid="version-history"[^>]*>', html)
    if heading is None:
        _error(page.file.src_uri, "版本记录标题未正确渲染，请确认 attr_list 扩展已启用。")
    # Python-Markdown appends footnotes after the document. Keep references above
    # the final version-history section without changing the Markdown source.
    before_history = html[:heading.start()]
    history_html = html[heading.start():]
    footnotes = history_html.find('<div class="footnote">')
    if footnotes != -1:
        before_history += history_html[footnotes:] + "\n"
        history_html = history_html[:footnotes]
    html = before_history + _history_panel(history_html, metadata, page.file.src_uri)
    title = re.search(r"</h1\s*>", html)
    if title:
        return html[:title.end()] + "\n" + banner + html[title.end():]
    # Material supplies an h1 from the navigation title when a note has no h1.
    return banner + "\n" + html
