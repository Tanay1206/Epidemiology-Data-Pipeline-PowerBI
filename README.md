Epidemiological COVID-19 Surveillance Pipeline 🦠📊

An end-to-end data engineering and analytics pipeline built to extract, process, and visualize historical epidemiological data. This project demonstrates the integration of Python-based data extraction, relational database architecture (SQL), and advanced business intelligence dashboarding (Power BI) to derive actionable healthcare insights.

🛠️ Tech Stack & Architecture

Data Extraction & Cleaning: Python (pandas, requests)

Database Management: SQLite (Relational Star Schema)

Data Visualization & Analytics: Power BI (DAX, UI/UX Design)

⚙️ The Pipeline Workflow

Extraction (ETL): Python script automatically requests raw, unstructured COVID-19 daily metrics from a public health API.

Transformation: Data is cleaned using pandas. Dates are formatted, null values are handled, and only core epidemiological metrics (Cases, Deaths, Hospitalizations) are isolated.

Loading (SQL): The cleaned data is pushed into a local SQLite database, meticulously organized into a Star Schema with a 1-to-Many relationship:

Dim_Location (Dimension table mapping State Codes)

Fact_Outbreak (Fact table storing daily numerical metrics)

Visualization: The relational database is imported into Power BI to build an interactive, high-tech command center.

📈 Dashboard Features

Custom DAX Measures: Calculates dynamic Case Fatality Rate (CFR) on the fly based on user filtering.

Geospatial Mapping: Utilizes Bing Maps to plot outbreak hot spots across the United States.

Timeline Slicer: Allows users to filter the entire dashboard by specific chronological windows (e.g., Summer 2020 peaks).

Premium UI/UX: Designed with "Elevation" principles, utilizing a dark charcoal theme, glowing neon accents, and clean data-ink ratios to mimic professional laboratory monitors.

🚀 How to View the Project

Download the Epidemiology-Data-Pipeline-PowerBI.pbix file from this repository.

Open the file using Microsoft Power BI Desktop.

Use the timeline slider at the top right to interact with the data!

Built by Tanay Singh - Bridging Biotechnology and Data Analytics.