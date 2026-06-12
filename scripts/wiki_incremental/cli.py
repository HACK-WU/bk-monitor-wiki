# -*- coding: utf-8 -*-
"""Command line entrypoint for wiki incremental update helpers."""

from __future__ import annotations

import argparse

from . import change_detection, index_builder


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="wiki-incremental", description="BK-Monitor wiki incremental update helpers")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build-index", help="Build source/wiki indexes into metadata.json")
    build_parser.add_argument("--wiki-dir", required=True)
    build_parser.add_argument("--commit")
    build_parser.add_argument("--repo-dir", default=".")
    build_parser.add_argument("--repo-url", default="")
    build_parser.add_argument("--branch", default="")
    build_parser.add_argument("--metadata")
    build_parser.add_argument("--output")

    detect_parser = subparsers.add_parser("detect", help="Detect wiki pages affected by a commit range")
    detect_parser.add_argument("--metadata", required=True)
    detect_parser.add_argument("--new-commit", required=True)
    detect_parser.add_argument("--old-commit")
    detect_parser.add_argument("--repo-dir", default=".")

    args = parser.parse_args(argv)
    if args.command == "build-index":
        return index_builder.main(
            [
                "--wiki-dir",
                args.wiki_dir,
                "--repo-dir",
                args.repo_dir,
                *(["--commit", args.commit] if args.commit else []),
                *(["--repo-url", args.repo_url] if args.repo_url else []),
                *(["--branch", args.branch] if args.branch else []),
                *(["--metadata", args.metadata] if args.metadata else []),
                *(["--output", args.output] if args.output else []),
            ]
        )
    if args.command == "detect":
        return change_detection.main(
            [
                "--metadata",
                args.metadata,
                "--new-commit",
                args.new_commit,
                "--repo-dir",
                args.repo_dir,
                *(["--old-commit", args.old_commit] if args.old_commit else []),
            ]
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

