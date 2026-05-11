import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from google.cloud import bigquery
from pathlib import Path

# ==============================
# CONFIGURACIÓN
# ==============================

SPREADSHEET_ID = "1zqDSWTc0iU9EFppUPXJgdfQNUG0E3LoVE3vvOr8X4FQ"
RANGE = "A5:BP"

PROJECT_ID = "sustained-edge-465417-m3"
DATASET_ID = "EFE_2026"
TABLE_ID   = "COLSUBSIDIO_2026_APPEND_V2"

CREDENTIALS_FILE = Path("C:/Users/User/Documents/VSC/ProyectDash/credenciales.json")

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

sheet = client_sheets.open_by_key(SPREADSHEET_ID).sheet1
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
# AGREGAR FECHA DE CARGA 🔥
# ==============================

df["fecha_carga"] = pd.Timestamp.now()

# ==============================
# VALIDACIÓN FINAL
# ==============================

print(f"✅ Filas finales: {len(df)}")
print("🔎 Columnas:")
print(df.columns.tolist())

# ==============================
# CARGA A BIGQUERY
# ==============================

client_bq = bigquery.Client.from_service_account_json(CREDENTIALS_FILE)

table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

job = client_bq.load_table_from_dataframe(
    df,
    table_ref,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True
    )
)

job.result()

print("🚀 Datos cargados exitosamente en BigQuery")