# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView

from ConnectionString import connection, cursor


class SaleReportScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SaleReportScreen, self).__init__()

        uic.loadUi('Screens/SaleReport.ui', self)

        self.generateButton.clicked.connect(self.GenerateReport)
        self.moneytext.setReadOnly(True)
        self.customerText.setReadOnly(True)

        self.moneyfrom.setEnabled(False)
        self.moneyto.setEnabled(False)
        self.customerfrom.setEnabled(False)
        self.customerto.setEnabled(False)

        self.radioButton_2.toggled.connect(self.toggleMoneyDateFields)
        self.radioButton_4.toggled.connect(self.toggleCustomerDateFields)

    def toggleMoneyDateFields(self):
        # Enable/disable money date fields based on the state of radioButton_2
        self.moneyfrom.setEnabled(self.radioButton_2.isChecked())
        self.moneyto.setEnabled(self.radioButton_2.isChecked())

    def toggleCustomerDateFields(self):
        # Enable/disable vendor date fields based on the state of radioButton_4
        self.customerfrom.setEnabled(self.radioButton_4.isChecked())
        self.customerto.setEnabled(self.radioButton_4.isChecked())

    def GenerateReport(self):
        if (not self.radioButton.isChecked() and not self.radioButton_2.isChecked()) or (not self.radioButton_3.isChecked() and not self.radioButton_4.isChecked()):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select the timeframe.")
            self.msg.show()
            return

        if self.radioButton_3.isChecked():
            query = f"""
                SELECT STRING_AGG(customerName, ', ') as customerNames
                FROM Customer
                WHERE customerID IN (
                    SELECT TOP 1 WITH TIES customerID
                    FROM Sale
                    GROUP BY customerID
                    ORDER BY COUNT(*) DESC
                )
            """

            cursor.execute(query)
            result = cursor.fetchone()
            self.customerText.setText(
                str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton_4.isChecked():
            customer_from_date = self.customerfrom.date().toString("yyyy-MM-dd")
            customer_to_date = self.customerto.date().toString("yyyy-MM-dd")

            # Query to find the most frequented vendor within the specified time frame
            query = f"""
                SELECT STRING_AGG(customerName, ', ') as customerNames
                FROM Customer
                WHERE customerID IN (
                    SELECT TOP 1 WITH TIES customerID
                    FROM Sale
                    WHERE saleDate BETWEEN '{customer_from_date}' AND '{customer_to_date}'
                    GROUP BY customerID
                    ORDER BY COUNT(*) DESC
                )
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.customerText.setText(
                str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton.isChecked():
            query = "select sum(totalAmount) from Sale"
            cursor.execute(query)
            result = cursor.fetchone()
            self.moneytext.setText(
                "RS. " + str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton_2.isChecked():
            money_from_date = self.moneyfrom.date().toString("yyyy-MM-dd")
            money_to_date = self.moneyto.date().toString("yyyy-MM-dd")

            # Query to calculate the sum of the total amount for purchases during the specified time frame
            query = f"""
                SELECT SUM(totalAmount) as totalAmountSum
                FROM Sale
                WHERE saleDate BETWEEN '{money_from_date}' AND '{money_to_date}'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.moneytext.setText(
                "RS. " + str(result[0]) if result and result[0] is not None else "N/A")
