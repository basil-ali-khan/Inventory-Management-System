# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import VendorScreen

# server = 'localhost'
# database = 'Inventory_Management_System'  # Name of your Northwind database
# use_windows_authentication = False  # Set to True to use Windows Authentication
# username = 'sa'  # Specify a username if not using Windows Authentication
# password = 'Sirmehdi69'  # Specify a password if not using Windows Authentication

# if use_windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:
connection_string = (
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=Inventory_Management_System;UID=sa;PWD=Sirmehdi69;TrustServerCertificate=yes;Connection Timeout=30;'
)

# Establish a connection to the database
connection = pyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()

class EditVendorScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EditVendorScreen, self).__init__()
        uic.loadUi("Screens/EditVendors.ui", self)



class AddVendorMessageBox(QMessageBox):
    def __init__(self, message, title):
        super().__init__()

        self.setIcon(QMessageBox.Icon.Information)
        self.setText(message)
        self.setWindowTitle(title)
        self.addButton(QMessageBox.StandardButton.Close)

class VendorScreen(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(VendorScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/Vendors.ui', self)

        self.PopulateVendorTable()        

        self.addVendorButton.clicked.connect(self.AddVendor)

        self.editVendorButton.clicked.connect(self.EditVendor)


    def PopulateVendorTable(self):
        cursor.execute("select * from vendor")
        self.vendorTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.vendorTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.vendorTable.setItem(row_index, col_index, item)

    def AddVendor(self):
        name = self.vendorNameBox.text()
        contact = self.vendorContactNumber.text()
        backupContact = self.vendorBackupContact.text()
        email = self.vendorEmail.text()
        address = self.vendorAddress.text()

        if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
            self.notAddedMsg = AddVendorMessageBox("Please enter complete information to add vendor", "Failed")
            self.notAddedMsg.show()
        else:
            sql_query = "insert into vendor values(?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (name, contact, backupContact, email, address))
            connection.commit()

            self.addMsg = AddVendorMessageBox("Vendor added successfully", "Success")
            self.addMsg.show()
    
    def EditVendor(self):
        self.editVendor = EditVendorScreen()
        self.editVendor.show()
        

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


    def OpenVendorScreen(self):
        self.vendor = VendorScreen()
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
            self.addMsg = AddVendorMessageBox("Incorrect Username and/or Password", "Error")
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
