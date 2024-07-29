import urwid
from src.kubernetes.manager import KubernetesManager
from src.utils.config_loader import load_config

class CarbonUI:
    def __init__(self):
        self.manager = KubernetesManager()
        self.header = urwid.Text("Carbon - Kubernetes IDE", align='center')
        self.body = urwid.Text("Please select a provider to get started.")
        self.frame = urwid.Frame(header=self.header, body=self.body, footer=None)
        self.loop = urwid.MainLoop(self.frame, unhandled_input=self.handle_input)

    def load_main_menu(self):
        body = [
            urwid.Text("Choose your provider:"),
            urwid.Divider(),
            urwid.Button("DigitalOcean", self.choose_provider, 'digitalocean'),
            urwid.Button("AWS", self.choose_provider, 'aws'),
        ]
        self.body = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.update_frame()

    def choose_provider(self, button, provider):
        self.manager.set_provider(provider)
        self.load_config_screen()

    def load_config_screen(self):
        body = [
            urwid.Text("Enter path to your YAML configuration:"),
            urwid.Divider(),
            urwid.Edit(caption="Path: ", edit_text=""),
            urwid.Button("Load", self.load_config),
        ]
        self.body = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.update_frame()

    def load_config(self, button):
        edit_widget = self.body.body[2]
        config_path = edit_widget.get_edit_text()
        try:
            config = load_config(config_path)
            self.manager.load_config(config)
            self.resource_selection_screen()
        except Exception as e:
            error_text = urwid.Text(('error', f"Error loading configuration: {str(e)}"))
            self.body.body.insert(3, error_text)
            self.loop.draw_screen()

    def build_sidebar(self):
        body = [
            urwid.Text("Resources:"),
            urwid.Divider(),
            urwid.Button("Pods", self.show_resources, 'pods'),
            urwid.Button("Namespaces", self.show_resources, 'namespaces'),
            urwid.Button("Deployments", self.show_resources, 'deployments'),
            urwid.Button("Services", self.show_resources, 'services'),
            urwid.Button("Ingresses", self.show_resources, 'ingresses'),
            urwid.Divider(),
            urwid.Button("Back to Main Menu", self.back_to_main),
        ]
        return urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(body)), title="Menu")

    def resource_selection_screen(self):
        self.sidebar = self.build_sidebar()
        self.body = urwid.Text("Please select a resource from the sidebar.")
        self.columns = urwid.Columns([('fixed', 20, self.sidebar), self.body])
        self.frame.body = self.columns

    def show_resources(self, button, resource_type):
        try:
            resources = self.manager.get_resource(resource_type)
            body = [
                urwid.Text(f"Kubernetes {resource_type.capitalize()}:"),
                urwid.Divider(),
            ]
            for item in resources:
                body.append(urwid.Text(f" - {item}"))
            self.body = urwid.ListBox(urwid.SimpleFocusListWalker(body))
            self.update_frame()
        except Exception as e:
            error_text = urwid.Text(('error', f"Error fetching {resource_type}: {str(e)}"))
            self.body.body.insert(3, error_text)
            self.loop.draw_screen()

    def back_to_main(self, button):
        self.load_main_menu()

    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def update_frame(self):
        if hasattr(self, 'columns'):
            self.columns.contents[1] = (self.body, self.columns.options())
        else:
            self.frame.body = self.body

    def run(self):
        self.load_main_menu()
        self.loop.run()
