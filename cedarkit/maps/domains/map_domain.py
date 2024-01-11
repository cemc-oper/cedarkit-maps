from typing import List, TYPE_CHECKING

import cartopy.crs as ccrs

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class MapDomain:
    def __init__(self, projection: ccrs.Projection, area: List[float]):
        self._projection = projection
        self._area = area

    def render_panel(self, panel: "Panel"):
        raise NotImplementedError

    def render_chart(self, chart: "Chart"):
        raise NotImplementedError

    @property
    def area(self) -> List[float]:
        """
        Map area, [start_longitude, end_longitude, start_latitude, end_latitude].
        For example, ``[70, 140, 15, 55]``.
        """
        return self._area

    @property
    def projection(self) -> ccrs.Projection:
        return self._projection


