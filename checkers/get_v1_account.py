from datetime import datetime

import allure
from hamcrest import assert_that as h_assert_that, all_of, has_property, has_properties, equal_to, has_items
from assertpy import assert_that as a_assert_that, soft_assertions
from checkers.http_checkers import check_status_code_http
from clients.http.dm_api_account.models.user_details_envelope import UserRole


class GetV1Account:
    @classmethod
    def check_response_values(cls, response, login):
        with allure.step("Проверка данных пользователя"):
            with check_status_code_http():
                h_assert_that(response, has_property('resource', all_of(
                    has_property('login', equal_to(login)),
                    has_property('rating', has_properties({
                        "enabled": equal_to(True),
                        "quality": equal_to(0),
                        "quantity": equal_to(0)
                    })),
                    has_property('roles', has_items('Guest', 'Player')),
                    has_property('settings', all_of(
                        has_property('color_schema', equal_to('Modern')),
                        has_property('paging', has_properties({
                            "posts_per_page": equal_to(10),
                            "comments_per_page": equal_to(10),
                            "topics_per_page": equal_to(10),
                            "entities_per_page": equal_to(10),
                            "messages_per_page": equal_to(10)
                        }))
                    ))
                )))
            with soft_assertions():
                a_assert_that(response.resource.login).is_equal_to(login)
                a_assert_that(response.resource.online).is_instance_of(datetime)
                a_assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
