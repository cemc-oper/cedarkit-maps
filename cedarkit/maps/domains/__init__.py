import inspect
from typing import Union

from .xy_domin import XYDomain, TimeStepAndLevelXYDomain
from .map_domain import MapDomain
from .east_asia import EastAsiaMapDomain, CnAreaMapDomain
from .north_polar import NorthPolarMapDomain
from .europe_asia import EuropeAsiaMapDomain
from .global_domain import GlobalMapDomain


def parse_domain(domain: Union[str, type[XYDomain], XYDomain]) -> XYDomain:
    if inspect.isclass(domain):
        d = domain()
    elif isinstance(domain, XYDomain):
        d = domain
    elif isinstance(domain, str):
        if domain == "cemc.east_asia":
            d = EastAsiaMapDomain()
        elif domain == "cemc.cn_area":
            d = CnAreaMapDomain()
        else:
            raise ValueError(f"invalid domain: {domain}")
    else:
        raise TypeError(f"invalid domain type")

    return d
