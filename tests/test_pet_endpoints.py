import pytest
import time


# Класс для тестирования эндпоинтов питомцев
class TestPetEndpoints:

    ###############################################################################################
    # Тест для создания нового питомца (POST /pet)
    #
    # Шаги:
    # 1. Отправляем POST запрос для создания питомца
    # 2. Проверяем статус код ответа
    # 3. Проверяем, что питомец создан с правильными данными
    ###############################################################################################
    def test_create_pet(self, api_client, pet_data):
        print("\n=== Тест создания питомца ===")

        # Шаг 1: Создание питомца
        print(pet_data)
        response = api_client.post("/pet", pet_data)

        # Шаг 2: Проверка статус кода
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        print("✓ Статус код 200 - OK")

        # Шаг 3: Проверка данных ответа
        response_data = response.json()
        assert response_data["id"] == pet_data["id"], "ID питомца не совпадает"
        assert response_data["name"] == pet_data["name"], "Имя питомца не совпадает"
        assert response_data["status"] == pet_data["status"], "Статус питомца не совпадает"
        print("✓ Данные питомца корректны")

        print("✅ Тест создания питомца пройден успешно")

        return response_data["id"]

    ###############################################################################################
    # Тест для получения информации о питомце по ID (GET /pet/{petId})
    #
    # Шаги:
    # 1. Создаем питомца
    # 2. Получаем питомца по ID
    # 3. Проверяем статус код и данные
    ###############################################################################################
    def test_get_pet_by_id(self, api_client, pet_data):
        print("\n=== Тест получения питомца по ID ===")

        # Шаг 1: Создание питомца
        create_response = api_client.post("/pet", pet_data)
        pet_id = create_response.json()["id"]
        print(f"✓ Создан питомец с ID: {pet_id}")

        # Шаг 2: Получение питомца по ID
        response = api_client.get(f"/pet/{pet_id}")

        # Шаг 3: Проверка статус кода
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        print("✓ Статус код 200 - OK")

        # Проверка данных
        response_data = response.json()
        assert response_data["id"] == pet_id, "ID питомца не совпадает"
        assert response_data["name"] == pet_data["name"], "Имя питомца не совпадает"
        print("✓ Данные питомца корректны")

        print("✅ Тест получения питомца по ID пройден успешно")

    ###############################################################################################
    # Тест для обновления информации о существующем питомце (PUT /pet)
    #
    # Шаги:
    # 1. Создаем питомца
    # 2. Обновляем данные питомца
    # 3. Проверяем, что данные обновились
    ###############################################################################################
    def test_update_pet(self, api_client, pet_data, updated_pet_data):
        print("\n=== Тест обновления питомца ===")

        # Шаг 1: Создание питомца
        create_response = api_client.post("/pet", pet_data)
        pet_id = create_response.json()["id"]
        print(f"✓ Создан питомец с ID: {pet_id}")

        # Шаг 2: Обновление питомца
        response = api_client.put("/pet", updated_pet_data)

        # Проверка статус кода
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        print("✓ Статус код 200 - OK")

        # Шаг 3: Проверка обновленных данных
        response_data = response.json()
        assert response_data["name"] == updated_pet_data["name"], "Имя не обновилось"
        assert response_data["status"] == updated_pet_data["status"], "Статус не обновился"
        print("✓ Данные питомца успешно обновлены")

        print("✅ Тест обновления питомца пройден успешно")

    ###############################################################################################
    # Тест для удаления питомца (DELETE /pet/{petId})
    #
    # Шаги:
    # 1. Создаем питомца
    # 2. Удаляем питомца
    # 3. Проверяем, что питомец удален
    # 4. Пытаемся получить удаленного питомца
    ###############################################################################################
    def test_delete_pet(self, api_client, pet_data):
        print("\n=== Тест удаления питомца ===")

        # Шаг 1: Создание питомца
        create_response = api_client.post("/pet", pet_data)
        pet_id = create_response.json()["id"]
        print(f"✓ Создан питомец с ID: {pet_id}")

        # Шаг 2: Удаление питомца
        delete_response = api_client.delete(f"/pet/{pet_id}")

        # Проверка статус кода удаления
        assert delete_response.status_code == 200, f"Ожидался статус 200, получен {delete_response.status_code}"
        print("✓ Статус код 200 при удалении - OK")

        # Шаг 3: Проверка сообщения об удалении
        delete_data = delete_response.json()
        assert delete_data["message"] == str(pet_id), "Сообщение об удалении не содержит ID питомца"
        print("✓ Сообщение об удалении корректно")

        # Шаг 4: Попытка получить удаленного питомца
        get_response = api_client.get(f"/pet/{pet_id}")
        assert get_response.status_code == 404, f"Ожидался статус 404, получен {get_response.status_code}"
        print("✓ Питомец действительно удален (статус 404)")

        print("✅ Тест удаления питомца пройден успешно")

    ###############################################################################################
    # Тест для проверки получения несуществующего питомца
    ###############################################################################################
    def test_get_nonexistent_pet(self, api_client):
        print("\n=== Тест получения несуществующего питомца ===")

        # Пытаемся получить питомца с несуществующим ID
        nonexistent_id = 999999999
        response = api_client.get(f"/pet/{nonexistent_id}")

        # Проверяем, что получаем ошибку 404
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        print("✓ Статус код 404 для несуществующего питомца - OK")

        response_data = response.json()
        assert "message" in response_data, "В ответе нет сообщения об ошибке"
        print("✓ Получено сообщение об ошибке")

        print("✅ Тест получения несуществующего питомца пройден успешно")


###############################################################################################
#    Комплексный тест полного жизненного цикла питомца
###############################################################################################
def test_complete_pet_lifecycle(api_client, pet_data, updated_pet_data):
    print("\n" + "=" * 50)
    print("КОМПЛЕКСНЫЙ ТЕСТ: Полный жизненный цикл питомца")
    print("=" * 50)

    # Создаем экземпляр тестового класса
    test_class = TestPetEndpoints()

    try:
        # 1. Создание питомца
        print("\n1. СОЗДАНИЕ ПИТОМЦА")
        pet_id = test_class.test_create_pet(api_client, pet_data)

        # Небольшая пауза между запросами
        time.sleep(1)

        # 2. Получение питомца
        print("\n2. ПОЛУЧЕНИЕ ПИТОМЦА")
        test_class.test_get_pet_by_id(api_client, pet_data)

        time.sleep(1)

        # 3. Обновление питомца
        print("\n3. ОБНОВЛЕНИЕ ПИТОМЦА")
        test_class.test_update_pet(api_client, pet_data, updated_pet_data)

        time.sleep(1)

        # 4. Удаление питомца
        print("\n4. УДАЛЕНИЕ ПИТОМЦА")
        test_class.test_delete_pet(api_client, updated_pet_data)

        time.sleep(1)

        # 5. Проверка несуществующего питомца
        print("\n5. ПРОВЕРКА НЕСУЩЕСТВУЮЩЕГО ПИТОМЦА")
        test_class.test_get_nonexistent_pet(api_client)

        print("\n" + "=" * 50)
        print("✅ ВСЕ ТЕСТЫ ЖИЗНЕННОГО ЦИКЛА ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Ошибка в комплексном тесте: {e}")
        raise
