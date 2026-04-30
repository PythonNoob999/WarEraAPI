from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import MURoles
from WarEraAPI.types.constants import MULeveling
from WarEraAPI.types.constants import MUActiveUpgradeLevels
from WarEraAPI.types.constants import MURankings
from WarEraAPI.utils import edit_types


@dataclass
class MilitaryUnit:

    _id: str
    user: str
    region: str
    name: str
    members: list[str]
    mercenaryReputation: int
    createdAt: datetime
    updatedAt: datetime
    roles: MURoles
    leveling: MULeveling
    activeUpgradeLevels: MUActiveUpgradeLevels
    rankings: MURankings | None = field(default=None)
    avatarUrl: str | None = field(default=None)
    animatedAvatarUrl: str | None = field(default=None)
    investedMoneyByUsers: dict[str, float] | None = field(default=None)


    def __post_init__(self):

        edit_types(self)
