from .alliance_formed import allianceFormedEvent
from .alliance_broken import allianceBrokenEvent
from .battle_ended import battleEndedEvent
from .battle_opened import battleOpenedEvent
from .country_money_transfer import countryMoneyTransferEvent
from .deposit_discovered import depositDiscoveredEvent
from .new_president import newPresidentEvent
from .peace_made import peaceMadeEvent
from .region_transfer import regionTransferEvent
from .war_declared import warDeclaredEvent

from WarEraAPI.types.constants import EVENT_TYPES
from typing import TypeAlias


EventTypes: TypeAlias = \
    allianceFormedEvent | allianceBrokenEvent | \
    battleEndedEvent | battleOpenedEvent | \
    countryMoneyTransferEvent | depositDiscoveredEvent | \
    newPresidentEvent | peaceMadeEvent | \
    regionTransferEvent | warDeclaredEvent

EventType: TypeAlias = type[EventTypes]