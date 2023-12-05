import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from ConnectionString import connection, cursor


class EditVendorScreen(QtWidgets.QMainWindow):
    vendorUpdated = QtCore.pyqtSignal()
    def __init__(self, vendor_data):
        super(EditVendorScreen, self).__init__()
        uic.loadUi('Screens/EditVendors.ui', self)
        self.setWindowTitle("Edit Vendor")

        # Assuming your UI file has QLineEdit widgets named vendorNameEdit, contactNumberEdit, emailEdit, addressEdit
        self.nameText.setText(vendor_data[1])
        self.contactText.setText(vendor_data[2])
        self.backupText.setText(vendor_data[3])
        self.emailText.setText(vendor_data[4])
        self.addressText.setText(vendor_data[5])

        # Save vendor_data as an instance variable
        self.vendor_data = vendor_data

        self.resetButton.clicked.connect(self.ResetEntries)
        self.saveButton.clicked.connect(self.SaveChanges)

    def ResetEntries(self):
        # Reset the text of the QLineEdit widgets to an empty string
        self.nameText.clear()
        self.contactText.clear()
        self.backupText.clear()
        self.emailText.clear()
        self.addressText.clear()

    def SaveChanges(self):
        # Get the updated information from the QLineEdit widgets
        updated_name = self.nameText.text()
        updated_contact = self.contactText.text()
        updated_backup = self.backupText.text()
        updated_email = self.emailText.text()
        updated_address = self.addressText.text()

        # Assuming vendor_id is the first element in vendor_data
        vendor_id = self.vendor_data[0]

        self.msg = QtWidgets.QMessageBox()
        if updated_name == '' or updated_contact == '' or updated_backup == '' or updated_email == '' or updated_address == '':
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter complete information.")
            self.msg.show()
        elif not updated_backup.isdigit() or not updated_contact.isdigit():
            self.msg.setWindowTitle("Error")
            self.msg.setText("Contact and Backup contact should be numeric")
            self.msg.show()
        else:
        # Run SQL query to update records in the database
            update_query = "UPDATE Vendor SET vendorName=?, contactNumber=?, backupContact=?, email=?, address=? WHERE vendorID=?"
            cursor.execute(update_query, (updated_name, updated_contact, updated_backup, updated_email, updated_address, vendor_id))
            connection.commit()

            # Optionally, show a success message
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Success")
            self.msg.setText("Vendor information updated successfully.")
            self.msg.show()

            # Emit the signal indicating that the vendor has been updated
            self.vendorUpdated.emit()

