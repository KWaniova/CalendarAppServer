import typing
import strawberry

# mutations (returning types)
# docstrings


books = [
    {"id": 1, "title": "Harry Potter", "author_id": 1},
    {"id": 2, "title": "Lord of The Rings", "author_id": 2},
    {"id": 3, "title": "1984", "author_id": 3}
]

authors = [
    {"id": 1, "name": 'J.K.Rowling'},
    {"id": 2, "name": 'J. R. R. Tolkien'},
    {"id": 3, "name": 'G. Orwell'},
]


def get_author_for_book(root) -> "Author":
    book_from_database = list(filter(lambda x: x["id"] == root.id, books))[0]
    author = list(filter(lambda x: x["id"] ==
                         book_from_database['author_id'], authors))[0]
    return Author(id=author['id'], name=author["name"])


@strawberry.type(description="This is book class")
class Book:
    id: strawberry.ID
    title: str
    author: "Author" = strawberry.field(resolver=get_author_for_book)


def get_books_for_author(root):
    return [Book(id=book['id'], title=book["title"]) for book in filter(lambda x: x.get("author_id") == root.id, books)]


@strawberry.type
class Author:
    id: strawberry.ID
    name: str
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors() -> typing.List[Author]:
    return [Author(id=author['id'], name=author["name"]) for author in authors]


def get_books() -> typing.List[Book]:
    return [Book(id=book['id'], title=book["title"]) for book in books]


@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=get_books)


@strawberry.input(description="This is input type of object")
class AddBookForAuthor:
    title: str
    author_id: strawberry.ID


@strawberry.type
class Mutation:
    @strawberry.mutation(description="This is mutation for adding book")
    def add_book(self, inputBook: AddBookForAuthor) -> None:
        author = list(filter(lambda x: x.id == int(
            inputBook.author_id), get_authors()))[0]
        books.append(
            {"id": len(books), "title": inputBook.title, "author_id": author.id})

    @strawberry.mutation  # nic nie zwraca
    def restart() -> None:
        print(f'Restarting the server')


schema = strawberry.Schema(query=Query, mutation=Mutation)
