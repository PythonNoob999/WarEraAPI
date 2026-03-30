from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import BattleSide
from WarEraAPI.types.constants import LiveRoundStats
from WarEraAPI.utils import edit_types


@dataclass
class Round:

    _id: str
    battle: str
    number: int
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    attacker: BattleSide
    defender: BattleSide
    live: LiveRoundStats | None = field(default=None)


    def __post_init__(self):

        edit_types(self)