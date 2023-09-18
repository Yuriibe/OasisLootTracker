import re
from scapy.all import *
from scapy.layers.inet import IP, TCP
from itemApi import *
import dataManager
import itemLogger

last_package = ""
last_payload = ""  # Initialize a variable to hold the last payload
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
    if (IP not in package):
        return
    ip = package[IP]

    is_bdo_ip = [x for x in all_ips if x in ip.src or x == ip.src]
    if len(is_bdo_ip) > 0:

        if not hasattr(package[TCP].payload, "load"):
            return

       # print(package[TCP].payload)
        payload_raw = bytes(package[TCP].payload).hex()
        content = last_payload + payload_raw

        position = 0

        while len(content[position:]) >= 500:
            position = 0
            matches = list(re.finditer('0b010006', content))

            if len(matches) == 0:
                return  # no match found, return - could cause issue if the identifier is split between two packages
                print("No Match")
            elif len(matches) == 1:
                match_location = matches[0].start()
                #print("Match 1")
            else:
                if matches[0].start() + 500 < matches[1].start():
                    match_location = matches[0].start()
                    #print("Match 2")
                else:
                    match_location = matches[1].start()
                    #print("Match 3")
            print(content)
            identifier_length = len('0b010006')
            content = content[match_location + identifier_length:]
            global last_package
            if last_package == 0:
                last_package = payload_raw
                print(last_package)
            else:
                length = min(len(last_package), len(payload_raw))
                differences = 0
                for i in range(0, length - 1, 2):
                    if (last_package[i:i + 2] != payload_raw[i:i + 2]):
                        differences += 1

                last_package = payload_raw
                #print(len(content))
                #print(content)
                #print(match_location)

            amount_hex = content[52:56]
           # id_hex = content[54:58]
            id_hex = content[46:50]
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


            content = content[match_location:]




def start_packet_sniffer():
    sniff(filter="tcp", prn=lambda x: package_handler(x, []))


start_packet_sniffer()
