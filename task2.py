# main.py

"""
Цей скрипт реалізує основні CRUD операції в MongoDB за допомогою бібліотеки PyMongo.

Вимоги:
- Встановлений MongoDB (локально або через Docker).
- Встановлена бібліотека PyMongo.

Рекомендації:
- Використовуйте віртуальне середовище Python для ізоляції залежностей.
- Запустіть MongoDB перед запуском цього скрипта.
"""

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

def get_database():
    """
    Підключається до бази даних MongoDB та повертає об'єкт бази даних.
    """
    try:
        # Замініть рядок підключення на ваш власний, якщо потрібно
        CONNECTION_STRING = "mongodb://localhost:27017/"
        client = MongoClient(CONNECTION_STRING)
        return client['cat_database']
    except Exception as e:
        print(f"Сталася помилка під час підключення до бази даних: {e}")

# Отримуємо об'єкт бази даних
db = get_database()
# Вибираємо колекцію 'cats'
collection = db['cats']

def display_all_cats():
    """
    Виводить всі записи з колекції 'cats'.
    """
    try:
        cats = collection.find()
        print("\nСписок всіх котів:")
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Сталася помилка під час отримання записів: {e}")

def find_cat_by_name(name):
    """
    Шукає кота за ім'ям та виводить його інформацію.
    :param name: Ім'я кота для пошуку.
    """
    try:
        cat = collection.find_one({'name': name})
        if cat:
            print(f"\nІнформація про кота '{name}':")
            print(cat)
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка під час пошуку кота: {e}")

def update_cat_age(name, new_age):
    """
    Оновлює вік кота за ім'ям.
    :param name: Ім'я кота для оновлення.
    :param new_age: Новий вік кота.
    """
    try:
        result = collection.update_one({'name': name}, {'$set': {'age': new_age}})
        if result.matched_count > 0:
            print(f"Вік кота '{name}' оновлено до {new_age}.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка під час оновлення віку кота: {e}")

def add_feature_to_cat(name, new_feature):
    """
    Додає нову характеристику до списку features кота за ім'ям.
    :param name: Ім'я кота для оновлення.
    :param new_feature: Нова характеристика для додавання.
    """
    try:
        result = collection.update_one({'name': name}, {'$push': {'features': new_feature}})
        if result.matched_count > 0:
            print(f"До кота '{name}' додано нову характеристику '{new_feature}'.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка під час додавання характеристики коту: {e}")

def delete_cat_by_name(name):
    """
    Видаляє запис кота з колекції за ім'ям.
    :param name: Ім'я кота для видалення.
    """
    try:
        result = collection.delete_one({'name': name})
        if result.deleted_count > 0:
            print(f"Кота з ім'ям '{name}' видалено.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка під час видалення кота: {e}")

def delete_all_cats():
    """
    Видаляє всі записи з колекції 'cats'.
    """
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except Exception as e:
        print(f"Сталася помилка під час видалення всіх котів: {e}")

def insert_cat(cat_data):
    """
    Додає нового кота до колекції.
    :param cat_data: Словник з даними кота.
    """
    try:
        result = collection.insert_one(cat_data)
        print(f"Додано кота з id {result.inserted_id}.")
    except Exception as e:
        print(f"Сталася помилка під час додавання кота: {e}")

def main():
    while True:
        print("\nВиберіть дію:")
        print("1. Вивести всі записи")
        print("2. Знайти кота за ім'ям")
        print("3. Оновити вік кота за ім'ям")
        print("4. Додати характеристику коту за ім'ям")
        print("5. Видалити кота за ім'ям")
        print("6. Видалити всі записи")
        print("7. Додати нового кота")
        print("0. Вийти")
        choice = input("Введіть номер дії: ")

        if choice == '1':
            display_all_cats()
        elif choice == '2':
            name = input("Введіть ім'я кота: ")
            find_cat_by_name(name)
        elif choice == '3':
            name = input("Введіть ім'я кота: ")
            try:
                new_age = int(input("Введіть новий вік кота: "))
                update_cat_age(name, new_age)
            except ValueError:
                print("Вік повинен бути числом.")
        elif choice == '4':
            name = input("Введіть ім'я кота: ")
            new_feature = input("Введіть нову характеристику: ")
            add_feature_to_cat(name, new_feature)
        elif choice == '5':
            name = input("Введіть ім'я кота: ")
            delete_cat_by_name(name)
        elif choice == '6':
            confirm = input("Ви впевнені, що хочете видалити всі записи? (так/ні): ")
            if confirm.lower() == 'так':
                delete_all_cats()
            else:
                print("Видалення скасовано.")
        elif choice == '7':
            name = input("Введіть ім'я кота: ")
            try:
                age = int(input("Введіть вік кота: "))
            except ValueError:
                print("Вік повинен бути числом.")
                continue
            features = input("Введіть характеристики кота через кому: ").split(',')
            features = [feature.strip() for feature in features]
            cat_data = {'name': name, 'age': age, 'features': features}
            insert_cat(cat_data)
        elif choice == '0':
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == '__main__':
    main()
