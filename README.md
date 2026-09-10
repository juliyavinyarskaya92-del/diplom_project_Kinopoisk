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
# Часть 8. Полезные команды для работы с README

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

---
# Часть 9: "Причесывание кода по параметрам и стандартам"

# 9.1 Проверка пунктуации и разметки внутри кода по PEP8— это стандарт оформления Python-кода. Соблюдение PEP8:
-Делает код единообразным в команде.
-Улучшает читаемость.
-Облегчает code review.
-Требуется в большинстве компаний (и в ТЗ твоего диплома).
Шаги:
1. Установить PEP8: pip install flake8
2. в терминале вписать команду: flake8 . --exclude=.venv,.git,__pycache__,allure-results,allure-report,.pytest_cache --max-line-length=120
В случае нахождения ошибрк по PEP8? можно обратиться к помощи black

# 9.2 Установить black- переформатирует код, но не меняет логику
Шаги:
1. Установить: pip install black
2. В терминале команда: black . --exclude='\.venv|\.git|__pycache__|allure-results|allure-report|\.pytest_cache' --line-length=120

После работы black нужно:
1. В терминале запустить повторную проверку: flake8
2. Затем, в случае если больше нет ошибок от flake8(PEP8), то необходимо повторно прогнать тесты, чтобы убедиться, что ничего не повредилось при устранении синтактических ошибок:
3. В терминале команда: pytest -q

# 9.3 Проверить diff в Git:
# 9.3.1: Посмотриv, что именно изменил black:
powershell
git diff
Это покажет все изменения.

# 9.3.2: Проверка, что тесты работают.
powershell
git diff --stat

# 9.3.3: Если тесты прошли:
powershell
git add .

# Проверить статус:

powershell
git status

Убедиться, что в staging только нужные файлы:
✅ README.md
✅ config.py
✅ pages/api_page.py
✅ pages/main_page.py
✅ tests/test_api.py
✅ tests/test_ui.py

НЕ должно быть:
❌ .env
❌ allure-results/
❌ __pycache__/
❌ .venv/

# Шаг Коммит:
powershell
git commit -m "style: apply black formatting and finalize project"

# Шаг Push:

powershell
git push
