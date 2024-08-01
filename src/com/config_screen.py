import urwid

def load_config_screen(ascii_banner, load_config_callback, back_to_main_callback):
    config_edit = urwid.Edit(caption="Path: ", edit_text="")
    body = urwid.Pile([
        ascii_banner,
        urwid.AttrMap(urwid.Text("Enter path to your YAML configuration", align='center'), 'header'),
        urwid.Divider(),
        config_edit,
        urwid.Divider(),
        urwid.AttrMap(urwid.Button("Load", load_config_callback), None, focus_map='reversed'),
        urwid.AttrMap(urwid.Button("Back", back_to_main_callback), None, focus_map='reversed'),
    ])
    return urwid.Filler(body, valign='top'), config_edit
