import random
import string
from collections import namedtuple
from datetime import datetime

import pytest
from pathlib import Path
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v
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

options = (
    'service.dm_api_account',
    'service.mailhog_account',
    'user.login',
    'user.password'
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    host = "http://185.185.143.231:5051"
    reporter = CoverageReporter(api_name="dm-api-account", host=host)
    reporter.setup("/swagger/Account/swagger.json?urls.primaryName=Account")
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    # config = Path(__file__).joinpath("../../").joinpath("config")
    config = Path(__file__).resolve().parent.parent / "config"
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"), disable_log=False)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(
        host=v.get("service.dm_api_account"), disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(
        host=v.get("service.dm_api_account"), disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login=v.get("user.login"),
        password=v.get("user.password")
    )
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    login = f"jtruf_{data}_{random_str}"
    password = v.get("user.password")
    email = f"{login}@list.ru"
    User = namedtuple("User", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
