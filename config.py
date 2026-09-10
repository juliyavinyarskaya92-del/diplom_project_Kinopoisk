import os
from pathlib import Path
from dotenv import load_dotenv

# Явно указываем путь к .env — рядом с этим файлом
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# === UI настройки ===
MAIN_URL = "https://kinopoisk.ru/"
MAIN_PAGE_TITLE = "Кинопоиск"

# === API настройки ===
API_URL = "https://api.poiskkino.dev"

# Берём токен из .env по имени API_KEY
API_KEY = os.getenv("API_KEY")

# Защита от None: если токена нет — падаем сразу с понятной ошибкой
if not API_KEY:
    raise ValueError(
        "Не задан API_KEY! Проверь файл .env в корне проекта. "
        "Формат строки: API_KEY=твой_токен"
    )

MY_HEADERS = {
    "X-API-KEY": API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# === Тестовые данные ===
MOVIE_ID = int(os.getenv("MOVIE_ID", 455188))
TEST_MOVIE_NAME = os.getenv("TEST_MOVIE_NAME", "Рыцарь дня")
TEST_PERSON_NAME = os.getenv("TEST_PERSON_NAME", "Том Круз")
TEST_PROFESSION = os.getenv("TEST_PROFESSION", "Актер")

# === UI настройки браузера ===
BROWSER = os.getenv("BROWSER", "chrome")
IMPLICIT_WAIT = 20