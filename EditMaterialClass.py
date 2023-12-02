import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

from ConnectionString import connection, cursor

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
        
