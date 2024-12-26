from . import model
import pprint
import re
import copy
from typing import Union

def read_book(path: str) -> model.TelephoneBook:
    """Читает файл книги контактов."""
    data = model.Open(path).read()
    book = model.TelephoneBook(data)
    return book

def print_all_contacts(book: model.TelephoneBook) -> None:
    """Печатает в консоли все контакты в читабельном виде."""
    pprint.pp(book.show_contacts(), width=100)


def search_by_id(book: model.TelephoneBook, contact_id: str) -> dict:
    """Ищет и возвращает контакт по уникальному ID (UUID)."""
    try:
        return book.get_contact(contact_id)
    except model.MyExcept as e:
        return e


def search_by_fullname(book: model.TelephoneBook, fullname: str) -> Union[model.Contact, str]:
    """Ищет контакт по точному совпадению с полем ФИО.

    Возвращает либо словарь с атрибутами найденного контакта, либо строку 'Совпадений нет'.
    """
    for id in book:
        if book[id]['ФИО'] == fullname:
            contact = model.Contact(book[id])
            return contact
    return 'Совпадений нет'


def regexp_search(book: model.TelephoneBook, search_string: str) -> Union[tuple, str]:
    """Ищет контакты по произвольной строке."""

    pattern = re.compile(search_string, re.IGNORECASE)
    found_keys = {}

    for id in book:
        test_contact = model.Contact(book[id])
        if pattern.search(test_contact.full_name):
            found_keys[id] = book[id]
        if pattern.search(test_contact.phone_number):
            found_keys[id] = book[id]
        if pattern.search(test_contact.company):
            found_keys[id] = book[id]
        if pattern.search(test_contact.comment):
            found_keys[id] = book[id]

    if len(found_keys) > 0:
        return len(found_keys), found_keys
    else:
        return "!!! Совпадений не найдено !!!"


def add_contact(path: str, contact: dict, book: model.TelephoneBook) -> str:
    """Функция добавление нового контакта в файл справочника.

    Проверяет на совпадение с существующими контактами по полю ФИО.
    """
    new_contact = model.Contact(contact)
    
    if search_by_fullname(book, new_contact.full_name) == 'Совпадений нет':
        updated_book = book.add_contact(new_contact)
        model.Save(path, updated_book).write()
        return '!!! Контакт добавлен !!!'
    else:
        return '!!! Контакт с таким ФИО уже существует !!!'


def del_contact(path: str, contact_id: str, book: model.TelephoneBook) -> Union[None, str]:
    """Функция удаления контакта."""
    try:
        updated_book = book.del_contact(contact_id)
    except model.MyExcept as e:
        return e
    model.Save(path, updated_book).write()
    return '!!! Контакт удален !!!'


def change_contact(path: str, contact_id: str, contact_changes: dict, book: model.TelephoneBook) -> Union[None, str]:
    """Функция изменения контакта и сохранения его в файле."""
    try:
        old_contact = model.Contact(book.get_contact(contact_id))
    except model.MyExcept as e:
        return e
    new_contact = copy.deepcopy(old_contact)
    
    if contact_changes['ФИО'] != '':
        new_contact.full_name = contact_changes['ФИО']
    if contact_changes['Телефон'] != '':
        new_contact.phone_number = contact_changes['Телефон']
    if contact_changes['Компания'] != '':
        new_contact.company = contact_changes['Компания']
    if contact_changes['Комментарии'] != '':
        new_contact.comment = contact_changes['Комментарии']
    
    if new_contact.all != old_contact.all:
        updated_book = book.change_contact(contact_id, new_contact)
        model.Save(path, updated_book).write()
        return '!!! Контакт изменен !!!'
    else:
        return '!!! Контакт остался без изменений !!!'
