import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from ConnectionString import connection, cursor

class EditProductScreen(QtWidgets.QMainWindow):
    def __init__(self, id, name, qtyProduced, currentPrice, categoryName, desc):
        super(EditProductScreen, self).__init__()
        uic.loadUi("Screens/EditProducts.ui", self)

        # self.productId = id
        self.productIdBox.setText(id)
        self.productNameBox.setText(name)
        self.qtyProducedBox.setText(qtyProduced)
        self.priceBox.setText(currentPrice)
        self.categoryBox.setCurrentText(categoryName)
        self.productDesc.setText(desc)

        self.cancelButton.clicked.connect(self.CancelEdit)
        self.doneButton.clicked.connect(self.DoneEdit)

    def CancelEdit(self):
        self.close()

    def DoneEdit(self):
        id = self.productIdBox.text()
        newName = self.productNameBox.text()
        newQuantityProduced = self.qtyProducedBox.text()
        newPrice = self.priceBox.text()
        newCategory = self.categoryBox.currentText()
        newDesc = self.productDesc.toPlainText()

        cursor.execute('select categoryId from category where categoryName = (?)', (newCategory,))
        categoryID = cursor.fetchone()
        categoryID = categoryID[0] if categoryID else None

        sql_query = """
                    update products
                    set productName = (?), quantityProduced = (?), price = (?), 
                    categoryID = (?), description = (?)
                    where productID = (?)
                    """
        cursor.execute(sql_query, (newName, newQuantityProduced, newPrice, categoryID, newDesc, id))
        connection.commit()
        
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('Success')
        self.msg.setText('Product edit successful')

        self.msg.show()
