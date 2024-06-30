from database import connect_to_db, insert_or_update_keyword
from translator import get_translations


def fetch_untranslated_keywords():
    try:
        conn = connect_to_db()
        c = conn.cursor()
        c.execute('''
            SELECT id, keyword
            FROM keywords
            WHERE trans_1 IS NULL OR trans_2 IS NULL OR trans_3 IS NULL
        ''')
        keywords = c.fetchall()
        for keyword in keywords:
            word_id, word = keyword
            print(f"Извлечено ключевое слово '{word}' с ID {word_id}")
            translations = get_translations(word)
            if translations is not None and len(translations) == 3:
                insert_or_update_keyword(word_id, translations)
            else:
                pass
                # print(f"Ошибка получения переводов для слова '{word}'")
    finally:
        conn.close()

if __name__ == "__main__":
    fetch_untranslated_keywords()
