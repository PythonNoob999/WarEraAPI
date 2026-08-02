from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.utils import edit_types


@dataclass
class TournamentTeam:

    _id: str
    tournament: str
    number: int
    countries: list[str]
    mus: list[str]
    users: list[str]
    participants: list[str]
    estimatedUsers: int
    createdAt: datetime
    updatedAt: datetime

    # NOTE: add literal types for those
    colorScheme: str
    status: str

    # optional fields
    damageByEntity: dict[str, int] | None = field(default=None)
    totalDamage: int | None = field(default=None)


    def __post_init__(self):

        edit_types(self)