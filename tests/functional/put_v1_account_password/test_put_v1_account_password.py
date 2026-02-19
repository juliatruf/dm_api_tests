def test_put_v1_account_password(account_helper, prepare_user):
    """
    Смена пароля зарегистрированного пользователя
    с последующей проверкой инвалидации старого пароля
    """
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = password[::-1]

    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.auth_client(login=login, password=password)
    account_helper.reset_user_password(login=login, email=email)
    token_confirm_password = account_helper.get_token_by_login(
        login=login, token_key_name=account_helper.TOKEN_KEY_PASSWORD_RESET
    )
    account_helper.change_user_password(
        login=login, token=token_confirm_password,
        old_password=password, new_password=new_password
    )
    account_helper.user_login(login=login, password=password, status_code=400,
                              error_message="Старый пароль не инвалидирован")
    account_helper.user_login(login=login, password=new_password)
