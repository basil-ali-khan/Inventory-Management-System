# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from ViewSaleClass import ViewSaleScreen
from AddSaleClass import AddSaleScreen
import SaleReportClass

from ConnectionString import connection, cursor

class SaleScreen(QtWidgets.QMainWindow):   

    def __init__(self):
        
        super(SaleScreen, self).__init__() 
        uic.loadUi('Screens/Sale.ui', self)

        self.PopulateSaleTable()        
        self.viewSaleButton.clicked.connect(self.ViewSale)
        self.addSaleButton.clicked.connect(self.AddSale)
        self.deleteSaleButton.clicked.connect(self.DeleteSale)
        self.searchSaleButton.clicked.connect(self.SearchSale)
        self.reportSaleButton.clicked.connect(self.ReportSale)

    def PopulateSaleTable(self):

        cursor.execute("SELECT Sale.saleID, Sale.saleDate, Sale.totalAmount, Customer.customerName, Customer.contactNumber FROM Sale join Customer on sale.customerID = Customer.customerID")
        self.saleTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.saleTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.saleTable.setItem(row_index, col_index, item)

    def ViewSale(self):
            
        selected_row = self.saleTable.currentRow()

        sale_id = str(self.saleTable.item(selected_row, 0).text())
        sale_date = str(self.saleTable.item(selected_row, 1).text())
        total_amount = int(self.saleTable.item(selected_row, 2).text()) 
        customer_name= str(self.saleTable.item(selected_row, 3).text())

        self.viewSale = ViewSaleScreen(sale_id, sale_date, total_amount, customer_name)
        self.viewSale.show()
            
    def AddSale(self):
        self.addSale = AddSaleScreen()
        self.addSale.show()

    def DeleteSale(self):

        selected_items = self.saleTable.selectedItems ()
        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText ("Please select an entry to delete.")
            self.msg.show()
            return
        
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Are you sure you want to delete this sale?")
        msgBox.setWindowTitle("Confirmation Box")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)

        returnValue = msgBox.exec()

        if returnValue == QtWidgets.QMessageBox.StandardButton.Ok:
        
            selected_row = selected_items[0].row()
            sale_id = int(self.saleTable.item(selected_row, 0). text())
            cursor.execute("select * from SaleProduct where saleID = ?", (sale_id,))
            
            for row in cursor.fetchall():
                Product_id = row[1]
                quantity = row[2]
                cursor.execute ("update Product set units = units - (?) where ProductID = ?", (quantity, Product_id,))
                cursor.execute ("update Product set units = (?) where ProductID = ? and units < 0", (0, Product_id,))

            cursor.execute("delete from saleProduct WHERE saleID = ?", (sale_id,))
            cursor.execute("delete from sale WHERE saleID = ?", (sale_id,))
            connection.commit ()

            self.msg = QtWidgets.QMessageBox()
            self.msg. setWindowTitle ("Success")
            self.msg.setText ("sale deleted successfully.")
            self.msg.show()
            self.PopulatesaleTable()

    def SearchSale(self):
        saleID = self.searchSaleId.text() 
        customerName = self.searchCustomerName.text() 
        contactNumber = self.searchPhoneNumber.text()
        fromDate = self.searchFromDate.date().toString("yyyy-MM-dd") 
        toDate = self.searchToDate.date().toString("yyyy-MM-dd") 

        query = """
        SELECT Sale.saleID, Sale.saleDate, Sale.totalAmount, customer.customerName, customer.contactNumber 
        FROM Sale 
        JOIN Customer ON Sale.customerID = Customer.customerID
        WHERE 1 = 1
        """

        params = []

        if saleID:
            query += " AND Sale.saleID = ? "
            params.append(saleID)

        if customerName:
            query += " AND customer.customerName LIKE ? "
            params.append('%' + customerName + '%')

        if fromDate != "2000-01-01" and toDate != "2000-01-01":
            query += " AND Sale.SaleDate BETWEEN ? AND ? "
            params.extend([fromDate, toDate])

        if contactNumber:
            query += " AND customer.contactNumber LIKE ? "
            params.append('%' + contactNumber + '%')

        cursor.execute(query, params)

        self.saleTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.saleTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.saleTable.setItem(row_index, col_index, item)

    def ReportSale(self):
        self.reportSale = SaleReportClass.SaleReportScreen()
        self.reportSale.show()


            