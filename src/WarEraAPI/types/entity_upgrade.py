from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from WarEraAPI.types.constants import UPGRADE_TYPE
from WarEraAPI.utils import edit_types


@dataclass
class EntityUpgrade:

    _id: str
    upgradeType: UPGRADE_TYPE
    level: int
    status: Literal["active", "disabled"]
    investedMoney: float
    investedConcrete: int
    investedSteel: int
    dependantUsersCount: int
    createdAt: datetime
    updatedAt: datetime
    statusChangedAt: datetime | None = field(default=None)
    willBeActiveAt: datetime | None = field(default=None)
    company: str | None = field(default=None)
    region: str | None = field(default=None)
    mu: str | None = field(default=None)


    def __post_init__(self):

        edit_types(self)