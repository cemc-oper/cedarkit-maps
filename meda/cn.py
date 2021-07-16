import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib as mpl

from .color_map import get_colormap_temp_19lev
from .map import get_china_map, get_china_nine_map


def draw_china_plot(
        field,
):
    projection = ccrs.PlateCarree()
    temp_19lev = get_colormap_temp_19lev()
    cn_features = get_china_map()
    nine_features = get_china_nine_map()

    fig = plt.figure(
        figsize=(6, 6),
        frameon=False,
        dpi=400
    )

    ax = fig.add_axes(
        [0.1, 0.1, 0.8, 0.8],
        # projection=ccrs.LambertConformal(
        #     central_longitude=105,
        #     central_latitude=90
        # ),
        projection=ccrs.PlateCarree()
    )

    # 添加底图
    # ax.add_feature(cfeature.LAND.with_scale('50m'))
    # ax.add_feature(cfeature.OCEAN.with_scale('50m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.5)
    # ax.add_feature(cfeature.RIVERS.with_scale('50m'), linewidth=0.5)
    # ax.add_feature(cfeature.LAKES.with_scale('50m'), linewidth=0.5)
    for f in cn_features:
        ax.add_feature(f)
    for f in nine_features:
        ax.add_feature(f)

    # 坐标轴
    #   坐标轴格式
    lon_formatter = LongitudeFormatter(
        zero_direction_label=True,
        degree_symbol="",
    )
    lat_formatter = LatitudeFormatter(
        degree_symbol=""
    )
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    #   标签位置
    ax.set_xticks(np.arange(70, 141, 10), crs=projection)
    ax.set_yticks(np.arange(15, 56, 5), crs=projection)
    #   标签大小
    ax.tick_params(
        "both",
        which="major",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelsize=5
    )

    # 网格线
    gl = ax.gridlines(
        crs=projection,
        draw_labels=False,
        linewidth=0.5,
        color='r',
        alpha=0.5,
        linestyle='--'
    )
    gl.ylocator = mticker.FixedLocator([20, 30, 40, 50])

    # 设置范围和大小
    ax.set_extent(
        [70, 140, 15, 55],
        crs=projection
    )
    ax.set_aspect((70 / 0.75) / (40 / 0.6), adjustable="box")

    # 填充图
    contour_lev = [
        -30, -26, -22, -18, -14, -10, -6, -2, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 40
    ]
    field.plot.contourf(
        ax=ax,
        transform=projection,
        vmin=-30,
        vmax=40,
        levels=contour_lev,
        add_colorbar=False,
        cmap=temp_19lev,
    )
    ax.set_title("")
    ax.set_xlabel("")
    ax.set_ylabel("")

    # 颜色条
    cax = ax.inset_axes([1.05, 0.02, 0.02, 0.96])
    norm = mcolors.BoundaryNorm(contour_lev, temp_19lev.N, extend="both")
    cbar = fig.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=temp_19lev),
        cax=cax,
        orientation="vertical",
        spacing='uniform',
        ticks=contour_lev,
        drawedges=True,
        extendrect=True,
    )
    cbar.ax.tick_params(
        "both",
        which="major",
        left=False,
        right=False,
        labelsize=7
    )
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs, ha='center')
    cbar.ax.yaxis.set_tick_params(pad=4)

    # 九段线子图
    sub_ax = fig.add_axes(
        [0.1, 0.18, 0.1, 0.14],
        # projection=ccrs.LambertConformal(
        #     central_longitude=114,
        #     central_latitude=90,
        # ),
        projection=ccrs.PlateCarree()
    )
    # sub_ax.add_feature(cfeature.LAND.with_scale('50m'))
    sub_ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.25)
    # sub_ax.add_feature(cfeature.OCEAN.with_scale('50m'))
    # sub_ax.add_feature(cfeature.RIVERS.with_scale('50m'))
    # sub_ax.add_feature(cfeature.LAKES.with_scale('50m'))

    for f in cn_features:
        sub_ax.add_feature(f, linewidth=0.5)
    for f in nine_features:
        sub_ax.add_feature(f, linewidth=1)

    sub_ax.set_extent(
        [105, 123, 2, 23],
        crs=projection
    )
    sub_ax.set_aspect((18 / 0.1) / (22 / 0.14), adjustable="box")
    sub_ax.set_adjustable('datalim')
    b = field.plot.contourf(
        ax=sub_ax,
        transform=projection,
        vmin=-30,
        vmax=40,
        levels=contour_lev,
        add_colorbar=False,
        cmap=temp_19lev
    )
    sub_ax.set_title("")

    sub_gl = sub_ax.gridlines(
        crs=projection,
        draw_labels=False,
        linewidth=0.2,
        color='r',
        alpha=0.5,
        linestyle='--'
    )
    sub_gl.ylocator = mticker.FixedLocator([10, 20])
    sub_gl.xlocator = mticker.FixedLocator([110, 120])

    # 绘制边界
    rect = mpatches.Rectangle(
        (-0.05, -0.05), 1.08, 1.08,
        edgecolor="black",
        fill=False,
        zorder=1000,
        lw=1.3,
        transform=ax.transAxes
    )
    rect = ax.add_patch(rect)
    rect.set_clip_on(False)

    # 标题
    ax.text(
        -0.05,
        1.03,
        "Temperature 2M ($^\circ$C)",
        verticalalignment="bottom",
        horizontalalignment='left',
        transform=ax.transAxes,
        fontsize=7,
    )
    ax.text(
        1.03,
        1.03,
        "GRAPES_GFS(NMC/CMA)",
        verticalalignment="bottom",
        horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=7,
    )
    ax.text(
        -0.05,
        -0.055,
        "2021071500 + 03h\n2021071508 + 03h",
        verticalalignment='top',
        horizontalalignment='left',
        transform=ax.transAxes,
        fontsize=7
    )
    ax.text(
        1.03,
        -0.055,
        "2021071503(UTC)\n2021071511(CST)",
        verticalalignment='top',
        horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=7
    )

    # 文本框
    ax.text(
        0.998,
        0.0022,
        "Scale 1:20000000 No:GS (2019) 1786",
        verticalalignment='bottom',
        horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=3,
        bbox=dict(
            boxstyle="round",
            edgecolor="black",
            facecolor="white",
            linewidth=0.5
        )
    )
    sub_ax.text(
        0.99,
        0.01,
        "Scale 1:40000000",
        verticalalignment='bottom',
        horizontalalignment='right',
        transform=sub_ax.transAxes,
        fontsize=3,
        bbox=dict(
            boxstyle="round",
            edgecolor="black",
            facecolor="white",
            linewidth=0.5
        )
    )

    plt.show()
