import urwid
import yaml
import os

from src.kubernetes.workloads import Workloads
from src.kubernetes.network import Network
from src.kubernetes.namespace import Namespace
from src.kubernetes.config import Config
from src.utils.config_loader import load_config
from src.tables.k8s.pod_table import build_pod_table
from src.tables.k8s.deployment_table import build_deployment_table
from src.tables.k8s.service_table import build_service_table
from src.tables.k8s.ingress_table import build_ingress_table
from src.tables.k8s.namespace_table import build_namespace_table
from src.tables.k8s.configmap_table import build_configmap_table
from src.tables.k8s.secret_table import build_secret_table
from src.com.terminal import TerminalWidget
from src.resources.resource_creator import ResourceCreator
from src.com.loading import LoadingWidget
from src.com.main_menu import load_main_menu
from src.com.config_screen import load_config_screen
from src.com.sidebar import build_sidebar, get_sidebar_buttons

class CarbonUI:
    def __init__(self):
        self.ascii_banner = urwid.Text("""
     _____   ___  ____________  _____ _   _ 
    /  __ \ / _ \ | ___ \ ___ \|  _  | \ | |
    | /  \// /_\ \| |_/ / |_/ /| | | |  \| |
    | |    |  _  ||    /| ___ \| | | | . ` |
    | \__/\| | | || |\ \| |_/ /\ \_/ / |\  |
     \____/\_| |_/\_| \_\____/  \___/\_| \_/
    ver 1.0.0
                                            
    Simplifying Kubernetes with a GUI-Based Terminal
                                        by rzpjunior
        """, align='center')
        self.header = urwid.AttrMap(urwid.Text("CARBON - Simple Kubernetes GUI-based Terminal", align='center'), 'header')
        self.body = urwid.Text("Please select a provider to get started.")
        self.terminal = TerminalWidget()
        self.frame = urwid.Frame(header=self.header, body=self.body, footer=None)
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
        self.editing = False 
        self.resource_creator = ResourceCreator(self)
        self.loading_widget = LoadingWidget()

    def load_main_menu(self):
        self.body = load_main_menu(self.ascii_banner, self.choose_provider, self.back_to_main)
        self.frame.body = self.body
        self.frame.footer = None

    def choose_provider(self, button, provider):
        self.provider = provider
        self.load_config_screen()

    def load_config_screen(self):
        self.body, self.config_edit = load_config_screen(self.ascii_banner, self.load_config, self.back_to_main)
        self.frame.body = self.body
        self.frame.footer = None

    def load_config(self, button):
        config_path = self.config_edit.get_edit_text()
        try:
            load_config(config_path)
            self.set_kubectl_config(config_path)
            self.config_loaded = True
            self.workloads = Workloads()
            self.network = Network()
            self.namespace = Namespace()
            self.config = Config()
            self.resource_selection_screen()
            self.frame.footer = self.terminal
        except Exception as e:
            error_text = urwid.Text(('failed', f"Error loading configuration: {str(e)}"))
            self.body.body.append(error_text)
            self.loop.draw_screen()

    def set_kubectl_config(self, config_path):
        os.environ['KUBECONFIG'] = config_path

    def build_sidebar(self):
        menu_buttons = get_sidebar_buttons(self)
        self.sidebar = build_sidebar(menu_buttons)

    def resource_selection_screen(self):
        self.build_sidebar()
        self.body = urwid.Text(".")
        self.columns = urwid.Columns([('fixed', 20, self.sidebar), urwid.Filler(self.body)])
        self.frame.body = self.columns

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

    def show_configmaps(self, button):
        self.show_resources('configmaps')

    def show_secrets(self, button):
        self.show_resources('secrets')

    def show_loading(self):
        loading_text = urwid.Text("Loading resources, please wait...", align='center')
        loading_spinner = urwid.Padding(self.loading_widget, align='center', width=('relative', 100))
        loading_pile = urwid.Pile([loading_text, urwid.Divider(), loading_spinner])
        self.body = urwid.Filler(loading_pile, valign='middle')
        self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
        self.loading_widget.start(self.loop)
        self.loop.draw_screen()

    def show_resources(self, resource_type):
        if not self.config_loaded:
            error_text = urwid.Text(('failed', "Configuration not loaded. Please load your configuration first."))
            self.body = urwid.ListBox(urwid.SimpleFocusListWalker([error_text]))
            self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
            self.loop.draw_screen()
            return

        self.show_loading()
        
        def fetch_resources(loop, user_data):
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
                elif resource_type == 'configmaps':
                    resources = self.config.list_configmaps()
                    self.body = build_configmap_table(resources, self.edit_configmap)
                elif resource_type == 'secrets':
                    resources = self.config.list_secrets()
                    self.body = build_secret_table(resources, self.edit_secret)
                elif resource_type == 'namespaces':
                    resources = self.namespace.list_namespaces()
                    self.body = build_namespace_table(resources, self.edit_namespace, self.delete_namespace)
                self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
                self.loading_widget.stop()
            except Exception as e:
                error_text = urwid.Text(('failed', f"Error fetching {resource_type}: {str(e)}"))
                self.body = urwid.ListBox(urwid.SimpleFocusListWalker([error_text]))
                self.columns.contents[1] = (self.body, self.columns.options('weight', 1))
                self.loading_widget.stop()
                self.loop.draw_screen()
        
        self.loop.set_alarm_in(0.1, fetch_resources)

    def delete_namespace(self, button, namespace):
        try:
            self.namespace.delete_namespace(namespace['name'])
            self.show_namespaces(button)
        except Exception as e:
            error_text = urwid.Text(('failed', f"Error deleting namespace: {str(e)}"))
            self.body.body.append(error_text)
            self.loop.draw_screen()

    def edit_namespace(self, button, namespace):
        yaml_content = self.namespace.get_namespace_yaml(namespace['name'])
        formatted_yaml = yaml.safe_dump(yaml_content, default_flow_style=False)
        edit_widget = urwid.Edit(edit_text=formatted_yaml, multiline=True)
        save_button = urwid.Button("Save", self.save_namespace, (namespace['name'], edit_widget))
        cancel_button = urwid.Button("Cancel", lambda button: self.resource_selection_screen())
        footer = urwid.Columns([save_button, cancel_button], dividechars=2)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Editing {namespace['name']}"),
            urwid.Divider(),
            edit_widget,
            urwid.Divider(),
            footer
        ]))
        self.frame.body = urwid.Frame(body, footer=footer)
        self.edit_widget = edit_widget
        self.save_button = save_button
        self.cancel_button = cancel_button
        self.current_edit_resource = 'namespace'
        self.namespace_name = namespace['name']
        self.editing = True

    def save_namespace(self, button, data):
        name, edit_widget = data
        yaml_content = yaml.safe_load(edit_widget.get_edit_text())
        self.namespace.update_namespace_yaml(name, yaml_content)
        self.resource_selection_screen()
        self.show_namespaces(button)

    def edit_resource(self, button, resource, get_yaml_func, save_func, resource_type):
        namespace = resource['namespace']
        name = resource['name']
        yaml_content = get_yaml_func(namespace, name)
        formatted_yaml = yaml.safe_dump(yaml.safe_load(yaml_content), default_flow_style=False)
        edit_widget = urwid.Edit(edit_text=formatted_yaml, multiline=True)
        save_button = urwid.Button("Save", save_func, (namespace, name, edit_widget))
        cancel_button = urwid.Button("Cancel", lambda button: self.resource_selection_screen())
        footer = urwid.Columns([save_button, cancel_button], dividechars=2)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Editing {namespace}/{name}"),
            urwid.Divider(),
            edit_widget,
            urwid.Divider(),
            footer
        ]))
        self.frame.body = urwid.Frame(body, footer=footer)
        self.edit_widget = edit_widget
        self.save_button = save_button
        self.cancel_button = cancel_button
        self.current_edit_resource = resource_type
        self.namespace = namespace
        self.name = name
        self.editing = True

    def save_resource(self, button, data, update_func, show_func):
        namespace, name, edit_widget = data
        yaml_content = edit_widget.get_edit_text()
        update_func(namespace, name, yaml_content)
        self.resource_selection_screen()
        show_func(button)
        self.editing = False

    def create_ingress(self, button):
        self.resource_creator.create_resource_screen('Ingress')

    def create_deployment(self, button):
        self.resource_creator.create_resource_screen('Deployment')

    def create_service(self, button):
        self.resource_creator.create_resource_screen('Service')

    def create_namespace(self, button):
        self.resource_creator.create_resource_screen('Namespace')

    def create_secret(self, button):
        self.resource_creator.create_resource_screen('Secret')

    def create_configmap(self, button):
        self.resource_creator.create_resource_screen('ConfigMap')

    def edit_pod(self, button, pod):
        self.edit_resource(button, pod, self.workloads.get_pod_yaml, self.save_pod, 'pod')

    def save_pod(self, button, data):
        self.save_resource(button, data, self.workloads.update_pod_yaml, self.show_pods)

    def edit_ingress(self, button, ingress):
        self.edit_resource(button, ingress, self.network.get_ingress_yaml, self.save_ingress, 'ingress')

    def save_ingress(self, button, data):
        self.save_resource(button, data, self.network.update_ingress_yaml, self.show_ingresses)

    def edit_service(self, button, service):
        self.edit_resource(button, service, self.network.get_service_yaml, self.save_service, 'service')

    def save_service(self, button, data):
        self.save_resource(button, data, self.network.update_service_yaml, self.show_services)

    def edit_deployment(self, button, deployment):
        self.edit_resource(button, deployment, self.workloads.get_deployment_yaml, self.save_deployment, 'deployment')

    def save_deployment(self, button, data):
        self.save_resource(button, data, self.workloads.update_deployment_yaml, self.show_deployments)
    
    def edit_configmap(self, button, configmap):
        self.edit_resource(button, configmap, self.config.get_configmap_yaml, self.save_configmap, 'configmap')

    def save_configmap(self, button, data):
        self.save_resource(button, data, self.config.update_configmap_yaml, self.show_configmaps)

    def edit_secret(self, button, secret):
        self.edit_resource(button, secret, self.config.get_secret_yaml, self.save_secret, 'secret')

    def save_secret(self, button, data):
        self.save_resource(button, data, self.config.update_secret_yaml, self.show_secrets)

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

        if isinstance(key, tuple) and key[0] in ('mouse press', 'mouse release', 'mouse drag', 'ctrl mouse release', 'ctrl mouse press'):
            return

        if self.editing:
            if key == 'ctrl x':
                self.resource_selection_screen()
                self.editing = False
            elif key == 'ctrl o':
                if self.current_edit_resource == 'pod':
                    self.save_pod(None, (self.namespace, self.name, self.edit_widget))
                elif self.current_edit_resource == 'ingress':
                    self.save_ingress(None, (self.namespace, self.name, self.edit_widget))
                elif self.current_edit_resource == 'service':
                    self.save_service(None, (self.namespace, self.name, self.edit_widget))
                elif self.current_edit_resource == 'deployment':
                    self.save_deployment(None, (self.namespace, self.name, self.edit_widget))
        else:
            if hasattr(self, 'edit_widget'):
                self.edit_widget.keypress((80,), key)

        if self.terminal:
            self.terminal.keypress((80,), key)

    def run(self):
        self.load_main_menu()
        self.loop.run()

if __name__ == "__main__":
    CarbonUI().run()
