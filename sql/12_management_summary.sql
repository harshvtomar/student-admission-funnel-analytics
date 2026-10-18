-- Entire simulation snapshot; NULL means undefined, never zero efficiency.
SELECT SUM(actual_spend) spend,SUM(budget) budget,SUM(impressions) impressions,SUM(clicks) clicks,SUM(leads) leads,SUM(application_completed) applications,SUM(enrolled) enrollments,SUM(actual_spend)/NULLIF(SUM(enrolled),0) cpe,1.0*SUM(enrolled)/NULLIF(SUM(leads),0) conversion FROM campaign_performance;
