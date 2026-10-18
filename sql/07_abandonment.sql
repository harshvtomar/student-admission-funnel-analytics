-- Unfinished-to-date, not permanent dropout.
SELECT institution_id,SUM(application_started) started,SUM(application_started-application_completed) incomplete,1.0*SUM(application_started-application_completed)/NULLIF(SUM(application_started),0) incomplete_rate FROM lead_facts GROUP BY institution_id;
