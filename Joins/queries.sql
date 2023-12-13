-- Join the two tables so that every column and record appears, regardless of if there is not an owner_id .
SELECT * FROM owners
FULL JOIN vehicles
ON owners.id = vehicles.owner_id;

--  id | first_name | last_name | id |  make  |  model  | year |  price   | owner_id
-- ----+------------+-----------+----+--------+---------+------+----------+----------
--   1 | Bob        | Hope      |  1 | Toyota | Corolla | 2002 |  2999.99 |        1
--   1 | Bob        | Hope      |  2 | Honda  | Civic   | 2012 | 12999.99 |        1
--   2 | Jane       | Smith     |  3 | Nissan | Altima  | 2016 | 23999.99 |        2
--   2 | Jane       | Smith     |  4 | Subaru | Legacy  | 2006 |  5999.99 |        2
--   3 | Melody     | Jones     |  5 | Ford   | F150    | 2012 |  2599.99 |        3
--   3 | Melody     | Jones     |  6 | GMC    | Yukon   | 2016 | 12999.99 |        3
--   4 | Sarah      | Palmer    |  7 | GMC    | Yukon   | 2014 | 22999.99 |        4
--   4 | Sarah      | Palmer    |  8 | Toyota | Avalon  | 2009 | 12999.99 |        4
--   4 | Sarah      | Palmer    |  9 | Toyota | Camry   | 2013 | 12999.99 |        4
--   5 | Alex       | Miller    | 10 | Honda  | Civic   | 2001 |  7999.99 |        5
--   6 | Shana      | Smith     | 11 | Nissan | Altima  | 1999 |  1899.99 |        6
--   6 | Shana      | Smith     | 12 | Lexus  | ES350   | 1998 |  1599.99 |        6
--   6 | Shana      | Smith     | 13 | BMW    | 300     | 2012 | 22999.99 |        6
--   6 | Shana      | Smith     | 14 | BMW    | 700     | 2015 | 52999.99 |        6
--   7 | Maya       | Malarkin  |    |        |         |      |          |
-- (15 rows)


--Count the number of cars for each owner. Display the owners first_name , last_name and count of vehicles. The first_name should be ordered in ascending order. Your output should look like this:
SELECT 
  first_name,
  last_name,
  COUNT(vehicles.id) AS vehicle_count
FROM owners
LEFT JOIN
  vehicles
ON
  owners.id = vehicles.owner_id
GROUP BY
  first_name, last_name
ORDER BY
  first_name ASC;

--  first_name | last_name | vehicle_count
-- ------------+-----------+---------------
--  Alex       | Miller    |             1
--  Bob        | Hope      |             2
--  Jane       | Smith     |             2
--  Maya       | Malarkin  |             0
--  Melody     | Jones     |             2
--  Sarah      | Palmer    |             3
--  Shana      | Smith     |             4
-- (7 rows)


-- Count the number of cars for each owner and display the average price for each of the cars as integers. Display the owners first_name , last_name, average price and count of vehicles. The first_name should be ordered in descending order. Only display results with more than one vehicle and an average price greater than 10000. Your output should look like this:
SELECT
  first_name,
  last_name,
  COUNT(vehicles.id) AS vehicle_count,
  ROUND(AVG(vehicles.price)) AS average_price
FROM
  owners
JOIN
  vehicles
ON owners.id = vehicles.owner_id
GROUP BY
  (first_name, last_name)
HAVING
  COUNT(vehicles.id) > 1 AND AVG(vehicles.price) > 10000
ORDER BY
  first_name DESC;

--  first_name | last_name | vehicle_count | average_price
-- ------------+-----------+---------------+---------------
--  Shana      | Smith     |             4 |         19875
--  Sarah      | Palmer    |             3 |         16333
--  Jane       | Smith     |             2 |         15000
-- (3 rows)

-- aggregate data for EACH owner, 