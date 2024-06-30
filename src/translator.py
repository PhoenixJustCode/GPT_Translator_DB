import openai
import os
from dotenv import load_dotenv

# Загрузка переменных из файла .env в переменные окружения
load_dotenv()

# Установка API ключа и базового URL
openai.api_key = os.getenv('API_KEY')
openai.api_base = os.getenv('API_URL')

# Чтение содержимого файла promt.txt
with open('promt.txt', 'r', encoding='utf-8') as file:
    prompt_template = file.read().strip()


def is_russian_alpha(text):
    russian_letters = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    return all(char.lower() in russian_letters for char in text if char.isalpha())

def get_translations(word):
    while True:
        try:
            # Подготовка данных для запроса
            prompt = prompt_template.format(word=word)
            content = word + " " + prompt  # Просто объединяем слово и шаблон запроса

            # Создание запроса к модели
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": content}
                ],
                n=10,
                timeout=5
            )

            # Получаем ответы и разделяем их на массив из трех элементов
            translations = response.choices[0].message['content'].strip().split('==')

            # Проверка на то, что все переводы состоят только из русских букв
            if all(is_russian_alpha(translation) for translation in translations):
                return translations
                
            else:
                print(f"Некорректные переводы: {translations}. Повторный запрос...")
        
        except Exception as e:
            print(f"Ошибка при запросе: {e}")
            return None
