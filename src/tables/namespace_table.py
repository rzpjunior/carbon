import urwid

def build_namespace_table(resources):
    headers = ['Name']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([('weight', 1, table_header[0])], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for resource in resources:
        row = [urwid.Text(resource['name'])]
        table_row = urwid.AttrMap(urwid.Columns([('weight', 1, row[0])], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
