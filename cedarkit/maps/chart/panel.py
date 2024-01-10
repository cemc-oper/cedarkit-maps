from dataclasses import dataclass
from typing import Optional, Tuple, Union, List, Any, Iterable

import matplotlib.pyplot as plt
import xarray as xr

from cedarkit.maps.style import Style
from cedarkit.maps.domains import MapDomain, parse_domain

from .chart import Chart


@dataclass
class Schema:
    figsize: Tuple[float, float] = (8, 8)
    dpi: float = 400


class Panel:
    def __init__(self, domain: Union[str, type[MapDomain], MapDomain]):
        self.schema = Schema()

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

    def add_chart(self, domain: Union[str, type[MapDomain], MapDomain]) -> Chart:
        chart = Chart(self, domain=domain)
        self.charts.append(chart)
        return chart

    def plot(self, data: Union[xr.DataArray, Iterable], style: Style, layer: Optional[List[Any]] = None):
        """

        Parameters
        ----------
        data
        style
        layer
            layer index list, default is None
        Returns
        -------

        """
        if isinstance(data, xr.DataArray):
            data = [data]

        for i, d in enumerate(data):
            self.charts[i].plot(data=d, style=style, layer=layer)
