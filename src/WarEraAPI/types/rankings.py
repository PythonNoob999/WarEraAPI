from dataclasses import dataclass

from WarEraAPI.types.constants import RANKING_TYPE
from WarEraAPI.types.constants import TIER
from WarEraAPI.types.constants import Ranking
from WarEraAPI.utils import edit_types


@dataclass
class Rankings:

    _id: str
    type: RANKING_TYPE
    isGlobal: bool
    items: list[Ranking]
    tierValues: dict[TIER, int]


    def __post_init__(self):

        edit_types(self)