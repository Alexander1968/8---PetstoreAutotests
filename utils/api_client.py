import requests
import json
############################################################################
#   Класс для работы с API PetStore
############################################################################
class PetStoreAPI:

    def __init__(self):
        self.base_url = "https://petstore.swagger.io/v2"
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    #########################################################################
    # HTTP-command ориентированная инкапсуляция
    #########################################################################
    # POST запрос
    def post(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)
        return response

    # GET запрос
    def get(self, endpoint):

        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response

    # PUT запрос
    def put(self, endpoint, data=None):

        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=data, headers=self.headers)
        return response

    # DELETE запрос
    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return response

    #########################################################################
    # Endpoints - ориентированная инкапсуляция
    #########################################################################
    # Получение питомца по ID
    def find_pet_by_id(self, pet_id):
        url = f"{self.base_url}/pet/{pet_id}"
        response = self.session.get(url)
        return response

    # Добавляем нового питомца
    def add_new_pet(self, pet_data):
        url = f"{self.base_url}/pet"
        response = self.session.post(url, json=pet_data)
        return response

    # Обнвляем питомца (по ID???)
    def update_existing_pet(self, pet_data):
        url = f"{self.base_url}/pet"
        response = self.session.put(url, json=pet_data)
        return response

    # Удаляем питомца по ID
    def delete_pet_by_id(self, pet_id):
        url = f"{self.base_url}/pet/{pet_id}"
        response = self.session.delete(url)
        return response