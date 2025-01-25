from typing import Optional, Self
from pydantic import BaseModel, model_validator


books = []


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None

    @model_validator(mode='after')
    def check_id_repeat(self) -> Self:
        for b in books:
            if self.id == b.id:
                raise ValueError(f'a book with ID = {self.id} already exists')
            elif self.title == b.title and self.author == b.author:
                raise ValueError(f'such a book: title="{self.title}", author="{self.author}" already exists')
        return self


books.append(Book(id=1, title="Война и мир", author="Л. Н. Толстой", year=1869))
books.append(Book(id=2, title="Обломов", author="И. А. Гончаров", year=1859))
books.append(Book(id=3, title="Отцы и дети", author="И. С. Тургенев", year=1861))
books.append(Book(id=4, title="Студент", author="А. П. Чехов", year=1894))
books.append(Book(id=5, title="Ионыч", author="А. П. Чехов", year=1898))
books.append(Book(id=6, title="Человек в футляре", author="А. П. Чехов", year=1898))
books.append(Book(id=7, title="Вишнёвый сад", author="А. П. Чехов", year=1903))
books.append(Book(id=8, title="Старуха Изергиль", author="М. Горький", year=1894))
books.append(Book(id=9, title="На дне", author="М. Горький", year=1902))
books.append(Book(id=10, title="Чистый понедельник", author="И. А. Бунин", year=1944))
books.append(Book(id=11, title="Господин из Сан-Франциско", author="И. А. Бунин", year=1915))
books.append(Book(id=12, title="Севастопольские рассказы", author="Л. Н. Толстой", year=1855))