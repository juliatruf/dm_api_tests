def test_get_v1_account_auth(auth_account_helper, prepare_user):
    """Получение данных текущего пользователя авторизованным клиентом"""
    response = auth_account_helper.get_current_user_info()
    actual_login = response.json()['resource']['login']
    expected_login = auth_account_helper.auth_login
    assert actual_login == expected_login, \
        (f"Ошибка идентификации! Ожидался пользователь: {expected_login}, "
         f"получен: {actual_login}"
         )


def test_get_v1_account_no_auth(account_helper):
    """Отказ в получении данных текущего пользователя неавторизованным клиентом"""
    response = account_helper.get_current_user_info(status_code=401)
    json_data = response.json()
    assert json_data.get("title") == "User must be authenticated", \
        f"Ожидался текст 'User must be authenticated', но получен '{json_data.get('title')}'"
