from typing import TypedDict
from typing import Literal


class battleOpenedEvent(TypedDict):

    type: Literal["battleOpened"]
    battle: str
    defenderCountry: str
    attackerCountry: str
    defenderRegion: str
    attackerRegion: str
    isResistance: bool