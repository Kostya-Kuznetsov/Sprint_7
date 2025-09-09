import requests
import allure
import pytest
from urls import *

@allure.description('Проверка создание заказа')
class TestCreateOrders:

    @allure.title("Проверяем создания заказа с разными вариантами цвета")
    # применяем параметризацию для цвета
    @pytest.mark.parametrize('colors', ['BLACK','GREY', ['BLACK','SILVER'], ''])
    def test_create_order(self, colors):
        payload = {
            "firstName": "Костя",
            "lastName": "Кузнецов",
            "address": "Москва, Клинская, 3",
            "metroStation": 7,
            "phone": "+7 999 888 98 98",
            "rentTime": 2,
            "deliveryDate": "2025-07-19",
            "comment": "В домофон не звонить",
            "color": [colors]
        }
        with allure.step(f"Создаём заказ с цветом`: {colors}"):
            response = requests.post(url_create_order, json=payload)
            assert response.status_code == 201, f"Ожидаемый статус 201, полученный {response.status_code}"
            assert 'track' in response.json(), f"Ожидаемый элемент в ответе 'track', полученный {response.json}"