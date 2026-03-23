from typing import List, Optional, Union, Tuple, TYPE_CHECKING

import pandas as pd
import cartopy.crs as ccrs

from cedarkit.maps.style import ContourStyle
from cedarkit.maps.util import AreaRange, GraphTitle, fill_graph_title
from cedarkit.maps.template import XYTemplate

if TYPE_CHECKING:
    from cedarkit.maps.chart import Chart, Panel, Layer
    from cedarkit.maps.painter.map_painter import MapPainter
    from cedarkit.maps.painter.axes_component_painter import AxesComponentPainter


class MapTemplate(XYTemplate):
    """
    地图模板基类，提供地图绑定的通用功能。
    
    Attributes
    ----------
    axes_component_painter : AxesComponentPainter
        坐标轴组件绑定器，用于绑定标题、色标等。子类必须初始化此属性。
    main_map_painter : MapPainter
        主地图绑定器。子类必须初始化此属性。
    """
    
    def __init__(
            self,
            projection: ccrs.Projection,
            area: Union[AreaRange, Tuple[float, float, float, float]],
            map_projection: Optional[ccrs.Projection] = None,
    ):
        super().__init__()
        if isinstance(area, AreaRange):
            self._area = area
        elif isinstance(area, tuple):
            self._area = AreaRange.from_tuple(area)
        else:
            raise ValueError("area must be AreaRange or tuple")
        self._projection = projection
        if map_projection is None:
            self._map_projection = self._projection
        else:
            self._map_projection = map_projection
        
        # 子类必须初始化这些属性
        self.axes_component_painter: Optional["AxesComponentPainter"] = None
        self.main_map_painter: Optional["MapPainter"] = None

    def render_panel(self, panel: "Panel"):
        raise NotImplementedError

    def render_chart(self, chart: "Chart"):
        raise NotImplementedError

    @property
    def area(self) -> AreaRange:
        """
        Map area range.
        """
        return self._area

    def total_area(self) -> AreaRange:
        """
        Total map area range including sub area.
        """
        return self._area

    @property
    def projection(self) -> ccrs.Projection:
        return self._projection

    @property
    def map_projection(self) -> ccrs.Projection:
        return self._map_projection

    def set_title(
            self,
            panel: "Panel",
            graph_name: str,
            system_name: str,
            start_time: pd.Timestamp,
            forecast_time: pd.Timedelta
    ):
        """
        设置图表标题。
        
        Parameters
        ----------
        panel : Panel
            面板对象
        graph_name : str
            图表名称
        system_name : str
            系统名称
        start_time : pd.Timestamp
            起报时间
        forecast_time : pd.Timedelta
            预报时效
        """
        graph_title = GraphTitle()
        fill_graph_title(
            graph_title=graph_title,
            graph_name=graph_name,
            system_name=system_name,
            start_time=start_time,
            forecast_time=forecast_time,
        )
        self._add_title_to_panel(panel=panel, graph_title=graph_title)

    def _add_title_to_panel(self, panel: "Panel", graph_title: GraphTitle):
        self.axes_component_painter.add_title(
            layer=panel.charts[0].layers[0],
            graph_title=graph_title
        )

    def add_colorbar(self, panel: "Panel", style: Union[ContourStyle, List[ContourStyle]]):
        """
        添加色标。
        
        Parameters
        ----------
        panel : Panel
            面板对象
        style : Union[ContourStyle, List[ContourStyle]]
            等值线样式，用于确定色标的颜色和级别
            
        Returns
        -------
        List
            色标对象列表
        """
        color_bars = self.axes_component_painter.add_colorbar(
            layer=panel.charts[0].layers[0],
            style=style,
        )
        return color_bars

    def render_map(self, layer: "Layer", map_painter: "MapPainter"):
        """
        渲染地图要素到图层。
        
        Parameters
        ----------
        layer : Layer
            图层对象
        map_painter : MapPainter
            地图绑定器
        """
        map_painter.render_layer(layer=layer)

    def add_map_info(self, layer: "Layer", map_painter: "MapPainter"):
        """
        添加地图信息标注（如审图号）。
        
        Parameters
        ----------
        layer : Layer
            图层对象
        map_painter : MapPainter
            地图绑定器
        """
        map_painter.add_map_info(layer=layer)
