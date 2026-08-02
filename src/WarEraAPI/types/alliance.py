from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import AllianceMember
from WarEraAPI.types.constants import AllianceRankings
from WarEraAPI.utils import edit_types


@dataclass
class Alliance:

    _id: str
    name: str
    scheme: str
    mapAccent: str
    leader: str
    memberCountries: list[AllianceMember]
    currentDevelopment: float
    coreDevelopment: float
    averageDevelopment: float
    avatarUrl: str
    rankings: AllianceRankings
    createdAt: datetime | None = field(default=None)
    updatedAt: datetime | None = field(default=None)


    def __post_init__(self):

        edit_types(self)