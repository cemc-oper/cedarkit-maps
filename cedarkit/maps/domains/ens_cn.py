from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import cartopy.mpl.geoaxes
from cartopy import crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import (
    get_china_map,
    get_china_nine_map,
    add_common_map_feature
)
from cedarkit.maps.util import (
    draw_map_box_gridlines,
    set_map_box_area,
    GraphTitle,
    fill_graph_title,
    set_map_box_title,
    GraphColorbar,
    add_map_box_colorbar,
    clear_axes,
)

from .map_domain import MapDomain

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class EnsCNMapDomain(MapDomain):
    def __init__(self, enable_max: bool = False):
        projection = ccrs.PlateCarree()
        domain = [73, 135, 16, 56]
        super().__init__(
            projection=projection,
            area=domain
        )

        self.member_count = 15
        self.enable_max = enable_max

        # plots with 15 members (mem01 to mem14, with control as mem00):
        #
        #   CTL  MAX  MEAN
        #    1    2    3    4    5
        #    6    7    8    9   10
        #   11   12   13   14
        #
        self.ncols = 5
        self.nrows = 1 + int(np.ceil((self.member_count - 1) / self.ncols))

        self.sub_domain = [105, 123, 2, 23]
        self.cn_features = None
        self.nine_features = None

    def render_panel(self, panel: "Panel"):
        self.load_map()
        fig = panel.fig

        # add box for figure, to be deleted
        ax = fig.add_axes((0, 0, 1, 1))
        clear_axes(ax)
        rect = ax.patch
        rect.set_linewidth(2)
        rect.set_edgecolor('blue')

        panel.main_box_ax = fig.add_axes((0.05, 0.1, 0.85, 0.8))
        clear_axes(panel.main_box_ax)
        # rect = self.main_box_ax.patch
        # rect.set_linewidth(1)
        # rect.set_edgecolor('red')

        gs = fig.add_gridspec(
            nrows=self.nrows, ncols=self.ncols,
            left=0.05, right=0.9, top=0.9, bottom=0.1,
            wspace=0, hspace=0,
        )
        panel.gs = gs

        chart_count = self.member_count
        if self.enable_max:
            chart_count += 1
        for number in range(0, chart_count):
            panel.add_chart(domain=self)

        current_chart_index = 0
        ax = fig.add_subplot(
            gs[0, 0],
            projection=self.projection
        )
        layer = Layer(chart=panel.charts[current_chart_index], projection=self.projection)
        layer.set_axes(ax)

        self.plot_map(ax, name="CTL")

        for number in range(1, self.member_count):
            current_chart_index += 1
            row_index = int((number - 1) / 5) + 1
            col_index = (number - 1) % 5
            ax = fig.add_subplot(
                gs[row_index, col_index],
                projection=self.projection
            )

            layer = Layer(chart=panel.charts[current_chart_index], projection=self.projection)
            layer.set_axes(ax)

            self.plot_map(ax, name=f"mem{number:02d}")

        if self.enable_max:
            current_chart_index += 1
            ax = fig.add_subplot(
                gs[0, 1],
                projection=self.projection
            )
            layer = Layer(chart=panel.charts[15], projection=self.projection)
            layer.set_axes(ax)
            self.plot_map(ax, name="MAX")

    def render_chart(self, chart: "Chart"):
        self.render_main_box(chart)
        # self.render_sub_layer()

        # rect = draw_map_box_by_map_type(self.chart.layers[0].ax)

    def load_map(self):
        self.cn_features = get_china_map()
        self.nine_features = get_china_nine_map()

    def render_main_box(self, chart: "Chart"):
        pass

    def plot_map(self, ax: cartopy.mpl.geoaxes.GeoAxes, name: str):
        ax.text(
            0,
            1,
            name,
            verticalalignment="top",
            horizontalalignment='left',
            transform=ax.transAxes,
            fontsize=7,
            color="r",
        )

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

        # #   坐标轴
        # set_map_box_axis(
        #     ax,
        #     xticks=np.arange(70, 141, 10),
        #     yticks=np.arange(15, 56, 5),
        #     projection=self.projection
        # )

        # #   网格线
        # draw_map_box_gridlines(
        #     ax,
        #     projection=self.projection,
        #     ylocator=[20, 30, 40, 50]
        # )

        #   设置区域范围和长宽比
        set_map_box_area(
            ax,
            area=self.area,
            projection=self.projection,
            # aspect=1.25  # 0.75/0.6
        )

        # x = 0.998
        # y = 0.0022
        # text = "Scale 1:20000000 No:GS (2019) 1786"
        # self.add_map_info(ax=ax, x=x, y=y, text=text)

        # 去掉垂直空白
        ax.set_aspect('auto')

    def render_sub_box(self, chart: "Chart"):
        fig = chart.fig
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
        layer = Layer(chart=chart, projection=self.projection)
        layer.set_axes(ax)

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
            panel: "Panel",
            graph_name: str,
            system_name: str,
            start_time: pd.Timestamp,
            forecast_time: pd.Timedelta
    ):
        # bottom titles
        left = 0
        bottom = -0.05
        top = 1.05
        right = 1
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

        graph_title.top_left_label = None
        graph_title.top_right_label = None

        set_map_box_title(
            panel.main_box_ax,
            graph_title=graph_title,
            fontsize=10,
        )

        # Title
        row = 0
        col = 1
        if self.enable_max:
            col += 1
        fig = panel.fig
        ax = fig.add_subplot(
            panel.gs[row, col:],
        )
        clear_axes(ax)

        title_nrows = 2
        height = 1.0 / (title_nrows + 2)

        ax.text(
            0.5, 1 - height*(1 + 0.5),
            f"{system_name}",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=15,
            color="red",
        )
        ax.text(
            0.5, 1 - height*(2 + 0.5),
            f"{graph_name}",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=15,
            color="black",
        )

    def add_colorbar(self, panel: "Panel", style: ContourStyle):
        ax = panel.main_box_ax

        #  (left, bottom, width, height)
        colorbar_box = [1.05, 0.02, 0.02, 1]

        graph_colorbar = GraphColorbar(
            colormap=style.colors,
            levels=style.levels,
            box=colorbar_box,
        )

        color_bar = add_map_box_colorbar(
            graph_colorbar=graph_colorbar,
            ax=ax,
        )
        return color_bar
