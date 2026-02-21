import json
import time
from json import JSONDecodeError

from retrying import retry

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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
        self.auth_login = login
        response = self.user_login(login=login, password=password)
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def create_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )
        # Регистрация пользователя без активации
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, "Пользователь не создан"
        return response

    def activate_user(
            self,
            login: str,
            validate_response: bool = True
    ):
        # Получение активационного токена
        start_time = time.time()
        token = self.get_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активационного токена превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"
        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(
            token=token,
            validate_response=validate_response
        )
        return response

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str,
            validate_response: bool = True
    ):
        # Регистрация нового пользователя с активацией
        self.create_new_user(login=login, password=password, email=email)
        return self.activate_user(login=login, validate_response=validate_response)

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = False
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
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        return response

    def change_user_email(
            self,
            login: str,
            password: str,
            email: str,
            validate_response: bool = True
    ):
        # Изменение email зарегистрированного пользователя
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(
            change_email=change_email,
            validate_response=validate_response
        )
        return response

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str,
            validate_response: bool = True
    ):
        # Получение авторизационного токена
        # token = self.user_login(login=login, password=old_password)
        auth_response = self.user_login(login=login, password=old_password, validate_response=False)
        auth_token = auth_response.headers["x-dm-auth-token"]
        # Сброс пароля (генерация токена сброса)
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(
            reset_password=reset_password,
            validate_response=validate_response,
            headers={"x-dm-auth-token": auth_token}
        )
        # Получение токена сброса из почты
        reset_token = self.get_token_by_login(login=login, token_type="reset")
        # Подтверждение смены пароля
        change_password = ChangePassword(
            login=login,
            old_password=old_password,
            new_password=new_password,
            token=reset_token
        )
        response = self.dm_account_api.account_api.put_v1_account_password(
            change_password=change_password,
            validate_response=validate_response
        )
        return response

    def get_current_user_info(
            self,
            validate_response: bool = True,
            **kwargs
    ):
        response = self.dm_account_api.account_api.get_v1_account(
            validate_response=validate_response,
            **kwargs
        )
        # assert response.status_code == 200, "Не удалось получить данные текущего пользователя"
        return response

    def logout_current_session(
            self,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        assert response.status_code == 204, (f"Ошибка при выходе из текущей сессии! "
                                             f"Ожидали 204, получили {response.status_code}")
        return response

    def logout_all_sessions(
            self,
            **kwargs
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
        assert response.status_code == 204, (f"Ошибка при выходе из всех сессий! "
                                             f"Ожидали 204, получили {response.status_code}")
        return response


    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_by_login(
            self,
            login,
            token_type="activation"
    ):
        """
        Получение токена активации или сброса пароля
        Args:
            login: логин пользователя
            token_type: тип токена (activation или reset)
        Returns:
            токен активации или сброса пароля
        """
        token = None
        # Получение письма из почтового сервера
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        # Извлечение токена письма
        for item in response.json()['items']:
            try:
                user_data = json.loads(item['Content']['Body'])
                user_login = user_data['Login']
                activation_token = user_data.get("ConfirmationLinkUrl")
                reset_token = user_data.get("ConfirmationLinkUri")
                if user_login == login and activation_token and token_type == "activation":
                    token = activation_token.split("/")[-1]
                elif user_login == login and reset_token and token_type == "reset":
                    token = reset_token.split("/")[-1]
            except (JSONDecodeError, KeyError, TypeError):
                continue
        return token
