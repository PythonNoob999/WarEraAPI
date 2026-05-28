from typing import TypedDict
from typing import Literal


class warDeclaredEvent(TypedDict):

    type: Literal["warDeclared"]
    war: str
    attackerCountry: str
    defenderCountry: str