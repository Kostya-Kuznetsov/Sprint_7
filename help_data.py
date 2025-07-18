import string
import random
import requests
from urls import *

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_random_login_password_name():

    login_pass = {}

    # генерируем логин, пароль, имя курьера
    login_pass['login'] = generate_random_string(7)
    login_pass['password'] = generate_random_string(7)
    login_pass['first_name'] = generate_random_string(7)

    return login_pass

def registration_courier():
    login_pass = generate_random_login_password_name()
    requests.post(url_create_courier, data=login_pass)
    return login_pass