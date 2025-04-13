from typing import Dict, List
from dataclasses import dataclass

@dataclass
class OrderDepth:
    buy_orders: Dict[float, int] = None
    sell_orders: Dict[float, int] = None


class Order:
    def __init__(self, symbol: str, price: float, quantity: int):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity


@dataclass
class Trade:
    symbol: str
    price: float
    quantity: int
    buyer: str = ""
    seller: str = ""


@dataclass
class TradingState:
    timestamp: int
    listings: Dict[str, float]
    order_depths: Dict[str, OrderDepth]
    own_trades: Dict[str, List[Trade]]
    market_trades: Dict[str, List[Trade]]
    position: Dict[str, int]
    observations: Dict[str, float]