import pytest
import requests
from help_data import generate_random_login_password_name
from urls import url_create_courier, url_courier_login, url_delete_courier

@pytest.fixture
def courier():
    # Создаём курьера
    payload = generate_random_login_password_name()
    response = requests.post(url_create_courier, data=payload)
    assert response.status_code == 201, f"Не удалось создать курьера, статус {response.status_code}"

    yield payload

    # После теста — удаляем курьера
    login = payload['login']
    password = payload['password']

    # Логинимся, чтобы получить id
    login_response = requests.post(url_courier_login, data={'login': login, 'password': password})
    if login_response.status_code == 200:
        courier_id = login_response.json().get('id')
        if courier_id:
            # Формируем url удаления с id
            delete_url = url_delete_courier.replace(':id', str(courier_id))
            delete_response = requests.delete(delete_url)
            assert delete_response.status_code == 200, f"Не удалось удалить курьера, статус {delete_response.status_code}"
