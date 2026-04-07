from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import ITEM
from WarEraAPI.utils import edit_types


@dataclass
class RecommendedRegion:

    regionId: str
    bonus: float
    ethicDepositBonus: float
    strategicBonus: float
    ethicSpecializationBonus: float
    taxPercent: int

    # Optional Deposit
    depositEndAt: datetime | None = field(default=None)
    itemCode: ITEM | None = field(default=None)
    depositBonus: float | None = field(default=None)


    def __post_init__(self):

        edit_types(self)