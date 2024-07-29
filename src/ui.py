import urwid
from src.kubernetes.manager import KubernetesManager
from src.utils.config_loader import load_config

class CarbonUI:
    def __init__(self):
        self.manager = KubernetesManager()
        self.main_menu = self.build_main_menu()
        self.loop = urwid.MainLoop(self.main_menu, unhandled_input=self.handle_input)

    def build_main_menu(self):
        body = [
            urwid.Text("Choose your provider:"),
            urwid.Divider(),
            urwid.Button("DigitalOcean", self.choose_provider, 'digitalocean'),
            urwid.Button("AWS", self.choose_provider, 'aws'),
        ]
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

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
        self.loop.widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def load_config(self, button):
        edit_widget = self.loop.widget.body[2]
        config_path = edit_widget.get_edit_text()
        try:
            config = load_config(config_path)
            self.manager.load_config(config)
            self.resource_selection_screen()
        except Exception as e:
            error_text = urwid.Text(('error', f"Error loading configuration: {str(e)}"))
            self.loop.widget.body.insert(3, error_text)
            self.loop.draw_screen()

    def resource_selection_screen(self, button=None):
        body = [
            urwid.Text("Select the resource type you want to view:"),
            urwid.Divider(),
            urwid.Button("Pods", self.show_resources, 'pods'),
            urwid.Button("Namespaces", self.show_resources, 'namespaces'),
            urwid.Button("Deployments", self.show_resources, 'deployments'),
            urwid.Button("Services", self.show_resources, 'services'),
            urwid.Button("Ingresses", self.show_resources, 'ingresses'),
            urwid.Button("Back", self.back_to_main),
        ]
        self.loop.widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def show_resources(self, button, resource_type):
        try:
            resources = self.manager.get_resource(resource_type)
            body = [
                urwid.Text(f"Kubernetes {resource_type.capitalize()}:"),
                urwid.Divider(),
            ]
            for item in resources:
                body.append(urwid.Text(f" - {item}"))
            body.append(urwid.Button("Back", self.resource_selection_screen))
            self.loop.widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        except Exception as e:
            error_text = urwid.Text(('error', f"Error fetching {resource_type}: {str(e)}"))
            self.loop.widget.body.insert(3, error_text)
            self.loop.draw_screen()

    def back_to_main(self, button):
        self.loop.widget = self.main_menu

    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()
