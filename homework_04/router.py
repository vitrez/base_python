from fastapi import APIRouter
from model import Book, books


router = APIRouter(
   prefix="/api",
   tags=["Таски"],
)


@router.get("/books/")
async def all_books():
    return {"books": books}


@router.post("/book/add")
async def add_book(book: Book):
    books.append(book)
    return {"book": book, "status": "added"}


@router.get("/books/author/{author}")
async def get_books_author(author: str):
    tmp = []
    for b in books:
        if b.author == author:
            tmp.append(b)
    return {"books": tmp}


@router.get("/books/id/{book_id}")
async def get_book(book_id: int):
    for b in books:
        if b.id == int(book_id):
            return {"book": b}