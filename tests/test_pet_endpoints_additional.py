import pytest
import time

from tests.conftest import pet_data


# Класс для тестирования эндпоинтов питомцев
class TestPetEndpointsAdditional:
####################################################################################################
#                                   Позитивные тесты
####################################################################################################
    ###############################################################################################
    # Тест для создания нового питомца (POST /pet)
    # Тип: позитивный
    # Шаги:
    # 1. Отправляем POST запрос для создания питомца
    # 2. Проверяем статус код ответа
    # 3. Проверяем, что питомец создан с правильными данными
    ###############################################################################################
    @pytest.mark.positive
    def test_create_pet(self, api_client, pet_data):
        print("\n=== Позитивный тест создания питомца ===")
        # print(pet_data)

        # Шаг 1: Создание питомца
        response = api_client.add_new_pet(pet_data)

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
        #return response_data["id"]
        return None

    ###############################################################################################
    # Тест для получения информации о питомце по ID (GET /pet/{petId})
    # Тип: позитивный
    # Шаги:
    # 1. Создаем питомца
    # 2. Получаем питомца по ID
    # 3. Проверяем статус код и данные
    ###############################################################################################
    @pytest.mark.positive
    def test_get_pet_by_id(self, api_client, pet_data):
        print("\n=== Тест получения питомца по ID ===")

        # Шаг 1: Создание питомца
        response = api_client.add_new_pet(pet_data)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        pet_id = response.json()["id"]
        print(f"✓ Создан питомец с ID: {pet_id}")

        # Шаг 2: Получение питомца по ID
        response = api_client.find_pet_by_id(pet_id)

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
    # Тип: позитивный
    # Шаги:
    # 1. Создаем питомца POST
    # 2. Обновляем данные питомца PUT
    # 3. Проверяем, что данные обновились
    ###############################################################################################
    @pytest.mark.positive
    def test_update_pet(self, api_client, pet_data, updated_pet_data):
        print("\n=== Тест обновления питомца ===")

        # Шаг 1: Создание питомца
        response = api_client.add_new_pet(pet_data)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        pet_id = response.json()["id"]
        print(f"✓ Создан питомец с ID: {pet_id}")

        # Шаг 2: Обновление питомца
        response = api_client.update_existing_pet(updated_pet_data)
        # Проверка статус кода
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        print("✓ Статус код 200 - OK")

        # Шаг 3: Проверка обновленных данных
        response_data = response.json()
        assert response_data["name"] == updated_pet_data["name"], "Имя обновилось"
        assert response_data["status"] == updated_pet_data["status"], "Статус обновился"
        assert response_data["photoUrls"] == updated_pet_data["photoUrls"], "Фото обновилось"

        print("✓ Данные питомца успешно обновлены")
        print("✅ Тест обновления питомца пройден успешно")

    ###############################################################################################
    # Тест для удаления питомца (DELETE /pet/{petId})
    # Тип: позитивный
    # Шаги:
    # 1. Создаем питомца
    # 2. Удаляем питомца
    # 3. Проверяем, что питомец удален
    # 4. Пытаемся получить удаленного питомца
    ###############################################################################################
    @pytest.mark.positive
    def test_delete_pet(self, api_client, pet_data):
        print("\n=== Тест удаления питомца ===")

        # Шаг 1: Создание питомца
        response = api_client.add_new_pet(pet_data)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        pet_id = response.json()["id"]
        print(f"✓ Создан питомец с ID: {pet_id}")

        # Шаг 2: Удаление питомца
        response = api_client.delete_pet_by_id(pet_id)

        # Проверка статус кода удаления
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        print("✓ Статус код 200 при удалении - OK")

        # Шаг 3: Проверка сообщения об удалении
        delete_data = response.json()
        assert delete_data["message"] == str(pet_id), "Сообщение об удалении не содержит ID питомца"
        print("✓ Сообщение об удалении корректно")

        # Шаг 4: Попытка получить удаленного питомца
        response = api_client.find_pet_by_id(pet_id)
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        print("✓ Питомец действительно удален (статус 404)")

        print("✅ Тест удаления питомца пройден успешно")


