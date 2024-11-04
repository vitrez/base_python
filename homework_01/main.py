import json
import pprint
import uuid
import re
from typing import Optional, Union

file_path = 'users.json'


def read_file(path: str) -> dict:
    """Читает json-файл и возвращает содержимое в виде словаря."""
    data_file = open(path, 'r', encoding='utf-8')
    data = json.load(data_file)
    data_file.close()
    return data


def print_all_contacts(path: str) -> None:
    """Печатает в консоли все контакты из файла."""
    data = read_file(path)
    pprint.pp(data, width=100)
    

def search_by_fullname(path: str, fullname: str) -> Union[dict, str]:
    """Ищет контакт по точному совпадению с полем ФИО.

    Возвращает либо словарь с атрибутами найденного контакта, либо строку 'Совпадений нет'.
    """
    data = read_file(path)
    for id in data.keys():
        if data[id]['ФИО'] == fullname:
            return data[id]
    return 'Совпадений нет'


def search_by_id(path: str, contact_id: str) -> dict:
    """Ищет и возвращает контакт по уникальному ID (UUID)."""
    data = read_file(path)
    if contact_id in data:
        return data[contact_id]


def regexp_search(path: str, search_string: str) -> None:
    """Ищет контакты по произвольной строке.
    
    Регистронезависисмый поиск по всем полям контактов.
    Печатает в консоль списко найденных контактов либо строку 'Совпадений не найдено'.
    """
    data = read_file(path)
    pattern = re.compile(search_string, re.IGNORECASE)
    found_keys = {}
    for id, val in data.items():
        if pattern.search(data[id]['ФИО']):
            found_keys[id] = val
        if pattern.search(data[id]['Телефон']):
            found_keys[id] = val
        if pattern.search(data[id]['Компания']):
            found_keys[id] = val
        if pattern.search(data[id]['Комментарии']):
            found_keys[id] = val
    if len(found_keys) > 0:
        print(f"\n Найдено контактов: {len(found_keys)}")
        pprint.pp(found_keys, width=100)
    else:
        print("\n !!! Совпадений не найдено !!!")


def add_contact(path: str, contact: dict) -> None:
    """Функция добавление нового контакта в файл справочника.

    Проверяет на совпадение с существующими контактами по полю ФИО.
    Генерирует уникальный UUID и назначает его новому контакту.
    """
    data = read_file(path)
    new_uuid = str(uuid.uuid4())
    while new_uuid in data:
        new_uuid = str(uuid.uuid4())
    if search_by_fullname(path, contact['ФИО']) == 'Совпадений нет':
        data[new_uuid] = contact
        with open(path, 'w', encoding='utf-8') as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)
        print('!!! Контакт добавлен !!!')
    else:
        print('!!! Контакт с таким ФИО уже существует !!!')


def del_contact(path: str, contact_id: str) -> None:
    """Функция удаления контакта."""
    data = read_file(path)
    if contact_id in data:
        del data[contact_id]
        with open(path, 'w', encoding='utf-8') as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)
        print('!!! Контакт удален !!!')


def change_contact(path: str, contact_id: str) -> None:
    """Функция изменения контакта и сохранения его в файле."""
    data = read_file(path)
    if contact_id in data:
        old_contact = data[contact_id].copy()
        full_name = input(f'''
            Текущее ФИО: {data[contact_id]['ФИО']}
            Введите новое ФИО или пропустите: ''')
        phone_number = input(f'''
            Текущий телефон: {data[contact_id]['Телефон']}
            Введите новый Телефон или пропустите: ''')
        company = input(f'''
            Текущая компания: {data[contact_id]['Компания']}
            Введите новую Компанию или пропустите: ''')
        comment = input(f'''
            Текущие комментарии: {data[contact_id]['Комментарии']}
            Введите новый Комментарий или пропустите: ''')  
    if full_name != '':
        data[contact_id]['ФИО'] = full_name
    if phone_number != '':
        data[contact_id]['Телефон'] = phone_number
    if company != '':
        data[contact_id]['Компания'] = company
    if comment != '':
        data[contact_id]['Комментарии'] = comment 
    if data[contact_id] != old_contact:
        with open(path, 'w', encoding='utf-8') as data_file:
            json.dump(data, data_file, ensure_ascii=False, indent=4)
        print('\n !!! Контакт изменен !!!')
    else:
        print('\n !!! Контакт остался без изменений !!!')
   

def menu() -> None:
    """Основная функция для работы с меню справочника."""
    ans=True
    while ans:
        print ("""
        -----------------------------------------
        Добро пожаловать в телефонный справочник
        -----------------------------------------
        1. Показать все контакты
        2. Найти контакт
        3. Добавить контакт
        4. Удалить контакт
        5. Изменить контакт
        6. Выйти
        """)
        ans = input("Выберите номер пункта меню: ")
        ### Пункт 1
        if ans == "1":
          print_all_contacts(file_path)

        ### Пункт 2
        elif ans == "2":
          search = input("Введите строку для поиска: ")
          regexp_search(file_path, search)

        ### Пункт 3
        elif ans == "3":
          full_name = input("Введите ФИО полностью: ")
          phone_number = input("Введите номер телефона в формате +7(ххх)ххх-хх-хх: ")
          company = input("Введите название компании: ")
          comment = input("Введите произвольный комментарий: ")
          print(f"""
                \n Вы хотите добавить следующий контакт: 
                ФИО: {full_name}
                Телефон: {phone_number}
                Компания: {company}
                Комментарии: {comment}
                """)
          confirmation = input("Сохраняем? (введите: да\нет) ")
          if confirmation == 'да':
            add_contact(file_path, {'ФИО':full_name, 'Телефон':phone_number, 'Компания':company, 'Комментарии':comment})
          else:
            print("\n !!! Контакт не сохранен !!!")

        ### Пункт 4
        elif ans == "4":
          id = input("Введите ID контакта для удаления: ")
          selected_contact = search_by_id(file_path, id)
          if selected_contact == None:
              print('\n !!! Нет контакта с таким ID !!!')
          else:
            print(f"Вы хотите удалить контакт: \n{selected_contact}")
            confirmation = input("Удаляем? (введите: да\нет) ")
            if confirmation == 'да':
              del_contact(file_path, id)
            else:  
              print("\n !!! Контакт не удален !!!")

        ### Пункт 5
        elif ans == "5":
          id = input("Введите ID контакта для изменения: ")
          selected_contact = search_by_id(file_path, id)
          if selected_contact == None:
              print('\n !!! Нет контакта с таким ID !!!')
          else:
            print(f"Вы хотите изменить контакт: \n{selected_contact}")
            confirmation = input("Изменяем? (введите: да\нет) ")
            if confirmation == 'да':
               change_contact(file_path, id)
            else:  
              print("\n !!! Контакт не изменен !!!")

        ### Пункт 6
        elif ans == "6":
          print("\n До свидания!")
          ans=False
        else:
          print("\n !!! Такого пункта меню нет. Попробуйте еще раз !!!")
          ans=True

# Run program
menu()
