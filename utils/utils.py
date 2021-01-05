globaltheme = None
import json
import os
import mpv

def theme(_theme: str) -> dict:
    global globaltheme 
    globaltheme = _theme

    path = os.path.realpath(__file__)[:-14] + "themes/" + _theme + '.json'
    with open(path) as f:
        colors = json.loads(f.read())
    return colors["colors"][0]

def playVideo(path: str):
    """ Plays the video given the path using mpv """
    try:
        player = mpv.MPV(player_operation_mode='pseudo-gui',
                 script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3',
                 input_default_bindings=True,
                 input_vo_keyboard=True,
                 osc=True)

        player.play(path)
        player.wait_for_playback()
        player.terminate()
    except mpv.ShutdownError:
        player.terminate()
        del player


def tStyle() -> 'ttk.Style()':
    from tkinter import ttk 
    palette = theme(globaltheme) 

    ####################### STYLE #######################
    style = ttk.Style()

    ######## Treeview Styling
    style.configure(
        "Treeview",
        foreground=palette["textcolor"],
        background=palette["bgcolor"],
        borderwidth=0,
        fieldbackground=palette["bgcolor"],
        font=("ARCADECLASSIC", 10),
    )


    # Selected song highlight colors
    style.map("Treeview", background=[("selected", palette["highlightedsongbg"])])
    style.map("Treeview", foreground=[("selected", palette["highlightedsongfg"])])
    
    # Removing the selection dashed lines
    style.layout("Treeview.Item",
        [('Treeitem.padding', {'sticky': 'nswe', 'children': 
            [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
            ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                 ('Treeitem.text', {'side': 'left', 'sticky': ''}),
            ],
        })])

    ######## Treeview Header Styling
    style.configure(
        "Treeview.Heading",
        background=palette["headerbg"],
        foreground=palette["headertext"],
        borderwidth=0,
    )

    # Hover highlight color
    style.map("Treeview.Heading", background=[("selected", palette["bgcolor"])])
    style.map("Treeview.Heading", foreground=[("selected", palette["textcolor"])])

    ######## Tabs Styling ########  
    style.configure("TNotebook", 
            background=palette['bgcolor'],
            foreground=palette['bgcolor'],
            borderwidth=0)

    style.configure("TNotebook.Tab", font=("ARCADECLASSIC", 12))

    style.configure("TNotebook.Tab", background=palette['bgcolor'],borderwidth=0)
    style.configure("TNotebook.Tab", foreground=palette['buttonbg'],borderwidth=0)

    style.map("TNotebook.Tab", background=[("selected", palette['highlightedsongbg'])])
    style.map("TNotebook.Tab", foreground=[("selected", palette['highlightedsongfg'])])

    return style
