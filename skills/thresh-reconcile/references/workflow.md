# Reconcile Workflow

## Quick Start
1. Ensure roadmap source is accessible (Drive doc, uploaded file, or Jira epics)
2. Run `/thresh-reconcile`
3. Claude parses roadmap, queries Jira backlog
4. Matches roadmap items to backlog coverage
5. Identifies gaps, orphans, duplicates
6. Forecasts capacity against commitments
7. Outputs to `product/reconciliation.json` + `.md`

## Common Chains
- `/thresh-synthesize` → `/thresh-reconcile` (customer evidence → backlog comparison)
- `/thresh-reconcile` → `/thresh-decompose` (fill gaps with new stories)
- `/thresh-reconcile` → `/thresh-publish` (label orphans in Jira)
- `/thresh-reconcile` → `/thresh-forecast` (capacity reality check)
