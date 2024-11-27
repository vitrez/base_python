import controller


def menu(file_path) -> None:
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
          controller.print_all_contacts(file_path)

        ### Пункт 2
        elif ans == "2":
          search = input("Введите строку для поиска: ")
          controller.regexp_search(file_path, search)

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
            controller.add_contact(file_path, {'ФИО':full_name, 'Телефон':phone_number, 'Компания':company, 'Комментарии':comment})
          else:
            print("\n !!! Контакт не сохранен !!!")

        ### Пункт 4
        elif ans == "4":
          id = input("Введите ID контакта для удаления: ")
          selected_contact = controller.search_by_id(file_path, id)
          if isinstance(selected_contact, dict):
            print(f"Вы хотите удалить контакт: \n{selected_contact}")
            confirmation = input("Удаляем? (введите: да\нет) ")
            if confirmation == 'да':
              controller.del_contact(file_path, id)
            else:  
              print("\n !!! Контакт не удален !!!")
          else:
              print(f'\n !!! {selected_contact} !!!')

        ### Пункт 5
        elif ans == "5":
          id = input("Введите ID контакта для изменения: ")
          selected_contact = controller.search_by_id(file_path, id)
          if isinstance(selected_contact, dict):
            print(f"Вы хотите изменить контакт: \n{selected_contact}")
            confirmation = input("Изменяем? (введите: да\нет) ")
            if confirmation == 'да':
               controller.change_contact(file_path, id)
            else:  
              print("\n !!! Контакт не изменен !!!")
          else:
              print(f'\n !!! {selected_contact} !!!')

        ### Пункт 6
        elif ans == "6":
          print("\n До свидания!")
          ans=False
        else:
          print("\n !!! Такого пункта меню нет. Попробуйте еще раз !!!")
          ans=True
