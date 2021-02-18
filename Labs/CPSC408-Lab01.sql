-- 1
select FirstName,LastName,Email from Employee;
-- 2
select * from Artist;
-- 3
select EmployeeId from Employee where Title like '%Manager%';
-- 4
select InvoiceId,min(Total) from Invoice;
select InvoiceId,max(Total) from Invoice;
-- 5
select BillingAddress,BillingCity,BillingPostalCode,Total from Invoice where BillingCountry like '%Germany%';
-- 6
select BillingAddress,BillingCity,BillingPostalCode,Total from Invoice where Total > 15 and Total < 25;
-- 7
select distinct BillingCountry from Invoice;
-- 8
select FirstName,LastName,CustomerId,Country from Customer where Country not like '%USA%';
-- 9
select FirstName,LastName,CustomerId,Country from Customer where Country like '%Brazil%';
--10
SELECT Name FROM Track INNER JOIN InvoiceLine USING(TrackId);