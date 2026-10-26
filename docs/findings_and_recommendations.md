# Findings and Recommendations

## 1. Executive Summary

This project analyzes a generated synthetic dataset of 1,440 fictional orders to demonstrate an end-to-end supply-chain analytics workflow using PostgreSQL, SQL, manual KPI validation, and Power BI.

In the embedded sample, 1,405 orders are marked delivered and 35 cancelled. Among delivered orders, the on-time rate is 87.3%, the in-full order rate is 73.8%, and the OTIF rate is 64.1%. The unit fill rate is 94.7% for delivered orders.

These values describe only the generated dataset; they are not real company results or evidence of actual supply-chain performance.

## 2. Findings

### 2.1. Order-Level OTIF Is Lower Than Either Individual Service Rate

Of the 1,405 delivered orders:

| Measure | Result | Denominator |
|---|---:|---|
| On-time orders | 1,227 (87.3%) | 1,405 delivered orders |
| In-full orders | 1,037 (73.8%) | 1,405 delivered orders |
| OTIF orders | 901 (64.1%) | 1,405 delivered orders |

OTIF requires an order to be both on time and in full, so it is lower than either individual rate. The counts indicate that 326 delivered orders were on time but not in full, while 136 were in full but late. A further 42 were neither on time nor in full. These categories account for the 504 delivered orders that did not meet OTIF.

### 2.2. Unit Fill and In-Full Order Rate Describe Different Aspects of Fulfillment

The unit fill rate is:

**12,883 delivered units ÷ 13,601 ordered units = 94.7%** for delivered orders.

The in-full order rate is 73.8%.

These results are not contradictory: unit fill measures the share of ordered units delivered across the eligible orders, whereas the in-full order rate requires every line on an order to be fulfilled. A relatively small unit shortfall can cause an entire order to fail the in-full test. In this sample, 1,037 delivered orders were in full, meaning 368 did not meet the order-level in-full definition.

### 2.3. Cancellations Are Included in the Submitted-Order Total but Excluded From Delivery-Service Rates

The sample contains 35 cancelled orders out of 1,440 submitted orders, a cancellation rate of 2.4%.

In line with the project’s KPI definitions, cancelled orders contribute to the cancellation rate and submitted-order count, but not to the on-time, in-full, OTIF, or delivered-order unit-fill calculations.

### 2.4. The KPI Logic Was Checked Against the Embedded Sample

The report’s reference results match the records embedded in the PBIX. The OTIF flag also matches the combined on-time-and-in-full condition for delivered orders.

These checks support the calculation logic for this sample; they do not establish that every Power BI measure has been reconciled against the corresponding SQL output.

### 2.5. Segment Results Should Be Interpreted as Demonstrations, Not Independent Discoveries

The project dataset is synthetic. Its generator intentionally varies late-delivery and partial-fulfillment probabilities by dimensions such as market, carrier, and product category.

Segment differences therefore demonstrate how the analysis can identify patterns in data; they are not independently discovered business trends, real benchmarks, or proof of root cause.

## 3. Recommendations

The recommendations below describe appropriate analytical next steps. Operational actions should be considered only if similar findings are confirmed using reliable real-world data.

| Priority | Recommendation | Why It Follows From This Analysis | What to Check Next |
|---:|---|---|---|
| 1 | **Investigate order-level completeness separately from unit fill.** | The unit fill rate is 94.7%, while only 73.8% of delivered orders are in full. Aggregate unit fill can conceal the number of orders affected by shortages. | Examine incomplete orders and their lines by SKU, category, customer segment, and market. Check the size and distribution of each order’s shortfall. |
| 2 | **Separate late-only, incomplete-only, and combined OTIF failures.** | The sample contains on-time but incomplete orders, in-full but late orders, and orders failing both conditions. These are different service outcomes and may require different investigations. | Compare the three failure groups by order month, market, carrier, and product. Include eligible order counts with every rate. |
| 3 | **Use segment comparisons to guide investigation, not to assert cause.** | The dashboard can reveal where sample rates differ, but the generated data does not establish why a difference occurred. | For a real dataset, verify definitions and coverage, check sample sizes and time periods, then investigate plausible operational explanations with supporting records. |
| 4 | **Show denominators alongside service percentages.** | A percentage based on a small number of eligible orders can be unstable and easy to overinterpret. | Keep delivered-order counts visible in carrier, customer-segment, and market/month comparisons, including tooltips or adjacent labels. |
| 5 | **Reconcile SQL and Power BI measures before claiming they agree.** | The project documentation notes that SQL-to-DAX reconciliation has not been established. Matching the report’s embedded sample totals does not replace a direct query-by-query reconciliation. | Apply the same filters and eligibility rules in SQL and Power BI; compare numerator, denominator, and final rate for each KPI. Record the results and any differences. |

## 4. Limitations

- The records and performance patterns are synthetic and fictional.
- The observed values should not be presented as a real company’s performance, industry benchmark, or expected operational outcome.
- Segment patterns in this dataset may reflect the generator’s programmed probabilities rather than naturally occurring supply-chain behavior.
- The dashboard’s headline values were checked against the embedded sample, but the SQL outputs and Power BI measures have not been fully reconciled under identical filters.
- This analysis identifies descriptive patterns. It does not establish causal explanations or quantify the business impact of a proposed intervention.

## 5. Conclusion

The project demonstrates how order-level and unit-level fulfillment measures can provide complementary views of service performance. In this synthetic sample, the difference between the unit fill rate and the in-full order rate illustrates why analysts should report both measures and clearly explain their grains and denominators.

The most useful next analytical step is to examine incomplete and late orders separately, include eligible-order counts in segment comparisons, and reconcile the dashboard measures with SQL before presenting the results as final.
