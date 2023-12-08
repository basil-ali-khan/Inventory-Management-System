# Inventory-Management-System
Packages Required:
  1. pyodbc
  2. pyqt6

To run the program, first make the following changes to the ConnectionString.py file:
  1. Replace the server-name with the server-name from the SSMS on your device
  2. If you are not using Windows Authentication, change 'use_windows_authentication' value to false and give the appropriate username and password
  3. Open Microsoft SQL Server Management Studio
  4. Open the Inventory_Management_System_Script sql file in SSMS and run the file
  5. In your IDE terminal, run the command `python main.py` to run the program
