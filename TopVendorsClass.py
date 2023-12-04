# # Importing essential modules
# import typing
# from PyQt6 import QtCore, QtWidgets, uic
# from PyQt6.QtCore import QDate
# from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
# import sys
# import pyodbc
# import EditCustomerClass

# from ConnectionString import connection, cursor

# class TopVendorScreen(QtWidgets.QMainWindow):
#     def __init__(self) :
#         super(TopVendorScreen, self).__init__()

#         uic.loadUi('Screens/TopVendors.ui', self)

#         self.setWindowTitle("Top Vendors")

#         self.okButton.clicked.connect(self.PopulateTopVendorTable)

#     def PopulateTopVendorTable(self):
#         noOfVendors = self.noOfVendors.text()
#         if not noOfVendors or not noOfVendors.isdigit():
#             self.msg = QtWidgets.QMessageBox()
#             self.msg.setWindowTitle("Error")
#             self.msg.setText("Please enter a positive numeric value for number of customers to be searched.")
#             self.msg.show()
#             return
        
#         sql_query = """
#                     select top (?) Vendor.vendorID, Vendor.vendorName, contactNumber, backupContact, email, [address],SUM(totalAmount) 
#                     from Purchase inner join Vendor on Purchase.vendorID = Vendor.vendorID 
#                     group by Vendor.vendorID, Vendor.vendorName, contactNumber, backupContact, email, [address]
#                     order by SUM(totalAmount) desc
# #                     """
#         cursor.execute(sql_query, int(noOfVendors))

#         self.topVendorTable.setRowCount(0)
#         for row_number, row_data in enumerate(cursor):
#             self.topVendorTable.insertRow(row_number)
#             for column_number, data in enumerate(row_data):
#                 self.topVendorTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))


# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import EditVendorClass

from ConnectionString import connection, cursor

class TopVendorScreen(QtWidgets.QMainWindow):
    def __init__(self) :
        super(TopVendorScreen, self).__init__()

        uic.loadUi('Screens/TopVendors.ui', self)

        self.setWindowTitle("Top Vendors")

        self.okButton.clicked.connect(self.PopulateTopVendorTable)

    def PopulateTopVendorTable(self):
        noOfVendors = self.noOfVendors.text()
        if not noOfVendors or not noOfVendors.isdigit():
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please enter a positive numeric value for number of Vendors to be searched.")
            self.msg.show()
            return
        
        sql_query = """
                    select top (?) Vendor.vendorID, Vendor.vendorName, contactNumber, backupContact, email, [address],SUM(totalAmount) 
                    from Purchase inner join Vendor on Purchase.vendorID = Vendor.vendorID 
                    group by Vendor.vendorID, Vendor.vendorName, contactNumber, backupContact, email, [address]
                    order by SUM(totalAmount) desc
      """
        
        cursor.execute(sql_query, int(noOfVendors))

        self.topVendorTable.setRowCount(0)
        for row_number, row_data in enumerate(cursor):
            self.topVendorTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.topVendorTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

