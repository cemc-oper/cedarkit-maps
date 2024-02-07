from typing import Tuple

import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.axes

from cedarkit.maps.map import (
    get_china_map,
    get_china_nine_map,
    add_common_map_feature
)
from cedarkit.maps.util import (
    draw_map_box_by_map_type,
    add_map_box_info_text_by_map_type,
    set_map_box_area,
    set_map_box_axis,
    draw_map_box_gridlines,
    add_map_box_main_layout,
    add_map_box_sub_layout,
)


def generate_east_asia_plot(
        figure_width=6,
        figure_height=6,
        figure_dpi=400
) -> Tuple[matplotlib.axes.Axes, matplotlib.axes.Axes]:
    """
    生成东亚区域图片底图

    Parameters
    ----------
    figure_width
    figure_height
    figure_dpi
        分辨率，`figure_height` * `figure_width` = 图片宽像素点数

    Returns
    -------
    Tuple[matplotlib.axes.Axes, matplotlib.axes.Axes]
        主地图和子图
    """
    projection = ccrs.PlateCarree()
    cn_features = get_china_map()
    nine_features = get_china_nine_map()

    fig = plt.figure(
        figsize=(figure_width, figure_height),
        frameon=False,
        dpi=figure_dpi
    )

    # projection=ccrs.LambertConformal(
    #     central_longitude=105,
    #     central_latitude=90
    # )

    # 主区域
    ax = add_map_box_main_layout(fig, projection=projection, map_type="east_asia")

    #   添加底图
    add_common_map_feature(
        ax,
        coastline=dict(
            scale="50m",
            style=dict(
                linewidth=0.5,
                # zorder=50
            )
        )
    )

    for f in cn_features:
        ax.add_feature(
            f,
            # zorder=100
        )
    for f in nine_features:
        ax.add_feature(
            f,
            # zorder=100
        )

    #   坐标轴
    set_map_box_axis(
        ax,
        xticks=np.arange(70, 141, 10),
        yticks=np.arange(15, 56, 5),
        projection=projection
    )

    #   网格线
    draw_map_box_gridlines(
        ax,
        projection=projection,
        ylocator=[20, 30, 40, 50]
    )

    #   设置区域范围和长宽比
    set_map_box_area(
        ax,
        area=[70, 140, 15, 55],
        projection=projection,
        aspect=1.25  # 0.75/0.6
    )

    # 子区域
    sub_ax = add_map_box_sub_layout(fig, projection)

    #   添加地图
    add_common_map_feature(
        sub_ax,
        coastline=dict(
            scale="50m",
            style=dict(
                linewidth=0.25,
                # zorder=50
            ),
        )
    )

    for f in cn_features:
        sub_ax.add_feature(
            f,
            linewidth=0.5,
            # zorder=100
        )
    for f in nine_features:
        sub_ax.add_feature(
            f,
            linewidth=1,
            # zorder=100
        )

    #   区域：南海子图
    set_map_box_area(
        sub_ax,
        area=[105, 123, 2, 23],
        projection=projection,
        aspect=0.1 / 0.14
    )

    #   网格线
    draw_map_box_gridlines(
        sub_ax,
        projection=projection,
        xlocator=[110, 120],
        ylocator=[10, 20],
        linewidth=0.2,
    )

    # 绘制边框
    rect = draw_map_box_by_map_type(ax)

    # 四角标题
    # set by user

    # 审图号文本框
    add_map_box_info_text_by_map_type(ax, "Scale 1:20000000 No:GS (2019) 1786", component_type="main")
    add_map_box_info_text_by_map_type(sub_ax, "Scale 1:40000000", component_type="sub")

    return ax, sub_ax
