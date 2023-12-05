# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditCustomerClass

from ConnectionString import connection, cursor

class TopCustomerScreen(QtWidgets.QMainWindow):
    def __init__(self) :
        super(TopCustomerScreen, self).__init__()

        uic.loadUi('Screens/TopCustomers.ui', self)
        

        self.setWindowTitle("Top Customers")

        self.okButton.clicked.connect(self.PopulateTopCustomerTable)

    def PopulateTopCustomerTable(self):
        noOfCustomers = self.noOfCustomers.text()
        if not noOfCustomers or not noOfCustomers.isdigit():
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter a positive numeric value for number of customers to be searched.")
            self.msg.show()
            return
        
        sql_query = """
                    select top (?) Customer.customerID, Customer.customerName, gender, contactNumber, backupContact, email, [address],SUM(totalAmount) 
                    from Sale inner join Customer on Sale.customerID = Customer.customerID 
                    group by Customer.customerID, Customer.customerName, gender, contactNumber, backupContact, email, [address]
                    order by SUM(totalAmount) desc
                    """
        cursor.execute(sql_query, int(noOfCustomers))

        self.topCustomerTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor):
            self.topCustomerTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.topCustomerTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

