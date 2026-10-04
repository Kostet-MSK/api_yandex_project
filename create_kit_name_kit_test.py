import sender_stand_request
import data


# ---------------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------

def get_kit_body(name):
    """
    Возвращает копию шаблона kit_body с подставленным значением name.
    Копия нужна, чтобы не изменять исходный словарь в data.py.
    """
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body


def positive_assert(name):
    """
    Позитивная проверка: комплект должен успешно создаться (201),
    а поле name в ответе — совпадать с переданным значением.
    """
    kit_body = get_kit_body(name)                                # тело запроса с нужным name
    token = sender_stand_request.get_new_user_token()            # получаем свежий токен
    kit_response = sender_stand_request.post_new_client_kit(kit_body, token)

    assert kit_response.status_code == 201                       # код ответа 201
    assert kit_response.json()["name"] == name                   # name в ответе совпадает


def negative_assert(name):
    """
    Негативная проверка: комплект создать нельзя, ожидаем код 400.
    """
    kit_body = get_kit_body(name)
    token = sender_stand_request.get_new_user_token()
    kit_response = sender_stand_request.post_new_client_kit(kit_body, token)

    assert kit_response.status_code == 400                       # код ответа 400

def negative_assert_no_name(kit_body):
    """
    Негативная проверка для случая, когда ключ 'name' отсутствует в теле запроса.
    Ожидаем код ответа 400.
    """
    token = sender_stand_request.get_new_user_token()
    kit_response = sender_stand_request.post_new_client_kit(kit_body, token)

    assert kit_response.status_code == 400
# ---------------------------------------------------------------------------
# ТЕСТЫ
# ---------------------------------------------------------------------------

# Тест 1. Допустимое количество символов (1): name = "a" → 201
def test_create_kit_1_letter_in_name():
    positive_assert("a")


# Тест 2. Допустимое количество символов (511): name = 511 символов → 201
def test_create_kit_511_letter_in_name():
    positive_assert(
        "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
    )  # 511 символов


# Тест 3. Недопустимое количество символов (0): name = "" → 400
def test_create_kit_0_letter_in_name():
    negative_assert("")


# Тест 4. Недопустимое количество символов (512): name = 512 символов → 400
def test_create_kit_512_letter_in_name():
    negative_assert(
        "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"
    )  # 512 символов


# Тест 5. Разрешённые символы (английские буквы): name = "QWErty" → 201
def test_create_kit_EN_letter_in_name():
    positive_assert("QWErty")


# Тест 6. Разрешённые символы (русские буквы): name = "Мария" → 201
def test_create_kit_RU_letter_in_name():
    positive_assert("Мария")


# Тест 7. Разрешённые символы (спецсимволы): name = "\"№%@," → 201
def test_create_kit_special_symbol_in_name():
    positive_assert("\"№%@\",")


# Тест 8. Разрешённые символы (пробелы): name = "Человек и КО" → 201
def test_create_kit_space_in_name():
    positive_assert("Человек и КО")


# Тест 9. Разрешённые символы (цифры в виде строки): name = "123" → 201
def test_create_kit_number_in_name():
    positive_assert("123")


# Тест 10. Параметр name не передан в запросе: kit_body = {} → 400
def test_create_kit_no_name_in_body():
    negative_assert_no_name({})


# Тест 11. Неверный тип параметра (число): name = 123 (int) → 400
def test_create_kit_integer_name():
    negative_assert(123)