import pytest
from utils.api_client import PetStoreAPI

# Глобальные идентификаторы
ID = 777777
CATEGORY_ID = 777
CATEGORY_NAME = "crocodiles"

@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return PetStoreAPI()

# Фикстура с тестовыми данными питомца
@pytest.fixture
def pet_data():
    return {
        "id": ID,
        "category": {
            "id": CATEGORY_ID,
            "name": CATEGORY_NAME,
        },
        "name": "Raptor Rex",
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
        "id": ID,
        "category": {
            "id": CATEGORY_ID,
            "name": CATEGORY_NAME,
        },
        "name": "Raptor Rex Updated",
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
