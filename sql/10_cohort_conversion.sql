-- Acquisition cohort split by individual 90-day maturity as of 2025-12-31.
SELECT month,mature,COUNT(*) leads,SUM(enrolled) enrollments,1.0*SUM(enrolled)/NULLIF(COUNT(*),0) conversion FROM lead_facts GROUP BY month,mature;
