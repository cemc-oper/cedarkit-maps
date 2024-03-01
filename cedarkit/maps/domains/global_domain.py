from typing import Union, List, TYPE_CHECKING

import cartopy.mpl.geoaxes
import numpy as np
import pandas as pd
from cartopy import crs as ccrs
import matplotlib.ticker as mticker

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import get_map_class, MapType
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
    from cedarkit.maps.chart import Chart, Panel


class GlobalMapDomain(MapDomain):
    def __init__(
            self,
            area: list[float] = None,
    ):
        self.default_area = [-180, 180, -90, 90]  # [start_longitude, end_longitude, start_latitude, end_latitude]
        if area is None:
            area = self.default_area  # [start_longitude, end_longitude, start_latitude, end_latitude]

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
        self.main_aspect = 1.25

        self.cn_features = None
        self.nine_features = None

        self.map_box_bottom_left_point = (0, 0)
        self.map_box_top_right_point = (1, 1)

        self.main_xticks_interval = 30
        self.main_yticks_interval = 30

        self.map_class = get_map_class()

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
        self.main_map = self.map_class(map_type=MapType.Portrait)
        self.sub_map = self.map_class(map_type=MapType.SouthChinaSea)

    def render_main_layer(self, chart: "Chart"):
        """
        绘制主地图

        Parameters
        ----------
        chart

        Returns
        -------

        """
        fig = chart.fig
        width = self.width
        height = self.height
        layout = [(1 - width) / 2, (1 - height) / 2, width, height]
        ax = fig.add_axes(
            layout,
            projection=self.map_projection,
        )
        layer = Layer(projection=self.projection, chart=chart)
        layer.set_axes(ax)

        features = []
        # coastline
        fs = self.main_map.coastline(scale="50m", style=dict(
            linewidth=0.5,
            # zorder=50
        ))
        features.extend(fs)

        fs = self.main_map.land(scale="50m", style=dict(
            zorder=-1
        ))
        features.extend(fs)

        # lakes
        # fs = self.main_map.lakes(scale="50m", style=dict(
        #     linewidth=0.25,
        #     facecolor='none',
        #     edgecolor="black",
        #     alpha=0.5
        # ))
        # features.extend(fs)

        # # china coastline
        # fs = self.main_map.china_coastline()
        # features.extend(fs)
        #
        # # china borders
        # fs = self.main_map.china_borders()
        # features.extend(fs)
        #
        # # china provinces
        # fs = self.main_map.china_provinces()
        # features.extend(fs)
        #
        # # china rivers
        # fs = self.main_map.china_rivers()
        # features.extend(fs)
        #
        # # south china sea
        # fs = self.main_map.china_nine_lines()
        # features.extend(fs)

        for f in features:
            ax.add_feature(
                f,
                # zorder=100
            )

        #   坐标轴
        # area = self.default_area
        area = self.area
        main_xticks = np.concatenate(
            (
                np.arange(
                    area[0], 0,
                    self.main_xticks_interval
                ),
                np.arange(
                    0, area[1] + self.main_xticks_interval,
                    self.main_xticks_interval,
                )
            ),
            axis=None,
        )
        main_yticks = np.arange(
            area[2],
            area[3] + self.main_yticks_interval,
            self.main_yticks_interval
        )
        set_map_box_axis(
            ax,
            xticks=main_xticks,
            yticks=main_yticks,
            projection=self.projection
        )

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

        #   网格线
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            xlocator=main_xticks[1:-1],
            ylocator=main_yticks[1:-1],
        )

        #   设置区域范围和长宽比
        ax.set_global()
        # set_map_box_area(
        #     ax,
        #     area=self.area,
        #     projection=self.projection,
        # )

        # x = 0.998
        # y = 0.0022
        # text = "Scale 1:20000000 No:GS (2019) 1786"
        # self.add_map_info(ax=ax, x=x, y=y, text=text)
        return layer

    @staticmethod
    def add_map_info(
            ax: cartopy.mpl.geoaxes.GeoAxes,
            x: float, y: float,
            text: str,
    ):
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

        graph_title.top_right_label = system_name
        start_time_label = start_time.strftime("%Y%m%d%H")
        forecat_hour = int(forecast_time / pd.Timedelta(hours=1))
        graph_title.top_left_label = f"{start_time_label} UTC Forecast t+{forecat_hour:03d}"
        graph_title.main_title_label = graph_name
        graph_title.main_pos = (0.5, 1.05)

        ax = panel.charts[0].layers[0].ax
        set_map_box_title(
            ax,
            graph_title=graph_title,
        )

    def add_colorbar(self, panel: "Panel", style: Union[ContourStyle, List[ContourStyle]]):
        """
                                 |  | left_padding_to_map_box_right_bound

        --------------------------
        |                        |
        |                        |
        |                        |
        |                        |  map box
        |                        |
        |                        |
        |                        |
        --------------------------  -- top_padding_to_map_box_bottom_bound
           ---------------------    --
           |                   |
           ---------------------
        | | left_padding_to_map_box_left_bound


        """
        if isinstance(style, ContourStyle):
            style = [style]
        count = len(style)

        left_padding_to_map_box_left_bound = 0.1
        top_padding_to_map_box_bottom_bound = -0.1
        height = 0.02
        total_width = 1 - 2*abs(top_padding_to_map_box_bottom_bound)

        if count > 0:
            width_padding = 0.02
        else:
            width_padding = 0

        width = total_width / count

        color_bars = []

        for index, current_style in enumerate(style):
            colorbar_box = [
                self.map_box_bottom_left_point[0] + left_padding_to_map_box_left_bound + index * width,  # 1.03 + 0.02 = 1.05
                self.map_box_bottom_left_point[1] + top_padding_to_map_box_bottom_bound,
                width - width_padding, height
            ]

            graph_colorbar = GraphColorbar(
                colormap=current_style.colors,
                levels=current_style.levels,
                box=colorbar_box,
                orientation="horizontal",
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
