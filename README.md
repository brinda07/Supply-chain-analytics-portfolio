Supply Chain Analytics Portfolio
Hi, Brinda. This portfolio showcases supply chain analytics projects using Python, SQL, Power BI, HTML, Plotly, and business-focused supply chain planning logic.

My goal is to demonstrate how raw operational data can be transformed into actionable supply chain insights, including demand forecasting, forecast accuracy management, inventory optimization, replenishment planning, supplier performance, and S&OP analysis.

Featured Projects
Project 1: Demand Forecasting & Inventory Planning
This project uses historical store sales data to build a demand-driven inventory planning framework. The analysis forecasts near-term demand, classifies inventory risk using ABC-XYZ logic, calculates safety stock and reorder points, and identifies high-priority replenishment items.

Inventory Planning Dashboard

Key outputs:

Forecasted next 30-day demand by store-family
ABC-XYZ inventory classification
Safety stock and reorder point calculation
Priority replenishment recommendation table
Power BI dashboard for executive review
Tools used: Python, Pandas, NumPy, Power BI, GitHub, VS Code

View Project Folder
Download Dashboard PDF

Project 2: Demand Planning & Forecast Accuracy Management
This project simulates a realistic monthly demand-planning process for 100 high-volume SKUs. It compares six explainable forecast models through rolling backtesting, uses chronological holdout validation, measures WAPE, MAPE, bias, MAE, and Forecast Value Added, and prioritizes high-risk SKUs for planner review.

Forecast Model Comparison

Key outputs:

52-week training window and 13-week forecast horizon
Six forecast models compared through rolling backtesting
Independent holdout validation with no future-data leakage
Champion-model selection by SKU
Forecast bias and FVA analysis
Planner exception queue based on demand volume, error, and bias
Interactive HTML and Plotly dashboard published with GitHub Pages
Holdout results: 34.3% WAPE, 65.7% forecast accuracy, +3.1% bias, and positive FVA for 75 of 100 SKUs.

Tools used: Python, Pandas, NumPy, HTML/CSS/JavaScript, Plotly, Matplotlib, GitHub Pages

Open Live Dashboard
View Project Folder

Portfolio Projects
Project	Focus Area	Tools	Status
Project 1: Demand Forecasting & Inventory Planning	Forecasting, inventory optimization, safety stock, reorder point	Python, Power BI	Completed
Project 2: Demand Planning & Forecast Accuracy Management	Rolling backtesting, WAPE, bias, FVA, planner exceptions	Python, HTML, Plotly	Live
Project 3: Supplier Performance & Spend Analysis	Supplier scorecard, spend analysis, sourcing risk	Python, Power BI, SQL	Planned
Project 4: S&OP Scenario Planning Dashboard	Demand-supply gap, inventory coverage, revenue risk	Power BI, Python	Planned
Skills Demonstrated
Demand forecasting and forecast accuracy management
Rolling backtesting and chronological model validation
WAPE, MAPE, bias, MAE, and Forecast Value Added
Exception-based demand planning
Inventory planning and ABC-XYZ classification
Safety stock and reorder point modeling
Data cleaning and transformation
Power BI, HTML, and Plotly dashboard design
Business recommendation writing
GitHub project documentation
Tools
Python
Pandas
NumPy
HTML / CSS / JavaScript
Plotly
Power BI
SQL
Excel
GitHub
VS Code
Contact
Open to Senior Supply Chain Analyst, Demand Planning Analyst, and Supply Chain Analytics roles.

## Repository map

- `docs/project-build-guide.md` — detailed build sequence and portfolio advice.
- `docs/step-by-step-project-instructions.md` — full follow-along manual from data acquisition to publishing.
- `docs/project-brief.md` — project purpose, scope, assumptions, and open questions.
- `docs/metric-definitions.md` — KPI definitions and field requirements.
- `docs/data-dictionary.md` — mapping template to complete after inspecting source files.
- `docs/ai-usage-log.md` — template for recording AI assistance and validation.
- `docs/reference/` — the attached general business-analysis template for reference.
- `data/raw/` — intentionally empty; raw tutorial data is excluded by default.
- `n8n/` — workflow plan; add an exported, credential-redacted workflow after building it.
- `sql/`, `src/`, `tests/` — planned analysis and validation code.
- `dashboard/` — planned dashboard screenshots or permitted sharing instructions.

## Build status

1. [x] Create project documentation scaffold.
2. [ ] Obtain and inspect the tutorial files; document provenance and reuse terms.
3. [ ] Map actual fields, row grain, keys, and data-quality issues.
4. [ ] Implement and test ingestion and clean SQL views.
5. [ ] Calculate only supported KPIs; independently validate results.
6. [ ] Build the dashboard, summarize findings, and record AI validation.
7. [ ] Publish a short case study and reproducible setup instructions.

## Before publishing

Replace placeholders with verified details. Do not commit credentials, private email data, or tutorial files unless redistribution is permitted. Keep real findings, estimates, assumptions, and simulated scenario details clearly distinguished. Follow `docs/step-by-step-project-instructions.md` for the detailed build, and use `docs/project-build-guide.md` as the concise project plan.
