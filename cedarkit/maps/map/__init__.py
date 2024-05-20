import importlib
from enum import Enum
from typing import Dict, List, Optional

import cartopy.feature as cfeature
import matplotlib.axes


DEFAULT_MAP_LOADER_PACKAGE = "cedarkit.maps.map.default"


class MapType(Enum):
    Portrait = "portrait"
    SouthChinaSea = "south_china_sea"
    Global = "global"


class MapLoader:
    """
    Load map features from map resources (such as Cartopy and shapefiles).
    """
    def __init__(self, map_type: MapType = MapType.Portrait, **kwargs):
        self.map_type = map_type
        self.kwargs = kwargs

    def coastline(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        ...

    def land(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        ...

    def rivers(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        ...

    def lakes(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        ...

    def china_coastline(self) -> List[cfeature.Feature]:
        ...

    def china_borders(self) -> List[cfeature.Feature]:
        ...

    def china_provinces(self) -> List[cfeature.Feature]:
        ...

    def china_rivers(self) -> List[cfeature.Feature]:
        ...

    def china_nine_lines(self) -> List[cfeature.Feature]:
        ...

    def global_borders(self) -> List[cfeature.Feature]:
        ...


def set_default_map_loader_package(map_package: str):
    """
    设置默认地图包名

    Parameters
    ----------
    map_package
        地图包字符串，例如 ``cedarkit.maps.map.default``

    Returns
    -------

    """
    global DEFAULT_MAP_LOADER_PACKAGE
    DEFAULT_MAP_LOADER_PACKAGE = map_package
    return map_package


def get_map_loader_class(map_loader_package: Optional[str] = None):
    """
    get map loader class object.
    """
    if map_loader_package is None:
        map_loader_package = DEFAULT_MAP_LOADER_PACKAGE
    package = importlib.import_module(map_loader_package)
    return package.map_class


def get_china_map(map_package: Optional[str] = None) -> List[cfeature.Feature]:
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
        map_package = DEFAULT_MAP_LOADER_PACKAGE
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
        map_package = DEFAULT_MAP_LOADER_PACKAGE
    package = importlib.import_module(map_package)
    return package.get_china_nine_map()


def add_common_map_feature(
        ax: matplotlib.axes.Axes,
        coastline: Optional[Dict] = None,
        land: Optional[Dict] = None,
        ocean: Optional[Dict] = None,
        rivers: Optional[Dict] = None,
        lakes: Optional[Dict] = None,
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
        _add_feature(ax, ocean, cfeature.OCEAN)

    if rivers is not None:
        _add_feature(ax, rivers, cfeature.RIVERS)

    if lakes is not None:
        _add_feature(ax, lakes, cfeature.LAKES)

    return ax


def _add_feature(ax: matplotlib.axes.Axes, config: Dict, feature_item: cfeature.NaturalEarthFeature):
    scale = config.get("scale", "50m")
    style = config.get("style", dict())
    ax.add_feature(feature_item.with_scale(scale), **style)
