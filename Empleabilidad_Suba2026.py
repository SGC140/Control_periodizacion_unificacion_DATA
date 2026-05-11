import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from google.cloud import bigquery
from pathlib import Path

# ==============================
# CONFIGURACIÓN
# ==============================

SPREADSHEET_ID = "1INgwRBsVt2KDcS5xmOG6FGKModYTxBzCmwRgWsAPCRE"
RANGE = "A2:BE"

PROJECT_ID = "sustained-edge-465417-m3"
DATASET_ID = "EFE_2026"
TABLE_ID   = "SUBA_2026_Empleabilidad"

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

sheet = client_sheets.open_by_key(SPREADSHEET_ID).worksheet("Empleabilidad")
# ==============================
# LECTURA Y NORMALIZACIÓN ROBUSTA
# ==============================

data = sheet.get_all_values()

print(f"🔎 Total filas crudas: {len(data)}")

# headers
headers = data[1]

# limpiar nombres vacíos de columnas
headers = [h if h != "" else f"col_{i}" for i, h in enumerate(headers)]

num_cols = len(headers)

rows_fixed = []

for i, row in enumerate(data[2:]):

    # ignorar filas vacías reales
    if not any(cell.strip() for cell in row if cell):
        continue

    # 🔥 AJUSTE CLAVE (esto evita el error)
    row = (row + [None] * num_cols)[:num_cols]

    rows_fixed.append(row)

# 🔥 CREACIÓN SEGURA DEL DATAFRAME
df = pd.DataFrame(rows_fixed, columns=headers)

print(f"📥 Filas originales: {len(df)}")
print(f"📥 Columnas originales: {len(df.columns)}")

# ==============================
# NORMALIZAR NULOS (CLAVE)
# ==============================

import numpy as np

# Convertir strings vacíos o espacios a None
df = df.replace(r'^\s*$', None, regex=True)

# Convertir NaN a None (por compatibilidad con BigQuery)
df = df.where(pd.notnull(df), None)

# ==============================
# LIMPIEZA DE DATOS
# ==============================

# Eliminar filas completamente vacías

print(df.head)

df = df.dropna(how="all")


# Normalizar vacíos (espacios, strings vacíos)
df = df.replace(r'^\s*$', None, regex=True)

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
    .str.normalize('NFKD')
    .str.encode('ascii', errors='ignore')
    .str.decode('utf-8')
    .str.replace(r"[^a-z0-9_#]", "", regex=True) 
)

# Eliminar columnas sin nombre
df = df.loc[:, df.columns.notna()]
df = df.loc[:, df.columns != ""]

# Eliminar duplicadas
df = df.loc[:, ~df.columns.duplicated()]

df = df.dropna(subset=['documento_de_identidad'])


# Reemplazar nombres vacíos restantes
df.columns = [col if col != "" else f"col_{i}" for i, col in enumerate(df.columns)]

print(f"📊 Columnas finales: {len(df.columns)}")

# ==============================
# TIPOS DE DATOS (ANTI-ERRORES)
# ==============================

# Convertir todo a string para evitar errores de schema
df = df.astype(str)
df["total_remisiones"].apply(pd.to_numeric, errors='coerce')
df["total_contratación"].apply(pd.to_numeric, errors='coerce')
print(df["total_remisiones"])

# ==============================
# VALIDACIÓN FINAL
# ==============================

print(f"✅ Filas finales: {len(df)}")
print("🔎 Columnas:")
print(df.columns.tolist())
df['proyecto'] = 'Suba es Oportunidad'
print(df)

# ==============================
# CARGA A BIGQUERY
# ==============================

client_bq = bigquery.Client.from_service_account_json(CREDENTIALS_FILE)

table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

from validacion_dataframes import validar_y_comparar

print("Iniciando control de calidad de columnas")
validar_y_comparar(sheet.title, df, client_bq, table_ref)

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