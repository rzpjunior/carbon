import urwid
import yaml
import subprocess
from .yaml_generator import generate_yaml_dict

class ResourceCreator:
    def __init__(self, ui):
        self.ui = ui
        self.resource_fields = []
        self.edit_widget = None
        self.save_button = None
        self.cancel_button = None
        self.current_edit_resource = None
        self.namespace = None
        self.name = None

    def create_resource_screen(self, resource_type):
        body = [
            urwid.Text(f"Create {resource_type}"),
            urwid.Divider(),
        ]

        fields = self.get_fields_for_resource(resource_type)
        self.resource_fields = fields

        for field in fields:
            body.append(urwid.Text(f"{field['label']}:"))
            body.append(urwid.Edit(edit_text=field['default'], multiline=field.get('multiline', False)))

        body.append(urwid.Divider())
        create_button = urwid.Button("Create", self.save_resource_yaml, resource_type)
        cancel_button = urwid.Button("Cancel", lambda button: self.ui.resource_selection_screen())
        buttons = urwid.Columns([create_button, cancel_button], dividechars=2)
        body.append(buttons)

        self.ui.body = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.ui.frame.body = self.ui.body

    def get_fields_for_resource(self, resource_type):
        fields = {
            'Ingress': [{'label': 'Name', 'default': ''}, {'label': 'Namespace', 'default': 'default'}, {'label': 'Rules', 'default': '', 'multiline': True}],
            'Deployment': [{'label': 'Name', 'default': ''}, {'label': 'Namespace', 'default': 'default'}, {'label': 'Replicas', 'default': '1'}, {'label': 'Containers', 'default': '', 'multiline': True}],
            'Service': [{'label': 'Name', 'default': ''}, {'label': 'Namespace', 'default': 'default'}, {'label': 'Ports', 'default': '', 'multiline': True}],
            'Namespace': [{'label': 'Name', 'default': ''}],
            'Secret': [{'label': 'Name', 'default': ''}, {'label': 'Namespace', 'default': 'default'}, {'label': 'Data', 'default': '', 'multiline': True}],
            'ConfigMap': [{'label': 'Name', 'default': ''}, {'label': 'Namespace', 'default': 'default'}, {'label': 'Data', 'default': '', 'multiline': True}]
        }
        return fields.get(resource_type, [])

    def save_resource_yaml(self, button, resource_type):
        field_values = {}
        index = 2
        for field in self.resource_fields:
            while not isinstance(self.ui.body.body[index], urwid.Edit):
                index += 1
            field_values[field['label'].lower().replace(' ', '_')] = self.ui.body.body[index].edit_text
            index += 1

        yaml_dict = generate_yaml_dict(resource_type, field_values)
        yaml_content = yaml.safe_dump(yaml_dict, default_flow_style=False)

        self.edit_widget = urwid.Edit(edit_text=yaml_content, multiline=True)
        footer = urwid.Columns([urwid.Button("Save", self.apply_resource_yaml, (resource_type, yaml_content)), urwid.Button("Cancel", lambda button: self.ui.resource_selection_screen())], dividechars=2)
        body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.Text(f"Creating {resource_type}"),
            urwid.Divider(),
            self.edit_widget,
            urwid.Divider(),
            footer
        ]))
        self.ui.frame.body = urwid.Frame(body, footer=footer)

    def apply_resource_yaml(self, button, data):
        resource_type, yaml_content = data
        yaml_path = f"/tmp/{resource_type.lower()}.yaml"
        with open(yaml_path, "w") as file:
            file.write(yaml_content)

        try:
            result = subprocess.run(["kubectl", "apply", "-f", yaml_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            message = f"{resource_type} created successfully.\n{result.stdout.decode('utf-8')}"
        except subprocess.CalledProcessError as e:
            message = f"Error creating {resource_type}: {e.stderr.decode('utf-8')}"

        self.ui.resource_selection_screen()
        success_message = urwid.Text(message)
        self.ui.columns.contents[1] = (urwid.ListBox(urwid.SimpleFocusListWalker([success_message])), self.ui.columns.options('weight', 1))
        self.ui.loop.draw_screen()
