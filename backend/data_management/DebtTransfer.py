from dataclasses import dataclass
from typing import List


@dataclass
class Debt:
    payer: str
    leech: str
    amount: float

@dataclass
class Transaction:
    payer: str
    leeches: List[str]
    amount: float

    split_type: str = 'even'

def transfer_debt(transaction: List[Transaction]):
    # TODO: take the transactions and output a list of debts
    pass