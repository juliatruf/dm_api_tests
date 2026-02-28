import allure

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from clients.http.dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step("Зарегистрировать нового пользователя")
    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :param registration:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    @allure.step("Получить данные пользователя")
    def get_v1_account(
            self,
            validate_response: bool = True,
            **kwargs
    ):
        """
        Get current user
        :param validate_response:
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Активировать пользователя")
    def put_v1_account_token(
            self,
            token,
            validate_response: bool = True
    ):
        """
        Activate registered user
        :param validate_response:
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}',
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Изменить email зарегистрированного пользователя")
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response: bool = True
    ):
        """
        Change registered user email
        :param change_email:
        :param validate_response:
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)

        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сбросить пароль пользователя")
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response: bool = True,
            **kwargs
    ):
        """
        Reset registered user password
        :param reset_password:
        :param validate_response:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Подтвердить новый пароль пользователя")
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response: bool = True,
            **kwargs
    ):
        """
        Change registered user password
        :param change_password:
        :param validate_response:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(mode='json', exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