####################################################################################################
#                                   Негативные тесты
####################################################################################################

    ###############################################################################################
    # Тест для проверки получения несуществующего питомца
    # Тип: негативный
    # Шаги:
    # 1. Пытаемся получить питомца с несуществующим id
    # 2. Проверяем, что статус-код ответа 404
    # 3. Прверяем, что в ответе нет сообщения об ошибке
    ###############################################################################################
    @pytest.mark.negative
    def test_get_nonexistent_pet(self, api_client):
        print("\n=== Тест получения несуществующего питомца ===")

        # Пытаемся получить питомца с несуществующим ID
        nonexistent_id = 999999999
        # Удаляем питомца на всякий случай
        api_response = api_client.delete_pet_by_id (nonexistent_id)
        # Запрашиваем питомца, коотрого мы только-что удалили
        response = api_client.find_pet_by_id(nonexistent_id)

        # Проверяем, что получаем ошибку 404
        exp_response = {"status_code" : 404, "type": "error", "message":"Pet not found"}
        assert response.status_code == exp_response["status_code"], f"Ожидался статус {exp_response["status_code"]}, получен {response.status_code}"
        # Проверка данных
        response_data = response.json()
        assert response_data["type"] == exp_response["type"], f"Ожидался type {exp_response["type"]}, получен {response_data["type"]}"
        assert response_data["message"] == exp_response["message"], f"Ожидался message '{exp_response["message"]}', получен {response_data["message"]}"
        print("✓ Статус код 404 для несуществующего питомца - OK")

        response_data = response.json()
        assert "message" in response_data, "В ответе нет сообщения об ошибке"
        print("✓ Получено сообщение об ошибке")

        print("✅ Тест получения несуществующего питомца пройден успешно")

        ###############################################################################################
        # Тест для обновления информации несуществующего питомце (PUT /pet)
        # Тип: негативный
        # Шаги:
        # 1. Удаляем питомца с большим id на всякий случай
        # 1. Обновляем данные несуществующего питомца PUT
        # 2. Проверяем, что вернулась ошибка 400 или 404
        ###############################################################################################
    @pytest.mark.negative
    def test_update_nonexistence_pet(self, api_client, pet_data):
        print("\n=== Тест обновления несуществующего питомца ===")
        nonexistent_id = 999999999

        # Удаляем питомца на всякий случай
        api_client.delete_pet_by_id(nonexistent_id)
        time.sleep(0.1)  # Задержка на всякий случай

        # Шаг 2: Обновление питомца которого только-что удалили
        pet_data['id'] = nonexistent_id
        response = api_client.update_existing_pet(pet_data)
        # Проверка статус кода
        assert response.status_code in [400, 404, 405], f"Ожидался статус 400, 404, 405получен {response.status_code}"
        print("✓ Статус код [400, 404, 405] - OK")

        print("✓ Данные питомца не обновлены")
        print("✅ Тест обновления питомца пройден успешно")

    ###############################################################################################
    # Тест для удаления несуществующего питомца (DELETE /pet/{petId})
    # Тип: егативный
    # Шаги:
    # 1. Удаляем питомца с большим Id на всякий случай
    # 2. Пытаемся удалить питомца с этим Id еще раз
    # 3. Проверяем, что возвращается [400, 404]
    ###############################################################################################
    @pytest.mark.negative
    def test_delete_nonexistent_pet(self, api_client, pet_data):
        print("\n=== Тест удаления несуществующего питомца ===")
        nonexistent_id = 999999999
        # Шаг 1: Удаляем питомца с болшим Id на всякий случай
        api_client.delete_pet_by_id(nonexistent_id)
        time.sleep(0.1) # Задержка на всякий случай
        #  2. Пытаемся удалить питомца с этим Id еще раз
        delete_response = api_client.delete_pet_by_id(nonexistent_id)

        # 3. Проверяем, что возвращается [400, 404]
        assert delete_response.status_code in [400, 404], f"Ожидался статус [400, 404], получен {delete_response.status_code}"
        print(f"✓ Статус код {delete_response.status_code} при удалении - OK")

        print("✅ Тест удаления несуществующего питомца пройден успешно")

    ###############################################################################################
    # Тест для проверки получения несуществующего питомца, с использованием параметризации
    # Тип: негативный
    # Шаги:
    # 1. Пытаемся получить питомца с id==0
    # 2. Пытаемся получить питомца с id==-1
    # 3. Пытаемся получить питомца с id=="invalid_string"
    # 4. Пытаемся получить питомца с id==""
    # 5. Пытаемся получить питомца с id==None
    # 6. Пытаемся получить питомца с id==999999999999999
    # Каждый раз анализируем код возврата
    ###############################################################################################
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_id, expected_status", [
        (0, [404]),  # нулевой ID
        (-1, [404]),  # отрицательный ID
        ("invalid_string", [400, 404]),  # строка вместо числа
        ("", [400, 405]),  # пустая строка
        (None, [400, 404]),  # None значение
        (999999999999999, [404]),  # очень большой ID
    ])
    def test_get_invalid_pet_ids(self, api_client, invalid_id, expected_status):
        response = api_client.find_pet_by_id(invalid_id)
        assert response.status_code in expected_status

    ###############################################################################################
    # Тест для проверки создания питомца, с неправильными параметрами
    # Тип: негативный
    # Шаги:
    # 1. Пытаемся создать питомца с id=="invalid_id"
    ###############################################################################################
    @pytest.mark.negative
    def test_create_pet_invalid_id_as_string(self, api_client):

        invalid_data = {
            "id": "invalid_id",  # строка вместо числа
            "name": "name",
            "status": "sold"
        }

        response = api_client.update_existing_pet(invalid_data)
        # Ожидаем ошибку валидации
        assert response.status_code in [400, 405], "Ожидалась ошибка валидации"



