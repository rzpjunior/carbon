import urwid

def build_pod_table(resources, edit_callback):
    headers = ['Name', 'Namespace', 'Status', 'Restarts', 'Age']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 2, table_header[0]), 
        ('weight', 2, table_header[1]), 
        ('weight', 1, table_header[2]), 
        ('weight', 1, table_header[3]), 
        ('weight', 1, table_header[4])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for resource in resources:
        status_attr = 'running' if resource['status'] == 'Running' else 'pending' if resource['status'] == 'Pending' else 'failed'
        row = [
            urwid.AttrMap(urwid.Button(resource['name'], align='center', on_press=edit_callback, user_data=resource), None, focus_map='reversed'),
            urwid.Text(resource['namespace'], align='center'),
            urwid.AttrMap(urwid.Text(resource['status'], align='center'), status_attr),
            urwid.Text(str(resource['restarts']), align='center'),
            urwid.Text(resource['age'], align='center')
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]), 
            ('weight', 2, row[1]), 
            ('weight', 1, row[2]), 
            ('weight', 1, row[3]), 
            ('weight', 1, row[4])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))