"""
CEMC 官方图片产品使用的中国区域底图，仅限 CEMC 内部使用

需要安装 cemc-meda-data 库，Metcode 地址 (仅 CEMC 内部访问，需要访问权限)

http://e.mc.met.cma/codingcorp/cedarkit/cemc-meda-data.git

如需使用，请联系 CEMC 获取。
"""
import importlib.resources
from typing import Dict, List

from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
import cartopy.crs as ccrs


MAP_PACKAGE_NAME = "cemc_meda_data"


def get_china_map() -> List[cfeature.Feature]:
    projection = ccrs.PlateCarree()
    shape_names = [
        dict(name="BOUL_G", type="g"),      # 陆地国界
        dict(name="BOUL_JDX", type="g"),    # 南海断续线
        dict(name="BOUL_GU", type="gu"),    # 未定国界
        dict(name="HAX", type="h"),         # 海岸线
        dict(name="BOUL_S", type="s"),      # 省界
        dict(name="BOUL_S2", type="s2"),    # 特别行政区界
        dict(name="HYDL", type="r"),        # 主要河流
        dict(name="HFCP_NH", type="h")      # 南海岛屿岸线
    ]
    features = []
    for shape_item in shape_names:
        shape_name = shape_item["name"]
        map_type = shape_item["type"]

        ref = importlib.resources.files(MAP_PACKAGE_NAME) / f"resources/maps/portrait/{shape_name}.shp"
        with importlib.resources.as_file(ref) as shape_file_name:
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


def get_china_nine_map() -> List[cfeature.Feature]:
    projection = ccrs.PlateCarree()
    shape_names = [
        dict(name="BOUL_G", type="g"),      # 陆地国界
        dict(name="BOUL_JDX", type="g"),    # 南海断续线
        dict(name="HAX", type="h"),         # 海岸线
        dict(name="BOUL_S", type="s"),      # 省界
        dict(name="BOUL_S2", type="s2"),    # 特别行政区界
        dict(name="HFCP_NH", type="h")      # 南海岛屿岸线
    ]
    features = []
    for shape_item in shape_names:
        shape_name = shape_item["name"]
        map_type = shape_item["type"]

        ref = importlib.resources.files(MAP_PACKAGE_NAME) / f"resources/maps/landscape/NANHAI/{shape_name}.shp"
        with importlib.resources.as_file(ref) as shape_file_name:
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


def get_map_feature_style(map_type: str) -> Dict:
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