###############################################################################################
    # Тест для создания нового питомца с неверными данными (POST /pet)
    # Тип: негативный
    # Шаги:
    # 1. Отправляем POST запрос для создания питомца
    # 2. Проверяем статус код ответа
    # 3. Проверяем, что питомец НЕ создан
    ###############################################################################################
    @pytest.mark.negative
    def test_create_pet_with_bad_id_as_string(self, api_client, pet_data):
        print("\n=== Негативный тест создания питомца ===")

        # Шаг 1: Создание питомца
        #print(pet_data)
        pet_data["id"] = "bad_id"
        response = api_client.add_new_pet(pet_data)

        # Шаг 2: Проверка статус кода
        assert response.status_code in [405], f"Ожидался статус 405, получен {response.status_code}"
        print("✓ Статус код 405 - OK")
        return None

####################################################################################################
#                                   Smoke тесты
####################################################################################################
###############################################################################################
#    Комплексный тест полного жизненного цикла питомца
###############################################################################################
@pytest.mark.smoke
def test_complete_pet_lifecycle(api_client, pet_data, updated_pet_data):
    print("\n" + "=" * 50)
    print("КОМПЛЕКСНЫЙ ТЕСТ: Полный жизненный цикл питомца")
    print("=" * 50)

    # Создаем экземпляр тестового класса
    test_class = TestPetEndpointsAdditional()

    try:
        # 1. Создание питомца
        print("\n1. СОЗДАНИЕ ПИТОМЦА")
        test_class.test_create_pet(api_client, pet_data)

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
        # print("\n5. ПРОВЕРКА НЕСУЩЕСТВУЮЩЕГО ПИТОМЦА")
        # test_class.test_get_nonexistent_pet(api_client)

        print("\n" + "=" * 50)
        print("✅ ВСЕ ТЕСТЫ ЖИЗНЕННОГО ЦИКЛА ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Ошибка в комплексном тесте: {e}")
        raise
