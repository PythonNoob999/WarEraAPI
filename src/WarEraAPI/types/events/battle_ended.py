from typing import TypedDict
from typing import Literal


class battleEndedEvent(TypedDict):

    type: Literal["battleEnded"]
    battle: str
    defenderCountry: str
    attackerCountry: str
    defenderRegion: str
    attackerRegion: str
    wonBy: str