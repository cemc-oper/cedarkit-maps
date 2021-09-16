import pkg_resources

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader


def get_china_map():
    china_shape_file = pkg_resources.resource_filename(
        "meda", "resources/map/china-shapefiles/shapefiles/china.shp"
    )
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
    china_nine_dotted_shape_file = pkg_resources.resource_filename(
        "meda", "resources/map/china-shapefiles/shapefiles/china_nine_dotted_line.shp"
    )
    china_nine_dotted_shape_reader = Reader(china_nine_dotted_shape_file)

    projection = ccrs.PlateCarree()
    nine_feature = cfeature.ShapelyFeature(
        china_nine_dotted_shape_reader.geometries(),
        projection,
        edgecolor='k',
        facecolor='none'
    )

    return [nine_feature]
