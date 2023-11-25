# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditVendorClass

# server = 'localhost'
# database = 'Inventory_Management_System'  # Name of your Northwind database
# use_windows_authentication = False  # Set to True to use Windows Authentication
# username = 'sa'  # Specify a username if not using Windows Authentication
# password = 'Sirmehdi69'  # Specify a password if not using Windows Authentication

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

        # if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
        #     self.notAddedMsg = AddVendorClass.AddVendorMessageBox("Please enter complete information to add vendor", "Failed")
        #     self.notAddedMsg.show()
        # else:
            # sql_query = "insert into vendor values(?, ?, ?, ?, ?)"
            # cursor.execute(sql_query, (name, contact, backupContact, email, address))
            # connection.commit()

        #     self.addMsg = AddVendorClass.AddVendorMessageBox("Vendor added successfully", "Success")
        #     self.addMsg.show()
        self.msg = QtWidgets.QMessageBox()
        if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter complete information.")
        else:
            sql_query = "insert into vendor values(?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (name, contact, backupContact, email, address))
            connection.commit()
            self.msg.setWindowTitle("Success")
            self.msg.setText("Vendor added successfully.")
        self.msg.show()
    
    def EditVendor(self):
        self.editVendor = EditVendorClass.EditVendorScreen()
        self.editVendor.show()
        