import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc


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

class EditCustomerScreen(QtWidgets.QMainWindow):
    customerUpdated = QtCore.pyqtSignal()
    def __init__(self, customer_data):
        super(EditCustomerScreen, self).__init__()
        uic.loadUi('Screens/EditCustomer.ui', self)

        # Assuming your UI file has QLineEdit widgets named vendorNameEdit, contactNumberEdit, emailEdit, addressEdit
        self.nameText.setText(customer_data[1])
        self.contactText.setText(customer_data[3])
        self.backupText.setText(customer_data[4])
        self.emailText.setText(customer_data[5])
        self.addressText.setText(customer_data[6])
        gender_index = self.genderComboBox.findText(customer_data[2])
        if gender_index != -1:
            self.genderComboBox.setCurrentIndex(gender_index)

        # Save customer_data as an instance variable
        self.customer_data = customer_data

        self.clearButton.clicked.connect(self.ClearEntries)
        self.saveButton.clicked.connect(self.SaveChanges)

    def ClearEntries(self):
        # Reset the text of the QLineEdit widgets to an empty string
        self.nameText.clear()
        self.contactText.clear()
        self.backupText.clear()
        self.emailText.clear()
        self.addressText.clear()

    def SaveChanges(self):
        # Get the updated information from the QLineEdit widgets
        updated_name = self.nameText.text()
        updated_gender = self.genderComboBox.currentText()
        updated_contact = self.contactText.text()
        updated_backup = self.backupText.text()
        updated_email = self.emailText.text()
        updated_address = self.addressText.text()

        # Assuming vendor_id is the first element in vendor_data
        customer_id = self.customer_data[0]

        self.msg = QtWidgets.QMessageBox()
        if updated_name == '' or updated_contact == '' or updated_backup == '' or updated_email == '' or updated_address == '':
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter complete information.")
            self.msg.show()
        else:
        # Run SQL query to update records in the database
            update_query = "UPDATE Customer SET customerName=?, gender=?, contactNumber=?, backupContact=?, email=?, address=? WHERE customerID=?"
            cursor.execute(update_query, (updated_name, updated_gender ,updated_contact, updated_backup, updated_email, updated_address, customer_id))
            connection.commit()

            # Optionally, show a success message
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Success")
            self.msg.setText("Customer information updated successfully.")
            self.msg.show()

            # Emit the signal indicating that the vendor has been updated
            self.customerUpdated.emit()

