import urwid
import libtunes.ui as ui


def combine(config):
    mainloop = urwid.MainLoop(ui.UIApplication(config))
    mainloop.run()
