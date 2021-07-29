import pkg_resources
import re
from pathlib import Path
from typing import Optional, List

import numpy as np
import matplotlib.colors as mcolors


def get_ncl_colormap(name, index: Optional[np.ndarray] = None, face_color="white") -> Optional[mcolors.ListedColormap]:
    """
    Generate Matplotlib colormap from NCL color map files in resource directory.

    Parameters
    ----------
    name
        ncl color map name without extension.
    index
    face_color

    Returns
    -------
    matplotlib.colors.ListedColormap
    """
    raw_colormap = _get_raw_ncl_colormap(name)
    if raw_colormap is None or index is None:
        return raw_colormap

    colors = []
    if index[0] == -1:
        colors = [face_color]
        index = index[1:]
    raw_colors = raw_colormap(index)
    colors.extend(raw_colors)
    color_map = mcolors.ListedColormap(colors)
    return color_map


def _get_raw_ncl_colormap(name) -> mcolors.ListedColormap:
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
