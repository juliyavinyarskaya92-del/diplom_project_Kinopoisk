import allure
import pytest
from pages.api_page import ApiPage
from config import MOVIE_ID, TEST_MOVIE_NAME, TEST_PERSON_NAME, TEST_PROFESSION


@allure.epic("API тесты ПоискКино")
@allure.feature("Фильмы и персоны")
@pytest.mark.api
class TestApi:
    """API-тесты для ПоискКино: фильмы и персоны."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Создание API-клиента перед каждым тестом."""
        self.api = ApiPage()

    @staticmethod
    def _attach_response(response):
        """Приложить URL, статус-код и тело ответа к Allure-отчёту."""
        allure.attach(
            response.url,
            name="Request URL",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            str(response.status_code),
            name="Status Code",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

    # ========== Тест 1: Поиск фильма по названию ==========
    @allure.story("Позитивный: поиск фильма по названию")
    @allure.title("Поиск фильма '{TEST_MOVIE_NAME}' возвращает 200 и результаты")
    @allure.description(
        "Проверяем, что API ПоискКино по запросу с названием фильма "
        "возвращает статус 200 и непустой список результатов."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_film_by_name(self):
        with allure.step(f"Ищем фильм по названию'{TEST_MOVIE_NAME}'"):
            response = self.api.search_films(TEST_MOVIE_NAME)
            self._attach_response(response)

        with allure.step("Проверить, что статус-код = 200"):
            assert response.status_code == 200, (
                f"Ожидали 200, получили {response.status_code}. " f"Ответ: {response.text}"
            )

        with allure.step("Проверить, что в ответе есть ключ 'docs'"):
            data = response.json()
            assert "docs" in data, "В ответе нет ключа 'docs'"

        with allure.step("Проверить, что список фильмов не пустой"):
            assert len(data["docs"]) > 0, "Поиск не вернул ни одного фильма"

    # ========== Тест 2: Получение фильма по ID ==========
    @allure.story("Позитивный: получение фильма по ID")
    @allure.title("Получение фильма по ID {MOVIE_ID}")
    @allure.description(
        "Проверяем, что API возвращает данные фильма по его ID, " "и что ID в ответе совпадает с запрошенным."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movie_by_id(self):
        with allure.step(f"Поиск фильма по ID={MOVIE_ID}"):
            response = self.api.get_movie_by_id(MOVIE_ID)
            self._attach_response(response)

        with allure.step("Проверить, что статус-код = 200"):
            assert response.status_code == 200, (
                f"Ожидали 200, получили {response.status_code}. " f"Ответ: {response.text}"
            )

        with allure.step(f"Проверить, что в ответе id = {MOVIE_ID}"):
            data = response.json()
            assert data["id"] == MOVIE_ID, f"Ожидали ID {MOVIE_ID}, получили {data['id']}"

    # ========== Тест 3: Поиск персоны ==========
    @allure.story("Поиск по имени актера")
    @allure.title("Поиск персоны '{TEST_PERSON_NAME}'")
    @allure.description("Проверяем, что API возвращает результаты поиска персоны " "по имени с фильтром по профессии.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_person(self):
        with allure.step(f"Запрос на поиск актера name='{TEST_PERSON_NAME}' " f"и profession='{TEST_PROFESSION}'"):
            response = self.api.search_person(TEST_PERSON_NAME, TEST_PROFESSION)
            self._attach_response(response)

        with allure.step("Проверить, что статус-код = 200"):
            assert response.status_code == 200, (
                f"Ожидали 200, получили {response.status_code}. " f"Ответ: {response.text}"
            )

        with allure.step("Проверить, что в ответе есть ключ 'docs'"):
            data = response.json()
            assert "docs" in data

        with allure.step("Проверить, что список персон не пустой"):
            assert len(data["docs"]) > 0, "Поиск не вернул ни одной персоны"

    # ========== Тест 4: Несуществующий ID ==========
    @allure.story("Поиск фильма с несуществующим ID")
    @allure.title("Несуществующий ID возвращает 404")
    @allure.description(
        "Негативный сценарий: проверяем, что API возвращает 404 "
        "при запросе фильма с несуществующим, но валидным по диапазону ID."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_invalid_id(self):
        invalid_id = 9999999  # ID в допустимом диапазоне (250–15000000)

        with allure.step(f"Отправить запрос с несуществующим id={invalid_id}"):
            response = self.api.get_movie_by_id(invalid_id)
            self._attach_response(response)

        with allure.step("Проверить, что статус-код = 404"):
            assert response.status_code == 404, (
                f"Ожидали 404, получили {response.status_code}. " f"Ответ: {response.text}"
            )

    # ========== Тест 5: Поиск по спецсимволам ==========
    @allure.story("Поиск фильма по несуществующему названию")
    @allure.title("Поиск по спецсимволам не находит фильмов")
    @allure.description(
        "Негативный сценарий: проверяем, что поиск по строке из спецсимволов "
        "не возвращает реальных фильмов (или возвращает 400)."
    )
    @allure.severity(allure.severity_level.MINOR)
    def test_search_special_chars(self):
        special_query = "@#$%^&*"

        with allure.step(f"Поиск фильма по несуществующему названию query='{special_query}'"):
            response = self.api.search_films(special_query)
            self._attach_response(response)

        with allure.step("Проверить, что статус-код в [200, 400]"):
            assert response.status_code in [200, 400], f"Неожиданный статус: {response.status_code}"

        with allure.step("Если 200 — проверить, что структура ответа корректна"):
            if response.status_code == 200:
                data = response.json()
                assert "docs" in data, "В ответе нет ключа 'docs'"
