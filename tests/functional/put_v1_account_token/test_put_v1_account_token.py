import allure

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account_login import PostV1AccountLogin


@allure.feature("Аккаунт пользователя")
@allure.story("Активация пользователя")
@allure.suite("Тесты на проверку метода PUT v1/account/token")
@allure.sub_suite("Позитивные тесты")
class TestsPutV1AccountToken:
    @allure.title("Проверка активации нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_put_v1_account_token(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.create_new_user(login=login, email=email, password=password)
        with check_status_code_http(
                expected_status_code=403,
                expected_message="User is inactive. Address the technical support for more details",
                allure_comment="Проверка невозможности входа в аккаунт для неактивированного пользователя"
        ):
            account_helper.user_login(login=login, password=password, validate_response=False)
        account_helper.activate_user(login=login)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1AccountLogin.check_response_values(response, login)

