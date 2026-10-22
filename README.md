<div align="center">

# Supply Chain Analytics Portfolio

**Demand planning · Inventory optimization · Fulfillment analytics**

![Portfolio](https://img.shields.io/badge/portfolio-supply%20chain%20analytics-176B87)
![Current project](https://img.shields.io/badge/current%20project-in%20progress-orange)
![Focus](https://img.shields.io/badge/focus-analyst%20internships-5B7C99)

*Turning operational data into actionable supply-chain insights.*

</div>

---

## Hi, I’m Brinda

This portfolio showcases supply chain analytics projects using Python, SQL, Power BI, HTML, Plotly, and business-focused planning methods. My goal is to demonstrate how raw operational data can be transformed into useful insights for demand planning, inventory decisions, order fulfillment, and operations.

I’m currently building toward **Supply Chain Analyst internship opportunities**. Project results and implementation status are identified below; planned work is not presented as completed work.

## Featured Projects

### Project 1 · Demand Forecasting & Inventory Planning

This project uses historical store sales data to build a demand-driven inventory planning framework. It forecasts near-term demand, classifies inventory risk using ABC-XYZ logic, calculates safety stock and reorder points, and identifies high-priority replenishment items.

**Key outputs**

- Forecasted next 30-day demand by store-family.
- ABC-XYZ inventory classification.
- Safety stock and reorder-point calculations.
- Priority replenishment recommendation table.
- Power BI dashboard for executive review.

**Tools:** Python · Pandas · NumPy · Power BI · GitHub · VS Code
**Status:** Completed
**Project links:** Add the project repository and dashboard/PDF links here when available.

---

### Project 2 · Demand Planning & Forecast Accuracy Management

This project simulates a monthly demand-planning process for 100 high-volume SKUs. It compares six explainable forecast models through rolling backtesting, uses chronological holdout validation, measures forecast error and bias, and prioritizes high-risk SKUs for planner review.

**Key outputs**

- 52-week training window and 13-week forecast horizon.
- Six forecast models compared through rolling backtesting.
- Independent holdout validation designed to prevent future-data leakage.
- Champion-model selection by SKU.
- Forecast bias and Forecast Value Added (FVA) analysis.
- Planner exception queue based on demand volume, error, and bias.
- Interactive HTML and Plotly dashboard published with GitHub Pages.

**Holdout results:** 34.3% WAPE · 65.7% forecast accuracy · +3.1% bias · positive FVA for 75 of 100 SKUs.

**Tools:** Python · Pandas · NumPy · HTML/CSS/JavaScript · Plotly · Matplotlib · GitHub Pages
**Status:** Live
**Project links:** Add the live dashboard and project repository links here when available.

---

### Project 3 · AI-Assisted Order Fulfillment Performance Analysis

Based on a tutorial’s fictional retailer scenario, this project asks which markets, products, or customers show the clearest order-fulfillment risk and what an operations team should investigate first. The planned workflow takes source CSVs through data validation and n8n into PostgreSQL, then uses SQL analysis and a dashboard to communicate findings.

**Planned outputs**

- Data dictionary, source notes, and data-quality checks.
- Repeatable CSV intake with load logging and duplicate/error handling.
- PostgreSQL staging and clean analytical layer.
- SQL analysis for only those fulfillment metrics supported by the source fields.
- Dashboard, evidence-backed findings, and a documented AI validation process.

**Scope note:** This project begins as order-fulfillment analysis, not proven inventory optimization. OTIF requires appropriate promised-date, actual-delivery, and ordered/delivered-quantity fields. Stockout, safety-stock, and reorder-point analysis require inventory and replenishment data. Unsupported metrics will be marked unavailable rather than inferred.

**Planned tools:** n8n · PostgreSQL · SQL · Python for validation · one dashboard tool to be selected · AI assistant for drafting and review
**Status:** In progress — the tutorial files have not yet been profiled.

- [Open the step-by-step project manual](docs/step-by-step-project-instructions.md)
- [Read the project brief](docs/project-brief.md)
- [View metric definitions](docs/metric-definitions.md)
- [Browse the project files](.)

<!-- Add a real dashboard screenshot here after the dashboard has been built and validated. -->

---

## Portfolio Roadmap

| Project | Focus area | Tools | Status |
|---|---|---|---|
| 1. Demand Forecasting & Inventory Planning | Forecasting, ABC-XYZ, safety stock, reorder point | Python, Power BI | Completed |
| 2. Demand Planning & Forecast Accuracy Management | Rolling backtesting, WAPE, bias, FVA, planner exceptions | Python, HTML, Plotly | Live |
| 3. AI-Assisted Order Fulfillment Performance Analysis | Data quality, SQL, workflow automation, fulfillment KPIs | n8n, PostgreSQL, SQL, Python, dashboard TBD | In progress |
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
**Workflow and development:** n8n · PostgreSQL · GitHub · VS Code
**AI:** Used as an assistant for drafting and review; final metrics and claims are independently checked.

## Project Documentation

For the current fulfillment project:

- [Detailed step-by-step build instructions](docs/step-by-step-project-instructions.md)
- [Project build guide](docs/project-build-guide.md)
- [Project brief](docs/project-brief.md)
- [Data dictionary template](docs/data-dictionary.md)
- [Metric definitions and field requirements](docs/metric-definitions.md)
- [AI usage and validation log](docs/ai-usage-log.md)
- [Business analysis portfolio template](docs/reference/Supply_Chain_Optimization_BA_Portfolio_Template.docx)

## Contact

Open to **Supply Chain Analyst internship** opportunities. Contact details and project links will be added here when ready to publish.

---

*Tutorial inspiration for Project 3: [AI-assisted supply-chain analytics walkthrough](https://www.youtube.com/watch?v=PglKAYgRdJ4). Its fictional scenario and sample data are identified as such. Findings will be reported only after the source data is inspected and the calculations are validated.*
