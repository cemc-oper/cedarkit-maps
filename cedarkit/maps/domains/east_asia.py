from typing import Union, List, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd
from cartopy import crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import get_map_loader_class, MapType, MapLoader
from cedarkit.maps.util import (
    AxesRect,
    AreaRange,
    GraphTitle,
    fill_graph_title,
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


class EastAsiaMapTemplate(MapTemplate):
    """
    东亚/中国底图布局，带南海子图
    """
    def __init__(
            self,
            area: Optional[AreaRange] = None,
            with_sub_area: bool = True,
    ):
        self.default_area = AreaRange(
            start_longitude=70,
            end_longitude=140,
            start_latitude=15,
            end_latitude=55,
        )
        if area is None:
            area = self.default_area

        projection = ccrs.PlateCarree()
        super().__init__(
            projection=projection,
            area=area
        )

        self.with_sub_area = with_sub_area

        self.width = 0.75
        self.height = 0.6
        self.main_aspect = 1.25

        self.sub_area = AreaRange(
            start_longitude=105,
            end_longitude=123,
            start_latitude=2,
            end_latitude=23,
        )
        self.sub_width = 0.1
        self.sub_height = 0.14
        self.sub_aspect = 0.1 / 0.14

        self.main_map_loader: Optional[MapLoader] = None
        self.main_map_painter: Optional[MapPainter] = None
        self.sub_map_loader: Optional[MapLoader] = None
        self.sub_map_painter: Optional[MapPainter] = None

        self.axes_component_painter = AxesComponentPainter(
            map_box_option=MapBoxOption(
                bottom_left_point=(-0.06, -0.05),
                top_right_point=(1.03, 1.03),
            ),
            color_bar_option=ColorBarOption(
                orientation="vertical",
                bottom_left_point=(1.05, -0.02),
                top_right_point=(1.07, 1.02),
            )
        )

        self.main_xticks_interval = 10
        self.main_yticks_interval = 5

        self.sub_xlocator = [110, 120]
        self.sub_ylocator = [10, 20]

        self.map_loader_class = get_map_loader_class()

    def total_area(self) -> AreaRange:
        main_area = self.area
        sub_area = self.sub_area

        total = AreaRange(
            start_longitude=min(main_area.start_longitude, sub_area.start_longitude),
            end_longitude=max(main_area.end_longitude, sub_area.end_longitude),
            start_latitude=min(main_area.start_latitude, sub_area.start_latitude),
            end_latitude=max(main_area.end_latitude, sub_area.end_latitude),
        )

        return total

    def render_panel(self, panel: "Panel"):
        chart = panel.add_chart(domain=self)
        self.load_map()
        self.render_chart(chart=chart)

    def load_map(self):
        """
        create map loader and map painter.
        """
        self.main_map_loader = self.map_loader_class(map_type=MapType.Portrait)
        self.sub_map_loader = self.map_loader_class(map_type=MapType.SouthChinaSea)

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
            lakes_config=MapFeatureConfig(
                loader=dict(
                    scale="50m",
                    style=dict(
                        linewidth=0.25,
                        facecolor='none',
                        edgecolor="black",
                        alpha=0.5
                    )
                ),
                render=True,
            ),
            china_coastline_config=MapFeatureConfig(render=True),
            china_borders_config=MapFeatureConfig(render=True),
            china_provinces_config=MapFeatureConfig(render=True),
            china_rivers_config=MapFeatureConfig(render=True),
            china_nine_lines_config=MapFeatureConfig(render=True),
            map_info=MapInfo(
                x=0.998,
                y=0.0022,
                text="Scale 1:20000000 No:GS (2019) 1786",
            ),
        )

        self.sub_map_painter = MapPainter(
            map_loader=self.sub_map_loader,
            coastline_config=MapFeatureConfig(
                loader=dict(
                    scale="50m",
                    style=dict(
                        linewidth=0.25,
                        # zorder=50
                    )
                ),
                render=True,
            ),
            china_coastline_config=MapFeatureConfig(render=True),
            china_borders_config=MapFeatureConfig(render=True),
            china_provinces_config=MapFeatureConfig(render=True),
            china_rivers_config=MapFeatureConfig(render=True),
            china_nine_lines_config=MapFeatureConfig(render=True),
            map_info=MapInfo(
                x=0.99,
                y=0.01,
                text="Scale 1:40000000",
            ),
        )

    def render_chart(self, chart: "Chart"):
        self.render_main_layer(chart=chart)
        if self.with_sub_area:
            self.render_sub_layer(chart=chart)

        self.axes_component_painter.draw_map_box(
            layer=chart.layers[0]
        )

    def render_main_layer(self, chart: "Chart") -> Layer:
        """
        绘制主地图

        Parameters
        ----------
        chart

        Returns
        -------
        Layer
        """
        width = self.width
        height = self.height
        rect = AxesRect(
            left=(1 - width)/2,
            bottom=(1 - height)/2,
            width=width,
            height=height,
        )

        area = self.area
        projection = self.projection
        aspect = self.main_aspect  # 0.75/0.6
        xticks_interval = self.main_xticks_interval
        yticks_interval = self.main_yticks_interval
        map_painter = self.main_map_painter

        # 创建 Layer
        #       width, height
        layer = chart.create_layer(
            rect=rect,
            projection=projection,
        )

        # 设置区域范围和长宽比
        #       area
        layer.set_area(area=area, aspect=aspect)

        # 坐标轴
        #       area, main_xticks_interval, main_yticks_interval
        # NOTE: 需要将边界点包含在内。
        # 当前方式存在问题，会将整形标签变为浮点类型
        xticks = np.arange(
            area.start_longitude,
            area.end_longitude + xticks_interval/10,
            xticks_interval
        )
        yticks = np.arange(
            area.start_latitude,
            area.end_latitude + yticks_interval/10,
            yticks_interval
        )
        layer.set_axis(xticks=xticks, yticks=yticks)

        # 网格线
        #       同坐标轴
        # 边界处是边框，不需要网格线，但需要坐标轴标注。边框会覆盖网格线，所以直接使用标签列表即可
        # xlocator = xticks[1:-1]
        # ylocator = yticks[1:-1]
        xlocator = xticks
        ylocator = yticks
        layer.gridlines(
            xlocator=xlocator,
            ylocator=ylocator,
        )

        # 地图信息标注
        #   x, y, text
        self.add_map_info(layer=layer, map_painter=map_painter)

        #   地图
        self.render_map(layer=layer, map_painter=map_painter)

        return layer

    def render_sub_layer(self, chart: "Chart") -> Layer:
        """
        绘制南海子图

        Parameters
        ----------
        chart

        Returns
        -------
        Layer
        """
        main_width = self.width
        main_height = self.height
        sub_width = self.sub_width
        sub_height = self.sub_height
        rect = AxesRect(
            left=(1 - main_width) / 2,
            bottom=(1 - main_height) / 2,
            width=sub_width,
            height=sub_height,
        )

        area = self.sub_area
        projection = self.projection
        aspect = self.sub_aspect
        xlocator = self.sub_xlocator
        ylocator = self.sub_ylocator
        map_painter = self.sub_map_painter

        # 创建 Layer
        layer = chart.create_layer(
            rect=rect,
            projection=projection,
        )
        ax = layer.ax

        # 区域：南海子图
        layer.set_area(area=area, aspect=aspect)

        # 网格线
        layer.gridlines(
            xlocator=xlocator,
            ylocator=ylocator,
            linewidth=0.2,
        )

        # 地图信息标注
        self.add_map_info(layer=layer, map_painter=map_painter)

        # 地图
        self.render_map(layer=layer, map_painter=map_painter)

        return layer

    def set_title(
            self,
            panel: "Panel",
            graph_name: str,
            system_name: str,
            start_time: pd.Timestamp,
            forecast_time: pd.Timedelta
    ):
        graph_title = GraphTitle()

        fill_graph_title(
            graph_title=graph_title,
            graph_name=graph_name,
            system_name=system_name,
            start_time=start_time,
            forecast_time=forecast_time,
        )

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

    def add_map_info(self, layer: Layer, map_painter: MapPainter):
        map_painter.add_map_info(layer=layer)


class CnAreaMapTemplate(EastAsiaMapTemplate):
    """
    中国区域底图布局，例如华北、华中、华南等
    """
    def __init__(
            self,
            area: Optional[AreaRange] = None,
            with_sub_area: bool = False,
    ):
        super().__init__(area=area, with_sub_area=with_sub_area)

        self.main_xticks_interval = 4
        self.main_yticks_interval = 2
        self.width = 0.8
        self.height = 0.6

