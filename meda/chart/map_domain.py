from typing import List, Optional, Tuple, TYPE_CHECKING

import cartopy.crs as ccrs
import numpy as np
from matplotlib import pyplot as plt

from meda.map import (
    add_common_map_feature,
    get_china_map,
    get_china_nine_map,
)
from meda.util import (
    set_map_box_axis,
    draw_map_box_gridlines,
    set_map_box_area,
    draw_map_box
)

from .sub_chart import SubChart

if TYPE_CHECKING:
    from meda.chart.chart import Chart


class MapDomain:
    def __init__(self, projection: ccrs.Projection, domain: List[float]):
        self._projection = projection
        self._domain = domain
        self.chart = None

    def set_chart(self, chart: "Chart"):
        self.chart = chart

    def render_chart(self):
        raise NotImplementedError

    @property
    def domain(self):
        return self._domain

    @property
    def projection(self):
        return self._projection


def parse_domain(domain: str) -> MapDomain:
    if domain == "cemc.east_asia":
        map_domain = EastAsiaMapDomain()
    else:
        raise ValueError(f"invalid domain: {domain}")

    return map_domain


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

    def set_chart(self, chart: "Chart"):
        super().set_chart(chart=chart)

    def render_chart(self):
        self.load_map()
        self.render_main_box()
        self.render_sub_box()

        rect = draw_map_box(self.chart.subcharts[0].ax)

    def load_map(self):
        self.cn_features = get_china_map()
        self.nine_features = get_china_nine_map()

    def render_main_box(self):
        fig = self.chart.fig
        width = 0.75
        height = 0.6
        layout = [(1 - width) / 2, (1 - height) / 2, width, height]
        ax = fig.add_axes(
            layout,
            # projection=ccrs.LambertConformal(
            #     central_longitude=105,
            #     central_latitude=90
            # ),
            projection=self.projection,
        )
        sub_chart = SubChart(chart=self.chart, projection=self.projection)
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
        self.add_text(ax=ax, x=x, y=y, text=text)

    def render_sub_box(self):
        fig = self.chart.fig
        main_width = 0.75
        main_height = 0.6
        sub_width = 0.1
        sub_height = 0.14
        ax = fig.add_axes(
            [(1 - main_width) / 2, (1 - main_height) / 2, sub_width, sub_height],
            # projection=ccrs.LambertConformal(
            #     central_longitude=114,
            #     central_latitude=90,
            # ),
            projection=self.projection,
        )
        sub_chart = SubChart(chart=self.chart, projection=self.projection)
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
        self.add_text(ax=ax, x=x, y=y, text=text)

    @staticmethod
    def add_text(ax, x, y, text):
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
