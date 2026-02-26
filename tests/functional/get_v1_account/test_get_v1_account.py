import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http

@allure.feature("Аккаунт пользователя")
@allure.story("Получение данных пользователя")
@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Позитивные тесты")
class TestsGetV1AccountPositive:
    @allure.title("Успешное получение данных текущего пользователя авторизованным клиентом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_v1_account_auth(self, auth_account_helper, prepare_user):
        response = auth_account_helper.get_current_user_info()
        login = auth_account_helper.auth_login
        GetV1Account.check_response_values(response, login)


@allure.feature("Аккаунт пользователя")
@allure.story("Получение данных пользователя")
@allure.suite("Тесты на проверку метода GET v1/account")
@allure.sub_suite("Негативные тесты")
class TestsGetV1AccountNegative:
    @allure.title("Отказ в получении данных текущего пользователя неавторизованным клиентом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(
                expected_status_code=401,
                expected_message="User must be authenticated",
                allure_comment="Проверка отклонения запроса без авторизационного токена"
        ):
            account_helper.get_current_user_info()
