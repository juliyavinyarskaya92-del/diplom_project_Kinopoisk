import allure
import requests
from config import MY_HEADERS, API_URL


class ApiPage:
    """Page Object для работы с API ПоискКино."""

    def __init__(self):
        self.base_url = API_URL
        self.headers = MY_HEADERS.copy()  # копия, чтобы не мутировать глобальный словарь
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @allure.step("Поиск фильма по названию: {phrase}")
    def search_films(self, phrase: str) -> requests.Response:
        """Универсальный метод для поиска фильмов по ключевому слову."""
        url = f"{self.base_url}/v1.5/movie/search"
        params = {"query": phrase}
        return self.session.get(url, params=params)

    @allure.step("Поиск персоны: {actor_name}, профессия: {profession_act}")
    def search_person(self, actor_name: str, profession_act: str) -> requests.Response:
        """Метод для поиска персоны (актера, режиссера и т.д.)."""
        url = f"{self.base_url}/v1.5/person"
        params = {"name": actor_name, "profession.value": profession_act}
        return self.session.get(url, params=params)

    @allure.step("Получение фильма по ID: {film_id}")
    def get_movie_by_id(self, film_id: int) -> requests.Response:
        """Поиск фильма по id. ID передается в URL (path parameter)."""
        url = f"{self.base_url}/v1.5/movie/{film_id}"
        return self.session.get(url)
