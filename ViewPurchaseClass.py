# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
# import VendorScreen, PurchaseClass

# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
# server = 'LAPTOP-MNMD5RBU'
# database = 'Inventory_Management_System_Script'  # Name of your Northwind database
# use_windows_authentication = True  # Set to True to use Windows Authentication
# username = 'your_username'  # Specify a username if not using Windows Authentication
# password = 'your_password'  # Specify a password if not using Windows Authentication

# if use_windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# connection = pyodbc.connect(connection_string)
# cursor = connection.cursor()

server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
database = 'Inventory_Management_System'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = 'Sirmehdi69'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = (
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=Inventory_Management_System;UID=sa;PWD=Sirmehdi69;TrustServerCertificate=yes;Connection Timeout=30;'
    )

# Establish a connection to the database
connection = pyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()



class ViewPurchaseScreen(QtWidgets.QMainWindow):
    def __init__(self, purchase_id, purchase_date, total_amount, vendor_id):
        super(ViewPurchaseScreen, self).__init__() 
        uic.loadUi("Screens/ViewPurchase.ui", self)

        self.purchase_id = int(purchase_id)
        self.purchase_date = QDate.fromString(str(purchase_date), 'yyyy-MM-dd')
        self.total_amount = int(total_amount)
        self.vendor_id = int(vendor_id)

        self.viewPurchaseId.setText(str(self.purchase_id))
        self.viewPurchaseId.setDisabled(True)

        self.viewPurchaseDate.setDate(self.purchase_date)
        self.viewPurchaseDate.setDisabled(True)

        self.viewTotalAmount.setText(str(self.total_amount))
        self.viewTotalAmount.setDisabled(True)

        self.viewVendorId.setText(str(self.vendor_id))
        self.viewVendorId.setDisabled(True)