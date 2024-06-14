from typing import Union, List, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd
from cartopy import crs as ccrs
import matplotlib.path as mpath

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import get_map_loader_class, MapType, MapLoader
from cedarkit.maps.util import (
    AxesRect,
    AreaRange,
    GraphTitle,
    fill_graph_title,
)
from cedarkit.maps.painter.map_painter import MapPainter, MapFeatureConfig, MapInfo
from cedarkit.maps.painter.axes_component_painter import (
    AxesComponentPainter, MapBoxOption, ColorBarOption,
)

from .map_template import MapTemplate

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class NorthPolarMapTemplate(MapTemplate):
    def __init__(
            self,
            area: Optional[AreaRange] = None,
    ):
        self.central_longitude = 110

        self.default_area = AreaRange(
            start_longitude=-180,
            end_longitude=180,
            start_latitude=0,
            end_latitude=90
        )
        if area is None:
            area = self.default_area  # [start_longitude, end_longitude, start_latitude, end_latitude]

        projection = ccrs.PlateCarree()
        map_projection = ccrs.NorthPolarStereo(central_longitude=self.central_longitude)
        super().__init__(
            area=area,
            projection=projection,
            map_projection=map_projection,
        )

        self.width = 0.75
        self.height = 0.8

        self.main_map_loader: Optional[MapLoader] = None
        self.main_map_painter: Optional[MapPainter] = None

        self.axes_component_painter = AxesComponentPainter(
            map_box_option=MapBoxOption(
                bottom_left_point=(-0.05, -0.05),
                top_right_point=(1.07, 1.03),
            ),
            color_bar_option=ColorBarOption(
                orientation="vertical",
                bottom_left_point=(1.09, -0.02),
                top_right_point=(1.11, 1.02),
            )
        )

        self.main_xticks_interval = 10
        self.main_yticks_interval = 5

        self.map_class = get_map_loader_class()

    def render_panel(self, panel: "Panel"):
        chart = panel.add_chart(domain=self)
        self.load_map()
        self.render_chart(chart=chart)

    def render_chart(self, chart: "Chart"):
        self.render_main_layer(chart=chart)

        self.axes_component_painter.draw_map_box(
            layer=chart.layers[0]
        )

    def load_map(self):
        self.main_map_loader = self.map_class(map_type=MapType.Portrait)

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
                x=1.065,
                y=-0.045,
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
        rect = AxesRect(
            left=(1 - width) / 2,
            bottom=(1 - height) / 2,
            width=width,
            height=height,
        )

        area = self.area
        projection = self.projection
        map_projection = self.map_projection
        map_painter = self.main_map_painter

        layer = chart.create_layer(
            rect=rect,
            projection=projection,
            map_projection=map_projection,
        )

        #   坐标轴
        self.set_axis(layer=layer)

        # 设置图形边界形状
        self.set_boundary(layer=layer)

        #   网格线
        ylocator = np.arange(0, 90, 15)
        xlocator = np.arange(-180, 180, 30)
        layer.gridlines(
            xlocator=xlocator,
            ylocator=ylocator,
            color="k"
        )

        layer.set_area(
            area=area,
        )

        # 地图信息标注
        #   x, y, text
        self.add_map_info(layer=layer, map_painter=map_painter)

        #   地图
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

    def set_boundary(self, layer: Layer):
        ax = layer.ax
        theta = np.linspace(0, 2 * np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)

    def set_axis(self, layer: Layer):
        ax = layer.ax
        ticks = np.arange(0, 180 + 30, 30)
        etick = ['0'] + [
            r'%dE' % tick for tick in ticks if (tick != 0) & (tick != 180)
        ] + ['180']
        wtick = [r'%dW' % tick for tick in ticks if (tick != 0) & (tick != 180)]
        labels = etick + wtick[::-1]
        xticks = np.arange(0, 360, 30)
        yticks = np.full_like(xticks, -4)  # Latitude where the labels will be drawn
        for xtick, ytick, label in zip(xticks, yticks, labels):
            if label == "60W":
                ax.text(
                    xtick,
                    -0.5,
                    label,
                    fontsize=8,
                    horizontalalignment='center',
                    verticalalignment='bottom',
                    transform=ccrs.Geodetic()
                )
            else:
                ax.text(
                    xtick,
                    ytick,
                    label,
                    fontsize=8,
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ccrs.Geodetic()
                )

    def render_map(self, layer: Layer, map_painter: MapPainter):
        map_painter.render_layer(layer=layer)

    def add_map_info(self, layer: Layer, map_painter: MapPainter):
        map_painter.add_map_info(layer=layer)
