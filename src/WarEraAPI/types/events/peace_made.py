from typing import TypedDict
from typing import Literal


class peaceMadeEvent(TypedDict):

    type: Literal["peaceMade"]
    wars: list[str]
    countries: list[str]