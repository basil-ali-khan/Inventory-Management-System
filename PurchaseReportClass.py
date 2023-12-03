# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView

from ConnectionString import connection, cursor


class PurchaseReportScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(PurchaseReportScreen, self).__init__()

        uic.loadUi('Screens/PurchaseReport.ui', self)

        self.generate.clicked.connect(self.GenerateReport)
        self.moneytext.setReadOnly(True)
        self.vendortext.setReadOnly(True)

        self.moneyfrom.setEnabled(False)
        self.moneyto.setEnabled(False)
        self.vendorfrom.setEnabled(False)
        self.vendorto.setEnabled(False)

        self.radioButton_2.toggled.connect(self.toggleMoneyDateFields)
        self.radioButton_4.toggled.connect(self.toggleVendorDateFields)

    def toggleMoneyDateFields(self):
        # Enable/disable money date fields based on the state of radioButton_2
        self.moneyfrom.setEnabled(self.radioButton_2.isChecked())
        self.moneyto.setEnabled(self.radioButton_2.isChecked())

    def toggleVendorDateFields(self):
        # Enable/disable vendor date fields based on the state of radioButton_4
        self.vendorfrom.setEnabled(self.radioButton_4.isChecked())
        self.vendorto.setEnabled(self.radioButton_4.isChecked())


    def GenerateReport(self):
        if (not self.radioButton.isChecked() and not self.radioButton_2.isChecked()) or (not self.radioButton_3.isChecked() and not self.radioButton_4.isChecked()):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select the timeframe.")
            self.msg.show()
            return

        if self.radioButton_3.isChecked():
            query = "select vendorName from Vendor where vendorID in (select top 1 vendorID from Purchase group by vendorID order by count(*) desc)"
            cursor.execute(query)
            result = cursor.fetchone()
            self.vendortext.setText(str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton_4.isChecked():
            vendor_from_date = self.vendorfrom.date().toString("yyyy-MM-dd")
            vendor_to_date = self.vendorto.date().toString("yyyy-MM-dd")

            # Query to find the most frequented vendor within the specified time frame
            query = f"""
                SELECT STRING_AGG(vendorName, ', ') as vendorNames
                FROM Vendor
                WHERE vendorID IN (
                    SELECT TOP 1 WITH TIES vendorID
                    FROM Purchase
                    WHERE purchaseDate BETWEEN '{vendor_from_date}' AND '{vendor_to_date}'
                    GROUP BY vendorID
                    ORDER BY COUNT(*) DESC
                )
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.vendortext.setText(str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton.isChecked():
            query = "select sum(totalAmount) from Purchase"
            cursor.execute(query)
            result = cursor.fetchone()
            self.moneytext.setText("RS. " + str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton_2.isChecked():
            money_from_date = self.moneyfrom.date().toString("yyyy-MM-dd")
            money_to_date = self.moneyto.date().toString("yyyy-MM-dd")

            # Query to calculate the sum of the total amount for purchases during the specified time frame
            query = f"""
                SELECT SUM(totalAmount) as totalAmountSum
                FROM Purchase
                WHERE purchaseDate BETWEEN '{money_from_date}' AND '{money_to_date}'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.moneytext.setText("RS. " + str(result[0]) if result and result[0] is not None else "N/A")






            

