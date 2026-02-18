# SQL Quick Reference Cheat Sheet
## For NYC Taxi Data Training

---

## Basic Query Structure

```sql
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column1
HAVING aggregate_condition
ORDER BY column1 DESC
LIMIT 100;
```

**Execution Order:** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

---

## SELECT Basics

```sql
-- All columns
SELECT * FROM trips LIMIT 10;

-- Specific columns
SELECT pickup_datetime, fare_amount FROM trips;

-- With alias
SELECT fare_amount AS fare FROM trips;

-- Calculated columns
SELECT fare_amount + tip_amount AS total FROM trips;
```

---

## WHERE Clause (Filter Rows)

```sql
-- Equality
WHERE passenger_count = 2

-- Comparison
WHERE fare_amount > 50
WHERE fare_amount >= 20 AND fare_amount <= 100

-- Multiple conditions
WHERE passenger_count = 2 AND fare_amount > 20
WHERE passenger_count = 1 OR passenger_count = 2

-- IN operator
WHERE passenger_count IN (1, 2, 3)

-- BETWEEN (inclusive)
WHERE fare_amount BETWEEN 20 AND 50

-- Pattern matching
WHERE zone_name LIKE 'Man%'  -- Starts with "Man"
WHERE zone_name LIKE '%Park%'  -- Contains "Park"

-- NULL checks
WHERE tip_amount IS NULL
WHERE tip_amount IS NOT NULL
```

---

## ORDER BY (Sort Results)

```sql
-- Ascending (default)
ORDER BY fare_amount

-- Descending
ORDER BY fare_amount DESC

-- Multiple columns
ORDER BY passenger_count, fare_amount DESC
```

---

## DISTINCT (Remove Duplicates)

```sql
-- Unique values
SELECT DISTINCT passenger_count FROM trips;

-- Count unique
SELECT COUNT(DISTINCT payment_type) FROM trips;
```

---

## Aggregate Functions

```sql
-- COUNT
SELECT COUNT(*) FROM trips;                    -- All rows
SELECT COUNT(tip_amount) FROM trips;           -- Non-NULL values
SELECT COUNT(DISTINCT payment_type) FROM trips; -- Unique values

-- SUM
SELECT SUM(fare_amount) FROM trips;

-- AVG
SELECT AVG(fare_amount) FROM trips;

-- MIN / MAX
SELECT MIN(fare_amount), MAX(fare_amount) FROM trips;

-- Multiple aggregates
SELECT 
    COUNT(*) AS total_trips,
    AVG(fare_amount) AS avg_fare,
    SUM(fare_amount) AS revenue
FROM trips;
```

---

## GROUP BY (Aggregate by Category)

```sql
-- Basic grouping
SELECT 
    passenger_count,
    COUNT(*) AS num_trips,
    AVG(fare_amount) AS avg_fare
FROM trips
GROUP BY passenger_count;

-- Multiple columns
SELECT 
    passenger_count,
    payment_type,
    COUNT(*) AS num_trips
FROM trips
GROUP BY passenger_count, payment_type;

-- With ORDER BY
SELECT 
    passenger_count,
    COUNT(*) AS num_trips
FROM trips
GROUP BY passenger_count
ORDER BY num_trips DESC;
```

**Rule:** Every column in SELECT must be either:
- In GROUP BY clause, OR
- Inside an aggregate function

---

## HAVING (Filter After Grouping)

```sql
-- Filter groups
SELECT 
    passenger_count,
    COUNT(*) AS num_trips
FROM trips
GROUP BY passenger_count
HAVING COUNT(*) > 1000;

-- WHERE vs HAVING
SELECT 
    passenger_count,
    AVG(fare_amount) AS avg_fare
FROM trips
WHERE fare_amount > 10          -- Filter BEFORE grouping
GROUP BY passenger_count
HAVING AVG(fare_amount) > 30    -- Filter AFTER grouping
```

---

## CASE Statements (If-Else Logic)

```sql
-- Simple CASE
SELECT 
    CASE 
        WHEN fare_amount < 10 THEN 'Cheap'
        WHEN fare_amount < 30 THEN 'Medium'
        ELSE 'Expensive'
    END AS fare_category,
    COUNT(*) AS num_trips
FROM trips
GROUP BY fare_category;

-- CASE in aggregation
SELECT 
    SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) AS credit_trips,
    SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) AS cash_trips
FROM trips;
```

---

## JOINs (Combine Tables)

