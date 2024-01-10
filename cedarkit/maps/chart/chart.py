from typing import List, Union, Optional, Any, TYPE_CHECKING

from cedarkit.maps.style import Style, ContourStyle, BarbStyle
from cedarkit.maps.domains import MapDomain

from .layer import Layer

if TYPE_CHECKING:
    from .panel import Panel


class Chart:
    def __init__(self, panel: "Panel", domain: Union[str, type[MapDomain], MapDomain]):
        self.panel = panel
        self.layers: List["Layer"] = []

        self.map_domain = domain
        # NOTE: MapDomain creates axes.
        # self.map_domain.render_chart(chart=self)

    @property
    def fig(self):
        return self.panel.fig

    def add_layer(self, layer: "Layer"):
        self.layers.append(layer)

    def plot(self, data, style: "Style", layer: Optional[List[Any]] = None):
        results = []
        if layer is None:
            layers = self.layers
        else:
            layers = [self.layers[i] for i in layer]
        for layer in layers:
            if isinstance(style, ContourStyle):
                if style.fill:
                    result = layer.contourf(data=data, style=style)
                else:
                    result = layer.contour(data=data, style=style)
            elif isinstance(style, BarbStyle):
                result = layer.barb(x=data[0], y=data[1], style=style)
            else:
                raise NotImplementedError(f"style is not implemented: {type(style)}")
            results.append(result)
        return results
