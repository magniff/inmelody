import watch
from .api_base import APICaller
from .validators import String, ZeroPositiveInteger, ZeroOne


class AudioAPICaller(APICaller):
    domain = "audio"


class AudioSearch(AudioAPICaller):
    method = "search"

    q = String
    auto_complete = ZeroOne
    lyrics = ZeroOne
    performer_only = ZeroOne
    search_own = ZeroOne
    offset = ZeroPositiveInteger
    count = ZeroPositiveInteger


class AudioGet(AudioAPICaller):
    method = "get"

    owner_id = ZeroPositiveInteger
    album_id = ZeroPositiveInteger
    audio_ids = watch.ArrayOf(ZeroPositiveInteger)
    need_user = ZeroOne
    offset = ZeroPositiveInteger
    count = ZeroPositiveInteger

