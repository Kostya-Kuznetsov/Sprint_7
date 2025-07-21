import requests
import allure
from urls import *

class TestOrderList:
    @allure.title('Проверка получения списка заказа')
    def test_order_list(self):

        response = requests.get(url_create_order)
        assert response.status_code == 200, f"Ожидаемый статус 200, получен {response.status_code}"
        json_data = response.json()
        assert 'orders' in json_data, "В ответе отсутствует ключ 'orders'"
        assert len(json_data['orders']) > 0, "Список 'orders' пуст"
        assert 'id' in json_data['orders'][0], "В первом заказе отсутствует ключ 'id'"