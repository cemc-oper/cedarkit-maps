from dataclasses import dataclass
from typing import Union, Optional, List, Dict, Callable, Any

import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker


PARAMETER_MAP = {
    "2t": "t2m",
}


PLOT_STYLE = dict(
    t2m=dict(
        colormap=dict(
            category="ncl",
            name="temp_19lev"
        ),
        contour=dict(
            levels=np.append(np.arange(-30, 40, 4), 40)
        )
    )
)


@dataclass
class Style:
    ...


@dataclass
class ColorbarStyle(Style):
    loc: Optional[str] = None
    label: Optional[str] = None
    label_levels: Optional[Union[List, np.ndarray]] = None


@dataclass
class ContourLabelStyle(Style):
    fontsize: Optional[Union[str, float]] = None
    inline: bool = True
    inline_spacing: float = 5
    fmt: Optional[Union[mticker.Formatter, str, Callable]] = None
    colors: Optional[Any] = None
    manual: bool = False
    zorder: Optional[float] = None


@dataclass
class ContourStyle(Style):
    colors: Optional[Union[str, List, mcolors.ListedColormap]] = None
    levels: Optional[Union[List, np.ndarray]] = None
    linewidths: Optional[Union[List, np.ndarray, float]] = None
    linestyles: Optional[Union[List, str]] = None
    fill: bool = False
    label: bool = False
    label_style: Optional[ContourLabelStyle] = None
    colorbar_style: Optional[ColorbarStyle] = None


@dataclass
class BarbStyle(Style):
    length: float = 4
    linewidth: float = 0.5
    pivot: str = "middle"
    barbcolor: str = "red"
    flagcolor: Optional[str] = "red"
    barb_increments: Optional[Dict] = None
    colorbar_style: Optional[ContourLabelStyle] = None

    def __post_init__(self):
        if self.barb_increments is None:
            self.barb_increments = dict(half=2, full=4, flag=20)
