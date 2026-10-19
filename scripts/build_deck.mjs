import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {finalizePresentation,applyPresentationChartFont} from '/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs';
const root=process.env.ADMISSIONFLOW_ROOT || process.cwd();
const out=root+'/reports/session2'; const work=(process.env.ADMISSIONFLOW_BUILD_DIR || '/tmp/admissionflow-artifacts');
const d=JSON.parse(await fs.readFile(out+'/business_inputs.json','utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const font='Nimbus Sans';
function text(s,name,value,x,y,width,height,size=24,color='#182b49',bold=false){const sh=s.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width,height},fill:'none',line:{style:'solid',fill:'none',width:0}});sh.text=value;sh.text.style={typeface:font,fontSize:size,color,bold};return sh;}
function slide(title,source){const s=p.slides.add();s.background.fill='#f6f8fc';text(s,'headline',title,64,46,1152,115,40,'#182b49',true);text(s,'source',`Portfolio simulation · ${source}`,64,661,1152,35,15,'#56657a');return s;}
function narrative(s,lines){lines.forEach((line,i)=>text(s,'point-'+i,line,72,190+i*135,1110,110,28));}
function plot(s,cats,vals,title,unit='#,##0'){
 const ch=s.charts.add('bar',{position:{left:64,top:190,width:800,height:420},title,titleTextStyle:{typeface:font,fontSize:22},categories:cats,series:[{name:title,values:vals.map(v=>Number(v.toFixed(8))),fill:'#2563eb'}],hasLegend:false,barOptions:{direction:'bar'},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:unit,textStyle:{typeface:font,fontSize:17}},xAxis:{numberFormatCode:unit,textStyle:{typeface:font,fontSize:16}},yAxis:{textStyle:{typeface:font,fontSize:18},majorGridlines:{style:'solid',fill:'#dfe7f1',width:1}}});
 applyPresentationChartFont(ch,{fontFamily:font});return ch;
}
function note(s,value){text(s,'interpretation',value,905,210,310,390,25);}
let s=slide('AdmissionFlow Intelligence: decisions from acquisition to enrollment','CampusGrowth Analytics · Leadership review');
narrative(s,['Business challenge: connect institutional campaign spending to student progression and enrollment.','Management workflow: monitor campaign efficiency, prioritize follow-up and produce consistent client reports.','Decision standard: use transparent metrics and controlled testing; synthetic associations are not real business impact.']);
s=slide('A reproducible simulation with explicit analytical boundaries','data/manifest.json · docs/METHODOLOGY.md');
narrative(s,['50,000 leads · 24 fictional institutions · 120 campaign-months · 7 channels · 8 markets.','Five relational tables, 12 SQL analyses and a fixed seed. Single primary campaign per lead prevents duplicated attribution.','2025 acquisition; outcomes through 31 December. Recent cohorts are incomplete; planner uses mature campaign-months only.']);
s=slide('₹189.39 lakh spent; 5,627 confirmed enrollments observed','reports/kpis.json · all 2025 campaigns');
plot(s,['Leads','Completed applications','Enrollments'],[d.kpis.leads,d.kpis.application_completed,d.kpis.enrolled],'Observed student outcomes');
note(s,`11.25% lead-to-enrollment\n\n₹3,366 per enrollment\n\n89.4% budget utilization\n\nNo tuition revenue or ROI modeled.`);
s=slide('6,323 started applications remain incomplete at the snapshot','reports/03_unique_conversion.csv · all cohorts');
plot(s,['Qualified','Started','Completed','Offers','Enrolled'],['qualified','application_started','application_completed','offer','enrolled'].map(k=>d.kpis[k]),'Student progression');
note(s,'68.6% of application starts are completed.\n\nInvestigate form friction and follow-up.\n\nRecent students may still progress: this is not a final loss estimate.');
s=slide('Investigate C007 before committing additional budget','reports/recommendations.csv · mature campaigns, ≥100 leads');
narrative(s,['C007: 349 leads, 32 enrollments and ₹2.51 lakh spend. Historical cost per enrollment is ₹7,848.','Completed-application rate: 18.3%, compared with the mature pooled benchmark of 29.1%.','Audit targeting, landing-page qualification and follow-up. Randomize a revised message test before making causal claims.']);
s=slide('Institution reports connect client reviews to campaign evidence','reports/session2/institutions · all 2025 cohorts');
const inst=[...d.institutions].sort((a,b)=>b.enrolled-a.enrolled).slice(0,5);
plot(s,inst.map(x=>x.segment),inst.map(x=>x.enrolled),'Top five by observed enrollment volume');
note(s,'Volume reflects campaign allocation as well as conversion.\n\nCompare cost per application and enrollment alongside volume.\n\nExport institution HTML and CSV packs from the app.');
s=slide('Territory differences guide investigation, not market claims','reports/session2/geography.csv · all cohorts');
const geo=[...d.geography].sort((a,b)=>b.lead_to_enrollment-a.lead_to_enrollment);
plot(s,geo.map(x=>x.segment),geo.map(x=>100*x.lead_to_enrollment),'Observed lead-to-enrollment (%)','0.0');
note(s,'Fictional population and simulated outcomes.\n\nReview mix and maturity before comparing territories.\n\nGeographic cost efficiency is unavailable without delivery-level spend.');
s=slide('A ₹10 lakh planning budget supports explicit cost scenarios','src/budget.py · mature history · 5% floor / 25% cap');
plot(s,d.scenarios.map(x=>x.scenario),d.scenarios.map(x=>x.modeled_enrollments),'Modeled enrollment equivalents','0.0');
note(s,'Cost assumptions:\n+25% / unchanged / −15%.\n\nLower historical CPE gets priority within limits.\n\nConstant efficiency; no saturation or incremental lift modeled.');
s=slide('A practical operating cadence for campaign management','Metric-backed investigation rules · portfolio recommendations');
narrative(s,['Weekly: review mature campaign flags, qualify high-cost leads and assign ownership for incomplete applications.','Monthly: reconcile SQL, Python and Excel; share scoped institutional reports and distinguish recent cohorts.','Before reallocating: validate capacity and lead quality, then run a controlled channel or campaign test with a defined success metric.']);
s=slide('Use the platform as a tested case study, then validate in practice','Methodology and handoff documentation');
narrative(s,['Delivered: seven dashboard pages, scenario planner, institution exports, Excel reporting and a reproducible SQL/Python pipeline.','Limits: synthetic outcomes, primary-touch attribution, right censoring and constant-efficiency planning. No demonstrated financial return.','Next: connect a consented CRM extract, add delivery-grain costs and estimate response curves only after adequate experiments.']);
await fs.mkdir(work+'/deck-previews',{recursive:true});
await fs.mkdir(work+'/final',{recursive:true});
const candidate=work+'/candidate.pptx';await (await PresentationFile.exportPptx(p)).save(candidate);
const skill='/root/.codex/skills/builtins/presentations';
await finalizePresentation({workspaceDir:work,candidatePath:candidate,finalPath:work+'/final/AdmissionFlow_Leadership_v2.pptx',pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],explicitTotalSlideCount:10,requiredNativeChartOwnerSlides:[3,4,6,7,8],requiredNativeTableOwnerSlides:[],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:work+'/deck_validation_v2.json'});
await fs.copyFile(work+'/final/AdmissionFlow_Leadership_v2.pptx',out+'/AdmissionFlow_Leadership.pptx');
for(const [i,sl] of p.slides.items.entries()){const blob=await p.export({slide:sl,format:'png',scale:1});await fs.writeFile(work+`/deck-previews/slide-${i+1}.png`,new Uint8Array(await blob.arrayBuffer()));}
// PDF is generated from the validated PPTX using LibreOffice (see refresh guide).
await fs.copyFile(work+'/deck_validation_v2.json',out+'/deck_validation.json');
console.log('Presentation exported');
