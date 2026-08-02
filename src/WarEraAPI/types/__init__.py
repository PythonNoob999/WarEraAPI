from .worker import Worker
from .company import Company
from .country import Country
from .event import Event
from .government import Government
from .region import Region
from .battle import Battle
from .battle_data import BattleData
from .round import Round
from .trading_order import TradingOrder
from .work_offer import WorkOffer
from .rankings import Rankings
from .search_result import SearchResult
from .game_dates import GameDates
from .user import User
from .article import Article
from .military_unit import MilitaryUnit
from .recommended_region import RecommendedRegion
from .production_bonus import ProductionBonus
from .entity_upgrade import EntityUpgrade
from .battle_order import BattleOrder
from .user_equipments import UserEquipments
from .party import Party
from .alliance import Alliance
from .tournament import Tournament
from .tournament_team import TournamentTeam
from .war import War
from .transactions import *
from .constants import *
from .events import *

from typing import TypeAlias


# behold this ugly sh*t

Transaction: TypeAlias = \
    TradingTransaction | ItemMarketTransaction | \
    BattleLootTransaction | WageTransaction | \
    DonationTransaction | ArticleTipTransaction | \
    OpenCaseTransaction | CraftItemTransaction | \
    DismantleItemTransaction
TransactionType: TypeAlias = type[Transaction]

TransactionMapping: dict[TRANSACTION_TYPE, TransactionType] = {
    "trading": TradingTransaction,
    "itemMarket": ItemMarketTransaction,
    "battleLoot": BattleLootTransaction,
    "wage": WageTransaction,
    "donation": DonationTransaction,
    "articleTip": ArticleTipTransaction,
    "openCase": OpenCaseTransaction,
    "craftItem": CraftItemTransaction,
    "dismantleItem": DismantleItemTransaction
}