-- Campaign grain; may exceed 100% in the simulation.
SELECT campaign_id,budget,actual_spend,actual_spend/NULLIF(budget,0) utilization FROM campaigns;
