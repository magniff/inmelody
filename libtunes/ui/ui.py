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

    def keypress(self, size, key):
        "Make this widget the final key processor"
        if key == "enter":
            player.set_media(vlc.Media(self.audio_record.mrl))
            player.play()
        return key

    def __init__(self, audio_record):
        self.audio_record = audio_record

        artist_title_widget = urwid.Text(
            "%s -- %s" % (self.audio_record.artist, self.audio_record.title),
            align=urwid.LEFT, wrap=urwid.CLIP,
        )

        duration_widget = urwid.Text(
            str(datetime.timedelta(seconds=self.audio_record.duration)),
            align=urwid.RIGHT, wrap=urwid.CLIP
        )

        container = urwid.Columns([artist_title_widget, duration_widget])
        super().__init__(urwid.AttrMap(container, "unfocused", "focused"))


class UIMainScreen(ControlledWidgetWrap):
    pass


class UIExitScreen(ControlledWidgetWrap):
    pass


class UILoginScreen(ControlledWidgetWrap):
    pass


class UIDefaultMainScreen(UIMainScreen):

    playlist_items = watch.ArrayOf(watch.builtins.InstanceOf(UIPlaylistItem))

    def __init__(self, playlist_items):
        self.playlist_items = playlist_items
        super().__init__(
            urwid.LineBox(
                urwid.ListBox(urwid.SimpleListWalker(self.playlist_items))
            )
        )


class UIDefaultExitScreen(UIExitScreen):
    def __init__(self):
        pass


class UIDefaultLoginScreen(UILoginScreen):
    def __init__(self):
        pass


class UIApplication(ControlledWidgetWrap):

    login_screen = watch.builtins.InstanceOf(UILoginScreen)
    exit_screen = watch.builtins.InstanceOf(UIExitScreen)
    main_screen = watch.builtins.InstanceOf(UIMainScreen)

    def __init__(self, main_screen, login_screen=None, exit_screen=None):
        self.login_screen = login_screen or UIDefaultLoginScreen()
        self.exit_screen = exit_screen or UIDefaultExitScreen()
        self.main_screen = main_screen
        super().__init__(self.main_screen)

    def unhandled_input(self, key):
        if player.is_playing():
            if key == 'right':
                player.set_position(player.get_position()+0.05)
            elif key == 'left':
                player.set_position(player.get_position()-0.05)

    def run_mainloop(self, palette=tuple()):
        self.mainloop = urwid.MainLoop(
            self.original_widget, palette=palette,
            unhandled_input=self.unhandled_input
        )
        self.mainloop.run()

