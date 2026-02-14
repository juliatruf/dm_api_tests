import uuid

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

def test_post_v1_account_login():
    """Авторизация нового пользователя"""
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    uid = uuid.uuid4().hex[:8]
    login = f'user_{uid}'
    email = f'{login}@mail.ru'
    password = '123456789'

    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)
