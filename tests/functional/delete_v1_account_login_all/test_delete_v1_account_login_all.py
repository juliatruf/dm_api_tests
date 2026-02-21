def test_delete_v1_account_login_all(account_helper, prepare_user):
    """
    Выход из аккаунта на всех устройствах, кроме текущего
    """
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)
    # Создание первой сессии (Токен А), которая далее будет инвалидирована
    response_other = account_helper.user_login(login=login, password=password, validate_response=False)
    token_a = response_other.headers['X-Dm-Auth-Token']
    # Авторизация текущего клиента (Токен B)
    account_helper.auth_client(login=login, password=password)
    token_b = account_helper.dm_account_api.account_api.session.headers.get('x-dm-auth-token')
    # Сравнение токенов разных сессий
    assert token_a != token_b, "Сервер должен был выдать разные токены для разных сессий"
    # Вызов DELETE /v1/account/login/all через авторизованный клиент
    account_helper.logout_all_sessions()
    # Проверка: Токен А первой сессии должен быть инвалидирован
    response =  account_helper.get_current_user_info(
        headers={'X-Dm-Auth-Token': token_a},
        validate_response=False
    )
    assert response.status_code == 401, "Сессия на другом устройстве должна была закрыться"
    # Проверка: Текущая сессия (Токен Б) должна остаться действительной
    account_helper.get_current_user_info()
