from hamcrest import assert_that, all_of, has_property, has_properties, starts_with, instance_of, equal_to, has_items


def test_get_v1_account_auth(auth_account_helper, prepare_user):
    """Получение данных текущего пользователя авторизованным клиентом"""
    response = auth_account_helper.get_current_user_info()
    assert_that(response, has_property('resource', all_of(
        has_property('login', equal_to(auth_account_helper.auth_login)),
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


def test_get_v1_account_no_auth(account_helper):
    """Отказ в получении данных текущего пользователя неавторизованным клиентом"""
    response = account_helper.get_current_user_info(validate_response=False)
    assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}"
