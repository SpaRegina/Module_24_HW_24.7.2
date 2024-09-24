from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

  status, result = pf.get_api_key(email, password)

  assert status == 200
  assert "key" in result

def test_get_all_pets_with_valid_key(filter=""):
  _, auth_key = pf.get_api_key(valid_email, valid_password)
  status, result = pf.get_list_of_pets(auth_key, filter)

  assert status == 200
  assert len(result["pets"]) > 0

def test_add_new_pet_with_valid_data(name="Рыжик", animal_type="Котик",
                                       age="1", pet_photo="images/ginger_cat.jpg"):

  pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
  _, auth_key = pf.get_api_key(valid_email, valid_password)

  status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

  assert status == 200
  assert result["name"] == name

def test_successful_delete_self_pet():

  _, auth_key = pf.get_api_key(valid_email, valid_password)
  _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

  if len(my_pets["pets"]) == 0:
    pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

  pet_id = my_pets["pets"][0]["id"]
  status, _ = pf.delete_pet(auth_key, pet_id)

  _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

  assert status == 200
  assert pet_id not in [pet["id"] for pet in my_pets["pets"]], "Pet ID is still in the list"

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("There is no my pets")

def test_create_pet_simple(name="Рыжик", animal_type="Котик", age="1"):

  _, auth_key = pf.get_api_key(valid_email, valid_password)

  status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

  assert status == 200
  assert result["name"] == name


def test_set_photo_pet(name="Рыжик", animal_type="Котик", age="1", pet_photo="images/ginger_cat.jpg"):

  pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

  _, auth_key = pf.get_api_key(valid_email, valid_password)

  _, my_pets = pf.get_list_of_pets(auth_key, filter="my_pets")

  if len(my_pets['pets']) > 0:
      pet_id = my_pets['pets'][0]['id']

      status, result = pf.set_photo_pet(auth_key, pet_id, pet_photo)

      assert status == 200
      assert result["name"] == name
  else:
      raise Exception("There are no pets to add a photo.")


# Тест с пустыми email и паролем
def test_get_api_key_with_empty_email_and_password():
    empty_email = ""
    empty_password = ""

    status, result = pf.get_api_key(empty_email, empty_password)

    assert status == 400 or status == 403, f"Ожидался код 400 или 403, но получен {status}. Ответ: {result}"


# Валидный адрес, невалидный пароль
def test_get_api_key_for_invalid_user(email=valid_email, password="invalid_password"):

      status, result = pf.get_api_key(email, password)
      assert status == 403


# Невалидный адрес, валидный пароль
def test_get_api_key_for_invalid_user(email="invalid_email", password=valid_password):

      status, result = pf.get_api_key(email, password)
      assert status == 403


# Невалидный адрес, невалидный пароль
def test_get_api_key_for_invalid_user(email="invalid_email", password="invalid_password"):

      status, result = pf.get_api_key(email, password)
      assert status == 403


# Тест на добавление питомца с несуществующим файлом фотографии
def test_add_pet_with_invalid_photo():
    invalid_pet_photo = os.path.join(os.path.dirname(__file__), "images/non_existent_photo.jpg")
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    try:
        status, result = pf.post_add_new_pet(auth_key, name="Рыжик", animal_type="Котик", age="1", pet_photo=invalid_pet_photo)
        assert False, "Ожидалось исключение FileNotFoundError"
    except FileNotFoundError:
        pass


# Тест на добавление питомца недействительным файлом фотографии
def test_set_photo_with_invalid_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    valid_pet_id = "valid_pet_id"
    invalid_pet_photo = "invalid_photo.jpg"  # Несуществующий файл

    try:
        status, result = pf.set_photo_pet(auth_key, valid_pet_id, invalid_pet_photo)
    except FileNotFoundError:
        status = "FileNotFoundError"

    assert status == "FileNotFoundError", f"Ожидалась ошибка FileNotFoundError, но получен {status}"


# Тест на добавление питомца пустым файлом фотографии
def test_set_photo_with_empty_photo_file():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    empty_pet_photo = os.path.join(os.path.dirname(__file__), "images/empty_photo.jpg")
    with open(empty_pet_photo, "wb") as f:
        pass

    valid_pet_id = "valid_pet_id"

    status, result = pf.set_photo_pet(auth_key, valid_pet_id, empty_pet_photo)

    assert status != 200, f"Ожидался код ошибки, но получен {status}. Ответ: {result}"


# Тест с неверным auth_key
def test_delete_pet_with_invalid_auth_key():
    invalid_auth_key = {"key": "invalid_key"}  # Некорректный ключ
    valid_pet_id = "valid_pet_id"  # Должен быть существующий ID питомца

    status, result = pf.delete_pet(invalid_auth_key, valid_pet_id)

    assert status == 403 or status == 401, f"Ожидался код 403 или 401, но получен {status}. Ответ: {result}"


# Тест с удалением питомца без pet_id
def test_delete_pet_without_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.delete_pet(auth_key, pet_id="")

    assert status == 404 or status == 400, f"Ожидался код 404 или 400, но получен {status}. Ответ: {result}"


# Тест с некорректным auth_key
def test_get_list_of_pets_with_invalid_auth_key():
    invalid_auth_key = {"key": "invalid_key"}
    filter_value = "my_pets"

    status, result = pf.get_list_of_pets(invalid_auth_key, filter_value)

    assert status == 403 or status == 401, f"Ожидался код 403 или 401, но получен {status}. Ответ: {result}"


