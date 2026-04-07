from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from WarEraAPI.types.constants import ItemMarket
from WarEraAPI.types.constants import ITEM_MARKET_CODE
from WarEraAPI.utils import edit_types


@dataclass
class BattleLootTransaction:

    _id: str
    itemCode: ITEM_MARKET_CODE
    quantity: int
    buyerId: str
    transactionType: Literal["battleLoot"]
    item: ItemMarket
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):

        edit_types(self)