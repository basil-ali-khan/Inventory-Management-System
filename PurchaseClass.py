# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from AddPurchaseClass import AddPurchaseScreen
from ViewPurchaseClass import ViewPurchaseScreen

from ConnectionString import connection, cursor


class PurchaseScreen(QtWidgets.QMainWindow):   

    def __init__(self):
        
        super(PurchaseScreen, self).__init__() 
        uic.loadUi('Screens/Purchase.ui', self)

        self.PopulatePurchaseTable()        
        self.viewPurchaseButton.clicked.connect(self.ViewPurchase)
        self.addPurchaseButton.clicked.connect(self.AddPurchase)
        self.deletePurchaseButton.clicked.connect(self.DeletePurchase)
        self.searchPurchaseButton.clicked.connect(self.SearchPurchase)

    def PopulatePurchaseTable(self):

        cursor.execute("select purchase.purchaseID, Purchase.purchaseDate, Purchase.totalAmount, vendor.vendorName from purchase join Vendor on purchase.vendorID = Vendor.vendorID")
        self.purchaseTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseTable.setItem(row_index, col_index, item)

    def ViewPurchase(self):
            
        selected_row = self.purchaseTable.currentRow()

        purchase_id = str(self.purchaseTable.item(selected_row, 0).text())
        purchase_date = str(self.purchaseTable.item(selected_row, 1).text())
        total_amount = int(self.purchaseTable.item(selected_row, 2).text()) 
        vendor_name = str(self.purchaseTable.item(selected_row, 3).text())

        self.viewPurchase = ViewPurchaseScreen(purchase_id, purchase_date, total_amount, vendor_name)
        self.viewPurchase.show()
            
    def AddPurchase(self):
        self.addPurchase = AddPurchaseScreen()
        self.addPurchase.show()

    def DeletePurchase(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Are you sure you want to delete this purchase?")
        msgBox.setWindowTitle("Confirmation Box")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)

        returnValue = msgBox.exec()

        if returnValue == QtWidgets.QMessageBox.StandardButton.Ok:
            selected_row = self.purchaseTable.currentRow()

            self.purchaseTable.removeRow(selected_row)

            # purchase_id = self.purchaseTable.item(selected_row, 0).text()
            
            # # Delete the data from the SQL database
            # cursor.execute(f"DELETE FROM Purchase WHERE PurchaseID = ?", purchase_id)
            # connection.commit()

    def SearchPurchase(self):
        purchaseId = self.searchPurchaseId.text()
        vendorName = self.searchVendorName.text()
        fromDate = self.searchFromDate.date().toString("yyyy-MM-dd")
        toDate = self.searchToDate.date().toString("yyyy-MM-dd")

        query = """
        select purchase.purchaseID, Purchase.purchaseDate, Purchase.totalAmount, vendor.vendorName from purchase join Vendor on purchase.vendorID = Vendor.vendorID
        WHERE """
        if purchaseId == "" and vendorName == "" and fromDate == "2000-01-01" and toDate == "2000-01-01":
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('Please select a search criteria and/or enter search value')

        elif purchaseId == "" and vendorName == "":
            query += """ (Purchase.purchaseDate BETWEEN ? AND ?) """ 
            cursor.execute(query, (fromDate, toDate))
            self.purchaseTable.setRowCount(0)

        elif purchaseId == "" and fromDate == "2000-01-01" and toDate == "2000-01-01":
            query += """ vendor.vendorName like (?) """
            cursor.execute(query, ('%' + vendorName + '%'))
            self.purchaseTable.setRowCount(0)

        elif vendorName == "" and fromDate == "2000-01-01" and toDate == "2000-01-01":
            query += """ purchase.purchaseID = ? """
            cursor.execute(query, (purchaseId))
            self.purchaseTable.setRowCount(0)

        elif fromDate == "2000-01-01" and toDate == "2000-01-01":
            query += """ purchase.purchaseID = ? AND vendor.vendorName like (?) """
            cursor.execute(query, (purchaseId, ('%' + vendorName + '%')))
            self.purchaseTable.setRowCount(0)

        elif vendorName == "":
            query += """ purchase.purchaseID = ? AND (Purchase.purchaseDate BETWEEN ? AND ?) """
            cursor.execute(query, (purchaseId, fromDate, toDate))
            self.purchaseTable.setRowCount(0)        

        elif purchaseId == "":
            query += """ vendor.vendorName like (?) AND (Purchase.purchaseDate BETWEEN ? AND ?) """
            cursor.execute(query, (('%' + vendorName + '%'), fromDate, toDate))
            self.purchaseTable.setRowCount(0)

        elif purchaseId == "" and vendorName == "" and fromDate == toDate:
            query += """ Purchase.purchaseDate = ?) """
            cursor.execute(query, (toDate))
            self.purchaseTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseTable.setItem(row_index, col_index, item)