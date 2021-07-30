import pkg_resources
from typing import Dict

from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.axes


def get_china_map():
    projection = ccrs.PlateCarree()
    shape_names = [
        dict(name="BOUL_G", type="g"),
        dict(name="BOUL_JDX", type="g"),
        dict(name="BOUL_GU", type="gu"),
        dict(name="HAX", type="h"),
        dict(name="BOUL_S", type="s"),
        dict(name="BOUL_S2", type="s2"),
        dict(name="HYDL", type="r"),
        dict(name="HFCP_NH", type="h")
    ]
    features = []
    for shape_item in shape_names:
        shape_name = shape_item["name"]
        map_type = shape_item["type"]
        shape_file_name = pkg_resources.resource_filename(
            "nwpc_meda_data", f"resources/maps/portrait/{shape_name}.shp"
        )
        reader = Reader(shape_file_name)
        feature_style = get_map_feature_style(map_type)
        feature = cfeature.ShapelyFeature(
            reader.geometries(),
            projection,
            facecolor="none",
            **feature_style
        )
        features.append(feature)

    return features


def get_china_nine_map():
    projection = ccrs.PlateCarree()
    shape_names = [
        dict(name="BOUL_G", type="g"),
        dict(name="BOUL_JDX", type="g"),
        dict(name="HAX", type="h"),
        dict(name="BOUL_S", type="s"),
        dict(name="BOUL_S2", type="s2"),
        dict(name="HFCP_NH", type="h")
    ]
    features = []
    for shape_item in shape_names:
        shape_name = shape_item["name"]
        map_type = shape_item["type"]
        shape_file_name = pkg_resources.resource_filename(
            "nwpc_meda_data", f"resources/maps/landscape/NANHAI/{shape_name}.shp"
        )
        reader = Reader(shape_file_name)
        feature_style = get_map_feature_style(map_type)
        feature = cfeature.ShapelyFeature(
            reader.geometries(),
            projection,
            facecolor="none",
            **feature_style
        )
        features.append(feature)

    return features


def get_map_feature_style(map_type):
    m = dict(
        g=dict(
            edgecolor="k",
            linewidth=1.5,
        ),
        gu=dict(
            edgecolor="k",
            linestyle=(0, (2, 1)),
            linewidth=1.5,
        ),
        s=dict(
            edgecolor="k",
            linewidth=0.8,
        ),
        s2=dict(
            edgecolor="k",
            linestyle="--",
            linewidth=1.8,
        ),
        r=dict(
            edgecolor="dodgerblue",
            linewidth=1.5,
        ),
        h=dict(
            edgecolor="dodgerblue",
            linewidth=1.2,
        ),
        m=dict(
            edgecolor="dodgerblue"
        )
    )
    return m[map_type]


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
