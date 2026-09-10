import pytest
import allure
from pages.api_page import ApiPage


@pytest.fixture
def api_page():
    return ApiPage()


@allure.feature("Поиск товаров")
@allure.story("API")
@allure.title("Поиск по автору")
@pytest.mark.positive
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("author", [
    "Пушкин",
    "Салтыков-Щедрин",
    "Scott",
])
def test_search_by_different_authors(api_page, author):
    with allure.step("Отправляем запрос на поиск книг по автору"):
        response = api_page.search_goods(213, author)
    with allure.step("Проверяем статус-код"):
        assert response.status_code == 200, "Ожидается статус код 200"
    with allure.step("Проверяем, что есть результаты поиска"):
        response_data = response.json()
        total_results = response_data['data']['relationships']['products']['meta']['pagination']['total']
        assert total_results > 0, f"Ожидались результаты поиска, но найдено: {total_results}"
    with allure.step("Проверяем релевантность поиска"):
        search_phrase = response_data['data']['attributes']['transformedPhrase']
        assert search_phrase.lower() == author.lower(), f"Поисковый запрос не совпадает: {search_phrase}"
