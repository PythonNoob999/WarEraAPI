from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from WarEraAPI.utils import edit_types


@dataclass
class BattleOrder:

    _id: str
    user: str
    battle: str
    side: Literal["attacker", "defender"]
    sideCountry: str
    text: str
    priority: Literal["low", "medium", "high"]
    isActive: bool
    createdAt: datetime
    updatedAt: datetime
    mu: str | None = field(default=None)
    country: str | None = field(default=None)


    def __post_init__(self):

        edit_types(self)