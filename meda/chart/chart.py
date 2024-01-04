from typing import List, Union, TYPE_CHECKING

from meda.style import Style, ContourStyle
from meda.domains import parse_domain, MapDomain

from .layer import Layer

if TYPE_CHECKING:
    from .panel import Panel


class Chart:
    def __init__(self, panel: "Panel", domain: Union[str, type[MapDomain], MapDomain]):
        self.panel = panel
        self.layers: List["Layer"] = []

        self.map_domain = parse_domain(domain)
        self.map_domain.set_chart(self)
        self.map_domain.render_chart()

    @property
    def fig(self):
        return self.panel.fig

    def add_layer(self, layer: "Layer"):
        self.layers.append(layer)

    def plot(self, data, style: "Style"):
        for layer in self.layers:
            if isinstance(style, ContourStyle):
                if style.fill:
                    layer.contourf(data=data, style=style)
                else:
                    layer.contour(data=data, style=style)
            else:
                raise NotImplementedError("style is not implemented")
