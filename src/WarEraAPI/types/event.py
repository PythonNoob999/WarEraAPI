from dataclasses import dataclass
from datetime import datetime

from WarEraAPI.utils import edit_types


@dataclass
class Event:

    _id: str
    countries: list[str]
    priority: int
    data: dict
    createdAt: datetime
    updatedAt: datetime


    def __post_init__(self):

        edit_types(self)