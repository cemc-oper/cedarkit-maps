"""
默认中国区域底图，使用 dongli/china-shapefiles 项目中的 Shapefile，已包含在本项目 resources 目录中。

项目地址：https://github.com/dongli/china-shapefiles
"""
import importlib.resources
from typing import List, Dict, Optional

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader

from . import MapType, MapLoader


class DefaultMapLoader(MapLoader):
    def __init__(self, map_type: MapType = MapType.Portrait, **kwargs):
        super().__init__(map_type=map_type, **kwargs)
        self.default_scale = "50m"

    def coastline(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        if scale is None:
            scale = self.default_scale
        feature_style = dict(
            edgecolor='black',
            facecolor='never',
        )
        if style is not None:
            feature_style.update(style)

        f = cfeature.NaturalEarthFeature(
            'physical', 'coastline',
            scale,
            **feature_style
        )
        return [f]

    def land(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        if scale is None:
            scale = self.default_scale
        feature_style = dict(
            facecolor='lightgrey',
        )
        if style is not None:
            feature_style.update(style)

        f = cfeature.NaturalEarthFeature(
            'physical', 'land',
            scale,
            **feature_style
        )
        return [f]

    def rivers(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        if scale is None:
            scale = self.default_scale
        feature_style = dict(
            edgecolor=cfeature.COLORS['water'],
            facecolor='never',
        )
        if style is not None:
            feature_style.update(style)

        f = cfeature.NaturalEarthFeature(
            'physical', 'rivers_lake_centerlines',
            scale,
            **feature_style
        )
        return [f]

    def lakes(self, scale: Optional[str] = None, style: Optional[Dict] = None) -> List[cfeature.Feature]:
        if scale is None:
            scale = self.default_scale
        feature_style = dict(
            edgecolor='none',
            facecolor=cfeature.COLORS['water'],
        )
        if style is not None:
            feature_style.update(style)

        f = cfeature.NaturalEarthFeature(
            'physical', 'lakes',
            scale,
            **feature_style
        )
        return [f]

    def china_coastline(self) -> List[cfeature.Feature]:
        return list()

    def china_borders(self) -> List[cfeature.Feature]:
        return get_china_map()

    def china_provinces(self) -> List[cfeature.Feature]:
        return list()

    def china_rivers(self) -> List[cfeature.Feature]:
        return list()

    def china_nine_lines(self) -> List[cfeature.Feature]:
        return get_china_nine_map()

    def global_borders(self) -> List[cfeature.Feature]:
        return list()


map_class = DefaultMapLoader


def get_china_map():
    ref = importlib.resources.files("cedarkit.maps") / "resources/map/china-shapefiles/shapefiles/china.shp"
    with importlib.resources.as_file(ref) as china_shape_file:
        china_shape_reader = Reader(china_shape_file)

        projection = ccrs.PlateCarree()
        cn_feature = cfeature.ShapelyFeature(
            china_shape_reader.geometries(),
            projection,
            edgecolor='k',
            facecolor='none'
        )

    return [cn_feature]


def get_china_nine_map():
    ref = importlib.resources.files("cedarkit.maps") / "resources/map/china-shapefiles/shapefiles/china_nine_dotted_line.shp"
    with importlib.resources.as_file(ref) as china_nine_dotted_shape_file:
        china_nine_dotted_shape_reader = Reader(china_nine_dotted_shape_file)

        projection = ccrs.PlateCarree()
        nine_feature = cfeature.ShapelyFeature(
            china_nine_dotted_shape_reader.geometries(),
            projection,
            edgecolor='k',
            facecolor='none'
        )

    return [nine_feature]
