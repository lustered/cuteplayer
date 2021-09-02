globaltheme = None
import json
import os
import mpv

palette = {
    "bliss": [
        {
            "bgcolor": "#555657",
            "entrybg": "#555657",
            "textcolor": "#F5D1C8",
            "buttonbg": "#F5D1C8",
            "buttontext": "#555657",
            "volumetroughcolor": "#F5D1C8",
            "timelinetroughcolor": "#F5D1C8",
            "highlightedsongfg": "#555657",
            "highlightedsongbg": "#F5D1C8",
            "currentsongtext": "#F5D1C8",
            "volumetext": "#F5D1C8",
            "timelinetext": "#F5D1C8",
            "headerbg": "#555657",
            "headertext": "#F5D1C8",
            "activebuttonbg": "#dec0b8",
            "entrytext": "#dec0b8",
        },
    ],
    "rainy": [
        {
            "bgcolor": "#5a5c5e",
            "entrybg": "#7b8085",
            "textcolor": "#c5e1fa",
            "buttonbg": "#a2ccf2",
            "buttontext": "#5a5c5e",
            "volumetroughcolor": "#a2ccf2",
            "timelinetroughcolor": "#a2ccf2",
            "highlightedsongfg": "#7b8085",
            "highlightedsongbg": "#85a9c9",
            "currentsongtext": "#c5e1fa",
            "volumetext": "#c5e1fa",
            "timelinetext": "#c5e1fa",
            "headerbg": "#5a5c5e",
            "headertext": "#c5e1fa",
            "activebuttonbg": "#85a9c9",
            "entrytext": "#5a5c5e",
        }
    ],
    "pastel": [
        {
            "bgcolor": "#e6d5ed",
            "entrybg": "#c6aadf",
            "textcolor": "#000000",
            "buttonbg": "#ffc0cb",
            "buttontext": "#000000",
            "volumetroughcolor": "#c6aadf",
            "timelinetroughcolor": "#ffc0cb",
            "highlightedsongfg": "#c5a7d1",
            "highlightedsongbg": "#000000",
            "currentsongtext": "#000000",
            "volumetext": "#000000",
            "timelinetext": "#000000",
            "headerbg": "#e6d5ed",
            "headertext": "#000000",
            "activebuttonbg": "#dea9b2",
            "entrytext": "#000000",
        }
    ],
    "flame": [
        {
            "bgcolor": "#080707",
            "entrybg": "#472a25",
            "textcolor": "#c9483e",
            "buttonbg": "#661b15",
            "buttontext": "#000000",
            "volumetroughcolor": "#c9483e",
            "timelinetroughcolor": "#c9483e",
            "highlightedsongfg": "#000000",
            "highlightedsongbg": "#c9483e",
            "currentsongtext": "#c9483e",
            "volumetext": "#c9483e",
            "timelinetext": "#c4727a",
            "headerbg": "#000000",
            "headertext": "#c9483e",
            "activebuttonbg": "#9e2e35",
            "entrytext": "#f06a5b",
        }
    ],
    "icons": [{"headericon": "☪ "}],
}


def theme(_theme: str) -> dict:
    global globaltheme
    globaltheme = _theme

    # deprecated approach without py2app
    # themepath = os.path.join(os.getcwd(), "/utils/themes/" + _theme + ".json")
    # with open(themepath) as f:
    #     colors = json.loads(f.read())
    return palette[_theme][0]


def playVideo(path: str):
    """Plays the video given the path using mpv"""
    try:
        player = mpv.MPV(
            player_operation_mode="pseudo-gui",
            script_opts="osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3",
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
        )

        player.play(path)
        player.wait_for_playback()
        player.terminate()
    except mpv.ShutdownError:
        player.terminate()
        del player


def tStyle() -> "ttk.Style()":
    from tkinter import ttk

    palette = theme(globaltheme)

    ####################### STYLE #######################
    style = ttk.Style()
    style.theme_use("default")

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
    style.layout(
        "Treeview.Item",
        [
            (
                "Treeitem.padding",
                {
                    "sticky": "nswe",
                    "children": [
                        ("Treeitem.indicator", {"side": "left", "sticky": ""}),
                        ("Treeitem.image", {"side": "left", "sticky": ""}),
                        ("Treeitem.text", {"side": "left", "sticky": ""}),
                    ],
                },
            )
        ],
    )

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
    style.configure(
        "TNotebook",
        background=palette["bgcolor"],
        foreground=palette["bgcolor"],
        borderwidth=0,
    )

    style.configure("TNotebook.Tab", font=("ARCADECLASSIC", 12))

    style.configure("TNotebook.Tab", background=palette["bgcolor"], borderwidth=0)
    style.configure("TNotebook.Tab", foreground=palette["buttonbg"], borderwidth=0)

    style.map("TNotebook.Tab", background=[("selected", palette["highlightedsongbg"])])
    style.map("TNotebook.Tab", foreground=[("selected", palette["highlightedsongfg"])])

    return style
