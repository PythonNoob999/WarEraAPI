from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.utils import edit_types


@dataclass
class Worker:

    _id: str
    user: str
    wage: float
    joinedAt: datetime | None = field(default=None)
    company: str | None = field(default=None)
    employer: str | None = field(default=None)
    fidelity: int | None = field(default=None)
    lockedUntil: str | None = field(default=None)
    createdAt: datetime | None = field(default=None)
    updatedAt: datetime | None = field(default=None)
    lastFidelityIncreaseAt: datetime | None = field(default=None)


    def __post_init__(self):

        edit_types(self)