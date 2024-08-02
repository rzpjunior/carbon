import urwid

def build_pod_table(resources, edit_callback, log_callback):
    headers = ['Name', 'Namespace', 'Status', 'Restarts', 'Age', 'Action']
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
        status_attr = 'running' if resource['status'] == 'Running' else 'pending' if resource['status'] == 'Pending' else 'failed'

        edit_button = urwid.Button("Edit")
        urwid.connect_signal(edit_button, 'click', edit_callback, resource)

        log_button = urwid.Button("View Logs")
        urwid.connect_signal(log_button, 'click', log_callback, resource)

        row = [
            urwid.AttrMap(urwid.Text(resource['name'], align='center'), None, focus_map='reversed'),
            urwid.Text(resource['namespace'], align='center'),
            urwid.AttrMap(urwid.Text(resource['status'], align='center'), status_attr),
            urwid.Text(str(resource['restarts']), align='center'),
            urwid.Text(resource['age'], align='center')
        ]

        buttons = urwid.Columns([
            urwid.AttrMap(edit_button, None, focus_map='reversed'),
            urwid.AttrMap(log_button, None, focus_map='reversed')
        ])

        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]), 
            ('weight', 2, row[1]), 
            ('weight', 1, row[2]), 
            ('weight', 1, row[3]), 
            ('weight', 1, row[4]),
            ('weight', 2, buttons)
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
