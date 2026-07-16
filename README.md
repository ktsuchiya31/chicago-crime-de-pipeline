# Chicago Crime DE Pipeline

End-to-end data engineering project built with Python, Apache Airflow, AWS S3, AWS Redshift Serverless, dbt Core, and Power BI.

## Architecture
Chicago Data Portal → Python → Airflow → S3 → Redshift → dbt → Power BI

## Stack
- Orchestration: Apache Airflow (Astro CLI + Docker)
- Storage: AWS S3
- Warehouse: AWS Redshift Serverless
- Transformation: dbt Core
- Visualization: Power BI
- CI/CD: GitHub Actions

## Setup
1. Clone the repo
2. Install Astro CLI
3. Run `astro dev start`
4. Open localhost:8080

## Dataset

Source: Chicago Data Portal — Crimes 2001 to Present
URL: https://data.cityofchicago.org/resource/ijzp-q8t2.json

- 100,000 rows, 22 columns
- Date range: 2025-2026
- Top crime types: Theft, Battery, Criminal Damage, Assault, Motor Vehicle Theft
- Top districts: 12, 8, 2, 6, 1
- Nulls: location_description (481), latitude/longitude (72), community_area (2)
- Columns to cast in dbt: latitude, longitude, x_coordinate, y_coordinate, year → numeric
- Columns to drop in dbt: location (redundant with lat/long)