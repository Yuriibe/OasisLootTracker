item_id = None
item_amount = None
item_total_price = None


def set_item_id(new_id):
    global item_id
    item_id = new_id


def get_item_id():
    return item_id


def set_item_amount(new_amount):
    global item_amount
    item_amount = new_amount


def get_item_amount():
    return item_amount


def set_item_total_price(new_total_price):
    global item_total_price
    item_total_price = new_total_price


def get_item_total_price():
    return item_total_price

