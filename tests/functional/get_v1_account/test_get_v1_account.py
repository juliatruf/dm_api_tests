def test_get_v1_account_auth(auth_account_helper):
    """Получение данных текущего пользователя авторизованным клиентом"""
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, "Не удалось получить данные текущего пользователя"


def test_get_v1_account(account_helper):
    """Отказ в получении данных текущего пользователя неавторизованным клиентом"""
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 401, (
        f"Ожидался статус 401, но получен {response.status_code}"
    )
    json_data = response.json()
    assert json_data.get("title") == "User must be authenticated", (
        f"Ожидался текст 'User must be authenticated', но получен '{json_data.get('title')}'"
    )
