from typing import Any
import uuid
import json


class MyExcept(Exception):
    """Класс кастомных исключений"""
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return f'Ошибка! {self.msg}'


class Open:
    """Класс для чтения файла в формате json"""
    def __init__(self, path: str) -> None:
        self.path = path

    def read(self) -> dict:
        """Читает json-файл и возвращает содержимое в виде словаря."""
        data_file = open(self.path, 'r', encoding='utf-8')
        data = json.load(data_file)
        data_file.close()
        return data


class Save:
    """Класс для записи файла в формате json"""
    def __init__(self, path: str, data: dict) -> None:
        self.path = path
        self.data = data

    def write(self) -> None:
        """Записывает данные в файл в формате json."""
        with open(self.path, 'w', encoding='utf-8') as data_file:
            json.dump(self.data, data_file, ensure_ascii=False, indent=4)


class Contact:
    """Класс контакта"""
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def __str__(self) -> str:
        """Возвращает контакт в строковом виде."""
        return str(self.data)

    @property
    def full_name(self) -> str:
        """Возвращает ФИО контакта."""
        return self.data['ФИО']
    
    @full_name.setter
    def full_name(self, new_full_name) -> str:
        """Изменяет ФИО контакта."""
        self.data['ФИО'] = new_full_name

    @property
    def phone_number(self) -> str:
        """Возвращает Телефон контакта."""
        return self.data['Телефон']
    
    @phone_number.setter
    def phone_number(self, new_phone_number) -> str:
        """Изменяет Телефон контакта."""
        self.data['Телефон'] = new_phone_number

    @property
    def company(self) -> str:
        """Возвращает Компанию контакта."""
        return self.data['Компания']
    
    @company.setter
    def company(self, new_company) -> str:
        """Изменяет Компанию контакта."""
        self.data['Компания'] = new_company

    @property
    def comment(self) -> str:
        """Возвращает Комментарии контакта."""
        return self.data['Комментарии']
    
    @comment.setter
    def comment(self, new_comment) -> str:
        """Изменяет Комментарии контакта."""
        self.data['Комментарии'] = new_comment
    
    @property
    def all(self) -> dict:
        """Возвращает все поля контакта."""
        return self.data    


class TelephoneBook:
    """Класс телефонного справочника"""
    def __init__(self, data: dict) -> None:
        self.data = data

    def __iter__(self) -> Any:
        for id in self.data:
            yield id

    def __getitem__(self, key) -> Any:
        return self.data[key]

    def add_contact(self, contact: Contact) -> dict:
        """Функция добавление нового контакта в файл справочника."""
        new_uuid = str(uuid.uuid4())
        while new_uuid in self.data:
            new_uuid = str(uuid.uuid4())
        self.data[new_uuid] = contact.all
        return self.data
    
    def del_contact(self, contact_id: str) -> dict:
        """Функция удаления контакта."""
        if contact_id in self.data:
            del self.data[contact_id]
        else:
            raise MyExcept('Нет контакта с таким ID.')
        return self.data

    def get_contact(self, contact_id: str) -> dict:
        """Ищет и возвращает контакт по уникальному ID (UUID)."""
        if contact_id in self.data:
            return self.data[contact_id]
        else:
            raise MyExcept('Нет контакта с таким ID.')
        
    def change_contact(self, contact_id: str, contact: Contact) -> dict:
        """Функция изменения контакта в файле справочника."""
        if contact_id in self.data:
          self.data[contact_id] = contact.all
        else:
            raise MyExcept('Нет контакта с таким ID.')
        return self.data
             
    def show_contacts(self) -> dict:
        """Выведет все контакты справочника"""
        return self.data
