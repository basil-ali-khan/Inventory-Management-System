# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditCustomerClass

from ConnectionString import connection, cursor

class CustomerHistoryScreen(QtWidgets.QMainWindow):
    def __init__(self, customer_id, customer_name, gender, contact, backup_contact, email, address):
        # Call the inherited classes __init__ method
        super(CustomerHistoryScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/CustomerHistory.ui', self)
        self.setWindowTitle("Customer History")

        self.customer_id = customer_id
        self.customer_name = customer_name
        self.contact = contact
        self.backup_contact = backup_contact
        self.email = email
        self.address = address
        self.gender = gender

        self.customerName.setText(customer_name)
        self.customerContact.setText(contact)
        self.customerBackup.setText(backup_contact)
        self.customerEmail.setText(email)
        self.customerAddress.setText(address)
        self.customerGender.setCurrentText(gender)
        self.openSaleButton.clicked.connect(self.ShowSaleDetails)
        self.clearButton.clicked.connect(self.ClearTable)

        self.setWindowTitle(f"Customer History - {customer_name}")

        self.PopulateSaleSummaryTable()

    def ClearTable(self):
        self.saleProductTable.setRowCount(0)

        
    def ShowSaleDetails(self):
        selected_items = self.saleSummaryTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to view details.")
            self.msg.show()
            return
        
        selected_row = selected_items[0].row()
        sale_id = int(self.saleSummaryTable.item(selected_row, 0).text())

        sql_query = """
                    select productName, [description], quantity, soldPrice, discount from SaleProduct 
                    inner join Products on SaleProduct.productID = Products.productID 
                    where saleID = ?
                    """
        cursor.execute(sql_query, (sale_id,))

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.saleProductTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.saleProductTable.setItem(row_index, col_index, item)
        self.saleProductTable.resizeColumnsToContents()


    def PopulateSaleSummaryTable(self):
        sql_query = """
                    select saleID, totalAmount, saleDate,username from Sale inner join customer on Sale.customerID = Customer.customerID 
                    inner join [User] on [User].userID = Sale.userID where Sale.customerID = ?
                    """
        cursor.execute(sql_query, self.customer_id)
        self.saleSummaryTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.saleSummaryTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.saleSummaryTable.setItem(row_index, col_index, item)