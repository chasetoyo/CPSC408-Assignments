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
    def __init__(self, container, text, relheight, relwidth, relx, rely, command):
        super().__init__(container, text=text, command=command)
        self.text = text
        self.place(relheight=relheight, relwidth=relwidth, relx=relx,rely=rely)

class Label(tk.Label):
    def __init__(self, container, text, rely, relx, anchor="center"):
        super().__init__(container, text=text)
        self.config(font = ("Courier", 14))
        self.place(relx=relx, rely=rely, anchor=anchor)

class MainFrame(tk.Frame):
    def __init__(self, parent, controller, table_num=0):
        tk.Frame.__init__(self, parent,width=1280,height=720)
        self.controller = controller
        self.grid(row=0, column=0)
        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.init_widgets()
        self.table_num = table_num

    def init_widgets(self):
              # container, text, relheight, relwidth, relx, rely, command
        b1 = Button(self, "Table 1", .2, .125, .29, .1, lambda: self.controller.show_frame("OrderFrame", 1))
        b2 = Button(self, "Table 2", .2, .1, .44, .1, lambda: self.controller.show_frame("OrderFrame",2))
        b3 = Button(self, "Table 3", .2, .175, .57, .1, lambda: self.controller.show_frame("OrderFrame",3))

        b4 = Button(self, "Table 4", .2, .125, .29, .35, lambda: self.controller.show_frame("OrderFrame",4))
        b5 = Button(self, "Table 5", .2, .1, .44, .35, lambda: self.controller.show_frame("OrderFrame",5))
        b6 = Button(self, "Table 6", .2, .175, .57, .35, lambda: self.controller.show_frame("OrderFrame",6))

        b7 = Button(self, "Table 7", .2, .125, .29, .6, lambda: self.controller.show_frame("OrderFrame",7))
        b8 = Button(self, "Table 8", .2, .175, .57, .6, lambda: self.controller.show_frame("OrderFrame", 8))

        l = Label(self, "Menya Le Nood", .05, .495)

    def greet(self):
        print("hello")

