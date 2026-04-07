from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from WarEraAPI.utils import edit_types


@dataclass
class ArticleTipTransaction:

    _id: str
    money: int
    sellerId: str
    buyerId: str
    transactionType: Literal["articleTip"]
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):

        edit_types(self)