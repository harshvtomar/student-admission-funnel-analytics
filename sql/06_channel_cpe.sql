-- Observed-to-date CPE, including immature cohorts; do not use to rank recent campaigns fairly.
SELECT acquisition_channel,SUM(actual_spend) spend,SUM(enrolled) enrollments,SUM(actual_spend)/NULLIF(SUM(enrolled),0) cpe FROM campaign_performance GROUP BY acquisition_channel;
