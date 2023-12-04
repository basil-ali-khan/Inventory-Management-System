# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditVendorClass

from ConnectionString import connection, cursor

class VendorHistoryScreen(QtWidgets.QMainWindow):
    def __init__(self, Vendor_id, Vendor_name, contact, backup_contact, email, address):
        # Call the inherited classes __init__ method
        super(VendorHistoryScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/VendorHistory.ui', self)

        self.Vendor_id = Vendor_id
        self.Vendor_name = Vendor_name
        self.contact = contact
        self.backup_contact = backup_contact
        self.email = email
        self.address = address

        self.vendorName.setText(Vendor_name)
        self.vendorContact.setText(contact)
        self.vendorBackup.setText(backup_contact)
        self.vendorEmail.setText(email)
        self.vendorAddress.setText(address)
        self.openPurchaseButton.clicked.connect(self.ShowPurchaseDetails)
        self.clearButton.clicked.connect(self.ClearTable)

        self.setWindowTitle(f"Vendor History - {Vendor_name}")

        self.PopulatePurchaseSummaryTable()

    def ClearTable(self):
        self.purchaseMaterialTable.setRowCount(0)

    def ShowPurchaseDetails(self):
        selected_items = self.purchaseSummaryTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to view details.")
            self.msg.show()
            return
        
        selected_row = selected_items[0].row()
        Purchase_id = int(self.purchaseSummaryTable.item(selected_row, 0).text())

        self.purchaseMaterialTable.setRowCount(0)

        sql_query = """
                    select Material.MaterialName, Material.description, PurchaseMaterial.quantity, PurchaseMaterial.cost from PurchaseMaterial 
                    inner join Material on PurchaseMaterial.MaterialID = Material.MaterialID 
                    where PurchaseID = ?
                    """
        cursor.execute(sql_query, (Purchase_id,))

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseMaterialTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseMaterialTable.setItem(row_index, col_index, item)
        self.purchaseMaterialTable.resizeColumnsToContents()


    def PopulatePurchaseSummaryTable(self):
        sql_query = """
                    select PurchaseID, totalAmount, PurchaseDate from Purchase where Purchase.VendorID = ?
                    """
        cursor.execute(sql_query, self.Vendor_id)
        self.purchaseSummaryTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseSummaryTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseSummaryTable.setItem(row_index, col_index, item)