from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from WarEraAPI.types.constants import ItemMarket
from WarEraAPI.utils import edit_types


@dataclass
class CraftItemTransaction:

    _id: str
    quantity: int
    sellerId: str
    buyerId: str
    itemCode: Literal["scraps"]
    transactionType: Literal["craftItem"]
    item: ItemMarket
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):
        
        edit_types(self)