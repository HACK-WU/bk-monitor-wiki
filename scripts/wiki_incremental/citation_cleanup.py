# -*- coding: utf-8 -*-
"""Clean stale source citations from wiki markdown."""

from __future__ import annotations

import os
import re


def cleanup_dead_citations(
    wiki_content: str,
    dead_files: list[str],
    renamed_files: dict[str, str],
) -> str:
    result = wiki_content
    for dead_path in dead_files:
        pattern = re.compile(
            r"^- \[[^\]]+\]\(file://" + re.escape(dead_path) + r"(?:#[^)]*)?\)\s*\n?",
            re.MULTILINE,
        )
        result = pattern.sub("", result)

    for old_path, new_path in renamed_files.items():
        path_pattern = re.compile(r"(file://)" + re.escape(old_path) + r"(#[^)]*)?")
        result = path_pattern.sub(lambda m: f"{m.group(1)}{new_path}{m.group(2) or ''}", result)
        old_name = os.path.basename(old_path)
        new_name = os.path.basename(new_path)
        if old_name != new_name:
            name_pattern = re.compile(r"(^- \[)" + re.escape(old_name) + r"((?::[^\]]+)?\]\(file://)", re.MULTILINE)
            result = name_pattern.sub(lambda m: f"{m.group(1)}{new_name}{m.group(2)}", result)

    result = re.sub(r"<cite>\s*\*\*本文引用的文件\*\*\s*</cite>\s*", "", result)
    # 移除所有引用条目已被清理的空来源块
    result = re.sub(
        r"^\*{0,2}(章节来源|图表来源|图示来源)\*{0,2}\s*\n"
        r"(?:(?:(?!- \[).)*\n)*"
        r"(?=\n|^#|\Z)",
        "",
        result,
        flags=re.MULTILINE,
    )
    return result

