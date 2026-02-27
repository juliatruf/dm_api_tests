import allure

from checkers.http_checkers import check_status_code_http


@allure.feature("Выход из аккаунта")
@allure.story("Выход изо всех сессий, кроме текущей")
@allure.suite("Тесты на проверку метода DELETE v1/account/login/all")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1AccountLoginAll:
    @allure.title("Проверка выхода из аккаунта на всех устройствах, кроме текущего")
    @allure.description("""
        Тест проверяет механизм выхода из всех сессий, кроме текущей:
        1. Создается сторонняя сессия (Token A).
        2. Создается текущая сессия (Token B).
        3. Выполняется сброс всех сессий через Token B.
        4. Token A должен стать невалидным (401).
        5. Token B должен сохранить доступ к системе (200).
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_v1_account_login_all(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        with allure.step("Создание сторонней сессии (Токен А), которая далее будет инвалидирована"):
            response_other = account_helper.user_login(login=login, password=password, validate_response=False)
            token_a = response_other.headers['X-Dm-Auth-Token']
        with allure.step("Авторизация текущего клиента (Токен B)"):
            account_helper.auth_client(login=login, password=password)
            token_b = account_helper.dm_account_api.account_api.session.headers.get('x-dm-auth-token')
            assert token_a != token_b, "Сервер должен был выдать разные токены для разных сессий"
        account_helper.logout_all_sessions()
        with check_status_code_http(
                expected_status_code=401,
                expected_message="User must be authenticated",
                allure_comment="Проверка инвалидации токена сторонней сессии (Токена А)"
        ):
            account_helper.get_current_user_info(headers={'X-Dm-Auth-Token': token_a})
        with allure.step("Проверка: текущая сессия (Токен B) должна остаться действительной"):
            account_helper.get_current_user_info()
