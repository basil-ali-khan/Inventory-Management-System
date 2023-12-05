# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from math import ceil, floor

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

class ViewEditSaleScreen(QtWidgets.QMainWindow):
    editDone = QtCore.pyqtSignal()
    def __init__(self, sale_id, sale_date, total_amount, customer_name):
        super(ViewEditSaleScreen, self).__init__() 
        uic.loadUi("Screens/ViewEditSale.ui", self)
        self.setWindowTitle("View/Edit Sale")

        self.ProductTable.itemSelectionChanged.connect(self.get_selected_Product_data)
        self.saveSaleButton.clicked.connect(self.SaveEdit)
        self.DoneSaleButton.clicked.connect(self.DoneEdit)

        self.sale_id = int(sale_id)
        self.sale_date = QDate.fromString(str(sale_date), 'yyyy-MM-dd')
        self.total_amount = int(total_amount)
        self.customer_name = str(customer_name)

        self.viewSaleId.setText(str(self.sale_id))
        self.viewSaleId.setDisabled(True)

        self.viewSaleDate.setDate(self.sale_date)
        self.viewSaleDate.setDisabled(True)

        self.viewTotalAmount.setText(str(self.total_amount))
        self.viewTotalAmount.setDisabled(True)

        self.viewCustomerName.setText(str(self.customer_name))
        self.viewCustomerName.setDisabled(True)

        cursor.execute("SELECT Products.ProductID, Products.ProductName, SaleProduct.Quantity, SaleProduct.soldprice, SaleProduct.Quantity*SaleProduct.soldprice, SaleProduct.Discount FROM Sale JOIN SaleProduct ON Sale.saleID = SaleProduct.saleID JOIN Products ON SaleProduct.ProductID = Products.ProductID WHERE Sale.saleID = ?", (sale_id,))
        self.ProductTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ProductTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ProductTable.setItem(row_index, col_index, item)

    def get_selected_Product_data(self):

        selected_row = self.ProductTable.currentRow()
        ProductID = self.ProductTable.item(selected_row, 0).text()
        ProductName = self.ProductTable.item(selected_row, 1).text()
        Quantity = self.ProductTable.item(selected_row, 2).text()
        UnitCost = self.ProductTable.item(selected_row, 3).text()
        Discount = self.ProductTable.item(selected_row, 5).text()
        
        self.ProductID.setText(ProductID)
        self.ProductName.setText(ProductName)
        self.Quantity.setText(Quantity)
        self.UnitCost.setText(UnitCost)
        self.editedDiscount.setText(Discount)

    def DoneEdit(self):
        self.editDone.emit()
        self.close()

    def UpdateTotal(self):
        total = 0.0
        for i in range(self.ProductTable.rowCount()):
            temp = float(self.ProductTable.item(i, 3).text()) * float(self.ProductTable.item(i, 2).text()) * (1 - float(self.ProductTable.item(i, 5).text()))
            total += temp
        self.viewTotalAmount.setText(str(round(total, 2)))

        sql_query = """
                    UPDATE Sale
                    set totalAmount = (?)
                    where saleID = (?)
                    """
        cursor.execute(sql_query, (round(total, 2),self.sale_id,))
        connection.commit()
    

    def SaveEdit(self):

        SaleId = self.viewSaleId.text()

        selected_row = self.ProductTable.currentRow()
        
        ProductID = self.ProductID.text()
        OldQuantity = self.ProductTable.item(selected_row, 2).text()
        sql_query = """ 
                    update products set quantityProduced = quantityProduced + (?), quantitySold = quantitySold - (?) where productID = (?)
                    """
        cursor.execute(sql_query, (OldQuantity, OldQuantity, ProductID,))
        connection.commit()
        Quantity = self.Quantity.text()
        UnitCost = self.UnitCost.text()
        discount = self.editedDiscount.text()
        try:
            if int(discount) < 0 or int(discount) > 1:
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle('Error')
                self.msg.setText('Discount should be between 0 and 1')
                self.msg.show()
                return
        except ValueError:
            if float(discount) < 0 or float(discount) > 1:
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle('Error')
                self.msg.setText('Discount should be between 0 and 1')
                self.msg.show()
                return
        if not Quantity.isdigit() or not UnitCost.replace('.', '', 1).isdigit() or not discount.replace('.', '', 1).isdigit():
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('No edits made. Incorrect Values entered')
            self.msg.show()
            return
        total = int(Quantity) * float(UnitCost) * (1- float(discount))

        # self.ProductTable.item(selected_row, 2).setText(str(Quantity))
        # self.ProductTable.item(selected_row, 3).setText(str(UnitCost))
        # self.ProductTable.item(selected_row, 4).setText(str(total))
        # self.ProductTable.item(selected_row, 5).setText(str(discount))

        sql_query = """ select quantityProduced - quantitySold from products where productID = (?) """
        cursor.execute(sql_query, (ProductID,))
        newAvailableQuantity = cursor.fetchone()[0]

        # quantityProducedDiff = int(Quantity) - int(OldQuantity)
        # quantitySoldDiff = -1 * quantityProducedDiff       

        # cursor.execute(" select quantityProduced, quantitySold from Products where ProductID = ? ", (ProductID,))
        # result = cursor.fetchone()
        # currentProducedQuantity= result[0]
        # currentSoldQuantity = result[1]


        # newProducedQuantity = currentProducedQuantity + quantityProducedDiff
        # newSoldQuantity = currentSoldQuantity - quantitySoldDiff
        # newAvailableQuantity = newProducedQuantity - newSoldQuantity

        if int(Quantity) > int(newAvailableQuantity):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('Quantity exceeds available quantity')
            self.msg.show()
            return
        
        self.ProductTable.item(selected_row, 2).setText(str(Quantity))
        self.ProductTable.item(selected_row, 3).setText(str(UnitCost))
        self.ProductTable.item(selected_row, 4).setText(str(total))
        self.ProductTable.item(selected_row, 5).setText(str(discount))
        
        self.UpdateTotal()

        # sql_query = """
        #             UPDATE products
        #             SET quantityProduced = (?), quantitySold =  (?)
        #             WHERE productID = (?)
        #             """
        # cursor.execute(sql_query, (newProducedQuantity, newSoldQuantity, ProductID))
        # connection.commit()

        # cursor.execute(" select quantityProduced from Products where ProductID = ? ", (ProductID,))
        # availableQuantity = cursor.fetchone()[0]

        # if int(Quantity) > int(availableQuantity):
        #     self.msg = QtWidgets.QMessageBox()
        #     self.msg.setWindowTitle('Error')
        #     self.msg.setText('Quantity exceeds available quantity')
        #     self.msg.show()
        #     return

        sql_query = """
                    UPDATE SaleProduct
                    SET quantity = (?), soldPrice = (?), discount = (?)
                    WHERE SaleId = (?) and ProductId = (?)
                    """
        cursor.execute(sql_query, (Quantity, UnitCost, discount, SaleId, ProductID))
        connection.commit()


        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('Success')
        self.msg.setText('Sale edit successful')
        self.msg.show()
        