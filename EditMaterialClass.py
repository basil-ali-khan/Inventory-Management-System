import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc


server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
database = 'Inventory_Management_System'  # Name of your Northwind database
use_windows_authentication = False  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = 'Sirmehdi69'  # Specify a password if not using Windows Authentication

if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = (
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=Inventory_Management_System;UID=sa;PWD=Sirmehdi69;TrustServerCertificate=yes;Connection Timeout=30;'
    )

# Establish a connection to the database
connection = pyodbc.connect(connection_string)

# Create a cursor to interact with the database
cursor = connection.cursor()

class EditMaterialScreen(QtWidgets.QMainWindow):   
    def __init__(self, id, name, desc, units):
        # Call the inherited classes __init__ method
        super(EditMaterialScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/EditMaterial.ui', self)

        self.materialIdBox.setText(id)
        self.materialNameBox.setText(name)
        self.unitsBox.setText(units)
        self.materialDescBox.setPlainText(desc)

        self.cancelButton.clicked.connect(self.CancelEdit)
        self.doneButton.clicked.connect(self.EditDone)

    def CancelEdit(self):
        self.close()

    def EditDone(self):
        id = self.materialIdBox.text()
        newName = self.materialNameBox.text()
        newUnits = self.unitsBox.text()
        newDesc = self.materialDescBox.toPlainText()

        sql_query = """
                    update material
                    set materialName = (?), description = (?), units = (?)
                    where materialID = (?)
                    """
        
        cursor.execute(sql_query, (newName, newDesc, newUnits, id))
        connection.commit()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Success")
        self.msg.setText("Edit done successfully.")
        self.msg.show()
        
