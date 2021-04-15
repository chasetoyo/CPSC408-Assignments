-- 1
create table Player (
pID integer primary key not null,
name varchar(64) not null,
teamName varchar(64)
);
-- 2
alter table Player
    add column age int;
-- 3
insert into Player values
(1, 'Player 1', 'Team A', 23),
(2, 'Player	2',	'Team A', null),
(3, 'Player	3',	'Team B', 28),
(4, 'Player	4',	'Team B', null);
-- 4
delete from Player where pID = 2;
-- 5
update Player set age = 25 where age is null;
-- 6
select count(*) count, avg(age) avg_age
from Player;
-- 7
drop table Player;
-- 8
select avg(Total) Brazil_Avg from Invoice
where BillingCountry = 'Brazil';
-- 9
SELECT BillingCity, avg(Total) Average
FROM Invoice
where BillingCountry = 'Brazil'
group by BillingCity;
-- 10
-- this gets the correct albumid, need to link to album name
-- SELECT AlbumID, count(*) as x
-- from Track
-- group by AlbumId having x > 20;
select s.Title from
(SELECT A.Title, count(*) as ct
from Track
INNER JOIN Album A on A.AlbumId = Track.AlbumId
group by Track.AlbumId having ct > 20) as s;
-- 11
select count(*) '2010'
from Invoice
where substr(InvoiceDate,1,4) = '2010';
-- 12
select BillingCountry, count(BillingCity) from Invoice
group by BillingCountry;
-- 13
-- album has the album title
-- track has the track name, albumid, and mediatypeid
-- mediatype has mediatypeid and name
select Album.Title Album, T.Name Track_Name, MT.Name Media_Type
from Album
INNER JOIN Track T on T.AlbumId = Album.AlbumId
INNER JOIN MediaType MT on T.MediaTypeId = MT.MediaTypeId;
-- 14
select count(*) Jane_Peacock_Ct from Customer
where SupportRepId =
(select EmployeeId from Employee
where FirstName || ' ' || LastName = 'Jane Peacock');

-- BONUS
-- Write a query to find the standard deviation of the sum of totals in the invoices table per billing
-- country. (You cannot use the built in stdev function, but can make use of the square, sqrt functions
-- etc.)

-- gets sum per billingcountry
-- select sum(Total) Total, BillingCountry from Invoice
-- group by BillingCountry;

-- mean of sum
-- select avg(subquery.Total) Average, Invoice.BillingCountry
-- from Invoice,
-- (select sum(i2.Total) Total, i2.BillingCountry from Invoice i2
-- group by i2.BillingCountry) subquery
-- group by Invoice.BillingCountry;

-- (xi - mean)^2
-- select s1.Total, s2.Average, s1.total - s2.Average, square(s1.total-s2.Average),s1.BillingCountry, count(*) from
-- (select sum(Total) Total, BillingCountry from Invoice
-- group by BillingCountry) as s1
-- join
-- (select avg(subquery.Total) Average, Invoice.BillingCountry
-- from Invoice,
-- (select sum(i2.Total) Total, i2.BillingCountry from Invoice i2
-- group by i2.BillingCountry) subquery
-- group by Invoice.BillingCountry) as s2
-- group by s1.BillingCountry;

-- stdev
-- this is the final answer
select sum(s3.sqr)/s3.ct stdev from
(select s1.Total, s2.Average, s1.total - s2.Average, square(s1.total-s2.Average) sqr, s1.BillingCountry, count(*) ct from
(select sum(Total) Total, BillingCountry from Invoice
group by BillingCountry) as s1
join
(select avg(subquery.Total) Average, Invoice.BillingCountry
from Invoice,
(select sum(i2.Total) Total, i2.BillingCountry from Invoice i2
group by i2.BillingCountry) subquery
group by Invoice.BillingCountry) as s2
group by s1.BillingCountry) as s3;