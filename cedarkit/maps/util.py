from typing import List, Optional, Tuple
from dataclasses import dataclass

import pandas as pd
import matplotlib as mpl
import matplotlib.axes
import matplotlib.figure
import matplotlib.colorbar
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
from cartopy import crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def add_map_box_main_layout(fig, projection, map_type="east_asia") -> mpl.axes.Axes:
    """
    添加主绘图区域

    Parameters
    ----------
    fig
    projection
    map_type

    Returns
    -------
    mpl.axes.Axes
    """
    if map_type == "east_asia":
        width = 0.75
        height = 0.6
        layout = [(1 - width)/2, (1 - height)/2, width, height]
    elif map_type == "europe_asia":
        width = 0.75
        height = 0.6
        layout = [0.1, 0.1, width, height]
    elif map_type == "north_polar":
        width = 0.75
        height = 0.8
        layout = [0.1, 0.1, width, height]
    else:
        raise ValueError(f"map_type is not supported: {map_type}")
    ax = fig.add_axes(
        layout,
        # projection=ccrs.LambertConformal(
        #     central_longitude=105,
        #     central_latitude=90
        # ),
        projection=projection
    )
    return ax


def add_map_box_sub_layout(fig, projection):
    main_width = 0.75
    main_height = 0.6
    sub_width = 0.1
    sub_height = 0.14
    ax = fig.add_axes(
        [(1 - main_width)/2, (1 - main_height)/2, sub_width, sub_height],
        # projection=ccrs.LambertConformal(
        #     central_longitude=114,
        #     central_latitude=90,
        # ),
        projection=projection,
    )
    return ax


def draw_map_box(ax: matplotlib.axes.Axes, bottom_left_point, top_right_point) -> mpatches.Rectangle:
    """
    添加图形边框

    Parameters
    ----------
    ax
    bottom_left_point
    top_right_point

    Returns
    -------
    mpatches.Rectangle
    """
    width = top_right_point[0] - bottom_left_point[0]
    height = top_right_point[1] - bottom_left_point[1]

    rect = mpatches.Rectangle(
        bottom_left_point, width, height,
        transform=ax.transAxes,
        edgecolor="black",
        fill=False,
        zorder=1000,
        lw=1.3,
    )
    rect = ax.add_patch(rect)
    rect.set_clip_on(False)
    return rect


def draw_map_box_by_map_type(ax: matplotlib.axes.Axes, map_type="east_asia") -> mpatches.Rectangle:
    """
    添加图形边框

    Parameters
    ----------
    ax
    map_type

    Returns
    -------
    mpatches.Rectangle
    """
    if map_type == "east_asia":
        bottom_left_point = (-0.06, -0.05)
        top_right_point = (1.03, 1.03)
        width = top_right_point[0] - bottom_left_point[0]
        height = top_right_point[1] - bottom_left_point[1]
    elif map_type == "north_polar":
        bottom_left_point = (-0.05, -0.05)
        top_right_point = (1.07, 1.03)
        width = top_right_point[0] - bottom_left_point[0]
        height = top_right_point[1] - bottom_left_point[1]
    else:
        raise ValueError(f"component_type is not supported: {map_type}")

    rect = mpatches.Rectangle(
        bottom_left_point, width, height,
        edgecolor="black",
        fill=False,
        zorder=1000,
        lw=1.3,
        transform=ax.transAxes
    )
    rect = ax.add_patch(rect)
    rect.set_clip_on(False)
    return rect


@dataclass
class GraphTitle:
    top_left_label: Optional[str] = None
    top_right_label: Optional[str] = None
    bottom_left_label: Optional[str] = None
    bottom_right_label: Optional[str] = None
    top_left_pos: Optional[str] = None

    left: Optional[float] = None
    bottom: Optional[float] = None
    top: Optional[float] = None
    right: Optional[float] = None


