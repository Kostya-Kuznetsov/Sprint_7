import pytest
import allure
import requests
from help_data import registration_courier, generate_random_string
from urls import *

@allure.description('Тестирование авторизации курьера')
class TestLoginCourier:

    @allure.title("Проверка авторизации курьера")
    def test_login_courier(self):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()
            # Достаем имя пользователя и пароль
            payload = {
                "login": login_pass.get('login'),
                "password": login_pass.get('password')
            }

        with allure.step("Авторизуемся под созданным курьером"):
            response = requests.post(url_courier_login, json=payload)

            assert response.status_code == 200, f"Ожидаемый статус 200, полученный {response.status_code}"

            response_data = response.json()
            assert  'id' in response_data, f"Ожидаемый в ответе 'id' курьера, нполученный {response.json()}"

            assert isinstance(response_data['id'], int)

    @pytest.mark.parametrize("payload_modifier, step_description", [
        (lambda creds: {"login": "", "password": creds.get('password')}, "Авторизуемся с пустым именем пользователя"),
        (lambda creds: {"login": creds.get('login'), "password": ""}, "Авторизуемся с пустым паролем"),
        (lambda creds: {"password": creds.get('password')}, "Авторизуемся без передачи поля 'login'"),
        (lambda creds: {"login": creds.get('login')}, "Авторизуемся без передачи поля 'password'"),
    ])
    @allure.title("Проверка появления ошибки при некорректных данных авторизации курьера")
    def test_courier_login_invalid(self, payload_modifier, step_description):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()

        payload = payload_modifier(login_pass)

        with allure.step(step_description):
            response = requests.post(url_courier_login, json=payload)
            assert response.status_code == 400, f"Ожидаемый статус 400, полученный {response.status_code}"
            assert response.json()['message'] == "Недостаточно данных для входа", \
                f"Ожидаемое сообщение 'Недостаточно данных для входа', полученное {response.json()['message']}"

    @pytest.mark.parametrize("login_value, password_value, allure_title, step_description", [
        (lambda creds: generate_random_string(7),  # некорректный логин
         lambda creds: creds.get('password'),
         "Проверка появления ошибки при авторизации с некорректным логином",
         "Авторизуемся с некорректным именем пользователя"),

        (lambda creds: creds.get('login'),  # некорректный пароль
         lambda creds: generate_random_string(7),
         "Проверка появления ошибки при авторизации с некорректным паролем",
         "Авторизуемся с некорректным паролем"),

        (lambda creds: generate_random_string(7),  # некорректный логин и пароль
         lambda creds: generate_random_string(7),
         "Проверка появления ошибки при авторизации с некорректным именем пользователя и паролем",
         "Авторизуемся с некорректным именем пользователя и паролем"),
    ])
    @allure.title("{allure_title}")
    def test_courier_login_invalid_credentials(self, login_value, password_value, allure_title, step_description):
        with allure.step("Создаём нового курьера"):
            login_pass = registration_courier()

        payload = {
            "login": login_value(login_pass) if callable(login_value) else login_value,
            "password": password_value(login_pass) if callable(password_value) else password_value,
        }

        with allure.step(step_description):
            response = requests.post(url_courier_login, json=payload)
            assert response.status_code == 404, f"Ожидаемый статус 404, но полученный {response.status_code}"
            assert response.json()['message'] == "Учетная запись не найдена", \
                f"Ожидаемое сообщение 'Учетная запись не найдена', полученное сообщение {response.json()['message']}"