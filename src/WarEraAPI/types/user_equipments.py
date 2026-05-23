from dataclasses import dataclass, field

from WarEraAPI.types.constants import ItemMarket
from WarEraAPI.types.constants import AMMO
from WarEraAPI.utils import edit_types


@dataclass
class UserEquipments:

    weapon: ItemMarket | None = field(default=None)
    helmet: ItemMarket | None = field(default=None)
    chest: ItemMarket | None = field(default=None)
    pants: ItemMarket | None = field(default=None)
    boots: ItemMarket | None = field(default=None)
    gloves: ItemMarket | None = field(default=None)
    ammo: AMMO | None = field(default=None)


    def __post_init__(self):

        edit_types(self)