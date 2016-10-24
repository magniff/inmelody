import watch
import datetime
import urwid

from ..playback.player import AudioRecord


class WW(watch.attr_controllers.AttributeControllerMeta, urwid.WidgetMeta):
    "Workaround to solve metaclass conflict."
    pass


class ControlledWidgetWrap(urwid.WidgetWrap, watch.WatchMe, metaclass=WW):
    "Base class for all custom widgets."

    def selectable(self):
        return True

    @property
    def original_widget(self):
        return self._w

    def keypress(self, size, key):
        return self.original_widget.keypress(size, key)


class UIPlaylistItem(ControlledWidgetWrap):

    audio_record = watch.builtins.InstanceOf(AudioRecord)

    def keypress(self, size, key):
        "Make this widget the final key processor"
        return key

    def __init__(self, audio_record):
        self.audio_record = audio_record

        artist_title_widget = urwid.Text(
            "%s -- %s" % (self.audio_record.artist, self.audio_record.title),
            align=urwid.LEFT,
            wrap=urwid.CLIP,
        )

        duration_widget = urwid.Text(
            str(datetime.timedelta(seconds=self.audio_record.duration)),
            align=urwid.RIGHT, wrap=urwid.CLIP
        )

        container = urwid.Columns([artist_title_widget, duration_widget])
        super().__init__(urwid.AttrMap(container, "unfocused", "focused"))


class UIPlaylist(ControlledWidgetWrap):

    playlist_items = watch.ArrayOf(watch.builtins.InstanceOf(UIPlaylistItem))

    def __init__(self, playlist_items):
        self.playlist_items = playlist_items
        super().__init__(urwid.ListBox(urwid.SimpleFocusListWalker(self.playlist_items)))

