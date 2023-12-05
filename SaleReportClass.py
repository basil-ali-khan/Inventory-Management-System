# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView

from ConnectionString import connection, cursor

class SaleReportScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SaleReportScreen, self).__init__()

        uic.loadUi('Screens/SaleReport.ui', self)

        self.setWindowTitle("Sale Report")

        self.generateItemButton.clicked.connect(self.GenerateItemReport)
        self.generateRevenueButton.clicked.connect(self.GenerateRevenueReport)
        self.revenueText.setReadOnly(True)
        self.itemText.setReadOnly(True)

        self.itemFrom.setEnabled(False)
        self.itemTo.setEnabled(False)
        self.dateEdit.setEnabled(False)

        self.radioButton_4.toggled.connect(self.toggleCustomerDateFields)
        self.radioButton_allTime.toggled.connect(self.toggleRevenueDate)
        self.radioButton_yearly.toggled.connect(self.toggleRevenueDate)
        self.radioButton_monthly.toggled.connect(self.toggleRevenueDate)
    def toggleRevenueDate(self):
        enabled = (
            self.radioButton_yearly.isChecked() or
            self.radioButton_monthly.isChecked() 
        )
        self.dateEdit.setEnabled(enabled)

    def toggleCustomerDateFields(self):
        # Enable/disable vendor date fields based on the state of radioButton_4
        self.itemFrom.setEnabled(self.radioButton_4.isChecked())
        self.itemTo.setEnabled(self.radioButton_4.isChecked())

    def GenerateItemReport(self):
        if (not self.radioButton_3.isChecked() and not self.radioButton_4.isChecked()):
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


    def GenerateRevenueReport(self):
        if (not self.radioButton_allTime.isChecked() and not self.radioButton_yearly.isChecked() and not self.radioButton_monthly.isChecked()):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select the timeframe.")
            self.msg.show()
            return
        # Check the selected timeframe
        if self.radioButton_allTime.isChecked():
            # Fetch revenue data for all time
            query = """
                SELECT YEAR(saleDate) as Year, SUM(totalAmount) as Revenue
                FROM Sale
                GROUP BY YEAR(saleDate)
                ORDER BY YEAR(MIN(saleDate))
            """
            cursor.execute(query)
            result = cursor.fetchall()

            self.revenueTable.setRowCount(len(result))
            self.revenueTable.setColumnCount(2)
            self.revenueTable.setHorizontalHeaderLabels(["Year", "Revenue"])

            for row, (year, revenue) in enumerate(result):
                # Concatenate "RS. " with the revenue values
                formatted_revenue = "RS. " + str(revenue)
                self.revenueTable.setItem(row, 0, QTableWidgetItem(str(year)))
                self.revenueTable.setItem(row, 1, QTableWidgetItem(formatted_revenue))

            self.revenueTable.resizeColumnsToContents()

            # Calculate and display the total revenue for all years
            total_revenue = sum(revenue for _, revenue in result)
            formatted_total_revenue = "RS. " + str(total_revenue)
            self.revenueText.setText(formatted_total_revenue)

        elif self.radioButton_yearly.isChecked():
            # Fetch revenue data for the selected year
            selected_year = self.dateEdit.date().year()
            query = f"""
                SELECT LEFT(DATENAME(MONTH, saleDate), 3) as Month, SUM(totalAmount) as Revenue
                FROM Sale
                WHERE YEAR(saleDate) = {selected_year}
                GROUP BY DATENAME(MONTH, saleDate)
                ORDER BY MONTH(MIN(saleDate))
            """
            cursor.execute(query)
            result = cursor.fetchall()
            self.revenueTable.setRowCount(len(result))
            self.revenueTable.setColumnCount(2)
            self.revenueTable.setHorizontalHeaderLabels(["Month", "Revenue"])

            for row, (month, revenue) in enumerate(result):
                # Concatenate "RS. " with the revenue values
                formatted_revenue = "RS. " + str(revenue)
                self.revenueTable.setItem(row, 0, QTableWidgetItem(month))
                self.revenueTable.setItem(row, 1, QTableWidgetItem(formatted_revenue))

            self.revenueTable.resizeColumnsToContents()

            # Calculate and display the total revenue for the selected year
            total_revenue = sum(revenue for _, revenue in result)
            formatted_total_revenue = "RS. " + str(total_revenue)
            self.revenueText.setText(formatted_total_revenue)

        elif self.radioButton_monthly.isChecked():
            # Fetch revenue data for the selected month
            selected_month = self.dateEdit.date().month()
            selected_year = self.dateEdit.date().year()

            query = f"""
                SELECT DAY(saleDate) as Day, SUM(totalAmount) as Revenue
                FROM Sale
                WHERE YEAR(saleDate) = {selected_year} AND MONTH(saleDate) = {selected_month}
                GROUP BY DAY(saleDate)
                ORDER BY DAY(saleDate)
            """
            cursor.execute(query)
            result = cursor.fetchall()
            self.revenueTable.setRowCount(len(result))
            self.revenueTable.setColumnCount(2)
            self.revenueTable.setHorizontalHeaderLabels(["Date", "Revenue"])

            for row, (day, revenue) in enumerate(result):
                # Concatenate "RS. " with the revenue values
                formatted_revenue = "RS. " + str(revenue)
                self.revenueTable.setItem(row, 0, QTableWidgetItem(str(day)))
                self.revenueTable.setItem(row, 1, QTableWidgetItem(formatted_revenue))

            self.revenueTable.resizeColumnsToContents()

            # Calculate and display the total revenue for the selected month
            total_revenue = sum(revenue for _, revenue in result)
            formatted_total_revenue = "RS. " + str(total_revenue)
            self.revenueText.setText(formatted_total_revenue)
        