class OrderFrame(tk.Frame):

    def __init__(self, parent, controller, table_num):
        tk.Frame.__init__(self, parent, width=1280,height=720)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.table_num = table_num

        db = create_connection(HOST_IP, USER_NAME, PASSWORD, DB)

        self.order = get_order(db, self.table_num)
        self.menu = get_menu(db)
        self.menu_names = get_menu_names(self.menu)
        self.tab_id = get_tab_id(db, table_num)
        self.change_dict = {}

        # frame title
        label = tk.Label(self, text="Table " + str(self.table_num), font=("Arial", 25))
        label.place(relx=0,rely=0)

        # submit button
        submit = Button(self, "Submit", .1, .1, 0, .45, command=lambda: self.multi_submit(db, self.change_dict, self.tab_id))

        # back button
        back = Button(self, "Back", .1, .1, .15, .45, command=lambda: self.controller.show_frame("MainFrame"))

        # CREATE TAB (ttk treeview)
        cols = ('Name', 'Quantity')
        self.tab = ttk.Treeview(self, columns=cols, show='headings')

        for col in cols:
            self.tab.heading(col, text=col)

        # add values from database
        for record in self.order:
            this_name = record[0]
            self.tab.insert("", "end", iid=this_name, values=record)
        self.tab.place(relx=0, rely=.1)

        # scrollbar for treeview
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tab.yview)
        vsb.place(relx=.305,rely=.1)
        self.tab.configure(yscrollcommand=vsb.set)

        # create menu buttons
        relx = .35
        rely = .05
        for name in self.menu_names:
            b1 = Button(self, name, .1, .12, relx, rely, command=lambda name=name: self.update_tree(self.tab, name))
            if relx >= .8:
                relx = .35
                rely += .12
            else:
                relx += .13

    def update_tree(self, treeview, item_name, qty=-1):
        if treeview.exists(item_name):
            qty = self.get_curr_qty(treeview, item_name)
            qty += 1
            treeview.set(item_name, "Quantity", qty)
        else:
            qty = 1
            record = (item_name, qty)
            treeview.insert("", "end", iid=item_name, values=record)

        # save changes made into dictionary
        self.change_dict[item_name] = qty
        print(self.change_dict)

    def get_curr_qty(self, treeview, item_name):
        values = treeview.item(item_name)["values"]
        qty = values[1]
        return qty

    def multi_submit(self, connection, change_dict, tab_id):
        # change_list should be of the form: [[food_name, qty],]
        for key in change_dict:
            self.submit(connection, key, tab_id, change_dict[key])

        change_dict = {}

    def submit(self, connection, food_name, tab_id, qty):
        menu_id = get_menu_item_id(connection, food_name)
        exists = check_exists(connection, "OrderItem", "TabID", tab_id, "MenuItemID", menu_id)

        if exists:
            # update OrderItem set Quantity = 3 where OrderItemID = 103 and MenuItemID = 101;
            stm = ("UPDATE `OrderItem` SET `Quantity` = %s "
                   "WHERE `TabID` = %s "
                   "AND `MenuItemID` = %s")
            vals = (qty, tab_id, menu_id)
            print(stm)
        else:
            stm = ("INSERT INTO `OrderItem` (TabID, MenuItemID, Quantity) "
                   "VALUES (%s, %s, %s)")
            vals = (tab_id, menu_id, qty)
            print(tab_id, menu_id, qty)
            print(stm)

        execute_stm(connection, stm, vals)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menya Le Nood")
        self.geometry("1280x720")
        self.resizable(0,0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self)
        self.container.pack(side="top", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in (OrderFrame, MainFrame):
        #     page_name = F.__name__
        #     print(page_name)
        #     frame = F(parent=self.container, controller=self, table_num=0)
        #     self.frames[page_name] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")

        self.create_frame(OrderFrame)
        self.create_frame(MainFrame)
        self.show_frame("MainFrame")

    def create_frame(self, frame_class):
        frame_name = frame_class.__name__
        frame = frame_class(parent=self.container, controller=self, table_num=0)
        self.frames[frame_name] = frame
        frame.grid(row=0, column=0,sticky="nsew")

    def show_frame(self, page_name, table_num=0):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.destroy()
        frame.__init__(parent=self.container,controller=self,table_num=table_num)
        frame.grid(row=0,column=0,sticky="nsew")
        # frame.table_num = table_num
        frame.tkraise()

"""
END GUI
"""

def execute_read_query(connection, query, vals):
    cursor = connection.cursor()
    result = None

    try:
        cursor.execute(query, vals)
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)

    return result

def get_order(connection, table_num):
    table_num = str(table_num)
    query = "SELECT Name, Quantity FROM `Order` WHERE TableNum = %s"
    vals = (table_num,)
    res = execute_read_query(connection, query, vals)
    return res

def get_menu(connection):
    query = "SELECT * FROM `MenuList`"
    res = execute_read_query(connection, query, ())
    return res

def get_menu_names(menu):
    names = []
    for record in menu:
        names.append(record[1])
    return names

def get_tab_id(connection, table_num):
    query = ("SELECT TabID FROM `Tab` WHERE TableNum = "
             "%s AND `Open` = 1")

    vals = (table_num,)
    res = execute_read_query(connection, query, vals)

    # check to avoid index out of bounds
    if res:
        return res[0][0]
    else:
        return res

def get_menu_item_id(connection, name):
    query = ("SELECT * from MenuItem where Name = %s")
    vals = (name,)

    res = execute_read_query(connection, query, vals)
    return res[0][0]

# subquery, check if record exists
def check_exists(connection, table, field, value, field2="", value2=""):
    query = ("SELECT EXISTS("
             "SELECT * FROM " + table
             + " WHERE `" + field + "` = %s)")
    vals = (value,)

    # if there are more values
    if field2:
        # drop final parentheses
        query = query[:-1]
        query += " AND `" + field2 + "`= %s)"
        vals = (value,value2)


    result = execute_read_query(connection, query, vals)
    # get boolean from sql query
    if result:
        exists = result[0][0]
    else:
        exists = 0

    return exists

def execute_stm(connection, stm, data):
    cursor = connection.cursor()
    try:
        cursor.execute(stm, data)
        connection.commit()
        return True
    except mysql.connector.Error as e:
        print(e)
        return False

app = App()
app.mainloop()
# get_menu(db)
# cursor = db.cursor()
# cursor.execute("SELECT * FROM `Order`")
# result = cursor.fetchall()
# print(result)
