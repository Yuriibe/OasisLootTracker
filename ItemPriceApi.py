import requests
from lxml import html
import re

def get_market_price(item_id):
    url = "https://eu-trade.naeu.playblackdesert.com/Trademarket/GetMarketPriceInfo"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'BlackDesert'
    }
    data = {
        "keyType": 0,
        "mainKey": item_id,
        "subKey": 0
    }

    response = requests.post(url, headers=headers, json=data)

    response_data = response.json()
    if 'resultMsg' in response_data:
        result_message = response_data['resultMsg']
        entries = result_message.split('-')
        if len(entries) > 3:
            last_entry = entries[-1]  # Get the last entry
            return last_entry
        else:
            return None
    else:
        return None


def get_vendor_price(item_id):
    url = 'https://bdocodex.com/us/item/' + str(item_id) + '/'
    response = requests.get(url)
    html_content = response.text
    tree = html.fromstring(html_content)
    xpath_query_vendor = '//td[@colspan="2"]'
    results_vendor = tree.xpath(xpath_query_vendor)

    for result_vendor in results_vendor:
        text_from_result = result_vendor.text_content()
        match = re.search(r"Sell price: ([\d,]+)", text_from_result)

        if match:
            sell_price = match.group(1)
            sell_price = sell_price.replace(",","")
            return sell_price
        else:
            return 1


