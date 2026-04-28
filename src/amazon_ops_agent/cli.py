from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ads_analysis import analyze_ads_report
from .ai_client import AIClient
from .config import load_settings
from .email_reply import draft_email_reply
from .image_plan import generate_image_plan
from .io import read_json, write_json
from .listing import optimize_listing


def main() -> None:
    parser = argparse.ArgumentParser(description="Amazon operations AI Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ads_parser = subparsers.add_parser("ads", help="Analyze Amazon advertising report")
    ads_parser.add_argument("--report", required=True, help="CSV/XLSX advertising report path")
    ads_parser.add_argument("--out", default="output/ads_analysis.json", help="Output JSON path")

    listing_parser = subparsers.add_parser("listing", help="Generate listing optimization plan")
    listing_parser.add_argument("--asin", help="ASIN override")
    listing_parser.add_argument("--product", required=True, help="Product brief JSON path")
    listing_parser.add_argument("--out", default="output/listing_plan.json", help="Output JSON path")

    email_parser = subparsers.add_parser("email", help="Draft buyer email reply")
    email_parser.add_argument("--scenario", required=True, help="After-sales scenario")
    email_parser.add_argument("--message", required=True, help="Buyer message")
    email_parser.add_argument("--out", default="output/email_reply.json", help="Output JSON path")

    image_parser = subparsers.add_parser("images", help="Generate Amazon image brief plan")
    image_parser.add_argument("--product", required=True, help="Product brief JSON path")
    image_parser.add_argument("--out", default="output/image_plan.json", help="Output JSON path")

    args = parser.parse_args()

    if args.command == "ads":
        result = analyze_ads_report(args.report)
        write_json(args.out, result)
        _print_result(args.out, result)
        return

    settings = load_settings()
    ai = AIClient(settings)

    if args.command == "listing":
        product = read_json(args.product)
        if args.asin:
            product["asin"] = args.asin
        result = optimize_listing(ai, product)
    elif args.command == "email":
        result = draft_email_reply(ai, args.scenario, args.message)
    elif args.command == "images":
        result = generate_image_plan(ai, read_json(args.product))
    else:
        parser.error("Unknown command")
        return

    write_json(args.out, result)
    _print_result(args.out, result)


def _print_result(path: str | Path, result: dict) -> None:
    print(f"Saved: {path}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

