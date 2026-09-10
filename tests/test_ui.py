import pytest
import allure
from selenium import webdriver
from pages.main_page import MainPage
from config import MAIN_URL, MAIN_PAGE_TITLE


@pytest.fixture
def main_page():
    driver = webdriver.Chrome()
    page = MainPage(driver, MAIN_URL)
    yield page
    driver.quit()


@allure.feature("Smoke")
@allure.story("UI")
@allure.title("Проверка заголовка главной страницы")
@pytest.mark.smoke
def test_check_main_page_title(main_page):
    with allure.step("Заголовок главной страницы"):
        assert main_page.check_page_title(MAIN_PAGE_TITLE)


@allure.feature("Поиск книг")
@allure.story("UI")
@allure.title("Поиск книги по полному названию")
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize("phrase", [
    "Вендиго",
    "1984",
    "Капитанская дочка"
])
def test_search_book_by_title(main_page,phrase):
    with allure.step("Закрытие всплывающих окон"):
        main_page.close_popups()
    with allure.step("Поиск книги по полному названию"):
        main_page.search_goods(phrase)
    with allure.step("Количество результатов больше 0"):
        assert main_page.get_search_results_count() > 0

@allure.feature("Поиск книг")
@allure.story("UI")
@allure.title("Поиск книги по автору")
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.parametrize("phrase", [
    "Пушкин",
    "Scott",
    "Салтыков-Щедрин"
])
def test_search_book_by_author(main_page,phrase):
    with allure.step("Закрытие всплывающих окон"):
        main_page.close_popups()
    with allure.step("Поиск книги по полному названию"):
        main_page.search_goods(phrase)
    with allure.step("Количество результатов больше 0"):
        assert main_page.get_search_results_count() > 0
