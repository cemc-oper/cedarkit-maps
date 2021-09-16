import importlib
from typing import Dict

import cartopy.feature as cfeature
import matplotlib.axes


DEFAULT_MAP_PACKAGE = "meda.map.default"


def set_default_map_package(map_package):
    global DEFAULT_MAP_PACKAGE
    DEFAULT_MAP_PACKAGE = map_package
    return map_package


def get_china_map(map_package=None):
    if map_package is None:
        map_package = DEFAULT_MAP_PACKAGE
    package = importlib.import_module(map_package)
    return package.get_china_map()


def get_china_nine_map(map_package=None):
    if map_package is None:
        map_package = DEFAULT_MAP_PACKAGE
    package = importlib.import_module(map_package)
    return package.get_china_nine_map()


def add_common_map_feature(ax: matplotlib.axes.Axes, coastline: Dict = None):
    """

    Parameters
    ----------
    ax
    coastline:

        {
            "scale": "50m",
            "style": {
                "linewidth": 0.5,
                # ...
            }
        }

    Returns
    -------

    """
    # ax.add_feature(cfeature.LAND.with_scale('50m'))
    # ax.add_feature(cfeature.OCEAN.with_scale('50m'))

    if coastline is not None:
        scale = coastline.get("scale", "50m")
        style = coastline.get("style", dict())
        ax.add_feature(cfeature.COASTLINE.with_scale(scale), **style)

    # ax.add_feature(cfeature.RIVERS.with_scale('50m'), linewidth=0.5)
    # ax.add_feature(cfeature.LAKES.with_scale('50m'), linewidth=0.5)
    return ax
