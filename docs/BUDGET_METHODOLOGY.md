# Budget planning methodology

The planner is a hypothetical resource-allocation exercise, not a forecast or an estimate of incremental returns. It uses selected complete campaign-months ending at least 91 days before 31 December 2025. All other sidebar filters remain in force.

Aggregate spend once per campaign. Calculate channel CPQL = spend / qualified leads, CPA = spend / completed applications and CPE = spend / confirmed enrollments. A channel is eligible only with at least 100 leads, positive spend and at least one enrollment. Excluded channels are shown in the historical-input table; their allocation is zero. Undefined unit costs are never treated as free acquisition.

The objective is to maximize the sum of allocated budget divided by historical channel CPE, subject to a fixed total and common minimum/maximum channel shares. The exact greedy solution starts with the minimum for every eligible channel and assigns the remainder in ascending CPE order, with alphabetical ties, until each cap binds. Calculations enforce integer paise and reject infeasible bounds. The default seven-channel example uses ₹1,000,000, a 5% floor and 25% cap. This is a linear, constant-efficiency assumption; the real business may have diminishing returns, limited inventory and cross-channel effects.

Conservative, base and optimistic use assumed unit-cost multipliers of 1.25, 1.00 and 0.85. Users may edit the active multiplier. Modeled outcome equivalents = allocated budget / (historical unit cost × multiplier). A common multiplier changes volumes but leaves ranking and allocation unchanged. Fractional volumes are calculation outputs, not promised enrollments. The default comparison table retains the three named standard assumptions; the active scenario table uses the user's edited assumption.

The Excel workbook implements the same rule for the exported seven-channel mature snapshot. Its CPE ordering and eligibility are fixed at refresh, so changing source rows requires regenerating the workbook. The app recomputes both dynamically. Workbook budget, share bounds and scenario assumptions are editable. Invalid constraints suppress allocation and show INVALID.

Before taking action, confirm lead quality, operational capacity, channel definitions and consented CRM records. Use randomized tests to estimate incremental changes. No tuition-based ROI, realized financial return or real Indian market demand is inferred.
