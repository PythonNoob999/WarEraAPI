from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from WarEraAPI.utils import edit_types


@dataclass
class DonationTransaction:

    _id: str
    money: int
    buyerId: str
    transactionType: Literal["donation"]
    createdAt: datetime
    updatedAt: datetime
    sellerCountryId: str | None = field(default=None)
    sellerMuId: str | None = field(default=None)
    sellerPartyId: str | None = field(default=None)


    def __post_init__(self):

        edit_types(self)