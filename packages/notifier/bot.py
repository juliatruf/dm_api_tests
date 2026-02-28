import os
from pathlib import Path

from dotenv import load_dotenv
from telebot import TeleBot
from vyper import v


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env", override=False)
config = Path(__file__).parent.joinpath("../../").joinpath("config")
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()


def send_file() -> None:
    token = os.environ.get("TG_TOKEN") or os.path.expandvars(str(v.get("telegram.token") or ""))
    chat_id = os.environ.get("TG_CHAT_ID") or os.path.expandvars(str(v.get("telegram.chat_id") or ""))
    telegram_bot = TeleBot(v.get("telegram.token"))
    file_path = Path(__file__).parent.joinpath('../../').joinpath("swagger-coverage-dm-api-account.html")
    with open(file_path, 'rb') as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption="coverage",
        )

if __name__ == "__main__":
    send_file()
