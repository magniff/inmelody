import urwid


def stop_main_loop(*args, **kwargs):
    raise urwid.ExitMainLoop()

