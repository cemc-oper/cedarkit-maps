from typing import Tuple

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.axes
import matplotlib.path as mpath

from cedarkit.maps.map import (
    get_china_map,
    get_china_nine_map,
    add_common_map_feature
)
from cedarkit.maps.util import (
    draw_map_box_by_map_type,
    add_map_box_info_text,
    set_map_box_area,
    set_map_box_axis,
    draw_map_box_gridlines,
    add_map_box_main_layout,
)


def generate_europe_asia_plot(
        figure_width=6,
        figure_height=6,
        figure_dpi=400
) -> matplotlib.axes.Axes:
    """
    生成欧亚区域图片底图

    Parameters
    ----------
    figure_width
    figure_height
    figure_dpi
        分辨率，`figure_height` * `figure_width` = 图片宽像素点数

    Returns
    -------
    matplotlib.axes.Axes
        底图
    """
    data_projection = ccrs.PlateCarree()
    projection = ccrs.LambertConformal(
        central_longitude=95,
        standard_parallels=(30, 60)
    )

    cn_features = get_china_map()
    nine_features = get_china_nine_map()

    fig = plt.figure(
        figsize=(figure_width, figure_height),
        frameon=False,
        dpi=figure_dpi
    )

    # 主区域
    ax = add_map_box_main_layout(fig, projection=projection, map_type="europe_asia")

    #   添加底图
    add_common_map_feature(
        ax,
        coastline=dict(
            scale="50m",
            style=dict(linewidth=0.5)
        )
    )

    for f in cn_features:
        ax.add_feature(f)
    for f in nine_features:
        ax.add_feature(f)

    #   坐标轴
    # set_map_box_axis(
    #     ax,
    #     xticks=np.arange(70, 141, 10),
    #     yticks=np.arange(15, 56, 5),
    #     projection=projection
    # )

    #   网格线
    draw_map_box_gridlines(
        ax,
        projection=data_projection,
        ylocator=np.arange(0, 70, 10),
        xlocator=np.arange(20, 170, 10)
    )

    #   设置区域范围和长宽比
    set_map_box_area(
        ax,
        area=[20, 170, 0, 70],
        projection=data_projection,
    )

    lon_range = (20, 170)
    lat_range = (0, 70)

    res = 1
    vertices = [
        (lon, lat_range[0]) for lon in np.arange(lon_range[0], lon_range[1] + 1, res)
    ] + [
        (lon_range[1], lat) for lat in np.arange(lat_range[0], lat_range[1] + 1, res)
    ] + [
        (lon, lat_range[1]) for lon in np.arange(lon_range[1], lon_range[0] - 1, -res)
    ] + [
        (lon_range[0], lat) for lat in np.arange(lat_range[1], lat_range[0] - 1, -res)
    ]

    path = mpath.Path(vertices)
    proj_to_data = ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData
    ax.set_boundary(proj_to_data.transform_path(path))

    # 绘制边框
    rect = draw_map_box_by_map_type(ax)

    # 四角标题
    # set by user

    # 审图号文本框
    add_map_box_info_text(ax, "Scale 1:20000000 No:GS (2019) 1786", map_type="europe_asia")

    return ax
