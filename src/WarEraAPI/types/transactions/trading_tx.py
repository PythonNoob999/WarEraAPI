from dataclasses import dataclass, field
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
    createdAt: datetime
    updatedAt: datetime
    buyerMuId: str | None = field(default=None)
    buyerPartyId: str | None = field(default=None)
    buyerCountryId: str | None = field(default=None)
    sellerMuId: str | None = field(default=None)
    sellerPartyId: str | None = field(default=None)
    sellerCountryId: str | None = field(default=None)
    processedByModAt: datetime | None = field(default=None)
    offerCreatedAt: datetime | None = field(default=None)


    def __post_init__(self):

        edit_types(self)