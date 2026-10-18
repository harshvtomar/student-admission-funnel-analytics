-- Student geography only; no defensible geographic cost allocation.
SELECT geographic_market,COUNT(*) leads,SUM(enrolled) enrollments,1.0*SUM(enrolled)/NULLIF(COUNT(*),0) conversion FROM lead_facts GROUP BY geographic_market;
