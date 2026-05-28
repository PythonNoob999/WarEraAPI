from typing import TypedDict
from typing import Literal

from WarEraAPI.types.constants import ITEM


class depositDiscoveredEvent(TypedDict):

    type: Literal["depositDiscoveredTransfer"]
    durationDays: int
    region: str
    itemCode: ITEM
    bonusPercent: int
    quantity: int | float