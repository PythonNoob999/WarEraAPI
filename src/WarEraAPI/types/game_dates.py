from dataclasses import dataclass
from datetime import datetime


from WarEraAPI.utils import edit_types


@dataclass
class GameDates:

    nextDayAt: datetime
    nextRegenAt: datetime
    previousDayAt: datetime
    nextCongressElectionsAt: datetime
    nextPresidentialElectionsAt: datetime
    nextMonthAt: datetime
    dailyMissionRegenAt: datetime
    weeklyMissionRegenAt: datetime


    def __post_init__(self):
        
        edit_types(self)