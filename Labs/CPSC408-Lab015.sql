--1
SELECT max(Total) Max_Invoice_Total FROM Invoice;
--2
SELECT Total FROM Invoice ORDER BY Total DESC LIMIT 1;
--3
-- select count(*) from Track;
SELECT MediaType.Name, count(*) Num_Tracks FROM MediaType
INNER JOIN Track
USING (MediaTypeId)
GROUP BY MediaType.Name;
--4
select MediaType.Name, count(*) Num_Tracks FROM MediaType
INNER JOIN Track
USING (MediaTypeId)
GROUP BY MediaType.Name
ORDER BY Num_Tracks desc;
--5
SELECT MediaType.Name, count(*) Num_Tracks FROM MediaType
INNER JOIN Track
USING (MediaTypeId)
GROUP BY MediaType.Name
HAVING (Num_Tracks > 200)
ORDER BY Num_Tracks desc;
--6
-- select count(*) from Track; (returns 3503)
-- join Artist, Track, Album
SELECT count(*) Count_A_Artist FROM Track
INNER JOIN Album A on A.AlbumId = Track.AlbumId
INNER JOIN Artist A2 on A2.ArtistId = A.ArtistId
WHERE A2.Name LIKE 'A%';
--7
SELECT FirstName || " " || LastName Full_Name,
substr(BirthDate, 1, 3) || '0' Decade from Employee;
--get decade and cat '0'