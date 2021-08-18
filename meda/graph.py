import xarray as xr
import numpy as np
import matplotlib.axes
import matplotlib.contour
import matplotlib.quiver
import cartopy.crs as ccrs


def add_contourf(
        ax: matplotlib.axes.Axes,
        field: xr.DataArray,
        projection: ccrs.Projection,
        levels: np.ndarray,
        **kwargs
) -> matplotlib.contour.QuadContourSet:
    """
    添加填充图

    Parameters
    ----------
    ax
    field
        要素场
    projection
    levels
    **kwargs

    Returns
    -------

    """
    min_level = min(levels)
    max_level = max(levels)
    c = field.plot.contourf(
        ax=ax,
        transform=projection,
        vmin=min_level,
        vmax=max_level,
        levels=levels,
        add_colorbar=False,
        **kwargs
    )
    return c


def add_contour(
        ax: matplotlib.axes.Axes,
        field: xr.DataArray,
        projection: ccrs.Projection,
        levels: np.ndarray,
        linestyles="solid",
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
    **kwargs

    Returns
    -------

    """
    min_level = min(levels)
    max_level = min(levels)
    c = field.plot.contour(
        ax=ax,
        transform=projection,
        vmin=min_level,
        vmax=max_level,
        levels=levels,
        add_colorbar=False,
        linestyles=linestyles,
        **kwargs,
    )
    return c


def add_contour_label(
        ax: matplotlib.axes.Axes,
        contour: matplotlib.contour.QuadContourSet,
        fontsize=7,
        **kwargs,
):
    """
    添加等直线标签

    Parameters
    ----------
    ax
    contour
    fontsize
    **kwargs

    Returns
    -------

    """
    label = ax.clabel(
        contour,
        manual=False,
        inline=True,
        fmt="{:.0f}".format,
        fontsize=fontsize,
        **kwargs
    )
    return label


def add_barb(
        ax: matplotlib.axes.Axes,
        x_field: xr.DataArray,
        y_field: xr.DataArray,
        projection,
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
        barb_increments=dict(half=2, full=4, flag=20),
        length=4,
        sizes=dict(
            # width=0.35,
            # spacing=0.14,
        ),
        linewidth=0.5,
        pivot='middle',
        barbcolor="red",
        flagcolor="red",
    )

    return barb
