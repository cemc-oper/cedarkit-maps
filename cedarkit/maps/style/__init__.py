from dataclasses import dataclass
from typing import Union, Optional, List, Dict

import numpy as np
import matplotlib.colors as mcolors

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
    pass


@dataclass
class ContourStyle(Style):
    colors: Optional[Union[str, List, mcolors.ListedColormap]] = None
    levels: Optional[Union[List, np.ndarray]] = None
    linewidths: Optional[Union[List, np.ndarray]] = None
    fill: bool = False


@dataclass
class BarbStyle(Style):
    length: float = 4
    linewidth: float = 0.5
    pivot: str = "middle"
    barbcolor: str = "red"
    flagcolor: str = "red"
    barb_increments: Optional[Dict] = None

    def __post_init__(self):
        if self.barb_increments is None:
            self.barb_increments = dict(half=2, full=4, flag=20)
