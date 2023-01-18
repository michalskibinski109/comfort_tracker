from enum import Enum
from pydantic import BaseModel


class Colors(Enum):
    PRIMARY = "#F2CC8F"
    SECONDARY = "#3D405B"
    THIRD = "#E07A5F"
    EXTRA = "#81B29A"
    EXTRA2 = "#F4F1DE"
    LIGHT_PRIMARY = "#E6CE8D"
    DEBUG = "#338393"
    WHITE = "#FFFFFF"


class Config(BaseModel):
    window_width: int = 900
    window_height: int = 600
    date: str = "2021-01-01"


CONFIG = Config()
