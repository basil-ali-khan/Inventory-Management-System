# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

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

class ViewEditPurchaseScreen(QtWidgets.QMainWindow):
    editDone = QtCore.pyqtSignal()
    def __init__(self, purchase_id, purchase_date, total_amount, vendor_name):
        super(ViewEditPurchaseScreen, self).__init__() 
        uic.loadUi("Screens/ViewPurchase.ui", self)
        self.setWindowTitle("View/Edit Purchase")

        self.MaterialTable.itemSelectionChanged.connect(self.get_selected_material_data)
        self.savePurchaseButton.clicked.connect(self.SaveEdit)
        self.DonePurchaseButton.clicked.connect(self.DoneEdit)

        self.purchase_id = int(purchase_id)
        self.purchase_date = QDate.fromString(str(purchase_date), 'yyyy-MM-dd')
        self.total_amount = int(total_amount)
        self.vendor_name = str(vendor_name)

        self.viewPurchaseId.setText(str(self.purchase_id))
        self.viewPurchaseId.setDisabled(True)

        self.viewPurchaseDate.setDate(self.purchase_date)
        self.viewPurchaseDate.setDisabled(True)

        self.viewTotalAmount.setText(str(self.total_amount))
        self.viewTotalAmount.setDisabled(True)

        self.viewVendorName.setText(str(self.vendor_name))
        self.viewVendorName.setDisabled(True)

        cursor.execute("SELECT Material.materialName, PurchaseMaterial.quantity, PurchaseMaterial.cost, PurchaseMaterial.quantity*PurchaseMaterial.cost FROM PurchaseMaterial JOIN Purchase ON PurchaseMaterial.purchaseID = Purchase.purchaseID JOIN Material ON PurchaseMaterial.materialID = Material.materialID WHERE PurchaseMaterial.purchaseID = ?", (purchase_id,))
        self.MaterialTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.MaterialTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.MaterialTable.setItem(row_index, col_index, item)

    
    def get_selected_material_data(self):

        selected_row = self.MaterialTable.currentRow()
        MaterialName = self.MaterialTable.item(selected_row, 0).text()
        Quantity = self.MaterialTable.item(selected_row, 1).text()
        UnitCost = self.MaterialTable.item(selected_row, 2).text()

        self.MaterialName.setText(MaterialName)
        self.Quantity.setText(Quantity)
        self.UnitCost.setText(UnitCost)

    def DoneEdit(self):
        self.editDone.emit()
        self.close()

    def UpdateTotal(self):
        total = 0
        for i in range(self.MaterialTable.rowCount()):
            total += int(self.MaterialTable.item(i, 3).text())
        self.viewTotalAmount.setText(str(total))

    def SaveEdit(self):
        selected_row = self.MaterialTable.currentRow()
        if selected_row == -1 or self.MaterialName.text() == "":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please Select a Material!")
            msgBox.setWindowTitle("Confirmation Box")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.exec()
            return
        
        PurchaseID = self.viewPurchaseId.text()
        Quantity = self.Quantity.text()
        UnitCost = self.UnitCost.text()

        if (
            Quantity == ""
            or UnitCost == ""

        ):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please Enter All Required Attributes!")
            msgBox.setWindowTitle("Confirmation Box")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.exec()

        elif not Quantity.isdigit() or int(Quantity) <= 0 or (UnitCost.isdigit() == False):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please Enter a valid quantity and unit cost!")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msgBox.exec()

        else:

            self.UpdateTotal()

            sql_query = """
                        update PurchaseMaterial
                        set quantity = (?), cost = (?)
                        WHERE purchaseID = (?) and materialID = (select materialID from Material where materialName = ?)
                        """
            
            cursor.execute(sql_query, (Quantity, UnitCost, PurchaseID, self.MaterialName.text()))
            connection.commit()

            sql_query = """
                        update Purchase
                        set totalAmount = (select sum(quantity * cost) from PurchaseMaterial where purchaseID = ?)
                        WHERE purchaseID = (?)
                        """
            cursor.execute(sql_query, (PurchaseID, PurchaseID))
            connection.commit()

            self.MaterialTable.setItem(selected_row, 1, QTableWidgetItem(Quantity))
            self.MaterialTable.setItem(selected_row, 2, QTableWidgetItem(UnitCost))
            self.MaterialTable.setItem(selected_row, 3, QTableWidgetItem(str(int(Quantity) * int(UnitCost))))

            self.UpdateTotal()



            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Success')
            self.msg.setText('Purchase edit successful')
            self.msg.show()
        