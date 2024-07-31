import urwid

def build_secret_table(secrets, edit_callback):
    headers = ['Name', 'Namespace', 'Type', 'Age']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 3, table_header[0]),
        ('weight', 3, table_header[1]),
        ('weight', 3, table_header[2]),
        ('weight', 2, table_header[3])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for secret in secrets:
        row = [
            urwid.AttrMap(urwid.Button(secret['name'], align="center", on_press=edit_callback, user_data=secret), None, focus_map='reversed'),
            urwid.Text(secret['namespace'], align='center'),
            urwid.Text(secret['type'], align='center'),
            urwid.Text(secret['age'], align='center')
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 3, row[0]),
            ('weight', 3, row[1]),
            ('weight', 3, row[2]),
            ('weight', 2, row[3])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
