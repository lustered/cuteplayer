globaltheme = None

def theme(_theme: str) -> dict:
    import json
    import os
    global globaltheme 
    globaltheme = _theme

    path = os.path.realpath(__file__)[:-14] + "themes/" + _theme + '.json'
    with open(path) as f:
        colors = json.loads(f.read())
    return colors["colors"][0]

def tStyle()-> 'ttk.Style()':
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

    return style

