# 1.Print/displayrecords from your database/tables.
# 2.Queryfor data/results with various parameters/filters
# 3.Create a new record
# 4.Delete records (soft delete function would be ideal)
# 5.Update records
# 6.Make use of transactions (commit & rollback)
# 7.Generate reports that can be exported (excel or csv format)
# 8.One query must perform an aggregation/group-by clause
# 9.One query must contain a sub-query.
# 10.Two queries must involve joins across at least 3 tables
# 11.Enforce referential integrality(PK/FK Constraints)
# 12.Include Database Views, Indexes

import tkinter as tk
from tkinter import ttk
import mysql.connector
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
from faker import Faker

# variable = StringVar(self.master)
# variable.set("one") # default value
# w = OptionMenu(self.master, variable, "one", "two", "three")
# w.pack()

#     def create_window(self):
#         window = Toplevel(self.master)
#         window.title("New Window")
#         window.geometry("200x200")
#         Label(window, text="Hello").pack()
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

HOST_IP = os.environ.get("HOST_IP")
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWD")
DB = os.environ.get("DB")

# Establish a Connection object with a MySQL database
def create_connection(host_ip, user_name, user_pw, database):
    connection = None

    print("Connecting to \'" + user_name + "\'" + "@" "\'" + host_ip + "\'" "...")

    try:
        connection = mysql.connector.connect(
            host=host_ip,
            user=user_name,
            passwd=user_pw,
            db=database,
            connect_timeout=30
        )

        print("Connection to \'" + user_name + "\' successful")

    except mysql.connector.Error as e:
        print(e)

    return connection

class Button(tk.Button):
    def __init__(self, container, text, row, column, ipady=30, ipadx=30, command=""):
        super().__init__(container, text=text, command=command)
        self.grid(row=row, column=column, padx=30, pady=30, ipadx=ipadx, ipady=ipady, sticky=tk.NSEW)

class Label(tk.Label):
    def __init__(self, container, text, row, column):
        super().__init__(container, text=text)
        self.config(font = ("Courier", 14))
        self.grid(row=row, column=column)

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.init_widgets()

    def init_widgets(self):
        b1 = Button(self, "Table 1", 2, 1, ipady=50, command=lambda: self.controller.show_frame("OrderFrame"))
        b2 = Button(self, "Table 2", 2, 2)
        b3 = Button(self, "Table 3", 2, 3, ipadx=50)
        b4 = Button(self, "Table 4", 3, 1, ipady=50)
        b5 = Button(self, "Table 5", 3, 2)
        b6 = Button(self, "Table 6", 3, 3, ipadx=50)
        b7 = Button(self, "Table 7", 4, 1, ipady=50)
        b8 = Button(self, "Table 8", 4, 3, ipadx=50)
        l = Label(self, "Menya Le Nood", 0, 2)

    def greet(self):
        print("hello")

class OrderFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("MainFrame"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menya Le Nood")
        self.geometry("1280x720")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self)
        container.pack(side="top", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (OrderFrame, MainFrame):
            page_name = F.__name__
            print(page_name)
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

"""
END GUI
"""

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)

    return result

def get_order(connection, table_no):
    table_no = str(table_no)
    query = "SELECT Name, Quantity FROM `Order` WHERE TableNum =" + table_no
    print(execute_read_query(connection, query))

def get_menu(connection):
    query = "SELECT * from `MenuList`"
    res = execute_read_query(connection, query)
    for thing in res:
        print(thing)
    print(res)

# app = App()
# app.mainloop()
db = create_connection(HOST_IP, USER_NAME, PASSWORD, DB)
get_order(db, 1)
get_menu(db)
cursor = db.cursor()
cursor.execute("SELECT * FROM `Order`")
result = cursor.fetchall()
print(result)