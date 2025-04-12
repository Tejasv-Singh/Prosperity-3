import time
import random

# Simulate getting market prices
def get_market_prices():
    return {
        "CROISSANTS": random.uniform(8, 12),
        "JAM": random.uniform(10, 14),
        "DJEMBE": random.uniform(25, 40),
        "PICNIC_BASKET1": random.uniform(100, 130),
        "PICNIC_BASKET2": random.uniform(60, 90)
    }

# Position limits
POSITION_LIMITS = {
    "CROISSANTS": 250,
    "JAM": 350,
    "DJEMBE": 60,
    "PICNIC_BASKET1": 60,
    "PICNIC_BASKET2": 100
}

# Current holdings
positions = {k: 0 for k in POSITION_LIMITS.keys()}

# Basket definitions
BASKET1_CONTENTS = {
    "CROISSANTS": 6,
    "JAM": 3,
    "DJEMBE": 1
}

BASKET2_CONTENTS = {
    "CROISSANTS": 4,
    "JAM": 2
}

# Compute the value of a basket using component prices
def compute_basket_value(basket_contents, prices):
    return sum(qty * prices[item] for item, qty in basket_contents.items())

# Simulated trade execution
def place_order(symbol, price, qty, side):
    print(f"Placing {side.upper()} order: {qty} {symbol} @ {round(price, 2)}")
    if side == "buy":
        positions[symbol] += qty
    elif side == "sell":
        positions[symbol] -= qty

# Arbitrage logic for Basket 1
def try_arbitrage_basket1(prices):
    value = compute_basket_value(BASKET1_CONTENTS, prices)
    market_price = prices["PICNIC_BASKET1"]
    spread = value - market_price

    if spread > 5:
        print("💡 Arbitrage: Buy BASKET1, Sell Components")
        if positions["PICNIC_BASKET1"] < POSITION_LIMITS["PICNIC_BASKET1"]:
            place_order("PICNIC_BASKET1", market_price, 1, "buy")
            for product, qty in BASKET1_CONTENTS.items():
                if positions[product] + qty <= POSITION_LIMITS[product]:
                    place_order(product, prices[product], qty, "sell")

    elif -spread > 5:
        print("💡 Arbitrage: Buy Components, Sell BASKET1")
        for product, qty in BASKET1_CONTENTS.items():
            if positions[product] + qty <= POSITION_LIMITS[product]:
                place_order(product, prices[product], qty, "buy")
        if positions["PICNIC_BASKET1"] < POSITION_LIMITS["PICNIC_BASKET1"]:
            place_order("PICNIC_BASKET1", market_price, 1, "sell")

# Arbitrage logic for Basket 2
def try_arbitrage_basket2(prices):
    value = compute_basket_value(BASKET2_CONTENTS, prices)
    market_price = prices["PICNIC_BASKET2"]
    spread = value - market_price

    if spread > 3:
        print("💡 Arbitrage: Buy BASKET2, Sell Components")
        if positions["PICNIC_BASKET2"] < POSITION_LIMITS["PICNIC_BASKET2"]:
            place_order("PICNIC_BASKET2", market_price, 1, "buy")
            for product, qty in BASKET2_CONTENTS.items():
                if positions[product] + qty <= POSITION_LIMITS[product]:
                    place_order(product, prices[product], qty, "sell")

    elif -spread > 3:
        print("💡 Arbitrage: Buy Components, Sell BASKET2")
        for product, qty in BASKET2_CONTENTS.items():
            if positions[product] + qty <= POSITION_LIMITS[product]:
                place_order(product, prices[product], qty, "buy")
        if positions["PICNIC_BASKET2"] < POSITION_LIMITS["PICNIC_BASKET2"]:
            place_order("PICNIC_BASKET2", market_price, 1, "sell")

# Main trading loop
if __name__ == "__main__":
    while True:
        prices = get_market_prices()
        print("\n📊 Market Prices:", {k: round(v, 2) for k, v in prices.items()})
        try_arbitrage_basket1(prices)
        try_arbitrage_basket2(prices)
        print("📦 Positions:", positions)
        time.sleep(2)
