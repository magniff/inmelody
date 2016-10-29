import urwid

from .. import provider
from .common import stop_main_loop
from .base import UIBaseScreen
from .main_screen import UIBaseMainFrame, UIBaseMainScreen
from .login_screen import logo_widget
from .components import (
    UIBackground, UIDoubleColumnFiltrableList, UIFiltrableRecordList
)
from .application import UIBaseApplication


class UILoginFrame(UIBaseMainFrame):

    def _on_login_success(self):
        self._next_screen()

    def _on_login_fail(self, status_widget):
        def callback():
            status_widget.set_text("Login or/and password is incorrect.")
        return callback

    def _on_login_in_progress(self, status_widget):
        def callback():
            status_widget.set_text("Connecting to vk.com")
        return callback

    def _connect(self, *args):
        provider.handle.connect(
            app_id=self._app_id_edit.get_edit_text(),
            login=self._login_edit.get_edit_text(),
            password=self._password_edit.get_edit_text(),
            fail_cb=self._on_login_fail(self._status_widget),
            succ_cb=self._on_login_success,
        )

    def _next_screen(self):
        self.application.mainloop.widget = self.application.main_screen

    def build_body(self):
        self._password_edit = urwid.Edit(
            caption="Password: ", mask="*",
            edit_text=provider.handle.password
        )
        self._login_edit = urwid.Edit(
            caption="VK login: ", mask="*",
            edit_text=provider.handle.login
        )
        self._app_id_edit = urwid.Edit(
            caption="App id: ", mask="*",
            edit_text=str(provider.handle.app_id)
        )
        self._connect_button = urwid.Button("Connect")
        self._cancel_button = urwid.Button("Cancel")
        self._status_widget = urwid.Text("")
        self._body_layout = urwid.Pile([
            logo_widget, self._app_id_edit, self._login_edit,
            self._password_edit,
            urwid.Columns(
                [
                    self._connect_button,
                    self._cancel_button
                ]),
            self._status_widget
        ])

        urwid.connect_signal(self._connect_button, 'click', self._connect)
        urwid.connect_signal(self._cancel_button, 'click', stop_main_loop)
        return urwid.Filler(urwid.LineBox(self._body_layout))

    def build_header(self):
        return urwid.Text("Header here")

    def build_footer(self):
        return urwid.Text("Footer here")


class UILoginScreen(UIBaseScreen):
    width = 80

    def build_frame(self):
        return UILoginFrame(application=self.application)

    def build_background(self):
        return UIBackground()


class UIMainFrame(UIBaseMainFrame):

    def build_body(self):
        return UIDoubleColumnFiltrableList(
            left=UIFiltrableRecordList(),
            right=UIFiltrableRecordList()
        )

    def build_header(self):
        return urwid.Text("Header here")

    def build_footer(self):
        return urwid.Text("Footer here")


class UIMainScreen(UIBaseMainScreen):

    def build_frame(self):
        return UIMainFrame(application=self.application)

    def build_background(self):
        return UIBackground()


DEFAULT_SCREENSET = {
    "login_screen": UILoginScreen,
    "main_screen": UIMainScreen
}


class UIDefaultApplication(UIBaseApplication):
    def unhandled_input(self, key):
        pass

    def __init__(self):
        super().__init__(screens=DEFAULT_SCREENSET)

