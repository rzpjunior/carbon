import urwid

def build_configmap_table(configmaps, edit_callback):
    headers = ['Name', 'Namespace', 'Age']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 3, table_header[0]),
        ('weight', 3, table_header[1]),
        ('weight', 2, table_header[2])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for configmap in configmaps:
        row = [
            urwid.AttrMap(urwid.Button(configmap['name'], align="center", on_press=edit_callback, user_data=configmap), None, focus_map='reversed'),
            urwid.Text(configmap['namespace'], align='center'),
            urwid.Text(configmap['age'], align='center')
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 3, row[0]),
            ('weight', 3, row[1]),
            ('weight', 2, row[2])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
