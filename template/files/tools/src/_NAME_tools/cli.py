"""{{NAME}}-tools — 統合 CLI ディスパッチャ．

Usage:
    {{NAME}}-tools visualize [...]
"""
from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="{{NAME}}-tools",
        description="Visualization & analysis tools",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("visualize", help="単一実行結果の可視化", add_help=False)

    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in {"-h", "--help"}:
        parser.parse_args(argv)
        return

    command = argv[0]
    rest = argv[1:]
    if command == "visualize":
        from {{NAME}}_tools.visualize import main as run_main
        run_main(rest)
    else:
        parser.parse_args(argv)  # 不正なサブコマンドはここでエラーになる


if __name__ == "__main__":
    main()
