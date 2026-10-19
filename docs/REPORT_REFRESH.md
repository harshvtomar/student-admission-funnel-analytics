# Reporting refresh

The Streamlit application and CSV/client-report pipeline need only Python 3.12 and requirements.txt. No credentials are required.

```bash
python -m pip install -r requirements.txt
python -m src.pipeline
python -m src.export_business
python -m pytest -q
streamlit run app.py
```

Institution selection and exports are on University Client Performance. Sidebar filters define the report scope. Download HTML for a readable report, or ZIP for the HTML plus campaign CSV. Open HTML in a browser and use Print → Save as PDF if needed. `src.export_business` creates all 24 unfiltered packs under `reports/session2/institutions/`.

## Excel and slide regeneration

`scripts/build_workbook.mjs` and `scripts/build_deck.mjs` use the @oai/artifact-tool runtime supplied by ChatGPT Work. This optional authoring dependency is not distributed in requirements.txt and is not guaranteed to be available in a generic Node installation. The delivered XLSX/PPTX/PDF can be opened without that runtime.

In a Work session with the authoring runtime, read the spreadsheet and presentation skills, copy each builder to a fresh scratch build directory, link its node_modules to `$CODEX_PRIMARY_RUNTIME_NODE_MODULES`, and run it with `$CODEX_PRIMARY_RUNTIME_NODE`. Set `ADMISSIONFLOW_ROOT` to the absolute repository checkout and `ADMISSIONFLOW_BUILD_DIR` to the fresh build directory. The deck additionally uses the presentation skill's validation helpers. Follow the skill's operation marker requirements. The deck finalizer intentionally refuses to overwrite an existing final candidate; use a fresh build directory for each refresh.

```bash
ADMISSIONFLOW_ROOT=/absolute/path/student-admission-funnel-analytics \
ADMISSIONFLOW_BUILD_DIR=/absolute/path/fresh-build \
"$CODEX_PRIMARY_RUNTIME_NODE" /absolute/path/fresh-build/build_workbook.mjs
# Run build_deck.mjs in the same environment after reading its skill requirements.
"$CODEX_PRIMARY_RUNTIME/dependencies/bin/override/soffice" --headless \
  --convert-to pdf --outdir reports/session2 reports/session2/AdmissionFlow_Leadership.pptx
```

Workbook controls compare the seven headline values against generated Python outputs. Scenario checks validate the base case, conservative cost sensitivity and infeasible caps. Exported XML was also scanned for formula-error caches. Source campaigns, geography and names are in `business_inputs.json`. The workbook has fixed ranges for this 120-campaign, seven-channel snapshot. For changed scope, update ranges and rebuild rather than pasting additional rows beyond them. CPE ordering and channel eligibility must be regenerated whenever historical source data changes.

Table filters do not change executive SUM formulas. Use Streamlit to analyze a filtered view. Scenario inputs are blue; rates are fractions and costs are INR. Undefined ratios show n.a. Native Excel/PowerPoint editing has not been tested; artifact previews and package checks do not certify every office suite's rendering.
