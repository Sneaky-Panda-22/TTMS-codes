USE TTMS;
-- DDL illustrations

-- CREATE
CREATE TABLE DemoEquipment (
    demo_id INT PRIMARY KEY,
    equipment_name VARCHAR(100)
);

-- INSERT some test records
INSERT INTO DemoEquipment
VALUES
(1, 'Test Blade'),
(2, 'Test Rubber');

SELECT * FROM DemoEquipment;

-- ALTER
ALTER TABLE DemoEquipment
ADD COLUMN price DECIMAL(10,2);

-- TRUNCATE
TRUNCATE TABLE DemoEquipment;

-- DROP
DROP TABLE DemoEquipment;




-- DML Illustrations

-- INSERT
INSERT INTO Player (name, playing_style, grip_type)
VALUES ('Demo Player', 'offensive', 'shakehand');

SELECT * FROM Player WHERE NAME = 'Demo Player';

select model,price from Blade where blade_id = 1;

-- UPDATE
UPDATE Blade
SET price = price + 100
WHERE blade_id = 1;

-- DELETE
DELETE FROM Player
WHERE name = 'Demo Player';




-- OPERATORS

-- Comparison and logical operators

-- Find no. of offensive players who use the shakehand grip:
SELECT * FROM Player WHERE playing_style = 'offensive' AND grip_type = 'shakehand' LIMIT 10;

-- Find blades costing more than ₹3,000:
SELECT COUNT(*) FROM Blade WHERE price > 3000;
-- price < 2000
SELECT brand, model, price
FROM Blade
WHERE price < 2000;

-- IN and NOT IN
-- Find players with either an offensive or defensive playing style:
SELECT COUNT(*) FROM Player WHERE playing_style IN ('offensive','defensive');


-- Find blades whose material is neither carbon nor wood.
SELECT blade_id, brand, model, material
FROM Blade
WHERE material NOT IN ('Carbon', 'Wood')
LIMIT 10;

-- BETWEEN
-- Find blades within a price range 2000 and 5000:
SELECT blade_id,brand,model,price FROM Blade WHERE price BETWEEN 2000 AND 5000;

-- Find rubbers priced between ₹500 and ₹2000.
SELECT rubber_id, brand, model, price
FROM Rubber
WHERE price BETWEEN 500 AND 2000;

-- LIKE
-- Find players whose names begin with 'A':
SELECT * FROM Player WHERE name LIKE 'A%';

-- Find rubber models containing the word Hurricane.
SELECT rubber_id, brand, model
FROM Rubber
WHERE model LIKE '%Hurricane%';

-- IS NULL
-- Find equipment whose material has not been recorded:
SELECT * FROM Blade WHERE material IS NULL;

-- EXISTS
-- Find players who have at least one recorded setup:
SELECT * FROM Player AS p WHERE EXISTS (SELECT 1 FROM Setup s WHERE s.player_id = p.player_id);
-- Find blades that are used in at least one setup.
SELECT b.blade_id, b.brand, b.model
FROM Blade b
WHERE EXISTS (
    SELECT 1
    FROM Setup s
    WHERE s.blade_id = b.blade_id
);

-- string
-- Display all blade brands in uppercase.
SELECT blade_id, brand, UPPER(brand) AS uppercase_brand FROM Blade LIMIT 10;

-- Display each rubber's brand and model together as a single name.
SELECT rubber_id,
       CONCAT(brand, ' ', model) AS rubber_name
FROM Rubber
LIMIT 10;

-- Arithmetic operators
-- Display what will be the price of each glue after incrementing the price by 10%:
SELECT name,price as old_price,price*1.1 AS new_price FROM Glue;

-- Calculate the price of each blade after applying a 10% discount.
SELECT blade_id, brand, model, price,
       ROUND(price * 0.90, 2) AS discounted_price
FROM Blade
LIMIT 10;

-- Aggregate functions
-- find the total number of players, total inventory cost,average blade cost,cheapest blade,most expensixe blade
SELECT COUNT(*) AS total_blades FROM Blade;
SELECT COUNT(*) AS total_blades, SUM(price) AS total_blade_value, AVG(price) AS average_blade_price, MIN(price) AS cheapest_blade, MAX(price) AS most_expensive_blad FROM Blade;

-- Query 1: Count the players
SELECT COUNT(*) AS total_players
FROM Player;

-- Query 2: Count the setups
SELECT COUNT(*) AS total_setups
FROM Setup;


-- GROUP BY
-- calculate the number of players for each playing style:
SELECT playing_style, COUNT(*) AS player_count FROM Player GROUP BY playing_style;
-- Count the number of setups recorded for each player
SELECT player_id, COUNT(*) AS setup_count
FROM Setup
GROUP BY player_id;


