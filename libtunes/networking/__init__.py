import watch
import vk

from .audio import AudioGet, AudioSearch


class NetworkgProvider(watch.WatchMe):
    api = watch.SomeOf(
        watch.builtins.InstanceOf(vk.API), watch.builtins.EqualsTo(None)
    )

    def connect(self, app_id, login, password):
        try:
            session = vk.AuthSession(
                app_id=app_id, user_login=login,
                user_password=password, scope='audio'
            )
        except vk.exceptions.VkAuthError:
            self.api = None
        else:
            self.api = vk.API(session)


network_provider = NetworkgProvider()
