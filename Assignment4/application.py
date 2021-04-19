import mysql.connector
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
from faker import Faker

# get credentials from .env file
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

# generate fake data
# take in file name and number of rows to be created
def export_data(file_name, num_rows):
	fake = Faker()

	with open(file_name, "w", newline='') as csv_file:
		writer = csv.writer(csv_file)
		# establish titles for each value
		writer.writerow(["Email", "PartySize", "ReservationTime", "Quantity", "Price", "FoodName", "FoodTypeName"])
		
		# create 'num_rows' entries
		for x in range(num_rows):
			email = fake.email()
			# party size between 1 and 10
			party = fake.random_number(1,10)
			# reservatinons within a year
			time = fake.date_time_between(start_date='now', end_date='+365d')
			# quantity between 1 and 20
			qty = fake.random_number(1,20)
			# between 5 and 17 dollars
			price = fake.random_int(50,170)/10.0
			# generate random (non food related words for names and types)
			foodname = fake.word()
			foodtypename = fake.word()

			writer.writerow([email, party, time, qty, price, foodname, foodtypename])

def insert_food_type(db, cursor, val):
	sql = """INSERT INTO foodtype(Name) VALUES (%s)"""
	cursor.execute(sql, val)
	db.commit()
	lastid = cursor.lastrowid
	return lastid

def insert_menu_item(db, cursor, val):
	sql = """INSERT INTO menuitem(Name, FoodTypeID) VALUES (%s, %s)"""
	cursor.execute(sql, val)
	db.commit()
	lastid = cursor.lastrowid
	return lastid

def insert_menu(db, cursor, val):
	sql = """INSERT INTO menu(MenuItemID, Price) VALUES (%s, %s)"""
	cursor.execute(sql, val)
	db.commit()
	lastid = cursor.lastrowid
	return lastid

def insert_order_item(db, cursor, val):
	sql = """INSERT INTO orderitem(TabID, MenuItemID, Quantity) VALUES (%s, %s, %s)"""
	cursor.execute(sql, val)
	db.commit()
	lastid = cursor.lastrowid
	return lastid

def insert_tab(db, cursor, val):
	sql = """INSERT INTO tab(ReservationID) VALUES (%s)"""
	cursor.execute(sql, val)
	db.commit()
	lastid = cursor.lastrowid
	return lastid

def insert_reservation(db, cursor, val):
	sql = """INSERT INTO reservation(Email, PartySize, ReservationTime) VALUES (%s, %s, %s)"""
	cursor.execute(sql, val)
	db.commit()
	lastid = cursor.lastrowid
	return lastid


# read in data from csv and insert into database
def import_data(db, file_name):
	cursor = db.cursor()

	# open csv with data
	with open(file_name, "r") as csv_file:
		reader = csv.DictReader(csv_file)
		ct = 0

		for row in reader:
			ct += 1
			# fill in database table by table

			# reservation table
			email = row["Email"]
			party_size = row["PartySize"]
			time = row["ReservationTime"]
			res_id = insert_reservation(db, cursor, (email, party_size, time))

			# tab table
			tab_id = insert_tab(db, cursor, (res_id,))

			# foodtype table
			food_type = row["FoodTypeName"]
			food_type_id = insert_food_type(db, cursor, (food_type,))

			# menuitem table
			food_name = row["FoodName"]
			menu_item_id = insert_menu_item(db, cursor, (food_name, food_type_id))

			#menu table
			price = row["Price"]
			insert_menu(db, cursor, (menu_item_id, price))

			#orderitem table
			qty = row["Quantity"]
			insert_order_item(db, cursor, (tab_id, menu_item_id, qty))

		print("Imported", str(ct), "records from", file_name)

# check if file exists
def file_exists(file_name):
	if os.path.isfile(file_name):
		return 1
	else:
		return 0

def main():
	# establish connection with mysql db
	db = create_connection(HOST_IP, USER_NAME, PASSWORD, DB)

	if db is None:
		return 0

	while True:
		print("------------------------")
		print("Enter 1 to Generate Fake Data"
			"\nEnter 2 to Import Data"
			"\nEnter q to quit")
		choice = input()

		if choice == "1":
			# file loop
			while True:
				file_name = input("Enter a file name to write data to: ")
				
				if file_exists(file_name):
					choice = input("Overwrite existing file?(y/n): ")

					if choice == "y" or choice == "Y":
						break
					else:
						continue

			#num recs loop
			while True:
				try:
					num_rows = int(input("Enter number of records to generate: "))
					break

				except ValueError as e:
					print("Invalid Input")
					continue
			
			export_data(file_name, num_rows)
			print("Exported", str(num_rows), "rows to", file_name)

		elif choice == "2":
			while True:
				file_name = input("Enter a file name to import from: ")
				
				if file_exists(file_name):
					print("Importing Records from", file_name)
					import_data(db, file_name)
					break
				
				else:
					print("Invalid File Name")

		elif choice == "q" or choice == "Q":
			print("Goodbye!")
			break

		else:
			print("Invalid Input")

if __name__ == "__main__":
	main()