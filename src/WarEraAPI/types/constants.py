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
    "case1", "case2", "scraps", "cocain", "coca",
    "wood", "paper"
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

RANKING_TYPE: TypeAlias = Literal[
    'weeklyCountryDamages', 'weeklyCountryDamagesPerCitizen', 'countryRegionDiff', 'countryDevelopment', 'countryActivePopulation', 'countryDamages', 'countryWealth', 'countryProductionBonus', 'countryBounty', 'weeklyUserDamages', 'userDamages', 'userWealth', 'userLevel', 'userReferrals', 'userSubscribers', 'userTerrain', 'userPremiumMonths', 'userPremiumGifts', 'userCasesOpened', 'userGemsPurchased', 'userBounty', 'muWeeklyDamages', 'muDamages', 'muTerrain', 'muWealth', 'muBounty'
]

ARTICLE_CATEGORY: TypeAlias = Literal[
    "news", "guide", "stats",
    "economy", "politics", "military",
    "begging", "entertainment", "election",
    "other", "official"
]

ARTICLE_TYPE: TypeAlias = Literal[
    "daily", "weekly", "top", "my", "subscriptions", "last"
]

TRANSACTION_TYPE: TypeAlias = Literal[
    "trading", "itemMarket", "battleLoot",
    "wage", "donation", "articleTip",
    "openCase", "craftItem", "dismantleItem"
]

ITEM_MARKET_CODE: TypeAlias = Literal[
    "knife", "gun", "rifle", "sniper", "tank", "jet",
    "helmet1", "helmet2", "helmet3", "helmet4", "helmet5", "helmet6",
    "chest1", "chest2", "chest3", "chest4", "chest5", "chest6",
    "gloves1", "gloves2", "gloves3", "gloves4", "gloves5", "gloves6",
    "pants1", "pants2", "pants3", "pants4", "pants5", "pants6",
    "boots1", "boots2", "boots3", "boots4", "boots5", "boots6",
]

UPGRADE_TYPE: TypeAlias = Literal[
    "bunker", "base", "pacificationCenter",
    "storage", "automatedEngine", "breakRoom",
    "headquarters", "dormitories"
]

BATTLE_FILTER: TypeAlias = Literal[
    "all", "yourCountry", "yourEnemies"
]

MERCENARY_CONTRACT_STATUS: TypeAlias = Literal[
    "active", "won", "cancelled",
    "expiredNoBids", "expiredBattle", "expiredRound"
]

MERCENARY_CONTRACT_SORT_BY: TypeAlias = Literal[
    "createdAt", "expiresAt", "currentPerK",
    "minimumDamage", "budget", "duration"
]

SORT_ORDER: TypeAlias = Literal[
    "asc", "desc"
]


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


class Ranking(TypedDict):

    country: str
    value: int
    rank: int
    tier: TIER
    _id: str


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


# User Stuff

class UserMute(TypedDict):

    reason: str
    mutedUntil: datetime

class UserBuffs(TypedDict):

    buffCodes: list[str]
    buffEndAt: datetime

class UserLeveling(TypedDict):

    level: int
    totalXp: int
    dailyXpLeft: int
    availableSkillPoints: int
    spentSkillPoints: int
    totalSkillPoints: int
    freeReset: int


class UserMissionsClaimedAt(TypedDict):

    starting: datetime
    daily: datetime


class UserMissions(TypedDict):

    claimedAt: UserMissionsClaimedAt
    rerolledWeeklyMissions: int
    rerolledDailyMissions: int


class UserDates(TypedDict):

    lastConnectionAt: datetime
    lastNotificationsCheckAt: datetime
    lastCountryMessageCheckAt: datetime
    lastGlobalMessageCheckAt: datetime
    lastEventsCheckAt: datetime
    lastWorkOfferApplications: list[datetime]
    lastHiresAt: list[datetime]
    lastWorkAt: datetime
    lastCompanyJoinedAt: datetime
    lastDailyRewardClaimedAt: datetime
    lastHelpAskedAt: datetime


class UserSkill(TypedDict):

    level: int
    currentBarValue: int
    value: int
    weapon: str | None
    equipment: str | None
    limited: str | None
    total: int
    totalAfterSoftCap: int | None
    hourlyBarRegen: int
    overflow: int | None
    ammoPercent: int | None
    buffsPercent: int | None
    debuffsPercent: int | None
    militaryRankPercent: float | None


