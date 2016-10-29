from .networking import create_api_handler, AudioGet
from .playback import AudioRecord


handle = None


class Provider:

    def get_records_by_user_id(self, user_id=None):
        getter = AudioGet(self._vk_api)
        if user_id is not None:
            getter.owner_id = user_id

        return (AudioRecord(record) for record in getter.call_api())

    def connect(self, app_id, login, password, fail_cb, succ_cb, *args):
        api = create_api_handler(app_id, login, password)
        if api is None:
            fail_cb()
        else:
            self._vk_api = api
            succ_cb()

    @property
    def app_id(self):
        return self._config.app_id

    @property
    def password(self):
        return self._config.password

    @property
    def login(self):
        return self._config.login

    def __init__(self, config):
        self._config = config
        self._vk_api = None


def configure(config_object):
    return Provider(config_object)

