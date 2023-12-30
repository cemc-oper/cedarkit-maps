from typing import Optional, TYPE_CHECKING

import matplotlib.axes

if TYPE_CHECKING:
    from meda.chart import Chart


class SubChart:
    def __init__(self, chart: "Chart"):
        self.ax: Optional[matplotlib.axes.Axes] = None
        self.chart = chart
        self.chart.add_subchart(self)

    def add_axes(self, ax: matplotlib.axes.Axes):
        self.ax = ax
