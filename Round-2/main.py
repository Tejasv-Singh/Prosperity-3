from typing import Dict, List
from datamodel import Order, TradingState, OrderDepth, Trade

class Trader:
    def __init__(self):
        self.position = {"CROISSANTS": 0, "JAMS": 0, "DJEMBE": 0, "PICNIC_BASKET1": 0, "PICNIC_BASKET2": 0}
        self.position_limits = {"CROISSANTS": 250, "JAMS": 350, "DJEMBE": 60, "PICNIC_BASKET1": 60, "PICNIC_BASKET2": 100}
        
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        
        # Update position with the current state
        if state.position:
            for product, pos in state.position.items():
                if product in self.position:
                    self.position[product] = pos
        
        # Basket compositions
        basket1_contents = {"CROISSANTS": 6, "JAMS": 3, "DJEMBE": 1}
        basket2_contents = {"CROISSANTS": 4, "JAMS": 2}
        
        for product in state.order_depths.keys():
            order_list = []
            
            if product == "PICNIC_BASKET1" or product == "PICNIC_BASKET2":
                # Get the best buy and sell prices for the basket
                bids = {}
                asks = {}
                
                if state.order_depths[product].buy_orders:
                    bids = state.order_depths[product].buy_orders
                
                if state.order_depths[product].sell_orders:
                    asks = state.order_depths[product].sell_orders
                
                # Calculate the value of the basket from its components
                if product == "PICNIC_BASKET1":
                    components = basket1_contents
                else:
                    components = basket2_contents
                
                component_value = 0
                all_components_available = True
                
                for component, quantity in components.items():
                    if component in state.order_depths:
                        if state.order_depths[component].sell_orders:  # Check if there are sell orders
                            best_sell_price = min(state.order_depths[component].sell_orders.keys())
                            component_value += quantity * best_sell_price
                        elif state.order_depths[component].buy_orders:  # If no sell orders, use buy orders
                            best_buy_price = max(state.order_depths[component].buy_orders.keys())
                            component_value += quantity * best_buy_price
                        else:
                            all_components_available = False
                            break
                    else:
                        all_components_available = False
                        break
                
                if all_components_available:
                    # Check if we can profit by buying basket and selling components
                    if bids:  # If there are buy orders for the basket
                        best_bid = max(bids.keys())
                        if best_bid > component_value:
                            # Profit by selling basket and buying components
                            available_sell_quantity = min(
                                bids[best_bid],
                                self.position_limits[product] - self.position[product]
                            )
                            
                            if available_sell_quantity > 0:
                                order_list.append(Order(product, best_bid, -available_sell_quantity))
                                self.position[product] -= available_sell_quantity
                                
                                # Buy the components
                                for component, quantity in components.items():
                                    component_qty = quantity * available_sell_quantity
                                    if component in state.order_depths and state.order_depths[component].sell_orders:
                                        sell_prices = sorted(state.order_depths[component].sell_orders.keys())
                                        remaining_qty = component_qty
                                        
                                        for price in sell_prices:
                                            available_qty = min(
                                                state.order_depths[component].sell_orders[price],
                                                remaining_qty,
                                                self.position_limits[component] - self.position[component]
                                            )
                                            
                                            if available_qty > 0:
                                                if component not in result:
                                                    result[component] = []
                                                result[component].append(Order(component, price, available_qty))
                                                self.position[component] += available_qty
                                                remaining_qty -= available_qty
                                            
                                            if remaining_qty == 0:
                                                break
                    
                    # Check if we can profit by selling basket and buying components
                    if asks:  # If there are sell orders for the basket
                        best_ask = min(asks.keys())
                        if best_ask < component_value:
                            # Profit by buying basket and selling components
                            available_buy_quantity = min(
                                asks[best_ask],
                                self.position_limits[product] + self.position[product]
                            )
                            
                            if available_buy_quantity > 0:
                                order_list.append(Order(product, best_ask, available_buy_quantity))
                                self.position[product] += available_buy_quantity
                                
                                # Sell the components
                                for component, quantity in components.items():
                                    component_qty = quantity * available_buy_quantity
                                    if component in state.order_depths and state.order_depths[component].buy_orders:
                                        buy_prices = sorted(state.order_depths[component].buy_orders.keys(), reverse=True)
                                        remaining_qty = component_qty
                                        
                                        for price in buy_prices:
                                            available_qty = min(
                                                state.order_depths[component].buy_orders[price],
                                                remaining_qty,
                                                self.position_limits[component] + self.position[component]
                                            )
                                            
                                            if available_qty > 0:
                                                if component not in result:
                                                    result[component] = []
                                                result[component].append(Order(component, price, -available_qty))
                                                self.position[component] -= available_qty
                                                remaining_qty -= available_qty
                                            
                                            if remaining_qty == 0:
                                                break
            
            if order_list:
                result[product] = order_list
        
        return result

# The following is required for local testing
if __name__ == "__main__":
    # Create a sample trading state for testing
    order_depth1 = OrderDepth(
        buy_orders={10: 10},
        sell_orders={12: 10}
    )
    order_depth2 = OrderDepth(
        buy_orders={5: 5},
        sell_orders={6: 5}
    )
    order_depth3 = OrderDepth(
        buy_orders={15: 5},
        sell_orders={17: 5}
    )
    order_depth4 = OrderDepth(
        buy_orders={80: 5},
        sell_orders={85: 5}
    )
    order_depth5 = OrderDepth(
        buy_orders={50: 5},
        sell_orders={55: 5}
    )
    
    state = TradingState(
        timestamp=0,
        listings={},
        order_depths={
            "CROISSANTS": order_depth1,
            "JAMS": order_depth2,
            "DJEMBE": order_depth3,
            "PICNIC_BASKET1": order_depth4, 
            "PICNIC_BASKET2": order_depth5
        },
        own_trades={},
        market_trades={},
        position={},
        observations={}
    )
    
    trader = Trader()
    result = trader.run(state)
    
    print("Trading Result:")
    for product, orders in result.items():
        print(f"{product}:")
        for order in orders:
            print(f"  Price: {order.price}, Quantity: {order.quantity}")