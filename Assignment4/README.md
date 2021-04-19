# CPSC 408 Assignment 4 (Normalized Database in MySQL)

## Chase Toyofuku-Souza

## Table of Contents

* [About](#about)
* [Required Dependencies](#Required-Dependencies)
* [Instructions](#Instructions)
* [Files](#Files)
* [Notes](#Notes)
* [References](#References)

## About
Now that you are familiar with designing a normalized database schema, your assignment is to create a normalized database schema, develop a data generation tool (using faker) and a python module to import the data.

## Required-Dependencies
* Faker
```sh
pip3 install faker
```
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
python3 application.py
```
3. Follow the on-screen prompts to import and export fake data from a csv file

### Files
- [`application.py`](application.py)
- [`Credential File`](.env)
- [`Schema`](create_tables.sql)

### Notes
This was implemented using a local MySQL instance, as I did not know the credentials for the CloudSQL. As long as valid credentials are entered in [`.env`](.env), I added an option to populate a database with the proper tables so that this application can be run on a different server besides my own.

### References
- https://faker.readthedocs.io/en/master/
- https://stackoverflow.com/questions/48596923/check-if-csv-file-is-empty-or-not-after-reading-with-dictreader/48596967
- https://stackoverflow.com/questions/20818155/not-all-parameters-were-used-in-the-sql-statement-python-mysql
- https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
- https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
- https://pypi.org/project/python-dotenv/
- https://zetcode.com/python/faker/