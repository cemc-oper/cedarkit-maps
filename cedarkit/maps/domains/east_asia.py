from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from cartopy import crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import (
    get_china_map,
    get_china_nine_map,
    add_common_map_feature
)
from cedarkit.maps.util import (
    draw_map_box,
    set_map_box_axis,
    draw_map_box_gridlines,
    set_map_box_area,
    GraphTitle,
    fill_graph_title,
    set_map_box_title,
    GraphColorbar,
    add_map_box_colorbar,
)

from .map_domain import MapDomain

if TYPE_CHECKING:
    from meda.chart import Chart


class EastAsiaMapDomain(MapDomain):
    def __init__(self):
        projection = ccrs.PlateCarree()
        domain = [70, 140, 15, 55]
        super().__init__(
            projection=projection,
            domain=domain
        )
        self.sub_domain = [105, 123, 2, 23]
        self.cn_features = None
        self.nine_features = None

        self.width = 0.75
        self.height = 0.6
        self.sub_width = 0.1
        self.sub_height = 0.14

    def set_chart(self, chart: "Chart"):
        super().set_chart(chart=chart)

    def render_chart(self):
        self.load_map()
        self.render_main_box()
        self.render_sub_box()

        rect = draw_map_box(self.chart.layers[0].ax)

    def load_map(self):
        self.cn_features = get_china_map()
        self.nine_features = get_china_nine_map()

    def render_main_box(self):
        fig = self.chart.fig
        width = self.width
        height = self.height
        layout = [(1 - width) / 2, (1 - height) / 2, width, height]
        ax = fig.add_axes(
            layout,
            # projection=ccrs.LambertConformal(
            #     central_longitude=105,
            #     central_latitude=90
            # ),
            projection=self.projection,
        )
        sub_chart = Layer(chart=self.chart, projection=self.projection)
        sub_chart.add_axes(ax)

        add_common_map_feature(
            ax,
            coastline=dict(
                scale="50m",
                style=dict(
                    linewidth=0.5,
                    # zorder=50
                )
            )
        )

        for f in self.cn_features:
            ax.add_feature(
                f,
                # zorder=100
            )

        for f in self.nine_features:
            ax.add_feature(
                f,
                # zorder=100
            )

        #   坐标轴
        set_map_box_axis(
            ax,
            xticks=np.arange(70, 141, 10),
            yticks=np.arange(15, 56, 5),
            projection=self.projection
        )

        #   网格线
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            ylocator=[20, 30, 40, 50]
        )

        #   设置区域范围和长宽比
        set_map_box_area(
            ax,
            area=self.domain,
            projection=self.projection,
            aspect=1.25  # 0.75/0.6
        )

        x = 0.998
        y = 0.0022
        text = "Scale 1:20000000 No:GS (2019) 1786"
        self.add_map_info(ax=ax, x=x, y=y, text=text)

    def render_sub_box(self):
        fig = self.chart.fig
        main_width = self.width
        main_height = self.height
        sub_width = self.sub_width
        sub_height = self.sub_height
        ax = fig.add_axes(
            [(1 - main_width) / 2, (1 - main_height) / 2, sub_width, sub_height],
            # projection=ccrs.LambertConformal(
            #     central_longitude=114,
            #     central_latitude=90,
            # ),
            projection=self.projection,
        )
        sub_chart = Layer(chart=self.chart, projection=self.projection)
        sub_chart.add_axes(ax)

        add_common_map_feature(
            ax,
            coastline=dict(
                scale="50m",
                style=dict(
                    linewidth=0.25,
                    # zorder=50
                ),
            )
        )

        for f in self.cn_features:
            ax.add_feature(
                f,
                linewidth=0.5,
                # zorder=100
            )
        for f in self.nine_features:
            ax.add_feature(
                f,
                linewidth=1,
                # zorder=100
            )

        #   区域：南海子图
        set_map_box_area(
            ax,
            area=self.sub_domain,
            projection=self.projection,
            aspect=0.1 / 0.14
        )

        #   网格线
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            xlocator=[110, 120],
            ylocator=[10, 20],
            linewidth=0.2,
        )

        x = 0.99
        y = 0.01
        text = "Scale 1:40000000"
        self.add_map_info(ax=ax, x=x, y=y, text=text)

    @staticmethod
    def add_map_info(ax, x: float, y: float, text: str):
        text_box = ax.text(
            x, y, text,
            verticalalignment='bottom',
            horizontalalignment='right',
            transform=ax.transAxes,
            fontsize=3,
            bbox=dict(
                boxstyle="round",
                edgecolor="black",
                facecolor="white",
                linewidth=0.5,
            )
        )
        return text_box

    def set_title(
            self,
            graph_name: str,
            system_name: str,
            start_time: pd.Timestamp,
            forecast_time: pd.Timedelta
    ):
        chart = self.chart

        left = -0.06
        bottom = -0.05 - 0.005
        top = 1.03
        right = 1.03
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
            chart.layers[0].ax,
            graph_title=graph_title,
        )

    def add_colorbar(self, style: ContourStyle):
        chart = self.chart

        colorbar_box = [1.05, 0.02, 0.02, 1]

        graph_colorbar = GraphColorbar(
            colormap=style.colors,
            levels=style.levels,
            box=colorbar_box,
        )

        color_bar = add_map_box_colorbar(
            chart.layers[0].ax,
            graph_colorbar=graph_colorbar,
        )
        return color_bar
