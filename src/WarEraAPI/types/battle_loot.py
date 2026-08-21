from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import BattleItemLoot
from WarEraAPI.utils import edit_types


@dataclass
class BattleLoot:

    _id: str
    battle: str
    user: str
    case1Count: int
    case2Count: int
    hits: int
    poolLoot: list[BattleItemLoot]
    totalDmg: int
    totalMoneyFromBounty: float
    totalMoneyFromContract: float
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):

        edit_types(self)