from typing import List

import numpy as np
import matplotlib as mpl
import matplotlib.axes
import matplotlib.colorbar
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def draw_map_box(ax: matplotlib.axes.Axes) -> mpatches.Rectangle:
    """
    Draw a boundary box for map plot.

    Parameters
    ----------
    ax

    Returns
    -------
    mpatches.Rectangle
    """
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
    return rect


def set_map_box_title(
        ax: matplotlib.axes.Axes,
        top_left: str = None,
        top_right: str = None,
        bottom_left: str = None,
        bottom_right: str = None,
) -> List:
    """
    Set four corner title for map plot with a box.

    Parameters
    ----------
    ax
    top_left
    top_right
    bottom_left
    bottom_right

    Returns
    -------

    """

    if top_left is None:
        top_left_text = None
    else:
        top_left_text = ax.text(
            -0.05,
            1.03,
            top_left,
            verticalalignment="bottom",
            horizontalalignment='left',
            transform=ax.transAxes,
            fontsize=7,
        )

    if top_right is None:
        top_right_text = None
    else:
        top_right_text = ax.text(
            1.03,
            1.03,
            top_right,
            verticalalignment="bottom",
            horizontalalignment='right',
            transform=ax.transAxes,
            fontsize=7,
        )

    if bottom_left is None:
        bottom_left_text = None
    else:
        bottom_left_text = ax.text(
            -0.05,
            -0.055,
            bottom_left,
            verticalalignment='top',
            horizontalalignment='left',
            transform=ax.transAxes,
            fontsize=7
        )

    if bottom_right is None:
        bottom_right_text = None
    else:
        bottom_right_text = ax.text(
            1.03,
            -0.055,
            bottom_right,
            verticalalignment='top',
            horizontalalignment='right',
            transform=ax.transAxes,
            fontsize=7
        )

    return [top_left_text, top_right_text, bottom_left_text, bottom_right_text]


def add_map_box_info_text(ax: matplotlib.axes.Axes, text: str, map_type: str = "main"):
    if map_type == "main":
        x = 0.998
        y = 0.0022
    elif map_type == "sub":
        x = 0.99
        y = 0.01
    else:
        raise ValueError(f"map_type must be main or sub.")

    text_box = ax.text(
        x, y, text,
        verticalalignment='bottom',
        horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=3,
        bbox=dict(
            boxstyle="round",
            edgecolor="black",
            facecolor="white",
            linewidth=0.5,
        )
    )
    return text_box


def add_map_box_colorbar(
        ax: matplotlib.axes.Axes, colormap: mcolors.ListedColormap, levels: List
) -> matplotlib.colorbar.Colorbar:
    cax = ax.inset_axes([1.05, 0.02, 0.02, 0.96])
    norm = mcolors.BoundaryNorm(levels, colormap.N, extend="both")
    cbar = ax.get_figure().colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=colormap),
        cax=cax,
        orientation="vertical",
        spacing='uniform',
        ticks=levels,
        drawedges=True,
        extendrect=True,
        extendfrac='auto',  # 延伸相同长度
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
    cbar.ax.yaxis.set_tick_params(pad=7)
    return cbar


def set_map_box_area(ax, area, projection, aspect=None):
    east_lon, west_lon, south_lat, north_lat = area
    ax.set_extent(
        area,
        crs=projection
    )
    if aspect is None:
        return
    ax.set_aspect((abs(west_lon - east_lon) / aspect) / (abs(north_lat - south_lat) / 1.0), adjustable="box")
    return ax


def set_map_box_axis(ax, xticks, yticks, projection):
    # 坐标轴样式
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
    ax.set_xticks(xticks, crs=projection)
    ax.set_yticks(yticks, crs=projection)
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
    return ax


def draw_map_box_gridlines(ax, projection, xlocator=None, ylocator=None, linewidth=0.5):
    gl = ax.gridlines(
        crs=projection,
        draw_labels=False,
        linewidth=linewidth,
        color='r',
        alpha=0.5,
        linestyle='--',
    )
    if ylocator:
        gl.ylocator = mticker.FixedLocator(ylocator)
    if xlocator:
        gl.xlocator = mticker.FixedLocator(xlocator)
    return gl


def clear_xarray_plot_components(ax):
    ax.set_title("")
    ax.set_xlabel("")
    ax.set_ylabel("")
    return ax


def add_map_box_main_layout(fig, projection):
    ax = fig.add_axes(
        [0.1, 0.1, 0.8, 0.8],
        # projection=ccrs.LambertConformal(
        #     central_longitude=105,
        #     central_latitude=90
        # ),
        projection=projection
    )
    return ax


def add_map_box_sub_layout(fig, projection):
    ax = fig.add_axes(
        [0.1, 0.18, 0.1, 0.14],
        # projection=ccrs.LambertConformal(
        #     central_longitude=114,
        #     central_latitude=90,
        # ),
        projection=projection,
    )
    return ax
