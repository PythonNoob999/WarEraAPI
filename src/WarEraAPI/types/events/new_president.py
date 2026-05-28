from typing import TypedDict
from typing import Literal


class newPresidentEvent(TypedDict):

    type: Literal["newPresident"]
    user: str 
    country: str
    election: str