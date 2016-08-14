import html

import vlc
import watch


class AudioRecord(dict):

    def __getattr__(self, attr_name):
        value = self[attr_name]
        if isinstance(value, str):
            return html.unescape(value).strip()
        return value

    @property
    def mrl(self):
        return self.url


class Playlist(watch.WatchMe):
    records = watch.ArrayOf(watch.builtins.InstanceOf(AudioRecord))

    def __init__(self, records):
        self.records = records

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        if index < 0:
            index = 0
        elif index >= len(self):
            index = len(self) - 1
        return self.records[index]

    def __repr__(self):
        header = "Playlist with %s records." % len(self)
        body = "\n".join(
            "%s -- %s by %s" % (
                counter, item.title, item.artist
            )
            for counter, item in enumerate(self.records)
        )
        return "%s\n%s" % (header, body)

    def remove_record(self, record):
        self.records.remove(record)

    def next_to(self, position):
        new_index = position + 1
        return 0 if new_index >= len(self) else new_index

    def prev_to(self, position):
        new_index = position - 1
        return len(self) - 1 if new_index < 0 else new_index

    def add_record(self, record):
        new_records = self.records + [record]
        if not type(self).records.predicate(new_records):
            self.complain("records", new_records)
        else:
            self.records = new_records


class PlaylistController(watch.builtins.InstanceOf):

    def __set__(self, player_instance, new_playlist):
        super().__set__(player_instance, new_playlist)
        player_instance.current_track_index = 0
        player_instance.stop()


class CurrentTrackIndexController(watch.builtins.InstanceOf):

    def __set__(self, player_instance, new_current_track_index):
        player_instance.stop()
        super().__set__(player_instance, new_current_track_index)


class Player(watch.WatchMe, vlc.MediaPlayer):

    playlist = PlaylistController(Playlist)
    current_track_index = CurrentTrackIndexController(int)

    def __new__(cls, playlist, *args):
        player = super().__new__(cls, *args)
        player.__class__ = cls
        player.playlist = playlist
        return player

    def __init__(self, *args):
        super().__init__()
        self.current_track_index = 0

    def play(self, in_list_number=None):
        if in_list_number is not None:
            self.current_track_index = in_list_number
        self.set_media(vlc.Media(self.playlist[self.current_track_index].mrl))
        super().play()

    def next(self):
        self.play(self.playlist.next_to(self.current_track_index))

    def prev(self):
        self.play(self.playlist.prev_to(self.current_track_index))
