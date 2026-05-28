from typing import TypedDict
from typing import Literal


class allianceBrokenEvent(TypedDict):

    type: Literal["allianceBroken"]
    countries: str