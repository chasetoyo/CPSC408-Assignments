import tkinter as tk
from tkinter import ttk

def greet():
    print("hello")

def create_table_frame(container):
    frame = ttk.Frame(container)

    b1 = ttk.Button(text="Table 1", command=greet)
    b2 = ttk.Button(text="Table 2", command=greet)
    b3 = ttk.Button(text="Table 3", command=greet)
    b4 = ttk.Button(text="Table 4", command=greet)
    b5 = ttk.Button(text="Table 5", command=greet)
    b6 = ttk.Button(text="Table 6", command=greet)
    b7 = ttk.Button(text="Table 7", command=greet)
    b8 = ttk.Button(text="Table 8", command=greet)
    l = ttk.Label(text="Menya Le Nood", font=("TkDefaultFont", 40))

    l.place(rely=.05, relx=.495, anchor="center")
    # 1 2 3
    b1.place(rely=.1,relx=.275,relwidth=.125,relheight=.2)
    b2.place(rely=.1,relx=.425,relwidth=.1,relheight=.2)
    b3.place(rely=.1,relx=.55,relwidth=.175,relheight=.2)
    # 4 5 6
    b4.place(rely=.35,relx=.275,relwidth=.125,relheight=.2)
    b5.place(rely=.35,relx=.425,relwidth=.1,relheight=.2)
    b6.place(rely=.35,relx=.55,relwidth=.175,relheight=.2)
    # 7 8
    b7.place(rely=.6,relx=.275,relwidth=.125,relheight=.2)
    b8.place(rely=.6,relx=.55,relwidth=.175,relheight=.2)
    
    return frame

def create_root():

    # root window
    root = tk.Tk()
    root.title('Menya Le Nood')
    root.geometry('1280x720')
    root.resizable(0, 0)

    table_frame = create_table_frame(root)
    table_frame.pack(side=tk.TOP)

    root.mainloop()

create_root()
