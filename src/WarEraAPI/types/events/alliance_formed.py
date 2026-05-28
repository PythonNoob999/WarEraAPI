from typing import TypedDict
from typing import Literal


class allianceFormedEvent(TypedDict):

    type: Literal["allianceFormed"]
    countries: str