class UserSkills(TypedDict):

    energy: UserSkill
    health: UserSkill
    hunger: UserSkill
    attack: UserSkill
    companies: UserSkill
    entrepreneurship: UserSkill
    production: UserSkill
    criticalChance: UserSkill
    criticalDamages: UserSkill
    armor: UserSkill
    precision: UserSkill
    dodge: UserSkill
    lootChance: UserSkill
    management: UserSkill


class UserStatsCase1Rarity(TypedDict):

    common: int
    uncommon: int
    rare: int
    epic: int
    legendary: int
    mythic: int


class UserStatsCase(TypedDict):

    byRarity: UserStatsCase1Rarity
    openedCount: int


class UserStatsWealth(TypedDict):

    companies: float
    items: float
    money: float
    equipments: float
    weapons: float
    total: float


class UserStats(TypedDict):

    worksCount: int
    damagesCount: int
    estimatedCompanyValues: float
    estimatedInventoryValue: float
    estimatedWealth: float
    case1: UserStatsCase
    wealth: UserStatsWealth
    case2: UserStatsCase


class UserEquipment(TypedDict):

    chest: str | None
    boots: str | None
    weapon: str | None
    pants: str | None
    ammo: str | None
    helmet: str | None
    gloves: str | None


class UserRankingsData(TypedDict):

    value: float
    rank: int
    tier: TIER


class UserRankings(TypedDict):

    userDamages: UserRankingsData | None
    weeklyUserDamages: UserRankingsData | None
    userWealth: UserRankingsData | None
    userLevel: UserRankingsData | None
    userReferrals: UserRankingsData | None
    userCasesOpened: UserRankingsData | None
    userBounty: UserRankingsData | None
    damagesCount: int | None


class UserPreferences(TypedDict):

    autoReplaceOnBreak: bool

# Article Stuff

class ArticleStats(TypedDict):

    likes: int
    dislikes: int
    score: int
    views: int
    comments: int
    subs: int
    tips: int
    gemTips: int


# MU Stuff

class MURoles(TypedDict):

    managers: list[str]
    commanders: list[str]


class MULeveling(TypedDict):

    level: int
    monthlyDamages: int


class MURankingData(TypedDict):

    value: float
    rank: int
    tier: TIER


class MURankings(TypedDict):

    muWeeklyDamages: MURankingData
    muBounty: MURankingData
    muDamages: MURankingData
    muTerrain: MURankingData
    muWealth: MURankingData


class MUActiveUpgradeLevels(TypedDict):

    dormitories: int
    headquarters: int | None


# Transactions Stuff

class ItemMarketSkills(TypedDict):

    attack: int | None
    criticalChance: int | None
    precision: int | None
    armor: int | None
    dodge: int | None
    criticalDamages: int | None


class ItemMarket(TypedDict):

    _id: str
    code: ITEM_MARKET_CODE
    type: Literal["equipment"]
    skills: ItemMarketSkills
    state: int
    maxState: int
    quantity: int
    lastAcquisitionAt: datetime
    isEquipStatsMigrated: bool | None


# Party stuff

class PartyEthics(TypedDict):

    militarism: int
    isolationism: int
    imperialism: int
    inudstrialism: int


# Alliances Stuff

class AllianceMember(TypedDict):

    country: str
    coreDevelopment: float
    averageDevelopment: float
    suspended: bool


class AllianceRanking(TypedDict):

    value: float
    rank: int
    tier: TIER


class AllianceRankings(TypedDict):

    allianceInitialDevelopment: AllianceRanking
    allianceDevelopment: AllianceRanking
    allianceWeeklyDamages: AllianceRanking
    allianceDamages: AllianceRanking
    alliancePopulation: AllianceRanking
    allianceWeeklyDamagesPerCitizen: AllianceRanking



# Tournament Stuff

class RegisteredParties(TypedDict):

    countries: list[str]
    mus: list[str]
    users: list[str]


class TournamentMatch(TypedDict):

    matchIndex: int
    attacker: str
    defender: str
    isQualificationRound: bool
    possibleAttackerTeamIds: list[str]
    possibleDefenderTeamIds: list[str]
    battle: str
    wonBy: str | None


class TournamentRound(TypedDict):

    roundNumber: int
    cases: int
    skillValue: int | None
    matches: list[TournamentMatch]


# War Stuff

class WarSide(TypedDict):

    country: str
    wonBattlesCount: int
    wonRoundsCount: int
    damages: int


# Mercenary Contract Auction Stuff

class MercenaryContractAuctionBid(TypedDict):

    mu: str
    user: str
    payout: float
    perK: float
    bidAt: datetime

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