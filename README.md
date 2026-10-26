<div align="center">

# Supply Chain Analytics Projects

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

### Project 3 · Order Fulfillment Analytics 

This project uses a deterministic, fully synthetic dataset generated in the repository. It demonstrates a complete analyst workflow from reproducible data generation through SQL-based KPI analysis and a Power BI dashboard. The business, customers, products, carriers, orders, prices, and delivery events are fictional.

**Implemented workflow**

`Synthetic data generation` → `Structural validation` → `PostgreSQL schema and CSV loading` → `SQL KPI and segment analysis` → `Manual KPI verification` → `Power BI dashboard` → `Project documentation`

**Completed implementation**

- Generated the five synthetic CSV tables and validated their schemas, keys, relationships, and business-rule constraints.
- Installed PostgreSQL, created `supply_chain_portfolio`, created the five analytical tables plus `load_audit`, and imported the five CSV files.
- Executed `01_create_tables.sql`, `02_quality_checks.sql`, `03_fulfillment_kpis.sql`, `04_segment_diagnostics.sql`, and `05_dashboard_views.sql`; created the one-row-per-order `order_service` view.
- Manually checked `ORD-000001` and `ORD-000036` for on-time, in-full, OTIF, and cancellation treatment.
- Connected Power BI to PostgreSQL, loaded `order_service`, `order_lines`, `customers`, `products`, and `carriers`, built the relationship model and seven named KPI measures, and created three report pages: **Fulfillment Overview**, **Diagnostic Segments**, and **Data & Methodology**.


**Data disclosure:** All records are fictional; delivery and partial-fulfillment variation is programmed by the generator. Dashboard results describe this synthetic sample only; they are not empirical findings, industry benchmarks, causal evidence, or real business performance. The dataset has no inventory-on-hand or replenishment history, so this is not inventory optimization.

**Tools:** Python · PostgreSQL 18 · SQL · Power BI · AI assistant. **Automation:** not implemented.
**Status:** Core data, database, SQL, manual-check, and Power BI implementation complete. Final findings/recommendations and dashboard files still need to be added to this repository.


## Portfolio Roadmap

| Project | Focus area | Tools | Status |
|---|---|---|---|
| 1. Demand Forecasting & Inventory Planning | Forecasting, ABC-XYZ, safety stock, reorder point | Python, Power BI | Completed |
| 2. Demand Planning & Forecast Accuracy Management | Rolling backtesting, WAPE, bias, FVA, planner exceptions | Python, HTML, Plotly | Live |
| 3. AI-Assisted Order Fulfillment Analytics on Synthetic Data | Synthetic data, data quality, PostgreSQL, SQL KPIs, manual verification, Power BI, AI-assisted development | Python, PostgreSQL 18, SQL, Power BI | Implementation complete; findings and repo artifacts pending |
| 4. Supplier Performance & Spend Analysis | Supplier scorecard, spend analysis, sourcing risk | Python, Power BI, SQL | Planned |
| 5. S&OP Scenario Planning Dashboard | Demand-supply gap, inventory coverage, revenue risk | Power BI, Python | Planned |


## Tools

**Analytics:** Python · SQL · Power BI
**Visualization:** Power BI 
**Workflow and development:** PostgreSQL · GitHub · VS Code 


## Contact

Open to **Supply Chain Analyst internship** opportunities. Contact details and project links will be added here when ready to publish.

---

*Workflow inspiration for Project 3: [AI-assisted supply-chain analytics walkthrough](https://www.youtube.com/watch?v=PglKAYgRdJ4). The tutorial’s restricted sample files are not included. The project’s separate generated dataset is synthetic and its patterns are not empirical findings.*
