import html
import vlc


class AudioRecord(dict):

    def __getattr__(self, attr_name):
        value = self[attr_name]
        if isinstance(value, str):
            return html.unescape(value).strip()
        return value

    @property
    def mrl(self):
        return self.url


class Player(vlc.MediaPlayer):

    @classmethod
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(*args, **kwargs)
        instance.__class__ = cls
        return instance

    def play_mrl(self, mrl):
        self.set_media(vlc.Media(mrl))
        super().play()

