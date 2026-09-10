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

    @pytest.fixture(autouse=True)
    def setup(self):
        options = Options()
        # options.add_argument("--headless=new")
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
        yield
        self.driver.quit()

    @allure.story("Позитивный: главная страница открывается")
    @allure.title("Главная страница Кинопоиска открывается с правильным title")
    def test_main_page_opens(self):
        self.page.open()
        title = self.page.get_page_title()
        assert MAIN_PAGE_TITLE in title, f"Ожидали '{MAIN_PAGE_TITLE}', получили '{title}'"

    @allure.story("Позитивный: поиск фильма")
    @allure.title("Поиск фильма '{TEST_MOVIE_NAME}' возвращает результаты")
    def test_search_movie(self):
        self.page.open().search(TEST_MOVIE_NAME)
        page_source = self.driver.page_source.lower()
        assert TEST_MOVIE_NAME.lower() in page_source, f"На странице нет результатов по запросу '{TEST_MOVIE_NAME}'"

    @allure.story("Позитивный: переход на страницу фильма")
    @allure.title("Клик по первому результату открывает страницу фильма")
    def test_click_first_result(self):
        self.page.open().search(TEST_MOVIE_NAME).click_first_result()
        title = self.page.get_movie_title()
        assert title, "Заголовок фильма пустой"

    @allure.story("Позитивный: URL меняется после поиска")
    @allure.title("После поиска URL содержит поисковый запрос")
    def test_url_changes_after_search(self):
        self.page.open().search(TEST_MOVIE_NAME)
        assert (
            "search" in self.driver.current_url or "film" in self.driver.current_url
        ), f"URL не изменился: {self.driver.current_url}"

    @allure.story("Негативный: поиск несуществующего фильма")
    @allure.title("Поиск 'фывапролдж12345' не находит результатов")
    def test_search_nonexistent_movie(self):
        self.page.open().search("фывапролдж12345")
        page_source = self.driver.page_source.lower()
        assert (
            "ничего не найдено" in page_source or "не найдено" in page_source or "нет результатов" in page_source
        ), "Страница не сообщила об отсутствии результатов"
