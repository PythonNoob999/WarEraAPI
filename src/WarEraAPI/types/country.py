from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import StrategicResources
from WarEraAPI.types.constants import Rankings
from WarEraAPI.types.constants import Taxes
from WarEraAPI.types.constants import Unrest
from WarEraAPI.types.constants import ITEM
from WarEraAPI.utils import edit_types


@dataclass
class Country:

    _id: str
    name: str
    code: str
    money: float
    orgs: list[str]
    allies: list[str]
    warsWith: list[str]
    scheme: str
    mapAccent: str
    taxes: Taxes
    unrest: Unrest
    rankings: Rankings
    updatedAt: datetime
    development: float
    currentBattleOrder: str | None = field(default=None)
    discordUrl: str | None = field(default=None)
    rulingParty: str | None = field(default=None)
    pinnedArticle: str | None = field(default=None)
    enemy: str | None = field(default=None)
    createdAt: datetime | None = field(default=None)
    specializedItem: ITEM | None = field(default=None)
    strategicResources: StrategicResources | None = field(default=None)
    bordersOpenUntil: datetime | None = field(default=None)


    def __post_init__(self):

        edit_types(self)