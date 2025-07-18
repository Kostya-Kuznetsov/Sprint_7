import requests
import allure
from urls import *

class TestOrderList:
    @allure.title('Проверка получения списка заказа')
    def test_order_list(self):

        response = requests.get(url_create_order)
        assert response.status_code == 200, f"Ожидаемый статус 200, полученный {response.status_code}"