def test_put_v1_account_email(account_helper, prepare_user):
    """Смена email зарегистрированного пользователя с последующей проверкой деактивации и активации"""
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f'{login}+1@bk.ru'

    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.change_user_email(login=login, password=password, new_email=new_email)
    account_helper.user_login(login=login, password=password, status_code=403,
                              error_message="Пользователь не деактивирован после смены email")
    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)
