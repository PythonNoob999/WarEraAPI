from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from WarEraAPI.utils import edit_types
from WarEraAPI.types.constants import UserLeveling
from WarEraAPI.types.constants import UserDates
from WarEraAPI.types.constants import UserMissions
from WarEraAPI.types.constants import UserSkills
from WarEraAPI.types.constants import UserStats
from WarEraAPI.types.constants import UserEquipment
from WarEraAPI.types.constants import UserRankings
from WarEraAPI.types.constants import UserBuffs
from WarEraAPI.types.constants import UserMute


@dataclass
class User:

    _id: str
    dates: UserDates
    leveling: UserLeveling
    username: str
    country: str
    isActive: bool
    skills: UserSkills
    militaryRank: int
    createdAt: datetime
    orgs: list | None = field(default=None)
    stats: UserStats | None = field(default=None)
    rankings: UserRankings | None = field(default=None)
    mu: str | None = field(default=None)
    usernameLower: str | None = field(default=None)
    canOnboard: bool | None = field(default=None)
    availableColorSchemes: list[str] | None = field(default=None)
    shouldUpdateProfile: bool | None = field(default=None)
    emailVerified: bool | None = field(default=None)
    updatedAt: datetime | None = field(default=None)
    finishedTours: dict[str, bool] | None = field(default=None)
    equipment: UserEquipment | None = field(default=None)
    avatarUrl: str | None = field(default=None)
    missions: UserMissions | None = field(default=None)
    party: str | None = field(default=None)
    muMaxLevelRewarded: int | None = field(default=None)
    company: str | None = field(default=None)
    infos: dict[str, Any] | None = field(default=None)
    warning: dict[str, Any] | None = field(default=None)
    discord: dict[str, Any] | None = field(default=None)
    equippedSkinKeys: dict[str, str] | None = field(default=None)
    animatedAvatarUrl: str | None = field(default=None)
    buffs: UserBuffs | None = field(default=None)
    mute: UserMute | None = field(default=None)
    isLocked: bool | None = field(default=None)


    def __post_init__(self):

        edit_types(self)