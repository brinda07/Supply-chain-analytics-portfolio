# Power BI Dashboard Artifacts

The project author has built the Power BI report with three pages:

1. **Fulfillment Overview**
2. **Diagnostic Segments**
3. **Data & Methodology**

The report file and screenshots are not currently stored in this repository. To make the implemented dashboard reviewable on GitHub, add one of these options:

## Preferred: share the Power BI file

Save a sanitized copy as:

```text
dashboard/supply-chain-fulfillment-analytics.pbix
```

Before committing, open the file once to confirm it is the intended final report. Remove or verify there are no private connection details, credentials, personal information, or unsanitized data. This project uses only the repository's synthetic data.

## Alternative: add page screenshots

Export or capture the three report pages and save them here:

```text
dashboard/screenshots/fulfillment-overview.png
dashboard/screenshots/diagnostic-segments.png
dashboard/screenshots/data-and-methodology.png
```

Keep the synthetic-data disclosure visible on the pages. Do not include database passwords, private server names, local user names, or other sensitive desktop details in screenshots.

## Findings and recommendations

The screenshots show the report, but they do not replace a written interpretation. Add a concise findings and recommendations section to the main README or a new case-study file after copying the actual report values, filters, periods, numerators, denominators, and segment volumes. Use [`docs/project-explainer.md`](../docs/project-explainer.md) as the project-specific guide. Do not invent values or frame synthetic differences as real operational performance.
