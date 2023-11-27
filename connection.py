# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import VendorClass
import ProductsClass
import MaterialClass
import EditVendorClass

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


class UI(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/UserAuthentication.ui', self)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.username.setPlaceholderText("Username")
        self.password.setPlaceholderText("Password")
        ###hardcoded for now, will later be enabled only if user has admin priveleges

        self.vendorsButton.setEnabled(False)
        self.customerButton.setEnabled(False)
        self.productsButton.setEnabled(False)
        self.salesButton.setEnabled(False)
        self.materialButton.setEnabled(False)
        self.purchaseButton.setEnabled(False)

        self.loginButton.clicked.connect(self.CheckPrivilege)
        self.vendorsButton.clicked.connect(self.OpenVendorScreen)
        self.productsButton.clicked.connect(self.OpenProductsScreen)
        self.materialButton.clicked.connect(self.OpenMaterialScreen)

    def OpenProductsScreen(self):
        self.products = ProductsClass.Product()
        self.products.show()

    def OpenMaterialScreen(self):
        self.materials = MaterialClass.Material()
        self.materials.show()


    def OpenVendorScreen(self):
        self.vendor = VendorClass.VendorScreen()
        self.vendor.show()
        
    def CheckPrivilege(self):
        username = self.username.text()
        password = self.password.text()
        sql_query = "select privilege from [User] where userName = ? and password = ?"
        cursor.execute(sql_query, (username, password))
        result = cursor.fetchone()
        if result is not None:
            result = result[0]
            if result == 'Admin':
                self.vendorsButton.setEnabled(True)
                self.customerButton.setEnabled(True)
                self.productsButton.setEnabled(True)
                self.salesButton.setEnabled(True)
                self.materialButton.setEnabled(True)
                self.purchaseButton.setEnabled(True)
            elif result == 'User':
                self.vendorsButton.setEnabled(False)
                self.customerButton.setEnabled(False)
                self.productsButton.setEnabled(False)
                self.salesButton.setEnabled(True)
                self.materialButton.setEnabled(False)
                self.purchaseButton.setEnabled(False)
        else:
            self.addMsg = QtWidgets.QMessageBox()
            self.addMsg.setWindowTitle('Error')
            self.addMsg.setText('Invalid credentials')
            # self.addMsg = AddVendorClass.AddVendorMessageBox("Incorrect Username and/or Password", "Error")
            self.addMsg.show()
            self.vendorsButton.setEnabled(False)
            self.customerButton.setEnabled(False)
            self.productsButton.setEnabled(False)
            self.salesButton.setEnabled(False)
            self.materialButton.setEnabled(False)
            self.purchaseButton.setEnabled(False)

        self.username.clear()
        self.password.clear()




app = QApplication(sys.argv)
loginScreen = UI()
loginScreen.show()
sys.exit(app.exec())
