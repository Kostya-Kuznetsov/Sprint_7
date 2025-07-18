# 🛴 Scooter API Testing Project

Автоматизированные API тесты для сервиса  **ЯндексСамокат**.  
[API Documentation](qa-scooter.praktikum-services.ru/docs/)

![API Testing](https://img.shields.io/badge/scope-API%20testing-blue) 
![Python](https://img.shields.io/badge/python-3.7%2B-green)
![Pytest](https://img.shields.io/badge/pytest-7.4.3-orange)

## 📦 Зависимости

```text
allure-pytest==2.13.2
Faker==20.1.0
pytest==7.4.3
Install with:

bash
pip install -r requirements.txt
🗂 Test Coverage
Endpoints
/api/v1/orders	order_list.py	GET
/api/v1/orders	test_create_order.py	POST
/api/v1/courier	test_create_courier.py	POST
/api/v1/courier/login	test_login_courier.py	POST
🚀 Running Tests
Install dependencies:

bash
pip install allure-pytest Faker pytest
Execute tests with Allure reporting:

bash
pytest --alluredir=allure_results
Generate report:

bash
allure serve allure_results
