from typing import TypedDict
from typing import Literal


class countryMoneyTransferEvent(TypedDict):

    type: Literal["countryMoneyTransfer"]
    countries: list[str]
    money: float | int