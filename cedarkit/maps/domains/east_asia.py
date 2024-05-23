from typing import Union, List, Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass

import numpy as np
import pandas as pd
from cartopy import crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import get_map_loader_class, MapType, MapLoader
from cedarkit.maps.util import (
    draw_map_box,
    set_map_box_axis,
    draw_map_box_gridlines,
    set_map_box_area,
    GraphTitle,
    fill_graph_title,
    set_map_box_title,
    add_map_info_text,
    GraphColorbar,
    add_map_box_colorbar,
)
from cedarkit.maps.painter.map_painter import MapPainter, MapFeatureConfig

from .map_template import MapTemplate

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


@dataclass
class RectSetting:
    left: float
    bottom: float
    width: float
    height: float


class EastAsiaMapTemplate(MapTemplate):
    """
    东亚/中国底图布局，带南海子图
    """
    def __init__(
            self,
            area: List[float] = None,
            with_sub_area: bool = True,
    ):
        self.default_area = [70, 140, 15, 55]  # [start_longitude, end_longitude, start_latitude, end_latitude]
        if area is None:
            area = self.default_area  # [start_longitude, end_longitude, start_latitude, end_latitude]

        projection = ccrs.PlateCarree()
        super().__init__(
            projection=projection,
            area=area
        )

        self.with_sub_area = with_sub_area

        self.width = 0.75
        self.height = 0.6
        self.main_aspect = 1.25

        self.sub_area = [105, 123, 2, 23]
        self.sub_width = 0.1
        self.sub_height = 0.14
        self.sub_aspect = 0.1 / 0.14

        self.main_map_loader: Optional[MapLoader] = None
        self.main_map_painter: Optional[MapPainter] = None
        self.sub_map_loader: Optional[MapLoader] = None
        self.sub_map_painter: Optional[MapPainter] = None

        self.map_box_bottom_left_point = (-0.06, -0.05)
        self.map_box_top_right_point = (1.03, 1.03)

        self.main_xticks_interval = 10
        self.main_yticks_interval = 5

        self.sub_xlocator = [110, 120]
        self.sub_ylocator = [10, 20]

        self.main_map_info_x = 0.998
        self.main_map_info_y = 0.0022
        self.main_map_info_text = "Scale 1:20000000 No:GS (2019) 1786"

        self.sub_map_info_x = 0.99
        self.sub_map_info_y = 0.01
        self.sub_map_info_text = "Scale 1:40000000"

        self.map_loader_class = get_map_loader_class()

    def render_panel(self, panel: "Panel"):
        chart = panel.add_chart(domain=self)
        self.load_map()
        self.render_chart(chart=chart)

    def load_map(self):
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
        )

    def render_chart(self, chart: "Chart"):
        self.render_main_layer(chart=chart)
        if self.with_sub_area:
            self.render_sub_layer(chart=chart)

        rect = draw_map_box(
            chart.layers[0].ax,
            bottom_left_point=self.map_box_bottom_left_point,
            top_right_point=self.map_box_top_right_point,
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
        rect = RectSetting(
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
        map_info_x = self.main_map_info_x
        map_info_y = self.main_map_info_y
        map_info_text = self.main_map_info_text
        map_painter = self.main_map_painter

        # 创建 Layer
        #       width, height
        layer = self.create_layer(
            chart=chart,
            rect=rect,
            projection=projection,
        )
        ax = layer.ax

        # 设置区域范围和长宽比
        #       area
        set_map_box_area(
            ax,
            area=area,
            projection=projection,
            aspect=aspect
        )

        # 坐标轴
        #       area, main_xticks_interval, main_yticks_interval
        xticks = np.arange(
            area[0],
            area[1] + xticks_interval,
            xticks_interval
        )
        yticks = np.arange(
            area[2],
            area[3] + yticks_interval,
            yticks_interval
        )
        set_map_box_axis(
            ax,
            xticks=xticks,
            yticks=yticks,
            projection=projection
        )

        # 网格线
        #       同坐标轴
        draw_map_box_gridlines(
            ax,
            projection=projection,
            xlocator=xticks[1:-1],
            ylocator=yticks[1:-1],
        )

        # 地图信息标注
        #   x, y, text
        add_map_info_text(
            ax=ax,
            x=map_info_x,
            y=map_info_y,
            text=map_info_text,
        )

        #   地图
        self.plot_map(layer=layer, map_painter=map_painter)

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
        rect = RectSetting(
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
        map_info_x = self.sub_map_info_x
        map_info_y = self.sub_map_info_y
        map_info_text = self.sub_map_info_text
        map_painter = self.sub_map_painter

        # 创建 Layer
        layer = self.create_layer(
            chart=chart,
            rect=rect,
            projection=self.projection,
        )
        ax = layer.ax

        # 区域：南海子图
        set_map_box_area(
            ax,
            area=area,
            projection=projection,
            aspect=aspect
        )

        # 网格线
        draw_map_box_gridlines(
            ax,
            projection=projection,
            xlocator=xlocator,
            ylocator=ylocator,
            linewidth=0.2,
        )

        # 地图信息标注
        add_map_info_text(
            ax=ax,
            x=map_info_x,
            y=map_info_y,
            text=map_info_text,
        )

        # 地图
        self.plot_map(layer=layer, map_painter=map_painter)

        return layer

    def plot_map(self, layer: "Layer", map_painter: MapPainter):
        map_painter.render_layer(layer=layer)

    def set_title(
            self,
            panel: "Panel",
            graph_name: str,
            system_name: str,
            start_time: pd.Timestamp,
            forecast_time: pd.Timedelta
    ):
        left = self.map_box_bottom_left_point[0]
        bottom = self.map_box_bottom_left_point[1] - 0.005
        top = self.map_box_top_right_point[1]
        right = self.map_box_top_right_point[0]
        graph_title = GraphTitle(
            left=left,
            bottom=bottom,
            top=top,
            right=right,
        )

        fill_graph_title(
            graph_title=graph_title,
            graph_name=graph_name,
            system_name=system_name,
            start_time=start_time,
            forecast_time=forecast_time,
        )

        set_map_box_title(
            panel.charts[0].layers[0].ax,
            graph_title=graph_title,
        )

    def add_colorbar(self, panel: "Panel", style: Union[ContourStyle, List[ContourStyle]]):
        """
                                 |  | left_padding_to_map_box_right_bound
                                    ---
        --------------------------  | |
        |                        |  | |
        |                        |  | |
        |                        |  | |
        |                        |  | |   colorbar
        |                        |  | |
        |                        |  | |
        |                        |  | |
        --------------------------  | |  --
               map box              ---  -- bottom_padding_to_map_box_bottom_bound


        """
        if isinstance(style, ContourStyle):
            style = [style]
        count = len(style)

        left_padding_to_map_box_right_bound = 0.02
        bottom_padding_to_map_box_bottom_bound = -0.02
        width = 0.02
        total_height = 1 + 2*abs(bottom_padding_to_map_box_bottom_bound)

        if count > 0:
            height_padding = 0.02
        else:
            height_padding = 0

        height = total_height / count

        color_bars = []

        for index, current_style in enumerate(style):
            colorbar_box = [
                self.map_box_top_right_point[0] + left_padding_to_map_box_right_bound,  # 1.03 + 0.02 = 1.05
                bottom_padding_to_map_box_bottom_bound + index * height,
                width, height - height_padding
            ]

            graph_colorbar = GraphColorbar(
                colormap=current_style.colors,
                levels=current_style.levels,
                box=colorbar_box,
            )

            colorbar_style = current_style.colorbar_style
            if colorbar_style is not None:
                if colorbar_style.label is not None:
                    graph_colorbar.label = colorbar_style.label
                if colorbar_style.loc is not None:
                    graph_colorbar.label_loc = colorbar_style.loc
                if colorbar_style.label_levels is not None:
                    graph_colorbar.label_levels = colorbar_style.label_levels

            color_bar = add_map_box_colorbar(
                graph_colorbar=graph_colorbar,
                ax=panel.charts[0].layers[0].ax,
            )

            color_bars.append(color_bar)

        return color_bars

    def create_layer(self, chart: "Chart", rect: RectSetting, projection: ccrs.Projection) -> Layer:
        fig = chart.fig
        layout = (rect.left, rect.bottom, rect.width, rect.height)
        ax = fig.add_axes(
            layout,
            projection=projection,
        )
        layer = Layer(projection=projection, chart=chart)
        layer.set_axes(ax)
        return layer


class CnAreaMapTemplate(EastAsiaMapTemplate):
    """
    中国区域底图布局，例如华北、华中、华南等
    """
    def __init__(
            self,
            area: List[float] = None,
            with_sub_area: bool = False,
    ):
        super().__init__(area=area, with_sub_area=with_sub_area)

        self.main_xticks_interval = 4
        self.main_yticks_interval = 2
        self.width = 0.8
        self.height = 0.6

