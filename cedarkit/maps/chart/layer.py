from typing import Optional, TYPE_CHECKING

import xarray as xr
import matplotlib.axes
import matplotlib.contour

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.graph import (
    add_contourf,
    add_contour,
    add_contour_label,
)

if TYPE_CHECKING:
    from meda.chart import Chart


class Layer:
    def __init__(self, chart: "Chart", projection):
        self.ax: Optional[matplotlib.axes.Axes] = None
        self.chart = chart
        self.chart.add_layer(self)
        self.projection = projection

    def add_axes(self, ax: matplotlib.axes.Axes):
        self.ax = ax

    def contourf(self, data: xr.DataArray, style: ContourStyle, **kwargs) -> matplotlib.contour.QuadContourSet:
        contour = add_contourf(
            self.ax,
            field=data,
            projection=self.projection,
            levels=style.levels,
            cmap=style.colors,
            **kwargs
        )
        return contour

    def contour(self, data: xr.DataArray, style: ContourStyle, **kwargs) -> matplotlib.contour.QuadContourSet:
        contour = add_contour(
            self.ax,
            field=data,
            projection=self.projection,
            levels=style.levels,
            colors=style.colors,
            linewidths=style.linewidths,
            **kwargs
        )

        return contour

    def contour_label(self, contour, colors):
        label = add_contour_label(
            self.ax,
            contour=contour,
            colors=colors
        )
        return label