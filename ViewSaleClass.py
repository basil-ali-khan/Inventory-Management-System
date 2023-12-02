# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
server = 'LAPTOP-MNMD5RBU'
database = 'Inventory_Management_System_Script'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

class ViewSaleScreen(QtWidgets.QMainWindow):
    def __init__(self, sale_id, sale_date, total_amount, customer_name):
        super(ViewSaleScreen, self).__init__() 
        uic.loadUi("Screens/ViewSale.ui", self)

        self.ProductTable.itemSelectionChanged.connect(self.get_selected_Product_data)
        self.saveSaleButton.clicked.connect(self.SaveEdit)
        self.cancelSaleButton.clicked.connect(self.CancelEdit)

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

        cursor.execute("SELECT Products.ProductName, Products.quanityProduced, SaleProduct.soldprice FROM Sale JOIN SaleProduct ON Sale.saleID = SaleProduct.saleID JOIN Products ON SaleProduct.ProductID = Products.ProductID WHERE Sale.saleID = ?", (sale_id,))
        self.ProductTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ProductTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ProductTable.setItem(row_index, col_index, item)

    def get_selected_Product_data(self):

        selected_row = self.ProductTable.currentRow()
        ProductName = self.ProductTable.item(selected_row, 0).text()
        Quantity = self.ProductTable.item(selected_row, 1).text()
        Price = self.ProductTable.item(selected_row, 2).text()

        self.ProductName.setText(ProductName)
        self.Quantity.setText(Quantity)
        self.Price.setText(Price)

    def CancelEdit(self):
        self.close()

    def SaveEdit(self):

        SaleId = self.viewSaleId.text()
        Quantity = self.Quantity.text()
        Price = self.Price.text()
        selected_row = self.ProductTable.currentRow()
        OldQuantity = self.ProductTable.item(selected_row, 1).text()
        cursor.execute(""" SELECT products.productID FROM products JOIN saleProduct ON products.productID = saleProduct.productID """)
        ProductID = cursor.fetchone()[0]  # Assuming ProductID is the first column

        sql_query = """
                    UPDATE products
                    SET quanityProduced = quanityProduced + (?)
                    WHERE productID = (?)
                    """

        # Correcting the way parameters are passed
        cursor.execute(sql_query, (OldQuantity, ProductID))
        connection.commit()

        cursor.execute(" select quanityProduced from products join saleProduct on products.productID = saleProduct.productID where saleProduct.saleID = ?", (SaleId,))
        availableQuantity = cursor.fetchone()

        if int(availableQuantity.quanityProduced) >= int(Quantity):

            sql_query = """
                        update SaleProduct
                        set quantity = (?), soldPrice = (?)
                        WHERE SaleId = (?)
                        """
            
            cursor.execute(sql_query, Quantity, Price, SaleId)
            connection.commit()
            
            sql_query = """
                        UPDATE products
                        SET quanityProduced = quanityProduced - (?)
                        WHERE productID = (?)
                        """
            cursor.execute(sql_query, (Quantity, ProductID))
            connection.commit() 

            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Success')
            self.msg.setText('Product edit successful')
            self.msg.show()
            self.close()

        else:

            sql_query = """
            UPDATE products
            SET quanityProduced = quanityProduced - (?)
            WHERE productID = (?)
            """
            cursor.execute(sql_query, (OldQuantity, ProductID))
            connection.commit()

            error_message = "Error: Required Quantity Is Not In Stock!."
            QMessageBox.critical(self, "Error", error_message)