import urwid

def build_sidebar(menu_buttons):
    menu_content = urwid.Pile(menu_buttons)
    return urwid.LineBox(menu_content, title="Menu")

def create_menu_button(label, callback):
    button = urwid.Button(label)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def get_sidebar_buttons(ui_instance):
    return [
        urwid.AttrMap(urwid.Text("Resources", align='center'), 'header'),
        urwid.Divider(),
        urwid.Text("Workloads:"),
        urwid.Divider(),
        create_menu_button("Pods", ui_instance.show_pods),
        create_menu_button("Deployments", ui_instance.show_deployments),
        urwid.Divider(),
        urwid.Text("Network:"),
        urwid.Divider(),
        create_menu_button("Services", ui_instance.show_services),
        create_menu_button("Ingresses", ui_instance.show_ingresses),
        urwid.Divider(),
        urwid.Text("Config:"),
        urwid.Divider(),
        create_menu_button("ConfigMaps", ui_instance.show_configmaps),
        create_menu_button("Secrets", ui_instance.show_secrets),
        urwid.Divider(),
        urwid.Text("Other:"),
        urwid.Divider(),
        create_menu_button("Namespaces", ui_instance.show_namespaces),
        urwid.Divider(),
        urwid.AttrMap(urwid.Text("Create", align='center'), 'header'),
        urwid.Divider(),
        create_menu_button("Ingress", ui_instance.create_ingress),
        create_menu_button("Deployment", ui_instance.create_deployment),
        create_menu_button("Service", ui_instance.create_service),
        create_menu_button("Namespace", ui_instance.create_namespace),
        create_menu_button("Secret", ui_instance.create_secret),
        create_menu_button("ConfigMap", ui_instance.create_configmap),
    ]
