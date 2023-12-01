import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
from EditMaterialClass import EditMaterialScreen


server = 'DESKTOP-UMMHQQL\SQLEXPRESS01'
database = 'Inventory_Management_System'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
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

class MaterialScreen(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(MaterialScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/Materials.ui', self)

        self.PopulateMaterialTable()

        self.searchMaterialButton.clicked.connect(self.SearchMaterial)

        self.editMaterialButton.clicked.connect(self.EditMaterial)

        self.refreshButton.clicked.connect(self.ClearSearch)

        self.addMaterialButton.clicked.connect(self.AddMaterial)

        self.clearMaterialButton.clicked.connect(self.ClearMaterialInfo)

    def ClearMaterialInfo(self):
        self.materialNameBox.setText('')
        self.unitsBox.setText('')
        self.materialDescBox.setText('')

    def AddMaterial(self):
        name = self.materialNameBox.text()
        units = self.unitsBox.text()
        desc = self.materialDescBox.toPlainText()

        self.msg = QtWidgets.QMessageBox()

        if name == '' or units == '' or desc == '':
            self.msg.setWindowTitle('Error')
            self.msg.setText('Please enter complete info')
        else:
            if not units.isdigit():
                self.msg.setWindowTitle('Error')
                self.msg.setText('Units should be a numeric value')
                self.msg.show()
            else:
                sql_query = f"insert into Material values(?, ?, ?)"
                cursor.execute(sql_query, (name, desc, units))
                connection.commit()

                self.msg.setWindowTitle('Success')
                self.msg.setText('Material added successfully')

                self.PopulateMaterialTable()
        
        self.msg.show()
    
    def ClearSearch(self):
        self.PopulateMaterialTable()
        self.searchMaterialValue.setText('')

    def EditMaterial(self):
        row = self.materialTable.currentRow()
        id = self.materialTable.item(row, 0).text()
        name = self.materialTable.item(row, 1).text()        
        desc = self.materialTable.item(row, 2).text()
        units = self.materialTable.item(row, 3).text()

        self.editMaterialScreen = EditMaterialScreen(id, name, desc, units)
        self.editMaterialScreen.show()

    def PopulateMaterialTable(self):
        cursor.execute('select * from material')
        self.materialTable.setRowCount(0)

        for row_index, row_data in enumerate(cursor.fetchall()):
            self.materialTable.insertRow(row_index)
            
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.materialTable.setItem(row_index, col_index, item)

    def SearchMaterial(self):
        criteria = self.searchMaterialCriteria.currentText().strip()
        criteriaValue = self.searchMaterialValue.text().strip()

        if (criteria != '' and criteriaValue != ''):        
            # print('criteria: ', criteria)

            if criteria == 'Material Name':
                sql_query = 'select * from Material where materialName like (?)'
                cursor.execute(sql_query, ('%' + criteriaValue + '%',))
                #connection.commit()
                self.materialTable.clearContents()
                self.materialTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    print('populating row')
                    self.materialTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        print('Adding item to material table.')
                        self.materialTable.setItem(row_index, col_index, item)

            elif criteria == 'Description':
                sql_query = 'select * from Material where description like (?)'
                cursor.execute(sql_query, ('%' + criteriaValue + '%',))
                #connection.commit()     
                self.materialTable.clearContents()
                self.materialTable.setRowCount(0)

                for row_index, row_data in enumerate(cursor.fetchall()):
                    print('populating row')
                    self.materialTable.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        print('Adding item to material table.')
                        self.materialTable.setItem(row_index, col_index, item)

            elif criteria == 'Units':
                if criteriaValue.isdigit():
                    sql_query = 'select * from Material where units = (?)'
                    cursor.execute(sql_query, (criteriaValue,))

                    self.materialTable.clearContents()
                    self.materialTable.setRowCount(0)

                    for row_index, row_data in enumerate(cursor.fetchall()):
                        print('populating row')
                        self.materialTable.insertRow(row_index)
                        for col_index, cell_data in enumerate(row_data):
                            item = QTableWidgetItem(str(cell_data))
                            print('Adding item to material table.')
                            self.materialTable.setItem(row_index, col_index, item)

                else:
                    self.msg = QtWidgets.QMessageBox()
                    self.msg.setWindowTitle('Error')
                    self.msg.setText('Units should be a numeric value')
                    self.msg.show()            

            print('Query executed')
            
        else:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('Please select search criteria and/or enter search value')
