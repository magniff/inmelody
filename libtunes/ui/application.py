import urwid


class UIBaseApplication:
    initial_widget_name = "login_screen"

    def __getattr__(self, attr_name):
        if attr_name not in self.screens:
            return super().__getattr__(attr_name)

        if isinstance(self.screens[attr_name], type):
            self.screens[attr_name] = self.screens[attr_name]()

        return self.screens[attr_name]

    def __init__(self, screens, palette):
        self.screens = screens
        self.mainloop = urwid.MainLoop(
            widget=self.screens[self.initial_widget_name](),
            unhandled_input=self.unhandled_input,
            palette=palette
        )

    def run_mainloop(self):
        self.mainloop.run()

    def unhandled_input(self, key):
        raise NotImplementedError()

