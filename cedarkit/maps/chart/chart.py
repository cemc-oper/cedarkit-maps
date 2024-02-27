from typing import List, Union, Optional, Any, TYPE_CHECKING

from cedarkit.maps.style import Style, ContourStyle, BarbStyle
from cedarkit.maps.domains import MapDomain, XYDomain

from .layer import Layer

if TYPE_CHECKING:
    from .panel import Panel


class Chart:
    """
    A sub graph in a Panel.
    A ``Chart`` may contain several ``Layer``s, such as a main layer for China and a sub layer for north china sea.

    Attributes
    ----------
    panel : Panel
    map_domain : MapDomain
    layers : List[Layer]
        layer list. Each layer has a map.
    """
    def __init__(self, panel: "Panel", domain: XYDomain):
        self.panel = panel
        self.map_domain = domain

        self.layers: List["Layer"] = []

        # NOTE: MapDomain creates axes.
        # self.map_domain.render_chart(chart=self)

    @property
    def fig(self):
        return self.panel.fig

    def add_layer(self, layer: "Layer"):
        self.layers.append(layer)

    def plot(self, data, style: "Style", layer: Optional[List[Any]] = None) -> List[Any]:
        """
        Plot data with style in layers.

        Parameters
        ----------
        data
            plot data. Different plot method may require different type of data.
            Such as contour needs one field, and barb needs a list with two fields.
        style
            plot style which is used to select plot method.
        layer
            which layer to be plotted on. If not set then all layers will be plotted on.

        Returns
        -------
        List[Any]
            plot results for each used layer.
        """
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
