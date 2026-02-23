from datetime import datetime
import pytest
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to
from checkers.http_checkers import check_status_code_http


def test_post_v1_account(account_helper, prepare_user):
    """Регистрация нового пользователя с последующей активацией и авторизацией"""
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with('jtruf'))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                    {
                        'rating': has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )


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
