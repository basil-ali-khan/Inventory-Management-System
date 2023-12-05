import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from EditProductClass import EditProductScreen

from ConnectionString import connection, cursor

class ProductScreen(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(ProductScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/Products.ui', self)

        self.PopulateProductTable()
        self.setWindowTitle("Products")

        self.addProductButton.clicked.connect(self.AddProduct)

        self.searchProductButton.clicked.connect(self.SearchProduct)

        self.clearProductButton.clicked.connect(self.ClearProduct)

        # self.refreshButton.clicked.connect(self.PopulateProductTable)

        self.deleteProductButton.clicked.connect(self.DeleteProduct)

        # self.productTable.itemClicked.connect(self.EditProduct)
        # self.editProductButton.clicked.connect(self.OpenProductToEdit(id, self.name, self.qtyProduced, self.currentPrice, self.categoryName, self.desc))

        self.editProductButton.clicked.connect(self.EditProduct)
    # row = id = name = desc = currentPrice = qtyProduced = categoryName = None

    def EditProduct(self):
        # row = product.row()
        
        selected_items = self.productTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to edit.")
            self.msg.show()
            return
        
        row = self.productTable.currentRow()

        id = self.productTable.item(row, 0).text()
        name = self.productTable.item(row, 1).text()        
        desc = self.productTable.item(row, 2).text()
        currentPrice = self.productTable.item(row, 3).text()
        qtyProduced = self.productTable.item(row, 4).text()
        categoryName = self.productTable.item(row, 6).text()

        self.editProductScreen = EditProductScreen(id, name, qtyProduced, currentPrice, categoryName, desc)
        self.editProductScreen.productUpdated.connect(self.PopulateProductTable)
        self.editProductScreen.show()
        
        
    def ClearProduct(self):
        self.productNameBox.setText('')
        self.productQuantityBox.setText('')
        self.unitPriceBox.setText('')
        self.productCategoryBox.setCurrentText('Men')
        self.productDescBox.setText('')


    def PopulateProductTable(self):
        cursor.execute('select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID')
        self.productTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.productTable.insertRow(row_index)
            
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.productTable.setItem(row_index, col_index, item)

    def AddProduct(self):
        # ID = self.productIdBox.text()
        name = self.productNameBox.text()
        quantityProduced = self.productQuantityBox.text()
        quantitySold = 0
        price = self.unitPriceBox.text()
        category = self.productCategoryBox.currentText()
        desc = self.productDescBox.toPlainText()

        sql_query = 'select categoryID from Category where categoryName = (?)'
        cursor.execute(sql_query, (category,))
        categoryID = cursor.fetchone()
        categoryID = categoryID[0] if categoryID else None

        self.msg = QtWidgets.QMessageBox()

        if name == '' or quantityProduced == '' or price == '' or category == '' or desc == '':
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter complete information.")   

        elif not quantityProduced.isdigit() or not price.isdigit():
            self.msg.setWindowTitle("Error")
            self.msg.setText("Price and quantity produced should be numeric")   

        else:
            sql_query = 'insert into Products([productName], [description], price, quantityProduced, quantitySold, categoryID) values(?, ?, ?, ?, ?, ?)'
            cursor.execute(sql_query, (name, desc, price, quantityProduced, quantitySold, categoryID))
            connection.commit()
            self.msg.setWindowTitle("Success")
            self.msg.setText("Product added successfully.")
            

        self.msg.show()
        self.PopulateProductTable()


    def SearchProduct(self):
        criteria = self.searchProductCriteria.currentText().strip()
        criteriaValue = self.searchProductValue.text().strip()


        if (criteria != '' and criteriaValue != ''):        
            # print('criteria: ', criteria)

            if criteria == 'Product Name':
                sql_query = 'select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID where productName like (?)'
                cursor.execute(sql_query, ('%' + criteriaValue + '%',))
            elif criteria == 'Quantity Produced':
                sql_query = 'select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID where quantityProduced = (?)'
                cursor.execute(sql_query, (criteriaValue,))
            elif criteria == 'Quantity Sold':
                sql_query = 'select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID where quantitySold = (?)'
                cursor.execute(sql_query, (criteriaValue,))
            elif criteria == 'Quantity Available':
                sql_query = "select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID  where quantityProduced - quantitySold = (?)"
                cursor.execute(sql_query, (criteriaValue,))
            elif criteria == 'Category Name':
                sql_query = 'select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID where categoryName = (?)'
                cursor.execute(sql_query, ('%' + criteriaValue + '%',))
            elif criteria == 'Price':
                sql_query = 'select productID, productName, [description], price, quantityProduced, quantitySold, categoryName from Products inner join Category on products.categoryID = Category.categoryID where price = (?)'
                cursor.execute(sql_query, (criteriaValue,))
            # cursor.execute(sql_query, ('%' + criteriaValue + '%',))

            print('Query executed')

            self.productTable.clearContents()
            self.productTable.setRowCount(0)

            rows = cursor.fetchall()

            if not rows:
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle("No Results")
                self.msg.setText("No results found for the given search criteria.")
                self.msg.show()
                # self.PopulateProductTable()
                return

            for row_index, row_data in enumerate(rows):
                print('populating row')
                self.productTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    print('Adding item to product table.')
                    self.productTable.setItem(row_index, col_index, item)

        else:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('Please select search criteria and/or enter search value')
            self.msg.show()


    def DeleteProduct(self):
        selected_items = self.productTable.selectedItems()

        if not selected_items:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select an entry to delete.")
            self.msg.show()
            return

        # Assuming the first column contains a unique identifier (e.g., product_id)
        selected_row = selected_items[0].row()
        product_id = int(self.productTable.item(selected_row, 0).text())

        # Code block to check if the productID exists as foreign key in other tables. If yes, then product cannot be deleted
        check_in_saleproduct = "SELECT COUNT(*) FROM SaleProduct WHERE productID = ?"
        cursor.execute(check_in_saleproduct, (product_id,))
        result1 = cursor.fetchone()

        check_in_productsmanufactured = "SELECT COUNT(*) FROM ProductsManufactured WHERE productID = ?"
        cursor.execute(check_in_productsmanufactured, (product_id,))
        result2 = cursor.fetchone()

        if (result1 or result2) and (result1[0] > 0 or result2[0] > 0):
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle("Error")
                self.msg.setText("Cannot delete product with existing records in database.")
                self.msg.show()
                return

        sql_query = "delete from Products WHERE productID = ?"
        cursor.execute(sql_query, (product_id,))
        connection.commit()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Success")
        self.msg.setText("Product deleted successfully.")
        self.msg.show()

        self.PopulateProductTable()

    