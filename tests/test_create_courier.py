import allure
import requests
from help_data import generate_random_string, generate_random_login_password_name
from urls import *

@allure.description('Тестирование создания курьера')
class TestCreateCourier:

    @allure.title('Создаем нового курьера, c обязательными полями')
    def test_create_new_courier(self):
        payload = generate_random_login_password_name()
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 201, f"Ожидаемый статус 201, полученный {response.status_code}"
        assert response.json() == {'ok': True}

    @allure.title('Проверка, появления ошибки при регистрации уже существующего в системе курьера')
    def test_cant_create_two_identical_couriers(self):
        with allure.step("Создание курьера с уникальными данными"):
            payload = generate_random_login_password_name()
            response = requests.post(url_create_courier, data=payload)
            assert response.status_code == 201, f"Ожидаемый статус 201, полученный {response.status_code}"

        with allure.step("Запрос на создание курьера с данными уже зарегистрированного курьера"):
            response2 = requests.post(url_create_courier, data=payload)
            assert response2.status_code == 409, f"Ожидаемый статус 409, полученный {response.status_code}"
            assert response2.json()['message'] == "Этот логин уже используется. Попробуйте другой.", \
                f"Ожидаемое сообщение'Этот логин уже используется', полученное сообщение {response.json()['message']}"

    @allure.title('Проверка появления ошибки при регистрации без логина')
    def test_registration_without_a_login_failed(self):
        payload = {
        'login': '',
        'password': generate_random_string(7),
        'firstName': generate_random_string(7)
        }
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 400, f"Ожидаемый статус 400, полученный {response.status_code}"
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи", \
            f"Ожидаемое сообщение 'Недостаточно данных для создания учетной записи', полученное сообщение  {response.json()['message']}"

    @allure.title('Проверка появления ошибки при регистрации без пароля')
    def test_registration_without_a_password_failed(self):
        payload = {
        'login': generate_random_string(7),
        'password': '',
        'firstName': generate_random_string(7)
        }
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 400, f"Ожидаемый статус 400, полученный {response.status_code}"
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи", \
            f"Ожидаемое сообщение 'Недостаточно данных для создания учетной записи', полученное сообщение  {response.json()['message']}"

    @allure.title('Проверка успешной регистрации с пустым поле Имя')
    def test_registration_without_a_first_name(self):
        payload = {
        'login': generate_random_string(7),
        'password': generate_random_string(7),
        'firstName': ''
        }
        response = requests.post(url_create_courier, data=payload)
        assert response.status_code == 201, f"Ожидаемый статус 201, полученный {response.status_code}"
        assert response.json() == {'ok': True}

    @allure.title('Проверка появления ошибки при создании курьера с таким же логином')
    def test_error_when_creating_courier_with_existing_login(self):
        with allure.step("Создание курьера с уникальными данными"):
            login_pass = generate_random_login_password_name()

            response = requests.post(url_create_courier, data=login_pass)
            assert response.status_code == 201, f"Ожидаемый статус 201, полученный {response.status_code}"

        with allure.step("Создание курьера с существующим логином"):
            payload = {
                "login": login_pass.get('login'),
                "password": generate_random_string(7),
                "firstName": generate_random_string(7)
            }
            response2 = requests.post(url_create_courier, data=payload)
            assert response2.status_code == 409, f"Ожидаемый статус 409, полученный {response.status_code}"
            assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."