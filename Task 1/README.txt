Checkout Analysis SQL Scripts
==============================

Overview
--------
This set of SQL scripts is designed to analyze checkout data by hour, focusing on various metrics such as daily checkout counts, historical comparisons, and percentage concentrations. The scripts create necessary tables, compute aggregate metrics, and provide insights into checkout trends.

Prerequisites
-------------
- Database System: MySQL 8.0 or higher
- Tables Required: Ensure that `checkout_1` and `checkout_2` tables are populated with relevant data before executing the scripts.

Instructions
------------
1. Create Main Table:
    - The script creates a `checkout` table to store hourly checkout data.
    - Run the following command to create the table:
      ```
      CREATE TABLE `checkout` (
        `time` VARCHAR(4) NOT NULL, 
        `today` INT DEFAULT NULL,
        `yesterday` INT DEFAULT NULL,
        `same_day_last_week` INT DEFAULT NULL,
        `avg_last_week` DOUBLE DEFAULT NULL,
        `avg_last_month` DOUBLE DEFAULT NULL,
        PRIMARY KEY (`time`)
      );
      ```

2. Create Temporary Tables:
    - `checkout_all`: Aggregates data by hour per day across various metrics.
    - `concentration_checkout_all`: Aggregates and calculates the concentration of checkouts by hour.
    - Run the script in the following order to create the temporary tables:
      ```
      CREATE TEMPORARY TABLE checkout_all AS
      ...
      CREATE TEMPORARY TABLE concentration_checkout_all AS
      ...
      ```

3. Run Analysis Queries:
    - Deviation Analysis: Calculate deviations of today's checkout count and concentration compared to the average.
    - Difference Analysis: Analyze the difference between checkout metrics of `c2` and `c1` by hour.
    - Comparison with Historical Data: Compare today's checkout metrics to historical data to identify minimum, maximum, and average values.
    - Execute the provided queries to perform the analysis.

4. Clean Up:
    - After running the queries and completing the analysis, drop the temporary tables to free up resources:
      ```
      DROP TABLE concentration_checkout_all;
      DROP TABLE checkout_all;
      ```

Description of Scripts
-----------------------
- Table Creation:
  - Creates the `checkout` table to store hourly checkout data.
  
- Temporary Tables:
  - `checkout_all`: Aggregates daily data by hour from `checkout_1` and `checkout_2`.
  - `concentration_checkout_all`: Calculates the concentration of checkouts by hour as a percentage of the total daily checkouts.

- Deviation Analysis:
  - Calculates the deviation of today's checkout counts and concentration compared to historical averages.

- Difference Analysis:
  - Determines the difference in checkout counts and concentration between `c2` and `c1` by hour.

- Historical Comparison:
  - Compares today's checkout data with historical values to determine the minimum, maximum, and average metrics.

Troubleshooting
--------------- 
- Database Compatibility: These scripts are optimized for MySQL. Adjustments may be necessary if running on another SQL dialect (e.g., PostgreSQL).