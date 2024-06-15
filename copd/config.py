from enum import Enum,IntEnum
from dataclasses import dataclass
from typing import Dict
TILE_SIZE = 16
X_TILES = 40
Y_TILES = 20
SCREEN_WIDTH = X_TILES * TILE_SIZE # 32 blocks wide
SCREEN_HEIGHT = Y_TILES * TILE_SIZE  # 18 blocks tall


OVERWORLD_MAP = [[0, 1, 2], [0, 1, 2]]

DEFAULT_MAP = [
    [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        28,
        29,
        30,
        31,
    ],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
]

GAME_CAPTION = "Crawl of PyDun"

class Layers(IntEnum):
    BG_Layer = 0
    Tile_Layer = 1
    Door_Layer = 2
    Player_Layer = 3

@dataclass
class Colors():
    NachoCheese = (255, 208, 108)
    DaytonaPeach = (253, 221, 200)
    DeadSalmon = (170, 148, 135)
    Snugglepuss = (158, 149, 188)
    SafetyGreen = (242, 253, 1)
    BreastCancerAwareness = (255, 109, 148)
    Cyantology = (122, 169, 199)
    MasterChief = (130, 149, 86)
    # Item Colors
    Common = (128, 128, 128)
    Uncommon = (0, 127, 14)
    Rare = (0, 127, 14)
    Epic = (156, 0, 255)
    Legendary = (156, 0, 255)
    # Primary Colors
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)

class MenuOption(Enum):
    CAPTION = 1
    PRINT = 2
    HANDLER = 3


@dataclass
class Option:
    type: MenuOption
    data: Dict