def fill_graph_title(
        graph_title: GraphTitle,
        graph_name: str,
        system_name: str,
        start_time: pd.Timestamp,
        forecast_time: pd.Timedelta,
) -> GraphTitle:
    utc_start_time_label = start_time.strftime('%Y%m%d%H')
    utc_valid_time_label = (start_time + forecast_time).strftime('%Y%m%d%H')
    cst_start_time_label = (start_time + pd.Timedelta(hours=8)).strftime('%Y%m%d%H')
    cst_valid_time_label = (start_time + forecast_time + pd.Timedelta(hours=8)).strftime('%Y%m%d%H')
    forecast_time_label = f"{int(forecast_time / pd.Timedelta(hours=1)):02}"
    graph_title.top_left_label = graph_name
    graph_title.top_right_label = system_name
    graph_title.bottom_left_label = f"{utc_start_time_label}+{forecast_time_label}h\n{cst_start_time_label}+{forecast_time_label}h"
    graph_title.bottom_right_label = f"{utc_valid_time_label}(UTC)\n{cst_valid_time_label}(CST)"

    return graph_title


def fill_graph_title_pos(graph_title: GraphTitle, map_type="east_asia"):
    if map_type == "east_asia":
        left = -0.06
        bottom = -0.05 - 0.005
        top = 1.03
        right = 1.03
    elif map_type == "north_polar":
        left = -0.06
        bottom = -0.05 - 0.005
        top = 1.03
        right = 1.07
    else:
        raise ValueError(f"component_type is not supported: {map_type}")

    graph_title.left = left
    graph_title.bottom = bottom
    graph_title.top = top
    graph_title.right = right

    return graph_title


def set_map_box_title(
        ax: matplotlib.axes.Axes,
        graph_title: GraphTitle,
        fontsize: Optional[float] = None,
) -> List:
    """
    为图形边框设置标题

    Parameters
    ----------
    ax
    graph_title

    Returns
    -------

    """
    if fontsize is None:
        fontsize = 7

    left = graph_title.left
    bottom = graph_title.bottom
    top = graph_title.top
    right = graph_title.right

    top_left = graph_title.top_left_label
    top_right = graph_title.top_right_label
    bottom_left = graph_title.bottom_left_label
    bottom_right = graph_title.bottom_right_label

    if top_left is None:
        top_left_text = None
    else:
        top_left_text = ax.text(
            left,
            top,
            top_left,
            verticalalignment="bottom",
            horizontalalignment='left',
            transform=ax.transAxes,
            fontsize=fontsize,
        )

    if top_right is None:
        top_right_text = None
    else:
        top_right_text = ax.text(
            right,
            top,
            top_right,
            verticalalignment="bottom",
            horizontalalignment='right',
            transform=ax.transAxes,
            fontsize=fontsize,
        )

    if bottom_left is None:
        bottom_left_text = None
    else:
        bottom_left_text = ax.text(
            left,
            bottom,
            bottom_left,
            verticalalignment='top',
            horizontalalignment='left',
            transform=ax.transAxes,
            fontsize=fontsize
        )

    if bottom_right is None:
        bottom_right_text = None
    else:
        bottom_right_text = ax.text(
            right,
            bottom,
            bottom_right,
            verticalalignment='top',
            horizontalalignment='right',
            transform=ax.transAxes,
            fontsize=fontsize
        )

    return [top_left_text, top_right_text, bottom_left_text, bottom_right_text]


def set_title(
        ax,
        graph_name: str,
        system_name: str,
        start_time: pd.Timestamp,
        forecast_time: pd.Timedelta,
        map_type="east_asia",
) -> List:
    """
    添加标题

    Parameters
    ----------
    ax
    graph_name
        图片名称，例如 `MSLP (hPa) line`
    system_name
        系统名称，例如 `CMA-GFS`
    start_time
        起报时次
    forecast_time
        预报时效
    map_type
        底图类型

    Returns
    -------

    """
    graph_title = GraphTitle()
    fill_graph_title(
        graph_title=graph_title,
        graph_name=graph_name,
        system_name=system_name,
        start_time=start_time,
        forecast_time=forecast_time,
    )

    fill_graph_title_pos(
        graph_title=graph_title,
        map_type=map_type
    )

    return set_map_box_title(
        ax,
        graph_title=graph_title
    )


def add_map_box_info_text(
        ax: matplotlib.axes.Axes, text: str,
        map_type: str = "east_asia",
        component_type: str = "main",
):
    if map_type == "east_asia":
        if component_type == "main":
            x = 0.998
            y = 0.0022
        elif component_type == "sub":
            x = 0.99
            y = 0.01
        else:
            raise ValueError(f"component_type is not supported: {component_type}.")
    elif map_type == "north_polar":
        x = 1.065
        y = -0.045
    elif map_type == "europe_asia":
        x = 1.03
        y = -0.045
    else:
        raise ValueError(f"map_type is not supported: {map_type}.")

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


