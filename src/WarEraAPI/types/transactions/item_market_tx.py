from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from WarEraAPI.types.constants import ItemMarket
from WarEraAPI.types.constants import ITEM_MARKET_CODE
from WarEraAPI.utils import edit_types


@dataclass
class ItemMarketTransaction:

    _id: str
    money: float
    quantity: int
    sellerId: str
    buyerId: str
    itemCode: ITEM_MARKET_CODE
    transactionType: Literal["itemMarket"]
    item: ItemMarket
    offerCreatedAt: datetime
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):
        
        edit_types(self)