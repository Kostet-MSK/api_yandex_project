import data
import requests
import configuration


def post_new_user(body):
    """
    Отправляет POST-запрос на создание нового пользователя.
    :param body: тело запроса (словарь) с данными пользователя
    :return: объект Response
    """
    return requests.post(
        configuration.USER_CREATE,
        headers=data.headers,
        json=body
    )


def get_new_user_token():
    """
    Создаёт нового пользователя и возвращает его authToken.
    Токен нужен для авторизации при создании комплекта.
    :return: строка authToken
    """
    response = post_new_user(data.user_body)
    return response.json()["authToken"]


def post_new_client_kit(kit_body, auth_token):
    """
    Отправляет POST-запрос на создание комплекта пользователя.
    :param kit_body: тело запроса (словарь) с именем комплекта
    :param auth_token: строка authToken для заголовка Authorization
    :return: объект Response
    """
    headers = {
        "Authorization": auth_token,          
        "Content-Type": "application/json"
    }

    return requests.post(
        configuration.USER_KIT,
        headers=headers,
        json=kit_body                          
    )