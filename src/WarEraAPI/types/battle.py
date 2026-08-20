from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import WAR_TYPE
from WarEraAPI.types.constants import WAR_ROLE
from WarEraAPI.types.constants import BattleParticipant
from typing import Literal


@dataclass
class Battle:

    _id: str
    type: WAR_TYPE
    rounds: list[str]
    roundsHistory: list[WAR_ROLE]
    isActive: bool
    roundsToWin: int
    createdAt: datetime
    updatedAt: datetime
    currentRound: str
    defender: BattleParticipant
    attacker: BattleParticipant

    # unknown attr type
    stats: dict

    # optional
    war: str | None = field(default=None)
    isBigBattle: bool | None = field(default=None)
    tournament: str | None = field(default=None)
    tournamentRoundNumber: int | None = field(default=None)
    endedAt: datetime | None = field(default=None)
    wonBy: WAR_ROLE | None = field(default=None)
    badgesProcessed: bool | None = field(default=None)
    isResistance: bool | None = field(default=None)