# color bar

@dataclass
class GraphColorbar:
    colormap: Optional[mcolors.ListedColormap] = None
    levels: Optional[List] = None
    box: Optional[List] = None
    label: Optional[str] = None
    label_loc: Optional[str] = None


def fill_colorbar_pos(graph_colorbar: GraphColorbar, map_type: str):
    if map_type == "east_asia":
        colorbar_box = [1.05, 0.02, 0.02, 1]
    elif map_type == "north_polar":
        colorbar_box = [1.08, 0.02, 0.02, 1]
    else:
        raise ValueError(f"map_type is not supported: {map_type}")
    graph_colorbar.box = colorbar_box
    return graph_colorbar


def add_map_box_colorbar(
        graph_colorbar: GraphColorbar,
        ax: Optional[matplotlib.axes.Axes] = None,
        fig: Optional[matplotlib.figure.Figure] = None,
) -> matplotlib.colorbar.Colorbar:
    colorbar_box = graph_colorbar.box
    levels = graph_colorbar.levels
    colormap = graph_colorbar.colormap

    if ax is not None:
        cax = ax.inset_axes(colorbar_box)
    elif fig is not None:
        cax = fig.add_axes(colorbar_box)
    else:
        raise ValueError(f"either ax or fig should be provided.")

    norm = mcolors.BoundaryNorm(levels, colormap.N, extend="both")
    cbar = cax.get_figure().colorbar(
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
    # ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(levels, ha='center')
    cbar.ax.yaxis.set_tick_params(pad=7)

    if graph_colorbar.label is not None:
        if graph_colorbar.label_loc is not None:
            label_loc = graph_colorbar.label_loc
        else:
            label_loc = None
        cbar.set_label(
            label=graph_colorbar.label,
            loc=label_loc,
        )

    return cbar


def add_colorbar(
        ax: matplotlib.axes.Axes,
        colormap: mcolors.ListedColormap,
        levels: List,
        map_type: str = "east_asia",
) -> matplotlib.colorbar.Colorbar:
    if map_type == "east_asia":
        colorbar_box = [1.05, 0.02, 0.02, 1]
    elif map_type == "north_polar":
        colorbar_box = [1.08, 0.02, 0.02, 1]
    else:
        raise ValueError(f"map_type is not supported: {map_type}")

    graph_colorbar = GraphColorbar(
        colormap=colormap,
        levels=levels,
        box=colorbar_box,
    )

    cbar = add_map_box_colorbar(graph_colorbar=graph_colorbar, ax=ax)
    return cbar


# area


def set_map_box_area(
        ax: matplotlib.axes.Axes,
        area: List[float],
        projection: ccrs.Projection,
        aspect: Optional[float] = None):
    east_lon, west_lon, south_lat, north_lat = area
    ax.set_extent(
        area,
        crs=projection
    )
    if aspect is None:
        return ax
    ax.set_aspect((abs(west_lon - east_lon) / aspect) / (abs(north_lat - south_lat) / 1.0), adjustable="box")
    return ax


def set_map_box_axis(
        ax,
        xticks, yticks,
        projection: ccrs.Projection
):
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


def draw_map_box_gridlines(
        ax, projection,
        xlocator=None, ylocator=None,
        linewidth=0.5,
        color="grey",
        alpha: float = 0.5,
        linetyle: str = "--",
):
    gl = ax.gridlines(
        crs=projection,
        draw_labels=False,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        linestyle=linetyle,
    )
    if ylocator is not None:
        gl.ylocator = mticker.FixedLocator(ylocator)
    if xlocator is not None:
        gl.xlocator = mticker.FixedLocator(xlocator)
    return gl


def clear_xarray_plot_components(ax):
    """
    清除 Xarray 自动绘图生成的图片组件，包括：

    * 标题
    * X轴标签
    * Y轴标签

    Parameters
    ----------
    ax

    Returns
    -------

    """
    ax.set_title("")
    ax.set_xlabel("")
    ax.set_ylabel("")
    return ax
