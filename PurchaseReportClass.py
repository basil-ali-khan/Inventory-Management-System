# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView

from ConnectionString import connection, cursor


class PurchaseReportScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(PurchaseReportScreen, self).__init__()

        uic.loadUi('Screens/PurchaseReport.ui', self)
        self.setWindowTitle("Purchase Report")

        self.generate.clicked.connect(self.GenerateReport)
        self.moneytext.setReadOnly(True)
        self.materialText.setReadOnly(True)

        self.moneyfrom.setEnabled(False)
        self.moneyto.setEnabled(False)
        self.materialfrom.setEnabled(False)
        self.materialto.setEnabled(False)

        self.radioButton_2.toggled.connect(self.toggleMoneyDateFields)
        self.radioButton_4.toggled.connect(self.toggleVendorDateFields)

    def toggleMoneyDateFields(self):
        # Enable/disable money date fields based on the state of radioButton_2
        self.moneyfrom.setEnabled(self.radioButton_2.isChecked())
        self.moneyto.setEnabled(self.radioButton_2.isChecked())

    def toggleVendorDateFields(self):
        # Enable/disable vendor date fields based on the state of radioButton_4
        self.materialfrom.setEnabled(self.radioButton_4.isChecked())
        self.materialto.setEnabled(self.radioButton_4.isChecked())

    def GenerateReport(self):
        if (not self.radioButton.isChecked() and not self.radioButton_2.isChecked() and not self.radioButton_3.isChecked() and not self.radioButton_4.isChecked()):
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select the timeframe.")
            self.msg.show()
            return

        if self.radioButton_3.isChecked():
            query = """
                SELECT STRING_AGG(materialInfo, CHAR(13) + CHAR(10)) as MostPurchasedMaterials
                FROM (
                    SELECT TOP 1 WITH TIES
                        materialName + ' (Description: ' + description + ', Quantity: ' + CAST(SUM(quantity) AS NVARCHAR) + ')' as materialInfo
                    from Purchase P join PurchaseMaterial PM on P.purchaseID = PM.purchaseID join Material M on PM.materialID = M.materialID
                    GROUP BY materialName, description
                    ORDER BY SUM(quantity) DESC
                ) AS MostPurchasedMaterialsSubquery
            """

            cursor.execute(query)
            result = cursor.fetchone()
            self.materialText.setText(
                str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton_4.isChecked():
            material_from_date = self.materialfrom.date().toString("yyyy-MM-dd")
            material_to_date = self.materialto.date().toString("yyyy-MM-dd")

            # Query to find the most frequented vendor within the specified time frame
            query = f"""
                SELECT STRING_AGG(materialInfo, CHAR(13) + CHAR(10)) as MostPurchasedMaterials
                FROM (
                    SELECT TOP 1 WITH TIES
                        materialName + ' (Description: ' + description + ', Quantity: ' + CAST(SUM(quantity) AS NVARCHAR) + ')' as materialInfo
                    FROM Purchase P
                        JOIN PurchaseMaterial PM ON P.purchaseID = PM.purchaseID
                        JOIN Material M ON PM.materialID = M.materialID
                    WHERE P.purchaseDate BETWEEN '{material_from_date}' AND '{material_to_date}'
                    GROUP BY materialName, description
                    ORDER BY SUM(quantity) DESC
                ) AS MostPurchasedMaterialsSubquery
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.materialText.setText(
                str(result[0]) if result and result[0] is not None else "N/A")

        if self.radioButton.isChecked():
            query = "select sum(totalAmount) from Purchase"
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
                FROM Purchase
                WHERE purchaseDate BETWEEN '{money_from_date}' AND '{money_to_date}'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            self.moneytext.setText(
                "RS. " + str(result[0]) if result and result[0] is not None else "N/A")