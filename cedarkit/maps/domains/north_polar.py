from typing import Union, List, Optional, TYPE_CHECKING

import cartopy.mpl.geoaxes
import numpy as np
import pandas as pd
from cartopy import crs as ccrs
import matplotlib.path as mpath

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
    add_map_info_text,
    GraphColorbar,
    add_map_box_colorbar,
)

from .map_domain import MapDomain

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class NorthPolarMapDomain(MapDomain):
    def __init__(
            self,
            area: Optional[List[float]] = None,
    ):
        self.central_longitude = 110

        self.default_area = [-180, 180, 0, 90]  # [start_longitude, end_longitude, start_latitude, end_latitude]
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
        self.main_aspect = 1.25

        self.cn_features = None
        self.nine_features = None

        self.map_box_bottom_left_point = (-0.05, -0.05)
        self.map_box_top_right_point = (1.07, 1.03)

        self.main_xticks_interval = 10
        self.main_yticks_interval = 5

        self.map_class = get_map_class()

    def render_panel(self, panel: "Panel"):
        chart = panel.add_chart(domain=self)
        self.load_map()
        self.render_chart(chart=chart)

    def render_chart(self, chart: "Chart"):
        self.render_main_layer(chart=chart)

        rect = draw_map_box(
            chart.layers[0].ax,
            bottom_left_point=self.map_box_bottom_left_point,
            top_right_point=self.map_box_top_right_point,
        )

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

        #   网格线
        # main_ylocator = [20, 30, 40, 50]
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            ylocator=np.arange(0, 90, 15),
            xlocator=np.arange(-180, 180, 30),
            color="k"
        )

        #   设置区域范围和长宽比
        set_map_box_area(
            ax,
            area=self.area,
            projection=self.projection
        )

        # 设置图形边界形状
        theta = np.linspace(0, 2 * np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)

        x = 1.065
        y = -0.045
        text = "Scale 1:20000000 No:GS (2019) 1786"
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

            color_bar = add_map_box_colorbar(
                graph_colorbar=graph_colorbar,
                ax=panel.charts[0].layers[0].ax,
            )

            color_bars.append(color_bar)

        return color_bars
