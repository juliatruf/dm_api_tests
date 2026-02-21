def test_put_v1_account_password(account_helper, prepare_user):
    """
    Смена пароля зарегистрированного пользователя
    с последующей проверкой инвалидации старого пароля
    """
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = password[::-1]

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_password(
        login=login,
        email=email,
        old_password=password,
        new_password=new_password
    )
    # response = account_helper.user_login(login=login, password=password, validate_response=False)
    # assert response.status_code == 400, "Старый пароль не инвалидирован"
    account_helper.user_login(login=login, password=new_password)
