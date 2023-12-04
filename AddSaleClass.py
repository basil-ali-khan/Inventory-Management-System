# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QAbstractItemView
import sys
import pyodbc

# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
database = 'Inventory_Management_System'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

class AddSaleScreen(QtWidgets.QMainWindow):
    saleAdded = QtCore.pyqtSignal()
    def __init__(self):
        super(AddSaleScreen, self).__init__()
        uic.loadUi("Screens/AddSales.ui", self)

        self.PopulateProductTable()
        self.PopulateCustomerTable()

        self.ProductTable.itemSelectionChanged.connect(self.get_selected_product_data)
        self.CustomerTable.itemSelectionChanged.connect(self.get_selected_customer_data)

        self.ProductID.setDisabled(True)
        self.ProductName.setDisabled(True)
        self.CustomerID.setDisabled(True)
        self.CustomerName.setDisabled(True)

        self.AddProductCustomer.clicked.connect(self.add_product_customer)
        self.AddSale.clicked.connect(self.add_sale)
        self.ClearSale.clicked.connect(self.clear)
        self.SearchProduct.clicked.connect(self.search_product)
        self.SearchCustomer.clicked.connect(self.search_customer)

    def PopulateProductTable(self):

        cursor.execute("SELECT * FROM Products")
        self.ProductTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ProductTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ProductTable.setItem(row_index, col_index, item)
        self.ProductTable.resizeColumnsToContents()
    def PopulateCustomerTable(self):

        cursor.execute("SELECT * FROM Customer")
        self.CustomerTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.CustomerTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.CustomerTable.setItem(row_index, col_index, item)
        self.CustomerTable.resizeColumnsToContents()

    def get_selected_product_data(self):

        selected_row = self.ProductTable.currentRow()
        if selected_row is not None:
            ProductID_item = self.ProductTable.item(selected_row, 0)
            ProductName_item = self.ProductTable.item(selected_row, 1)
            ProductPrice_item = self.ProductTable.item(selected_row, 3)

            if ProductID_item is not None and ProductName_item is not None:
                ProductID = ProductID_item.text()
                ProductName = ProductName_item.text()
                ProductPrice = ProductPrice_item.text()

                self.ProductID.setText(ProductID)
                self.ProductName.setText(ProductName)
                self.Price.setText(ProductPrice)
        else:
            error_message = "Error: No row is selected."
            QMessageBox.critical(self, "Error", error_message)

    def get_selected_customer_data(self):
        
        selected_row = self.CustomerTable.currentRow()

        if selected_row is not None:
            CustomerID_item = self.CustomerTable.item(selected_row, 0)
            CustomerName_item = self.CustomerTable.item(selected_row, 1) 
            Address_item = self.CustomerTable.item(selected_row, 6)
            ContactNumber_item = self.CustomerTable.item(selected_row, 3)
            BackupContactNumber_item = self.CustomerTable.item(selected_row, 4)
            Email_item = self.CustomerTable.item(selected_row, 5)

            if CustomerID_item is not None and CustomerName_item is not None and Address_item is not None and ContactNumber_item is not None and BackupContactNumber_item is not None and Email_item is not None:
                CustomerID = CustomerID_item.text()
                CustomerName = CustomerName_item.text()
                Address = Address_item.text()
                ContactNumber = ContactNumber_item.text()
                BackupContactNumber = BackupContactNumber_item.text()
                Email = Email_item.text()

                self.CustomerID.setText(CustomerID)
                self.CustomerName.setText(CustomerName)
                self.Address.setText(Address)
                self.ContactNumber.setText(ContactNumber)
                self.BackupContactNumber.setText(BackupContactNumber)
                self.Email.setText(Email)

            else:
                # Show an error message if the items are None
                error_message = "Error: Row Already Selected!"
                QMessageBox.critical(self, "Error", error_message)
        else:
            # Show an error message if no row is selected
            error_message = "Error: No row is selected."
            QMessageBox.critical(self, "Error", error_message)

    def add_product_customer(self):
        # Get text from line edits
        product_id = self.ProductID.text()
        product_name = self.ProductName.text()
        quantity = (self.Quantity.text())
        customer_id = self.CustomerID.text()
        customer_name = self.CustomerName.text()
        price = (self.Price.text())
        discount = (self.Discount.text())
        address = self.Address.text()
        contact_number = self.ContactNumber.text()
        backup_contact_number = self.BackupContactNumber.text()
        email = self.Email.text()
        # if product_id == '' or product_name == '' or quantity == '' or customer_id == '' or customer_name == '' or price == '' or discount == '' or address == '' or contact_number == '' or backup_contact_number == '' or email == '':
        #     error_message = "Error: Please fill all the fields."
        #     QMessageBox.critical(self, "Error", error_message)
        # elif not str(quantity).isdigit():
        #     error_message = "Error: Quantity must be a positive integer."
        #     QMessageBox.critical(self, "Error", error_message)
        
        # elif float(discount) >= 0.0 and float(discount) <= 1.0:
        #     total = price * quantity * (1 - discount)
        # else:
        #     error_message = "Error: Discount cannot be greater than 1 or less than 0."
        #     QMessageBox.critical(self, "Error", error_message)
        

        if (
            product_id == ""
            or product_name == ""
            or quantity == ""
            or customer_id == ""
            or customer_name == ""
            or price == ""
            or discount == ""
            or address == ""
            or contact_number == ""
            or backup_contact_number == ""
            or email == ""
        ):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please Enter All Required Attributes!")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.exec()
        elif not str(quantity).isdigit():
            error_message = "Error: Quantity must be a positive integer."
            QMessageBox.critical(self, "Error", error_message)
        
        elif not discount.replace('.', '', 1).isdigit() or (float(discount) < 0.0 or float(discount) > 1.0):
            error_message = "Error: Discount must be a float between 0 and 1."
            QMessageBox.critical(self, "Error", error_message)

        else:
            
            cursor.execute(" select quantityProduced from Products where ProductID = ? ", (product_id,))
            availableQuantity = cursor.fetchone()

            if int(availableQuantity.quantityProduced) >= int(quantity):

                total = float(price) * int(quantity) * (1 - float(discount))

                row_position = self.SaleDetailsTable.rowCount()
                self.SaleDetailsTable.insertRow(row_position)
                self.CustomerTable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

                self.SaleDetailsTable.setItem(
                    row_position, 0, QTableWidgetItem(product_id))
                self.SaleDetailsTable.setItem(
                    row_position, 1, QTableWidgetItem(product_name))
                self.SaleDetailsTable.setItem(
                    row_position, 2, QTableWidgetItem(customer_id))        
                self.SaleDetailsTable.setItem(
                    row_position, 3, QTableWidgetItem(customer_name))
                self.SaleDetailsTable.setItem(
                    row_position, 4, QTableWidgetItem(str(quantity)))
                self.SaleDetailsTable.setItem(
                    row_position, 5, QTableWidgetItem(str(price)))
                self.SaleDetailsTable.setItem(
                    row_position, 6, QTableWidgetItem(str(discount)))
                self.SaleDetailsTable.setItem(
                    row_position, 7, QTableWidgetItem(str(total)))
            
                self.ProductID.setText("")
                self.ProductName.setText("")
                self.Price.setText("")
                self.Quantity.setText("")
                self.Discount.setText("")

            else:
                error_message = "Error: Required Quantity Is Not In Stock!."
                QMessageBox.critical(self, "Error", error_message)            

    def add_sale(self):

        self.SaleDate.setDate(QDate.currentDate())
        SaleDate = self.SaleDate.date().toString("yyyy-MM-dd")
        num_rows = self.SaleDetailsTable.rowCount()
        UserID = 2
        
        # cursor.execute("SELECT max(saleID) AS SaleID from Sale")
        # result = cursor.fetchone()
        # SaleID = result[0]+1
        # UserID = 2

        # SaleDate = self.SaleDate.date().toString("yyyy-MM-dd")

        num_rows = self.SaleDetailsTable.rowCount()
        TotalAmount = 0
        for row in range(num_rows):
            TotalAmount = TotalAmount + float(self.SaleDetailsTable.item(row, 7).text())

        CustomerID = int(self.SaleDetailsTable.item(row, 2).text())

        sql_query = """
            INSERT INTO [Sale]
            ([saleDate], [totalAmount], [customerID], [userID])
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql_query, (SaleDate, TotalAmount, CustomerID, UserID))
        connection.commit()

        cursor.execute("SELECT max(saleID) AS SaleID from Sale")
        result = cursor.fetchone()
        SaleID = result[0]

        for row in range(num_rows):

            ProductID = int(self.SaleDetailsTable.item(row, 0).text())
            CustomerID = int(self.SaleDetailsTable.item(row, 2).text())
            Quantity = int(self.SaleDetailsTable.item(row, 4).text())
            Price = float(self.SaleDetailsTable.item(row, 5).text())
            Discount = float(self.SaleDetailsTable.item(row, 6).text())        

            total = Quantity*Price*(1 - Discount)
            sql_query = """
                        INSERT INTO [SaleProduct]
                        ([Saleid], [ProductID], [quantity], [soldPrice], [discount])
                        VALUES (?, ?, ?, ?, ?)
                    """
            cursor.execute(sql_query, (SaleID, ProductID, Quantity, Price, Discount))
            connection.commit()

            sql_query = """
            UPDATE Products
            SET quantityProduced = quantityProduced - (?), quantitySold = quantitySold + (?)
            WHERE productID = (?)
            """
            cursor.execute(sql_query, (Quantity, Quantity, ProductID))
            connection.commit()

        QtWidgets.QMessageBox.information(
            self, "Sale Added", f"Sale ID: {SaleID} has been added successfully.")

        self.saleAdded.emit()
        # connection.close()
        self.close()

    def clear(self):
        self.ProductID.setText("")
        self.ProductName.setText("")
        self.Quantity.setText("")
        self.Price.setText("")
        self.Discount.setText("")
        self.CustomerName.setText("")
        self.SaleDate.setDate(QDate(2000, 1, 1))
        self.CustomerID.setText("")
        self.ContactNumber.setText("")
        self.BackupContactNumber.setText("")
        self.Email.setText("")
        self.Address.setText("")
        self.SaleDetailsTable.setRowCount(0)

    def search_product(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        if self.ProductDropDown.currentText() == 'Product ID':
            try:
                search_text = int(self.SearchProductBar.text())
                cursor.execute("SELECT * from Products where productID = ?", (search_text,))

                self.ProductTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    self.ProductTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.ProductTable.setItem(row_index, col_index, item)
                self.ProductTable.resizeColumnsToContents()

            except ValueError:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid integer for Product ID.")
                msgBox.setWindowTitle("Confirmation Box")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgBox.exec()
                return

        elif self.ProductDropDown.currentText() == 'Product Name':
            try:
                search_text = str(self.SearchProductBar.text())
                query = """ SELECT * from Products where productName like (?) """
                cursor.execute(query, ('%' + search_text + '%'))

                self.ProductTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    self.ProductTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.ProductTable.setItem(row_index, col_index, item)
                self.ProductTable.resizeColumnsToContents()

            except ValueError:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid string for Product Name.")
                msgBox.setWindowTitle("Confirmation Box")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgBox.exec()                
                return

        elif self.ProductDropDown.currentText() == 'Description':
            try:
                search_text = str(self.SearchProductBar.text())
                query = """ SELECT * from Products where description like (?) """
                cursor.execute(query, ('%' + search_text + '%'))

                self.ProductTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    self.ProductTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.ProductTable.setItem(row_index, col_index, item)
                self.ProductTable.resizeColumnsToContents()

            except ValueError:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid string for Product Name.")
                msgBox.setWindowTitle("Confirmation Box")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgBox.exec()                
                return
            
        elif self.ProductDropDown.currentText() == 'Select':
            cursor.execute("SELECT * FROM Products")
            self.ProductTable.setRowCount(0)

            for row_index, row_data in enumerate(cursor.fetchall()):
                self.ProductTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.ProductTable.setItem(row_index, col_index, item)
            self.ProductTable.resizeColumnsToContents()

    def search_customer(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        if self.CustomerDropDown.currentText() == 'Customer ID':
            try:
                search_text = int(self.SearchCustomerBar.text())
                cursor.execute("SELECT * from Customer where customerID = ?", (search_text,))

                self.CustomerTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    self.CustomerTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.CustomerTable.setItem(row_index, col_index, item)
                self.CustomerTable.resizeColumnsToContents()
                
            except ValueError:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid integer for Customer ID.")
                msgBox.setWindowTitle("Confirmation Box")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgBox.exec()            
                return

        elif self.CustomerDropDown.currentText() == 'Customer Name':
            try:
                search_text = str(self.SearchCustomerBar.text())
                query = """ SELECT * from Customer where customerName like (?) """
                cursor.execute(query, ('%' + search_text + '%'))

                self.CustomerTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    self.CustomerTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.CustomerTable.setItem(row_index, col_index, item)
                self.CustomerTable.resizeColumnsToContents()
            except ValueError:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid string for Customer Name.")
                msgBox.setWindowTitle("Confirmation Box")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgBox.exec()            
                return
        elif self.CustomerDropDown.currentText() == 'Contact Number':
            try:
                search_text = str(self.SearchCustomerBar.text())
                query = """ SELECT * from Customer where contactNumber like (?) """
                cursor.execute(query, ('%' + search_text + '%'))

                self.CustomerTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    self.CustomerTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.CustomerTable.setItem(row_index, col_index, item)
                self.CustomerTable.resizeColumnsToContents()
            except ValueError:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Please enter a valid number")
                msgBox.setWindowTitle("Confirmation Box")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgBox.exec()            
                return

        else:
            cursor.execute("SELECT * FROM Customer")
            self.CustomerTable.setRowCount(0)

            for row_index, row_data in enumerate(cursor.fetchall()):
                self.CustomerTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.CustomerTable.setItem(row_index, col_index, item)

            self.CustomerTable.resizeColumnsToContents()