import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc


from ConnectionString import connection, cursor

class EditMaterialScreen(QtWidgets.QMainWindow):   
    materialUpdated = QtCore.pyqtSignal()
    def __init__(self, id, name, desc, units):
        # Call the inherited classes __init__ method
        super(EditMaterialScreen, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/EditMaterial.ui', self)
        self.setWindowTitle("Edit Material")

        self.materialIdBox.setText(id)
        self.materialNameBox.setText(name)
        self.unitsBox.setText(units)
        self.materialDescBox.setPlainText(desc)

        self.cancelButton.clicked.connect(self.CancelEdit)
        self.doneButton.clicked.connect(self.EditDone)

    def CancelEdit(self):
        self.close()

    def EditDone(self):
        self.msg = QtWidgets.QMessageBox()
        id = self.materialIdBox.text()
        newName = self.materialNameBox.text()
        newUnits = self.unitsBox.text()
        newDesc = self.materialDescBox.toPlainText()

        if not newUnits.isdigit():
            self.msg.setWindowTitle("Error")
            self.msg.setText("Units should be numeric")    
            self.msg.show()  
        else:  
            if id  != '' and newName != '' and newUnits != '' and newDesc != '':
                sql_query = """
                            update material
                            set materialName = (?), description = (?), units = (?)
                            where materialID = (?)
                            """
                
                cursor.execute(sql_query, (newName, newDesc, newUnits, id))
                connection.commit()

                
                self.msg.setWindowTitle("Success")
                self.msg.setText("Edit done successfully.")
                self.msg.show()

                self.materialUpdated.emit()
            else:
                self.msg.setWindowTitle("Error")
                self.msg.setText("Enter complete information")    
                self.msg.show()  

        
