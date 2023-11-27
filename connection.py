# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
# import VendorScreen, PurchaseClass
from PurchaseClass import PurchaseScreen

# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
server = 'LAPTOP-MNMD5RBU'
database = 'Inventory_Management_System_Script'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

class UI(QtWidgets.QMainWindow):   

    def __init__(self):

        super(UI, self).__init__() 
        
        uic.loadUi('Screens/UserAuthentication.ui', self)

        self.purchaseButton.setEnabled(True)
        self.purchaseButton.clicked.connect(self.OpenPurchaseScreen)

    def OpenPurchaseScreen(self):
        self.purchase = PurchaseScreen()
        self.purchase.show()

app = QApplication(sys.argv)
loginScreen = UI()
loginScreen.show()
sys.exit(app.exec())
