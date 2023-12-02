# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditVendorClass

server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
database = 'Inventory_Management_System'  # Name of your Northwind database
use_windows_authentication = False  # Set to True to use Windows Authentication
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
        self.searchVendorValue.setPlaceholderText("Search")
        self.addVendorButton.clicked.connect(self.AddVendor)
        self.editVendorButton.clicked.connect(self.EditVendor)
        self.searchVendorButton.clicked.connect(self.SearchVendor)
        self.deleteVendorButton.clicked.connect(self.DeleteVendor)

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
        self.msg = QtWidgets.QMessageBox()
        if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter complete information.")
        else:
            sql_query = "insert into vendor values(?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (name, contact,
                           backupContact, email, address))
            connection.commit()
            self.msg.setWindowTitle("Success")
            self.msg.setText("Vendor added successfully.")
            self.PopulateVendorTable()
        self.msg.show()

    def SearchVendor(self):
        criteria = self.searchVendorCriteria.currentText()
        if criteria == "Vendor Name":
            criteria = "vendorName"
        elif criteria == "Contact Number":
            criteria = "contactNumber"
        elif criteria == "Email":
            criteria = "email"
        value = self.searchVendorValue.text()
        if not value:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter a search value.")
            self.msg.show()
            return

        sql_query = f"select * from vendor where {criteria} like ?"
        cursor.execute(sql_query, ('%' + value + '%',))

        rows = cursor.fetchall()

        if not rows:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("No Results")
            self.msg.setText("No results found for the given search criteria.")
            self.msg.show()
            self.PopulateVendorTable()
            return

        self.vendorTable.setRowCount(0)

        for row_index, row_data in enumerate(rows):
            self.vendorTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.vendorTable.setItem(row_index, col_index, item)

    def DeleteVendor(self):
        selected_items = self.vendorTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to delete.")
            self.msg.show()
            return

        # Assuming the first column contains a unique identifier (e.g., vendor_id)
        selected_row = selected_items[0].row()
        vendor_id = int(self.vendorTable.item(selected_row, 0).text())

        # Code block to check if the vendor has purchase history. If yes, then vendor cannot be deleted
        sql_check_sales = "select count(*) from Purchase where vendorID = ?"
        cursor.execute(sql_check_sales, (vendor_id,))
        result = cursor.fetchone()

        # Throw error message if customers has pre-existing sales record
        if result and result[0] > 0:
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle("Error")
                self.msg.setText("Cannot delete vendor with existing purchase records.")
                self.msg.show()
                return

        sql_query = "delete from vendor WHERE vendorID = ?"
        cursor.execute(sql_query, (vendor_id))
        connection.commit()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Success")
        self.msg.setText("Vendor deleted successfully.")
        self.msg.show()

        self.PopulateVendorTable()  # Update the vendorTable after deletion

    def EditVendor(self):
        selected_items = self.vendorTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to edit.")
            self.msg.show()
            return

        selected_row = selected_items[0].row()
        vendor_data = [self.vendorTable.item(selected_row, col_index).text(
        ) for col_index in range(self.vendorTable.columnCount())]

        self.editVendor = EditVendorClass.EditVendorScreen(vendor_data)
        self.editVendor.vendorUpdated.connect(self.PopulateVendorTable)
        self.editVendor.show()
