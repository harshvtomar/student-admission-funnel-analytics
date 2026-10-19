import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.env.ADMISSIONFLOW_ROOT || process.cwd();
const out=root+'/reports/session2';
const d=JSON.parse(await fs.readFile(out+'/business_inputs.json','utf8'));
const w=Workbook.create();
const names=['Executive','Campaigns','Channels','Funnel','Institutions','Geography','Scenarios','Guide'];
const sheets=Object.fromEntries(names.map(n=>[n,w.worksheets.add(n)]));
const INR='"₹"#,##0.00;("₹"#,##0.00);"–"';
function put(s,cell,value){s.getRange(cell).values=[[value]];}
function formula(s,cell,value){s.getRange(cell).formulas=[[value]];}
function setup(name,title,last='J'){
 const s=sheets[name];s.showGridLines=false;
 s.getRange(`A1:${last}150`).format.font.name='Arial';
 s.getRange(`A1:${last}150`).format.font.size=11;
 s.getRange(`A1:${last}150`).format.columnWidth=18;
 s.getRange('A1:A150').format.columnWidth=36;
 s.getRange(`A1:${last}1`).merge();put(s,'A1',title);
 s.getRange(`A1:${last}1`).format={fill:'#182b49',font:{color:'#ffffff',bold:true,size:20},rowHeight:38};
 s.getRange(`A2:${last}2`).merge();put(s,'A2','PORTFOLIO SIMULATION · CampusGrowth Analytics · INR · Snapshot 31 Dec 2025');
 s.getRange(`A2:${last}2`).format={font:{color:'#56657a',size:10},rowHeight:25};
 s.freezePanes.freezeRows(4);return s;
}
function header(s,values,last){s.getRange(`A4:${last}4`).values=[values];s.getRange(`A4:${last}4`).format={fill:'#dce8fa',font:{bold:true,color:'#182b49'},rowHeight:34,wrapText:true};}
function chart(s,cat,val,title,anchor='J6',end='Q22'){
 const ch=s.charts.add('bar',[s.getRange(cat),s.getRange(val)]);ch.title=title;ch.setPosition(anchor,end);ch.hasLegend=false;ch.yAxis.numberFormatCode=title.includes('rate')?'0.0%':'#,##0';
}
let s=setup('Campaigns','Campaign scorecards','Q');
const keys=['campaign_id','institution_id','acquisition_channel','month','budget','actual_spend','leads','qualified','application_started','application_completed','offer','enrolled'];
header(s,['Campaign','Institution','Channel','Month','Budget INR','Spend INR','Leads','Qualified','Started','Completed','Offers','Enrolled','CPQL INR','CPA INR','CPE INR','Lead → enroll','Mature'], 'Q');
s.getRange('A5:L124').values=d.campaigns.map(r=>keys.map(k=>r[k]));
s.getRange('C5:C124').format.columnWidth=25;
for(let r=5;r<=124;r++){
 for(const [col,den] of [['M','H'],['N','J'],['O','L']])formula(s,`${col}${r}`,`=IF(${den}${r}=0,"n.a.",F${r}/${den}${r})`);
 formula(s,`P${r}`,`=IF(G${r}=0,"n.a.",L${r}/G${r})`);
 put(s,`Q${r}`,d.campaigns[r-5].month<='2025-09'?1:0);
}
s.getRange('E5:F124').setNumberFormat(INR);s.getRange('M5:O124').setNumberFormat(INR);s.getRange('P5:P124').setNumberFormat('0.0%');
s.tables.add('A4:Q124',true,'CampaignScorecards');
s.getRange('O5:O124').conditionalFormats.add('cellIs',{operator:'greaterThan',formula:5000,format:{fill:'#ffe2db',font:{color:'#a13118'}}});
function groupSheet(name,records,sourceColumn){
 const sh=setup(name,name==='Channels'?'Marketing channel performance':'Institution performance');
 header(sh,['Segment','Spend INR','Leads','Qualified','Completed','Enrolled','CPQL INR','CPA INR','CPE INR','Conversion'], 'J');
 records.forEach((item,i)=>{
  const r=i+5;put(sh,`A${r}`,item.segment);
  for(const [col,src] of [['B','F'],['C','G'],['D','H'],['E','J'],['F','L']])formula(sh,`${col}${r}`,`=SUMIF(Campaigns!$${sourceColumn}$5:$${sourceColumn}$124,A${r},Campaigns!$${src}$5:$${src}$124)`);
  for(const [col,den] of [['G','D'],['H','E'],['I','F']])formula(sh,`${col}${r}`,`=IF(${den}${r}=0,"n.a.",B${r}/${den}${r})`);
  formula(sh,`J${r}`,`=IF(C${r}=0,"n.a.",F${r}/C${r})`);
 });
 sh.getRange(`B5:B${records.length+4}`).setNumberFormat(INR);sh.getRange(`G5:I${records.length+4}`).setNumberFormat(INR);sh.getRange(`J5:J${records.length+4}`).setNumberFormat('0.0%');
 sh.tables.add(`A4:J${records.length+4}`,true,name+'Table');
 chart(sh,`A4:A${records.length+4}`,`F4:F${records.length+4}`,'Confirmed enrollments','L5','T24');
}
groupSheet('Channels',d.channels,'C');groupSheet('Institutions',d.institutions,'B');
s=setup('Geography','Geographic student conversion');header(s,['Market','Leads','Completed','Enrolled','Conversion'],'E');
d.geography.forEach((x,i)=>{let r=i+5;s.getRange(`A${r}:D${r}`).values=[[x.segment,x.leads,x.application_completed,x.enrolled]];formula(s,`E${r}`,`=IF(B${r}=0,"n.a.",D${r}/B${r})`);});
s.getRange('E5:E12').setNumberFormat('0.0%');s.tables.add('A4:E12',true,'Territories');chart(s,'A4:A12','E4:E12','Lead-to-enrollment rate','G5','O22');put(s,'A15','No geographic cost allocation: delivery-grain costs are unavailable.');
s=setup('Funnel','Student admission funnel');header(s,['Stage','Unique students','Previous-stage rate','Not progressed'],'D');
const stages=[['Leads','G'],['Qualified leads','H'],['Applications started','I'],['Applications completed','J'],['Admission offers','K'],['Enrollments','L']];
stages.forEach(([label,col],i)=>{let r=i+5;put(s,`A${r}`,label);formula(s,`B${r}`,`=SUM(Campaigns!${col}5:${col}124)`);if(i){formula(s,`C${r}`,`=IF(B${r-1}=0,"n.a.",B${r}/B${r-1})`);formula(s,`D${r}`,`=B${r-1}-B${r}`);}});
s.getRange('C6:C10').setNumberFormat('0.0%');chart(s,'A4:A10','B4:B10','Unique students','F5','N22');put(s,'A13','Recent cohorts remain incomplete; stage gaps are not all final losses.');
s=setup('Executive','AdmissionFlow | Executive dashboard');header(s,['Metric','Observed value','Python control','Difference'],'D');
const metric=[['Marketing spend','SUM(Campaigns!F5:F124)',d.kpis.actual_spend],['Unique leads','SUM(Campaigns!G5:G124)',d.kpis.leads],['Completed applications','SUM(Campaigns!J5:J124)',d.kpis.application_completed],['Confirmed enrollments','SUM(Campaigns!L5:L124)',d.kpis.enrolled],['Cost per enrollment','IF(B8=0,"n.a.",B5/B8)',d.kpis.cpe],['Lead-to-enrollment','IF(B6=0,"n.a.",B8/B6)',d.kpis.lead_to_enrollment],['Budget utilization','B5/SUM(Campaigns!E5:E124)',d.kpis.budget_utilization]];
metric.forEach(([label,f,v],i)=>{let r=i+5;put(s,`A${r}`,label);formula(s,`B${r}`,'='+f);put(s,`C${r}`,v);formula(s,`D${r}`,`=ROUND(B${r}-C${r},6)`);});
s.getRange('B5:C5').setNumberFormat(INR);s.getRange('B9:C9').setNumberFormat(INR);s.getRange('B10:C11').setNumberFormat('0.0%');s.getRange('D5:D11').setNumberFormat('0.00');
s.getRange('D5:D11').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#ffe2db'}});
put(s,'A14','Decision: investigate costly mature campaigns and application follow-up.');put(s,'A16','C007: 18.3% completed applications vs 29.1% mature pooled benchmark.');put(s,'A18','Do not infer real-world effectiveness or causal improvement from simulation.');
put(s,'A22','Month');put(s,'B22','Enrollments');
for(let i=0;i<12;i++){let r=23+i;put(s,`A${r}`,'2025-'+String(i+1).padStart(2,'0'));formula(s,`B${r}`,`=SUMIF(Campaigns!D$5:D$124,A${r},Campaigns!L$5:L$124)`);}
chart(s,'A22:A34','B22:B34','Enrollments by acquisition month','F4','N19');
// Single active scenario. Greedy allocations recalculate from editable total, floor and cap.
s=setup('Scenarios','Budget scenarios | Mature historical inputs','M');
const inputs=[['Budget INR',1000000],['Minimum share',.05],['Maximum share',.25],['Scenario','Base'],['Conservative multiplier',1.25],['Base multiplier',1],['Optimistic multiplier',.85]];
inputs.forEach(([label,value],i)=>{put(s,`A${i+4}`,label);put(s,`B${i+4}`,value)});
s.getRange('B4:B10').format.font.color='#135cc5';s.getRange('B5:B6').setNumberFormat('0%');s.getRange('B4').setNumberFormat(INR);
s.getRange('B7').dataValidation={rule:{type:'list',values:['Conservative','Base','Optimistic']}};
put(s,'A11','Active cost multiplier');formula(s,'B11','=IF(B7="Conservative",B8,IF(B7="Base",B9,B10))');
put(s,'A12','Constraint status');formula(s,'B12','=IF(AND(B4>=0.01,B5>=0,B6<=1,B5<=B6,7*ROUNDUP(ROUND(B4*100,0)*B5,0)<=ROUND(B4*100,0),7*ROUNDDOWN(ROUND(B4*100,0)*B6,0)>=ROUND(B4*100,0),B11>0),"OK","INVALID")');
const headers=['Channel (CPE rank)','Historical budget','Spend INR','Qualified','Completed','Enrolled','CPQL INR','CPA INR','CPE INR','Allocation INR','Modeled enrolled','Current share','New share'];
s.getRange('A15:M15').values=[headers];s.getRange('A15:M15').format={fill:'#dce8fa',font:{bold:true},wrapText:true,rowHeight:40};
d.allocation.forEach((item,i)=>{let r=i+16;put(s,`A${r}`,item.segment);
 for(const [col,src] of [['B','E'],['C','F'],['D','H'],['E','J'],['F','L']])formula(s,`${col}${r}`,`=SUMIFS(Campaigns!$${src}$5:$${src}$124,Campaigns!$C$5:$C$124,A${r},Campaigns!$Q$5:$Q$124,1)`);
 for(const [col,den] of [['G','D'],['H','E'],['I','F']])formula(s,`${col}${r}`,`=IF(${den}${r}=0,"n.a.",C${r}/${den}${r})`);
 const prior=i?`SUM(J$16:J${r-1})*100`:0;
 formula(s,`J${r}`,`=IF($B$12="OK",MIN(ROUNDDOWN(ROUND($B$4*100,0)*$B$6,0),ROUND($B$4*100,0)-${prior}-${6-i}*ROUNDUP(ROUND($B$4*100,0)*$B$5,0))/100,0)`);
 formula(s,`K${r}`,`=IF($B$12="OK",J${r}/(I${r}*$B$11),0)`);formula(s,`L${r}`,`=B${r}/SUM(B$16:B$22)`);formula(s,`M${r}`,`=IF($B$12="OK",J${r}/ROUND($B$4,2),0)`);
});
put(s,'A23','Total');for(const col of ['B','C','D','E','F','J','K','L','M'])formula(s,`${col}23`,`=SUM(${col}16:${col}22)`);
s.getRange('B16:C23').setNumberFormat(INR);s.getRange('G16:J23').setNumberFormat(INR);s.getRange('L16:M23').setNumberFormat('0.0%');s.getRange('K16:K23').setNumberFormat('0.0');
put(s,'A26','Rules: constant historical CPE; 100+ mature leads, positive spend and enrollment; all 7 channels eligible.');
put(s,'A28','Multiplier assumptions: conservative costs +25%; base unchanged; optimistic costs −15%. No causal lift.');
put(s,'A30','Ordering is a historical snapshot. Refresh through the generator if source data or eligibility changes.');
put(s,'A32','Invalid constraints suppress allocation. Modeled volumes are hypothetical, not a prediction.');
chart(s,'A15:A22','J15:J22','Recommended allocation (INR)','O5','W22');
s=setup('Guide','Reporting guide and provenance');
const guide=['Source: deterministic CampusGrowth simulation, seed 20261018; no real personal data.',
'Acquisition window: Jan–Dec 2025. Outcome snapshot: 31 December 2025.',
'Campaigns are the cost grain. Unique leads have one primary acquisition campaign.',
'Executive controls reconcile against reports/kpis.json and SQL management summaries.',
'Refresh: python -m src.pipeline; python -m src.export_business; then run scripts/build_workbook.mjs.',
'Builder requires the documented @oai/artifact-tool runtime. The Streamlit app does not.',
'Scenarios: edit blue inputs B4:B10. Recalculation is automatic in Excel.',
'Mature planner source: Jan–Sep complete campaign-months; 91-day campaign-end rule.',
'Workbook counts are observed-to-date; recent cohorts are not comparable to mature cohorts.',
'Filters on tables do not change executive SUM formulas. Use the dashboard for filtered analysis.',
'Geography has no cost allocation. No tuition revenue, ROI, causal effect or demand inference.',
'Institution ID-to-name mapping: reports/session2/business_inputs.json and dashboard client selector.',
'Source changes require a full refresh, including channel CPE rank and formula ranges.',
'Inspect docs/REPORT_REFRESH.md for exact commands and verification limitations.'];
guide.forEach((text,i)=>put(s,`A${i*2+4}`,text));
w.recalculate();
const checks=sheets.Executive.getRange('B5:B11').values.flat();
metric.forEach((m,i)=>{if(Math.abs(checks[i]-m[2])>1e-6)throw Error('Executive reconciliation '+m[0]);});
const base=sheets.Scenarios.getRange('K23').values[0][0];
if(Math.abs(base-d.scenarios[1].modeled_enrollments)>1e-7)throw Error('Scenario reconciliation');
put(sheets.Scenarios,'B7','Conservative');w.recalculate();
if(Math.abs(sheets.Scenarios.getRange('K23').values[0][0]-base/1.25)>1e-7)throw Error('Scenario sensitivity');
put(sheets.Scenarios,'B7','Base');put(sheets.Scenarios,'B6',.1);w.recalculate();
if(sheets.Scenarios.getRange('B12').values[0][0]!=='INVALID')throw Error('Constraint validation');
put(sheets.Scenarios,'B6',.25);w.recalculate();
await fs.mkdir((process.env.ADMISSIONFLOW_BUILD_DIR || '/tmp/admissionflow-artifacts')+'/workbook-previews',{recursive:true});
for(const name of names){const ranges={Scenarios:'A1:W32',Campaigns:'A1:Q14',Executive:'A1:N34',Channels:'A1:T24',Institutions:'A1:T29',Funnel:'A1:N24',Geography:'A1:O24',Guide:'A1:J32'};const blob=await w.render({sheetName:name,range:ranges[name],scale:1,format:'png'});await fs.writeFile((process.env.ADMISSIONFLOW_BUILD_DIR || '/tmp/admissionflow-artifacts')+'/workbook-previews/'+name+'.png',new Uint8Array(await blob.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(w)).save(out+'/AdmissionFlow_Business_Report.xlsx');
await fs.writeFile(out+'/workbook_validation.json',JSON.stringify({headline_controls:checks,base_modeled_enrollments:base,scenario_sensitivity:'passed',infeasible_constraints:'passed',sheets:names},null,2));
console.log('Workbook exported and controls passed');
