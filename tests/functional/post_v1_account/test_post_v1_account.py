import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(account_helper, prepare_user):
    """Регистрация нового пользователя с последующей активацией и авторизацией"""
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response, login)


@pytest.mark.parametrize('login, password, email, error_message, expected_status_code', [
    ('jtruf_2302', '1234', 'jtruf_2302@mail.ru', 'Validation failed', 400),
    ('jtruf_2202', '123456789', 'jtruf_2202mail.ru', 'Validation failed', 400),
    ('j', '123456789', 'jtruf@mail.ru', 'Validation failed', 400)
]
                         )
def test_post_v1_account_invalid_credentials(
        account_helper, login, password, email, error_message, expected_status_code
):
    """Отклонение регистрации нового пользователя с невалидными данными"""
    with check_status_code_http(expected_status_code, error_message):
        account_helper.register_new_user(login=login, password=password, email=email)
