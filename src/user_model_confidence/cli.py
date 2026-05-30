from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from user_model_confidence.scorer import score_conversation
from user_model_confidence.trace_writer import write_trace_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score a conversation JSON file and emit a confidence trace."
    )
    parser.add_argument("input", type=Path, help="Path to score-conversation JSON.")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save trace JSON and Markdown files to the output directory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for saved trace outputs. Defaults to outputs/.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Pretty-print JSON output.",
    )
    args = parser.parse_args(argv)

    try:
        with args.input.open("r", encoding="utf-8") as file:
            request = json.load(file)
        result = score_conversation(request)
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.save:
        json_path, markdown_path = write_trace_outputs(request, result, args.output_dir)
        print(f"saved trace JSON: {json_path}")
        print(f"saved trace Markdown: {markdown_path}")

    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent, ensure_ascii=False))
    return 0
