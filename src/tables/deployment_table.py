import urwid

def build_deployment_table(resources, edit_callback):
    headers = ['Name', 'Namespace', 'Pods', 'Replicas', 'Age', 'Conditions']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 2, table_header[0]),
        ('weight', 2, table_header[1]),
        ('weight', 1, table_header[2]),
        ('weight', 1, table_header[3]),
        ('weight', 1, table_header[4]),
        ('weight', 2, table_header[5])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for resource in resources:
        conditions_attr = 'running' if 'Available' in resource['conditions'] else 'pending'
        row = [
            urwid.AttrMap(urwid.Button(resource['name'], on_press=edit_callback, user_data=resource), None, focus_map='reversed'),
            urwid.Text(resource['namespace'], align='center'),
            urwid.Text(resource['pods'], align='center'),
            urwid.Text(str(resource['replicas']), align='center'),
            urwid.Text(resource['age'], align='center'),
            urwid.AttrMap(urwid.Text(resource['conditions'], align='center'), conditions_attr)
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]),
            ('weight', 2, row[1]),
            ('weight', 1, row[2]),
            ('weight', 1, row[3]),
            ('weight', 1, row[4]),
            ('weight', 2, row[5])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
