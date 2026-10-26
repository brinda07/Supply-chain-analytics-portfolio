<div align="center">

# Supply Chain Analytics Portfolio

**Demand planning · Inventory optimization · Fulfillment analytics**

![Portfolio](https://img.shields.io/badge/portfolio-supply%20chain%20analytics-176B87)
![Project 3 implementation](https://img.shields.io/badge/project%203-implementation%20complete-238636)
![Focus](https://img.shields.io/badge/focus-analyst%20internships-5B7C99)

*Turning operational data into actionable supply-chain insights.*

</div>

---

## Hi, I’m Brinda

This portfolio showcases supply chain analytics projects using Python, PostgreSQL, Power BI and business-focused planning methods. My goal is to demonstrate how raw operational data can be transformed into useful insights for demand planning, inventory decisions, order fulfillment, and operations.

I’m currently building toward **Supply Chain Analyst internship opportunities**. Project results and implementation status are identified below; planned work is not presented as completed work.

## Featured Projects

### Project 3 · AI-Assisted Order Fulfillment Analytics on Synthetic Data

This project uses a deterministic, fully synthetic dataset generated in the repository. It demonstrates a complete analyst workflow from reproducible data generation through SQL-based KPI analysis and a Power BI dashboard. The business, customers, products, carriers, orders, prices, and delivery events are fictional.

**Implemented workflow**

`Synthetic data generation` → `Structural validation` → `PostgreSQL schema and CSV loading` → `SQL KPI and segment analysis` → `Manual KPI verification` → `Power BI dashboard` → `Project documentation`

**Completed implementation**

- Generated the five synthetic CSV tables and validated their schemas, keys, relationships, and business-rule constraints.
- Installed PostgreSQL, created `supply_chain_portfolio`, created the five analytical tables plus `load_audit`, and imported the five CSV files.
- Executed `01_create_tables.sql`, `02_quality_checks.sql`, `03_fulfillment_kpis.sql`, `04_segment_diagnostics.sql`, and `05_dashboard_views.sql`; created the one-row-per-order `order_service` view.
- Manually checked `ORD-000001` and `ORD-000036` for on-time, in-full, OTIF, and cancellation treatment.
- Connected Power BI to PostgreSQL, loaded `order_service`, `order_lines`, `customers`, `products`, and `carriers`, built the relationship model and seven named KPI measures, and created three report pages: **Fulfillment Overview**, **Diagnostic Segments**, and **Data & Methodology**.
- Used AI assistance for schema understanding, SQL review, KPI validation, PostgreSQL troubleshooting, dashboard design review, and documentation support; analytical claims remain subject to human verification.

**Not implemented:** n8n or other workflow automation. The CSV import and SQL workflow described here is the actual project process; an older n8n draft in the repository was not used.

**What still needs your input for a reviewer-ready repo:** add the actual Power BI `.pbix` file or sanitized screenshots of its three pages, then write your findings and recommendations using the values and denominators in your dashboard. Those visual artifacts and result-specific conclusions are not currently stored in this repository.

**Data disclosure:** All records are fictional; delivery and partial-fulfillment variation is programmed by the generator. Dashboard results describe this synthetic sample only; they are not empirical findings, industry benchmarks, causal evidence, or real business performance. The dataset has no inventory-on-hand or replenishment history, so this is not inventory optimization.

**Tools:** Python · PostgreSQL 18 · SQL · Power BI · AI assistant. **Automation:** not implemented.
**Status:** Core data, database, SQL, manual-check, and Power BI implementation complete. Final findings/recommendations and dashboard files still need to be added to this repository.

- [Understand the project and write findings](docs/project-explainer.md)
- [Read the project brief](docs/project-brief.md)
- [Review KPI definitions](docs/metric-definitions.md)
- [Review manual KPI validation examples](tests/manual-kpi-validation.md)
- [Database setup and executed SQL steps](docs/database_setup.md)
- [Power BI files and publication checklist](dashboard/README.md)
- [Step-by-step reproducibility guide](docs/step-by-step-project-instructions.md)
- [Synthetic-data card](docs/synthetic-data-card.md)
- [Deterministic data generator](src/generate_synthetic_dataset.py)

An older, unexecuted n8n workflow draft remains under `n8n/` for reference only; it is not part of this implementation.

---

## Portfolio Roadmap

| Project | Focus area | Tools | Status |
|---|---|---|---|
| 1. Demand Forecasting & Inventory Planning | Forecasting, ABC-XYZ, safety stock, reorder point | Python, Power BI | Completed |
| 2. Demand Planning & Forecast Accuracy Management | Rolling backtesting, WAPE, bias, FVA, planner exceptions | Python, HTML, Plotly | Live |
| 3. AI-Assisted Order Fulfillment Analytics on Synthetic Data | Synthetic data, data quality, PostgreSQL, SQL KPIs, manual verification, Power BI, AI-assisted development | Python, PostgreSQL 18, SQL, Power BI | Implementation complete; findings and repo artifacts pending |
| 4. Supplier Performance & Spend Analysis | Supplier scorecard, spend analysis, sourcing risk | Python, Power BI, SQL | Planned |
| 5. S&OP Scenario Planning Dashboard | Demand-supply gap, inventory coverage, revenue risk | Power BI, Python | Planned |

## Skills Demonstrated

- Demand forecasting and forecast-accuracy measurement.
- Rolling backtesting and chronological model validation.
- WAPE, MAPE, bias, MAE, and Forecast Value Added.
- Exception-based demand planning.
- Inventory planning, ABC-XYZ classification, safety stock, and reorder points.
- Data cleaning, transformation, SQL, and relational modeling.
- Power BI, HTML, and Plotly dashboard design.
- Business recommendation writing and project documentation.
- Responsible AI-assisted analysis, including review and independent validation.

## Tools

**Analytics:** Python · Pandas · NumPy · SQL · Excel
**Visualization:** Power BI · Plotly · Matplotlib · HTML/CSS/JavaScript
**Workflow and development:** PostgreSQL · GitHub · VS Code · manual CSV loading for Project 3; no n8n automation
**AI:** Used as an assistant for drafting and review; final metrics and claims are independently checked.

## Project Documentation

For the current fulfillment project:

- [Detailed step-by-step build instructions](docs/step-by-step-project-instructions.md)
- [Project build guide](docs/project-build-guide.md)
- [Project brief](docs/project-brief.md)
- [Project explainer and findings guide](docs/project-explainer.md)
- [Data dictionary and table grains](docs/data-dictionary.md)
- [Metric definitions and field requirements](docs/metric-definitions.md)
- [Manual KPI validation evidence](tests/manual-kpi-validation.md)
- [Synthetic-data card](docs/synthetic-data-card.md)
- [Power BI artifact checklist](dashboard/README.md)
- [AI usage and validation log](docs/ai-usage-log.md)
- [Business analysis portfolio template](docs/reference/Supply_Chain_Optimization_BA_Portfolio_Template.docx)

## Contact

Open to **Supply Chain Analyst internship** opportunities. Contact details and project links will be added here when ready to publish.

---

*Workflow inspiration for Project 3: [AI-assisted supply-chain analytics walkthrough](https://www.youtube.com/watch?v=PglKAYgRdJ4). The tutorial’s restricted sample files are not included. The project’s separate generated dataset is synthetic and its patterns are not empirical findings.*
