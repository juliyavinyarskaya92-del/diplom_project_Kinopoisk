import allure
import requests
from config import MY_HEADERS, API_URL


class ApiPage:
    def __init__(self):
        self.base_url = API_URL
        self.headers = MY_HEADERS

    @allure.step("Отправка запроса на поиск")
    def search_goods(self, city_id, phrase):
        """Универсальный метод для поиска"""
        search_url = self.base_url +"/search/product"
        search_params = {
            'customerCityId': city_id,
            'products[page]': 1,
            'products[per-page]': 60,
            'phrase': phrase,
            'abTestGroup': 1
        }
        return requests.get(search_url, headers=self.headers, params=search_params )
