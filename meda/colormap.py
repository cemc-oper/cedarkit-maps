import pkg_resources
import re
from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.colors as mcolors


def get_ncl_colormap(name) -> Optional[mcolors.ListedColormap]:
    """
    Generate Matplotlib colormap from NCL color map files in resource directory.

    Parameters
    ----------
    name
        ncl color map name without extension.

    Returns
    -------
    matplotlib.colors.ListedColormap
    """
    color_map_dir = pkg_resources.resource_filename("meda", "resources/colormap/ncl")
    color_map_path = Path(color_map_dir, f"{name}.rgb")
    if not color_map_path.exists():
        color_map_path = Path(color_map_dir, f"{name}.gp")
    if not color_map_path.exists():
        return None

    prog = re.compile(r"\s+(\d+)\s+(\d+)\s+(\d+)")
    with open(color_map_path, "r") as f:
        buff = f.read()
        r = prog.findall(buff)
        rgbs = np.asarray(r, dtype="i4") / 255
        color_map = mcolors.ListedColormap(rgbs, name)
        return color_map
