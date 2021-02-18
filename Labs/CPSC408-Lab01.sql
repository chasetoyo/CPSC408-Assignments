select FirstName,LastName,Email from Employee;
select * from Artist;
select EmployeeId from Employee where Title like '%Manager%';
select InvoiceId,min(Total) from Invoice;
select InvoiceId,max(Total) from Invoice;
select BillingAddress,BillingCity,BillingPostalCode,Total from Invoice where BillingCountry like '%Germany%';\
select BillingAddress,BillingCity,BillingPostalCode,Total from Invoice where Total > 15 and Total < 25;
select distinct BillingCountry from Invoice;
select FirstName,LastName,CustomerId,Country from Customer where Country not like '%USA%';
select FirstName,LastName,CustomerId,Country from Customer where Country like '%Brazil%';
select Name from Playlist where PlaylistId like ;
SELECT Name FROM Track INNER JOIN InvoiceLine USING(TrackId);