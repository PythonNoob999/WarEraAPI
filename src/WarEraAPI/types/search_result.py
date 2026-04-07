from dataclasses import dataclass


@dataclass
class SearchResult:

    userIds: list[str]
    muIds: list[str]
    countryIds: list[str]
    regionIds: list[str]
    partyIds: list[str]
    hasData: bool