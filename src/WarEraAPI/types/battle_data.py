from dataclasses import dataclass, field

from WarEraAPI.types.constants import MinimalBattle
from WarEraAPI.types.constants import MinimalRound


@dataclass
class BattleData:

    battle: MinimalBattle
    round: MinimalRound