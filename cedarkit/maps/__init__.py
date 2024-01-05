from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cedarkit.maps")
except PackageNotFoundError:
    # package is not installed
    pass
