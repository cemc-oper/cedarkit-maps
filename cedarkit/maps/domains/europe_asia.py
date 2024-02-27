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
    GraphColorbar,
    add_map_box_colorbar,
)

from .map_domain import MapDomain

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel


class EuropeAsiaMapDomain(MapDomain):
    def __init__(
            self,
            area: Optional[List[float]] = None,
            with_sub_area: bool = False,
    ):
        self.central_longitude = 95
        self.standard_parallels = (30, 60)

        self.default_area = [20, 170, 0, 70]  # [start_longitude, end_longitude, start_latitude, end_latitude]
        if area is None:
            area = self.default_area  # [start_longitude, end_longitude, start_latitude, end_latitude]

        projection = ccrs.PlateCarree()
        map_projection = ccrs.LambertConformal(
            central_longitude=self.central_longitude,
            standard_parallels=self.standard_parallels,
        )
        super().__init__(
            area=area,
            projection=projection,
            map_projection=map_projection,
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

        self.map_box_bottom_left_point = (-0.04, -0.04)
        self.map_box_top_right_point = (1.04, 1.04)

        self.main_xticks_interval = 10
        self.main_yticks_interval = 5

        self.map_class = get_map_class()

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


        #   网格线
        # main_ylocator = [20, 30, 40, 50]
        draw_map_box_gridlines(
            ax,
            projection=self.projection,
            ylocator=np.arange(0, 70, 10),
            xlocator=np.arange(20, 170, 10),
        )

        #   设置区域范围和长宽比
        set_map_box_area(
            ax,
            area=self.area,
            projection=self.projection
        )

        # 设置图形边界形状
        lon_range = (20, 170)
        lat_range = (0, 70)

        res = 1
        vertices = [
                       (lon, lat_range[0]) for lon in np.arange(lon_range[0], lon_range[1] + 1, res)
                   ] + [
                       (lon_range[1], lat) for lat in np.arange(lat_range[0], lat_range[1] + 1, res)
                   ] + [
                       (lon, lat_range[1]) for lon in np.arange(lon_range[1], lon_range[0] - 1, -res)
                   ] + [
                       (lon_range[0], lat) for lat in np.arange(lat_range[1], lat_range[0] - 1, -res)
                   ]

        path = mpath.Path(vertices)
        proj_to_data = ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData
        ax.set_boundary(proj_to_data.transform_path(path))

        x = 1.035
        y = -0.035
        text = "Scale 1:20000000 No:GS (2019) 1786"
        self.add_map_info(ax=ax, x=x, y=y, text=text)
        return layer

    def render_sub_layer(self, chart: "Chart"):
        """
        绘制南海子图

        Parameters
        ----------
        chart

        Returns
        -------

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

        x = 1.065
        y = -0.045
        text = "Scale 1:40000000"
        self.add_map_info(ax=ax, x=x, y=y, text=text)

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
