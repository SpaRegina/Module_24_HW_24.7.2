import requests

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url + "api/key", headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url + "api/pets", headers=headers, params=filter)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        headers = {"auth_key": auth_key["key"]}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }
        files = {
            "pet_photo": open(pet_photo, "rb")
        }
        res = requests.post(self.base_url + "api/pets", headers=headers, data=data, files=files)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet(self, auth_key, pet_id):

        headers = {"auth_key": auth_key["key"]}

        res = requests.delete(self.base_url + f"api/pets/{pet_id}", headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        headers = {"auth_key": auth_key["key"]}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }

        res = requests.put(self.base_url + f"api/pets/{pet_id}", headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def create_pet_simple(self, auth_key, name, animal_type, age):
        headers = {"auth_key": auth_key["key"]}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }

        res = requests.post(self.base_url + f"api/create_pet_simple", headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def set_photo_pet(self, auth_key, pet_id, pet_photo):
        headers = {"auth_key": auth_key["key"]}
        data = {
        "pet_id": pet_id
        }
        files = {
        "pet_photo": open(pet_photo, "rb")
        }

        res = requests.post(self.base_url + f"api/pets/set_photo/{pet_id}", headers=headers, data=data, files=files)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

