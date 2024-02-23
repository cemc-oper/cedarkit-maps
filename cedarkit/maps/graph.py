from typing import Dict, Optional, Tuple

import xarray as xr
import numpy as np
import matplotlib.axes
import matplotlib.contour
import matplotlib.quiver
import cartopy.crs as ccrs


def add_contourf(
        ax: matplotlib.axes.Axes,
        field: xr.DataArray,
        levels: np.ndarray,
        projection: Optional[ccrs.Projection] = None,
        y_invert: bool = False,
        **kwargs
) -> matplotlib.contour.QuadContourSet:
    """
    添加填充图

    Parameters
    ----------
    ax
    field
        data field
    levels
        contour level list.
    projection
        map projection
    y_invert
    **kwargs

    Returns
    -------
    matplotlib.contour.QuadContourSet
    """
    min_level = min(levels)
    max_level = max(levels)

    first_dim = field[field.dims[0]]
    max_dim_value = max(first_dim).values
    min_dim_value = min(first_dim).values
    if y_invert:
        ylim = (max_dim_value, min_dim_value)
    else:
        ylim = None

    c = field.plot.contourf(
        ax=ax,
        transform=projection,
        vmin=min_level,
        vmax=max_level,
        levels=levels,
        add_colorbar=False,
        add_labels=False,
        extend="both",
        ylim=ylim,
        **kwargs
    )
    return c


def add_contour(
        ax: matplotlib.axes.Axes,
        field: xr.DataArray,
        levels: np.ndarray,
        projection: Optional[ccrs.Projection] = None,
        linestyles: str = "solid",
        y_invert: bool = False,
        **kwargs
) -> matplotlib.contour.QuadContourSet:
    """
    添加等直线图

    Parameters
    ----------
    ax
    field
        要素场
    projection
    levels
    linestyles
    y_invert
    **kwargs

    Returns
    -------
    matplotlib.contour.QuadContourSet
    """
    min_level = min(levels)
    max_level = max(levels)

    first_dim = field[field.dims[0]]
    max_dim_value = max(first_dim).values
    min_dim_value = min(first_dim).values
    if y_invert:
        ylim = (max_dim_value, min_dim_value)
    else:
        ylim = None

    c = field.plot.contour(
        ax=ax,
        transform=projection,
        vmin=min_level,
        vmax=max_level,
        levels=levels,
        add_colorbar=False,
        linestyles=linestyles,
        add_labels=False,
        ylim=ylim,
        **kwargs,
    )
    return c


def add_contour_label(
        ax: matplotlib.axes.Axes,
        contour: matplotlib.contour.QuadContourSet,
        fontsize: float = 7,
        manual: bool = False,
        inline: bool = True,
        fmt="{:.0f}".format,
        **kwargs,
):
    """
    添加等直线标签

    Parameters
    ----------
    ax
    contour
    fontsize
    manual
    inline
    fmt
    **kwargs

    Returns
    -------

    """
    label = ax.clabel(
        contour,
        fontsize=fontsize,
        manual=manual,
        inline=inline,
        fmt=fmt,
        **kwargs
    )
    return label


def add_barb(
        ax: matplotlib.axes.Axes,
        x_field: xr.DataArray,
        y_field: xr.DataArray,
        projection: Optional[ccrs.Projection] = None,
        length: float = 4,
        linewidth: float = 0.5,
        pivot: str = 'middle',
        barbcolor: str = "red",
        flagcolor: str = "red",
        barb_increments: Optional[Dict] = None,
        **kwargs
) -> matplotlib.quiver.Barbs:
    """
    添加风羽图

    Parameters
    ----------
    ax
    x_field
        u分量，东西风
    y_field
        v分量，南北风
    projection
    length
    linewidth
    pivot
    barbcolor
    flagcolor
    barb_increments

    Returns
    -------
    matplotlib.quiver.Barbs
    """
    lons, lats = np.meshgrid(x_field.longitude, y_field.latitude)

    # 风向杆
    barb = ax.barbs(
        lons, lats,
        x_field.data, y_field.data,
        transform=projection,
        barb_increments=barb_increments,
        length=length,
        linewidth=linewidth,
        pivot=pivot,
        barbcolor=barbcolor,
        flagcolor=flagcolor,
        # sizes=dict(
        #     width=0.35,
        #     spacing=0.14,
        # ),
        **kwargs
    )

    return barb
