import allure

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account_login import PostV1AccountLogin


@allure.feature("Аккаунт пользователя")
@allure.story("Смена пароля пользователя")
@allure.suite("Тесты на проверку метода PUT v1/account/password")
@allure.sub_suite("Позитивные тесты")
class TestsPutV1AccountPassword:
    @allure.title("Проверка успешного изменения пароля авторизованным пользователем")
    @allure.description("""
            Тест проверяет, что при смене пароля старый пароль инвалидируется 
            и пользователь может войти в систему с новым паролем
            """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_put_v1_account_password(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_password = password[::-1]

        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.change_password(
            login=login,
            email=email,
            old_password=password,
            new_password=new_password
        )
        with check_status_code_http(
            expected_status_code=400,
            expected_message="One or more validation errors occurred.",
            allure_comment="Проверка инвалидации старого пароля"
            ):
            account_helper.user_login(login=login, password=password, validate_response=False)
        response = account_helper.user_login(login=login, password=new_password, validate_response=True)
        PostV1AccountLogin.check_response_values(response, login)
