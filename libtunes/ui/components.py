import datetime

import urwid
import watch
from .. import provider
from ..playback.player import AudioRecord
from .base import ControlledWidgetWrap


class UIBaseComponent(ControlledWidgetWrap):
    pass


class UIBackground(UIBaseComponent):

    def __init__(self):
        super().__init__(urwid.SolidFill(" "))


class UIPlaylistItem(UIBaseComponent):

    audio_record = watch.builtins.InstanceOf(AudioRecord)

    def assign_weight(self, widget, weight):
        return ('weight', weight, widget)

    def keypress(self, size, key):
        if key == "enter":
            provider.playback.play_mrl(self.audio_record.mrl)
        elif key == "esc":
            provider.playback.stop()
        return key

    def __init__(self, audio_record):
        self.audio_record = audio_record

        duration_widget = urwid.Text(
            str(datetime.timedelta(seconds=self.audio_record.duration)),
            align=urwid.RIGHT, wrap=urwid.CLIP
        )

        title_widget = urwid.Text(
            self.audio_record.title, align=urwid.LEFT, wrap=urwid.CLIP
        )

        artist_widget = urwid.Text(
            self.audio_record.artist, align=urwid.LEFT, wrap=urwid.CLIP
        )

        container = urwid.Columns(
            [
                self.assign_weight(artist_widget, 2),
                self.assign_weight(title_widget, 4),
                self.assign_weight(duration_widget, 1)
            ],
            dividechars=2
        )
        super().__init__(
            urwid.AttrMap(container, "plitem_unfocused", "focused")
        )


class UIPlaylistFilter(UIBaseComponent):
    def __init__(self, filter_caption):
        super().__init__(urwid.Edit(filter_caption))


class UIFiltrableRecordList(UIBaseComponent):

    list_member_class = UIPlaylistItem
    filter_class = UIPlaylistFilter

    def record_list_by_user_id(self, user_id=None):
        return self.build_records_list_widget(
            provider.network.get_records_by_user_id(user_id=user_id)
        )

    def build_records_list_widget(self, records):
        record_widgets = [
            self.list_member_class(record) for record in records
        ]
        return urwid.ListBox(
            urwid.SimpleFocusListWalker(record_widgets)
        )

    def compose_widget(self):
        return self.records_list_widget

    def __init__(self, album_name="<Untitled album>"):
        self.album_name = album_name
        self.records_list_widget = self.record_list_by_user_id(user_id=None)
        super().__init__(self.compose_widget())


class UIDoubleColumnFiltrableList(UIBaseComponent):

    def compose_widget(self):
        return urwid.Columns([
            urwid.LineBox(self.left, title=self.left.album_name),
            urwid.LineBox(self.right, title=self.right.album_name),
        ])

    def __init__(self, left, right):
        self.left = left
        self.right = right
        super().__init__(self.compose_widget())

