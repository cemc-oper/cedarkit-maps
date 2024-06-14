from typing import Union, List, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd
from cartopy import crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import get_map_loader_class, MapType, MapLoader
from cedarkit.maps.util import (
    AxesRect,
    GraphTitle,
    AreaRange
)
from cedarkit.maps.painter.map_painter import (
    MapPainter, MapFeatureConfig, MapInfo
)
from cedarkit.maps.painter.axes_component_painter import (
    AxesComponentPainter, MapBoxOption, ColorBarOption,
)

from .map_template import MapTemplate

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class GlobalMapTemplate(MapTemplate):
    def __init__(
            self,
            area: Optional[AreaRange] = None,
    ):
        self.default_area = AreaRange(
            start_longitude=-180,
            end_longitude=180,
            start_latitude=-90,
            end_latitude=90,
        )
        if area is None:
            area = self.default_area

        self.central_longitude = 80

        projection = ccrs.PlateCarree()
        map_projection = ccrs.PlateCarree(central_longitude=self.central_longitude)

        super().__init__(
            projection=projection,
            area=area,
            map_projection=map_projection
        )

        self.width = 0.8
        self.height = 0.6

        self.main_map_loader: Optional[MapLoader] = None
        self.main_map_painter: Optional[MapPainter] = None

        self.axes_component_painter = AxesComponentPainter(
            map_box_option=MapBoxOption(
                bottom_left_point=(0, 0),
                top_right_point=(1, 1),
            ),
            color_bar_option=ColorBarOption(
                orientation="horizontal",
                bottom_left_point=(0.1, -0.12),
                top_right_point=(0.9, -0.1),
            )
        )

        self.main_xticks_interval = 30
        self.main_yticks_interval = 30

        self.map_loader_class = get_map_loader_class()

    def render_panel(self, panel: "Panel"):
        chart = panel.add_chart(domain=self)
        self.load_map()
        self.render_chart(chart=chart)

    def render_chart(self, chart: "Chart"):
        self.render_main_layer(chart=chart)

        # rect = draw_map_box(
        #     chart.layers[0].ax,
        #     bottom_left_point=self.map_box_bottom_left_point,
        #     top_right_point=self.map_box_top_right_point,
        # )

    def load_map(self):
        self.main_map_loader = self.map_loader_class(map_type=MapType.Portrait)

        self.main_map_painter = MapPainter(
            map_loader=self.main_map_loader,
            coastline_config=MapFeatureConfig(
                loader=dict(
                    scale="50m",
                    style=dict(
                        linewidth=0.5,
                        # zorder=50
                    )
                ),
                render=True,
            ),
            land_config=MapFeatureConfig(
                loader=dict(
                    scale="50m",
                    style=dict(
                        zorder=-1
                    )
                )
            ),
            map_info=MapInfo(
                x=0.998,
                y=0.0022,
                text="Scale 1:20000000 No:GS (2019) 1786",
            ),
        )

    def render_main_layer(self, chart: "Chart"):
        """
        绘制主地图

        Parameters
        ----------
        chart

        Returns
        -------

        """
        width = self.width
        height = self.height
        projection = self.projection
        map_painter = self.main_map_painter

        rect = AxesRect(
            left=(1 - width)/2,
            bottom=(1 - height)/2,
            width=width,
            height=height,
        )
        layer = chart.create_layer(
            rect=rect,
            projection=projection,
        )

        # 地图
        self.render_map(layer=layer, map_painter=map_painter)

        #   坐标轴
        # area = self.default_area
        area = self.area
        main_xticks = np.concatenate(
            (
                np.arange(
                    area.start_longitude, 0,
                    self.main_xticks_interval
                ),
                np.arange(
                    0, area.end_longitude + self.main_xticks_interval,
                    self.main_xticks_interval,
                )
            ),
            axis=None,
        )
        main_yticks = np.arange(
            area.start_latitude,
            area.end_latitude + self.main_yticks_interval,
            self.main_yticks_interval
        )

        layer.set_axis(xticks=main_xticks, yticks=main_yticks)
        self.set_axis_tick_params(layer=layer)

        #   网格线
        layer.gridlines(
            xlocator=main_xticks[1:-1],
            ylocator=main_yticks[1:-1],
        )

        #   设置区域范围和长宽比
        # ax.set_global()
        layer.set_area(area=area)

        return layer

    def set_axis_tick_params(self, layer: Layer):
        ax = layer.ax
        ax.tick_params(
            axis='both',
            which='major',
            bottom=True,
            left=True,
        )

        ax.tick_params(
            axis='both',
            which='minor',
            bottom=True,
            left=True,
        )

    def set_title(
            self,
            panel: "Panel",
            graph_name: str,
            system_name: str,
            start_time: pd.Timestamp,
            forecast_time: pd.Timedelta
    ):
        graph_title = GraphTitle()

        graph_title.top_right_label = system_name
        start_time_label = start_time.strftime("%Y%m%d%H")
        forecat_hour = int(forecast_time / pd.Timedelta(hours=1))
        graph_title.top_left_label = f"{start_time_label} UTC Forecast t+{forecat_hour:03d}"
        graph_title.main_title_label = graph_name

        self.axes_component_painter.add_title(
            layer=panel.charts[0].layers[0],
            graph_title=graph_title
        )

    def add_colorbar(self, panel: "Panel", style: Union[ContourStyle, List[ContourStyle]]):
        color_bars = self.axes_component_painter.add_colorbar(
            layer=panel.charts[0].layers[0],
            style=style,
        )
        return color_bars

    def render_map(self, layer: Layer, map_painter: MapPainter):
        map_painter.render_layer(layer=layer)


class GlobalAreaMapTemplate(GlobalMapTemplate):
    def __init__(
            self,
            area: Optional[AreaRange] = None
    ):
        super().__init__(area=area)
        self.main_map_type = MapType.Global

        self.main_xticks_interval = 10
        self.main_yticks_interval = 10

    def load_map(self):
        self.main_map_loader = self.map_loader_class(map_type=self.main_map_type)
        self.china_map = self.map_loader_class(map_type=MapType.Portrait)

        self.main_map_painter = MapPainter(
            map_loader=self.main_map_loader,
            coastline_config=MapFeatureConfig(
                loader=dict(
                    scale="50m",
                    style=dict(
                        linewidth=0.5,
                        # zorder=50
                    )
                ),
                render=True,
            ),
            global_borders_config=MapFeatureConfig(
                render=True,
            ),
            map_info=MapInfo(
                x=0.998,
                y=0.0022,
                text="Scale 1:20000000 No:GS (2019) 1786",
            ),
        )
