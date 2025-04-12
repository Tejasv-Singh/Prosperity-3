
import time
import random

BASKET1_CONTENTS = {
    "CROISSANTS": 6,
    "JAM": 3,
    "DJEMBE": 1
}

BASKET2_CONTENTS = {
    "CROISSANTS": 4,
    "JAM": 2
}

def get_market_prices():
    return {
        "CROISSANTS": random.randint(10, 16),
        "JAM": random.randint(12, 18),
        "DJEMBE": random.randint(35, 50),
        "PICNIC_BASKET1": random.randint(140, 180),
        "PICNIC_BASKET2": random.randint(75, 110)
    }

def compute_basket_value(basket_contents, prices):
    value = 0
    for item, qty in basket_contents.items():
        value += qty * prices[item]
    return value

def detect_arbitrage(prices):
    basket1_value = compute_basket_value(BASKET1_CONTENTS, prices)
    basket2_value = compute_basket_value(BASKET2_CONTENTS, prices)

    market_price1 = prices["PICNIC_BASKET1"]
    market_price2 = prices["PICNIC_BASKET2"]

    print("\n--- Current Prices ---")
    for item, price in prices.items():
        print(f"{item}: {price}")

    print("\n--- Basket Valuations ---")
    print(f"PICNIC_BASKET1: value={basket1_value}, market={market_price1}")
    print(f"PICNIC_BASKET2: value={basket2_value}, market={market_price2}")

    print("\n--- Arbitrage Suggestions ---")
    if market_price1 < basket1_value - 2:
        print("💡 Buy PICNIC_BASKET1 and sell its items individually (break it up).")
    elif market_price1 > basket1_value + 2:
        print("💡 Buy items and sell PICNIC_BASKET1 (create basket).")

    if market_price2 < basket2_value - 2:
        print("💡 Buy PICNIC_BASKET2 and sell its items individually (break it up).")
    elif market_price2 > basket2_value + 2:
        print("💡 Buy items and sell PICNIC_BASKET2 (create basket).")

while True:
    prices = get_market_prices()
    detect_arbitrage(prices)
    time.sleep(1)
