import watch
import urwid


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


class UIBaseScreen(urwid.Overlay):

    vertical_align = "middle"
    horisontal_align = "center"
    width = 140
    height = 50

    def build_background(self):
        raise NotImplementedError()

    def build_frame(self):
        raise NotImplementedError()

    def __init__(self, application):
        self.application = application
        super().__init__(
            self.build_frame(), self.build_background(),
            align=self.horisontal_align, width=self.width,
            valign=self.vertical_align, height=self.height
        )


