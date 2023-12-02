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

class AddSaleScreen(QtWidgets.QMainWindow):
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
        # self.AddPurchase.clicked.connect(self.add_sale)
        # self.ClearPurchase.clicked.connect(self.clear)
        # self.SearchMaterial.clicked.connect(self.search_material)
        # self.SearchVendor.clicked.connect(self.search_vendor)

    def PopulateProductTable(self):

        cursor.execute("SELECT * FROM Products")
        self.ProductTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ProductTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ProductTable.setItem(row_index, col_index, item)

    def PopulateCustomerTable(self):

        cursor.execute("SELECT * FROM Customer")
        self.CustomerTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.CustomerTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.CustomerTable.setItem(row_index, col_index, item)

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
        quantity = self.Quantity.text()
        customer_id = self.CustomerID.text()
        customer_name = self.CustomerName.text()
        price = self.Price.text()
        discount = self.Discount.text()
        address = self.Address.text()
        contact_number = self.ContactNumber.text()
        backup_contact_number = self.BackupContactNumber.text()
        email = self.Email.text()

        # Check the condition
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
            msgBox.setWindowTitle("Confirmation Box")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.exec()

        else:
            row_position = self.SaleDetailsTable.rowCount()
            self.SaleDetailsTable.insertRow(row_position)

            self.SaleDetailsTable.setItem(
                row_position, 0, QTableWidgetItem(self.ProductID.text()))
            self.SaleDetailsTable.setItem(
                row_position, 1, QTableWidgetItem(self.ProductName.text()))
            self.SaleDetailsTable.setItem(
                row_position, 2, QTableWidgetItem(self.CustomerID.text()))        
            self.SaleDetailsTable.setItem(
                row_position, 3, QTableWidgetItem(self.CustomerName.text()))
            self.SaleDetailsTable.setItem(
                row_position, 4, QTableWidgetItem(self.Price.text()))
            self.SaleDetailsTable.setItem(
                row_position, 5, QTableWidgetItem(self.Quantity.text()))
            self.SaleDetailsTable.setItem(
                row_position, 6, QTableWidgetItem(self.Discount.text()))
            
            self.ProductID.setText("")
            self.ProductName.setText("")
            self.CustomerID.setText("")
            self.CustomerName.setText("")
            self.Price.setText("")
            self.Quantity.setText("")
            self.Discount.setText("")

    def add_sale(self):

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT max(purchaseid) AS PurchaseID from Purchase")
        result = cursor.fetchone()
        PurchaseID = result[0]+1

        PurchaseDate = self.PurchaseDate.date().toString("yyyy-MM-dd")

        num_rows = self.SaleDetailsTable.rowCount()
        TotalAmount = 0
        for row in range(num_rows):
            TotalAmount = TotalAmount + int(self.SaleDetailsTable.item(row, 4).text()) * int(self.SaleDetailsTable.item(row, 5).text())

        CustomerID = int(self.SaleDetailsTable.item(row, 2).text())

        sql_query = """
            INSERT INTO [Purchase]
            ([purchaseDate], [totalAmount], [vendorID])
            VALUES (?, ?, ?)
        """
        cursor.execute(sql_query, (PurchaseDate, int(TotalAmount), int(CustomerID)))
        connection.commit()

        for row in range(num_rows):

            ProductID = int(self.SaleDetailsTable.item(row, 0).text())
            CustomerID = int(self.SaleDetailsTable.item(row, 2).text())
            UnitCost = int(self.SaleDetailsTable.item(row, 4).text())
            Quantity = int(self.SaleDetailsTable.item(row, 5).text())

            sql_query = """
                        INSERT INTO [PurchaseMaterial]
                        ([purchaseid], [materialID], [quantity], [cost])
                        VALUES (?, ?, ?, ?)
                    """
            cursor.execute(sql_query, (int(PurchaseID), int(ProductID), int(Quantity), int(UnitCost)))
            connection.commit()

        QtWidgets.QMessageBox.information(
            self, "Purchase Added", f"Purchase ID: {PurchaseID} has been added successfully.")

        connection.close()
        self.close()

    def clear(self):
        self.ProductID.setText("")
        self.ProductName.setText("")
        self.UnitCost.setText("")
        self.Quantity.setText("")
        self.CustomerID.setText("")
        self.CustomerName.setText("")
        self.PurchaseDate.setDate(QDate(2000, 1, 1))
        self.SaleDetailsTable.setRowCount(0)

    def search_material(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        if self.MaterialDropDown.currentText() == 'Material ID':
            search_text = int(self.SearchMaterial_2.text())
            cursor.execute("SELECT * from Material where materialID = ?", (search_text))

        elif self.MaterialDropDown.currentText() == 'Material Name':
            search_text = str(self.SearchMaterial_2.text())
            query = """
                SELECT * from Material where materialName like (?)
                """
            cursor.execute(query, ('%' + search_text + '%'))

        self.ProductTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ProductTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ProductTable.setItem(row_index, col_index, item)

    def search_vendor(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        if self.VendorDropDown.currentText() == 'Vendor ID':
            search_text = int(self.SearchVendor_2.text())
            cursor.execute("SELECT * from Vendor where vendorID = ?", (search_text))

        elif self.VendorDropDown.currentText() == 'Vendor Name':
            search_text = str(self.SearchVendor_2.text())
            query = """
                SELECT * from Vendor where vendorName like (?)
                """
            cursor.execute(query, ('%' + search_text + '%'))

        self.CustomerTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.CustomerTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.CustomerTable.setItem(row_index, col_index, item)