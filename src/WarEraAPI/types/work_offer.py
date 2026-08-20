from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from WarEraAPI.types.constants import ITEM
from WarEraAPI.utils import edit_types


@dataclass
class WorkOffer:

    _id: str
    company: str
    user: str
    region: str
    quantity: int
    initialQuantity: int
    wage: float
    createdAt: datetime
    updatedAt: datetime
    wageAfterTax: float

    # optional
    text: str | None = field(default=None)
    minEnergy: int | None = field(default=None)
    minProduction: int | None = field(default=None)
    minLevel: int | None = field(default=None)
    citizenship: str | None = field(default=None)


    def __post_init__(self):

        edit_types(self)