# AI Usage and Validation Log

Record actual use only. Do not include confidential data, credentials, or personal information in prompts. Save final prompts and the validated output or link to the relevant commit/query.

| Date / task | Tool | Input / prompt summary | Draft output | Human changes | Validation performed | Outcome / limitation |
|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Example constrained prompt

> Use only the schema and metric definitions below. First list missing fields or assumptions. Draft a query to calculate [supported KPI] by [dimension] at [declared grain]. Do not invent columns. Include a validation query that returns the underlying records for a sample of classifications. Explain how nulls, duplicates, and excluded records are handled.

## Validation checklist

- [ ] Confirmed the generated code uses real columns and correct join keys.
- [ ] Checked aggregation grain and prevented duplicate order-header values after joins.
- [ ] Checked KPI denominator, filters, nulls, dates, and currency handling.
- [ ] Compared results with an independent SQL/Python calculation or a hand-checked sample.
- [ ] Reviewed the generated narrative against validated queries and visuals.
- [ ] Recorded rejected or corrected AI suggestions and why.
