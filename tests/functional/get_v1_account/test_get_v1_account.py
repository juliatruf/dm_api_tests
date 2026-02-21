def test_get_v1_account_auth(auth_account_helper, prepare_user):
    """Получение данных текущего пользователя авторизованным клиентом"""
    auth_account_helper.get_current_user_info()


def test_get_v1_account_no_auth(account_helper):
    """Отказ в получении данных текущего пользователя неавторизованным клиентом"""
    response = account_helper.get_current_user_info(validate_response=False)
    assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
