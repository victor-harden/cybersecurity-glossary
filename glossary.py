#!/usr/bin/env python3
"""Searchable cybersecurity glossary."""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "terms.json"


def load(path: Path = DATA):
    return json.loads(path.read_text(encoding="utf-8"))


def search(terms, query: str):
    q = query.lower()
    return [t for t in terms
            if q in t["term"].lower()
            or q in t["definition"].lower()
            or any(q in tag.lower() for tag in t["tags"])]


def get(terms, name: str):
    for term in terms:
        if term["term"].lower() == name.lower():
            return term
    return None


def by_tag(terms, tag: str):
    return [t for t in terms if tag.lower() in [x.lower() for x in t["tags"]]]


def format_term(term) -> str:
    return f"{term['term']}\n  {term['definition']}\n  tags: {', '.join(term['tags'])}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Cybersecurity glossary")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search")
    group.add_argument("--term")
    group.add_argument("--tag")
    group.add_argument("--random", action="store_true")
    group.add_argument("--quiz", type=int, metavar="N")
    group.add_argument("--list", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--seed", type=int, help="deterministic random selection")
    args = parser.parse_args(argv)

    terms = load()
    if args.seed is not None:
        random.seed(args.seed)

    if args.search:
        results = search(terms, args.search)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("\n\n".join(format_term(t) for t in results) or "no matches")
        return 0 if results else 1

    if args.term:
        term = get(terms, args.term)
        if term is None:
            print(f"term not found: {args.term}", file=sys.stderr)
            return 1
        print(json.dumps(term, indent=2) if args.json else format_term(term))
        return 0

    if args.tag:
        results = by_tag(terms, args.tag)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("\n\n".join(format_term(t) for t in results) or "no matches")
        return 0 if results else 1

    if args.random:
        print(format_term(random.choice(terms)))
        return 0

    if args.quiz:
        sample = random.sample(terms, min(args.quiz, len(terms)))
        for item in sample:
            print(f"- {item['term']}")
        print("\nAnswers:")
        for item in sample:
            print(f"- {item['term']}: {item['definition']}")
        return 0

    if args.json:
        print(json.dumps(terms, indent=2))
    else:
        print("\n".join(sorted(t["term"] for t in terms)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
