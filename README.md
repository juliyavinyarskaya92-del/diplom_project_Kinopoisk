# Дипломный проект: Автотесты для Кинопоиска

## Оглавление
- [Описание](#описание)
- [Структура проекта](#структура-проекта)
- [Стек технологий](#стек-технологий)
- [Установка](#установка)
- [Запуск тестов](#запуск-тестов)
- [Автор](#автор)

---

## Описание

Финальная работа по ручному тестированию: [Ссылка на Yonote](https://vinni-juli.yonote.ru/share/9d9fd468-bc48-43d2-9999-a3bbe615a025)

Проект содержит UI- и API-автотесты для сайта **Кинопоиск** и его открытого API.

- **UI:** https://www.kinopoisk.ru/
- **API:** https://api.poiskkino.dev/documentation

**Протестированный функционал:**

**UI:**
- Открытие главной страницы
- Поиск фильма через строку поиска
- Переход на страницу фильма по клику
- Изменение URL после поиска
- Поиск несуществующего фильма (негативный)

**API:**
- Поиск фильма по названию
- Получение фильма по ID
- Поиск персоны по имени и профессии
- Получение фильма с несуществующим ID (негативный)
- Поиск с пустым запросом (негативный)

---

## Структура проекта

```
diplom_project_Kinopoisk/
├── pages/                  # Page Object классы
│   ├── __init__.py
│   ├── api_page.py         # API-клиент ПоискКино
│   └── main_page.py        # UI Page Object Кинопоиска
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── test_api.py         # API-тесты
│   └── test_ui.py          # UI-тесты
├── config.py               # Конфигурация
├── pytest.ini              # Настройки pytest
├── requirements.txt        # Зависимости
├── .env.example            # Шаблон переменных окружения
└── README.md               # Этот файл
```

---

## Стек технологий

- **pytest** — основная библиотека для написания и выполнения тестов.
- **selenium** — библиотека для автоматизации UI-тестирования.
- **webdriver-manager** — автоматическая установка ChromeDriver.
- **requests** — библиотека для работы с HTTP-клиентом (API-тестирование).
- **allure-pytest** — генерация отчётов о выполнении тестов.
- **python-dotenv** — загрузка переменных окружения из `.env`.

---

## Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/juliyavinyarskaya92-del/diplom_project_Kinopoisk.git
cd diplom_project_Kinopoisk
```

### 2. Создай и активируй виртуальное окружение

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS / Linux
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Создай файл `.env` в корне проекта

Скопируй `.env.example` → `.env` и заполни своими значениями:

```
API_KEY=твой_токен_от_poiskkino
MOVIE_ID=455188
TEST_MOVIE_NAME=Рыцарь дня
TEST_PERSON_NAME=Том Круз
TEST_PROFESSION=Актер
BROWSER=chrome
```

⚠️ Токен получи бесплатно на https://api.poiskkino.dev (или через телеграм-бот: @poiskkinodev_bot).
⚠️ Файл `.env` не коммитится в Git (он в `.gitignore`).

### 5. Установи Allure

Скачай с https://github.com/allure-framework/allure2/releases, распакуй в `C:\allure`, добавь `C:\allure\bin` в `PATH`.

Проверь:
```bash
allure --version
```

---

## Запуск тестов

### Только API-тесты

```bash
pytest -m api --alluredir=./allure-results
allure serve ./allure-results
```

### Только UI-тесты

```bash
pytest -m ui --alluredir=./allure-results
allure serve ./allure-results
```

### Все тесты

```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

### Дополнительные команды

```bash
pytest -v                     # подробный вывод
pytest -q                     # краткий вывод
pytest tests/test_api.py -v   # конкретный файл
pytest --clean-alluredir      # очистить прошлые результаты
```

---

Блок 7. Автор

## Автор

- **Студент:** Юлия Винярская
- **GitHub:** https://github.com/juliyavinyarskaya92-del
- **Репозиторий:** https://github.com/juliyavinyarskaya92-del/diplom_project_Kinopoisk.git

---
#Часть 8. Полезные команды для работы с README

Создать README.md в корне
bash
# PowerShell
New-Item README.md
Открыть в PyCharm
Правый клик по файлу → Open in Editor.

Проверить локально, как выглядит
bash
# Если установлен gh (GitHub CLI)
gh repo view --web
# Или просто открой GitHub в браузере после push
Обновить в Git
bash
git add README.md
git commit -m "docs: complete README with install and usage instructions"
git push