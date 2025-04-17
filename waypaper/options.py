"""Module that contains lists of possible options used in the application"""

from screeninfo import get_monitors

MONITOR_OPTIONS: list[str | None] = [m.name for m in get_monitors()]


from enum import Enum

from waypaper.backends import *


class ArgsEnum(Enum):
    def __new__(cls, *args: object, **kwargs: object):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class BackendOptions(ArgsEnum):
    def __init__(self, backend: Backend):
        self.backend = backend

    NONE = NoBackend()
    SWAYBG = SwayBgBackend()
    SWWW = SwwwBackend()
    FEH = FehBackend()
    WALLUTILS = WallutilsBackend()
    HYPRPAPER = HyprpaperBackend()
    MPVPAPER = MpvPaperBackend()


class FillOptions(Enum):
    FILL = "fill"
    STRETCH = "stretch"
    FIT = "fit"
    CENTER = "center"
    TILE = "tile"


class SortOptions(Enum):
    NAME = "name"
    DATE = "date"


class SortDirection(Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class SwwwTransitionTypes(Enum):
    ANY = "any"
    NONE = "none"
    SIMPLE = "simple"
    FADE = "fade"
    WIPE = "wipe"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    WAVE = "wave"
    GROW = "grow"
    CENTER = "center"
    OUTER = "outer"
    RANDOM = "random"
