from typing import TypedDict
from typing import Literal


class regionTransferEvent(TypedDict):

    type: Literal["regionTransfer"]
    countries: list[str]
    regions: list[str]
    amount: float | int