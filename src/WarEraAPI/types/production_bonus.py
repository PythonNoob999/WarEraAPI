from dataclasses import dataclass


@dataclass
class ProductionBonus:

    strategicBonus: float
    depositBonus: float
    ethicSpecializationBonus: float
    ethicDepositBonus: float
    total: float