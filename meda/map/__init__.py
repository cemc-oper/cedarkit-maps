import importlib
from typing import Dict, List

import cartopy.feature as cfeature
import matplotlib.axes


DEFAULT_MAP_PACKAGE = "meda.map.default"


def set_default_map_package(map_package: str):
    """
    设置默认地图包名

    Parameters
    ----------
    map_package
        地图包字符串，例如 ``meda.map.default``

    Returns
    -------

    """
    global DEFAULT_MAP_PACKAGE
    DEFAULT_MAP_PACKAGE = map_package
    return map_package


def get_china_map(map_package=None) -> List[cfeature.Feature]:
    """
    中国区域

    Parameters
    ----------
    map_package
        地图包字符串，例如 ``meda.map.default``
    Returns
    -------

    """
    if map_package is None:
        map_package = DEFAULT_MAP_PACKAGE
    package = importlib.import_module(map_package)
    return package.get_china_map()


def get_china_nine_map(map_package=None) -> List[cfeature.Feature]:
    """
    九段线

    Parameters
    ----------
    map_package
        地图包名，例如 ``meda.map.default`` 表示 meda 自带的地图包

    Returns
    -------

    """
    if map_package is None:
        map_package = DEFAULT_MAP_PACKAGE
    package = importlib.import_module(map_package)
    return package.get_china_nine_map()


def add_common_map_feature(
        ax: matplotlib.axes.Axes,
        coastline: Dict = None,
        land: Dict = None,
        ocean: Dict = None,
        rivers: Dict = None,
        lakes: Dict = None,
) -> matplotlib.axes.Axes:
    """
    添加通用地图特征

    Parameters
    ----------
    ax
    coastline
        海岸线

        {
            "scale": "50m",
            "style": {
                "linewidth": 0.5,
                # ...
            }
        }
    land
    ocean
    rivers
    lakes

    Returns
    -------
    matplotlib.axes.Axes
    """
    if coastline is not None:
        _add_feature(ax, coastline, cfeature.COASTLINE)

    if land is not None:
        _add_feature(ax, land, cfeature.LAND)

    if ocean is not None:
        _add_feature(ax, land, cfeature.OCEAN)

    if rivers is not None:
        _add_feature(ax, land, cfeature.RIVERS)

    if lakes is not None:
        _add_feature(ax, land, cfeature.LAKES)

    return ax


def _add_feature(ax: matplotlib.axes.Axes, config: Dict, feature_item: cfeature.NaturalEarthFeature):
    scale = config.get("scale", "50m")
    style = config.get("style", dict())
    ax.add_feature(feature_item.with_scale(scale), **style)
