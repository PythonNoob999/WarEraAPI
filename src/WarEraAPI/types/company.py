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
    estimatedValue: float
    movedUpAt: datetime
    # optional
    workers: None | List[Worker] = field(default=None)
    workOffer: None | str = field(default=None)
    disabledAt: None | datetime = field(default=None)
    # yeah idk what are these params
    dates: None | dict = field(default=None)
    upgradesV2: None | dict = field(default=None)


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