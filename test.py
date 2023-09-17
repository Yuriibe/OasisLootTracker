import re
from scapy.all import *
from scapy.layers.inet import IP, TCP
from itemApi import *
import dataManager
import itemLogger

last_package = ""
last_payload = b''  # Initialize a variable to hold the last payload
all_ips = ["20.76.13", "20.76.14.27",
           "20.76.14", "45.223.19.187", "63.32.251.0", "52.30.70.249"]
identifier_regex = r"[56][0-9a-f]0100[0-9a-f]{4}"
def reverse_id(id_hex):
    part1 = id_hex[:2]
    part2 = id_hex[2:]

    return part2 + part1

def get_price(item_id):
    if get_market_price(item_id) is not None:
        price = get_market_price(item_id)
    else:
        price = get_vendor_price(item_id)
    return price


def package_handler(package, messages):
    global last_package

    if (IP not in package):
        return
    ip = package[IP]

    is_bdo_ip = [x for x in all_ips if x in ip.src or x == ip.src]
    if len(is_bdo_ip) > 0:

        if not hasattr(package[TCP].payload, "load"):
            return


        payload_raw = bytes(package[TCP].payload).hex()

        # Merging the logic for handling split identifiers
        payload = last_package + payload_raw
        position = 0
        while(len(payload[position:]) >= 600):
            payload = payload[position:]
            position = 0
            match_location = 0
            matches = list(re.finditer(identifier_regex, payload))

            if len(matches) == 0:
                return  # no match found, return - could cause issue if the identifier is split between two packages
            elif len(matches) == 1:
                match_location = matches[0].start()
            else:
                if matches[0].start() + 600 < matches[1].start():
                    match_location = matches[0].start()
                else:
                    match_location = matches[1].start()

            payload = payload[match_location:]

        last_package = payload_raw

        # Continue with the original logic
        content = payload_raw
        while '0b010006' in content:
            index = content.index("0b010006")
            content = content[index:]

            amount_hex = content[60:64]
            id_hex = content[54:58]

            item_id = int(reverse_id(id_hex), 16)
            amount = int(amount_hex, 16)

            total_price = int(get_price(item_id)) * int(amount)
            item_name = str(get_item_name(item_id))
            dataManager.set_item_id(item_id)
            dataManager.set_item_name(item_name)
            dataManager.set_item_amount(amount)
            dataManager.set_item_total_price(total_price)
            itemLogger.log_items()
            print("Amount: " + str(amount))
            print("ID: " + str(item_id))
            print("Price: " + str(total_price))
            print("\n")

            content = content[index + 2:]



def start_packet_sniffer():
    sniff(filter="tcp", prn=lambda x: package_handler(x, []))


start_packet_sniffer()
