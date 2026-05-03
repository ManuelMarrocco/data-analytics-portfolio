# OLIST Delivery Performance Analysis

## Project Objective

The objective of this project was to investigate whether delivery delays were associated with customer dissatisfaction in the OLIST e-commerce dataset.

The simulated stakeholder had a vague business concern: negative reviews seemed to be connected to late orders, but no structured KPIs or clear operational evidence were available.

For this reason, the project started with a light data quality and data readiness check before defining the final scope of work.

---

## Business Context

The initial stakeholder request was not fully defined.  
Instead of moving directly into analysis, the first step was to understand whether the available data could support the business question.

The analysis focused on:

- Delivery performance
- Estimated vs actual delivery dates
- Customer review scores
- Negative review rate
- Seller-origin patterns
- Operational timing between order approval and carrier handoff

---

## Project Files

Main files included in this project:

- `olist_delivery_performance_final_presentation_20260430_v01.pdf` — final project presentation
- `olist_delivery_performance_stakeholder_update_20260428_v01.pdf` — interim stakeholder update
- `olist_sp_diagnostic_dashboard_followup_20260502_v01.pbix` — final Power BI dashboard extension
- `sp_city_diagnostic_dashboard_v01.csv.csv` — dataset used for the São Paulo diagnostic dashboard
- `pbi_01_delivery_status_review.csv` — delivery status and review analysis output
- `pbi_02_delay_bucket_review.csv` — delay bucket analysis output
- `pbi_03_critical_seller_zip_review.csv` — seller-origin follow-up output
- `pbi_04_approval_carrier_timing.csv` — approval-to-carrier timing output
- `olist_analysis_23042026.txt` — analysis notes and SQL workflow documentation
- `olist_data_quality_23042026.txt` — data quality documentation

---

## Dataset

The dataset includes OLIST marketplace data related to:

- Orders
- Customers
- Sellers
- Order items
- Products
- Payments
- Reviews
- Geolocation

The analysis used relational tables connected through fields such as order_id, customer_id, seller_id, product_id, and ZIP code prefixes.

---

## Analysis Approach

The project followed a structured workflow:

- Data intake and light data quality validation
- Scope of Work definition
- KPI readiness check
- Delivery status classification
- Late delivery and negative review analysis
- Delay bucket analysis
- Product, weight, and dimension checks
- Approval-to-carrier timing analysis
- Seller-origin and São Paulo follow-up analysis
- Final interactive dashboard for São Paulo city-level comparison

---

## Key Findings

The analysis showed that late deliveries were a minority of reviewed delivered orders, but they had a strong impact on customer dissatisfaction.

Main findings:

- Late deliveries represented around 6% of reviewed delivered orders
- Late orders generated a much higher negative review rate than early or on-time orders
- Delay severity analysis showed that short delays had high volume, while longer delays had stronger dissatisfaction severity
- Product category, weight, and dimensions did not show a strong explanatory pattern
- Late orders showed a higher average approval-to-carrier handoff time
- São Paulo emerged as the main follow-up area because of volume and seller-origin concentration

---

## Dashboard Extension

A final interactive Power BI dashboard was created as a learning extension.

The dashboard compares individual seller-origin cities in the São Paulo area against the overall São Paulo benchmark using metrics such as:

- Delivered reviewed orders
- Late delivery rate
- Negative review rate
- Average approval-to-carrier days
- Follow-up priority

This dashboard is intended for exploratory follow-up, not root-cause confirmation.

---

## Limitations

The analysis identifies strong associations, but it does not confirm the root cause of delivery delays or negative reviews.

Root cause confirmation would require additional operational data, such as:

- Exact seller/store locations
- Seller or warehouse mapping
- Carrier used per order
- Pickup, dispatch, and actual handoff timestamps
- Operational clusters or logistics hubs
- Capacity, backlog, staffing, and stock availability data

Because these data were not available, the project supports prioritization and follow-up investigation, not final operational decision-making.

---

## Tools & Methods

- SQL
- PostgreSQL
- Python
- Power BI
- Data quality validation
- KPI definition
- Relational data analysis
- Dashboard design
- Stakeholder-oriented reporting

---

## Notes

This project represents the most advanced stage of my current data analytics learning path.

Compared with the previous projects, it includes a more complete workflow: stakeholder clarification, data readiness validation, scope definition, SQL analysis, Power BI reporting, dashboard development, and explicit documentation of analytical limitations.
