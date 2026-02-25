from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


def test_get_v1_account_auth(auth_account_helper, prepare_user):
    """Получение данных текущего пользователя авторизованным клиентом"""
    response = auth_account_helper.get_current_user_info()
    login = auth_account_helper.auth_login
    GetV1Account.check_response_values(response,login)


def test_get_v1_account_no_auth(account_helper):
    """Отказ в получении данных текущего пользователя неавторизованным клиентом"""
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.get_current_user_info()
