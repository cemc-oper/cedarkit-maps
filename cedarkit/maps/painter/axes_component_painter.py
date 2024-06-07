from dataclasses import dataclass
from typing import Tuple, Union, List

from cedarkit.maps.chart import Layer
from cedarkit.maps.util import (
    draw_map_box,
    GraphTitle,
    set_map_box_title,
)
from cedarkit.maps.style import ContourStyle


@dataclass
class MapBoxOption:
    bottom_left_point: Tuple[float, float]
    top_right_point: Tuple[float, float]


@dataclass
class AxesComponentPainter:
    map_box_option: MapBoxOption

    def draw_map_box(self, layer: Layer):
        ax = layer.ax
        draw_map_box(
            ax,
            bottom_left_point=self.map_box_option.bottom_left_point,
            top_right_point=self.map_box_option.top_right_point,
        )

    def add_title(self, layer: Layer, graph_title: GraphTitle):
        graph_title.left = self.map_box_option.bottom_left_point[0]
        graph_title.bottom = self.map_box_option.bottom_left_point[1] - 0.005
        graph_title.top = self.map_box_option.top_right_point[1]
        graph_title.right = self.map_box_option.top_right_point[0]

        ax = layer.ax
        set_map_box_title(
            ax,
            graph_title=graph_title,
        )

    def add_colorbar(self, style: Union[ContourStyle, List[ContourStyle]]):
        pass
