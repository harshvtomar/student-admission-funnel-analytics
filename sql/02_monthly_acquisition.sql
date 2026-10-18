-- Acquisition month, not outcome calendar month.
SELECT substr(start_date,1,7) month,SUM(actual_spend) spend,SUM(leads) leads,SUM(application_completed) applications,SUM(enrolled) enrollments FROM campaign_performance GROUP BY month;
