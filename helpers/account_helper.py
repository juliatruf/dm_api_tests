import json
import time
from json import JSONDecodeError
from retrying import retry

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


class AccountHelper:
    # Константы для ключей в письмах MailHog
    TOKEN_KEY_ACTIVATION = 'ConfirmationLinkUrl'
    TOKEN_KEY_PASSWORD_RESET = 'ConfirmationLinkUri'

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
        self.auth_login = login
        response = self.user_login(login=login, password=password)
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def create_new_user(
            self,
            login: str,
            password: str,
            email: str,
            status_code: int = 201,
            error_message: str = None
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )
        # Регистрация пользователя без активации
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or f"Пользователь не создан {response.json()}")
        return response

    def activate_user(
            self,
            login: str,
            status_code: int = 200,
            error_message: str = None
    ):
        # Получение активационного токена
        start_time = time.time()
        token = self.get_token_by_login(login=login, token_key_name=self.TOKEN_KEY_ACTIVATION)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активационного токена превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"
        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # if status_code is not None:
        #     assert response.status_code == status_code, (
        #             error_message or "Пользователь не был активирован")
        return response

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        # Регистрация нового пользователя с активацией
        self.create_new_user(login=login, password=password, email=email)
        return self.activate_user(login=login)

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = False,
            status_code: int = 200,
            error_message: str = None
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        # Авторизация пользователя
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or "Пользователь не смог авторизоваться")
        if status_code == 200:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        return response

    def change_user_email(
            self,
            login: str,
            password: str,
            new_email: str,
            status_code: int = 200,
            error_message: str = None
    ):
        # Изменение email зарегистрированного пользователя
        json_data = {
            'login': login,
            'password': password,
            'email': new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or "Email зарегистрированного пользователя не был изменен")
        return response

    def reset_user_password(
            self,
            login: str,
            email: str,
            status_code: int = 200,
            error_message: str = None
    ):
        # Изменение пароля зарегистрированного пользователя
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or "Пароль зарегистрированного пользователя не был сброшен")
        return response

    def change_user_password(
            self,
            login: str,
            token: str,
            old_password: str,
            new_password: str,
            status_code: int = 200,
            error_message: str = None
    ):
        json_data = {
            'login': login,
            'token': token,
            'oldPassword': old_password,
            'newPassword': new_password
        }
        # Подтверждение смены пароля
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or "Пароль зарегистрированного пользователя не был изменен")
        return response

    def get_current_user_info(
            self,
            status_code: int = 200,
            error_message: str = None,
            **kwargs
    ):
        response = self.dm_account_api.account_api.get_v1_account(**kwargs)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or f"Ошибка при получении данных аккаунта! "
                                     f"Ожидали {status_code}, получили {response.status_code}. "
                                     f"Тело: {response.text}")
        return response

    def logout_current_session(
            self,
            status_code: int = 204,
            error_message: str = None,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or f"Ошибка при выходе из текущей сессии! "
                                     f"Ожидали {status_code}, получили {response.status_code}")
        return response

    def logout_all_sessions(
            self,
            status_code: int = 204,
            error_message: str = None,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
        if status_code is not None:
            assert response.status_code == status_code, (
                    error_message or f"Ошибка при выходе из всех сессий! "
                                     f"Ожидали {status_code}, получили {response.status_code}")
        return response


    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_by_login(
            self,
            login,
            token_key_name
    ):
        """Метод для поиска любого токена в письмах по имени ключа"""
        token = None
        # Получение письма из почтового сервера
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        # Извлечение токена письма
        for item in response.json()['items']:
            try:
                user_data = json.loads(item['Content']['Body'])
                user_login = user_data['Login']
                if user_login == login:
                    token = user_data[token_key_name].split('/')[-1]
            except (JSONDecodeError, KeyError, TypeError):
                continue
        return token
