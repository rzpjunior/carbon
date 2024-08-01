import urwid
import subprocess
import pyte

class TerminalWidget(urwid.WidgetWrap):
    def __init__(self):
        self.term = pyte.Screen(80, 24)
        self.stream = pyte.Stream()
        self.stream.attach(self.term)
        self.output = urwid.Text("", wrap='clip')
        self.output_box = urwid.ListBox(urwid.SimpleFocusListWalker([self.output]))
        self.output_box = urwid.BoxAdapter(self.output_box, height=15)
        self.input = urwid.Edit("user@CARBON ~> ", multiline=False)
        self.layout = urwid.Pile([self.output_box, ('pack', self.input)])
        self.frame = urwid.LineBox(self.layout)
        super().__init__(self.frame)

    def handle_input(self, key):
        if isinstance(key, str) and key == 'enter':
            command = self.input.edit_text
            self.input.edit_text = ""
            self.execute_command(command)
        elif isinstance(key, str):
            self.input.keypress((80,), key)

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.update_output(result.stdout + result.stderr)
        except Exception as e:
            self.update_output(str(e))

    def update_output(self, text):
        current_text = self.output.get_text()[0]
        new_text = f"{current_text}\n{text}" if current_text else text
        self.output.set_text(new_text)
        self.output_box.set_focus(len(self.output_box.body) - 1)

    def keypress(self, size, key):
        if key == 'enter':
            self.handle_input('enter')
        elif key in ('up', 'down'):
            return self.output_box.keypress(size, key)
        else:
            return self.input.keypress(size, key)
