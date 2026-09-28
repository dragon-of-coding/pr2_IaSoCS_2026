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
        isbn = book.get("isbn", "")

        line = f"{index}. {book['title']} - {book['author']}"

        if isbn:
            line += f" [{isbn}]"

        print(line)


def add_book(
    books: list[dict],
    title: str,
    author: str,
    isbn: str = "",
) -> dict:
    if len(books) >= MAX_BOOKS:
        raise ValueError("Catalog limit reached")

    title = title.strip()
    author = author.strip()
    isbn = isbn.strip()

    if not title:
        raise ValueError("Title cannot be empty")

    if not author:
        raise ValueError("Author cannot be empty")

    book = {
        "title": title,
        "author": author,
        "isbn": isbn,
    }

    books.append(book)

    return book


def search_by_author(
    books: list[dict],
    query: str,
) -> list[dict]:
    query = query.casefold()

    return [
        book
        for book in books
        if query in book["author"].casefold()
    ]

def find_by_isbn(
    books: list[dict],
    isbn: str,
) -> dict | None:
    isbn = isbn.strip()

    for book in books:
        if book.get("isbn", "") == isbn:
            return book

    return None

def export_books(
    books: list[dict],
    path: Path,
) -> None:
    lines = []

    for index, book in enumerate(books, start=1):
        lines.append(
            f"{index}. {book['title']} - {book['author']}"
        )

    text = "\n".join(lines)

    if text:
        text += "\n"

    path.write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Book catalog")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("list")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.add_argument("author")
    add_parser.add_argument(
        "--isbn",
        default="",
    )

    author_parser = subparsers.add_parser("author")
    author_parser.add_argument("query")

    isbn_parser = subparsers.add_parser("isbn")
    isbn_parser.add_argument("isbn")
    
    export_parser = subparsers.add_parser("export")
    export_parser.add_argument(
        "path",
        nargs="?",
        default="books_export.txt",
    )

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
                args.isbn,
            )

            save_books(books)

            print(
                f"Added: {book['title']} - "
                f"{book['author']}"
            )

        elif args.command == "author":
            print_books(
                search_by_author(
                    books,
                    args.query,
                )
            )

        elif args.command == "isbn":
            book = find_by_isbn(
                books,
                args.isbn,
            )

            if book is None:
                print("Book not found.")
            else:
                print(
                    f"{book['title']} - "
                    f"{book['author']}"
                )

        elif args.command == "export":
            export_books(
                books,
                Path(args.path),
            )

            print(
                f"Exported {len(books)} books "
                f"to {args.path}"
            )

    except (
        OSError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        raise SystemExit(f"Error: {error}")


if __name__ == "__main__":
    main()
