import vlc
import watch
import datetime
import urwid

from ..playback.player import AudioRecord
player = vlc.MediaPlayer()


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

    def assign_weight(self, widget, weight):
        return ('weight', weight, widget)

    def keypress(self, size, key):
        "Make this widget the final key processor"
        if key == "enter":
            player.set_media(vlc.Media(self.audio_record.mrl))
            player.play()
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
                self.assign_weight(title_widget, 3),
                self.assign_weight(duration_widget, 1)
            ],
            dividechars=2
        )
        super().__init__(urwid.AttrMap(container, "unfocused", "focused"))


class UIPlaylistFilter(ControlledWidgetWrap):
    def __init__(self, filter_caption):
        super().__init__(urwid.Edit(filter_caption))


class UIFiltrableRecordList(ControlledWidgetWrap):

    list_member_class = UIPlaylistItem
    filter_class = UIPlaylistFilter

    def build_records_list_widget(self, records):
        record_widgets = [
            self.list_member_class(record) for record in records
        ]
        return urwid.ListBox(
            urwid.SimpleFocusListWalker(record_widgets)
        )

    def compose_widget(self):
        return self.records_list_widget

    def __init__(self, records, album_name="<Untitled album>"):
        self.album_name = album_name
        self.records_list_widget = self.build_records_list_widget(records)
        super().__init__(self.compose_widget())


class UIDoubleColumnFiltrableList(urwid.Columns):

    def compose_widget(self):
        return [
            urwid.LineBox(self.left, title=self.left.album_name),
            urwid.LineBox(self.right, title=self.right.album_name),
        ]

    def __init__(self, left, rigth):
        self.left = left
        self.right = rigth
        super().__init__(self.compose_widget())


class UIMainFrame(urwid.Frame):

    def build_header(self):
        return urwid.Text("this would be header")

    def build_footer(self):
        return urwid.Text("this would be footer")

    def __init__(self, body):
        super().__init__(
            body=body, header=self.build_header(), footer=self.build_footer()
        )


class UIBackground(urwid.SolidFill):
    def __init__(self):
        super().__init__(" ")


class UIApplication(urwid.Overlay):
    background_widget_class = UIBackground

    def __init__(self, main_screen, background=None, **kwargs):
        super().__init__(
            main_screen, background or self.background_widget_class(),
            align='center', width=140, valign='middle', height=80
        )

    def unhandled_input(self, key):
        pass

    def run_mainloop(self, palette=tuple()):
        self.mainloop = urwid.MainLoop(
            self, palette=palette,
            unhandled_input=self.unhandled_input
        )
        self.mainloop.run()

