-- Institution acquisition attribution.
SELECT institution_id,SUM(leads) leads,SUM(qualified) qualified,SUM(application_started) started,SUM(application_completed) completed,SUM(offer) offers,SUM(enrolled) enrollments FROM campaign_performance GROUP BY institution_id;
