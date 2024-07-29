import urwid

def build_ingress_table(resources):
    headers = ['Name', 'Namespace']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 2, table_header[0]), 
        ('weight', 2, table_header[1])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for resource in resources:
        row = [
            urwid.Text(resource['name']),
            urwid.Text(resource['namespace'])
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]), 
            ('weight', 2, row[1])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
