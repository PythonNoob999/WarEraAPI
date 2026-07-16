from dataclasses import dataclass


@dataclass
class SearchResult:

    userIds: list[str]
    muIds: list[str]
    countryIds: list[str]
    regionIds: list[str]
    partyIds: list[str]
    allianceIds: list[str]
    hasData: bool