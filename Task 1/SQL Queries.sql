-- Table schema: checkout table to store hourly data
CREATE TABLE `checkout` (
  `time` VARCHAR(4) NOT NULL, 
  `today` INT DEFAULT NULL,
  `yesterday` INT DEFAULT NULL,
  `same_day_last_week` INT DEFAULT NULL,
  `avg_last_week` DOUBLE DEFAULT NULL,
  `avg_last_month` DOUBLE DEFAULT NULL,
  PRIMARY KEY (`time`) 
);

-- Temporary table to aggregate quantity of checkouts by hour per day
CREATE TEMPORARY TABLE checkout_all AS
SELECT
    c1.time,
    c2.today AS today_c2, 
    c2.yesterday AS yesterday_c2,
    c1.yesterday AS yesterday_c1,
    c2.same_day_last_week AS same_day_last_week_c2,
    c1.same_day_last_week AS same_day_last_week_c1,
    c2.avg_last_week AS avg_last_week_c2,
    c1.avg_last_week AS avg_last_week_c1,    
    c2.avg_last_month AS avg_last_month_c2,
    c1.avg_last_month AS avg_last_month_c1,
    ROUND(
		(c2.today + c2.yesterday + c1.yesterday + c2.same_day_last_week + c1.same_day_last_week +
		c2.avg_last_week + c1.avg_last_week + c2.avg_last_month + c1.avg_last_month) /9.0, 2) AS time_avg
FROM 
    checkout_1 c1
LEFT JOIN 
    checkout_2 c2 ON c1.time = c2.time;


-- Temporary table to aggregate and calculate concentration of checkouts by hour per day
CREATE TEMPORARY TABLE concentration_checkout_all AS
SELECT 
    c1.time,
    -- Calculte percentage changes for checkout_1 and checkout_2
    ROUND(SUM(c2.today) * 100.0 / (SELECT SUM(today) FROM checkout_2), 2) AS perc_today_c2,
    ROUND(SUM(c2.yesterday) * 100.0 / (SELECT SUM(yesterday) FROM checkout_2), 2) AS perc_yesterday_c2,
	ROUND(SUM(c1.yesterday) * 100.0 / (SELECT SUM(yesterday) FROM checkout_1), 2) AS perc_yesterday_c1,   
    ROUND(SUM(c2.same_day_last_week) * 100.0 / (SELECT SUM(same_day_last_week) FROM checkout_2), 2) AS perc_same_day_last_week_c2,
    ROUND(SUM(c1.same_day_last_week) * 100.0 / (SELECT SUM(same_day_last_week) FROM checkout_1), 2) AS perc_same_day_last_week_c1,
    ROUND(SUM(c2.avg_last_week) * 100.0 / (SELECT SUM(avg_last_week) FROM checkout_2), 2) AS perc_avg_last_week_c2,
    ROUND(SUM(c1.avg_last_week) * 100.0 / (SELECT SUM(avg_last_week) FROM checkout_1), 2) AS perc_avg_last_week_c1,    
    ROUND(SUM(c2.avg_last_month) * 100.0 / (SELECT SUM(avg_last_month) FROM checkout_2), 2) AS perc_avg_last_month_c2,
    ROUND(SUM(c1.avg_last_month) * 100.0 / (SELECT SUM(avg_last_month) FROM checkout_1), 2) AS perc_avg_last_month_c1,
    
    -- Calculate average percentage per hour by averaging all percentage calculations
    ROUND(
        (ROUND(SUM(c2.today) *100.0/ (SELECT SUM(today) FROM checkout_2), 2) +
        ROUND(SUM(c2.yesterday) *100.0/ (SELECT SUM(yesterday) FROM checkout_2), 2) +
        ROUND(SUM(c1.yesterday) *100.0/ (SELECT SUM(yesterday) FROM checkout_1), 2) +   
        ROUND(SUM(c2.same_day_last_week) *100.0/ (SELECT SUM(same_day_last_week) FROM checkout_2), 2) +
        ROUND(SUM(c1.same_day_last_week) *100.0/ (SELECT SUM(same_day_last_week) FROM checkout_1), 2) +
        ROUND(SUM(c2.avg_last_week) *100.0/ (SELECT SUM(avg_last_week) FROM checkout_2), 2) +
        ROUND(SUM(c1.avg_last_week) *100.0/ (SELECT SUM(avg_last_week) FROM checkout_1), 2) +    
        ROUND(SUM(c2.avg_last_month) *100.0/ (SELECT SUM(avg_last_month) FROM checkout_2), 2) +
        ROUND(SUM(c1.avg_last_month) *100.0/ (SELECT SUM(avg_last_month) FROM checkout_1), 2)
        ) /9.0, 2) AS perc_time_avg
FROM 
    checkout_1 c1
LEFT JOIN 
    checkout_2 c2 ON c1.time = c2.time
GROUP BY 
    c1.time;
    
-- Calculate the deviation of quantity of checkouts compared to the average
SELECT 
	time,
	ROUND(today_c2 - time_avg, 2) AS today_c2_dev,
    ROUND(yesterday_c2 - time_avg, 2) AS yesterday_c2_dev,
    ROUND(yesterday_c1 - time_avg, 2) AS yesterday_c1_dev,
	ROUND(same_day_last_week_c2 - time_avg, 2) AS same_day_last_week_c2_dev,
    ROUND(same_day_last_week_c1 - time_avg, 2) AS same_day_last_week_c1_dev,
    ROUND(avg_last_week_c2 - time_avg, 2) AS avg_last_week_c2_dev,  
    ROUND(avg_last_week_c1 - time_avg, 2) AS avg_last_week_c1_dev,    
    ROUND(avg_last_month_c2 - time_avg, 2) AS avg_last_month_c2_dev,  
    ROUND(avg_last_month_c1 - time_avg, 2) AS avg_last_month_c1_dev
