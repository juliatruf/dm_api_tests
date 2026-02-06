import requests


def test_post_v1_account():
    # Регистрация пользователя

    login = 'juliat_test'
    email = f'{login}@mail.ru'
    password = '1233456789'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получение письма из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # Получение активационоого токена
    ...

    # Активация пользователя

    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://185.185.143.231:5051/v1/account/2bf12c78-c18d-4efb-a111-f8de56a9be4b',
                            headers=headers)
    print(response.status_code)
    print(response.text)

    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
