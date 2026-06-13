"""从 relations-cache 备份恢复向量数据。

读取 relations-cache 备份，扫描对应 wiki 文件提取"简介"段落作为摘要，
生成 mem bulk-store 所需的 JSON 文件，通过向量化恢复语义搜索能力。

用法:
    cd /path/to/bk-monitor
    python3 bk-monitor-wiki/knowledge-indexer/scripts/restore_vectors.py \
        --cache bk-monitor-wiki/knowledge-indexer/backup/relations-cache.{timestamp}.bak.json \
        --wiki-dir bk-monitor-wiki/wiki \
        --output memories.json \
        --scope monitor \
        --category fact
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


def extract_summary(md_path: Path) -> Optional[str]:
    """从 wiki markdown 文件中提取 ## 简介 段落。

    策略：
    1. 找到 "## 简介" 标题行
    2. 取该段落的第一段非空、非引用文本作为摘要
    3. 限制在 200 字以内
    """
    if not md_path.exists():
        return None

    content = md_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    in_summary = False
    summary_lines = []

    for line in lines:
        stripped = line.strip()

        # 匹配 ## 简介 标题
        if re.match(r"^##\s+简介\s*$", stripped):
            in_summary = True
            continue

        if not in_summary:
            continue

        # 遇到下一个 ## 标题，简介段落结束
        if re.match(r"^##\s+", stripped) and "简介" not in stripped:
            break

        # 遇到 图表来源/章节来源 等来源标注，简介段落结束
        if re.match(r"^(图表来源|章节来源|图示来源)", stripped):
            break

        # 跳过空行、引用块、图片、代码块
        if not stripped or stripped.startswith(">") or stripped.startswith("```"):
            if summary_lines:
                break  # 已有内容且遇到空行，结束
            continue

        # 跳过 <cite> 块
        if stripped.startswith("<cite>") or stripped.startswith("</cite>"):
            continue

        # 跳过纯链接行
        if re.match(r"^\[.+\]\(file://", stripped):
            continue

        # 跳过 mermaid 图
        if stripped.startswith("```mermaid"):
            break

        # 收集文本
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", stripped)  # 去掉链接语法
        clean = re.sub(r"[*_~`#>]", "", clean)  # 去掉 markdown 标记
        summary_lines.append(clean)

        # 控制长度
        full = "".join(summary_lines)
        if len(full) > 250:
            break

    if not summary_lines:
        # 降级：取文件前 30 行中的第一段非空文本
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("<cite") and not stripped.startswith(">"):
                clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", stripped)
                clean = re.sub(r"[*_~`#>]", "", clean)
                if len(clean) > 20:
                    summary_lines.append(clean)
                    break

    summary = "".join(summary_lines).strip()
    return summary[:300] if summary else None


def build_bulk_store_json(
    cache_path: Path,
    wiki_dir: Path,
    output_path: Path,
    scope: str,
    category: str,
) -> dict:
    """读取 relations-cache，提取摘要，生成 bulk-store JSON。"""
    with open(cache_path, encoding="utf-8") as f:
        cache = json.load(f)

    entries = []
    stats = {"total": 0, "with_summary": 0, "missing_file": 0, "no_summary": 0}

    for group_path, group_info in cache.get("groups", {}).items():
        keywords = group_info.get("keywords", [])
        tags = ",".join(keywords[:5]) if keywords else ""

        for rel in group_info.get("hot_relations", []):
            source_path = rel.get("sourcePath", "")
            rel_text = rel.get("text", "")
            stats["total"] += 1

            md_file = wiki_dir / source_path
            if not md_file.exists():
                # 尝试匹配不同的大小写和命名
                stats["missing_file"] += 1
                print(f"  ⚠️  文件不存在: {source_path} (在 group: {group_path})", file=sys.stderr)
                continue

            summary = extract_summary(md_file)
            if not summary:
                stats["no_summary"] += 1
                # 即使没有摘要，仍然用标题作为 text
                text = f"{rel_text}\n\n[来源: {source_path}]"
            else:
                stats["with_summary"] += 1
                text = f"{summary}\n\n[来源: {source_path}]"

            entries.append({
                "text": text,
                "category": category,
                "importance": 0.7,
                "tags": tags,
                "scope": scope,
                # 额外元数据，供后续处理和验证
                "_meta": {
                    "sourcePath": source_path,
                    "relation": rel_text,
                    "group": group_path,
                },
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    return stats


def main():
    parser = argparse.ArgumentParser(description="从 relations-cache 恢复向量记忆数据")
    parser.add_argument("--cache", required=True, help="relations-cache 备份文件路径")
    parser.add_argument("--wiki-dir", required=True, help="wiki 文档目录")
    parser.add_argument("--output", default="memories.json", help="输出 JSON 文件路径")
    parser.add_argument("--scope", default="monitor", help="mem scope")
    parser.add_argument("--category", default="fact", help="默认分类 (preference/fact/decision/entity/reflection/other)")
    args = parser.parse_args()

    cache_path = Path(args.cache)
    wiki_dir = Path(args.wiki_dir)
    output_path = Path(args.output)

    if not cache_path.exists():
        print(f"❌ 备份文件不存在: {cache_path}", file=sys.stderr)
        sys.exit(1)

    if not wiki_dir.exists():
        print(f"❌ wiki 目录不存在: {wiki_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"📖 读取 relations-cache: {cache_path}")
    print(f"📂 wiki 目录: {wiki_dir}")
    print(f"📤 输出文件: {output_path}")
    print()

    stats = build_bulk_store_json(cache_path, wiki_dir, output_path, args.scope, args.category)

    print(f"\n{'='*50}")
    print(f"📊 统计:")
    print(f"  总条目:       {stats['total']}")
    print(f"  成功提取摘要: {stats['with_summary']}")
    print(f"  文件缺失:     {stats['missing_file']}")
    print(f"  无简介段落:   {stats['no_summary']}")
    print(f"  输出条目:     {stats['with_summary'] + stats['no_summary']}")
    print(f"\n✅ 结果已写入: {output_path}")
    print()
    print(f"下一步执行:")
    print(f"  mem bulk-store -f {output_path} --scope {args.scope} -c {args.category}")


if __name__ == "__main__":
    main()
