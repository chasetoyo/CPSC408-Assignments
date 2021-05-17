# 1.Print/displayrecords from your database/tables. ✓
# 2.Queryfor data/results with various parameters/filters ✓
# 3.Create a new record ✓
# 4.Delete records (soft delete function would be ideal) ✓
# 5.Update records ✓
# 6.Make use of transactions (commit & rollback) ✓
# 7.Generate reports that can be exported (excel or csv format) ✓
# 8.One query must perform an aggregation/group-by clause ✓
# 9.One query must contain a sub-query. ✓
# 10.Two queries must involve joins across at least 3 tables ✓
# 11.Enforce referential integrality(PK/FK Constraints) ✓
# 12.Include Database Views, Indexes ✓

import tkinter as tk
from tkinter import ttk
import mysql.connector
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
from faker import Faker

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
    def __init__(self, container, text, rely, relx, anchor="center", font="Courier", size=14):
        super().__init__(container, text=text)
        self.config(font = (font, size))
        self.place(relx=relx, rely=rely, anchor=anchor)

# view of all the restaurant tables, segues to order
class MainFrame(tk.Frame):
    def __init__(self, parent, controller, table_num=0):
        tk.Frame.__init__(self, parent,width=1280,height=720)
        self.controller = controller
        self.init_widgets()
        self.table_num = table_num

    def init_widgets(self):
        # container, text, relheight, relwidth, relx, rely, command

        # define every table
        b1 = Button(self, "Table 1", .2, .125, .29, .1, lambda: self.controller.show_frame("OrderFrame", 1))
        b2 = Button(self, "Table 2", .2, .1, .44, .1, lambda: self.controller.show_frame("OrderFrame",2))
        b3 = Button(self, "Table 3", .2, .175, .57, .1, lambda: self.controller.show_frame("OrderFrame",3))

        b4 = Button(self, "Table 4", .2, .125, .29, .35, lambda: self.controller.show_frame("OrderFrame",4))
        b5 = Button(self, "Table 5", .2, .1, .44, .35, lambda: self.controller.show_frame("OrderFrame",5))
        b6 = Button(self, "Table 6", .2, .175, .57, .35, lambda: self.controller.show_frame("OrderFrame",6))

        b7 = Button(self, "Table 7", .2, .125, .29, .6, lambda: self.controller.show_frame("OrderFrame",7))
        b8 = Button(self, "Table 8", .2, .175, .57, .6, lambda: self.controller.show_frame("OrderFrame", 8))

        l = Label(self, "Menya Le Nood", .05, .495)

        self.entry = tk.StringVar(self)
        self.email_entry = tk.Entry(self, textvariable=self.entry)
        self.email_entry.place(relheight=.05,relwidth=.2,relx=.79,rely=.74)
        report = Button(self, "Export Reports", .1, .2, .79, .8,
                        lambda: self.export_reports(self.email_entry.get()))

    def get_item_report(self, date):
        db = create_connection(HOST_IP, USER_NAME, PASSWORD, DB)

        stm = ("SELECT Name, SUM(Quantity*Price) AS Total_Sales FROM OrderItem "
               "JOIN Tab T on OrderItem.TabID = T.TabID "
               "JOIN Reservation R ON T.ReservationID = R.ReservationID "
               "JOIN Menu ON Menu.MenuItemID = OrderItem.MenuItemID "
               "JOIN MenuItem MI ON OrderItem.MenuItemID = MI.MenuItemID "
               "WHERE DATE(ReservationTime) = %s "
               "AND Open = 0 "
               "AND T.Deleted = 0 "
               "GROUP BY MI.MenuItemID")
        vals = (date,)

        res = execute_read_query(db, stm, vals)
        return res

    def get_category_report(self, date):
        db = create_connection(HOST_IP, USER_NAME, PASSWORD, DB)
        stm = ("SELECT FT.Name AS Category, SUM(Quantity*Price) AS Total_Sales FROM OrderItem "
               "join Tab T ON OrderItem.TabID = T.TabID "
               "join Reservation R ON T.ReservationID = R.ReservationID "
               "join Menu ON Menu.MenuItemID = OrderItem.MenuItemID "
               "join MenuItem MI ON OrderItem.MenuItemID = MI.MenuItemID "
               "join FoodType FT ON MI.FoodTypeID = FT.FoodTypeID "
               "where DATE(ReservationTime) = %s "
               "AND Open = 0 "
               "AND T.Deleted = 0 "
               "GROUP BY FT.FoodTypeID")
        vals = (date,)

        res = execute_read_query(db, stm, vals)
        return res

    def export_item_report(self, date):
        item_report = self.get_item_report(date)
        file_name  = date + "-item-report.csv"
        with open(file_name, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Food_Name", "Total_Sales"])

            for record in item_report:
                food_name = record[0]
                sale = record[1]
                writer.writerow([food_name, sale])

    def export_category_report(self, date):
        item_report = self.get_category_report(date)
        file_name  = date + "-category-report.csv"
        with open(file_name, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Category", "Total_Sales"])

            for record in item_report:
                category = record[0]
                sale = record[1]
                writer.writerow([category, sale])

    def export_reports(self, date):
        # NEED TO VALIDATE DATE
        self.export_item_report(date)
        self.export_category_report(date)
        self.entry.set("")

# responsible for making orders and reservations
class OrderFrame(tk.Frame):

    def __init__(self, parent, controller, table_num):
        tk.Frame.__init__(self, parent, width=1280,height=720)
        self.controller = controller
        self.table_num = table_num

        self.db = create_connection(HOST_IP, USER_NAME, PASSWORD, DB)

        self.order = self.get_order(self.db, self.table_num)

        self.menu = []
        self.menu_names = []
        self.menu_list = []

        self.tab_id = self.get_tab_id(self.db, table_num)
        self.change_dict = {}

        # if there is no existing tab for the table
        if not self.tab_id:
            self.init_reservation()
        else:
            self.init_widgets()

    def init_reservation(self):

        self.email_label = tk.Label(self, text="Email", font=("Arial", 15))
        self.email_entry = tk.Entry(self)

        self.party_label = tk.Label(self, text="Party Size", font=("Arial", 15))
        self.party_entry = tk.Entry(self)

        self.reservation_time_label = tk.Label(self, text="Reservation Time", font=("Arial", 15))
        self.reservation_time_entry = tk.Entry(self)

        self.reservation_id_label = tk.Label(self, text="Reservation ID", font=("Arial", 15))
        self.reservation_id_entry = tk.Entry(self)

        self.email_label.place(relheight=.1, relwidth=.2, relx=.4, rely=.3, anchor="center")
        self.email_entry.place(relheight=.05, relwidth=.2, relx=.55, rely=.3, anchor="center")

        self.party_label.place(relheight=.1, relwidth=.2, relx=.4, rely=.4, anchor="center")
        self.party_entry.place(relheight=.05, relwidth=.2, relx=.55, rely=.4, anchor="center")

        self.reservation_time_label.place(relheight=.1, relwidth=.2, relx=.38, rely=.5, anchor="center")
        self.reservation_time_entry.place(relheight=.05, relwidth=.2, relx=.55, rely=.5, anchor="center")

        self.reservation_id_label.place(relheight=.1, relwidth=.2, relx=.38, rely=.6, anchor="center")
        self.reservation_id_entry.place(relheight=.05, relwidth=.2, relx=.55, rely=.6, anchor="center")

        self.submit_res_button = Button(self, "Submit", .1, .2, .45, .65,
                                   command=lambda:
                                   self.submit_reservation(self.db))

        self.back_button = Button(self, "Back", .1, .2, .45, .75,
                                        command=lambda:
                                        self.controller.show_frame("MainFrame"))

    def init_widgets(self):
        # frame title
        label = tk.Label(self, text="Table " + str(self.table_num), font=("Arial", 25))
        label.place(relx=0,rely=0)

        # submit button (THIS ONE COMMITS)
        submit = Button(self, "Submit", .1, .32, 0, .61,
                        command=lambda: self.db.commit())

        # back button (rollback and return to mainframe)
        back = Button(self, "Back", .1, .1, .22, .5,
                      command=lambda: self.go_back())

        # close order button
        close_order = Button(self, "Close Order", .1, .1, .11, .5,
                             command=lambda: self.close_order(self.db, self.tab_id))

        # close order button
        # .1, .32, 0, .61
        delete = Button(self, "Delete Tab", .1, .1, 0, .5,
                             command=lambda: self.delete_tab(self.db, self.tab_id))

        # filter button
        option = tk.StringVar(self)
        option.set("") # default value
        filter = tk.OptionMenu(self, option, "","Ramen", "Tsukemen", "Drinks", "Appetizer", "Donburi",
                               command=lambda x=option.get(): self.filter_menu(self.db, x))

        filter.place(relx=.35, rely=.005)

        # price label
        self.total_price_label = Label(self, "$0", .45, .28)
        self.update_price_label()

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
        self.create_menu_buttons()

    def delete_tab(self, connection, tab_id):
        stm = ("UPDATE `Tab` SET `Deleted` = 1 "
               "WHERE `TabID` = %s")
        vals = (tab_id,)
        execute_stm(connection, stm, vals)

    def get_total_price(self, connection, tab_id):
        stm = ("SELECT SUM(Quantity * Price) FROM OrderItem "
               "JOIN Menu ON Menu.MenuItemID = OrderItem.MenuItemID WHERE "
               "TabID = (SELECT TabID from Tab where Open = 1 AND TabID = %s)")
        vals = (tab_id,)

        res = execute_read_query(connection, stm, vals)
        return res[0][0]

    def update_price_label(self):
        total_price = self.get_total_price(self.db, self.tab_id)
        total_price_str = "$" + str(total_price)
        self.total_price_label.config(text=total_price_str)

    def filter_menu(self, connection, food_type=""):
        # delete all the buttons for the menu items
        for x in self.menu_list:
            x.destroy()
        # recreate the ones that are filtered for
        self.create_menu_buttons(food_type)

    def update_tree(self, treeview, item_name, qty=-1):
        # if it exists, increment qty by 1
        if treeview.exists(item_name):
            qty = self.get_curr_qty(treeview, item_name)
            qty += 1
            treeview.set(item_name, "Quantity", qty)

        # else, init new record with qty 1
        else:
            qty = 1
            record = (item_name, qty)
            treeview.insert("", "end", iid=item_name, values=record)

        # save changes made into dictionary
        self.change_dict[item_name] = qty
        print(self.change_dict)
        self.submit(self.db, item_name,self.tab_id, qty, commit=False)

    def get_curr_qty(self, treeview, item_name):
        # returns the current value for qty in the treeview
        values = treeview.item(item_name)["values"]
        qty = values[1]
        return qty

    def submit(self, connection, food_name, tab_id, qty, commit):
        # check if the record exists to determine if update or insert
        menu_id = self.get_menu_item_id(connection, food_name)
        exists = check_exists(connection, "OrderItem", "TabID", tab_id, "MenuItemID", menu_id)

        # update if exists
        if exists:
            stm = ("UPDATE `OrderItem` SET `Quantity` = %s "
                   "WHERE `TabID` = %s "
                   "AND `MenuItemID` = %s")
            vals = (qty, tab_id, menu_id)
        # insert if it doesnt exist
        else:
            stm = ("INSERT INTO `OrderItem` (TabID, MenuItemID, Quantity) "
                   "VALUES (%s, %s, %s)")
            vals = (tab_id, menu_id, qty)

        execute_stm(connection, stm, vals, commit=commit)
        # update total price
        self.update_price_label()

    def submit_reservation(self, connection):
        # get required values
        email_val = self.email_entry.get()
        party_val = self.party_entry.get()
        res_time_val = self.reservation_time_entry.get()
        res_id_val = self.reservation_id_entry.get()

        # check if user just entered the id (used when not creating a new reservation)
        # if they did not use the id, insert
        if not res_id_val:
            stm = ("INSERT INTO `Reservation` (Email, PartySize, ReservationTime) "
               "VALUES (%s, %s, %s)")
            vals = (email_val, party_val, res_time_val)

            # get reservation_id just created
            res_id_val = execute_stm(connection, stm, vals)
        else:
            # verify the id is valid
            exists = check_exists(connection, "Reservation", "ReservationID", res_id_val)
            # dont do anything if they entered a bad id
            if not exists:
                return

        # create the tab
        self.create_tab(connection, res_id_val, self.table_num)

        # go back to the orderframe
        self.email_entry.destroy()
        self.party_entry.destroy()
        self.reservation_time_entry.destroy()
        self.email_label.destroy()
        self.party_label.destroy()
        self.reservation_time_label.destroy()
        self.submit_res_button.destroy()
        self.reservation_id_entry.destroy()
        self.reservation_id_label.destroy()
        self.back_button.destroy()

        self.init_widgets()

    def create_tab(self, connection, reservation_id, table_num):
        # create record in `Tab` based on reservationid and tablenum
        stm = ("INSERT INTO `Tab` (ReservationID, TableNum, Open, Deleted) "
               "VALUES (%s, %s, %s, 0)")
        vals = (reservation_id, table_num, 1)
        tab_id = execute_stm(connection, stm, vals)
        self.tab_id = tab_id

    def close_order(self, connection, tab_id):
        # simulating "checking out"
        stm = ("UPDATE `Tab` SET `Open` = 0 "
               "WHERE `TabID` = %s")
        vals = (tab_id,)

        execute_stm(connection, stm, vals)
        # go back to frame of restaurant tables
        self.controller.show_frame("MainFrame")

    def create_menu_buttons(self, food_type=""):
        # get list of menu item names according to filter
        self.menu = self.get_menu(self.db, food_type)
        self.menu_names = self.get_menu_names(self.menu)

        # place them in a grid
        relx = .35
        rely = .05
        for name in self.menu_names:
            b1 = Button(self, name, .1, .12, relx, rely, command=lambda name=name: self.update_tree(self.tab, name))
            self.menu_list.append(b1)
            if relx >= .8:
                relx = .35
                rely += .12
            else:
                relx += .13

    def get_order(self, connection, table_num):
        # read in the order for the current table
        table_num = str(table_num)
        query = "SELECT Name, Quantity FROM `Order` WHERE TableNum = %s"
        vals = (table_num,)
        res = execute_read_query(connection, query, vals)
        return res

    def get_menu(self, connection, food_type=""):
        query = "SELECT * FROM `MenuList`"
        vals = ()

        if food_type:
            query += " WHERE FoodType = %s"
            vals = (food_type,)

        res = execute_read_query(connection, query, vals)
        return res

    def get_menu_names(self, menu):
        names = []
        for record in menu:
            # index 1 is the name
            names.append(record[1])
        return names

    def get_menu_item_id(self, connection, name):
        query = ("SELECT * from MenuItem where Name = %s")
        vals = (name,)

        res = execute_read_query(connection, query, vals)
        return res[0][0]

    def get_tab_id(self, connection, table_num):
        # checks if the order is open and not deleted
        query = ("SELECT TabID FROM `Tab` WHERE TableNum = "
                 "%s AND `Open` = 1 AND `Deleted` = 0")

        vals = (table_num,)
        res = execute_read_query(connection, query, vals)

        # avoid index out of bounds
        if res:
            return res[0][0]
        else:
            return res

    # def is_deleted(self, connection, table_num):
    #     query = ("SELECT TabID FROM `Tab` WHERE TableNum = "
    #              "%s AND `Open` = 1")
    #
    #     vals = (table_num,)
    #     res = execute_read_query(connection, query, vals)
    #
    #     # check to avoid index out of bounds
    #     if res:
    #         return res[0][0]
    #     else:
    #         return res

    # rolls back and switches to mainframe
    def go_back(self):
        self.db.rollback()
        self.controller.show_frame("MainFrame")

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
        self.create_frame(OrderFrame)
        self.create_frame(MainFrame)
        self.show_frame("MainFrame")

    def create_frame(self, frame_class):
        frame_name = frame_class.__name__
        frame = frame_class(parent=self.container, controller=self, table_num=0)
        self.frames[frame_name] = frame
        frame.grid(row=0, column=0,sticky="nsew")

    def show_frame(self, page_name, table_num=0):
        "Show a frame for the given page name"
        frame = self.frames[page_name]
        frame.destroy()
        frame.__init__(parent=self.container,controller=self,table_num=table_num)
        frame.grid(row=0,column=0,sticky="nsew")
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

# check if record exists
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

def execute_stm(connection, stm, data, commit=True):
    cursor = connection.cursor()
    try:
        cursor.execute(stm, data)
        if commit:
            connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return -1

app = App()
app.mainloop()
