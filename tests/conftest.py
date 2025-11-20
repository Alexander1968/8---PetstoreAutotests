import pytest
from utils.api_client import PetStoreAPI
from py.xml import html

@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return PetStoreAPI()

# Фикстура с тестовыми данными питомца
@pytest.fixture
def pet_data():
    return {
        "id": 12345,
        "category": {
            "id": 1,
            "name": "dogs"
        },
        "name": "Rex",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 1,
                "name": "friendly"
            }
        ],
        "status": "available"
    }

# Фикстура с обновленными данными питомца
@pytest.fixture
def updated_pet_data():

    return {
        "id": 12345,
        "category": {
            "id": 1,
            "name": "dogs"
        },
        "name": "Rex Updated",
        "photoUrls": [
            "string_updated"
        ],
        "tags": [
            {
                "id": 1,
                "name": "very_friendly"
            }
        ],
        "status": "sold"
    }


# #############################################################
# class RussianHTMLReport:
#     def __init__(self):
#         self.translations = {
#             "Results": "Результаты",
#             "Summary": "Сводка",
#             "Test Report": "Отчет о тестировании",
#             "Environment": "Окружение",
#             "Passed": "Пройдено",
#             "Failed": "Провалено",
#             "Skipped": "Пропущено",
#             "XFailed": "Ожидаемо провалено",
#             "XPassed": "Неожиданно пройдено",
#             "Warnings": "Предупреждения",
#             "Error": "Ошибка",
#             "Duration": "Продолжительность",
#             "Source": "Источник"
#         }
#
#     def translate(self, text):
#         return self.translations.get(text, text)
#
# russian_report = RussianHTMLReport()
#
# def pytest_html_report_title(report):
#     report.title = "Отчет о тестировании"
#
# def pytest_html_results_table_header(cells):
#     cells.clear()
#     cells.extend([
#         html.th("Тест", class_="sortable"),
#         html.th("Результат", class_="sortable result"),
#         html.th("Продолжительность", class_="sortable"),
#         html.th("Описание")
#     ])
#
# def pytest_html_results_table_row(report, cells):
#     cells.clear()
#     cells.extend([
#         html.td(report.nodeid),
#         html.td(russian_report.translate(report.outcome.capitalize()),
#                 class_=f"col-result {report.outcome}"),
#         html.td(f"{getattr(report, 'duration', 0):.2f}s", class_="col-duration"),
#         html.td(getattr(report, 'description', ''), class_="col-description")
#     ])