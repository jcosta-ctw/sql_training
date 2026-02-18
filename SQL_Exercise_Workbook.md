# SQL Training - Exercise Workbook
## NYC Taxi Dataset Exercises with Solutions

---

## Database Schema

**trips table:**
```
trip_id              INT
pickup_datetime      TIMESTAMP
dropoff_datetime     TIMESTAMP
pickup_location_id   INT
dropoff_location_id  INT
passenger_count      INT
trip_distance        DECIMAL
fare_amount          DECIMAL
tip_amount           DECIMAL
total_amount         DECIMAL
payment_type         INT (1=Credit, 2=Cash, 3=No Charge, 4=Dispute)
```

**zones table:**
```
location_id          INT
zone_name            VARCHAR
borough              VARCHAR
```

---

## PART 1: Basic SELECT & WHERE (Exercises 1-5)

### Exercise 1: First Query
**Task:** Write a query to select the first 10 trips showing only pickup time and fare amount.

### Exercise 2: Column Calculations
**Task:** Select pickup time, fare amount, tip amount, and calculate the total (fare + tip). Name the calculated column `total_paid`. Show first 20 rows.

### Exercise 3: Filtering Trips
**Task:** Find all trips with exactly 2 passengers where the fare was more than $30. Show pickup time, passenger count, and fare. Limit to 50 rows.

### Exercise 4: Using IN Operator
**Task:** Find trips with 1, 2, or 3 passengers and fare between $20 and $50. Show all columns. Limit to 100 rows.

### Exercise 5: Top Fares
**Task:** Find the 20 most expensive trips. Show pickup time, passenger count, distance, and fare. Sort by fare descending.

## PART 2: Aggregations & GROUP BY (Exercises 6-10)

### Exercise 6: Basic Statistics
**Task:** Calculate the following for ALL trips:
- Total number of trips
- Total revenue (sum of fares)
- Average fare
- Minimum fare
- Maximum fare


### Exercise 7: Trips by Passenger Count
**Task:** For each passenger count value (1-6), show:
- The passenger count
- Number of trips
- Average fare
- Average trip distance

Sort by passenger count.


### Exercise 8: Payment Type Analysis
**Task:** For each payment type, show:
- Payment type (use CASE to show 'Credit', 'Cash', 'Other')
- Number of trips
- Average fare
- Average tip
- Tip as percentage of fare

Sort by number of trips descending.


### Exercise 9: High Volume Zones
**Task:** Find pickup locations with more than 5,000 trips. Show:
- Pickup location ID
- Number of trips
- Total revenue
- Average fare

Sort by revenue descending.


### Exercise 10: Distance Categories
**Task:** Categorize trips by distance:
- 'Short' (< 2 miles)
- 'Medium' (2-5 miles)
- 'Long' (> 5 miles)

For each category show trip count and average fare. Sort by category.


## PART 3: JOINs (Exercises 11-15)

### Exercise 11: Basic JOIN
**Task:** Join trips with zones to show pickup zone names. Display:
- Pickup time
- Pickup zone name
- Pickup borough
- Fare amount

Limit to 50 rows.


### Exercise 12: Double JOIN
**Task:** Show pickup AND dropoff zone names for each trip. Display:
- Pickup time
- Pickup zone name
- Dropoff zone name
- Trip distance
- Fare amount

Limit to 50 rows.


### Exercise 13: Manhattan Analysis
**Task:** Find all trips that started in Manhattan. Show:
- Borough (should all be Manhattan)
- Zone name
- Number of trips
- Average fare
- Total revenue

Sort by number of trips descending. Show top 10 zones.


### Exercise 14: Borough-to-Borough Traffic
**Task:** Find the most popular borough-to-borough routes. Show:
- Pickup borough
- Dropoff borough
- Number of trips
- Average fare

Sort by trip count descending. Show top 20 routes.


