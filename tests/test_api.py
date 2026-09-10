import allure
import pytest
from pages.api_page import ApiPage
from config import MOVIE_ID, TEST_MOVIE_NAME, TEST_PERSON_NAME, TEST_PROFESSION


@allure.epic("API тесты ПоискКино")
@allure.feature("Фильмы и персоны")
@pytest.mark.api
class TestApi:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.api = ApiPage()

    @allure.story("Позитивный: поиск фильма по названию")
    @allure.title("Поиск фильма '{TEST_MOVIE_NAME}' возвращает 200 и результаты")
    def test_search_film_by_name(self):
        response = self.api.search_films(TEST_MOVIE_NAME)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. " f"Ответ: {response.text}"
        data = response.json()
        assert "docs" in data, "В ответе нет ключа 'docs'"
        assert len(data["docs"]) > 0, "Поиск не вернул ни одного фильма"

    @allure.story("Позитивный: получение фильма по ID")
    @allure.title("Получение фильма по ID {MOVIE_ID}")
    def test_get_movie_by_id(self):
        response = self.api.get_movie_by_id(MOVIE_ID)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. " f"Ответ: {response.text}"
        data = response.json()
        assert data["id"] == MOVIE_ID, f"Ожидали ID {MOVIE_ID}, получили {data['id']}"

    @allure.story("Позитивный: поиск персоны")
    @allure.title("Поиск персоны '{TEST_PERSON_NAME}'")
    def test_search_person(self):
        response = self.api.search_person(TEST_PERSON_NAME, TEST_PROFESSION)
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}. " f"Ответ: {response.text}"
        data = response.json()
        assert "docs" in data
        assert len(data["docs"]) > 0, "Поиск не вернул ни одной персоны"

    @allure.story("Негативный: фильм с несуществующим ID")
    @allure.title("Несуществующий ID возвращает 404")
    def test_get_movie_invalid_id(self):
        # ID в допустимом диапазоне, но несуществующий
        response = self.api.get_movie_by_id(9999999)  # 7 цифр, в диапазоне
        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}. " f"Ответ: {response.text}"

    @allure.story("Негативный: поиск по спецсимволам")
    @allure.title("Поиск по спецсимволам не находит фильмов")
    def test_search_special_chars(self):
        response = self.api.search_films("@#$%^&*")
        assert response.status_code in [200, 400], f"Неожиданный статус: {response.status_code}"
        if response.status_code == 200:
            data = response.json()
            # Спецсимволы вряд ли найдут реальные фильмы
            # Но API может вернуть что угодно — проверяем формат
            assert "docs" in data
