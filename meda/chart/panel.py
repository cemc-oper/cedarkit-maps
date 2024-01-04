from dataclasses import dataclass
from typing import Optional, Tuple, Union

import matplotlib.pyplot as plt

from meda.style import Style
from meda.domains import MapDomain

from .chart import Chart


@dataclass
class Schema:
    figsize: Tuple[float, float] = (6, 6)
    dpi: float = 400


class Panel:
    def __init__(self, domain: Union[str, type[MapDomain], MapDomain]):
        self.schema = Schema()

        self._fig: Optional[plt.figure] = None

        self.charts = []

        self.add_chart(domain=domain)

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

    def add_chart(self, domain: Union[str, type[MapDomain], MapDomain]):
        chart = Chart(self, domain=domain)
        self.charts.append(chart)

    def plot(self, data, style: Style):
        self.charts[0].plot(data=data, style=style)

