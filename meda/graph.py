import xarray as xr
import numpy as np
import matplotlib.axes
import matplotlib.contour
import cartopy.crs as ccrs


def add_contourf(
        ax: matplotlib.axes.Axes,
        field: xr.DataArray,
        projection: ccrs.Projection,
        levels: np.ndarray,
        **kwargs
) -> matplotlib.contour.QuadContourSet:
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
    label = ax.clabel(
        contour,
        manual=False,
        inline=True,
        fmt="{:.0f}".format,
        fontsize=fontsize,
        **kwargs
    )
    return label
