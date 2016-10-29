import vk
from .audio import AudioGet, AudioSearch


def create_api_handler(app_id, login, password):
    try:
        session = vk.AuthSession(
            app_id=app_id, user_login=login,
            user_password=password, scope='audio'
        )
    except vk.exceptions.VkAuthError:
        api = None
    else:
        api = vk.API(session)
    finally:
        return api

