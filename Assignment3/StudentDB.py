import sqlite3
import pandas as pd

db = './StudentDB.db'
csv = './students.csv'

#establish db connection
conn = sqlite3.connect(db)
cursor = conn.cursor()

# takes csv and populates db
def import_csv(csv):
	student_data = pd.read_csv(csv)

	# convert int to str
	student_data['ZipCode'] = student_data['ZipCode'].astype(str)

	# iterate over each row in dataframe and insert into db
	for i in range(student_data.shape[0]):
		sql = '''INSERT into Student(FirstName,LastName,Address,City,State,
				ZipCode,MobilePhoneNumber,Major,GPA)
				VALUES(?,?,?,?,?,?,?,?,?)'''
		cursor.execute(sql, student_data.iloc[i])
		conn.commit()

# DisplayAll Students andall of their attributes.
# pass in a select statement and values
def display_students(sql,vals):
	cursor.execute(sql,vals)
	rec = cursor.fetchall()
	df = pd.DataFrame(rec, 
		columns=['StudentID','FirstName','LastName','GPA','Major','FacultyAdvisor',
		'Address','City','State','ZipCode','MobilePhoneNumber','isDeleted'])
	# check if there is nothing in the database
	if check_empty(df):
		print("No Records Found")
	else:
		df = df.to_string()
		print(df)

# Add NewStudentsi.All attributes are requiredwhen creating a new student.
# 	ii.Please make sure to validate user input appropriately.
# 	1.forexample,a GPA can’t have a value of ‘foobar’etc.

def add_student():
	# bools to check correct input
	first_valid = 0
	last_valid = 0
	major_valid = 0
	faculty_valid = 0
	address_valid = 0
	phone_valid = 0
	city_valid = 0
	zip_valid = 0
	state_valid = 0
	gpa_valid = 0
	pid_valid = 0

	while True:
		try:
			if first_valid == 0:
				first_name = input("Enter First Name: ")
				first_valid = 1

			if last_valid == 0:
				last_name = input("Enter Last Name: ")
				last_valid = 1

			if gpa_valid == 0:
				gpa = float(input("Enter GPA: "))
				gpa_valid = 1

			if major_valid == 0:
				major = input("Enter Major: ")
				major_valid = 1
			
			if faculty_valid == 0:
				faculty_advisor = input("Enter Faculty Advisor: ")
				faculty_valid = 1
			
			if address_valid == 0:
				address = input("Enter Address: ")
				address_valid = 1

			if city_valid == 0:
				city = input("Enter City: ")
				city_valid = 1

			if state_valid == 0:
				state = input("Enter State: ")
				state_valid = 1

			if zip_valid == 0:
				zip = int(input("Enter Zip Code: "))
				zip_valid = 1
			
			if phone_valid == 0:
				phone = int(input("Enter Phone Number: "))
				phone_valid = 1	
		
		except ValueError:
			print("Must enter a number")
			continue
		else:
			break

	print(first_name, last_name, gpa, major, faculty_advisor, address, city, state, zip, phone)
	
	sql = '''INSERT INTO Student(FirstName,LastName,GPA,Major,FacultyAdvisor,Address,
			City,State,ZipCode,MobilePhoneNumber)
			VALUES(?,?,?,?,?,?,?,?,?,?)'''
	cursor.execute(sql,
		[first_name, last_name, gpa, major, faculty_advisor, address, city, state, zip, phone])
	conn.commit()

# Update Students
# 	i.Only thefollowing fields can be updated
# 		1.Major, Advisor, MobilePhoneNumber

def update_student():
	sid = (input("Enter StudentID of student you would like to update: "))
	
	# check if student exists
	if exists(sid)== 0:
		print('StudentID does not exist')
		return
	
	while True:
		print("------------------------")
		print("What field would you like to update?")
		print("Enter 1 for Major\nEnter 2 for Faculty Advisor\nEnter 3 for MobilePhoneNumber")
		choice = input()
		
		sid = int(sid)

		if choice == "1":
			major = input("Enter new Major: ")
			sql = '''UPDATE Student
	              SET Major = ?
	              WHERE StudentId = ?'''
			cursor.execute(sql, [major, sid])
			conn.commit()
			break

		elif choice == "2":
			advisor = input("Enter new Faculty Advisor: ")
			sql = '''UPDATE Student
	              SET FacultyAdvisor = ?
	              WHERE StudentId = ?'''
			cursor.execute(sql, [advisor, sid])
			conn.commit()
			break

		elif choice == "3":
			phone = input("Enter new Mobile Phone Number: ")
			sql = '''UPDATE Student
	              SET MobilePhoneNumber = ?
	              WHERE StudentId = ?'''
			cursor.execute(sql, [phone, sid])
			conn.commit()
			break

		else:
			print("Invalid Choice")

	print("Updated!")

# Delete Studentsby StudentId
# 	Perform a “soft”delete on studentsthat is, setisDeletedto true(1)
def delete_student():
	sid = (input("Enter StudentID of student you would like to delete: "))

	# check if student exists
	if exists(sid) == 0:
		print('StudentID does not exist')
		return
	
	sql = ''' UPDATE Student
	        SET isDeleted = 1
	        WHERE StudentId = ?'''
	
	cursor.execute(sql, [int(sid)])
	conn.commit()

	print("Deleted")

def check_empty(df):
	if df.shape[0] == 0:
		return 1
	return 0

def exists(value):
	query = "SELECT EXISTS(SELECT * FROM Student WHERE StudentId = ?)"
	cursor.execute(query,[value])
	result = cursor.fetchall()
	exists = result[0][0]
	
	return exists

# Search/DisplaystudentsbyMajor, GPA, City, State and Advisor.
def search_student():
	print("------------------------")
	print("What field would you like to search by?")
	print("Enter 1 for Major\nEnter 2 for GPA\nEnter 3 for City"
		"\nEnter 4 for State\nEnter 5 for Advisor\n"
		"Enter q to quit")
	choice = input()

	if choice == "1":
		x = input("Enter Major: ")
		sql = '''SELECT * from Student
				WHERE Major = ?'''
		display_students(sql,[x])
	elif choice == "2":
		x = input("Enter GPA: ")
		sql = '''SELECT * from Student
				WHERE GPA = ?'''
		display_students(sql,[x])
	elif choice == "3":
		x = input("Enter City: ")
		sql = '''SELECT * from Student
				WHERE City = ?'''
		display_students(sql,[x])
	elif choice == "4":
		x = input("Enter State: ")
		sql = '''SELECT * from Student
				WHERE State = ?'''
		display_students(sql,[x])
	elif choice == "5":
		x = input("Enter Faculty Advisor: ")
		sql = '''SELECT * from Student
				WHERE FacultyAdvisor = ?'''
		display_students(sql,[x])
	else:
		print("Invalid Choice")

if __name__ == "__main__":
	while True:
		print("------------------------")
		print("What do you want to do")
		print("Enter 1 to Display All Students\nEnter 2 to Insert New Student\nEnter 3 to Update"
			"\nEnter 4 to Delete\nEnter 5 to Search\n"
			"Enter q to quit")
		choice = input()

		if choice == "1":
			sql = '''SELECT * from Student'''
			display_students(sql,[])
		elif choice == "2":
			add_student()
		elif choice == "3":
			update_student()
		elif choice == "4":
			delete_student()
		elif choice == "5":
			search_student()
		elif choice == "q" or choice == "Q":
			break
		else:
			print("Bad Input")