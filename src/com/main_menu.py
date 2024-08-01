import urwid

def load_main_menu(ascii_banner, choose_provider_callback, back_to_main_callback):
    body = urwid.Pile([
        ascii_banner,
        urwid.Divider(),
        urwid.Text("Choose your provider:", align='center'),
        urwid.Divider(),
        urwid.AttrMap(urwid.Button("DigitalOcean", choose_provider_callback, 'digitalocean'), None, focus_map='reversed'),
        urwid.AttrMap(urwid.Button("AWS", choose_provider_callback, 'aws'), None, focus_map='reversed'),
        urwid.Divider(),
        urwid.Text("Note: This will set the configuration for kubectl", align='center'),
    ])
    return urwid.Filler(body, valign='top')
