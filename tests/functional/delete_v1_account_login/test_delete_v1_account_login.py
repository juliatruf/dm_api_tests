from checkers.http_checkers import check_status_code_http


def test_delete_v1_account_login(auth_account_helper):
    """Проверка инвалидирования токена текущей сессии после logout"""
    # Выход из аккаунта
    auth_account_helper.logout_current_session()
    # Попытка получить данные пользователя с инвалидированным токеном
    with check_status_code_http(401, "User must be authenticated"):
        auth_account_helper.get_current_user_info()