### Exercise 15: LEFT JOIN to Find Missing Data
**Task:** Find trips that have an invalid pickup_location_id (not in zones table). Use LEFT JOIN. Show:
- Count of trips with valid zones
- Count of trips with invalid zones (NULL zone_name)


## PART 4: Subqueries & CTEs (Exercises 16-18)

### Exercise 16: Subquery in WHERE
**Task:** Find all trips where the fare is above the average fare. Show:
- Pickup time
- Fare amount
- How much above average (fare - average)

Limit to 100 rows.


### Exercise 17: CTE for Readability
**Task:** Rewrite Exercise 16 using a CTE. The result should be the same but more readable.


### Exercise 18: Multi-Step CTE Analysis
**Task:** Create a multi-step analysis:
1. CTE 1: Get daily trip counts and revenue
2. CTE 2: Calculate 7-day moving averages
3. Final query: Show dates with above-average daily revenue


## PART 5: Window Functions (Exercises 19-22)

### Exercise 19: Ranking Zones
**Task:** Rank pickup zones by total revenue. Show:
- Rank (1 = highest revenue)
- Zone name
- Borough
- Total revenue
- Number of trips

Show top 20.


### Exercise 20: Top 3 Trips Per Zone
**Task:** For each pickup zone, find the 3 most expensive trips. Show:
- Zone name
- Pickup time
- Fare amount
- Rank within zone (1, 2, 3)

Use QUALIFY to filter.


### Exercise 21: Running Total
**Task:** Calculate running total of trips by date. Show:
- Date
- Daily trip count
- Cumulative trips (running total)


### Exercise 22: Day-over-Day Comparison
**Task:** Compare each day's revenue to the previous day. Show:
- Date
- Daily revenue
- Previous day revenue
- Change amount
- Change percentage


## BONUS CHALLENGES (Advanced)

### Bonus 1: Most Profitable Routes
**Task:** Find the 10 most profitable pickup-dropoff zone pairs. Consider both:
- Total revenue generated
- Number of trips (must have at least 100 trips)
- Average fare

Show pickup zone, dropoff zone, metrics above.


### Bonus 2: Peak Hours Analysis
**Task:** Find the busiest hour of each day of week. Show:
- Day of week (Monday, Tuesday, etc.)
- Hour (0-23)
- Number of trips
- Rank within that day (1 = busiest hour)


### Bonus 3: Cohort Analysis
**Task:** Create a cohort analysis showing:
- Week of first trip (cohort week)
- Weeks since first trip (0, 1, 2, ...)
- Number of unique zones with pickups
- Total trips

This shows how pickup activity grows over time.


## ANSWER KEY SUMMARY

### Quick Reference

**Basic Queries:**
- SELECT, WHERE, LIMIT, ORDER BY

**Aggregations:**
- COUNT(*), SUM(), AVG(), MIN(), MAX()
- GROUP BY, HAVING

**JOINs:**
- INNER JOIN (matching rows only)
- LEFT JOIN (all from left table)
- Multiple JOINs (same table twice with different aliases)

**Advanced:**
- Subqueries (query inside query)
- CTEs (WITH clause - named subqueries)
- Window Functions (ROW_NUMBER, LAG, running totals)

---

## TIPS FOR SUCCESS

1. **Start Simple:** Build queries incrementally. Get SELECT working, then add WHERE, then ORDER BY, etc.

2. **Use LIMIT:** Always test with LIMIT 10 or LIMIT 100 first to avoid overwhelming output.

3. **Comment Your Code:** Use `--` for comments to document your logic.

4. **Formatting Matters:** 
   - Put each column on its own line
   - Indent nested queries
   - Use consistent capitalization (KEYWORDS in caps)

5. **Test Incrementally:** 
   - Test each CTE separately
   - Build window functions step by step
   - Check GROUP BY before adding HAVING

6. **Common Mistakes:**
   - Forgetting to GROUP BY all non-aggregate columns
   - Using WHERE instead of HAVING (or vice versa)
   - Missing table aliases in multi-table queries
   - Not handling NULL values (use COALESCE or NULLIF)

---
