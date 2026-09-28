import argparse
import json
from pathlib import Path


DATA_FILE = Path("books.json")


def load_books(path: Path = DATA_FILE) -> list[dict]:
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Catalog must contain a JSON list")

    return data


def print_books(books: list[dict]) -> None:
    if not books:
        print("Catalog is empty.")
        return

    for index, book in enumerate(books, start=1):
        print(f"{index}. {book['title']} - {book['author']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Book catalog")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "list",
        help="Show all books",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        books = load_books()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Error: {error}")

    if args.command == "list":
        print_books(books)


if __name__ == "__main__":
    main()
