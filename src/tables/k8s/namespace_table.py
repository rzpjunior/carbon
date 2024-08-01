import urwid

def build_namespace_table(namespaces, edit_callback=None, delete_callback=None):
    headers = ['Namespace', 'Action']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 2, table_header[0]),
        ('weight', 2, table_header[1])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]

    for namespace in namespaces:
        edit_button = urwid.Button("Edit")
        if edit_callback:
            urwid.connect_signal(edit_button, 'click', edit_callback, namespace)

        delete_button = urwid.Button("Delete")
        if delete_callback:
            urwid.connect_signal(delete_button, 'click', delete_callback, namespace)

        row = [
            urwid.Text(namespace['name'], align='center')
        ]

        buttons = urwid.Columns([
            urwid.AttrMap(edit_button, None, focus_map='reversed'),
            urwid.AttrMap(delete_button, None, focus_map='reversed')
        ])

        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]),
            ('weight', 2, buttons),
        ], dividechars=1), 'line')

        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
