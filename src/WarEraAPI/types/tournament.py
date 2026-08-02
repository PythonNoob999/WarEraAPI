from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import RegisteredParties
from WarEraAPI.types.constants import TournamentRound
from WarEraAPI.utils import edit_types


@dataclass
class Tournament:

    _id: str
    name: str
    description: str
    isActive: bool
    teamSize: float
    teamCount: int
    roundsCount: int
    activeRound: int
    createdAt: datetime
    updatedAt: datetime
    startAt: datetime
    rounds: dict[str, TournamentRound]
    # NOTE: add literal types for those
    status: str
    type: str
    maxRarity: str
    skillKey: str
    autoQualify1stRound: list[str]
    registered: RegisteredParties
    winnerTournamentTeam: str | None = field(default=None)

    def __post_init__(self):

        edit_types(self)