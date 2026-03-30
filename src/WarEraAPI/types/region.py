from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import RESOURCE
from WarEraAPI.types.constants import Deposit
from WarEraAPI.utils import edit_types


@dataclass
class Region:

    _id: str
    code: str
    country: str
    initialCountry: str
    neighbors: list[str]
    isCapital: bool
    isLinkedToCapital: bool
    upgradesV2: dict
    name: str
    mainCity: str
    development: float
    baseDevelopment: float
    countryCode: str
    position: list[float]
    biome: str
    climate: str
    resistance: int
    resistanceMax: int
    # idk about these also
    stats: dict
    dates: dict
    # optional
    activeBattle: dict | None = field(default=None)
    hasCoast: bool | None = field(default=None)
    deposit: Deposit | None = field(default=None)
    activeUpgradeLevels: dict | None = field(default=None)
    lastResistanceContributionAt: datetime | None = field(default=None)
    lastRevoltEndedAt: datetime | None = field(default=None)
    lastBattleEndedAt: datetime | None = field(default=None)
    strategicResource: RESOURCE | None = field(default=None)


    def __post_init__(self):

        edit_types(self)