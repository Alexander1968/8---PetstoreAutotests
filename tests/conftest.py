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
