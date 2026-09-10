import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Locators:
    SEARCH_FIELD = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[type='submit']")
    TITLES = (By.CSS_SELECTOR, "div.product-card__content")
    POPUP_CLOSE = (By.CSS_SELECTOR, '[data-popmechanic-close]')
    CITY_CONFIRM = (By.CSS_SELECTOR, '.chg-app-button--primary.chg-app-button--block')


class MainPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get(url)

    def _wait_for_elements(self, locator, multiple=False, timeout=10):
        if multiple:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator))
        else:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))

    @allure.step("Выбор города")
    def close_popups(self):
        city_elements = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(Locators.CITY_CONFIRM)
        )
        if city_elements and city_elements[0].is_displayed():
            city_elements[0].click()
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(Locators.CITY_CONFIRM)
            )

        popup_elements = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(Locators.POPUP_CLOSE)
        )
        if popup_elements and popup_elements[0].is_displayed():
            popup_elements[0].click()
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(Locators.POPUP_CLOSE)
            )

    @allure.step("Проверка заголовка страницы")
    def check_page_title(self, expected_title):
        WebDriverWait(self.driver, 10).until(EC.title_is(expected_title))
        return True

    @allure.step("Поиск товара по фразе")
    def search_goods(self, phrase):
        search_field = self._wait_for_elements(Locators.SEARCH_FIELD, multiple=False)
        search_field.send_keys(phrase)
        search_button = self._wait_for_elements(Locators.SEARCH_BUTTON, multiple=False)
        search_button.click()

    @allure.step("Получаем количество элементов в результатах поиска")
    def get_search_results_count(self):
        elements = self._wait_for_elements(Locators.TITLES, multiple=True)
        return len(elements)
