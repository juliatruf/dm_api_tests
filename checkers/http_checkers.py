import allure
import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: int = requests.codes.OK,
        expected_message: str = "",
        allure_comment: str = ""
):
    step_name = allure_comment if allure_comment else f"Ожидаем ответ: {expected_status_code} {expected_message}"
    with allure.step(step_name):
        try:
            yield
            if expected_status_code != requests.codes.OK:
                raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
            if expected_message:
                raise AssertionError(f"Должно быть получено сообщение '{expected_message}', "
                                     f"но запрос прошел успешно")
        except HTTPError as e:
            actual_json = e.response.json()
            allure.attach(
                str(actual_json),
                name="Actual Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            assert e.response.status_code == expected_status_code
            assert actual_json['title'] == expected_message
