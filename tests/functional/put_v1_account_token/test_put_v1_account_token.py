def test_put_v1_account_token(account_helper, prepare_user):
    """Активация нового пользователя"""
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.create_new_user(login=login, email=email, password=password)
    account_helper.user_login(
        login=login,
        password=password,
        status_code=403,
        error_message="Пользователь без активации не должен иметь возможности авторизоваться!"
    )
    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)