```sql
-- INNER JOIN (matching rows only)
SELECT 
    t.pickup_datetime,
    z.zone_name,
    t.fare_amount
FROM trips t
INNER JOIN zones z ON t.pickup_location_id = z.location_id;

-- LEFT JOIN (all from left table)
SELECT 
    t.pickup_datetime,
    z.zone_name
FROM trips t
LEFT JOIN zones z ON t.pickup_location_id = z.location_id;

-- Multiple JOINs
SELECT 
    t.pickup_datetime,
    pickup_zone.zone_name AS pickup,
    dropoff_zone.zone_name AS dropoff
FROM trips t
INNER JOIN zones pickup_zone 
    ON t.pickup_location_id = pickup_zone.location_id
INNER JOIN zones dropoff_zone 
    ON t.dropoff_location_id = dropoff_zone.location_id;
```

---

## Subqueries

```sql
-- In WHERE clause
SELECT *
FROM trips
WHERE fare_amount > (SELECT AVG(fare_amount) FROM trips);

-- In FROM clause
SELECT 
    passenger_count,
    avg_fare
FROM (
    SELECT 
        passenger_count,
        AVG(fare_amount) AS avg_fare
    FROM trips
    GROUP BY passenger_count
) AS subquery
WHERE avg_fare > 30;

-- With IN
SELECT *
FROM trips
WHERE pickup_location_id IN (
    SELECT location_id 
    FROM zones 
    WHERE borough = 'Manhattan'
);
```

---

## CTEs (Common Table Expressions)

```sql
-- Single CTE
WITH high_fares AS (
    SELECT * 
    FROM trips 
    WHERE fare_amount > 50
)
SELECT 
    passenger_count,
    COUNT(*) AS num_trips
FROM high_fares
GROUP BY passenger_count;

-- Multiple CTEs
WITH 
manhattan_zones AS (
    SELECT location_id 
    FROM zones 
    WHERE borough = 'Manhattan'
),
manhattan_trips AS (
    SELECT t.*
    FROM trips t
    INNER JOIN manhattan_zones z
        ON t.pickup_location_id = z.location_id
)
SELECT 
    COUNT(*) AS total_trips,
    AVG(fare_amount) AS avg_fare
FROM manhattan_trips;
```

---

## Window Functions

```sql
-- ROW_NUMBER (sequential numbering)
SELECT 
    pickup_datetime,
    fare_amount,
    ROW_NUMBER() OVER (ORDER BY fare_amount DESC) AS fare_rank
FROM trips;

-- PARTITION BY (separate windows per group)
SELECT 
    passenger_count,
    fare_amount,
    ROW_NUMBER() OVER (
        PARTITION BY passenger_count 
        ORDER BY fare_amount DESC
    ) AS rank_in_group
FROM trips;

-- Running total
SELECT 
    pickup_datetime,
    fare_amount,
    SUM(fare_amount) OVER (
        ORDER BY pickup_datetime
    ) AS running_total
FROM trips;

-- LAG / LEAD (previous/next row)
SELECT 
    pickup_datetime,
    fare_amount,
    LAG(fare_amount) OVER (ORDER BY pickup_datetime) AS prev_fare,
    LEAD(fare_amount) OVER (ORDER BY pickup_datetime) AS next_fare
FROM trips;

-- Moving average
SELECT 
    pickup_datetime,
    fare_amount,
    AVG(fare_amount) OVER (
        ORDER BY pickup_datetime
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7
FROM trips;
```

---

## Date/Time Functions

```sql
-- Extract parts
EXTRACT(YEAR FROM pickup_datetime)
EXTRACT(MONTH FROM pickup_datetime)
EXTRACT(DAY FROM pickup_datetime)
EXTRACT(HOUR FROM pickup_datetime)
EXTRACT(DOW FROM pickup_datetime)  -- Day of week (0-6)

-- Truncate to date/hour/day/week/month
DATE_TRUNC('day', pickup_datetime)
DATE_TRUNC('hour', pickup_datetime)
DATE_TRUNC('week', pickup_datetime)
DATE_TRUNC('month', pickup_datetime)

-- Date difference
DATEDIFF('day', pickup_datetime, dropoff_datetime)

-- Date arithmetic
pickup_datetime + INTERVAL '1 day'
pickup_datetime - INTERVAL '2 hours'
```

---

## String Functions

