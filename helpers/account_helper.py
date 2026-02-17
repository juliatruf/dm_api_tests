import json
from json import JSONDecodeError
from retrying import retry

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={'login': login, 'password': password}
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"],
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        return

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"
        # Получение активационного токена
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен пользователя {login} не был получен"
        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'remember_me': remember_me
        }
        # Авторизация пользователя
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        return response

    def change_registered_user_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        # Изменение email зарегистрированного пользователя
        json_data = {
            'login': login,
            'password': password,
            'email': new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Email зарегистрированного пользователя не был изменен"
        # Проверка деактивации: попытка авторизации пользователя с неподтвержденным email
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, "Пользователь не деактивирован после смены email"
        # Получение активационного токена после смены email зарегистрированного пользователя
        token = self.get_activation_token_by_login(login)
        assert token is not None, f"Токен пользователя {login} не был получен"
        # Активация пользователя после смены email
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован после смены email"
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        # Получение письма из почтового сервера
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        for item in response.json()['items']:
            try:
                user_data = json.loads(item['Content']['Body'])
            except (JSONDecodeError, KeyError):
                continue
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
