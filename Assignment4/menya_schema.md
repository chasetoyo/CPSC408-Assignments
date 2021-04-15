# Schema

## Menu
---
**MenuID (pk)**, Name, Price, *FoodType (fk)*

- 1, tonkotsu ramen, 15, ramen

- 2, shoyu tsukemen, 15, tsukemen

- 3, gyoza, 5, appetizer

- 4, karaage don, 10, donburi

---
## Order (by table)

**OrderID (pk)**, Total, PartySize

- 1, 30, 2

- 2, 45, 3

- 3, 10, 1

---
## OrderItem

**OrderItemID (pk)**, *OrderID (fk)*, *MenuID (fk)*, Amount

- 1, 1, 2, 2

- 2, 1, 3, 1

---
## Employee

**EmployeeID (pk)**, FirstName, LastName, Address, Salary, Email, *JobID (fk)*
- 1, john, doe, 321 bird st, 15, johndoe@gmail.com, 2
- 2, jane, doe, 123 bird ave, 20, janedoe@gmail.com, 1

---
## Reservation

**ReservationID (pk)**, PartySize, ReservationTime
- 1, 3, 2021-4-20 18:00:00
- 2, 2, 2021-4-21 17:00:00

---
## Job

**JobID (pk)**, Description
- 1, Chef
- 2, Server
- 3, Cashier