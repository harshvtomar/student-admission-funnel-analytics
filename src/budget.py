"""Bounded, rules-based planning. Outputs are hypothetical capacity, not forecasts."""
import math
import pandas as pd
from .generate import AS_OF
from .metrics import segment_performance

SCENARIOS = {'Conservative': 1.25, 'Base': 1.0, 'Optimistic': 0.85}

def historical_inputs(c, l):
    """Complete mature campaign-months only, retaining the caller's other filters."""
    c = c[pd.to_datetime(c.end_date) + pd.Timedelta(days=91) <= AS_OF]
    l = l[l.campaign_id.isin(c.campaign_id)]
    if c.empty:
        return pd.DataFrame()
    p = segment_performance(c, l, 'acquisition_channel')
    p['cost_per_qualified_lead'] = p.actual_spend / p.qualified.replace(0, float('nan'))
    p['current_budget_share'] = p.budget / p.budget.sum()
    p['eligible'] = (p.leads >= 100) & (p.enrolled > 0) & (p.actual_spend > 0)
    return p

def allocate(history, total_budget=1000000.0, minimum_share=0.05, maximum_share=0.25):
    """Maximize sum(allocation / historical CPE), with identical share bounds.

    Greedy allocation is exact for this continuous linear objective. Integer paise
    enforce the fixed budget. No marginal response, saturation or causal lift is modeled.
    """
    if not all(math.isfinite(x) for x in [total_budget, minimum_share, maximum_share]):
        raise ValueError('Inputs must be finite.')
    if total_budget <= 0 or not 0 <= minimum_share <= maximum_share <= 1:
        raise ValueError('Budget must be positive and 0 ≤ minimum ≤ maximum ≤ 100%.')
    if history.empty or 'eligible' not in history:
        raise ValueError('No mature history is available for planning.')
    p = history.loc[history.eligible].copy()
    if p.empty:
        raise ValueError('No channels meet the 100-lead, positive-spend and enrollment requirements.')
    if p.cpe.isna().any() or (p.cpe <= 0).any():
        raise ValueError('Eligible channels require positive historical CPE.')
    cents = round(total_budget * 100)
    if cents < 1:
        raise ValueError('Budget must be at least one paisa.')
    lo, hi = math.ceil(cents * minimum_share), math.floor(cents * maximum_share)
    if len(p) * lo > cents or len(p) * hi < cents:
        raise ValueError(f'Infeasible constraints for {len(p)} eligible channels. Lower the minimum or raise the maximum.')
    p = p.sort_values(['cpe', 'segment']).reset_index(drop=True)
    remaining = cents - len(p) * lo
    amounts = []
    for _ in range(len(p)):
        extra = min(hi - lo, remaining)
        amounts.append((lo + extra) / 100)
        remaining -= extra
    p['recommended_budget'] = amounts
    p['recommended_share'] = p.recommended_budget / (cents / 100)
    return p

def scenario_outputs(allocation, cost_multiplier=1.0):
    if not math.isfinite(cost_multiplier) or cost_multiplier <= 0:
        raise ValueError('Cost multiplier must be positive and finite.')
    p = allocation.copy()
    p['assumed_cost_multiplier'] = cost_multiplier
    for outcome, cost in [('qualified_leads', 'cost_per_qualified_lead'), ('completed_applications', 'cost_per_application'), ('enrollments', 'cpe')]:
        p['modeled_' + outcome] = p.recommended_budget / (p[cost] * cost_multiplier)
    return p
