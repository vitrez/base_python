import pytest
import json
import os
import sys

PACKAGE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(PACKAGE_DIR))

from homework_03 import controller
from homework_03 import model


test_path = 'temp_users.json'
fake_id = "1122334455"
exception_text = 'Ошибка! Нет контакта с таким ID.'
test_dict = {
                "a3ae55cc-ec58-48e3-812a-7988409d4315": {
                    "ФИО": "Касьянова Александра Александровна",
                    "Телефон": "+7(912)261-85-38",
                    "Компания": "Глобал Групп",
                    "Комментарии": "haulage alizarin consider"
                },
                "5ac280d6-9c55-4f42-ac82-a439cd24836d": {
                    "ФИО": "Иванов Максим Матвеевич",
                    "Телефон": "+7(499)245-83-56",
                    "Компания": "Костоправы",
                    "Комментарии": "impiety embitter exposit"
                },
                "01ff6bf4-5445-45f7-82ba-657a1fc78468": {
                    "ФИО": "Сизов Дмитрий Макарович",
                    "Телефон": "+7(499)439-62-77",
                    "Компания": "ООО «Петрофф-Аудит»",
                    "Комментарии": "stopgap pimple cooperate"
                }
            }

test_contact = {
                    "ФИО": "Ковалев Андрей Даниилович",
                    "Телефон": "+7(903)811-74-66",
                    "Компания": "SoNa Private Consulting",
                    "Комментарии": "FCC Gerald saloonkeep"
                }


@pytest.fixture(scope="session")
def create_file():
    with open(test_path, 'w', encoding='utf-8') as data_file:
        json.dump(test_dict, data_file, ensure_ascii=False, indent=4)
    yield test_path
    os.remove(test_path)

@pytest.fixture()
def open_book():
    book = controller.read_book(test_path)
    yield book

def test_read_book(create_file):
    book = controller.read_book(create_file)
    assert isinstance(book, model.TelephoneBook)

def test_search_by_id(open_book):
    contact = controller.search_by_id(open_book, "5ac280d6-9c55-4f42-ac82-a439cd24836d")
    assert isinstance(contact, dict)
    assert len(contact) == 4
    assert contact["Телефон"] == "+7(499)245-83-56"
    contact = controller.search_by_id(open_book, fake_id)
    assert str(contact) == exception_text

def test_search_by_fullname(open_book):
    contact = controller.search_by_fullname(open_book, "Сизов Дмитрий Макарович")
    assert isinstance(contact, model.Contact)
    assert contact.company == "ООО «Петрофф-Аудит»"
    contact = controller.search_by_fullname(open_book, "Иванов Иван Иванович")
    assert contact == 'Совпадений нет'

def test_regexp_search(open_book):
    contact = controller.regexp_search(open_book, '499')
    assert isinstance(contact, tuple)
    assert isinstance(contact[1], dict)
    assert len(contact[1]) == 2
    contact = controller.regexp_search(open_book, 'несуществующее поле')
    assert contact == "!!! Совпадений не найдено !!!"

def test_add_contact(open_book):
    assert len(open_book.show_contacts()) == 3
    status = controller.add_contact(test_path, test_contact, open_book)
    assert status == '!!! Контакт добавлен !!!'
    assert len(open_book.show_contacts()) == 4
    status = controller.add_contact(test_path, test_contact, open_book)
    assert status == '!!! Контакт с таким ФИО уже существует !!!'
    assert len(open_book.show_contacts()) == 4

def test_del_contact(open_book):
    assert len(open_book.show_contacts()) == 4
    status = controller.del_contact(test_path, "a3ae55cc-ec58-48e3-812a-7988409d4315", open_book)
    assert status == '!!! Контакт удален !!!'
    assert len(open_book.show_contacts()) == 3
    status = controller.del_contact(test_path, fake_id, open_book)
    assert str(status) == exception_text
    assert len(open_book.show_contacts()) == 3

def test_change_contact(open_book):
    contact_changes = {"ФИО": "", "Телефон": "", "Компания": "OTUS", "Комментарии": ""}
    status = controller.change_contact(test_path, "01ff6bf4-5445-45f7-82ba-657a1fc78468", contact_changes, open_book)
    assert status == '!!! Контакт изменен !!!'
    contact = open_book.get_contact("01ff6bf4-5445-45f7-82ba-657a1fc78468")
    assert contact["Компания"] == "OTUS"
    status = controller.change_contact(test_path, fake_id, contact_changes, open_book)
    assert str(status) == exception_text


if __name__ == '__main__':
    pytest.main()