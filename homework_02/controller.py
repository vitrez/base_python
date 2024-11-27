import model
import pprint
import re
import copy
from typing import Optional, Union


def print_all_contacts(path: str) -> None:
    """Печатает в консоли все контакты из файла."""
    data = model.Open(path).read()
    book = model.TelephoneBook(data)
    pprint.pp(book.show_contacts(), width=100)


def search_by_id(path: str, contact_id: str) -> dict:
    """Ищет и возвращает контакт по уникальному ID (UUID)."""
    data = model.Open(path).read()
    book = model.TelephoneBook(data)
    try:
        return book.get_contact(contact_id)
    except model.MyExcept:
        return 'Нет контакта с таким ID'


def search_by_fullname(path: str, fullname: str) -> Union[model.Contact, str]:
    """Ищет контакт по точному совпадению с полем ФИО.

    Возвращает либо словарь с атрибутами найденного контакта, либо строку 'Совпадений нет'.
    """
    data = model.Open(path).read()
    book = model.TelephoneBook(data)

    for id in book:
        if book[id]['ФИО'] == fullname:
            contact = model.Contact(book[id])
            return contact
    return 'Совпадений нет'


def regexp_search(path: str, search_string: str) -> None:
    """Ищет контакты по произвольной строке."""
    data = model.Open(path).read()
    book = model.TelephoneBook(data)

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
        print(f"\n Найдено контактов: {len(found_keys)}")
        pprint.pp(found_keys, width=100)
    else:
        print("\n !!! Совпадений не найдено !!!")


def add_contact(path: str, contact: dict) -> None:
    """Функция добавление нового контакта в файл справочника.

    Проверяет на совпадение с существующими контактами по полю ФИО.
    """
    data = model.Open(path).read()
    book = model.TelephoneBook(data)
    new_contact = model.Contact(contact)
    
    if search_by_fullname(path, new_contact.full_name) == 'Совпадений нет':
        updated_book = book.add_contact(new_contact)
        model.Save(path, updated_book).write()
        print('!!! Контакт добавлен !!!')
    else:
        print('!!! Контакт с таким ФИО уже существует !!!')


def del_contact(path: str, contact_id: str) -> Union[None, str]:
    """Функция удаления контакта."""
    data = model.Open(path).read()
    try:
        updated_book = model.TelephoneBook(data).del_contact(contact_id)
    except model.MyExcept:
        return 'Нет контакта с таким ID'
    model.Save(path, updated_book).write()
    print('!!! Контакт удален !!!')


def change_contact(path: str, contact_id: str) -> Union[None, str]:
    """Функция изменения контакта и сохранения его в файле."""
    book = model.TelephoneBook(model.Open(path).read())
    try:
        old_contact = model.Contact(book.get_contact(contact_id))
    except model.MyExcept:
        return 'Нет контакта с таким ID'
    new_contact = copy.deepcopy(old_contact)

    full_name = input(f'''
        Текущее ФИО: {old_contact.full_name}
        Введите новое ФИО или пропустите: ''')
    phone_number = input(f'''
        Текущий телефон: {old_contact.phone_number}
        Введите новый Телефон или пропустите: ''')
    company = input(f'''
        Текущая компания: {old_contact.company}
        Введите новую Компанию или пропустите: ''')
    comment = input(f'''
        Текущие комментарии: {old_contact.comment}
        Введите новый Комментарий или пропустите: ''')  
    
    if full_name != '':
        new_contact.full_name = full_name
    if phone_number != '':
        new_contact.phone_number = phone_number
    if company != '':
        new_contact.company = company
    if comment != '':
        new_contact.comment = comment
    
    if new_contact.all != old_contact.all:
        updated_book = book.change_contact(contact_id, new_contact)
        model.Save(path, updated_book).write()
        print('\n !!! Контакт изменен !!!')
    else:
        print('\n !!! Контакт остался без изменений !!!')
