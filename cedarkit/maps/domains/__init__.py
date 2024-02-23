import inspect
from typing import Union

from .map_domain import MapDomain
from .xy_domin import XYDomain
from .east_asia import EastAsiaMapDomain, CnAreaMapDomain


def parse_domain(domain: Union[str, type[MapDomain], MapDomain, type[XYDomain], XYDomain]) -> MapDomain:
    if inspect.isclass(domain):
        d = domain()
    elif isinstance(domain, MapDomain):
        d = domain
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
