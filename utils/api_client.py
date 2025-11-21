import requests
import json
############################################################################
#   Класс для работы с API PetStore
############################################################################
class PetStoreAPI:

    def __init__(self):
        self.base_url = "https://petstore.swagger.io/v2"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

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