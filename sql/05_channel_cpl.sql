-- Fully loaded simulated campaign spend includes organic and referral operating costs.
SELECT acquisition_channel,SUM(actual_spend) spend,SUM(leads) leads,SUM(actual_spend)/NULLIF(SUM(leads),0) cpl FROM campaign_performance GROUP BY acquisition_channel;
