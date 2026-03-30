from typing import Literal
from typing import TypedDict
from typing import TypeAlias
from datetime import datetime


ITEM: TypeAlias = Literal[
    "limestone", "iron", "petroleum",
    "concrete", "steel", "oil",
    "grain", "livestock", "fish",
    "bread", "steak", "cookedFish",
    "lead",
    "ammo", "lightAmmo", "heavyAmmo",
    "case1", "case2", "scraps", "cocain", "coca"
]

AMMO: TypeAlias = Literal[
    "ammo", "lightAmmo", "heavyAmmo"
]

TIER: TypeAlias = Literal[
    "bronze", "sliver", "gold",
    "platinum", "diamond", "master"
]

RESOURCE: TypeAlias = Literal[
    "diamonds", "lithium", "rareEarths", "coal", "gold",
    "uranium"
]

EVENT_TYPES: TypeAlias = Literal[
    "battleOpened", "peaceMade", "countryMoneyTransfer", "regionTransfer",
    "depositDiscovered", "newPresident", "battleEnded",
    "allianceFormed", "warDeclared", "allianceBroken"
]

WAR_TYPE: TypeAlias = Literal[
    "war", "resistance", "tournament"
]

WAR_ROLE: TypeAlias = Literal["defender", "attacker"]


class ActiveUpgradeLevels(TypedDict):

    storage: int
    automatedEngine: int
    breakRoom: int


class Taxes(TypedDict):

    income: int
    market: int
    selfWork: int


class Unrest(TypedDict):

    barMax: int
    bar: int
    lastContributionAt: datetime


class Bonuses(TypedDict):

    productionPercent: int
    developmentPercent: int


class RankInfo(TypedDict):

    value: int
    rank: int
    tier: TIER


class Rankings(TypedDict):

    countryRegionDiff: RankInfo
    countryDamages: RankInfo
    weeklyCountryDamages: RankInfo
    weeklyCountryDamagesPerCitizen: RankInfo
    countryDevelopment: RankInfo
    countryActivePopulation: RankInfo
    countryWealth: RankInfo
    countryBounty: RankInfo
    countryProductionBonus: RankInfo


class StrategicResources(TypedDict):

    resources: dict[RESOURCE, list[str]]
    bonuses: Bonuses


class Deposit(TypedDict):

    type: ITEM
    startsAt: datetime
    endsAt: datetime
    bonusPercent: int


# War Stuff

class BattleParticipant(TypedDict):
    
    region: str
    country: str
    wonRoundsCount: int
    countryOrders: list[str]
    muOrders: list[str]
    damages: int
    hitCount: int
    tournamentTeam: str | None


class WeaponHitSkillsData(TypedDict):

    attack: int
    criticalChance: int


class WeaponHitData(TypedDict):

    _id: str
    code: str
    skills: WeaponHitSkillsData
    state: int
    maxState: int
    quantity: int
    lastAcquisitionAt: datetime


class EquipmentsHitSkillsData(TypedDict):

    criticalDamages: int | None
    armor: int | None
    dodge: int | None
    precision: int | None


class EquipmentsHitData(TypedDict):

    _id: str
    type: str
    code: str
    skills: EquipmentsHitSkillsData
    state: int
    maxState: int
    quantity: int
    lastAcquisitionAt: datetime


class BattleHit(TypedDict):

    _id: str
    user: str
    damages: int
    mu: str
    isCriticalHit: bool
    isMissed: bool
    hitAt: datetime
    weapon: WeaponHitData
    equipments: list[EquipmentsHitData]
    ammo: AMMO


class BattleSide(TypedDict):

    country: str
    damages: int
    points: int
    lastHits: list[BattleHit]
    hitCount: int


class LiveRoundStats(TypedDict):
    
    ticksCount: int
    actualTickPoints: int
    nextTickAt: datetime


# Minimal Stuff

class MinimalRound(TypedDict):

    roundId: str
    attackerDamages: int
    defenderDamages: int
    isActive: bool
    actualTickPoints: int
    attackerPoints: int
    nextTickAt: datetime
    defenderPoints: int 


class MinimalBattle(TypedDict):

    isActive: bool
    attackerCountryOrders: list[str]
    defenderCountryOrders: list[str]
    roundIds: list[str]
    roundHistory: list[WAR_ROLE]