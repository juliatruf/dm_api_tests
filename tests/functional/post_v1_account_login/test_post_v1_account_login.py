import allure

from checkers.post_v1_account_login import PostV1AccountLogin


@allure.feature("Аутентификация пользователя")
@allure.story("Вход в систему по логину и паролю")
@allure.suite("Тесты на проверку метода POST v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1AccountLoginPositive:
    @allure.title("Успешная аутентификация нового пользователя по логину и паролю")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_v1_account_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, email=email, password=password)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1AccountLogin.check_response_values(response, login)
