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


def generate_north_polar_plot(
        figure_width=6,
        figure_height=6,
        figure_dpi=400
) -> matplotlib.axes.Axes:
    """
    生成北半球区域图片底图

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
    projection = ccrs.NorthPolarStereo(central_longitude=110)
    data_projection = ccrs.PlateCarree()

    fig = plt.figure(
        figsize=(figure_width, figure_height),
        frameon=False,
        dpi=figure_dpi
    )

    # 主区域
    ax = add_map_box_main_layout(fig, projection=projection, map_type="north_polar")

    #   添加底图
    add_common_map_feature(
        ax,
        coastline=dict(
            scale="50m",
            style=dict(linewidth=0.5)
        )
    )

    # 添加底图
    cn_features = get_china_map()
    nine_features = get_china_nine_map()
    for f in cn_features:
        ax.add_feature(f)
    for f in nine_features:
        ax.add_feature(f)

    # 坐标轴
    ticks = np.arange(0, 210, 30)
    etick = ['0'] + [
        r'%dE' % tick for tick in ticks if (tick != 0) & (tick != 180)
    ] + ['180']
    wtick = [r'%dW' % tick for tick in ticks if (tick != 0) & (tick != 180)]
    labels = etick + wtick[::-1]
    xticks = np.arange(0, 360, 30)
    yticks = np.full_like(xticks, -4)  # Latitude where the labels will be drawn
    for xtick, ytick, label in zip(xticks, yticks, labels):
        if label == "60W":
            ax.text(
                xtick,
                -0.5,
                label,
                fontsize=8,
                horizontalalignment='center',
                verticalalignment='bottom',
                transform=ccrs.Geodetic()
            )
        else:
            ax.text(
                xtick,
                ytick,
                label,
                fontsize=8,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ccrs.Geodetic()
            )

    # 网格线
    draw_map_box_gridlines(
        ax,
        projection=data_projection,
        ylocator=np.arange(0, 90, 15),
        xlocator=np.arange(-180, 180, 30),
        color="k"
    )

    # 设置区域范围
    set_map_box_area(
        ax,
        area=[-180, 180, 0, 90],
        projection=data_projection
    )

    # 设置图形边界形状
    theta = np.linspace(0, 2 * np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)

    # 绘制边框
    rect = draw_map_box_by_map_type(ax, map_type="north_polar")

    add_map_box_info_text(
        ax,
        "Scale 1:20000000 No:GS (2019) 1786",
        map_type="north_polar",
        component_type="main"
    )

    return ax
