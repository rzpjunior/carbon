import urwid
import itertools

class LoadingWidget(urwid.WidgetWrap):
    def __init__(self):
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])
        self.text = urwid.Text(next(self.spinner), align='center')
        super().__init__(self.text)

    def start(self, loop):
        self._loop = loop
        self._handle = loop.set_alarm_in(0.1, self._update_spinner)

    def _update_spinner(self, loop, user_data):
        self.text.set_text(next(self.spinner))
        self._handle = loop.set_alarm_in(0.1, self._update_spinner)

    def stop(self):
        if hasattr(self, '_handle'):
            self._loop.remove_alarm(self._handle)