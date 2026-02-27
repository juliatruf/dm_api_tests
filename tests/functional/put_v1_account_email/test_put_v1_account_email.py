import allure

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account_login import PostV1AccountLogin


@allure.feature("Аккаунт пользователя")
@allure.story("Изменение email пользователя")
@allure.suite("Тесты на проверку метода PUT v1/account/email")
@allure.sub_suite("Позитивные тесты")
class TestsPutV1AccountEmail:
    @allure.title("Проверка изменения email пользователя на валидный адрес")
    @allure.description("""
           Тест проверяет, что при вызове метода смены email пользователь деактивируется 
           и должен снова пройти активацию.
           """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_put_v1_account_email(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        new_email = f'{login}+1@bk.ru'

        account_helper.register_new_user(login=login, email=email, password=password)
        account_helper.change_user_email(login=login, password=password, email=new_email)
        with check_status_code_http(
                expected_status_code=403,
                expected_message="User is inactive. Address the technical support for more details",
                allure_comment="Проверка деактивации пользователя после смены email"
        ):
            account_helper.user_login(login=login, password=password, validate_response=False)
        account_helper.activate_user(login=login)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1AccountLogin.check_response_values(response, login)