FROM 
	checkout_all;


-- Calculate the deviation of concentration of checkouts compared to the average
SELECT 
	time,
	ROUND(perc_today_c2 - perc_time_avg, 2) AS perc_today_c2_dev,
    ROUND(perc_yesterday_c2 - perc_time_avg, 2) AS perc_yesterday_c2_dev,
    ROUND(perc_yesterday_c1 - perc_time_avg, 2) AS perc_yesterday_c1_dev,
	ROUND(perc_same_day_last_week_c2 - perc_time_avg, 2) AS perc_same_day_last_week_c2_dev,
    ROUND(perc_same_day_last_week_c1 - perc_time_avg, 2) AS perc_same_day_last_week_c1_dev,
    ROUND(perc_avg_last_week_c2 - perc_time_avg, 2) AS perc_avg_last_week_c2_dev,  
    ROUND(perc_avg_last_week_c1 - perc_time_avg, 2) AS perc_avg_last_week_c1_dev,    
    ROUND(perc_avg_last_month_c2 - perc_time_avg, 2) AS perc_avg_last_month_c2_dev,  
    ROUND(perc_avg_last_month_c1 - perc_time_avg, 2) AS perc_avg_last_month_c1_dev
FROM 
	concentration_checkout_all;
    
    
-- Calculate the difference in checkout quantity between c2 and c1 by hour
SELECT 
	time,
    ROUND(today_c2 - yesterday_c2, 2) AS today_c2_dif,
    ROUND(yesterday_c2 - yesterday_c1, 2) AS yesterday_c2_dif,
    ROUND(same_day_last_week_c2 - same_day_last_week_c1, 2) AS same_day_last_week_dif,
    ROUND(avg_last_week_c2 - avg_last_week_c1, 2) AS avg_last_week_dif,
    ROUND(avg_last_month_c2 - avg_last_month_c1, 2) AS avg_last_month_dif
FROM 
	checkout_all;


-- Calculate the difference in checkout concentration between c2 and c1 by hour
SELECT 
	time,
    ROUND(perc_today_c2 - perc_yesterday_c2, 2) AS perc_today_c2_dif,
    ROUND(perc_yesterday_c2 - perc_yesterday_c1, 2) AS perc_yesterday_c2_dif,
    ROUND(perc_same_day_last_week_c2 - perc_same_day_last_week_c1, 2) AS perc_same_day_last_week_dif,
    ROUND(perc_avg_last_week_c2 - perc_avg_last_week_c1, 2) AS perc_avg_last_week_dif,
    ROUND(perc_avg_last_month_c2 - perc_avg_last_month_c1, 2) AS perc_avg_last_month_dif
FROM 
	concentration_checkout_all;


-- Today (c2) vs historical checkouts (as quantity of checkouts)
SELECT 
	time,
    today_c2,
	LEAST(
		yesterday_c2, 
		yesterday_c1, 
		same_day_last_week_c2, 
		same_day_last_week_c1,
		avg_last_week_c2,
		avg_last_week_c1,
		avg_last_month_c2,
		avg_last_month_c1
	) AS min_value,
	GREATEST(
		yesterday_c2, 
		yesterday_c1, 
		same_day_last_week_c2, 
		same_day_last_week_c1,
		avg_last_week_c2,
		avg_last_week_c1,
		avg_last_month_c2,
		avg_last_month_c1
	) AS max_value,
    ROUND(
		((yesterday_c2
		+ yesterday_c1 
		+ same_day_last_week_c2 
		+ same_day_last_week_c1
		+ avg_last_week_c2
		+ avg_last_week_c1
		+ avg_last_month_c2
		+ avg_last_month_c1) 
		/ 8), 2) AS average_value
FROM
	checkout_all;
    
    
-- Today (c2) vs historical checkouts (as hourly % of total checkouts in a day)
SELECT 
	time,
    perc_today_c2,
	LEAST(
		perc_yesterday_c2, 
		perc_yesterday_c1, 
		perc_same_day_last_week_c2, 
		perc_same_day_last_week_c1,
		perc_avg_last_week_c2,
		perc_avg_last_week_c1,
		perc_avg_last_month_c2,
		perc_avg_last_month_c1
	) AS perc_min_value,
	GREATEST(
		perc_yesterday_c2, 
		perc_yesterday_c1, 
		perc_same_day_last_week_c2, 
		perc_same_day_last_week_c1,
		perc_avg_last_week_c2,
		perc_avg_last_week_c1,
		perc_avg_last_month_c2,
		perc_avg_last_month_c1
	) AS perc_max_value,
    ROUND(
		((perc_yesterday_c2
		+ perc_yesterday_c1 
		+ perc_same_day_last_week_c2 
		+ perc_same_day_last_week_c1
		+ perc_avg_last_week_c2
		+ perc_avg_last_week_c1
		+ perc_avg_last_month_c2
		+ perc_avg_last_month_c1) 
		/ 8), 2) AS perc_average_value
FROM
	concentration_checkout_all;


-- Drop temporary tables
DROP TABLE concentration_checkout_all;
DROP TABLE checkout_all;