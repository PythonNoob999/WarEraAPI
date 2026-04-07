from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from WarEraAPI.types.constants import ITEM
from WarEraAPI.utils import edit_types


@dataclass
class TradingTransaction:

    _id: str
    money: float
    itemCode: ITEM
    quantity: int
    sellerId: str
    buyerId: str
    transactionType: Literal["trading"]
    offerCreatedAt: datetime
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):

        edit_types(self)