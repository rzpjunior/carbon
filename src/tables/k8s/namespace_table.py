import urwid

def build_namespace_table(namespaces, edit_callback=None, delete_callback=None):
    table_header = urwid.Columns([
        urwid.Text("Namespace Name", align='center'),
        urwid.Text("Actions", align='center'),
    ])

    rows = [table_header, urwid.Divider()]

    for namespace in namespaces:
        edit_button = urwid.Button("Edit")
        if edit_callback:
            urwid.connect_signal(edit_button, 'click', edit_callback, namespace)

        delete_button = urwid.Button("Delete")
        if delete_callback:
            urwid.connect_signal(delete_button, 'click', delete_callback, namespace)

        buttons = urwid.Columns([
            urwid.AttrMap(edit_button, None, focus_map='reversed'),
            urwid.AttrMap(delete_button, None, focus_map='reversed')
        ])

        row = urwid.Columns([
            urwid.Text(namespace['name'], align='center'),
            buttons
        ])

        rows.append(row)

    return urwid.ListBox(urwid.SimpleFocusListWalker(rows))
