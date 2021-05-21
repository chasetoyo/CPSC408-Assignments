# CPSC 408 Final Project (Restaurant POS Using MySQL and Tkinter)

## Chase Toyofuku-Souza

## Table of Contents

* [About](#about)
* [Required Dependencies](#Required-Dependencies)
* [Instructions](#Instructions)
* [Files](#Files)
* [Notes](#Notes)
* [References](#References)

## About
Final project for CPSC 408 (Database Management) at Chapman University. A GUI built in Python using Tkinter, which connects to a Cloud MySQL database, and allows the user to create reservations, open tabs, close tabs, and generate daily reports of sales.

## Required-Dependencies
* MySQL Connector
```sh
pip3 install mysql-connector-python
```
* dotenv
```sh
pip3 install python-dotenv
```

## Instructions
1. Populate [`.env`](.env) file with the correct MySQL connection information
2. Run the application
```sh
python3 final.py
```
3. Choose a table and enter valid reservation information
	- Email: 'xxx@email.xxx', Party Size: integer, Reservation Time: *YYYY-MM-DD HH:MM:SS*
	- OR Enter a valid reservation ID if you know it
4. Select on an item to add it to the order, finalize order with submit
5. Select *Close Order* to close an order and have it appear in a report
6. On the menu with table numbers, enter date string in the form *YYYY-MM-DD* to get a csv report

### Files
- [`final.py`](final.py)
- [`Credential File`](.env)

### Notes
Must enter valid credentials in [`.env`](.env).

### References
- https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
- https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
- https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
- https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
- https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
- https://stackoverflow.com/questions/16373887/how-to-set-the-text-value-content-of-an-entry-widget-using-a-button-in-tkinter
- https://stackoverflow.com/questions/30614279/python-tkinter-tree-get-selected-item-values/30615520
- https://www.pythontutorial.net/tkinter/tkraise/
- https://www.pythontutorial.net/tkinter/tkinter-frame/
- https://pythonguides.com/python-tkinter-treeview/
- https://stackoverflow.com/questions/12364981/how-to-delete-tkinter-widgets-from-a-window
- https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
- https://docs.python.org/3/library/tkinter.ttk.html