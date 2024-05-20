from typing import Union, List, TYPE_CHECKING

import numpy as np
import pandas as pd
from cartopy import crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.chart import Layer
from cedarkit.maps.map import get_map_loader_class, MapType
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

from .map_domain import MapDomain

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class EastAsiaMapDomain(MapDomain):
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

        self.cn_features = None
        self.nine_features = None
        self.main_map = None
        self.sub_map = None

        self.map_box_bottom_left_point = (-0.06, -0.05)
        self.map_box_top_right_point = (1.03, 1.03)

        self.main_xticks_interval = 10
        self.main_yticks_interval = 5

        self.map_class = get_map_loader_class()

    def render_panel(self, panel: "Panel"):
        chart = panel.add_chart(domain=self)
        self.load_map()
        self.render_chart(chart=chart)

    def render_chart(self, chart: "Chart"):
        self.render_main_layer(chart=chart)
        if self.with_sub_area:
            self.render_sub_layer(chart=chart)

        rect = draw_map_box(
            chart.layers[0].ax,
            bottom_left_point=self.map_box_bottom_left_point,
            top_right_point=self.map_box_top_right_point,
        )

    def load_map(self):
        self.main_map = self.map_class(map_type=MapType.Portrait)
        self.sub_map = self.map_class(map_type=MapType.SouthChinaSea)

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
        fig = chart.fig
        width = self.width
        height = self.height
        layout = [(1 - width) / 2, (1 - height) / 2, width, height]
        ax = fig.add_axes(
            layout,
            projection=self.projection,
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

        # lakes
        fs = self.main_map.lakes(scale="50m", style=dict(
            linewidth=0.25,
            facecolor='none',
            edgecolor="black",
            alpha=0.5
        ))
        features.extend(fs)

        # china coastline
        fs = self.main_map.china_coastline()
        features.extend(fs)

        # china borders
        fs = self.main_map.china_borders()
        features.extend(fs)

        # china provinces
        fs = self.main_map.china_provinces()
        features.extend(fs)

        # china rivers
        fs = self.main_map.china_rivers()
        features.extend(fs)

        # south china sea
        fs = self.main_map.china_nine_lines()
        features.extend(fs)

        for f in features:
            ax.add_feature(
                f,
                # zorder=100
            )

        #   坐标轴
        # area = self.default_area
        area = self.area
        main_xticks = np.arange(
            area[0],
            area[1] + self.main_xticks_interval,
            self.main_xticks_interval
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

        #   网格线
        # main_ylocator = [20, 30, 40, 50]
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            xlocator=main_xticks[1:-1],
            ylocator=main_yticks[1:-1],
        )

        #   设置区域范围和长宽比
        set_map_box_area(
            ax,
            area=self.area,
            projection=self.projection,
            aspect=self.main_aspect  # 0.75/0.6
        )

        #   地图信息标注
        x = 0.998
        y = 0.0022
        text = "Scale 1:20000000 No:GS (2019) 1786"
        add_map_info_text(ax=ax, x=x, y=y, text=text)

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

        features = []
        # coastline
        fs = self.sub_map.coastline(scale="50m", style=dict(
            linewidth=0.25,
            # zorder=50
        ))
        features.extend(fs)

        # lakes

        # china coastline
        fs = self.sub_map.china_coastline()
        features.extend(fs)

        # china borders
        fs = self.sub_map.china_borders()
        features.extend(fs)

        # china provinces
        fs = self.sub_map.china_provinces()
        features.extend(fs)

        # china rivers
        fs = self.sub_map.china_rivers()
        features.extend(fs)

        # south china sea
        fs = self.sub_map.china_nine_lines()
        features.extend(fs)

        for f in features:
            ax.add_feature(
                f,
                # zorder=100
            )

        # for f in self.cn_features:
        #     ax.add_feature(
        #         f,
        #         linewidth=0.5,
        #         # zorder=100
        #     )
        # for f in self.nine_features:
        #     ax.add_feature(
        #         f,
        #         linewidth=1,
        #         # zorder=100
        #     )

        #   区域：南海子图
        set_map_box_area(
            ax,
            area=self.sub_area,
            projection=self.projection,
            aspect=self.sub_aspect
        )

        #   网格线
        sub_xlocator = [110, 120]
        sub_ylocator = [10, 20]
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            xlocator=sub_xlocator,
            ylocator=sub_ylocator,
            linewidth=0.2,
        )

        #   地图信息标注
        x = 0.99
        y = 0.01
        text = "Scale 1:40000000"
        add_map_info_text(ax=ax, x=x, y=y, text=text)

        return layer

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


class CnAreaMapDomain(EastAsiaMapDomain):
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

