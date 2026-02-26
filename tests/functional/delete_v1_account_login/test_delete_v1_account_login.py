import allure

from checkers.http_checkers import check_status_code_http


@allure.feature("Выход из аккаунта")
@allure.story("Выход из текущей сессии")
@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1AccountLogin:
    @allure.title("Проверка инвалидирования токена текущей сессии после logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_v1_account_login(self, auth_account_helper):
        auth_account_helper.logout_current_session()
        with check_status_code_http(
                expected_status_code=401,
                expected_message="User must be authenticated",
                allure_comment="Проверка отклонения запроса данных пользователя с инвалидированным токеном"
        ):
            auth_account_helper.get_current_user_info()
