from typing import List, TYPE_CHECKING

import cartopy.crs as ccrs

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart


class MapDomain:
    def __init__(self, projection: ccrs.Projection, domain: List[float]):
        self._projection = projection
        self._domain = domain
        self.chart = None

    def set_chart(self, chart: "Chart"):
        self.chart = chart

    def render_chart(self):
        raise NotImplementedError

    @property
    def domain(self):
        return self._domain

    @property
    def projection(self):
        return self._projection


