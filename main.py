# import typing
# from PyQt6 import QtCore, QtWidgets, uic
# from PyQt6.QtCore import QDate
# from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
# import sys
# import pyodbc
# import VendorClass
# import CustomerClass
# import MaterialClass
# import ProductsClass

# from ConnectionString import connection, cursor

# class UI(QtWidgets.QMainWindow):
#     def __init__(self):
#         # Call the inherited classes __init__ method
#         super(UI, self).__init__()

#         # Load the .ui file
#         uic.loadUi('Screens/UserAuthentication.ui', self)
#         self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

#         self.username.setPlaceholderText("Username")
#         self.password.setPlaceholderText("Password")

#         self.vendorsButton.setEnabled(False)
#         self.customerButton.setEnabled(False)
#         self.productsButton.setEnabled(False)
#         self.salesButton.setEnabled(False)
#         self.materialButton.setEnabled(False)
#         self.purchaseButton.setEnabled(False)
#         self.logoutButton.setEnabled(False)

#         self.loginButton.clicked.connect(self.CheckPrivilege)
#         self.vendorsButton.clicked.connect(self.OpenVendorScreen)
#         self.customerButton.clicked.connect(self.OpenCustomerScreen)
#         self.logoutButton.clicked.connect(self.Logout)

#         self.logged_in = False

#         self.productsButton.clicked.connect(self.OpenProductsScreen)
#         self.materialButton.clicked.connect(self.OpenMaterialScreen)

#     def OpenProductsScreen(self):
#         self.products = ProductsClass.ProductScreen()
#         self.products.show()

#     def OpenMaterialScreen(self):
#         self.materials = MaterialClass.MaterialScreen()
#         self.materials.show()

#     def OpenCustomerScreen(self):
#         self.customer = CustomerClass.CustomerScreen()
#         self.customer.show()

#     def OpenVendorScreen(self):
#         self.vendor = VendorClass.VendorScreen()
#         self.vendor.show()

#     def CheckPrivilege(self):
#         username = self.username.text()
#         password = self.password.text()
#         sql_query = "select privilege from [User] where userName = ? and password = ?"
#         cursor.execute(sql_query, (username, password))
#         result = cursor.fetchone()
#         if result is not None:
#             result = result[0]
#             if result == 'Admin':
#                 self.vendorsButton.setEnabled(True)
#                 self.customerButton.setEnabled(True)
#                 self.productsButton.setEnabled(True)
#                 self.salesButton.setEnabled(True)
#                 self.materialButton.setEnabled(True)
#                 self.purchaseButton.setEnabled(True)
#             elif result == 'User':
#                 self.vendorsButton.setEnabled(False)
#                 self.customerButton.setEnabled(False)
#                 self.productsButton.setEnabled(False)
#                 self.salesButton.setEnabled(True)
#                 self.materialButton.setEnabled(False)
#                 self.purchaseButton.setEnabled(False)
#             self.logged_in = True
#             self.logoutButton.setEnabled(True)
#             self.loginButton.setEnabled(False)
            
#         else:
#             self.addMsg = QtWidgets.QMessageBox()
#             self.addMsg.setWindowTitle('Error')
#             self.addMsg.setText('Invalid credentials')
#             self.addMsg.show()
#             self.vendorsButton.setEnabled(False)
#             self.customerButton.setEnabled(False)
#             self.productsButton.setEnabled(False)
#             self.salesButton.setEnabled(False)
#             self.materialButton.setEnabled(False)
#             self.purchaseButton.setEnabled(False)

#         self.username.clear()
#         self.password.clear()
#         self.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)  # So that the cursor does not go the password entry

#     def Logout(self):
#         self.vendorsButton.setEnabled(False)
#         self.customerButton.setEnabled(False)
#         self.productsButton.setEnabled(False)
#         self.salesButton.setEnabled(False)
#         self.materialButton.setEnabled(False)
#         self.purchaseButton.setEnabled(False)
#         self.logoutButton.setEnabled(False)
#         self.logged_in = False
#         self.logoutButton.setEnabled(False)
#         self.loginButton.setEnabled(True)
#         self.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)  # So that the cursor does not go the password entry

