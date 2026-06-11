# Data Ingestion and Management Pipeline

This repository houses a collection of scripts designed for the ingestion, transformation, and management of data from various operational sources (primarily Google Sheets) into a centralized Data Warehouse in Google BigQuery. The system automates data cleaning, validation, and loading for multiple projects, ensuring data consistency and availability for analysis and reporting.

---

## Badges

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-orange?style=for-the-badge&logo=google-cloud)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-API-green?style=for-the-badge&logo=google-sheets)
![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-red?style=for-the-badge&logo=pandas)
![Project Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

---

## Table of Contents

1.  [Project Overview](#1-project-overview)
2.  [System Architecture](#2-system-architecture)
    *   [Data Flow](#21-data-flow)
    *   [Key Components](#22-key-components)
3.  [Repository Structure](#3-repository-structure)
4.  [Environment Setup](#4-environment-setup)
    *   [Operating System Level Dependencies](#41-operating-system-level-dependencies)
    *   [Python Dependencies](#42-python-dependencies)
    *   [Environment Variables](#43-environment-variables)
    *   [Google Cloud Authentication](#44-google-cloud-authentication)
5.  [Core Logic and Pipeline](#5-core-logic-and-pipeline)
    *   [Data Ingestion Scripts (Upload)](#51-data-ingestion-scripts-upload)
    *   [Schema Validation Module (`validacion_dataframes.py`)](#52-schema-validation-module-validacion_dataframespy)
    *   [Historical Append Script (`Append_DATA_BQ.py`)](#53-historical-append-script-append_data_bqpy)
    *   [Data Profiling Scripts (`Limpieza_*.py`)](#54-data-profiling-scripts-limpieza_py)
    *   [Execution Orchestrator (`trigger.py`)](#55-execution-orchestrator-triggerpy)
6.  [Data Output Examples](#6-data-output-examples)
    *   [Clean DataFrame (Pre-BigQuery)](#61-clean-dataframe-pre-bigquery)
    *   [Historical Append Table in BigQuery](#62-historical-append-table-in-bigquery)
7.  [Business Value and Analytical Capabilities](#7-business-value-and-analytical-capabilities)
    *   [What is Displayed](#71-what-is-displayed)
    *   [What it Allows to Measure](#72-what-it-allows-to-measure)
    *   [What it Allows to Diagnose](#73-what-it-allows-to-diagnose)
    *   [What it Allows to Resolve](#74-what-it-allows-to-resolve)
    *   [What it Allows to Delimit](#75-what-it-allows-to-delimit)
    *   [What it Allows to Optimize](#76-what-it-allows-to-optimize)
    *   [What it Allows to Standardize](#77-what-it-allows-to-standardize)
    *   [What it Allows to Rethink](#78-what-it-allows-to-rethink)

---

## 1. Project Overview

This project automates the extraction, transformation, and loading (ETL) of data from Google Sheets into Google BigQuery. Its main objective is to consolidate operational information from multiple programs and projects (e.g., "Ecolombia 2.0", "Colsubsidio 2026", "Jóvenes a la E", "Suba es Oportunidad") into a structured and centralized format. This facilitates data analysis, report generation, and evidence-based decision-making, eliminating reliance on error-prone and slow manual processes.

---

## 2. System Architecture

The architecture is based on a micro-service (script) approach that interacts with Google Cloud APIs and data processing libraries.

### 2.1 Data Flow

The data pipeline follows a clear pattern:

1.  **Source**: Operational data resides in Google Sheets spreadsheets, managed by different project teams.
2.  **Extraction**: Python scripts use the Google Sheets API (`gspread`) to read the data.
3.  **Transformation**: `pandas` is used to perform cleaning operations, column name normalization, data type conversion, null value handling, and duplicate removal.
4.  **Validation**: A schema validation module compares the structure of the transformed DataFrame with the schema of the target table in BigQuery to prevent inconsistencies.
5.  **Loading**: Clean and validated data is loaded into specific Google BigQuery tables (`google-cloud-bigquery`).
6.  **Orchestration**: A `trigger.py` script coordinates the execution of all ingestion scripts.
7.  **Historical Append**: A dedicated script (`Append_DATA_BQ.py`) manages the creation of historical snapshots of certain tables in BigQuery.
8.  **Data Profiling**: Cleaning scripts (`Limpieza_*.py`) allow for inspecting the quality of data already loaded into BigQuery.

### 2.2 Key Components

*   **Google Sheets**: Primary data source.
*   **Google Cloud BigQuery**: Scalable, serverless Data Warehouse for data storage and analysis.
*   **Python Scripts**:
    *   **Ingestion Scripts (`Upload_*.py`, `Caracterizacion_*.py`, `Empleabilidad_*.py`, `Satisfaccion_*.py`, `CONVOCATORIA_*.py`, `UnificadoFormacion_*.py`)**: Responsible for extracting, cleaning, and loading data for each specific source.
    *   **`validacion_dataframes.py`**: Schema quality control module.
    *   **`Append_DATA_BQ.py`**: Manages the creation of historical tables.
    *   **`Limpieza_*.py`**: Data profiling scripts for BigQuery.
    *   **`trigger.py`**: Main orchestrator of the ingestion pipeline.
*   **`credenciales.json`**: Service account credentials file for Google Cloud authentication.
*   **`.env`**: File for secure management of environment variables (project IDs, datasets, spreadsheets).

---

## 3. Repository Structure

```
.
├── Append_DATA_BQ.py
├── CONVOCATORIA_ECOLOMBIA_2026.py
├── Caracterizacion Colsubsidio2026.py
├── Caracterizacion_ECO_2026.py
├── Caracterizacion_JAE_2026.py
├── Caracterizacion_Suba2026.py
├── Empleabilidad_ECO.py
├── Empleabilidad_JAE_2026_V1.0.py
├── Empleabilidad_Suba2026.py
├── Limpieza_caracterizacion.py
├── Limpieza_empleabilidad.py
├── Limpieza_satisfaccion.py
├── Limpieza_seguimiento.py
├── Satisfaccion_Colsubsidio2026.py
├── Satisfaccion_ECO.py
├── Satisfaccion_JAE_2026.py
├── Satisfaccion_Suba.py
├── UnificadoFormacion_Suba2026.py
├── Upload Colsubsidio2026.py
├── Upload Suba2026.py
├── Upload_ECO++_2026.py
├── Upload_JAE_2026.py
├── trigger.py
├── validacion_dataframes.py
├── credenciales.json
└── .env
```

---

## 4. Environment Setup

To run the scripts, it is necessary to set up the development and authentication environment.

### 4.1 Operating System Level Dependencies

This project does not require specific operating system-level dependencies beyond a standard Python installation. All necessary libraries are managed via `pip`.

### 4.2 Python Dependencies

The required Python libraries are listed below. It is recommended to use a virtual environment for their installation.

```bash
pip install pandas gspread google-cloud-bigquery python-dotenv
```

### 4.3 Environment Variables

An `.env` file is used to manage sensitive environment variables and project-specific configurations. This file **must not be versioned** in source control systems.

Create an `.env` file in the project root with the following format, replacing the example values with your own:

```dotenv
PROJECT_ID="your-gcp-project-id"
DATA_SET="your-bigquery-dataset-id"
Sheets_Convocatoria_ECO="google-sheet-id-for-ecolombia-convocatoria"
Sheets_Colsubsidio="google-sheet-id-for-colsubsidio"
Sheets_JAE="google-sheet-id-for-jae"
Sheets_Seguimiento_Suba="google-sheet-id-for-suba-seguimiento"
Sheets_ECO="google-sheet-id-for-ecolombia-seguimiento"
Data_suba_empleabilidad="google-sheet-id-for-suba-empleabilidad"
Sheets_Satisfaccion_Suba="google-sheet-id-for-suba-satisfaccion"
Data_looker_suba="google-sheet-id-for-suba-looker-data"
BQ_Caracterizacion="your-bigquery-dataset-id.your-bigquery-table-caracterizacion"
BQ_Empleabilidad="your-bigquery-dataset-id.your-bigquery-table-empleabilidad"
BQ_Satisfaccion="your-bigquery-dataset-id.your-bigquery-table-satisfaccion"
BQ_Seguimiento="your-bigquery-dataset-id.your-bigquery-table-seguimiento"
```

### 4.4 Google Cloud Authentication

This project uses a Google Cloud service account to authenticate with BigQuery and Google Sheets.

1.  **Create a Service Account**: In your Google Cloud project, create a service account.
2.  **Assign Roles**: Assign the necessary roles to the service account:
    *   `BigQuery Data Editor` (or `BigQuery Data Owner`) to write to BigQuery.
    *   `BigQuery Data Viewer` to read from BigQuery (for `Append_DATA_BQ.py` and `Limpieza_*.py`).
    *   `Editor` (or `Owner`) for Google Sheets and Google Drive (for `gspread` and sheet access).
3.  **Generate JSON Key**: Generate a JSON key for the service account.
4.  **Save File**: Rename the downloaded JSON file to `credenciales.json` and place it in the repository root. **This file must be treated as sensitive and should not be versioned.**

---

## 5. Core Logic and Pipeline

The project consists of several Python scripts, each with a specific function within the data pipeline.

### 5.1 Data Ingestion Scripts (Upload)

Scripts such as `CONVOCATORIA_ECOLOMBIA_2026.py`, `Caracterizacion_*.py`, `Empleabilidad_*.py`, `Satisfaccion_*.py`, `UnificadoFormacion_*.py`, and `Upload_*.py` are responsible for data ingestion.

**Common Logic:**

1.  **Configuration Loading**: They use `python-dotenv` to load environment variables (`PROJECT_ID`, `DATASET_ID`, `TABLE_ID`, `Sheets_ID`).
2.  **Authentication**: They establish connection with Google Sheets (`gspread`) and Google BigQuery (`google-cloud-bigquery`) using `credenciales.json`.
3.  **Extraction**: They read data from a specific Google Sheets spreadsheet.
4.  **Header Pre-processing**: They handle cases where headers might be in rows other than the first or contain empty cells.
5.  **Cleaning and Transformation (`pandas`)**:
    *   Removal of entirely empty rows and columns.
    *   Replacement of empty strings or whitespace with `None`/`NaN`.
    *   Removal of rows with null values in key columns (e.g., `Número de Documento`).
    *   **Column Name Normalization**: Robust process to standardize column names:
        *   Convert to lowercase.
        *   Replace spaces with underscores.
        *   Remove special characters and line breaks.
        *   Normalize Unicode characters (accents, ñ) to ASCII.
        *   Handle duplicate columns.
    *   **Data Type Conversion**: Explicit conversion of columns to numeric types (integers, floats), dates, or percentages as appropriate.
    *   Addition of a `proyecto` column to identify the data source.
6.  **Schema Validation**: They invoke the `validar_y_comparar` function from the `validacion_dataframes.py` module to ensure that the resulting DataFrame matches the schema of the target table in BigQuery.
7.  **Loading to BigQuery**: They use `client_bq.load_table_from_dataframe` with `write_disposition="WRITE_TRUNCATE"` to overwrite the target table in BigQuery, ensuring that the data is always up-to-date. `autodetect=True` allows BigQuery to infer column data types if an explicit schema is not specified.

**Example of Column Normalization (common code snippet):**

```python
DF.columns = (DF.columns
              .str.replace(" ","_")
              .str.normalize('NFKD')
              .str.encode('ascii', errors='ignore')
              .str.decode('utf-8')
              .str.lower()
              .str.replace(r"[\r\n]+", "", regex=True)
              .str.replace(r"[^a-z0-9_#]", "", regex=True)              
              )
```

### 5.2 Schema Validation Module (`validacion_dataframes.py`)

This module is fundamental for the pipeline's integrity. Before each load to BigQuery, it is invoked to compare the schema of the source DataFrame with the schema of the target table in BigQuery.

**Logic:**

1.  It attempts to retrieve the BigQuery table schema. If the table does not exist, the script stops.
2.  It compares the number of columns between the DataFrame and the BigQuery table.
3.  It compares column names (after sorting them) to identify discrepancies.
4.  If there are differences in quantity or names, it reports missing or extra columns and stops the execution of the loading script, thus preventing corrupt or incomplete data loads.

**Added Value:**
This module acts as a **schema quality guardian**, preventing costly errors in BigQuery that could arise from unexpected changes in the source spreadsheets. It allows **diagnosing** data structure issues at the source before they affect the Data Warehouse, **delimiting** the risk of inconsistencies and **standardizing** schema expectations.

### 5.3 Historical Append Script (`Append_DATA_BQ.py`)

This script is responsible for maintaining a historical record of certain tables in BigQuery.

**Logic:**

1.  It identifies tables in BigQuery that contain the word "unificado" (excluding "formacion" and "append").
2.  For each of these tables, it reads its content into a `pandas` DataFrame.
3.  It adds a `Fecha_Append` column with the `YYYY-MM` format (month and year of execution).
4.  It loads the resulting DataFrame into a BigQuery table with the `_APPEND` suffix (e.g., `SUBA_2026_UnificadoFormacion_APPEND`).
5.  It uses `write_disposition="WRITE_APPEND"` to append new records to the existing table, creating a history of the data over time.

**Added Value:**
It allows **measuring** data evolution over time, facilitating trend analysis and historical comparisons. It solves the need for data **periodization** without modifying the main transactional tables, and **standardizes** the process of capturing historical snapshots.

### 5.4 Data Profiling Scripts (`Limpieza_*.py`)

The scripts `Limpieza_caracterizacion.py`, `Limpieza_empleabilidad.py`, `Limpieza_satisfaccion.py`, and `Limpieza_seguimiento.py` are data quality diagnostic tools.

**Logic:**

1.  They connect to BigQuery and query a specific table (defined by a `BQ_*` environment variable).
2.  They load the data into a `pandas` DataFrame.
3.  They iterate over the DataFrame columns (excluding some identifier columns like 'Nombre', 'Documento', etc.).
4.  For each column, they print `value_counts()`, showing the distribution of unique values and the presence of nulls.

**Added Value:**
These scripts are crucial for **diagnosing** data quality issues in BigQuery tables. They allow analysts to quickly **identify** inconsistent values, input errors, unexpected patterns, or the prevalence of null values in critical columns. This facilitates the **optimization** of data collection processes and the **standardization** of quality criteria.

### 5.5 Execution Orchestrator (`trigger.py`)

This script acts as the main entry point for executing the data ingestion pipeline.

**Logic:**

1.  It scans the current directory to find all `.py` files.
2.  It maintains a list of `archivos_excluidos` (such as `trigger.py` itself, cleaning scripts, validation scripts, etc.) to avoid executing them directly.
3.  It iterates over the remaining scripts (`scripts_ejecutables`) and executes them one by one using `subprocess.run()`.
4.  It reports the success or failure of each execution.
5.  Finally, it summarizes whether the update was complete or if there were failures, listing the problematic scripts.

**Added Value:**
The `trigger.py` **automates** the sequential execution of ingestion scripts, **simplifying** pipeline operation. It allows **resolving** the complexity of executing multiple scripts manually and **standardizes** the data update process. Its failure reporting system helps to quickly **diagnose** any interruptions in the data flow.

---

## 6. Data Output Examples

### 6.1 Clean DataFrame (Pre-BigQuery)

This is an example of the DataFrame structure after cleaning and normalization by one of the ingestion scripts, just before being loaded into BigQuery.

```
   numero_de_documento  tipo_de_documento     nombre_completo  fecha_nacimiento  edad  genero  ...  estado_actual  fecha_actualizacion  proyecto
0            101234567                CC  Persona Uno Ejemplo        1990-01-15    34  Masculino  ...       Activo           2024-07-20  Ecolombia 2.0
1            209876543                TI  Persona Dos Ejemplo        2005-03-22    19  Femenino  ...       Inactivo           2024-07-19  Ecolombia 2.0
2            304567890                CC  Persona Tres Ejemplo       1988-11-01    35  Masculino  ...       Activo           2024-07-21  Ecolombia 2.0
```

### 6.2 Historical Append Table in BigQuery

Example of how a table in BigQuery would look after multiple executions of the `Append_DATA_BQ.py` script, showing the `Fecha_Append` column.

```sql
-- Example table: `your-gcp-project-id.your-bigquery-dataset-id.ECOPLUS_2026_CONVOCATORIA_APPEND`

SELECT
    numero_de_documento,
    nombre_completo,
    estado_actual,
    fecha_actualizacion,
    proyecto,
    fecha_append
FROM
    `your-gcp-project-id.your-bigquery-dataset-id.ECOPLUS_2026_CONVOCATORIA_APPEND`
LIMIT 5;
```

| numero_de_documento | nombre_completo     | estado_actual | fecha_actualizacion | proyecto      | fecha_append |
| :------------------ | :------------------ | :------------ | :------------------ | :------------ | :----------- |
| 101234567           | Persona Uno Ejemplo | Activo        | 2024-07-20          | Ecolombia 2.0 | 2024-07      |
| 209876543           | Persona Dos Ejemplo | Inactivo      | 2024-07-19          | Ecolombia 2.0 | 2024-07      |
| 101234567           | Persona Uno Ejemplo | Activo        | 2024-08-20          | Ecolombia 2.0 | 2024-08      |
| 209876543           | Persona Dos Ejemplo | Activo        | 2024-08-19          | Ecolombia 2.0 | 2024-08      |
| 304567890           | Persona Tres Ejemplo| Activo        | 2024-08-21          | Ecolombia 2.0 | 2024-08      |

---

## 7. Business Value and Analytical Capabilities

This data pipeline is not just a technical solution; it is a strategic tool that enhances business intelligence and project management.

### 7.1 What is Displayed

The system consolidates and presents a unified view of operational data from multiple programs. This includes:
*   **Characterization Data**: Demographic, socioeconomic, and educational profiles of participants.
*   **Call and Follow-up Data**: Information on the registration process, participant status in program phases, and training progress.
*   **Employability Data**: Tracking of applications, referrals, job placements, and insertion outcomes.
*   **Satisfaction Data**: Participant feedback on the quality of programs and services.
*   **Historical Data**: Monthly snapshots of the evolution of key indicators.

### 7.2 What it Allows to Measure

*   **Program Effectiveness**: Conversion rates in calls, training completion rates, employability rates.
*   **Social Impact**: Number of beneficiaries, profiles of served population, improvement in employability conditions.
*   **Operational Performance**: Cycle times in processes, efficiency in participant management.
*   **User Satisfaction**: Net Promoter Score (NPS), satisfaction levels with different program components.
*   **Temporal Evolution**: Trends in all indicators over time, thanks to historical appends.

### 7.3 What it Allows to Diagnose

*   **Bottlenecks**: Identify program phases with low retention or conversion.
*   **Data Quality Issues**: Detect inconsistencies, outliers, or missing data in original sources (Google Sheets) through profiling and validation scripts.
*   **Data Collection Inefficiencies**: Point out areas where manual data entry is prone to errors or ambiguities.
*   **Deviations from Plan**: Compare actual progress with established objectives for each program.
*   **Training Needs**: Identify gaps in participant skills or in the training offer.

### 7.4 What it Allows to Resolve

*   **Information Silos**: Unify dispersed data from multiple spreadsheets into a single Data Warehouse.
*   **Data Inconsistencies**: Apply standardized cleaning and normalization rules to ensure consistency.
*   **Reporting Delays**: Automate data ingestion, reducing preparation time for analysis.
*   **Decisions Based on Obsolete Data**: Provide updated and validated data regularly.
*   **Human Errors**: Minimize manual intervention in the ETL process.

### 7.5 What it Allows to Delimit

*   **Data Quality Risks**: Schema validation and data profiling limit the entry of erroneous or poorly structured information.
*   **Ambiguity in Definitions**: Column normalization and data type standardization delimit the interpretation of fields.
*   **Operational Costs**: Automation reduces the need for human resources dedicated to repetitive ETL tasks.
*   **Scope of Problems**: By quickly diagnosing failures, the impact of errors on the system can be delimited.

### 7.6 What it Allows to Optimize

*   **Reporting and Analysis Processes**: By having clean and structured data in BigQuery, the creation of dashboards and ad-hoc analyses is faster and more reliable.
*   **Resource Allocation**: Identify where resources (human, financial) are generating the greatest impact or where more are needed.
*   **Intervention Strategies**: Adjust training or employability programs based on participant performance and satisfaction.
*   **Participant Experience**: Improve touchpoints and services by better understanding user needs and feedback.
*   **Pipeline Efficiency**: The `trigger.py` orchestrator optimizes script execution, ensuring the process is robust and efficient.

### 7.7 What it Allows to Standardize

*   **Data Models**: Create a consistent and unified data model in BigQuery for all projects.
*   **ETL Processes**: Establish a uniform ingestion, cleaning, and loading pipeline for new data sources.
*   **Metrics and Indicators**: Define key metrics consistently across all programs, allowing for meaningful comparisons.
*   **Data Quality**: Implement a set of cleaning and validation rules that are applied homogeneously.
*   **Documentation and Governance**: By having an automated and well-defined process, data documentation and governance are facilitated.

### 7.8 What it Allows to Rethink

*   **Data Collection Strategies**: By identifying recurring issues in sources, how information is collected from the origin can be rethought.
*   **Program Design**: Use generated insights to redesign or improve training and employability programs, making them more effective and aligned with market needs.
*   **Participant Interaction**: Rethink how beneficiaries are interacted with based on satisfaction and follow-up data.
*   **Data Infrastructure**: Evaluate the need for additional tools or architectural changes to support future growth.
*   **Data Culture**: Foster a culture where decisions are based on reliable and accessible data, transforming the organization into a more data-driven entity.