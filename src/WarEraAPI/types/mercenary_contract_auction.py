from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import WAR_ROLE
from WarEraAPI.types.constants import MercenaryContractAuctionBid
from WarEraAPI.utils import edit_types


@dataclass
class MercenaryContractAuction:

    _id: str
    country: str
    createdBy: str
    battle: str
    forCountry: str
    forCountrySide: WAR_ROLE
    minimumDamage: int
    budget: float
    initialPerK: float
    duration: int
    professionalsOnly: bool
    expiresAt: datetime
    currentPerK: float
    currentPayout: float
    bids: list[MercenaryContractAuctionBid]
    status: str
    createdAt: datetime
    updatedAt: datetime

    # optional
    round: str | None = field(default=None)
    roundNumber: int | None = field(default=None)
    currentWinner: str | None = field(default=None)
    currentWinnerUser: str | None = field(default=None)


    def __post_init__(self):

        edit_types(self)