from enum import Enum
from dataclasses import dataclass
from typing import Dict


class MenuOption(Enum):
    CAPTION = 1
    PRINT = 2
    HANDLER = 3


@dataclass
class Option:
    type: MenuOption
    data: Dict
