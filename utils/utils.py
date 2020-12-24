def theme(_theme: str) -> dict:
    import json
    import os
    path = os.path.realpath(__file__)[:-14] + "themes/" + _theme + '.json'
    with open(path) as f:
        colors = json.loads(f.read())
    return colors["colors"][0]
