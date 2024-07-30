import urwid
import yaml

from src.kubernetes.workloads import Workloads
from src.kubernetes.network import Network
from src.kubernetes.namespace import Namespace
from src.utils.config_loader import load_config
from src.tables.pod_table import build_pod_table
from src.tables.deployment_table import build_deployment_table
from src.tables.service_table import build_service_table
from src.tables.ingress_table import build_ingress_table
from src.tables.namespace_table import build_namespace_table
from src.terminal import TerminalWidget

class CarbonUI:
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text("Carbon - Kubernetes IDE", align='center'), 'header')
        self.body = urwid.Text("Please select a provider to get started.")
        self.terminal = TerminalWidget()
        self.frame = urwid.Frame(header=self.header, body=self.body, footer=self.terminal)
        self.loop = urwid.MainLoop(self.frame, unhandled_input=self.handle_input, palette=[
            ('header', 'black', 'light gray', 'standout'),
            ('reversed', 'standout', ''),
            ('running', 'dark green', ''),
            ('pending', 'yellow', ''),
            ('failed', 'dark red', ''),
            ('line', 'light gray', 'black')
        ])
        self.sidebar = None
        self.config_loaded = False

    def load_main_menu(self):
        body = [
            urwid.Text("Choose your provider:"),
            urwid.Divider(),
            urwid.Button("DigitalOcean", self.choose_provider, 'digitalocean'),
            urwid.Button("AWS", self.choose_provider, 'aws'),
        ]
        self.body = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.frame.body = self.body

    def choose_provider(self, button, provider):
        self.provider = provider
        self.load_config_screen()

    def load_config_screen(self):
        body = [
            urwid.Text("Enter path to your YAML configuration:"),
            urwid.Divider(),
            urwid.Edit(caption="Path: ", edit_text=""),
            urwid.Button("Load", self.load_config),
        ]
        self.body = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.frame.body = self.body

    def load_config(self, button):
        edit_widget = self.body.body[2]
        config_path = edit_widget.get_edit_text()
        try:
            load_config(config_path)
            self.config_loaded = True
            self.workloads = Workloads()
            self.network = Network()
            self.namespace = Namespace()
            self.resource_selection_screen()
        except Exception as e:
            error_text = urwid.Text(('failed', f"Error loading configuration: {str(e)}"))
            self.body.body.insert(3, error_text)
            self.loop.draw_screen()

    def build_sidebar(self):
        menu_content = urwid.Pile([
            urwid.AttrMap(urwid.Text("Resources", align='center'), 'header'),
            urwid.Divider(),
            urwid.Text("Workloads:"),
            urwid.Divider(),
            self.create_menu_button("Pods", self.show_pods),
            self.create_menu_button("Deployments", self.show_deployments),
            urwid.Divider(),
            urwid.Text("Network:"),
            urwid.Divider(),
            self.create_menu_button("Services", self.show_services),
            self.create_menu_button("Ingresses", self.show_ingresses),
            urwid.Divider(),
            urwid.Text("Other:"),
            urwid.Divider(),
            self.create_menu_button("Namespaces", self.show_namespaces),
            urwid.Divider(),
            urwid.Text("Tools:"),
            urwid.Divider(),
            self.create_menu_button("Terminal", self.show_terminal),
        ])
        return urwid.LineBox(menu_content, title="Menu")

    def create_menu_button(self, label, callback):
        button = urwid.Button(label)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')

    def resource_selection_screen(self):
        self.sidebar = self.build_sidebar()
        self.body = urwid.Text(".")
        self.columns = urwid.Columns([('fixed', 20, self.sidebar), urwid.Filler(self.body)])
        self.frame.body = self.columns

    def show_terminal(self, button):
        # The terminal is always at the bottom, no need to switch body content
        pass

    def show_pods(self, button):
        self.show_resources('pods')

    def show_deployments(self, button):
        self.show_resources('deployments')

    def show_services(self, button):
        self.show_resources('services')

    def show_ingresses(self, button):
        self.show_resources('ingresses')

    def show_namespaces(self, button):
        self.show_resources('namespaces')

    def show_resources(self, resource_type):
        if not self.config_loaded:
            error_text = urwid.Text(('failed', "Configuration not loaded. Please load your configuration first."))
            self.body = urwid.ListBox(urwid.SimpleFocusListWalker([error_text]))
            self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
            self.loop.draw_screen()
            return
        
        try:
            if resource_type == 'pods':
                resources = self.workloads.list_pods_detailed()
                self.body = build_pod_table(resources, self.edit_pod)
            elif resource_type == 'deployments':
                resources = self.workloads.list_deployments_detailed()
                self.body = build_deployment_table(resources, self.edit_deployment)
            elif resource_type == 'services':
                resources = self.network.list_services()
                self.body = build_service_table(resources, self.edit_service)
            elif resource_type == 'ingresses':
                resources = self.network.list_ingresses()
                self.body = build_ingress_table(resources, self.edit_ingress)
            elif resource_type == 'namespaces':
                resources = self.namespace.list_namespaces()
                self.body = build_namespace_table(resources)
            self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
        except Exception as e:
            error_text = urwid.Text(('failed', f"Error fetching {resource_type}: {str(e)}"))
            self.body = urwid.ListBox(urwid.SimpleFocusListWalker([error_text]))
            self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
            self.loop.draw_screen()

    def edit_pod(self, button, pod):
        namespace = pod['namespace']
        name = pod['name']
        yaml_content = self.workloads.get_pod_yaml(namespace, name)
        formatted_yaml = yaml.safe_dump(yaml.safe_load(yaml_content), default_flow_style=False)
        edit_widget = urwid.Edit(edit_text=formatted_yaml)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Editing {namespace}/{name}"),
            urwid.Divider(),
            edit_widget,
            urwid.Divider(),
            urwid.Button("Save", self.save_pod, (namespace, name, edit_widget)),
            urwid.Button("Cancel", lambda button: self.resource_selection_screen())
        ]))
        self.frame.body = body

    def save_pod(self, button, data):
        namespace, name, edit_widget = data
        yaml_content = edit_widget.get_edit_text()
        self.workloads.update_pod_yaml(namespace, name, yaml_content)
        self.resource_selection_screen()
        self.show_pods(button)

    def edit_ingress(self, button, ingress):
        namespace = ingress['namespace']
        name = ingress['name']
        yaml_content = self.network.get_ingress_yaml(namespace, name)
        formatted_yaml = yaml.safe_dump(yaml.safe_load(yaml_content), default_flow_style=False)
        edit_widget = urwid.Edit(edit_text=formatted_yaml)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Editing {namespace}/{name}"),
            urwid.Divider(),
            edit_widget,
            urwid.Divider(),
            urwid.Button("Save", self.save_ingress, (namespace, name, edit_widget)),
            urwid.Button("Cancel", lambda button: self.resource_selection_screen())
        ]))
        self.frame.body = body

    def save_ingress(self, button, data):
        namespace, name, edit_widget = data
        yaml_content = edit_widget.get_edit_text()
        try:
            self.network.update_ingress_yaml(namespace, name, yaml_content)
            self.resource_selection_screen(None)
            self.show_ingresses(button)
        except Exception as e:
            error_text = urwid.Text(('failed', f"Error saving ingress: {str(e)}"))
            self.frame.body.body.insert(4, error_text)
            self.loop.draw_screen()

    def edit_service(self, button, service):
        namespace = service['namespace']
        name = service['name']
        yaml_content = self.network.get_service_yaml(namespace, name)
        formatted_yaml = yaml.safe_dump(yaml.safe_load(yaml_content), default_flow_style=False)
        edit_widget = urwid.Edit(edit_text=formatted_yaml)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Editing {namespace}/{name}"),
            urwid.Divider(),
            edit_widget,
            urwid.Divider(),
            urwid.Button("Save", self.save_service, (namespace, name, edit_widget)),
            urwid.Button("Cancel", lambda button: self.resource_selection_screen())
        ]))
        self.frame.body = body

    def save_service(self, button, data):
        namespace, name, edit_widget = data
        yaml_content = edit_widget.get_edit_text()
        self.network.update_service_yaml(namespace, name, yaml_content)
        self.resource_selection_screen()
        self.show_services(button) 

    def edit_deployment(self, button, deployment):
        namespace = deployment['namespace']
        name = deployment['name']
        yaml_content = self.workloads.get_deployment_yaml(namespace, name)
        formatted_yaml = yaml.safe_dump(yaml.safe_load(yaml_content), default_flow_style=False)
        edit_widget = urwid.Edit(edit_text=formatted_yaml)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Editing {namespace}/{name}"),
            urwid.Divider(),
            edit_widget,
            urwid.Divider(),
            urwid.Button("Save", self.save_deployment, (namespace, name, edit_widget)),
            urwid.Button("Cancel", lambda button: self.resource_selection_screen())
        ]))
        self.frame.body = body

    def save_deployment(self, button, data):
        namespace, name, edit_widget = data
        yaml_content = edit_widget.get_edit_text()
        self.workloads.update_deployment_yaml(namespace, name, yaml_content)
        self.resource_selection_screen()
        self.show_deployments(button)

    def close_connection(self, button):
        self.workloads = None
        self.network = None
        self.namespace = None
        self.config_loaded = False
        self.load_main_menu()

    def back_to_main(self, button):
        self.load_main_menu()

    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if isinstance(self.frame.footer, TerminalWidget):
            self.frame.footer.handle_input(key)

    def run(self):
        self.load_main_menu()
        self.loop.run()

if __name__ == "__main__":
    CarbonUI().run()
