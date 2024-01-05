from typing import Union, Optional, List

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


class Style:
    def __init__(self):
        pass


class ContourStyle(Style):
    def __init__(
            self,
            colors: Optional[Union[str, List, mcolors.ListedColormap]] = None,
            levels: Optional[Union[List, np.ndarray]] = None,
            linewidths: Optional[Union[List, np.ndarray]] = None,
            fill: Optional[bool] = None,
    ):
        super().__init__()
        self.colors = colors
        self.levels = levels
        self.linewidths = linewidths
        if fill is None:
            self.fill = False
        else:
            self.fill = fill
