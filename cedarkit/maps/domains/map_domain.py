from typing import List, TYPE_CHECKING

import cartopy.crs as ccrs

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class MapDomain:
    def __init__(self, projection: ccrs.Projection, domain: List[float]):
        self._projection = projection
        self._domain = domain

    def render_panel(self, panel: "Panel"):
        raise NotImplementedError

    def render_chart(self, chart: "Chart"):
        raise NotImplementedError

    @property
    def domain(self):
        return self._domain

    @property
    def projection(self):
        return self._projection


