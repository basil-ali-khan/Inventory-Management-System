# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView

from ConnectionString import connection, cursor

class SaleReportScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SaleReportScreen, self).__init__()

        uic.loadUi('Screens/SaleReport.ui', self)

        self.generateItemButton.clicked.connect(self.GenerateReport)
        self.moneytext.setReadOnly(True)
        self.itemText.setReadOnly(True)

        self.moneyfrom.setEnabled(False)
        self.moneyto.setEnabled(False)
        self.itemFrom.setEnabled(False)
        self.itemTo.setEnabled(False)

        self.radioButton_2.toggled.connect(self.toggleMoneyDateFields)
        self.radioButton_4.toggled.connect(self.toggleCustomerDateFields)

    def toggleMoneyDateFields(self):
        # Enable/disable money date fields based on the state of radioButton_2
        self.moneyfrom.setEnabled(self.radioButton_2.isChecked())
        self.moneyto.setEnabled(self.radioButton_2.isChecked())

    def toggleCustomerDateFields(self):
        # Enable/disable vendor date fields based on the state of radioButton_4
        self.itemFrom.setEnabled(self.radioButton_4.isChecked())
        self.itemTo.setEnabled(self.radioButton_4.isChecked())

    def GenerateReport(self):
        if (not self.radioButton.isChecked() and not self.radioButton_2.isChecked() and not self.radioButton_3.isChecked() and not self.radioButton_4.isChecked()):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select the timeframe.")
            self.msg.show()
            return

        # for best selling item all time

        if self.radioButton_3.isChecked():
            query = """
                SELECT STRING_AGG(productInfo, CHAR(13) + CHAR(10)) as BestSellingProducts
                FROM (
                    SELECT TOP 1 WITH TIES
                        productName + ' (Description: ' + description + ', Quantity: ' + CAST(SUM(quantity) AS NVARCHAR) + ')' as productInfo
                    FROM Sale S
                    JOIN SaleProduct SP ON S.saleID = SP.saleID
                    JOIN Products P ON SP.productID = P.productID
                    GROUP BY productName, description
                    ORDER BY SUM(quantity) DESC
                ) AS BestSellingProductsSubquery
            """

            cursor.execute(query)
            result = cursor.fetchone()
            self.itemText.setText(
                str(result[0]) if result and result[0] is not None else "N/A")

        # for best selling item within a specific timeframe

        if self.radioButton_4.isChecked():
            item_from_date = self.itemFrom.date().toString("yyyy-MM-dd")
            item_to_date = self.itemTo.date().toString("yyyy-MM-dd")

            query = f"""
                SELECT STRING_AGG(productInfo, CHAR(13) + CHAR(10)) as BestSellingProducts
                FROM (
                    SELECT TOP 1 WITH TIES
                        productName + ' (Description: ' + description + ', Quantity: ' + CAST(SUM(quantity) AS NVARCHAR) + ')' as productInfo
                    FROM Sale S
                    JOIN SaleProduct SP ON S.saleID = SP.saleID
                    JOIN Products P ON SP.productID = P.productID
                    WHERE S.saleDate BETWEEN '{item_from_date}' AND '{item_to_date}'
                    GROUP BY productName, description
                    ORDER BY SUM(quantity) DESC
                ) AS BestSellingProductsSubquery
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.itemText.setText(
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
