import urwid

from .base import UIBaseScreen


class UIBaseMainFrame(urwid.Frame):

    def build_body(self):
        raise NotImplementedError()

    def build_header(self):
        raise NotImplementedError()

    def build_footer(self):
        raise NotImplementedError()

    def __init__(self, application):
        self.application = application
        super().__init__(
            body=self.build_body(),
            header=self.build_header(),
            footer=self.build_footer()
        )


class UIBaseMainScreen(UIBaseScreen):
    pass

