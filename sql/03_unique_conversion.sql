-- One row per unique lead; zero denominator returns NULL.
SELECT COUNT(*) leads,SUM(application_completed) applications,SUM(enrolled) enrollments,1.0*SUM(enrolled)/NULLIF(COUNT(*),0) conversion FROM lead_facts;
