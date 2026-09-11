import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from config import MAIN_PAGE_TITLE, TEST_MOVIE_NAME, BROWSER


@allure.epic("UI тесты Кинопоиска")
@allure.feature("Поиск и навигация")
@pytest.mark.ui
class TestUI:
    """UI-тесты главной страницы Кинопоиска и поиска фильмов."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Создание и закрытие WebDriver для каждого теста."""
        options = Options()
        # options.add_argument("--headless=new")  # отключено для отладки
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        if BROWSER == "chrome":
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Firefox()

        self.driver.implicitly_wait(5)
        self.page = MainPage(self.driver)

        # Allure: прикладываем информацию об окружении
        allure.attach(
            self.driver.capabilities["browserName"],
            name="Browser",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            self.driver.capabilities["browserVersion"],
            name="Browser Version",
            attachment_type=allure.attachment_type.TEXT,
        )

        yield
        self.driver.quit()

    # ========== Тест 1: Открытие главной страницы ==========
    @allure.story("Позитивный: главная страница открывается")
    @allure.title("Главная страница Кинопоиска открывается с правильным title")
    @allure.description(
        "Проверяем, что главная страница Кинопоиска открывается, "
        "и что в title страницы содержится ожидаемая подстрока."
    )
    @allure.severity(allure.severity_level.BLOCKER)
    def test_main_page_opens(self):
        with allure.step("Открыть главную страницу Кинопоиска"):
            self.page.open()

        with allure.step("Получить title страницы"):
            title = self.page.get_page_title()
            allure.attach(title, name="Page Title", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Проверить, что '{MAIN_PAGE_TITLE}' содержится в title"):
            assert MAIN_PAGE_TITLE in title, f"Ожидали '{MAIN_PAGE_TITLE}', получили '{title}'"

    # ========== Тест 2: Поиск фильма ==========
    @allure.story("Позитивный: поиск фильма")
    @allure.title("Поиск фильма '{TEST_MOVIE_NAME}' возвращает результаты")
    @allure.description(
        "Проверяем, что поиск фильма через строку поиска возвращает результаты — "
        "на странице появляется текст с названием фильма."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_movie(self):
        with allure.step(f"Открыть главную и ввести в поиск '{TEST_MOVIE_NAME}'"):
            self.page.open().search(TEST_MOVIE_NAME)

        with allure.step("Получить HTML-код страницы результатов"):
            page_source = self.driver.page_source.lower()
            allure.attach(
                self.driver.current_url,
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(f"Проверить, что '{TEST_MOVIE_NAME}' есть на странице"):
            assert TEST_MOVIE_NAME.lower() in page_source, f"На странице нет результатов по запросу '{TEST_MOVIE_NAME}'"

    # ========== Тест 3: Клик по первому результату ==========
    @allure.story("Позитивный: переход на страницу фильма")
    @allure.title("Клик по первому результату открывает страницу фильма")
    @allure.description(
        "Проверяем, что при клике на первый результат поиска " "открывается страница фильма с непустым заголовком (h1)."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_first_result(self):
        with allure.step(f"Открыть главную, найти '{TEST_MOVIE_NAME}', кликнуть по первому результату"):
            self.page.open().search(TEST_MOVIE_NAME).click_first_result()

        with allure.step("Получить заголовок фильма"):
            title = self.page.get_movie_title()
            allure.attach(title, name="Movie Title", attachment_type=allure.attachment_type.TEXT)
            allure.attach(
                self.driver.current_url,
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверить, что заголовок не пустой"):
            assert title, "Заголовок фильма пустой"

    # ========== Тест 4: URL меняется после поиска ==========
    @allure.story("Позитивный: URL меняется после поиска")
    @allure.title("После поиска URL содержит поисковый запрос")
    @allure.description(
        "Проверяем, что после ввода поискового запроса URL страницы " "меняется и содержит признак страницы поиска."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_url_changes_after_search(self):
        with allure.step("Запомнить URL до поиска"):
            self.page.open()
            url_before = self.driver.current_url
            allure.attach(url_before, name="URL before search", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Выполнить поиск '{TEST_MOVIE_NAME}'"):
            self.page.search(TEST_MOVIE_NAME)

        with allure.step("Получить URL после поиска"):
            url_after = self.driver.current_url
            allure.attach(url_after, name="URL after search", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверить, что URL изменился и содержит 'search' или 'film'"):
            assert "search" in url_after or "film" in url_after, f"URL не изменился: {url_after}"

    # ========== Тест 5: Поиск несуществующего фильма ==========
    @allure.story("Негативный: поиск несуществующего фильма")
    @allure.title("Поиск 'фывапролдж12345' не находит результатов")
    @allure.description(
        "Негативный сценарий: проверяем, что при поиске несуществующего фильма "
        "Кинопоиск сообщает об отсутствии результатов."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_nonexistent_movie(self):
        with allure.step("Выполнить поиск по несуществующему фильму"):
            self.page.open().search("фывапролдж12345")

        with allure.step("Дождаться появления сообщения 'ничего не найдено'"):
            # Явно ждём, что на странице появится текст об отсутствии результатов
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            from config import IMPLICIT_WAIT

            WebDriverWait(self.driver, IMPLICIT_WAIT).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "ничего не найдено")
            )

        with allure.step("Приложить HTML и URL к отчёту"):
            allure.attach(
                self.driver.current_url,
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                self.driver.page_source,
                name="Page Source",
                attachment_type=allure.attachment_type.HTML,
            )

        with allure.step("Проверить, что на странице есть сообщение об отсутствии результатов"):
            page_source = self.driver.page_source.lower()
            assert (
                "ничего не найдено" in page_source or "не найдено" in page_source
            ), f"Страница не сообщила об отсутствии результатов. URL: {self.driver.current_url}"
