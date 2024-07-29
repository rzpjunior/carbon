import urwid

def build_ingress_table(ingresses):
    headers = ['Name', 'Namespace', 'LoadBalancers', 'Rules', 'Age']
    table_header = [urwid.Text(header, align='center') for header in headers]
    table_header = urwid.AttrMap(urwid.Columns([
        ('weight', 2, table_header[0]), 
        ('weight', 2, table_header[1]), 
        ('weight', 2, table_header[2]), 
        ('weight', 4, table_header[3]), 
        ('weight', 1, table_header[4])
    ], dividechars=1), 'line')

    table_rows = [urwid.LineBox(table_header), urwid.Divider()]
    for ingress in ingresses:
        row = [
            urwid.Text(ingress['name'], align='center'),
            urwid.Text(ingress['namespace'], align='center'),
            urwid.Text(ingress['load_balancers'], align='center'),
            urwid.Text(ingress['rules'], align='center'),
            urwid.Text(ingress['age'], align='center')
        ]
        table_row = urwid.AttrMap(urwid.Columns([
            ('weight', 2, row[0]), 
            ('weight', 2, row[1]), 
            ('weight', 2, row[2]), 
            ('weight', 4, row[3]), 
            ('weight', 1, row[4])
        ], dividechars=1), 'line')
        table_rows.append(urwid.LineBox(table_row))

    return urwid.ListBox(urwid.SimpleFocusListWalker(table_rows))
