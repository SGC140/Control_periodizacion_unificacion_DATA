import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from google.cloud import bigquery
from pathlib import Path
import dotenv
from dotenv import load_dotenv
import os
# ==============================
# CONFIGURACIÓN
# ==============================

load_dotenv(override=True)

SPREADSHEET_ID = os.getenv("Sheets_Colsubsidio")
RANGE = "A:BZ"

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATA_SET")
TABLE_ID   = "COLSUBSIDIO_2026_Caracterizacion"

CREDENTIALS_FILE = "credenciales.json"

# ==============================
# AUTENTICACIÓN
# ==============================

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
client_sheets = gspread.authorize(creds)

# ==============================
# LEER DATOS DESDE SHEETS
# ==============================

sheet = client_sheets.open_by_key(SPREADSHEET_ID).worksheet("Caracterización")
data = sheet.get(RANGE)

headers = data[0]
rows = data[1:]

df = pd.DataFrame(rows, columns=headers)

print(f"📥 Filas originales: {len(df)}")
print(f"📥 Columnas originales: {len(df.columns)}")

# ==============================
# LIMPIEZA DE DATOS
# ==============================

# Eliminar filas completamente vacías
df = df.dropna(how="all")
df = df.dropna(subset=['Numero de documento'])

# Normalizar vacíos (espacios, strings vacíos)
df = df.replace(r'^\s*$', None, regex=True)

# Eliminar columnas completamente vacías
cols_before = set(df.columns)
df = df.dropna(axis=1, how='all')
cols_after = set(df.columns)

eliminadas = cols_before - cols_after
print(f"🧹 Columnas eliminadas vacías: {len(eliminadas)}")

# ==============================
# LIMPIEZA ROBUSTA DE COLUMNAS
# ==============================

# Limpiar nombres
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace(" ", "_")
    .str.replace(r"[^\w]", "", regex=True)
    .str.lower()
)

# Eliminar columnas sin nombre
df = df.loc[:, df.columns.notna()]
df = df.loc[:, df.columns != ""]

# Eliminar duplicadas
df = df.loc[:, ~df.columns.duplicated()]

# Reemplazar nombres vacíos restantes
df.columns = [col if col != "" else f"col_{i}" for i, col in enumerate(df.columns)]

print(f"📊 Columnas finales: {len(df.columns)}")

# ==============================
# TIPOS DE DATOS (ANTI-ERRORES)
# ==============================

# Convertir todo a string para evitar errores de schema
df = df.astype(str)

# ==============================
# VALIDACIÓN FINAL
# ==============================

print(f"✅ Filas finales: {len(df)}")
print("🔎 Columnas:")
print(df.columns.tolist())
df['proyecto'] = 'Colsubsidio 2026' 
print(df)

# ==============================
# CARGA A BIGQUERY
# ==============================

client_bq = bigquery.Client.from_service_account_json(CREDENTIALS_FILE)

table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

from validacion_dataframes import validar_y_comparar

print("Iniciando control de calidad de columnas")
validar_y_comparar(sheet, df, client_bq, table_ref)

job = client_bq.load_table_from_dataframe(
    df,
    table_ref,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
)

job.result()

print("🚀 Datos cargados exitosamente en BigQuery")