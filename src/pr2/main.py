import argparse
import json
from pathlib import Path


DATA_FILE = Path("books.json")
MAX_BOOKS = 200


def load_books(path: Path = DATA_FILE) -> list[dict]:
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Catalog must contain a JSON list")

    return data


def save_books(
    books: list[dict],
    path: Path = DATA_FILE,
) -> None:
    path.write_text(
        json.dumps(
            books,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def print_books(books: list[dict]) -> None:
    if not books:
        print("Catalog is empty.")
        return

    for index, book in enumerate(books, start=1):
        print(f"{index}. {book['title']} - {book['author']}")


def add_book(
    books: list[dict],
    title: str,
    author: str,
) -> dict:
    if len(books) >= MAX_BOOKS:
        raise ValueError("Catalog limit reached")

    title = title.strip()
    author = author.strip()

    if not title:
        raise ValueError("Title cannot be empty")

    if not author:
        raise ValueError("Author cannot be empty")

    book = {
        "title": title,
        "author": author,
    }

    books.append(book)

    return book


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

    add_parser = subparsers.add_parser(
        "add",
        help="Add a book",
    )

    add_parser.add_argument("title")
    add_parser.add_argument("author")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        books = load_books()

        if args.command == "list":
            print_books(books)

        elif args.command == "add":
            book = add_book(
                books,
                args.title,
                args.author,
            )

            save_books(books)

            print(
                f"Added: {book['title']} - "
                f"{book['author']}"
            )

    except (
        OSError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        raise SystemExit(f"Error: {error}")


if __name__ == "__main__":
    main()
