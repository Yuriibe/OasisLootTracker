import dataManager
import itemApi

# Initialize an empty dictionary to accumulate items
picked_up_items_in_session = {}

def log_items():
    # Get item ID and amount from dataManager
    item_id = dataManager.get_item_id()
    item_amount = dataManager.get_item_amount()

    # Check if the item is already in the dictionary
    if item_id in picked_up_items_in_session:
        # If it's already there, update the quantity
        picked_up_items_in_session[item_id] += item_amount
    else:
        # If it's not in the dictionary, add it with the initial quantity
        picked_up_items_in_session[item_id] = item_amount

    # Print the updated dictionary
    print(picked_up_items_in_session)


def calculate_profit():
    total_profit = 0
    for item_id, item_amount in picked_up_items_in_session.items():
        price = get_price(item_id)
        total_price = int(price) * int(item_amount)
        total_profit += total_price
    formatted_total_profit = '{:,.0f}'.format(total_profit)
    return formatted_total_profit

def get_price(item_id):
    if itemApi.get_market_price(item_id) is not None:
        price = itemApi.get_market_price(item_id)
    else:
        price = itemApi.get_vendor_price(item_id)
    return price


