# -*- coding: utf-8 -*-
"""Infer Wiki directory placement for new source files based on existing mapping patterns.

Extracts path-prefix rules from source_to_wiki and uses them to suggest where
new (unmapped) source files should be placed in the Wiki directory structure.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import PurePosixPath


@dataclass
class PlacementRule:
    """A single inferred mapping rule from source prefix to Wiki top-level directory."""

    source_prefix: str
    wiki_dir: str
    confidence: int  # 0-100, percentage of dominant wiki dir
    sample_count: int


@dataclass
class PlacementSuggestion:
    """Suggestion for where a new source file should be placed in Wiki."""

    source_path: str
    suggested_wiki_dir: str
    confidence: int
    rule: PlacementRule
    # Whether the file should extend an existing page or create a new one
    strategy: str = "new_page"  # "new_page" | "extend_existing"
    related_wikis: list[str] = field(default_factory=list)


def _strip_repo_prefix(path: str) -> tuple[str, ...]:
    """Strip 'bkmonitor/' prefix and return remaining path parts."""
    parts = PurePosixPath(path).parts
    if parts and parts[0] == "bkmonitor":
        parts = parts[1:]
    return parts


def infer_rules(
    source_to_wiki: dict[str, list[str]],
    min_confidence: int = 60,
    min_samples: int = 3,
) -> list[PlacementRule]:
    """Extract placement rules from existing source_to_wiki mapping.

    Uses 2-level source path prefixes (after stripping 'bkmonitor/') to find
    dominant Wiki top-level directories.

    Args:
        source_to_wiki: Existing mapping from source file paths to Wiki page paths.
        min_confidence: Minimum percentage for a rule to be considered reliable (0-100).
        min_samples: Minimum number of mapping occurrences required.

    Returns:
        List of PlacementRule sorted by confidence descending.
    """
    prefix_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for src, wikis in source_to_wiki.items():
        parts = _strip_repo_prefix(src)
        if len(parts) < 2:
            continue
        src_prefix = "/".join(parts[:2])
        for w in wikis:
            w_top = PurePosixPath(w).parts[0]
            prefix_counts[src_prefix][w_top] += 1

    rules: list[PlacementRule] = []
    for src_prefix, wiki_counts in prefix_counts.items():
        total = sum(wiki_counts.values())
        if total < min_samples:
            continue
        top_wiki = max(wiki_counts, key=wiki_counts.get)
        top_count = wiki_counts[top_wiki]
        pct = top_count * 100 // total
        if pct >= min_confidence:
            rules.append(
                PlacementRule(
                    source_prefix=src_prefix,
                    wiki_dir=top_wiki,
                    confidence=pct,
                    sample_count=total,
                )
            )

    # Sort by confidence descending, then by sample_count descending
    rules.sort(key=lambda r: (-r.confidence, -r.sample_count))
    return rules


def suggest_placement(
    new_source_path: str,
    rules: list[PlacementRule],
    source_to_wiki: dict[str, list[str]],
) -> PlacementSuggestion | None:
    """Suggest Wiki placement for a new (unmapped) source file.

    Tries to match the file's path prefix against inferred rules.
    If matched, also checks for related existing Wiki pages in the same
    directory that cover sibling source files (for potential extend_existing).

    Args:
        new_source_path: Path of the new source file (e.g. 'bkmonitor/apm/core/new_feature.py').
        rules: Pre-computed placement rules from infer_rules().
        source_to_wiki: Existing source_to_wiki mapping for context lookup.

    Returns:
        PlacementSuggestion if a rule matches, None otherwise.
    """
    parts = _strip_repo_prefix(new_source_path)
    if len(parts) < 2:
        return None

    src_prefix = "/".join(parts[:2])

    # Find matching rule (first match, rules are sorted by confidence)
    matched_rule: PlacementRule | None = None
    for rule in rules:
        if rule.source_prefix == src_prefix:
            matched_rule = rule
            break

    if matched_rule is None:
        return None

    # Check for related existing Wiki pages (same source prefix -> same wiki dir)
    related_wikis: set[str] = set()
    for src, wikis in source_to_wiki.items():
        src_parts = _strip_repo_prefix(src)
        if len(src_parts) >= 2 and "/".join(src_parts[:2]) == src_prefix:
            for w in wikis:
                if PurePosixPath(w).parts[0] == matched_rule.wiki_dir:
                    related_wikis.add(w)

    # Determine strategy: if there are closely related pages, suggest extending
    strategy = "extend_existing" if related_wikis else "new_page"

    return PlacementSuggestion(
        source_path=new_source_path,
        suggested_wiki_dir=matched_rule.wiki_dir,
        confidence=matched_rule.confidence,
        rule=matched_rule,
        strategy=strategy,
        related_wikis=sorted(related_wikis),
    )


def suggest_placements_batch(
    new_source_paths: list[str],
    source_to_wiki: dict[str, list[str]],
    min_confidence: int = 60,
    min_samples: int = 3,
) -> tuple[list[PlacementSuggestion], list[str]]:
    """Batch-suggest Wiki placements for multiple new source files.

    Args:
        new_source_paths: List of new source file paths.
        source_to_wiki: Existing source_to_wiki mapping.
        min_confidence: Minimum confidence threshold for rules.
        min_samples: Minimum sample count for rules.

    Returns:
        Tuple of (suggestions, unmatched_paths).
    """
    rules = infer_rules(source_to_wiki, min_confidence, min_samples)
    suggestions: list[PlacementSuggestion] = []
    unmatched: list[str] = []

    for path in new_source_paths:
        suggestion = suggest_placement(path, rules, source_to_wiki)
        if suggestion:
            suggestions.append(suggestion)
        else:
            unmatched.append(path)

    return suggestions, unmatched
