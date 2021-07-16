import matplotlib.colors as mcolors


def get_colormap_temp_19lev() -> mcolors.ListedColormap:
    rgbs = [
        (7, 30, 70),
        (7, 47, 107),
        (8, 82, 156),
        (33, 113, 181),
        (66, 146, 199),
        (90, 160, 205),
        (120, 191, 214),
        (170, 220, 230),
        (219, 245, 255),
        (240, 252, 255),
        (255, 240, 245),
        (255, 224, 224),
        (252, 187, 170),
        (252, 146, 114),
        (251, 106, 74),
        (240, 60, 43),
        (204, 24, 30),
        (166, 15, 20),
        (120, 10, 15),
        (95, 0, 0),
    ]
    rgbs_norm = [(a / 255, b / 255, c / 255) for a, b, c in rgbs]

    temp_19lev = mcolors.ListedColormap(rgbs_norm, "temp_19lev")
    return temp_19lev
