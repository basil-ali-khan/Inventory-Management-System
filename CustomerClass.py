# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditCustomerClass

# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
# database = 'Inventory_Management_System'  # Name of your Northwind database
# use_windows_authentication = False  # Set to True to use Windows Authentication
# username = 'sa'  # Specify a username if not using Windows Authentication
# password = 'Sirmehdi69'  # Specify a password if not using Windows Authentication

# if use_windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:
#     connection_string = (
#         'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=Inventory_Management_System;UID=sa;PWD=Sirmehdi69;TrustServerCertificate=yes;Connection Timeout=30;'
#     )

# # Establish a connection to the database
# connection = pyodbc.connect(connection_string)

# # Create a cursor to interact with the database
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

class CustomerScreen(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(CustomerScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/Customers.ui', self)

        self.PopulateCustomerTable()
        self.searchCustomerValue.setPlaceholderText("Search")
        self.addCustomerButton.clicked.connect(self.AddCustomer)
        self.editCustomerButton.clicked.connect(self.EditCustomer)
        self.searchCustomerButton.clicked.connect(self.SearchCustomer)
        self.deleteCustomerButton.clicked.connect(self.DeleteCustomer)

    def PopulateCustomerTable(self):
        cursor.execute("select * from Customer")
        self.customerTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.customerTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.customerTable.setItem(row_index, col_index, item)

    def AddCustomer(self):
        name = self.customerName.text()
        gender = self.customerGender.currentText()
        contact = self.customerContact.text()
        backupContact = self.customerBackup.text()
        email = self.customerEmail.text()
        address = self.customerAddress.text()
        self.msg = QtWidgets.QMessageBox()
        if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter complete information.")
        else:
            sql_query = "insert into Customer values(?, ?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (name, gender, contact, backupContact, email, address))
            connection.commit()
            self.msg.setWindowTitle("Success")
            self.msg.setText("Customer added successfully.")
            self.PopulateCustomerTable()
        self.msg.show()

    def SearchCustomer(self):
        criteria = self.searchCustomerCriteria.currentText()
        if criteria == "Customer Name":
            criteria = "customerName"
        elif criteria == "Contact Number":
            criteria = "contactNumber"
        elif criteria == "Email":
            criteria = "email"
        value = self.searchCustomerValue.text()
        if not value:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter a search value.")
            self.msg.show()
            return

        sql_query = f"select * from Customer where {criteria} like ?"
        cursor.execute(sql_query, ('%' + value + '%',))

        rows = cursor.fetchall()

        if not rows:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("No Results")
            self.msg.setText("No results found for the given search criteria.")
            self.msg.show()
            self.PopulateCustomerTable()
            return

        self.customerTable.setRowCount(0)

        for row_index, row_data in enumerate(rows):
            self.customerTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.customerTable.setItem(row_index, col_index, item)

    def EditCustomer(self):
        selected_items = self.customerTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to edit.")
            self.msg.show()
            return

        selected_row = selected_items[0].row()
        customer_data = [self.customerTable.item(selected_row, col_index).text() for col_index in range(self.customerTable.columnCount())]

        self.editCustomer = EditCustomerClass.EditCustomerScreen(customer_data)
        self.editCustomer.customerUpdated.connect(self.PopulateCustomerTable)
        self.editCustomer.show()

    def DeleteCustomer(self):
        selected_items = self.customerTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to delete.")
            self.msg.show()
            return

        selected_row = selected_items[0].row()
        customer_id = int(self.customerTable.item(selected_row, 0).text())

        sql_query = "delete from Customer WHERE customerID = ?"
        cursor.execute(sql_query, (customer_id))
        connection.commit()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Success")
        self.msg.setText("Customer deleted successfully.")
        self.msg.show()

        self.PopulateCustomerTable()  # Update the vendorTable after deletion



