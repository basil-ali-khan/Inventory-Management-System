# # Importing essential modules
# from PyQt6 import QtWidgets, uic
# from PyQt6.QtCore import QDate
# from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
# import sys
# import pyodbc
# import EditVendorClass
# import TopVendorsClass

# from ConnectionString import connection, cursor

# class VendorScreen(QtWidgets.QMainWindow):
#     def __init__(self):
#         # Call the inherited classes __init__ method
#         super(VendorScreen, self).__init__()

#         # Load the .ui file
#         uic.loadUi('Screens/Vendors.ui', self)

#         self.PopulateVendorTable()
#         self.searchVendorValue.setPlaceholderText("Search")
#         self.addVendorButton.clicked.connect(self.AddVendor)
#         self.editVendorButton.clicked.connect(self.EditVendor)
#         self.searchVendorButton.clicked.connect(self.SearchVendor)
#         self.deleteVendorButton.clicked.connect(self.DeleteVendor)
#         self.vendorHistoryButton.clicked.connect(self.OpenVendorHistoryScreen)
#         self.topVendorsButton.clicked.connect(self.OpenTopVendorsScreen)

#     def PopulateVendorTable(self):
#         cursor.execute("select * from vendor")
#         self.vendorTable.setRowCount(0)

#         for row_index, row_data in enumerate(cursor.fetchall()):
#             self.vendorTable.insertRow(row_index)
#             for col_index, cell_data in enumerate(row_data):
#                 item = QTableWidgetItem(str(cell_data))
#                 self.vendorTable.setItem(row_index, col_index, item)

#     def AddVendor(self):
#         name = self.vendorNameBox.text()
#         contact = self.vendorContactNumber.text()
#         backupContact = self.vendorBackupContact.text()
#         email = self.vendorEmail.text()
#         address = self.vendorAddress.text()
#         self.msg = QtWidgets.QMessageBox()
#         if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
#             self.msg.setWindowTitle("Error")
#             self.msg.setText("Please enter complete information.")
#         else:
#             sql_query = "insert into vendor values(?, ?, ?, ?, ?)"
#             cursor.execute(sql_query, (name, contact,
#                            backupContact, email, address))
#             connection.commit()
#             self.msg.setWindowTitle("Success")
#             self.msg.setText("Vendor added successfully.")
#             self.PopulateVendorTable()
#         self.msg.show()

#     def SearchVendor(self):
#         criteria = self.searchVendorCriteria.currentText()
#         if criteria == "Vendor Name":
#             criteria = "vendorName"
#         elif criteria == "Contact Number":
#             criteria = "contactNumber"
#         elif criteria == "Email":
#             criteria = "email"
#         value = self.searchVendorValue.text()
#         if not value:
#             self.msg = QtWidgets.QMessageBox()
#             self.msg.setWindowTitle("Error")
#             self.msg.setText("Please enter a search value.")
#             self.msg.show()
#             return

#         sql_query = f"select * from vendor where {criteria} like ?"
#         cursor.execute(sql_query, ('%' + value + '%',))

#         rows = cursor.fetchall()

#         if not rows:
#             self.msg = QtWidgets.QMessageBox()
#             self.msg.setWindowTitle("No Results")
#             self.msg.setText("No results found for the given search criteria.")
#             self.msg.show()
#             self.PopulateVendorTable()
#             return

#         self.vendorTable.setRowCount(0)

#         for row_index, row_data in enumerate(rows):
#             self.vendorTable.insertRow(row_index)
#             for col_index, cell_data in enumerate(row_data):
#                 item = QTableWidgetItem(str(cell_data))
#                 self.vendorTable.setItem(row_index, col_index, item)

#     def DeleteVendor(self):
#         selected_items = self.vendorTable.selectedItems()

#         if not selected_items:
#             self.msg = QtWidgets.QMessageBox()
#             self.msg.setWindowTitle("Error")
#             self.msg.setText("Please select an entry to delete.")
#             self.msg.show()
#             return

#         # Assuming the first column contains a unique identifier (e.g., vendor_id)
#         selected_row = selected_items[0].row()
#         vendor_id = int(self.vendorTable.item(selected_row, 0).text())

#         # Code block to check if the vendor has purchase history. If yes, then vendor cannot be deleted
#         sql_check_sales = "select count(*) from Purchase where vendorID = ?"
#         cursor.execute(sql_check_sales, (vendor_id,))
#         result = cursor.fetchone()

#         # Throw error message if customers has pre-existing sales record
#         if result and result[0] > 0:
#                 self.msg = QtWidgets.QMessageBox()
#                 self.msg.setWindowTitle("Error")
#                 self.msg.setText("Cannot delete vendor with existing purchase records.")
#                 self.msg.show()
#                 return

#         sql_query = "delete from vendor WHERE vendorID = ?"
#         cursor.execute(sql_query, (vendor_id))
#         connection.commit()

#         self.msg = QtWidgets.QMessageBox()
#         self.msg.setWindowTitle("Success")
#         self.msg.setText("Vendor deleted successfully.")
#         self.msg.show()

#         self.PopulateVendorTable()  # Update the vendorTable after deletion

#     def EditVendor(self):
#         selected_items = self.vendorTable.selectedItems()

#         if not selected_items:
#             self.msg = QtWidgets.QMessageBox()
#             self.msg.setWindowTitle("Error")
#             self.msg.setText("Please select an entry to edit.")
#             self.msg.show()
#             return

#         selected_row = selected_items[0].row()
#         vendor_data = [self.vendorTable.item(selected_row, col_index).text(
#         ) for col_index in range(self.vendorTable.columnCount())]

#         self.editVendor = EditVendorClass.EditVendorScreen(vendor_data)
#         self.editVendor.vendorUpdated.connect(self.PopulateVendorTable)
#         self.editVendor.show()

#     def OpenVendorHistoryScreen(self):
#         pass

#     def OpenTopVendorsScreen(self):
#         self.topVendors = TopVendorsClass.TopVendorScreen()
#         self.topVendors.show()

# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditVendorClass
from VendorHistoryClass import VendorHistoryScreen
from TopVendorsClass import TopVendorScreen

from ConnectionString import connection, cursor


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
        self.VendorHistoryButton.clicked.connect(self.OpenVendorHistoryScreen)
        self.topVendorsButton.clicked.connect(self.OpenTopVendorsScreen)

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
        elif not contact.isdigit() or not backupContact.isdigit():
            self.msg.setWindowTitle("Error")
            self.msg.setText("Contact and Backup contact should be numeric")
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

        # Throw error message if vendors has pre-existing sales record
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

    def OpenTopVendorsScreen(self):
        self.topvendors = TopVendorScreen()
        self.topvendors.show()
    
    def OpenVendorHistoryScreen(self):
        selected_items = self.vendorTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to view history.")
            self.msg.show()
            return

        selected_row = selected_items[0].row()
        vendor_id = int(self.vendorTable.item(selected_row, 0).text())
        vendor_name = self.vendorTable.item(selected_row, 1).text()
        contact = self.vendorTable.item(selected_row, 2).text()
        backup_contact = self.vendorTable.item(selected_row, 3).text()
        email = self.vendorTable.item(selected_row, 4).text()
        address = self.vendorTable.item(selected_row, 5).text()

        self.vendorHistory = VendorHistoryScreen(vendor_id, vendor_name, contact, backup_contact, email, address)
        self.vendorHistory.show()

        

