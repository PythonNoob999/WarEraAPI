from typing import List
from dataclasses import dataclass, field
from datetime import datetime

from WarEraAPI.types.constants import ITEM, ActiveUpgradeLevels
from WarEraAPI.types.worker import Worker
from WarEraAPI.utils import edit_types


@dataclass
class Company:

    _id: str
    user: str
    region: str
    itemCode: ITEM
    isFull: bool
    name: str
    concreteInvested: int
    activeUpgradeLevels: ActiveUpgradeLevels
    production: float
    workerCount: int
    createdAt: datetime
    updatedAt: datetime
    # optional
    movedUpAt: datetime | None = field(default=None)
    estimatedValue: float | None = field(default=None)
    workers: List[Worker] | None = field(default=None)
    workOffer: str | None  = field(default=None)
    disabledAt: datetime | None  = field(default=None)
    # yeah idk what are these params
    dates: dict | None  = field(default=None)
    upgradesV2: dict | None  = field(default=None)


    def __post_init__(self):

        edit_types(self)

        # this type assignment error is annoying
        if (
            isinstance(self.workers, list)
            and
            len(self.workers) > 0
            and
            isinstance(self.workers[0], dict)
        ):
            workers: list[dict] = self.workers
            self.workers = [
                Worker(**worker) for worker in workers
            ]