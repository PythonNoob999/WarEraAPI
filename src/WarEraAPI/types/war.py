from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import WarSide
from WarEraAPI.utils import edit_types


@dataclass
class War:

    _id: str
    isActive: bool
    battles: list[str]
    priority: str
    attacker: WarSide
    defender: WarSide
    priorityEndAt: datetime | None = field(default=None )
    createdAt: datetime | None = field(default=None)
    updatedAt: datetime | None = field(default=None)


    def __post_init__(self):

        edit_types(self)