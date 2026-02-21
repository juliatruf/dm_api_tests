def test_delete_v1_account_login(auth_account_helper):
    """Проверка инвалидирования токена текущей сессии после logout"""
    # Выход из аккаунта
    auth_account_helper.logout_current_session()
    # Попытка получить данные пользователя с инвалидированным токеном
    response = auth_account_helper.get_current_user_info(validate_response=False)
    assert response.status_code == 401, "Токен текущей сессии не инвалидирован после logout"
