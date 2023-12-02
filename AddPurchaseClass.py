# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from MaterialClass import MaterialScreen
from VendorClass import VendorScreen

from ConnectionString import connection, cursor

class AddPurchaseScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(AddPurchaseScreen, self).__init__()
        uic.loadUi("Screens/AddPurchase.ui", self)

        self.PopulateMaterialTable()
        self.PopulateVendorTable()

        self.MaterialTable.itemSelectionChanged.connect(self.get_selected_material_data)
        self.vendorTable.itemSelectionChanged.connect(self.get_selected_vendor_data)

        self.MaterialID.setDisabled(True)
        self.MaterialName.setDisabled(True)
        self.VendorID.setDisabled(True)
        self.VendorName.setDisabled(True)

        self.AddMaterialVendor.clicked.connect(self.add_material)
        self.AddPurchase.clicked.connect(self.add_purchase)
        self.ClearPurchase.clicked.connect(self.clear)
        self.SearchMaterial.clicked.connect(self.search_material)
        self.SearchVendor.clicked.connect(self.search_vendor)
        self.addMaterialButton.clicked.connect(self.add_new_material)
        self.addVendorButton.clicked.connect(self.add_vendor)
        self.refreshMaterialButton.clicked.connect(self.PopulateMaterialTable)
        self.refreshVendorButton.clicked.connect(self.PopulateVendorTable)


    def add_new_material(self):
        self.addMaterialScreen = MaterialScreen()
        self.addMaterialScreen.show()
    
    def add_vendor(self):
        self.addVendorScreen = VendorScreen()
        self.addVendorScreen.show()

    def PopulateMaterialTable(self):

        cursor.execute("SELECT * FROM Material")
        self.MaterialTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.MaterialTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.MaterialTable.setItem(row_index, col_index, item)

    def PopulateVendorTable(self):

        cursor.execute("SELECT * FROM Vendor")
        self.vendorTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.vendorTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.vendorTable.setItem(row_index, col_index, item)

    def get_selected_material_data(self):

        selected_row = self.MaterialTable.currentRow()
        if selected_row is not None:
            MaterialID_item = self.MaterialTable.item(selected_row, 0)
            MaterialName_item = self.MaterialTable.item(selected_row, 1)

            if MaterialID_item is not None and MaterialName_item is not None:
                MaterialID = MaterialID_item.text()
                MaterialName = MaterialName_item.text()

                self.MaterialID.setText(MaterialID)
                self.MaterialName.setText(MaterialName)
            else:
                # Show an error message if the items are None
                error_message = "Error: Row Already Selected!."
                QMessageBox.critical(self, "Error", error_message)
        else:
            # Show an error message if no row is selected
            error_message = "Error: No row is selected."
            QMessageBox.critical(self, "Error", error_message)

    def get_selected_vendor_data(self):
        selected_row = self.vendorTable.currentRow()

        if selected_row is not None:
            VendorID_item = self.vendorTable.item(selected_row, 0)
            VendorName_item = self.vendorTable.item(selected_row, 1)

            if VendorID_item is not None and VendorName_item is not None:
                VendorID = VendorID_item.text()
                VendorName = VendorName_item.text()

                self.VendorID.setText(VendorID)
                self.VendorName.setText(VendorName)
            else:
                # Show an error message if the items are None
                error_message = "Error: Row Already Selected!"
                QMessageBox.critical(self, "Error", error_message)
        else:
            # Show an error message if no row is selected
            error_message = "Error: No row is selected."
            QMessageBox.critical(self, "Error", error_message)

    def add_material(self):

        if self.MaterialID.text() == '' or self.MaterialName.text() == '' or self.UnitCost.text() == '' or self.Quantity.text() == '' or self.VendorID.text() == '' or self.VendorName.text() == '':
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setText("Please Select All Required Attributes!")
            self.msgBox.setWindowTitle("Confirmation Box")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            self.msgBox.show()

        else:
            row_position = self.purchaseDetailsTable.rowCount()
            self.purchaseDetailsTable.insertRow(row_position)

            if (self.UnitCost.text().isdigit() and self.Quantity.text().isdigit()):

                self.purchaseDetailsTable.setItem(
                    row_position, 0, QTableWidgetItem(self.MaterialID.text()))
                self.purchaseDetailsTable.setItem(
                    row_position, 1, QTableWidgetItem(self.MaterialName.text()))
                self.purchaseDetailsTable.setItem(
                    row_position, 2, QTableWidgetItem(self.VendorID.text()))        
                self.purchaseDetailsTable.setItem(
                    row_position, 3, QTableWidgetItem(self.VendorName.text()))
                self.purchaseDetailsTable.setItem(
                    row_position, 4, QTableWidgetItem(self.UnitCost.text()))
                self.purchaseDetailsTable.setItem(
                    row_position, 5, QTableWidgetItem(self.Quantity.text()))
                
            else:
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setText('Unit Price and Quantity should be numeric')
                self.msgBox.setWindowTitle('Error')
                self.msgBox.show()

            self.MaterialID.setText("")
            self.MaterialName.setText("")
            self.UnitCost.setText("")
            self.Quantity.setText("")
            self.VendorID.setText("")
            self.VendorName.setText("")

    def add_purchase(self):

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT max(purchaseid) AS PurchaseID from Purchase")
        result = cursor.fetchone()
        PurchaseID = result[0]+1

        PurchaseDate = self.PurchaseDate.date().toString("yyyy-MM-dd")

        num_rows = self.purchaseDetailsTable.rowCount()
        TotalAmount = 0
        for row in range(num_rows):
            TotalAmount = TotalAmount + int(self.purchaseDetailsTable.item(row, 4).text()) * int(self.purchaseDetailsTable.item(row, 5).text())

        VendorID = int(self.purchaseDetailsTable.item(row, 2).text())

        sql_query = """
            INSERT INTO [Purchase]
            ([purchaseDate], [totalAmount], [vendorID])
            VALUES (?, ?, ?)
        """
        cursor.execute(sql_query, (PurchaseDate, int(TotalAmount), int(VendorID)))
        connection.commit()

        for row in range(num_rows):

            MaterialID = int(self.purchaseDetailsTable.item(row, 0).text())
            VendorID = int(self.purchaseDetailsTable.item(row, 2).text())
            UnitCost = int(self.purchaseDetailsTable.item(row, 4).text())
            Quantity = int(self.purchaseDetailsTable.item(row, 5).text())

            sql_query = """
                        INSERT INTO [PurchaseMaterial]
                        ([purchaseid], [materialID], [quantity], [cost])
                        VALUES (?, ?, ?, ?)
                    """
            cursor.execute(sql_query, (int(PurchaseID), int(MaterialID), int(Quantity), int(UnitCost)))
            connection.commit()

        QtWidgets.QMessageBox.information(
            self, "Purchase Added", f"Purchase ID: {PurchaseID} has been added successfully.")

        connection.close()
        self.close()

    def clear(self):
        self.MaterialID.setText("")
        self.MaterialName.setText("")
        self.UnitCost.setText("")
        self.Quantity.setText("")
        self.VendorID.setText("")
        self.VendorName.setText("")
        self.PurchaseDate.setDate(QDate(2000, 1, 1))
        self.purchaseDetailsTable.setRowCount(0)

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

        self.MaterialTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.MaterialTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.MaterialTable.setItem(row_index, col_index, item)

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

        self.vendorTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.vendorTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.vendorTable.setItem(row_index, col_index, item)