from dataclasses import dataclass, field
from datetime import datetime


from WarEraAPI.types.constants import PartyEthics
from WarEraAPI.utils import edit_types


@dataclass
class Party:

    _id: str
    name: str
    ethics: PartyEthics
    country: str
    region: str
    leader: str
    councilMembers: list[str]
    members: list[str]
    createdAt: datetime
    updatedAt: datetime
    description: str
    avatarUrl: str | None = field(default=None)
    treasurer: str | None = field(default=None)
    primaryWinner: str | None = field(default=None)


    def __post_init__(self):

        edit_types(self)