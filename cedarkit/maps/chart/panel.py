from dataclasses import dataclass
from typing import Optional, Tuple, Union, List, Any, Iterable

import matplotlib.pyplot as plt
import xarray as xr

from cedarkit.maps.style import Style
from cedarkit.maps.domains import MapDomain, XYDomain, parse_domain

from .chart import Chart


@dataclass
class Schema:
    figsize: Tuple[float, float] = (8, 8)
    dpi: float = 400


class Panel:
    """
    A plot ``Panel`` which contains several ``Chart``s.

    Attributes
    ----------
    map_domain : MapDomain or XYDomain
        A ``MapDomain`` instance which is used to draw map and other items within a plot.
    schema : Schema
        panel settings, used to create ``matplotlib.pyplot.Figure``
    charts : List[Chart]
        chart list. each chart is a map box.
    """
    def __init__(
            self,
            domain: Union[str, type[MapDomain], MapDomain, type[XYDomain], XYDomain],
            schema: Optional[Schema] = None
    ):
        if schema is None:
            self.schema = Schema()
        else:
            self.schema = schema

        self._fig: Optional[plt.figure] = None

        self.charts = []

        self.map_domain = parse_domain(domain)
        self.map_domain.render_panel(self)

    @property
    def fig(self) -> plt.Figure:
        if self._fig is None:
            self._fig = plt.figure(
                figsize=self.schema.figsize,
                frameon=False,
                dpi=self.schema.dpi,
            )
        return self._fig

    def show(self):
        plt.show()

    def add_chart(self, domain: MapDomain) -> Chart:
        """
        Add a ``Chart`` to the panel

        Parameters
        ----------
        domain
            ``MapDomain``, different chart may use different domains.
        Returns
        -------
        Chart
        """
        chart = Chart(self, domain=domain)
        self.charts.append(chart)
        return chart

    def plot(self, data: Union[xr.DataArray, Iterable], style: Style, layer: Optional[List[Any]] = None) -> List[Any]:
        """
        Plot data in charts.

        Parameters
        ----------
        data
            iterable data, each ``Chart`` use one data to plot.
        style
            plot style, ``Layer`` use style to determine which plot method to use.
        layer
            layer index list, data will only be plotted in selected layers, default is all layers in chart.
        Returns
        -------
        List
            graphs list for each chart.
        """
        graphs = []

        if isinstance(data, xr.DataArray):
            data = [data]

        for i, d in enumerate(data):
            graph = self.charts[i].plot(data=d, style=style, layer=layer)
            graphs.append(graph)

        return graphs
