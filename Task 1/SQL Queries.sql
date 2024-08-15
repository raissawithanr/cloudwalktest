-- Understanding concentration of transactions by hour disregading day

SELECT 
    c1.time,
    ROUND(SUM(c1.today) * 100.0 / (SELECT SUM(today) FROM checkout_1), 2) AS today_c1,
    ROUND(SUM(c2.today) * 100.0 / (SELECT SUM(today) FROM checkout_2), 2) AS today_c2,
    ROUND(SUM(c1.yesterday) * 100.0 / (SELECT SUM(yesterday) FROM checkout_1), 2) AS yesterday_c1,
    ROUND(SUM(c2.yesterday) * 100.0 / (SELECT SUM(yesterday) FROM checkout_2), 2) AS yesterday_c2,
    ROUND(SUM(c1.same_day_last_week) * 100.0 / (SELECT SUM(same_day_last_week) FROM checkout_1), 2) AS same_day_last_week_c1,
    ROUND(SUM(c2.same_day_last_week) * 100.0 / (SELECT SUM(same_day_last_week) FROM checkout_2), 2) AS same_day_last_week_c2,
    ROUND(SUM(c1.avg_last_week) * 100.0 / (SELECT SUM(avg_last_week) FROM checkout_1), 2) AS avg_last_week_c1,
    ROUND(SUM(c2.avg_last_week) * 100.0 / (SELECT SUM(avg_last_week) FROM checkout_2), 2) AS avg_last_week_c2,
    ROUND(SUM(c1.avg_last_month) * 100.0 / (SELECT SUM(avg_last_month) FROM checkout_1), 2) AS avg_last_month_c1,
    ROUND(SUM(c2.avg_last_month) * 100.0 / (SELECT SUM(avg_last_month) FROM checkout_2), 2) AS avg_last_month_c2
FROM 
    checkout_1 c1
LEFT JOIN 
    checkout_2 c2 ON c1.time = c2.time
GROUP BY 
    c1.time;