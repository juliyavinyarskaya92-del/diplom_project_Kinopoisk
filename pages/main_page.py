import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import MAIN_URL, IMPLICIT_WAIT


class MainPage:
    """Page Object главной страницы Кинопоиска."""

    # === Локаторы ===
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[role='combobox'][placeholder*='Фильмы']")
    FIRST_RESULT_LINK = (By.CSS_SELECTOR, "a[href*='/film/'], a[href*='/series/'], a[data-tid]")
    MOVIE_TITLE = (By.CSS_SELECTOR, "h1[data-tid], h1")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, IMPLICIT_WAIT)

    @allure.step("Открываем главную страницу Кинопоиска")
    def open(self):
        self.driver.get(MAIN_URL)
        return self

    @allure.step("Ищем фильм: {query}")
    def search(self, query: str):
        search_input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.ENTER)
        return self

    @allure.step("Кликаем по первому результату поиска")
    def click_first_result(self):
        first = self.wait.until(EC.element_to_be_clickable(self.FIRST_RESULT_LINK))
        first.click()
        return self

    @allure.step("Получаем заголовок фильма")
    def get_movie_title(self) -> str:
        title = self.wait.until(EC.visibility_of_element_located(self.MOVIE_TITLE))
        return title.text

    @allure.step("Получаем title страницы")
    def get_page_title(self) -> str:
        return self.driver.title
