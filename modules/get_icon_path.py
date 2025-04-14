import os

def get_icon_path(iconloc: str):
    if os.path.exists(iconloc):
        return iconloc
    elif os.path.exists(iconloc[iconloc.rfind('\\')+1:]):
        return iconloc[iconloc.rfind('\\')+1:]
    else:
        return None