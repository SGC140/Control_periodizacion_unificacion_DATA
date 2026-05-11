import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from google.cloud import bigquery
from pathlib import Path

# ==============================
# CONFIGURACIÓN
# ==============================

SPREADSHEET_ID = "14FAmBuo9RN642X8BQk2RT7j509CVY6tV8rWEbI-WbDU"

PROJECT_ID = "sustained-edge-465417-m3"
DATASET_ID = "EFE_2026"
TABLE_ID   = "SUBA_2026_V2"

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
# LEER DATOS DESDE SHEETS (ROBUSTO)
# ==============================

sheet = client_sheets.open_by_key(SPREADSHEET_ID).worksheet("BASE DE ATENCIÓN")

data = sheet.get_all_values()

print(f"🔎 Total filas crudas: {len(data)}")

# 👉 headers en fila 4 (índice 3)
headers = data[2]

# limpiar nombres vacíos de columnas
headers = [h if h != "" else f"col_{i}" for i, h in enumerate(headers)]

num_cols = len(headers)

rows_fixed = []

for row in data[3:]:  # datos desde fila 5

    # ignorar filas completamente vacías
    if not any(cell.strip() for cell in row if cell):
        continue

    # ajustar longitud de columnas
    row = (row + [None] * num_cols)[:num_cols]

    rows_fixed.append(row)

# ==============================
# CREAR DATAFRAME
# ==============================

df = pd.DataFrame(rows_fixed, columns=headers)

print(f"📥 Filas leídas: {len(df)}")
print(f"📥 Columnas leídas: {len(df.columns)}")

# ==============================
# NORMALIZAR NULOS (CLAVE)
# ==============================

df = df.replace(r'^\s*$', None, regex=True)
df = df.where(pd.notnull(df), None)

# ==============================
# ELIMINAR FILAS VACÍAS
# ==============================

df["_is_empty"] = df.isna().all(axis=1)

df_vacias = df[df["_is_empty"]]
df = df[~df["_is_empty"]].drop(columns="_is_empty")

print(f"🧹 Filas vacías eliminadas: {len(df_vacias)}")

# ==============================
# ELIMINAR COLUMNAS VACÍAS
# ==============================

cols_before = set(df.columns)
df = df.dropna(axis=1, how='all')
cols_after = set(df.columns)

print(f"🧹 Columnas eliminadas vacías: {len(cols_before - cols_after)}")

# ==============================
# LIMPIEZA DE NOMBRES DE COLUMNAS
# ==============================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace(" ", "_")
    .str.replace(r"[^\w]", "", regex=True)
    .str.lower()
)

# eliminar duplicadas
df = df.loc[:, ~df.columns.duplicated()]

print(f"📊 Columnas finales: {len(df.columns)}")

# ==============================
# VALIDACIÓN FINAL
# ==============================

print(f"✅ Filas finales: {len(df)}")
print("🔎 Columnas:")
print(df.columns.tolist())

print("🔎 Muestra de datos:")
print(df.head())

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