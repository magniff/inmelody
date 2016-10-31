import urwid
import vk
import watch

from .networking import create_api_handler, AudioGet
from .playback import AudioRecord, Player


class BaseController(watch.WatchMe):
    pass


class Network(BaseController):
    vk_app_id = watch.builtins.InstanceOf(int)
    login = watch.builtins.InstanceOf(str)
    password = watch.builtins.InstanceOf(str)
    api = watch.builtins.InstanceOf(vk.API)

    def __init__(self, config_object):
        self.vk_app_id = config_object.app_id
        self.login = config_object.login
        self.password = config_object.password

    def get_records_by_user_id(self, user_id=None):
        getter = AudioGet(self.api)
        if user_id is not None:
            getter.owner_id = user_id
        return tuple(AudioRecord(record) for record in getter.call_api())

    def connect(self, app_id, login, password, fail_cb, succ_cb, *args):
        api = create_api_handler(app_id, login, password)
        if api is None:
            fail_cb()
        else:
            self.api = api
            succ_cb()


class UI(BaseController):
    pass


class Playback(BaseController):
    player = watch.builtins.InstanceOf(Player)

    def __init__(self, player=None):
        self.player = player or Player()

    def stop(self):
        self.player.stop()

    def play_mrl(self, mrl):
        self.player.play_mrl(mrl)


class App(BaseController):

    def shutdown(self):
        raise urwid.ExitMainLoop()

    def __getattr__(self, attr_name):
        return getattr(self.app, attr_name)

    def __init__(self, app):
        self.app = app


app = None
network = None
playback = None
ui = None

