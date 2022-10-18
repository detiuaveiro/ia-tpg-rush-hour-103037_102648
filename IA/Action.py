

from dataclasses import dataclass
from typing import List

@dataclass
class Action:
    piece: str
    direction: List[int]