# CPSC 408 Assignment 3 (SQLite)
## Chase Toyofuku-Souza

## About
The first goal is to create a SQLite database *StudentsDB.db* with the following schema:
```sql

Student (
	StudentId INTEGER PRIMARY KEY,
	FirstName TEXT,
	LastName TEXT,
	GPA REAL,
	Major TEXT,
	FacultyAdvisor TEXT,
	Address TEXT,
	City TEXT,
	State TEXT,
	ZipCode TEXT,
	MobilePhoneNumber TEXT,
	isDeleted INTEGER
)
```
Then, we must write a Python function that imports a file, *students.csv* into StudentsDB. There is then a simple CRUD Python application to interact with StudentsDB.

### Files
- [`StudentDB.py`](StudentDB.py)
- [`StudentDB.db`](StudentDB.db)
- [`students.csv`](students.csv)

### References
- https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
- https://www.sqlitetutorial.net/sqlite-create-table/
- https://stackoverflow.com/questions/1676551/best-way-to-test-if-a-row-exists-in-a-mysql-table
- https://stackoverflow.com/questions/21142531/sqlite3-operationalerror-no-such-column