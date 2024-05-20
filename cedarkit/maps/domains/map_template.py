from typing import List, Optional, TYPE_CHECKING

import cartopy.crs as ccrs

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel

from .xy_template import XYTemplate


class MapTemplate(XYTemplate):
    def __init__(
            self,
            projection: ccrs.Projection,
            area: List[float],
            map_projection: Optional[ccrs.Projection] = None,
    ):
        super().__init__()
        self._area = area
        self._projection = projection
        if map_projection is None:
            self._map_projection = self._projection
        else:
            self._map_projection = map_projection

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

    @property
    def map_projection(self) -> ccrs.Projection:
        return self._map_projection
