# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from AddPurchaseClass import AddPurchaseScreen
from ViewEditPurchaseClass import ViewEditPurchaseScreen
from PurchaseReportClass import PurchaseReportScreen

# # server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
# database = 'Inventory_Management_System'  # Name of your Northwind database
# use_windows_authentication = True  # Set to True to use Windows Authentication
# username = 'your_username'  # Specify a username if not using Windows Authentication
# password = 'your_password'  # Specify a password if not using Windows Authentication

# if use_windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# connection = pyodbc.connect(connection_string)
# cursor = connection.cursor()

from ConnectionString import connection, cursor

class PurchaseScreen(QtWidgets.QMainWindow):   

    def __init__(self):
        
        super(PurchaseScreen, self).__init__() 
        uic.loadUi('Screens/Purchase.ui', self)
        self.setWindowTitle("Purchase")

        self.PopulatePurchaseTable()        
        self.viewPurchaseButton.clicked.connect(self.ViewPurchase)
        self.addPurchaseButton.clicked.connect(self.AddPurchase)
        self.deletePurchaseButton.clicked.connect(self.DeletePurchase)
        self.searchPurchaseButton.clicked.connect(self.SearchPurchase)
        self.reportsButton.clicked.connect(self.ReportPurchase)
    
    def ReportPurchase(self):
        self.reportPurchase = PurchaseReportScreen()
        self.reportPurchase.show()

    def PopulatePurchaseTable(self):

        cursor.execute("select purchase.purchaseID, Purchase.purchaseDate, Purchase.totalAmount, vendor.vendorName from purchase join Vendor on purchase.vendorID = Vendor.vendorID")
        self.purchaseTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseTable.setItem(row_index, col_index, item)

    def ViewPurchase(self):
            
        # selected_row = self.purchaseTable.currentRow()

        selected_items = self.purchaseTable.selectedItems ()
        if not selected_items:
            self.msg = QtWidgets. QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText ("Please select an entry to view.")
            self.msg.show()
            return
            
        selected_row = self.purchaseTable.currentRow()
        purchase_id = str(self.purchaseTable.item(selected_row, 0).text())
        purchase_date = str(self.purchaseTable.item(selected_row, 1).text())
        total_amount = int(self.purchaseTable.item(selected_row, 2).text()) 
        vendor_name = str(self.purchaseTable.item(selected_row, 3).text())

        self.viewEditPurchase = ViewEditPurchaseScreen(purchase_id, purchase_date, total_amount, vendor_name)
        self.viewEditPurchase.editDone.connect(self.PopulatePurchaseTable)
        self.viewEditPurchase.show()
            
    def AddPurchase(self):
        self.addPurchase = AddPurchaseScreen()
        # self.addPurchase.addPurchaseButton.connect(self.PopulatePurchaseTable)
        self.addPurchase.show()

    def DeletePurchase(self):

        selected_items = self.purchaseTable.selectedItems ()
        if not selected_items:
            self.msg = QtWidgets. QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText ("Please select an entry to delete.")
            self.msg.show()
            return
        
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Are you sure you want to delete this purchase?")
        msgBox.setWindowTitle("Confirmation Box")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)

        returnValue = msgBox.exec()

        if returnValue == QtWidgets.QMessageBox.StandardButton.Ok:
        
            selected_row = selected_items[0].row()
            purchase_id = int(self.purchaseTable.item(selected_row, 0). text())
            cursor.execute("select * from PurchaseMaterial where purchaseID = ?", (purchase_id,))
            
            for row in cursor.fetchall():
                material_id = row[1]
                quantity = row[2]
                cursor.execute ("update Material set units = units - (?) where materialID = ?", (quantity, material_id,))
                cursor.execute ("update Material set units = (?) where materialID = ? and units < 0", (0, material_id,))

            cursor.execute("delete from PurchaseMaterial WHERE purchaseID = ?", (purchase_id,))
            cursor.execute("delete from Purchase WHERE purchaseID = ?", (purchase_id,))
            connection.commit ()

            self.msg = QtWidgets.QMessageBox()
            self.msg. setWindowTitle ("Success")
            self.msg.setText ("Purchase deleted successfully.")
            self.msg.show()
            self.PopulatePurchaseTable()

    def SearchPurchase(self):
        purchaseId = self.searchPurchaseId.text()
        vendorName = self.searchVendorName.text()
        fromDate = self.searchFromDate.date().toString("yyyy-MM-dd")
        toDate = self.searchToDate.date().toString("yyyy-MM-dd")

        query = """
        SELECT purchase.purchaseID, Purchase.purchaseDate, Purchase.totalAmount, vendor.vendorName 
        FROM purchase 
        JOIN Vendor ON purchase.vendorID = Vendor.vendorID
        WHERE 1 = 1
        """

        params = []

        if purchaseId:
            if purchaseId.isdigit():
                query += " AND purchase.purchaseID = ? "
                params.append(purchaseId)

            else:
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle('Error')
                self.msg.setText('Purchase ID should be numeric')

                self.msg.show()

        if vendorName:
            query += " AND vendor.vendorName LIKE ? "
            params.append('%' + vendorName + '%')

        if fromDate != "2000-01-01" and toDate != "2000-01-01":
            query += " AND Purchase.purchaseDate BETWEEN ? AND ? "
            params.extend([fromDate, toDate])

        cursor.execute(query, params)

        self.purchaseTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseTable.setItem(row_index, col_index, item)