import urwid


class UIBaseApplication:
    initial_widget_name = "login_screen"

    def __getattr__(self, attr_name):
        if attr_name not in self._screens:
            return super().__getattr__(attr_name)

        if isinstance(self._screens[attr_name], type):
            self._screens[attr_name] = self._screens[attr_name](self)

        return self._screens[attr_name]

    def __init__(self, screens):
        self._screens = screens

    def run_mainloop(self, palette):
        self.mainloop = urwid.MainLoop(
            getattr(self, self.initial_widget_name), palette=palette,
            unhandled_input=self.unhandled_input
        )
        self.mainloop.run()

    def unhandled_input(self, key):
        raise NotImplementedError()

