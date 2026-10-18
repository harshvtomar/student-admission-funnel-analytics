PRAGMA foreign_keys=ON;
CREATE TABLE institutions(institution_id TEXT PRIMARY KEY,institution_name TEXT NOT NULL,state TEXT NOT NULL,city TEXT NOT NULL,institution_category TEXT NOT NULL,course_segment TEXT NOT NULL,campaign_budget_allocation REAL NOT NULL CHECK(campaign_budget_allocation>=0));
CREATE TABLE campaigns(campaign_id TEXT PRIMARY KEY,institution_id TEXT NOT NULL REFERENCES institutions,acquisition_channel TEXT NOT NULL,campaign_objective TEXT NOT NULL,start_date TEXT NOT NULL,end_date TEXT NOT NULL,budget REAL NOT NULL CHECK(budget>=0),actual_spend REAL NOT NULL CHECK(actual_spend>=0),clicks INTEGER NOT NULL CHECK(clicks>=0),impressions INTEGER NOT NULL CHECK(impressions>=clicks));
CREATE TABLE leads(lead_id TEXT PRIMARY KEY,created_at TEXT NOT NULL,acquisition_source TEXT NOT NULL,campaign_id TEXT NOT NULL REFERENCES campaigns,institution_id TEXT NOT NULL REFERENCES institutions,geographic_market TEXT NOT NULL,course_preference TEXT NOT NULL,qualification_status TEXT NOT NULL CHECK(qualification_status IN ('qualified','not_qualified')));
CREATE TABLE events(event_id TEXT PRIMARY KEY,lead_id TEXT NOT NULL REFERENCES leads,event_type TEXT NOT NULL CHECK(event_type IN ('qualified','application_started','application_completed','offer','enrolled')),event_timestamp TEXT NOT NULL,event_status TEXT NOT NULL CHECK(event_status='achieved'),UNIQUE(lead_id,event_type));
CREATE TABLE enrollments(enrollment_id TEXT PRIMARY KEY,lead_id TEXT UNIQUE NOT NULL REFERENCES leads,institution_id TEXT NOT NULL REFERENCES institutions,admission_decision_date TEXT NOT NULL,confirmation_date TEXT NOT NULL,enrollment_outcome TEXT NOT NULL CHECK(enrollment_outcome='confirmed'));
CREATE INDEX idx_leads_campaign ON leads(campaign_id);
CREATE INDEX idx_events_lead ON events(lead_id);
CREATE VIEW lead_facts AS
SELECT l.*,substr(created_at,1,7) AS month,
CASE WHEN julianday('2025-12-31 23:59:59')-julianday(created_at)>=90 THEN 1 ELSE 0 END AS mature,
MAX(CASE WHEN event_type='qualified' THEN 1 ELSE 0 END) AS qualified,
MAX(CASE WHEN event_type='application_started' THEN 1 ELSE 0 END) AS application_started,
MAX(CASE WHEN event_type='application_completed' THEN 1 ELSE 0 END) AS application_completed,
MAX(CASE WHEN event_type='offer' THEN 1 ELSE 0 END) AS offer,
MAX(CASE WHEN event_type='enrolled' THEN 1 ELSE 0 END) AS enrolled
FROM leads l LEFT JOIN events e ON l.lead_id=e.lead_id AND e.event_status='achieved' GROUP BY l.lead_id;
-- Aggregate student facts BEFORE joining campaign costs to avoid spend multiplication.
CREATE VIEW campaign_performance AS
WITH f AS (SELECT campaign_id,COUNT(*) leads,SUM(qualified) qualified,SUM(application_started) application_started,SUM(application_completed) application_completed,SUM(offer) offer,SUM(enrolled) enrolled FROM lead_facts GROUP BY campaign_id)
SELECT c.*,COALESCE(f.leads,0) leads,COALESCE(f.qualified,0) qualified,COALESCE(f.application_started,0) application_started,COALESCE(f.application_completed,0) application_completed,COALESCE(f.offer,0) offer,COALESCE(f.enrolled,0) enrolled,
1.0*c.actual_spend/NULLIF(f.leads,0) cpl,1.0*c.actual_spend/NULLIF(f.enrolled,0) cpe,
1.0*f.enrolled/NULLIF(f.leads,0) lead_to_enrollment
FROM campaigns c LEFT JOIN f ON c.campaign_id=f.campaign_id;
