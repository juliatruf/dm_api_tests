from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_put_v1_account_email():
    account_api = AccountApi(host='http://185.185.143.231:5051')
    login_api = LoginApi(host='http://185.185.143.231:5051')
    mailhog_api = MailhogApi(host='http://185.185.143.231:5025')

    login = 'juliatr_test5'
    email_initial = f'{login}@inbox.ru'
    email_updated = f'{login}@bk.ru'
    password = '123456789'

    # Регистрация пользователя
    json_data = {
        'login': login,
        'email': email_initial,
        'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не создан {response.json()}"

    # Получение письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получение активационного токена
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Изменение email зарегистрированного пользователя
    json_data = {
        'login': login,
        'password': password,
        'email': email_updated
    }
    response = account_api.put_v1_account_email(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Email зарегистрированного пользователя не был изменен"

    # Авторизация пользователя с неподтвержденным email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Пользователь не деактивирован после смены email"

    # Получение письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получение активационного токена после смены email зарегистрированного пользователя
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен пользователя {login} не был получен"

    # Активация пользователя после смены email
    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован после смены email"

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
