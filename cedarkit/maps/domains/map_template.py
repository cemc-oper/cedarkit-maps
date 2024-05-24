from typing import List, Optional, Union, Tuple, TYPE_CHECKING

import cartopy.crs as ccrs

from ..util import AreaRange

from .xy_template import XYTemplate


if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class MapTemplate(XYTemplate):
    def __init__(
            self,
            projection: ccrs.Projection,
            area: Union[AreaRange, Tuple[float, float, float, float]],
            map_projection: Optional[ccrs.Projection] = None,
    ):
        super().__init__()
        if isinstance(area, AreaRange):
            self._area = area
        elif isinstance(area, tuple):
            self._area = AreaRange.from_tuple(area)
        else:
            raise ValueError("area must be AreaRange or tuple")
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
    def area(self) -> AreaRange:
        """
        Map area range.
        """
        return self._area

    @property
    def projection(self) -> ccrs.Projection:
        return self._projection

    @property
    def map_projection(self) -> ccrs.Projection:
        return self._map_projection
