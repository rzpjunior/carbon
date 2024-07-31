import urwid

def build_service_table(services, edit_callback):
    headers = ['Name', 'Namespace', 'Type', 'Cluster IP', 'Ports', 'External IP', 'Selector', 'Age', 'Status']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 2, table_header[0]), 
        ('weight', 2, table_header[1]), 
        ('weight', 1, table_header[2]), 
        ('weight', 2, table_header[3]), 
        ('weight', 2, table_header[4]), 
        ('weight', 2, table_header[5]), 
        ('weight', 2, table_header[6]), 
        ('weight', 1, table_header[7]) 
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for service in services:
        status_attr = 'running' if service['status'] == 'Active' else 'pending' if service['status'] == 'Pending' else 'failed'
        row = [
            urwid.AttrMap(urwid.Button(service['name'], align='center', on_press=edit_callback, user_data=service), None, focus_map='reversed'),
            urwid.Text(service['namespace'], align='center'),
            urwid.Text(service['type'], align='center'),
            urwid.Text(service['cluster_ip'], align='center'),
            urwid.Text(service['ports'], align='center'),
            urwid.Text(service['external_ip'], align='center'),
            urwid.Text(service['age'], align='center'),
            urwid.AttrMap(urwid.Text(service['status'], align='center'), status_attr)
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]), 
            ('weight', 2, row[1]), 
            ('weight', 1, row[2]), 
            ('weight', 2, row[3]), 
            ('weight', 2, row[4]), 
            ('weight', 2, row[5]), 
            ('weight', 2, row[6]), 
            ('weight', 1, row[7])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
