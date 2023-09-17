import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
import dataManager
from lootTracker import start_packet_sniffer
import threading
import itemLogger



class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window to be frameless, always on top, and transparent to mouse events
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(
            Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # Set the window's opacity (transparency)
        self.setWindowOpacity(0.7)

        # Set the size and position of the overlay
        self.setGeometry(100, 100, 800, 600)

        # Create a QLabel widget
        self.item_id_label = QLabel("", self)
        self.item_id_label.setGeometry(10, 10, 400, 30)  # Set label position and size
        self.item_id_label.setStyleSheet('font-size: 20px; color: black;')

        self.item_name_label = QLabel("", self)
        self.item_name_label.setGeometry(10, 60, 400, 30)  # Set label position and size
        self.item_name_label.setStyleSheet('font-size: 20px; color: black;')

        self.item_amount_label = QLabel("", self)
        self.item_amount_label.setGeometry(10, 110, 400, 30)  # Set label position and size
        self.item_amount_label.setStyleSheet('font-size: 20px; color: black;')

        self.item_total_price_label = QLabel("", self)
        self.item_total_price_label.setGeometry(10, 160, 400, 30)  # Set label position and size
        self.item_total_price_label.setStyleSheet('font-size: 20px; color: black;')

        self.item_total_profit_label = QLabel("", self)
        self.item_total_profit_label.setGeometry(10, 210, 400, 30)  # Set label position and size
        self.item_total_profit_label.setStyleSheet('font-size: 20px; color: black;')

        # Create a timer to periodically update the item ID label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(100)  # Update every 1000 milliseconds (1 second)

    def update_labels(self):
        # Update the item ID label with the latest item ID
        item_id = dataManager.get_item_id()
        self.item_id_label.setText(f'Item ID: {item_id}')

        # Update the item amount label with the latest item amount
        item_amount = dataManager.get_item_amount()
        self.item_amount_label.setText(f'Amount: {item_amount}')

        # Update the item total price label with the latest total price
        item_total_price = dataManager.get_item_total_price()
        self.item_total_price_label.setText(f'Total Price: {item_total_price}')

        # Update the item name label with the latest item name
        item_name = dataManager.get_item_name()
        self.item_name_label.setText(f'Item Name: {item_name}')

       # total_profit = itemLogger.calculate_profit()
        #self.item_total_profit_label.setText(f'Total Profit: {total_profit}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sniffer_thread = threading.Thread(target=start_packet_sniffer)
    sniffer_thread.start()
    sys.exit(app.exec_())
