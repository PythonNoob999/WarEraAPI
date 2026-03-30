from dataclasses import dataclass, field


@dataclass
class Government:

    _id: str
    country: str
    congressMembers: list[str]
    president: str | None = field(default=None)
    minOfDefense: str | None = field(default=None)
    vicePresident: str | None = field(default=None)
    minOfForeignAffairs: str | None = field(default=None)
    minOfEconomy: str | None = field(default=None)