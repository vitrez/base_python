from . import controller
import pprint


def menu(file_path) -> None:
    """Основная функция для работы с меню справочника."""
    ans=True
    while ans:
        print ("""
        -----------------------------------------
        Добро пожаловать в телефонный справочник
        -----------------------------------------
        1. Показать все контакты
        2. Найти контакт по ID
        3. Найти контакт по атрибутам
        4. Добавить контакт
        5. Удалить контакт
        6. Изменить контакт
        7. Выйти
        """)
        ans = input("Выберите номер пункта меню: ")
        ### Пункт 1
        if ans == "1":
          book = controller.read_book(file_path)
          controller.print_all_contacts(book)

        ### Пункт 2
        elif ans == "2":
          search = input("Введите ID контакта: ")
          book = controller.read_book(file_path)
          print(controller.search_by_id(book, search))

        ### Пункт 3
        elif ans == "3":
          search = input("Введите строку для поиска: ")
          book = controller.read_book(file_path)
          #controller.regexp_search(book, search)
          result = controller.regexp_search(book, search)
          if isinstance(result, tuple):
            print(f"\n Найдено контактов: {result[0]}")
            print("\n ")
            pprint.pp(result[1], width=100)
          else:
            print(result)

        ### Пункт 4
        elif ans == "4":
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
            book = controller.read_book(file_path)
            status = controller.add_contact(file_path, {'ФИО':full_name, 'Телефон':phone_number, 'Компания':company, 'Комментарии':comment}, book)
            print(status)
          else:
            print("\n !!! Контакт не сохранен !!!")

        ### Пункт 5
        elif ans == "5":
          id = input("Введите ID контакта для удаления: ")
          book = controller.read_book(file_path)
          selected_contact = controller.search_by_id(book, id)
          if isinstance(selected_contact, dict):
            print(f"Вы хотите удалить контакт: \n{selected_contact}")
            confirmation = input("Удаляем? (введите: да\нет) ")
            if confirmation == 'да':
              status = controller.del_contact(file_path, id, book)
              print(status)
            else:  
              print("\n !!! Контакт не удален !!!")
          else:
              print(f'\n !!! {selected_contact} !!!')

        ### Пункт 6
        elif ans == "6":
          id = input("Введите ID контакта для изменения: ")
          book = controller.read_book(file_path)
          selected_contact = controller.search_by_id(book, id)
          if isinstance(selected_contact, dict):
            print(f"Вы хотите изменить контакт: \n{selected_contact}")
            confirmation = input("Изменяем? (введите: да\нет) ")
            if confirmation == 'да':
                contact_changes = {}
                contact_changes['ФИО'] = input(f'''
                    Текущее ФИО: {selected_contact['ФИО']}
                    Введите новое ФИО или пропустите: ''')
                contact_changes['Телефон'] = input(f'''
                    Текущий телефон: {selected_contact['Телефон']}
                    Введите новый Телефон или пропустите: ''')
                contact_changes['Компания'] = input(f'''
                    Текущая компания: {selected_contact['Компания']}
                    Введите новую Компанию или пропустите: ''')
                contact_changes['Комментарии'] = input(f'''
                    Текущие комментарии: {selected_contact['Комментарии']}
                    Введите новый Комментарий или пропустите: ''')  
                status = controller.change_contact(file_path, id, contact_changes, book)
                print(status)
            else:  
                print("\n !!! Контакт не изменен !!!")
          else:
              print(f'\n !!! {selected_contact} !!!')

        ### Пункт 7
        elif ans == "7":
          print("\n До свидания!")
          ans=False
        else:
          print("\n !!! Такого пункта меню нет. Попробуйте еще раз !!!")
          ans=True
