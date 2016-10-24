import vk
from .audio import AudioGet, AudioSearch


def create_api_handler(config):
    try:
        session = vk.AuthSession(
            app_id=config.app_id, user_login=config.login,
            user_password=config.password, scope='audio'
        )
    except vk.exceptions.VkAuthError:
        api = None
    else:
        api = vk.API(session)
    finally:
        return api