# app = QApplication(sys.argv)
# loginScreen = UI()
# loginScreen.show()
# sys.exit(app.exec())


# Importing essential modules
import typing
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMessageBox,QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc
import VendorClass
import ProductsClass
import MaterialClass
import EditVendorClass
import CustomerClass
from PurchaseClass import PurchaseScreen

from ConnectionString import connection, cursor

class UI(QtWidgets.QMainWindow):   
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        
        # Load the .ui file
        uic.loadUi('Screens/UserAuthentication.ui', self)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.username.setPlaceholderText("Username")
        self.password.setPlaceholderText("Password")
        ###hardcoded for now, will later be enabled only if user has admin priveleges

        self.vendorsButton.setEnabled(False)
        self.customerButton.setEnabled(False)
        self.productsButton.setEnabled(False)
        self.salesButton.setEnabled(False)
        self.materialButton.setEnabled(False)
        self.purchaseButton.setEnabled(False)
        self.logoutButton.setEnabled(False)

        self.loginButton.clicked.connect(self.CheckPrivilege)
        self.vendorsButton.clicked.connect(self.OpenVendorScreen)
        self.productsButton.clicked.connect(self.OpenProductsScreen)
        self.materialButton.clicked.connect(self.OpenMaterialScreen)
        self.customerButton.clicked.connect(self.OpenCustomerScreen)
        self.purchaseButton.clicked.connect(self.OpenPurchaseScreen)
        self.logoutButton.clicked.connect(self.Logout)

        self.logged_in = False

    def OpenPurchaseScreen(self):
        self.purchase = PurchaseScreen()
        self.purchase.show()

    def OpenProductsScreen(self):
        self.products = ProductsClass.ProductScreen()
        self.products.show()

    def OpenMaterialScreen(self):
        self.materials = MaterialClass.MaterialScreen()
        self.materials.show()

    def OpenVendorScreen(self):
        self.vendor = VendorClass.VendorScreen()
        self.vendor.show()

    def OpenCustomerScreen(self):
        self.customer = CustomerClass.CustomerScreen()
        self.customer.show()
        
    def CheckPrivilege(self):
        username = self.username.text()
        password = self.password.text()
        sql_query = "select privilege from [User] where userName = ? and password = ?"
        cursor.execute(sql_query, (username, password))
        result = cursor.fetchone()
        if result is not None:
            result = result[0]
            if result == 'Admin':
                self.vendorsButton.setEnabled(True)
                self.customerButton.setEnabled(True)
                self.productsButton.setEnabled(True)
                self.salesButton.setEnabled(True)
                self.materialButton.setEnabled(True)
                self.purchaseButton.setEnabled(True)
            elif result == 'User':
                self.vendorsButton.setEnabled(False)
                self.customerButton.setEnabled(False)
                self.productsButton.setEnabled(False)
                self.salesButton.setEnabled(True)
                self.materialButton.setEnabled(False)
                self.purchaseButton.setEnabled(False)
            self.logged_in = True
            self.logoutButton.setEnabled(True)
            self.loginButton.setEnabled(False)
            
        else:
            self.addMsg = QtWidgets.QMessageBox()
            self.addMsg.setWindowTitle('Error')
            self.addMsg.setText('Invalid credentials')
            self.addMsg.show()
            self.vendorsButton.setEnabled(False)
            self.customerButton.setEnabled(False)
            self.productsButton.setEnabled(False)
            self.salesButton.setEnabled(False)
            self.materialButton.setEnabled(False)
            self.purchaseButton.setEnabled(False)

        self.username.clear()
        self.password.clear()
        self.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)  # So that the cursor does not go the password entry

    def Logout(self):
        self.vendorsButton.setEnabled(False)
        self.customerButton.setEnabled(False)
        self.productsButton.setEnabled(False)
        self.salesButton.setEnabled(False)
        self.materialButton.setEnabled(False)
        self.purchaseButton.setEnabled(False)
        self.logoutButton.setEnabled(False)
        self.logged_in = False
        self.logoutButton.setEnabled(False)
        self.loginButton.setEnabled(True)
        self.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)  # So that the cursor does not go the password entry

app = QApplication(sys.argv)
loginScreen = UI()
loginScreen.show()
sys.exit(app.exec())