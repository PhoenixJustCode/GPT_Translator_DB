import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')


def create_keywords_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(''' 
        SELECT count(name) 
        FROM sqlite_master 
        WHERE type='table' AND name='keywords'
    ''')

    if c.fetchone()[0] == 0:
        c.execute('''
            CREATE TABLE keywords (
                id INTEGER PRIMARY KEY,
                keyword TEXT UNIQUE NOT NULL,
                trans_1 TEXT,
                trans_2 TEXT,
                trans_3 TEXT
            )
        ''')

        c.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords (keyword)
        ''')

        print("Таблица keywords успешно создана.")
    else:
        pass

    conn.commit()
    conn.close()


def connect_to_db():
    conn = sqlite3.connect(DB_NAME)
    return conn


def insert_keyword(keyword):
    conn = connect_to_db()
    c = conn.cursor()

    # Проверка, существует ли уже такое ключевое слово
    c.execute('SELECT id FROM keywords WHERE keyword = ?', (keyword,))
    existing_record = c.fetchone()
    if existing_record:
        print(f"Ключевое слово '{keyword}' уже существует в базе данных.")
        conn.close()
        return

    # Если ключевого слова нет, вставляем его
    c.execute('INSERT INTO keywords (keyword) VALUES (?)', (keyword,))
    conn.commit()
    conn.close()
    print(f"Добавлено ключевое слово '{keyword}' в базу данных.")


def insert_or_update_keyword(keyword_id, translations):
    conn = connect_to_db()
    c = conn.cursor()

    # Обновляем записи переводов в базе данных
    c.execute('''
        UPDATE keywords
        SET trans_1 = ?, trans_2 = ?, trans_3 = ?
        WHERE id = ?
    ''', (translations[0], translations[1], translations[2], keyword_id))

    if c.rowcount == 0:
        print(f"Ключевое слово с ID {keyword_id} не найдено в базе данных.")
    else:
        print(f"Обновлены переводы для ключевого слова с ID {keyword_id}.")

    conn.commit()
    conn.close()


# Создание таблицы keywords, если она еще не существует
create_keywords_table()

# Пример добавления ключевого слова
keyword_to_insert = input("Введите слово: ")
insert_keyword(keyword_to_insert)
