import inspect
from typing import Union

from .map_domain import MapDomain
from .east_asia import EastAsiaMapDomain


def parse_domain(domain: Union[str, type[MapDomain], MapDomain]) -> MapDomain:
    if inspect.isclass(domain):
        d = domain()
    elif isinstance(domain, MapDomain):
        d = domain
    elif isinstance(domain, str):
        if domain == "cemc.east_asia":
            d = EastAsiaMapDomain()
        else:
            raise ValueError(f"invalid domain: {domain}")
    else:
        raise TypeError(f"invalid domain type")

    return d