-- Numeric functions
SELECT ROUND(AVG(price), 2) AS average_price,CEIL(AVG(price)) AS rounded_up_average,FLOOR(AVG(price)) AS rounded_down_average FROM Blade;

SELECT ROUND(AVG(price), 2) AS average_blade_price
FROM Blade;

SELECT ROUND(AVG(price), 2) AS average_rubber_price
FROM Rubber;

-- Date and time functions
SELECT setup_id,created_at,YEAR(created_at) AS setup_year,MONTH(created_at) AS setup_month,DATE(created_at) AS setup_date FROM Setup LIMIT 10;

-- UNION and UNION ALL
SELECT brand FROM Blade UNION SELECT brand FROM Rubber;
SELECT brand FROM Blade UNION ALL SELECT brand FROM Rubber;

-- Simple subquery
-- Find blades that cost more than the average blade price:
SELECT brand,model,price FROM Blade WHERE price > (SELECT AVG(price) FROM Blade);

-- Nested subquery
-- Find players who have recorded a setup using a blade that costs more than the average blade price:

SELECT DISTINCT p.player_id,p.name FROM Player AS p WHERE p.player_id IN(
    SELECT s.player_id FROM Setup AS s WHERE s.blade_id IN(
        SELECT b.blade_id FROM Blade AS b WHERE b.price > (
            SELECT AVG(price) FROM Blade
        )
    )
);

-- Correlated subquery
SELECT p.player_id, p.name
FROM Player p
WHERE (
    SELECT COUNT(*)
    FROM Setup s
    WHERE s.player_id = p.player_id
) > (
    SELECT AVG(setup_count)
    FROM (
        SELECT COUNT(*) AS setup_count
        FROM Setup
        GROUP BY player_id
    ) AS player_setup_counts
);

-- Procedures: 
-- get the info of blades that are between a price range (a,b):
create procedure getBladesByPrice(
    IN min_price DECIMAL(10,2),
    IN max_price DECIMAL(10,2)
) 
BEGIN 
    select brand, model, price from Blade where price between min_price and max_price; 
END

call getBladesByPrice(2000,5000);

-- View a Player's Complete Setup
CREATE PROCEDURE GetPlayerSetup(IN p_player_id INT)
BEGIN
    SELECT
        P.name AS Player_Name,
        B.brand AS Blade_Brand,
        B.model AS Blade_Model,
        RF.brand AS Forehand_Rubber_Brand,
        RF.model AS Forehand_Rubber_Model,
        RB.brand AS Backhand_Rubber_Brand,
        RB.model AS Backhand_Rubber_Model,
        G.brand AS Glue_Brand,
        G.name AS Glue_Name,
        S.created_at AS Setup_Date
    FROM Setup S
    JOIN Player P
        ON S.player_id = P.player_id
    JOIN Blade B
        ON S.blade_id = B.blade_id
    JOIN Rubber RF
        ON S.forehand_rubber_id = RF.rubber_id
    JOIN Rubber RB
        ON S.backhand_rubber_id = RB.rubber_id
    JOIN Glue G
        ON S.glue_id = G.glue_id
    WHERE P.player_id = p_player_id;
END

call GetPlayerSetup(1);

-- Find Players Using a Particular Blade
CREATE PROCEDURE FindPlayersUsingBlade(IN p_blade_id INT)
BEGIN
    SELECT
        P.player_id,
        P.name AS Player_Name,
        P.playing_style,
        B.brand AS Blade_Brand,
        B.model AS Blade_Model,
        S.created_at AS Setup_Date
    FROM Setup S
    JOIN Player P
        ON S.player_id = P.player_id
    JOIN Blade B
        ON S.blade_id = B.blade_id
    WHERE B.blade_id = p_blade_id
    ORDER BY P.name;
END

call FindPlayersUsingBlade(1);


-- Find a player's total equipment cost
CREATE PROCEDURE GetPlayerSetupCosts(IN p_player_id INT)
BEGIN
    SELECT
        P.name AS Player_Name,
        S.setup_id AS Setup_ID,
        B.price AS Blade_Price,
        RF.price AS Forehand_Rubber_Price,
        RB.price AS Backhand_Rubber_Price,
        G.price AS Glue_Price,
        (
            B.price + RF.price + RB.price + G.price
        ) AS Total_Equipment_Cost
    FROM Setup S
    JOIN Player P
        ON S.player_id = P.player_id
    JOIN Blade B
        ON S.blade_id = B.blade_id
    JOIN Rubber RF
        ON S.forehand_rubber_id = RF.rubber_id
    JOIN Rubber RB
        ON S.backhand_rubber_id = RB.rubber_id
    JOIN Glue G
        ON S.glue_id = G.glue_id
    WHERE P.player_id = p_player_id;
END

call GetPlayerSetupCosts(1);