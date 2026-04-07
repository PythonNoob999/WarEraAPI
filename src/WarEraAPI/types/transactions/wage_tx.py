from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from WarEraAPI.utils import edit_types


@dataclass
class WageTransaction:

    _id: str
    money: int
    quantity: int
    sellerId: str
    buyerId: str
    transactionType: Literal["wage"]
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):

        edit_types(self)