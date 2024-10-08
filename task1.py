import psycopg2
from psycopg2 import sql
from faker import Faker
import random

# Підключення до бази даних PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="localhost"
    )

# Створення таблиць
def create_tables(cur):
    # Створення таблиці користувачів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
    """)

    # Створення таблиці статусів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE
        );
    """)

    # Створення таблиці завдань
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            status_id INTEGER REFERENCES status(id),
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
    """)

# Заповнення таблиць випадковими даними
def seed_data(cur, fake):
    # Додавання статусів
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cur.execute(
            "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING",
            (status,)
        )

    # Додавання випадкових користувачів
    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (fullname, email)
        )

    # Додавання випадкових завдань
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    for _ in range(20):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )

# Приклади запитів
def execute_queries(cur):
    # Отримати всі завдання певного користувача
    user_id = 1
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cur.fetchall()
    print(f"Завдання користувача з id={user_id}: {tasks}")

    # Вибрати завдання за певним статусом
    cur.execute("""
        SELECT * FROM tasks WHERE status_id = (
            SELECT id FROM status WHERE name = 'new'
        );
    """)
    new_tasks = cur.fetchall()
    print(f"Завдання зі статусом 'new': {new_tasks}")

    # Оновити статус конкретного завдання
    task_id = 1
    cur.execute("""
        UPDATE tasks 
        SET status_id = (SELECT id FROM status WHERE name = 'in progress') 
        WHERE id = %s
    """, (task_id,))

    # Отримати список користувачів, які не мають жодного завдання
    cur.execute("""
        SELECT * FROM users 
        WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
    """)
    users_without_tasks = cur.fetchall()
    print(f"Користувачі без завдань: {users_without_tasks}")

    # Отримати всі завдання, які ще не завершено
    cur.execute("""
        SELECT * FROM tasks 
        WHERE status_id != (SELECT id FROM status WHERE name = 'completed');
    """)
    incomplete_tasks = cur.fetchall()
    print(f"Завдання, які не завершено: {incomplete_tasks}")

# Основна функція
def main():
    # Підключаємося до бази даних
    conn = connect_db()
    cur = conn.cursor()

    # Створюємо таблиці
    create_tables(cur)

    # Ініціалізація Faker
    fake = Faker()

    # Заповнення таблиць випадковими даними
    seed_data(cur, fake)

    # Виконуємо SQL-запити
    execute_queries(cur)

    # Застосування змін та закриття підключення
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
