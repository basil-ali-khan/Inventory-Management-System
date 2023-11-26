# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import VendorScreen, PurchaseScreen

# server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
server = 'LAPTOP-MNMD5RBU'
database = 'Inventory_Management_System'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish a connection to the database
connection = pyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()

# ---------------------------------------------------------------------------------

# VENDOR

# ---------------------------------------------------------------------------------

class EditVendorScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(EditVendorScreen, self).__init__()
        uic.loadUi("Screens/EditVendors.ui", self)

class AddVendorMessageBox(QMessageBox):
    def __init__(self, message, title):
        super().__init__()

        self.setIcon(QMessageBox.Icon.Information)
        self.setText(message)
        self.setWindowTitle(title)
        self.addButton(QMessageBox.StandardButton.Close)

class VendorScreen(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(VendorScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/Vendors.ui', self)

        self.PopulateVendorTable()        

        self.addVendorButton.clicked.connect(self.AddVendor)

        self.editVendorButton.clicked.connect(self.EditVendor)


    def PopulateVendorTable(self):
        cursor.execute("SELECT * FROM Vendor")
        self.vendorTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.vendorTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.vendorTable.setItem(row_index, col_index, item)

    def AddVendor(self):
        name = self.vendorNameBox.text()
        contact = self.vendorContactNumber.text()
        backupContact = self.vendorBackupContact.text()
        email = self.vendorEmail.text()
        address = self.vendorAddress.text()

        if name == '' or contact == '' or backupContact == '' or email == '' or address == '':
            self.notAddedMsg = AddVendorMessageBox("Please enter complete information to add vendor", "Failed")
            self.notAddedMsg.show()
        else:
            sql_query = "insert into vendor values(?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (name, contact, backupContact, email, address))
            connection.commit()

            self.addMsg = AddVendorMessageBox("Vendor added successfully", "Success")
            self.addMsg.show()
    
    def EditVendor(self):
        self.editVendor = EditVendorScreen()
        self.editVendor.show()

# ---------------------------------------------------------------------------------

# PURCHASE

# ---------------------------------------------------------------------------------

class ViewPurchaseScreen(QtWidgets.QMainWindow):
    def __init__(self, purchase_id, vendor_id, purchase_date, total_amount):
        super(ViewPurchaseScreen, self).__init__() 
        uic.loadUi("Screens/ViewPurchase.ui", self)

        self.purchase_id = int(purchase_id)
        self.vendor_id = int(vendor_id)
        self.purchase_date = int(purchase_date)
        self.total_amount = int(total_amount)

        self.viewPurchaseId.setText(self.purchase_id)
        self.viewPurchaseId.setDisabled(True)

        self.viewVendorId.setText(self.vendor_id)
        self.viewVendorId.setDisabled(True)

        self.viewPurchaseDate.setText(self.purchase_date)
        self.viewPurchaseDate.setDisabled(True)

        self.viewTotalAmount.setText(self.total_amount)
        self.viewTotalAmount.setDisabled(True)

class AddPurchaseScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddPurchaseScreen, self).__init__()
        uic.loadUi("Screens/AddPurchase.ui", self)

        self.PopulateMaterialTable()
        self.PopulateVendorTable()

        self.materialTable.itemSelectionChanged.connect(self.get_selected_material_data)
        self.vendorTable.itemSelectionChanged.connect(self.get_selected_vendor_data)

        self.MaterialID.setDisabled(True)
        self.MaterialName.setDisabled(True)
        self.VendorID.setDisabled(True)
        self.VendorName.setDisabled(True)

        self.AddMaterialVendor.clicked.connect(self.add_material)
        self.AddPurchase.clicked.connect(self.add_purchase)
        self.ClearPurchase.clicked.connect(self.clear)

    def PopulateMaterialTable(self):

        cursor.execute("SELECT * FROM Material")
        self.materialTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.materialTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.materialTable.setItem(row_index, col_index, item)

    def PopulateVendorTable(self):

        cursor.execute("SELECT * FROM Vendor")
        self.vendorTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.vendorTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.vendorTable.setItem(row_index, col_index, item)

    def get_selected_material_data(self):

        selected_row = self.materialTable.currentRow()
        MaterialID = self.materialTable.item(selected_row, 0).text()
        MaterialName = self.materialTable.item(selected_row, 1).text()

        self.MaterialID.setText(MaterialID)
        self.MaterialName.setText(MaterialName)

    def get_selected_vendor_data(self):

        selected_row = self.vendorTable.currentRow()
        VendorID = self.vendorTable.item(selected_row, 0).text()
        VendorName = self.vendorTable.item(selected_row, 1).text()

        self.VendorID.setText(VendorID)
        self.VendorName.setText(VendorName)

    def add_material(self):

        if self.MaterialID == "" or self.MaterialName == "" or self.UnitPrice == "" or self.Quantity == "" or self.VendorID == "" or self.VendorName == "":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please Select All Required Attributes!")
            msgBox.setWindowTitle("Confirmation Box")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

        else:
            row_position = self.purchaseDetailsTable.rowCount()
            self.purchaseDetailsTable.insertRow(row_position)

            self.purchaseDetailsTable.setItem(
                row_position, 0, QTableWidgetItem(self.MaterialID.text()))
            self.purchaseDetailsTable.setItem(
                row_position, 1, QTableWidgetItem(self.MaterialName.text()))
            self.purchaseDetailsTable.setItem(
                row_position, 2, QTableWidgetItem(self.UnitPrice.text()))
            self.purchaseDetailsTable.setItem(
                row_position, 3, QTableWidgetItem(self.Quantity.text()))
            self.purchaseDetailsTable.setItem(
                row_position, 4, QTableWidgetItem(self.VendorID.text()))        
            self.purchaseDetailsTable.setItem(
                row_position, 5, QTableWidgetItem(self.VendorName.text()))  

            header = self.purchaseDetailsTable.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

            self.MaterialID.setText("")
            self.MaterialName.setText("")
            self.UnitPrice.setText("")
            self.Quantity.setText("")
            self.VendorID.setText("")
            self.VendorName.setText("")

    def add_purchase(self):

        # Retrieve the newly inserted order ID
        cursor.execute("SELECT max(purchaseid) AS PurchaseID from Purchase")
        result = cursor.fetchone()
        PurchaseID = result[0]+1

        # Get order information from input fields
        PurchaseDate = self.PurchaseDate.date().toString("yyyy-MM-dd")
        UnitPrice = self.UnitPrice.text()
        Quantity = self.Quantity.text()
        VendorID = self.VendorID.text()

        # TODO: Provide the  connection string to connect to the Northwind database
        connection = pyodbc.connect(connection_string)

        cursor = connection.cursor()

        # TODO: Write SQL query with parameters to insert Purchase
        sql_query = """
                    INSERT INTO [Purchase]
                    ([PurchaseID], [PurchaseDate], [TotalAmount], [VendorID])
                    VALUES (?, ?, ?, ?)
                """
        
        # Execute the SQL query with parameter values
        cursor.execute(sql_query, (int(PurchaseID), PurchaseDate, int(UnitPrice*Quantity), int(VendorID)))
        connection.commit()

        # Show a message box with the order ID
        QtWidgets.QMessageBox.information(
            self, "Purchase Added", f"Purchase ID: {PurchaseID} has been added successfully.")

        num_rows = self.purchaseDetailsTable.rowCount()

        for row in range(num_rows):

            MaterialID = int(self.purchaseDetailsTable.item(row, 0).text())
            UnitPrice = int(self.purchaseDetailsTable.item(row, 2).text())
            Quantity = int(self.purchaseDetailsTable.item(row, 3).text())
            VendorID = int(self.purchaseDetailsTable.item(row, 4).text())

            # TODO: Write SQL query with parameters to insert Purchase

            sql_query = """
                        INSERT INTO [PurchaseMaterial]
                        ([PurchaseID], [MaterialID], [Quantity], [UnitPrice], [VendorID])
                        VALUES (?, ?, ?, ?)
                    """

            # Execute the SQL query with parameter values
            cursor.execute(sql_query, (int(PurchaseID), int(MaterialID), int(Quantity), int(UnitPrice), int(VendorID)))
            connection.commit()

        # Close the database connection
        connection.close()

    def clear(self):
        self.MaterialID.setText("")
        self.MaterialName.setText("")
        self.UnitPrice.setText("")
        self.Quantity.setText("")
        self.VendorID.setText("")
        self.VendorName.setText("")
        self.PurchaseDate.setDate(QDate(2000, 1, 1))

class PurchaseScreen(QtWidgets.QMainWindow):   

    def __init__(self):
        
        super(PurchaseScreen, self).__init__() 
        uic.loadUi('Screens/Purchase.ui', self)

        self.PopulatePurchaseTable()        
        self.viewPurchaseButton.clicked.connect(self.ViewPurchase)
        self.addPurchaseButton.clicked.connect(self.AddPurchase)
        self.deletePurchaseButton.clicked.connect(self.DeletePurchase)

    def PopulatePurchaseTable(self):

        cursor.execute("SELECT * FROM Purchase")
        self.purchaseTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.purchaseTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.purchaseTable.setItem(row_index, col_index, item)

    def ViewPurchase(self):
            
        selected_row = self.purchaseTable.currentRow()

        purchase_id = int(self.purchaseTable.item(selected_row, 0).text())
        vendor_id = int(self.purchaseTable.item(selected_row, 1).text())
        purchase_date = int(self.purchaseTable.item(selected_row, 2).text())
        total_amount = int(self.purchaseTable.item(selected_row, 3).text())

        self.viewPurchase = ViewPurchaseScreen(purchase_id, vendor_id, purchase_date, total_amount)
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

class UI(QtWidgets.QMainWindow):   

    def __init__(self):

        super(UI, self).__init__() 
        
        uic.loadUi('Screens/UserAuthentication.ui', self)

        self.vendorsButton.setEnabled(True)
        self.vendorsButton.clicked.connect(self.OpenVendorScreen)

        self.purchaseButton.setEnabled(True)
        self.purchaseButton.clicked.connect(self.OpenPurchaseScreen)

    def OpenVendorScreen(self):
        self.vendor = VendorScreen()
        self.vendor.show()

    def OpenPurchaseScreen(self):
        self.purchase = PurchaseScreen()
        self.purchase.show()
        

app = QApplication(sys.argv)
loginScreen = UI()
loginScreen.show()
sys.exit(app.exec())
