# LA Crimes Analysis (2020–2024)

## Project Objective

The objective of this project was to analyze reported crime incidents in Los Angeles from 2020 to 2024 in order to support high-level public safety prioritization.

The stakeholder wanted to understand:

- Which areas of the city were most affected by reported crimes
- Which crime categories were most frequent
- Whether meaningful patterns existed between victim age, victim sex, and weapon usage
- How crime levels evolved over time

---

## Dataset

The dataset contains crime incident records from Los Angeles, including:

- Reported date and occurrence date
- Crime codes and crime descriptions
- Weapon codes and weapon descriptions
- Victim age and victim sex
- Geographic coordinates
- Police area and area name
- Street/location information
- General incident location context

---

## Data Quality and Preparation

A significant part of the project focused on preparing and validating the dataset before analysis.

Main checks and preparation steps included:

- Date parsing and time normalization
- Duplicate incident checks
- Missing value analysis
- Validation of victim age anomalies
- Recoding of unclear victim sex categories
- Geographic coordinate validation
- Recovery of missing geographic coordinates where possible
- Selection of relevant fields for analysis

The original dataset was preserved, while cleaned and prepared outputs were created for analysis and visualization.

---

## Geographic Analysis Approach

One of the main challenges was the geographic visualization of crime concentration.

The available coordinates covered a very large portion of Los Angeles, and plotting every individual crime incident or using a dense heatmap created excessive visual noise.

For this reason, the final visualization used a more aggregated, area-oriented approach to support high-level geographic prioritization rather than exact hotspot detection.

This approach helps identify areas with higher crime concentration while avoiding misleading precision.

---

## Key Findings

The analysis showed that:

- Crime incidents were concentrated in a limited number of major categories
- Vehicle theft, simple assault, and burglary from vehicle were among the most frequent crime types
- Some areas showed higher reported crime volumes than others
- Crime levels appeared relatively stable across most of the 2020–2023 period
- The most recent 2024 data required caution because of possible delayed reporting
- Weapon-related patterns were mainly concentrated around common categories such as bodily force and other frequently recorded weapon types

---

## Tools & Methods

- Python (Pandas)
- Data cleaning and preprocessing
- Exploratory data analysis
- Geographic data validation
- Power BI dashboard development
- Data visualization and stakeholder-oriented reporting

---

## Limitations

This project does not define operational policing decisions or specific intervention strategies.

The analysis supports geographic and crime-category prioritization, but final operational decisions would require additional context from public safety teams, local knowledge, staffing constraints, and operational planning data.

---

## Notes

This project represents a more structured stage of my data analytics learning path, with stronger focus on data quality, stakeholder scope, geographic interpretation, and Power BI visualization.
