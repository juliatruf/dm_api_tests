def test_put_v1_account_token(account_helper, prepare_user):
    """Активация нового пользователя"""
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.create_new_user(login=login, email=email, password=password)
    # response = account_helper.user_login(login=login, password=password, validate_response=False)
    # assert response.status_code == 403, "Пользователь без активации не должен иметь возможности авторизоваться!"
    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)