```sql
-- Case conversion
UPPER(zone_name)
LOWER(zone_name)

-- Concatenation
CONCAT(zone_name, ' - ', borough)
zone_name || ' - ' || borough

-- Substring
SUBSTRING(zone_name, 1, 5)

-- Length
LENGTH(zone_name)

-- Trim whitespace
TRIM(zone_name)
```

---

## Math Functions

```sql
-- Rounding
ROUND(fare_amount, 2)
CEIL(fare_amount)
FLOOR(fare_amount)

-- Absolute value
ABS(fare_amount - tip_amount)

-- Power/Square root
POWER(trip_distance, 2)
SQRT(trip_distance)

-- NULL handling
COALESCE(tip_amount, 0)  -- Use 0 if NULL
NULLIF(trip_distance, 0)  -- Return NULL if 0
```

---

## UNION (Combine Result Sets)

```sql
-- UNION (removes duplicates)
SELECT location_id, zone_name FROM zones WHERE borough = 'Manhattan'
UNION
SELECT location_id, zone_name FROM zones WHERE borough = 'Brooklyn';

-- UNION ALL (keeps duplicates, faster)
SELECT location_id FROM zones WHERE borough = 'Manhattan'
UNION ALL
SELECT location_id FROM zones WHERE borough = 'Brooklyn';
```

---

## Performance Tips

```sql
-- Use LIMIT when exploring
SELECT * FROM trips LIMIT 100;

-- Be specific with columns (avoid SELECT *)
SELECT pickup_datetime, fare_amount FROM trips;

-- Filter early with WHERE
SELECT * FROM trips WHERE fare_amount > 100 LIMIT 10;

-- Use indexes (in production)
CREATE INDEX idx_pickup_location ON trips(pickup_location_id);

-- Explain query plan
EXPLAIN SELECT * FROM trips WHERE fare_amount > 50;
```

---

## Common Mistakes to Avoid

❌ **Using WHERE instead of HAVING**
```sql
-- Wrong: WHERE with aggregate
SELECT passenger_count, COUNT(*) 
FROM trips 
WHERE COUNT(*) > 100  -- ERROR!
GROUP BY passenger_count;

-- Correct: HAVING with aggregate
SELECT passenger_count, COUNT(*) 
FROM trips 
GROUP BY passenger_count
HAVING COUNT(*) > 100;  -- ✓
```

❌ **Missing GROUP BY columns**
```sql
-- Wrong: column not in GROUP BY
SELECT passenger_count, payment_type, COUNT(*) 
FROM trips 
GROUP BY passenger_count;  -- ERROR!

-- Correct: all non-aggregate columns in GROUP BY
SELECT passenger_count, payment_type, COUNT(*) 
FROM trips 
GROUP BY passenger_count, payment_type;  -- ✓
```

❌ **Comparing to NULL incorrectly**
```sql
-- Wrong: = NULL doesn't work
WHERE tip_amount = NULL  -- Always FALSE!

-- Correct: use IS NULL
WHERE tip_amount IS NULL  -- ✓
```

---

## Quick Tips

✅ Write queries incrementally (SELECT → WHERE → GROUP BY → ORDER BY)
✅ Test with LIMIT first
✅ Use table aliases (t, z) for readability
✅ Comment your code with `--`
✅ Format for readability (one column per line)
✅ Use CTEs for complex logic (more readable than nested subqueries)
✅ Start simple, add complexity gradually

---

## Example: Complete Analysis

```sql
-- Question: What are the top 10 most profitable pickup zones in Manhattan?

WITH manhattan_zones AS (
    -- Step 1: Get Manhattan zone IDs
    SELECT location_id, zone_name
    FROM zones
    WHERE borough = 'Manhattan'
),
manhattan_trips AS (
    -- Step 2: Filter trips to Manhattan pickups
    SELECT 
        t.pickup_location_id,
        t.fare_amount,
        t.trip_distance
    FROM trips t
    INNER JOIN manhattan_zones z 
        ON t.pickup_location_id = z.location_id
)
-- Step 3: Aggregate and rank
SELECT 
    z.zone_name,
    COUNT(*) AS num_trips,
    SUM(mt.fare_amount) AS total_revenue,
    AVG(mt.fare_amount) AS avg_fare,
    AVG(mt.trip_distance) AS avg_distance
FROM manhattan_trips mt
INNER JOIN manhattan_zones z 
    ON mt.pickup_location_id = z.location_id
GROUP BY z.zone_name
ORDER BY total_revenue DESC
LIMIT 10;
```

---

**Remember:** Practice is key! Try to solve problems without looking at solutions first. 🎓
